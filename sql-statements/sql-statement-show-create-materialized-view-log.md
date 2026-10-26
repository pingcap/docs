---
title: SHOW CREATE MATERIALIZED VIEW LOG | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW CREATE MATERIALIZED VIEW LOG for the TiDB database.
---

# SHOW CREATE MATERIALIZED VIEW LOG

The `SHOW CREATE MATERIALIZED VIEW LOG` statement shows the creation statement for the materialized view log on a base table.

<!-- TODO: Confirm the introduction version, output columns, and required privileges. Source: pingcap/tidb#72409. -->

## Synopsis

```ebnf+diagram
ShowCreateMaterializedViewLogStmt ::=
    'SHOW' 'CREATE' 'MATERIALIZED' 'VIEW' 'LOG' 'ON' TableName
```

The `ON` clause is required. `TableName` specifies the base table name and can include a database qualifier.

## Examples

Show the creation statement for a materialized view log, with or without a database qualifier:

```sql
SHOW CREATE MATERIALIZED VIEW LOG ON t;
SHOW CREATE MATERIALIZED VIEW LOG ON test.t;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`CREATE MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-create-materialized-view-log.md)
- [`SHOW MATERIALIZED VIEW LOGS`](/sql-statements/sql-statement-show-materialized-view-logs.md)
