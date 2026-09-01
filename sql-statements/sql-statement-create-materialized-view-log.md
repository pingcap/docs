---
title: CREATE MATERIALIZED VIEW LOG | TiDB SQL Statement Reference
summary: Learn how to use CREATE MATERIALIZED VIEW LOG to define a materialized view log in TiDB.
---

# CREATE MATERIALIZED VIEW LOG

The `CREATE MATERIALIZED VIEW LOG` statement defines a materialized view log on a base table. You can specify table options, purge scheduling, and an accumulation alert threshold.

## Synopsis

```ebnf+diagram
CreateMaterializedViewLogStmt ::=
    'CREATE' 'MATERIALIZED' 'VIEW' 'LOG' 'ON' TableName '(' ColumnList ')' MLogCreateOptionListOpt MLogPurgeClauseOpt MLogAccumulationAlertClauseOpt

MLogCreateOptionListOpt ::=
    MLogCreateOptionList?

MLogCreateOptionList ::=
    MLogCreateOption+

MLogCreateOption ::=
    'SHARD_ROW_ID_BITS' EqOpt LengthNum
|   'PRE_SPLIT_REGIONS' EqOpt LengthNum

MLogPurgeClauseOpt ::=
    MLogPurgeClause?

MLogPurgeClause ::=
    'PURGE' 'IMMEDIATE'
|   'PURGE' MLogStartWithOpt 'NEXT' Expression

MLogStartWithOpt ::=
    ( 'START' 'WITH' Expression )?

MLogAccumulationAlertClauseOpt ::=
    ( 'ALERT' 'ROWS' SignedNum )?
```

The `START WITH` and `NEXT` expressions must return `DATETIME` or `TIMESTAMP` values.

The clauses in `CREATE MATERIALIZED VIEW LOG` must appear in the following order:

1. The base table name and column list.
2. Table options, if any.
3. The `PURGE` clause, if any.
4. The `ALERT ROWS` clause, if any.

## Examples

Create a materialized view log with immediate purging and an accumulation alert:

```sql
CREATE MATERIALIZED VIEW LOG ON t (a, b)
    PURGE IMMEDIATE
    ALERT ROWS 10;
```

Create a materialized view log with scheduled purging:

```sql
CREATE MATERIALIZED VIEW LOG ON t (a)
    PURGE NEXT DATE_ADD(NOW(), INTERVAL 1 HOUR);
```

## See also

- [Materialized Views](/materialized-views.md)
- [`ALTER MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-alter-materialized-view-log.md)
- [`DROP MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-drop-materialized-view-log.md)
