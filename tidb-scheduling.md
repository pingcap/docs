---
title: TiDB 调度
summary: 介绍 TiDB 集群中的 PD 调度组件。
---

# TiDB 调度

Placement Driver ([PD](https://github.com/tikv/pd)) 在 TiDB 集群中充当管理者角色，同时负责调度集群中的 Regions。本文介绍 PD 调度组件的设计和核心概念。

## 调度场景

TiKV 是 TiDB 使用的分布式键值存储引擎。在 TiKV 中，数据被组织为 Regions，这些 Regions 会在多个存储节点上进行复制。在所有副本中，Leader 负责读写操作，Follower 负责复制 Leader 的 Raft 日志。

现在考虑以下场景：

* 为了高效利用存储空间，同一 Region 的多个副本需要根据 Region 大小合理分布在不同节点上；
* 对于多数据中心拓扑结构，一次数据中心故障只会导致所有 Regions 的一个副本失效；
* 当新增 TiKV 存储节点时，可以对数据进行重新平衡；
* 当 TiKV 存储节点发生故障时，PD 需要考虑：
    * 失效存储的恢复时间。
        * 如果时间短（例如，服务重启），是否需要调度。
        * 如果时间长（例如，磁盘故障导致数据丢失），应如何调度。
    * 所有 Regions 的副本。
        * 如果某些 Regions 的副本数不足，PD 需要补充。
        * 如果副本数超过预期（例如，故障存储恢复后重新加入集群），PD 需要删除多余的副本。
* 读写操作在 Leader 上进行，不能只在少数几个存储节点上分布；
* 不是所有的 Regions 都是热点，因此需要平衡所有 TiKV 存储节点的负载；
* 在 Regions 进行平衡时，数据传输会消耗大量网络/磁盘流量和 CPU 时间，可能影响线上服务。

这些场景可能同时发生，增加了解决的难度。同时，整个系统在动态变化，因此需要调度器收集关于集群的所有信息，然后进行调整。因此，引入 PD 到 TiDB 集群中。

## 调度需求

上述场景可以归类为两类：

1. 一个分布式且高可用的存储系统必须满足以下要求：

    * 适当的副本数量。
    * 副本需要根据不同的拓扑结构分布在不同的机器上。
    * 集群能够自动从 TiKV 节点故障中进行灾难恢复。

2. 一个良好的分布式系统需要具备以下优化：

    * 所有 Region Leader 在存储节点上均匀分布；
    * 所有 TiKV 节点的存储容量平衡；
    * 热点负载平衡；
    * 负载均衡的速度需要有限制，以确保线上服务的稳定；
    * 维护人员可以手动将 Peer 上线/下线。

在满足第一类需求后，系统将具备容错能力；而满足第二类需求后，资源利用会更高效，系统的扩展性也会更好。

为了实现这些目标，PD 需要首先收集信息，例如 Peer 状态、Raft 组信息以及访问 Peer 的统计数据。然后需要为 PD 制定一些策略，使其能根据这些信息和策略制定调度计划。最后，PD 会向 TiKV Peer 分发操作指令，完成调度计划。

## 基本调度操作

所有调度计划包含三种基本操作：

* 添加新副本
* 删除副本
* 在 Raft 组中的副本之间转移 Region Leader

它们由 Raft 命令 `AddReplica`、`RemoveReplica` 和 `TransferLeader` 实现。

## 信息收集

调度依赖于信息的收集。简而言之，PD 调度组件需要了解所有 TiKV Peer 和所有 Regions 的状态。TiKV Peer 会向 PD 上报以下信息：

- 每个 TiKV Peer 上报的状态信息：

    每个 TiKV Peer 定期向 PD 发送心跳。PD 不仅检查存储是否存活，还会在心跳消息中收集 [`StoreState`](https://github.com/pingcap/kvproto/blob/release-8.5/proto/pdpb.proto#L473)。`StoreState` 包含：

    * 总磁盘空间
    * 可用磁盘空间
    * Regions 数量
    * 读写速度
    * 发送/接收快照的数量（快照可能在副本之间复制）
    * 是否超载
    * 标签（详见 [Perception of Topology](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels)）

    你可以使用 PD 控制命令检查 TiKV 存储的状态，状态可能为 Up、Disconnect、Offline、Down 或 Tombstone。以下是所有状态的描述及其关系。

    + **Up**：TiKV 存储正常服务中。
    + **Disconnect**：PD 与 TiKV 存储之间的心跳超过 20 秒未收到。如果超过 `max-store-down-time` 指定的时间，状态由 "Disconnect" 变为 "Down"。
    + **Down**：PD 与 TiKV 存储之间的心跳超过 `max-store-down-time`（默认 30 分钟）。在此状态下，TiKV 存储会开始补充存活存储上的各个 Region 的副本。
    + **Offline**：通过 PD 控制手动将 TiKV 存储下线。此状态仅为中间状态，存储在此状态下会将所有 Region 转移到符合迁移条件的其他 "Up" 存储。当 `leader_count` 和 `region_count`（通过 PD 控制获取）都显示为 `0` 时，存储状态变为 "Tombstone"。在 "Offline" 状态下，不要禁用存储服务或存储所在的物理服务器。在存储下线的过程中，如果集群没有目标存储进行 Region 迁移（例如，存储不足以容纳副本），存储会一直处于 "Offline" 状态。
    + **Tombstone**：TiKV 存储完全离线。可以使用 `remove-tombstone` 接口安全清理处于此状态的 TiKV。从 v6.5.0 开始，如果不手动处理，PD 会在节点变为 Tombstone 一个月后自动删除内部存储的 Tombstone 记录。

    ![TiKV store status relationship](/media/tikv-store-status-relationship.png)

- Region Leader 上报的信息：

    每个 Region Leader 定期向 PD 发送心跳，报告 [`RegionState`](https://github.com/pingcap/kvproto/blob/release-8.5/proto/pdpb.proto#L312)，包括：

    * Leader 自身位置
    * 其他副本位置
    * 离线副本数量
    * 读写速度

PD 通过这两类心跳收集集群信息，然后据此做出决策。

此外，PD 还可以通过扩展接口获取更多信息，以做出更精准的决策。例如，如果存储的心跳中断，PD 无法判断 Peer 是暂时下线还是永久下线。它会等待一段时间（默认 30 分钟），如果仍未收到心跳，则视为存储离线，然后将该存储上的所有 Region 在其他存储上进行平衡。

但有时存储是由维护人员手动设置为离线状态，维护人员可以通过 PD 控制接口告知 PD。这样，PD 可以立即进行所有 Region 的平衡。

## 调度策略

收集完信息后，PD 需要一些策略来制定调度计划。

**Strategy 1: Region 的副本数需要正确**

PD 可以通过 Region Leader 的心跳知道某个 Region 的副本数是否正确。如果不正确，PD 可以通过添加/删除副本来调整。副本数不正确的原因可能包括：

* 存储故障，导致某些 Region 的副本数少于预期；
* 故障后存储恢复，导致某些 Region 的副本数多于预期；
* [`max-replicas`](https://github.com/pingcap/pd/blob/v4.0.0-beta/conf/config.toml#L95) 被修改。

**Strategy 2: Region 的副本需要在不同位置**

注意这里的“位置”不同于“机器”。一般 PD 只能确保 Region 的副本不在同一 Peer 上，以避免 Peer 故障导致多个副本丢失。然而在生产环境中，可能有以下需求：

* 多个 TiKV Peer 在同一台机器上；
* TiKV Peer 分布在多个机架上，即使某个机架故障，系统仍应可用；
* TiKV Peer 分布在多个数据中心，即使某个数据中心故障，系统仍应可用；

这些需求的关键在于 Peer 可以具有相同的“位置”，这是容错的最小单元。Region 的副本不能全部在同一单元内。因此，可以为 TiKV Peer 配置 [labels](https://github.com/tikv/tikv/blob/v4.0.0-beta/etc/config-template.toml#L140)，并在 PD 上设置 [location-labels](https://github.com/pingcap/pd/blob/v4.0.0-beta/conf/config.toml#L100)，以指定哪些标签用于标记位置。

**Strategy 3: 副本需要在存储节点之间平衡**

Region 副本的大小是固定的，因此保持副本在存储节点之间的平衡有助于数据大小的均衡。

**Strategy 4: Leader 需要在存储节点之间平衡**

读写操作在 Leader 上进行，按照 Raft 协议，PD 需要将 Leader 分布到整个集群中，而不是只在少数几个 Peer 上。

**Strategy 5: 热点需要在存储节点之间平衡**

PD 可以通过存储节点和 Region 的心跳检测热点，从而实现热点的分布。

**Strategy 6: 存储容量需要在存储节点之间平衡**

启动时，TiKV 存储会报告 `capacity`，表示存储空间的限制。PD 在调度时会考虑这一点。

**Strategy 7: 调整调度速度以稳定线上服务**

调度会消耗 CPU、内存、网络和 I/O 流量。资源利用过度会影响线上服务，因此 PD 需要限制同时进行的调度任务数。默认此策略较为保守，但如果需要更快的调度速度，可以进行调整。

## 调度实现

PD 通过存储节点和 Region 的心跳收集集群信息，然后根据这些信息和策略制定调度计划。调度计划是一系列基本操作的组合。每次 PD 收到 Region Leader 的 Region 心跳时，会检查该 Region 是否已有待执行的操作。如果需要调度新的操作，PD 会将操作放入心跳响应中，并通过后续的 Region 心跳监控操作的执行情况。

注意，这里的“操作”仅是对 Region Leader 的建议，Region 可以选择跳过。Region 的 Leader 会根据当前状态决定是否跳过调度操作。