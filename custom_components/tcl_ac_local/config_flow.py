"""Config flow for TCL AC Local (LAN only, no cloud login)."""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import CONF_DEVICE_ID, CONF_DEVICES, CONF_KEY, CONF_MAC, DOMAIN
from .protocol import (
    TclAcClient,
    TclAcDevice,
    TclAcDiscovery,
    TclAcLockedError,
    authenticate_tcl_ac_device,
    discover_tcl_ac_devices,
)

CONF_SCAN_SUBNET = "scan_subnet"
CONF_SELECTION = "selection"
CONF_SETUP_METHOD = "setup_method"
CONF_SEED_HOSTS = "seed_hosts"
SETUP_METHOD_LOCAL_DISCOVERY = "local_discovery"
SETUP_METHOD_MANUAL = "manual"

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class LocalDiscoveryResult:
    """Devices found through LAN discovery."""

    devices: list[dict[str, Any]]
    locked_devices: list[TclAcDiscovery]


def _mac_unique_id(mac: str) -> str:
    return mac.replace(":", "").replace("-", "").lower()


def _manual_schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(CONF_NAME, default=defaults.get(CONF_NAME, "")): str,
            vol.Required(CONF_HOST, default=defaults.get(CONF_HOST, "")): str,
            vol.Required(CONF_MAC, default=defaults.get(CONF_MAC, "")): str,
            vol.Required(CONF_KEY, default=defaults.get(CONF_KEY, "")): str,
        }
    )


def _user_schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_SETUP_METHOD,
                default=defaults.get(CONF_SETUP_METHOD, SETUP_METHOD_LOCAL_DISCOVERY),
            ): vol.In(
                {
                    SETUP_METHOD_LOCAL_DISCOVERY: "Local discovery (recommended)",
                    SETUP_METHOD_MANUAL: "Manual setup",
                }
            )
        }
    )


def _local_discovery_schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Optional(CONF_SEED_HOSTS, default=defaults.get(CONF_SEED_HOSTS, "")): str,
            vol.Required(CONF_SCAN_SUBNET, default=defaults.get(CONF_SCAN_SUBNET, True)): bool,
        }
    )


def _select_schema(devices: list[dict[str, Any]]) -> vol.Schema:
    options = {
        device[CONF_MAC]: (
            f"{device[CONF_NAME]} ({device[CONF_MAC]}, {device.get(CONF_HOST) or 'no host'})"
        )
        for device in devices
    }
    return vol.Schema({vol.Required(CONF_SELECTION, default=list(options)): cv.multi_select(options)})


async def _validate_input(hass: HomeAssistant, data: dict[str, Any]) -> None:
    client = TclAcClient(
        TclAcDevice(
            host=data[CONF_HOST],
            mac=data[CONF_MAC],
            key=data[CONF_KEY],
            device_id=int(data.get(CONF_DEVICE_ID, 1)),
        )
    )
    await hass.async_add_executor_job(client.get_state)


async def _validate_devices(hass: HomeAssistant, devices: list[dict[str, Any]]) -> None:
    for device in devices:
        if not device.get(CONF_HOST):
            raise OSError("Could not find the device host on the LAN")
        await _validate_input(hass, device)


def _configured_macs(hass: HomeAssistant) -> set[str]:
    macs: set[str] = set()
    for entry in hass.config_entries.async_entries(DOMAIN):
        if CONF_DEVICES in entry.data:
            macs.update(_mac_unique_id(device[CONF_MAC]) for device in entry.data[CONF_DEVICES])
        elif entry.data.get(CONF_MAC):
            macs.add(_mac_unique_id(entry.data[CONF_MAC]))
    return macs


