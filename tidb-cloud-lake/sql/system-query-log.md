---
title: system.query_log
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.696"/>

A read-only in-memory table stores all the query logs. For the specific fields available in the query logs, refer to the [Examples](#examples) section.

## Setting a Session Tag

You can optionally assign a tag to your session, making it easier to filter logs in the log table based on the assigned session tag. For example, the following assigns the tag `eric` to the current session:

```sql
set session query_tag='eric';
```

We can then run a query and retrieve the log from the log table using the assigned tag:

```sql
show users;

select query_tag, query_text from system.query_log where query_tag='eric' limit 1;
```

In the returned result, you can find the record for the query, tagged as 'eric':

```sql
-[ RECORD 1 ]-----------------------------------
               query_tag: eric
              query_text: SHOW USERS
```

## Examples

The `system.query_log` table stores detailed logs of executed queries. Here's an example of what the log entry looks like:

```sql
SELECT * FROM system.query_log;
```

```sql
...
-[ RECORD 10 ]-----------------------------------
                log_type: 2
           log_type_name: Finish
            handler_type: HTTPQuery
               tenant_id: default
              cluster_id: default
                 node_id: bwElPLZxWt0F8LOFAqsIL2
                sql_user: root
          sql_user_quota: UserQuota<cpu:0,mem:0,store:0>
     sql_user_privileges: ROLES: ["account_admin"]
                query_id: 1957f343-564e-471f-b036-a10ff853357e
              query_kind: Other
              query_text: SHOW USERS
              query_hash: 63c65a28ae257d780e93a8a627190775
query_parameterized_hash: 63c65a28ae257d780e93a8a627190775
              event_date: 2025-04-27
              event_time: 2025-04-27 16:59:31.681036
        query_start_time: 2025-04-27 16:59:31.671825
       query_duration_ms: 9
query_queued_duration_ms: 0
        current_database: default
               databases:
                  tables:
                 columns:
             projections:
            written_rows: 0
           written_bytes: 0
       join_spilled_rows: 0
      join_spilled_bytes: 0
        agg_spilled_rows: 0
       agg_spilled_bytes: 0
   group_by_spilled_rows: 0
  group_by_spilled_bytes: 0
        written_io_bytes: 0
written_io_bytes_cost_ms: 0
               scan_rows: 1
              scan_bytes: 164
           scan_io_bytes: 0
   scan_io_bytes_cost_ms: 0
         scan_partitions: 0
        total_partitions: 0
             result_rows: 1
            result_bytes: 146
               cpu_usage: 8
            memory_usage: 0
  bytes_from_remote_disk: 0
   bytes_from_local_disk: 0
       bytes_from_memory: 0
             client_info:
          client_address: 192.168.65.1
              user_agent: bendsql/0.24.1-f1f7de0
          exception_code: 0
          exception_text:
             stack_trace:
          server_version: v1.2.731-nightly-eb671da5e5(rust-1.88.0-nightly-2025-04-27T06:06:12.942159732Z)
               query_tag: eric
        session_settings: acquire_lock_timeout=30, aggregate_spilling_memory_ratio=60, auto_compaction_imperfect_blocks_threshold=25, auto_compaction_segments_limit=3, collation=utf8, compact_max_block_selection=10000, copy_dedup_full_path_by_default=0, cost_factor_aggregate_per_row=5, cost_factor_hash_table_per_row=10, cost_factor_network_per_row=50, create_query_flight_client_with_current_rt=1, data_retention_time_in_days=1, ddl_column_type_nullable=1, default_order_by_null=nulls_last, disable_join_reorder=0, disable_variant_check=0, dynamic_sample_time_budget_ms=0, efficiently_memory_group_by=0, enable_aggregating_index_scan=1, enable_analyze_histogram=0, enable_auto_fix_missing_bloom_index=0, enable_auto_vacuum=0, enable_block_stream_write=0, enable_bloom_runtime_filter=1, enable_cbo=1, enable_clickhouse_handler=0, enable_compact_after_multi_table_insert=0, enable_compact_after_write=1, enable_dio=1, enable_distributed_compact=0, enable_distributed_copy_into=1, enable_distributed_merge_into=1, enable_distributed_pruning=1, enable_distributed_recluster=0, enable_distributed_replace_into=0, enable_dphyp=1, enable_dst_hour_fix=0, enable_expand_roles=1, enable_experimental_aggregate_hashtable=1, enable_experimental_merge_into=1, enable_experimental_procedure=0, enable_experimental_queries_executor=0, enable_geo_create_table=0, enable_hive_parquet_predict_pushdown=1, enable_last_snapshot_location_hint=1, enable_loser_tree_merge_sort=1, enable_materialized_cte=1, enable_merge_into_row_fetch=1, enable_new_copy_for_text_formats=1, enable_optimizer_trace=0, enable_parallel_multi_merge_sort=1, enable_parquet_page_index=1, enable_parquet_prewhere=0, enable_parquet_rowgroup_pruning=1, enable_planner_cache=1, enable_prune_cache=1, enable_prune_pipeline=1, enable_query_result_cache=0, enable_refresh_aggregating_index_after_write=1, enable_replace_into_partitioning=1, enable_strict_datetime_parser=1, enable_table_lock=1, enforce_broadcast_join=0, enforce_shuffle_join=0, error_on_nondeterministic_update=1, external_server_connect_timeout_secs=10, external_server_request_batch_rows=65536, external_server_request_max_threads=256, external_server_request_retry_times=8, external_server_request_timeout_secs=180, flight_client_timeout=60, flight_connection_max_retry_times=0, flight_connection_retry_interval=1, force_aggregate_data_spill=0, force_join_data_spill=0, force_sort_data_spill=0, force_window_data_spill=0, format_null_as_str=1, geometry_output_format=GeoJSON, group_by_shuffle_mode=before_merge, group_by_two_level_threshold=20000, hide_options_in_show_create_table=1, hilbert_clustering_min_bytes=107374182400, hilbert_num_range_ids=1000, hilbert_sample_size_per_block=1000, hive_parquet_chunk_size=16384, http_handler_result_timeout_secs=60, idle_transaction_timeout_secs=14400, inlist_to_join_threshold=1024, input_read_buffer_size=4194304, join_spilling_buffer_threshold_per_proc_mb=512, join_spilling_memory_ratio=60, join_spilling_partition_bits=4, lazy_read_threshold=1000, load_file_metadata_expire_hours=24, max_block_size=65536, max_cte_recursive_depth=1000, max_execute_time_in_seconds=0, max_inlist_to_or=3, max_memory_usage=6574653440, max_push_down_limit=10000, max_query_memory_usage=0, max_result_rows=0, max_set_operator_count=18446744073709551615, max_spill_io_requests=48, max_storage_io_requests=48, max_threads=8, max_vacuum_temp_files_after_query=18446744073709551615, network_policy=, numeric_cast_option=rounding, optimizer_skip_list=, parquet_fast_read_bytes=16777216, parquet_max_block_size=8192, parse_datetime_ignore_remainder=1, persist_materialized_cte=0, prefer_broadcast_join=1, purge_duplicated_files_in_copy=0, query_flight_compression=LZ4, query_out_of_memory_behavior=throw, query_result_cache_allow_inconsistent=0, query_result_cache_max_bytes=1048576, query_result_cache_min_execute_secs=1, query_result_cache_ttl_secs=300, query_tag=eric, quoted_ident_case_sensitive=1, random_function_seed=0, recluster_block_size=1972396032, recluster_timeout_secs=43200, replace_into_bloom_pruning_max_column_number=4, replace_into_shuffle_strategy=0, sandbox_tenant=, script_max_steps=10000, short_sql_max_length=128, sort_spilling_batch_bytes=8388608, sort_spilling_memory_ratio=60, spilling_file_format=parquet, spilling_to_disk_vacuum_unknown_temp_dirs_limit=18446744073709551615, sql_dialect=PostgreSQL, statement_queue_ttl_in_seconds=15, statement_queued_timeout_in_seconds=0, storage_fetch_part_num=2, storage_io_max_page_bytes_for_read=524288, storage_io_min_bytes_for_seek=48, storage_read_buffer_size=1048576, stream_consume_batch_size_hint=0, table_lock_expire_secs=30, timezone=UTC, unquoted_ident_case_sensitive=0, use_parquet2=0, use_vacuum2_to_purge_transient_table_data=0, warehouse=, window_num_partitions=256, window_partition_sort_block_size=65536, window_partition_spilling_memory_ratio=60, window_partition_spilling_to_disk_bytes_limit=0, window_spill_unit_size_mb=256, scope: SESSION
                   extra:
             has_profile: true
       peek_memory_usage: {"bwElPLZxWt0F8LOFAqsIL2":576850}
```
