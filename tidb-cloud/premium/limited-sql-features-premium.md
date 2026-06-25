---
title: Limited SQL Features on TiDB Cloud
summary: Learn about the limited SQL features on TiDB Cloud.
---

# Limited SQL features on TiDB Cloud

TiDB Cloud works with almost all workloads that TiDB supports, but there are some feature differences between TiDB Self-Managed and TiDB Cloud. This document describes the limitations of SQL features on TiDB Cloud. We are constantly filling in the feature gaps between TiDB Self-Managed and TiDB Cloud. If you require these features or capabilities in the gap, [contact us](/tidb-cloud/tidb-cloud-support.md) for a feature request.

## Statements

### Placement and range management

| Statement | TiDB Cloud Premium | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `ALTER PLACEMENT POLICY` | Not supported | Not supported [^1] |
| `ALTER RANGE` | Not supported | Not supported |
| `CREATE PLACEMENT POLICY` | Not supported | Not supported [^1] |
| `DROP PLACEMENT POLICY` | Not supported | Not supported [^1] |
| `SHOW CREATE PLACEMENT POLICY` | Not supported | Not supported [^1] |
| `SHOW PLACEMENT` | Not supported | Not supported [^1] |
| `SHOW PLACEMENT FOR` | Not supported | Not supported [^1] |
| `SHOW PLACEMENT LABELS` | Not supported | Not supported [^1] |
| `SHOW TABLE REGIONS` | Supported | Not supported [^1] |
| `SPLIT REGION` | Supported | Not supported [^1] |

### Resource groups

| Statement | TiDB Cloud Premium | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `ALTER RESOURCE GROUP` | Not supported | Not supported [^2] |
| `CALIBRATE RESOURCE` | Not supported | Not supported [^2] |
| `CREATE RESOURCE GROUP` | Not supported | Not supported [^2] |
| `DROP RESOURCE GROUP` | Not supported | Not supported [^2] |
| `SET RESOURCE GROUP` | Not supported | Not supported [^2] |
| `SHOW CREATE RESOURCE GROUP` | Not supported | Not supported [^2] |

### Others

| Statement | TiDB Cloud Premium | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `BACKUP` | Not supported | Not supported [^3] |
| `SHOW BACKUPS` | Not supported | Not supported [^3] |
| `RESTORE` | Not supported | Not supported [^3] |
| `SHOW RESTORES` | Not supported | Not supported [^3] |
| `BACKUP LOGS` | Not supported | Not supported |
| `STOP BACKUP LOGS` | Not supported | Not supported |
| `PAUSE BACKUP LOGS` | Not supported | Not supported |
| `RESUME BACKUP LOGS` | Not supported | Not supported |
| `SHOW BACKUP LOGS STATUS` | Not supported | Not supported |
| `SHOW BACKUP LOGS METADATA` | Not supported | Not supported |
| `PURGE BACKUP LOGS` | Not supported | Not supported |
| `SHOW BR JOB` | Not supported | Not supported |
| `SHOW BR JOB QUERY` | Not supported | Not supported |
| `CANCEL BR JOB` | Not supported | Not supported |
| `SHOW BACKUP META` | Not supported | Not supported |
| `RECOVER TABLE` | Not supported | Not supported |
| `ADMIN RESET TELEMETRY_ID` | Supported | Telemetry is not supported on {{{ .starter }}} or {{{ .essential }}}. |
| `ADMIN SHOW TELEMETRY` | Not supported | Not supported [^4] |
| `ADMIN SHOW SLOW` | Not supported | Not supported [^5] |
| `ADMIN PLUGINS ENABLE` | Not supported | Not supported [^8] |
| `ADMIN PLUGINS DISABLE` | Not supported | Not supported [^8] |
| `ADMIN SET BDR ROLE` | Not supported | Not supported |
| `ADMIN SHOW BDR ROLE` | Not supported | Not supported |
| `ADMIN UNSET BDR ROLE` | Not supported | Not supported |
| `ADMIN REPAIR TABLE` | Not supported | Not supported |
| `ALTER INSTANCE` | Not supported | Not supported |
| `ALTER INSTANCE RELOAD TLS` | Not supported | {{{ .starter }}} and {{{ .essential }}} automatically refresh the TLS certificate. |
| `ALTER TABLE ... ATTRIBUTES` | Not supported | Not supported |
| `CHANGE DRAINER` | Not supported | Not supported [^7] |
| `CHANGE PUMP` | Not supported | Not supported [^7] |
| `FLASHBACK CLUSTER` | Not supported | Not supported [^3] |
| `IMPORT INTO` | Supported. Blocks `IMPORT INTO` from a local file path. Blocks `IMPORT INTO` statements that use an S3 `EXTERNAL_ID`. | Not supported |
| `LOAD DATA INFILE` | Blocks `LOAD DATA LOCAL INFILE` from a local file path. | Only supports `LOAD DATA LOCAL INFILE` |
| `LOAD STATS` | Not supported | Not supported |
| `SELECT ... INTO OUTFILE` | Not supported | Not supported [^4] |
| `SET CONFIG` | Not supported | Not supported [^4] |
| `SHOW CONFIG` | Not supported | Not supported [^4] |
| `SHOW DRAINER STATUS` | Not supported | Not supported [^7] |
| `SHOW PLUGINS` | Not supported | Not supported [^8] |
| `SHOW PUMP STATUS` | Not supported | Not supported [^7] |
| `SHUTDOWN` | Not supported | Not supported [^4] |
| `PLAN REPLAYER` | Supported | Supported in a different way[^11] |
| `time_to_live` | Supported | Not supported |

