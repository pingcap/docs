---
title: VACUUM TABLES
summary: Reclaims storage by running VACUUM TABLE cleanup on writable FUSE tables in one database or across databases in the current catalog.
---

# VACUUM TABLES

Reclaims storage by running [`VACUUM TABLE`](/tidb-cloud-lake/sql/vacuum-table.md) cleanup on writable FUSE tables in one database or across databases in the current catalog. It preserves current table data and follows the same retention and snapshot-tag protection rules as single-table cleanup.

## Syntax

```sql
VACUUM TABLES [FROM <database>]
```

| Scope | Behavior | Required privilege |
|-------|----------|--------------------|
| `FROM <database>` | Cleans eligible tables in the specified database. | `SUPER` access to that database |
| No `FROM` clause | Cleans eligible tables in all non-system databases in the current catalog, not just the current database. | Global `SUPER` |

Non-FUSE tables and read-only tables are skipped. Ordinary per-table cleanup errors are logged and processing continues with other tables. Cancellation stops the operation; errors listing databases or tables can also stop it. Completion does not guarantee that every table was cleaned successfully.

The command does not return a result set. It does not clean dropped objects or temporary files; use [`VACUUM ALL`](/tidb-cloud-lake/sql/vacuum-all.md) to include those operations.

## Examples

```sql
VACUUM TABLES FROM default;
```

To clean eligible tables across all non-system databases in the current catalog:

```sql
VACUUM TABLES;
```
