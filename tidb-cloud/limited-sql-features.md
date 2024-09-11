---
title: Limited SQL Features on TiDB Cloud
summary: TiDB Cloudの制限された SQL 機能について説明します。
---

# TiDB Cloudの SQL 機能が制限されている {#limited-sql-features-on-tidb-cloud}

TiDB Cloud は、 TiDB がサポートするほぼすべてのワークロードで動作しますが、TiDB Self-Managed とTiDB Cloud Dedicated/Serverless には機能上の違いがいくつかあります。このドキュメントでは、 TiDB Cloudの SQL 機能の制限について説明します。TiDB Self-Managed とTiDB Cloud Dedicated/Serverless 間の機能ギャップは、常に埋められています。ギャップを埋めるためにこれらの機能や機能が必要な場合は、機能リクエスト[お問い合わせ](/tidb-cloud/tidb-cloud-support.md)送信してください。

## 声明 {#statements}

### 配置と範囲管理 {#placement-and-range-management}

| 声明                             | TiDB Cloud専用 | TiDB Cloudサーバーレス |
| :----------------------------- | :----------- | :--------------- |
| `ALTER PLACEMENT POLICY`       | サポート         | サポートされていません[^1]  |
| `CREATE PLACEMENT POLICY`      | サポート         | サポートされていません[^1]  |
| `DROP PLACEMENT POLICY`        | サポート         | サポートされていません[^1]  |
| `SHOW CREATE PLACEMENT POLICY` | サポート         | サポートされていません[^1]  |
| `SHOW PLACEMENT`               | サポート         | サポートされていません[^1]  |
| `SHOW PLACEMENT FOR`           | サポート         | サポートされていません[^1]  |
| `SHOW PLACEMENT LABELS`        | サポート         | サポートされていません[^1]  |
| `SHOW TABLE REGIONS`           | サポート         | サポートされていません[^1]  |
| `SPLIT REGION`                 | サポート         | サポートされていません[^1]  |

### リソース グループ {#resource-groups}

| 声明                           | TiDB Cloud専用 | TiDB Cloudサーバーレス |
| :--------------------------- | :----------- | :--------------- |
| `ALTER RESOURCE GROUP`       | サポート         | サポートされていません[^2]  |
| `CALIBRATE RESOURCE`         | サポートされていません  | サポートされていません[^2]  |
| `CREATE RESOURCE GROUP`      | サポート         | サポートされていません[^2]  |
| `DROP RESOURCE GROUP`        | サポート         | サポートされていません[^2]  |
| `SET RESOURCE GROUP`         | サポート         | サポートされていません[^2]  |
| `SHOW CREATE RESOURCE GROUP` | サポート         | サポートされていません[^2]  |

### その他 {#others}

