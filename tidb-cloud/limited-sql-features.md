---
title: Limited SQL Features on TiDB Cloud Dedicated
summary: Learn about the limited SQL features on TiDB Cloud Dedicated.
---

# Limited SQL features on TiDB Cloud Dedicated

TiDB Cloud Dedicated works with almost all workloads that TiDB supports, but there are some feature differences between TiDB Self-Managed and TiDB Cloud Dedicated. This document describes the limitations of SQL features on TiDB Cloud Dedicated. We are constantly filling in the feature gaps between TiDB Self-Managed and TiDB Cloud Dedicated. If you require these features or capabilities in the gap, [contact us](/tidb-cloud/tidb-cloud-support.md) for a feature request.

> **Note:**
>
> This document applies only to TiDB Cloud Dedicated clusters. For TiDB X instances, see [Limited SQL Features on TiDB X Instances](/tidb-cloud/limited-sql-features-tidb-x.md).

## Statements

### Placement and range management

| Statement | TiDB Cloud Dedicated |
|:-|:-|
| `ALTER PLACEMENT POLICY` | Supported |
| `CREATE PLACEMENT POLICY` | Supported |
| `DROP PLACEMENT POLICY` | Supported |
| `SHOW CREATE PLACEMENT POLICY` | Supported |
| `SHOW PLACEMENT` | Supported |
| `SHOW PLACEMENT FOR` | Supported |
| `SHOW PLACEMENT LABELS` | Supported |
| `SHOW TABLE REGIONS` | Supported |
| `SPLIT REGION` | Supported |

### Resource groups

| Statement | TiDB Cloud Dedicated |
|:-|:-|
| `ALTER RESOURCE GROUP` | Supported |
| `CALIBRATE RESOURCE` | Not supported |
| `CREATE RESOURCE GROUP` | Supported |
| `DROP RESOURCE GROUP` | Supported |
| `SET RESOURCE GROUP` | Supported |
| `SHOW CREATE RESOURCE GROUP` | Supported |

### Others

| Statement | TiDB Cloud Dedicated |
|:-|:-|
| `BACKUP` | Supported |
| `SHOW BACKUPS` | Supported |
| `RESTORE` | Supported |
| `SHOW RESTORES` | Supported |
| `ADMIN RESET TELEMETRY_ID` | Supported |
| `ADMIN SHOW TELEMETRY` | Not supported [^1] |
| `ADMIN SHOW SLOW` | Supported |
| `ADMIN PLUGINS ENABLE` | Supported |
| `ADMIN PLUGINS DISABLE` | Supported |
| `ALTER INSTANCE RELOAD TLS` | Supported |
| `LOAD DATA INFILE` | Supports `LOAD DATA LOCAL INFILE`, and `LOAD DATA INFILE` from Amazon S3 or Google Cloud Storage |
| `CHANGE DRAINER` | Not supported [^2] |
| `CHANGE PUMP` | Not supported [^2] |
| `FLASHBACK CLUSTER` | Supported |
| `LOAD STATS` | Supported |
| `SELECT ... INTO OUTFILE` | Not supported [^1] |
| `SET CONFIG` | Not supported [^1] |
| `SHOW CONFIG` | Not supported [^1] |
| `SHOW DRAINER STATUS` | Not supported [^2] |
| `SHOW PLUGINS` | Supported |
| `SHOW PUMP STATUS` | Not supported [^2] |
| `SHUTDOWN` | Not supported [^1] |
| `PLAN REPLAYER` | Supported |

## Functions and operators

| Function and operator | TiDB Cloud Dedicated |
|:-|:-|
| `SLEEP` | No Limitation |

## System tables

