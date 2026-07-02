---
title: TiDB X インスタンスで制限される SQL 機能
summary: TiDB X インスタンスで制限される SQL 機能について説明します。
---

# TiDB X インスタンスで制限される SQL 機能

TiDB X インスタンスは、[TiDB Xアーキテクチャ](/tidb-cloud/tidb-x-architecture.md) 上に構築されたサービス指向の TiDB Cloud オファリングであり、{{{ .starter }}}、Essential、Premium インスタンスなどが含まれます。

TiDB Cloud は TiDB がサポートするほぼすべてのワークロードに対応していますが、TiDB Self-Managed と TiDB Cloud の間には一部機能差があります。このドキュメントでは、TiDB Cloud Starter、Essential、Premium における SQL 機能の制限事項について説明します。TiDB Self-Managed と TiDB Cloud の機能差は継続的に解消されています。これらの不足している機能や機能性が必要な場合は、機能リクエストとして [contact us](/tidb-cloud/tidb-cloud-support.md) してください。

> **Note:**
>
> このドキュメントは {{{ .starter }}}、Essential、Premium にのみ適用されます。TiDB Cloud Dedicated については、[Limited SQL Features on TiDB Cloud Dedicated](/tidb-cloud/limited-sql-features.md) を参照してください。

## Statements {#statements}

### Placement と range 管理 {#placement-and-range-management}

| ステートメント | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `ALTER PLACEMENT POLICY` | サポートされていません [^1] | サポートされていません [^1] |
| `ALTER RANGE` | サポートされていません | サポートされていません |
| `CREATE PLACEMENT POLICY` | サポートされていません [^1] | サポートされていません [^1] |
| `DROP PLACEMENT POLICY` | サポートされていません [^1] | サポートされていません [^1] |
| `SHOW CREATE PLACEMENT POLICY` | サポートされていません [^1] | サポートされていません [^1] |
| `SHOW PLACEMENT` | サポートされていません [^1] | サポートされていません [^1] |
| `SHOW PLACEMENT FOR` | サポートされていません [^1] | サポートされていません [^1] |
| `SHOW PLACEMENT LABELS` | サポートされていません [^1] | サポートされていません [^1] |
| `SHOW TABLE REGIONS` | サポートされています | サポートされていません [^1] |
| `SPLIT REGION` | サポートされています | サポートされていません [^1] |

### リソースグループ {#resource-groups}

| Statement | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `ALTER RESOURCE GROUP` | サポートされていません [^2] | サポートされていません [^2] |
| `CALIBRATE RESOURCE` | サポートされていません [^2] | サポートされていません [^2] |
| `CREATE RESOURCE GROUP` | サポートされていません [^2] | サポートされていません [^2] |
| `DROP RESOURCE GROUP` | サポートされていません [^2] | サポートされていません [^2] |
| `SET RESOURCE GROUP` | サポートされていません [^2] | サポートされていません [^2] |
| `SHOW CREATE RESOURCE GROUP` | サポートされていません [^2] | サポートされていません [^2] |

### Others {#others}

