---
title: TiDB 中的超时机制
summary: 了解 TiDB 中的超时机制，以及排查错误的解决方案。
---

# TiDB 中的超时机制

本文档介绍了 TiDB 中的各种超时机制，帮助你排查相关错误。

## GC 超时

TiDB 的事务实现采用了 MVCC（多版本并发控制）机制。当新写入的数据覆盖旧数据时，旧数据不会被替换，而是与新写入的数据一同保留。不同版本通过时间戳进行区分。TiDB 通过定期的垃圾回收（GC）机制清理不再需要的旧数据。

- 对于 TiDB v4.0 之前的版本：

    默认情况下，每个 MVCC 版本（即一致性快照）会保留 10 分钟。读取时间超过 10 分钟的事务会收到 `GC life time is shorter than transaction duration` 错误。

- 对于 TiDB v4.0 及之后的版本：

    对于运行时间不超过 24 小时的事务，事务执行期间会阻止垃圾回收（GC）。不会出现 `GC life time is shorter than transaction duration` 错误。

如果在某些场景下你需要临时更长的读取时间，可以增加 MVCC 版本的保留时间：

- 对于 TiDB v5.0 之前的版本：在 TiDB 的 `mysql.tidb` 表中调整 `tikv_gc_life_time`。
- 对于 TiDB v5.0 及之后的版本：调整系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)。

注意，系统变量的配置是全局且即时生效的。增加该值会延长所有现有快照的生命周期，减少该值会立即缩短所有快照的生命周期。过多的 MVCC 版本会影响 TiDB 集群的性能，因此你需要及时将该变量恢复为之前的设置。

<CustomContent platform="tidb">

> **Tip:**
>
> 特别地，当 Dumpling 从 TiDB 导出数据（小于 1 TB）时，如果 TiDB 版本为 v4.0.0 或更高，并且 Dumpling 能访问 TiDB 集群的 PD 地址和 [`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md) 表，Dumpling 会自动调整 GC safe point，阻止 GC，不影响原有集群。
>
> 但在以下任一场景下，Dumpling 无法自动调整 GC 时间：
>
> - 数据量非常大（超过 1 TB）。
> - Dumpling 无法直接连接 PD，例如 TiDB 集群部署在 TiDB Cloud 或与 Dumpling 隔离的 Kubernetes 上。
>
> 在这些场景下，你必须提前手动延长 GC 时间，以避免导出过程中因 GC 导致导出失败。
>
> 详情参见 [手动设置 TiDB GC 时间](/dumpling-overview.md#manually-set-the-tidb-gc-time)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Tip:**
>
> 特别地，当 Dumpling 从 TiDB 导出数据（小于 1 TB）时，如果 TiDB 版本大于等于 v4.0.0，并且 Dumpling 能访问 TiDB 集群的 PD 地址，Dumpling 会自动延长 GC 时间，不影响原有集群。
>
> 但在以下任一场景下，Dumpling 无法自动调整 GC 时间：
>
> - 数据量非常大（超过 1 TB）。
> - Dumpling 无法直接连接 PD，例如 TiDB 集群部署在 TiDB Cloud 或与 Dumpling 隔离的 Kubernetes 上。
>
> 在这些场景下，你必须提前手动延长 GC 时间，以避免导出过程中因 GC 导致导出失败。
>
> 详情参见 [手动设置 TiDB GC 时间](https://docs.pingcap.com/tidb/stable/dumpling-overview#manually-set-the-tidb-gc-time)。

</CustomContent>

关于 GC 的更多信息，参见 [GC 概述](/garbage-collection-overview.md)。

## 事务超时

在某些场景下，事务已开启但既未提交也未回滚，你可能需要更细粒度的控制和更短的超时时间，以防止长时间持有锁。此时，你可以使用 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)（TiDB v7.6.0 引入）来控制用户会话中事务的空闲超时时间。

GC 不会影响正在进行的事务。但悲观事务的并发数量仍有上限，事务超时和事务使用的内存都有上限。你可以通过 TiDB 配置文件 `[performance]` 分类下的 `max-txn-ttl` 参数修改事务超时时间，默认值为 60 分钟。

如 `INSERT INTO t10 SELECT * FROM t1` 这类 SQL 语句不会受到 GC 的影响，但如果执行时间超过 `max-txn-ttl`，会因超时被回滚。

## SQL 执行超时

TiDB 还提供了一个系统变量（`max_execution_time`，默认值为 `0`，表示不限制）用于限制单条 SQL 语句的执行时间。目前该系统变量仅对 `SELECT` 语句（包括 `SELECT ... FOR UPDATE`）生效。`max_execution_time` 的单位为 `ms`，但实际精度为 100ms 级别，而非毫秒级。

## JDBC 查询超时

<CustomContent platform="tidb">

自 v6.1.0 起，当 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) 配置项为默认值 `true` 时，你可以使用 MySQL JDBC 提供的 `setQueryTimeout()` 方法控制查询超时。

> **Note:**
>
> 如果你的 TiDB 版本低于 v6.1.0，或 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) 设置为 `false`，`setQueryTimeout()` 对 TiDB 无效。这是因为客户端在检测到查询超时时会向数据库发送 `KILL` 命令。但由于 TiDB 服务是负载均衡的，TiDB 不会执行 `KILL` 命令，以避免错误节点上的连接被终止。在这种情况下，你可以使用 `max_execution_time` 控制查询超时。

</CustomContent>

<CustomContent platform="tidb-cloud">

自 v6.1.0 起，当 [`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#enable-global-kill-new-in-v610) 配置项为默认值 `true` 时，你可以使用 MySQL JDBC 提供的 `setQueryTimeout()` 方法控制查询超时。

> **Note:**
>
> 如果你的 TiDB 版本低于 v6.1.0，或 [`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#enable-global-kill-new-in-v610) 设置为 `false`，`setQueryTimeout()` 对 TiDB 无效。这是因为客户端在检测到查询超时时会向数据库发送 `KILL` 命令。但由于 TiDB 服务是负载均衡的，TiDB 不会执行 `KILL` 命令，以避免错误节点上的连接被终止。在这种情况下，你可以使用 `max_execution_time` 控制查询超时。

</CustomContent>

TiDB 提供了以下与 MySQL 兼容的超时控制参数。

- **wait_timeout**，控制与 Java 应用的非交互式空闲连接超时时间。自 TiDB v5.4 起，`wait_timeout` 默认值为 28800 秒，即 8 小时。对于 v5.4 之前的版本，默认值为 0，表示无限制超时。
- **interactive_timeout**，控制与 Java 应用的交互式空闲连接超时时间。默认值为 8 小时。
- **max_execution_time**，控制连接中 SQL 执行的超时时间，仅对 `SELECT` 语句（包括 `SELECT ... FOR UPDATE`）生效。默认值为 0，表示连接可以无限忙碌，即 SQL 语句可以无限执行。

但在实际生产环境中，空闲连接和无限执行的 SQL 语句会对数据库和应用产生负面影响。你可以在应用的连接字符串中配置这两个会话级变量，避免空闲连接和无限执行的 SQL 语句。例如，设置如下：

- `sessionVariables=wait_timeout=3600`（1 小时）
- `sessionVariables=max_execution_time=300000`（5 分钟）

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>