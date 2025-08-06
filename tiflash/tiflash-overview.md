---
title: TiFlash 概述
summary: 了解 TiFlash 的架构和关键特性。
---

# TiFlash 概述

[TiFlash](https://github.com/pingcap/tiflash) 是使 TiDB 成为混合事务/分析处理（HTAP）数据库的关键组件。作为 TiKV 的列式存储扩展，TiFlash 同时提供了良好的隔离级别和强一致性保证。

在 TiFlash 中，列式副本是根据 Raft Learner 共识算法进行异步复制的。当读取这些副本时，通过校验 Raft 索引和多版本并发控制（MVCC），实现了快照隔离级别的一致性。

<CustomContent platform="tidb-cloud">

通过 TiDB Cloud，你可以根据 HTAP 工作负载轻松创建包含一个或多个 TiFlash 节点的 HTAP 集群。如果在创建集群时未指定 TiFlash 节点数量，或者你想要添加更多 TiFlash 节点，可以通过[扩容集群](/tidb-cloud/scale-tidb-cluster.md)来更改节点数量。

</CustomContent>

## 架构

![TiFlash Architecture](/media/tidb-storage-architecture-1.png)

上图展示了包含 TiFlash 节点的 HTAP 形态下的 TiDB 架构。

TiFlash 提供列式存储，并通过 ClickHouse 高效实现了一层协处理器。与 TiKV 类似，TiFlash 也拥有 Multi-Raft 系统，支持以 Region 为单位进行数据复制和分布（详见 [数据存储](https://www.pingcap.com/blog/tidb-internal-data-storage/)）。

TiFlash 能以低成本实时复制 TiKV 节点中的数据，不会阻塞 TiKV 的写入操作。同时，TiFlash 提供与 TiKV 相同的读取一致性，并确保读取到最新数据。TiFlash 中的 Region 副本在逻辑上与 TiKV 中的副本完全一致，并会与 TiKV 的 Leader 副本同时进行分裂和合并。

在 Linux AMD64 架构上部署 TiFlash 时，CPU 必须支持 AVX2 指令集。你可以通过 `grep avx2 /proc/cpuinfo` 是否有输出进行验证。对于 Linux ARM64 架构，CPU 必须支持 ARMv8 指令集架构。你可以通过 `grep 'crc32' /proc/cpuinfo | grep 'asimd'` 是否有输出进行验证。使用这些指令集扩展可以让 TiFlash 的向量化引擎获得更好的性能。

<CustomContent platform="tidb">

TiFlash 同时兼容 TiDB 和 TiSpark，这使你可以自由选择这两种计算引擎。

</CustomContent>

建议将 TiFlash 部署在与 TiKV 不同的节点上，以保证负载隔离。如果没有业务隔离需求，也可以将 TiFlash 和 TiKV 部署在同一节点。

目前，数据不能直接写入 TiFlash。你需要先将数据写入 TiKV，然后再复制到 TiFlash，因为 TiFlash 以 Learner 角色接入 TiDB 集群。TiFlash 支持以表为单位进行数据复制，但部署后默认不会复制任何数据。要复制指定表的数据，请参见 [为表创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-tables)。

TiFlash 主要由两部分组成：列式存储组件和 TiFlash proxy 组件。TiFlash proxy 组件负责 Multi-Raft 共识算法的通信。

当 TiFlash 收到为某张表创建副本的 DDL 命令后，TiDB 会自动在 PD 中创建相应的 [placement rules](https://docs.pingcap.com/tidb/stable/configure-placement-rules)，然后 PD 会根据这些规则进行相应的数据调度。

## 关键特性

TiFlash 具备以下关键特性：

- [异步复制](#asynchronous-replication)
- [一致性](#consistency)
- [智能选择](#intelligent-choice)
- [计算加速](#computing-acceleration)

### 异步复制

TiFlash 中的副本以 Raft Learner 这一特殊角色进行异步复制。这意味着当 TiFlash 节点宕机或出现高网络延迟时，TiKV 中的应用仍可正常运行。

这种复制机制继承了 TiKV 的两个优点：自动负载均衡和高可用性。

- TiFlash 不依赖额外的复制通道，而是直接以多对多的方式从 TiKV 接收数据。
- 只要 TiKV 中的数据未丢失，你可以随时恢复 TiFlash 中的副本。

### 一致性

TiFlash 提供与 TiKV 相同的快照隔离级别一致性，并确保读取到最新数据，这意味着你可以读取之前写入 TiKV 的数据。这种一致性通过校验数据复制进度来实现。

每当 TiFlash 收到读取请求时，Region 副本会向 Leader 副本发送进度校验请求（轻量级的 RPC 请求）。只有当当前复制进度包含了读取请求时间戳所覆盖的数据后，TiFlash 才会执行读取操作。

### 智能选择

TiDB 可以自动选择使用 TiFlash（列存）或 TiKV（行存），也可以在同一个查询中同时使用两者，以确保最佳性能。

这种选择机制类似于 TiDB 选择不同索引来执行查询。TiDB 优化器会根据读取成本的统计信息做出合适的选择。

### 计算加速

TiFlash 通过两种方式加速 TiDB 的计算：

- 列式存储引擎在执行读取操作时更高效。
- TiFlash 分担了 TiDB 的部分计算负载。

TiFlash 分担计算负载的方式与 TiKV Coprocessor 相同：TiDB 会将可以在存储层完成的计算下推。能否下推取决于 TiFlash 的支持情况。详情请参见 [支持的下推计算](/tiflash/tiflash-supported-pushdown-calculations.md)。

## 使用 TiFlash

TiFlash 部署完成后，数据复制不会自动开始。你需要手动指定需要复制的表。

<CustomContent platform="tidb">

你可以根据自身需求，使用 TiDB 读取 TiFlash 副本以进行中等规模的分析处理，或使用 TiSpark 读取 TiFlash 副本以进行大规模分析处理。详见以下章节：

</CustomContent>

<CustomContent platform="tidb-cloud">

你可以使用 TiDB 读取 TiFlash 副本以进行分析处理。详见以下章节：

</CustomContent>

- [创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)
- [使用 TiDB 读取 TiFlash 副本](/tiflash/use-tidb-to-read-tiflash.md)

<CustomContent platform="tidb">

- [使用 TiSpark 读取 TiFlash 副本](/tiflash/use-tispark-to-read-tiflash.md)

</CustomContent>

- [使用 MPP 模式](/tiflash/use-tiflash-mpp-mode.md)

<CustomContent platform="tidb">

如需体验从导入数据到在 TPC-H 数据集上查询的完整流程，请参见 [TiDB HTAP 快速上手](/quick-start-with-htap.md)。

</CustomContent>

## 参见

<CustomContent platform="tidb">

- 如需部署包含 TiFlash 节点的新集群，请参见 [使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。
- 如需在已部署集群中添加 TiFlash 节点，请参见 [扩容 TiFlash 集群](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)。
- [维护 TiFlash 集群](/tiflash/maintain-tiflash.md)。
- [TiFlash 性能调优](/tiflash/tune-tiflash-performance.md)。
- [TiFlash 配置](/tiflash/tiflash-configuration.md)。
- [监控 TiFlash 集群](/tiflash/monitor-tiflash.md)。
- 了解 [TiFlash 告警规则](/tiflash/tiflash-alert-rules.md)。
- [排查 TiFlash 集群问题](/tiflash/troubleshoot-tiflash.md)。
- [TiFlash 支持的下推计算](/tiflash/tiflash-supported-pushdown-calculations.md)
- [TiFlash 数据校验](/tiflash/tiflash-data-validation.md)
- [TiFlash 兼容性](/tiflash/tiflash-compatibility.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [TiFlash 性能调优](/tiflash/tune-tiflash-performance.md)。
- [TiFlash 支持的下推计算](/tiflash/tiflash-supported-pushdown-calculations.md)
- [TiFlash 兼容性](/tiflash/tiflash-compatibility.md)

</CustomContent>
