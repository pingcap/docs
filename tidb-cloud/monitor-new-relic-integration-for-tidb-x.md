---
title: 将 TiDB Cloud 与 New Relic 集成（PREVIEW）
summary: 了解如何使用 New Relic 集成监控你的 TiDB Cloud 实例。
---

# 将 TiDB Cloud 与 New Relic 集成（PREVIEW）

TiDB Cloud 支持与 New Relic 集成。你可以将 TiDB Cloud 配置为把你的 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例的指标发送到 [New Relic](https://newrelic.com/)。完成后，你可以直接在 New Relic 仪表板中查看这些指标。

## 前提条件 {#prerequisites}

- 要将 TiDB Cloud 与 New Relic 集成，你必须拥有一个 [New Relic](https://newrelic.com/) 账户，并[创建一个 New Relic API key](https://one.newrelic.com/admin-portal/api-keys/home?)，其类型为 `Ingest - License`。

    如果你还没有 New Relic 账户，请访问 [https://newrelic.com/signup](https://newrelic.com/signup) 注册。

- 要为 TiDB Cloud 设置第三方指标集成，你必须在 TiDB Cloud 中具有 `Organization Owner`、`Project Owner` 或 `Instance Manager` 访问权限。要查看集成页面，你至少需要 `Project Viewer` 或 `Instance Viewer` 角色，以访问 TiDB Cloud 中你所在组织下的目标 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例。

## 限制 {#limitations}

- [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 实例不支持 New Relic 集成。
- 当你的 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例状态为 **CREATING**、**RESTORING**、**PAUSED** 或 **RESUMING** 时，不支持 New Relic 集成。
- 删除已集成 New Relic 的实例时，其关联的集成服务也会一并删除。

## 步骤 {#steps}

### 步骤 1. 导入预构建的 New Relic 仪表板 {#step-1-import-the-pre-built-new-relic-dashboard}

目前，适用于 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 的 TiDB Cloud 仪表板尚未在 New Relic marketplace 中提供。在其发布之前，你需要手动下载仪表板 JSON 文件并将其导入 New Relic。

1. 根据你的实例类型下载对应的 New Relic 仪表板 JSON 文件：

    <CustomContent plan="essential">

    - 对于在 2026 年 7 月 1 日及之后创建的 TiDB Cloud Essential 实例，请下载此 JSON 文件：<https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-new-relic-integration-tidb-cloud-dynamic-tracker-essential-v2.json>。注意，`v2` 后缀仅表示仪表板 JSON 文件的版本。
    - 对于在 2026 年 7 月 1 日之前创建的 TiDB Cloud Essential 实例，请下载此 JSON 文件：<https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-new-relic-integration-tidb-cloud-dynamic-tracker-essential.json>。

    </CustomContent>

    <CustomContent plan="premium">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-new-relic-integration-tidb-cloud-dynamic-tracker-premium.json>

    </CustomContent>

2. 在 JSON 文件中，将你的 [New Relic account ID](https://docs.newrelic.com/docs/accounts/accounts-billing/account-structure/account-id/) 添加到所有 `"accountIds": []` 字段中。

    例如：

    ```json
    "accountIds": [
      1234567
    ],
    ```

    > **Note:**
    >
    > 为避免集成错误，请确保已在 JSON 文件中的所有 `"accountIds"` 字段中添加你的 account ID。

3. 登录 [New Relic](https://one.newrelic.com/)，在左侧导航栏中点击 **Dashboards**，然后点击右上角的 **Import dashboard**。

4. 在显示的对话框中，将准备好的 JSON 文件内容粘贴到文本区域，选择权限设置，然后点击 **Save**。

### 步骤 2. 使用你的 New Relic API key 进行集成 {#step-2-integrate-with-your-new-relic-api-key}

<CustomContent plan="essential">

1. 在 [TiDB Cloud console](https://tidbcloud.com/) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .essential }}} 实例的名称，进入其实例概览页面。
2. 在左侧导航窗格中，点击 **Integrations**。
3. 在 **Integrations** 页面上，找到 **New Relic (PREVIEW)** 集成并点击 **Connect**。
4. 输入你的 New Relic API key，选择托管你的 New Relic 账户的区域，然后点击 **Test Integration**。

    - 如果测试成功，会显示 **Confirm** 按钮。
    - 如果测试失败，会显示错误消息。请根据消息进行故障排查，然后重试集成。

5. 点击 **Confirm** 完成集成。

</CustomContent>

<CustomContent plan="premium">

1. 在 [TiDB Cloud console](https://tidbcloud.com/) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .premium }}} 实例的名称，进入其实例概览页面。
2. 在左侧导航窗格中，点击 **Settings** > **Integrations**。
3. 在 **Integrations** 页面上，找到 **New Relic (PREVIEW)** 集成并点击 **Connect**。
4. 输入你的 New Relic API key，选择托管你的 New Relic 账户的区域，然后点击 **Test Integration**。

    - 如果测试成功，会显示 **Confirm** 按钮。
    - 如果测试失败，会显示错误消息。请根据消息进行故障排查，然后重试集成。

5. 点击 **Confirm** 完成集成。

</CustomContent>

## 查看预构建的仪表板 {#view-the-pre-built-dashboard}

完成集成后，要查看预构建的仪表板，请在 [New Relic](https://one.newrelic.com/) 中进入 **Dashboards** > **Dashboard List**，然后选择在[步骤 1](#step-1-import-the-pre-built-new-relic-dashboard)中导入的仪表板。在仪表板页面上，你可以按目标实例名称或实例 ID 进行筛选，然后查看指标。

你也可以从 [TiDB Cloud console](https://tidbcloud.com/) 访问 New Relic 中的 **Dashboard List** 页面：进入目标实例的 **Integrations** 页面，点击 **New Relic (PREVIEW)**，然后点击 **Dashboard**。

## New Relic 可用的指标 {#metrics-available-to-new-relic}

New Relic 会跟踪你的 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例的以下指标。

<CustomContent plan="essential">

> **Note:**
>
> `tidb_cloud.cdc_changefeed_*` 指标仅适用于在 2026 年 7 月 1 日及之后创建的 TiDB Cloud Essential 实例。

| 指标名称 | 指标类型 | 标签 | 描述 |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB server 中当前连接数 |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 活跃连接数 |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按连接结果统计的客户端断开连接数 |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 中每秒运行的所有 SQL 语句消耗的总时间，包括所有进程的 CPU 时间和非空闲等待时间 |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按语句类型统计的每秒执行 SQL 语句数 |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 执行 SQL 语句时每秒发生的错误类型统计（例如语法错误和主键冲突） |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 每秒处理的命令数 |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒命中执行计划缓存的查询数 |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 从网络请求发送到 TiDB 到响应返回给客户端之间的持续时间 |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行的事务数 |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .essential }}} 实例基于行的存储大小（字节） |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .essential }}} 实例的列式存储大小（字节）。如果未启用 TiFlash，则返回 0。 |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 消耗的总 Request Units/s（RU/s） |
| `tidb_cloud.cdc_changefeed_latency` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | changefeed 上游与下游之间的数据复制延时 |
| `tidb_cloud.cdc_changefeed_status` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | Changefeed 状态：<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |

</CustomContent>

<CustomContent plan="premium">

| 指标名称 | 指标类型 | 标签 | 描述 |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB server 中当前连接数 |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 活跃连接数 |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按连接结果统计的客户端断开连接数 |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 中每秒运行的所有 SQL 语句消耗的总时间，包括所有进程的 CPU 时间和非空闲等待时间 |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按语句类型统计的每秒执行 SQL 语句数 |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 执行 SQL 语句时每秒发生的错误类型统计（例如语法错误和主键冲突） |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 每秒处理的命令数 |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒命中执行计划缓存的查询数 |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 从网络请求发送到 TiDB 到响应返回给客户端之间的持续时间 |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行的事务数 |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .premium }}} 实例基于行的存储大小（字节） |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .premium }}} 实例的列式存储大小（字节） |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 消耗的总 Request Units/s（RU/s） |
| `tidb_cloud.cdc_changefeed_latency` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | changefeed 上游与下游之间的数据复制延时 |
| `tidb_cloud.cdc_changefeed_status` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | Changefeed 状态：<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |

</CustomContent>