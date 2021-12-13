# Helm chart for User Workspaces

## Prerequisites

* This chart requires Docker Engine 1.8+ in any of their supported platforms.

## Chart Components

* Creates all components from the VS Chart.
* Creates all components from the rm-resource-catalogue Chart.

## Installing the Chart

You can install the chart with the release name `rm-user-workspace` in `eoepca` namespace as below.

```bash
$ helm install user-workspace charts/rm-user-workspace
```

You can debug with:

```bash
helm install --dry-run --debug user-workspace charts/rm-user-workspace
```

## Values

The configuration parameters in this section control the resource catalogue configuration.

| Parameter                               | Description                                                                                    | Default                          |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------- |
| vs                        | The configuration tree of the VS Chart  | For the complete defaults see the values.yaml      |
| rm-resource-catalogue                                 | The configuration tree of the rm-resource-catalogue Chart  | For the complete defaults see the values.yaml       |