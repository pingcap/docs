O11y Vector Agent Configuration for Per-TiDB-Cluster Diagnostic Data Collection.

# Basic Configuration

```toml
# Replace all ${VAR} placeholders with appropriate values

# Vector Agent data directory
data_dir = "/vector-data-dir"

[api]
# Whether to enable Vector Agent's management API
enabled = false

# Self-monitoring collection
[sources.self_metrics]
type = "internal_metrics"

# 将 Expose Vector's own metrics in Prometheus format on /metrics endpoint
[sinks.self_metrics_sink]
type = "prometheus_exporter"
inputs = ["self_metrics"]
address = "0.0.0.0:${METRICS_PORT}"
```

# Feature Configuration

## Top SQL

```toml
# Top SQL collection configuration
[sources.topsql]
type = "topsql"
# PD endpoint for cluster topology discovery
pd_address = "db-pd:2379"
# TLS certificate paths
tls.ca_path = "${TLS_PATH}/ca.crt"
tls.crt_path = "${TLS_PATH}/tls.crt"
tls.key_path = "${TLS_PATH}/tls.key"
# Number of top SQL statements to retain per minute
top_n = 10

# Top SQL metadata transformation
[transforms.topsql_add_meta]
type = "remap"
inputs = ["topsql"]
source = """
.labels.provider = "${PROVIDER}"
.labels.region = "${REGION}"
.labels.k8s_cluster_name = "${K8S_CLUSTER_NAME}"
.labels.k8s_namespace = "${K8S_NAMESPACE}"
.labels.project_id = "${PROJECT_ID}"
.labels.tenant_id = "${TENANT_ID}"
.labels.cluster_id = "${CLUSTER_ID}"
"""

# Top SQL export to VictoriaMetrics
[sinks.topsql_vm]
type = "vm_import"
inputs = ["topsql_add_meta"]
endpoint = "${VM_IMPORT_URL}"
batch.max_events = 1000
batch.max_bytes = 1048576 # 1MiB
batch.timeout_secs = 1
buffer.type = "disk"
buffer.max_size = 536870912 # 512MiB
buffer.when_full = "drop_newest"
```

## Continuous Profiling

### AWS

```toml
# Continuous Profiling Collection Configuration
[sources.conprof]
type = "conprof"
# PD endpoint for cluster topology subscription
pd_address = "db-pd:2379"
# TLS certificate paths
tls.ca_path = "${TLS_PATH}/ca.crt"
tls.crt_path = "${TLS_PATH}/tls.crt"
tls.key_path = "${TLS_PATH}/tls.key"
# Enable TiKV heap profiling (older TiKV versions may not support heap profiling)
enable_tikv_heap_profile = true

# Continuous Profiling Transformation - prepares S3 write path
[transforms.conprof_add_meta]
type = "remap"
inputs = ["conprof"]
source = """
.key_prefix = join!(["0", "${TENANT_ID}", "${PROJECT_ID}", "${CLUSTER_ID}", "profiles", .filename], separator: "/")
"""

# Continuous Profiling Export to S3.
[sinks.conprof_s3]
type = "aws_s3"
inputs = ["conprof_add_meta"]
encoding.codec = "raw_message"
region = "${REGION}"
bucket = "${BUCKET}"
key_prefix = "{{ key_prefix }}"
filename_time_format = ""
filename_append_uuid = false
batch.max_bytes = 1 # DO NOT BATCH
batch.max_events = 1
batch.timeout_secs = 1
auth.assume_role = "${ROLE_ARN}" # IAM role for write permissions
```

### GCP

```toml
# Continuous Profiling Collection Configuration
[sources.conprof]
type = "conprof"
# PD endpoint for cluster topology subscription
pd_address = "db-pd:2379"
# TLS certificate paths
tls.ca_path = "${TLS_PATH}/ca.crt"
tls.crt_path = "${TLS_PATH}/tls.crt"
tls.key_path = "${TLS_PATH}/tls.key"
# Enable TiKV heap profiling (older TiKV versions may not support heap profiling)
enable_tikv_heap_profile = true

# Continuous Profiling Transformation - prepares GCS write path
[transforms.conprof_add_meta]
type = "remap"
inputs = ["conprof"]
source = """
.key_prefix = join!(["0", "${TENANT_ID}", "${PROJECT_ID}", "${CLUSTER_ID}", "profiles", .filename], separator: "/")
"""

# Continuous Profiling Export to GCS.
[sinks.conprof_gcs]
type = "gcp_cloud_storage"
inputs = ["conprof_add_meta"]
encoding.codec = "raw_message"
bucket = "${BUCKET}"
key_prefix = "{{ key_prefix }}"
filename_time_format = ""
filename_append_uuid = false
batch.max_bytes = 1 # DO NOT BATCH
batch.max_events = 1
batch.timeout_secs = 1
```

