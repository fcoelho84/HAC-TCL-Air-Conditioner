# Protocolo local BroadLink / DNA (TCL AC)

Transporte: **UDP porta 80**.

Criptografia: **AES-128-CBC**  
IV: `562e17996d093d28ddb3ba695a2e6f58`  
Chave inicial (auth): `097628343fe99e23765c1513accf8b02`  
Checksum: soma `0xBEAF` (16-bit).

Magic externo: `5aa5aa555aa5aa55`  
Magic interno: `a5a55a5a` (também visto no DEX do TCL Home 7.1.0)  
Device type testado: `0x507C`

## Auth (sem conta)

1. Discovery BroadLink → host, MAC, `devtype`, flag locked.
2. Comando `0x0065`, payload `0x50` bytes, criptografado com chave inicial.
3. Resposta: device id (u32 LE) + chave de 16 bytes (hex 32 chars).
4. Se `LOCKED`, auth falha (`0xffff`).

## Controle

Comando `0x006A`. Corpo interno JSON:

| Ação | Byte ação | Body |
|------|-----------|------|
| get | `1` | `{}` |
| set | `2` | `{ "param": value, ... }` |

### Parâmetros usados pelo climate

| Campo | Significado |
|-------|-------------|
| `pwr` | 0/1 power |
| `temp` | setpoint ×10 °C |
| `envtemp` | temperatura ambiente |
| `tcl_mode` | 1 heat, 2 dry, 3 cool, 4 fan, 5 auto |
| `tcl_mark` | fan speed |
| `tcl_vdir` / `tcl_hdir` | swing vertical / horizontal |

Extras (switches): `pwfmode`, `ecomode`, `qtmode`, `bglight`, `beep`, `ac_health`, …

Implementação: `custom_components/tcl_ac_local/protocol.py`.

## Evidência / atribuição

- RE TCL Home 7.1.0: `docs/reverse-engineering.md`
- Wire format / cliente: derivado de [jestempablo/home-assistant-tcl-intelligent-ac](https://github.com/jestempablo/home-assistant-tcl-intelligent-ac) (MIT)
