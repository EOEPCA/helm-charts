# HELM Chart for Policy Decision Point (PDP)

## Prerequisites

* This chart requires Docker Engine 1.8+ in any of their supported platforms.  Please see vendor requirements [here for more information](https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker).
* At least 2GB of RAM. Make sure to assign enough memory to the Docker VM if you're running on Docker for Mac or Windows.

## Chart Components

* Creates a Policy Decision Point deployment
* Creates a Kubernetes Service on specified port (default: 5567)
* Creates a sidecar MongoDB Service to be used as database

## Installing the Chart

You can install the chart with the release name `pdp` in `default` namespace.

```console
$ helm install pdp charts/pdp-engine
```

> Note - If you do not specify a name, helm will select a name for you.

### Installed Components

You can use `kubectl get` to view all of the installed components.

```console
$ kubectl get all -l app=pdp-engine
NAME                              READY   STATUS    RESTARTS   AGE
pod/pdp-engine-7dcb846c9f-8qxvh   2/2     Running   0          2d20h

NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)             AGE
service/pdp-engine   ClusterIP   10.105.58.133   <none>        5567/TCP,1025/TCP   2d20h

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/pdp-engine   1/1     1            1           2d20h

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/pdp-engine-7dcb846c9f   1         1         1       2d20h
```

## Connecting to the PDP

1. Follow the documentation of the PDP Repository in GitHub: [Wiki Policy-Decision-Point](https://github.com/EOEPCA/um-pdp-engine/wiki).

## Values

The configuration parameters in this section control the  endpoints for poicy registration and validation utilized by the PDP instance.

| Parameter                               | Description                                                                                    | Default                          |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------- |
| global.namespace                    | Name where the pdp instance is going to install in the cluster  | `default`                              |
| global.domain                            | Name for the sso_url UMA Compliant | `myplatform.eoepca.org`                        |
| global.pdp             | Generic name for all pdp components in installation | `pdp-engine` |
| global.prefix            | Value to correct ingress redirect prior to URL above | `/`        |
| global.host  | IP where the PDP will launch its components, within a cluster the ip will be generated dynamically and local to the cluster | `0.0.0.0`  |
| global.port | Default port where the PDP will expose the service  | `5576`                       |
| global.nginxIp | IP for the nginx ingress controller                                                        | `10.0.2.15`  
| global.ingressPath | Value to correct ingress redirect. It will add the path specified at the end of the domain name and prior to the endpoints.                                                       | `10Gi`                   |
| configMap.check_ssl_certs       | Checks if the server is running and delivers a valid certificate                             | `false`                  |
| configMap.debug_mode       | Boolean for deploy with verbose logs                             | `true`                  |

## Ports

The PDP exposes the service using both http and https ports.
  port: Exposes the Kubernetes service on the specified port within the cluster. Other pods within the cluster can communicate with the service on the specified port.
  targetPort: Is the port on which the service will send requests to, that your pod will be listening on.
  type: Kind of protocol used

  ```yaml
  ports:
  http-pdp:
    port: 5567
    targetPort: 5567
    type: TCP
  https-pdp:
    port: 1025
    targetPort: 443
    type: TCP
  ```

## Liveness and Readiness

The PDP instance has liveness and readiness checks specified.

## Resources

You can specify the resource limits for this chart in the values.yaml file.  Make sure you comment out or remove the curly brackets from the values.yaml file before specifying resource limits.
Example:

```yaml
requests:
  serviceCpu: 4m
  serviceMemory: 70Mi
  dbCpu: 2m
  dbMemory: 70Mi
```

## Persistence

As the PDP will generate a Persistent Volume in its deployment, the persistence tab in the values.yaml will determine the default space of the disk, type of access constrain and Mode of creation. 

```yaml
persistence: 
  accessModes: ReadWriteMany
  dbStorageSize: 5Gi
  type: DirectoryOrCreate
```
For the volumeClaim:

```yaml
volumeClaim:
  name: um-pdp-engine-pvc
  create: true
```

