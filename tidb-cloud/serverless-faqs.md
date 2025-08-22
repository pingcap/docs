---
title: TiDB Cloud Serverless 常见问题
summary: 了解与 TiDB Cloud Serverless 相关的最常见问题（FAQ）。
aliases: ['/tidbcloud/serverless-tier-faqs']
---

# TiDB Cloud Serverless 常见问题

<!-- markdownlint-disable MD026 -->

本文档列出了关于 TiDB Cloud Serverless 的最常见问题。

## 通用常见问题

### 什么是 TiDB Cloud Serverless？

TiDB Cloud Serverless 为你和你的组织提供具备完整 HTAP 能力的 TiDB 数据库。它是 TiDB 的全托管、自动弹性伸缩的部署方式，让你可以立即开始使用数据库，开发和运行应用程序时无需关心底层节点，并且能够根据应用负载变化自动扩缩容。

### 如何开始使用 TiDB Cloud Serverless？

请参考 5 分钟上手的 [TiDB Cloud 快速入门](/tidb-cloud/tidb-cloud-quickstart.md)。

### 在 TiDB Cloud 中，我最多可以创建多少个 TiDB Cloud Serverless 集群？

对于 TiDB Cloud 中的每个组织，默认最多可以创建五个 [免费集群](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)。如需创建更多 TiDB Cloud Serverless 集群，你需要添加信用卡并创建 [可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan) 以供使用。

### TiDB Cloud 的所有功能在 TiDB Cloud Serverless 上都完全支持吗？

部分 TiDB Cloud 功能在 TiDB Cloud Serverless 上仅部分支持或暂不支持。详细信息请参见 [TiDB Cloud Serverless 限制与配额](/tidb-cloud/serverless-limitations.md)。

### TiDB Cloud Serverless 何时会支持除 AWS 以外的云平台，如 Google Cloud 或 Azure？

我们正在积极推进 TiDB Cloud Serverless 向包括 Google Cloud 和 Azure 在内的其他云平台扩展。但目前尚无具体时间表，因为我们当前专注于弥补功能差距并确保所有环境下的无缝体验。请放心，我们会持续努力让 TiDB Cloud Serverless 支持更多云平台，并在进展过程中及时向社区更新。

### 在 TiDB Cloud Serverless 推出前，我创建了 Developer Tier 集群。还能继续使用我的集群吗？

可以，你的 Developer Tier 集群已自动迁移为 TiDB Cloud Serverless 集群，无需中断即可获得更好的用户体验。

### 什么是 TiDB Cloud Serverless 的列式存储？

TiDB Cloud Serverless 的列式存储作为行存储的额外副本，确保强一致性。与传统的行存储（按行存储数据）不同，列式存储按列组织数据，优化了数据分析任务。

列式存储是实现 TiDB HTAP（混合事务与分析处理）能力的关键特性，通过无缝融合事务型和分析型负载。

为高效管理列式存储数据，TiDB Cloud Serverless 使用独立的弹性 TiFlash 引擎。在查询执行时，优化器会引导集群自动决定是从行存储还是列存储读取数据。

### 在哪些场景下应使用 TiDB Cloud Serverless 的列式存储？

在以下场景下建议使用 TiDB Cloud Serverless 的列式存储：

- 你的负载包含需要高效数据扫描和聚合的分析型任务。
- 你优先考虑分析型负载的性能提升。
- 你希望将分析处理与事务处理隔离，避免对 TP（事务处理）负载产生性能影响。独立的列式存储有助于优化不同负载模式。

在这些场景下，列式存储可以显著提升查询性能，并为系统中的混合负载提供无缝体验。

### 如何在 TiDB Cloud Serverless 中使用列式存储？

在 TiDB Cloud Serverless 中使用列式存储的方式与 TiFlash 类似。你可以在表级或数据库级启用列式存储：

- 表级：为某个表分配 TiFlash 副本，即可为该表启用列式存储。
- 数据库级：为数据库中的所有表配置 TiFlash 副本，实现整个数据库的列式存储。

为表设置 TiFlash 副本后，TiDB 会自动将该表的数据从行存储同步到列式存储，确保数据一致性并优化分析型查询的性能。

关于如何设置 TiFlash 副本，详见 [创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)。

## 计费与计量常见问题

### 什么是 Request Units？

