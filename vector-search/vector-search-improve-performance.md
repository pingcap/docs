---
title: 提升向量搜索性能
summary: 学习提升 TiDB 向量搜索性能的最佳实践。
---

# 提升向量搜索性能

TiDB 向量搜索使你能够执行近似最近邻（ANN）查询，搜索与图片、文档或其他输入相似的结果。为了提升查询性能，请参考以下最佳实践。

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
> The vector search feature is available on TiDB Self-Managed, [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless), and [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated). For TiDB Self-Managed and TiDB Cloud Dedicated, the TiDB version must be v8.4.0 or later (v8.5.0 or later is recommended).

## 为向量列添加向量搜索索引

[向量搜索索引](/vector-search/vector-search-index.md) 能显著提升向量搜索查询的性能，通常提升 10 倍或更多，代价是召回率略有下降。

## 确保向量索引已完全构建

在插入大量向量数据后，部分数据可能处于 Delta 层，等待持久化。此类数据的向量索引会在数据持久化后进行构建。在所有向量数据完成索引之前，向量搜索的性能不会达到最佳。要查看索引构建进度，请参见 [View index build progress](/vector-search/vector-search-index.md#view-index-build-progress)。

## 减少向量维度或缩短嵌入向量

随着向量维度的增加，向量索引和查询的计算复杂度会显著提升，需进行更多的浮点数比较。

为了优化性能，建议在可行的情况下减少向量维度。这通常需要切换到其他的嵌入模型。在切换模型时，需要评估模型变更对向量查询准确率的影响。

某些嵌入模型如 OpenAI `text-embedding-3-large` 支持 [缩短嵌入向量](https://openai.com/index/new-embedding-models-and-api-updates/)，即在不影响嵌入表达概念的前提下，去除向量序列末尾的一些数字。你也可以使用此类模型来减小向量维度。

## 在结果中排除向量列

向量嵌入数据通常较大，仅在搜索过程中使用。通过在查询结果中排除向量列，可以大幅减少 TiDB 服务器与 SQL 客户端之间传输的数据量，从而提升查询性能。

要排除向量列，应在 `SELECT` 子句中明确列出你希望检索的列，而不是使用 `SELECT *` 来获取所有列。

## 预热索引

当访问从未使用过或长时间未访问的索引（冷访问）时，TiDB 需要从云存储或磁盘加载整个索引（而非从内存加载）。此过程耗时较长，常导致查询延迟增加。此外，如果长时间没有 SQL 查询（例如数小时），计算资源会被回收，后续访问会变成冷访问。

为了避免此类查询延迟，可以在实际工作负载之前，通过运行类似的向量搜索查询预热索引，从而使索引处于热状态。