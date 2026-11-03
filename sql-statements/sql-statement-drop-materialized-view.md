---
title: DROP MATERIALIZED VIEW | TiDB SQL Statement Reference
summary: Learn how to use DROP MATERIALIZED VIEW to remove a materialized view in TiDB.
---

# DROP MATERIALIZED VIEW

The `DROP MATERIALIZED VIEW` statement removes a materialized view.

## Synopsis

```ebnf+diagram
DropMaterializedViewStmt ::=
    'DROP' 'MATERIALIZED' 'VIEW' TableName
|   'DROP' 'MATERIALIZED' 'VIEW' 'IF' 'EXISTS' TableName
```

## Examples

Drop a materialized view:

```sql
DROP MATERIALIZED VIEW mv;
```

Drop a materialized view only when it exists:

```sql
DROP MATERIALIZED VIEW IF EXISTS mv;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`CREATE MATERIALIZED VIEW`](/sql-statements/sql-statement-create-materialized-view.md)
