---
title: COMPARE MATERIALIZED VIEW | TiDB SQL Statement Reference
summary: An overview of the usage of COMPARE MATERIALIZED VIEW for the TiDB database.
---

# COMPARE MATERIALIZED VIEW

The `COMPARE MATERIALIZED VIEW` statement compares a materialized view with a snapshot of the result of its defining query.

> **Warning:**
>
> The comparison runs on TiDB and does not support massively parallel processing (MPP). Comparing a large materialized view can exhaust the available memory on the TiDB server and fail with an out-of-memory (OOM) error. Before comparing a large materialized view, assess its data volume and the available memory on the TiDB server.

<!-- TODO: Confirm the introduction version, comparison details, output table requirements, and required privileges. Source: pingcap/tidb#72409. -->

## Synopsis

```ebnf+diagram
CompareMaterializedViewStmt ::=
    'COMPARE' 'MATERIALIZED' 'VIEW' MViewName AsOfClause CompareMaterializedViewOutputOpt

MViewName ::= TableName

AsOfClause ::=
    'AS' 'OF' 'TIMESTAMP' Expression

CompareMaterializedViewOutputOpt ::=
    ( 'OUTPUT' 'INTO' 'TABLE' TableName )?
```

- `MViewName` specifies the materialized view name.
- `AS OF TIMESTAMP` is required and accepts a SQL expression for the snapshot timestamp.
- `OUTPUT INTO TABLE` is optional and specifies a table for the comparison output. It must appear after `AS OF TIMESTAMP`.
- Both `MViewName` and the output `TableName` can include database qualifiers.

## Examples

Compare a materialized view with a snapshot of its defining query result:

```sql
COMPARE MATERIALIZED VIEW mv AS OF TIMESTAMP '2026-01-01 00:00:00';
```

Specify a table for the comparison output:

```sql
COMPARE MATERIALIZED VIEW test.mv AS OF TIMESTAMP '2026-01-01 00:00:00'
    OUTPUT INTO TABLE test.diff;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`CREATE MATERIALIZED VIEW`](/sql-statements/sql-statement-create-materialized-view.md)
- [`REFRESH MATERIALIZED VIEW`](/sql-statements/sql-statement-refresh-materialized-view.md)
