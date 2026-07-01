---
title: TiDB Cloud Dedicated 上受限的 SQL 功能
summary: 了解 TiDB Cloud Dedicated 上受限的 SQL 功能。
---

# TiDB Cloud Dedicated 上受限的 SQL 功能

TiDB Cloud Dedicated 支持几乎所有 TiDB 支持的工作负载，但 TiDB 自建版与 TiDB Cloud Dedicated 之间存在一些功能差异。本文档描述了 TiDB Cloud Dedicated 上 SQL 功能的限制。我们正在不断弥补 TiDB 自建版与 TiDB Cloud Dedicated 之间的功能差距。如果你需要这些尚未支持的功能或能力，请[联系我们](/tidb-cloud/tidb-cloud-support.md)提交功能请求。

> **注意：**
>
> 本文档仅适用于 TiDB Cloud Dedicated。对于 TiDB Cloud Starter、Essential 和 Premium，请参见 [TiDB X 实例上受限的 SQL 功能](/tidb-cloud/limited-sql-features-tidb-x.md)。

## 语句

### 数据放置与范围管理

| 语句 | TiDB Cloud Dedicated |
|:-|:-|
| `ALTER PLACEMENT POLICY` | 支持 |
| `CREATE PLACEMENT POLICY` | 支持 |
| `DROP PLACEMENT POLICY` | 支持 |
| `SHOW CREATE PLACEMENT POLICY` | 支持 |
| `SHOW PLACEMENT` | 支持 |
| `SHOW PLACEMENT FOR` | 支持 |
| `SHOW PLACEMENT LABELS` | 支持 |
| `SHOW TABLE REGIONS` | 支持 |
| `SPLIT REGION` | 支持 |

### 资源组

| 语句 | TiDB Cloud Dedicated |
|:-|:-|
| `ALTER RESOURCE GROUP` | 支持 |
| `CALIBRATE RESOURCE` | 不支持 |
| `CREATE RESOURCE GROUP` | 支持 |
| `DROP RESOURCE GROUP` | 支持 |
| `SET RESOURCE GROUP` | 支持 |
| `SHOW CREATE RESOURCE GROUP` | 支持 |

### 其他

| 语句 | TiDB Cloud Dedicated |
|:-|:-|
| `BACKUP` | 支持 |
| `SHOW BACKUPS` | 支持 |
| `RESTORE` | 支持 |
| `SHOW RESTORES` | 支持 |
| `ADMIN RESET TELEMETRY_ID` | 支持 |
| `ADMIN SHOW TELEMETRY` | 不支持 [^1] |
| `ADMIN SHOW SLOW` | 支持 |
| `ADMIN PLUGINS ENABLE` | 支持 |
| `ADMIN PLUGINS DISABLE` | 支持 |
| `ALTER INSTANCE RELOAD TLS` | 支持 |
| `LOAD DATA INFILE` | 支持 `LOAD DATA LOCAL INFILE`，以及从 Amazon S3 或 Google Cloud Storage 的 `LOAD DATA INFILE` |
| `CHANGE DRAINER` | 不支持 [^2] |
| `CHANGE PUMP` | 不支持 [^2] |
| `FLASHBACK CLUSTER` | 支持 |
| `LOAD STATS` | 支持 |
| `SELECT ... INTO OUTFILE` | 不支持 [^1] |
| `SET CONFIG` | 不支持 [^1] |
| `SHOW CONFIG` | 不支持 [^1] |
| `SHOW DRAINER STATUS` | 不支持 [^2] |
| `SHOW PLUGINS` | 支持 |
| `SHOW PUMP STATUS` | 不支持 [^2] |
| `SHUTDOWN` | 不支持 [^1] |
| `PLAN REPLAYER` | 支持 |

## 函数与运算符

| 函数与运算符 | TiDB Cloud Dedicated |
|:-|:-|
| `SLEEP` | 无限制 |

## 系统表