| ステートメント | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `BACKUP` | サポートされていません [^3] | サポートされていません [^3] |
| `SHOW BACKUPS` | サポートされていません [^3] | サポートされていません [^3] |
| `RESTORE` | サポートされていません [^3] | サポートされていません [^3] |
| `SHOW RESTORES` | サポートされていません [^3] | サポートされていません [^3] |
| `BACKUP LOGS` | サポートされていません | サポートされていません |
| `STOP BACKUP LOGS` | サポートされていません | サポートされていません |
| `PAUSE BACKUP LOGS` | サポートされていません | サポートされていません |
| `RESUME BACKUP LOGS` | サポートされていません | サポートされていません |
| `SHOW BACKUP LOGS STATUS` | サポートされていません | サポートされていません |
| `SHOW BACKUP LOGS METADATA` | サポートされていません | サポートされていません |
| `PURGE BACKUP LOGS` | サポートされていません | サポートされていません |
| `SHOW BR JOB` | サポートされていません | サポートされていません |
| `SHOW BR JOB QUERY` | サポートされていません | サポートされていません |
| `CANCEL BR JOB` | サポートされていません | サポートされていません |
| `SHOW BACKUP META` | サポートされていません | サポートされていません |
| `RECOVER TABLE` | サポートされていません | サポートされていません |
| `ADMIN RESET TELEMETRY_ID` | サポートされています | Telemetry は {{{ .starter }}} または {{{ .essential }}} ではサポートされていません。 |
| `ADMIN SHOW TELEMETRY` | サポートされていません [^4] | サポートされていません [^4] |
| `ADMIN SHOW SLOW` | サポートされていません [^5] | サポートされていません [^5] |
| `ADMIN PLUGINS ENABLE` | サポートされていません [^8] | サポートされていません [^8] |
| `ADMIN PLUGINS DISABLE` | サポートされていません [^8] | サポートされていません [^8] |
| `ADMIN SET BDR ROLE` | サポートされていません | サポートされていません |
| `ADMIN SHOW BDR ROLE` | サポートされていません | サポートされていません |
| `ADMIN UNSET BDR ROLE` | サポートされていません | サポートされていません |
| `ADMIN REPAIR TABLE` | サポートされていません | サポートされていません |
| `ALTER INSTANCE` | サポートされていません | サポートされていません |
| `ALTER INSTANCE RELOAD TLS` | サポートされていません | {{{ .starter }}} と {{{ .essential }}} では TLS 証明書が自動的に更新されます。 |
| `ALTER TABLE ... ATTRIBUTES` | サポートされていません | サポートされていません |
| `CHANGE DRAINER` | サポートされていません [^7] | サポートされていません [^7] |
| `CHANGE PUMP` | サポートされていません [^7] | サポートされていません [^7] |
| `FLASHBACK CLUSTER` | サポートされていません [^3] | サポートされていません [^3] |
| `IMPORT INTO` | サポートされていますが、ローカルファイルパスまたは S3 EXTERNAL_ID を使用する IMPORT INTO ステートメントはブロックされます。 | サポートされていません |
| `LOAD DATA INFILE` | ローカルファイルパスからの `LOAD DATA LOCAL INFILE` はブロックされます。 | `LOAD DATA LOCAL INFILE` のみサポートされます |
| `LOAD STATS` | サポートされていません | サポートされていません |
| `SELECT ... INTO OUTFILE` | サポートされていません [^4] | サポートされていません [^4] |
| `SET CONFIG` | サポートされていません [^4] | サポートされていません [^4] |
| `SHOW CONFIG` | サポートされていません [^4] | サポートされていません [^4] |
| `SHOW DRAINER STATUS` | サポートされていません [^7] | サポートされていません [^7] |
| `SHOW PLUGINS` | サポートされていません [^8] | サポートされていません [^8] |
| `SHOW PUMP STATUS` | サポートされていません [^7] | サポートされていません [^7] |
| `SHUTDOWN` | サポートされていません [^4] | サポートされていません [^4] |
| `PLAN REPLAYER` | サポートされています | サポートされていますが、異なるファイルダウンロード方法を使用します [^11] |
| `time_to_live` | サポートされています | サポートされていません |

## Functions and operators {#functions-and-operators}

