---
title: system.views
---

Provides metadata information for all views. 

See also:

- [information_schema.views](../20-information-schema-tables/information-schema-views.md)
- [SHOW VIEWS](../../10-sql-commands/00-ddl/05-view/show-views.md)

```sql title='Examples:'
SELECT * FROM system.views LIMIT 3;

╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ catalog │ database │ database_id │  name  │ table_id │ engine │ engine_full │         created_on         │      dropped_on     │         updated_on         │       owner      │ comment │            view_query           │
│  String │  String  │    UInt64   │ String │  UInt64  │ String │    String   │          Timestamp         │ Nullable(Timestamp) │          Timestamp         │ Nullable(String) │  String │              String             │
├─────────┼──────────┼─────────────┼────────┼──────────┼────────┼─────────────┼────────────────────────────┼─────────────────────┼────────────────────────────┼──────────────────┼─────────┼─────────────────────────────────┤
│ default │ default  │           1 │ b      │   133095 │ VIEW   │ VIEW        │ 2025-06-30 04:59:27.844141 │ NULL                │ 2025-06-30 04:59:27.844142 │ NULL             │         │ SELECT * FROM hits.hits LIMIT 1 │
│ default │ default  │           1 │ c      │   119483 │ VIEW   │ VIEW        │ 2025-06-30 02:51:52.319229 │ NULL                │ 2025-06-30 02:51:52.319229 │ NULL             │         │ SELECT * FROM default.a         │
│ default │ default  │           1 │ v      │   133330 │ VIEW   │ VIEW        │ 2025-06-30 05:24:42.054795 │ NULL                │ 2025-06-30 05:24:42.054796 │ NULL             │         │ SELECT * FROM default.t         │
│ default │ default  │           1 │ xvl    │   119736 │ VIEW   │ VIEW        │ 2025-06-30 03:55:24.335369 │ NULL                │ 2025-06-30 03:55:24.335370 │ NULL             │         │ SELECT * FROM hits.hits LIMIT 1 │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

To show the schema of `system.views`, use `DESCRIBE system.views`:

```sql
DESCRIBE system.views;

╭────────────────────────────────────────────────────────────────────────────────╮
│    Field    │       Type      │  Null  │            Default           │  Extra │
│    String   │      String     │ String │            String            │ String │
├─────────────┼─────────────────┼────────┼──────────────────────────────┼────────┤
│ catalog     │ VARCHAR         │ NO     │ ''                           │        │
│ database    │ VARCHAR         │ NO     │ ''                           │        │
│ database_id │ BIGINT UNSIGNED │ NO     │ 0                            │        │
│ name        │ VARCHAR         │ NO     │ ''                           │        │
│ table_id    │ BIGINT UNSIGNED │ NO     │ 0                            │        │
│ engine      │ VARCHAR         │ NO     │ ''                           │        │
│ engine_full │ VARCHAR         │ NO     │ ''                           │        │
│ created_on  │ TIMESTAMP       │ NO     │ '1970-01-01 00:00:00.000000' │        │
│ dropped_on  │ TIMESTAMP       │ YES    │ NULL                         │        │
│ updated_on  │ TIMESTAMP       │ NO     │ '1970-01-01 00:00:00.000000' │        │
│ owner       │ VARCHAR         │ YES    │ NULL                         │        │
│ comment     │ VARCHAR         │ NO     │ ''                           │        │
│ view_query  │ VARCHAR         │ NO     │ ''                           │        │
╰────────────────────────────────────────────────────────────────────────────────╯
```