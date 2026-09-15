---
title: system.databases_with_history
summary: 记录所有数据库，包括活动数据库和已删除的数据库。它显示每个数据库的 catalog、名称、唯一 ID、owner（如果已指定）以及删除时间戳（如果仍处于活动状态则为 NULL）。
---

# system.databases_with_history

> **注意：**
>
> 于 v1.1.658 引入。

记录所有数据库，包括活动数据库和已删除的数据库。它显示每个数据库的 catalog、名称、唯一 ID、owner（如果已指定）以及删除时间戳（如果仍处于活动状态则为 NULL）。

另请参阅：[SHOW DROP DATABASES](/tidb-cloud-lake/sql/show-drop-databases.md)

```sql
SELECT * FROM system.databases_with_history;

┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ catalog │        name        │     database_id     │       owner      │         dropped_on         │
├─────────┼────────────────────┼─────────────────────┼──────────────────┼────────────────────────────┤
│ default │ system             │ 4611686018427387905 │ NULL             │ NULL                       │
│ default │ information_schema │ 4611686018427387906 │ NULL             │ NULL                       │
│ default │ default            │                   1 │ NULL             │ NULL                       │
│ default │ my_db              │                 114 │ NULL             │ 2024-11-15 02:44:46.207120 │
└────────────────────────────────────────────────────────────────────────────────────────────────────┘
```