---
title: 提升向量检索性能
summary: 了解提升 TiDB 向量检索性能的最佳实践。
---

# 提升向量检索性能

TiDB 向量检索支持执行近似最近邻（ANN）查询，用于查找与图片、文档或其他输入相似的结果。为了提升查询性能，请参考以下最佳实践。

<CustomContent platform="tidb">

> **Warning:**
>
> 向量检索功能为实验性特性。不建议在生产环境中使用。该功能可能会在没有提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 向量检索功能处于 beta 阶段，可能会在没有提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

> **Note:**
>
> 向量检索功能适用于 TiDB 自建版、[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)。对于 TiDB 自建版和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 及以上（推荐 v8.5.0 及以上）。

## 为向量列添加向量检索索引

[向量检索索引](/vector-search/vector-search-index.md) 能显著提升向量检索查询的性能，通常可提升 10 倍以上，代价仅为召回率的轻微下降。

## 确保向量索引已完全构建

在你插入大量向量数据后，部分数据可能仍处于 Delta 层，等待持久化。这部分数据的向量索引会在数据持久化后构建。在所有向量数据都被索引之前，向量检索的性能并不理想。要查看索引的构建进度，请参见 [查看索引构建进度](/vector-search/vector-search-index.md#view-index-build-progress)。

## 降低向量维度或缩短嵌入向量

随着向量维度的增加，向量检索索引和查询的计算复杂度会显著提升，需要进行更多的浮点数比较。

为了优化性能，建议在可行的情况下降低向量维度。这通常需要切换到其他嵌入模型。在切换模型时，你需要评估模型变更对向量查询准确率的影响。

某些嵌入模型（如 OpenAI 的 `text-embedding-3-large`）支持[缩短嵌入向量](https://openai.com/index/new-embedding-models-and-api-updates/)，即在不影响嵌入向量语义表达能力的前提下，从向量序列末尾移除部分数值。你也可以通过此类嵌入模型来降低向量维度。

## 查询结果中排除向量列

向量嵌入数据通常体积较大，仅在检索过程中使用。通过在查询结果中排除向量列，可以大幅减少 TiDB 服务器与 SQL 客户端之间传输的数据量，从而提升查询性能。

要排除向量列，请在 `SELECT` 子句中显式列出你需要查询的字段，而不是使用 `SELECT *` 查询所有列。

## 预热索引

当访问从未被使用过或长时间未被访问（冷访问）的索引时，TiDB 需要从云存储或磁盘（而非内存）加载整个索引。此过程会耗费一定时间，通常导致查询延迟升高。此外，如果长时间（如数小时）没有 SQL 查询，计算资源会被回收，后续访问也会变为冷访问。

为避免此类查询延迟，在实际负载前，可以通过执行命中向量索引的类似向量检索查询来预热索引。