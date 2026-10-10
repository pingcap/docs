---
title: information_schema.tables
summary: information_schema.tables システムテーブルは、すべてのデータベースにまたがるすべてのテーブルに関するメタデータを提供するビューであり、スキーマ、タイプ、エンジン、作成の詳細などを含みます。また、data length、index length、row count などのストレージメトリクスも含まれており、テーブル構造と使用状況を把握するのに役立ちます。
---

# information_schema.tables

`information_schema.tables` システムテーブルは、すべてのデータベースにまたがるすべてのテーブルに関するメタデータを提供するビューであり、スキーマ、タイプ、エンジン、作成の詳細などを含みます。また、data length、index length、row count などのストレージメトリクスも含まれており、テーブル構造と使用状況を把握するのに役立ちます。

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