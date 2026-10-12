# Reverse engineering — TCL Home 7.1.0

## Artefatos

| Artefato | Origem |
|----------|--------|
| `TCL+Home_7.1.0_APKPure.xapk` | Downloads |
| `com.tcl.tclhome.apk` | base split (`package_name=com.tcl.tclhome`, version `7.1.0` / `70100045`) |
| `config.armeabi_v7a.apk` | native libs (`libapp.so` Flutter AOT, `libCHIPController.so` Matter, …) |

Ferramentas: REA MCP (`open_binary` + Ghidra 12.1.4 em `libapp.so`), JADX CLI 1.5.3 no DEX, strings/binários no APK.

JADX MCP (`REA_JADX_MCP_JAR`) foi preparado em `.re/tools/`; o servidor MCP já em execução precisa ser reconectado para usar `inspect_android_*` via REA.

## Observações (estáticas)

### Identidade BroadLink no app

Classe decompilada:

`com.tcl.libiotbase.module.iot.bean.BroadLinkDeviceInfo`

Campos: `mac`, `did`, `pid`, `cookie`, `timezone`, `productKey`, `devType`.

String de recurso: `iot_string_broadlink_ac`.

DEX também contém `getLocalkey` / `setLocalkey` / `localkey` e log `readLocalKey [key = `.

### Flutter (`libapp.so`)

Strings (Ghidra `search_strings` / `strings`):

- `_createLocalController@…`
- `LocalKey`
- família MQTT (`MqttPropertyEngine`, `bindMqtt`, `deviceMqttEndpoint`, …)
- propriedades AC UI (`targetTemperature`, `workMode`, `isPowerOn`, …)

**Inferência:** runtime do app mistura **MQTT cloud** (controle “oficial” na UI Flutter) com um caminho **local** (`LocalKey` / `_createLocalController`) alinhado a dispositivos BroadLink/DNA.

### Framing DNA no DEX

Bytes `a5a55a5a` (inner magic DNA) presentes em `classes20.dex`.

Chave AES inicial BroadLink e IV **não** aparecem como ASCII hex neste build; implementação de pacote tende a estar em binário ofuscado / SDK nativo. Constantes de wire usadas no HAC vêm do protocolo BroadLink/DNA público e da integração MIT testada em ACs TCL (ver `protocol.md`).

### O que isto **não** prova

- Não houve captura de tráfego LAN neste trabalho.
- Não se afirma que **todo** AC no TCL Home use BroadLink; Matter (`libCHIPController`) e MQTT são caminhos paralelos.
- Modelos só-cloud (sem módulo DNA) não respondem a UDP `:80` BroadLink.

## Conclusão para o HAC

Para controle **local sem login**, o caminho viável observado + corroborado é:

1. Descoberta BroadLink/DNA na LAN (UDP).
2. Auth `0x0065` → chave por dispositivo.
3. Get/set `0x006A` com corpo JSON (`pwr`, `temp`, `tcl_mode`, …).

Detalhe do wire: [`protocol.md`](protocol.md).
