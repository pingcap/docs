---
title: 分层存储概览
summary: 了解 TiDB Cloud Premium 和 BYOC 中的分层存储，包括其概念、架构、使用场景和实现原理。
---

# 分层存储概览

分层存储可帮助你将不常访问的表或分区数据迁移到成本更低的存储层，同时保持 SQL 语义不变。本页介绍 IA（Infrequent Access）存储的架构、权衡因素和场景建议，帮助你判断何时适合使用 IA 存储。

> **注意：**
>
> 分层存储目前在 {{{ .premium }}} 和 {{{ .byoc }}} 中处于**私有预览**阶段，默认禁用。如需使用，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 为你的实例启用。本文描述的行为反映的是当前预览版的实现，正式发布（GA）前可能会发生变化。

## 简介 {#introduction}

分层存储是 {{{ .premium }}} 和 {{{ .byoc }}} 提供的**表级和分区级存储分层能力**。它专为不常访问的数据设计。你可以将表或分区指定为 Infrequent Access（IA）存储类。系统会将完整数据集存储在远程对象存储中（例如 Amazon S3 或 Alibaba Cloud OSS），同时仅在本地存储中保留元信息以及按需缓存的热点数据段。

从应用程序的角度来看，IA 表的行为与标准表相同。所有查询、事务、备份和恢复语义都保持不变。主要区别在于成本与性能之间的权衡：本地存储使用量会显著降低，但冷读（即所需数据在本地缓存中不可用时）的延时会更高，因为数据必须先从远程对象存储中获取。

主要特性：

- **透明语义**：所有 SQL 操作（包括 `SELECT`、`INSERT`、`UPDATE` 和 `DELETE`）的行为都与标准表相同。
- **更低的存储成本**：数据存储在低成本对象存储中，只有热点数据会缓存在本地。在典型场景下，存储成本可降低约 50%。实际降幅取决于你选择的 IA 缓存级别。详情请参见 [TiDB Cloud 计费](/tidb-cloud/tidb-cloud-billing.md)。
- **细粒度控制**：同时支持表级和分区级存储分层。分区级设置优先于表级设置。
- **灵活转换**：支持 IA 与标准存储类之间的双向转换，且不会丢失数据。
- **无缝集成**：与 Raft Region、MVCC、BR backup and restore、TiCDC 以及其他 TiDB 组件完全集成。
- **可观测且可调优**：转换进度、IA 读统计信息以及集群级缓存命中率可在 SQL 输出和 Cloud Console 中查看，并且 IA 缓存级别可配置。

## 使用场景 {#usage-scenarios}

本节介绍适合和不适合使用 IA 存储的场景，以及帮助你判断是否应使用 IA 的检查清单。

### 推荐场景 {#recommended-scenarios}

| 业务场景 | 数据特征 | 推荐冷热边界 |
|-|-|-|
| 电商历史订单 / 金融交易 | 写入频繁，近期数据读写密集，历史修改较少 | 6 个月 |
| 财务凭证 / 审计日志 / 发票 | 一次写入，很少修改，保留 7-15 年 | 2 年 |
| 应用日志 / 监控指标 / API 调用 | 高吞吐写入，近期故障排查频繁 | 90 天 |
| 社交媒体帖子 / 评论 / 照片元信息 | 初期访问峰值高，随后逐渐下降 | 30-90 天 |
| 工业传感器 / 网联汽车 | 写入吞吐极高，近期监控要求实时性 | 1 年 |
| 数据仓库历史分析 | 批量写入，修改较少，面向历史趋势分析 | 90 天 |
| AI 对话历史 / memory | 基于会话写入，近期高频访问，用于历史用户画像 | 180 天 |
| LLM 训练数据集 | 训练期间访问频繁，训练完成后访问量快速下降 | 训练结束 + 30 天 |
| AI 推理日志 / 结果 | 高并发写入，近期用于监控，历史数据用于优化 | 90 天 |
| 向量数据库 | 很少修改，近期查询频繁 | 30-90 天 |

**通用经验法则**：数据量大 + 访问频率随时间下降 + 偶尔查询且对响应时间没有严格要求 → 适合使用 IA。

### 不推荐场景 {#not-recommended-scenarios}

