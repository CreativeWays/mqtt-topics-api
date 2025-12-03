{{/*
Expand the name of the chart.
*/}}
{{- define "mqtt-topics-api.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "mqtt-topics-api.fullname" -}}
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
Common labels
*/}}
{{- define "mqtt-topics-api.labels" -}}
helm.sh/chart: {{ include "mqtt-topics-api.name" . }}-{{ .Chart.Version | replace "+" "_" }}
app.kubernetes.io/name: {{ include "mqtt-topics-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Service labels
*/}}
{{- define "mqtt-topics-api.serviceLabels" -}}
{{ include "mqtt-topics-api.labels" . }}
app.kubernetes.io/component: service
{{- end }}

{{/*
Image name for a service
*/}}
{{- define "mqtt-topics-api.image" -}}
{{- $service := .service -}}
{{- with .context.Values.global.image }}
{{- printf "%s/%s:%s" .repository $service .tag }}
{{- end }}
{{- end }}
