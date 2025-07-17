---
title: sys Schema
summary: Learn about the system tables in the `sys` schema.
---

# `sys` Schema

Starting from v8.0.0, TiDB provides the `sys` schema. You can use the views in `sys` schema to understand the data in the system tables, [`INFORMATION_SCHEMA`](/information-schema/information-schema.md), and [`PERFORMANCE SCHEMA`](/performance-schema/performance-schema.md) of TiDB.

## Tables for MySQL compatibility

| Table name                                                                                       | Description                                               |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)                                  | Records indexes that have not been used since the last start of TiDB. |