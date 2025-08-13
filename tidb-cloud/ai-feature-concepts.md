---
title: AI Features
summary: 了解 TiDB Cloud 的 AI 功能。
---

# AI 功能

TiDB Cloud 的 AI 功能让你能够充分利用先进技术进行数据探索、搜索和集成。从基于自然语言的 SQL 查询生成，到高性能的向量搜索，TiDB 将数据库能力与现代 AI 功能相结合，为创新应用提供强大动力。TiDB 支持主流 AI 框架、嵌入模型，并可与 ORM 库无缝集成，为语义搜索和 AI 驱动分析等场景提供了多样化的平台。

本文档将重点介绍这些 AI 功能，以及它们如何提升 TiDB 的使用体验。

## Chat2Query（Beta）

Chat2Query 是集成在 SQL Editor 中的 AI 驱动功能，能够帮助用户通过自然语言指令生成、调试或重写 SQL 查询。更多信息，参见 [Explore your data with AI-assisted SQL Editor](/tidb-cloud/explore-data-with-chat2query.md)。

此外，TiDB Cloud 为 TiDB Cloud Serverless 集群提供了 Chat2Query API。启用后，TiDB Cloud 会自动创建一个名为 Chat2Query 的系统 Data App，以及一个 Data Service 中的 Chat2Data endpoint。你可以调用该 endpoint，通过提供指令让 AI 生成并执行 SQL 语句。更多信息，参见 [Get started with Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

## 向量搜索（Beta）

向量搜索是一种以数据语义为核心、提供相关性结果的搜索方式。

与依赖精确关键词匹配和词频的传统全文搜索不同，向量搜索会将多种数据类型（如文本、图片或音频）转换为高维向量，并基于这些向量之间的相似度进行查询。这种搜索方式能够捕捉数据的语义含义和上下文信息，从而更准确地理解用户意图。

即使搜索词与数据库中的内容并不完全匹配，向量搜索也能通过分析数据的语义，返回符合用户意图的结果。例如，全文搜索 “a swimming animal” 只会返回包含这些精确关键词的结果。而向量搜索则可以返回其他游泳动物（如鱼或鸭子）的结果，即使这些结果中并不包含完全相同的关键词。

更多信息，参见 [Vector Search (Beta) Overview](/vector-search/vector-search-overview.md)。

## AI 集成

### AI 框架

TiDB 官方支持多种主流 AI 框架，使你能够轻松将基于这些框架开发的 AI 应用与 TiDB 向量搜索集成。

支持的 AI 框架列表，参见 [Vector Search Integration Overview](/vector-search/vector-search-integration-overview.md#ai-frameworks)。

### 嵌入模型与服务

向量嵌入（embedding），也称为嵌入，是一组数字序列，用于在高维空间中表示现实世界的对象。它能够捕捉非结构化数据（如文档、图片、音频和视频）的语义和上下文信息。

嵌入模型是一类将数据转换为 [vector embeddings](/vector-search/vector-search-overview.md#vector-embedding) 的算法。选择合适的嵌入模型对于确保语义搜索结果的准确性和相关性至关重要。

TiDB 向量搜索支持存储最多 16383 维的向量，能够满足大多数嵌入模型的需求。对于非结构化文本数据，你可以在 [Massive Text Embedding Benchmark (MTEB) Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) 上找到表现最优的文本嵌入模型。

### 对象关系映射（ORM）库

对象关系映射（ORM）库是一类工具，能够让开发者以所选编程语言中的对象形式操作数据库记录，从而简化应用与关系型数据库之间的交互。

TiDB 支持将向量搜索与 ORM 库集成，实现对向量数据与传统关系数据的统一管理。这一集成对于需要存储和查询 AI 模型生成的向量嵌入的应用尤为有用。通过使用 ORM 库，开发者可以无缝操作存储在 TiDB 中的向量数据，利用数据库能力执行如最近邻搜索等复杂的向量操作。

支持的 ORM 库列表，参见 [Vector Search Integration Overview](/vector-search/vector-search-integration-overview.md#object-relational-mapping-orm-libraries)。