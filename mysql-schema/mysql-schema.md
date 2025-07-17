---
title: mysql Schema
summary: Learn about the TiDB system tables.
---

# `mysql` Schema

The `mysql` schema contains TiDB system tables. The design is similar to the `mysql` schema in MySQL, where tables such as `mysql.user` can be edited directly. It also contains a number of tables which are extensions to MySQL.

> **Note:**
>
> In most scenarios, it is not recommended to change the content of system tables directly using `INSERT`, `UPDATE`, or `DELETE`. Instead, use statements such as [`CREATE USER`](/sql-statements/sql-statement-create-user.md), [`ALTER USER`](/sql-statements/sql-statement-alter-user.md), [`DROP USER`](/sql-statements/sql-statement-drop-user.md), [`GRANT`](/sql-statements/sql-statement-grant-privileges.md), [`REVOKE`](/sql-statements/sql-statement-revoke-privileges.md), and [`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md) to manage users and privileges. If direct modification of system tables is unavoidable, use [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md) to make the changes take effect.

## Grant system tables

These system tables contain grant information about user accounts and their privileges:

- [`user`](/mysql-schema/mysql-schema-user.md): user accounts, global privileges, and other non-privilege columns
- `db`: database-level privileges
- `tables_priv`: table-level privileges
- `columns_priv`: column-level privileges
- `password_history`: password change history
- `default_roles`: the default roles for a user
- `global_grants`: dynamic privileges
- `global_priv`: the authentication information based on certificates
- `role_edges`: the relationship between roles

## Cluster status system tables

* The `tidb` table contains some global information about TiDB:

    * `bootstrapped`: whether the TiDB cluster has been initialized. Note that this value is read-only and cannot be modified.
    * `tidb_server_version`: the version information of TiDB when it is initialized. Note that this value is read-only and cannot be modified.
    * `system_tz`: the system time zone of TiDB.
    * `new_collation_enabled`: whether TiDB has enabled the [new framework for collations](/character-set-and-collation.md#new-framework-for-collations). Note that this value is read-only and cannot be modified.

## Server-side help system tables

Currently, the `help_topic` is NULL.

## Statistics system tables

- `stats_buckets`: the buckets of statistics
- `stats_histograms`: the histograms of statistics
- `stats_top_n`: the TopN of statistics
- `stats_meta`: the meta information of tables, such as the total number of rows and updated rows
- `stats_extended`: extended statistics, such as the order correlation between columns
- `stats_feedback`: the query feedback of statistics
- `stats_fm_sketch`: the FMSketch distribution of the histogram of the statistics column
- `stats_table_locked`: information about the locked statistics
- `stats_meta_history`: the meta information in the historical statistics
- `stats_history`: the other information in the historical statistics
- `analyze_options`: the default `analyze` options for each table
- `column_stats_usage`: the usage of column statistics
- `analyze_jobs`: the ongoing statistics collection tasks and the history task records within the last 7 days

## Execution plan-related system tables

- `bind_info`: the binding information of execution plans
- `capture_plan_baselines_blacklist`: the blocklist for the automatic binding of the execution plan

## System tables related to PLAN REPLAYER

- `plan_replayer_status`: the [`PLAN REPLAYER CAPTURE`](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#use-plan-replayer-capture) tasks registered by the user
- `plan_replayer_task`: the results of [`PLAN REPLAYER CAPTURE`](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#use-plan-replayer-capture) tasks

## GC worker system tables

> **Note:**
>
> The GC worker system tables are only applicable to TiDB Self-Managed and not available on [TiDB Cloud](https://docs.pingcap.com/tidbcloud/).

- `gc_delete_range`: the KV range to be deleted
- `gc_delete_range_done`: the deleted KV range

## System tables related to cached tables

- `table_cache_meta` stores the metadata of cached tables.

## TTL related system tables

* `tidb_ttl_table_status`: the previously executed TTL job and ongoing TTL job for all TTL tables
* `tidb_ttl_task`: the current ongoing TTL subtasks
* `tidb_ttl_job_history`: the execution history of TTL tasks in the last 90 days

## System tables related to runaway queries

* `tidb_runaway_queries`: the history records of all identified runaway queries in the past 7 days
* `tidb_runaway_watch`: the watch list of runaway queries
* `tidb_runaway_watch_done`: a watch list of deleted or expired runaway queries

## System tables related to metadata locks

* [`tidb_mdl_view`](/mysql-schema/mysql-schema-tidb-mdl-view.md): a view of metadata locks. You can use it to view the information about the currently blocked DDL statements. See also [Metadata Lock](/metadata-lock.md).
* `tidb_mdl_info`: used internally by TiDB to synchronize metadata locks across nodes.

## System tables related to DDL statements

* `tidb_ddl_history`: the history records of DDL statements
* `tidb_ddl_job`: the metadata of DDL statements that are currently being executed by TiDB
* `tidb_ddl_reorg`: the metadata of physical DDL statements (such as adding indexes) that are currently being executed by TiDB

## System tables related to TiDB Distributed eXecution Framework (DXF)

* `dist_framework_meta`: the metadata of the Distributed eXecution Framework (DXF) task scheduler
* `tidb_global_task`: the metadata of the current DXF task
* `tidb_global_task_history`: the metadata of the historical DXF tasks, including both succeeded and failed tasks
* `tidb_background_subtask`: the metadata of the current DXF subtask
* `tidb_background_subtask_history`: the metadata of the historical DXF subtasks

## System tables related to Resource Control

* `request_unit_by_group`: the history records of consumed resource units (RUs) of all resource groups

## System tables related to backup and restore

* `tidb_pitr_id_map`: the ID mapping information for point-in-time recovery (PITR) operations

## Miscellaneous system tables

<CustomContent platform="tidb">

> **Note:**
>
> The `tidb`, `expr_pushdown_blacklist`, `opt_rule_blacklist`, `table_cache_meta`, `tidb_import_jobs`, and `tidb_timers` system tables are only applicable to TiDB Self-Managed and not available on [TiDB Cloud](https://docs.pingcap.com/tidbcloud/).

- `GLOBAL_VARIABLES`: global system variable table
- `expr_pushdown_blacklist`: the blocklist for expression pushdown
- `opt_rule_blacklist`: the blocklist for logical optimization rules
- `tidb_import_jobs`: the job information of [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)
- `tidb_timers`: the metadata of internal timers
- `advisory_locks`: information related to [Locking functions](/functions-and-operators/locking-functions.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- `GLOBAL_VARIABLES`: global system variable table

</CustomContent>