- 对延时极其敏感的**热点 OLTP 表**（核心在线事务表，对每毫秒都敏感）
- 需要**频繁进行大范围扫描**的数据集（持续访问大量冷数据的 AP 查询）
- 需要在 IA 和 Standard 之间**频繁切换**的表
- 访问模式**高度离散**且几乎没有局部性的数据
- 访问模式不符合“**随时间递减**”趋势的场景

### 决策检查清单 {#decision-checklist}

在设置 IA 之前，请验证以下各项：

- [ ] 已从业务角度确认该表/分区的数据访问频率会逐渐下降
- [ ] 该表可以改为分区表，因为使用分区表更容易管理冷热数据分离
- [ ] 对于普通表的冷热分离，热点数据占整表比例低于 10%
- [ ] 冷数据访问频率很低；例如，查询 QPS 不超过 10，以避免对象存储带宽饱和
- [ ] 不需要对 IA 表频繁执行大范围 AP 扫描
- [ ] 可以接受冷读延时：一次 SQL 执行可能会发起多个远程请求，且延时会随缓存状态、请求并发度以及访问的冷数据量而变化
- [ ] 已了解冷读存在读放大：单条 100 字节记录最多可能出现 30,000× 放大（约 3 MiB 冷数据）
- [ ] 单次查询涉及的冷数据不超过 100 MiB
- [ ] 单次查询访问的冷数据行数不超过 100 行
- [ ] 已规划观察期（首个分区至少覆盖一个完整业务日）
- [ ] 已了解从 IA 切回 Standard 需要较长时间，并且带宽成本较高

## 实现原理 {#implementation-principles}

本节介绍分层存储的架构、数据存储层级、读放大分析以及 LSM-Tree 写入路径。

### 架构概览 {#architecture-overview}

分层存储的实现跨越 TiDB → TiKV → Object Store 三层架构：

```
┌──────────────────────────────────────────────────────────────────┐
│ TiDB Schema Layer                                                │
│ · STORAGE_CLASS / ENGINE_ATTRIBUTE written to TiDB schema        │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ TiKV Region Management Layer                                     │
│ · IA tables/partitions occupy dedicated regions, avoiding        │
│   hot/cold data in the same shard                                │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ TiKV IA Cache Management Layer (IaManager)                       │
│ · Local cache for cold storage data                              │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Remote Object Storage (S3/OSS)                                   │
│ · Full SST data stored as whole objects, not by segment          │
└──────────────────────────────────────────────────────────────────┘
```

**Raft ChangeSet 保证一致性**：存储类变更会通过 Raft ChangeSet 复制到所有副本。这可确保每个相关分片在重启、恢复、切分和合并过程中都保持一致的存储类状态，从而避免因 Region 拓扑结构变化导致的数据丢失或损坏。

### 本地缓存和缓存级别 {#local-cache-and-cache-level}

IaManager layer 会在每个 TiKV 节点上为 IA 数据维护本地缓存。可缓存的数据量由 IA 缓存级别决定，并受限于为缓存预留的本地磁盘容量上限。

缓存级别是集群范围的设置，共有四个选项：**Economy**、**Default**、**Balanced** 和 **Deep**。级别越高，缓存的 IA 数据比例越大，缓存命中率和成本也越高。缓存淘汰由系统管理：你不能指定哪些数据保留在缓存中，也不能为单个表或分区设置不同的级别。关于如何修改缓存级别，请参见[配置和管理分层存储](/tidb-cloud/tiered-storage-guide.md)。

### 数据存储层级 {#data-storage-hierarchy}

一个 SSTable 自上而下的内部层级如下：

```
SSTable ──→ Segment ──→ Block ──→ KV Pair
(file)      (1 MiB)     (32 KiB)    (single record)
```

| 层级 | 默认大小 | 作用 |
|-|-|-|
| **Segment** | 1 MiB | TiKV 从对象存储读取并写入本地缓存的**最小单位**；可避免过多小请求带来的 API 调用成本和 QPS 限流 |
| **Block** | 32 KiB | 本地文件读取、压缩以及**内存/磁盘缓存**的基本单位 |

这意味着，缓存未命中时并不会只获取单条 KV 记录，而是会将整个 Segment 加载到本地存储中。如果后续查询命中同一 Segment 中的数据，就能享受到热点读的性能收益。但对于一次性查询且后续不再访问的情况，读放大的代价会相对较高。

