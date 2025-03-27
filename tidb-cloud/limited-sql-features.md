---
title: Limited SQL Features on TiDB Cloud
summary: Learn about the limited SQL features on TiDB Cloud.
---

# Limited SQL features on TiDB Cloud

TiDB Cloud works with almost all workloads that TiDB supports, but there are some feature differences between TiDB Self-Managed and TiDB Cloud Starter. This document describes the limitations of SQL features on TiDB Cloud. We are constantly filling in the feature gaps between TiDB Self-Managed and TiDB Cloud Starter. If you require these features or capabilities in the gap, [contact us](/tidb-cloud/tidb-cloud-support.md) for a feature request.

## Statements

### Placement and range management

| Statement | TiDB Cloud Starter |
|:-|:-|
| `ALTER PLACEMENT POLICY` | Not supported [^1] |
| `CREATE PLACEMENT POLICY` | Not supported [^1] |
| `DROP PLACEMENT POLICY` | Not supported [^1] |
| `SHOW CREATE PLACEMENT POLICY` | Not supported [^1] |
| `SHOW PLACEMENT` | Not supported [^1] |
| `SHOW PLACEMENT FOR` | Not supported [^1] |
| `SHOW PLACEMENT LABELS` | Not supported [^1] |
| `SHOW TABLE REGIONS` | Not supported [^1] |
| `SPLIT REGION` | Not supported [^1] |

### Resource groups

| Statement | TiDB Cloud Starter |
|:-|:-|
| `ALTER RESOURCE GROUP` | Not supported [^2] |
| `CALIBRATE RESOURCE` | Not supported [^2] |
| `CREATE RESOURCE GROUP` | Not supported [^2] |
| `DROP RESOURCE GROUP` | Not supported [^2] |
| `SET RESOURCE GROUP` | Not supported [^2] |
| `SHOW CREATE RESOURCE GROUP` | Not supported [^2] |

### Others

| Statement | TiDB Cloud Starter |
|:-|:-|
| `BACKUP` | Not supported [^3] |
| `SHOW BACKUPS` | Not supported [^3] |
| `RESTORE` | Not supported [^3] |
| `SHOW RESTORES` | Not supported [^3] |
| `ADMIN RESET TELEMETRY_ID` | Telemetry is not supported on TiDB Cloud Starter. |
| `ADMIN SHOW TELEMETRY` | Not supported [^4] |
| `ADMIN SHOW SLOW` | Not supported [^5] |
| `ADMIN PLUGINS ENABLE` | Not supported [^8] |
| `ADMIN PLUGINS DISABLE` | Not supported [^8] |
| `ALTER INSTANCE RELOAD TLS` | TiDB Cloud Starter automatically refreshes the TLS certificate. |
| `LOAD DATA INFILE` | Only supports `LOAD DATA LOCAL INFILE` |
| `CHANGE DRAINER` | Not supported [^7] |
| `CHANGE PUMP` | Not supported [^7] |
| `FLASHBACK CLUSTER` | Not supported [^3] |
| `LOAD STATS` | Not supported |
| `SELECT ... INTO OUTFILE` | Not supported [^4] |
| `SET CONFIG` | Not supported [^4] |
| `SHOW CONFIG` | Not supported [^4] |
| `SHOW DRAINER STATUS` | Not supported [^7] |
| `SHOW PLUGINS` | Not supported [^8] |
| `SHOW PUMP STATUS` | Not supported [^7] |
| `SHUTDOWN` | Not supported [^4] |
| `PLAN REPLAYER` | Supported in a different way[^11] |

## Functions and operators

