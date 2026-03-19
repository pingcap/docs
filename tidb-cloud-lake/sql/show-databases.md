---
title: SHOW DATABASES
summary: Shows the list of databases that exist on the instance.
---

# SHOW DATABASES

> **Note:**
>
> Introduced or updated in v1.2.290.

Shows the list of databases that exist on the instance.

See also: [system.databases](/tidb-cloud-lake/sql/system-databases.md)

## Syntax

```sql
SHOW [ FULL ] DATABASES
    [ LIKE '<pattern>' | WHERE <expr> ]
```

| Parameter | Description                                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| FULL      | Lists the results with additional information. See [Examples](#examples) for more details.                                  |
| LIKE      | Filters the results by their names using case-sensitive pattern matching.                                                   |
| WHERE     | Filters the results using an expression in the WHERE clause.                                                                |

## Examples

```sql
SHOW DATABASES;

┌──────────────────────┐
│ databases_in_default │
├──────────────────────┤
│ canada               │
│ china                │
│ default              │
│ information_schema   │
│ system               │
│ test                 │
└──────────────────────┘

SHOW FULL DATABASES;

┌───────────────────────────────────────────────────┐
│ catalog │       owner      │ databases_in_default │
├─────────┼──────────────────┼──────────────────────┤
│ default │ account_admin    │ canada               │
│ default │ account_admin    │ china                │
│ default │ NULL             │ default              │
│ default │ NULL             │ information_schema   │
│ default │ NULL             │ system               │
│ default │ account_admin    │ test                 │
└───────────────────────────────────────────────────┘
```
