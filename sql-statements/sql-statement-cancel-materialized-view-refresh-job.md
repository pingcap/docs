---
title: CANCEL MATERIALIZED VIEW REFRESH JOB | TiDB SQL Statement Reference
summary: Learn how to cancel a running materialized view refresh job in TiDB.
---

# CANCEL MATERIALIZED VIEW REFRESH JOB

The `CANCEL MATERIALIZED VIEW REFRESH JOB` statement requests cancellation of a running materialized view refresh job.

## Required privileges

To cancel a refresh job, you need the `OPERATE VIEW` privilege on the materialized view associated with the job.

## Synopsis

```ebnf+diagram
CancelMaterializedViewJobStmt ::=
    'CANCEL' 'MATERIALIZED' 'VIEW' 'REFRESH' 'JOB' Int64Num
```

The job must be running. To find a refresh job ID, query [`mysql.tidb_mview_refresh_hist`](/mysql-schema/mysql-schema-tidb-mview-refresh-hist.md).

## Examples

Cancel the materialized view refresh job with ID `1`:

```sql
CANCEL MATERIALIZED VIEW REFRESH JOB 1;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`REFRESH MATERIALIZED VIEW`](/sql-statements/sql-statement-refresh-materialized-view.md)
- [`mysql.tidb_mview_refresh_hist`](/mysql-schema/mysql-schema-tidb-mview-refresh-hist.md)
