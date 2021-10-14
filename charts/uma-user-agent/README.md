# HELM Chart for UMA User Agent

This README describes how to install the UMA User Agent in your Kubernetes cluster using `Helm`.

## Sources and Documentation

The sources for `uma-user-agent` and associated documentation are on GitHub:
* Repository: https://github.com/EOEPCA/uma-user-agent
* README Documentation: https://github.com/EOEPCA/uma-user-agent/blob/develop/README.md

These should be consulted for a detailed understanding of the purpose, scope and usage of the UMA User Agent.

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

To install the chart with the release name `my-uma-agent`:
```sh
helm install my-uma-agent eoepca/uma-user-agent -f my-values.yaml
```

This will deploy the release with default values, plus overrides from the file `my-values.yaml`.

## Upgrading the Chart

```sh
helm upgrade my-uma-agent eoepca/uma-user-agent -f my-values.yaml
```

## Configuration

The following table lists the configuration parameters of the UMA User Agent chart and their default values.<br>
_For reference, the `uma-user-agent` application configuration parameters are described [here](https://github.com/EOEPCA/uma-user-agent/blob/develop/README.md#agent-configuration)._

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| global.context | Textual identifier that is used to distinguish between instances | `generic` |
| global.clusterDomain | The fully-qualified domain of the Kubernetes cluster | `svc.cluster.local` |
| global.domain | The DNS domain of the deployment | `myplatform.eoepca.org` |
| global.pep | The name of the PEP instance with which to communicate | `pep-engine` |
| global.ports.proxy-pep.port | The port on the PEP to connect for `auth_request` | `5566` |
| global.certManager.clusterIssuer | The name of the `ClusterIssuer` instance for tls.<br>Leave blank for no TLS | `""` |
| image.repository | The container image to use | `eoepca/uma-user-agent` |
| image.tag | The tag of the container image to use | `""`<br>(default `latest`) |
| image.pullPolicy | The image pull policy for the container runtime | `IfNotPresent` |
| fullnameOverride | Fully qualified application name | `""` |
| nameOverride | Suffix used to create fully-qualified application name, in combination with the helm release name | `""` |
| service.type | Type of Kubernetes service to create | `ClusterIP` |
| service.port | Listen port for service | `80` |
| nginxIntegration.enabled | Boolean to enable the integration with the Nginx Ingress Controller.<br>When enabled will create ingress resources with annotations as described by https://github.com/EOEPCA/uma-user-agent/blob/develop/README.md#nginx-configuration | `false` |
| nginxIntegration.hosts | Array of hosts to specify for ingress configuration... | {see below} |
| nginxIntegration.hosts[].host | First part of the hostname - global.domain will be appended | `""` |
| nginxIntegration.hosts[].paths | Array of paths for host... | {see below} |
| nginxIntegration.hosts[].paths.path | Request URI path | `/` |
| nginxIntegration.hosts[].paths.service.name | Name of the backend service for reverse-proxy | `myservice` |
| nginxIntegration.hosts[].paths.service.port | Port of the backend service for reverse-proxy | `80` |
| nginxIntegration.annotations | Additional annotations for the ingress | `{}` |
| config.configMapName | Name of the `ConfigMap` that is used to pass the `config.yaml` file<br>_Defaults to an auto-generated name that is based on the app release name_ | `""` |
| client.credentialsSecretName | Name of the `Secret` that is used to pass the `client.yaml` file<br>_Defaults to an auto-generated name that is based on the app release name_ | `""` |
| httpTimeout | Timeout (as client) for http requests (secs) | `10` |
| logging.level | Logging level: `panic`, `fatal`, `error`, `warn`/`warning`, `info`, `debug`, `trace` | `info` |
| userIdCookieName | Name of the cookie that carries the User Id Token | `auth_user_id` |
| authRptCookieName | Name of the cookie that carries the RPT of the last successful request<br>Note that this is a prefix for the name that is appended with `-<endpoint-name>` | `auth_rpt` |
| unauthorizedResponse | Text that should form the value for the `Www-Authenticate` header in the `401` response | {blank} |
| openAccess | Boolean to set 'open' access to the resource server.<br>A value of true bypasses protections (typically used for debugging) | `false` |