| 数据库 | 表 | TiDB Cloud Dedicated |
|:-|:-|:-|
| `information_schema` | `ATTRIBUTES` | 支持 |
| `information_schema` | `CLUSTER_CONFIG` | 不支持 [^1] |
| `information_schema` | `CLUSTER_HARDWARE` | 不支持 [^1] |
| `information_schema` | `CLUSTER_INFO` | 支持 |
| `information_schema` | `CLUSTER_LOAD` | 不支持 [^1] |
| `information_schema` | `CLUSTER_LOG` | 不支持 [^1] |
| `information_schema` | `CLUSTER_SLOW_QUERY` | 支持 |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY` | 支持 |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_EVICTED` | 支持 |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_HISTORY` | 支持 |
| `information_schema` | `CLUSTER_SYSTEMINFO` | 不支持 [^1] |
| `information_schema` | `INSPECTION_RESULT` | 不支持 [^1] |
| `information_schema` | `INSPECTION_RULES` | 不支持 [^1] |
| `information_schema` | `INSPECTION_SUMMARY` | 不支持 [^1] |
| `information_schema` | `METRICS_SUMMARY` | 不支持 [^1] |
| `information_schema` | `METRICS_SUMMARY_BY_LABEL` | 不支持 [^1] |
| `information_schema` | `METRICS_TABLES` | 不支持 [^1] |
| `information_schema` | `PLACEMENT_POLICIES` | 支持 |
| `information_schema` | `RESOURCE_GROUPS` | 支持 |
| `information_schema` | `SLOW_QUERY` | 支持 |
| `information_schema` | `STATEMENTS_SUMMARY` | 支持 |
| `information_schema` | `STATEMENTS_SUMMARY_EVICTED` | 支持 |
| `information_schema` | `TIDB_HOT_REGIONS` | 不支持 [^1] |
| `information_schema` | `TIDB_HOT_REGIONS_HISTORY` | 支持 |
| `information_schema` | `TIDB_SERVERS_INFO` | 支持 |
| `information_schema` | `TIKV_REGION_PEERS` | 支持 |
| `information_schema` | `TIKV_REGION_STATUS` | 支持 |
| `information_schema` | `TIKV_STORE_STATUS` | 支持 |
| `performance_schema` | `pd_profile_allocs` | 不支持 [^1] |
| `performance_schema` | `pd_profile_block` | 不支持 [^1] |
| `performance_schema` | `pd_profile_cpu` | 不支持 [^1] |
| `performance_schema` | `pd_profile_goroutines` | 不支持 [^1] |
| `performance_schema` | `pd_profile_memory` | 不支持 [^1] |
| `performance_schema` | `pd_profile_mutex` | 不支持 [^1] |
| `performance_schema` | `tidb_profile_allocs` | 不支持 [^1] |
| `performance_schema` | `tidb_profile_block` | 不支持 [^1] |
| `performance_schema` | `tidb_profile_cpu` | 不支持 [^1] |
| `performance_schema` | `tidb_profile_goroutines` | 不支持 [^1] |
| `performance_schema` | `tidb_profile_memory` | 不支持 [^1] |
| `performance_schema` | `tidb_profile_mutex` | 不支持 [^1] |
| `performance_schema` | `tikv_profile_cpu` | 不支持 [^1] |
| `mysql` | `expr_pushdown_blacklist` | 不支持 [^1] |
| `mysql` | `gc_delete_range` | 不支持 [^1] |
| `mysql` | `gc_delete_range_done` | 不支持 [^1] |
| `mysql` | `opt_rule_blacklist` | 不支持 [^1] |
| `mysql` | `tidb` | 不支持 [^1] |

## 系统变量

| 变量 | TiDB Cloud Dedicated |
|:-|:-|
| `datadir` | 无限制 |
| `interactive_timeout` | 无限制 |
| `max_allowed_packet` | 无限制 |
| `plugin_dir` | 无限制 |
| `plugin_load` | 无限制 |
| `require_secure_transport` | 不支持 [^3] |
| `skip_name_resolve` | 无限制 |
| `sql_log_bin` | 无限制 |
| `tidb_analyze_skip_column_types` | 无限制 |
| `tidb_cdc_write_source` | 无限制 |
| `tidb_check_mb4_value_in_utf8` | 不支持 [^1] |
| `tidb_config` | 不支持 [^1] |
| `tidb_ddl_disk_quota` | 无限制 |
| `tidb_ddl_enable_fast_reorg` | 无限制 |
| `tidb_ddl_error_count_limit` | 无限制 |
| `tidb_ddl_flashback_concurrency` | 无限制 |
| `tidb_ddl_reorg_batch_size` | 无限制 |
| `tidb_ddl_reorg_priority` | 无限制 |
| `tidb_ddl_reorg_worker_cnt` | 无限制 |
| `tidb_dml_type` | 无限制 |
| `tidb_enable_1pc` | 无限制 |
| `tidb_enable_async_commit` | 无限制 |
| `tidb_enable_auto_analyze` | 无限制 |
| `tidb_enable_collect_execution_info` | 不支持 [^1] |
| `tidb_enable_ddl` | 无限制 |
| `tidb_enable_gc_aware_memory_track` | 无限制 |
| `tidb_enable_gogc_tuner` | 无限制 |
| `tidb_enable_local_txn` | 无限制 |
| `tidb_enable_resource_control` | 无限制 |
| `tidb_enable_slow_log` | 不支持 [^1] |
| `tidb_enable_stmt_summary` | 无限制 |
| `tidb_enable_telemetry` | 不支持 [^1] |
| `tidb_enable_top_sql` | 无限制 |
| `tidb_enable_tso_follower_proxy` | 无限制 |
| `tidb_expensive_query_time_threshold` | 不支持 [^1] |
| `tidb_force_priority` | 不支持 [^1] |
| `tidb_gc_concurrency` | 无限制 |
| `tidb_gc_enable` | 无限制 |
| `tidb_gc_max_wait_time` | 无限制 |
| `tidb_gc_run_interval` | 无限制 |
| `tidb_gc_scan_lock_mode` | 无限制 |
| `tidb_general_log` | 不支持 [^1] |
| `tidb_generate_binary_plan` | 无限制 |
| `tidb_gogc_tuner_threshold` | 无限制 |
| `tidb_guarantee_linearizability` | 无限制 |
| `tidb_isolation_read_engines` | 无限制 |
| `tidb_log_file_max_days` | 无限制 |
| `tidb_memory_usage_alarm_ratio` | 不支持 [^1] |
| `tidb_metric_query_range_duration` | 不支持 [^1] |
| `tidb_metric_query_step` | 不支持 [^1] |
| `tidb_opt_write_row_id` | 不支持 [^1] |
| `tidb_placement_mode` | 无限制 |
| `tidb_pprof_sql_cpu` | 不支持 [^1] |
| `tidb_record_plan_in_slow_log` | 不支持 [^1] |
| `tidb_redact_log` | 不支持 [^1] |
| `tidb_replica_read` | 无限制 |
| `tidb_restricted_read_only` | 不支持 [^1] |
| `tidb_row_format_version` | 不支持 [^1] |
| `tidb_scatter_region` | 无限制 |
| `tidb_server_memory_limit` | 无限制 |
| `tidb_server_memory_limit_gc_trigger` | 无限制 |
| `tidb_server_memory_limit_sess_min_size` | 无限制 |
| `tidb_simplified_metrics` | 无限制 |
| `tidb_slow_query_file` | 不支持 [^1] |
| `tidb_slow_log_threshold` | 不支持 [^1] |
| `tidb_slow_txn_log_threshold` | 不支持 [^1] |
| `tidb_stats_load_sync_wait` | 无限制 |
| `tidb_stmt_summary_history_size` | 无限制 |
| `tidb_stmt_summary_internal_query` | 无限制 |
| `tidb_stmt_summary_max_sql_length` | 无限制 |
| `tidb_stmt_summary_max_stmt_count` | 无限制 |
| `tidb_stmt_summary_refresh_interval` | 无限制 |
| `tidb_sysproc_scan_concurrency` | 无限制 |
| `tidb_top_sql_max_meta_count` | 不支持 [^1] |
| `tidb_top_sql_max_time_series_count` | 不支持 [^1] |
| `tidb_tso_client_batch_max_wait_time` | 无限制 |
| `tidb_ttl_delete_batch_size` | 无限制 |
| `tidb_ttl_delete_rate_limit` | 无限制 |
| `tidb_ttl_delete_worker_count` | 无限制 |
| `tidb_ttl_job_schedule_window_end_time` | 无限制 |
| `tidb_ttl_job_schedule_window_start_time` | 无限制 |
| `tidb_ttl_running_tasks` | 无限制 |
| `tidb_ttl_scan_batch_size` | 无限制 |
| `tidb_ttl_scan_worker_count` | 无限制 |
| `tidb_txn_mode` | 无限制 |
| `tidb_wait_split_region_finish` | 无限制 |
| `tidb_wait_split_region_timeout` | 无限制 |
| `txn_scope` | 无限制 |
| `validate_password.enable` | 无限制 |
| `validate_password.length` | 无限制 |
| `validate_password.mixed_case_count` | 无限制 |
| `validate_password.number_count` | 无限制 |
| `validate_password.policy` | 无限制 |
| `validate_password.special_char_count` | 无限制 |
| `wait_timeout` | 无限制 |

[^1]: 该功能在 [安全增强模式（SEM）](/system-variables.md#tidb_enable_enhanced_security) 下不可用。

[^2]: TiDB Cloud 不支持 Drainer 和 Pump。

[^3]: 不支持。在 TiDB Cloud Dedicated 集群上启用 `require_secure_transport` 会导致 SQL 客户端连接失败。