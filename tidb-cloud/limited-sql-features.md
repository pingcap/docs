---
title: Limited SQL Features on TiDB Cloud
summary: Learn about the limited SQL features on TiDB Cloud.
---

# TiDB Cloud上の制限された SQL 機能 {#limited-sql-features-on-tidb-cloud}

TiDB Cloud は、 TiDB がサポートするほぼすべてのワークロードで動作しますが、TiDB セルフホストと TiDB 専用/サーバーレスの間には機能の違いがいくつかあります。このドキュメントでは、 TiDB Cloud上の SQL 機能の制限について説明します。私たちは常に、TiDB セルフホスト型と TiDB 専用/サーバーレス間の機能ギャップを埋めています。これらの機能またはギャップ内の機能が必要な場合は、機能リクエストの場合は[お問い合わせ](/tidb-cloud/tidb-cloud-support.md) 。

## ステートメント {#statements}

### 配置と範囲管理 {#placement-and-range-management}

| 声明                             | TiDB専用     | TiDB サーバーレス     |
| :----------------------------- | :--------- | :-------------- |
| `ALTER PLACEMENT POLICY`       | サポートされています | サポートされていません[^1] |
| `CREATE PLACEMENT POLICY`      | サポートされています | サポートされていません[^1] |
| `DROP PLACEMENT POLICY`        | サポートされています | サポートされていません[^1] |
| `SHOW CREATE PLACEMENT POLICY` | サポートされています | サポートされていません[^1] |
| `SHOW PLACEMENT`               | サポートされています | サポートされていません[^1] |
| `SHOW PLACEMENT FOR`           | サポートされています | サポートされていません[^1] |
| `SHOW PLACEMENT LABELS`        | サポートされています | サポートされていません[^1] |
| `SHOW TABLE REGIONS`           | サポートされています | サポートされていません[^1] |
| `SPLIT REGION`                 | サポートされています | サポートされていません[^1] |

### リソースグループ {#resource-groups}

| 声明                           | TiDB専用      | TiDB サーバーレス     |
| :--------------------------- | :---------- | :-------------- |
| `ALTER RESOURCE GROUP`       | サポートされています  | サポートされていません[^2] |
| `CALIBRATE RESOURCE`         | サポートされていません | サポートされていません[^2] |
| `CREATE RESOURCE GROUP`      | サポートされています  | サポートされていません[^2] |
| `DROP RESOURCE GROUP`        | サポートされています  | サポートされていません[^2] |
| `SET RESOURCE GROUP`         | サポートされています  | サポートされていません[^2] |
| `SHOW CREATE RESOURCE GROUP` | サポートされています  | サポートされていません[^2] |

### その他 {#others}

