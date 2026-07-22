---
title: TiDB-X-CLOUD.202510.1 发布说明
summary: 了解 TiDB-X-CLOUD.202510.1 内核的功能。
---

# TiDB-X-CLOUD.202510.1 发布说明

**发布日期**：2026 年 4 月 28 日

**适用的 TiDB Cloud 计划**：{{{ .premium }}}

**TiDB X 内核版本**：`TiDB-X-CLOUD.202510.1`

{{{ .premium }}} 自 2026 年 4 月 28 日起开始公测，使用 `TiDB-X-CLOUD.202510.1` 内核。

在 `TiDB-X-CLOUD.202510.1` 中：

- `202510` 表示该内核版本的基线代码分支创建于 2025 年 10 月，这与发布日期不同。
- `1` 表示这是基于 `TiDB-X-CLOUD.202510` 基线分支构建的第一个补丁版本。

`TiDB-X-CLOUD.202510.1` 内核基于 [TiDB v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/) 内核，并包含了 TiDB v8.5.0 中引入的大部分功能和改进。

此外，与 [TiDB v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/) 内核相比，`TiDB-X-CLOUD.202510.1` 内核引入了以下功能：

## 全新的 TiDB X 架构 {#new-tidb-x-architecture}

* 引入 TiDB X 架构。这是一种云原生共享存储架构，将云原生对象存储作为 TiDB 的基础支撑。

    该架构可为 AI 时代的工作负载提供弹性扩展、可预测的性能以及优化的总体拥有成本（TCO）。

    TiDB X 标志着从 [classic TiDB](https://docs.pingcap.com/tidbcloud/tidb-architecture/?plan=premium) 的 shared-nothing 架构向云原生共享存储架构的根本性演进。通过从 shared-nothing 架构转向共享存储架构，TiDB X 解决了耦合节点的物理限制，从而实现以下技术目标：

    - **加速扩展**：通过消除物理数据迁移的需求，将扩展性能最高提升 10 倍。
    - **任务隔离**：确保后台维护任务（例如 compaction）与在线事务流量之间零干扰。
    - **资源弹性**：实现真正的“按需付费”模型，使计算资源能够独立于存储容量进行扩展。

    更多信息，请参见 [TiDB X Architecture](https://docs.pingcap.com/tidbcloud/tidb-x-architecture/?plan=premium)。

## 性能特性 {#performance-features}

* 支持对特定表的数据进行重新分布（实验特性）[#63260](https://github.com/pingcap/tidb/issues/63260) @[bufferflies](https://github.com/bufferflies)

    PD 会自动调度数据，使其尽可能均匀地分布在集群中的所有 TiKV 节点上。不过，这种自动调度关注的是整个集群。在某些情况下，即使集群范围内的数据分布是均衡的，某个特定表的数据在各个 TiKV 节点上的分布仍可能不均匀。

   现在，你可以使用 [`SHOW TABLE DISTRIBUTION`](https://docs.pingcap.com/tidbcloud/sql-statement-show-table-distribution/?plan=premium) 语句检查特定表的数据在所有 TiKV 节点上的分布情况。如果数据分布不均衡，你可以使用 [`DISTRIBUTE TABLE`](https://docs.pingcap.com/tidbcloud/sql-statement-distribute-table/?plan=premium) 语句对该表的数据进行重新分布（实验特性），以改善负载均衡。

    请注意，对特定表的数据重新分布是一次性任务，并且有超时限制。如果分布任务在超时前未完成，将自动退出。

    更多信息，请参见[文档](https://docs.pingcap.com/tidbcloud/sql-statement-distribute-table/?plan=premium)。

* 支持在 DDL 语句中嵌入 `ANALYZE` [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell) @[AilinKid](https://github.com/AilinKid)

    该功能适用于以下类型的 DDL 语句：

    - 创建新索引的 DDL 语句：[`ADD INDEX`](https://docs.pingcap.com/tidbcloud/sql-statement-add-index/?plan=premium)
    - 重组现有索引的 DDL 语句：[`MODIFY COLUMN`](https://docs.pingcap.com/tidbcloud/sql-statement-modify-column/?plan=premium) 和 [`CHANGE COLUMN`](https://docs.pingcap.com/tidbcloud/sql-statement-change-column/?plan=premium)

    启用该功能后，TiDB 会在新建或重组后的索引对用户可见之前，自动运行一次 `ANALYZE`（统计信息收集）操作。这样可以避免在索引创建或重组后，由于统计信息暂时不可用而导致优化器估算不准确以及潜在的执行计划变更。

     更多信息，请参见[文档](https://docs.pingcap.com/tidbcloud/ddl_embedded_analyze/?plan=premium)。

## 限制 {#limitations}

由于 TiDB X 与 classic TiDB 在架构上存在差异，TiDB X 内核不支持 classic TiDB 内核中的以下存储特性：

- [TiKV MVCC In-Memory Engine (IME)](https://docs.pingcap.com/tidb/v8.5/tikv-in-memory-engine)
- [Follower Read](https://docs.pingcap.com/tidb/v8.5/follower-read)

如需了解更多限制，请参见 [Limited SQL features on TiDB X Instances](https://docs.pingcap.com/tidbcloud/limited-sql-features-tidb-x/?plan=premium)。