| Database | Table | TiDB Cloud Dedicated |
|:-|:-|:-|
| `information_schema` | `ATTRIBUTES` | Supported |
| `information_schema` | `CLUSTER_CONFIG` | Not supported [^1] |
| `information_schema` | `CLUSTER_HARDWARE` | Not supported [^1] |
| `information_schema` | `CLUSTER_INFO` | Supported |
| `information_schema` | `CLUSTER_LOAD` | Not supported [^1] |
| `information_schema` | `CLUSTER_LOG` | Not supported [^1] |
| `information_schema` | `CLUSTER_SLOW_QUERY` | Supported |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY` | Supported |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_EVICTED` | Supported |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_HISTORY` | Supported |
| `information_schema` | `CLUSTER_SYSTEMINFO` | Not supported [^1] |
| `information_schema` | `INSPECTION_RESULT` | Not supported [^1] |
| `information_schema` | `INSPECTION_RULES` | Not supported [^1] |
| `information_schema` | `INSPECTION_SUMMARY` | Not supported [^1] |
| `information_schema` | `METRICS_SUMMARY` | Not supported [^1] |
| `information_schema` | `METRICS_SUMMARY_BY_LABEL` | Not supported [^1] |
| `information_schema` | `METRICS_TABLES` | Not supported [^1] |
| `information_schema` | `PLACEMENT_POLICIES` | Supported |
| `information_schema` | `RESOURCE_GROUPS` | Supported |
| `information_schema` | `SLOW_QUERY` | Supported |
| `information_schema` | `STATEMENTS_SUMMARY` | Supported |
| `information_schema` | `STATEMENTS_SUMMARY_EVICTED` | Supported |
| `information_schema` | `TIDB_HOT_REGIONS` | Not supported [^1] |
| `information_schema` | `TIDB_HOT_REGIONS_HISTORY` | Supported |
| `information_schema` | `TIDB_SERVERS_INFO` | Supported |
| `information_schema` | `TIKV_REGION_PEERS` | Supported |
| `information_schema` | `TIKV_REGION_STATUS` | Supported |
| `information_schema` | `TIKV_STORE_STATUS` | Supported |
| `performance_schema` | `pd_profile_allocs` | Not supported [^1] |
| `performance_schema` | `pd_profile_block` | Not supported [^1] |
| `performance_schema` | `pd_profile_cpu` | Not supported [^1] |
| `performance_schema` | `pd_profile_goroutines` | Not supported [^1] |
| `performance_schema` | `pd_profile_memory` | Not supported [^1] |
| `performance_schema` | `pd_profile_mutex` | Not supported [^1] |
| `performance_schema` | `tidb_profile_allocs` | Not supported [^1] |
| `performance_schema` | `tidb_profile_block` | Not supported [^1] |
| `performance_schema` | `tidb_profile_cpu` | Not supported [^1] |
| `performance_schema` | `tidb_profile_goroutines` | Not supported [^1] |
| `performance_schema` | `tidb_profile_memory` | Not supported [^1] |
| `performance_schema` | `tidb_profile_mutex` | Not supported [^1] |
| `performance_schema` | `tikv_profile_cpu` | Not supported [^1] |
| `mysql` | `expr_pushdown_blacklist` | Not supported [^1] |
| `mysql` | `gc_delete_range` | Not supported [^1] |
| `mysql` | `gc_delete_range_done` | Not supported [^1] |
| `mysql` | `opt_rule_blacklist` | Not supported [^1] |
| `mysql` | `tidb` | Not supported [^1] |

## System variables

| Variable | TiDB Cloud Dedicated |
|:-|:-|
| `datadir` | No limitation |
| `interactive_timeout` | No limitation |
| `max_allowed_packet` | No limitation |
| `plugin_dir` | No limitation |
| `plugin_load` | No limitation |
| `require_secure_transport` | Not supported [^3] |
| `skip_name_resolve` | No limitation |
| `sql_log_bin` | No limitation |
| `tidb_analyze_skip_column_types` | No limitation |
| `tidb_cdc_write_source` | No limitation |
| `tidb_check_mb4_value_in_utf8` | Not supported [^1] |
| `tidb_config` | Not supported [^1] |
| `tidb_ddl_disk_quota` | No limitation |
| `tidb_ddl_enable_fast_reorg` | No limitation |
| `tidb_ddl_error_count_limit` | No limitation |
| `tidb_ddl_flashback_concurrency` | No limitation |
| `tidb_ddl_reorg_batch_size` | No limitation |
| `tidb_ddl_reorg_priority` | No limitation |
| `tidb_ddl_reorg_worker_cnt` | No limitation |
| `tidb_dml_type` | No limitation |
| `tidb_enable_1pc` | No limitation |
| `tidb_enable_async_commit` | No limitation |
| `tidb_enable_auto_analyze` | No limitation |
| `tidb_enable_collect_execution_info` | Not supported [^1] |
| `tidb_enable_ddl` | No limitation |
| `tidb_enable_gc_aware_memory_track` | No limitation |
| `tidb_enable_gogc_tuner` | No limitation |
| `tidb_enable_local_txn` | No limitation |
| `tidb_enable_resource_control` | No limitation |
| `tidb_enable_slow_log` | Not supported [^1] |
| `tidb_enable_stmt_summary` | No limitation |
| `tidb_enable_telemetry` | Not supported [^1] |
| `tidb_enable_top_sql` | No limitation |
| `tidb_enable_tso_follower_proxy` | No limitation |
| `tidb_expensive_query_time_threshold` | Not supported [^1] |
| `tidb_force_priority` | Not supported [^1] |
| `tidb_gc_concurrency` | No limitation |
| `tidb_gc_enable` | No limitation |
| `tidb_gc_max_wait_time` | No limitation |
| `tidb_gc_run_interval` | No limitation |
| `tidb_gc_scan_lock_mode` | No limitation |
| `tidb_general_log` | Not supported [^1] |
| `tidb_generate_binary_plan` | No limitation |
| `tidb_gogc_tuner_threshold` | No limitation |
| `tidb_guarantee_linearizability` | No limitation |
| `tidb_isolation_read_engines` | No limitation |
| `tidb_log_file_max_days` | No limitation |
| `tidb_memory_usage_alarm_ratio` | Not supported [^1] |
| `tidb_metric_query_range_duration` | Not supported [^1] |
| `tidb_metric_query_step` | Not supported [^1] |
| `tidb_opt_write_row_id` | Not supported [^1] |
| `tidb_placement_mode` | No limitation |
| `tidb_pprof_sql_cpu` | Not supported [^1] |
| `tidb_record_plan_in_slow_log` | Not supported [^1] |
| `tidb_redact_log` | Not supported [^1] |
| `tidb_replica_read` | No limitation |
| `tidb_restricted_read_only` | Not supported [^1] |
| `tidb_row_format_version` | Not supported [^1] |
| `tidb_scatter_region` | No limitation |
| `tidb_server_memory_limit` | No limitation |
| `tidb_server_memory_limit_gc_trigger` | No limitation |
| `tidb_server_memory_limit_sess_min_size` | No limitation |
| `tidb_simplified_metrics` | No limitation |
| `tidb_slow_query_file` | Not supported [^1] |
| `tidb_slow_log_threshold` | Not supported [^1] |
| `tidb_slow_txn_log_threshold` | Not supported [^1] |
| `tidb_stats_load_sync_wait` | No limitation |
| `tidb_stmt_summary_history_size` | No limitation |
| `tidb_stmt_summary_internal_query` | No limitation |
| `tidb_stmt_summary_max_sql_length` | No limitation |
| `tidb_stmt_summary_max_stmt_count` | No limitation |
| `tidb_stmt_summary_refresh_interval` | No limitation |
| `tidb_sysproc_scan_concurrency` | No limitation |
| `tidb_top_sql_max_meta_count` | Not supported [^1] |
| `tidb_top_sql_max_time_series_count` | Not supported [^1] |
| `tidb_tso_client_batch_max_wait_time` | No limitation |
| `tidb_ttl_delete_batch_size` | No limitation |
| `tidb_ttl_delete_rate_limit` | No limitation |
| `tidb_ttl_delete_worker_count` | No limitation |
| `tidb_ttl_job_schedule_window_end_time` | No limitation |
| `tidb_ttl_job_schedule_window_start_time` | No limitation |
| `tidb_ttl_running_tasks` | No limitation |
| `tidb_ttl_scan_batch_size` | No limitation |
| `tidb_ttl_scan_worker_count` | No limitation |
| `tidb_txn_mode` | No limitation |
| `tidb_wait_split_region_finish` | No limitation |
| `tidb_wait_split_region_timeout` | No limitation |
| `txn_scope` | No limitation |
| `validate_password.enable` | No limitation |
| `validate_password.length` | No limitation |
| `validate_password.mixed_case_count` | No limitation |
| `validate_password.number_count` | No limitation |
| `validate_password.policy` | No limitation |
| `validate_password.special_char_count` | No limitation |
| `wait_timeout` | No limitation |

[^1]: The feature is unavailable in [Security Enhanced Mode (SEM)](/system-variables.md#tidb_enable_enhanced_security).

[^2]: Drainer and Pump are not supported on TiDB Cloud.

[^3]: Not supported. Enabling `require_secure_transport` for TiDB Cloud Dedicated clusters will result in SQL client connection failures.
