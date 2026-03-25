---
title: "TiDB Cloud Starter 常见问题"
summary: 了解与 TiDB Cloud Starter 相关的最常见问题（FAQ）。
aliases: ['/zh/tidbcloud/serverless-tier-faqs']
---

# TiDB Cloud Starter 常见问题

<!-- markdownlint-disable MD026 -->

本文档列出了关于 TiDB Cloud Starter 的最常见问题。

## 通用常见问题

### 什么是 TiDB Cloud Starter？

TiDB Cloud Starter 为你和你的组织提供具备完整 HTAP 能力的 TiDB 数据库。它是一个全托管、自动扩展的 TiDB 部署，让你可以立即开始使用数据库，开发和运行应用程序，无需关心底层节点，并且能够根据应用负载变化自动扩展。

### TiDB Cloud Starter 与 TiDB Cloud Serverless 有什么关系？

自 2025 年 8 月 12 日起，TiDB Cloud Starter 是 TiDB Cloud Serverless 的新名称。

在更名为 Starter 之前，TiDB Cloud 的 Serverless 层作为数千开发者的入门点，提供了一个可用于生产的数据库，能够自动扩展，几秒内启动，并且在超出大量免费额度前无需付费。

虽然 “serverless” 准确反映了该服务的工作方式，但许多首次使用的用户觉得这个术语抽象且含义繁杂。

为了让这个入门层的用途更加清晰，我们将其更名为 Starter，这是使用 TiDB Cloud 构建应用的最快方式。你对 Serverless 层的所有了解依然适用：

- 一个全托管的数据库，支持行存和列存，适用于混合 OLTP 和 OLAP 负载。
- 自动且按需扩展，无需容量规划或手动调优。
- 内置向量搜索和全文搜索，支持 GenAI 检索、聊天机器人及其他 AI 应用。
- 每个组织每月最多可免费创建五个集群（每个集群 5 GiB 行存数据 + 5 GiB 列存数据 + 5000 万 [RU](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)）。

### 如何开始使用 TiDB Cloud Starter？

请参考 5 分钟上手指南 [TiDB Cloud 快速入门](/tidb-cloud/tidb-cloud-quickstart.md)

### 在 TiDB Cloud 中，我最多可以创建多少个 TiDB Cloud Starter 集群？

在 TiDB Cloud 中，每个组织默认最多可以创建五个 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 集群。如需创建更多 TiDB Cloud Starter 集群，你需要添加信用卡并设置 [消费上限](/tidb-cloud/manage-serverless-spend-limit.md)。

### TiDB Cloud Starter 是否完全支持所有 TiDB Cloud 功能？

部分 TiDB Cloud 功能在 TiDB Cloud Starter 上仅部分支持或不支持。详情请参见 [TiDB Cloud Starter 限制与配额](/tidb-cloud/serverless-limitations.md)。

### TiDB Cloud Starter 何时会支持除 AWS 以外的云平台，如 Google Cloud 或 Azure？

我们正在积极推进 TiDB Cloud Starter 向 Google Cloud 和 Azure 等其他云平台的扩展。但目前尚无具体时间表，因为我们当前专注于补齐功能差距并确保所有环境下的无缝体验。请放心，我们会持续努力让 TiDB Cloud Starter 支持更多云平台，并在进展过程中及时向社区更新。

### 在 TiDB Cloud Starter 推出前，我创建了 Developer Tier 集群。还能继续使用吗？

可以，你的 Developer Tier 集群已自动迁移为 TiDB Cloud Starter 集群，带来更好的用户体验，且不会影响你之前的使用。

### 什么是 TiDB Cloud Starter 的列存储？

TiDB Cloud Starter 的列存储作为行存储的额外副本，确保强一致性。与传统的行存储（按行存储数据）不同，列存储按列组织数据，优化了数据分析任务。

列存储是实现 TiDB HTAP (Hybrid Transactional and Analytical Processing) 能力的关键特性，通过无缝融合事务型和分析型负载。

为高效管理列存储数据，TiDB Cloud Starter 使用独立的弹性 TiFlash 引擎。在查询执行过程中，优化器会自动引导集群决定从行存储还是列存储读取数据。

### 在 TiDB Cloud Starter 中，什么时候应该使用列存储？

