---
title: system.virtual_columns
summary: Contains information about the created virtual columns in the system.
---

# system.virtual_columns

> **Note:**
>
> Introduced or updated in v1.2.832.

Contains information about the created virtual columns in the system.

See also: [SHOW VIRTUAL COLUMNS](/tidb-cloud-lake/sql/show-virtual-columns.md)

Virtual columns are enabled by default starting from v1.2.832.

```sql
SELECT * FROM system.virtual_columns;

╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ database │  table │ source_column │ virtual_column_id │ virtual_column_name │ virtual_column_type │
│  String  │ String │     String    │       UInt32      │        String       │        String       │
├──────────┼────────┼───────────────┼───────────────────┼─────────────────────┼─────────────────────┤
│ default  │ test   │ val           │        3000000000 │ ['id']              │ UInt64              │
│ default  │ test   │ val           │        3000000001 │ ['name']            │ String              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```
