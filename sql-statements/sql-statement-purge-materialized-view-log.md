---
title: PURGE MATERIALIZED VIEW LOG | TiDB SQL Statement Reference
summary: Learn how to use PURGE MATERIALIZED VIEW LOG to manually purge a materialized view log in TiDB.
---

# PURGE MATERIALIZED VIEW LOG

The `PURGE MATERIALIZED VIEW LOG` statement manually purges the materialized view log on a base table.

## Synopsis

```ebnf+diagram
PurgeMaterializedViewLogStmt ::=
    'PURGE' 'MATERIALIZED' 'VIEW' 'LOG' 'ON' TableName
```

## Examples

Purge the materialized view log on `t`:

```sql
PURGE MATERIALIZED VIEW LOG ON t;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`CREATE MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-create-materialized-view-log.md)
- [`CANCEL MATERIALIZED VIEW LOG PURGE JOB`](/sql-statements/sql-statement-cancel-materialized-view-log-purge-job.md)
- [`mysql.tidb_mlog_purge_hist`](/mysql-schema/mysql-schema-tidb-mlog-purge-hist.md)
