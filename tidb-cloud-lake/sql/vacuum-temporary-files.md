---
title: VACUUM TEMPORARY FILES
summary: Removes temporary files created by {{{ .lake }}}, such as spill files.
---

# VACUUM TEMPORARY FILES

Removes temporary spill files created during query execution and cleans up inactive temporary-table sessions for the tenant.

See also: [system.temp_files](/tidb-cloud-lake/sql/system-temp-files.md), [VACUUM ALL](/tidb-cloud-lake/sql/vacuum-all.md).

## Syntax

```sql
VACUUM TEMPORARY FILES [RETAIN <number> {SECONDS | DAYS}] [LIMIT <limit>]
```

| Parameter | Description |
|-----------|-------------|
| `RETAIN` | Retention period for temporary spill files. Defaults to 3 days. This is independent of `data_retention_time_in_days` and does not set the lifetime of temporary-table sessions. |
| `LIMIT` | Limits spill-file deletion first. The remaining allowance limits the number of inactive temporary-table sessions to clean, rather than individual files within those sessions. If omitted, no explicit limit is applied. |

Requires global `SUPER` privilege. The command does not return a result set.

## Examples

Inspect temporary files:

```sql
SELECT * FROM system.temp_files;
```

Clean up using the default retention:

```sql
VACUUM TEMPORARY FILES;
```

Retain spill files for 2 days and limit cleanup:

```sql
VACUUM TEMPORARY FILES RETAIN 2 DAYS LIMIT 1000;
```
