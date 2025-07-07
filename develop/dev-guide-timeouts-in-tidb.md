---
title: TiDB中的超时
summary: 了解TiDB中的超时机制，以及排查错误的解决方案。
---

# TiDB中的超时

本文档描述了TiDB中的各种超时设置，帮助你排查相关错误。

## GC超时

TiDB的事务实现采用MVCC（多版本并发控制）机制。当新写入的数据覆盖旧数据时，旧数据不会被立即替换，而是与新数据一同保留。不同版本通过时间戳进行区分。TiDB通过定期的垃圾回收（GC）机制，清理不再需要的旧数据。

- 对于TiDB版本早于v4.0：

    默认情况下，每个MVCC版本（一致性快照）会被保留10分钟。读取时间超过10分钟的事务会收到错误 `GC life time is shorter than transaction duration`。

- 对于TiDB v4.0及之后版本：

    对于持续时间不超过24小时的运行中的事务，垃圾回收（GC）在事务执行期间会被阻止。不会出现 `GC life time is shorter than transaction duration` 错误。

如果在某些情况下需要临时延长读取时间，可以增加MVCC版本的保留时间：

- 对于TiDB版本早于v5.0：在TiDB的`mysql.tidb`表中调整`tikv_gc_life_time`。
- 对于TiDB v5.0及之后版本：调整系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)。

注意，系统变量配置会立即生效且全局生效。增加其值会延长所有快照的存活时间，减少则会立即缩短所有快照的存活时间。过多的MVCC版本会影响TiDB集群的性能，因此需要及时将其调整回之前的设置。

<CustomContent platform="tidb">

> **Tip:**
>
> 具体来说，当Dumpling从TiDB导出数据（少于1TB）时，如果TiDB版本为v4.0.0或更高，且Dumpling可以访问PD地址以及TiDB集群的 [`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md) 表，Dumpling会自动调整GC安全点以阻止GC，不影响原有集群。
>
> 但在以下任一场景中，Dumpling无法自动调整GC时间：
>
> - 数据量非常大（超过1TB）。
> - Dumpling无法直接连接到PD，例如TiDB集群在TiDB Cloud或在与Dumpling分离的Kubernetes上。
>
> 在此类场景中，必须提前手动延长GC时间，以避免在导出过程中因GC导致导出失败。
>
> 详细信息请参见 [Manually set the TiDB GC time](/dumpling-overview.md#manually-set-the-tidb-gc-time)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Tip:**
>
> 具体来说，当Dumpling从TiDB导出数据（少于1TB）时，如果TiDB版本大于或等于v4.0.0，且Dumpling可以访问TiDB集群的PD地址，Dumpling会自动延长GC时间，不影响原有集群。
>
> 但在以下任一场景中，Dumpling无法自动调整GC时间：
>
> - 数据量非常大（超过1TB）。
> - Dumpling无法直接连接到PD，例如TiDB集群在TiDB Cloud或在与Dumpling分离的Kubernetes上。
>
> 在此类场景中，必须提前手动延长GC时间，以避免在导出过程中因GC导致导出失败。
>
> 详细信息请参见 [Manually set the TiDB GC time](https://docs.pingcap.com/tidb/stable/dumpling-overview#manually-set-the-tidb-gc-time)。

</CustomContent>

有关GC的更多信息，请参见 [GC Overview](/garbage-collection-overview.md)。

## 事务超时

在事务启动后未提交或回滚的场景中，可能需要更细粒度的控制和更短的超时时间，以防止长时间持有锁。在这种情况下，可以使用 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)（在TiDB v7.6.0中引入）来控制用户会话中事务的空闲超时。

GC不会影响正在进行的事务，但对悲观事务的最大并发数、事务超时限制以及事务使用的内存都有上限。你可以通过TiDB配置文件中 `[performance]` 类别下的 `max-txn-ttl` 来修改事务超时时间，默认值为 `60` 分钟。

像 `INSERT INTO t10 SELECT * FROM t1` 这样的SQL语句不受GC影响，但超出 `max-txn-ttl` 后会因超时而回滚。

## SQL执行超时

TiDB还提供了一个系统变量（`max_execution_time`，默认值为 `0`，表示无限制）用以限制单个SQL语句的执行时间。目前，该变量仅对只读SQL语句生效。`max_execution_time`的单位为毫秒，但实际精度为100毫秒级，而非毫秒级。

## JDBC查询超时

<CustomContent platform="tidb">

从v6.1.0开始，当 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) 配置项设置为默认值 `true` 时，可以使用MySQL JDBC提供的 `setQueryTimeout()` 方法控制查询超时。

> **Note:**
>
> 当你的TiDB版本早于v6.1.0或 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) 设置为 `false` 时，`setQueryTimeout()` 不适用于TiDB。这是因为客户端在检测到查询超时时会向数据库发送 `KILL` 命令，但由于TiDB服务采用负载均衡，TiDB不会执行 `KILL` 命令以避免在错误的TiDB节点终止连接。在这种情况下，可以使用 `max_execution_time` 来控制查询超时。

</CustomContent>

<CustomContent platform="tidb-cloud">

从v6.1.0开始，当 [`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#enable-global-kill-new-in-v610) 配置项设置为默认值 `true` 时，可以使用MySQL JDBC提供的 `setQueryTimeout()` 方法控制查询超时。

> **Note:**
>
> 当你的TiDB版本早于v6.1.0或 [`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#enable-global-kill-new-in-v610) 设置为 `false` 时，`setQueryTimeout()` 不适用于TiDB。这是因为客户端在检测到查询超时时会向数据库发送 `KILL` 命令，但由于TiDB服务采用负载均衡，TiDB不会执行 `KILL` 命令以避免在错误的TiDB节点终止连接。在这种情况下，可以使用 `max_execution_time` 来控制查询超时。

</CustomContent>

TiDB提供了以下MySQL兼容的超时控制参数。

- **wait_timeout**，控制连接到Java应用的非交互式空闲超时。自TiDB v5.4起，`wait_timeout`的默认值为 `28800` 秒，即8小时。对于早于v5.4的版本，默认值为 `0`，表示无限超时。
- **interactive_timeout**，控制连接到Java应用的交互式空闲超时。默认值为 `8 hours`。
- **max_execution_time**，控制连接中的SQL执行超时，仅对只读SQL语句有效。默认值为 `0`，表示无限制，即SQL语句可以无限长时间执行。

但在实际生产环境中，空闲连接和无限期执行的SQL语句会对数据库和应用产生负面影响。你可以通过在应用的连接字符串中配置这两个会话变量，避免空闲连接和无限期执行的SQL。例如，设置：

- `sessionVariables=wait_timeout=3600`（1小时）
- `sessionVariables=max_execution_time=300000`（5分钟）

## 需要帮助吗？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>