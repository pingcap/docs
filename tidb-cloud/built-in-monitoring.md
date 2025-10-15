---
title: TiDB Cloud 内置指标
summary: 了解如何查看 TiDB Cloud 内置指标及这些指标的含义。
---

# TiDB Cloud 内置指标

TiDB Cloud 会在 **Metrics** 页面收集并展示你的集群的全套标准指标。通过查看这些指标，你可以轻松识别性能问题，并判断当前的数据库部署是否满足你的需求。

## 查看 Metrics 页面

要在 **Metrics** 页面查看指标，请按照以下步骤操作：

1. 在你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群的名称，进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏，点击 **Monitoring** > **Metrics**。

## 指标保留策略

对于 TiDB Cloud 集群，指标数据会保留 7 天。

## TiDB Cloud Dedicated 集群的指标

以下章节介绍了 TiDB Cloud Dedicated 集群在 **Metrics** 页面上的各项指标。

### 概览

| 指标名称  | 标签 | 描述                                   |
| :------------| :------| :-------------------------------------------- |
| Database Time by SQL types | database time, {SQL type} | database time：每秒的总数据库时间。<br/> {SQL type}：按 SQL 类型（如 `SELECT`、`INSERT`、`UPDATE`）统计的每秒数据库时间。|
| Query Per Second | {SQL type} | 所有 TiDB 实例每秒执行的 SQL 语句数量，按 SQL 类型（如 `SELECT`、`INSERT`、`UPDATE`）统计。|
| Query Duration | avg-{SQL type}, 99-{SQL type} | 从 TiDB 接收到客户端请求到 TiDB 执行请求并返回结果给客户端的持续时间。通常，客户端请求以 SQL 语句形式发送；但该持续时间也可能包括如 `COM_PING`、`COM_SLEEP`、`COM_STMT_FETCH` 和 `COM_SEND_LONG_DATA` 等命令的执行时间。TiDB 支持 Multi-Query，即客户端可以一次发送多条 SQL 语句，如 `select 1; select 1; select 1;`。此时，该查询的总执行时间包含所有 SQL 语句的执行时间。|
| Failed Queries | All, {Error type} @ {instance} | 按每个 TiDB 实例每分钟 SQL 语句执行错误统计的错误类型（如语法错误、主键冲突）。包含发生错误的模块和错误码。|
| Command Per Second | Query, StmtExecute, and StmtPrepare | 所有 TiDB 实例每秒按命令类型处理的命令数量。|
| Queries Using Plan Cache OPS | hit, miss | hit：所有 TiDB 实例每秒使用计划缓存的查询数量。<br/> miss：所有 TiDB 实例每秒未命中计划缓存的查询数量。|
| Transaction Per Second | {types}-{transaction model} | 每秒执行的事务数量。|
| Transaction Duration | avg-{transaction model}, 99-{transaction model} | 事务的平均或第 99 百分位持续时间。|
| Connection Count | All, active connection | All：所有 TiDB 实例的连接数。<br/> Active connections：所有 TiDB 实例的活跃连接数。|
| Disconnection Count | {instance}-{result} | 每个 TiDB 实例断开连接的客户端数量。|

### 高级

| 指标名称  | 标签 | 描述                                   |
| :------------| :------| :-------------------------------------------- |
| Average Idle Connection Duration | avg-in-txn, avg-not-in-txn | 连接空闲持续时间表示连接处于空闲状态的时长。<br/> avg-in-txn：连接处于事务中时的平均空闲持续时间。<br/> avg-not-in-txn：连接不在事务中时的平均空闲持续时间。|
| Get Token Duration | avg, 99 | 获取 SQL 语句 token 所消耗的平均或第 99 百分位持续时间。|
| Parse Duration | avg, 99 | 解析 SQL 语句所消耗的平均或第 99 百分位持续时间。|
| Compile Duration | avg, 99 | 将解析后的 SQL AST 编译为执行计划所消耗的平均或第 99 百分位持续时间。|
| Execute Duration | avg, 99 | 执行 SQL 语句执行计划所消耗的平均或第 99 百分位持续时间。|
| Average TiDB KV Request Duration | {Request Type} | 所有 TiDB 实例按请求类型（如 `Get`、`Prewrite`、`Commit`）执行 KV 请求的平均耗时。|
| Average TiKV gRPC Duration | {Request Type} | 所有 TiKV 实例按请求类型（如 `kv_get`、`kv_prewrite`、`kv_commit`）执行 gRPC 请求的平均耗时。|
| Average / P99 PD TSO Wait/RPC Duration | wait-avg/99, rpc-avg/99 | Wait：所有 TiDB 实例等待 PD 返回 TSO 的平均或第 99 百分位持续时间。<br/> RPC：所有 TiDB 实例从发送 TSO 请求到 PD 到收到 TSO 的平均或第 99 百分位持续时间。|
| Average / P99 Storage Async Write Duration | avg, 99 | 异步写入所消耗的平均或第 99 百分位持续时间。平均存储异步写入持续时间 = 平均 store 持续时间 + 平均 apply 持续时间。|
| Average / P99 Store Duration | avg, 99 | 异步写入过程中 store 循环所消耗的平均或第 99 百分位持续时间。|
| Average / P99 Apply Duration | avg, 99 | 异步写入过程中 apply 循环所消耗的平均或第 99 百分位持续时间。|
| Average / P99 Append Log Duration | avg, 99 | Raft 追加日志所消耗的平均或第 99 百分位持续时间。|
| Average / P99 Commit Log Duration | avg, 99 | Raft 提交日志所消耗的平均或第 99 百分位持续时间。|
| Average / P99 Apply Log Duration | avg, 99 | Raft 应用日志所消耗的平均或第 99 百分位持续时间。|
| Affected Rows | {SQL type} | 按 SQL 类型每秒处理的行数。|
| Leader Count | {instance} | TiKV 节点上承载的 Raft leader Region 数量。|
| Region Count | {instance} | TiKV 节点管理的总数据 Region 数量。|

