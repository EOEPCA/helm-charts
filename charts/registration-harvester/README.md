# Helm chart for Registration Harvester component

## Chart Components

* Creates a Registration Harvester deployment.
* Creates a Kubernetes Service for the Harvester API on specified port (default: 8080)
* Creates a Harvester API Ingress controler.

## Installing the Chart

You can install the chart with the release name `registration-harvester` in `eoepca` namespace as below.

```bash
$ helm install registration-harvester charts/registration-harvester
```

## Values

The configuration parameters in this section control the Harvester configuration.