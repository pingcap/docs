---
title: TiFlash 概述
summary: 了解 TiFlash 的架构和关键特性。
---

# TiFlash 概述

[TiFlash](https://github.com/pingcap/tiflash) 是使 TiDB 本质上成为混合事务/分析处理（HTAP）数据库的关键组件。作为 TiKV 的列存储扩展，TiFlash 提供了良好的隔离级别和强一致性保证。

在 TiFlash 中，列副本是根据 Raft Learner 共识算法异步复制的。当读取这些副本时，通过验证 Raft 索引和多版本并发控制（MVCC）实现快照隔离级别的一致性。

<CustomContent platform="tidb-cloud">

使用 TiDB Cloud，你可以根据你的 HTAP 工作负载，轻松创建一个 HTAP 集群，指定一个或多个 TiFlash 节点。如果在创建集群时未指定 TiFlash 节点数，或者你想添加更多的 TiFlash 节点，可以通过 [扩展集群](/tidb-cloud/scale-tidb-cluster.md) 来调整节点数。

</CustomContent>

## 架构

![TiFlash 架构](/media/tidb-storage-architecture-1.png)

上图是 TiDB 在其 HTAP 形式下的架构，包括 TiFlash 节点。

TiFlash 提供列存储，底层由 ClickHouse 高效实现的协处理器层支持。与 TiKV 类似，TiFlash 也拥有 Multi-Raft 系统，支持以 Region 为单位进行数据复制和分布（详见 [Data Storage](https://www.pingcap.com/blog/tidb-internal-data-storage/)）。

TiFlash 以低成本进行 TiKV 节点中的数据实时复制，不阻塞 TiKV 的写入。同时，提供与 TiKV 相同的读取一致性，确保读取到最新的数据。TiFlash 中的 Region 副本在逻辑上与 TiKV 中的相同，并会随着 TiKV 中的 Leader 副本一起拆分和合并。

在 Linux AMD64 架构下部署 TiFlash 时，CPU 必须支持 AVX2 指令集。确保执行 `grep avx2 /proc/cpuinfo` 有输出。在 Linux ARM64 架构下部署 TiFlash 时，CPU 必须支持 ARMv8 指令集架构。确保执行 `grep 'crc32' /proc/cpuinfo | grep 'asimd'` 有输出。通过使用指令集扩展，TiFlash 的向量化引擎可以提供更好的性能。

<CustomContent platform="tidb">

TiFlash 兼容 TiDB 和 TiSpark，允许你在这两种计算引擎之间自由选择。

</CustomContent>

建议将 TiFlash 部署在不同于 TiKV 的节点上，以确保工作负载隔离。如果不需要业务隔离，也可以将 TiFlash 和 TiKV 部署在同一节点。

目前，数据不能直接写入 TiFlash。你需要在 TiKV 中写入数据，然后复制到 TiFlash，因为 TiFlash 以 Learner 角色连接到 TiDB 集群。TiFlash 支持以表为单位进行数据复制，但部署后默认不复制任何数据。若要复制特定表的数据，请参见 [Create TiFlash replicas for tables](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-tables)。

TiFlash 由两个主要组件组成：列存储组件和 TiFlash 代理组件。TiFlash 代理组件负责使用 Multi-Raft 共识算法进行通信。

在收到创建表副本的 DDL 命令后，TiDB 会自动在 PD 中创建相应的 [placement rules](https://docs.pingcap.com/tidb/stable/configure-placement-rules)，然后 PD 根据这些规则进行数据调度。

## 关键特性

TiFlash 具有以下关键特性：

- [Asynchronous replication](#asynchronous-replication)
- [Consistency](#consistency)
- [Intelligent choice](#intelligent-choice)
- [Computing acceleration](#computing-acceleration)

### Asynchronous replication

TiFlash 中的副本以特殊角色 Raft Learner 异步复制。这意味着当 TiFlash 节点宕机或出现高网络延迟时，TiKV 中的应用仍能正常进行。

这种复制机制继承了 TiKV 的两个优势：自动负载均衡和高可用性。

- TiFlash 不依赖额外的复制通道，而是以多对多的方式直接从 TiKV 接收数据。
- 只要 TiKV 中的数据未丢失，你可以随时在 TiFlash 中恢复副本。

### Consistency

TiFlash 提供与 TiKV 相同的快照隔离级别的一致性，确保读取到最新数据，也就是说可以读取之前在 TiKV 中写入的数据。这一一致性通过验证数据复制进度实现。

每次 TiFlash 接收到读取请求时，Region 副本会向 Leader 副本发送一个进度验证请求（轻量级 RPC 请求）。TiFlash 只有在当前复制进度包含了读取请求时间戳所覆盖的数据后，才会执行读取操作。

### Intelligent choice

TiDB 可以自动选择使用 TiFlash（列存）或 TiKV（行存），或在一次查询中同时使用两者，以确保最佳性能。

这一选择机制类似于 TiDB 选择不同索引执行查询的方式。TiDB 优化器会根据读取成本的统计信息做出合理选择。

### Computing acceleration

TiFlash 通过两种方式加速 TiDB 的计算：

- 列存储引擎在执行读取操作时更高效。
- TiFlash 分担了部分 TiDB 的计算工作负载。

TiFlash 以与 TiKV 协处理器类似的方式共享计算工作负载：TiDB 将存储层可以完成的计算下推。是否支持下推取决于 TiFlash 的支持情况。详见 [Supported pushdown calculations](/tiflash/tiflash-supported-pushdown-calculations.md)。

## 使用 TiFlash

部署完成后，数据复制不会自动开始。你需要手动指定要复制的表。

<CustomContent platform="tidb">

你可以使用 TiDB 读取 TiFlash 副本进行中等规模的分析处理，或使用 TiSpark 读取 TiFlash 副本进行大规模分析处理，具体取决于你的需求。详见：

</CustomContent>

<CustomContent platform="tidb-cloud">

你可以使用 TiDB 读取 TiFlash 副本进行分析处理。详见：

</CustomContent>

- [Create TiFlash Replicas](/tiflash/create-tiflash-replicas.md)
- [Use TiDB to Read TiFlash Replicas](/tiflash/use-tidb-to-read-tiflash.md)

<CustomContent platform="tidb">

- [Use TiSpark to Read TiFlash Replicas](/tiflash/use-tispark-to-read-tiflash.md)

</CustomContent>

- [Use MPP Mode](/tiflash/use-tiflash-mpp-mode.md)

<CustomContent platform="tidb">

想要体验从导入数据到查询的完整流程（如 TPC-H 数据集），请参考 [Quick Start with TiDB HTAP](/quick-start-with-htap.md)。

</CustomContent>

## 相关链接

<CustomContent platform="tidb">

- 若要部署带有 TiFlash 节点的新集群，参见 [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md)。
- 若要在已部署的集群中添加 TiFlash 节点，参见 [Scale out a TiFlash cluster](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)。
- [Maintain a TiFlash cluster](/tiflash/maintain-tiflash.md)。
- [Tune TiFlash performance](/tiflash/tune-tiflash-performance.md)。
- [Configure TiFlash](/tiflash/tiflash-configuration.md)。
- [Monitor the TiFlash cluster](/tiflash/monitor-tiflash.md)。
- 了解 [TiFlash alert rules](/tiflash/tiflash-alert-rules.md)。
- [Troubleshoot a TiFlash cluster](/tiflash/troubleshoot-tiflash.md)。
- [Supported push-down calculations in TiFlash](/tiflash/tiflash-supported-pushdown-calculations.md)
- [Data validation in TiFlash](/tiflash/tiflash-data-validation.md)
- [TiFlash compatibility](/tiflash/tiflash-compatibility.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [Tune TiFlash performance](/tiflash/tune-tiflash-performance.md)。
- [Supported push-down calculations in TiFlash](/tiflash/tiflash-supported-pushdown-calculations.md)
- [TiFlash compatibility](/tiflash/tiflash-compatibility.md)

</CustomContent>