# HELM Chart for the Policy Enforcement Point (PEP)

## Prerequisites

* This chart requires Docker Engine 1.8+ in any of their supported platforms.  Please see vendor requirements [here for more information](https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker).
* At least 2GB of RAM. Make sure to assign enough memory to the Docker VM if you're running on Docker for Mac or Windows.

## Chart Components

* Creates a Policy Enforcement Point deployment
* Creates a Kubernetes Service on specified ports (defaults: 5566 and 5576)
* Creates a sidecar MongoDB Service to be used as database for resource registration and access control

## Installing the Chart

You can install the chart with the release name `pep` in `default` namespace.

```console
$ helm install pep charts/pep-engine
```

> Note - If you do not specify a name, helm will select a name for you.

### Installed Components

You can use `kubectl get` to view all of the installed components.

```console
$ kubectl get all -l app=pep-engine
NAME                              READY   STATUS    RESTARTS   AGE
pod/pep-engine-756679fd6f-t5qk8   2/2     Running   0          2d21h

NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
service/pep-engine   ClusterIP   10.109.208.137   <none>        5566/TCP,5576/TCP   2d21h

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/pep-engine   1/1     1            1           2d21h

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/pep-engine-756679fd6f   1         1         1       2d21h
```

## Connecting to the PEP

1. Follow the documentation of the PEP Repository in GitHub: [Wiki Policy-Enforcement-Point](https://github.com/EOEPCA/um-pep-engine/wiki).

## Values

The configuration parameters in this section control the  endpoints for poicy registration and validation utilized by the PEP instance.

| Parameter                               | Description                                                                                    | Default                          |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------- |
| global.namespace                    | Name where the pep instance is going to install in the cluster  | `default`                              |
| global.domain                            | Name for the sso_url UMA Compliant | `myplatform.eoepca.org`                        |
| global.pep             | Generic name for all pep components in installation | `pep-engine` |
| global.clusterDomain            | Domain of the Kubernetes cluster | `svc.cluster.local`        |
| global.serviceHost  | IP where the PEP will launch its components, within a cluster the ip will be generated dynamically and local to the cluster | `0.0.0.0`  |
| global.nginxIp | IP for the nginx ingress controller                                                        | `10.0.2.15`  
| configMap.useThreads | Boolean for threading option  | `true`                       |
| global.umaValidation | Value to configure the PEP to validate policies when the UMA Flow is being done, this involves generally the PDP                                                       | `true`                   |
| configMap.sslCerts       | Checks if the server is running and delivers a valid certificate                             | `false`                  |
| configMap.debugMode       | Boolean for deploy with verbose logs                             | `true`                  |
| configMap.asHostname       | Authorization Server: Just the hostname part. Will be pre-pended to the `global.domain` for the FQDN                             | `auth`                  |
| configMap.pdpHostname       | PDP: Just the hostname part. Will be pre-pended to the `global.domain` for the FQDN                             | `pdp`                  |
| configMap.pdpPort       | PDP default service port                              | `5567`                  |
| configMap.pdpPolicy       | PDP policy service endpoint                             | `/pdp/policy/`                  |
| configMap.verifySignature       | Boolean JWT signature verification                             | `false`                  |
| configMap.defaultResourcePath       | Path from where the resource server will read the default resources for registration                             | `/data/default-resources.json`                  |
| configMap.workingMode       | Specifies the way of how the pep proxy will behave, check the documentation for more information                             | `FULL`                  |

## Ports

The PEP exposes two different services. `proxy-pep` will define the ports for the proxy service while the `resources-pep` determines the port of the resources service.
  port: Exposes the Kubernetes service on the specified port within the cluster. Other pods within the cluster can communicate with the service on the specified port.
  targetPort: Is the port on which the service will send requests to, that your pod will be listening on.
  type: Kind of protocol used

  ```yaml
  ports:
    proxy-pep:
      port: 5566
      targetPort: 5566
      type: TCP
    resources-pep:
      port: 5576
      targetPort: 5576
      type: TCP
  ```

## Liveness and Readiness

The PEP instance has liveness and readiness checks specified.

## Resources

You can specify the resource limits for this chart in the values.yaml file.  Make sure you comment out or remove the curly brackets from the values.yaml file before specifying resource limits.
Example:

```yaml
requests:
  serviceCpu: 2m
  serviceMemory: 50Mi
  dbCpu: 3m
  dbMemory: 150Mi
```

## Persistence

As the PEP will generate a Persistent Volume in its deployment, the persistence tab in the values.yaml will determine the default space of the disk, type of access constrain and Mode of creation. 

```yaml
persistence: 
  accessModes: ReadWriteMany
  dbStorageSize: 5Gi
  type: DirectoryOrCreate
```
For the volumeClaim:

```yaml
volumeClaim:
  name: um-pep-engine-pvc
  create: true
```

