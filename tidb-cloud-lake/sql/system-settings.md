---
title: system.settings
summary: 現在のセッションのシステム設定を格納します。
---

# system.settings

現在のセッションのシステム設定を保存します。

```sql
SELECT * FROM system.settings;
```

| 名前 | 値 | デフォルト | レベル | 説明 | 型 |
|------|-------|---------|-------|-------------|------|
| acquire_lock_timeout | 30 | 30 | DEFAULT | ロックを取得するための最大タイムアウトを秒単位で設定します。 | UInt64 |
| aggregate_spilling_memory_ratio | 60 | 60 | LOCAL | クエリ実行中に、集計器がデータをストレージにスピルする前に使用できる最大メモリ比率をバイト単位で設定します。 | UInt64 |
| allow_query_exceeded_limit | 0 | 0 | DEFAULT | クエリが設定済みのメモリ制限を超過することを許可し、メモリ競合が発生するまでエラー通知を遅延させます。 | UInt64 |
| auto_compaction_imperfect_blocks_threshold | 25 | 25 | GLOBAL | 書き込み後に自動 compaction をトリガーするしきい値です。自動 compaction を無効にするには 0 に設定します。 | UInt64 |
| auto_compaction_segments_limit | 3 | 3 | DEFAULT | 書き込み後に自動的にトリガーされる recluster の対象となるセグメントの最大数です。 | UInt64 |
| binary_input_format | utf-8 | utf-8 | DEFAULT | 文字列リテラルを BINARY カラムに挿入する際の解釈方法を制御します (HEX、BASE64、UTF-8、または UTF-8-LOSSY)。 | String |
| binary_output_format | hex | hex | DEFAULT | BINARY カラムの表示方法を制御します (HEX、BASE64、UTF-8、または UTF-8-LOSSY)。 | String |
| bloom_runtime_filter_threshold | 3000000 | 3000000 | DEFAULT | bloom ランタイムフィルターを生成するための最大行数を設定します。 | UInt64 |
| collation | utf8 | utf8 | DEFAULT | 文字の照合順序を設定します。使用可能な値には "utf8" が含まれます。 | String |
| compact_max_block_selection | 1000 | 1000 | DEFAULT | compact 操作中に選択できる不完全なブロックの最大数を制限します。 | UInt64 |
| copy_dedup_full_path_by_default | 0 | 0 | DEFAULT | テーブル作成時に table option copy_dedup_full_path が設定されていない場合のデフォルト値です。 | UInt64 |
| cost_factor_aggregate_per_row | 5 | 5 | DEFAULT | データ 1 行あたりのグループ化操作のコスト係数です。 | UInt64 |
| cost_factor_hash_table_per_row | 10 | 10 | DEFAULT | データ 1 行あたりのハッシュテーブル構築のコスト係数です。 | UInt64 |
| cost_factor_network_per_row | 50 | 50 | DEFAULT | データ 1 行あたりのネットワーク送信のコスト係数です。 | UInt64 |
| create_query_flight_client_with_current_rt | 1 | 1 | DEFAULT | クエリ操作で現在のランタイムを使用するかどうかをオン (1) またはオフ (0) にします。 | UInt64 |
| data_retention_num_snapshots_to_keep | 0 | 0 | DEFAULT | vacuum 操作中に保持するスナップショット数を指定します。data_retention_time_in_days を上書きします。0 に設定すると、この設定は無視されます。 | UInt64 |
| data_retention_time_in_days | 1 | 1 | DEFAULT | データ保持期間を日単位で設定します。 | UInt64 |
| date_format_style | Oracle | Oracle | DEFAULT | 日付形式のスタイルを設定します (datetime 関数で使用)。使用可能な値: "MySQL"、"Oracle"。 | String |
| ddl_column_type_nullable | 1 | 1 | DEFAULT | テーブル操作で新しいカラムをデフォルトで nullable (1) にするか、しない (0) かを設定します。 | UInt64 |
| default_order_by_null | nulls_last | nulls_last | DEFAULT | 数値の default_order_by_null モードを設定します。値: "nulls_first"、"nulls_last"、"nulls_first_on_asc_last_on_desc"。 | String |
| disable_join_reorder | 0 | 0 | DEFAULT | join reorder 最適化を無効にします。 | UInt64 |
| disable_variant_check | 0 | 0 | DEFAULT | variant チェックを無効にして、無効な JSON 値の挿入を許可します。 | UInt64 |
| dynamic_sample_time_budget_ms | 0 | 0 | DEFAULT | 動的サンプルの時間予算をミリ秒単位で設定します。 | UInt64 |
| enable_aggregating_index_scan | 1 | 1 | DEFAULT | クエリ時に aggregating index データのスキャンを有効にします。 | UInt64 |
| enable_analyze_histogram | 0 | 0 | DEFAULT | テーブル分析時に、クエリ最適化のためのヒストグラム分析を有効にします。 | UInt64 |
| enable_auto_analyze | 1 | 1 | DEFAULT | 書き込み後の auto analyze を有効にします。0 で無効、1 で有効です。 | UInt64 |
| enable_auto_detect_datetime_format | 0 | 0 | DEFAULT | 非 ISO datetime 形式の自動検出を有効にします。関数、COPY、VARIANT cast で機能します。 | UInt64 |
| enable_auto_fix_missing_bloom_index | 0 | 0 | DEFAULT | 不足している bloom index の自動修正を有効にします。 | UInt64 |
| enable_auto_materialize_cte | 1 | 1 | DEFAULT | CTE の自動 materialize を有効にします。0 で無効、1 で有効です。 | UInt64 |
| enable_auto_vacuum | 0 | 0 | DEFAULT | テーブルに対して VACUUM 操作を自動的にトリガーするかどうかを指定します。 | UInt64 |
| enable_backpressure_spiller | 0 | 0 | DEFAULT | 新しい backpressure spiller を使用します。 | UInt64 |
| enable_block_stream_write | 1 | 1 | GLOBAL | block stream write を有効にします。 | UInt64 |
| enable_bloom_runtime_filter | 1 | 1 | DEFAULT | JOIN の bloom ランタイムフィルター最適化を有効にします。 | UInt64 |
| enable_cbo | 1 | 1 | DEFAULT | コストベース最適化を有効にします。 | UInt64 |
| enable_compact_after_multi_table_insert | 0 | 0 | DEFAULT | 複数テーブルへの insert 後の recluster と compact を有効にします。 | UInt64 |
| enable_compact_after_write | 1 | 1 | DEFAULT | 書き込み後 (copy/insert/replace-into/merge-into) の compact を有効にします。より多くのメモリが必要です。 | UInt64 |
| enable_cse_optimizer | 0 | 0 | DEFAULT | 共通部分式除去の最適化を有効にします。 | UInt64 |
| enable_decimal_sum_widening | 0 | 0 | DEFAULT | SUM の引数を Decimal(19..38, scale) から Decimal(76, scale) に自動的に拡張します。 | UInt64 |
| enable_dio | 1 | 1 | DEFAULT | Direct IO を有効にします。 | UInt64 |
| enable_distributed_compact | 0 | 0 | DEFAULT | テーブル compaction の分散実行を有効にします。 | UInt64 |
| enable_distributed_copy_into | 1 | 1 | DEFAULT | 'COPY INTO' の分散実行を有効にします。 | UInt64 |
| enable_distributed_merge_into | 1 | 1 | DEFAULT | 'MERGE INTO' の分散実行を有効にします。 | UInt64 |
| enable_distributed_pruning | 1 | 1 | DEFAULT | 分散 index pruning を有効にします。 | UInt64 |
| enable_distributed_recluster | 1 | 1 | GLOBAL | テーブル recluster の分散実行を有効にします。 | UInt64 |
| enable_distributed_replace_into | 0 | 0 | DEFAULT | 'REPLACE INTO' の分散実行を有効にします。 | UInt64 |
| enable_dphyp | 1 | 1 | DEFAULT | dphyp join order アルゴリズムを有効にします。 | UInt64 |
| enable_dst_hour_fix | 0 | 0 | DEFAULT | 時刻変換時に無効な DST を 1 時間加算して処理します。精度は保証されません (デフォルトでは無効)。 | UInt64 |
| enable_expand_roles | 1 | 1 | DEFAULT | show grants ステートメント実行時にロール展開を有効にします (デフォルトで有効)。 | UInt64 |
| enable_experiment_aggregate | 1 | 1 | DEFAULT | 実験的な集計を有効にします (デフォルトで有効)。 | UInt64 |
| enable_experiment_hash_index | 1 | 1 | DEFAULT | 実験的設定: hash index を有効にします (デフォルトで有効)。 | UInt64 |
| enable_experimental_connection_privilege_check | 0 | 0 | DEFAULT | 実験的設定: connection object privilege check を有効にします (デフォルトで無効)。 | UInt64 |
| enable_experimental_new_join | 1 | 1 | DEFAULT | 実験的な新しい join 実装を有効にします。 | UInt64 |
| enable_experimental_procedure | 1 | 1 | GLOBAL | 'PROCEDURE' の実験的機能を有効にします。 | UInt64 |
| enable_experimental_rbac_check | 1 | 1 | DEFAULT | 実験的設定: stage と udf の権限チェックを有効にします (デフォルトで有効)。 | UInt64 |
| enable_experimental_row_access_policy | 0 | 0 | DEFAULT | 実験的設定: row access policy を有効にします (デフォルトで無効)。 | UInt64 |
| enable_experimental_sequence_privilege_check | 0 | 0 | DEFAULT | 実験的設定: sequence object privilege check を有効にします (デフォルトで無効)。 | UInt64 |
| enable_experimental_table_ref | 0 | 0 | DEFAULT | 実験的設定: table ref を有効にします (デフォルトで無効)。 | UInt64 |
| enable_experimental_virtual_column | 0 | 0 | DEFAULT | 実験的な virtual column を有効にします。 | UInt64 |
| enable_fixed_rows_sort | 1 | 1 | DEFAULT | fixed rows sort serialize を有効にします。 | UInt64 |
| enable_geo_create_table | 1 | 1 | DEFAULT | geometry/geography 型でのテーブル作成および変更を有効にします。 | UInt64 |
| enable_group_by_column_first | 0 | 0 | DEFAULT | GROUP BY 名を SELECT エイリアスより先に入力カラムへ解決します。互換性のためデフォルトでは無効です。 | UInt64 |
| enable_hive_parquet_predict_pushdown | 1 | 1 | DEFAULT | この変数を 1 に設定することで hive parquet predict pushdown を有効にします。デフォルト値は 1 です。 | UInt64 |
| enable_join_runtime_filter | 1 | 1 | DEFAULT | JOIN のランタイムフィルター最適化を有効にします。 | UInt64 |
| enable_last_snapshot_location_hint | 1 | 1 | DEFAULT | last_snapshot_location_hint オブジェクトの書き込みを有効にします。 | UInt64 |
| enable_loser_tree_merge_sort | 1 | 1 | DEFAULT | loser tree merge sort を有効にします。 | UInt64 |
| enable_materialized_cte | 1 | 1 | DEFAULT | materialized common table expression を有効にします。 | UInt64 |
| enable_merge_into_row_fetch | 1 | 1 | DEFAULT | merge into row fetch 最適化を有効にします。 | UInt64 |
| enable_mutation_block_id_repartition | 1 | 1 | DEFAULT | join ベースの mutation で row fetch 前にローカル block_id repartition を有効にし、重複したブロック読み取りを減らします。 | UInt64 |
| enable_new_copy_for_text_formats | 1 | 1 | DEFAULT | CSV ファイルのロード (load) に新しい実装を使用します。 | UInt64 |
| enable_optimizer_trace | 0 | 0 | DEFAULT | optimizer trace を有効にします。 | UInt64 |
| enable_parallel_multi_merge_sort | 1 | 1 | DEFAULT | parallel multi merge sort を有効にします。 | UInt64 |
| enable_parallel_union_all | 0 | 0 | DEFAULT | 並列 UNION ALL を有効にします。デフォルトは 0、1 で有効です。 | UInt64 |
| enable_parquet_page_index | 1 | 1 | DEFAULT | parquet page index を有効にします。 | UInt64 |
| enable_parquet_prewhere | 0 | 0 | DEFAULT | parquet prewhere を有効にします。 | UInt64 |
| enable_parquet_rowgroup_pruning | 1 | 1 | DEFAULT | parquet rowgroup pruning を有効にします。 | UInt64 |
| enable_planner_cache | 1 | 1 | DEFAULT | 同一クエリの論理プランのキャッシュを有効にします。 | UInt64 |
| enable_proxy_bloom_pruning | 0 | 0 | DEFAULT | PROXY の軽量ルート推定中に bloom index pruning を有効にします。ルーティングを低コストに保つため、デフォルトでは無効です。 | UInt64 |
| enable_prune_cache | 1 | 1 | DEFAULT | pruning 結果のキャッシュを有効にします。 | UInt64 |
| enable_prune_pipeline | 1 | 1 | DEFAULT | pruning pipeline を有効にします。 | UInt64 |
| enable_query_result_cache | 0 | 0 | DEFAULT | 同一クエリのパフォーマンス向上のため、クエリ結果のキャッシュを有効にします。 | UInt64 |
| enable_refresh_aggregating_index_after_write | 1 | 1 | DEFAULT | 新しいデータの書き込み後に aggregating index を更新します。 | UInt64 |
| enable_replace_into_partitioning | 1 | 1 | DEFAULT | replace-into ステートメントの partitioning を有効にします (テーブルにクラスターキーがある場合)。 | UInt64 |
| enable_result_set_spilling | 0 | 0 | DEFAULT | メモリ使用量がしきい値を超えたときに、結果セットデータをストレージへスピルすることを有効にします。 | UInt64 |
| enable_selector_executor | 1 | 1 | DEFAULT | filter expression 用の selector executor を有効にします。 | UInt64 |
| enable_shuffle_sort | 0 | 0 | DEFAULT | shuffle sort を有効にします。 | UInt64 |
| enable_sort_spill_prefetch | 1 | 1 | DEFAULT | スピルされた sort ブロックに対する非同期 restore prefetch を有効にします。 | UInt64 |
| enable_sort_spill_stream_regroup | 1 | 1 | DEFAULT | merge 前にドメインごとに sort spill stream を再グループ化することを有効にします。 | UInt64 |
| enable_strict_datetime_parser | 1 | 1 | DEFAULT | 有効な場合、datetime 関数は ISO 8601 形式のみを受け付けます。無効な場合は、best-effort parsing にフォールバックします。 | UInt64 |
| enable_table_lock | 1 | 1 | DEFAULT | 必要に応じてテーブルロックを有効にします (デフォルトで有効)。 | UInt64 |
| enable_table_snapshot_stats | 0 | 0 | DEFAULT | スナップショットに対する analyze table statistics を有効にします。 | UInt64 |
| enforce_broadcast_join | 0 | 0 | DEFAULT | broadcast join を強制します。 | UInt64 |
| enforce_local | 0 | 0 | DEFAULT | ローカルプランを強制します。 | UInt64 |
| enforce_shuffle_join | 0 | 0 | DEFAULT | shuffle join を強制します。 | UInt64 |
| error_on_nondeterministic_update | 1 | 1 | DEFAULT | 複数結合された行を更新する際にエラーを返すかどうかを指定します。 | UInt64 |
| external_server_connect_timeout_secs | 10 | 10 | DEFAULT | 外部サーバーへの接続タイムアウトです。 | UInt64 |
| external_server_request_batch_rows | 65536 | 65536 | DEFAULT | 外部サーバーへのリクエスト時のバッチ行数です。 | UInt64 |
| external_server_request_max_threads | 256 | 256 | DEFAULT | 外部サーバーへのリクエスト時の最大スレッド数です。 | UInt64 |
| external_server_request_retry_times | 8 | 8 | DEFAULT | 外部サーバーへのリクエスト時の最大リトライ回数です。 | UInt64 |
| external_server_request_timeout_secs | 180 | 180 | DEFAULT | 外部サーバーへのリクエストタイムアウトです。 | UInt64 |
| flight_client_keep_alive_interval_secs | 0 | 0 | DEFAULT | 2 回の flight TCP keepalive probe の間隔を秒単位で設定します。0 で keepalive を無効にします。 | UInt64 |
| flight_client_keep_alive_retries | 0 | 0 | DEFAULT | flight 接続で peer を到達不能と判断する前の TCP keepalive リトライ回数を設定します。0 で keepalive を無効にします。 | UInt64 |
| flight_client_keep_alive_time_secs | 0 | 0 | DEFAULT | flight TCP 接続が keepalive probe を送信するまでのアイドル時間を秒単位で設定します。0 で keepalive を無効にします。 | UInt64 |
| flight_client_timeout | 60 | 60 | DEFAULT | flight client リクエストを処理できる最大時間を秒単位で設定します。 | UInt64 |
| flight_connection_max_retry_times | 0 | 0 | DEFAULT | クラスター flight の最大リトライ回数です。0 の場合は無効です。 | UInt64 |
| flight_connection_retry_interval | 1 | 1 | DEFAULT | クラスター flight のリトライ間隔を秒単位で設定します。 | UInt64 |
| force_aggregate_data_spill | 0 | 0 | DEFAULT | テスト専用です。有効にすると、集計データは強制的に外部ストレージへスピルされます。 | UInt64 |
| force_aggregate_shuffle_mode | auto | auto | DEFAULT | テスト専用です。集計の shuffle モードです。オプション: 'auto'、'row'、'bucket'。 | String |
| force_eager_aggregate | 0 | 0 | DEFAULT | eager aggregate ルールの適用を強制します。 | UInt64 |
| force_join_data_spill | 0 | 0 | DEFAULT | テスト専用です。有効にすると、join データは強制的に外部ストレージへスピルされます。 | UInt64 |
| force_materialized_cte_spill | 0 | 0 | DEFAULT | テスト専用です。有効にすると、materialized CTE データは強制的に外部ストレージへスピルされます。 | UInt64 |
| force_sort_data_spill | 0 | 0 | DEFAULT | テスト専用です。有効にすると、sort データは強制的に外部ストレージへスピルされます。 | UInt64 |
| force_window_data_spill | 0 | 0 | DEFAULT | テスト専用です。有効にすると、window データは強制的に外部ストレージへスピルされます。 | UInt64 |
| format_null_as_str | 0 | 0 | DEFAULT | query api レスポンスで NULL を文字列としてフォーマットします。 | UInt64 |
| geometry_output_format | GeoJSON | GeoJSON | DEFAULT | GEOMETRY 値の表示形式です。値: "WKT"、"WKB"、"EWKT"、"EWKB"、"GeoJSON"。 | String |
| group_by_shuffle_mode | before_merge | before_merge | DEFAULT | Group by の shuffle モードです。'before_partial' はよりバランスが取れますが、より多くのデータ交換が必要です。 | String |
| grouping_sets_channel_size | 2 | 2 | DEFAULT | grouping sets から union への変換に使用するチャネルサイズを設定します。 | UInt64 |
| grouping_sets_to_union | 0 | 0 | DEFAULT | grouping sets から union への変換を有効にします。 | UInt64 |
| hash_shuffle_bytes_threshold | 4194304 | 4194304 | DEFAULT | hash shuffle block partition stream の最大バイトしきい値を設定します。 | UInt64 |
| hash_shuffle_rows_threshold | 8192 | 8192 | DEFAULT | hash shuffle block partition stream の最大行数しきい値を設定します。 | UInt64 |
| hide_options_in_show_create_table | 1 | 1 | DEFAULT | SHOW TABLE CREATE の末尾にある SNAPSHOT_LOCATION や STORAGE_FORMAT などのテーブル関連情報を非表示にします。 | UInt64 |
| hilbert_clustering_min_bytes | 107374182400 | 107374182400 | DEFAULT | Hilbert Clustering のブロック最小バイトサイズを設定します。 | UInt64 |
| hilbert_num_range_ids | 1000 | 1000 | DEFAULT | Hilbert clustering における range ID のドメインを指定します。値を大きくすると粒度は細かくなりますが、パフォーマンスコストが発生する可能性があります。 | UInt64 |
| hilbert_sample_size_per_block | 1000 | 1000 | DEFAULT | Hilbert clustering で使用するブロックごとのサンプルポイント数を指定します。 | UInt64 |
| hive_parquet_chunk_size | 16384 | 16384 | DEFAULT | parquet から {{{ .lake }}} processor へ 1 回の読み取りで取得する最大行数です。 | UInt64 |
| http_handler_result_timeout_secs | 240 | 240 | DEFAULT | poll がない状態で http クエリセッションが期限切れになるまでのタイムアウトを秒単位で設定します。 | UInt64 |
| http_json_result_mode | display | display | DEFAULT | HTTP クエリ JSON データのエンコード方法を制御します。値: "display"、"driver"。 | String |
| idle_transaction_timeout_secs | 14400 | 14400 | DEFAULT | クエリがないアクティブセッションのタイムアウトを秒単位で設定します。 | UInt64 |
| inlist_runtime_bloom_prune_threshold | 64 | 64 | DEFAULT | ランタイム block bloom pruning における IN リストの最大値数を設定します。 | UInt64 |
| inlist_runtime_filter_threshold | 1024 | 1024 | DEFAULT | ランタイムフィルター生成における IN リストの最大値数を設定します。 | UInt64 |
| inlist_to_join_threshold | 1024 | 1024 | DEFAULT | IN リストを JOIN に変換するしきい値を設定します。 | UInt64 |
| input_read_buffer_size | 4194304 | 4194304 | DEFAULT | バッファ付きリーダーがストレージからデータを読み取る際に使用するバッファへ割り当てるメモリサイズをバイト単位で設定します。 | UInt64 |
| join_runtime_filter_selectivity_threshold | 10 | 10 | DEFAULT | bloom join ランタイムフィルターの選択率しきい値 (パーセンテージ) です。デフォルトの 10 は 10% を意味します。 | UInt64 |
| join_spilling_buffer_threshold_per_proc_mb | 512 | 512 | DEFAULT | 各 join processor のスピルバッファしきい値 (MB) を設定します。 | UInt64 |
| join_spilling_memory_ratio | 60 | 60 | LOCAL | hash join がデータをストレージにスピルする前に使用できる最大メモリ比率をバイト単位で設定します。0 は無制限です。 | UInt64 |
| join_spilling_partition_bits | 4 | 4 | DEFAULT | join spilling のパーティション数を設定します。デフォルト値は 4 で、2^4 パーティションを意味します。 | UInt64 |
| lazy_read_across_join_threshold | 10 | 10 | DEFAULT | join をまたぐ lazy read 最適化を有効にするクエリ内の最大 LIMIT を設定します。0 に設定するとこの最適化を無効にします。 | UInt64 |
| lazy_read_threshold | 1000 | 1000 | DEFAULT | lazy read 最適化を有効にするクエリ内の最大 LIMIT を設定します。0 に設定するとこの最適化を無効にします。 | UInt64 |
| load_file_metadata_expire_hours | 24 | 24 | DEFAULT | COPY INTO でロード (load) されたファイルのメタデータが期限切れになるまでの時間を時間単位で設定します。 | UInt64 |
| materialized_cte_spilling_memory_ratio | 60 | 60 | DEFAULT | materialized CTE 実行がデータをストレージにスピルする前に使用できる最大メモリ比率をバイト単位で設定します。0 は無制限です。 | UInt64 |
| max_aggregate_restore_worker | 16 | 16 | DEFAULT | aggregate restore の最大 worker 数を設定します。 | UInt64 |
| max_aggregate_spill_level | 3 | 3 | DEFAULT | aggregate spill の最大再帰深度です。各レベルでデータは 4 つのより小さい部分に再パーティション化されます。 | UInt64 |
| max_block_bytes | 52428800 | 52428800 | DEFAULT | 読み取り可能な単一データブロックの最大バイトサイズを設定します。 | UInt64 |
| max_block_size | 65536 | 65536 | DEFAULT | 読み取り可能な単一データブロックの最大行数を設定します。 | UInt64 |
| max_cte_recursive_depth | 1000 | 1000 | DEFAULT | 再帰 CTE の最大再帰深度です。 | UInt64 |
| max_execute_time_in_seconds | 0 | 0 | DEFAULT | クエリ実行時間の最大値を秒単位で設定します。0 は無制限を意味します。 | UInt64 |
| max_hash_join_spill_level | 1 | 1 | DEFAULT | hash join spill の最大再帰深度です。各レベルでデータは 16 個のより小さい部分に再パーティション化されます。 | UInt64 |
| max_inlist_to_or | 3 | 3 | DEFAULT | OR 演算子に変換される IN 式に含められる値の最大数を設定します。 | UInt64 |
| max_memory_usage | 51539607552 | 51539607552 | DEFAULT | 単一クエリの処理に使用できる最大メモリ使用量をバイト単位で設定します。 | UInt64 |
| max_public_keys_per_user | 10 | 10 | DEFAULT | キーペア認証でユーザーごとに許可される公開鍵の最大数です。 | UInt64 |
| max_push_down_limit | 10000 | 10000 | DEFAULT | leaf operator に push down できる行数制限の最大値を設定します。 | UInt64 |
| max_query_memory_usage | 25769803776 | 25769803776 | LOCAL | クエリの最大メモリ使用量です。0 に設定するとメモリ使用量は無制限です。 | UInt64 |
| max_result_rows | 0 | 0 | DEFAULT | クエリ結果で返せる最大行数を設定します。0 は無制限を意味します。 | UInt64 |
| max_set_operator_count | 18446744073709551615 | 18446744073709551615 | DEFAULT | クエリ内の set operator の最大数です。 | UInt64 |
| max_spill_io_requests | 8 | 8 | DEFAULT | 同時実行可能な spill I/O リクエストの最大数を設定します。 | UInt64 |
| max_storage_io_requests | 64 | 64 | DEFAULT | 同時実行可能なストレージ I/O リクエストの最大数を設定します。 | UInt64 |
| max_threads | 8 | 8 | DEFAULT | リクエスト実行に使用する最大スレッド数を設定します。 | UInt64 |
| max_vacuum_temp_files_after_query | 18446744073709551615 | 18446744073709551615 | DEFAULT | クエリ後に削除される temp file の最大数です。0 の場合は無効です。 | UInt64 |
| max_vacuum_threads | 1 | 1 | DEFAULT | vacuum 操作の実行に使用する最大スレッド数を設定します。 | UInt64 |
| min_max_runtime_filter_threshold | 18446744073709551615 | 18446744073709551615 | DEFAULT | min-max ランタイムフィルター生成の最大行数を設定します。 | UInt64 |
| nested_loop_join_threshold | 10000 | 10000 | DEFAULT | nested loop join を使用するしきい値を設定します。0 に設定すると nested loop join を無効にします。 | UInt64 |
| network_policy |  |  | DEFAULT | テナント内のすべてのユーザーに対する network policy です。 | String |
| numeric_cast_option | rounding | rounding | DEFAULT | 数値 cast モードを "rounding" または "truncating" に設定します。 | String |
| optimizer_skip_list |  |  | DEFAULT | クエリ最適化中にスキップする optimizer 名のカンマ区切りリストです。 | String |
| parquet_fast_read_bytes | 1048576 | 1048576 | LOCAL | サイズの小さい Parquet ファイルは、カラムごとではなくファイル全体として読み取られます。デフォルト値: 1MB。 | UInt64 |
| parquet_max_block_size | 8192 | 8192 | DEFAULT | parquet reader の最大ブロックサイズです。 | UInt64 |
| parquet_rowgroup_hint_bytes | 134217728 | 134217728 | DEFAULT | 大きな parquet ファイルを読み取り用に複数の rowgroup に分割する際のヒントとなるバイト数です。デフォルト値: 128MB。 | UInt64 |
| parse_datetime_ignore_remainder | 1 | 1 | GLOBAL | 文字列を datetime に解析する際に末尾の文字を無視します。 | UInt64 |
| persist_materialized_cte | 1 | 1 | DEFAULT | materialized CTE をディスクに永続化するかどうかを決定します。 | UInt64 |
| prefer_broadcast_join | 1 | 1 | DEFAULT | broadcast join を有効にします。 | UInt64 |
| prewhere_selectivity_threshold | 100 | 100 | DEFAULT | prewhere 中に行選択を残りカラムの読み取りへ push down するための最大選択率パーセンテージです。 | UInt64 |
| proxy_routing_model | statistics | statistics | DEFAULT | PROXY がターゲットテーブルを選択する方法を制御します。値: 'statistics'、'prefix'。 | String |
| purge_duplicated_files_in_copy | 0 | 0 | DEFAULT | copy into table 実行中に検出された重複ファイルを削除します。 | UInt64 |
| queries_queue_retry_timeout | 300 | 300 | DEFAULT | クエリキュータイムアウトのリトライ間隔です。再試行しない場合は 0 です。 | UInt64 |
| query_flight_compression | LZ4 | LZ4 | DEFAULT | Flight の圧縮方式です。値: "None"、"LZ4"、"ZSTD"。 | String |
| query_out_of_memory_behavior | spilling | spilling | LOCAL | クエリのメモリ制限を超えた場合、システムは事前定義されたアクションを適用します。値: "throw"、"spilling"。 | String |
| query_result_cache_allow_inconsistent | 0 | 0 | DEFAULT | {{{ .lake }}} が基になるデータと不整合なキャッシュ済みクエリ結果を返すかどうかを決定します。 | UInt64 |
| query_result_cache_max_bytes | 1048576 | 1048576 | DEFAULT | 単一クエリ結果のキャッシュに使用できる最大バイトサイズを設定します。 | UInt64 |
| query_result_cache_min_execute_secs | 1 | 1 | DEFAULT | クエリをキャッシュするには、最初のブロック取得に少なくともこの秒数がかかる必要があります。 | UInt64 |
| query_result_cache_ttl_secs | 300 | 300 | DEFAULT | キャッシュされたクエリ結果の time-to-live (TTL) を秒単位で設定します。 | UInt64 |
| query_tag |  |  | DEFAULT | このセッションの query tag を設定します。 | String |
| quoted_ident_case_sensitive | 1 | 1 | GLOBAL | 引用付き名前を大文字小文字区別ありで扱うには 1、区別なしで扱うには 0 に設定します。 | UInt64 |
| random_function_seed | 0 | 0 | DEFAULT | random 関数のシードです。 | UInt64 |
| recluster_block_size | 9277129359 | 9277129359 | DEFAULT | recluster 用ブロックの最大バイトサイズを設定します。 | UInt64 |
| recluster_timeout_secs | 43200 | 43200 | DEFAULT | recluster final のタイムアウトまでの秒数を設定します。 | UInt64 |
| replace_into_bloom_pruning_max_column_number | 4 | 4 | DEFAULT | replace-into ステートメントで bloom pruning に使用されるカラムの最大数です。 | UInt64 |
| replace_into_shuffle_strategy | 0 | 0 | DEFAULT | shuffle 戦略を選択します: 0 は Block、1 は Segment レベルです。 | UInt64 |
| s3_storage_class | STANDARD | STANDARD | DEFAULT | デフォルトの S3 storage class です。値: "STANDARD"、"INTELLIGENT_TIERING"。 | String |
| sandbox_tenant |  |  | DEFAULT | このセッションにカスタムの 'sandbox_tenant' を注入します。テスト目的専用です。 | String |
| script_max_steps | 10000 | 10000 | DEFAULT | script の 1 回の実行で許可される最大ステップ数です。 | UInt64 |
| short_sql_max_length | 2048 | 2048 | DEFAULT | short_sql 関数で SQL クエリを切り詰める最大長を設定します。 | UInt64 |
| sort_spilling_batch_bytes | 20971520 | 20971520 | DEFAULT | merge sorter がストレージへスピルする非圧縮サイズを設定します。 | UInt64 |
| sort_spilling_memory_ratio | 60 | 60 | LOCAL | クエリ実行中に、sorter がデータをストレージにスピルする前に使用できる最大メモリ比率をバイト単位で設定します。 | UInt64 |
| spatial_runtime_filter_threshold | 1024 | 1024 | DEFAULT | spatial list におけるランタイムフィルター生成の最大値数を設定します。 | UInt64 |
| spill_writer_memory_pool_size_mb | 20 | 20 | DEFAULT | 各 spill writer のメモリプールサイズ (MB) を設定します。 | UInt64 |
| spilling_file_format | parquet | parquet | DEFAULT | spilling に使用するストレージファイル形式を設定します。値: "arrow"、"parquet"。 | String |
| spilling_to_disk_vacuum_unknown_temp_dirs_limit | 18446744073709551615 | 18446744073709551615 | DEFAULT | 予期せず中断されたクエリに対してクリーンアップするディレクトリの最大数を設定します。 | UInt64 |
| sql_dialect | PostgreSQL | PostgreSQL | DEFAULT | SQL 方言を設定します。使用可能な値: "PostgreSQL"、"MySQL"、"Experimental"、"Hive"、"Prql"。 | String |
| statement_queue_ttl_in_seconds | 15 | 15 | DEFAULT | meta service との lease 更新操作の間隔を秒単位で設定します。 | UInt64 |
| statement_queued_timeout_in_seconds | 0 | 0 | DEFAULT | キュー内で待機できる最大秒数です。デフォルト値は 0 (無制限) です。 | UInt64 |
| storage_fetch_part_num | 2 | 2 | DEFAULT | クエリ実行中にストレージから並列取得するパーティション数を設定します。 | UInt64 |
| storage_io_max_page_bytes_for_read | 524288 | 524288 | DEFAULT | 1 回の I/O 操作でストレージから読み取れるデータページの最大バイトサイズを設定します。 | UInt64 |
| storage_io_min_bytes_for_seek | 48 | 48 | DEFAULT | 新しい位置を seek する際に、1 回の I/O 操作でストレージから読み取る必要があるデータの最小バイトサイズを設定します。 | UInt64 |
| storage_read_buffer_size | 1048576 | 1048576 | DEFAULT | データをメモリに読み込むために使用するバッファのバイトサイズを設定します。 | UInt64 |
| stream_consume_batch_size_hint | 0 | 0 | DEFAULT | stream 消費時のバッチサイズのヒントです。無効にするには 0 に設定します。 | UInt64 |
| system_tables_count_db_concurrency | 16 | 16 | DEFAULT | system.tables count 最適化で使用する DB レベルの並行性を設定します。 | UInt64 |
| table_lock_expire_secs | 30 | 30 | DEFAULT | テーブルロックの有効期限までの秒数を設定します。 | UInt64 |
| timezone | UTC | UTC | DEFAULT | タイムゾーンを設定します。 | String |
| trace_sample_rate | 1 | 1 | DEFAULT | trace sample rate を設定します。値は '0' から '100' の間である必要があります。 | UInt64 |
| udf_cloud_import_presign_expire_secs | 259200 | 259200 | DEFAULT | クラウド UDF stage import の presign 有効期限です。 | UInt64 |
| unquoted_ident_case_sensitive | 0 | 0 | DEFAULT | 引用なし名前を大文字小文字区別ありにするには 1、区別なしにするには 0 に設定します。 | UInt64 |
| use_legacy_query_executor | 0 | 0 | DEFAULT | legacy query executor にフォールバックします。 | UInt64 |
| use_parquet2 | 0 | 0 | DEFAULT | この設定は非推奨です。 | UInt64 |
| warehouse |  |  | DEFAULT | warehouse を設定するには `USE WAREHOUSE` ステートメントを使用してください。 | String |
| week_start | 1 | 1 | DEFAULT | 週の最初の日を指定します (週関連の日付関数で使用)。 | UInt64 |
| window_num_partitions | 256 | 256 | DEFAULT | window operator のパーティション数を設定します。 | UInt64 |
| window_partition_sort_block_size | 65536 | 65536 | DEFAULT | window partition でソートするデータブロックのブロックサイズを設定します。 | UInt64 |
| window_partition_spilling_memory_ratio | 60 | 60 | GLOBAL | window partitioner がデータをストレージにスピルする前に使用できる最大メモリ比率をバイト単位で設定します。 | UInt64 |
| window_spill_unit_size_mb | 256 | 256 | DEFAULT | window operator のスピル単位サイズ (MB) を設定します。 | UInt64 |