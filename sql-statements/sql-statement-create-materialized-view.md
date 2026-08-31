---
title: CREATE MATERIALIZED VIEW | TiDB SQL Statement Reference
summary: Learn how to use CREATE MATERIALIZED VIEW to define a materialized view in TiDB.
---

# CREATE MATERIALIZED VIEW

The `CREATE MATERIALIZED VIEW` statement defines a materialized view from a `SELECT` statement. You can specify table options, refresh scheduling, and attributes for the materialized view.

## Synopsis

```ebnf+diagram
CreateMaterializedViewStmt ::=
    'CREATE' 'MATERIALIZED' 'VIEW' TableName '(' ColumnList ')' MViewTableOptionListOpt MViewRefreshClauseOpt MViewAttributesOpt 'AS' CreateViewSelectOpt

MViewTableOptionListOpt ::=
    MViewTableOptionList?

MViewTableOptionList ::=
    MViewTableOption+

MViewTableOption ::=
    'COMMENT' EqOpt stringLit
|   'SHARD_ROW_ID_BITS' EqOpt LengthNum
|   'PRE_SPLIT_REGIONS' EqOpt LengthNum

MViewRefreshClauseOpt ::=
    MViewRefreshClause?

MViewRefreshClause ::=
    'REFRESH' 'FAST' MViewStartWithOrNextOpt

MViewStartWithOrNextOpt ::=
    MViewStartWithOrNext?

MViewStartWithOrNext ::=
    'START' 'WITH' Expression 'NEXT' Expression
|   'NEXT' Expression

MViewAttributesOpt ::=
    ( 'ATTRIBUTES' EqOpt stringLit )?
```

The clauses in `CREATE MATERIALIZED VIEW` must appear in the following order:

1. The materialized view name and column list.
2. Table options, if any.
3. The `REFRESH` clause, if any.
4. The `ATTRIBUTES` clause, if any.
5. The `AS` clause and the `SELECT` statement.

## Examples

Create a materialized view with a query:

```sql
CREATE MATERIALIZED VIEW mv (a) AS SELECT 1;
```

Create a materialized view with table options, refresh scheduling, and attributes:

```sql
CREATE MATERIALIZED VIEW mv (a)
    COMMENT = 'example'
    SHARD_ROW_ID_BITS = 2
    PRE_SPLIT_REGIONS = 3
    REFRESH FAST NEXT 300
    ATTRIBUTES = 'example'
    AS SELECT 1;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`ALTER MATERIALIZED VIEW`](/sql-statements/sql-statement-alter-materialized-view.md)
- [`DROP MATERIALIZED VIEW`](/sql-statements/sql-statement-drop-materialized-view.md)
