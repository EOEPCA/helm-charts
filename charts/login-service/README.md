# HELM Chart for the Login Service

## Prerequisites

* This chart requires Docker Engine 1.8+ in any of their supported platforms.  Please see vendor requirements [here for more information](https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker).
* At least 2GB of RAM. Make sure to assign enough memory to the Docker VM if you're running on Docker for Mac or Windows.

## Chart Components
* It's a nested Helm Chart with more than one service and deployments
* Creates a full Login Service Instance (Gluu based)
* Exposes the oxtrust service for access to the UI

## Installing the Chart

You can install the chart with the release name `id4eo` in `default` namespace. The entire installation of the Login Service will take around 20 minutes to be up depending on the resources of the machine.

```console
$ helm install id4eo charts/login-service
```
> Note - If you do not specify a name, helm will select a name for you.

The installation will apply all charts described within the login-service chart.
  * Config-Init: This instance will stand as a Job that will ingest the first configuration data for the other services to feed from in installation. 
  * OpenDJ: The WrenDS image will create the backend for the LDAP database and will comunicate with the presistence Job to apply all custom changes done in Gluu.
  * Persistence: This Job will run aside the OpenDJ pod to ingest the custom data into the database.
  * OxPassport: This Pod will allow the passport feature to the hole Login Service, it applies to the login feature.
  * OxAuth: This deployment will set up the Authentication and Authorization service. Needs the previous pods to be running.
  * OxTrust: This is the last to be installed and will offer the main Gluu UI from where the application can be accessed.

### Installed Components

You can use `kubectl get` to view all of the installed components.

```console
$ kubectl get all | grep id4eo
pod/id4eo-config-27zwh                  0/1     Completed   0          164m
pod/id4eo-opendj-init-ss-0              1/1     Running     0          164m
pod/id4eo-oxauth-6946d5c4b8-vv2ms       1/1     Running     1          164m
pod/id4eo-oxpassport-6b44dddd4b-79t2d   1/1     Running     0          164m
pod/id4eo-oxtrust-ss-0                  1/1     Running     1          164m
pod/id4eo-persistence-init-ss-k7qmw     0/1     Completed   0          164m

deployment.apps/id4eo-oxauth       1/1     1            1           164m

deployment.apps/id4eo-oxpassport   1/1     1            1           164m
replicaset.apps/id4eo-oxauth-6946d5c4b8       1         1         1       164m
replicaset.apps/id4eo-oxpassport-6b44dddd4b   1         1         1       164m


statefulset.apps/id4eo-opendj-init-ss   1/1     164m
statefulset.apps/id4eo-oxtrust-ss       1/1     164m
job.batch/id4eo-config                1/1           3m35s      164m
job.batch/id4eo-persistence-init-ss   1/1           11m        164m
```

## Connecting to the Login Service

