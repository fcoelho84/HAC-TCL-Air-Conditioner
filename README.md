# HAC-TCL-Air-Conditioner

Integração Home Assistant (HACS) para ar-condicionado TCL **na LAN**, sem login cloud.

Protocolo: BroadLink/DNA (UDP `:80`, AES-128-CBC). RE do app **TCL Home 7.1.0** + wire format corroborado (MIT). Detalhes em [`docs/`](docs/).

## Instalar via HACS

1. HACS → ⋮ → **Custom repositories**
2. Repository: URL deste repo
3. Category: **Integration**
4. Add → procure **TCL AC Local** → Download
5. Reinicie o Home Assistant
6. Settings → Devices & services → Add → **TCL AC Local**

HA e o AC na mesma rede. UDP porta **80** precisa passar.

## Uso

1. Escolha **Local discovery** (recomendado) ou **Manual setup**.
2. Selecione os ACs autenticados.
3. Controle via `climate.*` (modo, temperatura, fan, swing).

Sem conta TCL Home / Intelligent AC. A chave local sai da auth BroadLink na LAN.

## Protocolo (resumo)

| Ação | Como |
|------|------|
| Descobrir | UDP BroadLink (broadcast / multicast / seed IP) |
| Autenticar | cmd `0x0065` → chave por dispositivo |
| Ler / escrever | cmd `0x006A` + JSON (`pwr`, `temp`, `tcl_mode`, …) |

## Docs

| Arquivo | Conteúdo |
|---------|----------|
| [`docs/reverse-engineering.md`](docs/reverse-engineering.md) | RE do APK TCL Home |
| [`docs/protocol.md`](docs/protocol.md) | Wire protocol |
| [`docs/architecture.md`](docs/architecture.md) | Arquitetura do HAC |
| [`docs/home-assistant.md`](docs/home-assistant.md) | Runtime HA |

## Estrutura HACS

```text
hacs.json
custom_components/tcl_ac_local/
docs/
README.md
```

Domain: `tcl_ac_local` · versão: `0.1.0`

## Limitações

- Alvo: ACs com módulo BroadLink/DNA (`0x507C`).
- Unidades só MQTT/Matter no TCL Home podem não responder.
- Dispositivo com lock BroadLink bloqueia auth local.

## Créditos

Cliente de protocolo e mapeamento de parâmetros derivados de [jestempablo/home-assistant-tcl-intelligent-ac](https://github.com/jestempablo/home-assistant-tcl-intelligent-ac) (MIT). RE e empacotamento local-only neste repo.
