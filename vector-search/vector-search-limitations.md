---
title: 向量检索的限制
summary: 了解 TiDB 向量检索的限制。
---

# 向量检索的限制

本文档介绍了 TiDB 向量检索已知的限制。

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
> 向量检索功能适用于 TiDB 自建版、[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)、[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)。对于 TiDB 自建版和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 及以上（推荐 v8.5.0 及以上）。

## 向量数据类型的限制

- 每个 [vector](/vector-search/vector-search-data-types.md) 最多支持 16383 维。
- 向量数据类型无法存储 `NaN`、`Infinity` 或 `-Infinity` 值。
- 向量数据类型无法存储双精度浮点数。如果你在向量列中插入或存储双精度浮点数，TiDB 会将其转换为单精度浮点数。
- 向量列不能作为主键或主键的一部分。
- 向量列不能作为唯一索引或唯一索引的一部分。
- 向量列不能作为分区键或分区键的一部分。
- 目前，TiDB 不支持将向量列修改为其他数据类型（如 `JSON` 和 `VARCHAR`）。

## 向量索引的限制

参见 [向量检索限制](/vector-search/vector-search-index.md#restrictions)。

## 与 TiDB 工具的兼容性

<CustomContent platform="tidb">

- 请确保你使用的是 v8.4.0 或更高版本的 BR 进行数据备份和恢复。不支持将包含向量数据类型的表恢复到 v8.4.0 之前的 TiDB 集群。
- TiDB Data Migration (DM) 不支持将 MySQL 向量数据类型迁移或同步到 TiDB。
- 当 TiCDC 将向量数据同步到不支持向量数据类型的下游时，会将向量数据类型转换为其他类型。更多信息请参见 [与向量数据类型的兼容性](/ticdc/ticdc-compatibility.md#compatibility-with-vector-data-types)。

</CustomContent>

<CustomContent platform="tidb-cloud">

- TiDB Cloud 控制台中的数据迁移功能不支持将 MySQL 向量数据类型迁移或同步到 TiDB Cloud。

</CustomContent>

## 反馈

我们非常重视你的反馈，并随时为你提供帮助：

<CustomContent platform="tidb">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)
- [访问我们的支持门户](https://tidb.support.pingcap.com/)

</CustomContent>
