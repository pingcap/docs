---
title: TiDB 中的超时
summary: 了解 TiDB 中的超时机制，以及排查错误的解决方案。
---

# TiDB 中的超时

本文档描述了 TiDB 中的各种超时设置，帮助你排查错误。

## GC 超时

TiDB 的事务实现采用 MVCC（多版本并发控制）机制。当新写入的数据覆盖旧数据时，旧数据不会被立即替换，而是与新数据一同保留。不同版本通过时间戳进行区分。TiDB 通过定期的垃圾回收（GC）机制，清理不再需要的旧数据。

- 对于 TiDB 版本早于 v4.0：

    默认情况下，每个 MVCC 版本（一致性快照）会被保留 10 分钟。耗时超过 10 分钟的事务在读取时会返回错误 `GC life time is shorter than transaction duration`。

- 对于 TiDB v4.0 及更高版本：

    对于持续时间不超过 24 小时的运行中的事务，垃圾回收（GC）在事务执行期间会被阻塞，不会出现 `GC life time is shorter than transaction duration` 错误。

如果在某些情况下需要临时延长读取时间，可以增加 MVCC 版本的保留时间：

- 对于 TiDB 版本早于 v5.0：在 TiDB 的 `mysql.tidb` 表中调整 `tikv_gc_life_time`。
- 对于 TiDB v5.0 及更高版本：调整系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)。

注意，系统变量配置会立即生效且具有全局作用。增加其值会延长所有快照的存活时间，减少则会立即缩短所有快照的存活时间。过多的 MVCC 版本会影响 TiDB 集群的性能，因此需要及时将其调整回之前的设置。

<CustomContent platform="tidb">

> **Tip:**
>
> 具体来说，当 Dumpling 从 TiDB 导出数据（少于 1 TB）时，如果 TiDB 版本为 v4.0.0 及以上，且 Dumpling 能访问 PD 地址以及 TiDB 集群的 [`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md) 表，Dumpling 会自动调整 GC 安全点以阻止 GC，而不会影响原有集群。
>
> 但在以下任一场景中，Dumpling 无法自动调整 GC 时间：
>
> - 数据量非常大（超过 1 TB）。
> - Dumpling 无法直接连接 PD，例如 TiDB 集群在 TiDB Cloud 或在与 Dumpling 分离的 Kubernetes 上。
>
> 在此类场景中，必须提前手动延长 GC 时间，以避免在导出过程中因 GC 导致导出失败。
>
> 更多详情请参见 [Manually set the TiDB GC time](/dumpling-overview.md#manually-set-the-tidb-gc-time)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Tip:**
>
> 具体来说，当 Dumpling 从 TiDB 导出数据（少于 1 TB）时，如果 TiDB 版本大于或等于 v4.0.0，且 Dumpling 能访问 TiDB 集群的 PD 地址，Dumpling 会自动延长 GC 时间，而不会影响原有集群。
>
> 但在以下任一场景中，Dumpling 无法自动调整 GC 时间：
>
> - 数据量非常大（超过 1 TB）。
> - Dumpling 无法直接连接 PD，例如 TiDB 集群在 TiDB Cloud 或在 Kubernetes 上，与 Dumpling 分离。
>
> 在此类场景中，必须提前手动延长 GC 时间，以避免在导出过程中因 GC 导致导出失败。
>
> 更多详情请参见 [Manually set the TiDB GC time](https://docs.pingcap.com/tidb/stable/dumpling-overview#manually-set-the-tidb-gc-time)。

</CustomContent>

有关 GC 的更多信息，请参见 [GC Overview](/garbage-collection-overview.md)。

## 事务超时

在事务启动后未提交或回滚的场景中，可能需要更细粒度的控制和更短的超时，以防止长时间持有锁。在这种情况下，可以使用 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)（在 TiDB v7.6.0 中引入）来控制用户会话中事务的空闲超时。

GC 不会影响正在进行的事务，但对悲观事务的最大并发数、事务超时限制以及事务使用的内存有限制。你可以通过 TiDB 配置文件中 `[performance]` 类别下的 `max-txn-ttl` 来修改事务超时时间，默认值为 `60` 分钟。

像 `INSERT INTO t10 SELECT * FROM t1` 这样的 SQL 语句不受 GC 影响，但超出 `max-txn-ttl` 后会因超时而回滚。

## SQL 执行超时

TiDB 还提供了系统变量（`max_execution_time`，默认值为 `0`，表示无限制）来限制单个 SQL 语句的执行时间。目前，该变量仅对只读 SQL 语句生效。`max_execution_time` 的单位为 `ms`，但实际精度为 `100ms`，而非毫秒级。

## JDBC 查询超时

<CustomContent platform="tidb">

从 v6.1.0 开始，当 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) 配置项设置为默认值 `true` 时，可以使用 MySQL JDBC 提供的 `setQueryTimeout()` 方法控制查询超时。

> **Note:**
>
> 当你的 TiDB 版本早于 v6.1.0 或 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) 设置为 `false` 时，`setQueryTimeout()` 不适用于 TiDB。这是因为客户端在检测到查询超时时会向数据库发送 `KILL` 命令，但由于 TiDB 服务采用负载均衡，TiDB 不会执行 `KILL` 命令以避免在错误的 TiDB 节点终止连接。在这种情况下，可以使用 `max_execution_time` 来控制查询超时。

</CustomContent>

<CustomContent platform="tidb-cloud">

从 v6.1.0 开始，当 [`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#enable-global-kill-new-in-v610) 配置项设置为默认值 `true` 时，可以使用 MySQL JDBC 提供的 `setQueryTimeout()` 方法控制查询超时。

> **Note:**
>
> 当你的 TiDB 版本早于 v6.1.0 或 [`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#enable-global-kill-new-in-v610) 设置为 `false` 时，`setQueryTimeout()` 不适用于 TiDB。这是因为客户端在检测到查询超时时会向数据库发送 `KILL` 命令，但由于 TiDB 服务采用负载均衡，TiDB 不会执行 `KILL` 命令以避免在错误的 TiDB 节点终止连接。在这种情况下，可以使用 `max_execution_time` 来控制查询超时。

</CustomContent>

TiDB 提供了以下与 MySQL 兼容的超时控制参数。

- **wait_timeout**，控制连接到 Java 应用程序的非交互式空闲超时。自 TiDB v5.4 起，`wait_timeout` 的默认值为 `28800` 秒，即 8 小时。对于早于 v5.4 的版本，默认值为 `0`，表示无限超时。
- **interactive_timeout**，控制连接到 Java 应用程序的交互式空闲超时。默认值为 `8 hours`。
- **max_execution_time**，控制连接中的 SQL 执行超时，仅对只读 SQL 语句有效。默认值为 `0`，表示允许连接无限繁忙，即 SQL 语句可以无限长时间执行。

但在实际生产环境中，空闲连接和无限执行的 SQL 语句会对数据库和应用造成负面影响。你可以通过在应用的连接字符串中配置这两个会话变量，避免空闲连接和无限执行。例如，设置如下：

- `sessionVariables=wait_timeout=3600`（1 小时）
- `sessionVariables=max_execution_time=300000`（5 分钟）

## 需要帮助吗？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>