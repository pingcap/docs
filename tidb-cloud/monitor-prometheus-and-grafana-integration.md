---
title: 集成 TiDB Cloud 与 Prometheus 和 Grafana（Beta）
summary: 了解如何通过 Prometheus 和 Grafana 集成监控你的 TiDB 集群。
---

# 集成 TiDB Cloud 与 Prometheus 和 Grafana（Beta）

TiDB Cloud 提供了一个 [Prometheus](https://prometheus.io/) API 端点（Beta）。如果你拥有 Prometheus 服务，可以轻松地通过该端点监控 TiDB Cloud 的关键指标。

本文档介绍了如何配置 Prometheus 服务以从 TiDB Cloud 端点读取关键指标，以及如何使用 [Grafana](https://grafana.com/) 查看这些指标。

## 前提条件

- 若要将 TiDB Cloud 与 Prometheus 集成，你必须拥有自托管或托管的 Prometheus 服务。

- 若要编辑 TiDB Cloud 的第三方集成设置，你必须拥有组织的 **Organization Owner** 权限，或在 TiDB Cloud 中拥有目标项目的 **Project Member** 权限。

## 限制

- 你无法在 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群中使用 Prometheus 和 Grafana 集成。

- 当集群状态为 **CREATING**、**RESTORING**、**PAUSED** 或 **RESUMING** 时，Prometheus 和 Grafana 集成不可用。

## 步骤

### 步骤 1. 获取 Prometheus 的 scrape_config 文件

在配置 Prometheus 服务以读取 TiDB Cloud 指标之前，你需要先在 TiDB Cloud 中生成一个 `scrape_config` YAML 文件。该 `scrape_config` 文件包含一个唯一的 bearer token，允许 Prometheus 服务监控当前项目中的所有数据库集群。

要获取 Prometheus 的 `scrape_config` 文件，请执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Integrations**。
3. 在 **Integrations** 页面，点击 **Integration to Prometheus (BETA)**。
4. 点击 **Add File**，为当前项目生成并显示 scrape_config 文件。

5. 复制 `scrape_config` 文件的内容，以备后续使用。

    > **注意：**
    >
    > 出于安全考虑，TiDB Cloud 只会显示新生成的 `scrape_config` 文件一次。请确保在关闭文件窗口前复制内容。如果忘记复制，需要在 TiDB Cloud 中删除该 `scrape_config` 文件并重新生成。要删除 `scrape_config` 文件，选择该文件，点击 **...**，然后点击 **Delete**。

### 步骤 2. 集成 Prometheus

1. 在你的 Prometheus 服务指定的监控目录中，找到 Prometheus 配置文件。

    例如，`/etc/prometheus/prometheus.yml`。

2. 在 Prometheus 配置文件中，找到 `scrape_configs` 部分，然后将从 TiDB Cloud 获取的 `scrape_config` 文件内容复制到该部分。

3. 在你的 Prometheus 服务中，检查 **Status** > **Targets**，确认新的 `scrape_config` 文件已被读取。如果没有，你可能需要重启 Prometheus 服务。

### 步骤 3. 使用 Grafana GUI 仪表盘可视化指标

当你的 Prometheus 服务已从 TiDB Cloud 读取指标后，可以按如下方式使用 Grafana GUI 仪表盘进行可视化：

1. 在 [此处](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-grafana-dashboard-UI.json) 下载 TiDB Cloud 的 Grafana 仪表盘 JSON 文件。

2. [将该 JSON 导入到你自己的 Grafana GUI](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard) 以可视化指标。
    
    > **注意：**
    >
    > 如果你已经在使用 Prometheus 和 Grafana 监控 TiDB Cloud，并希望引入新提供的指标，建议新建一个仪表盘，而不是直接更新现有仪表盘的 JSON。

3. （可选）根据需要自定义仪表盘，例如添加或移除面板、变更数据源、修改显示选项等。

关于如何使用 Grafana 的更多信息，请参见 [Grafana 文档](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)。

## scrape_config 的轮换最佳实践

为提升数据安全性，建议定期轮换 `scrape_config` 文件中的 bearer token。

1. 按照 [步骤 1](#step-1-get-a-scrape_config-file-for-prometheus) 为 Prometheus 创建新的 `scrape_config` 文件。
2. 将新文件的内容添加到你的 Prometheus 配置文件中。
3. 确认 Prometheus 服务仍能从 TiDB Cloud 读取数据后，从 Prometheus 配置文件中移除旧的 `scrape_config` 文件内容。
4. 在项目的 **Integrations** 页面，删除对应的旧 `scrape_config` 文件，防止他人使用其读取 TiDB Cloud Prometheus 端点。

## Prometheus 可用指标

Prometheus 会跟踪你的 TiDB 集群的以下指标数据。

| 指标名称 |  指标类型  | 标签 | 描述 |
|:--- |:--- |:--- |:--- |
| tidbcloud_db_queries_total| count | sql_type: `Select\|Insert\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | 执行的语句总数 |
| tidbcloud_db_failed_queries_total | count | type: `planner:xxx\|executor:2345\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | 执行错误的总数 |
| tidbcloud_db_connections | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | 当前 TiDB 服务器的连接数 |
| tidbcloud_db_query_duration_seconds | histogram | sql_type: `Select\|Insert\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | 语句的耗时直方图 |
| tidbcloud_changefeed_latency | gauge | changefeed_id | changefeed 上游与下游之间的数据同步延迟 |
| tidbcloud_changefeed_checkpoint_ts | gauge | changefeed_id | changefeed 的检查点时间戳，表示已成功写入下游的最大 TSO（Timestamp Oracle）|
| tidbcloud_changefeed_replica_rows | gauge | changefeed_id | changefeed 每秒写入下游的同步行数 |
| tidbcloud_node_storage_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>component: `tikv\|tiflash` | TiKV/TiFlash 节点的磁盘已用字节数 |
| tidbcloud_node_storage_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>component: `tikv\|tiflash` | TiKV/TiFlash 节点的磁盘容量字节数 |
| tidbcloud_node_cpu_seconds_total | count | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的 CPU 使用量 |
| tidbcloud_node_cpu_capacity_cores | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的 CPU 限制核数 |
| tidbcloud_node_memory_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的已用内存字节数 |
| tidbcloud_node_memory_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的内存容量字节数 |
| tidbcloud_node_storage_available_bytes | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>` | TiKV/TiFlash 节点可用磁盘空间（字节）|
| tidbcloud_disk_read_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | 每个存储设备的读延迟（秒）|
| tidbcloud_disk_write_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | 每个存储设备的写延迟（秒）|
| tidbcloud_kv_request_duration | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv`<br/>cluster_name: `<cluster name>`<br/>`type`: `BatchGet\|Commit\|Prewrite\|...` | TiKV 按类型请求的耗时（秒）|
| tidbcloud_component_uptime | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tidb\|tikv\|tiflash`<br/>cluster_name: `<cluster name>` | TiDB 组件的运行时长（秒）|
| tidbcloud_ticdc_owner_resolved_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | changefeed owner 的 resolved timestamp 延迟（秒）|
| tidbcloud_changefeed_status | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | changefeed 状态：<br/>`-1`: 未知<br/>`0`: 正常<br/>`1`: 警告<br/>`2`: 失败<br/>`3`: 已停止<br/>`4`: 已完成<br/>`6`: 警告<br/>`7`: 其他 |
| tidbcloud_resource_manager_resource_unit_read_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | Resource Manager 消耗的读请求单元 |
| tidbcloud_resource_manager_resource_unit_write_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | Resource Manager 消耗的写请求单元 |

## 常见问题

- 为什么同一指标在 Grafana 和 TiDB Cloud 控制台上同时显示的数值不同？

    因为 Grafana 和 TiDB Cloud 的聚合计算逻辑不同，所以显示的聚合值可能会有差异。你可以调整 Grafana 中的 `mini step` 配置，以获得更细粒度的指标值。