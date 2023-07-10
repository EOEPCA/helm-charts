# Helm chart for the Bucket Operator Wrapper

## Prerequisites

* This chart requires Docker Engine 1.8+ in any of their supported platforms.

## Chart Components

* Creates a Kubernetes Service for the Bucket Operator Wrapper.

## Installing the Chart

You can install the chart with the release name `rm-bucket-operator-wrapper` in `eoepca` namespace as below.

```bash
$ helm install bucket-operator-wrapper charts/rm-bucket-operator-wrapper
```

You can debug with:

```bash
helm install --dry-run --debug bucket-operator-wrapper charts/rm-bucket-operator-wrapper
```

