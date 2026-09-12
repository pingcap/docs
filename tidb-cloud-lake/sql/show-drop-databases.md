---
title: SHOW DROP DATABASES
summary: 列出所有数据库；如果数据库已被删除，则同时显示其删除时间戳，便于用户查看已删除的数据库及其详细信息。
---

# SHOW DROP DATABASES

列出所有数据库；如果数据库已被删除，则同时显示其删除时间戳，便于用户查看已删除的数据库及其详细信息。

- 只有仍处于数据保留时间内的已删除数据库才能被找回。
- 建议使用管理员用户，例如 `root`。如果你使用的是 {{{ .lake }}}，请使用具有 `account_admin` 角色的用户来查询已删除的数据库。

另请参阅：[system.databases_with_history](/tidb-cloud-lake/sql/system-databases-with-history.md)

## 语法 {#syntax}

```sql
SHOW DROP DATABASES
    [ FROM <catalog> ]
    [ LIKE '<pattern>' | WHERE <expr> ]
```

## 示例 {#examples}

```sql
-- Create a new database named my_db
CREATE DATABASE my_db;

-- Drop the database my_db
DROP DATABASE my_db;

-- If a database has been dropped, dropped_on shows the deletion time;
-- If it is still active, dropped_on is NULL.
SHOW DROP DATABASES;

┌─────────────────────────────────────────────────────────────────────────────────┐
│ catalog │        name        │     database_id     │         dropped_on         │
├─────────┼────────────────────┼─────────────────────┼────────────────────────────┤
│ default │ default            │                   1 │ NULL                       │
│ default │ information_schema │ 4611686018427387906 │ NULL                       │
│ default │ my_db              │                 114 │ 2024-11-15 02:44:46.207120 │
│ default │ system             │ 4611686018427387905 │ NULL                       │
└─────────────────────────────────────────────────────────────────────────────────┘
```