def _update_configured_host(hass: HomeAssistant, mac: str, host: str) -> bool:
    target_mac = _mac_unique_id(mac)
    for entry in hass.config_entries.async_entries(DOMAIN):
        if CONF_DEVICES in entry.data:
            changed = False
            devices: list[dict[str, Any]] = []
            found = False
            for device in entry.data[CONF_DEVICES]:
                updated = dict(device)
                if _mac_unique_id(updated[CONF_MAC]) == target_mac:
                    found = True
                    if updated.get(CONF_HOST) != host:
                        updated[CONF_HOST] = host
                        changed = True
                devices.append(updated)
            if found:
                if changed:
                    data = dict(entry.data)
                    data[CONF_DEVICES] = devices
                    hass.config_entries.async_update_entry(entry, data=data)
                return True
        elif entry.data.get(CONF_MAC) and _mac_unique_id(entry.data[CONF_MAC]) == target_mac:
            if entry.data.get(CONF_HOST) != host:
                data = dict(entry.data)
                data[CONF_HOST] = host
                hass.config_entries.async_update_entry(entry, data=data)
            return True
    return False


def _filter_unconfigured_devices(
    hass: HomeAssistant, devices: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    configured_macs = _configured_macs(hass)
    filtered: list[dict[str, Any]] = []
    seen_macs: set[str] = set()
    for device in devices:
        unique_mac = _mac_unique_id(device[CONF_MAC])
        if unique_mac in seen_macs:
            continue
        seen_macs.add(unique_mac)
        if unique_mac in configured_macs:
            if host := device.get(CONF_HOST):
                _update_configured_host(hass, device[CONF_MAC], host)
            continue
        filtered.append(device)
    return filtered


def _devices_unique_id(devices: list[dict[str, Any]], prefix: str) -> str:
    macs = ",".join(sorted(_mac_unique_id(device[CONF_MAC]) for device in devices))
    return prefix + "_" + hashlib.sha1(macs.encode()).hexdigest()[:16]


def _parse_seed_hosts(raw_hosts: str) -> list[str]:
    return [host for host in re.split(r"[\s,;]+", raw_hosts.strip()) if host]


def _locked_device_summary(devices: list[TclAcDiscovery]) -> str:
    return ", ".join(f"{device.name} ({device.mac}, {device.host})" for device in devices)


def _accountless_device_configs(seed_hosts: list[str], scan_subnet: bool) -> LocalDiscoveryResult:
    devices: list[dict[str, Any]] = []
    locked_devices: list[TclAcDiscovery] = []

    for discovery in discover_tcl_ac_devices(
        seed_hosts=seed_hosts,
        scan_subnet=scan_subnet,
    ):
        try:
            auth = authenticate_tcl_ac_device(discovery)
            client = TclAcClient(
                TclAcDevice(
                    host=discovery.host,
                    mac=discovery.mac,
                    key=auth.key,
                    device_id=auth.device_id,
                )
            )
            client.get_state()
        except TclAcLockedError:
            locked_devices.append(discovery)
            continue
        except Exception:  # noqa: BLE001
            continue

        devices.append(
            {
                CONF_NAME: discovery.name,
                CONF_HOST: discovery.host,
                CONF_MAC: discovery.mac,
                CONF_KEY: auth.key,
                CONF_DEVICE_ID: auth.device_id,
            }
        )

    return LocalDiscoveryResult(devices=devices, locked_devices=locked_devices)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for TCL AC Local."""

    VERSION = 1

    def __init__(self) -> None:
        self._discovered_device: dict[str, Any] | None = None
        self._local_devices: list[dict[str, Any]] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        if user_input is not None:
            if user_input[CONF_SETUP_METHOD] == SETUP_METHOD_MANUAL:
                return await self.async_step_manual()
            return await self.async_step_local_discovery()
        return self.async_show_form(step_id="user", data_schema=_user_schema(user_input), errors={})

    async def async_step_dhcp(self, discovery_info: Any) -> config_entries.ConfigFlowResult:
        host = getattr(discovery_info, "ip", None)
        if not host:
            return self.async_abort(reason="not_supported")

        result = await self.hass.async_add_executor_job(
            _accountless_device_configs,
            [str(host)],
            False,
        )
        devices = result.devices
        if not devices:
            if result.locked_devices:
                for locked_device in result.locked_devices:
                    if _update_configured_host(self.hass, locked_device.mac, locked_device.host):
                        return self.async_abort(reason="already_configured")
                return self.async_abort(reason="locked_device")
            return self.async_abort(reason="not_supported")

        device = devices[0]
        if _update_configured_host(self.hass, device[CONF_MAC], device[CONF_HOST]):
            return self.async_abort(reason="already_configured")

        await self.async_set_unique_id(_mac_unique_id(device[CONF_MAC]))
        self._abort_if_unique_id_configured(updates={CONF_HOST: device[CONF_HOST]})
        self._discovered_device = device
        self.context["title_placeholders"] = {
            CONF_NAME: device[CONF_NAME],
            CONF_HOST: device[CONF_HOST],
        }
        return await self.async_step_dhcp_confirm()

    async def async_step_dhcp_confirm(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        if self._discovered_device is None:
            return self.async_abort(reason="not_supported")

        errors: dict[str, str] = {}
        if user_input is not None:
            device = self._discovered_device
            await self.async_set_unique_id(_mac_unique_id(device[CONF_MAC]))
            self._abort_if_unique_id_configured(updates={CONF_HOST: device[CONF_HOST]})
            try:
                await _validate_devices(self.hass, [device])
            except Exception:  # noqa: BLE001
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=device[CONF_NAME],
                    data={CONF_DEVICES: [device]},
                )

        device = self._discovered_device
        return self.async_show_form(
            step_id="dhcp_confirm",
            description_placeholders={
                CONF_NAME: device[CONF_NAME],
                CONF_HOST: device[CONF_HOST],
                CONF_MAC: device[CONF_MAC],
            },
            errors=errors,
        )

    async def async_step_local_discovery(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                result = await self.hass.async_add_executor_job(
                    _accountless_device_configs,
                    _parse_seed_hosts(user_input.get(CONF_SEED_HOSTS, "")),
                    bool(user_input.get(CONF_SCAN_SUBNET, True)),
                )
            except Exception:  # noqa: BLE001
                _LOGGER.exception("LAN discovery failed")
                errors["base"] = "discovery_error"
            else:
                devices = _filter_unconfigured_devices(self.hass, result.devices)
                if not devices:
                    if result.locked_devices:
                        errors["base"] = "locked_device"
                    elif result.devices:
                        errors["base"] = "all_devices_configured"
                    else:
                        errors["base"] = "no_lan_devices"
                else:
                    self._local_devices = devices
                    return await self.async_step_select_local()

        return self.async_show_form(
            step_id="local_discovery",
            data_schema=_local_discovery_schema(user_input),
            errors=errors,
        )

    async def async_step_select_local(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            selected = user_input.get(CONF_SELECTION) or []
            devices = [device for device in self._local_devices if device[CONF_MAC] in selected]
            if not devices:
                errors["base"] = "no_devices_selected"
            else:
                try:
                    await _validate_devices(self.hass, devices)
                except Exception:  # noqa: BLE001
                    errors["base"] = "cannot_connect"
                else:
                    await self.async_set_unique_id(_devices_unique_id(devices, "local"))
                    return self.async_create_entry(
                        title="TCL AC Local",
                        data={CONF_DEVICES: devices},
                    )

        return self.async_show_form(
            step_id="select_local",
            data_schema=_select_schema(self._local_devices),
            errors=errors,
        )

    async def async_step_manual(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            device = {
                CONF_NAME: user_input[CONF_NAME],
                CONF_HOST: user_input[CONF_HOST],
                CONF_MAC: user_input[CONF_MAC],
                CONF_KEY: user_input[CONF_KEY],
                CONF_DEVICE_ID: 1,
            }
            try:
                await _validate_devices(self.hass, [device])
            except Exception:  # noqa: BLE001
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(_mac_unique_id(device[CONF_MAC]))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=device[CONF_NAME],
                    data={CONF_DEVICES: [device]},
                )

        return self.async_show_form(
            step_id="manual",
            data_schema=_manual_schema(user_input),
            errors=errors,
        )
