# Helm chart for Resource Catalogue service

## Prerequisites

* This chart requires Docker Engine 1.8+ in any of their supported platforms.

## Chart Components

* Creates a Resource Catalogue deployment based on pycsw.
* Creates a Resource Catalogue Database deployment based on PostgreSQL.
* Creates a Kubernetes Service for the Resource Catalogue on specified port (default: 8000)
* Creates a Kubernetes Service for the Resource Catalogue Database on specified port (default: 5432)
* Creates a Persistence Volume for the Resource Catalogue Database.
* Creates a Resource Catalogue Ingress controler.

## Installing the Chart

You can install the chart with the release name `ades` in `eoepca` namespace as below.

```bash
$ helm install resource-catalogue charts/rm-resource-catalogue
```

You can debug with:

```bash
helm install --dry-run --debug resource-catalogue charts/rm-resource-catalogue
```

## Values

The configuration parameters in this section control the resource catalogue configuration.

| Parameter                               | Description                                                                                    | Default                          |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------- |
| global.namespace                        | Name of the Kubernetes namespace to install the helm chart  | `rm`                              |
| db.name                                 | Name of the database deployment  | `resource-catalogue-db`                              |
| db.service_name                       | Name of the database service  | `resource-catalogue-db-service`                              |
| db.image                        | Docker image name for the catalogue database  | `postgis/postgis:12-3.1`                              |
| db.port                        | Port of the database service  | `5432`                              |
| db.database                        | Catalogue database name  | `pycsw`                              |
| db.user                        | Database user/owner of the catalogue database  | `postgres`                              |
| db.volume_name                        | Volume name that stores the database data  | `resource-catalogue-db-data`                              |
| db.volume_path                        | Volume path for the database data  | `/var/lib/postgresql/data/pgdata`                              |
| db.volume_size                        | Volume size to store the database data  | `500Mi`                              |
| ingress.name                        | Name of the Kubernetes ingress for the catalogue  | `resource-catalogue`                              |
| ingress.class                        | Class of the Kubernetes ingress  | `nginx`                              |
| ingress.host                        | Hostname to be used by the Kubernetes ingress controler  | `resource-catalogue.demo.eoepca.org`                              |
| pycsw.name                        | Name of the catalogue deployment  | `resource-catalogue`                              |
| pycsw.image.repository              | DockerHub repository for the catalogue images  | `geopython/pycsw`                              |
| pycsw.image.tag                        | Docker image tag for the catalogue image  | `eoepca-0.9.0`                              |
| pycsw.container_port                        | Container port of the catalogue service  | `8000`                              |
| pycsw.service_name                        | Name of the catalogue service  | `resource-catalogue-service`                              |
| pycsw.service_port                        | Port of the catalogue service  | `80`                              |
| pycsw.configmap_name                        | Name of the Kubernetes configmap  | `resource-catalogue-configmap`                              |
| pycsw.volume_name                        | Volume name that stores the catalogue configuration  | `resource-catalogue-config`                              |
| pycsw.volume_path                        | Volume path for the catalogue configuration  | `/etc/pycsw`                              |
| pycsw.config                        | Configuration settings for pycsw  | See https://docs.pycsw.org/en/latest/configuration.html                              |
| pycsw.config.server.home                        | The full filesystem path to pycsw  | `/home/pycsw`                              |
| pycsw.config.server.url                       | The URL of the resulting service  | `https://resource-catalogue.demo.eoepca.org/`                              |
| pycsw.config.server.maxrecords                        | The maximum number of records to return by default.  | `10`                              |
| pycsw.config.server.federatedcatalogues               | Comma delimited list of CSW endpoints to be used for distributed searching  |                               |
| pycsw.config.server.profiles                       | Comma delimited list of profiles to load at runtime | `apiso`                              |
| pycsw.config.server.workers                        | Number of worker threads for the WSGI catalogue server  | `2`                              |
| pycsw.config.manager.transactions                        | Whether to enable transactions  | `false`                              |
| pycsw.config.manager.allowed_ips                       | Comma delimited list of IP addresses, wildcards or CIDR notations allowed to perform transactions | `127.0.0.1`                              |
| pycsw.config.metadata                       | Metadata for the catalogue CSW GetCapabilities document and OGC API landing page  | See https://docs.pycsw.org/en/latest/configuration.html                             |
| pycsw.config.repository.database                       | The full file path to the metadata database, in database URL format  | `postgresql://postgres:mypass@resource-catalogue-db/pycsw`                              |
| pycsw.config.repository.table                       | The table name for metadata records  | `records`                              |
| pycsw.config.inspire                       | INSPIRE specific metadata for the catalogue CSW GetCapabilities document and OGC API landing page  | See https://docs.pycsw.org/en/latest/configuration.html                              |