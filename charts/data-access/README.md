# HELM Chart for Resource Guard

This README describes how to install the Data Access in your Kubernetes cluster using `Helm`.

## Description





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

To install the chart with the release name `my-data-access`:
```sh
helm install my-data-access eoepca/data-access -f my-values.yaml
```

This will deploy the release with default values, plus overrides from the file `my-values.yaml`.

## Upgrading the Chart

```sh
helm upgrade my-data-access eoepca/data-access -f my-values.yaml
```

## Configuration

The Resource Guard comprises only sub-chart dependencies, i.e. has no templates of its own. Thus, it is configured as values passthru to its subcharts, whose helm values are documented at:
* View Server - `vs`

Nevertheless, we detail in the following tables some parameters that are commonly specified.

### `global` Configuration