### 服务器

| 指标名称  | 标签 | 描述                                   |
| :------------| :------| :-------------------------------------------- |
| TiDB Uptime | node | 每个 TiDB 节点自上次重启以来的运行时长。|
| TiDB CPU Usage | node, limit | 每个 TiDB 节点的 CPU 使用率统计或上限。|
| TiDB Memory Usage | node, limit | 每个 TiDB 节点的内存使用量统计或上限。|
| TiKV Uptime | node | 每个 TiKV 节点自上次重启以来的运行时长。|
| TiKV CPU Usage | node, limit | 每个 TiKV 节点的 CPU 使用率统计或上限。|
| TiKV Memory Usage | node, limit | 每个 TiKV 节点的内存使用量统计或上限。|
| TiKV IO Bps | node-write, node-read | 每个 TiKV 节点每秒读写的总输入/输出字节数。|
| TiKV Storage Usage | node, limit | 每个 TiKV 节点的存储使用量统计或上限。|
| TiFlash Uptime | node | 每个 TiFlash 节点自上次重启以来的运行时长。|
| TiFlash CPU Usage | node, limit | 每个 TiFlash 节点的 CPU 使用率统计或上限。|
| TiFlash Memory Usage | node, limit | 每个 TiFlash 节点的内存使用量统计或上限。|
| TiFlash IO MBps | node-write, node-read | 每个 TiFlash 节点的读写总字节数。|
| TiFlash Storage Usage | node, limit | 每个 TiFlash 节点的存储使用量统计或上限。|

## TiDB Cloud Starter 和 TiDB Cloud Essential 集群的指标

**Metrics** 页面为 TiDB Cloud Starter 和 TiDB Cloud Essential 集群提供了两个指标标签页：

- **Cluster Status**：展示集群级别的主要指标。
- **Database Status**：展示数据库级别的主要指标。

### Cluster Status

下表展示了 **Cluster Status** 标签页下的集群级主要指标。

| 指标名称  | 标签 | 描述                                   |
| :------------| :------| :-------------------------------------------- |
| Request Units | RU per second | Request Unit（RU）是用于衡量 TiDB Cloud Starter 集群中查询或事务资源消耗的单位。除了用户查询，后台活动也会消耗 RU，因此即使 QPS 为 0，每秒 RU 使用量也可能不为零。|
| Capacity vs Usage (RU/s) | Provisioned capacity (RCU), Consumed RU/s | TiDB Cloud Essential 集群中配置的 Request Capacity Units（RCU）和每秒消耗的 Request Units（RU）。|
| Used Storage Size | Row-based storage, Columnar storage | 行存储和列存储的存储空间大小。|
| Query Per Second | All, {SQL type} | 每秒执行的 SQL 语句数量，按 SQL 类型（如 `SELECT`、`INSERT`、`UPDATE`）统计。|
| Query Duration | Avg, P99, P99-{SQL type} | 从客户端请求到 TiDB Cloud Starter 或 TiDB Cloud Essential 集群接收请求、执行并返回结果的持续时间。|
| Failed Query | All | 每秒 SQL 语句执行错误的数量。|
| Transaction Per Second | All | 每秒执行的事务数量。|
| Transaction Duration | Avg, P99 | 事务的执行持续时间。|
| Lock-wait | P95, P99 | 事务等待获取悲观锁所花费的时间。较高的值通常表示对同一行或键存在竞争。|
| Total Connection | All | 连接到 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的连接数。|
| Idle Connection Duration | P99, P99(in-txn), P99(not-in-txn) | 连接在开启事务时处于空闲状态的时间。较长的持续时间通常表示应用逻辑较慢或存在长事务。|

### Database Status

下表展示了 **Database Status** 标签页下的数据库级主要指标。

| 指标名称  | 标签 | 描述                                   |
| :------------| :------| :-------------------------------------------- |
| QPS Per DB | All, {Database name} | 每个数据库每秒执行的 SQL 语句数量，按 SQL 类型（如 `SELECT`、`INSERT`、`UPDATE`）统计。|
| Average Query Duration Per DB | All, {Database name} | 从客户端请求到数据库接收请求、执行并返回结果的持续时间。|
| Failed Query Per DB | All, {Database name} | 每个数据库每秒 SQL 语句执行错误的类型统计。|

## FAQ

**1. 为什么本页面的某些面板为空？**

如果某个面板没有显示任何指标，可能的原因如下：

- 对应集群的负载没有触发该指标。例如，如果没有失败的查询，则失败查询指标始终为空。
- 集群版本较低。你需要将其升级到最新的 TiDB 版本才能看到这些指标。

如果排除了上述原因，你可以联系 [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) 进行排查。

**2. 为什么在极少数情况下指标会出现不连续？**

在极少数情况下，指标可能会丢失，例如当指标系统压力过大时。

如果你遇到此问题，可以联系 [PingCAP Support](/tidb-cloud/tidb-cloud-support.md) 进行排查。