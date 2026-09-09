```yaml
# Please replace the variables in the ${} format in the configuration appropriately.
scrape_configs:
- job_name: ${NAMESPACE}-core-components
  scrape_interval: 15s
  honor_labels: true
  scheme: https
  tls_config:
    ca_file: /var/lib/cluster-assets-tls/ca.crt
    cert_file: /var/lib/cluster-assets-tls/tls.crt
    key_file: /var/lib/cluster-assets-tls/tls.key
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    regex: db(-.*)?
    action: keep
  - source_labels: [__meta_kubernetes_namespace]
    regex: ${NAMESPACE}
    action: keep
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    regex: "true"
    action: keep
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    regex: pd|tidb|tiflash|tikv
    action: keep
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    target_label: job
    replacement: ${NAMESPACE}-db-$1
    action: replace
  - source_labels: [__meta_kubernetes_pod_name, __meta_kubernetes_pod_label_app_kubernetes_io_instance,
            __meta_kubernetes_pod_label_app_kubernetes_io_component, __meta_kubernetes_namespace,
            __meta_kubernetes_pod_annotation_prometheus_io_port]
    target_label: __address__
    regex: (.+);(.+);(.+);(.+);(.+)
    replacement: $1.$2-$3-peer.$4:$5
    action: replace
  - source_labels: [__meta_kubernetes_namespace]
    target_label: kubernetes_namespace
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    target_label: cluster
    action: replace
  - source_labels: [__meta_kubernetes_pod_name]
    target_label: instance
    action: replace
  - source_labels: [instance]
    target_label: instance
    regex: db-(\d+)-([a-zA-Z0-9]+)-tidb-(\d+)
    replacement: db-tidb-$3-ac-$1
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    target_label: component
    action: replace
  - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_pod_label_app_kubernetes_io_instance]
    separator: '-'
    target_label: tidb_cluster
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    target_label: __metrics_path__
    regex: (.+)
    action: replace
  kubernetes_sd_configs:
  - role: pod
    kubeconfig_file: ""
    namespaces:
      own_namespace: false
      names:
      - ${NAMESPACE}
- job_name: ${NAMESPACE}-tiproxy
  scrape_interval: 15s
  honor_labels: true
  scheme: https
  tls_config:
    insecure_skip_verify: true
    ca_file: /var/lib/cluster-assets-tls/ca.crt
    cert_file: /var/lib/cluster-assets-tls/tls.crt
    key_file: /var/lib/cluster-assets-tls/tls.key
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    regex: db
    action: keep
  - source_labels: [__meta_kubernetes_namespace]
    regex: ${NAMESPACE}
    action: keep
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    regex: "true"
    action: keep
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    regex: tiproxy
    action: keep
  - source_labels: [__meta_kubernetes_pod_name, __meta_kubernetes_pod_label_app_kubernetes_io_instance,
            __meta_kubernetes_pod_label_app_kubernetes_io_component, __meta_kubernetes_namespace,
            __meta_kubernetes_pod_annotation_prometheus_io_port]
    target_label: __address__
    regex: (.+);(.+);(.+);(.+);(.+)
    replacement: $1.$2-$3-peer.$4:$5
    action: replace
  - source_labels: [__meta_kubernetes_namespace]
    target_label: kubernetes_namespace
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    target_label: cluster
    action: replace
  - source_labels: [__meta_kubernetes_pod_name]
    target_label: instance
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    target_label: component
    action: replace
  - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_pod_label_app_kubernetes_io_instance]
    separator: '-'
    target_label: tidb_cluster
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    target_label: __metrics_path__
    regex: (.+)
    action: replace
  kubernetes_sd_configs:
  - role: pod
    kubeconfig_file: ""
    namespaces:
      own_namespace: false
      names:
      - ${NAMESPACE}
- job_name: ${NAMESPACE}-importer
  scrape_interval: 15s
  honor_labels: true
  scheme: https
  tls_config:
    ca_file: /var/lib/cluster-assets-tls/ca.crt
    cert_file: /var/lib/cluster-assets-tls/tls.crt
    key_file: /var/lib/cluster-assets-tls/tls.key
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    regex: db
    action: keep
  - source_labels: [__meta_kubernetes_namespace]
    regex: ${NAMESPACE}
    action: keep
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    regex: "true"
    action: keep
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    regex: importer
    action: keep
  - source_labels: [__meta_kubernetes_pod_name, __meta_kubernetes_pod_label_app_kubernetes_io_instance,
            __meta_kubernetes_namespace,__meta_kubernetes_pod_annotation_prometheus_io_port]
    target_label: __address__
    regex: (.+);(.+);(.+);(.+)
    replacement: $1.$2-importer.$3:$4
    action: replace
  - source_labels: [__meta_kubernetes_namespace]
    target_label: kubernetes_namespace
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    target_label: cluster
    action: replace
  - source_labels: [__meta_kubernetes_pod_name]
    target_label: instance
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    target_label: component
    action: replace
  - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_pod_label_app_kubernetes_io_instance]
    separator: '-'
    target_label: tidb_cluster
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    target_label: __metrics_path__
    regex: (.+)
    action: replace
  kubernetes_sd_configs:
  - role: pod
    kubeconfig_file: ""
    namespaces:
      own_namespace: false
      names:
      - ${NAMESPACE}
- job_name: ${NAMESPACE}-lightning
  scrape_interval: 15s
  honor_labels: true
  scheme: https
  tls_config:
    insecure_skip_verify: true
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    regex: db
    action: keep
  - source_labels: [__meta_kubernetes_namespace]
    regex: ${NAMESPACE}
    action: keep
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    regex: "true"
    action: keep
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    regex: tidb-lightning
    action: keep
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_name,
        __meta_kubernetes_namespace, __meta_kubernetes_pod_annotation_prometheus_io_port]
    target_label: __address__
    regex: (.+);(.+);(.+)
    replacement: $1.$2:$3
    action: replace
  - source_labels: [__meta_kubernetes_namespace]
    target_label: kubernetes_namespace
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    target_label: cluster
    action: replace
  - source_labels: [__meta_kubernetes_pod_name]
    target_label: instance
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    target_label: component
    action: replace
  - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_pod_label_app_kubernetes_io_instance]
    separator: '-'
    target_label: tidb_cluster
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    target_label: __metrics_path__
    regex: (.+)
    action: replace
  kubernetes_sd_configs:
  - role: pod
    kubeconfig_file: ""
    namespaces:
      own_namespace: false
      names:
      - ${NAMESPACE}
- job_name: ${NAMESPACE}-dumpling
  scrape_interval: 15s
  honor_labels: true
  scheme: http
  kubernetes_sd_configs:
  - role: pod
    kubeconfig_file: ""
    namespaces:
      own_namespace: false
      names:
      - ${NAMESPACE}
  tls_config:
    insecure_skip_verify: true
  relabel_configs:
  - source_labels: [__meta_kubernetes_namespace]
    regex: ${NAMESPACE}
    action: keep
  - source_labels: [__meta_kubernetes_pod_name]
    regex: dumpling-job-(.+)
    action: keep
  - source_labels: [__meta_kubernetes_pod_ip]
    target_label: __address__
    regex: (.+)
    replacement: $1:8281
    action: replace
  - source_labels: [__meta_kubernetes_namespace]
    target_label: kubernetes_namespace
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_job_name]
    target_label: instance
    action: replace
- job_name: ${NAMESPACE}-dwworker
  scrape_interval: 15s
  honor_labels: true
  scheme: http
  kubernetes_sd_configs:
  - role: pod
    kubeconfig_file: ""
    namespaces:
      own_namespace: false
      names:
      - ${NAMESPACE}
  tls_config:
    insecure_skip_verify: true
  relabel_configs:
  - source_labels: [__meta_kubernetes_namespace]
    regex: ${NAMESPACE}
    action: keep
  - source_labels: [__meta_kubernetes_pod_name]
    regex: dwworker-(.+)
    action: keep
  - source_labels: [__meta_kubernetes_pod_ip]
    target_label: __address__
    regex: (.+)
    replacement: $1:8185
    action: replace
  - source_labels: [__meta_kubernetes_namespace]
    target_label: kubernetes_namespace
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    target_label: instance
    action: replace
- job_name: ${NAMESPACE}-tiflash-proxy
  scrape_interval: 15s
  honor_labels: true
  scheme: https
  tls_config:
    ca_file: /var/lib/cluster-assets-tls/ca.crt
    cert_file: /var/lib/cluster-assets-tls/tls.crt
    key_file: /var/lib/cluster-assets-tls/tls.key
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    regex: db
    action: keep
  - source_labels: [__meta_kubernetes_namespace]
    regex: ${NAMESPACE}
    action: keep
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    regex: "true"
    action: keep
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    regex: tiflash
    action: keep
  - source_labels: [__meta_kubernetes_pod_name, __meta_kubernetes_pod_label_app_kubernetes_io_instance,
            __meta_kubernetes_pod_label_app_kubernetes_io_component, __meta_kubernetes_namespace,
            __meta_kubernetes_pod_annotation_tiflash_proxy_prometheus_io_port]
    target_label: __address__
    regex: (.+);(.+);(.+);(.+);(.+)
    replacement: $1.$2-$3-peer.$4:$5
    action: replace
  - source_labels: [__meta_kubernetes_namespace]
    target_label: kubernetes_namespace
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    target_label: cluster
    action: replace
  - source_labels: [__meta_kubernetes_pod_name]
    target_label: instance
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    target_label: component
    action: replace
  - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_pod_label_app_kubernetes_io_instance]
    separator: '-'
    target_label: tidb_cluster
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    target_label: __metrics_path__
    regex: (.+)
    action: replace
  kubernetes_sd_configs:
  - role: pod
    kubeconfig_file: ""
    namespaces:
      own_namespace: false
      names:
      - ${NAMESPACE}
- job_name: ${NAMESPACE}-ticdc
  scrape_interval: 15s
  honor_labels: true
  scheme: https
  tls_config:
    ca_file: /var/lib/cluster-assets-tls/ca.crt
    cert_file: /var/lib/cluster-assets-tls/tls.crt
    key_file: /var/lib/cluster-assets-tls/tls.key
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    regex: db|db-cdc|rg\d+-op\d+-c\d+|changefeed-\d+
    action: keep
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    target_label: job
    replacement: ${NAMESPACE}-$1-ticdc
    action: replace
  - source_labels: [__meta_kubernetes_namespace]
    regex: ${NAMESPACE}
    action: keep
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    regex: "true"
    action: keep
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    regex: ticdc
    action: keep
  - source_labels: [__meta_kubernetes_pod_name, __meta_kubernetes_pod_label_app_kubernetes_io_instance,
            __meta_kubernetes_pod_label_app_kubernetes_io_component, __meta_kubernetes_namespace,
            __meta_kubernetes_pod_annotation_prometheus_io_port]
    target_label: __address__
    regex: (.+);(.+);(.+);(.+);(.+)
    replacement: $1.$2-$3-peer.$4:$5
    action: replace
  - source_labels: [__meta_kubernetes_namespace]
    target_label: kubernetes_namespace
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    target_label: cluster
    action: replace
  - source_labels: [__meta_kubernetes_pod_name]
    target_label: instance
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    target_label: component
    action: replace
  - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_pod_label_app_kubernetes_io_instance]
    separator: '-'
    target_label: tidb_cluster
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    target_label: __metrics_path__
    regex: (.+)
    action: replace
  kubernetes_sd_configs:
  - role: pod
    kubeconfig_file: ""
    namespaces:
      own_namespace: false
      names:
      - ${NAMESPACE}
- job_name: ${NAMESPACE}-tidb-auditlog
  honor_labels: true
  scrape_interval: 15s
  scheme: http
  kubernetes_sd_configs:
  - api_server: null
    role: pod
    namespaces:
      names:
      - ${NAMESPACE}
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    regex: db
    action: keep
  - source_labels: [__meta_kubernetes_namespace]
    regex: ${NAMESPACE}
    action: keep
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    regex: "true"
    action: keep
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    regex: tidb
    action: keep
  - source_labels: [__meta_kubernetes_pod_name, __meta_kubernetes_pod_label_app_kubernetes_io_instance,
      __meta_kubernetes_namespace, __meta_kubernetes_pod_annotation_tidb_auditlog_prometheus_io_port]
    regex: (.+);(.+);(.+);(.+)
    target_label: __address__
    replacement: $1.$2-tidb-peer.$3:$4
    action: replace
  - source_labels: [__meta_kubernetes_pod_annotation_tidb_auditlog_prometheus_io_port]
    regex: (.+)
    target_label: __address__
    action: keep
  - source_labels: [__meta_kubernetes_namespace]
    target_label: kubernetes_namespace
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_instance]
    target_label: cluster
    action: replace
  - source_labels: [__meta_kubernetes_pod_name]
    target_label: instance
    action: replace
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    target_label: component
    replacement: auditlog
    action: replace
  - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_pod_label_app_kubernetes_io_instance]
    separator: '-'
    target_label: tidb_cluster
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    regex: (.+)
    target_label: __metrics_path__
- job_name: ${NAMESPACE}-node-exporter
  honor_labels: true
  scrape_interval: 15s
  scheme: http
  params:
    collect[]:
      - meminfo
      - cpu
  kubernetes_sd_configs:
  - api_server: null
    role: pod
    namespaces:
      names:
      - ${NAMESPACE}
  relabel_configs:
  - source_labels:
    - __meta_kubernetes_pod_label_app_kubernetes_io_instance
    action: keep
    regex: db(-.*)?
  - source_labels:
    - __meta_kubernetes_namespace
    action: keep
    regex: ${NAMESPACE}
  - source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_scrape
    action: keep
    regex: "true"
  - source_labels:
    - __meta_kubernetes_pod_label_app_kubernetes_io_component
    action: keep
    regex: pd|tikv|tidb|tiflash
  - action: replace
    regex: (.+)
    replacement: $1:9100
    target_label: __address__
    source_labels:
    - __meta_kubernetes_pod_host_ip
  - source_labels:
    - __meta_kubernetes_pod_label_app_kubernetes_io_instance
    action: replace
    target_label: cluster
  - source_labels:
    - __meta_kubernetes_pod_name
    action: replace
    target_label: instance
  - source_labels: [instance]
    target_label: instance
    regex: db-(\d+)-([a-zA-Z0-9]+)-tidb-(\d+)
    replacement: db-tidb-$3-ac-$1
    action: replace
  - source_labels:
    - __meta_kubernetes_pod_label_app_kubernetes_io_component
    action: replace
    target_label: component
  - source_labels:
    - __meta_kubernetes_namespace
    - __meta_kubernetes_pod_label_app_kubernetes_io_instance
    separator: '-'
    target_label: tidb_cluster
  metric_relabel_configs:
  - source_labels:
    - __name__
    action: keep
    regex: 'node_cpu_seconds_total|node_memory_MemTotal_bytes|node_memory_MemAvailable_bytes|node_memory_MemFree_bytes|node_memory_Buffers_bytes|node_memory_Cached_bytes'
- job_name: ${NAMESPACE}-kubelet
  honor_labels: true
  scrape_interval: 15s
  scheme: https
  bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
  kubernetes_sd_configs:
  - api_server: null
    role: pod
    namespaces:
      names:
      - ${NAMESPACE}
  tls_config:
    insecure_skip_verify: true
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
  relabel_configs:
  - source_labels:
    - __meta_kubernetes_pod_label_app_kubernetes_io_instance
    action: keep
    regex: db
  - source_labels:
    - __meta_kubernetes_namespace
    action: keep
    regex: ${NAMESPACE}
  - source_labels:
    - __meta_kubernetes_pod_label_app_kubernetes_io_component
    action: keep
    regex: pd|tikv|tidb|tiflash
  - action: replace
    regex: (.+)
    replacement: $1:10250
    target_label: __address__
    source_labels:
    - __meta_kubernetes_pod_host_ip
  - source_labels:
    - __meta_kubernetes_pod_label_app_kubernetes_io_instance
    action: replace
    target_label: cluster
  - source_labels:
    - __meta_kubernetes_pod_name
    action: replace
    target_label: instance
  - source_labels:
    - __meta_kubernetes_pod_label_app_kubernetes_io_component
    action: replace
    target_label: component
  - source_labels:
    - __meta_kubernetes_namespace
    - __meta_kubernetes_pod_label_app_kubernetes_io_instance
    separator: '-'
    target_label: tidb_cluster
  metric_relabel_configs:
  - source_labels:
    - namespace
    action: keep
    regex: ${NAMESPACE}
  - source_labels:
    - __name__
    action: keep
    regex: 'kubelet_volume_stats_available_bytes|kubelet_volume_stats_capacity_bytes'
- job_name: ${NAMESPACE}-tiflow
  honor_labels: true
  scrape_interval: 15s
  scheme: http
  kubernetes_sd_configs:
  - api_server: null
    role: pod
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    regex: "true"
    action: keep
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    action: keep
    regex: tiflow-executor
  - source_labels: [__meta_kubernetes_pod_label_tiflow_cloud_pingcap_com_tidb_cluster_name]
    action: keep
    regex: "${CLUSTER_ID}"
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    regex: (.+)
    target_label: __metrics_path__
  - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_component]
    action: replace
    target_label: component
  - source_labels: [__meta_kubernetes_namespace]
    target_label: kubernetes_namespace
    action: replace
  - source_labels: [__meta_kubernetes_pod_name]
    target_label: instance
    action: replace
  metric_relabel_configs:
  - source_labels:
    - __name__
    action: keep
    regex: 'dm_mydumper_exit_with_error_count|dm_loader_exit_with_error_count|dm_syncer_exit_with_error_count|dm_worker_task_state|dm_syncer_replication_lag_gauge'
```
