# IAM BB Helm Chart

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

* Keycloak
* Open Policy Administration Layer (OPAL) with an embedded or separate
  instance of Open Policy Agent (OPA)
* Identity API (optional, deprecated)
* APISIX (optional)
* Configuration for Crossplane Keycloak Provider (optional, via
  `iam-bb-config´ Helm chart) 

All components can be enabled or disabled separately. Keycloak and OPAL with
OPA are enabled by default. They are the core components of the IAM BB.
APISIX is also enabled by default to facilitate a simple setup of the IAM BB
with APISIX for evaluation. Identity API and the Crossplane configuration
are disabled by default.

Identity API is only provided for compatibility with old code from EOEPCA 1.4
and should not be used unless required for this purpose. It will be
removed in a later release.

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
to Keycloak and can also preconfigure clients for OPA and/or Identity API
as Crossplane CRs. As an alternative to installing the `iam-bb-config`
Helm chart, the required clients can also be configured manually. Note that
the `iam-bb-config` Helm chart requires Crossplane and the Crossplane
Keycloak Provider to be present. It does not deploy them itself.

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
* `keycloak`: IAM-BB-specific settings for Keycloak. This section
  configures Keycloak for the IAM BB and allows customizing settings that
  are not covered by the `iam` section.
* `opal`: IAM-BB-specific settings for OPAL and OPA. This section
  configures OPAL and OPA for the IAM BB and allows customizing settings
  that are not covered by the `iam` section.
* `apisix`: IAM-BB-specific settings for APISIX. Only relevant if APISIX
  is deployed through the IAM BB Helm chart. Customizations should rarely
  be necessary.
* `iam-bb-config`: Settings for the `iam-bb-config` subchart. Should not
  be changed. All values are propagated here via yaml anchors.
* `identityApi`: Redundant `enabled` setting for Identity API. This
  section is deprecated and only needed if Identity API is enabled.
  Otherwise it may be removed.
* `identity-service`: Settings for the `identity-service` subchart.
  This section is deprecated and only needed if Identity API is enabled.
  Otherwise it may be removed.

In a custom `values.yaml` file, settings may be omitted if they do not
deviate from the default. If settings that are propagated by anchors
are omitted, all references to the respective anchors must be removed as
well. Vice versa, references should only be removed if the settings
they refer to are also removed in order to avoid inconsistencies.

### Realm initialization process

Realm initialization is split into two phases. The first phase (basic
initialization) is set up by the IAM BB Helm chart using
`keycloak-config-cli` if `iam.keycloak.configuration.useKeycloakConfigCli`
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

The `iam-bb-config` Helm chart also creates Keycloak clients for external
access to OPA and Identity API if
`iam.keycloak.configuration.createClients` is set to `true`.

Optionally, the `iam-bb-config` chart is also able to create the realm as
a Crossplane CR (if `iam.keycloak.configuration.realm.create` is `true`).
However, this only makes sense in very rare cases and should generally be
avoided. In any case, this requires using an existing `ProviderConfig`
that grants full admin access to Keycloak.

## Deployment Options

This section describes the major options that the IAM BB Helm chart
offers. For additional details and further possibilities please refer
to the comments in the
[default `values.yaml` file](https://github.com/EOEPCA/helm-charts-dev/blob/develop/charts/iam-bb/values.yaml).

### Selection of components

| Parameter                 | Default | Description                                                                                                      |
|---------------------------|---------|------------------------------------------------------------------------------------------------------------------|
| `iam.keycloak.enabled`    | `true`  | Determines if Keycloak shall be installed.                                                                       |
| `iam.opa.enabled`         | `true`  | Determines if OPAL and OPA shall be installed.                                                                   |
| `iam.identityApi.enabled` | `false` | Determines if Identity API shall be installed. (deprecated)                                                      |
| `iam.apisix.enabled`      | `true`  | Determines if APISIX shall be installed as part of the IAM BB. Set this to `false` if it is deployed separately. |
| `iam.config.enabled`      | `false` | Determines if the Crossplane-based realm configuration (`iam-bb-config` Helm chart) shall be applied.            |

Each component can be deployed separately by installing the IAM BB Helm
chart multiple times with different settings for the `enabled` flags. This
may be helpful e.g. if they shall appear as separate apps in ArgoCD.

In a simple setup (e.g. for evaluation), the default set of components
(including APISIX) should be selected. In more complex setups, it
may be better to deploy APISIX separately as an infrastructure
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
possible to apply the `iam-bb-config` Helm chart. In this case, there
are the following alternatives:

* Apply the `iam-bb-config` Helm chart separately from the "main"
  EOEPCA environment. The referred secrets have to be taken over
  manually before in this case.
* Configure the `ProviderConfig` (if Crossplane shall be used) and
  required Keycloak clients manually. If desired, Keycloak clients
  can also be included in the basic configuration applied by
  `keycloak-config-cli` (see `keycloak.keycloakConfigCli.*`
  options below).

### Basic realm initialization

Basic realm initialisation is controlled by the following options:

| Parameter                                                  | Default                   | Description                                                                                |
|------------------------------------------------------------|---------------------------|--------------------------------------------------------------------------------------------|
| `iam.keycloak.configuration.useKeycloakConfigCli`          | `false`                   | Enable or disable basic realm initialization.                                              |
| `iam.keycloak.configuration.realm.name`                    | "eoepca"                  | Internal name (identifier) of the EOEPCA realm                                             |
| `iam.keycloak.configuration.realm.displayName`             | "EOEPCA"                  | Display name of the EOEPCA realm                                                           |
| `iam.keycloak.configuration.provider.createServiceAccount` | `false`                   | Enable or disable creation of client and service account for Crossplane Keycloak Provider. |
| `iam.keycloak.configuration.provider.clientSecret`         | ""                        | Client secret for the service account                                                      |
| `iam.keycloak.configuration.provider.clientSecretRef`      | unset                     | Reference to an existing secret that contains Keycloak location and credentials            |
| `keycloak.keycloakConfigCli.existingConfigMap`             | "initial-keycloak-config" | Config map that contains the realm definition                                              |
| `keycloak.keycloakConfigCli.configuration`                 | unset                     | Literal realm definition (not used by default)                                             |

For a fresh IAM BB setup, `useKeycloakConfigCli` should be set to
`true`, and `createServiceAccount` should also be set to `true` if
Crossplane shall be used. The other values should typically be left
untouched. Leaving `useKeycloakConfigCli` at its default value `false`
only makes sense for existing setups where a prior manual realm
configuration needs to be preserved. It is planned to change the default
value to `true` soon. Leaving `createServiceAccount` at its default
value `false` may be useful if Crossplane is not used or if it is
intended to set up the service account manually. In both cases, the
`iam-bb-config` Helm chart cannot be applied automatically.

By default, the parameter `keycloak.keycloakConfigCli.existingConfigMap`
refers to a config map that is generated by the Helm chart and represents
the standard realm definition. If required for some reason, the realm
definition can be customized by creating a custom config map and pointing
`existingConfigMap` to it. Alternatively, the realm definition can
be configured literally; In this case, `existingConfigMap` must explicitly
be set to `null`.

By default, the client secret is generated automatically.

### Crossplane support

The `iam-bb-config` Helm chart can be applied manually or as a subchart
of the `iam-bb` Helm chart by setting `iam.config.enabled` to `true`.
In both cases, the following parameters are available. They are used
by both Helm charts and must be kept consistent if the `iam-bb-config`
is executed manually. Note that some parameters are shared with basic
initialisation.

| Parameter                                               | Default  | Description                                                              |
|---------------------------------------------------------|----------|--------------------------------------------------------------------------|
| `iam.keycloak.configuration.useCrossplane`              | `false`  | Enable or disable creation of Crossplane CRs. (main switch)              |
| `iam.keycloak.configuration.createClients`              | `true`   | Enable or disable creation of clients as Crossplane CRs.                 |
| `iam.keycloak.configuration.realm.create`               | `false`  | Enable or disable creation of realm as Crossplane CRs. (not recommended) |
| `iam.keycloak.configuration.realm.name`                 | "eoepca" | Internal name (identifier) of the EOEPCA realm                           |
| `iam.keycloak.configuration.realm.displayName`          | "EOEPCA" | Display name of the EOEPCA realm                                         |
| `iam.keycloak.configuration.provider.create`            | `true`   | Enable or disable creation of the `ProviderConfig`.                      |
| `iam.keycloak.configuration.provider.clientSecret`      | ""       | Client secret for the Crossplane provider client                         |
| `iam.keycloak.configuration.provider.secretRef`         | unset    | Reference to a secret that contains Keycloak location and credentials    |
| `iam.keycloak.configuration.provider.existingConfigRef` | ""       | Name of an existing `ProviderConfig` to use                              |

For a typical IAM BB setup, Crossplane should be leveraged. Hence
`useCrossplane` should be set to `true`. The other settings can
safely be left at their defaults.
The provider client secret is generated automatically in this case.
Client names and secrets for OPA and Identity API clients are shared
with the route configuration. See the following sections for details.

### Routes

The Helm chart is able to create routes for Keycloak, OPA and Identity API.
Routes are only generated for components that are enabled.
Route generation can be further controlled by the following parameters:

| Parameter                         | Default        | Description                                             |
|-----------------------------------|----------------|---------------------------------------------------------|
| `iam.keycloak.createRoute`        | `true`         | Enable or disable creation of route for Keycloak.       |
| `iam.opa.createRoute`             | `true`         | Enable or disable creation of route for OPA.            |
| `iam.identityApi.createRoute`     | `true`         | Enable or disable creation of route for Identity API.   |
| `iam.opa.clientId`                | "opa"          | Client ID for OPA client                                |
| `iam.opa.clientSecret`            | ""             | Client secret for OPA client                            |
| `iam.opa.clientSecretRef`         | ""             | Name of existing secret that contains the client secret |
| `iam.identityApi.clientId`        | "identity-api" | Client ID for Identity API client                       |
| `iam.identityApi.clientSecret`    | ""             | Client secret for Identity API client                   |
| `iam.identityApi.clientSecretRef` | ""             | Name of existing secret that contains the client secret |

Thus by default, a route is created for each component that is enabled.
For security reasons, however, route creation should be disabled for
components that need not be accessed from the Internet. In a single-cluster
setup, this typically applies to OPA and maybe Identity API.

By default, secrets are generated automatically. If `clientSecretRef`
is used to reference an existing secret, this secret may contain further
parameters like the client ID.

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
      Note that new values are generated each time the Helm chart is
      applied, i.e., existing values are not preserved.
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

The `*.clientSecretRef` parameters are usually of type string and
simply specify a secret name. However,
`iam.keycloak.configuration.provider.clientSecretRef` is a
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
used OPA version is the one that comes with OPAL and that may be outdated.

In addition to setting the parameter `iam.opa.inline` to `true`, the
parameter `opal.client.extraEnv.OPAL_INLINE_OPA_ENABLED` must be
set to `"True"` so that inline OPA is actually started.
