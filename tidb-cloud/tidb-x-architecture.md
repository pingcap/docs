---
title: TiDB X 架构
summary: 了解云原生共享存储 TiDB X 架构如何实现弹性扩展性、可预测的性能以及优化的总拥有成本。
---

# TiDB X 架构

TiDB X 是一种全新的分布式 SQL 架构，使云原生对象存储成为 TiDB 的核心。目前在 TiDB Cloud <CustomContent plan="starter,essential,dedicated">Starter 和 Essential</CustomContent><CustomContent plan="premium">Starter、Essential 和 Premium</CustomContent> 版本中可用，该架构为 AI 时代的工作负载带来了弹性扩展性、可预测的性能和优化的总拥有成本（TCO）。

TiDB X 代表了从 [经典 TiDB](/tidb-architecture.md) 的共享无架构到云原生共享存储架构的根本性演进。通过将对象存储作为共享持久化存储层，TiDB X 引入了计算工作负载的分离，将在线事务工作负载与资源密集型的后台任务隔离开来。

本文档将介绍 TiDB X 架构，阐述 TiDB X 的设计动机，并描述与经典 TiDB 架构相比的关键创新点。

## 经典 TiDB 的限制

本节分析了经典 TiDB 的架构及其促使 TiDB X 诞生的限制。

### 经典 TiDB 的优势

经典 TiDB 的共享无架构解决了传统单体数据库的局限性。通过将计算与存储解耦，并采用 Raft 一致性算法，提供了分布式 SQL 工作负载所需的高可用性和扩展性。

经典 TiDB 架构具备以下基础能力：

- **横向扩展性**：支持读写性能的线性扩展。集群可扩展以处理每秒数百万的 QPS，并在数千万张表中管理超过 1 PiB 的数据。
- **HTAP (Hybrid Transactional and Analytical Processing)**：统一了事务和分析型工作负载。通过将重型聚合和 Join 操作下推到 TiFlash（列式存储引擎），可对最新事务数据进行可预测的实时分析，无需复杂的 ETL 流程。
- **无阻塞的 schema 变更**：采用全在线 DDL 实现。schema 变更不会阻塞读写，允许数据模型以最小的应用延时或可用性影响进行演进。
- **高可用性**：支持无缝的集群升级和扩容操作。确保关键服务在维护或资源调整期间始终可用。
- **多云支持**：作为开源解决方案，支持 <CustomContent language="en,zh">Amazon Web Services (AWS)、Google Cloud、Microsoft Azure 和阿里云</CustomContent><CustomContent language="ja">Amazon Web Services (AWS)、Google Cloud 和 Microsoft Azure</CustomContent>，实现云中立，避免厂商锁定。

### 经典 TiDB 的挑战

虽然经典 TiDB 的共享无架构具备高可用性，但存储与计算在本地节点上的紧耦合，在极大规模环境下带来了限制。随着数据量增长和云原生需求演进，出现了若干结构性挑战。

- **扩展性限制**

    - 数据迁移开销：在经典 TiDB 中，扩容（增加节点）或缩容（移除节点）操作需要在节点间物理迁移 SST 文件。对于大规模数据集，这一过程耗时且在数据迁移期间会因大量 CPU 和 I/O 消耗而影响在线流量性能。

    - 存储引擎瓶颈：经典 TiDB 底层的 RocksDB 存储引擎采用单一 LSM tree，并由全局互斥锁保护。这一设计导致扩展性上限，系统难以处理大数据集（例如单个 TiKV 节点超过 6 TiB 数据或 30 万个 SST 文件），无法充分利用硬件能力。

