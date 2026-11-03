---
title: Materialized Views
summary: Learn what materialized views are in TiDB, when to use them, and where the creation, refresh, limitation, and compatibility details belong.
---

# Materialized Views

TiDB materialized views store the result of a query in a reusable object so you can avoid recomputing the same result repeatedly. This page collects the core concept, usage flow, and limitations for the feature.

## Usage scenarios

Materialized views are intended for workloads that repeatedly read the same query result.

- Reuse expensive analytical query results.
- Reduce repeated computation for read-heavy workloads.
- Provide a stable result set for downstream consumers that do not need to rerun the base query each time.

## Prerequisites

- To create a materialized view or materialized view log, set [`tidb_mview_enable`](/system-variables.md#tidb_mview_enable) to `ON`. This variable is `OFF` by default.
- <!-- TODO: confirm the minimum TiDB version. -->
- <!-- TODO: confirm whether the feature depends on specific storage engines or cluster settings. -->

## How it works

TiDB materialized views are backed by stored data derived from a query. This page covers how to create, refresh, query, and manage materialized views.

## Create and manage materialized views

### Create a materialized view

For the syntax of this statement, see [`CREATE MATERIALIZED VIEW`](/sql-statements/sql-statement-create-materialized-view.md).

### Create a materialized view log

For the syntax of this statement, see [`CREATE MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-create-materialized-view-log.md).

### Control materialized view maintenance

TiDB uses an internal maintenance session to build a materialized view. You can control the resources and storage engines used by this session with the following system variables:

- [`tidb_mview_maintain_mem_quota`](/system-variables.md#tidb_mview_maintain_mem_quota): Sets the memory quota for the materialized view maintenance session.
- [`tidb_mview_maintain_isolation_read_engines`](/system-variables.md#tidb_mview_maintain_isolation_read_engines): Specifies the storage engines that the maintenance session can use to read data.
- [`tidb_mview_maintain_import_threads`](/system-variables.md#tidb_mview_maintain_import_threads): Sets the thread count for the `IMPORT INTO` operation used by the initial materialized view build. A value of `0` means that TiDB does not set an explicit thread count.
- [`tidb_mview_maintain_import_disk_quota`](/system-variables.md#tidb_mview_maintain_import_disk_quota): Sets the disk quota for the `IMPORT INTO` operation used by the initial materialized view build. An empty value means that TiDB does not set an explicit disk quota.

When you submit `CREATE MATERIALIZED VIEW`, TiDB records the current values of these variables in the DDL job and uses them for the initial build.

### Refresh a materialized view

Use [`REFRESH MATERIALIZED VIEW`](/sql-statements/sql-statement-refresh-materialized-view.md) to refresh a materialized view manually. You can use `FAST` refresh to apply changes from materialized view logs, or `COMPLETE` refresh to recompute the complete result of the materialized view query.

`COMPLETE` refresh requires one of the following methods. Although `DELTA APPLY` only changes rows that differ, it is a complete refresh method because TiDB recomputes the full materialized view query before applying the differences.

| Method | How it refreshes the materialized view | Transaction behavior |
| --- | --- | --- |
| `COMPLETE IN PLACE` | Deletes all existing rows from the materialized view and inserts the complete recomputed result. | Runs the delete and insert operations in one transaction. |
| `COMPLETE DELTA APPLY` | Recomputes the complete result, compares it with the current materialized view by its grouping keys, and applies only inserted, deleted, and changed rows. The materialized view must have an explicit `PRIMARY KEY` or `UNIQUE KEY` so that TiDB can uniquely locate existing rows. | Runs the comparison and row changes in one transaction. |
| `COMPLETE OUT OF PLACE` | Creates a shadow table, builds the complete recomputed result in that table, and then switches the materialized view to the replacement table. | Does not run as a single transaction. The existing materialized view remains available while TiDB builds the shadow table. If the build fails before cutover, the existing materialized view is not changed. |

Use `DRY RUN` to view the planned refresh steps without refreshing the materialized view. Use `WITH PROFILE` to execute the refresh and return step-level runtime information. To cancel a running refresh, use [`CANCEL MATERIALIZED VIEW REFRESH JOB`](/sql-statements/sql-statement-cancel-materialized-view-refresh-job.md) with the job ID in [`mysql.tidb_mview_refresh_hist`](/mysql-schema/mysql-schema-tidb-mview-refresh-hist.md).

### Query a materialized view

This section will describe how queries resolve to the stored result and any optimizer behavior. <!-- TODO: fill in from the spec. -->

### Alter a materialized view

For the syntax of this statement, see [`ALTER MATERIALIZED VIEW`](/sql-statements/sql-statement-alter-materialized-view.md).

### Alter a materialized view log

For the syntax of this statement, see [`ALTER MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-alter-materialized-view-log.md).

### Purge a materialized view log

To manually purge a materialized view log, use [`PURGE MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-purge-materialized-view-log.md). To cancel a purge job, use [`CANCEL MATERIALIZED VIEW LOG PURGE JOB`](/sql-statements/sql-statement-cancel-materialized-view-log-purge-job.md).

#### Purge throttling

TiDB uses adaptive throttling to spread materialized view log purge work across an available time window. Before deleting rows, TiDB counts the rows eligible for purge and calculates a purge deadline. For a scheduled purge, the deadline does not extend beyond the next scheduled run. For a manually triggered purge, TiDB uses an internal bounded time window, shortened when an earlier next scheduled run exists.

TiDB uses the following calculation to determine the target delete rate:

```text
delete time budget = time until deadline * tidb_mlog_purge_rate_budget_ratio
target delete rate = max(pending rows / delete time budget, tidb_mlog_purge_min_rate)
```

The target delete rate is measured in rows per second. TiDB deletes rows in batches and waits between batches when deletion has progressed ahead of the target rate. This keeps the average delete rate close to the calculated target.

For example, assume that 120,000 rows are pending, there are 60 seconds until the deadline, `tidb_mlog_purge_rate_budget_ratio` is `0.5`, and `tidb_mlog_purge_min_rate` is `2000`. TiDB uses 30 seconds as the delete time budget and sets the target delete rate to 4,000 rows per second. If only 20,000 rows are pending under the same settings, the calculated rate is about 667 rows per second, so TiDB uses the 2,000 rows-per-second minimum target instead.

> **Note:**
>
> Adaptive throttling is best effort. TiDB uses a preliminary TiFlash query to count pending rows and calculate the plan. If TiDB cannot obtain the pending-row statistics, throttling configuration, or purge deadline, it continues with normal unthrottled batched deletion instead of failing the purge.

You can configure materialized view log purge jobs using the following system variables:

- [`tidb_mlog_purge_batch_size`](/system-variables.md#tidb_mlog_purge_batch_size): Sets the maximum number of rows deleted in each purge batch.
- [`tidb_mlog_purge_min_rate`](/system-variables.md#tidb_mlog_purge_min_rate): Sets the lower bound of the adaptive purge target delete rate.
- [`tidb_mlog_purge_rate_budget_ratio`](/system-variables.md#tidb_mlog_purge_rate_budget_ratio): Sets the fraction of the available time before the purge deadline that TiDB targets for deletion.
- [`tidb_mlog_purge_delete_tiflash_threads`](/system-variables.md#tidb_mlog_purge_delete_tiflash_threads): Sets the TiFlash thread count used by purge `DELETE` statements.
- [`tidb_mlog_log_slow_purge`](/system-variables.md#tidb_mlog_log_slow_purge): Controls whether TiDB records purge statements in the slow query log.

### Drop a materialized view

For the syntax of these statements, see [`DROP MATERIALIZED VIEW`](/sql-statements/sql-statement-drop-materialized-view.md) and [`DROP MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-drop-materialized-view-log.md).

## System tables

TiDB stores materialized view maintenance metadata in the `mysql` schema. The following tables are created for materialized view and materialized view log maintenance:

- `mysql.tidb_mview_refresh_info`: Stores the current refresh scheduling information for each materialized view. This table is used internally by the automatic refresh scheduler.
- `mysql.tidb_mlog_purge_info`: Stores the current purge scheduling information for each materialized view log. This table is used internally by the automatic purge scheduler.
- [`mysql.tidb_mview_refresh_alert`](/mysql-schema/mysql-schema-tidb-mview-refresh-alert.md): Stores the current refresh alert level for each materialized view.
- [`mysql.tidb_mview_refresh_hist`](/mysql-schema/mysql-schema-tidb-mview-refresh-hist.md): Stores materialized view refresh history for user queries.
- [`mysql.tidb_mlog_purge_hist`](/mysql-schema/mysql-schema-tidb-mlog-purge-hist.md): Stores materialized view log purge history for user queries.

The `_info` tables are internal maintenance metadata tables. Do not modify TiDB system tables directly.

## Limitations

- <!-- TODO: list unsupported DDL, DML, replication, or optimizer cases from the spec. -->
- <!-- TODO: add size, freshness, or compatibility limits if they exist. -->

## Compatibility

- <!-- TODO: describe MySQL compatibility gaps or version-specific behavior. -->
- <!-- TODO: describe behavior differences across TiDB versions or storage layouts. -->

## See also

- [Views](/views.md)
