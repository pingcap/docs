---
title: 集成 TiDB Cloud 与 Datadog（公测中）
summary: 了解如何使用 Datadog 集成监控你的 TiDB Cloud 实例。
---

# 集成 TiDB Cloud 与 Datadog（公测中）

TiDB Cloud 支持与 Datadog 集成。你可以将 TiDB Cloud 配置为把你的 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例的指标发送到 [Datadog](https://www.datadoghq.com/)。完成后，你可以直接在 Datadog 仪表板中查看这些指标。

## 前提条件 {#prerequisites}

- 要将 TiDB Cloud 与 Datadog 集成，你必须拥有一个 Datadog 账户以及一个 [Datadog API key](https://app.datadoghq.com/organization-settings/api-keys)。首次创建 Datadog 账户时，Datadog 会为你分配一个 API key。

    如果你还没有 Datadog 账户，请访问 [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup) 注册。

- 要为 TiDB Cloud 设置第三方指标集成，你必须在 TiDB Cloud 中具有 `Organization Owner`、`Project Owner` 或 `Instance Manager` 访问权限。要查看集成页面，你至少需要 `Project Viewer` 或 `Instance Viewer` 角色，以访问 TiDB Cloud 中你所在组织下目标 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例。

## 限制 {#limitations}

- [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 实例不支持 Datadog 集成。
- 当你的 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例状态为 **CREATING**、**RESTORING**、**PAUSED** 或 **RESUMING** 时，不支持 Datadog 集成。

## 步骤 {#steps}

### 第 1 步：导入预构建的 Datadog 仪表板 {#step-1-import-the-pre-built-datadog-dashboard}

目前，适用于 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 的 TiDB Cloud 仪表板尚未在 Datadog 集成市场中提供。你需要手动下载仪表板 JSON 文件并将其导入 Datadog。

1. 下载适用于你的实例类型的 Datadog 仪表板 JSON 文件：

    <CustomContent plan="essential">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-datadog-integration-tidb-cloud-dynamic-tracker-essential.json>

    </CustomContent>

    <CustomContent plan="premium">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-datadog-integration-tidb-cloud-dynamic-tracker-premium.json>

    </CustomContent>

2. 登录 [Datadog](https://app.datadoghq.com)，然后进入 **Dashboards** > **Dashboard List**。

3. 点击右上角的 **+ New Dashboard**。输入仪表板名称，然后选择 **Start from blank dashboard**。

4. 在新建的仪表板中，点击右上角的齿轮图标（**Configure**），然后选择 **Import dashboard JSON...**。

5. 在弹出的对话框中，粘贴 JSON 内容，或拖放 JSON 文件。

6. 点击 **Yes, Replace** 确认导入。

### 第 2 步：使用你的 Datadog API key 进行集成 {#step-2-integrate-with-your-datadog-api-key}

<CustomContent plan="essential">

1. 在 [TiDB Cloud console](https://tidbcloud.com/) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .essential }}} 实例的名称，进入其实例概览页面。
2. 在左侧导航栏中，点击 **Integrations** > **Integration to Datadog (Preview)**。
3. 输入你的 Datadog API key，并选择你的 Datadog Region。
4. 点击 **Test Integration**。

    - 如果测试成功，会显示 **Confirm** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示进行故障排查，然后重试集成。

5. 点击 **Confirm** 完成集成。

</CustomContent>

<CustomContent plan="premium">

1. 在 [TiDB Cloud console](https://tidbcloud.com/) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .premium }}} 实例的名称，进入其实例概览页面。
2. 在左侧导航栏中，点击 **Settings** > **Integrations** > **Integration to Datadog (Preview)**。
3. 输入你的 Datadog API key，并选择你的 Datadog Region。
4. 点击 **Test Integration**。

    - 如果测试成功，会显示 **Confirm** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示进行故障排查，然后重试集成。

5. 点击 **Confirm** 完成集成。

</CustomContent>

## 查看预构建的仪表板 {#view-the-pre-built-dashboard}

完成集成后，要查看预构建的仪表板，请在 [Datadog](https://app.datadoghq.com) 中进入 **Dashboards** > **Dashboard List**，然后选择在[第 1 步](#step-1-import-the-pre-built-datadog-dashboard)中导入的仪表板。在仪表板页面中，你可以按目标实例名称进行筛选并查看指标。

你也可以从 [TiDB Cloud console](https://tidbcloud.com/) 进入 Datadog 的 **Dashboard List** 页面：进入目标实例的 **Integrations** 页面，点击 **Datadog (Preview)**，然后点击 **Dashboard**。

## Datadog 可用的指标 {#metrics-available-to-datadog}

Datadog 会跟踪你的 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例的以下指标。

<CustomContent plan="essential">

> **Note:**
>
> 当前，{{{ .essential }}} 的 changefeed 功能仅按需提供，且 `tidb_cloud.changefeed_*` 指标不可用。

| Metric name | Metric type | Labels | Description |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB server 中当前连接数 |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 活跃连接数 |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按连接结果统计的客户端断开连接数 |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 中运行的所有 SQL 语句每秒消耗的总时间，包括所有进程的 CPU 时间和非空闲等待时间 |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按语句类型统计的每秒执行 SQL 语句数 |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 执行 SQL 语句时每秒发生的错误类型统计（例如语法错误和主键冲突） |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 每秒处理的命令数 |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒命中执行计划缓存的查询数 |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 从网络请求发送到 TiDB 到响应返回给客户端之间的持续时间 |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行的事务数 |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .essential }}} 实例基于行存储的数据大小（字节） |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .essential }}} 实例基于列存储的数据大小（字节）。如果未启用 TiFlash，则返回 0。 |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 消耗的总 Request Units/s（RU/s） |

</CustomContent>

<CustomContent plan="premium">

| Metric name | Metric type | Labels | Description |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB server 中当前连接数 |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 活跃连接数 |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按连接结果统计的客户端断开连接数 |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 中运行的所有 SQL 语句每秒消耗的总时间，包括所有进程的 CPU 时间和非空闲等待时间 |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按语句类型统计的每秒执行 SQL 语句数 |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 执行 SQL 语句时每秒发生的错误类型统计（例如语法错误和主键冲突） |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 每秒处理的命令数 |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒命中执行计划缓存的查询数 |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 从网络请求发送到 TiDB 到响应返回给客户端之间的持续时间 |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行的事务数 |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .premium }}} 实例基于行存储的数据大小（字节） |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .premium }}} 实例基于列存储的数据大小（字节） |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 消耗的总 Request Units/s（RU/s） |
| `tidb_cloud.changefeed_latency` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | changefeed 上游与下游之间的数据复制延时 |
| `tidb_cloud.changefeed_status` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | Changefeed 状态：<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |

</CustomContent>