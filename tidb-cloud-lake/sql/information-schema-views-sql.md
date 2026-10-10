---
title: information_schema.views
summary: すべてのビューのメタデータ情報を提供します。
---

# information_schema.views

すべてのビューのメタデータ情報を提供します。

関連情報:

- [SHOW VIEWS](/tidb-cloud-lake/sql/show-views.md)

```sql
DESCRIBE information_schema.views;

╭───────────────────────────────────────────────────────────────────────────╮
│            Field           │       Type       │  Null  │ Default │  Extra │
│           String           │      String      │ String │  String │ String │
├────────────────────────────┼──────────────────┼────────┼─────────┼────────┤
│ table_catalog              │ VARCHAR          │ NO     │ ''      │        │
│ table_schema               │ VARCHAR          │ NO     │ ''      │        │
│ table_name                 │ VARCHAR          │ NO     │ ''      │        │
│ view_definition            │ VARCHAR          │ NO     │ ''      │        │
│ check_option               │ VARCHAR          │ NO     │ ''      │        │
│ is_updatable               │ TINYINT UNSIGNED │ NO     │ 0       │        │
│ is_insertable_into         │ BOOLEAN          │ NO     │ false   │        │
│ is_trigger_updatable       │ TINYINT UNSIGNED │ NO     │ 0       │        │
│ is_trigger_deletable       │ TINYINT UNSIGNED │ NO     │ 0       │        │
│ is_trigger_insertable_into │ TINYINT UNSIGNED │ NO     │ 0       │        │
╰───────────────────────────────────────────────────────────────────────────╯
```