## Key Visualizer

### AWS

```toml
# Key Visualizer Collection Configuration
[sources.keyviz]
type = "keyviz"
# PD endpoint for cluster topology subscription
pd_address = "db-pd:2379"
# TLS certificate paths
tls.ca_path = "${TLS_PATH}/ca.crt"
tls.crt_path = "${TLS_PATH}/tls.crt"
tls.key_path = "${TLS_PATH}/tls.key"

# Key Visualizer Transformation - prepares S3 write path
[transforms.keyviz_add_meta]
type = "remap"
inputs = ["keyviz"]
source = """
.key_prefix = join!(["0", "${TENANT_ID}", "${PROJECT_ID}", "${CLUSTER_ID}", "regions", .filename], separator: "/")
"""

# Key Visualizer Export to S3.
[sinks.keyviz_s3]
type = "aws_s3"
inputs = ["keyviz_add_meta"]
encoding.codec = "raw_message"
region = "${REGION}"
bucket = "${BUCKET}"
key_prefix = "{{ key_prefix }}"
filename_time_format = ""
filename_append_uuid = false
batch.max_bytes = 1 # DO NOT BATCH
batch.max_events = 1
batch.timeout_secs = 1
auth.assume_role = "${ROLE_ARN}"
```

### GCP

```toml
# Key Visualizer Collection Configuration
[sources.keyviz]
type = "keyviz"
# PD endpoint for cluster topology subscription
pd_address = "db-pd:2379"
# TLS certificate paths
tls.ca_path = "${TLS_PATH}/ca.crt"
tls.crt_path = "${TLS_PATH}/tls.crt"
tls.key_path = "${TLS_PATH}/tls.key"

# Key Visualizer Transformation - prepares GCS write path
[transforms.keyviz_add_meta]
type = "remap"
inputs = ["keyviz"]
source = """
.key_prefix = join!(["0", "${TENANT_ID}", "${PROJECT_ID}", "${CLUSTER_ID}", "regions", .filename], separator: "/")
"""

# Key Visualizer Export to GCS.
[sinks.keyviz_gcs]
type = "gcp_cloud_storage"
inputs = ["keyviz_add_meta"]
encoding.codec = "raw_message"
bucket = "${BUCKET}"
key_prefix = "{{ key_prefix }}"
filename_time_format = ""
filename_append_uuid = false
batch.max_bytes = 1 # DO NOT BATCH
batch.max_events = 1
batch.timeout_secs = 1
```

# Full Configuration Example

## AWS

```toml
data_dir = "${DATA_PATH}"

[api]
enabled = false

[sources.topsql]
type = "topsql"
pd_address = "db-pd:2379"
tls.ca_path = "${TLS_PATH}/ca.crt"
tls.crt_path = "${TLS_PATH}/tls.crt"
tls.key_path = "${TLS_PATH}/tls.key"
top_n = 10

[transforms.topsql_add_meta]
type = "remap"
inputs = ["topsql"]
source = """
.labels.provider = "${PROVIDER}"
.labels.region = "${REGION}"
.labels.k8s_cluster_name = "${K8S_CLUSTER_NAME}"
.labels.k8s_namespace = "${K8S_NAMESPACE}"
.labels.project_id = "${PROJECT_ID}"
.labels.tenant_id = "${TENANT_ID}"
.labels.cluster_id = "${CLUSTER_ID}"
"""

[sinks.topsql_vm]
type = "vm_import"
inputs = ["topsql_add_meta"]
endpoint = "${VM_IMPORT_URL}"
batch.max_events = 1000
batch.max_bytes = 1048576 # 1MiB
batch.timeout_secs = 1
buffer.type = "disk"
buffer.max_size = 536870912 # 512MiB
buffer.when_full = "drop_newest"

[sources.conprof]
type = "conprof"
pd_address = "db-pd:2379"
tls.ca_path = "${TLS_PATH}/ca.crt"
tls.crt_path = "${TLS_PATH}/tls.crt"
tls.key_path = "${TLS_PATH}/tls.key"
enable_tikv_heap_profile = true

[transforms.conprof_add_meta]
type = "remap"
inputs = ["conprof"]
source = """
.key_prefix = join!(["0", "${TENANT_ID}", "${PROJECT_ID}", "${CLUSTER_ID}", "profiles", .filename], separator: "/")
"""

[sinks.conprof_s3]
type = "aws_s3"
inputs = ["conprof_add_meta"]
encoding.codec = "raw_message"
region = "${REGION}"
bucket = "${BUCKET}"
key_prefix = "{{ key_prefix }}"
filename_time_format = ""
filename_append_uuid = false
batch.max_bytes = 1 # DO NOT BATCH
batch.max_events = 1
batch.timeout_secs = 1
auth.assume_role = "${ROLE_ARN}"

[sources.keyviz]
type = "keyviz"
pd_address = "db-pd:2379"
tls.ca_path = "${TLS_PATH}/ca.crt"
tls.crt_path = "${TLS_PATH}/tls.crt"
tls.key_path = "${TLS_PATH}/tls.key"

[transforms.keyviz_add_meta]
type = "remap"
inputs = ["keyviz"]
source = """
.key_prefix = join!(["0", "${TENANT_ID}", "${PROJECT_ID}", "${CLUSTER_ID}", "regions", .filename], separator: "/")
"""

[sinks.keyviz_s3]
type = "aws_s3"
inputs = ["keyviz_add_meta"]
encoding.codec = "raw_message"
region = "${REGION}"
bucket = "${BUCKET}"
key_prefix = "{{ key_prefix }}"
filename_time_format = ""
filename_append_uuid = false
batch.max_bytes = 1 # DO NOT BATCH
batch.max_events = 1
batch.timeout_secs = 1
auth.assume_role = "${ROLE_ARN}"

[sources.self_metrics]
type = "internal_metrics"

[sinks.self_metrics_sink]
type = "prometheus_exporter"
inputs = ["self_metrics"]
address = "0.0.0.0:${METRICS_PORT}"
```

