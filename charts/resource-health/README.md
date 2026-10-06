# Helm-chart for Resource Health Core

This Helm-chart covers the core components of the Resource Health BB, and assumes you have separately provisioned the equivalent of an OpenTelemetry-collector (i.e. an OTLP endpoint) and a database to query (i.e. an equivalent of OpenSearch).

For a complete deployment, see `resource-health-reference-deployment`.