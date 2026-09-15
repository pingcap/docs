---
title: system.tables_with_history
summary: 提供所有表（包括历史表）的元信息。它包含表属性、创建时间、行数、数据大小等详细信息。
---

# system.tables_with_history

提供所有表（包括历史表）的元信息。它包含表属性、创建时间、行数、数据大小等详细信息。

另请参阅：[SHOW DROP TABLES](/tidb-cloud-lake/sql/show-drop-tables.md)

```sql title='Examples:'
SELECT * FROM system.tables_with_history LIMIT 3;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ catalog │ database │        name        │       table_id      │ total_columns │         engine        │      engine_full      │ cluster_by │ is_transient │ is_attach │         created_on         │      dropped_on     │         updated_on         │     num_rows     │     data_size    │ data_compressed_size │    index_size    │ number_of_segments │ number_of_blocks │       owner      │ comment │ table_type │
├─────────┼──────────┼────────────────────┼─────────────────────┼───────────────┼───────────────────────┼───────────────────────┼────────────┼──────────────┼───────────┼────────────────────────────┼─────────────────────┼────────────────────────────┼──────────────────┼──────────────────┼──────────────────────┼──────────────────┼────────────────────┼──────────────────┼──────────────────┼─────────┼────────────┤
│ default │ system   │ metrics            │ 4611686018427387919 │             5 │ SystemMetrics         │ SystemMetrics         │            │              │           │ 2024-11-20 21:04:12.950815 │ NULL                │ 2024-11-20 21:04:12.950815 │             NULL │             NULL │                 NULL │             NULL │               NULL │             NULL │ NULL             │         │ BASE TABLE │
│ default │ system   │ clustering_history │ 4611686018427387925 │             6 │ SystemLogTable        │ SystemLogTable        │            │              │           │ 2024-11-20 21:04:12.952439 │ NULL                │ 2024-11-20 21:04:12.952439 │             NULL │             NULL │                 NULL │             NULL │               NULL │             NULL │ NULL             │         │ BASE TABLE │
│ default │ system   │ queries_profiling  │ 4611686018427387941 │             7 │ QueriesProfilingTable │ QueriesProfilingTable │            │              │           │ 2024-11-20 21:04:12.952588 │ NULL                │ 2024-11-20 21:04:12.952588 │             NULL │             NULL │                 NULL │             NULL │               NULL │             NULL │ NULL             │         │ BASE TABLE │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

要查看 `system.tables_with_history` 的表结构，请使用 `DESCRIBE system.tables_with_history`：

```sql
DESCRIBE system.tables_with_history;

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│         Field        │       Type      │  Null  │            Default           │  Extra │
├──────────────────────┼─────────────────┼────────┼──────────────────────────────┼────────┤
│ catalog              │ VARCHAR         │ NO     │ ''                           │        │
│ database             │ VARCHAR         │ NO     │ ''                           │        │
│ name                 │ VARCHAR         │ NO     │ ''                           │        │
│ table_id             │ BIGINT UNSIGNED │ NO     │ 0                            │        │
│ total_columns        │ BIGINT UNSIGNED │ NO     │ 0                            │        │
│ engine               │ VARCHAR         │ NO     │ ''                           │        │
│ engine_full          │ VARCHAR         │ NO     │ ''                           │        │
│ cluster_by           │ VARCHAR         │ NO     │ ''                           │        │
│ is_transient         │ VARCHAR         │ NO     │ ''                           │        │
│ is_attach            │ VARCHAR         │ NO     │ ''                           │        │
│ created_on           │ TIMESTAMP       │ NO     │ '1970-01-01 00:00:00.000000' │        │
│ dropped_on           │ TIMESTAMP       │ YES    │ NULL                         │        │
│ updated_on           │ TIMESTAMP       │ NO     │ '1970-01-01 00:00:00.000000' │        │
│ num_rows             │ BIGINT UNSIGNED │ YES    │ NULL                         │        │
│ data_size            │ BIGINT UNSIGNED │ YES    │ NULL                         │        │
│ data_compressed_size │ BIGINT UNSIGNED │ YES    │ NULL                         │        │
│ index_size           │ BIGINT UNSIGNED │ YES    │ NULL                         │        │
│ number_of_segments   │ BIGINT UNSIGNED │ YES    │ NULL                         │        │
│ number_of_blocks     │ BIGINT UNSIGNED │ YES    │ NULL                         │        │
│ owner                │ VARCHAR         │ YES    │ NULL                         │        │
│ comment              │ VARCHAR         │ NO     │ ''                           │        │
│ table_type           │ VARCHAR         │ NO     │ ''                           │        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```