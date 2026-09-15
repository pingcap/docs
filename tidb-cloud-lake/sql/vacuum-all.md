---
title: VACUUM ALL
summary: Runs VACUUM TABLES, VACUUM DROPPED OBJECTS, and VACUUM TEMPORARY FILES in order to reclaim storage.
---

# VACUUM ALL

`VACUUM ALL` cleans table history, dropped objects, and temporary files. `VACUUM ALL` runs the following cleanup operations in order:

1. [VACUUM TABLES](/tidb-cloud-lake/sql/vacuum-tables.md): Cleans eligible history from writable FUSE tables across non-system databases in the current catalog.
2. [VACUUM DROPPED OBJECTS](/tidb-cloud-lake/sql/vacuum-dropped-objects.md): Cleans eligible dropped objects across databases in the current catalog, including dropped databases.
3. [VACUUM TEMPORARY FILES](/tidb-cloud-lake/sql/vacuum-temporary-files.md): Cleans the tenant's temporary spill files and inactive temporary-table sessions using the default retention and no explicit limit.

Each step follows its own retention and protection rules. Current data in active tables is preserved; cleaned history and dropped objects cannot be recovered. Temporary spill-file retention is separate from `data_retention_time_in_days`.

## Syntax

```sql
VACUUM ALL
```

Requires global `SUPER` privilege. There is no database filter or command option. The command does not return a result set.

A failure that propagates from one step stops execution before the following steps. Per-table errors handled by batch cleanup retain the behavior described in [VACUUM TABLES](09-vacuum-tables.md). Cleanup already completed is not rolled back.

## Example

```sql
VACUUM ALL;
```