| 声明                          | TiDB Cloud専用                   | TiDB Cloudサーバーレス                           |
| :-------------------------- | :----------------------------- | :----------------------------------------- |
| `BACKUP`                    | サポート                           | サポートされていません[^3]                            |
| `SHOW BACKUPS`              | サポート                           | サポートされていません[^3]                            |
| `RESTORE`                   | サポート                           | サポートされていません[^3]                            |
| `SHOW RESTORES`             | サポート                           | サポートされていません[^3]                            |
| `ADMIN RESET TELEMETRY_ID`  | サポート                           | テレメトリはTiDB Cloud Serverless ではサポートされていません。 |
| `ADMIN SHOW TELEMETRY`      | サポートされていません[^4]                | サポートされていません[^4]                            |
| `ADMIN SHOW SLOW`           | サポート                           | サポートされていません[^5]                            |
| `ADMIN PLUGINS ENABLE`      | サポート                           | サポートされていません[^8]                            |
| `ADMIN PLUGINS DISABLE`     | サポート                           | サポートされていません[^8]                            |
| `ALTER INSTANCE RELOAD TLS` | サポート                           | TiDB Cloud Serverless は TLS 証明書を自動的に更新します。 |
| `LOAD DATA INFILE`          | `LOAD DATA LOCAL INFILE`のみサポート | `LOAD DATA LOCAL INFILE`のみサポート             |
| `CHANGE DRAINER`            | サポートされていません[^7]                | サポートされていません[^7]                            |
| `CHANGE PUMP`               | サポートされていません[^7]                | サポートされていません[^7]                            |
| `FLASHBACK CLUSTER`         | サポート                           | サポートされていません[^3]                            |
| `LOAD STATS`                | サポート                           | サポートされていません                                |
| `SELECT ... INTO OUTFILE`   | サポートされていません[^4]                | サポートされていません[^4]                            |
| `SET CONFIG`                | サポートされていません[^4]                | サポートされていません[^4]                            |
| `SHOW CONFIG`               | サポートされていません[^4]                | サポートされていません[^4]                            |
| `SHOW DRAINER STATUS`       | サポートされていません[^7]                | サポートされていません[^7]                            |
| `SHOW PLUGINS`              | サポート                           | サポートされていません[^8]                            |
| `SHOW PUMP STATUS`          | サポートされていません[^7]                | サポートされていません[^7]                            |
| `SHUTDOWN`                  | サポートされていません[^4]                | サポートされていません[^4]                            |
| `PLAN REPLAYER`             | サポート                           | 別の方法でサポート[^11]                             |

## 関数と演算子 {#functions-and-operators}

