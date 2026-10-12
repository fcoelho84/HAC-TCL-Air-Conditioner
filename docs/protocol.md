# Protocolos

## Ativo (v0.2): cloud TCL Home

1. Login `https://pa.account.tcl.com/account/login?clientId=54148614`
2. `https://prod-center.aws.tcljd.com/v3/global/cloud_url_get`
3. Refresh tokens → Cognito + MQTT endpoint
4. Controle via AWS IoT (`boto3`)

Implementação: `custom_components/tcl_ac_local/tcl.py`, `session_manager.py`, `aws_iot.py`.

## Legado / paralelo: BroadLink DNA LAN

Alguns ACs TCL também falam UDP `:80` BroadLink/DNA (sem conta em runtime).  
Código arquivado em `.re/archive-broadlink/` e notas em `docs/reverse-engineering.md`.  
A integração ativa deste repo usa **conta TCL Home**.
