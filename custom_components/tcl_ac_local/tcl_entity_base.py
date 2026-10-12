"""."""

import re

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .coordinator import IotDeviceCoordinator
from .device import Device, toDeviceInfo


def type_to_translation_key(entity_type: str) -> str:
    key = entity_type.replace(".", "_")
    key = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "_", key)
    return key.lower()


class TclEntityBase(CoordinatorEntity):
    def __init__(
        self, coordinator: IotDeviceCoordinator, type: str, name: str, device: Device
    ) -> None:
        super().__init__(coordinator)
        self.device = device
        self.type = type
        self._attr_has_entity_name = True
        self._attr_translation_key = type_to_translation_key(type)
        self._attr_name = None
        self._attr_unique_id = f"{DOMAIN}-{type}-{device.device_id}"

    @callback
    def _handle_coordinator_update(self) -> None:
        self.device = self.coordinator.get_device_by_id(self.device.device_id)
        self.async_write_ha_state()

    @property
    def unique_id(self) -> str:
        return self._attr_unique_id

    @property
    def device_info(self) -> DeviceInfo:
        return toDeviceInfo(self.device)

    @property
    def state_class(self) -> str | None:
        return None

    @property
    def available(self) -> bool:
        return self.device.is_online == 1


class TclNonPollingEntityBase(Entity):
    def __init__(self, type: str, name: str, device: Device) -> None:
        super().__init__()
        self.device = device
        self.type = type
        self._attr_has_entity_name = True
        self._attr_translation_key = type_to_translation_key(type)
        self._attr_name = None
        self._attr_unique_id = f"{DOMAIN}-{type}-{device.device_id}"

    @property
    def unique_id(self) -> str:
        return self._attr_unique_id

    @property
    def device_info(self) -> DeviceInfo:
        return toDeviceInfo(self.device)

    @property
    def state_class(self) -> str | None:
        return None