TiDB Cloud Serverless 采用按需付费模式，你只需为存储空间和集群使用量付费。在该模式下，所有集群活动（如 SQL 查询、批量操作和后台任务）都以 [Request Units（RUs）](/tidb-cloud/tidb-cloud-glossary.md#request-unit) 进行量化。RU 是对集群请求规模和复杂度的抽象度量。详细信息请参见 [TiDB Cloud Serverless 价格详情](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/)。

### TiDB Cloud Serverless 是否有免费套餐？

对于你所在组织的前五个 TiDB Cloud Serverless 集群，TiDB Cloud 为每个集群提供如下免费额度：

- 行存储：5 GiB
- 列存储：5 GiB
- [Request Units（RUs）](/tidb-cloud/tidb-cloud-glossary.md#request-unit)：每月 5000 万 RU

如果你使用的是可扩展集群，超出免费额度的部分将会计费。对于免费集群，达到免费额度后，该集群的读写操作将被限流，直到你升级为可扩展集群或新月初重置用量。

更多信息请参见 [TiDB Cloud Serverless 使用额度](/tidb-cloud/select-cluster-tier.md#usage-quota)。

### 免费套餐有哪些限制？

在免费套餐下，由于资源不可扩展，集群性能受到限制。每个查询的内存分配被限制为 256 MiB，并且每秒的 RU 可能出现明显瓶颈。为最大化集群性能并避免这些限制，你可以升级为 [可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)。

### 如何评估我的工作负载所需的 RU 数量并规划每月预算？

要获取单条 SQL 语句的 RU 消耗，可以使用 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption) SQL 语句。但需要注意，`EXPLAIN ANALYZE` 返回的 RU 用量不包含出口（egress）RUs，因为出口用量在网关单独计量，TiDB 服务器无法得知。

要查看集群的 RU 和存储用量，请在集群概览页面查看 **Usage this month** 面板。结合历史资源用量和该面板的实时用量数据，你可以跟踪集群资源消耗并合理预估支出上限。如果免费额度无法满足需求，你可以升级为 [可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan) 并设置支出上限。更多信息请参见 [TiDB Cloud Serverless 使用额度](/tidb-cloud/select-cluster-tier.md#usage-quota)。

### 如何优化我的工作负载以减少 RU 消耗？

请确保你的查询已根据 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md) 指南进行优化，以获得最佳性能。要识别消耗 RU 最多的 SQL 语句，可前往集群的 [**Diagnosis**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page) 页面，查看 **SQL Statements** 标签页，在此可按 **Total RU** 或 **Mean RU** 排序，观察 SQL 执行情况和高消耗语句。更多信息请参见 [语句分析](/tidb-cloud/tune-performance.md#statement-analysis)。此外，减少出口流量同样有助于降低 RU 消耗。建议在查询中仅返回必要的列和行，从而减少网络出口流量。通过精确选择和过滤返回的列与行，可以优化网络利用率。

### TiDB Cloud Serverless 的存储如何计量？

存储计量基于 TiDB Cloud Serverless 集群中存储的数据量，以 GiB/月为单位。计算方式为：所有表和索引的总大小（不含数据压缩或副本）乘以该月内数据存储的小时数。

### 为什么在立即删除表或数据库后，存储用量没有变化？

这是因为 TiDB 会在一段时间内保留已删除的表和数据库。该保留期确保依赖这些表的事务可以继续执行不受影响。此外，保留期也使 [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)/[`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) 功能成为可能，便于你在误删时恢复表和数据库。

### 为什么在没有主动运行查询时仍有 RU 消耗？

多种场景下会产生 RU 消耗。常见场景包括后台查询（如在 TiDB 实例间同步模式变更），以及某些 Web 控制台功能生成的查询（如加载模式）。这些过程即使没有用户显式触发，也会消耗 RU。

### 为什么在负载稳定时 RU 用量会出现突增？

RU 用量突增可能由 TiDB 的必要后台任务引起。这些任务（如自动分析表和重建统计信息）是生成优化查询计划所必需的。

### 当集群用尽免费额度或超出支出上限时会发生什么？

一旦集群达到免费额度或支出上限，系统会立即拒绝任何新的连接请求，直到额度提升或新月初重置用量。已建立的连接在达到额度前会保持活跃，但会受到限流。更多信息请参见 [TiDB Cloud Serverless 限制与配额](/tidb-cloud/serverless-limitations.md#usage-quota)。

### 为什么在导入数据时 RU 用量会出现突增？

在 TiDB Cloud Serverless 集群的数据导入过程中，只有数据成功导入时才会产生 RU 消耗，因此会导致 RU 用量突增。

### 在 TiDB Cloud Serverless 中使用列式存储会产生哪些费用？

TiDB Cloud Serverless 的列式存储计费方式与行存储类似。使用列式存储时，会额外创建一个副本用于存储数据（不含索引）。从行存储到列式存储的数据同步不会产生额外费用。

详细价格信息请参见 [TiDB Cloud Serverless 价格详情](https://www.pingcap.com/tidb-serverless-pricing-details/)。

### 使用列式存储会更贵吗？

TiDB Cloud Serverless 的列式存储由于额外副本，会产生更多存储和数据同步资源的费用。但在运行分析型查询时，列式存储更具性价比。

根据 TPC-H 基准测试，在列式存储上运行分析型查询的成本约为行存储的三分之一。

因此，虽然初期因副本增加会有额外成本，但分析型查询的计算成本降低，使其在特定场景下更具成本优势。尤其对于有分析需求的用户，列式存储可大幅降低成本，带来显著的节省空间。

## 安全常见问题

### 我的 TiDB Cloud Serverless 是共享还是专用的？

Serverless 技术为多租户设计，所有集群使用的资源是共享的。如需获得基础设施和资源隔离的托管 TiDB 服务，你可以升级为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

### TiDB Cloud Serverless 如何保障安全性？

- 你的连接通过传输层安全协议（TLS）加密。关于如何使用 TLS 连接 TiDB Cloud Serverless，详见 [TLS 连接到 TiDB Cloud Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md)。
- TiDB Cloud Serverless 上所有持久化数据均采用集群所在云服务商的工具进行静态加密。

## 运维常见问题

### 我可以升级集群运行的 TiDB 版本吗？

不可以。TiDB Cloud Serverless 集群会随着 TiDB Cloud 推出新版本自动升级。你可以在 [TiDB Cloud 控制台](https://tidbcloud.com/project/clusters) 或最新的 [发布说明](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes) 中查看集群当前运行的 TiDB 版本。你也可以连接到集群，使用 `SELECT version()` 或 `SELECT tidb_version()` 查询 TiDB 版本。