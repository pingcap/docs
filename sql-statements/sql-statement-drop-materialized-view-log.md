---
title: DROP MATERIALIZED VIEW LOG | TiDB SQL Statement Reference
summary: Learn how to use DROP MATERIALIZED VIEW LOG to remove a materialized view log in TiDB.
---

# DROP MATERIALIZED VIEW LOG

The `DROP MATERIALIZED VIEW LOG` statement removes a materialized view log from a base table.

## Synopsis

```ebnf+diagram
DropMaterializedViewLogStmt ::=
    'DROP' 'MATERIALIZED' 'VIEW' 'LOG' IfExists 'ON' TableName

IfExists ::=
    ( 'IF' 'EXISTS' )?
```

## Examples

Drop a materialized view log:

```sql
DROP MATERIALIZED VIEW LOG ON t;
```

Drop a materialized view log only when it exists:

```sql
DROP MATERIALIZED VIEW LOG IF EXISTS ON t;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`CREATE MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-create-materialized-view-log.md)
