---
title: system.settings
summary: Stores the system settings of the current session.
---

# system.settings

> **Note:**
>
> Introduced or updated in v1.2.745.

Stores the system settings of the current session.

```sql
SELECT * FROM system.settings;
```

| Name | Value | Default | Level | Description | Type |
|------|-------|---------|-------|-------------|------|
| acquire_lock_timeout | 30 | 30 | DEFAULT | Sets the maximum timeout in seconds for acquire a lock. | UInt64 |
| aggregate_spilling_memory_ratio | 60 | 60 | LOCAL | Sets the maximum memory ratio in bytes that an aggregator can use before spilling data to storage during query execution. | UInt64 |
| allow_query_exceeded_limit | 0 | 0 | DEFAULT | Allow queries to overshoot the configured memory limit, deferring error notification until memory contention is encountered. | UInt64 |
| auto_compaction_imperfect_blocks_threshold | 25 | 25 | GLOBAL | Threshold for triggering auto compaction after write. Set to 0 to disable auto compaction. | UInt64 |
| auto_compaction_segments_limit | 3 | 3 | DEFAULT | The maximum number of segments that can be reclustered automatically triggered after write. | UInt64 |
| binary_input_format | utf-8 | utf-8 | DEFAULT | Controls how string literals are interpreted when inserted into BINARY columns (HEX, BASE64, UTF-8, or UTF-8-LOSSY). | String |
| binary_output_format | hex | hex | DEFAULT | Controls how BINARY columns are rendered (HEX, BASE64, UTF-8, or UTF-8-LOSSY). | String |
| bloom_runtime_filter_threshold | 3000000 | 3000000 | DEFAULT | Sets the maximum number of rows for bloom runtime filter generation. | UInt64 |
| collation | utf8 | utf8 | DEFAULT | Sets the character collation. Available values include "utf8". | String |
| compact_max_block_selection | 1000 | 1000 | DEFAULT | Limits the maximum number of imperfect blocks that can be selected during a compact operation. | UInt64 |
| copy_dedup_full_path_by_default | 0 | 0 | DEFAULT | The default value if table option copy_dedup_full_path is not set when creating table. | UInt64 |
| cost_factor_aggregate_per_row | 5 | 5 | DEFAULT | Cost factor of grouping operation for a data row. | UInt64 |
| cost_factor_hash_table_per_row | 10 | 10 | DEFAULT | Cost factor of building hash table for a data row. | UInt64 |
| cost_factor_network_per_row | 50 | 50 | DEFAULT | Cost factor of transmit via network for a data row. | UInt64 |
| create_query_flight_client_with_current_rt | 1 | 1 | DEFAULT | Turns on (1) or off (0) the use of the current runtime for query operations. | UInt64 |
| data_retention_num_snapshots_to_keep | 0 | 0 | DEFAULT | Specifies how many snapshots to retain during vacuum operations. Overrides data_retention_time_in_days. If set to 0, this setting will be ignored. | UInt64 |
| data_retention_time_in_days | 1 | 1 | DEFAULT | Sets the data retention time in days. | UInt64 |
| date_format_style | Oracle | Oracle | DEFAULT | Sets the date format style (used by datetime functions). Available values: "MySQL", "Oracle". | String |
| ddl_column_type_nullable | 1 | 1 | DEFAULT | Sets new columns to be nullable (1) or not (0) by default in table operations. | UInt64 |
| default_order_by_null | nulls_last | nulls_last | DEFAULT | Set numeric default_order_by_null mode. Values: "nulls_first", "nulls_last", "nulls_first_on_asc_last_on_desc". | String |
| disable_join_reorder | 0 | 0 | DEFAULT | Disable join reorder optimization. | UInt64 |
| disable_variant_check | 0 | 0 | DEFAULT | Disable variant check to allow insert invalid JSON values. | UInt64 |
| dynamic_sample_time_budget_ms | 0 | 0 | DEFAULT | Time budget for dynamic sample in milliseconds. | UInt64 |
| enable_aggregating_index_scan | 1 | 1 | DEFAULT | Enables scanning aggregating index data while querying. | UInt64 |
| enable_analyze_histogram | 0 | 0 | DEFAULT | Enables analyze histogram for query optimization during analyzing table. | UInt64 |
| enable_auto_analyze | 1 | 1 | DEFAULT | Enables automatically analyze after write. 0 for disable, 1 for enable. | UInt64 |
| enable_auto_detect_datetime_format | 0 | 0 | DEFAULT | Enable auto-detection for non-ISO datetime formats. Works across functions, COPY, and VARIANT cast. | UInt64 |
| enable_auto_fix_missing_bloom_index | 0 | 0 | DEFAULT | Enables auto fix missing bloom index. | UInt64 |
| enable_auto_materialize_cte | 1 | 1 | DEFAULT | Enables auto materialize CTE. 0 for disable, 1 for enable. | UInt64 |
| enable_auto_vacuum | 0 | 0 | DEFAULT | Whether to automatically trigger VACUUM operations on tables. | UInt64 |
| enable_backpressure_spiller | 0 | 0 | DEFAULT | Use new backpressure spiller. | UInt64 |
| enable_block_stream_write | 1 | 1 | GLOBAL | Enables block stream write. | UInt64 |
| enable_bloom_runtime_filter | 1 | 1 | DEFAULT | Enables bloom runtime filter optimization for JOIN. | UInt64 |
| enable_cbo | 1 | 1 | DEFAULT | Enables cost-based optimization. | UInt64 |
| enable_compact_after_multi_table_insert | 0 | 0 | DEFAULT | Enables recluster and compact after multi-table insert. | UInt64 |
| enable_compact_after_write | 1 | 1 | DEFAULT | Enables compact after write (copy/insert/replace-into/merge-into), needs more memory. | UInt64 |
| enable_cse_optimizer | 0 | 0 | DEFAULT | Enables common subexpression elimination optimization. | UInt64 |
| enable_decimal_sum_widening | 0 | 0 | DEFAULT | Automatically widen SUM arguments from Decimal(19..38, scale) to Decimal(76, scale). | UInt64 |
| enable_dio | 1 | 1 | DEFAULT | Enables Direct IO. | UInt64 |
| enable_distributed_compact | 0 | 0 | DEFAULT | Enables distributed execution of table compaction. | UInt64 |
| enable_distributed_copy_into | 1 | 1 | DEFAULT | Enables distributed execution for the 'COPY INTO'. | UInt64 |
| enable_distributed_merge_into | 1 | 1 | DEFAULT | Enables distributed execution for 'MERGE INTO'. | UInt64 |
| enable_distributed_pruning | 1 | 1 | DEFAULT | Enable distributed index pruning. | UInt64 |
| enable_distributed_recluster | 1 | 1 | GLOBAL | Enable distributed execution of table recluster. | UInt64 |
| enable_distributed_replace_into | 0 | 0 | DEFAULT | Enables distributed execution of 'REPLACE INTO'. | UInt64 |
| enable_dphyp | 1 | 1 | DEFAULT | Enables dphyp join order algorithm. | UInt64 |
| enable_dst_hour_fix | 0 | 0 | DEFAULT | Time conversion handles invalid DST by adding an hour. Accuracy not guaranteed (disabled by default). | UInt64 |
| enable_expand_roles | 1 | 1 | DEFAULT | Enable expand roles when execute show grants statement (enabled by default). | UInt64 |
| enable_experiment_aggregate | 1 | 1 | DEFAULT | Enable experiment aggregate (enabled by default). | UInt64 |
| enable_experiment_hash_index | 1 | 1 | DEFAULT | Experiment setting: enable hash index (enabled by default). | UInt64 |
| enable_experimental_connection_privilege_check | 0 | 0 | DEFAULT | Experiment setting: enable connection object privilege check (disabled by default). | UInt64 |
| enable_experimental_new_join | 1 | 1 | DEFAULT | Enables the experimental new join implementation. | UInt64 |
| enable_experimental_procedure | 1 | 1 | GLOBAL | Enables the experimental feature for 'PROCEDURE'. | UInt64 |
| enable_experimental_rbac_check | 1 | 1 | DEFAULT | Experiment setting: enable stage and udf privilege check (enabled by default). | UInt64 |
| enable_experimental_row_access_policy | 0 | 0 | DEFAULT | Experiment setting: enable row access policy (disabled by default). | UInt64 |
| enable_experimental_sequence_privilege_check | 0 | 0 | DEFAULT | Experiment setting: enable sequence object privilege check (disabled by default). | UInt64 |
| enable_experimental_table_ref | 0 | 0 | DEFAULT | Experiment setting: enable table ref (disabled by default). | UInt64 |
| enable_experimental_virtual_column | 0 | 0 | DEFAULT | Enables experimental virtual column. | UInt64 |
| enable_fixed_rows_sort | 1 | 1 | DEFAULT | Enable fixed rows sort serialize. | UInt64 |
| enable_geo_create_table | 1 | 1 | DEFAULT | Create and alter table with geometry/geography type. | UInt64 |
| enable_group_by_column_first | 0 | 0 | DEFAULT | Resolve GROUP BY names to input columns before SELECT aliases. Disabled by default for compatibility. | UInt64 |
| enable_hive_parquet_predict_pushdown | 1 | 1 | DEFAULT | Enables hive parquet predict pushdown by setting this variable to 1. Default value: 1. | UInt64 |
| enable_join_runtime_filter | 1 | 1 | DEFAULT | Enables runtime filter optimization for JOIN. | UInt64 |
| enable_last_snapshot_location_hint | 1 | 1 | DEFAULT | Enables writing last_snapshot_location_hint object. | UInt64 |
| enable_loser_tree_merge_sort | 1 | 1 | DEFAULT | Enables loser tree merge sort. | UInt64 |
| enable_materialized_cte | 1 | 1 | DEFAULT | Enable materialized common table expression. | UInt64 |
| enable_merge_into_row_fetch | 1 | 1 | DEFAULT | Enable merge into row fetch optimization. | UInt64 |
| enable_mutation_block_id_repartition | 1 | 1 | DEFAULT | Enable local block_id repartition before row fetch in join-based mutations to reduce duplicate block reads. | UInt64 |
| enable_new_copy_for_text_formats | 1 | 1 | DEFAULT | Use new implementation for loading CSV files. | UInt64 |
| enable_optimizer_trace | 0 | 0 | DEFAULT | Enables optimizer trace. | UInt64 |
| enable_parallel_multi_merge_sort | 1 | 1 | DEFAULT | Enables parallel multi merge sort. | UInt64 |
| enable_parallel_union_all | 0 | 0 | DEFAULT | Enable parallel UNION ALL. Default is 0, 1 for enable. | UInt64 |
| enable_parquet_page_index | 1 | 1 | DEFAULT | Enables parquet page index. | UInt64 |
| enable_parquet_prewhere | 0 | 0 | DEFAULT | Enables parquet prewhere. | UInt64 |
| enable_parquet_rowgroup_pruning | 1 | 1 | DEFAULT | Enables parquet rowgroup pruning. | UInt64 |
| enable_planner_cache | 1 | 1 | DEFAULT | Enables caching logic plan from same query. | UInt64 |
| enable_proxy_bloom_pruning | 0 | 0 | DEFAULT | Enable bloom index pruning during PROXY lightweight route estimation. Disabled by default to keep routing cheap. | UInt64 |
| enable_prune_cache | 1 | 1 | DEFAULT | Enable to cache the pruning result. | UInt64 |
| enable_prune_pipeline | 1 | 1 | DEFAULT | Enable pruning pipeline. | UInt64 |
| enable_query_result_cache | 0 | 0 | DEFAULT | Enables caching query results to improve performance for identical queries. | UInt64 |
| enable_refresh_aggregating_index_after_write | 1 | 1 | DEFAULT | Refresh aggregating index after new data written. | UInt64 |
| enable_replace_into_partitioning | 1 | 1 | DEFAULT | Enables partitioning for replace-into statement (if table has cluster keys). | UInt64 |
| enable_result_set_spilling | 0 | 0 | DEFAULT | Enable spilling result set data to storage when memory usage exceeds the threshold. | UInt64 |
| enable_selector_executor | 1 | 1 | DEFAULT | Enables selector executor for filter expression. | UInt64 |
| enable_shuffle_sort | 0 | 0 | DEFAULT | Enable shuffle sort. | UInt64 |
| enable_sort_spill_prefetch | 1 | 1 | DEFAULT | Enable asynchronous restore prefetch for spilled sort blocks. | UInt64 |
| enable_sort_spill_stream_regroup | 1 | 1 | DEFAULT | Enable regrouping sort spill streams by domain before merge. | UInt64 |
| enable_strict_datetime_parser | 1 | 1 | DEFAULT | When enabled, datetime functions only accept ISO 8601 formats. When disabled, falls back to best-effort parsing. | UInt64 |
| enable_table_lock | 1 | 1 | DEFAULT | Enables table lock if necessary (enabled by default). | UInt64 |
| enable_table_snapshot_stats | 0 | 0 | DEFAULT | Enable analyze table statistics for snapshots. | UInt64 |
| enforce_broadcast_join | 0 | 0 | DEFAULT | Enforce broadcast join. | UInt64 |
| enforce_local | 0 | 0 | DEFAULT | Enforce local plan. | UInt64 |
| enforce_shuffle_join | 0 | 0 | DEFAULT | Enforce shuffle join. | UInt64 |
| error_on_nondeterministic_update | 1 | 1 | DEFAULT | Whether to return an error when updating a multi-joined row. | UInt64 |
| external_server_connect_timeout_secs | 10 | 10 | DEFAULT | Connection timeout to external server. | UInt64 |
| external_server_request_batch_rows | 65536 | 65536 | DEFAULT | Request batch rows to external server. | UInt64 |
| external_server_request_max_threads | 256 | 256 | DEFAULT | Request maximum number of threads to external server. | UInt64 |
| external_server_request_retry_times | 8 | 8 | DEFAULT | Request max retry times to external server. | UInt64 |
| external_server_request_timeout_secs | 180 | 180 | DEFAULT | Request timeout to external server. | UInt64 |
| flight_client_keep_alive_interval_secs | 0 | 0 | DEFAULT | Sets the interval in seconds between two flight TCP keepalive probes. 0 disables keepalive. | UInt64 |
| flight_client_keep_alive_retries | 0 | 0 | DEFAULT | Sets the number of TCP keepalive retries for flight connections before declaring the peer unreachable. 0 disables keepalive. | UInt64 |
| flight_client_keep_alive_time_secs | 0 | 0 | DEFAULT | Sets the idle time in seconds before a flight TCP connection sends keepalive probes. 0 disables keepalive. | UInt64 |
| flight_client_timeout | 60 | 60 | DEFAULT | Sets the maximum time in seconds that a flight client request can be processed. | UInt64 |
| flight_connection_max_retry_times | 0 | 0 | DEFAULT | The maximum retry count for cluster flight. Disable if 0. | UInt64 |
| flight_connection_retry_interval | 1 | 1 | DEFAULT | The retry interval of cluster flight in seconds. | UInt64 |
| force_aggregate_data_spill | 0 | 0 | DEFAULT | For testing only. Aggregate data will be forcibly spilled to external storage if enabled. | UInt64 |
| force_aggregate_shuffle_mode | auto | auto | DEFAULT | For testing only. Shuffle mode for aggregation. Options: 'auto', 'row', 'bucket'. | String |
| force_eager_aggregate | 0 | 0 | DEFAULT | Force apply rule eager aggregate. | UInt64 |
| force_join_data_spill | 0 | 0 | DEFAULT | For testing only. Join data will be forcibly spilled to external storage if enabled. | UInt64 |
| force_materialized_cte_spill | 0 | 0 | DEFAULT | For testing only. Materialized CTE data will be forcibly spilled to external storage if enabled. | UInt64 |
| force_sort_data_spill | 0 | 0 | DEFAULT | For testing only. Sort data will be forcibly spilled to external storage if enabled. | UInt64 |
| force_window_data_spill | 0 | 0 | DEFAULT | For testing only. Window data will be forcibly spilled to external storage if enabled. | UInt64 |
| format_null_as_str | 0 | 0 | DEFAULT | Format NULL as str in query api response. | UInt64 |
| geometry_output_format | GeoJSON | GeoJSON | DEFAULT | Display format for GEOMETRY values. Values: "WKT", "WKB", "EWKT", "EWKB", "GeoJSON". | String |
| group_by_shuffle_mode | before_merge | before_merge | DEFAULT | Group by shuffle mode. 'before_partial' is more balanced, but more data needs to exchange. | String |
| grouping_sets_channel_size | 2 | 2 | DEFAULT | Sets the channel size for grouping sets to union transformation. | UInt64 |
| grouping_sets_to_union | 0 | 0 | DEFAULT | Enables grouping sets to union. | UInt64 |
| hash_shuffle_bytes_threshold | 4194304 | 4194304 | DEFAULT | Sets the max bytes threshold for hash shuffle block partition stream. | UInt64 |
| hash_shuffle_rows_threshold | 8192 | 8192 | DEFAULT | Sets the max rows threshold for hash shuffle block partition stream. | UInt64 |
| hide_options_in_show_create_table | 1 | 1 | DEFAULT | Hides table-relevant information such as SNAPSHOT_LOCATION and STORAGE_FORMAT at the end of SHOW TABLE CREATE. | UInt64 |
| hilbert_clustering_min_bytes | 107374182400 | 107374182400 | DEFAULT | Sets the minimum byte size of blocks for Hilbert Clustering. | UInt64 |
| hilbert_num_range_ids | 1000 | 1000 | DEFAULT | Specifies the domain of range IDs in Hilbert clustering. A larger value provides finer granularity but may incur a performance cost. | UInt64 |
| hilbert_sample_size_per_block | 1000 | 1000 | DEFAULT | Specifies the number of sample points per block used in Hilbert clustering. | UInt64 |
| hive_parquet_chunk_size | 16384 | 16384 | DEFAULT | The max number of rows each read from parquet to {{{ .lake }}} processor. | UInt64 |
| http_handler_result_timeout_secs | 240 | 240 | DEFAULT | Set the timeout in seconds that a http query session expires without any polls. | UInt64 |
| http_json_result_mode | display | display | DEFAULT | Controls how HTTP query JSON data is encoded. Values: "display", "driver". | String |
| idle_transaction_timeout_secs | 14400 | 14400 | DEFAULT | Set the timeout in seconds for active session without any query. | UInt64 |
| inlist_runtime_bloom_prune_threshold | 64 | 64 | DEFAULT | Sets the maximum number of values in an IN list for runtime block bloom pruning. | UInt64 |
| inlist_runtime_filter_threshold | 1024 | 1024 | DEFAULT | Sets the maximum number of values in an IN list for runtime filter generation. | UInt64 |
| inlist_to_join_threshold | 1024 | 1024 | DEFAULT | Set the threshold for converting IN list to JOIN. | UInt64 |
| input_read_buffer_size | 4194304 | 4194304 | DEFAULT | Sets the memory size in bytes allocated to the buffer used by the buffered reader to read data from storage. | UInt64 |
| join_runtime_filter_selectivity_threshold | 10 | 10 | DEFAULT | Selectivity threshold (percentage) for bloom join runtime filters. Default 10 means 10%. | UInt64 |
| join_spilling_buffer_threshold_per_proc_mb | 512 | 512 | DEFAULT | Set the spilling buffer threshold (MB) for each join processor. | UInt64 |
| join_spilling_memory_ratio | 60 | 60 | LOCAL | Sets the maximum memory ratio in bytes that hash join can use before spilling data to storage. 0 is unlimited. | UInt64 |
| join_spilling_partition_bits | 4 | 4 | DEFAULT | Set the number of partitions for join spilling. Default value is 4, meaning 2^4 partitions. | UInt64 |
| lazy_read_across_join_threshold | 10 | 10 | DEFAULT | Sets the maximum LIMIT in a query to enable lazy read across joins. Setting it to 0 disables the optimization. | UInt64 |
| lazy_read_threshold | 1000 | 1000 | DEFAULT | Sets the maximum LIMIT in a query to enable lazy read optimization. Setting it to 0 disables the optimization. | UInt64 |
| load_file_metadata_expire_hours | 24 | 24 | DEFAULT | Sets the hours that the metadata of files loaded with COPY INTO will expire in. | UInt64 |
| materialized_cte_spilling_memory_ratio | 60 | 60 | DEFAULT | Sets the maximum memory ratio in bytes that materialized CTE execution can use before spilling data to storage. 0 is unlimited. | UInt64 |
| max_aggregate_restore_worker | 16 | 16 | DEFAULT | Sets the maximum number of workers for aggregate restore. | UInt64 |
| max_aggregate_spill_level | 3 | 3 | DEFAULT | Maximum recursion depth for the aggregate spill. Each level repartitions data into 4 smaller parts. | UInt64 |
| max_block_bytes | 52428800 | 52428800 | DEFAULT | Sets the maximum byte size of a single data block that can be read. | UInt64 |
| max_block_size | 65536 | 65536 | DEFAULT | Sets the maximum rows size of a single data block that can be read. | UInt64 |
| max_cte_recursive_depth | 1000 | 1000 | DEFAULT | Max recursive depth for recursive CTE. | UInt64 |
| max_execute_time_in_seconds | 0 | 0 | DEFAULT | Sets the maximum query execution time in seconds. Setting it to 0 means no limit. | UInt64 |
| max_hash_join_spill_level | 1 | 1 | DEFAULT | Maximum recursion depth for the hash join spill. Each level repartitions data into 16 smaller parts. | UInt64 |
| max_inlist_to_or | 3 | 3 | DEFAULT | Sets the maximum number of values that can be included in an IN expression to be converted to an OR operator. | UInt64 |
| max_memory_usage | 51539607552 | 51539607552 | DEFAULT | Sets the maximum memory usage in bytes for processing a single query. | UInt64 |
| max_public_keys_per_user | 10 | 10 | DEFAULT | Maximum number of public keys allowed per user for key-pair authentication. | UInt64 |
| max_push_down_limit | 10000 | 10000 | DEFAULT | Sets the maximum number of rows limit that can be pushed down to the leaf operator. | UInt64 |
| max_query_memory_usage | 25769803776 | 25769803776 | LOCAL | The maximum memory usage for query. If set to 0, memory usage is unlimited. | UInt64 |
| max_result_rows | 0 | 0 | DEFAULT | Sets the maximum number of rows that can be returned in a query result. Setting it to 0 means no limit. | UInt64 |
| max_set_operator_count | 18446744073709551615 | 18446744073709551615 | DEFAULT | The maximum count of set operators in a query. | UInt64 |
| max_spill_io_requests | 8 | 8 | DEFAULT | Sets the maximum number of concurrent spill I/O requests. | UInt64 |
| max_storage_io_requests | 64 | 64 | DEFAULT | Sets the maximum number of concurrent storage I/O requests. | UInt64 |
| max_threads | 8 | 8 | DEFAULT | Sets the maximum number of threads to execute a request. | UInt64 |
| max_vacuum_temp_files_after_query | 18446744073709551615 | 18446744073709551615 | DEFAULT | The maximum temp files will be removed after query. Disable if 0. | UInt64 |
| max_vacuum_threads | 1 | 1 | DEFAULT | Sets the maximum number of threads to execute vacuum operation. | UInt64 |
| min_max_runtime_filter_threshold | 18446744073709551615 | 18446744073709551615 | DEFAULT | Sets the maximum number of rows for min-max runtime filter generation. | UInt64 |
| nested_loop_join_threshold | 10000 | 10000 | DEFAULT | Set the threshold for use nested loop join. Setting it to 0 disables nested loop join. | UInt64 |
| network_policy |  |  | DEFAULT | Network policy for all users in the tenant. | String |
| numeric_cast_option | rounding | rounding | DEFAULT | Set numeric cast mode as "rounding" or "truncating". | String |
| optimizer_skip_list |  |  | DEFAULT | Comma-separated list of optimizer names to skip during query optimization. | String |
| parquet_fast_read_bytes | 1048576 | 1048576 | LOCAL | Parquet file with smaller size will be read as a whole file instead of column by column. Default value: 1MB. | UInt64 |
| parquet_max_block_size | 8192 | 8192 | DEFAULT | Max block size for parquet reader. | UInt64 |
| parquet_rowgroup_hint_bytes | 134217728 | 134217728 | DEFAULT | Hint bytes for dividing large parquet files into multiple rowgroups for reading. Default value: 128MB. | UInt64 |
| parse_datetime_ignore_remainder | 1 | 1 | GLOBAL | Ignore trailing chars when parse string to datetime. | UInt64 |
| persist_materialized_cte | 1 | 1 | DEFAULT | Decides if materialized CTEs should be persisted to disk. | UInt64 |
| prefer_broadcast_join | 1 | 1 | DEFAULT | Enables broadcast join. | UInt64 |
| prewhere_selectivity_threshold | 100 | 100 | DEFAULT | Maximum selectivity percentage for pushing row selection into remain-column reads during prewhere. | UInt64 |
| proxy_routing_model | statistics | statistics | DEFAULT | Controls how PROXY chooses a target table. Values: 'statistics', 'prefix'. | String |
| purge_duplicated_files_in_copy | 0 | 0 | DEFAULT | Purge duplicated files detected during execution of copy into table. | UInt64 |
| queries_queue_retry_timeout | 300 | 300 | DEFAULT | The retry interval for query queue timeout. 0 if never retry. | UInt64 |
| query_flight_compression | LZ4 | LZ4 | DEFAULT | Flight compression method. Values: "None", "LZ4", "ZSTD". | String |
| query_out_of_memory_behavior | spilling | spilling | LOCAL | If the query memory limit is exceeded, the system will enforce predefined actions. Values: "throw", "spilling". | String |
| query_result_cache_allow_inconsistent | 0 | 0 | DEFAULT | Determines whether {{{ .lake }}} will return cached query results that are inconsistent with the underlying data. | UInt64 |
| query_result_cache_max_bytes | 1048576 | 1048576 | DEFAULT | Sets the maximum byte size of cache for a single query result. | UInt64 |
| query_result_cache_min_execute_secs | 1 | 1 | DEFAULT | For a query to be cached, it must take at least this many seconds to fetch the first block. | UInt64 |
| query_result_cache_ttl_secs | 300 | 300 | DEFAULT | Sets the time-to-live (TTL) in seconds for cached query results. | UInt64 |
| query_tag |  |  | DEFAULT | Sets the query tag for this session. | String |
| quoted_ident_case_sensitive | 1 | 1 | GLOBAL | Set to 1 for case-sensitive treatment of quoted names, or 0 for case-insensitive. | UInt64 |
| random_function_seed | 0 | 0 | DEFAULT | Seed for random function. | UInt64 |
| recluster_block_size | 9277129359 | 9277129359 | DEFAULT | Sets the maximum byte size of blocks for recluster. | UInt64 |
| recluster_timeout_secs | 43200 | 43200 | DEFAULT | Sets the seconds that recluster final will be timeout. | UInt64 |
| replace_into_bloom_pruning_max_column_number | 4 | 4 | DEFAULT | Max number of columns used by bloom pruning for replace-into statement. | UInt64 |
| replace_into_shuffle_strategy | 0 | 0 | DEFAULT | Choose shuffle strategy: 0 for Block, 1 for Segment level. | UInt64 |
| s3_storage_class | STANDARD | STANDARD | DEFAULT | Default S3 storage class. Values: "STANDARD", "INTELLIGENT_TIERING". | String |
| sandbox_tenant |  |  | DEFAULT | Injects a custom 'sandbox_tenant' into this session. For testing purposes only. | String |
| script_max_steps | 10000 | 10000 | DEFAULT | The maximum steps allowed in a single execution of script. | UInt64 |
| short_sql_max_length | 2048 | 2048 | DEFAULT | Sets the maximum length for truncating SQL queries in short_sql function. | UInt64 |
| sort_spilling_batch_bytes | 20971520 | 20971520 | DEFAULT | Sets the uncompressed size that merge sorter will spill to storage. | UInt64 |
| sort_spilling_memory_ratio | 60 | 60 | LOCAL | Sets the maximum memory ratio in bytes that a sorter can use before spilling data to storage during query execution. | UInt64 |
| spatial_runtime_filter_threshold | 1024 | 1024 | DEFAULT | Sets the maximum number of values in a spatial list for runtime filter generation. | UInt64 |
| spill_writer_memory_pool_size_mb | 20 | 20 | DEFAULT | Set the memory pool size (MB) for each spill writer. | UInt64 |
| spilling_file_format | parquet | parquet | DEFAULT | Set the storage file format for spilling. Values: "arrow", "parquet". | String |
| spilling_to_disk_vacuum_unknown_temp_dirs_limit | 18446744073709551615 | 18446744073709551615 | DEFAULT | Set the maximum number of directories to clean up for unexpected interrupted queries. | UInt64 |
| sql_dialect | PostgreSQL | PostgreSQL | DEFAULT | Sets the SQL dialect. Available values: "PostgreSQL", "MySQL", "Experimental", "Hive", "Prql". | String |
| statement_queue_ttl_in_seconds | 15 | 15 | DEFAULT | Interval in seconds between lease renewal operations with the meta service. | UInt64 |
| statement_queued_timeout_in_seconds | 0 | 0 | DEFAULT | The maximum waiting seconds in the queue. The default value is 0 (no limit). | UInt64 |
| storage_fetch_part_num | 2 | 2 | DEFAULT | Sets the number of partitions that are fetched in parallel from storage during query execution. | UInt64 |
| storage_io_max_page_bytes_for_read | 524288 | 524288 | DEFAULT | Sets the maximum byte size of data pages that can be read from storage in a single I/O operation. | UInt64 |
| storage_io_min_bytes_for_seek | 48 | 48 | DEFAULT | Sets the minimum byte size of data that must be read from storage in a single I/O operation when seeking a new location. | UInt64 |
| storage_read_buffer_size | 1048576 | 1048576 | DEFAULT | Sets the byte size of the buffer used for reading data into memory. | UInt64 |
| stream_consume_batch_size_hint | 0 | 0 | DEFAULT | Hint for batch size during stream consumption. Set it to 0 to disable it. | UInt64 |
| system_tables_count_db_concurrency | 16 | 16 | DEFAULT | Sets the DB-level concurrency used by system.tables count optimization. | UInt64 |
| table_lock_expire_secs | 30 | 30 | DEFAULT | Sets the seconds that the table lock will expire in. | UInt64 |
| timezone | UTC | UTC | DEFAULT | Sets the timezone. | String |
| trace_sample_rate | 1 | 1 | DEFAULT | Setting the trace sample rate. The value should be between '0' and '100'. | UInt64 |
| udf_cloud_import_presign_expire_secs | 259200 | 259200 | DEFAULT | Presign expiry for cloud UDF stage imports. | UInt64 |
| unquoted_ident_case_sensitive | 0 | 0 | DEFAULT | Set to 1 to make unquoted names case-sensitive, or 0 for case-insensitive. | UInt64 |
| use_legacy_query_executor | 0 | 0 | DEFAULT | Fallback to legacy query executor. | UInt64 |
| use_parquet2 | 0 | 0 | DEFAULT | This setting is deprecated. | UInt64 |
| warehouse |  |  | DEFAULT | Please use the `USE WAREHOUSE` statement to set the warehouse. | String |
| week_start | 1 | 1 | DEFAULT | Specifies the first day of the week (used by week-related date functions). | UInt64 |
| window_num_partitions | 256 | 256 | DEFAULT | Sets the number of partitions for window operator. | UInt64 |
| window_partition_sort_block_size | 65536 | 65536 | DEFAULT | Sets the block size of data blocks to be sorted in window partition. | UInt64 |
| window_partition_spilling_memory_ratio | 60 | 60 | GLOBAL | Sets the maximum memory ratio in bytes that a window partitioner can use before spilling data to storage. | UInt64 |
| window_spill_unit_size_mb | 256 | 256 | DEFAULT | Sets the spill unit size (MB) for window operator. | UInt64 |
