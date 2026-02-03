# Helm chart for Registration API service

## Prerequisites

* This chart requires Docker Engine 1.8+ in any of their supported platforms.

## Chart Components

* Creates a Registration API deployment based on pygeoapi.
* Creates a Kubernetes Service for the Registration API on specified port (default: 8000)
* Creates a Registration API Ingress controler.

## Installing the Chart

You can install the chart with the release name `registration-api` in `eoepca` namespace as below.

```bash
$ helm install registration-api charts/registration-api
```

You can debug with:

```bash
helm install --dry-run --debug registration-api charts/registration-api
```

## Values

The configuration parameters in this section control the registration API configuration.

| Parameter                               | Description                                                                                    | Default                          |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------- |
| global.namespace                        | Name of the Kubernetes namespace to install the helm chart  | `rm`                              |
| ingress.enabled                     | Set true to enable the ingress controler, false to disable  | `true`                              |
| ingress.subpath_enabled             | Set true to enable path based configuration of the ingress controler, false to disable  | `false`                              |
| ingress.subpath                    | Subpath of the registration API to be set to the ingress rules/rewrites. The pygeoapi.config.server.url value should be set accordingly  | `/registration-api`                              |
| ingress.name                        | Name of the Kubernetes ingress for the registration API  | `registration-api`                              |
| ingress.class                        | Class of the Kubernetes ingress  | `nginx`                              |
| ingress.host                        | Hostname to be used by the Kubernetes ingress controler  | `registration-api.demo.eoepca.org`                              |
| pygeoapi.name                        | Name of the registration API deployment  | `registration-api`                              |
| pygeoapi.image.repository              | DockerHub repository for the registration API images  | `eoepca/registration-api`                              |
| pygeoapi.image.tag                        | Docker image tag for the registration API image  | `latest`                              |
| pygeoapi.container_port                        | Container port of the registration API service  | `80`                              |
| pygeoapi.service_name                        | Name of the registration API service  | `registration-api-service`                              |
| pygeoapi.service_port                        | Port of the registration API service  | `80`                              |
| pygeoapi.configmap_name                        | Name of the Kubernetes configmap  | `registration-api-configmap`                              |
| pygeoapi.volume_name                        | Volume name that stores the registration API configuration  | `registration-api-config`                              |
| pygeoapi.volume_path                        | Volume path for the registration API configuration  | `/pygeoapi`                              |
| pygeoapi.config                        | Configuration settings for pygeoapi  | See hhttps://docs.pygeoapi.io/en/latest/configuration.html                              |
