---
title: system.databases
summary: 提供系统中所有数据库的元信息，包括其 catalog、名称、唯一 ID、所有者以及删除时间戳。
---

# system.databases

提供系统中所有数据库的元信息，包括其 catalog、名称、唯一 ID、所有者以及删除时间戳。

另请参阅：[SHOW DATABASES](/tidb-cloud-lake/sql/show-databases.md)

```sql title='Examples:'
SELECT * FROM system.databases;

┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ catalog │        name        │     database_id     │       owner      │      dropped_on     │
├─────────┼────────────────────┼─────────────────────┼──────────────────┼─────────────────────┤
│ default │ system             │ 4611686018427387905 │ NULL             │ NULL                │
│ default │ information_schema │ 4611686018427387906 │ NULL             │ NULL                │
│ default │ default            │                   1 │ NULL             │ NULL                │
│ default │ doc                │                2597 │ account_admin    │ NULL                │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

要查看 `system.databases` 的 schema，请使用 `DESCRIBE system.databases`：

```sql
DESCRIBE system.databases;

┌───────────────────────────────────────────────────────────┐
│    Field    │       Type      │  Null  │ Default │  Extra │
├─────────────┼─────────────────┼────────┼─────────┼────────┤
│ catalog     │ VARCHAR         │ NO     │ ''      │        │
│ name        │ VARCHAR         │ NO     │ ''      │        │
│ database_id │ BIGINT UNSIGNED │ NO     │ 0       │        │
│ owner       │ VARCHAR         │ YES    │ NULL    │        │
│ dropped_on  │ TIMESTAMP       │ YES    │ NULL    │        │
└───────────────────────────────────────────────────────────┘
```