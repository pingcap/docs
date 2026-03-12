---
title: information_schema.tables
---

The `information_schema.tables` system table is a view that provides metadata about all tables across all databases, including their schema, type, engine, and creation details. It also includes storage metrics such as data length, index length, and row count, offering insights into table structure and usage.


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