| 声明                               | TiDB専用                         | TiDB サーバーレス                      |
| :------------------------------- | :----------------------------- | :------------------------------- |
| `BACKUP`                         | サポートされています                     | サポートされていません[^3]                  |
| `SHOW BACKUPS`                   | サポートされています                     | サポートされていません[^3]                  |
| `RESTORE`                        | サポートされています                     | サポートされていません[^3]                  |
| `SHOW RESTORES`                  | サポートされています                     | サポートされていません[^3]                  |
| `ADMIN RESET TELEMETRY_ID`       | サポートされています                     | テレメトリは TiDB サーバーレスではサポートされていません。 |
| `ADMIN SHOW TELEMETRY`           | サポートされていません[^4]                | サポートされていません[^4]                  |
| `ADMIN SHOW SLOW`                | サポートされています                     | サポートされていません[^5]                  |
| `ADMIN PLUGINS ENABLE`           | サポートされています                     | サポートされていません[^8]                  |
| `ADMIN PLUGINS DISABLE`          | サポートされています                     | サポートされていません[^8]                  |
| `ALTER INSTANCE RELOAD TLS`      | サポートされています                     | TiDB サーバーレスは TLS 証明書を自動的に更新します。  |
| `LOAD DATA INFILE`               | `LOAD DATA LOCAL INFILE`のみサポート | `LOAD DATA LOCAL INFILE`のみサポート   |
| `CHANGE DRAINER`                 | サポートされていません[^7]                | サポートされていません[^7]                  |
| `CHANGE PUMP`                    | サポートされていません[^7]                | サポートされていません[^7]                  |
| `FLASHBACK CLUSTER TO TIMESTAMP` | サポートされています                     | サポートされていません[^3]                  |
| `LOAD STATS`                     | サポートされています                     | サポートされていません                      |
| `SELECT ... INTO OUTFILE`        | サポートされていません[^4]                | サポートされていません[^4]                  |
| `SET CONFIG`                     | サポートされていません[^4]                | サポートされていません[^4]                  |
| `SHOW CONFIG`                    | サポートされていません[^4]                | サポートされていません[^4]                  |
| `SHOW DRAINER STATUS`            | サポートされていません[^7]                | サポートされていません[^7]                  |
| `SHOW PLUGINS`                   | サポートされています                     | サポートされていません[^8]                  |
| `SHOW PUMP STATUS`               | サポートされていません[^7]                | サポートされていません[^7]                  |
| `SHUTDOWN`                       | サポートされていません[^4]                | サポートされていません[^4]                  |
| `CREATE TABLE ... AUTO_ID_CACHE` | サポートされています                     | サポートされていません[^12]                 |

## 関数と演算子 {#functions-and-operators}

