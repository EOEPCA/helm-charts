# Helm chart for the Minio Bucket API

## Prerequisites

* This chart requires Docker Engine 1.8+ in any of their supported platforms.

## Chart Components

* Creates a Kubernetes Service for the Minio Bucket API.

## Installing the Chart

You can install the chart with the release name `rm-minio-bucket-api` in `eoepca` namespace as below.

```bash
$ helm install minio-bucket-api charts/rm-minio-bucket-api
```

You can debug with:

```bash
helm install --dry-run --debug minio-bucket-api charts/rm-minio-bucket-api
```