| 関数と演算子  | TiDB Cloud専用 | TiDB Cloudサーバーレス                                                                                              |
| :------ | :----------- | :------------------------------------------------------------------------------------------------------------ |
| `SLEEP` | 制限なし         | [`SLEEP()`関数](https://docs.pingcap.com/tidbcloud/miscellaneous-functions)最大 300 秒のスリープ時間しかサポートできないという制限があります。 |

## システムテーブル {#system-tables}

| データベース               | テーブル                                 | TiDB Cloud専用    | TiDB Cloudサーバーレス |
| :------------------- | :----------------------------------- | :-------------- | :--------------- |
| `information_schema` | `ATTRIBUTES`                         | サポート            | サポートされていません[^1]  |
| `information_schema` | `CLUSTER_CONFIG`                     | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `CLUSTER_HARDWARE`                   | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `CLUSTER_INFO`                       | サポート            | サポートされていません[^1]  |
| `information_schema` | `CLUSTER_LOAD`                       | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `CLUSTER_LOG`                        | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `CLUSTER_SLOW_QUERY`                 | サポート            | サポートされていません[^5]  |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY`         | サポート            | サポートされていません[^6]  |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_EVICTED` | サポート            | サポートされていません[^6]  |
| `information_schema` | `CLUSTER_STATEMENTS_SUMMARY_HISTORY` | サポート            | サポートされていません[^6]  |
| `information_schema` | `CLUSTER_SYSTEMINFO`                 | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `INSPECTION_RESULT`                  | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `INSPECTION_RULES`                   | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `INSPECTION_SUMMARY`                 | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `METRICS_SUMMARY`                    | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `METRICS_SUMMARY_BY_LABEL`           | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `METRICS_TABLES`                     | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `PLACEMENT_POLICIES`                 | サポート            | サポートされていません[^1]  |
| `information_schema` | `RESOURCE_GROUPS`                    | サポート            | サポートされていません[^2]  |
| `information_schema` | `SLOW_QUERY`                         | サポート            | サポートされていません[^5]  |
| `information_schema` | `STATEMENTS_SUMMARY`                 | サポート            | サポートされていません[^6]  |
| `information_schema` | `STATEMENTS_SUMMARY_EVICTED`         | サポート            | サポートされていません[^6]  |
| `information_schema` | `STATEMENTS_SUMMARY_HISTORY`         | サポート            | サポートされていません[^6]  |
| `information_schema` | `TIDB_HOT_REGIONS`                   | サポートされていません[^4] | サポートされていません[^4]  |
| `information_schema` | `TIDB_HOT_REGIONS_HISTORY`           | サポート            | サポートされていません[^1]  |
| `information_schema` | `TIDB_SERVERS_INFO`                  | サポート            | サポートされていません[^1]  |
| `information_schema` | `TIKV_REGION_PEERS`                  | サポート            | サポートされていません[^1]  |
| `information_schema` | `TIKV_REGION_STATUS`                 | サポート            | サポートされていません[^1]  |
| `information_schema` | `TIKV_STORE_STATUS`                  | サポート            | サポートされていません[^1]  |
| `performance_schema` | `pd_profile_allocs`                  | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `pd_profile_block`                   | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `pd_profile_cpu`                     | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `pd_profile_goroutines`              | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `pd_profile_memory`                  | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `pd_profile_mutex`                   | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `tidb_profile_allocs`                | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `tidb_profile_block`                 | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `tidb_profile_cpu`                   | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `tidb_profile_goroutines`            | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `tidb_profile_memory`                | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `tidb_profile_mutex`                 | サポートされていません[^4] | サポートされていません[^4]  |
| `performance_schema` | `tikv_profile_cpu`                   | サポートされていません[^4] | サポートされていません[^4]  |
| `mysql`              | `expr_pushdown_blacklist`            | サポートされていません[^4] | サポートされていません[^4]  |
| `mysql`              | `gc_delete_range`                    | サポートされていません[^4] | サポートされていません[^4]  |
| `mysql`              | `gc_delete_range_done`               | サポートされていません[^4] | サポートされていません[^4]  |
| `mysql`              | `opt_rule_blacklist`                 | サポートされていません[^4] | サポートされていません[^4]  |
| `mysql`              | `tidb`                               | サポートされていません[^4] | サポートされていません[^4]  |

## システム変数 {#system-variables}

| 変数                                        | TiDB Cloud専用     | TiDB Cloudサーバーレス           |
| :---------------------------------------- | :--------------- | :------------------------- |
| `datadir`                                 | 制限なし             | サポートされていません[^1]            |
| `interactive_timeout`                     | 制限なし             | 読み取り専用[^10]                |
| `max_allowed_packet`                      | 制限なし             | 読み取り専用[^10]                |
| `plugin_dir`                              | 制限なし             | サポートされていません[^8]            |
| `plugin_load`                             | 制限なし             | サポートされていません[^8]            |
| `require_secure_transport`                | サポートされていません[^12] | 読み取り専用[^10]                |
| `skip_name_resolve`                       | 制限なし             | 読み取り専用[^10]                |
| `sql_log_bin`                             | 制限なし             | 読み取り専用[^10]                |
| `tidb_cdc_write_source`                   | 制限なし             | 読み取り専用[^10]                |
| `tidb_check_mb4_value_in_utf8`            | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_config`                             | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_ddl_disk_quota`                     | 制限なし             | 読み取り専用[^10]                |
| `tidb_ddl_enable_fast_reorg`              | 制限なし             | 読み取り専用[^10]                |
| `tidb_ddl_error_count_limit`              | 制限なし             | 読み取り専用[^10]                |
| `tidb_ddl_flashback_concurrency`          | 制限なし             | 読み取り専用[^10]                |
| `tidb_ddl_reorg_batch_size`               | 制限なし             | 読み取り専用[^10]                |
| `tidb_ddl_reorg_priority`                 | 制限なし             | 読み取り専用[^10]                |
| `tidb_ddl_reorg_worker_cnt`               | 制限なし             | 読み取り専用[^10]                |
| `tidb_enable_1pc`                         | 制限なし             | 読み取り専用[^10]                |
| `tidb_enable_async_commit`                | 制限なし             | 読み取り専用[^10]                |
| `tidb_enable_auto_analyze`                | 制限なし             | 読み取り専用[^10]                |
| `tidb_enable_collect_execution_info`      | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_enable_ddl`                         | 制限なし             | 読み取り専用[^10]                |
| `tidb_enable_gc_aware_memory_track`       | 制限なし             | 読み取り専用[^10]                |
| `tidb_enable_gogc_tuner`                  | 制限なし             | 読み取り専用[^10]                |
| `tidb_enable_local_txn`                   | 制限なし             | 読み取り専用[^10]                |
| `tidb_enable_resource_control`            | 制限なし             | 読み取り専用[^10]                |
| `tidb_enable_slow_log`                    | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_enable_stmt_summary`                | 制限なし             | 読み取り専用[^10]                |
| `tidb_enable_telemetry`                   | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_enable_top_sql`                     | 制限なし             | 読み取り専用[^10]                |
| `tidb_enable_tso_follower_proxy`          | 制限なし             | 読み取り専用[^10]                |
| `tidb_expensive_query_time_threshold`     | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_force_priority`                     | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_gc_concurrency`                     | 制限なし             | 読み取り専用[^10]                |
| `tidb_gc_enable`                          | 制限なし             | 読み取り専用[^10]                |
| `tidb_gc_life_time`                       | 制限なし             | 読み取り専用[^10]                |
| `tidb_gc_max_wait_time`                   | 制限なし             | 読み取り専用[^10]                |
| `tidb_gc_run_interval`                    | 制限なし             | 読み取り専用[^10]                |
| `tidb_gc_scan_lock_mode`                  | 制限なし             | 読み取り専用[^10]                |
| `tidb_general_log`                        | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_generate_binary_plan`               | 制限なし             | 読み取り専用[^10]                |
| `tidb_gogc_tuner_threshold`               | 制限なし             | 読み取り専用[^10]                |
| `tidb_guarantee_linearizability`          | 制限なし             | 読み取り専用[^10]                |
| `tidb_isolation_read_engines`             | 制限なし             | 読み取り専用[^10]                |
| `tidb_log_file_max_days`                  | 制限なし             | 読み取り専用[^10]                |
| `tidb_memory_usage_alarm_ratio`           | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_metric_query_range_duration`        | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_metric_query_step`                  | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_opt_write_row_id`                   | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_placement_mode`                     | 制限なし             | 読み取り専用[^10]                |
| `tidb_pprof_sql_cpu`                      | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_record_plan_in_slow_log`            | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_redact_log`                         | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_restricted_read_only`               | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_row_format_version`                 | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_scatter_region`                     | 制限なし             | 読み取り専用[^10]                |
| `tidb_server_memory_limit`                | 制限なし             | 読み取り専用[^10]                |
| `tidb_server_memory_limit_gc_trigger`     | 制限なし             | 読み取り専用[^10]                |
| `tidb_server_memory_limit_sess_min_size`  | 制限なし             | 読み取り専用[^10]                |
| `tidb_simplified_metrics`                 | 制限なし             | 読み取り専用[^10]                |
| `tidb_slow_query_file`                    | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_slow_log_threshold`                 | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_slow_txn_log_threshold`             | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_stats_load_sync_wait`               | 制限なし             | 読み取り専用[^10]                |
| `tidb_stmt_summary_history_size`          | 制限なし             | 読み取り専用[^10]                |
| `tidb_stmt_summary_internal_query`        | 制限なし             | 読み取り専用[^10]                |
| `tidb_stmt_summary_max_sql_length`        | 制限なし             | 読み取り専用[^10]                |
| `tidb_stmt_summary_max_stmt_count`        | 制限なし             | 読み取り専用[^10]                |
| `tidb_stmt_summary_refresh_interval`      | 制限なし             | 読み取り専用[^10]                |
| `tidb_sysproc_scan_concurrency`           | 制限なし             | 読み取り専用[^10]                |
| `tidb_top_sql_max_meta_count`             | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_top_sql_max_time_series_count`      | サポートされていません[^4]  | サポートされていません[^4]            |
| `tidb_tso_client_batch_max_wait_time`     | 制限なし             | 読み取り専用[^10]                |
| `tidb_ttl_delete_batch_size`              | 制限なし             | 読み取り専用[^10]                |
| `tidb_ttl_delete_rate_limit`              | 制限なし             | 読み取り専用[^10]                |
| `tidb_ttl_delete_worker_count`            | 制限なし             | 読み取り専用[^10]                |
| `tidb_ttl_job_schedule_window_end_time`   | 制限なし             | 読み取り専用[^10]                |
| `tidb_ttl_job_schedule_window_start_time` | 制限なし             | 読み取り専用[^10]                |
| `tidb_ttl_running_tasks`                  | 制限なし             | 読み取り専用[^10]                |
| `tidb_ttl_scan_batch_size`                | 制限なし             | 読み取り専用[^10]                |
| `tidb_ttl_scan_worker_count`              | 制限なし             | 読み取り専用[^10]                |
| `tidb_txn_mode`                           | 制限なし             | 読み取り専用[^10]                |
| `tidb_wait_split_region_finish`           | 制限なし             | 読み取り専用[^10]                |
| `tidb_wait_split_region_timeout`          | 制限なし             | 読み取り専用[^10]                |
| `txn_scope`                               | 制限なし             | 読み取り専用[^10]                |
| `validate_password.enable`                | 制限なし             | 常に有効[^9]                   |
| `validate_password.length`                | 制限なし             | 少なくとも`8` [^9]              |
| `validate_password.mixed_case_count`      | 制限なし             | 少なくとも`1` [^9]              |
| `validate_password.number_count`          | 制限なし             | 少なくとも`1` [^9]              |
| `validate_password.policy`                | 制限なし             | `MEDIUM`または`STRONG` [^9]のみ |
| `validate_password.special_char_count`    | 制限なし             | 少なくとも`1` [^9]              |
| `wait_timeout`                            | 制限なし             | 読み取り専用[^10]                |

[^1]: TiDB Cloud Serverless ではデータ配置の構成はサポートされていません。

[^2]: TiDB Cloud Serverless ではリソース グループの構成はサポートされていません。

[^3]: TiDB Cloud Serverless で[バックアップと復元](/tidb-cloud/backup-and-restore-serverless.md)操作を実行するには、代わりにTiDB Cloudコンソールを使用できます。

[^4]: この機能は[Security強化モード (SEM)](/system-variables.md#tidb_enable_enhanced_security)では利用できません。

[^5]: TiDB Cloud Serverless で[遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)追跡するには、代わりにTiDB Cloudコンソールを使用できます。

[^6]: TiDB Cloud Serverless で[ステートメント分析](/tidb-cloud/tune-performance.md#statement-analysis)実行するには、代わりにTiDB Cloudコンソールを使用できます。

[^7]: DrainerとPump はTiDB Cloudではサポートされていません。

[^8]: プラグインはTiDB Cloud Serverless ではサポートされていません。

[^9]: TiDB Cloud Serverless は強力なパスワード ポリシーを適用します。

[^10]: 変数はTiDB Cloud Serverless では読み取り専用です。

[^11]: TiDB Cloud Serverless は、 [例](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#examples-of-exporting-cluster-information)のように`PLAN REPLAYER`から`${tidb-server-status-port}`でエクスポートされたファイルのダウンロードをサポートしていません。代わりに、 TiDB Cloud Serverless はファイルをダウンロードするための[署名済みURL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)生成します。この URL は生成後 10 時間有効であることに注意してください。

[^12]: サポートされていません。TiDB TiDB Cloud Dedicated クラスターで`require_secure_transport`有効にすると、SQL クライアント接続が失敗します。