| 関数と演算子  | TiDB専用 | TiDB サーバーレス                                                                                                     |
| :------ | :----- | :-------------------------------------------------------------------------------------------------------------- |
| `SLEEP` | 制限なし   | [`SLEEP()`関数](https://docs.pingcap.com/tidbcloud/miscellaneous-functions)は、最大 300 秒のスリープ時間しかサポートできないという制限があります。 |

## システムテーブル {#system-tables}

| データベース               | テーブル                                 | TiDB専用          | TiDB サーバーレス     |
| :------------------- | :----------------------------------- | :-------------- | :-------------- |
| `information_schema` | `ATTRIBUTES`                         | サポートされています      | サポートされていません[^1] |
| `information_schema` | `CLUSTER_CONFIG`                     | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `CLUSTER_HARDWARE`                   | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `CLUSTER_INFO`                       | サポートされています      | サポートされていません[^1] |
| `information_schema` | `CLUSTER_LOAD`                       | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `CLUSTER_LOG`                        | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `CLUSTER_SLOW_QUERY`                 | サポートされています      | サポートされていません[^5] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY`         | サポートされています      | サポートされていません[^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_EVICTED` | サポートされています      | サポートされていません[^6] |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_HISTORY` | サポートされています      | サポートされていません[^6] |
| `information_schema` | `CLUSTER_SYSTEMINFO`                 | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `INSPECTION_RESULT`                  | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `INSPECTION_RULES`                   | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `INSPECTION_SUMMARY`                 | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `METRICS_SUMMARY`                    | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `METRICS_SUMMARY_BY_LABEL`           | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `METRICS_TABLES`                     | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `PLACEMENT_POLICIES`                 | サポートされています      | サポートされていません[^1] |
| `information_schema` | `RESOURCE_GROUPS`                    | サポートされています      | サポートされていません[^2] |
| `information_schema` | `SLOW_QUERY`                         | サポートされています      | サポートされていません[^5] |
| `information_schema` | `STATEMENTS_SUMMARY`                 | サポートされています      | サポートされていません[^6] |
| `information_schema` | `STATEMENTS_SUMMARY_EVICTED`         | サポートされています      | サポートされていません[^6] |
| `information_schema` | `STATEMENTS_SUMMARY_HISTORY`         | サポートされています      | サポートされていません[^6] |
| `information_schema` | `TIDB_HOT_REGIONS`                   | サポートされていません[^4] | サポートされていません[^4] |
| `information_schema` | `TIDB_HOT_REGIONS_HISTORY`           | サポートされています      | サポートされていません[^1] |
| `information_schema` | `TIDB_SERVERS_INFO`                  | サポートされています      | サポートされていません[^1] |
| `information_schema` | `TIFLASH_SEGMENTS`                   | サポートされています      | サポートされていません[^1] |
| `information_schema` | `TIFLASH_TABLES`                     | サポートされています      | サポートされていません[^1] |
| `information_schema` | `TIKV_REGION_PEERS`                  | サポートされています      | サポートされていません[^1] |
| `information_schema` | `TIKV_REGION_STATUS`                 | サポートされています      | サポートされていません[^1] |
| `information_schema` | `TIKV_STORE_STATUS`                  | サポートされています      | サポートされていません[^1] |
| `performance_schema` | `pd_profile_allocs`                  | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `pd_profile_block`                   | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `pd_profile_cpu`                     | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `pd_profile_goroutines`              | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `pd_profile_memory`                  | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `pd_profile_mutex`                   | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `tidb_profile_allocs`                | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `tidb_profile_block`                 | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `tidb_profile_cpu`                   | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `tidb_profile_goroutines`            | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `tidb_profile_memory`                | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `tidb_profile_mutex`                 | サポートされていません[^4] | サポートされていません[^4] |
| `performance_schema` | `tikv_profile_cpu`                   | サポートされていません[^4] | サポートされていません[^4] |
| `mysql`              | `expr_pushdown_blacklist`            | サポートされていません[^4] | サポートされていません[^4] |
| `mysql`              | `gc_delete_range`                    | サポートされていません[^4] | サポートされていません[^4] |
| `mysql`              | `gc_delete_range_done`               | サポートされていません[^4] | サポートされていません[^4] |
| `mysql`              | `opt_rule_blacklist`                 | サポートされていません[^4] | サポートされていません[^4] |
| `mysql`              | `tidb`                               | サポートされていません[^4] | サポートされていません[^4] |
| `mysql`              | `tidb_ttl_job_history`               | サポートされています      | サポートされていません[^9] |
| `mysql`              | `tidb_ttl_table_status`              | サポートされています      | サポートされていません[^9] |
| `mysql`              | `tidb_ttl_task`                      | サポートされています      | サポートされていません[^9] |

## システム変数 {#system-variables}

| 変数                                        | TiDB専用          | TiDB サーバーレス                       |
| :---------------------------------------- | :-------------- | :-------------------------------- |
| `datadir`                                 | 制限なし            | サポートされていません[^1]                   |
| `interactive_timeout`                     | 制限なし            | 読み取り専用[^11]                       |
| `max_allowed_packet`                      | 制限なし            | 読み取り専用[^11]                       |
| `plugin_dir`                              | 制限なし            | サポートされていません[^8]                   |
| `plugin_load`                             | 制限なし            | サポートされていません[^8]                   |
| `skip_name_resolve`                       | 制限なし            | 読み取り専用[^11]                       |
| `sql_log_bin`                             | 制限なし            | 読み取り専用[^11]                       |
| `tidb_cdc_write_source`                   | 制限なし            | 読み取り専用[^11]                       |
| `tidb_check_mb4_value_in_utf8`            | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_config`                             | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_ddl_disk_quota`                     | 制限なし            | 読み取り専用[^11]                       |
| `tidb_ddl_enable_fast_reorg`              | 制限なし            | 読み取り専用[^11]                       |
| `tidb_ddl_error_count_limit`              | 制限なし            | 読み取り専用[^11]                       |
| `tidb_ddl_flashback_concurrency`          | 制限なし            | 読み取り専用[^11]                       |
| `tidb_ddl_reorg_batch_size`               | 制限なし            | 読み取り専用[^11]                       |
| `tidb_ddl_reorg_priority`                 | 制限なし            | 読み取り専用[^11]                       |
| `tidb_ddl_reorg_worker_cnt`               | 制限なし            | 読み取り専用[^11]                       |
| `tidb_enable_1pc`                         | 制限なし            | 読み取り専用[^11]                       |
| `tidb_enable_async_commit`                | 制限なし            | 読み取り専用[^11]                       |
| `tidb_enable_auto_analyze`                | 制限なし            | 読み取り専用[^11]                       |
| `tidb_enable_collect_execution_info`      | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_enable_ddl`                         | 制限なし            | 読み取り専用[^11]                       |
| `tidb_enable_gc_aware_memory_track`       | 制限なし            | 読み取り専用[^11]                       |
| `tidb_enable_gogc_tuner`                  | 制限なし            | 読み取り専用[^11]                       |
| `tidb_enable_local_txn`                   | 制限なし            | 読み取り専用[^11]                       |
| `tidb_enable_resource_control`            | 制限なし            | 読み取り専用[^11]                       |
| `tidb_enable_slow_log`                    | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_enable_stmt_summary`                | 制限なし            | 読み取り専用[^11]                       |
| `tidb_enable_telemetry`                   | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_enable_top_sql`                     | 制限なし            | 読み取り専用[^11]                       |
| `tidb_enable_tso_follower_proxy`          | 制限なし            | 読み取り専用[^11]                       |
| `tidb_expensive_query_time_threshold`     | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_force_priority`                     | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_gc_concurrency`                     | 制限なし            | 読み取り専用[^11]                       |
| `tidb_gc_enable`                          | 制限なし            | 読み取り専用[^11]                       |
| `tidb_gc_life_time`                       | 制限なし            | 読み取り専用[^11]                       |
| `tidb_gc_max_wait_time`                   | 制限なし            | 読み取り専用[^11]                       |
| `tidb_gc_run_interval`                    | 制限なし            | 読み取り専用[^11]                       |
| `tidb_gc_scan_lock_mode`                  | 制限なし            | 読み取り専用[^11]                       |
| `tidb_general_log`                        | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_generate_binary_plan`               | 制限なし            | 読み取り専用[^11]                       |
| `tidb_gogc_tuner_threshold`               | 制限なし            | 読み取り専用[^11]                       |
| `tidb_guarantee_linearizability`          | 制限なし            | 読み取り専用[^11]                       |
| `tidb_isolation_read_engines`             | 制限なし            | 読み取り専用[^11]                       |
| `tidb_log_file_max_days`                  | 制限なし            | 読み取り専用[^11]                       |
| `tidb_memory_usage_alarm_ratio`           | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_metric_query_range_duration`        | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_metric_query_step`                  | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_opt_write_row_id`                   | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_placement_mode`                     | 制限なし            | 読み取り専用[^11]                       |
| `tidb_pprof_sql_cpu`                      | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_record_plan_in_slow_log`            | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_redact_log`                         | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_restricted_read_only`               | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_row_format_version`                 | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_scatter_region`                     | 制限なし            | 読み取り専用[^11]                       |
| `tidb_server_memory_limit`                | 制限なし            | 読み取り専用[^11]                       |
| `tidb_server_memory_limit_gc_trigger`     | 制限なし            | 読み取り専用[^11]                       |
| `tidb_server_memory_limit_sess_min_size`  | 制限なし            | 読み取り専用[^11]                       |
| `tidb_simplified_metrics`                 | 制限なし            | 読み取り専用[^11]                       |
| `tidb_slow_query_file`                    | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_slow_log_threshold`                 | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_slow_txn_log_threshold`             | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_stats_load_sync_wait`               | 制限なし            | 読み取り専用[^11]                       |
| `tidb_stmt_summary_history_size`          | 制限なし            | 読み取り専用[^11]                       |
| `tidb_stmt_summary_internal_query`        | 制限なし            | 読み取り専用[^11]                       |
| `tidb_stmt_summary_max_sql_length`        | 制限なし            | 読み取り専用[^11]                       |
| `tidb_stmt_summary_max_stmt_count`        | 制限なし            | 読み取り専用[^11]                       |
| `tidb_stmt_summary_refresh_interval`      | 制限なし            | 読み取り専用[^11]                       |
| `tidb_sysproc_scan_concurrency`           | 制限なし            | 読み取り専用[^11]                       |
| `tidb_top_sql_max_meta_count`             | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_top_sql_max_time_series_count`      | サポートされていません[^4] | サポートされていません[^4]                   |
| `tidb_tso_client_batch_max_wait_time`     | 制限なし            | 読み取り専用[^11]                       |
| `tidb_ttl_delete_batch_size`              | 制限なし            | 読み取り専用[^9]                        |
| `tidb_ttl_delete_rate_limit`              | 制限なし            | 読み取り専用[^9]                        |
| `tidb_ttl_delete_worker_count`            | 制限なし            | 読み取り専用[^9]                        |
| `tidb_ttl_job_enable`                     | 制限なし            | 読み取り専用[^9]                        |
| `tidb_ttl_job_schedule_window_end_time`   | 制限なし            | 読み取り専用[^9]                        |
| `tidb_ttl_job_schedule_window_start_time` | 制限なし            | 読み取り専用[^9]                        |
| `tidb_ttl_running_tasks`                  | 制限なし            | 読み取り専用[^9]                        |
| `tidb_ttl_scan_batch_size`                | 制限なし            | 読み取り専用[^9]                        |
| `tidb_ttl_scan_worker_count`              | 制限なし            | 読み取り専用[^9]                        |
| `tidb_txn_mode`                           | 制限なし            | 読み取り専用[^11]                       |
| `tidb_wait_split_region_finish`           | 制限なし            | 読み取り専用[^11]                       |
| `tidb_wait_split_region_timeout`          | 制限なし            | 読み取り専用[^11]                       |
| `txn_scope`                               | 制限なし            | 読み取り専用[^11]                       |
| `validate_password.enable`                | 制限なし            | 常に有効[^10]                         |
| `validate_password.length`                | 制限なし            | 少なくとも`8` [^10]                    |
| `validate_password.mixed_case_count`      | 制限なし            | 少なくとも`1` [^10]                    |
| `validate_password.number_count`          | 制限なし            | 少なくとも`1` [^10]                    |
| `validate_password.policy`                | 制限なし            | `MEDIUM`または`STRONG`のみを指定できます[^10] |
| `validate_password.special_char_count`    | 制限なし            | 少なくとも`1` [^10]                    |
| `wait_timeout`                            | 制限なし            | 読み取り専用[^11]                       |

[^1]: データ配置の構成は、TiDB サーバーレスではサポートされていません。

[^2]: リソース グループの構成は、TiDB サーバーレスではサポートされていません。

[^3]: TiDB サーバーレスで[バックアップと復元](/tidb-cloud/backup-and-restore-serverless.md)操作を実行するには、代わりにTiDB Cloudコンソールを使用できます。

[^4]: この機能は[Security強化モード (SEM)](/system-variables.md#tidb_enable_enhanced_security)では使用できません。

[^5]: TiDB サーバーレスで[遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)を追跡するには、代わりにTiDB Cloudコンソールを使用できます。

[^6]: TiDB サーバーレスで[ステートメント分析](/tidb-cloud/tune-performance.md#statement-analysis)を実行するには、代わりにTiDB Cloudコンソールを使用できます。

[^7]: DrainerとPumpはTiDB Cloudではサポートされていません。

[^8]: プラグインは TiDB サーバーレスではサポートされていません。

[^9]: [生存時間 (TTL)](/time-to-live.md)は現在 TiDB サーバーレスでは利用できません。

[^10]: TiDB サーバーレスは強力なパスワード ポリシーを適用します。

[^11]: この変数は、TiDB サーバーレスでは読み取り専用です。

[^12]: [`AUTO_ID_CACHE`](/auto-increment.md#cache-size-control)を使用したキャッシュ サイズのカスタマイズは、TiDB サーバーレスでは一時的に利用できません。
