{{/*
Expand the name of the chart.
*/}}
{{- define "identity-gatekeeper.name" -}}
{{- default .Chart.Name (default .Values.fullnameOverride .Values.nameOverride) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "identity-gatekeeper.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "identity-gatekeeper.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "identity-gatekeeper.labels" -}}
helm.sh/chart: {{ include "identity-gatekeeper.chart" . }}
{{ include "identity-gatekeeper.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Values.deployment.image.tag | default .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "identity-gatekeeper.selectorLabels" -}}
app.kubernetes.io/name: {{ include "identity-gatekeeper.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "identity-gatekeeper.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "identity-gatekeeper.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Return the appropriate apiVersion for ingress
*/}}
{{- define "identity-gatekeeper.ingress.apiVersion" -}}
{{- if semverCompare "<1.14-0" (include "identity-gatekeeper.kubeVersion" $) -}}
{{- print "extensions/v1beta1" -}}
{{- else if semverCompare "<1.19-0" (include "identity-gatekeeper.kubeVersion" $) -}}
{{- print "networking.k8s.io/v1beta1" -}}
{{- else -}}
{{- print "networking.k8s.io/v1" -}}
{{- end -}}
{{- end -}}

{{/*
Return the target Kubernetes version
*/}}
{{- define "identity-gatekeeper.kubeVersion" -}}
  {{- default .Capabilities.KubeVersion.Version .Values.kubeVersionOverride }}
{{- end -}}

{{/*
Internal URL for the target service
*/}}
{{- define "identity-gatekeeper.targetUrl" -}}
http://{{ .Values.targetService.name }}.{{ .Release.Namespace }}.svc.cluster.local:{{ .Values.targetService.port.number }}
{{- end }}

{{/*
Internal base URL for the services (minus port number)
*/}}
{{- define "identity-gatekeeper.baseServiceUrl" -}}
http://{{ include "identity-gatekeeper.fullname" . }}.{{ .Release.Namespace }}.svc.cluster.local
{{- end }}

{{/*
Internal URL for the proxy service
*/}}
{{- define "identity-gatekeeper.proxyServiceUrl" -}}
{{ include "identity-gatekeeper.baseServiceUrl" . }}:{{ .Values.service.proxy.port }}
{{- end }}

{{/*
Internal URL for the admin service
*/}}
{{- define "identity-gatekeeper.adminServiceUrl" -}}
{{ include "identity-gatekeeper.baseServiceUrl" . }}:{{ .Values.service.admin.port }}
{{- end }}

{{/*
Ingress server-snippets - merged from constituent parts
*/}}
{{- define "identity-gatekeeper.ingressServerSnippet" -}}
{{ .Values.ingress.serverSnippets.custom }}
{{ .Values.ingress.serverSnippets.gatekeeper }}
{{ tpl .Values.ingress.serverSnippets.auth $ }}
{{- end }}
