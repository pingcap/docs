---
title: system.databases_with_history
summary: Records all databases, including active and dropped ones. It shows each database's catalog, name, unique ID, owner (if specified), and the deletion timestamp (NULL if still active).
---

> **Note:**
>
> Introduced in v1.1.658.

Records all databases, including active and dropped ones. It shows each database's catalog, name, unique ID, owner (if specified), and the deletion timestamp (NULL if still active). 

See also: [SHOW DROP DATABASES](/tidb-cloud-lake/sql/show-drop-databases.md)

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