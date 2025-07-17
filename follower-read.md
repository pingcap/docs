---
title: Follower Read
summary: 本文档描述了 Follower Read 的使用和实现机制。
---

# Follower Read

当某个 Region 出现读热点时，Region 的 leader 可能成为整个系统的读瓶颈。在这种情况下，启用 Follower Read 功能可以显著减轻 leader 的负载，并通过在多个 follower 之间平衡负载，提升整个系统的吞吐量。本文介绍了 Follower Read 的使用方法及其实现机制。

## 概述

Follower Read 功能指在强一致性读取的前提下，使用任何一个 Region 的 follower 副本来处理读请求。该功能提升了 TiDB 集群的吞吐量，减轻了 leader 的负载。它包含一系列负载均衡机制，将 TiKV 的读负载从 leader 副本转移到 Region 的 follower 副本。TiKV 的 Follower Read 实现为用户提供了强一致性读取能力。

> **Note:**
>
> 为了实现强一致性读取，当前 follower 节点需要向 leader 节点请求当前的执行进度（即 `ReadIndex`），这会带来额外的网络请求开销。因此，Follower Read 的主要优势在于将读取请求与写入请求隔离开，并提升整体的读取吞吐量。

## 使用方法

要启用 TiDB 的 Follower Read 功能，可以修改 `tidb_replica_read` 变量的值，如下所示：

```sql
set [session | global] tidb_replica_read = '<target value>';
```

作用域：SESSION | GLOBAL

默认值：leader

该变量用于设置预期的数据读取模式。

- 当 `tidb_replica_read` 的值设置为 `leader` 或空字符串时，TiDB 保持默认行为，将所有读取操作都发送到 leader 副本进行。
- 当 `tidb_replica_read` 的值设置为 `follower` 时，TiDB 会选择某个 Region 的 follower 副本来执行所有读取操作。
- 当 `tidb_replica_read` 的值设置为 `leader-and-follower` 时，TiDB 可以从任何副本中选择进行读取。在此模式下，读取请求在 leader 和 follower 之间进行负载均衡。
- 当 `tidb_replica_read` 的值设置为 `prefer-leader` 时，TiDB 优先选择 leader 副本进行读取。如果 leader 副本在处理读取请求时明显较慢（例如由于磁盘或网络性能波动），TiDB 会选择其他可用的 follower 副本进行读取。
- 当 `tidb_replica_read` 的值设置为 `closest-replicas` 时，TiDB 优先选择同一可用区内的副本进行读取，可以是 leader 或 follower。如果没有同一可用区内的副本，TiDB 会从 leader 副本读取。
- 当 `tidb_replica_read` 的值设置为 `closest-adaptive` 时：

    - 如果读取请求的估算结果大于或等于 [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)，TiDB 更倾向于选择同一可用区内的副本进行读取。为了避免在不同可用区之间造成读流量分布不均，TiDB 会动态检测所有在线的 TiDB 和 TiKV 节点的可用区分布。在每个可用区内，`closest-adaptive` 配置生效的 TiDB 节点数量受到限制，数量与该可用区中 TiDB 节点最少的数量相同，其他 TiDB 节点会自动从 leader 副本读取。例如，如果 TiDB 节点分布在 3 个可用区（A、B 和 C），其中 A 和 B 各有 3 个 TiDB 节点，C 只有 2 个，A 和 B 中 `closest-adaptive` 配置生效的 TiDB 节点数量为 2，A 和 B 中的其他 TiDB 节点会自动选择 leader 副本进行读取。
    - 如果读取请求的估算结果小于 [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)，TiDB 只能选择 leader 副本进行读取。

- 当 `tidb_replica_read` 的值设置为 `learner` 时，TiDB 从 learner 副本读取数据。如果该 Region 没有 learner 副本，TiDB 会返回错误。

<CustomContent platform="tidb">

> **Note:**
>
> 当 `tidb_replica_read` 的值设置为 `closest-replicas` 或 `closest-adaptive` 时，你需要配置集群，确保副本按照指定的配置在可用区之间分布。有关配置 `location-labels` 以调度副本的详细信息，请参考 [Schedule replicas by topology labels](/schedule-replicas-by-topology-labels.md)。TiDB 依赖 `zone` 标签匹配同一可用区内的 TiKV 节点，因此你需要确保 `zone` 标签包含在 PD 的 `location-labels` 配置中，以及在每个 TiDB 和 TiKV 节点的配置中包含 `zone`。如果你的集群使用 TiDB Operator 部署，参考 [High availability of data](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/configure-a-tidb-cluster#high-availability-of-data)。

</CustomContent>

## 实现机制

在引入 Follower Read 功能之前，TiDB 采用强 leader 原则，将所有读写请求提交给 Region 的 leader 节点处理。虽然 TiKV 可以在多个物理节点上均匀分布 Regions，但对于每个 Region，只有 leader 能提供对外服务。其他 follower 只能不断接收由 leader 复制的数据，并为在发生故障切换时的投票选举做准备，不能处理外部的读请求。

为了在不违反线性一致性或影响 Snapshot Isolation 的前提下，实现 follower 节点的数据读取，follower 需要使用 Raft 协议的 `ReadIndex` 来确保读请求可以读取到已在 leader 上提交的最新数据。在 TiDB 层面，Follower Read 只需根据负载均衡策略，将 Region 的读请求发送到 follower 副本。

### 强一致性读取

当 follower 节点处理读请求时，首先会使用 Raft 协议的 `ReadIndex` 与 Region 的 leader 交互，获取当前 Raft 组的最新提交索引。leader 的最新提交索引应用到 follower 后，才开始处理读请求。

### follower 副本选择策略

由于 Follower Read 功能不影响 TiDB 的 Snapshot Isolation 事务隔离级别，TiDB 采用轮询策略选择 follower 副本。目前，对于协处理器请求，负载均衡策略的粒度为连接级别。对于连接到特定 Region 的 TiDB 客户端，所选的 follower 是固定的，只有在失败或调度策略调整时才会切换。

然而，对于非协处理器请求（如点查询），负载均衡策略的粒度为事务级别。对于在特定 Region 上的 TiDB 事务，所选的 follower 也是固定的，只有在失败或调度策略调整时才会切换。如果一个事务同时包含点查询和协处理器请求，这两类请求会根据前述调度策略分别进行读取调度。在这种情况下，即使协处理器请求和点查询针对同一 Region，TiDB 也会将它们作为独立事件进行处理。
