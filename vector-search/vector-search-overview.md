---
title: Vector Search 概览
summary: 了解 TiDB 中的 Vector Search。该功能提供了一种先进的搜索解决方案，用于在各种数据类型（包括文档、图片、音频和视频）中执行语义相似性搜索。
---

# Vector Search 概览

Vector search 为跨多种数据类型（如文档、图片、音频和视频）提供了一种强大的语义相似性搜索解决方案。它允许开发者利用他们的 MySQL 专业知识，构建具有生成式 AI 功能的可扩展应用，简化了高级搜索功能的集成。

<CustomContent platform="tidb">

> **Warning:**
>
> The vector search feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> The vector search feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> The vector search feature is available on TiDB Self-Managed, [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless), and [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated). 对于 TiDB Self-Managed 和 TiDB Cloud Dedicated，TiDB 版本必须为 v8.4.0 或更高（建议 v8.5.0 或更高）。

## 概念

Vector search 是一种以数据的语义为优先的搜索方法，旨在提供相关性更高的结果。

不同于依赖精确关键词匹配和词频的传统全文搜索，vector search 将各种数据类型（如文本、图片或音频）转换为高维向量，并基于这些向量之间的相似性进行查询。这种搜索方式捕捉了数据的语义含义和上下文信息，从而实现对用户意图的更精准理解。

即使搜索词与数据库中的内容不完全匹配，vector search 仍能通过分析数据的语义，提供符合用户意图的结果。

例如，全文搜索“a swimming animal” 只会返回包含这些关键词的结果。而 vector search 可以返回其他会游泳的动物，比如鱼或鸭子，即使这些结果不包含完全相同的关键词。

### Vector embedding

Vector embedding，也称为 embedding，是一组用以表示现实世界对象的数字序列，存在于高维空间中。它捕捉非结构化数据（如文档、图片、音频和视频）的含义和上下文。

Vector embedding 在机器学习中至关重要，是实现语义相似性搜索的基础。

TiDB 引入了 [Vector data types](/vector-search/vector-search-data-types.md) 和 [Vector search index](/vector-search/vector-search-index.md)，旨在优化向量 embedding 的存储与检索，增强其在 AI 应用中的使用效果。你可以在 TiDB 中存储 vector embedding，并通过这些数据类型执行 vector search 查询，以找到最相关的数据。

### Embedding model

Embedding model 是将数据转换为 [vector embedding](#vector-embedding) 的算法。

选择合适的 embedding model 对确保语义搜索结果的准确性和相关性至关重要。对于非结构化文本数据，你可以在 [Massive Text Embedding Benchmark (MTEB) Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) 上找到表现优异的文本 embedding 模型。

若要了解如何为你的特定数据类型生成 vector embedding，请参考集成教程或 embedding 模型的示例。

## Vector search 的工作原理

将原始数据转换为 vector embedding 并存储在 TiDB 后，你的应用可以执行 vector search 查询，以找到与用户查询在语义或上下文上最相关的数据。

TiDB 的 vector search 通过使用 [distance function](/vector-search/vector-search-functions-and-operators.md) 计算给定向量与数据库中存储的向量之间的距离，从而识别前 k 个最近邻（KNN）向量。距离最接近的向量代表在意义上最相似的数据。

![The Schematic TiDB Vector Search](/media/vector-search/embedding-search.png)

作为具有集成 vector search 功能的关系型数据库，TiDB 允许你将数据及其对应的向量表示（即 vector embedding）存储在同一数据库中。你可以选择以下存储方式：

- 将数据及其对应的 vector 表示存储在同一表的不同列中。
- 将数据及其对应的 vector 表示存储在不同的表中。在这种情况下，检索数据时需要使用 `JOIN` 查询将表连接起来。

## 应用场景

### Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation（RAG）是一种旨在优化大型语言模型（LLMs）输出的架构。通过使用 vector search，RAG 应用可以在数据库中存储 vector embedding，并在 LLM 生成响应时检索相关文档作为额外上下文，从而提升答案的质量和相关性。

### Semantic search

语义搜索是一种基于查询含义返回结果的搜索技术，而非仅仅匹配关键词。它利用 embedding 解释不同语言和各种数据类型（如文本、图片和音频）中的含义。然后，vector search 算法使用这些 embedding 来找到最符合用户查询的相关数据。

### Recommendation engine

推荐引擎是一种主动向用户推荐内容、产品或服务的系统。它通过创建代表用户行为和偏好的 embedding，帮助系统识别其他用户互动或感兴趣的类似项目。这增加了推荐的相关性和吸引力。

## 相关链接

若要开始使用 TiDB Vector Search，请参考以下文档：

- [Get started with vector search using Python](/vector-search/vector-search-get-started-using-python.md)
- [Get started with vector search using SQL](/vector-search/vector-search-get-started-using-sql.md)
