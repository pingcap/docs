---
title: SHOW DROP DATABASES
summary: 削除されたデータベースがある場合、その削除タイムスタンプとともにすべてのデータベースを一覧表示し、削除済みデータベースとその詳細を確認できるようにします。
---

# SHOW DROP DATABASES

削除されたデータベースがある場合、その削除タイムスタンプとともにすべてのデータベースを一覧表示し、削除済みデータベースとその詳細を確認できるようにします。

- 削除されたデータベースは、データ保持期間内にある場合にのみ取得できます。
- `root` などの admin ユーザーを使用することを推奨します。{{{ .lake }}} を使用している場合は、`account_admin` ロールを持つユーザーを使用して削除済みデータベースを照会してください。

関連情報: [system.databases_with_history](/tidb-cloud-lake/sql/system-databases-with-history.md)

## 構文 {#syntax}

```sql
SHOW DROP DATABASES
    [ FROM <catalog> ]
    [ LIKE '<pattern>' | WHERE <expr> ]
```

## 例 {#examples}

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