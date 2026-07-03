---
title: TiDB X 实例上的 SQL 功能限制
summary: 了解 TiDB X 实例上的 SQL 功能限制。
---

# TiDB X 实例上的 SQL 功能限制

TiDB X 实例是一种面向服务的 TiDB Cloud 产品，基于 [TiDB X architecture](/tidb-cloud/tidb-x-architecture.md) 构建，例如 {{{ .starter }}}、Essential 或 Premium 实例。

TiDB Cloud 适用于 TiDB 支持的几乎所有工作负载，但 TiDB Self-Managed 与 TiDB Cloud 之间仍存在一些功能差异。本文档介绍 TiDB Cloud Starter、Essential 和 Premium 在 SQL 功能方面的限制。我们正在持续缩小 TiDB Self-Managed 与 TiDB Cloud 之间的功能差距。如果你需要这些尚未覆盖的功能或能力，请[联系我们](/tidb-cloud/tidb-cloud-support.md)提交功能请求。

> **Note:**
>
> 本文档仅适用于 {{{ .starter }}}、Essential 和 Premium。对于 TiDB Cloud Dedicated，请参见 [TiDB Cloud Dedicated 上的 SQL 功能限制](/tidb-cloud/limited-sql-features.md)。

## 语句 {#statements}

### 放置策略与范围管理 {#placement-and-range-management}

| Statement | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `ALTER PLACEMENT POLICY` | 不支持 [^1] | 不支持 [^1] |
| `ALTER RANGE` | 不支持 | 不支持 |
| `CREATE PLACEMENT POLICY` | 不支持 [^1] | 不支持 [^1] |
| `DROP PLACEMENT POLICY` | 不支持 [^1] | 不支持 [^1] |
| `SHOW CREATE PLACEMENT POLICY` | 不支持 [^1] | 不支持 [^1] |
| `SHOW PLACEMENT` | 不支持 [^1] | 不支持 [^1] |
| `SHOW PLACEMENT FOR` | 不支持 [^1] | 不支持 [^1] |
| `SHOW PLACEMENT LABELS` | 不支持 [^1] | 不支持 [^1] |
| `SHOW TABLE REGIONS` | 支持 | 不支持 [^1] |
| `SPLIT REGION` | 支持 | 不支持 [^1] |

### 资源组 {#resource-groups}

| Statement | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `ALTER RESOURCE GROUP` | 不支持 [^2] | 不支持 [^2] |
| `CALIBRATE RESOURCE` | 不支持 [^2] | 不支持 [^2] |
| `CREATE RESOURCE GROUP` | 不支持 [^2] | 不支持 [^2] |
| `DROP RESOURCE GROUP` | 不支持 [^2] | 不支持 [^2] |
| `SET RESOURCE GROUP` | 不支持 [^2] | 不支持 [^2] |
| `SHOW CREATE RESOURCE GROUP` | 不支持 [^2] | 不支持 [^2] |

### 其他 {#others}

