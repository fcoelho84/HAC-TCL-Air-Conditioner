# HAC-TCL-Air-Conditioner

Integração Home Assistant (HACS) para ar-condicionado via **conta TCL Home**.

Login com e-mail/telefone + senha do app → API cloud + AWS IoT → entidades `climate.*` (e extras).

Baseado no RE do app TCL Home e no stack MIT de [nemesa/ha-tcl-home-unofficial-integration](https://github.com/nemesa/ha-tcl-home-unofficial-integration).

## Instalar via HACS

1. HACS → ⋮ → **Custom repositories**
2. Repository: URL deste repo
3. Category: **Integration**
4. Add → **TCL AC Local** → Download
5. Reinicie o Home Assistant
6. Settings → Devices & services → Add → **TCL AC Local**

## Uso

1. Informe **e-mail/telefone** e **senha** do TCL Home.
2. Confirme URLs do app (deixe o padrão).
3. Os ACs da conta entram como `climate` / switches / sensors.

Recomendado: conta secundária com dispositivos compartilhados (evita risco de ban).

## Como funciona

| Etapa | O quê |
|-------|--------|
| Login | `pa.account.tcl.com` (mesmo do app) |
| Cloud | `prod-center.aws.tcljd.com` → tokens / MQTT endpoint |
| Controle | AWS IoT (boto3) — power, modo, temp, fan, … |

Internet necessária. Não é LAN BroadLink puro.

## Docs

| Arquivo | Conteúdo |
|---------|----------|
| [`docs/home-assistant.md`](docs/home-assistant.md) | Instalação / uso |
| [`docs/architecture.md`](docs/architecture.md) | Fluxo conta → cloud → entidades |
| [`docs/reverse-engineering.md`](docs/reverse-engineering.md) | RE do APK |
| [`docs/protocol.md`](docs/protocol.md) | Notas BroadLink LAN (legado / paralelo) |

## Estrutura

```text
hacs.json
custom_components/tcl_ac_local/
docs/
README.md
```

Domain: `tcl_ac_local` · versão: `0.2.0`

## Créditos

Cloud/login/AWS IoT: [nemesa/ha-tcl-home-unofficial-integration](https://github.com/nemesa/ha-tcl-home-unofficial-integration) (MIT, András Nemes).  
Login base: [DavidIlie/tcl-home-ac](https://github.com/DavidIlie/tcl-home-ac).
