---
title: TiDB Cloud Lake 概览
summary: TiDB Cloud Lake 是面向分析型工作负载的云原生数据仓库服务。它将计算与存储分离，并支持 ANSI SQL、半结构化数据处理以及面向 AI 的工作流。
---

# TiDB Cloud Lake 概览

TiDB Cloud Lake 是面向分析型工作负载的云原生数据仓库服务。它将计算与存储分离，使你能够独立配置计算集群，并随着工作负载变化进行扩展，同时以更具成本效益的方式将数据存储在对象存储中。

TiDB Cloud Lake 在一个平台中支持 ANSI SQL、半结构化数据处理、向量搜索以及面向 AI 的工作流。它专为希望获得托管式分析体验、而无需自行运维底层基础设施的团队而设计。

> **警告：**
>
> TiDB Cloud Lake 当前处于 **public preview** 阶段。随着我们持续改进产品，功能可用性和服务限制可能会发生变化。

## 为什么选择 {{{ .lake }}}？ {#why-lake}

{{{ .lake }}} 将分析、向量、搜索和地理空间工作负载整合到一个云原生平台中。借助存储与计算分离、ANSI SQL 支持以及托管式基础设施，团队能够以更高的灵活性、更好的性能和更优的成本效率处理多模态数据。

| 功能 | 描述 | 了解更多 |
|---|---|---|
| **统一引擎** | 分析、向量、搜索和地理空间共享同一个优化器和运行时。 | [TiDB Cloud Lake 架构](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md) |
| **统一数据** | 结构化、半结构化、非结构化和向量数据共享对象存储。 | [TiDB Cloud Lake 架构](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md) |
| **原生分析** | ANSI SQL、窗口函数、增量聚合和流式 BI 在同一平台上运行。 | [工作区](/tidb-cloud-lake/guides/worksheet.md) |
| **原生向量** | Embeddings、向量索引和语义检索都可在 SQL 中运行。 | [向量搜索](/tidb-cloud-lake/guides/vector-search-guide.md) |
| **原生搜索** | 全文搜索和倒排索引为混合检索提供支持。 | [全文索引](/tidb-cloud-lake/guides/full-text-index.md) |
| **原生地理空间** | 地理空间索引和函数为地图与位置服务提供支持。 | [地理空间分析](/tidb-cloud-lake/guides/geo-analytics.md) |

## 开始使用 {#get-started}

1. [**快速入门**](/tidb-cloud-lake/lake-quick-start.md)：创建你的账户并运行第一个工作流。
2. [**连接到 TiDB Cloud Lake**](/tidb-cloud-lake/guides/connection-overview.md)：为你的工作流选择合适的客户端或驱动。
3. [**了解架构**](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md)：了解元信息、计算和存储层。
4. [**探索产品功能**](/tidb-cloud-lake/guides/vector-search-guide.md)：从分析、向量、搜索和地理空间能力开始探索。