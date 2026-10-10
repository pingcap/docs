---
title: system.virtual_columns
summary: システム内で作成された仮想カラムに関する情報を含みます。
---

# system.virtual_columns

システム内で作成された仮想カラムに関する情報を含みます。

関連情報: [SHOW VIRTUAL COLUMNS](/tidb-cloud-lake/sql/show-virtual-columns.md)

仮想カラムは v1.2.832 以降、デフォルトで有効になっています。

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