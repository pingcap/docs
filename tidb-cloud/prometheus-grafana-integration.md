---
title: 将 TiDB Cloud 集成到 Prometheus 和 Grafana（预览版）
summary: 了解如何通过 Prometheus 和 Grafana 集成监控你的 TiDB Cloud 实例。
---

# 将 TiDB Cloud 集成到 Prometheus 和 Grafana（预览版）

TiDB Cloud 提供了一个 [Prometheus](https://prometheus.io/) API 端点。如果你拥有 Prometheus service，可以轻松地从该端点监控 TiDB Cloud 的关键统计/指标（信息）。

本文档介绍了如何配置你的 Prometheus service，从 <CustomContent plan="essential">TiDB Cloud Essential</CustomContent><CustomContent plan="premium">TiDB Cloud Premium</CustomContent> 端点读取关键统计/指标（信息），以及如何使用 [Grafana](https://grafana.com/) 查看这些统计/指标（信息）。

## 前提条件

- 若要将 TiDB Cloud 集成到 Prometheus，必须拥有自托管或托管的 Prometheus service。

- 若要为 TiDB Cloud 设置第三方统计/指标（信息）集成，你必须在 TiDB Cloud 中拥有 `Organization Owner` 或 `Instance Manager` 访问权限。若要查看集成页面，至少需要 `Project Viewer` 或 `Instance Viewer` 角色，以访问你所在 Organization 下目标 <CustomContent plan="essential">TiDB Cloud Essential 集群</CustomContent><CustomContent plan="premium">TiDB Cloud Premium 实例</CustomContent>。

## 限制

- Prometheus 和 Grafana 集成不适用于 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 集群。
- 当集群状态为 **CREATING**、**RESTORING**、**PAUSED** 或 **RESUMING** 时，不支持 Prometheus 和 Grafana 集成。

## 操作步骤

### 步骤 1. 获取 Prometheus 的 `scrape_config` 文件

在配置 Prometheus service 以读取 TiDB Cloud 统计/指标（信息）之前，你需要先在 TiDB Cloud 中生成一个 `scrape_config` YAML 文件。该 `scrape_config` 文件包含一个唯一的 bearer token，允许 Prometheus service 监控你的目标 <CustomContent plan="essential">集群</CustomContent><CustomContent plan="premium">实例</CustomContent>。

<CustomContent plan="essential">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标 TiDB Cloud Essential 集群名称，进入其概览页面。
2. 在左侧导航栏，点击 **Integrations** > **Integration to Prometheus(Preview)**。
3. 点击 **Add File**，为当前 TiDB Cloud Essential 集群生成并显示 `scrape_config` 文件。
4. 复制 `scrape_config` 文件内容，供后续使用。

</CustomContent>

<CustomContent plan="premium">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 TiDB Cloud Premium 实例名称，进入其概览页面。
2. 在左侧导航栏，点击 **Settings** > **Integrations** > **Integration to Prometheus(Preview)**。
3. 点击 **Add File**，为当前 TiDB Cloud Premium 实例生成并显示 `scrape_config` 文件。
4. 复制 `scrape_config` 文件内容，供后续使用。

</CustomContent>

> **注意：**
>
> - 出于安全考虑，TiDB Cloud 只会显示新生成的 `scrape_config` 文件一次。请确保在关闭文件窗口前复制内容。
> - 如果忘记复制，可以在 TiDB Cloud 中删除该 `scrape_config` 文件并重新生成。要删除 `scrape_config` 文件，选择该文件，点击 **...**，然后点击 **Delete**。

### 步骤 2. 集成到 Prometheus

1. 在你的 Prometheus service 指定的监控目录中，找到 Prometheus 配置文件。

    例如：`/etc/prometheus/prometheus.yml`。

2. 在 Prometheus 配置文件中，找到 `scrape_configs` 部分，然后将从 TiDB Cloud 获取的 `scrape_config` 文件内容复制到该部分。

3. 在 Prometheus service 中，检查 **Status** > **Targets**，以验证新的 `scrape_config` 文件是否已被读取。如果没有，可能需要重启 Prometheus service。

### 步骤 3. 使用 Grafana GUI 仪表盘可视化统计/指标（信息）

当你的 Prometheus service 成功读取 TiDB Cloud 的统计/指标（信息）后，可以通过 Grafana GUI 仪表盘进行可视化，操作如下：

1. 从以下链接下载 <CustomContent plan="essential">TiDB Cloud Essential</CustomContent><CustomContent plan="premium">TiDB Cloud Premium</CustomContent> 的 Grafana 仪表盘 JSON 文件：

    <CustomContent plan="essential">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker-essential.json>

    </CustomContent>
    <CustomContent plan="premium">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker-premium.json>

    </CustomContent>

2. [将该 JSON 导入到你自己的 Grafana GUI](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard)，以可视化统计/指标（信息）。

    > **注意：**
    >
    > 如果你已经使用 Prometheus 和 Grafana 监控 <CustomContent plan="essential">集群</CustomContent><CustomContent plan="premium">实例</CustomContent>，并希望引入新开放的统计/指标（信息），建议新建一个仪表盘，而不是直接更新现有仪表盘的 JSON。

3. （可选）根据需要自定义仪表盘，例如添加或移除面板、变更数据源、修改显示选项等。

关于如何使用 Grafana 的更多信息，请参见 [Grafana 官方文档](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)。

## `scrape_config` 轮转最佳实践

为提升数据安全性，建议定期轮转 `scrape_config` 文件的 bearer token。

1. 按照 [步骤 1](#step-1-get-a-scrape_config-file-for-prometheus) 创建新的 Prometheus `scrape_config` 文件。
2. 将新文件内容添加到你的 Prometheus 配置文件中。
3. 确认 Prometheus service 能够从 TiDB Cloud 读取后，从 Prometheus 配置文件中移除旧的 `scrape_config` 文件内容。
4. 在 <CustomContent plan="essential">集群</CustomContent><CustomContent plan="premium">实例</CustomContent> 的 **Integrations** 页面，删除对应的旧 `scrape_config` 文件，阻止其他人使用该文件从 TiDB Cloud Prometheus 端点读取数据。

## Prometheus 可用统计/指标（信息）

Prometheus 会为你的 <CustomContent plan="essential">集群</CustomContent><CustomContent plan="premium">实例</CustomContent> 跟踪以下统计/指标（信息）。

<CustomContent plan="essential">

> **注意：**
>
> TiDB Cloud Essential 不支持 TiCDC 组件，因此当前不提供 `tidbcloud_changefeed_*` 相关统计/指标（信息）。

| 统计/指标（信息）名称 | 统计/指标（信息）类型 | 标签 | 描述 |
|:--- |:--- |:--- |:--- |
| `tidbcloud_db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 当前 TiDB server 的连接数 |
| `tidbcloud_db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 活跃连接数 |
| `tidbcloud_db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按连接结果统计的断开 client 数量 |
| `tidbcloud_db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 时间模型统计，表示所有进程 CPU 消耗总和与非空闲等待时间总和之和 |
| `tidbcloud_db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行的 SQL 语句数，按语句类型统计 |
| `tidbcloud_db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行 SQL 语句时发生的错误类型（如语法错误、主键冲突）统计 |
| `tidbcloud_db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 每秒处理的命令数 |
| `tidbcloud_db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒命中执行计划缓存的查询统计 |
| `tidbcloud_db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 网络请求发送到 TiDB 并返回 client 的耗时 |
| `tidbcloud_db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行的事务数 |
| `tidbcloud_db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 集群行存储空间（字节数） |
| `tidbcloud_db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 集群列存储空间（字节数）。若未启用 TiFlash，则返回 0。 |
| `tidbcloud_resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 已消耗的 Request Units（RU）总数。|

</CustomContent>

<CustomContent plan="premium">

| 统计/指标（信息）名称 | 统计/指标（信息）类型 | 标签 | 描述 |
|:--- |:--- |:--- |:--- |
| `tidbcloud_db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 当前 TiDB server 的连接数 |
| `tidbcloud_db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 活跃连接数 |
| `tidbcloud_db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 按连接结果统计的断开 client 数量 |
| `tidbcloud_db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 时间模型统计，表示所有进程 CPU 消耗总和与非空闲等待时间总和之和 |
| `tidbcloud_db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行的 SQL 语句数，按语句类型统计 |
| `tidbcloud_db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行 SQL 语句时发生的错误类型（如语法错误、主键冲突）统计 |
| `tidbcloud_db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB 每秒处理的命令数 |
| `tidbcloud_db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒命中执行计划缓存的查询统计 |
| `tidbcloud_db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 网络请求发送到 TiDB 并返回 client 的耗时 |
| `tidbcloud_db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 每秒执行的事务数 |
| `tidbcloud_db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 集群行存储空间（字节数） |
| `tidbcloud_db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 集群列存储空间（字节数）。 |
| `tidbcloud_resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 已消耗的 Request Units（RU）总数。 |
| `tidbcloud_changefeed_latency` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | changefeed 上游与下游间的数据同步延时 |
| `tidbcloud_changefeed_status` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | changefeed 状态：<br/>`-1`: 未知<br/>`0`: 正常<br/>`1`: 警告<br/>`2`: 失败<br/>`3`: 已停止<br/>`4`: 已完成<br/>`6`: 警告<br/>`7`: 其他 |

</CustomContent>

## 常见问题

- 为什么同一统计/指标（信息）在 Grafana 和 TiDB Cloud 控制台同时显示的值不同？

    Grafana 和 TiDB Cloud 使用不同的聚合计算逻辑，因此显示的聚合值可能不同。你可以在 Grafana 中调整 `mini step` 配置，以获得更细粒度的统计/指标（信息）值。