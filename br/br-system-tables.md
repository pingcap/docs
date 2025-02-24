---
title: the unrecoverable system tables by snapshot restore
summary: list the unrecoverable system tables by snapshot restore
---

# the unrecoverable system tables by snapshot restore

When the cluster is in snapshot backup, BR backs up system tables as tables with the database name prefix with `__TiDB_BR_Temporary`. For example, the table `mysql.user` will be backed up as `__TiDB_BR_Temporary_mysql.user`.

When the cluster is in snapshot restore, BR at first restores tables with the database name prefix with `__TiDB_BR_Temporary`, in order to avoid conflicts with existing system tables in the cluster. Then when BR starts to restore the system tables, it inserts the data from tables with the database name prefix with `__TiDB_BR_Temporary` to the corresponding system tables through the `REPLACE INTO` SQL.

The following lists the system tables that cannot be restored by the above methods for snapshot restore.

* `mysql`
    * `advisory_locks` 
    * `analyze_jobs`
    * `analyze_options`
    * `capture_plan_baselines_blacklist`
    * `column_stats_usage`
    * `dist_framework_meta`
    * `gc_delete_range`
    * `gc_delete_range_done`
    * `global_variables`
    * `help_topic`
    * `index_advisor_results`
    * `plan_replayer_status`
    * `plan_replayer_task`
    * `request_unit_by_group`
    * `stats_buckets`
    * `stats_extended`
    * `stats_feedback`
    * `stats_fm_sketch`
    * `stats_histograms`
    * `stats_history`
    * `stats_meta`
    * `stats_meta_history`
    * `stats_table_locked`
    * `stats_top_n`
    * `table_cache_meta`
    * `tidb`
    * `tidb_background_subtask`
    * `tidb_background_subtask_history`
    * `tidb_ddl_history`
    * `tidb_ddl_job`
    * `tidb_ddl_notifier`
    * `tidb_ddl_reorg`
    * `tidb_global_task`
    * `tidb_global_task_history`
    * `tidb_import_jobs`
    * `tidb_mdl_info`
    * `tidb_mdl_view`
    * `tidb_pitr_id_map`
    * `tidb_runaway_queries`
    * `tidb_runaway_watch`
    * `tidb_runaway_watch_done`
    * `tidb_timers`
    * `tidb_ttl_job_history`
    * `tidb_ttl_table_status`
    * `tidb_ttl_task`

* `sys`
    * `schema_unused_indexes`
