---
title: 聚合索引
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中聚合索引的相关操作，便于参考。
---

# 聚合索引

本页按功能分类，全面概述了 {{{ .lake }}} 中聚合索引的相关操作，便于参考。

## 聚合索引管理 {#aggregating-index-management}

| 命令 | 描述 |
|---------|-------------|
| [CREATE AGGREGATING INDEX](/tidb-cloud-lake/sql/create-aggregating-index.md) | 为表创建新的聚合索引 |
| [DROP AGGREGATING INDEX](/tidb-cloud-lake/sql/drop-aggregating-index.md) | 删除聚合索引 |
| [REFRESH AGGREGATING INDEX](/tidb-cloud-lake/sql/refresh-aggregating-index.md) | 使用最新数据更新聚合索引 |

## 相关主题 {#related-topics}

- [聚合索引](/tidb-cloud-lake/guides/aggregating-index.md)

> **注意：**
>
> {{{ .lake }}} 中的聚合索引用于通过预先计算并存储聚合结果来提升聚合查询的性能。