- **稳定性与性能干扰**

    - 资源争用：高写入流量会触发大量本地 compaction 任务以合并 SST 文件。在经典 TiDB 中，这些 compaction 任务与服务在线流量的 TiKV 节点共用资源，导致 CPU 和 I/O 争用，可能影响在线应用。

    - 缺乏物理隔离：逻辑 Region 与物理 SST 文件之间没有物理隔离。诸如 Region 迁移（负载均衡）等操作会带来 compaction 开销，直接与用户查询争用资源，导致潜在的性能抖动。

    - 写入限流：在高写入压力下，若后台 compaction 无法跟上前台写入流量，经典 TiDB 会触发流控机制以保护存储引擎，导致写入吞吐受限和应用延时突增。

- **资源利用率与成本**

    - 过度预留：为保证高峰流量和后台维护期间的稳定性与性能，用户通常需按“高水位”需求过度预留硬件资源。

    - 扩容不灵活：由于计算与存储耦合，用户可能仅为获得更多存储能力而被迫增加昂贵的计算型节点，即使 CPU 利用率很低。

### TiDB X 的设计动机

转向 TiDB X 的核心驱动力是将数据与物理计算资源解耦。通过从共享无架构转向共享存储架构，TiDB X 解决了节点耦合带来的物理限制，实现以下技术目标：

- **加速扩展**：通过消除物理数据迁移，将扩展性能提升至 10 倍。
- **任务隔离**：确保后台维护任务（如 compaction）与在线事务流量零干扰。
- **资源弹性**：实现真正的“按需付费”模式，计算资源可独立于存储容量弹性扩展。

