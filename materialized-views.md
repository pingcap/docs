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

This section will describe refresh behavior, supported refresh modes, and operational guidance. The `REFRESH` clause syntax is documented in [`CREATE MATERIALIZED VIEW`](/sql-statements/sql-statement-create-materialized-view.md) and [`ALTER MATERIALIZED VIEW`](/sql-statements/sql-statement-alter-materialized-view.md). <!-- TODO: fill in from the spec. -->

### Query a materialized view

This section will describe how queries resolve to the stored result and any optimizer behavior. <!-- TODO: fill in from the spec. -->

### Alter a materialized view

For the syntax of this statement, see [`ALTER MATERIALIZED VIEW`](/sql-statements/sql-statement-alter-materialized-view.md).

### Alter a materialized view log

For the syntax of this statement, see [`ALTER MATERIALIZED VIEW LOG`](/sql-statements/sql-statement-alter-materialized-view-log.md).

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
