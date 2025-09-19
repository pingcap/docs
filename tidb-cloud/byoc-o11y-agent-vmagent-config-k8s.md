```yaml
# Please replace the variables in the ${} format in the configuration appropriately.
scrape_configs:
- bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
  honor_labels: false
  job_name: kubelet
  kubernetes_sd_configs:
  - role: node
  relabel_configs:
  - source_labels:
    - __meta_kubernetes_node_address_InternalIP
    target_label: instance
  - action: labelmap
    regex: __meta_kubernetes_node_label_(.+)
  - replacement: shoot
    target_label: type
  - action: replace
    regex: (.*)
    replacement: $1
    separator: ;
    source_labels:
    - __metrics_path__
    target_label: metrics_path
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
- bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
  honor_labels: true
  job_name: cadvisor
  kubernetes_sd_configs:
  - role: node
  metrics_path: /metrics/cadvisor
  relabel_configs:
  - source_labels:
    - __meta_kubernetes_node_address_InternalIP
    target_label: instance
  - action: labelmap
    regex: __meta_kubernetes_node_label_(.+)
  - replacement: shoot
    target_label: type
  - action: replace
    source_labels:
    - cluster
    target_label: tidb_cluster
  - action: replace
    source_labels:
    - k8s_cluster_info
    target_label: cluster
  - action: replace
    regex: (.*)
    replacement: $1
    separator: ;
    source_labels:
    - __metrics_path__
    target_label: metrics_path
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
- honor_labels: false
  job_name: kube-state-metrics
  kubernetes_sd_configs:
  - namespaces:
      names:
      - monitoring
    role: service
  metric_relabel_configs:
  - action: drop
    regex: ^.+\.tf-pod.+$
    source_labels:
    - pod
  relabel_configs:
  - action: keep
    regex: kube-state-metrics
    source_labels:
    - __meta_kubernetes_service_name
  - replacement: kube-state-metrics
    target_label: instance
- honor_labels: false
  job_name: ebs-csi-node
  scrape_interval: 15s
  kubernetes_sd_configs:
  - role: endpoints
    namespaces:
      names:
      - kube-system
  relabel_configs:
  - action: keep
    regex: ebs-csi-node
    source_labels:
    - __meta_kubernetes_endpoints_name
  - source_labels: [__meta_kubernetes_endpoint_port_name]
    regex: metrics
    replacement: $1
    action: keep
  - source_labels:
    - __meta_kubernetes_pod_name
    target_label: pod
  - action: replace
    regex: (.*)
    replacement: $1
    source_labels:
    - __meta_kubernetes_pod_node_name
    target_label: instance
  scrape_timeout: 15s
- honor_labels: false
  job_name: node-exporter
  kubernetes_sd_configs:
  - role: endpoints
  relabel_configs:
  - action: keep
    regex: node-exporter-prometheus-node-exporter
    source_labels:
    - __meta_kubernetes_endpoints_name
  - source_labels:
    - __meta_kubernetes_pod_name
    target_label: pod
  - action: labelmap
    regex: __meta_kubernetes_node_label_(.+)
  - action: replace
    regex: (.*)
    replacement: $1
    separator: ;
    source_labels:
    - __meta_kubernetes_pod_node_name
    target_label: instance
  scrape_timeout: 30s
- honor_labels: false
  job_name: metrics-agents
  kubernetes_sd_configs:
  - role: endpoints
  relabel_configs:
  - action: keep
    regex: (.*)vmagent
    source_labels:
    - __meta_kubernetes_endpoints_name
  - source_labels:
    - __meta_kubernetes_namespace
    target_label: namespace
  - source_labels:
    - __meta_kubernetes_pod_name
    target_label: pod
  - source_labels:
    - __meta_kubernetes_service_name
    target_label: service
  scrape_timeout: 30s
- honor_labels: false
  job_name: vector-agents
  kubernetes_sd_configs:
  - role: pod
  relabel_configs:
  - action: keep
    regex: vector
    source_labels:
    - __meta_kubernetes_pod_container_name
  - action: keep
    regex: prom-exporter
    source_labels:
    - __meta_kubernetes_pod_container_port_name
  - source_labels:
    - __meta_kubernetes_namespace
    target_label: namespace
  scrape_timeout: 30s
- honor_labels: false
  honor_timestamps: true
  job_name: cert-manager
  kubernetes_sd_configs:
  - role: endpoints
  metrics_path: /metrics
  relabel_configs:
  - action: keep
    regex: controller
    replacement: $1
    separator: ;
    source_labels:
    - __meta_kubernetes_service_label_app_kubernetes_io_component
  - action: keep
    regex: cert-manager
    replacement: $1
    separator: ;
    source_labels:
    - __meta_kubernetes_service_label_app_kubernetes_io_name
  - action: keep
    regex: cert-manager
    replacement: $1
    separator: ;
    source_labels:
    - __meta_kubernetes_service_label_app_kubernetes_io_instance
  - action: keep
    regex: "9402"
    replacement: $1
    separator: ;
    source_labels:
    - __meta_kubernetes_pod_container_port_number
  - action: replace
    regex: Node;(.*)
    replacement: ${1}
    separator: ;
    source_labels:
    - __meta_kubernetes_endpoint_address_target_kind
    - __meta_kubernetes_endpoint_address_target_name
    target_label: node
  - action: replace
    regex: Pod;(.*)
    replacement: ${1}
    separator: ;
    source_labels:
    - __meta_kubernetes_endpoint_address_target_kind
    - __meta_kubernetes_endpoint_address_target_name
    target_label: pod
  - action: replace
    regex: (.*)
    replacement: $1
    separator: ;
    source_labels:
    - __meta_kubernetes_namespace
    target_label: namespace
  - action: replace
    regex: (.*)
    replacement: $1
    separator: ;
    source_labels:
    - __meta_kubernetes_service_name
    target_label: service
  - action: replace
    regex: (.*)
    replacement: $1
    separator: ;
    source_labels:
    - __meta_kubernetes_pod_name
    target_label: pod
  - action: replace
    regex: (.*)
    replacement: ${1}
    separator: ;
    source_labels:
    - __meta_kubernetes_service_name
    target_label: job
  - action: replace
    regex: (.+)
    replacement: ${1}
    separator: ;
    source_labels:
    - __meta_kubernetes_service_label_cert_manager
    target_label: job
  - action: replace
    regex: (.*)
    replacement: "9402"
    separator: ;
    target_label: endpoint
  scrape_interval: 1m
  scrape_timeout: 30s
- honor_labels: false
  job_name: 'coredns'
  kubernetes_sd_configs:
  - role: pod
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_label_eks_amazonaws_com_component, __meta_kubernetes_pod_container_port_name]
    regex: coredns;metrics
    action: keep
  - source_labels: [__meta_kubernetes_namespace]
    action: replace
    target_label: namespace
  - source_labels: [__meta_kubernetes_pod_name]
    action: replace
    target_label: pod
  - source_labels: [__meta_kubernetes_pod_node_name]
    action: replace
    target_label: node
```
