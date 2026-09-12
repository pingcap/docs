---
title: information_schema.tables
summary: `information_schema.tables` 系统表是一个视图，用于提供所有数据库中所有表的元信息，包括其 schema、类型、引擎以及创建详情。它还包含诸如数据长度、索引长度和行数等存储指标信息，帮助了解表结构和使用情况。
---

# information_schema.tables

`information_schema.tables` 系统表是一个视图，用于提供所有数据库中所有表的元信息，包括其 schema、类型、引擎以及创建详情。它还包含诸如数据长度、索引长度和行数等存储指标信息，帮助了解表结构和使用情况。

```sql
DESCRIBE information_schema.tables;

┌────────────────────────────────────────────────────────────────────────────────────┐
│      Field      │       Type      │  Null  │            Default           │  Extra │
├─────────────────┼─────────────────┼────────┼──────────────────────────────┼────────┤
│ table_catalog   │ VARCHAR         │ NO     │ ''                           │        │
│ table_schema    │ VARCHAR         │ NO     │ ''                           │        │
│ table_name      │ VARCHAR         │ NO     │ ''                           │        │
│ table_type      │ VARCHAR         │ NO     │ ''                           │        │
│ engine          │ VARCHAR         │ NO     │ ''                           │        │
│ create_time     │ TIMESTAMP       │ NO     │ '1970-01-01 00:00:00.000000' │        │
│ drop_time       │ TIMESTAMP       │ YES    │ NULL                         │        │
│ data_length     │ BIGINT UNSIGNED │ YES    │ NULL                         │        │
│ index_length    │ BIGINT UNSIGNED │ YES    │ NULL                         │        │
│ table_rows      │ BIGINT UNSIGNED │ YES    │ NULL                         │        │
│ auto_increment  │ NULL            │ NO     │ NULL                         │        │
│ table_collation │ NULL            │ NO     │ NULL                         │        │
│ data_free       │ NULL            │ NO     │ NULL                         │        │
│ table_comment   │ VARCHAR         │ NO     │ ''                           │        │
└────────────────────────────────────────────────────────────────────────────────────┘
```