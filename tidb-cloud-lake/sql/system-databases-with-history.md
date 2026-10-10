---
title: system.databases_with_history
summary: アクティブなデータベースと削除済みのデータベースを含む、すべてのデータベースを記録します。各データベースの catalog、名前、一意の ID、owner（指定されている場合）、および削除タイムスタンプ（まだアクティブな場合は NULL）を表示します。
---

# system.databases_with_history

> **Note:**
>
> v1.1.658 で導入されました。

アクティブなデータベースと削除済みのデータベースを含む、すべてのデータベースを記録します。各データベースの catalog、名前、一意の ID、owner（指定されている場合）、および削除タイムスタンプ（まだアクティブな場合は NULL）を表示します。

関連情報: [SHOW DROP DATABASES](/tidb-cloud-lake/sql/show-drop-databases.md)

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