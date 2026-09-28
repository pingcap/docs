---
title: VACUUM TABLE
summary: Permanently removes eligible historical snapshots and their unneeded segments, blocks, and related files from a FUSE table to reclaim storage.
aliases: ['/tidbcloudlake/vacuum-table-sql/']
---

# VACUUM TABLE

The `VACUUM TABLE` command permanently removes eligible historical snapshots and their unneeded segments, blocks, and related files from a FUSE table to reclaim storage. The table and its current data remain available.

See also: [VACUUM TABLES](/tidb-cloud-lake/sql/vacuum-tables.md), [VACUUM DROPPED OBJECTS](/tidb-cloud-lake/sql/vacuum-dropped-objects.md), [VACUUM ALL](/tidb-cloud-lake/sql/vacuum-all.md).

## Syntax

```sql
VACUUM TABLE [<database>.]<table>
```

If the database is omitted, the current database is used. The command operates in the current catalog and requires `SUPER` access to the table. Only writable FUSE tables are supported.

The command does not return a result set.

## Retention and Snapshot Tags

Cleanup respects `data_retention_time_in_days` (1 day by default). Historical data that has been removed cannot be queried through Time Travel or restored with Flashback.

Snapshots referenced by unexpired [snapshot tags](/tidb-cloud-lake/sql/create-snapshot-tag.md), including tags without an expiration time, and the data they reference are protected from cleanup. Expired tags no longer protect their snapshots. VACUUM attempts to remove expired tags; a failure to delete an expired tag does not stop cleanup.

Use a session setting to adjust the retention period for subsequent cleanup operations:

```sql
SET data_retention_time_in_days = 2;
SHOW SETTINGS LIKE 'data_retention_time_in_days';
```

## Examples

Create a table and change its data, then clean up eligible history:

```sql
CREATE OR REPLACE TABLE vacuum_example (id INT);
INSERT INTO vacuum_example VALUES (1), (2);
DELETE FROM vacuum_example WHERE id = 1;
VACUUM TABLE vacuum_example;
SELECT * FROM vacuum_example;
```

The current row remains available. Recently created history is retained until it becomes eligible for cleanup.

Compaction and storage reclamation are separate operations. To compact a table and then clean up eligible historical files:

```sql
OPTIMIZE TABLE vacuum_example COMPACT;
VACUUM TABLE vacuum_example;
```
