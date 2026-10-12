# Arquitetura

```text
HA config flow
  → username / password (TCL Home)
  → SessionManager.do_account_auth (pa.account.tcl.com)
  → cloud_url_get + refresh tokens (AWS Cognito / saas)
  → AwsIot.get_all_things
  → climate / switch / sensor / …
```

Runtime: **cloud polling** (`iot_class: cloud_polling`).  
HA precisa de internet. Credenciais ficam no config entry do HA.
