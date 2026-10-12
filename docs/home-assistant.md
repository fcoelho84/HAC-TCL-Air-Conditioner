# Home Assistant

## Setup

1. Add integration **TCL AC Local**.
2. Digite conta TCL Home (e-mail/telefone + senha).
3. Deixe URLs padrão.
4. ACs da conta aparecem automaticamente.

## Dependências

O `manifest.json` instala: `boto3`, `PyJWT`.

## Conta

Use conta secundária e compartilhe os dispositivos no app TCL Home.

## Logs

```yaml
logger:
  logs:
    custom_components.tcl_ac_local: info
```
