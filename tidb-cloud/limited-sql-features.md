---
title: Limited SQL Features on TiDB Cloud Dedicated
summary: TiDB Cloud Dedicatedの制限された SQL 機能について説明します。
---

# TiDB Cloud Dedicatedの SQL 機能が制限されている {#limited-sql-features-on-tidb-cloud-dedicated}

TiDB Cloud Dedicated はTiDB がサポートするほぼすべてのワークロードで動作しますが、TiDB Self-Managed とTiDB Cloud Dedicatedには機能面で若干の違いがあります。このドキュメントでは、TiDB Cloud Dedicatedにおける SQL 機能の制限事項について説明します。TiDB Self-Managed とTiDB Cloud Dedicatedの機能ギャップは継続的に埋められています。これらの機能やギャップを埋める必要がある場合は、機能リクエストを送信して[お問い合わせ](/tidb-cloud/tidb-cloud-support.md) 。

> **注記：**
>
> このドキュメントは TiDB Cloud Dedicated にのみ適用されます。TiDB Cloud Starter、Essential、Premium については、[TiDB X インスタンスで制限される SQL 機能](/tidb-cloud/limited-sql-features-tidb-x.md) を参照してください。

## ステートメント {#statements}

### 配置と範囲管理 {#placement-and-range-management}

| ステートメント                             | TiDB Cloud Dedicated |
| :----------------------------- | :----------- |
| `ALTER PLACEMENT POLICY`       | サポートされている    |
| `CREATE PLACEMENT POLICY`      | サポートされている    |
| `DROP PLACEMENT POLICY`        | サポートされている    |
| `SHOW CREATE PLACEMENT POLICY` | サポートされている    |
| `SHOW PLACEMENT`               | サポートされている    |
| `SHOW PLACEMENT FOR`           | サポートされている    |
| `SHOW PLACEMENT LABELS`        | サポートされている    |
| `SHOW TABLE REGIONS`           | サポートされている    |
| `SPLIT REGION`                 | サポートされている    |

### リソースグループ {#resource-groups}

| ステートメント                           | TiDB Cloud Dedicated |
| :--------------------------- | :----------- |
| `ALTER RESOURCE GROUP`       | サポートされている    |
| `CALIBRATE RESOURCE`         | サポートされていません  |
| `CREATE RESOURCE GROUP`      | サポートされている    |
| `DROP RESOURCE GROUP`        | サポートされている    |
| `SET RESOURCE GROUP`         | サポートされている    |
| `SHOW CREATE RESOURCE GROUP` | サポートされている    |

### その他 {#others}

| ステートメント                          | TiDB Cloud Dedicated                                                                         |
| :-------------------------- | :----------------------------------------------------------------------------------- |
| `BACKUP`                    | サポートされている                                                                            |
| `SHOW BACKUPS`              | サポートされている                                                                            |
| `RESTORE`                   | サポートされている                                                                            |
| `SHOW RESTORES`             | サポートされている                                                                            |
| `ADMIN RESET TELEMETRY_ID`  | サポートされている                                                                            |
| `ADMIN SHOW TELEMETRY`      | サポートされていません[^1]                                                                      |
| `ADMIN SHOW SLOW`           | サポートされている                                                                            |
| `ADMIN PLUGINS ENABLE`      | サポートされている                                                                            |
| `ADMIN PLUGINS DISABLE`     | サポートされている                                                                            |
| `ALTER INSTANCE RELOAD TLS` | サポートされている                                                                            |
| `LOAD DATA INFILE`          | Amazon S3 または Google Cloud Storage から`LOAD DATA LOCAL INFILE` `LOAD DATA INFILE`サポート |
| `CHANGE DRAINER`            | サポートされていません[^2]                                                                      |
| `CHANGE PUMP`               | サポートされていません[^2]                                                                      |
| `FLASHBACK CLUSTER`         | サポートされている                                                                            |
| `LOAD STATS`                | サポートされている                                                                            |
| `SELECT ... INTO OUTFILE`   | サポートされていません[^1]                                                                      |
| `SET CONFIG`                | サポートされていません[^1]                                                                      |
| `SHOW CONFIG`               | サポートされていません[^1]                                                                      |
| `SHOW DRAINER STATUS`       | サポートされていません[^2]                                                                      |
| `SHOW PLUGINS`              | サポートされている                                                                            |
| `SHOW PUMP STATUS`          | サポートされていません[^2]                                                                      |
| `SHUTDOWN`                  | サポートされていません[^1]                                                                      |
| `PLAN REPLAYER`             | サポートされている                                                                            |

