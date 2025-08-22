---
title: 将 TiDB Cloud 集成到 Datadog（预览版）
summary: 了解如何通过 Datadog 集成监控你的 TiDB 集群。
---

# 将 TiDB Cloud 集成到 Datadog（预览版）

TiDB Cloud 支持 Datadog 集成（预览版）。你可以配置 TiDB Cloud，将你的 TiDB 集群的监控指标发送到 [Datadog](https://www.datadoghq.com/)。之后，你可以直接在 Datadog 仪表盘中查看这些指标。

## Datadog 集成版本

自 2022 年 3 月 4 日起，TiDB Cloud 已支持 Datadog 集成（Beta）。从 2025 年 7 月 31 日起，TiDB Cloud 推出了增强的预览版集成。

- **Datadog integration (Preview)**：如果在 2025 年 7 月 31 日前，你的组织内没有未删除的 Datadog 或 New Relic 集成，TiDB Cloud 会为你的组织提供 Datadog 集成的预览版，以体验最新的增强功能。
- **Datadog integration (Beta)**：如果在 2025 年 7 月 31 日前，你的组织内至少有一个未删除的 Datadog 或 New Relic 集成，TiDB Cloud 会保留现有和新建的集成为 Beta 版本，以避免影响当前的仪表盘。我们也会主动与你联系，讨论合适的迁移方案和时间表。

## 前提条件

- 要将 TiDB Cloud 集成到 Datadog，你必须拥有 Datadog 账号和 [Datadog API key](https://app.datadoghq.com/organization-settings/api-keys)。首次创建 Datadog 账号时，Datadog 会为你分配一个 API key。

    如果你还没有 Datadog 账号，请在 [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup) 注册。

- 要为 TiDB Cloud 设置第三方监控指标集成，你必须在 TiDB Cloud 中拥有 `Organization Owner` 或 `Project Owner` 权限。要通过提供的链接访问集成页面或已配置的仪表盘，你至少需要 `Project Viewer` 角色，以访问 TiDB Cloud 项目下的目标集群。

## 限制

- 你无法在 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群中使用 Datadog 集成。

- 当集群状态为 **CREATING**、**RESTORING**、**PAUSED** 或 **RESUMING** 时，Datadog 集成不可用。

- 当带有 Datadog 集成的集群被删除时，其关联的集成服务也会被移除。

## 操作步骤

### 步骤 1. 使用你的 Datadog API Key 进行集成

根据你的 [Datadog 集成版本](#datadog-集成版本)，访问集成页面的步骤有所不同。

<SimpleTab>
<div label="Datadog integration (Preview)">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 在左侧导航栏，点击 **Settings** > **Integrations**。
3. 在 **Integrations** 页面，点击 **Integration to Datadog (PREVIEW)**。
4. 输入你的 Datadog API key 并选择你的 Datadog 站点。
5. 点击 **Test Integration**。

    - 如果测试成功，会显示 **Confirm** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示进行排查并重试集成。

6. 点击 **Confirm** 完成集成。

</div>
<div label="Datadog integration (Beta)">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Integrations**。
3. 在 **Integrations** 页面，点击 **Integration to Datadog (BETA)**。
4. 输入你的 Datadog API key 并选择你的 Datadog 站点。
5. 点击 **Test Integration**。

    - 如果测试成功，会显示 **Confirm** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示进行排查并重试集成。

6. 点击 **Confirm** 完成集成。

</div>
</SimpleTab>

### 步骤 2. 在 Datadog 中安装 TiDB Cloud 集成

根据你的 [Datadog 集成版本](#datadog-集成版本)，操作步骤有所不同。

<SimpleTab>
<div label="Datadog integration (Preview)">

在 Datadog 合并待处理的 [PR](https://github.com/DataDog/integrations-extras/pull/2751) 后，新的 TiDB Cloud 仪表盘将在 Datadog 中可用。在此之前，你可以通过以下步骤手动导入仪表盘：

1. 在 [这里](https://github.com/pingcap/diag/blob/integration/integration/dashboards/datadog-dashboard.json) 下载新仪表盘的 JSON 文件。
2. 登录 [Datadog](https://app.datadoghq.com)，点击左侧导航栏的 **Dashboards**，然后点击右上角的 **+ New Dashboard**。
3. 在弹出的对话框中，点击 **New Dashboard** 创建一个新的空白仪表盘。
4. 在新建的仪表盘页面，点击右上角的 **Configure**，在弹出的面板底部点击 **Import dashboard JSON...**。
5. 在弹出的对话框中，上传下载的 JSON 文件，完成仪表盘的设置。

</div>
<div label="Datadog integration (Beta)">

1. 登录 [Datadog](https://app.datadoghq.com)。
2. 进入 Datadog 的 [**TiDB Cloud Integration** 页面](https://app.datadoghq.com/account/settings#integrations/tidb-cloud)。
3. 在 **Configuration** 标签页，点击 **Install Integration**。 [**TiDB Cloud Cluster Overview**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview) 仪表盘会显示在你的 [**Dashboard List**](https://app.datadoghq.com/dashboard/lists) 中。

</div>
</SimpleTab>

## 查看预置仪表盘

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，进入 **Integrations** 页面。
2. 根据你的 [Datadog 集成版本](#datadog-集成版本)，执行以下操作之一：

    - 对于 Datadog integration (Beta)，点击 **Datadog** 区域的 **Dashboard** 链接。
    - 对于 Datadog integration (Preview)，点击 **Datadog** 区域的 **Dashboard** 链接，在打开的页面左侧导航栏点击 **Dashboard**，然后点击 **TiDB Cloud Dynamic Tracker**，即可查看包含完整指标的新仪表盘。

   >**Note:**
   >
   > 对于 Datadog integration (Preview)，请注意以下事项：
   >
   > - 在 Datadog 合并待处理的 [PR](https://github.com/DataDog/integrations-extras/pull/2751) 之前，**Dashboard** 链接会跳转到旧版仪表盘，该仪表盘不包含预览版引入的最新指标。
   > - 一旦待处理的 [PR](https://github.com/DataDog/integrations-extras/pull/2751) 被合并，**Datadog** 区域的 **Dashboard** 链接将跳转到新版仪表盘。

## Datadog 可用指标

Datadog 会跟踪你的 TiDB 集群的以下指标。

| 指标名称  | 指标类型 | 标签 | 描述                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidb_cloud.db_database_time| gauge | sql_type: Select\|Insert\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | 每秒在 TiDB 中运行的所有 SQL 语句消耗的总时间，包括所有进程的 CPU 时间和非空闲等待时间。 |
| tidb_cloud.db_query_per_second| gauge | type: Select\|Insert\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | 所有 TiDB 实例每秒执行的 SQL 语句数量，按语句类型（`SELECT`、`INSERT` 或 `UPDATE`）统计。 |
| tidb_cloud.db_average_query_duration| gauge | sql_type: Select\|Insert\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | 客户端网络请求发送到 TiDB 与 TiDB 执行后返回请求给客户端之间的持续时间。 |
| tidb_cloud.db_failed_queries| gauge | type: executor:xxxx\|parser:xxxx\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | 按每个 TiDB 实例每秒发生的 SQL 执行错误类型（如语法错误、主键冲突）进行统计。 |
| tidb_cloud.db_total_connection| gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | 当前 TiDB 服务器的连接数。 |
| tidb_cloud.db_active_connections| gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | 活跃连接数。 |
| tidb_cloud.db_disconnections| gauge | result: ok\|error\|undetermined<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | 断开连接的客户端数量。 |
| tidb_cloud.db_command_per_second| gauge | type: Query\|StmtPrepare\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | TiDB 每秒处理的命令数，按命令执行结果的成功或失败分类。 |
| tidb_cloud.db_queries_using_plan_cache_ops| gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | 每秒使用 [Plan Cache](/sql-prepared-plan-cache.md) 的查询统计。执行计划缓存仅支持 prepared statement 命令。 |
| tidb_cloud.db_transaction_per_second| gauge | txn_mode: pessimistic\|optimistic<br/>type: abort\|commit\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | 每秒执行的事务数量。 |
| tidb_cloud.node_storage_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…<br/>component: tikv\|tiflash | TiKV/TiFlash 节点的磁盘使用量（字节）。 |
| tidb_cloud.node_storage_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…<br/>component: tikv\|tiflash | TiKV/TiFlash 节点的磁盘容量（字节）。 |
| tidb_cloud.node_cpu_seconds_total | count | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点的 CPU 使用量。 |
| tidb_cloud.node_cpu_capacity_cores | gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点的 CPU 核心数上限。 |
| tidb_cloud.node_memory_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点已用内存（字节）。 |
| tidb_cloud.node_memory_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/>component: tidb\|tikv\|tiflash | TiDB/TiKV/TiFlash 节点的内存容量（字节）。 |

对于 Datadog integration (Preview)，还可用以下附加指标：

| 指标名称  | 指标类型 | 标签 | 描述                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidbcloud.node_storage_available_bytes | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>` | TiKV/TiFlash 节点可用磁盘空间（字节）。 |
| tidbcloud.disk_read_latency | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | 每个存储设备的读延迟（秒）。 |
| tidbcloud.disk_write_latency | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | 每个存储设备的写延迟（秒）。 |
| tidbcloud.kv_request_duration | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv`<br/>cluster_name: `<cluster name>`<br/>`type`: `BatchGet\|Commit\|Prewrite\|...` | 按类型统计 TiKV 请求的持续时间（秒）。 |
| tidbcloud.component_uptime | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tidb\|tikv\|tiflash`<br/>cluster_name: `<cluster name>` | TiDB 组件的运行时长（秒）。 |
| tidbcloud.ticdc_owner_checkpoint_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>`| changefeed owner 的 checkpoint 时间戳延迟（秒）。 |
| tidbcloud.ticdc_owner_resolved_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | changefeed owner 的 resolved 时间戳延迟（秒）。 |
| tidbcloud.changefeed_status | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | Changefeed 状态：<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |
| tidbcloud.resource_manager_resource_unit_read_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | Resource Manager 消耗的读请求单元（RU）。 |
| tidbcloud.resource_manager_resource_unit_write_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | Resource Manager 消耗的写请求单元（RU）。 |
| tidb_cloud.dm_task_state | gauge | instance: `instance`<br/>task: `task`<br/>cluster_name: `<cluster name>` | 数据迁移任务状态：<br/>0: Invalid<br/>1: New<br/>2: Running<br/>3: Paused<br/>4: Stopped<br/>5: Finished<br/>15: Error |
| tidb_cloud.dm_syncer_replication_lag_bucket | gauge | instance: `instance`<br/>cluster_name: `<cluster name>` | 数据迁移的复制延迟（bucket）。 |
| tidb_cloud.dm_syncer_replication_lag_gauge | gauge | instance: `instance`<br/>task: `task`<br/>cluster_name: `<cluster name>` | 数据迁移的复制延迟（gauge）。 |
| tidb_cloud.dm_relay_read_error_count | gauge | instance: `instance`<br/>cluster_name: `<cluster name>` | 从主库读取 binlog 失败次数。 |