关于该架构的更多背景，请参阅博客 [The Making of TiDB X: Origins, Architecture, and What’s to Come](https://www.pingcap.com/blog/tidbx-origins-architecture/)。

## TiDB X 架构概览

TiDB X 是经典 TiDB 分布式设计的云原生演进。它继承了经典 TiDB 的以下架构优势：

- **无状态的 SQL 层**：SQL 层（TiDB server）为无状态的，仅负责查询解析、优化和执行，不存储持久化数据。
- **网关与连接管理**：TiProxy（或负载均衡器）维护持久化客户端连接并无缝路由 SQL 流量。TiProxy 最初为支持在线升级而设计，如今已成为天然的网关组件。
- **基于 [Region](/tidb-cloud/tidb-cloud-glossary.md#region) 的动态分片**：TiKV 采用基于范围的分片单元 Region（默认 256 MiB）。数据被切分为数百万个 Region，系统自动管理 Region 的分布、迁移和负载均衡。

TiDB X 在此基础上，将本地共享无存储替换为 **云原生共享存储对象存储**。这一转变实现了“[计算与计算的分离](#separation-of-compute-and-compute)”模型，将资源密集型任务卸载到弹性池，确保即时扩展和可预测的性能。

TiDB X 架构如下所示：

![TiDB X Architecture](/media/tidb-x/tidb-x-architecture.png)

### 对象存储支持

TiDB X 使用对象存储（如 Amazon S3）作为所有数据的唯一真实来源。与经典架构将数据存储于本地磁盘不同，TiDB X 将所有数据的持久化副本存储在 **共享对象存储层**。上层的 **共享缓存层**（行引擎和列式引擎）作为高性能缓存，确保低延时。

由于权威数据已存储于对象存储，备份仅需依赖增量 Raft 日志和存储于 S3 的元信息，无论总数据量多大，备份操作都能在数秒内完成。在扩容操作中，新 TiKV 节点无需从现有节点复制大量数据，而是直接连接对象存储，按需加载所需数据，大幅加速扩容过程。

### 自动扩缩机制

TiDB X 架构为弹性扩展而设计，依赖负载均衡器和 **隔离 SQL 层** 的无状态特性。共享缓存层可根据 CPU 使用率或磁盘容量进行扩缩。系统可在数秒内自动增加或移除计算 pod，以适应实时工作负载需求。

这种技术弹性实现了基于消耗的按需付费定价模式。用户无需为高峰流量预留资源，系统会在流量高峰时自动扩容，在空闲时自动缩容，最大限度降低成本。

### 微服务与工作负载隔离

TiDB X 实现了精细的职责分离，确保多样化工作负载互不干扰。**隔离 SQL 层**由独立的计算节点组构成，支持工作负载隔离或多租户技术场景，不同应用可使用专属计算资源，同时共享同一底层数据。

**共享服务层**将重型数据库操作拆解为独立微服务，包括 compaction、统计信息收集和 DDL 执行。通过将索引创建或大规模数据导入等资源密集型后台操作卸载到该层，TiDB X 确保这些操作不会与服务在线用户流量的计算节点争用 CPU 或内存资源。该设计为关键应用提供了更可预测的性能，并允许网关、SQL 计算、缓存和后台服务等各组件根据自身资源需求独立扩展。

## TiDB X 的关键创新

下图对比了经典 TiDB 与 TiDB X 架构，突出展示了从 **共享无** 到 **共享存储** 的转变，以及计算工作负载分离的引入。

![Classic TiDB vs TiDB X architecture](/media/tidb-x/tidb-classic-vs-tidb-x-1.png)

- **引擎演进**：在经典 TiDB 中，Raft 引擎负责多 raft 日志管理，RocksDB 负责本地磁盘上的物理数据存储。在 TiDB X 中，这些组件被 **全新 RF 引擎**（Raft 引擎）和 **重构的 KV 引擎** 替代。KV 引擎是替代 RocksDB 的 LSM tree 存储引擎，二者均针对高性能和与对象存储的无缝集成进行了专门优化。

- **计算工作负载分离**：图中的虚线表示对对象存储层的后台读写操作。在 TiDB X 中，RF/KV 引擎与对象存储的交互与前台进程解耦，确保后台操作不会影响在线流量延时。

### 计算与计算的分离

虽然经典 TiDB 已实现计算（SQL 层）与存储（TiKV）的分离，TiDB X 在 SQL 层和存储层内部进一步引入了分离。该设计将用于在线事务工作负载的 **轻量级计算** 与资源密集型后台任务的 **重型计算** 区分开来。

- **轻量级计算**：为 OLTP 工作负载（如用户查询）专属分配资源。

    对于轻量级 OLTP 工作负载，由于重型计算任务被卸载到弹性计算池，服务用户流量的 TiKV 服务器仅专注于在线查询。因此，TiDB X 能以更少资源实现更稳定、可预测的性能，确保后台任务不会干扰在线事务处理。

- **重型计算**：为后台任务（如 compaction、备份、统计信息收集、数据加载和慢查询处理）单独分配弹性计算池。

    对于 DDL 操作和大规模数据导入等重型计算任务，TiDB X 可自动按需分配弹性计算资源，以全速运行这些工作负载，且对在线流量影响极小。例如，在添加索引时，TiDB worker、Coprocessor worker 和 TiKV worker 会根据数据量动态分配。这些弹性计算资源与处理在线流量的 TiDB 和 TiKV 服务器物理隔离，确保资源密集型操作不再与关键 OLTP 查询争用资源。在实际场景中，索引创建速度可比经典 TiDB 快 5 倍，且不会影响在线服务。

### 从共享无到共享存储的转变

TiDB X 从经典的 **共享无** 架构（数据需在 TiKV 节点间物理复制）转向 **共享存储** 架构。在 TiDB X 中，对象存储（如 Amazon S3）而非本地磁盘成为所有持久化数据的唯一真实来源。这消除了扩容时大规模数据复制的需求，实现了快速弹性。

转向对象存储不会降低前台读写性能。

- 读操作：轻量级请求由本地缓存和磁盘直接响应，只有重型读负载才会下推到远程弹性 Coprocessor worker。
- 写操作：与对象存储的交互为异步。Raft 日志首先持久化到本地磁盘，Raft WAL（预写日志）分片随后在后台上传到对象存储。
- Compaction：当 MemTable 数据写满并刷盘到本地磁盘后，Region leader 会将 SST 文件上传到对象存储。远程 compaction 在弹性 compaction worker 上完成后，TiKV 节点会收到通知，从对象存储加载已 compact 的 SST 文件。

### 弹性 TCO（按需付费）

在经典 TiDB 中，集群通常需为同时应对高峰流量和后台任务而过度预留资源。TiDB X 支持 **自动扩缩**，用户仅为实际消耗的资源付费（按需付费）。重型任务的后台资源按需分配，用完即释放，杜绝资源浪费。

TiDB X 采用 [Request Capacity Unit](/tidb-cloud/tidb-cloud-glossary.md#request-capacity-unit-rcu)（RCU）衡量分配的计算能力。1 个 RCU 提供固定量的计算资源，可处理一定数量的 SQL 请求。你分配的 RCU 数量决定了集群的基线性能和吞吐能力。你可以设置上限以控制成本，同时享受弹性扩展带来的收益。

### 从 LSM tree 到 LSM forest

在经典 TiDB 中，每个 TiKV 节点运行一个 RocksDB 实例，将所有 Region 的数据存储在一个大型 LSM tree 中。由于数千个 Region 的数据混杂在一起，Region 迁移、扩容或缩容等操作会触发大范围 compaction，消耗大量 CPU 和 I/O 资源，可能影响在线流量。单一 LSM tree 由全局互斥锁保护，随着数据量增长（如单节点超过 6 TiB 或 30 万个 SST 文件），全局互斥锁竞争加剧，影响读写性能。

TiDB X 通过从单一 LSM tree 演进为 **LSM forest**，重构了存储引擎。在保留逻辑 Region 抽象的同时，TiDB X 为每个 Region 分配独立的 LSM tree。这种物理隔离消除了扩容、Region 迁移和数据加载等操作中的跨 Region compaction 开销。单个 Region 的操作仅影响自身的 tree，不存在全局互斥锁竞争。

![Classic TiDB vs TiDB X](/media/tidb-x/tidb-classic-vs-tidb-x-2.png)

### 极速弹性扩展

借助共享对象存储和每个 Region 独立 LSM tree 的设计，TiDB X 在扩容或缩容 TiKV 节点时无需物理数据迁移或大规模 compaction。扩展操作比经典 TiDB **快 5～10 倍**，同时保持在线工作负载的稳定延时。

## 架构对比总结

下表总结了经典 TiDB 到 TiDB X 的架构演进，并说明 TiDB X 如何提升扩展性、性能隔离和成本效率。

| Feature | Classic TiDB | TiDB X | Primary benefit (TiDB X) |
| --- | --- | --- | --- |
| 架构 | Shared-nothing（数据存储于本地磁盘） | Shared-storage（对象存储为权威持久化存储） | 对象存储实现云原生弹性 |
| 稳定性 | 前台与后台任务共用资源 | 计算与计算分离（重型任务采用弹性计算池） | 写入密集或维护期间保护 OLTP 工作负载 |
| 性能 | OLTP 与后台任务争用 CPU 和 I/O | 重型任务专属弹性池 | OLTP 延时更低，重型任务更快完成 |
| 扩展机制 | 物理数据迁移（TiKV 节点间 SST 文件复制） | TiKV 节点仅通过对象存储读写 SST 文件 | 扩容/缩容速度提升 5～10 倍 |
| 存储引擎 | 每 TiKV 节点单一 LSM tree（RocksDB） | LSM forest（每 Region 独立 LSM tree） | 消除全局互斥锁竞争，降低 compaction 干扰 |
| DDL 执行 | DDL 与用户流量争用本地 CPU 和 I/O | DDL 卸载至弹性计算资源 | schema 变更更快，延时更可预测 |
| 成本模型 | 需为高峰工作负载过度预留资源 | 弹性 TCO（按需付费） | 仅为实际资源消耗付费 |
| 备份 | 依赖数据量的物理备份 | 基于元信息与对象存储集成 | 备份操作显著加速 |