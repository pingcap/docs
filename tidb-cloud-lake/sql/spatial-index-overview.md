---
title: 空间索引
summary: 空间索引可加速对 `GEOMETRY` 列的空间谓词过滤。
---

# 空间索引

{{{ .lake }}} 中的空间索引可加速对 `GEOMETRY` 列的空间谓词过滤。它们专为 Fuse 表设计，并帮助优化器在计算精确空间函数之前先裁剪数据块。

> **Tip:**
>
> 空间索引会自动维护创建索引后写入的数据。对于创建索引前表中已存在的数据，如果你需要回填现有行，请使用 `REFRESH SPATIAL INDEX`。

## 空间索引管理 {#spatial-index-management}

| Command | 描述 |
|---------|-------------|
| [CREATE SPATIAL INDEX](/tidb-cloud-lake/sql/create-spatial-index.md) | 在一个或多个 `GEOMETRY` 列上创建新的空间索引 |
| [REFRESH SPATIAL INDEX](/tidb-cloud-lake/sql/refresh-spatial-index.md) | 为创建索引前已存在的行回填空间索引数据 |
| [DROP SPATIAL INDEX](/tidb-cloud-lake/sql/drop-spatial-index.md) | 从表中删除空间索引 |

## 支持的谓词 {#supported-predicates}

{{{ .lake }}} 可以使用空间索引来加速基于以下空间谓词构建的查询：

- `ST_CONTAINS`
- `ST_INTERSECTS`
- `ST_WITHIN`
- `ST_DWITHIN`

## 限制 {#limitations}

- 空间索引支持用于 Fuse 表。
- 建立索引的列必须是 `GEOMETRY` 类型。
- 不支持 `GEOGRAPHY` 列。

## 相关主题 {#related-topics}

- [地理空间函数](/tidb-cloud-lake/sql/geospatial-functions.md)