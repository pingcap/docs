---
title: CANCEL MATERIALIZED VIEW LOG PURGE JOB | TiDB SQL Statement Reference
summary: Learn how to use CANCEL MATERIALIZED VIEW LOG PURGE JOB to cancel a materialized view log purge job in TiDB.
---

# CANCEL MATERIALIZED VIEW LOG PURGE JOB

The `CANCEL MATERIALIZED VIEW LOG PURGE JOB` statement cancels a materialized view log purge job by its ID.

## Synopsis

```ebnf+diagram
CancelMaterializedViewJobStmt ::=
    'CANCEL' 'MATERIALIZED' 'VIEW' 'LOG' 'PURGE' 'JOB' Int64Num
```

## Examples

Cancel the materialized view log purge job with ID `1`:

```sql
CANCEL MATERIALIZED VIEW LOG PURGE JOB 1;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`PURGE MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-purge-materialized-view-log.md)
- [`mysql.tidb_mlog_purge_hist`](/mysql-schema/mysql-schema-tidb-mlog-purge-hist.md)
