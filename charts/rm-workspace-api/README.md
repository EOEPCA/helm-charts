# Workspace API & UI Layer Helm Chart

## Quick Install

e.g.
```bash
helm upgrade --install rm-workspace-api rm-workspace-api
    --repo https://eoepca.github.io/helm-charts
    --version 2.2.0
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
| `maxSessions` | positive integer (default `3`) | `MAX_SESSIONS` |
| `disableDockerRegistry` | `true` \| `false` | `DISABLE_DOCKER_REGISTRY` |
| `endpoint` | URL (`https://…`) or empty | `ENDPOINT` |
| `region` | AWS region code (e.g. `eu-central-1`) or empty | `REGION` |
| `uiMode` | `ui` \| `no` | `UI_MODE` |
| `frontendUrl` | base path in prod or absolute dev URL (default `/ui/management`) | `FRONTEND_URL` |
| `forwardedAllowIps` | `""` \| `"*"` \| comma-sep CIDRs | `FORWARDED_ALLOW_IPS`, `GUNICORN_CMD_ARGS=--forwarded-allow-ips=…` |
| `providerEnvironment` | provider environment name (e.g. `datalab`) | `PROVIDER_ENVIRONMENT` |
| `stores` | Comma-separated store names; empty disables stores | `STORES` |
| `disableStorage` | `true` \| `false` (default `false`) | `DISABLE_STORAGE` |
| `disableDatalab` | `true` \| `false` (default `false`) | `DISABLE_DATALAB` |
| `secretNamespaces` | Additional existing namespaces (default `[]`) | Secret-get Roles and RoleBindings |
| `authMode` | `gateway` \| `no` | `AUTH_MODE` |
| `authAudience` | JWT audience value when `AUTH_MODE=gateway` (default `workspace-api`) | `AUTH_AUDIENCE` |
| `authDebug` | `true` \| `false` | `AUTH_DEBUG` |
| `extraEnv` | list of `{name: ..., value: ...}` | extra container env |

## Kubernetes access

The API service account needs these permissions in the release namespace:

| API group | Resources | Verbs |
|---|---|---|
| `pkg.internal` | `datalabs`, `storages` | `get`, `list`, `create`, `patch`, `delete` |
| Core (`""`) | `secrets` | `get` |

The chart grants these permissions with a Role and RoleBinding. The API does
not read CRD definitions, PVCs, or ResourceQuotas. Provider controllers manage
child resources. No ClusterRole or ClusterRoleBinding is required.

Set `disableStorage` or `disableDatalab` to `true` to disable the corresponding
provider. Both default to `false`.

`stores` selects the API's supported store names. Its default is
`"postgres,redis,mongo"`. Set `stores: ""` to disable all stores. This value does
not inspect installed CRDs or operators. Install the required providers and
backing operators before use. Replace the old `disableStores` and
`disabledStoreTypes` settings with `stores`.

The API can read Secrets in the release namespace. Set `secretNamespaces` to
add Secret `get` access in other existing namespaces. The chart creates a Role
and RoleBinding in each unique namespace and skips the release namespace.
Each binding refers to the API service account in the release namespace,
including a custom `serviceAccount.name`. The chart does not create namespaces.
The installer must have permission to create these Roles and RoleBindings.
A connection or OAuth2 Secret read failure does not stop other reads.
