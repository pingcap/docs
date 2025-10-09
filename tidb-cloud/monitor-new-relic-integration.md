---
title: 集成 TiDB Cloud 与 New Relic
summary: 了解如何通过 New Relic 集成监控你的 TiDB 集群。
---

# 集成 TiDB Cloud 与 New Relic

TiDB Cloud 支持与 New Relic 集成。你可以配置 TiDB Cloud，将你的 TiDB 集群的指标发送到 [New Relic](https://newrelic.com/)。之后，你可以直接在 New Relic 的仪表盘中查看这些指标。

## New Relic 集成版本

自 2023 年 4 月 11 日起，TiDB Cloud 支持项目级 New Relic 集成（Beta）。自 2025 年 7 月 31 日起，TiDB Cloud 推出集群级 New Relic 集成（预览版）。自 2025 年 9 月 30 日起，集群级 New Relic 集成将正式发布（GA）。

- **集群级 New Relic 集成**：如果在 2025 年 7 月 31 日前，你的组织内没有未删除的旧版项目级 Datadog 或 New Relic 集成，TiDB Cloud 将为你的组织提供集群级 New Relic 集成，以体验最新的增强功能。
- **旧版项目级 New Relic 集成（Beta）**：如果在 2025 年 7 月 31 日前，你的组织内至少有一个未删除的旧版项目级 Datadog 或 New Relic 集成，TiDB Cloud 会在项目级保留现有和新建的集成，以避免影响当前的仪表盘。请注意，旧版项目级 New Relic 集成将于 2025 年 10 月 31 日弃用。如果你的组织仍在使用这些旧版集成，请按照 [迁移 Datadog 和 New Relic 集成](/tidb-cloud/migrate-metrics-integrations.md) 的指引，迁移到新的集群级集成，以最大程度减少对指标相关服务的影响。

## 前提条件

- 若要将 TiDB Cloud 与 New Relic 集成，你必须拥有一个 [New Relic](https://newrelic.com/) 账号，并[创建一个 `Ingest - License` 类型的 New Relic API key](https://one.newrelic.com/admin-portal/api-keys/home?)。

    如果你还没有 New Relic 账号，请在 [这里](https://newrelic.com/signup) 注册。

- 若要为 TiDB Cloud 设置第三方指标集成，你必须在 TiDB Cloud 中拥有 `Organization Owner` 或 `Project Owner` 权限。若要通过提供的链接查看集成页面或访问已配置的仪表盘，你至少需要 `Project Viewer` 角色，以访问 TiDB Cloud 项目下的目标集群。

## 限制

- 你无法在 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 或 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群中使用 New Relic 集成。

- 当集群状态为 **CREATING**、**RESTORING**、**PAUSED** 或 **RESUMING** 时，New Relic 集成不可用。

- 当带有 New Relic 集成的集群被删除时，其关联的集成服务也会被移除。

## 操作步骤

### 步骤 1. 使用你的 New Relic API Key 集成

根据你的 [New Relic 集成版本](#new-relic-集成版本)，访问集成页面的步骤有所不同。

<SimpleTab>
<div label="集群级 New Relic 集成">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称，进入其概览页面。
2. 在左侧导航栏，点击 **Settings** > **Integrations**。
3. 在 **Integrations** 页面，点击 **Integration to New Relic**。
4. 输入你的 New Relic API key，并选择 New Relic 的站点。
5. 点击 **Test Integration**。

    - 如果测试成功，会显示 **Confirm** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示排查并重试集成。

6. 点击 **Confirm** 完成集成。

</div>
<div label="旧版项目级 New Relic 集成（Beta）">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的下拉框切换到目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Integrations**。
3. 在 **Integrations** 页面，点击 **Integration to New Relic (BETA)**。
4. 输入你的 New Relic API key，并选择 New Relic 的站点。
5. 点击 **Test Integration**。

    - 如果测试成功，会显示 **Confirm** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示排查并重试集成。

6. 点击 **Confirm** 完成集成。

</div>
</SimpleTab>

### 步骤 2. 在 New Relic 中添加 TiDB Cloud 仪表盘

根据你的 [New Relic 集成版本](#new-relic-集成版本)，操作步骤有所不同。

<SimpleTab>
<div label="集群级 New Relic 集成">

在 New Relic 合并待处理的 [PR](https://github.com/newrelic/newrelic-quickstarts/pull/2681) 后，将会有新的 TiDB Cloud 仪表盘可用。在此之前，你可以通过以下步骤手动导入仪表盘：

1. 准备新仪表盘的 JSON 文件。

    1. 在 [这里](https://github.com/pingcap/diag/blob/integration/integration/dashboards/newrelic-dashboard.json) 下载模板 JSON 文件。
    2. 在 JSON 文件的第 4 行添加 `"permissions": "PUBLIC_READ_WRITE"`，如下所示：

        ```json
        {
          "name": "TiDB Cloud Dynamic Tracker",
          "description": null,
          "permissions": "PUBLIC_READ_WRITE",
          ...
        }
        ```

    3. 在 JSON 文件的所有 `"accountIds": []` 字段中，添加你的 New Relic 账号 ID。

        例如：

        ```json
        "accountIds": [
          1234567
        ],
        ```

        > **注意**：
        >
        > 为避免集成出错，请确保你的账号 ID 已添加到 JSON 文件中所有的 `"accountIds"` 字段。

2. 登录 [New Relic](https://one.newrelic.com/)，点击左侧导航栏的 **Dashboards**，然后点击右上角的 **Import dashboard**。
3. 在弹出的对话框中，将准备好的 JSON 文件内容全部粘贴到文本区域，然后点击 **Import dashboard**。

</div>
<div label="旧版项目级 New Relic 集成（Beta）">

1. 登录 [New Relic](https://one.newrelic.com/)。
2. 点击 **Add Data**，搜索 `TiDB Cloud`，然后进入 **TiDB Cloud Monitoring** 页面。你也可以直接点击 [链接](https://one.newrelic.com/marketplace?state=79bf274b-0c01-7960-c85c-3046ca96568e) 访问该页面。
3. 选择你的账号 ID，并在 New Relic 中创建仪表盘。

</div>
</SimpleTab>

## 查看预置仪表盘

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 **Integrations** 页面。

2. 在 **New Relic** 区域点击 **Dashboard** 链接，查看你的 TiDB 集群的预置仪表盘。

3. 根据你的 [New Relic 集成版本](#new-relic-集成版本)，执行以下操作之一：

    - 对于集群级 New Relic 集成，点击 **TiDB Cloud Dynamic Tracker** 查看新仪表盘。
    - 对于旧版项目级 New Relic 集成（Beta），点击 **TiDB Cloud Monitoring** 查看旧版仪表盘。

## New Relic 可用指标

New Relic 会跟踪你的 TiDB 集群的以下指标。

| 指标名称  | 指标类型 | 标签 | 描述                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidb_cloud.db_database_time| gauge | sql_type: Select\|Insert\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 每秒在 TiDB 中运行的所有 SQL 语句消耗的总时间，包括所有进程的 CPU 时间和非空闲等待时间。 |
| tidb_cloud.db_query_per_second| gauge | type: Select\|Insert\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 所有 TiDB 实例每秒执行的 SQL 语句数量，按 `SELECT`、`INSERT`、`UPDATE` 等语句类型统计。 |
| tidb_cloud.db_average_query_duration| gauge | sql_type: Select\|Insert\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 客户端网络请求发送到 TiDB 与 TiDB 执行后返回给客户端之间的耗时。 |
| tidb_cloud.db_failed_queries| gauge | type: executor:xxxx\|parser:xxxx\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 每秒每个 TiDB 实例发生的 SQL 执行错误，按错误类型（如语法错误、主键冲突等）统计。 |
| tidb_cloud.db_total_connection| gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 当前 TiDB 服务器的连接数。 |
| tidb_cloud.db_active_connections| gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 活跃连接数。 |
| tidb_cloud.db_disconnections| gauge | result: ok\|error\|undetermined<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 断开连接的客户端数量。 |
| tidb_cloud.db_command_per_second| gauge | type: Query\|StmtPrepare\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | TiDB 每秒处理的命令数，按命令执行结果的成功或失败分类。 |
| tidb_cloud.db_queries_using_plan_cache_ops| gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 每秒使用 [Plan Cache](/sql-prepared-plan-cache.md) 的查询统计。执行计划缓存仅支持 prepared statement 命令。 |
| tidb_cloud.db_transaction_per_second| gauge | txn_mode: pessimistic\|optimistic<br/><br/>type: abort\|commit\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | 每秒执行的事务数。 |
| tidb_cloud.node_storage_used_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…<br/><br/>component: tikv\|tiflash | TiKV/TiFlash 节点的磁盘使用量（字节）。 |
| tidb_cloud.node_storage_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…<br/><br/>component: tikv\|tiflash | TiKV/TiFlash 节点的磁盘容量（字节）。 |
| tidb_cloud.node_cpu_seconds_total (Beta only) | count | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点的 CPU 使用量。 |
| tidb_cloud.node_cpu_capacity_cores | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点的 CPU 核心数上限。 |
| tidb_cloud.node_memory_used_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点已用内存（字节）。 |
| tidb_cloud.node_memory_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点的内存容量（字节）。 |

对于集群级 New Relic 集成，还支持以下额外指标：

| 指标名称  | 指标类型 | 标签 | 描述                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidb_cloud.node_storage_available_bytes | gauge | instance: `tidb-0\|tidb-1\|...`<br/><br/>component: `tikv\|tiflash`<br/><br/>cluster_name: `<cluster name>` | TiKV 或 TiFlash 节点可用磁盘空间（字节）。 |
| tidb_cloud.node_disk_read_latency | gauge | instance: `tidb-0\|tidb-1\|...`<br/><br/>component: `tikv\|tiflash`<br/><br/>cluster_name: `<cluster name>`<br/><br/>`device`: `nvme.*\|dm.*` | 每个存储设备的读延迟（秒）。 |
| tidb_cloud.node_disk_write_latency | gauge | instance: `tidb-0\|tidb-1\|...`<br/><br/>component: `tikv\|tiflash`<br/><br/>cluster_name: `<cluster name>`<br/><br/>`device`: `nvme.*\|dm.*` | 每个存储设备的写延迟（秒）。 |
| tidb_cloud.db_kv_request_duration | gauge | instance: `tidb-0\|tidb-1\|...`<br/><br/>component: `tikv`<br/><br/>cluster_name: `<cluster name>`<br/><br/>`type`: `BatchGet\|Commit\|Prewrite\|...` | TiKV 按类型请求的耗时（秒）。 |
| tidb_cloud.db_component_uptime | gauge | instance: `tidb-0\|tidb-1\|...`<br/><br/>component: `tidb\|tikv\|tiflash`<br/><br/>cluster_name: `<cluster name>` | TiDB 组件的运行时长（秒）。 |
| tidb_cloud.cdc_changefeed_latency (AKA cdc_changefeed_checkpoint_ts_lag) | gauge | changefeed_id: `<changefeed-id>`<br/><br/>cluster_name: `<cluster name>`| changefeed owner 的 checkpoint timestamp 延迟（秒）。 |
| tidb_cloud.cdc_changefeed_resolved_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/><br/>cluster_name: `<cluster name>` | changefeed owner 的 resolved timestamp 延迟（秒）。 |
| tidb_cloud.cdc_changefeed_status | gauge | changefeed_id: `<changefeed-id>`<br/><br/>cluster_name: `<cluster name>` | Changefeed 状态：<br/><br/>`-1`: Unknown<br/><br/>`0`: Normal<br/><br/>`1`: Warning<br/><br/>`2`: Failed<br/><br/>`3`: Stopped<br/><br/>`4`: Finished<br/><br/>`6`: Warning<br/><br/>`7`: Other |
| tidb_cloud.resource_manager_resource_unit_read_request_unit | gauge | cluster_name: `<cluster name>`<br/><br/>resource_group: `<group-name>` | Resource Manager 消耗的读请求单元（RU）。 |
| tidb_cloud.resource_manager_resource_unit_write_request_unit | gauge | cluster_name: `<cluster name>`<br/><br/>resource_group: `<group-name>` | Resource Manager 消耗的写请求单元（RU）。 |
| tidb_cloud.dm_task_state | gauge | instance: `instance`<br/><br/>task: `task`<br/><br/>cluster_name: `<cluster name>` | 数据迁移任务状态：<br/><br/>`0`: Invalid<br/><br/>`1`: New<br/><br/>`2`: Running<br/><br/>`3`: Paused<br/><br/>`4`: Stopped<br/><br/>`5`: Finished<br/><br/>`15`: Error |
| tidb_cloud.dm_syncer_replication_lag_bucket | gauge | instance: `instance`<br/><br/>cluster_name: `<cluster name>` | 数据迁移的复制延迟（bucket）。 |
| tidb_cloud.dm_syncer_replication_lag_gauge | gauge | instance: `instance`<br/><br/>task: `task`<br/><br/>cluster_name: `<cluster name>` | 数据迁移的复制延迟（gauge）。 |
| tidb_cloud.dm_relay_read_error_count | gauge | instance: `instance`<br/><br/>cluster_name: `<cluster name>` | 从主库读取 binlog 失败次数。 |
| tidb_cloud.node_memory_available_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点可用内存（字节）。 |
| tidb_cloud.cdc_changefeed_replica_rows | gauge | changefeed_id: `<changefeed-id>`<br/><br/>cluster_name: `<cluster name>` | TiCDC 节点每秒写入下游的事件数。 |
| tidb_cloud.node_cpu_seconds_total_rate | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点的 CPU 使用率。 |