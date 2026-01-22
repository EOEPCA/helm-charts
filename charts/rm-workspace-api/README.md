# Workspace API & UI Layer Helm Chart

## Quick Install

e.g.
```bash
helm upgrade --install rm-workspace-api rm-workspace-api
    --repo https://eoepca.github.io/helm-charts
    --version 2.0.0
    --namespace workspace
    --create-namespace
    --set prefixForName="ws"
    --set endpoint="https://minio.develop.eoepca.org"
    --set region="eoepca-demo"
    --set forwardedAllowIps="true"
    --set sessionMode="on"
    --set useVcluster="true"
    --set gunicornWorkers="5"
    --set uiMode="ui"
```

## Values ↔︎ Env/Runtime

| Helm value | Possible values | Maps to (env/runtime) |
|---|---|---|
| `gunicornWorkers` | positive integer (e.g. `1`, `3`, `8`) | `GUNICORN_WORKERS` |
| `prefixForName` | DNS-1123 prefix (`[a-z0-9]([-a-z0-9]*[a-z0-9])?`) | `PREFIX_FOR_NAME` |
| `useVcluster` | `true` \| `false` | `USE_VCLUSTER` |
| `sessionMode` | `auto` \| `on` \| `off` | `SESSION_MODE` |
| `endpoint` | URL (`https://…`) or empty | `ENDPOINT` |
| `region` | AWS region code (e.g. `eu-central-1`) or empty | `REGION` |
| `uiMode` | `ui` \| `no` | `UI_MODE` |
| `forwardedAllowIps` | `""` \| `"*"` \| comma-sep CIDRs | `FORWARDED_ALLOW_IPS`, `GUNICORN_CMD_ARGS=--forwarded-allow-ips=…` |
| `extraEnv` | list of `{name: ..., value: ...}` | extra container env |
