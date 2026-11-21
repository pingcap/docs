---
title: SHOW MATERIALIZED VIEWS | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW MATERIALIZED VIEWS for the TiDB database.
---

# SHOW MATERIALIZED VIEWS

The `SHOW MATERIALIZED VIEWS` statement shows a list of materialized views in a database.

<!-- TODO: Confirm the introduction version, output columns, and required privileges. Source: pingcap/tidb#72409. -->

## Synopsis

```ebnf+diagram
ShowMaterializedViewsStmt ::=
    'SHOW' 'MATERIALIZED' 'VIEWS' ShowDatabaseNameOpt ShowLikeOrWhereOpt

ShowDatabaseNameOpt ::=
    ( ( 'FROM' | 'IN' ) DBName )?

ShowLikeOrWhereOpt ::=
    ( 'LIKE' SimpleExpr | 'WHERE' Expression )?
```

The database clause and filter clause are optional. Specify the database name as an identifier, not a string literal. `LIKE` and `WHERE` are mutually exclusive.

## Examples

List materialized views, optionally specifying a database and filter:

```sql
SHOW MATERIALIZED VIEWS;
SHOW MATERIALIZED VIEWS FROM test;
SHOW MATERIALIZED VIEWS IN test LIKE 'mv%';
```

## See also

- [Materialized Views](/materialized-views.md)
- [`CREATE MATERIALIZED VIEW`](/sql-statements/sql-statement-create-materialized-view.md)
- [`SHOW CREATE MATERIALIZED VIEW`](/sql-statements/sql-statement-show-create-materialized-view.md)
- [`SHOW MATERIALIZED VIEW REMAIN_LOGS`](/sql-statements/sql-statement-show-materialized-view-remain-logs.md)