## GCP

```toml
data_dir = "${DATA_PATH}"

[api]
enabled = false

[sources.topsql]
type = "topsql"
pd_address = "db-pd:2379"
tls.ca_path = "${TLS_PATH}/ca.crt"
tls.crt_path = "${TLS_PATH}/tls.crt"
tls.key_path = "${TLS_PATH}/tls.key"
top_n = 10

[transforms.topsql_add_meta]
type = "remap"
inputs = ["topsql"]
source = """
.labels.provider = "${PROVIDER}"
.labels.region = "${REGION}"
.labels.k8s_cluster_name = "${K8S_CLUSTER_NAME}"
.labels.k8s_namespace = "${K8S_NAMESPACE}"
.labels.project_id = "${PROJECT_ID}"
.labels.tenant_id = "${TENANT_ID}"
.labels.cluster_id = "${CLUSTER_ID}"
"""

[sinks.topsql_vm]
type = "vm_import"
inputs = ["topsql_add_meta"]
endpoint = "${VM_IMPORT_URL}"
batch.max_events = 1000
batch.max_bytes = 1048576 # 1MiB
batch.timeout_secs = 1
buffer.type = "disk"
buffer.max_size = 536870912 # 512MiB
buffer.when_full = "drop_newest"

[sources.conprof]
type = "conprof"
pd_address = "db-pd:2379"
tls.ca_path = "${TLS_PATH}/ca.crt"
tls.crt_path = "${TLS_PATH}/tls.crt"
tls.key_path = "${TLS_PATH}/tls.key"
enable_tikv_heap_profile = true

[transforms.conprof_add_meta]
type = "remap"
inputs = ["conprof"]
source = """
.key_prefix = join!(["0", "${TENANT_ID}", "${PROJECT_ID}", "${CLUSTER_ID}", "profiles", .filename], separator: "/")
"""

[sinks.conprof_gcs]
type = "gcp_cloud_storage"
inputs = ["conprof_add_meta"]
encoding.codec = "raw_message"
bucket = "${BUCKET}"
key_prefix = "{{ key_prefix }}"
filename_time_format = ""
filename_append_uuid = false
batch.max_bytes = 1 # DO NOT BATCH
batch.max_events = 1
batch.timeout_secs = 1

[sources.keyviz]
type = "keyviz"
pd_address = "db-pd:2379"
tls.ca_path = "${TLS_PATH}/ca.crt"
tls.crt_path = "${TLS_PATH}/tls.crt"
tls.key_path = "${TLS_PATH}/tls.key"

[transforms.keyviz_add_meta]
type = "remap"
inputs = ["keyviz"]
source = """
.key_prefix = join!(["0", "${TENANT_ID}", "${PROJECT_ID}", "${CLUSTER_ID}", "regions", .filename], separator: "/")
"""

[sinks.keyviz_gcs]
type = "gcp_cloud_storage"
inputs = ["keyviz_add_meta"]
encoding.codec = "raw_message"
bucket = "${BUCKET}"
key_prefix = "{{ key_prefix }}"
filename_time_format = ""
filename_append_uuid = false
batch.max_bytes = 1 # DO NOT BATCH
batch.max_events = 1
batch.timeout_secs = 1

[sources.self_metrics]
type = "internal_metrics"

[sinks.self_metrics_sink]
type = "prometheus_exporter"
inputs = ["self_metrics"]
address = "0.0.0.0:${METRICS_PORT}"
```
