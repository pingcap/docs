---
title: Data Purge and Recycle
summary: In {{{ .lake }}}, data is not immediately deleted when you run DROP, TRUNCATE, or DELETE commands. This enables {{{ .lake }}}'s time travel feature, allowing you to access previous states of your data. However, this approach means that storage space is not automatically freed up after these operations.
---

# Data Purge and Recycle

This document describes how to reclaim storage space in {{{ .lake }}} after deleting rows or dropping tables. It also explains how to manage temporary spill files and inactive temporary-table sessions.

## Overview

Deleting rows or dropping a table does not necessarily release its storage immediately. {{{ .lake }}} retains historical data and dropped objects for recovery. `VACUUM` reclaims storage once data becomes eligible for cleanup. Cleaned history and dropped objects cannot be recovered.

## Choose a Cleanup Scope

| Command | Cleanup scope | Effect |
|---------|---------------|--------|
| [VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table.md) | One writable FUSE table | Removes eligible history while preserving the table and current data. |
| [VACUUM TABLES](/tidb-cloud-lake/sql/vacuum-tables.md) | Writable FUSE tables in a specified database, or all non-system databases in the current catalog | Performs the same historical cleanup in bulk. |
| [VACUUM DROPPED OBJECTS](/sql/sql-commands/ddl/table/vacuum-dropped-objects) | Dropped objects in a specified database, or all databases in the current catalog, including dropped databases | Removes eligible dropped objects, their storage, and their metadata. |
| [VACUUM TEMPORARY FILES](/sql/sql-commands/administration-cmds/vacuum-temp-files) | Tenant temporary spill files and inactive temporary-table sessions | Cleans temporary storage. |
| [VACUUM ALL](/sql/sql-commands/administration-cmds/vacuum-all) | Table history, dropped objects, then temporary files | Runs the three cleanup steps in order using their respective retention rules. |

Single-table cleanup requires `SUPER` access to the table. Database-scoped batch or dropped-object cleanup requires `SUPER` access to that database. Batch table and dropped-object cleanup without FROM, VACUUM ALL, and temporary-file cleanup require global `SUPER` privilege.

Batch table cleanup skips non-FUSE and read-only tables. Ordinary per-table failures are logged and other tables are processed; cancellation and errors listing databases or tables can stop the operation. These commands do not return result sets.

## Clean Table History

```sql
VACUUM TABLE default.my_table;
```

Compaction combines small blocks and segments. To compact first and then reclaim eligible historical storage:

```sql
OPTIMIZE TABLE default.my_table COMPACT;
VACUUM TABLE default.my_table;
```

For batch cleanup:

```sql
-- One database
VACUUM TABLES FROM default;

-- All non-system databases in the current catalog
VACUUM TABLES;
```

## Clean Dropped Objects

```sql
-- One database
VACUUM DROPPED OBJECTS FROM default;

-- All databases in the current catalog, including dropped databases
VACUUM DROPPED OBJECTS;
```

This removes eligible dropped objects and their metadata as well as storage. They can no longer be recovered with `UNDROP`.

## Clean Temporary Files or Run All Steps

```sql
VACUUM TEMPORARY FILES;
```

To run table-history, dropped-object, and temporary-file cleanup in sequence:

```sql
VACUUM ALL;
```

A failure propagated by a step prevents later steps from running. Cleanup already completed is not rolled back.

## Retention and Protection

For table history and dropped objects, use `data_retention_time_in_days` (1 day by default). For example, set a 2-day retention period for the current session:

```sql
SET data_retention_time_in_days = 2;
SHOW SETTINGS LIKE 'data_retention_time_in_days';
```

Active-table cleanup preserves snapshots and data referenced by unexpired snapshot tags, including tags with no expiration. Expired tags no longer protect history; VACUUM attempts to remove them without aborting cleanup if tag deletion fails.

Temporary spill files have a separate retention period of 3 days by default. Override it with RETAIN; this option does not set the lifetime of temporary-table sessions:

```sql
VACUUM TEMPORARY FILES RETAIN 2 DAYS;
```
