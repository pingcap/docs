---
title: system.temporary_tables
summary: 提供当前会话中所有现有临时表的信息。
---

# system.temporary_tables

提供当前会话中所有现有临时表的信息。

```sql title='Examples:'
SELECT * FROM system.temporary_tables;

┌────────────────────────────────────────────────────┐
│ database │   name   │       table_id      │ engine │
├──────────┼──────────┼─────────────────────┼────────┤
│ default  │ my_table │ 4611686018427407904 │ FUSE   │
└────────────────────────────────────────────────────┘
```