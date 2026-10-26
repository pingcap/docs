---
title: SHOW MATERIALIZED VIEW LOG WAIT_PURGE | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW MATERIALIZED VIEW LOG WAIT_PURGE for the TiDB database.
---

# SHOW MATERIALIZED VIEW LOG WAIT_PURGE

The `SHOW MATERIALIZED VIEW LOG ... WAIT_PURGE` statement shows information about the log records waiting to be purged from the materialized view log on a base table.

<!-- TODO: Confirm the introduction version, output columns, and required privileges. Source: pingcap/tidb#72409. -->

## Synopsis

```ebnf+diagram
ShowMaterializedViewLogWaitPurgeStmt ::=
    'SHOW' 'MATERIALIZED' 'VIEW' 'LOG' 'ON' TableName 'WAIT_PURGE'
```

`TableName` specifies the base table name and can include a database qualifier. Both `ON` and `WAIT_PURGE` are required. This form does not accept `LIKE` or `WHERE` clauses.

## Examples

Show materialized view log records waiting to be purged:

```sql
SHOW MATERIALIZED VIEW LOG ON t WAIT_PURGE;
SHOW MATERIALIZED VIEW LOG ON test.t WAIT_PURGE;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`SHOW MATERIALIZED VIEW LOGS`](/sql-statements/sql-statement-show-materialized-view-logs.md)
- [`PURGE MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-purge-materialized-view-log.md)
