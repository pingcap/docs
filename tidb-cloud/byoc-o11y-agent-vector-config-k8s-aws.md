```yaml
# Please replace the variables in the ${} format in the configuration appropriately.

customConfig:
  data_dir: /vector-data-dir
  api:
    enabled: true
    address: 0.0.0.0:8686
    playground: false

  sources:
    all_logs:
      type: kubernetes_logs
    journald:
      type: journald

    self_metrics:
      type: internal_metrics

    oom_filenames:
      type: filename
      include:
        - /var/tidb_oom_record/**/*

    replayer_filenames:
      type: filename
      include:
        - /var/tidb_plan_replayer/**/*

    self_logs:
      type: internal_logs

  transforms:
    ensure_component:
      type: remap
      inputs:
        - all_logs
      drop_on_error: true
      reroute_dropped: true
      source: |-
        if !is_null(.kubernetes.container_name) && .kubernetes.container_name == "slowlog" {
          .o11y.component = "slowlog"
        } else if !is_null(.kubernetes.container_name) && .kubernetes.container_name == "statementlog" {
          .o11y.component = "statementlog"
        } else if !is_null(.kubernetes.pod_labels."app.kubernetes.io/component") {
          .o11y.component = .kubernetes.pod_labels."app.kubernetes.io/component"
        } else if !is_null(.kubernetes.container_name) {
          .o11y.component = .kubernetes.container_name
        } else {
          .o11y.component = "unknown"
        }
    route_logs:
      type: route
      inputs:
        - ensure_component
      route:
        tidb_cluster_general_logs: |-
          includes(["tidb","tikv","pd","ticdc","tiflash","tiflash-learner","db-tidb-extra-access","backup","restore","tidb-lightning","dm-master","dm-worker","extra-tidb","statementlog"], .o11y.component)
        tidb_cluster_slow_logs: |-
          .o11y.component == "slowlog"
        infra_logs: |-
          !includes(["tidb","tikv","pd","ticdc","tiflash","tiflash-learner","db-tidb-extra-access","backup","restore","tidb-lightning","dm-master","dm-worker","extra-tidb","slowlog","statementlog"], .o11y.component)
    multiline_slow_logs:
      type: reduce
      inputs:
        - route_logs.tidb_cluster_slow_logs
      starts_when:
        type: vrl
        source: |-
          res, err = starts_with(.message, "# Time: ")
          if err != null {
            false
          } else {
            res
          }
      merge_strategies:
        message: concat_newline

    ensure_cluster_id:
      type: remap
      inputs:
        - multiline_slow_logs
        - route_logs.tidb_cluster_general_logs
      drop_on_error: true
      reroute_dropped: true
      source: |-
        if !is_null(.kubernetes.pod_labels."tags.tidbcloud.com/cluster") {
          .o11y.cluster_id = .kubernetes.pod_labels."tags.tidbcloud.com/cluster"
        } else {
          parsed, err = parse_grok(.kubernetes.pod_namespace, "tidb%{GREEDYDATA:cluster_id}")
          if err == null {
            .o11y.cluster_id = parsed.cluster_id
          } else {
            .o11y.cluster_id = "unknown"
          }
        }
        if is_null(.kubernetes.pod_labels.app) {
          .kubernetes.pod_labels.app = .kubernetes.pod_name
        }
        if is_null(.kubernetes.pod_labels.release) {
          .kubernetes.pod_labels.release = "unknown"
        }
    enrich_tidb_cluster_log_message:
      type: remap
      inputs:
        - ensure_cluster_id
      drop_on_error: true
      reroute_dropped: true
      source: |-
        t = to_string!(.timestamp)
        node = .kubernetes.pod_node_name
        pod_namespace = .kubernetes.pod_namespace
        pod_name = .kubernetes.pod_name
        container_name = .kubernetes.container_name
        prefix = join!([t, node, pod_namespace, pod_name, container_name], ";")
        new_message, err = prefix + " " + .message
        if err == null {
          .message = new_message
        }
    enrich_infra_log_message:
      type: remap
      inputs:
        - route_logs.infra_logs
      drop_on_error: true
      reroute_dropped: true
      source: |-
        t = to_string!(.timestamp)
        node = .kubernetes.pod_node_name
        pod_namespace = .kubernetes.pod_namespace
        pod_name = .kubernetes.pod_name
        container_name = .kubernetes.container_name
        prefix = join!([t, node, pod_namespace, pod_name, container_name], ";")
        new_message, err = prefix + " " + .message
        if err == null {
          .message = new_message
        }
    ensure_general_cluster_id:
      type: remap
      inputs:
        # pod logs except tidb cluster general logs
        - route_logs.infra_logs
        # unmatched logs
        - ensure_component.dropped
        - route_logs._unmatched
        - ensure_cluster_id.dropped
      drop_on_error: true
      reroute_dropped: true
      source: |-
        .o11y.cluster_id = "general_component"
        if is_null(.kubernetes.pod_labels.app) {
          .kubernetes.pod_labels.app = .kubernetes.pod_name
        }
        if is_null(.kubernetes.pod_labels.release) {
          .kubernetes.pod_labels.release = "unknown"
        }
    oom_file_key_transform:
      type: remap
      inputs:
        - oom_filenames
      source: |-
        fields = split!(.message, "/")
        # /var/tidb_oom_record/1/9993/337845892/tidb337845892/db-tidb-0/running_sql2022-12-06T10:26:43Z
        isV1 = length(fields) == 9
        # /var/tidb_oom_record/1/9993/337845892/tidb337845892/db-tidb-0/record2022-12-06T10:26:43Z/running_sql
        isV2 = length(fields) == 10
        assert!(isV1 || isV2)
        tenant_id = fields[3]
        project_id = fields[4]
        cluster_id = fields[5]
        module = "oom_record"
        component = replace!(fields[7], r'^.+?-(?P<component>.+)-.*', "$$component")
        generating_timestr = replace!(fields[8], r'^[^0-9]*', "")
        generating_unix = to_string(to_unix_timestamp(parse_timestamp!(generating_timestr, "%+")))
        instance = replace!(fields[7], r'^.+?-', "")
        if isV1 {
          filename = fields[8]
          .key = join!(["0", tenant_id, project_id, cluster_id, module, component, generating_unix, instance, filename], separator: "/")
        } else if isV2 {
          filename = join!([fields[9], generating_timestr])
          .key = join!(["0", tenant_id, project_id, cluster_id, module, component, generating_unix, instance, filename], separator: "/")
        }
    replayer_file_key_transform:
      type: remap
      inputs:
        - replayer_filenames
      source: |-
        # v1: /var/tidb_plan_replayer/1/9993/337845892/tidb337845892/db-tidb-0/replayer_single_3Z90hA56EN0g4_Iav6PcZQ==_1670838592076844774.zip
        # v2: /var/tidb_plan_replayer/1/9993/337845892/tidb337845892/db-tidb-0/replayer_r4hyX-MHJmxGo9rXva9fEg==_1670834504569984706.zip
        fields = split!(.message, "/")
        tenant_id = fields[3]
        project_id = fields[4]
        cluster_id = fields[5]
        module = "plan_replayer"
        component = replace!(fields[7], r'^.+?-(?P<component>.+)-.*', "$$component")
        generating_timestr = replace!(fields[8], r'^replayer.+_(?P<ts>\d+)\.zip', "$$ts")
        generating_unix = slice!(generating_timestr, 0, length(generating_timestr) - 9)
        instance = replace!(fields[7], r'^.+?-', "")
        filename = fields[8]
        .key = join!(["0", tenant_id, project_id, cluster_id, module, component, generating_unix, instance, filename], separator: "/")
  sinks:
    s3_infra_logs:
      type: aws_s3
      inputs:
        - enrich_infra_log_message
      region: ${REGION}
      bucket: ${BUCKET}
      key_prefix: |-
        1/${TENANT_ID}/${PROJECT_ID}/k8s-infra/logs/{{ `{{ o11y.component }}` }}/
      compression: gzip
      batch:
        max_bytes: 104857600 # 100MB
        timeout_secs: 180 # 3 minutes
      buffer:
        type: disk
        max_size: 1073741824 # 1GB
      encoding:
        codec: text
      auth:
        # hostNetwork must be enabled
        assume_role: ${ROLE_ARN}

    s3_tidb_cluster_logs:
      type: aws_s3
      inputs:
        - enrich_tidb_cluster_log_message
      region: ${REGION}
      bucket: ${BUCKET}
      key_prefix: |-
        0/${TENANT_ID}/${PROJECT_ID}/{{ `{{ o11y.cluster_id }}` }}/logs/{{ `{{ o11y.component }}` }}/
      compression: gzip
      batch:
        max_bytes: 104857600 # 100MB
        timeout_secs: 60 # 1 minute
      buffer:
        type: disk
        max_size: 1073741824 # 1GB
      encoding:
        codec: text
      auth:
        # hostNetwork must be enabled
        assume_role: ${ROLE_ARN}

    s3_unmatched_kubernetes_logs:
      type: aws_s3
      inputs:
        - ensure_component.dropped
        - route_logs._unmatched
        - ensure_cluster_id.dropped
        - enrich_tidb_cluster_log_message.dropped
        - enrich_infra_log_message.dropped
      region: ${REGION}
      bucket: ${BUCKET}
      key_prefix: |-
        1/${TENANT_ID}/${PROJECT_ID}/k8s-infra/logs/_unmatched/
      compression: gzip
      batch:
        max_bytes: 104857600 # 100MB
        timeout_secs: 180 # 3 minutes
      buffer:
        type: disk
        max_size: 1073741824 # 1GB
      encoding:
        codec: json
      auth:
        # hostNetwork must be enabled
        assume_role: ${ROLE_ARN}

    s3_journald_logs:
      type: aws_s3
      inputs:
        - journald
      region: ${REGION}
      bucket: ${BUCKET}
      key_prefix: |-
        1/${TENANT_ID}/${PROJECT_ID}/k8s-infra/logs/journald/{{ `{{ host }}` }}/
      compression: gzip
      batch:
        max_bytes: 104857600 # 100MB
        timeout_secs: 180 # 3 minutes
      buffer:
        type: disk
        max_size: 1073741824 # 1GB
      encoding:
        codec: text
      auth:
        # hostNetwork must be enabled
        assume_role: ${ROLE_ARN}
    self_metrics_sink:
      type: prometheus_exporter
      inputs:
        - self_metrics
      address: "0.0.0.0:9598"

    loki_pod_logs:
      type: loki
      inputs:
      # tidb cluster general logs
      - ensure_cluster_id
      # infra component logs
      - ensure_general_cluster_id

      encoding:
        codec: text
      compression: gzip
      endpoint: ${LOKI_URL}
      labels:
        cluster_env: "${CLUSTER_ENV}"
        cluster: "${PROVIDER}-dataplane/${K8S_CLUSTER_NAME}"
        tenant_id: "${TENANT_ID}"
        project_id: "${PROJECT_ID}"
        cluster_id: '{{ "{{ o11y.cluster_id }}" }}'
        node: '{{ "{{ kubernetes.pod_node_name }}" }}'
        namespace: '{{ "{{ kubernetes.pod_namespace }}" }}'
        instance: '{{ "{{ kubernetes.pod_name }}" }}'
        container: '{{ "{{ kubernetes.container_name }}" }}'
        app: '{{ "{{ kubernetes.pod_labels.app }}" }}'
        release: '{{ "{{ kubernetes.pod_labels.release }}" }}'
        stream: '{{ "{{ stream }}" }}'
      out_of_order_action: accept # require Loki >= 2.4.0
      batch:
        max_bytes: 10240 # 10KiB
        timeout_secs: 1
      buffer:
        max_size: 2147483648 # 2GiB
        type: disk
    loki_sys_logs:
      type: loki
      inputs:
      - journald
      encoding:
        codec: json
      compression: gzip
      endpoint: ${LOKI_URL}
      labels:
        cluster_env: "${CLUSTER_ENV}"
        cluster: "${PROVIDER}-dataplane/${K8S_CLUSTER_NAME}"
        tenant_id: "${TENANT_ID}"
        project_id: "${PROJECT_ID}"
        node: '{{ "{{ host }}" }}'
        syslog: '{{ "{{ SYSLOG_IDENTIFIER }}" }}'
      out_of_order_action: accept # require Loki >= 2.4.0
      batch:
        max_bytes: 10240 # 10KiB
        timeout_secs: 1
      buffer:
        max_size: 2147483648 # 2GiB
        type: disk


    s3_upload_oom_file:
      type: aws_s3_upload_file
      inputs:
        - oom_file_key_transform
      region: ${REGION}
      bucket: ${BUCKET}
      auth:
        assume_role: ${ROLE_ARN}

    s3_upload_replayer_file:
      type: aws_s3_upload_file
      inputs:
        - replayer_file_key_transform
      region: ${REGION}
      bucket: ${BUCKET}
      auth:
        assume_role: ${ROLE_ARN}

    self_logs_sink:
      type: loki
      inputs:
        - self_logs
      encoding:
        codec: json
      compression: gzip
      endpoint: ${LOKI_URL}
      labels:
        cluster_env: "${CLUSTER_ENV}"
        cluster: "${PROVIDER}-dataplane/${K8S_CLUSTER_NAME}"
        app: "vector_log_agent"
        node: '{{ "{{ host }}" }}'
      out_of_order_action: accept # require Loki >= 2.4.0
      batch:
        max_bytes: 10240 # 10KiB
        timeout_secs: 1
      buffer:
        max_size: 1073741824 # 1GiB
        type: disk

# extraVolumes -- Additional Volumes to use with Vector Pods
extraVolumes:
  - name: machine-id
    hostPath:
      path: /etc/machine-id
      type: File
  - name: tidb-oom-record
    hostPath:
      path: /var/tidb_oom_record
      type: DirectoryOrCreate
  - name: tidb-plan-replayer
    hostPath:
      path: /var/tidb_plan_replayer
      type: DirectoryOrCreate

# extraVolumeMounts -- Additional Volume to mount into Vector Containers
extraVolumeMounts:
  - name: machine-id
    mountPath: /etc/machine-id
    readOnly: true
  - name: tidb-oom-record
    mountPath: /var/tidb_oom_record
  - name: tidb-plan-replayer
    mountPath: /var/tidb_plan_replayer

# resources -- Set Vector resource requests and limits.
resources:
  requests:
    cpu: ${REQUEST_CPU}
    memory: ${REQUEST_MEMORY}
  limits:
    cpu: ${LIMIT_CPU}
    memory: ${LIMIT_MEMORY}

role: "Agent"

## Configuration for Vector's data persistence
## Persistence always used for Agent role
persistence:
  hostPath:
    # persistence.hostPath.path -- Override path used for hostPath persistence
    ## Valid for Agent role
    path: "/var/lib/vector/01"

# rollWorkload -- Add a checksum of the generated ConfigMap to workload annotations
rollWorkload: true

## Define the Vector image to use
image:
  # image.repository -- Override default registry + name for Vector
  repository: ${IMAGE_REPO}
  # image.pullPolicy -- Vector image pullPolicy
  pullPolicy: IfNotPresent
  tag: ${IMAGE_TAG}

# dnsPolicy -- Specify DNS policy for Vector Pods
## Ref: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy
dnsPolicy: ClusterFirst

## Configure a HorizontalPodAutoscaler for Vector
## Valid for Aggregator and Stateless-Aggregator roles
autoscaling:
  # autoscaling.enabled -- Enabled autoscaling for the Aggregator and Stateless-Aggregator
  enabled: false
  # autoscaling.minReplicas -- Minimum replicas for Vector's HPA

podDisruptionBudget:
  # podDisruptionBudget.enabled -- Enable a PodDisruptionBudget for Vector
  enabled: false

rbac:
  # rbac.create -- If true, create and use RBAC resources. Only valid for the Agent role
  create: true

psp:
  # psp.create -- If true, create a PodSecurityPolicy resource. PodSecurityPolicy is deprecated as of Kubernetes v1.21, and will be removed in v1.25
  ## Intended for use with the Agent role
  create: false

serviceAccount:
  # serviceAccount.create -- If true, create ServiceAccount
  create: true
  annotations:
    eks.amazonaws.com/role-arn: ${SA_ROLE_ARN}
  # serviceAccount.automountToken -- Automount API credentials for the Vector ServiceAccount
  automountToken: true

# tolerations -- Allow Vector to schedule on tainted nodes
tolerations:
  - operator: Exists

## Configuration for Vector's Service
service:
  # service.enabled -- If true, create and use a Service resource
  enabled: false

## Configuration for Vector's Ingress
ingress:
  # ingress.enabled -- If true, create and use an Ingress resource
  enabled: false

# livenessProbe -- Override default liveness probe settings, if customConfig is used requires customConfig.api.enabled true
## Requires Vector's API to be enabled
livenessProbe:
  httpGet:
    path: /health
    port: api
  initialDelaySeconds: 30
  periodSeconds: 30
  failureThreshold: 10
  timeoutSeconds: 10

# readinessProbe -- Override default readiness probe settings, if customConfig is used requires customConfig.api.enabled true
## Requires Vector's API to be enabled
readinessProbe:
  httpGet:
    path: /health
    port: api

## Configure a PodMonitor for Vector
## Requires the PodMonitor CRD to be installed
podMonitor:
  # podMonitor.enabled -- If true, create a PodMonitor for Vector
  enabled: false
containerPorts:
  - name: prom-exporter
    containerPort: 9598
    protocol: TCP
  - name: api
    containerPort: 8686
    protocol: TCP

## Optional built-in HAProxy load balancer
haproxy:
  # haproxy.enabled -- If true, create a HAProxy load balancer
  enabled: false
```