| Function and operator | TiDB Cloud Starter |
|:-|:-|
| `SLEEP` | The [`SLEEP()` function](https://docs.tidb.io/tidbcloud/miscellaneous-functions) has a limitation wherein it can only support a maximum sleep time of 300 seconds.|

## System tables

| Database | TiDB Cloud Starter |
|:-|:-|
| `information_schema` | Not supported [^1] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^1] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^5] |
| `information_schema` | Not supported [^6] |
| `information_schema` | Not supported [^6] |
| `information_schema` | Not supported [^6] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^1] |
| `information_schema` | Not supported [^2] |
| `information_schema` | Not supported [^5] |
| `information_schema` | Not supported [^6] |
| `information_schema` | Not supported [^6] |
| `information_schema` | Not supported [^6] |
| `information_schema` | Not supported [^4] |
| `information_schema` | Not supported [^1] |
| `information_schema` | Not supported [^1] |
| `information_schema` | Not supported [^1] |
| `information_schema` | Not supported [^1] |
| `information_schema` | Not supported [^1] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `performance_schema` | Not supported [^4] |
| `mysql` | Not supported [^4] |
| `mysql` | Not supported [^4] |
| `mysql` | Not supported [^4] |
| `mysql` | Not supported [^4] |
| `mysql` | Not supported [^4] |

## System variables

| Variable | TiDB Cloud Starter |
|:-|:-|
| `datadir` | Not supported [^1] |
| `interactive_timeout` | Read-only [^10] |
| `max_allowed_packet` | Read-only [^10] |
| `plugin_dir` | Not supported [^8] |
| `plugin_load` | Not supported [^8] |
| `require_secure_transport` | Read-only [^10] |
| `skip_name_resolve` | Read-only [^10] |
| `sql_log_bin` | Read-only [^10] |
| `tidb_cdc_write_source` | Read-only [^10] |
| `tidb_check_mb4_value_in_utf8` | Not supported [^4] |
| `tidb_config` | Not supported [^4] |
| `tidb_ddl_disk_quota` | Read-only [^10] |
| `tidb_ddl_enable_fast_reorg` | Read-only [^10] |
| `tidb_ddl_error_count_limit` | Read-only [^10] |
| `tidb_ddl_flashback_concurrency` | Read-only [^10] |
| `tidb_ddl_reorg_batch_size` | Read-only [^10] |
| `tidb_ddl_reorg_priority` | Read-only [^10] |
| `tidb_ddl_reorg_worker_cnt` | Read-only [^10] |
| `tidb_enable_1pc` | Read-only [^10] |
| `tidb_enable_async_commit` | Read-only [^10] |
| `tidb_enable_auto_analyze` | Read-only [^10] |
| `tidb_enable_collect_execution_info` | Not supported [^4] |
| `tidb_enable_ddl` | Read-only [^10] |
| `tidb_enable_gc_aware_memory_track` | Read-only [^10] |
| `tidb_enable_gogc_tuner` | Read-only [^10] |
| `tidb_enable_local_txn` | Read-only [^10] |
| `tidb_enable_resource_control` | Read-only [^10] |
| `tidb_enable_slow_log` | Not supported [^4] |
| `tidb_enable_stmt_summary` | Read-only [^10] |
| `tidb_enable_telemetry` | Not supported [^4] |
| `tidb_enable_top_sql` | Read-only [^10] |
| `tidb_enable_tso_follower_proxy` | Read-only [^10] |
| `tidb_expensive_query_time_threshold` | Not supported [^4] |
| `tidb_force_priority` | Not supported [^4] |
| `tidb_gc_concurrency` | Read-only [^10] |
| `tidb_gc_enable` | Read-only [^10] |
| `tidb_gc_max_wait_time` | Read-only [^10] |
| `tidb_gc_run_interval` | Read-only [^10] |
| `tidb_gc_scan_lock_mode` | Read-only [^10] |
| `tidb_general_log` | Not supported [^4] |
| `tidb_generate_binary_plan` | Read-only [^10] |
| `tidb_gogc_tuner_threshold` | Read-only [^10] |
| `tidb_guarantee_linearizability` | Read-only [^10] |
| `tidb_isolation_read_engines` | Read-only [^10] |
| `tidb_log_file_max_days` | Read-only [^10] |
| `tidb_memory_usage_alarm_ratio` | Not supported [^4] |
| `tidb_metric_query_range_duration` | Not supported [^4] |
| `tidb_metric_query_step` | Not supported [^4] |
| `tidb_opt_write_row_id` | Not supported [^4] |
| `tidb_placement_mode` | Read-only [^10] |
| `tidb_pprof_sql_cpu` | Not supported [^4] |
| `tidb_record_plan_in_slow_log` | Not supported [^4] |
| `tidb_redact_log` | Not supported [^4] |
| `tidb_restricted_read_only` | Not supported [^4] |
| `tidb_row_format_version` | Not supported [^4] |
| `tidb_scatter_region` | Read-only [^10] |
| `tidb_server_memory_limit` | Read-only [^10] |
| `tidb_server_memory_limit_gc_trigger` | Read-only [^10] |
| `tidb_server_memory_limit_sess_min_size` | Read-only [^10] |
| `tidb_simplified_metrics` | Read-only [^10] |
| `tidb_slow_query_file` | Not supported [^4] |
| `tidb_slow_log_threshold` | Not supported [^4] |
| `tidb_slow_txn_log_threshold` | Not supported [^4] |
| `tidb_stats_load_sync_wait` | Read-only [^10] |
| `tidb_stmt_summary_history_size` | Read-only [^10] |
| `tidb_stmt_summary_internal_query` | Read-only [^10] |
| `tidb_stmt_summary_max_sql_length` | Read-only [^10] |
| `tidb_stmt_summary_max_stmt_count` | Read-only [^10] |
| `tidb_stmt_summary_refresh_interval` | Read-only [^10] |
| `tidb_sysproc_scan_concurrency` | Read-only [^10] |
| `tidb_top_sql_max_meta_count` | Not supported [^4] |
| `tidb_top_sql_max_time_series_count` | Not supported [^4] |
| `tidb_tso_client_batch_max_wait_time` | Read-only [^10] |
| `tidb_ttl_delete_batch_size` | Read-only [^10] |
| `tidb_ttl_delete_rate_limit` | Read-only [^10] |
| `tidb_ttl_delete_worker_count` | Read-only [^10] |
| `tidb_ttl_job_schedule_window_end_time` | Read-only [^10] |
| `tidb_ttl_job_schedule_window_start_time` | Read-only [^10] |
| `tidb_ttl_running_tasks` | Read-only [^10] |
| `tidb_ttl_scan_batch_size` | Read-only [^10] |
| `tidb_ttl_scan_worker_count` | Read-only [^10] |
| `tidb_txn_mode` | Read-only [^10] |
| `tidb_wait_split_region_finish` | Read-only [^10] |
| `tidb_wait_split_region_timeout` | Read-only [^10] |
| `txn_scope` | Read-only [^10] |
| `validate_password.enable` | Always enabled [^9] |
| `validate_password.length` | At least `8` [^9] |
| `validate_password.mixed_case_count` | At least `1` [^9] |
| `validate_password.number_count` | At least `1` [^9] |
| `validate_password.policy` | Can only be `MEDIUM` or `STRONG` [^9] |
| `validate_password.special_char_count` | At least `1` [^9] |
| `wait_timeout` | Read-only [^10] |

