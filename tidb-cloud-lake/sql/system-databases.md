---
title: system.databases
summary: システム内のすべてのデータベースに関するメタデータ（catalog、名前、一意の ID、所有者、削除タイムスタンプなど）を提供します。
---

# system.databases

システム内のすべてのデータベースに関するメタデータ（catalog、名前、一意の ID、所有者、削除タイムスタンプなど）を提供します。

関連情報: [SHOW DATABASES](/tidb-cloud-lake/sql/show-databases.md)

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

`system.databases` のスキーマを表示するには、`DESCRIBE system.databases` を使用します。

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