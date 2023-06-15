# Helm chart for the Registration API

## Prerequisites

* This chart requires Docker Engine 1.8+ in any of their supported platforms.

## Chart Components

* Creates a Registration API deployment for a specific workspace.

## Installing the Chart

You can install the chart with the release name `rm-registration-api` in `eoepca` namespace as below.

```bash
$ helm install registration-api charts/rm-registration-api
```

You can debug with:

```bash
helm install --dry-run --debug registration-api charts/rm-registration-api
```

## Values

The configuration parameters in this section control the resource catalogue configuration.

| Parameter                               | Description                                                                                    | Default                          |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------- |
| replicaCount                        | The number of replicas to create  | 1                              |
| image.repository                                 | The image repository to use  | `eoepca/rm-registration-api`                              |
| image.pullPolicy                       | The pull policy to use  | `IfNotPresent`                              |
| image.tag                        | Image tag to use  | `""`                              |
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
| redisServiceName           | Name of the redis service in the namespace | "vs-redis-master"      |
| workspaceK8sNamespace           | Name of the kubernetes namespace to deploy | "rm"      |
| autoProtectionEnabled | Whether to register register a PEP resource for the created workspace  | "True" |
