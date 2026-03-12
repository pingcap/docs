---
title: system.databases
---

Provides metadata about all databases in the system, including their catalogs, names, unique IDs, owners, and drop timestamps.

See also: [SHOW DATABASES](../../10-sql-commands/00-ddl/00-database/show-databases.md)

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

To show the schema of `system.databases`, use `DESCRIBE system.databases`:

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