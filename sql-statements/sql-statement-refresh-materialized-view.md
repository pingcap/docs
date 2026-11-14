---
title: REFRESH MATERIALIZED VIEW | TiDB SQL Statement Reference
summary: Learn how to manually refresh a materialized view in TiDB with fast or complete refresh methods.
---

# REFRESH MATERIALIZED VIEW

The `REFRESH MATERIALIZED VIEW` statement manually refreshes a materialized view. Use `FAST` to apply changes from materialized view logs, or use `COMPLETE` to recompute the materialized view query.

## Required privileges

To refresh a materialized view, you need the `OPERATE VIEW` privilege on the materialized view and the `SELECT` privilege on its base tables. `DRY RUN` and `WITH PROFILE` also require the `SHOW VIEW` privilege on the materialized view.

## Synopsis

```ebnf+diagram
RefreshMaterializedViewStmt ::=
    'REFRESH' 'MATERIALIZED' 'VIEW' TableName RefreshWithAsyncModeOpt ( FastRefresh | CompleteRefresh ) RefreshObserveOpt

RefreshWithAsyncModeOpt ::=
    ( 'WITH' 'ASYNC' 'MODE' )?

FastRefresh ::=
    'FAST' AsOfClauseOpt

AsOfClauseOpt ::=
    ( 'AS' 'OF' 'TIMESTAMP' Expression )?

CompleteRefresh ::=
    'COMPLETE' ( 'IN' 'PLACE' | 'DELTA' 'APPLY' | 'OUT' 'OF' 'PLACE' )

RefreshObserveOpt ::=
    ( 'DRY' 'RUN' | 'WITH' 'PROFILE' )?
```

The clauses must appear in the order shown in the syntax. `AS OF TIMESTAMP` is supported only with `FAST`. `DRY RUN` and `WITH PROFILE` are mutually exclusive.

> **Note:**
>
> `WITH ASYNC MODE` is accepted by the parser but is not supported for materialized view refreshes yet.

## Refresh methods

### FAST

`FAST` refresh applies changes recorded in materialized view logs since the last successful refresh. You can use `AS OF TIMESTAMP` to bound the refresh at a specified timestamp.

### COMPLETE IN PLACE

`COMPLETE IN PLACE` recomputes the materialized view query by deleting all current rows and inserting the complete result. TiDB performs the delete and insert operations in one transaction.

### COMPLETE DELTA APPLY

`COMPLETE DELTA APPLY` recomputes the complete materialized view query. TiDB compares the recomputed result with the current materialized view by its grouping keys and applies only the rows that need to be inserted, deleted, or updated. It is not a fast refresh because it still computes the full query result.

`COMPLETE DELTA APPLY` requires the materialized view to have an explicit `PRIMARY KEY` or `UNIQUE KEY` so that TiDB can uniquely locate existing rows. The materialized view query must have grouping keys so that TiDB can compare the current and recomputed results. The comparison and the resulting row changes run in one transaction.

### COMPLETE OUT OF PLACE

`COMPLETE OUT OF PLACE` creates a shadow table, loads the complete recomputed result into it, and then switches the materialized view to the replacement table. The original materialized view remains available until the cutover.

This method is non-transactional: building the shadow table and switching to it are not one transaction. If the shadow-table build fails before cutover, TiDB keeps the original materialized view unchanged.

## Observe a refresh

Use `DRY RUN` to build and return the planned refresh steps without executing the refresh. Use `WITH PROFILE` to execute the refresh and return the execution time and plan information for each refresh step.

## Examples

Refresh a materialized view using materialized view logs:

```sql
REFRESH MATERIALIZED VIEW mv FAST;
```

Refresh a materialized view up to a specified timestamp:

```sql
REFRESH MATERIALIZED VIEW mv FAST AS OF TIMESTAMP '2026-09-24 12:00:00';
```

Refresh a materialized view by replacing all existing rows:

```sql
REFRESH MATERIALIZED VIEW mv COMPLETE IN PLACE;
```

Refresh a materialized view by applying only the differences from the complete recomputed result:

```sql
REFRESH MATERIALIZED VIEW mv COMPLETE DELTA APPLY;
```

Refresh a materialized view by building a replacement table:

```sql
REFRESH MATERIALIZED VIEW mv COMPLETE OUT OF PLACE;
```

View the plan for a refresh without executing it:

```sql
REFRESH MATERIALIZED VIEW mv COMPLETE DELTA APPLY DRY RUN;
```

Execute a refresh and return profile information:

```sql
REFRESH MATERIALIZED VIEW mv COMPLETE OUT OF PLACE WITH PROFILE;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`CREATE MATERIALIZED VIEW`](/sql-statements/sql-statement-create-materialized-view.md)
- [`ALTER MATERIALIZED VIEW`](/sql-statements/sql-statement-alter-materialized-view.md)
- [`CANCEL MATERIALIZED VIEW REFRESH JOB`](/sql-statements/sql-statement-cancel-materialized-view-refresh-job.md)
- [`mysql.tidb_mview_refresh_hist`](/mysql-schema/mysql-schema-tidb-mview-refresh-hist.md)
