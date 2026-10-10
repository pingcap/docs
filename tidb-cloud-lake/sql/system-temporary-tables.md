---
title: system.temporary_tables
summary: 現在のセッションに存在するすべての一時テーブルに関する情報を提供します。
---

# system.temporary_tables

現在のセッションに存在するすべての一時テーブルに関する情報を提供します。

```sql title='Examples:'
SELECT * FROM system.temporary_tables;

┌────────────────────────────────────────────────────┐
│ database │   name   │       table_id      │ engine │
├──────────┼──────────┼─────────────────────┼────────┤
│ default  │ my_table │ 4611686018427407904 │ FUSE   │
└────────────────────────────────────────────────────┘
```