| Statement | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `BACKUP` | 不支持 [^3] | 不支持 [^3] |
| `SHOW BACKUPS` | 不支持 [^3] | 不支持 [^3] |
| `RESTORE` | 不支持 [^3] | 不支持 [^3] |
| `SHOW RESTORES` | 不支持 [^3] | 不支持 [^3] |
| `BACKUP LOGS` | 不支持 | 不支持 |
| `STOP BACKUP LOGS` | 不支持 | 不支持 |
| `PAUSE BACKUP LOGS` | 不支持 | 不支持 |
| `RESUME BACKUP LOGS` | 不支持 | 不支持 |
| `SHOW BACKUP LOGS STATUS` | 不支持 | 不支持 |
| `SHOW BACKUP LOGS METADATA` | 不支持 | 不支持 |
| `PURGE BACKUP LOGS` | 不支持 | 不支持 |
| `SHOW BR JOB` | 不支持 | 不支持 |
| `SHOW BR JOB QUERY` | 不支持 | 不支持 |
| `CANCEL BR JOB` | 不支持 | 不支持 |
| `SHOW BACKUP META` | 不支持 | 不支持 |
| `RECOVER TABLE` | 不支持 | 不支持 |
| `ADMIN RESET TELEMETRY_ID` | 支持 | {{{ .starter }}} 或 {{{ .essential }}} 不支持 Telemetry。 |
| `ADMIN SHOW TELEMETRY` | 不支持 [^4] | 不支持 [^4] |
| `ADMIN SHOW SLOW` | 不支持 [^5] | 不支持 [^5] |
| `ADMIN PLUGINS ENABLE` | 不支持 [^8] | 不支持 [^8] |
| `ADMIN PLUGINS DISABLE` | 不支持 [^8] | 不支持 [^8] |
| `ADMIN SET BDR ROLE` | 不支持 | 不支持 |
| `ADMIN SHOW BDR ROLE` | 不支持 | 不支持 |
| `ADMIN UNSET BDR ROLE` | 不支持 | 不支持 |
| `ADMIN REPAIR TABLE` | 不支持 | 不支持 |
| `ALTER INSTANCE` | 不支持 | 不支持 |
| `ALTER INSTANCE RELOAD TLS` | 不支持 | {{{ .starter }}} 和 {{{ .essential }}} 会自动刷新 TLS 证书。 |
| `ALTER TABLE ... ATTRIBUTES` | 不支持 | 不支持 |
| `CHANGE DRAINER` | 不支持 [^7] | 不支持 [^7] |
| `CHANGE PUMP` | 不支持 [^7] | 不支持 [^7] |
| `FLASHBACK CLUSTER` | 不支持 [^3] | 不支持 [^3] |
| `IMPORT INTO` | 支持，但会阻止使用本地文件路径或 S3 EXTERNAL_ID 的 `IMPORT INTO` 语句。 | 不支持 |
| `LOAD DATA INFILE` | 阻止从本地文件路径执行 `LOAD DATA LOCAL INFILE`。 | 仅支持 `LOAD DATA LOCAL INFILE` |
| `LOAD STATS` | 不支持 | 不支持 |
| `SELECT ... INTO OUTFILE` | 不支持 [^4] | 不支持 [^4] |
| `SET CONFIG` | 不支持 [^4] | 不支持 [^4] |
| `SHOW CONFIG` | 不支持 [^4] | 不支持 [^4] |
| `SHOW DRAINER STATUS` | 不支持 [^7] | 不支持 [^7] |
| `SHOW PLUGINS` | 不支持 [^8] | 不支持 [^8] |
| `SHOW PUMP STATUS` | 不支持 [^7] | 不支持 [^7] |
| `SHUTDOWN` | 不支持 [^4] | 不支持 [^4] |
| `PLAN REPLAYER` | 支持 | 支持，但使用不同的文件下载方式 [^11] |
| `time_to_live` | 支持 | 不支持 |

## 函数和运算符 {#functions-and-operators}

