# IAM BB Helm Chart

**TODO: Adapt to match EOEPCA 2.1**

## Introduction

This README provides an overview of the EOEPCA Identity and Access
Management Building Block (IAM BB) Helm chart and the main configuration
options it offers.

For more general instructions for installing the IAM BB using Helm you
should refer to the respective section of the
[Installation Guide](https://eoepca.readthedocs.io/projects/iam/en/latest/admin/installation/installation/#deployment-via-helm).

Details about the individual settings that can be made are documented
directly in the
[default `values.yaml` file](https://github.com/EOEPCA/helm-charts-dev/blob/develop/charts/iam-bb/values.yaml)

## Components

The Helm chart is able to install the following components:

* Keycloak (via Keycloak Operator)
* Open Policy Administration Layer (OPAL) with an embedded or separate
  instance of Open Policy Agent (OPA)
* APISIX (optional)
* Configuration for Crossplane Keycloak Provider (optional, via
  `iam-bb-config´ Helm chart) 

All components can be enabled or disabled separately. Keycloak and OPAL with
OPA are enabled by default. They are the core components of the IAM BB.
APISIX and the Crossplane configuration are disabled by default.

In simple cases (e.g. for evaluation), APISIX can be installed as part of
the IAM BB by enabling it in the `values.yaml` file. In most cases, however,
it should be installed separately as an infrastructure service and in a
separate namespace.
This can be done using the IAM BB Helm chart by enabling APISIX and
disabling all other components. Alternatively, APISIX can be installed
via its standard Helm chart. In this case, the global redirect and port
correction rules should be applied manually. In both cases, APISIX should
be deployed prior to the IAM BB, because the IAM BB relies on its CRDs.

The optional Crossplane configuration is provided as a separate Helm chart
(`iam-bb-config`), which can be applied separately or as part of the
`iam-bb` Helm chart. It provides a global `ProviderConfig` that is linked
to Keycloak and can also preconfigure a client for OPA as a Crossplane CR.
As an alternative to installing the `iam-bb-config` Helm chart, the
required clients can also be configured manually. Note that the
`iam-bb-config` Helm chart requires Crossplane and the Crossplane
Keycloak Provider to be present. It does not deploy them itself.

## Optional prerequisites

Depending on the settings in the `values.yaml` file, the `iam-bb`
and/or `iam-bb-config` Helm chart may depend on additional
software components. If required, these components must be installed
prior to the IAM BB. Note that the default settings in the `values.yaml`
file acer chosen to avoid all of the dependencies listed below.
So no additional software is required by default.

* *Crossplane Keycloak Provider*: If the parameter
  `iam.keycloak.configuration.useCrossplane` is set to `true`,
  the `iam-bb-config` Helm chart depends on the CRDs of the
  Crossplane Keycloak Provider, which in turn depends on
  Crossplane.
* *External Secrets Operator* (ESO):
  * If a separate target namespace
    for Crossplane resources is selected through the parameter
    `iam.config.targetNamespace` and the parameter
    `iam.config.propagateSecrets` is `true`, the `iam-bb-config`
    Helm chart creates external secrets in the target namespace and
    thus depends on ESO.
  * If a separate Crossplane target namespace is selected and the
    parameter `iam.keycloak.configuration.createSecretStore` is
    set to `true` or `auto`, the `iam-bb` Helm chart generates
    a cluster secret store and thus depends on ESO.
* *Kubernetes Secret Generator* (KSO): If the parameter
  `iam.keycloak.configuration.useSecretGenerator` is set to
  `true`, the `iam-bb` Helm chart generates annotations for
  KSO, which only work if KSO is installed. Note that KSO is
  *not* part of a typical EOEPCA setup.

## Background Information

### Value file structure

The `values.yaml` file consists of the following sections:

* `global`: A few global settings that apply to the IAM BB Helm chart as
  well as to its subcharts.
* `iam`: Main configuration section for the IAM BB. Most relevant settings
  can be made here. Some settings are propagated to other sections through
  yaml anchors in order to minimize redundant settings in service-specific
  sections. Make sure to preserve the anchors and references to them when
  changing settings that use anchors.
* `keycloak-operator`: IAM-BB-specific settings for the Keycloak Operator
  and Keycloak. This section configures Keycloak for the IAM BB and allows
  customizing settings that are not covered by the `iam` section.
* `keycloak`: Former IAM-BB-specific settings for Keycloak Bitnami Chart.
  Not supported any more.
* `opal`: IAM-BB-specific settings for OPAL and OPA. This section
  configures OPAL and OPA for the IAM BB and allows customizing settings
  that are not covered by the `iam` section.
* `apisix`: IAM-BB-specific settings for APISIX. Only relevant if APISIX
  is deployed through the IAM BB Helm chart. Customizations should rarely
  be necessary.
* `iam-bb-config`: Settings for the `iam-bb-config` subchart. Should not
  be changed. All values are propagated here via yaml anchors.

In a custom `values.yaml` file, settings may be omitted if they do not
deviate from the default. If settings that are propagated by anchors
are omitted, all references to the respective anchors must be removed as
well. Vice versa, references should only be removed if the settings
they refer to are also removed in order to avoid inconsistencies.

### Realm initialization process

Realm initialization is split into two phases. The first phase (basic
initialization) is set up by the IAM BB Helm chart as a
`KeycloakRealmImport` resource if `iam.keycloak.configuration.realm.create`
is set to `true`.

During this phase, the EOEPCA realm itself is created. If
`iam.keycloak.configuration.provider.createServiceAccount` is also set
to `true`, additionally a Keycloak client with an associated service
account is created that has administrative rights on the created realm.
This client is intended to be used by the Crossplane Keycloak Provider
to further populate the EOEPCA realm.

The second realm initialization phase is performed by the `iam-bb-config`
Helm chart. It relies on Crossplane and the Crossplane Keycloak Provider
and only works if both are available. The `iam-bb-config` Helm
chart is applied as a subchart if `iam.config.enabled` is set to `true`.
Alternatively it can be applied manually. In both cases, Crossplane CRs
are only actually generated if `iam.keycloak.configuration.useCrossplane`
is set to `true`.

The `iam-bb-config` Helm chart creates a `ProviderConfig` for the
Crossplane Keycloak Provider if
`iam.keycloak.configuration.provider.create` is set to `true`. This is
the preferred option, because it allows full automation of the
initialization process. The created provider is limited to the EOEPCA
realm. It can (and should) also be used by other BBs to perform Keycloak
setup.

Alternatively, an existing `ProviderConfig` can be reused by setting
`iam.keycloak.configuration.provider.existingConfigRef` to its name.
However, this only makes sense if the `iam-bb-config` Helm chart
is deployed independently of Keycloak in a separate step.

The `iam-bb-config` Helm chart also creates a Keycloak client for
external access to OPA if `iam.keycloak.configuration.createClients`
is set to `true`.

Optionally, the `iam-bb-config` chart is also able to create the realm as
a Crossplane CR (if `iam.keycloak.configuration.realm.createUsingCrossplane`
is `true`). However, this is deprecated and only makes sense in very rare
cases and should generally be avoided. In any case, this requires using an
existing `ProviderConfig` that grants full admin access to Keycloak.

The Crossplane resources can be installed in a separate namespace by
setting `iam.config.targetNamespace` accordingly or by installing the
`iam-bb-config` Helm chart directly into the desired target namespace.
If a separate target namespace is configured, the Helm chart can
optionally generate External Secrets Operator resources to propagate
the required secrets into the target namespace (see
`iam.config.propagateSecrets`).

## Deployment Options

This section describes the major options that the IAM BB Helm chart
offers. For additional details and further possibilities please refer
to the comments in the
[default `values.yaml` file](https://github.com/EOEPCA/helm-charts-dev/blob/develop/charts/iam-bb/values.yaml).

### Selection of components

| Parameter                 | Default | Description                                                                                                           |
|---------------------------|---------|-----------------------------------------------------------------------------------------------------------------------|
| `iam.keycloak.enabled`    | `true`  | Determines if Keycloak shall be installed.                                                                            |
| `iam.opa.enabled`         | `true`  | Determines if OPAL and OPA shall be installed.                                                                        |
| `iam.apisix.enabled`      | `false` | Determines if APISIX shall be installed as part of the IAM BB. Set this to `true` to deploy it along with the IAM BB. |
| `iam.config.enabled`      | `false` | Determines if the Crossplane-based realm configuration (`iam-bb-config` Helm chart) shall be applied.                 |

Each component can be deployed separately by installing the IAM BB Helm
chart multiple times with different settings for the `enabled` flags. This
may be helpful e.g. if they shall appear as separate apps in ArgoCD.

In a simple setup (e.g. for evaluation), the default set of components
(plus APISIX) should be selected. In more complex setups, it
is better to deploy APISIX separately as an infrastructure
component. Keycloak and OPAL/OPA should be deployed together unless
there is a good reason to separate them.

#### Considerations for Crossplane-based realm configuration

By default, the `iam-bb-config` Helm chart is not applied automatically,
because it requires Crossplane and the Crossplane Keycloak Provider
to be installed. When deploying EOEPCA as a whole or a selection of BBs
that includes the Workspace BB, these are required anyway and should
be preinstalled. In this case `iam.config.enabled` should be set to
`true`. In conjunction with further options, this allows for a fully
automated initialisation process.

However, there may be cases where this is not possible. E.g., for
security reasons, the IAM BB might be installed in a secured environment
that is separated from the remaining EOEPCA environment and that may
not have Crossplane installed. In such an environment, it is not
possible to apply the `iam-bb-config` Helm chart as a subchart. In this
case, there are the following alternatives:

* Apply the `iam-bb-config` Helm chart separately from the "main"
  EOEPCA environment. The referenced secrets have to be taken over
  manually before in this case.
* Configure the `ProviderConfig` (if Crossplane shall be used) and
  required Keycloak clients manually. If desired, Keycloak clients
  can also be included in the basic realm configuration (see
  `iam.keycloak.configuration.realm.customClients` option).

### Basic realm initialization

**TODO: Update to Operator-based realm initialization***

Basic realm initialisation is controlled by the following options:

| Parameter                                                  | Default  | Description                                                                                |
|------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------|
| `iam.keycloak.configuration.realm.create`                  | `true`   | Enable or disable creation of realm.                                                       |
| `iam.keycloak.configuration.realm.name`                    | "eoepca" | Internal name (identifier) of the EOEPCA realm                                             |
| `iam.keycloak.configuration.realm.displayName`             | "EOEPCA" | Display name of the EOEPCA realm                                                           |
| `iam.keycloak.configuration.realm.customClients`           | []       | List of extra clients to create during basic realm initialization                          |
| `iam.keycloak.configuration.realm.customUsers`             | []       | List of extra users to create during basic realm initialization                            |
| `iam.keycloak.configuration.realm.customSettings`          | unset    | Extra realm configuration to apply during initial realm initialization                     |
| `iam.keycloak.configuration.provider.createServiceAccount` | `false`  | Enable or disable creation of client and service account for Crossplane Keycloak Provider. |
| `iam.keycloak.configuration.provider.clientSecret`         | ""       | Client secret for the service account                                                      |
| `iam.keycloak.configuration.provider.secretRef`            | unset    | Reference to an existing secret that contains Keycloak location and credentials            |
| `iam.keycloak.configuration.provider.existingConfigRef`    | unset    | Reference to an existing `ProviderConfig` to use                                           |

For a fresh IAM BB setup, `realm.create` should be set to
`true`, and `createServiceAccount` should also be set to `true` if
Crossplane shall be used. The other values should typically be left
untouched. Leaving `createServiceAccount` at its default
value `false` may be useful if Crossplane is not used or if it is
intended to set up the service account manually. In both cases, the
`iam-bb-config` Helm chart cannot be applied automatically.

The initial realm configuration can be tailored using the `custom*`
parameters. The substructure of these parameters matches that of
the corresponding structures of a Keycloak realm export. Note,
however, that `customSettings` must not contain any settings that
are covered by other parameters, like realm namd, clients or users.
Also note that the initial realm configuration is only applied
when the realm is created. The realm is never updated automatically.

By default, the client secret is generated automatically.

### Crossplane support

The `iam-bb-config` Helm chart can be applied manually or as a subchart
of the `iam-bb` Helm chart by setting `iam.config.enabled` to `true`.
In both cases, the following parameters are available. They are used
by both Helm charts and must be kept consistent if the `iam-bb-config`
chart is executed manually. Note that some parameters are shared with
basic initialisation.

| Parameter                                               | Default  | Description                                                           |
|---------------------------------------------------------|----------|-----------------------------------------------------------------------|
| `iam.keycloak.configuration.useCrossplane`              | `false`  | Enable or disable creation of Crossplane CRs. (main switch)           |
| `iam.keycloak.configuration.createClients`              | `true`   | Enable or disable creation of clients as Crossplane CRs.              |
| `iam.keycloak.configuration.realm.name`                 | "eoepca" | Internal name (identifier) of the EOEPCA realm                        |
| `iam.keycloak.configuration.provider.create`            | `true`   | Enable or disable creation of the `ProviderConfig`.                   |
| `iam.keycloak.configuration.provider.clientSecret`      | ""       | Client secret for the Crossplane provider client                      |
| `iam.keycloak.configuration.provider.secretRef`         | unset    | Reference to a secret that contains Keycloak location and credentials |
| `iam.keycloak.configuration.provider.existingConfigRef` | ""       | Name of an existing `ProviderConfig` to use                           |
| `iam.config.targetNamespace`                            | ""       | Name of separate namespace for Crossplane resources                   |

For a typical IAM BB setup, Crossplane should be leveraged. Hence
`useCrossplane` should be set to `true`. The other settings can
safely be left at their defaults.
The provider client secret is generated automatically in this case.
Client names and secrets for the OPA client are shared
with the route configuration. See the following sections for details.

### Routes

The Helm chart is able to create routes for Keycloak and OPA.
Routes are only generated for components that are enabled.
Route generation can be further controlled by the following parameters:

| Parameter                         | Default        | Description                                             |
|-----------------------------------|----------------|---------------------------------------------------------|
| `iam.keycloak.createRoute`        | `true`         | Enable or disable creation of route for Keycloak.       |
| `iam.opa.createRoute`             | `true`         | Enable or disable creation of route for OPA.            |
| `iam.opa.clientId`                | "opa"          | Client ID for OPA client                                |
| `iam.opa.clientSecret`            | ""             | Client secret for OPA client                            |
| `iam.opa.clientSecretRef`         | ""             | Name of existing secret that contains the client secret |

Thus by default, a route is created for each component that is enabled.
For security reasons, however, route creation should be disabled for
components that need not be accessed from the Internet. In a single-cluster
setup, this typically applies to OPA.

By default, secrets are generated automatically. If `clientSecretRef`
is used to reference an existing secret, this secret may contain further
parameters like the client ID.

### CORS Configuration

Enable CORS for JavaScript applications from different domains to authenticate
with Keycloak.

| Parameter                            | Default | Description                                           |
|--------------------------------------|---------|-------------------------------------------------------|
| `iam.keycloak.cors.enabled`          | `false` | Enable CORS for Keycloak route                        |
| `iam.keycloak.cors.allowedOrigins`   | `*`     | Comma-separated list of allowed origins.              |
| `iam.keycloak.cors.allowedHeaders`   | `*`     | Comma-separated list of allowed headers.              |
| `iam.keycloak.cors.exposedHeaders`   | `*`     | Comma-separated list of exposed headers.              |
| `iam.keycloak.cors.allowedMethods`   | (all)   | Comma-separated list of allowed methods.              |
| `iam.keycloak.cors.allowCredentials` | `true`  | Allow credentials (cookies, auth headers) in requests |
| `iam.keycloak.cors.mayAge`           | 3600    | Pre-flight cache max age in seconds                   |

**Note:** When credentials are enabled with specific origins, browsers
reject wildcard `*`. List all origins and headers explicitly for multi-tenant setups.

The default for `allowedMethods` is to allow all standard HTTP methods, i.e.,
GET,HEAD,PUT,PATCH,POST,DELETE and OPTIONS.

#### Example

```yaml
keycloak:
  cors:
    enabled: true
    allowedOrigins: "https://eoapi.develop.eoepca.org,https://another-app.develop.eoepca.org"
    allowedHeaders: "X-Custom-Header,X-Another-Header"
    exposedHeaders: "X-Custom-Header"
    allowCredentials: true
```

### Handling of secrets

The Helm chart supports four approaches to specify or generate client
secrets:

1. Client secrets can be specified literally in the `*.clientSecret`
   parameter.
2. Client secrets can be specified through an existing secret using the
   `*.clientSecretRef` parameter.
3. Client secrets that are not specified explicitly can be generated by
   two means:
   1. Using Helm's `randAlphaNum` function. This is the default.
      Existing values are preserved on `helm upgrade`. Note that this
      approach does not work well with ArgoCD, because ArgoCD uses
      `helm template` instead of `helm upgrade`, which causes secrets
      to be regenerated on every sync.
   2. By generating annotations for `kubernetes-secret-generator`.
      This is the case if the parameter
      `iam.keycloak.configuration.useSecretGenerator` is set to `true`.
      This approach only works if `kubernetes-secret-generator` is
      installed. Value generation is controlled by
      `kubernetes-secret-generator` (independently of Helm).

The recommended approach for operational use is to specify secret
values as existing secrets, because this provides full control over
them.

Note that the client secret for the Crossplane Keycloak provider
cannot be generated using `kubernetes-secret-generator`. It is
generated using `randAlphaNum` even if `useSecretGenerator` is set
to `true`.

The `*.clientSecretRef` parameters are of type string and
simply specify a secret name. However,
`iam.keycloak.configuration.provider.secretRef` is a
structured value, and the secret it refers to must contain the
complete provider configuration instead of just the client secret.
See `values.yaml` file for more details.

### OPA deployment

By default, OPA is deployed in a separate pod. This has the advantage
that the version of OPA can be chosen freely and is not tied to the one
that comes with OPAL. The OPA image to use can be specified through
the structured parameter `iam.opa.image`.

By setting the parameter `iam.opa.inline` to `true`, the Helm chart
can be instructed *not* to deploy OPA in a separate pod. In this case the
used OPA version is the one that comes with OPAL, which may be outdated.

In addition to setting the parameter `iam.opa.inline` to `true`, the
parameter `opal.client.extraEnv.OPAL_INLINE_OPA_ENABLED` must be
set to `"True"` so that inline OPA is actually started.
