---
title: system.virtual_columns
summary: 包含系统中已创建的虚拟列的信息。
---

# system.virtual_columns

包含系统中已创建的虚拟列的信息。

另请参阅：[SHOW VIRTUAL COLUMNS](/tidb-cloud-lake/sql/show-virtual-columns.md)

从 v1.2.832 开始，默认启用虚拟列。

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