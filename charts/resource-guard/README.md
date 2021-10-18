# HELM Chart for Resource Guard

This README describes how to install the Resource Guard in your Kubernetes cluster using `Helm`.

## Description

The Resource Guard provides protection of a _Resource Server_ by application of two sub-components:
* **UMA User Agent**<br>
  Integrates with nginx by providing an `auth_request` endpoint through which nginx reverse-proxy (ingress controller) can obtain authorization before proxying a request.
  Defers to the PEP for the policy enforcement. The UMA User Agent acts as a UMA client in its interactions with the PEP, and interfaces to the _Token Endpoint_ of the system _Authorization Server_ to follow the UMA flow.
* **Policy Enforcement Point (PEP)**<br>
  Integrates with the `uma-user-agent` by providing an `auth_request` endpoint through which the UMA User Agent can obtain authorization as a UMA client.
  The PEP integrates with the system _Authorization Server_ to engage in the UMA flow.

Both the UMA User Agent and the PEP offer an HTTP interface in accordance with the nginx module [`ngx_http_auth_request_module`](https://nginx.org/en/docs/http/ngx_http_auth_request_module.html). The authorization flow chains `nginx -> uma-user-agent -> pep`, as illustrated in the following sequence diagram.

![Nginx auth_request](https://raw.githubusercontent.com/EOEPCA/uma-user-agent/develop/uml/export/Nginx%20auth_request.png)

Thus the Resource Guard is deployed as a `uma-user-agent`/`pep-engine` pair that have been coherently configured to protect a given _Resource Server_. These are deployed as chart dependencies of the Resource Guard.

For more details on these sub-compoents see their respective documentation:
* Policy Enforcement Point (PEP) - `pep-engine`
  * Component: https://github.com/EOEPCA/um-pep-engine/wiki
  * Helm chart: https://github.com/EOEPCA/helm-charts/blob/main/charts/pep-engine/README.md
* UMA User Agent - `uma-user-agent`
  * Component: https://github.com/EOEPCA/uma-user-agent/blob/develop/README.md
  * Helm chart: https://github.com/EOEPCA/helm-charts/blob/main/charts/uma-user-agent/README.md

## Prerequisites

* A Kubernetes cluster. Tested with version `v1.18.10`.
* NGINX Ingress Controller deployed in cluster. Tested with chart version `ingress-nginx-2.11.1`, image `ingress-nginx/controller:v0.34.1`.

## Adding the Helm Repository

This step is required if you are installing the chart via the helm repository.

```sh
helm repo add eoepca https://eoepca.github.io/helm-charts
helm repo update
```

## Installing the Chart

To install the chart with the release name `my-resource-guard`:
```sh
helm install my-resource-guard eoepca/resource-guard -f my-values.yaml
```

This will deploy the release with default values, plus overrides from the file `my-values.yaml`.

## Upgrading the Chart

```sh
helm upgrade my-resource-guard eoepca/resource-guard -f my-values.yaml
```

## Configuration

The Resource Guard comprises only sub-chart dependencies, i.e. has no templates of its own. Thus, it is configured as values passthru to its subcharts, whose helm values are documented at:
* Policy Enforcement Point (PEP) - `pep-engine`<br>
  https://github.com/EOEPCA/helm-charts/blob/main/charts/pep-engine/README.md
* UMA User Agent - `uma-user-agent`<br>
  https://github.com/EOEPCA/helm-charts/blob/main/charts/uma-user-agent/README.md

Nevertheless, we detail in the following tables some parameters that are commonly specified.

### `global` Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| global.context | Textual identifier that is used to distinguish between instances | `generic` |
| global.clusterDomain | The fully-qualified domain of the Kubernetes cluster | `svc.cluster.local` |
| global.domain | The DNS domain of the deployment | `myplatform.eoepca.org` |
| global.pep | The name of the PEP instance | `pep-engine` |
| global.realm | Authorization realm | `eoepca` |
| global.ports.proxy-pep.port:<br>global.ports.proxy-pep.targetPort: | PEP authorization/proxy port | `port: 5566`<br>`targetPort: 5566` |
| global.ports.resource-pep.port:<br>global.ports.resource-pep.targetPort: | PEP resources API port | `port: 5576`<br>`targetPort: 5576` |
| global.nginxIp | IP address of the Nginx ingress controller | `10.0.2.15`<br>(minikube) |
| global.resourceServer.name<br>global.resourceServer.port | Connection details for target Resource Server | `name: myservice`<br>`port: 80` |
| global.certManager.clusterIssuer | The name of the `ClusterIssuer` instance for tls.<br>Leave blank for no TLS | `""` |


### `pep-engine` Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| pep-engine.configMap.asHostname | Authorization Server: Just the hostname part. Will be pre-pended to the `global.domain` for the FQDN | `auth` |
| pep-engine.configMap.pdpHostname | PDP: Just the hostname part. Will be pre-pended to the `global.domain` for the FQDN | `pdp` |
| pep-engine.configMap.workingMode | PEP mode: FULL (PEP will proxy), PARTIAL (PEP is nginx `auth_request` helper) | `FULL` |
| pep-engine.defaultResources\[\].name<br>pep-engine.defaultResources\[\].description<br>pep-engine.defaultResources\[\].resource_uri<br>pep-engine.defaultResources\[\].scopes<br>pep-engine.defaultResources\[\].default_owner | Default resources to apply for initial protection<br>_The default value protects the base path with `public_access` under the ownership of an operator_ | <pre>defaultResources:<br>  - name: "Base Path"<br>    description: "Base path for Open Access to service"<br>    resource_uri: "/"<br>    scopes:<br>      - "public_access"<br>    default_owner: "0000000000000"</pre> |
| pep-engine.customDefaultResources\[\] | Additional (custom) default resources - designed to be supplied for specific deployment policies.<br>A separate value from `defaultResources` is used to avoid inadvertently overwriting the default policy. | `[]` |
| pep-engine.image.repository<br>pep-engine.image.tag<br>pep-engine.image.pullPolicy | PEP container image overrides | <pre>repository: eoepca/um-pep-engine<br>tag: ""<br>pullPolicy: IfNotPresent |
| pep-engine.volumeClaim.name | Name of the PVC that the PEP should use | `um-pep-engine-pvc` |
| pep-engine.volumeClaim.create | `false` assumes the PVC already exists | `true` |


### `uma-user-agent` Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| uma-user-agent.image.repository | The container image to use | `eoepca/uma-user-agent` |
| uma-user-agent.image.tag | The tag of the container image to use | `""`<br>(default `latest`) |
| uma-user-agent.image.pullPolicy | The image pull policy for the container runtime | `IfNotPresent` |
| uma-user-agent.fullnameOverride | Fully qualified application name | `""` |
| uma-user-agent.nameOverride | Suffix used to create fully-qualified application name, in combination with the helm release name | `""` |
| uma-user-agent.service.type | Type of Kubernetes service to create | `ClusterIP` |
| uma-user-agent.service.port | Listen port for service | `80` |
| uma-user-agent.nginxIntegration.enabled | Boolean to enable the integration with the Nginx Ingress Controller.<br>When enabled will create ingress resources with annotations as described by https://github.com/EOEPCA/uma-user-agent/blob/develop/README.md#nginx-configuration | `false` |
| uma-user-agent.nginxIntegration.hosts | Array of hosts to specify for ingress configuration... | {see below} |
| uma-user-agent.nginxIntegration.hosts[].host | First part of the hostname - global.domain will be appended | `""` |
| uma-user-agent.nginxIntegration.hosts[].paths | Array of paths for host... | {see below} |
| uma-user-agent.nginxIntegration.hosts[].paths.path | Request URI path | `/` |
| uma-user-agent.nginxIntegration.hosts[].paths.service.name | Name of the backend service for reverse-proxy | `myservice` |
| uma-user-agent.nginxIntegration.hosts[].paths.service.port | Port of the backend service for reverse-proxy | `80` |
| uma-user-agent.nginxIntegration.annotations | Additional annotations for the ingress | `{}` |
| uma-user-agent.config.configMapName | Name of the `ConfigMap` that is used to pass the `config.yaml` file<br>_Defaults to an auto-generated name that is based on the app release name_ | `""` |
| uma-user-agent.client.credentialsSecretName | Name of the `Secret` that is used to pass the `client.yaml` file<br>_Defaults to an auto-generated name that is based on the app release name_ | `""` |
| uma-user-agent.httpTimeout | Timeout (as client) for http requests (secs) | `10` |
| uma-user-agent.logging.level | Logging level: `panic`, `fatal`, `error`, `warn`/`warning`, `info`, `debug`, `trace` | `info` |
| uma-user-agent.userIdCookieName | Name of the cookie that carries the User Id Token | `auth_user_id` |
| uma-user-agent.authRptCookieName | Name of the cookie that carries the RPT of the last successful request<br>Note that this is a prefix for the name that is appended with `-<endpoint-name>` | `auth_rpt` |
| uma-user-agent.unauthorizedResponse | Text that should form the value for the `Www-Authenticate` header in the `401` response | `""` |
| uma-user-agent.openAccess | Boolean to set 'open' access to the resource server.<br>A value of true bypasses protections (typically used for debugging) | `false` |