Segment 仅用于组织本地缓存。在对象存储中，SST 文件会作为一个完整对象存储，而不会被切分为多个 Segment，因此修改 Segment 大小不会重写对象存储中的任何数据。在 {{{ .byoc }}} 中，Segment 大小可配置。详情请参见[配置和管理分层存储](/tidb-cloud/tiered-storage-guide.md)。

### 读放大分析 {#read-amplification-analysis}

**缓存未命中时的读放大路径**：

```
User queries 1 record (100 Bytes)
→ Block cache miss
→ TiKV loads segments from 3 LSM levels from object storage
→ Approximately 3 MiB data fetched from object storage to local
→ Read amplification: ~30,000×
```

每次缓存未命中所获取的数据量会随着 Segment 大小而变化。以上数据基于默认 Segment 大小 1 MiB。

这种放大在以下两种场景中的表现不同：

- **后续可复用**：加载的 Segment 会保留在 IA 缓存中；后续命中将变为热点读，从而摊薄初始放大成本
- **一次性查询**：例如执行大范围扫描的临时分析查询——加载的数据不会被再次复用，导致读成本非常高。此外，新加载的数据会将本地缓存中的“旧数据”淘汰出去，而这些旧数据可能是真正的热点数据，它们被淘汰后会触发新的缓存未命中，形成级联性能影响

因此，分层存储最适合**小范围、集中式的查询模式**，而不适合频繁的大范围扫描。

### LSM-Tree 写入路径 {#lsm-tree-write-path}

写入路径与 Standard 表保持一致：

```
INSERT/UPDATE/DELETE
→ Memtable (hot write, unaffected by IA)
→ L0 SST (hot write, unaffected by IA)
→ L1+ SST (after compaction, opened in IA mode based on storage class)
```

- 写入仍然会先进入 memtable/L0 —— 本地热点写路径不会直接变成远程写入
- 满足 IA 条件的 L1+ 文件会在 reload/compaction 后以 IA 模式打开
- `memtable` 和 `L0` 等热点写路径不会直接进入 IA
- IA 的主要目标是 Write CF L1+ 层

这也解释了为什么存储成本下降是近似值而不是精确值。IA 存储空间仅覆盖表的 L1 及更深层级。memtable 和 L0 文件仍保留在本地磁盘上，不计入 IA 存储，因此表的总空间是其 memtable、L0 和 L1+ 数据之和。表中究竟有多少数据实际迁移到了 IA 存储，取决于写入速率和 compaction 进度。

## 转换效率 {#conversion-efficiency}

无论是使用 `STORAGE_CLASS` 形式还是 `ENGINE_ATTRIBUTE` 形式，修改存储类的 `ALTER TABLE` 语句都能在几秒内完成，因为它只会修改 schema 元信息。随后，Region 级别的数据迁移会在 TiKV 中异步执行，因此总耗时取决于数据量和转换方向。

### Standard → IA {#standard-ia}

测试参考：约 1 TB 逻辑数据（含索引）可在 5 分钟内完成转换，过程中对 QPS 和延时的影响可忽略不计。单个 TiKV CPU 增加约 0.5c，并在约 5 分钟内恢复。

```
TiDB schema takes effect → Schema Manager sync (30s) → TiKV broadcast
→ Region alignment / Split → ChangeSet updates Shard → Reload files
```

### IA → Standard {#ia-standard}

测试参考：2.09 TB 逻辑数据（含索引）大约耗时 3 小时 10 分钟（每个 TiKV 约 ~1.61k regions/hour），对象存储 GET 吞吐约为 1.6 GiB/s。转换期间，Standard 分区 QPS 下降约 3.78%，P99 增加约 18.63%，单个 TiKV CPU 增加约 0.5c。

```
Same chain as above + full object storage data download to local
```

> **注意：**
>
> 这些数据来自测试环境，并不代表真实生产场景。你应根据自身业务测试获得准确数据。

如需使用 `SHOW STORAGE_CLASS TRANSITIONS` 跟踪正在进行的转换，或在 `mysql.tidb_storage_class_transition_history` 中查询历史转换耗时，请参见[分层存储可观测性](/tidb-cloud/tiered-storage-observability.md)。