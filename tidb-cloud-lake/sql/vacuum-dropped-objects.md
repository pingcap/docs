---
title: VACUUM DROPPED OBJECTS
summary: Permanently removes eligible dropped objects and reclaims their storage and metadata.
aliases: ['/tidbcloudlake/vacuum-drop-table/','/tidbcloudlake/vacuum-drop-table-sql/']
---

# VACUUM DROPPED OBJECTS

Permanently removes eligible dropped objects and reclaims their storage and metadata. This includes dropped tables and, when scanning all databases, dropped databases. Dropped view metadata is also cleaned up. Objects that have been vacuumed cannot be recovered with `UNDROP`.

To list dropped tables in a database, use [SHOW DROP TABLES](/tidb-cloud-lake/sql/show-drop-tables.md). To clean history from an active table, use [VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table.md).

## Syntax

```sql
VACUUM DROPPED OBJECTS [FROM <database>]
```

| Parameter | Description |
|-----------|-------------|
| `FROM <database>` | Restricts cleanup to the specified database in the current catalog. If omitted, scans all databases in the current catalog, including dropped databases. |

With `FROM`, the command requires `SUPER` access to the database. Without `FROM`, it requires global `SUPER` privilege.

The command does not return a result set.

## Retention

Dropped objects become eligible for cleanup after the retention period configured by `data_retention_time_in_days` (1 day by default). Removing storage and metadata is permanent.

```sql
SET data_retention_time_in_days = 2;
SHOW SETTINGS LIKE 'data_retention_time_in_days';
```

## Examples

Clean up eligible dropped objects from a specific database:

```sql
VACUUM DROPPED OBJECTS FROM default;
```

Clean up eligible dropped objects across all databases in the current catalog:

```sql
VACUUM DROPPED OBJECTS;
```