Follow the documentation of the Login-Service Repository in GitHub: [Wiki Login Service](https://github.com/EOEPCA/um-login-service/wiki).

## Values

The values can be edited in each sub-chart or on most generic at the parent level.
The configuration parameters in this section control the base domain and most general configuration for every sub-chart.

## Global

The global section will apply the values overwriting the defined in the global section of the subcharts values.

| Parameter                        | Description                                                                                           | Default                          |
| -------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------- |
| namespace                        | Name of the namespace where the login service instance is going to install in the cluster             | `default`                        |
| nginxIp                          | IP for the nginx ingress controller                                                                   | `10.0.2.15`                      |  
| serviceName                      | Name for the main OpenDJ service                                                                      | `opendj`                         |
| oxAuthServiceName                | Name for the main OxAuth service                                                                      | `oxauth`                         |
| persistenceServiceName           | Name for the main persistence Job service                                                             | `persistence`                    |
| oxTrustServiceName               | Name for the main OxTrust service                                                                     | `oxtrust`                        |
| domain                           | Name for the sso_url UMA Compliant                                                                    | `myplatform.eoepca.org`          |
| gluuLdapUrl                      | URL where the LDAP backend is running                                                                 | `opendj:1636`                    |
| gluuMaxRamFraction               | Number of fractions of RAM, where 1 is the 100% of the requested RAM                                  | `1`                              |
| configAdapterName                | Name for the k8s config adapter                                                                       | `kubernetes`                     |
| configSecretAdapter              | Name for the k8s secret adapter                                                                       | `kubernetes`                     |
| provisioner                      | Clustering provisioner name                                                                           | `k8s.io/minikube-hostpath`       |



## Config

For the Config Job the main configuration will focus on certificate signatures and base LDAP customization. The image used is from gluuFederation `gluufederation/config-init:4.1.1_02`.
This will be the first instance to complete, the rest of the deployments will be waiting for the config-job to finish ingesting data in the volume and then consume it.
                                                                                                                                                                     |
| Parameter                        | Description                                                                                           | Default                          |
| -------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------- |
| enabled                          | Boolean value to enable or not the chart installation                                                 | `true`                           |
| domain                           | Name for the sso_url UMA Compliant                                                                    | `myplatform.eoepca.org`          |  
| ldapType                         | Value for specifying the LDAP controller                                                              | `opendj`                         |
| countryCode                      | Code for the country desired (This will apply to the certificate generation)                          | `ES`                             |
| state                            | Name for the state desired (This will apply to the certificate generation)                            | `Madrid`                         |
| city                             | Name for the city desired (This will apply to the certificate generation)                             | `Tres Cantos`                    |
| email                            | E-Mail of the organization (This will apply to the certificate generation)                            | `eoepca@deimos-space.com`        |
| orgName                          | Name of the organization (This will apply to the certificate generation)                              | `Deimos Space S.L.U.`            |
| adminPass                        | Password for the administrator user                                                                   | `defaultPWD`                     |
| ldapPass                         | Password for the root LDAP operations                                                                 | `defaultPWD`                     |
| redisPass                        | Password for the redis backend instance                                                               | `aaaa`                           |
| gluuConfAdapter                  | Name for the k8s secret adapter                                                                       | `kubernetes`                     |

This Job has its own resource requests specified in the limits and requests same as the persistence details:

  ```yaml
  limits:
    cpu: 600m
    memory: 800Mi
  requests:
    cpu: 100m
    memory: 500Mi

  persistence:
    size: 1Gi
    accessModes: ReadWriteOnce
    storageClassName: ""
  ```

## OpenDJ

OpenDJ StatefulSet will set up the LDAP backend of the Login Service and wait for the Persistence Job to ingest the data into the database. The image used is from GluuFederation `gluufederation/wrends:4.1.1_01`. The expected behavior is to start listening in some ports and after the persistence is finish complete the installation by starting the LDAP service.
The basic configuration can be done in the values of the parent chart, but for more specific customization the child chart has its own values.

### Parent

| Parameter                        | Description                                                                                           | Default                          |
| -------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------- |
| enabled                          | Boolean value to enable or not the chart installation                                                 | `true`                           |
| gluuCacheType                    | Name for the sso_url UMA Compliant                                                                    | `myplatform.eoepca.org`          |  
| gluuRedisEnabled                 | Value for specifying the LDAP controller                                                              | `opendj`                         |

At the parent definition, the image for the login-persistence can be specified:

  ```yaml
  enabled: true
  gluuCacheType: NATIVE_PERSISTENCE
  gluuRedisEnabled: false
  volumeClaim:
    name: um-login-service-pvc
  persistence:
    enabled: true
    image:
      repository: eoepca/um-login-persistence
      pullPolicy: IfNotPresent
      tag: "v1.0"
  ```

### Child

At the child level the main configuration variables for the OpenDJ are the following:

| Parameter                        | Description                                                                                            | Default                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------- |
| gluuLdapInit                     | Boolean value to enable the LDAP instance.                                                             | `true`                           |
| gluuLdapInitHost                 | Host name for where the LDAP instance is going to be found.                                            | `localhost`                      |  
| gluuLdapInitPort                 | Port where the LDAP is going to expose the service.                                                    | `1636`                           |
| gluuOxtrustConfigGeneration      | Boolean to decide whether or not apply OxTrust configuration backend.                                  | `true`                           |
| gluuCacheType                    | Options REDIS or NATIVE_PERSISTENCE. If REDIS is used gluuRedisEnabled config has to be set to true    | `NATIVE_PERSISTENCE`             |
| gluuCertAltName                  | Name for the delegation of the certificate creation.                                                   | `opendj`                         |
| gluuRedisEnabled                 | Will determin if GLUU_REDIS_URL and GLUU_REDIS_TYPE if they will be used.                              | `false`                          |
| gluuRedisCacheType               | Default cache tipe for REDIS, no other option allowed.                                                 | `REDIS`                          |
| gluuRedisUrl                     | Redis url with port. Used when Redis is deployed for Cache                                             | `redis:6379`                     |
| gluuRedisType                    | Type of Redis deployed. ("SHARDED", "STANDALONE", "CLUSTER", or "SENTINEL")                            | `STANDALONE`                     |

This chart has the task of raising two types of deployments, the OpenDJ and the Persistence Job. The customization of the Job is done at the same level of variables as that of the OpenDJ, these being the following values ​​to configure:

| Parameter                        | Description                                                                                            | Default                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------- |
| enabled                          | Boolean value to enable the persistence ingestion.                                                     | `true`                           |
| size                             | Initial size for the basic load of configuration.                                                      | `100M`                           |
| pvcSize                          | Desired size of the Persistent Volume.                                                                 | `3Gi`                            |
| name                             | Name of the chart deployment.                                                                          | `persistence`                    |
| accessModes                      | Access type for the PVC.                                                                               | `ReadWriteMany`                  |
| type                             | Type of PVC deployment.                                                                                | `DirectoryOrCreate`              |
| dbStorageSize                    | Database storage capacity.                                                                             | `3Gi`                            |
| statefulSetReplicas              | Number of replicas of the Stateful Set.                                                                | `1`                              |
| restartPolicy                    | Policy for restarting the image.                                                                       | `Never`                          |
| configAdapter                    | Name of the config adapter.                                                                            | `GLUU_CONFIG_ADAPTER`            |
| adapter                          | The config backend adapter.                                                                            | `kubernetes`                     |
| secretAdapter                    | Name for the secret adapter.                                                                           | `GLUU_SECRET_ADAPTER`            |
| passport                         | Name for the variable that enables the use of passport.                                                | `GLUU_PASSPORT_ENABLED`          |
| passportv                        | Value that enables the use of passport.                                                                | `true`                           |
| ldapUrl                          | Name for the LDAP URL variable.                                                                        | `GLUU_LDAP_URL`                  |
| ldapUrlv                         | The LDAP database's IP address or hostname.                                                            | `opendj:1636`                    |
| persistenceType                  | Name for the persistence backend.                                                                      | `GLUU_PERSISTENCE_TYPE`          |
| persistenceTypev                 | Persistence backend being used (one of ldap, couchbase, or hybrid; default to ldap)                    | `ldap`                           |
| oxtrustConf                      | Name of the OxTrust configuration variable.                                                            | `GLUU_OXTRUST_CONFIG_GENERATION` |
| oxtrustConfv                     | Whether to generate oxShibboleth configuration or not (default to true)                                | `false`                          |
| clientID                         | Name of the LDAP client ID variable.                                                                   | `LP_CLIENT_ID`                   |
| clientIDv                        | LDAP Client ID value.                                                                                  | `1234567890`                     |
| clientSecret                     | Name of the LDAP client Secret variable.                                                               | `LP_CLIENT_SECRET`               |
| clientSecretv                    | LDAP Client Secret value.                                                                              | `0987654321`                     |
| pdpEp                            | Endponit for the PDP Ingress path.                                                                     | `/pdp`                           |


COIH Provider values needs to be configured after deployment for security issues, as all values are passed throught the ConfigMap as env variables, the name of those env vars need to be specified:

  ```yaml
  coihClientID: COIH_CLIENT_ID
  coihClientIDv: "1234"
  coihClientSecret: COIH_CLIENT_SECRET
  coihClientSecretv: "1234"
  ```
## OxAuth

### Parent

The OxAuth deployment will have all configuration derived from the LDAP service, by default the image used belongs to Gluu organization under the name and tag `gluufederation/oxauth:4.1.1_03`. The generic values for the parent will contain:

| Parameter                        | Description                                                                                            | Default                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------- |
| enabled                          | Boolean value to enable the OxAuth installation.                                                       | `true`                           |
| dynamicStorage                   | Boolean value to enable the dynamic location of storage.                                               | `100M`                           |

### Child

For further customization the child values will have in addition the following variables:

| Parameter                        | Description                                                                                            | Default                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------- |
| replicaCount                     | Boolean value to control the number of replicas of the deployment.                                     | `1`                              |
| falsure                          | Boolean value to interact with the `GLUU_SYNC_CASA_MANIFESTS` variable.                                | `true`                           |
| ports.containerPort              | Port number where the service will run.                                                                | `8080`                           |

The base configuration for jetty support needs some mount path for the volume to create and populate following the schema:

  ```yaml
  volumeMounts:
    logs:
      mountPath: /opt/gluu/jetty/oxauth/logs
      subPath: oxauth/logs
    ext:
      mountPath: /opt/gluu/jetty/oxauth/lib/ext
      subPath: oxauth/lib/ext
    static:
      mountPath: /opt/gluu/jetty/oxauth/custom/static
      subPath: oxauth/custom/static
    pages:
      mountPath: /opt/gluu/jetty/oxauth/custom/pages
      subPath: oxauth/custom/pages
  ```

## OxTrust

### Parent

The OxTrust deployment will have all configuration derived from the LDAP service same as OxAuth, by default the image used belongs to Gluu organization under the name and tag `gluufederation/oxtrust:4.1.1_02`. The generic values for the parent will contain:

| Parameter                        | Description                                                                                            | Default                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------- |
| enabled                          | Boolean value to enable the OxTrust installation.                                                      | `true`                           |
| dynamicStorage                   | Boolean value to enable the dynamic location of storage.                                               | `100M`                           |

### Child

For further customization the child values will have in addition the following variables:

| Parameter                        | Description                                                                                            | Default                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------- |
| replicaCount                     | Boolean value to control the number of replicas of the deployment.                                     | `1`                              |
| gluuOxauthBackend                | URL and port for the oxauth service internally.                                                        | `oxauth:8080`                    |
| containerPort                    | Port number where the OxAuth service will be running.                                                  | `8080`                           |
| gluuMaxRamFraction               | Number of fractions of RAM, where 1 is the 100% of the requested RAM.                                  | `1`                              |
| service.port                     | Port number where the service will run.                                                                | `80`                             |

The base configuration for jetty support needs some mount path for the volume to create and populate following the schema:

  ```yaml
  volumeMounts:
    logs:
      mountPath: /opt/gluu/jetty/identity/logs
      subPath: oxtrust/logs
    ext:
      mountPath: /opt/gluu/jetty/identity/lib/ext
      subPath: oxtrust/lib/ext
    static:
      mountPath: /opt/gluu/jetty/identity/custom/static
      subPath: oxtrust/custom/static
    pages:
      mountPath: /opt/gluu/jetty/identity/custom/pages
      subPath: oxtrust/custom/pages
  ```

## Nginx

The Nginx controller can be used as Ingress for load balancing, currently will use the tls-certificates and specify the domain name for the Login Service. It uses an external image to manage tls with Gluu under the name and tag repository `kungus/gluu-tls-initializer:stable`

  ```yaml
  nginx:
    enabled: true
    ingress:
      enabled: true
      annotations: {}
      path: /
      hosts:
        - myplatform.eoepca.org
      tls: 
      - secretName: tls-certificate
        hosts:
          - myplatform.eoepca.org
    resources: {}
    autoscaling:
      enabled: false
      minReplicas: 1
      maxReplicas: 100
      targetCPUUtilizationPercentage: 80
      # targetMemoryUtilizationPercentage: 80
    nodeSelector: {}
    tolerations: []
    affinity: {}
    tags:
      redis: false
  ```

## Liveness and Readiness

The Login Service instance has liveness and readiness checks specified in each sub-chart, it may need to be specified in some specifics services that takes some time to be ready such as OxAuth, OxTrust and OpenDJ.


