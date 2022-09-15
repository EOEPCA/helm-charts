# Helm chart for the Workspace API

## Prerequisites

* This chart requires Docker Engine 1.8+ in any of their supported platforms.

## Chart Components

* Creates a Workspace API deployment based on pycsw.
* Creates a Kubernetes Service for the Workspace API.
* Creates a Kubernetes Service Account for the Workspace API.
* Creates a Cluster Role for the Workspace API.
* Creates a Cluster Role Binding for the Workspace API.
* Creates a Workspace API Ingress controller.

## Installing the Chart

You can install the chart with the release name `rm-workspace-api` in `eoepca` namespace as below.

```bash
$ helm install workspace-api charts/rm-workspace-api
```

You can debug with:

```bash
helm install --dry-run --debug workspace-api charts/rm-workspace-api
```

## Values

The configuration parameters in this section control the resource catalogue configuration.

| Parameter                               | Description                                                                                    | Default                          |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------- |
| replicaCount                        | The number of replicas to create  | 1                              |
| image.repository                                 | The image repository to use  | `eoepca/rm-workspace-api`                              |
| image.pullPolicy                       | The pull policy to use  | `IfNotPresent`                              |
| image.tag                        | Image tag to use  | `""`                              |
| imagePullSecrets                        | Any image pull sectets to use  | `[{name: flux-workspace-api}]`                              |
| nameOverride                        | Override the full name  | `""`                              |
| fullNameOverride                        | Override the name  | `""`                              |
| serviceAccount.create                        | Whether or not to create a service account  | `true`                              |
| serviceAccount.annotations                        | Any annotations to give the service account  | `{true}`                              |
| serviceAccount.name                        | Override the service account name  | `""`                              |
| podAnnotations                        | Additional annotations for the Pod  | `{prometheus.io/scrape: "true"}`                              |
| podSecurityContext                        | Specify the Pods security context  | `{}`                              |
| securityContext                        | Specify the security context  | `{}`                              |
| service.type                        | The service type to use  | `ClusterIP`                              |
| service.port                        | Specify the service port  | `80`                              |
| ingress.enabled                        | Whether or not to enable an ingress controller  | `true`                              |
| ingress.annotations                        | Additional annotations for the ingress  | `{}`                              |
| ingress.hosts                        | Configured ingress hosts  | `[{host: "workspace-api.eopca.org", paths: ["/"]}]`                              |
| ingress.tls                        | Configured TLS ingress hosts  | `[]`                              |
| resources.limits.cpu              | CPU Limits  | `0.5`                              |
| resources.limits.memory              | Memory Limits  | `512Mi`                              |
| resources.requests.cpu              | CPU Requests  | `0.05`                              |
| resources.requests.memory              | Memory Requests  | `128Mi`                              |
| nodeSelector                        | Specify a node selector  | `{}`                              |
| tolerations                        | Specify a tolerations  | `{}`                              |
| affinity                        | Specify a affinity  | `{}`                              |
| prefixForName                        | Specify a workspace prefix to be prepended before each workspace  | `develop-user`                              |
| workspaceSecretName                        | Specify the name of the secret containing the workspace bucket credentials  | `bucket`                              |
| namespaceForBucketResource                        | Specify the namespace for the created bucket resource  | `rm`                              |
| workspaceConfigMapName                        | Specify the name of the ConfigMap to locate the | `workspace`                              |
| s3Endpoint                        | The S3 Endpoint for the users bucket | `https://cf2.cloudferro.com:8080`                              |
| s3Region                        | The S3 Region for the users bucket | `RegionOne`                              |
| umaClientSecretName                        | The UMA Client Secret Name | `""`                             |
| umaClientSecretNamespace                        | The UMA Client Secret Namespace | `""`                             |
| workspaceChartsConfigMap          | Name of config map which features the helm chart templates which define the workspace | ""      |
| fluxHelmOperator.enabled     | Whether to install the flux helm operator together with the workspace api (for cluster which don't use flux) | false | 
| redisServiceName           | Name of the redis service in the namespace | "vs-redis-master"      |
| harborUrl | URL of harbor service | "" |
| harborUsername | Username of harbor admin user | "" |
| harborPassword | Password of harbor admin user | "" |


## Defining the workspace

The workspace-api deploys a workspace by rendering the contents of a config map (referenced by `workspaceChartsConfigMap`) as a jinja2 template and applying the resulting HelmRelease.

The jinja2 template is rendered with the following template variables:

* `workspace_name`
* `default_owner`
* Access data for the workspace bucket: `access_key_id`, `secret_access_key`, `bucket`, `projectid`
