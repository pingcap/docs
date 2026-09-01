---
title: ALTER MATERIALIZED VIEW LOG | TiDB SQL Statement Reference
summary: Learn how to use ALTER MATERIALIZED VIEW LOG to modify a materialized view log in TiDB.
---

# ALTER MATERIALIZED VIEW LOG

The `ALTER MATERIALIZED VIEW LOG` statement changes the purge configuration or adds columns to a materialized view log. You can specify multiple actions in one statement by separating them with commas.

## Synopsis

```ebnf+diagram
AlterMaterializedViewLogStmt ::=
    'ALTER' 'MATERIALIZED' 'VIEW' 'LOG' 'ON' TableName AlterMaterializedViewLogActionList

AlterMaterializedViewLogActionList ::=
    AlterMaterializedViewLogAction ( ',' AlterMaterializedViewLogAction )*

AlterMaterializedViewLogAction ::=
    AlterMLogPurgeClause
|   'ADD' ColumnKeywordOpt '(' ColumnList ')'

AlterMLogPurgeClause ::=
    MLogPurgeClause
|   'PURGE'

MLogPurgeClause ::=
    'PURGE' 'IMMEDIATE'
|   'PURGE' MLogStartWithOpt 'NEXT' Expression

MLogStartWithOpt ::=
    ( 'START' 'WITH' Expression )?
```

The `START WITH` and `NEXT` expressions must return `DATETIME` or `TIMESTAMP` values.

## Examples

Change the purge schedule:

```sql
ALTER MATERIALIZED VIEW LOG ON t PURGE NEXT DATE_ADD(NOW(), INTERVAL 1 HOUR);
```

Add columns to a materialized view log:

```sql
ALTER MATERIALIZED VIEW LOG ON t ADD COLUMN (b, c);
```

Specify multiple actions in one statement:

```sql
ALTER MATERIALIZED VIEW LOG ON t
    PURGE,
    ADD COLUMN (b, c);
```

## See also

- [Materialized Views](/materialized-views.md)
- [`CREATE MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-create-materialized-view-log.md)
- [`DROP MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-drop-materialized-view-log.md)