在以下场景中建议使用 TiDB Cloud Starter 的列存储：

- 你的负载包含需要高效数据扫描和聚合的分析型任务。
- 你优先考虑提升分析型负载的性能。
- 你希望将分析处理与事务处理隔离，避免对 TP 负载产生性能影响。独立的列存储有助于优化不同的负载模式。

在这些场景下，列存储可以显著提升查询性能，为系统中的混合负载带来无缝体验。

### 如何在 TiDB Cloud Starter 中使用列存储？

在 TiDB Cloud Starter 中使用列存储与 TiFlash 的用法类似。你可以在表级别和数据库级别启用列存储：

- 表级别：为某个表分配 TiFlash 副本，为该表启用列存储。
- 数据库级别：为数据库内所有表配置 TiFlash 副本，实现整个数据库的列存储。

为表设置 TiFlash 副本后，TiDB 会自动将该表的数据从行存储同步到列存储，确保数据一致性并优化分析型查询的性能。

关于如何设置 TiFlash 副本，详见 [创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)。

### 为什么我的连接在空闲几分钟后会断开？

当你通过 Public Endpoint 连接时，连接会经过多个网络服务商和中间设备。这些设备可能有较短的空闲超时时间，导致连接被提前中断。详情请参见 [连接限制](/tidb-cloud/serverless-limitations.md#connection)。

### 为什么会收到 “Connection limit exceeded” 错误？

当你的集群超过最大并发连接数限制时，会出现该错误。详情请参见 [连接限制](/tidb-cloud/serverless-limitations.md#connection)。

## 计费与计量常见问题

### 什么是 Request Units？

TiDB Cloud Starter 采用按需付费模式，即你只需为存储空间和集群使用量付费。在该模式下，所有集群活动（如 SQL 查询、大批量操作和后台作业）都以 [Request Units (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru) 进行量化。RU 是对在集群上发起的请求规模和复杂度的抽象度量。详情请参见 [TiDB Cloud Starter 价格详情](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)。

### TiDB Cloud Starter 是否有免费计划？

对于你所在组织的前五个 TiDB Cloud Starter 集群，TiDB Cloud 为每个集群提供如下免费额度：

- 行存储：5 GiB
- 列存储：5 GiB
- [Request Units (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)：每月 5000 万 RU

如果为某个 TiDB Cloud Starter 集群设置了每月消费上限，超出免费额度的部分将会计费。对于免费集群，达到免费额度后，该集群的读写操作将被限流，直到你设置每月消费上限或新月开始时用量重置。

详情请参见 [TiDB Cloud Starter 使用额度](/tidb-cloud/select-cluster-tier.md#usage-quota)。

### 免费计划有哪些限制？

在免费计划下，集群性能受限于不可扩展的资源。每个查询的内存分配被限制为 256 MiB，并且每秒的 RU 可能出现瓶颈。为最大化集群性能并避免这些限制，你可以为 TiDB Cloud Starter 集群 [设置每月消费上限](/tidb-cloud/manage-serverless-spend-limit.md)。

### 如何评估我的负载所需的 RU 数量并规划每月预算？

要获取单条 SQL 语句的 RU 消耗，可以使用 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption) SQL 语句。但需要注意，`EXPLAIN ANALYZE` 返回的 RU 用量不包含出口流量 RU，因为出口用量在网关单独计量，TiDB 服务器无法获知。

要查看集群的 RU 和存储用量，请在集群概览页面查看 **本月用量** 面板。结合历史资源用量和该面板的实时用量数据，你可以跟踪集群资源消耗并合理预估消费上限。如果免费额度无法满足需求，可以编辑消费上限以获取更多资源。详情请参见 [TiDB Cloud Starter 使用额度](/tidb-cloud/select-cluster-tier.md#usage-quota)。

### 如何优化我的负载以减少 RU 消耗？

请确保你的查询已根据 [优化 SQL 性能](/develop/dev-guide-optimize-sql-overview.md) 指南进行优化，以获得最佳性能。要识别消耗 RU 最多的 SQL 语句，可进入集群的 [**诊断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page) 页面，查看 **SQL Statements** 标签页，在此可观察 SQL 执行情况，并按 **Total RU** 或 **Mean RU** 排序查看高消耗语句。详情请参见 [语句分析](/tidb-cloud/tune-performance.md#statement-analysis)。此外，减少出口流量同样有助于降低 RU 消耗。建议在查询中仅返回必要的列和行，从而减少网络出口流量。通过精确选择和过滤返回的列与行，可以优化网络利用率。

### TiDB Cloud Starter 的存储如何计量？

存储计量基于 TiDB Cloud Starter 集群中存储的数据量，以 GiB/月为单位。计算方式为：所有表和索引的总大小（不含数据压缩或副本）乘以该月内数据存储的小时数。

### 为什么在立即删除表或数据库后，存储用量没有变化？

这是因为 TiDB 会在一段保留时间内保留已删除的表和数据库。该保留时间确保依赖这些表的事务可以继续执行不受影响。此外，保留时间也使 [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)/[`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) 功能成为可能，便于你在误删时恢复表和数据库。

### 为什么在没有主动运行查询时仍有 RU 消耗？

RU 消耗可能出现在多种场景。常见场景包括后台查询，如在 TiDB 实例间同步 schema 变更、执行 DDL 作业、刷新权限、刷新 SQL 绑定和刷新全局变量等。另一个场景是某些 Web 控制台功能会生成查询，如加载 schema。这些过程即使没有用户主动触发，也会消耗 RU。

### 为什么在负载稳定时 RU 用量会出现突增？

RU 用量突增可能是由于 TiDB 必要的后台作业引起。这些作业（如自动分析表和重建统计信息）用于生成优化的查询计划。

### 当集群用尽免费额度或超出消费上限时会发生什么？

当集群达到免费额度或消费上限后，系统会立即拒绝任何新的连接请求，直到额度提升或新月开始时用量重置。已建立的连接会继续保持，但会被限流。详情请参见 [TiDB Cloud Starter 限制与配额](/tidb-cloud/serverless-limitations.md#usage-quota)。

### 为什么在导入数据时 RU 用量会出现突增？

在 TiDB Cloud Starter 集群的数据导入过程中，只有数据成功导入时才会消耗 RU，因此会导致 RU 用量突增。

### 在 TiDB Cloud Starter 中使用列存储会产生哪些费用？

TiDB Cloud Starter 的列存储计费方式与行存储类似。使用列存储时，会额外创建一个副本用于存储数据（不含索引）。从行存储到列存储的数据同步不会产生额外费用。

详细价格信息请参见 [TiDB Cloud Starter 价格详情](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)。

### 使用列存储是否更贵？

TiDB Cloud Starter 的列存储由于额外副本，会产生更多存储和数据同步资源消耗，因此成本更高。但在运行分析型查询时，列存储更具性价比。

根据 TPC-H 基准测试，在列存储上运行分析型查询的成本约为行存储的三分之一。

因此，虽然初期因副本增加带来一定成本，但分析型查询的计算成本大幅降低，对于特定场景更具性价比。尤其对于有分析需求的用户，列存储可显著降低成本，带来可观的节省空间。

## 安全常见问题

### 我的 TiDB Cloud Starter 是共享还是专用的？

Serverless 技术采用多租户技术，所有集群使用的资源是共享的。如需获得基础设施和资源隔离的托管 TiDB 服务，可以升级为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

### TiDB Cloud Starter 如何保障安全？

- 你的连接通过 Transport Layer Security (TLS) 加密。关于如何使用 TLS 连接 TiDB Cloud Starter，详见 [TLS 连接到 TiDB Cloud Starter](/tidb-cloud/secure-connections-to-serverless-clusters.md)。
- TiDB Cloud Starter 上所有持久化数据均采用集群所在云服务商的工具进行静态加密。

## 运维常见问题

### 我可以升级集群运行的 TiDB 版本吗？

不可以。TiDB Cloud Starter 集群会随着 TiDB Cloud 推出新版本自动升级。你可以在 [TiDB Cloud 控制台](https://tidbcloud.com/project/clusters) 或最新的 [发布说明](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes) 查看集群当前的 TiDB 版本。你也可以连接到集群，使用 `SELECT version()` 或 `SELECT tidb_version()` 查询 TiDB 版本。