| Function and operator | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `SLEEP` | 制限はありません | [`SLEEP()` function](https://docs.pingcap.com/tidbcloud/miscellaneous-functions) 関数は、最大 300 秒のスリープ時間をサポートします。 |

## System tables {#system-tables}

| Database | Table | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|:-|
| `metrics_schema` | すべてのデータベース | サポートされていません | サポートされていません |
| `information_schema` | `ATTRIBUTES` | サポートされています | サポートされていません [^1] |
| `information_schema` | `CLUSTER_CONFIG` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `CLUSTER_HARDWARE` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `CLUSTER_INFO` | サポートされています | サポートされていません [^1] |
| `information_schema` | `CLUSTER_LOAD` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `CLUSTER_LOG` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `CLUSTER_SLOW_QUERY` | サポートされていません [^5] | サポートされていません [^5] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY` | サポートされています | サポートされていません [^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_EVICTED` | サポートされています | サポートされていません [^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_HISTORY` | サポートされています | サポートされていません [^6] |
| `information_schema` | `CLUSTER_SYSTEMINFO` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `INSPECTION_RESULT` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `INSPECTION_RULES` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `INSPECTION_SUMMARY` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `METRICS_SUMMARY` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `METRICS_SUMMARY_BY_LABEL` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `METRICS_TABLES` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `PLACEMENT_POLICIES` | サポートされていません [^1] | サポートされていません [^1] |
| `information_schema` | `RESOURCE_GROUPS` | サポートされていません [^2] | サポートされていません [^2] |
| `information_schema` | `SLOW_QUERY` | サポートされていません [^5] | サポートされていません [^5] |
| `information_schema` | `STATEMENTS_SUMMARY` | サポートされています | サポートされていません [^6] |
| `information_schema` | `STATEMENTS_SUMMARY_EVICTED` | サポートされています | サポートされていません [^6] |
| `information_schema` | `TIDB_HOT_REGIONS` | サポートされていません [^4] | サポートされていません [^4] |
| `information_schema` | `TIDB_HOT_REGIONS_HISTORY` | サポートされています | サポートされていません [^1] |
| `information_schema` | `TIDB_SERVERS_INFO` | サポートされています | サポートされていません [^1] |
| `information_schema` | `TIKV_REGION_PEERS` | サポートされています | サポートされていません [^1] |
| `information_schema` | `TIKV_REGION_STATUS` | サポートされています | サポートされていません [^1] |
| `information_schema` | `TIKV_STORE_STATUS` | サポートされています | サポートされていません [^1] |
| `performance_schema` | `pd_profile_allocs` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `pd_profile_block` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `pd_profile_cpu` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `pd_profile_goroutines` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `pd_profile_memory` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `pd_profile_mutex` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `tidb_profile_allocs` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `tidb_profile_block` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `tidb_profile_cpu` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `tidb_profile_goroutines` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `tidb_profile_memory` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `tidb_profile_mutex` | サポートされていません [^4] | サポートされていません [^4] |
| `performance_schema` | `tikv_profile_cpu` | サポートされていません [^4] | サポートされていません [^4] |
| `mysql` | `expr_pushdown_blacklist` | サポートされていません [^4] | サポートされていません [^4] |
| `mysql` | `gc_delete_range` | サポートされていません [^4] | サポートされていません [^4] |
| `mysql` | `gc_delete_range_done` | サポートされていません [^4] | サポートされていません [^4] |
| `mysql` | `opt_rule_blacklist` | サポートされていません [^4] | サポートされていません [^4] |
| `mysql` | `tidb` | サポートされていません [^4] | サポートされていません [^4] |

## System variables {#system-variables}

| Variable | {{{ .premium }}} | {{{ .starter }}} and {{{ .essential }}} |
|:-|:-|:-|
| `hostname` | 値は非表示です | 値は非表示です |
| `datadir` | 値は非表示です | サポートされていません [^1] |
| `ddl_slow_threshold` | 読み取り専用 | 読み取り専用 |
| `block_encryption_mode` | 読み取り専用 | 読み取り専用 |
| `max_connections` | 読み取り専用 | 読み取り専用 |
| `mpp_version` | 読み取り専用 | 読み取り専用 |
| `interactive_timeout` | 制限はありません | 読み取り専用 [^10] |
| `max_allowed_packet` | 制限はありません | 読み取り専用 [^10] |
| `plugin_dir` | サポートされていません [^8] | サポートされていません [^8] |
| `plugin_load` | サポートされていません [^8] | サポートされていません [^8] |
| `require_secure_transport` | サポートされていません | 読み取り専用 [^10] |
| `skip_name_resolve` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `sql_log_bin` | 制限はありません | 読み取り専用 [^10] |
| `tidb_adaptive_closest_read_threshold` | サポートされていません | サポートされていません |
| `tidb_allow_batch_cop` | 読み取り専用 | 読み取り専用 |
| `tidb_allow_mpp` | 読み取り専用 | 読み取り専用 |
| `tidb_analyze_skip_column_types` | 制限はありません | 読み取り専用 [^10] |
| `tidb_analyze_version` | 読み取り専用 | 読み取り専用 |
| `tidb_backoff_lock_fast` | 読み取り専用 | 読み取り専用 |
| `tidb_backoff_weight` | 読み取り専用 | 読み取り専用 |
| `tidb_batch_commit` | サポートされていません | サポートされていません |
| `tidb_batch_delete` | サポートされていません | サポートされていません |
| `tidb_batch_insert` | サポートされていません | サポートされていません |
| `tidb_capture_plan_baselines` | 読み取り専用 | 読み取り専用 |
| `tidb_cdc_write_source` | 制限はありません | 読み取り専用 [^10] |
| `tidb_check_mb4_value_in_utf8` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_cloud_storage_uri` | サポートされていません | サポートされていません |
| `tidb_config` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_constraint_check_in_place` | 読み取り専用 | 読み取り専用 |
| `tidb_constraint_check_in_place_pessimistic` | 読み取り専用 | 読み取り専用 |
| `tidb_cost_model_version` | 読み取り専用 | 読み取り専用 |
| `tidb_ddl_disk_quota` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_ddl_enable_fast_reorg` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_ddl_error_count_limit` | 制限はありません | 読み取り専用 [^10] |
| `tidb_ddl_flashback_concurrency` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_ddl_reorg_batch_size` | 制限はありません | 読み取り専用 [^10] |
| `tidb_ddl_reorg_max_write_speed` | サポートされていません | サポートされていません |
| `tidb_ddl_reorg_priority` | 制限はありません | 読み取り専用 [^10] |
| `tidb_ddl_reorg_worker_cnt` | 制限はありません | 読み取り専用 [^10] |
| `tidb_disable_txn_auto_retry` | サポートされていません | サポートされていません |
| `tidb_dml_batch_size` | サポートされていません | サポートされていません |
| `tidb_dml_type` | サポートされていません | 読み取り専用 [^10] |
| `tidb_enable_1pc` | 制限はありません | 読み取り専用 [^10] |
| `tidb_enable_analyze_snapshot` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_async_commit` | 制限はありません | 読み取り専用 [^10] |
| `tidb_enable_async_merge_global_stats` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_auto_analyze` | 制限はありません | 読み取り専用 [^10] |
| `tidb_enable_batch_dml` | サポートされていません | サポートされていません |
| `tidb_enable_chunk_rpc` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_collect_execution_info` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_enable_column_tracking` | サポートされていません | サポートされていません |
| `tidb_enable_ddl` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_enable_dist_task` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_exchange_partition` | サポートされていません | サポートされていません |
| `tidb_enable_extended_stats` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_fast_analyze` | サポートされていません | サポートされていません |
| `tidb_enable_gc_aware_memory_track` | 制限はありません | 読み取り専用 [^10] |
| `tidb_enable_global_index` | サポートされていません | サポートされていません |
| `tidb_enable_gogc_tuner` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_enable_historical_stats` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_historical_stats_for_capture` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_legacy_instance_scope` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_list_partition` | サポートされていません | サポートされていません |
| `tidb_enable_local_txn` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_enable_metadata_lock` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_mutation_checker` | 読み取り専用 | サポートされていません |
| `tidb_enable_new_cost_interface` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_parallel_hashagg_spill` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_pipelined_window_function` | 制限はありません | サポートされていません |
| `tidb_enable_plan_replayer_capture` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_plan_replayer_continuous_capture` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_point_get_cache` | サポートされていません | サポートされていません |
| `tidb_enable_rate_limit_action` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_resource_control` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_enable_reuse_chunk` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_slow_log` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_enable_stats_owner` | 読み取り専用 | 読み取り専用 |
| `tidb_enable_stmt_summary` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_enable_table_partition` | サポートされていません | サポートされていません |
| `tidb_enable_telemetry` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_enable_tiflash_read_for_write_stmt` | サポートされていません | サポートされていません |
| `tidb_enable_tmp_storage_on_oom` | サポートされていません | サポートされていません |
| `tidb_enable_top_sql` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_enable_tso_follower_proxy` | 制限はありません | 読み取り専用 [^10] |
| `tidb_enable_vectorized_expression` | 読み取り専用 | 読み取り専用 |
| `tidb_evolve_plan_baselines` | サポートされていません | サポートされていません |
| `tidb_evolve_plan_task_end_time` | サポートされていません | サポートされていません |
| `tidb_evolve_plan_task_max_time` | サポートされていません | サポートされていません |
| `tidb_evolve_plan_task_start_time` | サポートされていません | サポートされていません |
| `tidb_expensive_query_time_threshold` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_force_priority` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_gc_concurrency` | 制限はありません | 読み取り専用 [^10] |
| `tidb_gc_enable` | 制限はありません | 読み取り専用 [^10] |
| `tidb_gc_leader_desc` | サポートされていません | サポートされていません |
| `tidb_gc_max_wait_time` | 制限はありません | 読み取り専用 [^10] |
| `tidb_gc_run_interval` | 制限はありません | 読み取り専用 [^10] |
| `tidb_gc_scan_lock_mode` | 制限はありません | 読み取り専用 [^10] |
| `tidb_general_log` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_generate_binary_plan` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_gogc_tuner_threshold` | 制限はありません | 読み取り専用 [^10] |
| `tidb_guarantee_linearizability` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_hash_exchange_with_new_collation` | 読み取り専用 | 読み取り専用 |
| `tidb_historical_stats_duration` | サポートされていません | サポートされていません |
| `tidb_isolation_read_engines` | 制限はありません | 読み取り専用 [^10] |
| `tidb_load_based_replica_read_threshold` | 読み取り専用 | 読み取り専用 |
| `tidb_lock_unchanged_keys` | 読み取り専用 | 読み取り専用 |
| `tidb_log_file_max_days` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_mem_oom_action` | 読み取り専用 | 読み取り専用 |
| `tidb_mem_quota_analyze` | 読み取り専用 | 読み取り専用 |
| `tidb_memory_debug_mode_alarm_ratio` | サポートされていません | サポートされていません |
| `tidb_memory_debug_mode_min_heap_inuse` | サポートされていません | サポートされていません |
| `tidb_memory_usage_alarm_keep_record_num` | 読み取り専用 | 読み取り専用 |
| `tidb_memory_usage_alarm_ratio` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_merge_join_concurrency` | サポートされていません | サポートされていません |
| `tidb_metric_query_range_duration` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_metric_query_step` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_non_prepared_plan_cache_size` | サポートされていません | サポートされていません |
| `tidb_opt_broadcast_cartesian_join` | 読み取り専用 | 読み取り専用 |
| `tidb_opt_concurrency_factor` | 読み取り専用 | 読み取り専用 |
| `tidb_opt_copcpu_factor` | 読み取り専用 | 読み取り専用 |
| `tidb_opt_write_row_id` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_partition_prune_mode` | サポートされていません | サポートされていません |
| `tidb_pessimistic_txn_fair_locking` | サポートされていません | サポートされていません |
| `tidb_placement_mode` | 制限はありません | 読み取り専用 [^10] |
| `tidb_pprof_sql_cpu` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_pre_split_regions` | 読み取り専用 | 読み取り専用 |
| `tidb_prepared_plan_cache_size` | サポートされていません | 読み取り専用 |
| `tidb_rc_read_check_ts` | 読み取り専用 | 読み取り専用 |
| `tidb_rc_write_check_ts` | 読み取り専用 | 読み取り専用 |
| `tidb_read_consistency` | 読み取り専用 | 読み取り専用 |
| `tidb_record_plan_in_slow_log` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_redact_log` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_replica_read` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_request_source_type` | サポートされていません | サポートされていません |
| `tidb_restricted_read_only` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_retry_limit` | サポートされていません | サポートされていません |
| `tidb_row_format_version` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_scatter_region` | 制限はありません | 読み取り専用 [^10] |
| `tidb_server_memory_limit` | 制限はありません | 読み取り専用 [^10] |
| `tidb_server_memory_limit_gc_trigger` | 制限はありません | 読み取り専用 [^10] |
| `tidb_server_memory_limit_sess_min_size` | 制限はありません | 読み取り専用 [^10] |
| `tidb_service_scope` | 読み取り専用 | 読み取り専用 |
| `tidb_simplified_metrics` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_skip_missing_partition_stats` | 読み取り専用 | 読み取り専用 |
| `tidb_slow_log_threshold` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_slow_query_file` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_slow_txn_log_threshold` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_stats_load_pseudo_timeout` | 読み取り専用 | 読み取り専用 |
| `tidb_stats_load_sync_wait` | 制限はありません | 読み取り専用 [^10] |
| `tidb_stmt_summary_enable_persistent` | 読み取り専用 | 読み取り専用 |
| `tidb_stmt_summary_file_max_backups` | 読み取り専用 | 読み取り専用 |
| `tidb_stmt_summary_file_max_days` | 読み取り専用 | 読み取り専用 |
| `tidb_stmt_summary_file_max_size` | 読み取り専用 | 読み取り専用 |
| `tidb_stmt_summary_filename` | 読み取り専用 | 読み取り専用 |
| `tidb_stmt_summary_history_size` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_stmt_summary_internal_query` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_stmt_summary_max_sql_length` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_stmt_summary_max_stmt_count` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_stmt_summary_refresh_interval` | 読み取り専用 [^10] | 読み取り専用 [^10] |
| `tidb_store_limit` | 読み取り専用 | 読み取り専用 |
| `tidb_streamagg_concurrency` | サポートされていません | 読み取り専用 |
| `tidb_sysproc_scan_concurrency` | 制限はありません | 読み取り専用 [^10] |
| `tidb_top_sql_max_meta_count` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_top_sql_max_time_series_count` | サポートされていません [^4] | サポートされていません [^4] |
| `tidb_track_aggregate_memory_usage` | 読み取り専用 | 読み取り専用 |
| `tidb_txn_assertion_level` | 読み取り専用 | 読み取り専用 |
| `tidb_txn_commit_batch_size` | 読み取り専用 | 読み取り専用 |
| `tidb_tso_client_batch_max_wait_time` | 制限はありません | 読み取り専用 [^10] |
| `tidb_ttl_delete_batch_size` | 制限はありません | 読み取り専用 [^10] |
| `tidb_ttl_delete_rate_limit` | 制限はありません | 読み取り専用 [^10] |
| `tidb_ttl_delete_worker_count` | 制限はありません | 読み取り専用 [^10] |
| `tidb_ttl_job_schedule_window_end_time` | 制限はありません | 読み取り専用 [^10] |
| `tidb_ttl_job_schedule_window_start_time` | 制限はありません | 読み取り専用 [^10] |
| `tidb_ttl_running_tasks` | 制限はありません | 読み取り専用 [^10] |
| `tidb_ttl_scan_batch_size` | 制限はありません | 読み取り専用 [^10] |
| `tidb_ttl_scan_worker_count` | 制限はありません | 読み取り専用 [^10] |
| `tidb_txn_mode` | 制限はありません | 読み取り専用 [^10] |
| `tidb_use_plan_baselines` | 読み取り専用 | 読み取り専用 |
| `tidb_wait_split_region_finish` | 制限はありません | 読み取り専用 [^10] |
| `tidb_wait_split_region_timeout` | 制限はありません | 読み取り専用 [^10] |
| `tiflash_compute_dispatch_policy` | 読み取り専用 | 読み取り専用 |
| `tiflash_replica_read` | サポートされていません | サポートされていません |
| `tikv_client_read_timeout` | サポートされていません | サポートされていません |
| `tx_isolation_one_shot` | サポートされていません | サポートされていません |
| `tx_read_ts` | サポートされていません | サポートされていません |
| `txn_scope` | 制限はありません | 読み取り専用 [^10] |
| `validate_password.enable` | 制限はありません | 常に有効です [^9] |
| `validate_password.length` | 制限はありません | 少なくとも `8` [^9] |
| `validate_password.mixed_case_count` | 制限はありません | 少なくとも `1` [^9] |
| `validate_password.number_count` | 制限はありません | 少なくとも `1` [^9] |
| `validate_password.policy` | 制限はありません | `MEDIUM` または `STRONG` のみ指定できます [^9] |
| `validate_password.special_char_count` | 制限はありません | 少なくとも `1` [^9] |
| `wait_timeout` | 制限はありません | 読み取り専用 [^10] |

[^1]: データ配置の設定は {{{ .starter }}}、Essential、Premium ではサポートされていません。

[^2]: リソースグループの設定は {{{ .starter }}}、Essential、Premium ではサポートされていません。

[^3]: {{{ .starter }}}、Essential、Premium で [Back up and Restore](/tidb-cloud/backup-and-restore-serverless.md) 操作を実行するには、代わりに TiDB Cloud コンソールを使用できます。

[^4]: この機能は [Security Enhanced Mode (SEM)](/system-variables.md#tidb_enable_enhanced_security) では利用できません。

[^5]: {{{ .starter }}}、Essential、Premium で [Slow Query](/tidb-cloud/tune-performance.md#slow-query) を追跡するには、代わりに TiDB Cloud コンソールを使用できます。

[^6]: {{{ .starter }}} または {{{ .essential }}} で [Statement Analysis](/tidb-cloud/tune-performance.md#statement-analysis) を実行するには、代わりに TiDB Cloud コンソールを使用できます。

[^7]: Drainer と Pump は TiDB Cloud ではサポートされていません。

[^8]: プラグインは {{{ .starter }}}、Essential、Premium ではサポートされていません。

[^9]: {{{ .starter }}} と {{{ .essential }}} では強力なパスワードポリシーが適用されます。

[^10]: この変数は {{{ .starter }}} と {{{ .essential }}} では読み取り専用です。

[^11]: {{{ .starter }}} と {{{ .essential }}} では、[example](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#examples-of-exporting-cluster-information) に示されているように、`${tidb-server-status-port}` を介して `PLAN REPLAYER` がエクスポートしたファイルをダウンロードすることはサポートされていません。代わりに、{{{ .starter }}} と {{{ .essential }}} では、ファイルをダウンロードするための [presigned URL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html) が生成されます。この URL は生成後 10 時間有効です。