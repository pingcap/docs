---
title: Follower Read
summary: 本文档介绍了 Follower Read 的使用方法和实现机制。
---

# Follower Read

当某个 Region 出现读热点时，该 Region 的 leader 可能会成为整个系统的读瓶颈。在这种情况下，启用 Follower Read 功能可以显著降低 leader 的负载，并通过在多个 follower 之间平衡负载，提高整个系统的吞吐量。本文档将介绍 Follower Read 的使用方法和实现机制。

## 概述

Follower Read 功能指的是在保证强一致性读的前提下，允许使用 Region 的任意 follower 副本来处理读请求。该功能提升了 TiDB 集群的吞吐量，并降低了 leader 的负载。它包含一系列负载均衡机制，将 TiKV 的读负载从 leader 副本分担到 Region 的 follower 副本。TiKV 的 Follower Read 实现为用户提供了强一致性读。

> **Note:**
>
> 为了实现强一致性读，follower 节点目前需要向 leader 节点请求当前的执行进度（即 `ReadIndex`），这会带来一次额外的网络请求开销。因此，Follower Read 的主要收益在于将集群中的读请求与写请求隔离，并提升整体读吞吐量。

## 使用方法

要启用 TiDB 的 Follower Read 功能，可以按如下方式修改 `tidb_replica_read` 变量的值：

```sql
set [session | global] tidb_replica_read = '<target value>';
```

作用域：SESSION | GLOBAL

默认值：leader

该变量用于设置期望的数据读取模式。

- 当你将 `tidb_replica_read` 的值设置为 `leader` 或空字符串时，TiDB 保持默认行为，所有读操作都发送到 leader 副本执行。
- 当你将 `tidb_replica_read` 的值设置为 `follower` 时，TiDB 会选择 Region 的某个 follower 副本来执行读操作。如果该 Region 存在 learner 副本，TiDB 也会以同等优先级考虑使用它们进行读操作。如果当前 Region 没有可用的 follower 或 learner 副本，TiDB 会从 leader 副本读取数据。
- 当 `tidb_replica_read` 的值设置为 `leader-and-follower` 时，TiDB 可以选择任意副本执行读操作。在该模式下，读请求会在 leader 和 follower 之间进行负载均衡。
- 当 `tidb_replica_read` 的值设置为 `prefer-leader` 时，TiDB 优先选择 leader 副本执行读操作。如果 leader 副本在处理读操作时明显变慢（如磁盘或网络性能抖动导致），TiDB 会选择其他可用的 follower 副本执行读操作。
- 当 `tidb_replica_read` 的值设置为 `closest-replicas` 时，TiDB 优先选择同一可用区内的副本执行读操作，该副本可以是 leader 也可以是 follower。如果同一可用区内没有副本，TiDB 会从 leader 副本读取数据。
- 当 `tidb_replica_read` 的值设置为 `closest-adaptive` 时：

    - 如果某次读请求的预估结果大于或等于 [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630) 的值，TiDB 优先选择同一可用区内的副本进行读操作。为避免读流量在各可用区分布不均，TiDB 会动态检测所有在线 TiDB 和 TiKV 节点的可用区分布。在每个可用区内，`closest-adaptive` 配置生效的 TiDB 节点数量始终等于 TiDB 节点最少的可用区中的节点数，其他 TiDB 节点会自动从 leader 副本读取。例如，TiDB 节点分布在 3 个可用区（A、B、C），其中 A 和 B 各有 3 个 TiDB 节点，C 只有 2 个 TiDB 节点，则每个可用区 `closest-adaptive` 配置生效的 TiDB 节点数为 2，A 和 B 区域中多余的 TiDB 节点会自动选择 leader 副本进行读操作。
    - 如果某次读请求的预估结果小于 [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630) 的值，TiDB 只能选择 leader 副本进行读操作。

- 当你将 `tidb_replica_read` 的值设置为 `learner` 时，TiDB 会从 learner 副本读取数据。如果当前 Region 没有可用的 learner 副本，TiDB 会从可用的 leader 或 follower 副本读取数据。

<CustomContent platform="tidb">

> **Note:**
>
> 当你将 `tidb_replica_read` 设置为 `closest-replicas` 或 `closest-adaptive` 时，为确保副本按照指定配置分布在各可用区，需要为 PD 配置 `location-labels`，并根据 [Schedule replicas by topology labels](/schedule-replicas-by-topology-labels.md) 为 TiDB 和 TiKV 设置正确的 `labels`。TiDB 依赖 `zone` label 匹配同一可用区的 TiKV 节点，因此需要确保 PD 的 `location-labels` 中包含 `zone`，且每个 TiDB 和 TiKV 节点的配置中都包含 `zone`。如果你的集群是通过 TiDB Operator 部署的，请参考 [High availability of data](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-availability-of-data)。
>
> 对于 TiDB v7.5.0 及更早版本：
>
> - 如果你将 `tidb_replica_read` 设置为 `follower`，且没有可用的 follower 或 learner 副本，TiDB 会返回错误。
> - 如果你将 `tidb_replica_read` 设置为 `learner`，且没有可用的 learner 副本，TiDB 会返回错误。

</CustomContent>

## 实现机制

在引入 Follower Read 功能之前，TiDB 遵循强 leader 原则，所有读写请求都提交给 Region 的 leader 节点处理。虽然 TiKV 可以将 Region 均匀分布在多个物理节点上，但对于每个 Region，只有 leader 能对外提供服务，其他 follower 只能持续接收 leader 的数据复制，并在发生故障时准备参与 leader 选举。

为了在不违反线性一致性或影响 TiDB 的快照隔离（Snapshot Isolation）的前提下，允许在 follower 节点读取数据，follower 节点需要使用 Raft 协议的 `ReadIndex`，以确保读请求能够读取到 leader 已提交的最新数据。在 TiDB 层面，Follower Read 功能只需根据负载均衡策略，将 Region 的读请求发送到 follower 副本即可。

### 强一致性读

当 follower 节点处理读请求时，会首先通过 Raft 协议的 `ReadIndex` 与 Region 的 leader 交互，获取当前 Raft group 的最新提交索引。在该提交索引被 follower 本地应用后，才开始处理读请求。

### Follower 副本选择策略

由于 Follower Read 功能不会影响 TiDB 的快照隔离级别，TiDB 采用轮询（round-robin）策略选择 follower 副本。目前，对于 coprocessor 请求，Follower Read 负载均衡策略的粒度为连接级别。对于连接到某个 Region 的 TiDB 客户端，所选的 follower 是固定的，只有在失败或调度策略调整时才会切换。

而对于非 coprocessor 请求（如点查），Follower Read 负载均衡策略的粒度为事务级别。对于某个 Region 上的 TiDB 事务，所选的 follower 是固定的，只有在失败或调度策略调整时才会切换。如果一个事务同时包含点查和 coprocessor 请求，这两类请求会按照上述调度策略分别进行读调度。在这种情况下，即使 coprocessor 请求和点查针对同一个 Region，TiDB 也会将它们作为独立事件处理。