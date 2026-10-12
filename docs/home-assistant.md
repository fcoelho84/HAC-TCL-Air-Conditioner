# Home Assistant

## Instalar (HACS)

1. HACS → Custom repositories → este repo → Integration.
2. Download **TCL AC Local**.
3. Reinicie o HA.
4. Settings → Devices & services → Add → **TCL AC Local**.

## Setup

Preferir **Local discovery**.

Opcional: IPs seed e scan de subnet se o broadcast for filtrado.

HA e o AC precisam estar na mesma L2/L3 com UDP `:80` liberado.

## Manual

Se já tiver MAC + chave (32 hex) + IP: **Manual setup**.

## Entidades

| Plataforma | Uso |
|------------|-----|
| `climate` | modo, temp, fan, swing, on/off |
| `switch` | turbo, eco, quiet, display, … |
| `select` | opções de airflow detalhadas |
| `sensor` | outdoor / coil / vent / erros |
| `binary_sensor` | diagnósticos |

## Limitações

- Só módulos BroadLink/DNA (`devtype` `0x507C` no discovery).
- AC “só MQTT / Matter” no TCL Home pode não responder.
- Dispositivo `LOCKED` bloqueia auth local.
