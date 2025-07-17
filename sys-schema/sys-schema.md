---
title: sys Schema
summary: 了解 `sys` schema 中的系统表。
---

# `sys` Schema

从 v8.0.0 版本开始，TiDB 提供了 `sys` schema。你可以使用 `sys` schema 中的视图来了解系统表中的数据，参考 [`INFORMATION_SCHEMA`](/information-schema/information-schema.md) 和 [`PERFORMANCE SCHEMA`](/performance-schema/performance-schema.md) 的内容。

## 兼容 MySQL 的表

| Table name                                                                                       | Description                                               |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)                                  | 记录自 TiDB 上次启动以来未被使用的索引。 |