## 関数と演算子 {#functions-and-operators}

| 関数と演算子  | TiDB Cloud Dedicated |
| :------ | :----------- |
| `SLEEP` | 制限なし         |

## システムテーブル {#system-tables}

| データベース               | テーブル                                 | TiDB Cloud Dedicated    |
| :------------------- | :----------------------------------- | :-------------- |
| `information_schema` | `ATTRIBUTES`                         | サポートされている       |
| `information_schema` | `CLUSTER_CONFIG`                     | サポートされていません[^1] |
| `information_schema` | `CLUSTER_HARDWARE`                   | サポートされていません[^1] |
| `information_schema` | `CLUSTER_INFO`                       | サポートされている       |
| `information_schema` | `CLUSTER_LOAD`                       | サポートされていません[^1] |
| `information_schema` | `CLUSTER_LOG`                        | サポートされていません[^1] |
| `information_schema` | `CLUSTER_SLOW_QUERY`                 | サポートされている       |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY`         | サポートされている       |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_EVICTED` | サポートされている       |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_HISTORY` | サポートされている       |
| `information_schema` | `CLUSTER_SYSTEMINFO`                 | サポートされていません[^1] |
| `information_schema` | `INSPECTION_RESULT`                  | サポートされていません[^1] |
| `information_schema` | `INSPECTION_RULES`                   | サポートされていません[^1] |
| `information_schema` | `INSPECTION_SUMMARY`                 | サポートされていません[^1] |
| `information_schema` | `METRICS_SUMMARY`                    | サポートされていません[^1] |
| `information_schema` | `METRICS_SUMMARY_BY_LABEL`           | サポートされていません[^1] |
| `information_schema` | `METRICS_TABLES`                     | サポートされていません[^1] |
| `information_schema` | `PLACEMENT_POLICIES`                 | サポートされている       |
| `information_schema` | `RESOURCE_GROUPS`                    | サポートされている       |
| `information_schema` | `SLOW_QUERY`                         | サポートされている       |
| `information_schema` | `STATEMENTS_SUMMARY`                 | サポートされている       |
| `information_schema` | `STATEMENTS_SUMMARY_EVICTED`         | サポートされている       |
| `information_schema` | `TIDB_HOT_REGIONS`                   | サポートされていません[^1] |
| `information_schema` | `TIDB_HOT_REGIONS_HISTORY`           | サポートされている       |
| `information_schema` | `TIDB_SERVERS_INFO`                  | サポートされている       |
| `information_schema` | `TIKV_REGION_PEERS`                  | サポートされている       |
| `information_schema` | `TIKV_REGION_STATUS`                 | サポートされている       |
| `information_schema` | `TIKV_STORE_STATUS`                  | サポートされている       |
| `performance_schema` | `pd_profile_allocs`                  | サポートされていません[^1] |
| `performance_schema` | `pd_profile_block`                   | サポートされていません[^1] |
| `performance_schema` | `pd_profile_cpu`                     | サポートされていません[^1] |
| `performance_schema` | `pd_profile_goroutines`              | サポートされていません[^1] |
| `performance_schema` | `pd_profile_memory`                  | サポートされていません[^1] |
| `performance_schema` | `pd_profile_mutex`                   | サポートされていません[^1] |
| `performance_schema` | `tidb_profile_allocs`                | サポートされていません[^1] |
| `performance_schema` | `tidb_profile_block`                 | サポートされていません[^1] |
| `performance_schema` | `tidb_profile_cpu`                   | サポートされていません[^1] |
| `performance_schema` | `tidb_profile_goroutines`            | サポートされていません[^1] |
| `performance_schema` | `tidb_profile_memory`                | サポートされていません[^1] |
| `performance_schema` | `tidb_profile_mutex`                 | サポートされていません[^1] |
| `performance_schema` | `tikv_profile_cpu`                   | サポートされていません[^1] |
| `mysql`              | `expr_pushdown_blacklist`            | サポートされていません[^1] |
| `mysql`              | `gc_delete_range`                    | サポートされていません[^1] |
| `mysql`              | `gc_delete_range_done`               | サポートされていません[^1] |
| `mysql`              | `opt_rule_blacklist`                 | サポートされていません[^1] |
| `mysql`              | `tidb`                               | サポートされていません[^1] |

## システム変数 {#system-variables}

| 変数                                        | TiDB Cloud Dedicated     |
| :---------------------------------------- | :--------------- |
| `datadir`                                 | 制限なし             |
| `interactive_timeout`                     | 制限なし             |
| `max_allowed_packet`                      | 制限なし             |
| `plugin_dir`                              | 制限なし             |
| `plugin_load`                             | 制限なし             |
| `require_secure_transport`                | サポートされていません[^3] |
| `skip_name_resolve`                       | 制限なし             |
| `sql_log_bin`                             | 制限なし             |
| `tidb_analyze_skip_column_types`          | 制限なし             |
| `tidb_cdc_write_source`                   | 制限なし             |
| `tidb_check_mb4_value_in_utf8`            | サポートされていません[^1]  |
| `tidb_config`                             | サポートされていません[^1]  |
| `tidb_ddl_disk_quota`                     | 制限なし             |
| `tidb_ddl_enable_fast_reorg`              | 制限なし             |
| `tidb_ddl_error_count_limit`              | 制限なし             |
| `tidb_ddl_flashback_concurrency`          | 制限なし             |
| `tidb_ddl_reorg_batch_size`               | 制限なし             |
| `tidb_ddl_reorg_priority`                 | 制限なし             |
| `tidb_ddl_reorg_worker_cnt`               | 制限なし             |
| `tidb_dml_type`                           | 制限なし             |
| `tidb_enable_1pc`                         | 制限なし             |
| `tidb_enable_async_commit`                | 制限なし             |
| `tidb_enable_auto_analyze`                | 制限なし             |
| `tidb_enable_collect_execution_info`      | サポートされていません[^1]  |
| `tidb_enable_ddl`                         | 制限なし             |
| `tidb_enable_gc_aware_memory_track`       | 制限なし             |
| `tidb_enable_gogc_tuner`                  | 制限なし             |
| `tidb_enable_local_txn`                   | 制限なし             |
| `tidb_enable_resource_control`            | 制限なし             |
| `tidb_enable_slow_log`                    | サポートされていません[^1]  |
| `tidb_enable_stmt_summary`                | 制限なし             |
| `tidb_enable_telemetry`                   | サポートされていません[^1]  |
| `tidb_enable_top_sql`                     | 制限なし             |
| `tidb_enable_tso_follower_proxy`          | 制限なし             |
| `tidb_expensive_query_time_threshold`     | サポートされていません[^1]  |
| `tidb_force_priority`                     | サポートされていません[^1]  |
| `tidb_gc_concurrency`                     | 制限なし             |
| `tidb_gc_enable`                          | 制限なし             |
| `tidb_gc_max_wait_time`                   | 制限なし             |
| `tidb_gc_run_interval`                    | 制限なし             |
| `tidb_gc_scan_lock_mode`                  | 制限なし             |
| `tidb_general_log`                        | サポートされていません[^1]  |
| `tidb_generate_binary_plan`               | 制限なし             |
| `tidb_gogc_tuner_threshold`               | 制限なし             |
| `tidb_guarantee_linearizability`          | 制限なし             |
| `tidb_isolation_read_engines`             | 制限なし             |
| `tidb_log_file_max_days`                  | 制限なし             |
| `tidb_memory_usage_alarm_ratio`           | サポートされていません[^1]  |
| `tidb_metric_query_range_duration`        | サポートされていません[^1]  |
| `tidb_metric_query_step`                  | サポートされていません[^1]  |
| `tidb_opt_write_row_id`                   | サポートされていません[^1]  |
| `tidb_placement_mode`                     | 制限なし             |
| `tidb_pprof_sql_cpu`                      | サポートされていません[^1]  |
| `tidb_record_plan_in_slow_log`            | サポートされていません[^1]  |
| `tidb_redact_log`                         | サポートされていません[^1]  |
| `tidb_replica_read`                       | 制限なし             |
| `tidb_restricted_read_only`               | サポートされていません[^1]  |
| `tidb_row_format_version`                 | サポートされていません[^1]  |
| `tidb_scatter_region`                     | 制限なし             |
| `tidb_server_memory_limit`                | 制限なし             |
| `tidb_server_memory_limit_gc_trigger`     | 制限なし             |
| `tidb_server_memory_limit_sess_min_size`  | 制限なし             |
| `tidb_simplified_metrics`                 | 制限なし             |
| `tidb_slow_query_file`                    | サポートされていません[^1]  |
| `tidb_slow_log_threshold`                 | サポートされていません[^1]  |
| `tidb_slow_txn_log_threshold`             | サポートされていません[^1]  |
| `tidb_stats_load_sync_wait`               | 制限なし             |
| `tidb_stmt_summary_history_size`          | 制限なし             |
| `tidb_stmt_summary_internal_query`        | 制限なし             |
| `tidb_stmt_summary_max_sql_length`        | 制限なし             |
| `tidb_stmt_summary_max_stmt_count`        | 制限なし             |
| `tidb_stmt_summary_refresh_interval`      | 制限なし             |
| `tidb_sysproc_scan_concurrency`           | 制限なし             |
| `tidb_top_sql_max_meta_count`             | サポートされていません[^1]  |
| `tidb_top_sql_max_time_series_count`      | サポートされていません[^1]  |
| `tidb_tso_client_batch_max_wait_time`     | 制限なし             |
| `tidb_ttl_delete_batch_size`              | 制限なし             |
| `tidb_ttl_delete_rate_limit`              | 制限なし             |
| `tidb_ttl_delete_worker_count`            | 制限なし             |
| `tidb_ttl_job_schedule_window_end_time`   | 制限なし             |
| `tidb_ttl_job_schedule_window_start_time` | 制限なし             |
| `tidb_ttl_running_tasks`                  | 制限なし             |
| `tidb_ttl_scan_batch_size`                | 制限なし             |
| `tidb_ttl_scan_worker_count`              | 制限なし             |
| `tidb_txn_mode`                           | 制限なし             |
| `tidb_wait_split_region_finish`           | 制限なし             |
| `tidb_wait_split_region_timeout`          | 制限なし             |
| `txn_scope`                               | 制限なし             |
| `validate_password.enable`                | 制限なし             |
| `validate_password.length`                | 制限なし             |
| `validate_password.mixed_case_count`      | 制限なし             |
| `validate_password.number_count`          | 制限なし             |
| `validate_password.policy`                | 制限なし             |
| `validate_password.special_char_count`    | 制限なし             |
| `wait_timeout`                            | 制限なし             |

[^1]: この機能は[セキュリティ強化モード（SEM）](/system-variables.md#tidb_enable_enhanced_security)では利用できません。

[^2]: DrainerとPump はTiDB Cloudではサポートされていません。

[^3]: サポートされていません。TiDB Cloud Dedicated クラスターで`require_secure_transport`有効にすると、SQL クライアント接続が失敗します。
