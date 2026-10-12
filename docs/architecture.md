# Arquitetura do HAC

```text
Home Assistant
  └─ custom_components/tcl_ac_local/
       config_flow   → discovery LAN / manual (sem cloud)
       protocol      → UDP BroadLink/DNA + AES
       coordinator   → poll get_state ~30s
       climate       → power, mode, temp, fan, swing
       switch/select/sensor/binary_sensor → extras
```

Fluxo:

1. Config flow descobre AC (broadcast UDP / seed IP / scan /24) e autentica.
2. Guarda `host`, `mac`, `key`, `device_id` no config entry.
3. Coordinator chama `TclAcClient.get_state()` em executor.
4. Entidades leem o dict de estado e enviam `set` / `set_params`.

Sem credenciais TCL Home / Intelligent AC. Runtime 100% LAN.
