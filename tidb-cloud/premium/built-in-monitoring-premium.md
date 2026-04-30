---
title: "{{{ .premium }}} 内置指标"
summary: 了解如何查看 {{{ .premium }}} 内置指标以及这些指标的含义。
---

# {{{ .premium }}} 内置指标

TiDB Cloud 会在 **Metrics** 页面收集并展示你的 {{{ .premium }}} 实例的一整套标准指标。通过查看这些指标，你可以轻松识别性能问题，并判断当前数据库部署是否满足你的需求。

## 查看 Metrics 页面 {#view-the-metrics-page}

要在 **Metrics** 页面查看指标，请执行以下步骤：

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击目标 {{{ .premium }}} 实例的名称，进入其概览页面。

    > **提示：**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 在左侧导航栏中，点击 **Monitoring** > **Metrics**。

## 指标保留策略 {#metrics-retention-policy}

对于 {{{ .premium }}} 实例，指标数据会保留 7 天。

## {{{ .premium }}} 实例的指标 {#metrics-for-premium-instances}

以下各节介绍了 {{{ .premium }}} 实例在 **Metrics** 页面上的指标。

### 概览 {#overview}

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Request Units per Second | Total RU per second | Request Unit (RU) 是用于跟踪查询或事务资源消耗的计量单位。除了你运行的查询之外，后台活动也可能消耗 request units，因此当 QPS 为 0 时，每秒 request units 也可能不为 0。 |
| Used Storage Size | {type} | 行存的大小和列存的大小。 |
| Query Per Second | All, {SQL type} | 每秒执行的 SQL 语句数量，按 SQL 类型统计，例如 `SELECT`、`INSERT` 和 `UPDATE`。 |
| Query Duration | avg, avg-{SQL type}, 99, 99-{SQL type} | 从 TiDB 接收到来自客户端的请求，到 TiDB 执行该请求并将结果返回给客户端的持续时间。 |
| Database Time by SQL Types | All, {SQL type} | All：每秒总数据库时间。<br/> {SQL type}：每秒 SQL 语句消耗的数据库时间，按 SQL 类型统计，例如 `SELECT`、`INSERT` 和 `UPDATE`。 |
| Failed Queries | All | 根据每分钟 SQL 语句执行错误统计的错误类型（例如语法错误和主键冲突）。 |
| Command Per Second | {type} | 按命令类型统计的每秒处理命令数。 |
| Queries Using Plan Cache OPS | hit, miss | hit：每秒使用 plan cache 的查询数。<br/> miss：每秒未命中 plan cache 的查询数。 |
| Transaction Per Second | {types}-{transaction model} | 每秒执行的事务数。 |
| Transaction Duration | avg-{transaction model}, 99-{transaction model} | 事务的平均持续时间或第 99 百分位持续时间。 |
| Connection Count | All, active connection | All：连接数。<br/> Active connections：活跃连接数。 |
| Disconnection Count | {result} | 断开连接的客户端数量。 |

### 数据库 {#database}

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| QPS Per DB | All, {database} | 每个数据库每秒执行的 SQL 语句数量，按 SQL 类型统计，例如 `SELECT`、`INSERT` 和 `UPDATE`。 |
| Query Duration Per DB | avg, avg-{database}, 99, 99-{database} | 从数据库接收到来自客户端的请求，到数据库执行该请求并将结果返回给客户端的持续时间。 |
| Failed Query Per DB | All, {database} | 根据每个数据库每秒 SQL 语句执行错误统计的错误类型。 |

### 高级 {#advanced}

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Average Idle Connection Duration | avg-in-txn, avg-not-in-txn | 连接空闲持续时间表示连接处于空闲状态的持续时间。<br/> avg-in-txn：连接处于事务内时的平均连接空闲持续时间。<br/>avg-not-in-txn：连接不处于事务内时的平均连接空闲持续时间。 |
| Get Token Duration | avg, 99 | 获取 SQL 语句 token 所消耗的平均持续时间或第 99 百分位持续时间。 |
| Parse Duration | avg, 99 | 解析 SQL 语句所消耗的平均持续时间或第 99 百分位持续时间。 |
| Compile Duration | avg, 99 | 将解析后的 SQL AST 编译为执行计划所消耗的平均持续时间或第 99 百分位持续时间。 |
| Execute Duration | avg, 99 | 执行 SQL 语句执行计划所消耗的平均持续时间或第 99 百分位持续时间。 |
| Average TiDB KV Request Duration | {Request Type} | 按请求类型统计执行 KV 请求所消耗的平均时间，例如 `Get`、`Prewrite` 和 `Commit`。 |
| Average / P99 PD TSO Wait/RPC Duration | wait-avg/99, rpc-avg/99 | Wait：等待 PD 返回 TSO 的平均持续时间或第 99 百分位持续时间。<br/> RPC：从向 PD 发送 TSO 请求到接收到 TSO 的平均时间或第 99 百分位持续时间。 |

## 常见问题 {#faq}

**1. 为什么此页面上的某些面板为空？**

如果某个面板未提供任何指标，可能原因如下：

- 对应 {{{ .premium }}} 实例的工作负载未触发该指标。例如，在没有失败查询的情况下，failed query 指标始终为空。
- {{{ .premium }}} 实例的 TiDB 版本较低。你需要将其升级到最新版本的 TiDB 才能看到这些指标。

如果排除了以上所有原因，你可以联系 [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) 进行故障排查。

**2. 为什么在极少数情况下指标可能不连续？**

在某些极少数情况下，指标可能会丢失，例如当指标系统压力过高时。

如果你遇到此问题，可以联系 [PingCAP Support](/tidb-cloud/tidb-cloud-support.md) 进行故障排查。