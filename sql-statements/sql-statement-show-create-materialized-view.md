---
title: SHOW CREATE MATERIALIZED VIEW | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW CREATE MATERIALIZED VIEW for the TiDB database.
---

# SHOW CREATE MATERIALIZED VIEW

The `SHOW CREATE MATERIALIZED VIEW` statement shows the creation statement for a materialized view.

<!-- TODO: Confirm the introduction version, output columns, and required privileges. Source: pingcap/tidb#72409. -->

## Synopsis

```ebnf+diagram
ShowCreateMaterializedViewStmt ::=
    'SHOW' 'CREATE' 'MATERIALIZED' 'VIEW' MViewName

MViewName ::= TableName
```

`MViewName` specifies the materialized view name and can include a database qualifier.

## Examples

Show the creation statement for a materialized view, with or without a database qualifier:

```sql
SHOW CREATE MATERIALIZED VIEW mv;
SHOW CREATE MATERIALIZED VIEW test.mv;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`CREATE MATERIALIZED VIEW`](/sql-statements/sql-statement-create-materialized-view.md)
- [`SHOW MATERIALIZED VIEWS`](/sql-statements/sql-statement-show-materialized-views.md)
