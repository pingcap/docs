---
title: 集成 TiDB Cloud 与 Prometheus 和 Grafana
summary: 了解如何通过集成 Prometheus 和 Grafana 监控你的 TiDB 集群。
---

# 集成 TiDB Cloud 与 Prometheus 和 Grafana

TiDB Cloud 提供了一个 [Prometheus](https://prometheus.io/) API 端点。如果你拥有 Prometheus service，可以轻松地通过该端点监控 TiDB Cloud 的关键统计/指标（信息）。

本文档介绍了如何配置你的 Prometheus service 以从 TiDB Cloud 端点读取关键统计/指标（信息），以及如何使用 [Grafana](https://grafana.com/) 查看这些统计/指标（信息）。

## Prometheus 集成版本

自 2022 年 3 月 15 日起，TiDB Cloud 支持项目级 Prometheus 集成（Beta）。自 2025 年 10 月 21 日起，TiDB Cloud 推出集群级 Prometheus 集成（预览版）。自 2025 年 12 月 2 日起，集群级 Prometheus 集成正式可用（GA）。

- **集群级 Prometheus 集成**：如果在 2025 年 10 月 21 日前，你的组织内没有未删除的遗留项目级 Prometheus 集成，TiDB Cloud 将为你的组织提供集群级 Prometheus 集成，以体验最新增强功能。

- **遗留项目级 Prometheus 集成（Beta）**：如果在 2025 年 10 月 21 日前，你的组织内至少有一个未删除的遗留项目级 Prometheus 集成，TiDB Cloud 会为你的组织保留现有和新建的项目级集成，以避免影响当前的仪表盘。

    > **注意**
    >
    > 遗留项目级 Prometheus 集成将于 2026 年 1 月 9 日弃用。如果你的组织仍在使用这些遗留集成，请按照 [迁移 Prometheus 集成](/tidb-cloud/migrate-prometheus-metrics-integrations.md) 迁移到新的集群级集成，以最大程度减少对统计/指标（信息）相关 service 的影响。

## 前提条件

- 若要集成 TiDB Cloud 与 Prometheus，你必须拥有自托管或托管的 Prometheus service。

- 若要为 TiDB Cloud 设置第三方统计/指标（信息）集成，你必须在 TiDB Cloud 中拥有 `Organization Owner` 或 `Project Owner` 访问权限。若要查看集成页面，你至少需要 `Project Viewer` 角色，以访问 TiDB Cloud 项目下的目标集群。

## 限制

- Prometheus 和 Grafana 集成目前仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。
- 当集群状态为 **CREATING**、**RESTORING**、**PAUSED** 或 **RESUMING** 时，不支持 Prometheus 和 Grafana 集成。

## 步骤

### 步骤 1. 获取 Prometheus 的 scrape_config 文件

在配置 Prometheus service 以读取 TiDB Cloud 统计/指标（信息）之前，你需要先在 TiDB Cloud 中生成一个 `scrape_config` YAML 文件。该 `scrape_config` 文件包含一个唯一的 bearer token，允许 Prometheus service 监控你的目标集群。

根据你的 [Prometheus 集成版本](#prometheus-integration-versions)，获取 Prometheus 的 `scrape_config` 文件及访问集成页面的步骤有所不同。

<SimpleTab>
<div label="集群级 Prometheus 集成">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 在左侧导航栏，点击 **Settings** > **Integrations**。
3. 在 **Integrations** 页面，点击 **Integration to Prometheus**。
4. 点击 **Add File**，为当前集群生成并显示 `scrape_config` 文件。
5. 复制 `scrape_config` 文件内容，供后续使用。

</div>
<div label="遗留项目级 Prometheus 集成（Beta）">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的下拉框切换到目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Integrations**。
3. 在 **Integrations** 页面，点击 **Integration to Prometheus (BETA)**。
4. 点击 **Add File**，为当前项目生成并显示 scrape_config 文件。
5. 复制 scrape_config 文件内容，供后续使用。

</div>
</SimpleTab>

> **注意：**
>
> 出于安全考虑，TiDB Cloud 仅会显示新生成的 `scrape_config` 文件一次。请确保在关闭文件窗口前复制内容。如果忘记复制，需要在 TiDB Cloud 中删除该 `scrape_config` 文件并重新生成。要删除 `scrape_config` 文件，选择该文件，点击 **...**，然后点击 **Delete**。

### 步骤 2. 集成 Prometheus

1. 在你的 Prometheus service 指定的监控目录中，找到 Prometheus 配置文件。

    例如，`/etc/prometheus/prometheus.yml`。

2. 在 Prometheus 配置文件中，找到 `scrape_configs` 部分，然后将从 TiDB Cloud 获取的 `scrape_config` 文件内容复制到该部分。

3. 在你的 Prometheus service 中，检查 **Status** > **Targets**，确认新的 `scrape_config` 文件已被读取。如果没有，你可能需要重启 Prometheus service。

### 步骤 3. 使用 Grafana GUI 仪表盘可视化统计/指标（信息）

当你的 Prometheus service 已经从 TiDB Cloud 读取统计/指标（信息）后，可以按如下方式使用 Grafana GUI 仪表盘进行可视化：

1. 根据你的 [Prometheus 集成版本](#prometheus-integration-versions)，下载 TiDB Cloud for Prometheus 的 Grafana 仪表盘 JSON 文件的链接不同。

    - 对于集群级 Prometheus 集成，请在[此处](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker.json)下载 Grafana 仪表盘 JSON 文件。
    - 对于遗留项目级 Prometheus 集成（Beta），请在[此处](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-grafana-dashboard-UI.json)下载 Grafana 仪表盘 JSON 文件。

2. [将该 JSON 导入到你自己的 Grafana GUI](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard)，以可视化统计/指标（信息）。

    > **注意：**
    >
    > 如果你已经在使用 Prometheus 和 Grafana 监控 TiDB Cloud，并希望引入新可用的统计/指标（信息），建议新建一个仪表盘，而不是直接更新现有仪表盘的 JSON。

3. （可选）根据需要自定义仪表盘，例如添加或移除面板、变更数据源、修改显示选项等。

关于如何使用 Grafana 的更多信息，请参见 [Grafana 官方文档](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)。

## scrape_config 轮转最佳实践

为提升数据安全性，建议定期轮转 `scrape_config` 文件的 bearer token。

1. 按照 [步骤 1](#step-1-get-a-scrape_config-file-for-prometheus) 为 Prometheus 创建新的 `scrape_config` 文件。
2. 将新文件内容添加到你的 Prometheus 配置文件中。
3. 确认 Prometheus service 仍能从 TiDB Cloud 读取后，从 Prometheus 配置文件中移除旧的 `scrape_config` 文件内容。
4. 在项目或集群的 **Integrations** 页面，删除对应的旧 `scrape_config` 文件，阻止他人使用其读取 TiDB Cloud Prometheus 端点。

## Prometheus 可用统计/指标（信息）

Prometheus 会跟踪你的 TiDB 集群的以下统计/指标（信息）数据。

| 统计/指标（信息）名称 | 统计/指标（信息）类型  | 标签 | 描述 |
|:--- |:--- |:--- |:--- |
| tidbcloud_db_queries_total| count | sql_type: `Select\|Insert\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | 执行的 statement 总数 |
| tidbcloud_db_failed_queries_total | count | type: `planner:xxx\|executor:2345\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | 执行错误总数 |
| tidbcloud_db_connections | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | 当前 TiDB server 的连接数 |
| tidbcloud_db_query_duration_seconds | histogram | sql_type: `Select\|Insert\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | statement 的耗时直方图 |
| tidbcloud_changefeed_latency | gauge | changefeed_id | changefeed 上游与下游间的数据同步延时 |
| tidbcloud_changefeed_checkpoint_ts | gauge | changefeed_id | changefeed 的 checkpoint 时间戳，表示已成功写入下游的最大 TSO（Timestamp Oracle）|
| tidbcloud_changefeed_replica_rows | gauge | changefeed_id | changefeed 每秒写入下游的副本行数 |
| tidbcloud_node_storage_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>component: `tikv\|tiflash` | TiKV/TiFlash 节点的磁盘已用字节数 |
| tidbcloud_node_storage_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>component: `tikv\|tiflash` | TiKV/TiFlash 节点的磁盘容量字节数 |
| tidbcloud_node_cpu_seconds_total | count | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的 CPU 使用量 |
| tidbcloud_node_cpu_capacity_cores | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的 CPU 限制核数 |
| tidbcloud_node_memory_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的已用内存字节数 |
| tidbcloud_node_memory_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | TiDB/TiKV/TiFlash 节点的内存容量字节数 |
| tidbcloud_node_storage_available_bytes | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>` | TiKV/TiFlash 节点可用磁盘空间（字节）|
| tidbcloud_disk_read_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | 每个存储设备的读延时（秒）|
| tidbcloud_disk_write_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | 每个存储设备的写延时（秒）|
| tidbcloud_kv_request_duration | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv`<br/>cluster_name: `<cluster name>`<br/>`type`: `BatchGet\|Commit\|Prewrite\|...` | TiKV 各类型请求的耗时（秒）|
| tidbcloud_component_uptime | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tidb\|tikv\|tiflash`<br/>cluster_name: `<cluster name>` | TiDB 组件的运行时长（秒）|
| tidbcloud_ticdc_owner_resolved_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | changefeed owner 的 resolved 时间戳延时（秒）|
| tidbcloud_changefeed_status | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | changefeed 状态：<br/>`-1`: 未知<br/>`0`: 正常<br/>`1`: 警告<br/>`2`: 失败<br/>`3`: 已停止<br/>`4`: 已完成<br/>`6`: 警告<br/>`7`: 其他 |
| tidbcloud_resource_manager_resource_unit_read_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | Resource Manager 消耗的读请求单元数 |
| tidbcloud_resource_manager_resource_unit_write_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | Resource Manager 消耗的写请求单元数 |

对于集群级 Prometheus 集成，还可获取以下额外统计/指标（信息）：

| 统计/指标（信息）名称 | 统计/指标（信息）类型  | 标签 | 描述 |
|:--- |:--- |:--- |:--- |
| tidbcloud_dm_task_status | gauge | instance: `instance`<br/>task: `task`<br/>cluster_name: `<cluster name>` | 数据迁移任务状态：<br/>0: Invalid<br/>1: New<br/>2: Running<br/>3: Paused<br/>4: Stopped<br/>5: Finished<br/>15: Error |
| tidbcloud_dm_syncer_replication_lag_bucket | gauge | instance: `instance`<br/>cluster_name: `<cluster name>` | 数据迁移的同步延时（bucket）|
| tidbcloud_dm_syncer_replication_lag_gauge | gauge | instance: `instance`<br/>task: `task`<br/>cluster_name: `<cluster name>` | 数据迁移的同步延时（gauge）|
| tidbcloud_dm_relay_read_error_count | count | instance: `instance`<br/>cluster_name: `<cluster name>` | 从主库读取 binlog 失败的次数 |

## 常见问题

- 为什么同一统计/指标（信息）在 Grafana 和 TiDB Cloud 控制台上同时显示的数值不同？

    Grafana 与 TiDB Cloud 的聚合计算逻辑不同，因此显示的聚合值可能存在差异。你可以在 Grafana 中调整 `mini step` 配置，以获得更细粒度的统计/指标（信息）值。