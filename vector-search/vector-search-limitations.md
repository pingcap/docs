---
title: Vector Search Limitations
summary: 了解 TiDB 向量搜索的限制。
---

# Vector Search Limitations

本文档描述了 TiDB 向量搜索的已知限制。

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
> The vector search feature is available on TiDB Self-Managed, [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless), and [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated). For TiDB Self-Managed and TiDB Cloud Dedicated, the TiDB 版本必须是 v8.4.0 或更高（建议 v8.5.0 或更高）。

## Vector data type limitations

- 每个 [vector](/vector-search/vector-search-data-types.md) 支持最多 16383 维。
- 向量数据类型不能存储 `NaN`、`Infinity` 或 `-Infinity` 值。
- 向量数据类型不能存储双精度浮点数。如果你在向量列中插入或存储双精度浮点数，TiDB 会将其转换为单精度浮点数。
- 向量列不能用作主键或作为主键的一部分。
- 向量列不能用作唯一索引或作为唯一索引的一部分。
- 向量列不能用作分区键或作为分区键的一部分。
- 目前，TiDB 不支持将向量列修改为其他数据类型（如 `JSON` 和 `VARCHAR`）。

## Vector index limitations

请参阅 [Vector search restrictions](/vector-search/vector-search-index.md#restrictions)。

## Compatibility with TiDB tools

<CustomContent platform="tidb">

- 确保你使用的是 v8.4.0 或更高版本的 BR 进行数据备份和还原。不支持将带有向量数据类型的表还原到早于 v8.4.0 的 TiDB 集群。
- TiDB Data Migration (DM) 不支持将 MySQL 9.0 的向量数据类型迁移或复制到 TiDB。
- 当 TiCDC 将向量数据复制到不支持向量数据类型的下游时，会将向量数据类型更改为其他类型。更多信息请参见 [Compatibility with vector data types](/ticdc/ticdc-compatibility.md#compatibility-with-vector-data-types)。

</CustomContent>

<CustomContent platform="tidb-cloud">

- TiDB Cloud 控制台中的 Data Migration 功能不支持将 MySQL 9.0 的向量数据类型迁移或复制到 TiDB Cloud。

</CustomContent>

## Feedback

我们重视你的反馈，并随时愿意提供帮助：

<CustomContent platform="tidb">

- [Join our Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [Join our Discord](https://discord.gg/zcqexutz2R)
- [Visit our Support Portal](https://tidb.support.pingcap.com/)

</CustomContent>