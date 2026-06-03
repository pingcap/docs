---
title: 集成 TiDB Cloud 与 Prometheus 和 Grafana（预览版）
summary: 了解如何通过 Prometheus 和 Grafana 集成监控你的 TiDB Cloud 实例。
---

# 集成 TiDB Cloud 与 Prometheus 和 Grafana（预览版）

TiDB Cloud 提供了一个 [Prometheus](https://prometheus.io/) API 端点。如果你已有 Prometheus 服务，即可通过该端点轻松监控 TiDB Cloud 的关键指标。

本文介绍如何配置你的 Prometheus 服务，从 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 端点读取关键指标，以及如何使用 [Grafana](https://grafana.com/) 查看这些指标。

## 前提条件 {#prerequisites}

- 要将 TiDB Cloud 与 Prometheus 集成，你必须拥有一个自托管或托管的 Prometheus 服务。

- 要为 TiDB Cloud 设置第三方指标集成，你必须在 TiDB Cloud 中具有 `Organization Owner` 或 `Instance Manager` 访问权限。要查看集成页面，你至少需要 `Project Viewer` 或 `Instance Viewer` 角色，以访问 TiDB Cloud 中你的 Organization 下目标 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例。

## 限制 {#limitation}

- [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 实例不支持 Prometheus 和 Grafana 集成。
- 当你的 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例状态为 **CREATING**、**RESTORING**、**PAUSED** 或 **RESUMING** 时，不支持 Prometheus 和 Grafana 集成。

## 步骤 {#steps}

### 步骤 1. 获取用于 Prometheus 的 `scrape_config` 文件 {#step-1-get-a-scrape-config-file-for-prometheus}

在配置 Prometheus 服务以读取 TiDB Cloud 指标之前，你需要先在 TiDB Cloud 中生成一个 `scrape_config` YAML 文件。`scrape_config` 文件包含一个唯一的 bearer token，用于允许 Prometheus 服务监控目标 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例。

<CustomContent plan="essential">

1. 在 [TiDB Cloud console](https://tidbcloud.com/) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .essential }}} 实例名称，进入其实例概览页面。
2. 在左侧导航栏中，点击 **Integrations** > **Integration to Prometheus(Preview)**。
3. 点击 **Add File**，为当前 {{{ .essential }}} 实例生成并显示 `scrape_config` 文件。
4. 复制 `scrape_config` 文件内容，供后续使用。

</CustomContent>

<CustomContent plan="premium">

1. 在 [TiDB Cloud console](https://tidbcloud.com/) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .premium }}} 实例名称，进入其实例概览页面。
2. 在左侧导航栏中，点击 **Settings** > **Integrations** > **Integration to Prometheus(Preview)**。
3. 点击 **Add File**，为当前 {{{ .premium }}} 实例生成并显示 `scrape_config` 文件。
4. 复制 `scrape_config` 文件内容，供后续使用。

</CustomContent>

> **Note:**
>
> - 出于安全原因，TiDB Cloud 仅会显示一次新生成的 `scrape_config` 文件。请确保在关闭文件窗口之前复制其内容。 
> - 如果你忘记复制，请在 TiDB Cloud 中删除该 `scrape_config` 文件并重新生成一个。要删除 `scrape_config` 文件，请选中文件，点击 **...**，然后点击 **Delete**。

### 步骤 2. 与 Prometheus 集成 {#step-2-integrate-with-prometheus}

1. 在 Prometheus 服务指定的监控目录中，找到 Prometheus 配置文件。

    例如，`/etc/prometheus/prometheus.yml`。

2. 在 Prometheus 配置文件中，找到 `scrape_configs` 部分，然后将从 TiDB Cloud 获取的 `scrape_config` 文件内容复制到该部分。

3. 在 Prometheus 服务中，检查 **Status** > **Targets**，确认新的 `scrape_config` 文件已被读取。如果没有，你可能需要重启 Prometheus 服务。

### 步骤 3. 使用 Grafana GUI 仪表板可视化指标 {#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics}

在 Prometheus 服务读取到来自 TiDB Cloud 的指标后，你可以按如下方式使用 Grafana GUI 仪表板对指标进行可视化：

1. 通过以下链接下载适用于 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 的 Grafana dashboard JSON 文件：

    <CustomContent plan="essential">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker-essential.json>

    </CustomContent>
    <CustomContent plan="premium">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker-premium.json>

    </CustomContent>

2. [将此 JSON 导入你自己的 Grafana GUI](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard) 以可视化这些指标。

    > **Note:**
    >
    > 如果你已经在使用 Prometheus 和 Grafana 监控 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例，并且希望纳入新提供的指标，建议你创建一个新的 dashboard，而不是直接更新现有 dashboard 的 JSON。

3. （可选）根据需要自定义 dashboard，例如添加或删除面板、更改数据源以及修改显示选项。

有关如何使用 Grafana 的更多信息，请参见 [Grafana documentation](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)。

## 轮换 `scrape_config` 的最佳实践 {#best-practice-for-rotating-scrape-config}

为提高数据安全性，建议定期轮换 `scrape_config` 文件中的 bearer token。

1. 按照[步骤 1](#step-1-get-a-scrape_config-file-for-prometheus)为 Prometheus 创建新的 `scrape_config` 文件。
2. 将新文件的内容添加到你的 Prometheus 配置文件中。
3. 确认 Prometheus 服务可以从 TiDB Cloud 读取数据后，从 Prometheus 配置文件中移除旧 `scrape_config` 文件的内容。
4. 在你的 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例的 **Integrations** 页面中，删除对应的旧 `scrape_config` 文件，以防止其他人继续使用它从 TiDB Cloud Prometheus 端点读取数据。

## Prometheus 可用指标 {#metrics-available-to-prometheus}

Prometheus 会跟踪你的 <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 实例的以下指标数据。

<CustomContent plan="essential">

> **Note:**
>
> {{{ .essential }}} 不支持 TiCDC 组件，因此当前 `tidbcloud_changefeed_*` 指标不可用。

| Metric name | Metric type | Labels | Description |
|:--- |:--- |:--- |:--- |
| `tidbcloud_db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB server 中当前连接数 |
| `tidbcloud_db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 活跃连接数 |
| `tidbcloud_db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按连接结果统计的客户端断开连接数 |
| `tidbcloud_db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 一项时间模型统计值，表示所有进程 CPU 消耗总和与非空闲等待时间总和之和 |
| `tidbcloud_db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按语句类型统计的每秒执行 SQL 语句数 |
| `tidbcloud_db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行 SQL 语句时发生的错误类型统计（例如语法错误、主键冲突） |
| `tidbcloud_db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 每秒处理的命令数 |
| `tidbcloud_db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒命中 Execution Plan Cache 的查询统计 |
| `tidbcloud_db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 从网络请求发送到 TiDB 到返回给客户端之间的持续时间 |
| `tidbcloud_db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行的事务数 |
| `tidbcloud_db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .essential }}} 实例基于行存储的数据大小（字节） |
| `tidbcloud_db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .essential }}} 实例基于列存储的数据大小（字节）。如果未启用 TiFlash，则返回 0。 |
| `tidbcloud_resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 已消耗的 Request Units (RU) 总量。|

</CustomContent>

<CustomContent plan="premium">

| Metric name | Metric type | Labels | Description |
|:--- |:--- |:--- |:--- |
| `tidbcloud_db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB server 中当前连接数 |
| `tidbcloud_db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 活跃连接数 |
| `tidbcloud_db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按连接结果统计的客户端断开连接数 |
| `tidbcloud_db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 一项时间模型统计值，表示所有进程 CPU 消耗总和与非空闲等待时间总和之和 |
| `tidbcloud_db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按语句类型统计的每秒执行 SQL 语句数 |
| `tidbcloud_db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行 SQL 语句时发生的错误类型统计（例如语法错误、主键冲突） |
| `tidbcloud_db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 每秒处理的命令数 |
| `tidbcloud_db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒命中 Execution Plan Cache 的查询统计 |
| `tidbcloud_db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 从网络请求发送到 TiDB 到返回给客户端之间的持续时间 |
| `tidbcloud_db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行的事务数 |
| `tidbcloud_db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .premium }}} 实例基于行存储的数据大小（字节） |
| `tidbcloud_db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .premium }}} 实例基于列存储的数据大小（字节）。 |
| `tidbcloud_resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 已消耗的 Request Units (RU) 总量。 |
| `tidbcloud_changefeed_latency` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | changefeed 上游与下游之间的数据复制延迟 |
| `tidbcloud_changefeed_status` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | Changefeed 状态：<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |

</CustomContent>

## FAQ {#faq}

- 为什么同一时间在 Grafana 和 TiDB Cloud console 中看到的同一指标值不同？

    Grafana 和 TiDB Cloud 使用不同的聚合计算逻辑，因此显示的聚合值可能不同。你可以调整 Grafana 中的 `mini step` 配置，以获得更细粒度的指标值。