## Functions and operators

| Function and operator | TiDB Cloud Premium | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `SLEEP` | No Limitation | The [`SLEEP()` function](https://docs.pingcap.com/tidbcloud/miscellaneous-functions) has a limitation wherein it can only support a maximum sleep time of 300 seconds. |

## System tables

| Database | Table | TiDB Cloud Premium | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|:-|
| `metrics_schema` | All databases | Not supported | Not supported |
| `information_schema` | `ATTRIBUTES` | Supported | Not supported [^1] |
| `information_schema` | `CLUSTER_CONFIG` | Not supported | Not supported [^4] |
| `information_schema` | `CLUSTER_HARDWARE` | Not supported | Not supported [^4] |
| `information_schema` | `CLUSTER_INFO` | Supported | Not supported [^1] |
| `information_schema` | `CLUSTER_LOAD` | Not supported | Not supported [^4] |
| `information_schema` | `CLUSTER_LOG` | Not supported | Not supported [^4] |
| `information_schema` | `CLUSTER_SLOW_QUERY` | Not supported | Not supported [^5] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY` | Supported | Not supported [^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_EVICTED` | Supported | Not supported [^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_HISTORY` | Supported | Not supported [^6] |
| `information_schema` | `CLUSTER_SYSTEMINFO` | Not supported | Not supported [^4] |
| `information_schema` | `INSPECTION_RESULT` | Not supported | Not supported [^4] |
| `information_schema` | `INSPECTION_RULES` | Not supported | Not supported [^4] |
| `information_schema` | `INSPECTION_SUMMARY` | Not supported | Not supported [^4] |
| `information_schema` | `METRICS_SUMMARY` | Not supported | Not supported [^4] |
| `information_schema` | `METRICS_SUMMARY_BY_LABEL` | Not supported | Not supported [^4] |
| `information_schema` | `METRICS_TABLES` | Not supported | Not supported [^4] |
| `information_schema` | `PLACEMENT_POLICIES` | Not supported | Not supported [^1] |
| `information_schema` | `RESOURCE_GROUPS` | Not supported | Not supported [^2] |
| `information_schema` | `SLOW_QUERY` | Not supported | Not supported [^5] |
| `information_schema` | `STATEMENTS_SUMMARY` | Supported | Not supported [^6] |
| `information_schema` | `STATEMENTS_SUMMARY_EVICTED` | Supported | Not supported [^6] |
| `information_schema` | `TIDB_HOT_REGIONS` | Not supported | Not supported [^4] |
| `information_schema` | `TIDB_HOT_REGIONS_HISTORY` | Supported | Not supported [^1] |
| `information_schema` | `TIDB_SERVERS_INFO` | Supported | Not supported [^1] |
| `information_schema` | `TIKV_REGION_PEERS` | Supported | Not supported [^1] |
| `information_schema` | `TIKV_REGION_STATUS` | Supported | Not supported [^1] |
| `information_schema` | `TIKV_STORE_STATUS` | Supported | Not supported [^1] |
| `performance_schema` | `pd_profile_allocs` | Not supported | Not supported [^4] |
| `performance_schema` | `pd_profile_block` | Not supported | Not supported [^4] |
| `performance_schema` | `pd_profile_cpu` | Not supported | Not supported [^4] |
| `performance_schema` | `pd_profile_goroutines` | Not supported | Not supported [^4] |
| `performance_schema` | `pd_profile_memory` | Not supported | Not supported [^4] |
| `performance_schema` | `pd_profile_mutex` | Not supported | Not supported [^4] |
| `performance_schema` | `tidb_profile_allocs` | Not supported | Not supported [^4] |
| `performance_schema` | `tidb_profile_block` | Not supported | Not supported [^4] |
| `performance_schema` | `tidb_profile_cpu` | Not supported | Not supported [^4] |
| `performance_schema` | `tidb_profile_goroutines` | Not supported | Not supported [^4] |
| `performance_schema` | `tidb_profile_memory` | Not supported | Not supported [^4] |
| `performance_schema` | `tidb_profile_mutex` | Not supported | Not supported [^4] |
| `performance_schema` | `tikv_profile_cpu` | Not supported | Not supported [^4] |
| `mysql` | `expr_pushdown_blacklist` | Not supported | Not supported [^4] |
| `mysql` | `gc_delete_range` | Not supported | Not supported [^4] |
| `mysql` | `gc_delete_range_done` | Not supported | Not supported [^4] |
| `mysql` | `opt_rule_blacklist` | Not supported | Not supported [^4] |
| `mysql` | `tidb` | Not supported | Not supported [^4] |

## System variables

| Variable | TiDB Cloud Premium | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `hostname` | Value hidden | Value hidden |
| `datadir` | Value hidden | Not supported [^1] |
| `ddl_slow_threshold` | Read-only | Read-only |
| `block_encryption_mode` | Read-only | Read-only |
| `max_connections` | Read-only | Read-only |
| `mpp_version` | Read-only | Read-only |
| `interactive_timeout` | No limitation | Read-only [^10] |
| `max_allowed_packet` | No limitation | Read-only [^10] |
| `plugin_dir` | Not supported | Not supported [^8] |
| `plugin_load` | Not supported | Not supported [^8] |
| `require_secure_transport` | Not supported | Read-only [^10] |
| `skip_name_resolve` | Read-only | Read-only [^10] |
| `sql_log_bin` | No limitation | Read-only [^10] |
| `tidb_adaptive_closest_read_threshold` | Not supported | Not supported |
| `tidb_allow_batch_cop` | Read-only | Read-only |
| `tidb_allow_mpp` | Read-only | Read-only |
| `tidb_analyze_skip_column_types` | No limitation | Read-only [^10] |
| `tidb_analyze_version` | Read-only | Read-only |
| `tidb_backoff_lock_fast` | Read-only | Read-only |
| `tidb_backoff_weight` | Read-only | Read-only |
| `tidb_batch_commit` | Not supported | Not supported |
| `tidb_batch_delete` | Not supported | Not supported |
| `tidb_batch_insert` | Not supported | Not supported |
| `tidb_capture_plan_baselines` | Read-only | Read-only |
| `tidb_cdc_write_source` | No limitation | Read-only [^10] |
| `tidb_check_mb4_value_in_utf8` | Not supported | Not supported [^4] |
| `tidb_cloud_storage_uri` | Not supported | Not supported |
| `tidb_config` | Not supported | Not supported [^4] |
| `tidb_constraint_check_in_place` | Read-only | Read-only |
| `tidb_constraint_check_in_place_pessimistic` | Read-only | Read-only |
| `tidb_cost_model_version` | Read-only | Read-only |
| `tidb_ddl_disk_quota` | Read-only | Read-only [^10] |
| `tidb_ddl_enable_fast_reorg` | Read-only | Read-only [^10] |
| `tidb_ddl_error_count_limit` | No limitation | Read-only [^10] |
| `tidb_ddl_flashback_concurrency` | Read-only | Read-only [^10] |
| `tidb_ddl_reorg_batch_size` | No limitation | Read-only [^10] |
| `tidb_ddl_reorg_max_write_speed` | Not supported | Not supported |
| `tidb_ddl_reorg_priority` | No limitation | Read-only [^10] |
| `tidb_ddl_reorg_worker_cnt` | No limitation | Read-only [^10] |
| `tidb_disable_txn_auto_retry` | Not supported | Not supported |
| `tidb_dml_batch_size` | Not supported | Not supported |
| `tidb_dml_type` | Not supported | Read-only [^10] |
| `tidb_enable_1pc` | No limitation | Read-only [^10] |
| `tidb_enable_analyze_snapshot` | Read-only | Read-only |
| `tidb_enable_async_commit` | No limitation | Read-only [^10] |
| `tidb_enable_async_merge_global_stats` | Read-only | Read-only |
| `tidb_enable_auto_analyze` | No limitation | Read-only [^10] |
| `tidb_enable_batch_dml` | Not supported | Not supported |
| `tidb_enable_chunk_rpc` | Read-only | Read-only |
| `tidb_enable_collect_execution_info` | Not supported | Not supported [^4] |
| `tidb_enable_column_tracking` | Not supported | Not supported |
| `tidb_enable_ddl` | Read-only | Read-only [^10] |
| `tidb_enable_dist_task` | Read-only | Read-only |
| `tidb_enable_exchange_partition` | Not supported | Not supported |
| `tidb_enable_extended_stats` | Read-only | Read-only |
| `tidb_enable_fast_analyze` | Not supported | Not supported |
| `tidb_enable_gc_aware_memory_track` | No limitation | Read-only [^10] |
| `tidb_enable_global_index` | Not supported | Not supported |
| `tidb_enable_gogc_tuner` | Read-only | Read-only [^10] |
| `tidb_enable_historical_stats` | Read-only | Read-only |
| `tidb_enable_historical_stats_for_capture` | Read-only | Read-only |
| `tidb_enable_legacy_instance_scope` | Read-only | Read-only |
| `tidb_enable_list_partition` | Not supported | Not supported |
| `tidb_enable_local_txn` | Read-only | Read-only [^10] |
| `tidb_enable_metadata_lock` | Read-only | Read-only |
| `tidb_enable_mutation_checker` | Read-only | Not supported |
| `tidb_enable_new_cost_interface` | Read-only | Read-only |
| `tidb_enable_parallel_hashagg_spill` | Read-only | Read-only |
| `tidb_enable_pipelined_window_function` | No limitation | Not supported |
| `tidb_enable_plan_replayer_capture` | Read-only | Read-only |
| `tidb_enable_plan_replayer_continuous_capture` | Read-only | Read-only |
| `tidb_enable_point_get_cache` | Not supported | Not supported |
| `tidb_enable_rate_limit_action` | Read-only | Read-only |
| `tidb_enable_resource_control` | Read-only | Read-only [^10] |
| `tidb_enable_reuse_chunk` | Read-only | Read-only |
| `tidb_enable_slow_log` | Not supported | Not supported [^4] |
| `tidb_enable_stats_owner` | Read-only | Read-only |
| `tidb_enable_stmt_summary` | Read-only | Read-only [^10] |
| `tidb_enable_table_partition` | Not supported | Not supported |
| `tidb_enable_telemetry` | Not supported | Not supported [^4] |
| `tidb_enable_tiflash_read_for_write_stmt` | Not supported | Not supported |
| `tidb_enable_tmp_storage_on_oom` | Not supported | Not supported |
| `tidb_enable_top_sql` | Read-only | Read-only [^10] |
| `tidb_enable_tso_follower_proxy` | No limitation | Read-only [^10] |
| `tidb_enable_vectorized_expression` | Read-only | Read-only |
| `tidb_evolve_plan_baselines` | Not supported | Not supported |
| `tidb_evolve_plan_task_end_time` | Not supported | Not supported |
| `tidb_evolve_plan_task_max_time` | Not supported | Not supported |
| `tidb_evolve_plan_task_start_time` | Not supported | Not supported |
| `tidb_expensive_query_time_threshold` | Not supported | Not supported [^4] |
| `tidb_force_priority` | Not supported | Not supported [^4] |
| `tidb_gc_concurrency` | No limitation | Read-only [^10] |
| `tidb_gc_enable` | No limitation | Read-only [^10] |
| `tidb_gc_leader_desc` | Not supported | Not supported |
| `tidb_gc_max_wait_time` | No limitation | Read-only [^10] |
| `tidb_gc_run_interval` | No limitation | Read-only [^10] |
| `tidb_gc_scan_lock_mode` | No limitation | Read-only [^10] |
| `tidb_general_log` | Not supported | Not supported [^4] |
| `tidb_generate_binary_plan` | Read-only | Read-only [^10] |
| `tidb_gogc_tuner_threshold` | No limitation | Read-only [^10] |
| `tidb_guarantee_linearizability` | Read-only | Read-only [^10] |
| `tidb_hash_exchange_with_new_collation` | Read-only | Read-only |
| `tidb_historical_stats_duration` | Not supported | Not supported |
| `tidb_isolation_read_engines` | No limitation | Read-only [^10] |
| `tidb_load_based_replica_read_threshold` | Read-only | Read-only |
| `tidb_lock_unchanged_keys` | Read-only | Read-only |
| `tidb_log_file_max_days` | Read-only | Read-only [^10] |
| `tidb_mem_oom_action` | Read-only | Read-only |
| `tidb_mem_quota_analyze` | Read-only | Read-only |
| `tidb_memory_debug_mode_alarm_ratio` | Not supported | Not supported |
| `tidb_memory_debug_mode_min_heap_inuse` | Not supported | Not supported |
| `tidb_memory_usage_alarm_keep_record_num` | Read-only | Read-only |
| `tidb_memory_usage_alarm_ratio` | Not supported | Not supported [^4] |
| `tidb_merge_join_concurrency` | Not supported | Not supported |
| `tidb_metric_query_range_duration` | Not supported | Not supported [^4] |
| `tidb_metric_query_step` | Not supported | Not supported [^4] |
| `tidb_non_prepared_plan_cache_size` | Not supported | Not supported |
| `tidb_opt_broadcast_cartesian_join` | Read-only | Read-only |
| `tidb_opt_concurrency_factor` | Read-only | Read-only |
| `tidb_opt_copcpu_factor` | Read-only | Read-only |
| `tidb_opt_write_row_id` | Not supported | Not supported [^4] |
| `tidb_partition_prune_mode` | Not supported | Not supported |
| `tidb_pessimistic_txn_fair_locking` | Not supported | Not supported |
| `tidb_placement_mode` | No limitation | Read-only [^10] |
| `tidb_pprof_sql_cpu` | Not supported | Not supported [^4] |
| `tidb_pre_split_regions` | Read-only | Read-only |
| `tidb_prepared_plan_cache_size` | Not supported | Read-only |
| `tidb_rc_read_check_ts` | Read-only | Read-only |
| `tidb_rc_write_check_ts` | Read-only | Read-only |
| `tidb_read_consistency` | Read-only | Read-only |
| `tidb_record_plan_in_slow_log` | Not supported | Not supported [^4] |
| `tidb_redact_log` | Not supported | Not supported [^4] |
| `tidb_replica_read` | Read-only | Read-only [^10] |
| `tidb_request_source_type` | Not supported | Not supported |
| `tidb_restricted_read_only` | Not supported | Not supported [^4] |
| `tidb_retry_limit` | Not supported | Not supported |
| `tidb_row_format_version` | Not supported | Not supported [^4] |
| `tidb_scatter_region` | No limitation | Read-only [^10] |
| `tidb_server_memory_limit` | No limitation | Read-only [^10] |
| `tidb_server_memory_limit_gc_trigger` | No limitation | Read-only [^10] |
| `tidb_server_memory_limit_sess_min_size` | No limitation | Read-only [^10] |
| `tidb_service_scope` | Read-only | Read-only |
| `tidb_simplified_metrics` | Read-only | Read-only [^10] |
| `tidb_skip_missing_partition_stats` | Read-only | Read-only |
| `tidb_slow_log_threshold` | Not supported | Not supported [^4] |
| `tidb_slow_query_file` | Not supported | Not supported [^4] |
| `tidb_slow_txn_log_threshold` | Not supported | Not supported [^4] |
| `tidb_stats_load_pseudo_timeout` | Read-only | Read-only |
| `tidb_stats_load_sync_wait` | No limitation | Read-only [^10] |
| `tidb_stmt_summary_enable_persistent` | Read-only | Read-only |
| `tidb_stmt_summary_file_max_backups` | Read-only | Read-only |
| `tidb_stmt_summary_file_max_days` | Read-only | Read-only |
| `tidb_stmt_summary_file_max_size` | Read-only | Read-only |
| `tidb_stmt_summary_filename` | Read-only | Read-only |
| `tidb_stmt_summary_history_size` | Read-only | Read-only [^10] |
| `tidb_stmt_summary_internal_query` | Read-only | Read-only [^10] |
| `tidb_stmt_summary_max_sql_length` | Read-only | Read-only [^10] |
| `tidb_stmt_summary_max_stmt_count` | Read-only | Read-only [^10] |
| `tidb_stmt_summary_refresh_interval` | Read-only | Read-only [^10] |
| `tidb_store_limit` | Read-only | Read-only |
| `tidb_streamagg_concurrency` | Not supported | Read-only |
| `tidb_sysproc_scan_concurrency` | No limitation | Read-only [^10] |
| `tidb_top_sql_max_meta_count` | Not supported | Not supported [^4] |
| `tidb_top_sql_max_time_series_count` | Not supported | Not supported [^4] |
| `tidb_track_aggregate_memory_usage` | Read-only | Read-only |
| `tidb_txn_assertion_level` | Read-only | Read-only |
| `tidb_txn_commit_batch_size` | Read-only | Read-only |
| `tidb_tso_client_batch_max_wait_time` | No limitation | Read-only [^10] |
| `tidb_ttl_delete_batch_size` | No limitation | Read-only [^10] |
| `tidb_ttl_delete_rate_limit` | No limitation | Read-only [^10] |
| `tidb_ttl_delete_worker_count` | No limitation | Read-only [^10] |
| `tidb_ttl_job_schedule_window_end_time` | No limitation | Read-only [^10] |
| `tidb_ttl_job_schedule_window_start_time` | No limitation | Read-only [^10] |
| `tidb_ttl_running_tasks` | No limitation | Read-only [^10] |
| `tidb_ttl_scan_batch_size` | No limitation | Read-only [^10] |
| `tidb_ttl_scan_worker_count` | No limitation | Read-only [^10] |
| `tidb_txn_mode` | No limitation | Read-only [^10] |
| `tidb_use_plan_baselines` | Read-only | Read-only |
| `tidb_wait_split_region_finish` | No limitation | Read-only [^10] |
| `tidb_wait_split_region_timeout` | No limitation | Read-only [^10] |
| `tiflash_compute_dispatch_policy` | Read-only | Read-only |
| `tiflash_replica_read` | Not supported | Not supported |
| `tikv_client_read_timeout` | Not supported | Not supported |
| `tx_isolation_one_shot` | Not supported | Not supported |
| `tx_read_ts` | Not supported | Not supported |
| `txn_scope` | No limitation | Read-only [^10] |
| `validate_password.enable` | No limitation | Always enabled [^9] |
| `validate_password.length` | No limitation | At least `8` [^9] |
| `validate_password.mixed_case_count` | No limitation | At least `1` [^9] |
| `validate_password.number_count` | No limitation | At least `1` [^9] |
| `validate_password.policy` | No limitation | Can only be `MEDIUM` or `STRONG` [^9] |
| `validate_password.special_char_count` | No limitation | At least `1` [^9] |
| `wait_timeout` | No limitation | Read-only [^10] |

[^1]: Configuring data placement is not supported on {{{ .starter }}} or {{{ .essential }}}.

[^2]: Configuring resource groups is not supported on {{{ .starter }}} or {{{ .essential }}}.

[^3]: To perform [Back up and Restore](/tidb-cloud/backup-and-restore-serverless.md) operations on {{{ .starter }}} or {{{ .essential }}}, you can use the TiDB Cloud console instead.

[^4]: The feature is unavailable in [Security Enhanced Mode (SEM)](/system-variables.md#tidb_enable_enhanced_security).

[^5]: To track [Slow Query](/tidb-cloud/tune-performance.md#slow-query) on {{{ .starter }}} or {{{ .essential }}}, you can use the TiDB Cloud console instead.

[^6]: To perform [Statement Analysis](/tidb-cloud/tune-performance.md#statement-analysis) on {{{ .starter }}} or {{{ .essential }}}, you can use the TiDB Cloud console instead.

[^7]: Drainer and Pump are not supported on TiDB Cloud.

[^8]: Plugin is not supported on {{{ .starter }}} or {{{ .essential }}}.

[^9]: {{{ .starter }}} and {{{ .essential }}} enforce a strong password policy.

[^10]: The variable is read-only on {{{ .starter }}} and {{{ .essential }}}.

[^11]: {{{ .starter }}} and {{{ .essential }}} do not support downloading the file exported by `PLAN REPLAYER` through `${tidb-server-status-port}` as in the [example](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#examples-of-exporting-cluster-information). Instead, {{{ .starter }}} and {{{ .essential }}} generate a [presigned URL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html) for you to download the file. Note that this URL remains valid for 10 hours after generation.


