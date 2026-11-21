---
title: SHOW MATERIALIZED VIEW LOGS | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW MATERIALIZED VIEW LOGS for the TiDB database.
---

# SHOW MATERIALIZED VIEW LOGS

The `SHOW MATERIALIZED VIEW LOGS` statement shows a list of materialized view logs in a database.

<!-- TODO: Confirm the introduction version, output columns, and required privileges. Source: pingcap/tidb#72409. -->

## Synopsis

```ebnf+diagram
ShowMaterializedViewLogsStmt ::=
    'SHOW' 'MATERIALIZED' 'VIEW' 'LOGS' ShowDatabaseNameOpt ShowLikeOrWhereOpt

ShowDatabaseNameOpt ::=
    ( ( 'FROM' | 'IN' ) DBName )?

ShowLikeOrWhereOpt ::=
    ( 'LIKE' SimpleExpr | 'WHERE' Expression )?
```

The database clause and filter clause are optional. Specify the database name as an identifier, not a string literal. `LIKE` and `WHERE` are mutually exclusive.

## Examples

List materialized view logs, optionally specifying a database and filter:

```sql
SHOW MATERIALIZED VIEW LOGS;
SHOW MATERIALIZED VIEW LOGS FROM test;
SHOW MATERIALIZED VIEW LOGS IN test LIKE '$mlog$%';
```

## See also

- [Materialized Views](/materialized-views.md)
- [`CREATE MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-create-materialized-view-log.md)
- [`SHOW CREATE MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-show-create-materialized-view-log.md)
- [`SHOW MATERIALIZED VIEW LOG WAIT_PURGE`](/sql-statements/sql-statement-show-materialized-view-log-wait-purge.md)