| Function and operator | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `SLEEP` | 无限制 | [`SLEEP()` function](https://docs.pingcap.com/tidbcloud/miscellaneous-functions) 函数支持的最大休眠时间为 300 秒。 |

## 系统表 {#system-tables}

| Database | Table | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|:-|
| `metrics_schema` | 所有数据库 | 不支持 | 不支持 |
| `information_schema` | `ATTRIBUTES` | 支持 | 不支持 [^1] |
| `information_schema` | `CLUSTER_CONFIG` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `CLUSTER_HARDWARE` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `CLUSTER_INFO` | 支持 | 不支持 [^1] |
| `information_schema` | `CLUSTER_LOAD` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `CLUSTER_LOG` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `CLUSTER_SLOW_QUERY` | 不支持 [^5] | 不支持 [^5] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY` | 支持 | 不支持 [^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_EVICTED` | 支持 | 不支持 [^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_HISTORY` | 支持 | 不支持 [^6] |
| `information_schema` | `CLUSTER_SYSTEMINFO` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `INSPECTION_RESULT` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `INSPECTION_RULES` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `INSPECTION_SUMMARY` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `METRICS_SUMMARY` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `METRICS_SUMMARY_BY_LABEL` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `METRICS_TABLES` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `PLACEMENT_POLICIES` | 不支持 [^1] | 不支持 [^1] |
| `information_schema` | `RESOURCE_GROUPS` | 不支持 [^2] | 不支持 [^2] |
| `information_schema` | `SLOW_QUERY` | 不支持 [^5] | 不支持 [^5] |
| `information_schema` | `STATEMENTS_SUMMARY` | 支持 | 不支持 [^6] |
| `information_schema` | `STATEMENTS_SUMMARY_EVICTED` | 支持 | 不支持 [^6] |
| `information_schema` | `TIDB_HOT_REGIONS` | 不支持 [^4] | 不支持 [^4] |
| `information_schema` | `TIDB_HOT_REGIONS_HISTORY` | 支持 | 不支持 [^1] |
| `information_schema` | `TIDB_SERVERS_INFO` | 支持 | 不支持 [^1] |
| `information_schema` | `TIKV_REGION_PEERS` | 支持 | 不支持 [^1] |
| `information_schema` | `TIKV_REGION_STATUS` | 支持 | 不支持 [^1] |
| `information_schema` | `TIKV_STORE_STATUS` | 支持 | 不支持 [^1] |
| `performance_schema` | `pd_profile_allocs` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `pd_profile_block` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `pd_profile_cpu` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `pd_profile_goroutines` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `pd_profile_memory` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `pd_profile_mutex` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_allocs` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_block` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_cpu` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_goroutines` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_memory` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tidb_profile_mutex` | 不支持 [^4] | 不支持 [^4] |
| `performance_schema` | `tikv_profile_cpu` | 不支持 [^4] | 不支持 [^4] |
| `mysql` | `expr_pushdown_blacklist` | 不支持 [^4] | 不支持 [^4] |
| `mysql` | `gc_delete_range` | 不支持 [^4] | 不支持 [^4] |
| `mysql` | `gc_delete_range_done` | 不支持 [^4] | 不支持 [^4] |
| `mysql` | `opt_rule_blacklist` | 不支持 [^4] | 不支持 [^4] |
| `mysql` | `tidb` | 不支持 [^4] | 不支持 [^4] |

## 系统变量 {#system-variables}

| Variable | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `hostname` | 值已隐藏 | 值已隐藏 |
| `datadir` | 值已隐藏 | 不支持 [^1] |
| `ddl_slow_threshold` | 只读 | 只读 |
| `block_encryption_mode` | 只读 | 只读 |
| `max_connections` | 只读 | 只读 |
| `mpp_version` | 只读 | 只读 |
| `interactive_timeout` | 无限制 | 只读 [^10] |
| `max_allowed_packet` | 无限制 | 只读 [^10] |
| `plugin_dir` | 不支持 [^8] | 不支持 [^8] |
| `plugin_load` | 不支持 [^8] | 不支持 [^8] |
| `require_secure_transport` | 不支持 | 只读 [^10] |
| `skip_name_resolve` | 只读 [^10] | 只读 [^10] |
| `sql_log_bin` | 无限制 | 只读 [^10] |
| `tidb_adaptive_closest_read_threshold` | 不支持 | 不支持 |
| `tidb_allow_batch_cop` | 只读 | 只读 |
| `tidb_allow_mpp` | 只读 | 只读 |
| `tidb_analyze_skip_column_types` | 无限制 | 只读 [^10] |
| `tidb_analyze_version` | 只读 | 只读 |
| `tidb_backoff_lock_fast` | 只读 | 只读 |
| `tidb_backoff_weight` | 只读 | 只读 |
| `tidb_batch_commit` | 不支持 | 不支持 |
| `tidb_batch_delete` | 不支持 | 不支持 |
| `tidb_batch_insert` | 不支持 | 不支持 |
| `tidb_capture_plan_baselines` | 只读 | 只读 |
| `tidb_cdc_write_source` | 无限制 | 只读 [^10] |
| `tidb_check_mb4_value_in_utf8` | 不支持 [^4] | 不支持 [^4] |
| `tidb_cloud_storage_uri` | 不支持 | 不支持 |
| `tidb_config` | 不支持 [^4] | 不支持 [^4] |
| `tidb_constraint_check_in_place` | 只读 | 只读 |
| `tidb_constraint_check_in_place_pessimistic` | 只读 | 只读 |
| `tidb_cost_model_version` | 只读 | 只读 |
| `tidb_ddl_disk_quota` | 只读 [^10] | 只读 [^10] |
| `tidb_ddl_enable_fast_reorg` | 只读 [^10] | 只读 [^10] |
| `tidb_ddl_error_count_limit` | 无限制 | 只读 [^10] |
| `tidb_ddl_flashback_concurrency` | 只读 [^10] | 只读 [^10] |
| `tidb_ddl_reorg_batch_size` | 无限制 | 只读 [^10] |
| `tidb_ddl_reorg_max_write_speed` | 不支持 | 不支持 |
| `tidb_ddl_reorg_priority` | 无限制 | 只读 [^10] |
| `tidb_ddl_reorg_worker_cnt` | 无限制 | 只读 [^10] |
| `tidb_disable_txn_auto_retry` | 不支持 | 不支持 |
| `tidb_dml_batch_size` | 不支持 | 不支持 |
| `tidb_dml_type` | 不支持 | 只读 [^10] |
| `tidb_enable_1pc` | 无限制 | 只读 [^10] |
| `tidb_enable_analyze_snapshot` | 只读 | 只读 |
| `tidb_enable_async_commit` | 无限制 | 只读 [^10] |
| `tidb_enable_async_merge_global_stats` | 只读 | 只读 |
| `tidb_enable_auto_analyze` | 无限制 | 只读 [^10] |
| `tidb_enable_batch_dml` | 不支持 | 不支持 |
| `tidb_enable_chunk_rpc` | 只读 | 只读 |
| `tidb_enable_collect_execution_info` | 不支持 [^4] | 不支持 [^4] |
| `tidb_enable_column_tracking` | 不支持 | 不支持 |
| `tidb_enable_ddl` | 只读 [^10] | 只读 [^10] |
| `tidb_enable_dist_task` | 只读 | 只读 |
| `tidb_enable_exchange_partition` | 不支持 | 不支持 |
| `tidb_enable_extended_stats` | 只读 | 只读 |
| `tidb_enable_fast_analyze` | 不支持 | 不支持 |
| `tidb_enable_gc_aware_memory_track` | 无限制 | 只读 [^10] |
| `tidb_enable_global_index` | 不支持 | 不支持 |
| `tidb_enable_gogc_tuner` | 只读 [^10] | 只读 [^10] |
| `tidb_enable_historical_stats` | 只读 | 只读 |
| `tidb_enable_historical_stats_for_capture` | 只读 | 只读 |
| `tidb_enable_legacy_instance_scope` | 只读 | 只读 |
| `tidb_enable_list_partition` | 不支持 | 不支持 |
| `tidb_enable_local_txn` | 只读 [^10] | 只读 [^10] |
| `tidb_enable_metadata_lock` | 只读 | 只读 |
| `tidb_enable_mutation_checker` | 只读 | 不支持 |
| `tidb_enable_new_cost_interface` | 只读 | 只读 |
| `tidb_enable_parallel_hashagg_spill` | 只读 | 只读 |
| `tidb_enable_pipelined_window_function` | 无限制 | 不支持 |
| `tidb_enable_plan_replayer_capture` | 只读 | 只读 |
| `tidb_enable_plan_replayer_continuous_capture` | 只读 | 只读 |
| `tidb_enable_point_get_cache` | 不支持 | 不支持 |
| `tidb_enable_rate_limit_action` | 只读 | 只读 |
| `tidb_enable_resource_control` | 只读 [^10] | 只读 [^10] |
| `tidb_enable_reuse_chunk` | 只读 | 只读 |
| `tidb_enable_slow_log` | 不支持 [^4] | 不支持 [^4] |
| `tidb_enable_stats_owner` | 只读 | 只读 |
| `tidb_enable_stmt_summary` | 只读 [^10] | 只读 [^10] |
| `tidb_enable_table_partition` | 不支持 | 不支持 |
| `tidb_enable_telemetry` | 不支持 [^4] | 不支持 [^4] |
| `tidb_enable_tiflash_read_for_write_stmt` | 不支持 | 不支持 |
| `tidb_enable_tmp_storage_on_oom` | 不支持 | 不支持 |
| `tidb_enable_top_sql` | 只读 [^10] | 只读 [^10] |
| `tidb_enable_tso_follower_proxy` | 无限制 | 只读 [^10] |
| `tidb_enable_vectorized_expression` | 只读 | 只读 |
| `tidb_evolve_plan_baselines` | 不支持 | 不支持 |
| `tidb_evolve_plan_task_end_time` | 不支持 | 不支持 |
| `tidb_evolve_plan_task_max_time` | 不支持 | 不支持 |
| `tidb_evolve_plan_task_start_time` | 不支持 | 不支持 |
| `tidb_expensive_query_time_threshold` | 不支持 [^4] | 不支持 [^4] |
| `tidb_force_priority` | 不支持 [^4] | 不支持 [^4] |
| `tidb_gc_concurrency` | 无限制 | 只读 [^10] |
| `tidb_gc_enable` | 无限制 | 只读 [^10] |
| `tidb_gc_leader_desc` | 不支持 | 不支持 |
| `tidb_gc_max_wait_time` | 无限制 | 只读 [^10] |
| `tidb_gc_run_interval` | 无限制 | 只读 [^10] |
| `tidb_gc_scan_lock_mode` | 无限制 | 只读 [^10] |
| `tidb_general_log` | 不支持 [^4] | 不支持 [^4] |
| `tidb_generate_binary_plan` | 只读 [^10] | 只读 [^10] |
| `tidb_gogc_tuner_threshold` | 无限制 | 只读 [^10] |
| `tidb_guarantee_linearizability` | 只读 [^10] | 只读 [^10] |
| `tidb_hash_exchange_with_new_collation` | 只读 | 只读 |
| `tidb_historical_stats_duration` | 不支持 | 不支持 |
| `tidb_isolation_read_engines` | 无限制 | 只读 [^10] |
| `tidb_load_based_replica_read_threshold` | 只读 | 只读 |
| `tidb_lock_unchanged_keys` | 只读 | 只读 |
| `tidb_log_file_max_days` | 只读 [^10] | 只读 [^10] |
| `tidb_mem_oom_action` | 只读 | 只读 |
| `tidb_mem_quota_analyze` | 只读 | 只读 |
| `tidb_memory_debug_mode_alarm_ratio` | 不支持 | 不支持 |
| `tidb_memory_debug_mode_min_heap_inuse` | 不支持 | 不支持 |
| `tidb_memory_usage_alarm_keep_record_num` | 只读 | 只读 |
| `tidb_memory_usage_alarm_ratio` | 不支持 [^4] | 不支持 [^4] |
| `tidb_merge_join_concurrency` | 不支持 | 不支持 |
| `tidb_metric_query_range_duration` | 不支持 [^4] | 不支持 [^4] |
| `tidb_metric_query_step` | 不支持 [^4] | 不支持 [^4] |
| `tidb_non_prepared_plan_cache_size` | 不支持 | 不支持 |
| `tidb_opt_broadcast_cartesian_join` | 只读 | 只读 |
| `tidb_opt_concurrency_factor` | 只读 | 只读 |
| `tidb_opt_copcpu_factor` | 只读 | 只读 |
| `tidb_opt_write_row_id` | 不支持 [^4] | 不支持 [^4] |
| `tidb_partition_prune_mode` | 不支持 | 不支持 |
| `tidb_pessimistic_txn_fair_locking` | 不支持 | 不支持 |
| `tidb_placement_mode` | 无限制 | 只读 [^10] |
| `tidb_pprof_sql_cpu` | 不支持 [^4] | 不支持 [^4] |
| `tidb_pre_split_regions` | 只读 | 只读 |
| `tidb_prepared_plan_cache_size` | 不支持 | 只读 |
| `tidb_rc_read_check_ts` | 只读 | 只读 |
| `tidb_rc_write_check_ts` | 只读 | 只读 |
| `tidb_read_consistency` | 只读 | 只读 |
| `tidb_record_plan_in_slow_log` | 不支持 [^4] | 不支持 [^4] |
| `tidb_redact_log` | 不支持 [^4] | 不支持 [^4] |
| `tidb_replica_read` | 只读 [^10] | 只读 [^10] |
| `tidb_request_source_type` | 不支持 | 不支持 |
| `tidb_restricted_read_only` | 不支持 [^4] | 不支持 [^4] |
| `tidb_retry_limit` | 不支持 | 不支持 |
| `tidb_row_format_version` | 不支持 [^4] | 不支持 [^4] |
| `tidb_scatter_region` | 无限制 | 只读 [^10] |
| `tidb_server_memory_limit` | 无限制 | 只读 [^10] |
| `tidb_server_memory_limit_gc_trigger` | 无限制 | 只读 [^10] |
| `tidb_server_memory_limit_sess_min_size` | 无限制 | 只读 [^10] |
| `tidb_service_scope` | 只读 | 只读 |
| `tidb_simplified_metrics` | 只读 [^10] | 只读 [^10] |
| `tidb_skip_missing_partition_stats` | 只读 | 只读 |
| `tidb_slow_log_threshold` | 不支持 [^4] | 不支持 [^4] |
| `tidb_slow_query_file` | 不支持 [^4] | 不支持 [^4] |
| `tidb_slow_txn_log_threshold` | 不支持 [^4] | 不支持 [^4] |
| `tidb_stats_load_pseudo_timeout` | 只读 | 只读 |
| `tidb_stats_load_sync_wait` | 无限制 | 只读 [^10] |
| `tidb_stmt_summary_enable_persistent` | 只读 | 只读 |
| `tidb_stmt_summary_file_max_backups` | 只读 | 只读 |
| `tidb_stmt_summary_file_max_days` | 只读 | 只读 |
| `tidb_stmt_summary_file_max_size` | 只读 | 只读 |
| `tidb_stmt_summary_filename` | 只读 | 只读 |
| `tidb_stmt_summary_history_size` | 只读 [^10] | 只读 [^10] |
| `tidb_stmt_summary_internal_query` | 只读 [^10] | 只读 [^10] |
| `tidb_stmt_summary_max_sql_length` | 只读 [^10] | 只读 [^10] |
| `tidb_stmt_summary_max_stmt_count` | 只读 [^10] | 只读 [^10] |
| `tidb_stmt_summary_refresh_interval` | 只读 [^10] | 只读 [^10] |
| `tidb_store_limit` | 只读 | 只读 |
| `tidb_streamagg_concurrency` | 不支持 | 只读 |
| `tidb_sysproc_scan_concurrency` | 无限制 | 只读 [^10] |
| `tidb_top_sql_max_meta_count` | 不支持 [^4] | 不支持 [^4] |
| `tidb_top_sql_max_time_series_count` | 不支持 [^4] | 不支持 [^4] |
| `tidb_track_aggregate_memory_usage` | 只读 | 只读 |
| `tidb_txn_assertion_level` | 只读 | 只读 |
| `tidb_txn_commit_batch_size` | 只读 | 只读 |
| `tidb_tso_client_batch_max_wait_time` | 无限制 | 只读 [^10] |
| `tidb_ttl_delete_batch_size` | 无限制 | 只读 [^10] |
| `tidb_ttl_delete_rate_limit` | 无限制 | 只读 [^10] |
| `tidb_ttl_delete_worker_count` | 无限制 | 只读 [^10] |
| `tidb_ttl_job_schedule_window_end_time` | 无限制 | 只读 [^10] |
| `tidb_ttl_job_schedule_window_start_time` | 无限制 | 只读 [^10] |
| `tidb_ttl_running_tasks` | 无限制 | 只读 [^10] |
| `tidb_ttl_scan_batch_size` | 无限制 | 只读 [^10] |
| `tidb_ttl_scan_worker_count` | 无限制 | 只读 [^10] |
| `tidb_txn_mode` | 无限制 | 只读 [^10] |
| `tidb_use_plan_baselines` | 只读 | 只读 |
| `tidb_wait_split_region_finish` | 无限制 | 只读 [^10] |
| `tidb_wait_split_region_timeout` | 无限制 | 只读 [^10] |
| `tiflash_compute_dispatch_policy` | 只读 | 只读 |
| `tiflash_replica_read` | 不支持 | 不支持 |
| `tikv_client_read_timeout` | 不支持 | 不支持 |
| `tx_isolation_one_shot` | 不支持 | 不支持 |
| `tx_read_ts` | 不支持 | 不支持 |
| `txn_scope` | 无限制 | 只读 [^10] |
| `validate_password.enable` | 无限制 | 始终启用 [^9] |
| `validate_password.length` | 无限制 | 至少为 `8` [^9] |
| `validate_password.mixed_case_count` | 无限制 | 至少为 `1` [^9] |
| `validate_password.number_count` | 无限制 | 至少为 `1` [^9] |
| `validate_password.policy` | 无限制 | 只能为 `MEDIUM` 或 `STRONG` [^9] |
| `validate_password.special_char_count` | 无限制 | 至少为 `1` [^9] |
| `wait_timeout` | 无限制 | 只读 [^10] |

[^1]: {{{ .starter }}}、Essential 和 Premium 不支持配置数据放置。

[^2]: {{{ .starter }}}、Essential 和 Premium 不支持配置资源组。

[^3]: 要在 {{{ .starter }}}、Essential 或 Premium 上执行[备份与恢复](/tidb-cloud/backup-and-restore-serverless.md)操作，可以改用 TiDB Cloud 控制台。

[^4]: 该功能在 [Security Enhanced Mode (SEM)](/system-variables.md#tidb_enable_enhanced_security) 中不可用。

[^5]: 要在 {{{ .starter }}}、Essential 或 Premium 上跟踪[慢查询](/tidb-cloud/tune-performance.md#slow-query)，可以改用 TiDB Cloud 控制台。

[^6]: 要在 {{{ .starter }}} 或 {{{ .essential }}} 上执行[语句分析](/tidb-cloud/tune-performance.md#statement-analysis)，可以改用 TiDB Cloud 控制台。

[^7]: TiDB Cloud 不支持 Drainer 和 Pump。

[^8]: {{{ .starter }}}、Essential 和 Premium 不支持插件。

[^9]: {{{ .starter }}} 和 {{{ .essential }}} 强制执行强密码策略。

[^10]: 该变量在 {{{ .starter }}} 和 {{{ .essential }}} 上为只读。

[^11]: {{{ .starter }}} 和 {{{ .essential }}} 不支持像[示例](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#examples-of-exporting-cluster-information)中所示那样，通过 `${tidb-server-status-port}` 下载 `PLAN REPLAYER` 导出的文件。相反，{{{ .starter }}} 和 {{{ .essential }}} 会生成一个 [presigned URL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html) 供你下载文件。请注意，该 URL 在生成后 10 小时内有效。