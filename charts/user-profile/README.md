# HELM Chart for the User Profile

## Prerequisites

* This chart requires Docker Engine 1.8+ in any of their supported platforms.  Please see vendor requirements [here for more information](https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker).
* At least 2GB of RAM. Make sure to assign enough memory to the Docker VM if you're running on Docker for Mac or Windows.

## Chart Components

* Creates a User Profile deployment
* Creates a Kubernetes Service on specified port (default: 5566)
* Exposes a User Interface under the ingress path where the user attributes can be queried

## Installing the Chart

You can install the chart with the release name `user` in `default` namespace.

```console
$ helm install user charts/user-profile
```

> Note - If you do not specify a name, helm will select a name for you.

### Installed Components

You can use `kubectl get` to view all of the installed components.

```console
$ kubectl get all -l app=user-profile
NAME                                READY   STATUS              RESTARTS   AGE
pod/user-profile-5668dcbd84-ndhs7   0/1     ContainerCreating   0          95s

NAME                   TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)             AGE
service/user-profile   ClusterIP   10.98.180.85   <none>        5566/TCP,1028/TCP   95s

NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/user-profile   0/1     1            0           95s

NAME                                      DESIRED   CURRENT   READY   AGE
replicaset.apps/user-profile-5668dcbd84   1         1         0       95s
```

## Connecting to the User Profile

1. Follow the documentation of the User-Profile Repository in GitHub: [Wiki User-Profile](https://github.com/EOEPCA/um-user-profile/wiki).

## Values

The configuration parameters in this section control the base aspects to make the User Profile connect to the Login Service and deploy an instance of the User Profile in a clusterized environment.

| Parameter                               | Description                                                                                    | Default                          |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------- |
| global.baseUri                    | Path under where the user_profile will expose its interface, this will be the endpoint for the service  | `/web_ui`                              |
| global.domain                            | Name for the sso_url UMA Compliant | `myplatform.eoepca.org`                        |
| global.user             | Generic name for all user-profile components in installation | `user-profile` |
| global.serviceHost  | IP where the User Profile will launch its components, within a cluster the ip will be generated dynamically and local to the cluster | `0.0.0.0`  |
| global.servicePort | Default port where the User Profile will expose the service  | `5566`                       |
| global.nginxIp | IP for the nginx ingress controller                                                        | `10.0.2.15`  
| configMap.check_ssl_certs       | Checks if the server is running and delivers a valid certificate                             | `false`                  |
| configMap.debug_mode       | Boolean for deploy with verbose logs                             | `true`                  |

## Config Map

The values specified in the ConfigMap will apply changes on the front page of the user interface deployed such as the title, images, and base theme colors among other configurations for the client to be registered in Gluu

  ```yaml
 configMap:
  title: "EOEPCA User Profile"
  scopes: "openid email user_name"
  redirectUri: "/web_ui/oauth/callback"
  postLogoutRedirectUri: "/web_ui"
  oauthCallbackPath: "/oauth/callback"
  logoutEndpoint: "/logout"
  protectedAttributes: "userName active emails displayName value primary"
  blacklistAttributes: "schemas id meta $ref"
  separatorUiAttributes: "->"
  colorWebBackground: "#D7EDEC"
  colorWebHeader: "#FFFFFF"
  logoAltName: "EOEPCA Logo"
  logoImagePath: "/static/img/logo.png"
  colorHeaderTable: "#38A79F"
  colorTextHeaderTable: "white"
  colorButtonModify: "#38A79F"
  useThreads: "true"
  debugMode: "true"
  ```

## Ports

The User Profile exposes the service using both http and https ports.
  port: Exposes the Kubernetes service on the specified port within the cluster. Other pods within the cluster can communicate with the service on the specified port.
  targetPort: Is the port on which the service will send requests to, that your pod will be listening on.
  type: Kind of protocol used

  ```yaml
 ports:
  http-up:
    port: 5566
    targetPort: 5566
    type: TCP
  https-up:
    port: 1028
    targetPort: 443
    type: TCP
  ```

## Liveness and Readiness

The User Profile instance has liveness and readiness checks specified.

## Resources

You can specify the resource limits for this chart in the values.yaml file.  Make sure you comment out or remove the curly brackets from the values.yaml file before specifying resource limits.
Example:

```yaml
requests:
  memory: 70Mi
  cpu: 3m
```

## Persistence

As the User Profile will generate a Persistent Volume in its deployment, the persistence tab in the values.yaml will determine the default space of the disk, type of access constrain and Mode of creation. 

```yaml
persistence: 
  accessModes: ReadWriteMany
  dbStorageSize: 5Gi
  type: DirectoryOrCreate
```
For the volumeClaim:

```yaml
volumeClaim:
  name: um-user-profile-pvc
  create: true
```
