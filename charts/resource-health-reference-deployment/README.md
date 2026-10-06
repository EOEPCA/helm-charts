# Helm chart for reference deployment

This is a deployment of the Resource Health BB, including an OpenTelemetry-collector deployment and 
an OpenSearch deployment. This leads to a fully functional setup.

Currently there is only one mandatory values to set:
- `.Values.global.defaultInternalIssuerRef.name` must be set to the name of a `ClusterIssuer` for the internal service domain (typically `svc.cluster.local`).