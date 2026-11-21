---
title: SHOW MATERIALIZED VIEW REMAIN_LOGS | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW MATERIALIZED VIEW REMAIN_LOGS for the TiDB database.
---

# SHOW MATERIALIZED VIEW REMAIN_LOGS

The `SHOW MATERIALIZED VIEW ... REMAIN_LOGS` statement shows information about the logs remaining for a materialized view refresh.

<!-- TODO: Confirm the introduction version, output columns, and required privileges. Source: pingcap/tidb#72409. -->

## Synopsis

```ebnf+diagram
ShowMaterializedViewRemainLogsStmt ::=
    'SHOW' 'MATERIALIZED' 'VIEW' MViewName 'REMAIN_LOGS'

MViewName ::= TableName
```

`MViewName` specifies the materialized view name and can include a database qualifier. `REMAIN_LOGS` is required. This form does not accept `LIKE` or `WHERE` clauses.

## Examples

Show the remaining refresh logs for a materialized view:

```sql
SHOW MATERIALIZED VIEW mv REMAIN_LOGS;
SHOW MATERIALIZED VIEW test.mv REMAIN_LOGS;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`SHOW MATERIALIZED VIEWS`](/sql-statements/sql-statement-show-materialized-views.md)
- [`REFRESH MATERIALIZED VIEW`](/sql-statements/sql-statement-refresh-materialized-view.md)