[^1]: Configuring data placement is not supported on TiDB Cloud Starter.

[^2]: Configuring resource groups is not supported on TiDB Cloud Starter.

[^3]: To perform [Back up and Restore](/tidb-cloud/backup-and-restore-serverless.md) operations on TiDB Cloud Starter, you can use the TiDB Cloud console instead.

[^4]: The feature is unavailable in [Security Enhanced Mode (SEM)](/system-variables.md#tidb_enable_enhanced_security).

[^5]: To track [Slow Query](/tidb-cloud/tune-performance.md#slow-query) on TiDB Cloud Starter, you can use the TiDB Cloud console instead.

[^6]: To perform [Statement Analysis](/tidb-cloud/tune-performance.md#statement-analysis) on TiDB Cloud Starter, you can use the TiDB Cloud console instead.

[^7]: Drainer and Pump are not supported on TiDB Cloud.

[^8]: Plugin is not supported on TiDB Cloud Starter.

[^9]: TiDB Cloud Starter enforces strong password policy.

[^10]: The variable is read-only on TiDB Cloud Starter.

[^11]: TiDB Cloud Starter does not support downloading the file exported by `PLAN REPLAYER` through `${tidb-server-status-port}` as in the [example](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#examples-of-exporting-cluster-information). Instead, TiDB Cloud Starter generates a [presigned URL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html) for you to download the file. Note that this URL remains valid for 10 hours after generation.
