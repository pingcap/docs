---
title: ALTER MATERIALIZED VIEW | TiDB SQL Statement Reference
summary: Learn how to use ALTER MATERIALIZED VIEW to modify a materialized view in TiDB.
---

# ALTER MATERIALIZED VIEW

The `ALTER MATERIALIZED VIEW` statement modifies the comment, refresh schedule, or attributes of a materialized view. You can specify multiple actions in one statement by separating them with commas.

## Synopsis

```ebnf+diagram
AlterMaterializedViewStmt ::=
    'ALTER' 'MATERIALIZED' 'VIEW' TableName AlterMaterializedViewActionList

AlterMaterializedViewActionList ::=
    AlterMaterializedViewAction ( ',' AlterMaterializedViewAction )*

AlterMaterializedViewAction ::=
    'COMMENT' EqOpt stringLit
|   'REFRESH' MViewStartWithOrNextOpt
|   'ATTRIBUTES' EqOpt stringLit

MViewStartWithOrNextOpt ::=
    MViewStartWithOrNext?

MViewStartWithOrNext ::=
    'START' 'WITH' Expression 'NEXT' Expression
|   'NEXT' Expression
```

The `START WITH` and `NEXT` expressions must return `DATETIME` or `TIMESTAMP` values.

## Examples

Change the comment of a materialized view:

```sql
ALTER MATERIALIZED VIEW mv COMMENT = 'updated comment';
```

Change the refresh schedule:

```sql
ALTER MATERIALIZED VIEW mv
    REFRESH START WITH NOW() NEXT DATE_ADD(NOW(), INTERVAL 1 HOUR);
```

Change multiple properties in one statement:

```sql
ALTER MATERIALIZED VIEW mv
    COMMENT = 'updated comment',
    REFRESH NEXT DATE_ADD(NOW(), INTERVAL 1 HOUR),
    ATTRIBUTES = 'updated attributes';
```

## See also

- [Materialized Views](/materialized-views.md)
- [`CREATE MATERIALIZED VIEW`](/sql-statements/sql-statement-create-materialized-view.md)
- [`DROP MATERIALIZED VIEW`](/sql-statements/sql-statement-drop-materialized-view.md)
