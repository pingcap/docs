---
title: system.settings
summary: 存储当前会话的系统设置。
---

# system.settings

存储当前会话的系统设置。

```sql
SELECT * FROM system.settings;
```

| 名称 | 值 | 默认值 | 级别 | 描述 | 类型 |
|------|-------|---------|-------|-------------|------|
| acquire_lock_timeout | 30 | 30 | DEFAULT | 设置获取锁的最大超时时间（秒）。 | UInt64 |
| aggregate_spilling_memory_ratio | 60 | 60 | LOCAL | 设置聚合器在查询执行期间将数据溢写到存储之前可使用的最大内存比例（按字节计）。 | UInt64 |
| allow_query_exceeded_limit | 0 | 0 | DEFAULT | 允许查询超出已配置的内存限制，并将错误通知延迟到发生内存争用时。 | UInt64 |
| auto_compaction_imperfect_blocks_threshold | 25 | 25 | GLOBAL | 写入后触发自动 compact 的阈值。设置为 0 可禁用自动 compact。 | UInt64 |
| auto_compaction_segments_limit | 3 | 3 | DEFAULT | 写入后自动触发 recluster 时允许处理的最大 segment 数量。 | UInt64 |
| binary_input_format | utf-8 | utf-8 | DEFAULT | 控制插入到 BINARY 列时如何解释字符串字面量（HEX、BASE64、UTF-8 或 UTF-8-LOSSY）。 | String |
| binary_output_format | hex | hex | DEFAULT | 控制 BINARY 列的输出格式（HEX、BASE64、UTF-8 或 UTF-8-LOSSY）。 | String |
| bloom_runtime_filter_threshold | 3000000 | 3000000 | DEFAULT | 设置生成 bloom 运行时过滤器的最大行数。 | UInt64 |
| collation | utf8 | utf8 | DEFAULT | 设置字符排序规则。可用值包括 `"utf8"`。 | String |
| compact_max_block_selection | 1000 | 1000 | DEFAULT | 限制 compact 操作期间可选择的不完整数据块的最大数量。 | UInt64 |
| copy_dedup_full_path_by_default | 0 | 0 | DEFAULT | 创建表时，如果未设置表选项 copy_dedup_full_path，则使用该默认值。 | UInt64 |
| cost_factor_aggregate_per_row | 5 | 5 | DEFAULT | 单行数据执行分组操作的成本因子。 | UInt64 |
| cost_factor_hash_table_per_row | 10 | 10 | DEFAULT | 单行数据构建哈希表的成本因子。 | UInt64 |
| cost_factor_network_per_row | 50 | 50 | DEFAULT | 单行数据通过网络传输的成本因子。 | UInt64 |
| create_query_flight_client_with_current_rt | 1 | 1 | DEFAULT | 打开 (1) 或关闭 (0) 在查询操作中使用当前运行时。 | UInt64 |
| data_retention_num_snapshots_to_keep | 0 | 0 | DEFAULT | 指定在 vacuum 操作期间要保留的快照数量。会覆盖 data_retention_time_in_days。若设置为 0，则忽略此设置。 | UInt64 |
| data_retention_time_in_days | 1 | 1 | DEFAULT | 设置数据保留时间（天）。 | UInt64 |
| date_format_style | Oracle | Oracle | DEFAULT | 设置日期格式风格（由 datetime 函数使用）。可用值：`"MySQL"`、`"Oracle"`。 | String |
| ddl_column_type_nullable | 1 | 1 | DEFAULT | 设置表操作中新列默认是否可为 NULL：1 表示可为空，0 表示不可为空。 | UInt64 |
| default_order_by_null | nulls_last | nulls_last | DEFAULT | 设置数值型 default_order_by_null 模式。可选值：`"nulls_first"`、`"nulls_last"`、`"nulls_first_on_asc_last_on_desc"`。 | String |
| disable_join_reorder | 0 | 0 | DEFAULT | 禁用 join 重排序优化。 | UInt64 |
| disable_variant_check | 0 | 0 | DEFAULT | 禁用 variant 检查，以允许插入无效的 JSON 值。 | UInt64 |
| dynamic_sample_time_budget_ms | 0 | 0 | DEFAULT | 动态采样的时间预算（毫秒）。 | UInt64 |
| enable_aggregating_index_scan | 1 | 1 | DEFAULT | 启用查询时扫描 aggregating index 数据。 | UInt64 |
| enable_analyze_histogram | 0 | 0 | DEFAULT | 在分析表时启用直方图分析，以进行查询优化。 | UInt64 |
| enable_auto_analyze | 1 | 1 | DEFAULT | 启用写入后的自动分析。0 表示禁用，1 表示启用。 | UInt64 |
| enable_auto_detect_datetime_format | 0 | 0 | DEFAULT | 启用对非 ISO datetime 格式的自动检测。适用于函数、COPY 和 VARIANT cast。 | UInt64 |
| enable_auto_fix_missing_bloom_index | 0 | 0 | DEFAULT | 启用自动修复缺失的 bloom index。 | UInt64 |
| enable_auto_materialize_cte | 1 | 1 | DEFAULT | 启用自动物化 CTE。0 表示禁用，1 表示启用。 | UInt64 |
| enable_auto_vacuum | 0 | 0 | DEFAULT | 是否自动对表触发 VACUUM 操作。 | UInt64 |
| enable_backpressure_spiller | 0 | 0 | DEFAULT | 使用新的背压 spiller。 | UInt64 |
| enable_block_stream_write | 1 | 1 | GLOBAL | 启用 block stream write。 | UInt64 |
| enable_bloom_runtime_filter | 1 | 1 | DEFAULT | 启用 JOIN 的 bloom 运行时过滤器优化。 | UInt64 |
| enable_cbo | 1 | 1 | DEFAULT | 启用基于成本的优化。 | UInt64 |
| enable_compact_after_multi_table_insert | 0 | 0 | DEFAULT | 启用多表插入后的 recluster 和 compact。 | UInt64 |
| enable_compact_after_write | 1 | 1 | DEFAULT | 启用写入后（copy/insert/replace-into/merge-into）执行 compact，需要更多内存。 | UInt64 |
| enable_cse_optimizer | 0 | 0 | DEFAULT | 启用公共子表达式消除优化。 | UInt64 |
| enable_decimal_sum_widening | 0 | 0 | DEFAULT | 自动将 SUM 参数从 Decimal(19..38, scale) 扩展为 Decimal(76, scale)。 | UInt64 |
| enable_dio | 1 | 1 | DEFAULT | 启用 Direct IO。 | UInt64 |
| enable_distributed_compact | 0 | 0 | DEFAULT | 启用表 compact 的分布式执行。 | UInt64 |
| enable_distributed_copy_into | 1 | 1 | DEFAULT | 启用 `COPY INTO` 的分布式执行。 | UInt64 |
| enable_distributed_merge_into | 1 | 1 | DEFAULT | 启用 `MERGE INTO` 的分布式执行。 | UInt64 |
| enable_distributed_pruning | 1 | 1 | DEFAULT | 启用分布式索引裁剪。 | UInt64 |
| enable_distributed_recluster | 1 | 1 | GLOBAL | 启用表 recluster 的分布式执行。 | UInt64 |
| enable_distributed_replace_into | 0 | 0 | DEFAULT | 启用 `REPLACE INTO` 的分布式执行。 | UInt64 |
| enable_dphyp | 1 | 1 | DEFAULT | 启用 dphyp join 顺序算法。 | UInt64 |
| enable_dst_hour_fix | 0 | 0 | DEFAULT | 时间转换在遇到无效 DST 时通过增加一小时进行处理。准确性不保证（默认禁用）。 | UInt64 |
| enable_expand_roles | 1 | 1 | DEFAULT | 在执行 show grants 语句时启用角色展开（默认启用）。 | UInt64 |
| enable_experiment_aggregate | 1 | 1 | DEFAULT | 启用实验性 aggregate（默认启用）。 | UInt64 |
| enable_experiment_hash_index | 1 | 1 | DEFAULT | 实验设置：启用 hash index（默认启用）。 | UInt64 |
| enable_experimental_connection_privilege_check | 0 | 0 | DEFAULT | 实验设置：启用 connection 对象权限检查（默认禁用）。 | UInt64 |
| enable_experimental_new_join | 1 | 1 | DEFAULT | 启用实验特性的新 join 实现。 | UInt64 |
| enable_experimental_procedure | 1 | 1 | GLOBAL | 启用 `PROCEDURE` 的实验特性。 | UInt64 |
| enable_experimental_rbac_check | 1 | 1 | DEFAULT | 实验设置：启用 stage 和 udf 权限检查（默认启用）。 | UInt64 |
| enable_experimental_row_access_policy | 0 | 0 | DEFAULT | 实验设置：启用行访问策略（默认禁用）。 | UInt64 |
| enable_experimental_sequence_privilege_check | 0 | 0 | DEFAULT | 实验设置：启用 sequence 对象权限检查（默认禁用）。 | UInt64 |
| enable_experimental_table_ref | 0 | 0 | DEFAULT | 实验设置：启用 table ref（默认禁用）。 | UInt64 |
| enable_experimental_virtual_column | 0 | 0 | DEFAULT | 启用实验性的虚拟列。 | UInt64 |
| enable_fixed_rows_sort | 1 | 1 | DEFAULT | 启用 fixed rows sort serialize。 | UInt64 |
| enable_geo_create_table | 1 | 1 | DEFAULT | 允许创建和修改包含 geometry/geography 类型的表。 | UInt64 |
| enable_group_by_column_first | 0 | 0 | DEFAULT | 在 SELECT 别名之前，优先将 GROUP BY 名称解析为输入列。为兼容性考虑，默认禁用。 | UInt64 |
| enable_hive_parquet_predict_pushdown | 1 | 1 | DEFAULT | 将此变量设置为 1 以启用 hive parquet predict pushdown。默认值：1。 | UInt64 |
| enable_join_runtime_filter | 1 | 1 | DEFAULT | 启用 JOIN 的运行时过滤器优化。 | UInt64 |
| enable_last_snapshot_location_hint | 1 | 1 | DEFAULT | 启用写入 last_snapshot_location_hint 对象。 | UInt64 |
| enable_loser_tree_merge_sort | 1 | 1 | DEFAULT | 启用 loser tree merge sort。 | UInt64 |
| enable_materialized_cte | 1 | 1 | DEFAULT | 启用物化公共表表达式。 | UInt64 |
| enable_merge_into_row_fetch | 1 | 1 | DEFAULT | 启用 merge into row fetch 优化。 | UInt64 |
| enable_mutation_block_id_repartition | 1 | 1 | DEFAULT | 在基于 join 的变异操作中，在 row fetch 之前启用本地 block_id 重新分区，以减少重复的数据块读取。 | UInt64 |
| enable_new_copy_for_text_formats | 1 | 1 | DEFAULT | 使用新的实现加载 CSV 文件。 | UInt64 |
| enable_optimizer_trace | 0 | 0 | DEFAULT | 启用优化器跟踪。 | UInt64 |
| enable_parallel_multi_merge_sort | 1 | 1 | DEFAULT | 启用并行 multi merge sort。 | UInt64 |
| enable_parallel_union_all | 0 | 0 | DEFAULT | 启用并行 UNION ALL。默认值为 0，1 表示启用。 | UInt64 |
| enable_parquet_page_index | 1 | 1 | DEFAULT | 启用 parquet page index。 | UInt64 |
| enable_parquet_prewhere | 0 | 0 | DEFAULT | 启用 parquet prewhere。 | UInt64 |
| enable_parquet_rowgroup_pruning | 1 | 1 | DEFAULT | 启用 parquet rowgroup pruning。 | UInt64 |
| enable_planner_cache | 1 | 1 | DEFAULT | 启用对相同查询的逻辑计划缓存。 | UInt64 |
| enable_proxy_bloom_pruning | 0 | 0 | DEFAULT | 在 PROXY 轻量级路由估算期间启用 bloom index pruning。默认禁用，以保持路由开销较低。 | UInt64 |
| enable_prune_cache | 1 | 1 | DEFAULT | 启用缓存裁剪结果。 | UInt64 |
| enable_prune_pipeline | 1 | 1 | DEFAULT | 启用 pruning pipeline。 | UInt64 |
| enable_query_result_cache | 0 | 0 | DEFAULT | 启用查询结果缓存，以提升相同查询的性能。 | UInt64 |
| enable_refresh_aggregating_index_after_write | 1 | 1 | DEFAULT | 在写入新数据后刷新 aggregating index。 | UInt64 |
| enable_replace_into_partitioning | 1 | 1 | DEFAULT | 为 replace-into 语句启用分区（如果表具有 cluster key）。 | UInt64 |
| enable_result_set_spilling | 0 | 0 | DEFAULT | 当内存使用超过阈值时，启用将结果集数据溢写到存储。 | UInt64 |
| enable_selector_executor | 1 | 1 | DEFAULT | 为过滤表达式启用 selector executor。 | UInt64 |
| enable_shuffle_sort | 0 | 0 | DEFAULT | 启用 shuffle sort。 | UInt64 |
| enable_sort_spill_prefetch | 1 | 1 | DEFAULT | 为溢写的排序数据块启用异步恢复预取。 | UInt64 |
| enable_sort_spill_stream_regroup | 1 | 1 | DEFAULT | 在合并前按域对排序溢写流重新分组。 | UInt64 |
| enable_strict_datetime_parser | 1 | 1 | DEFAULT | 启用后，datetime 函数仅接受 ISO 8601 格式。禁用后，将回退为尽力解析。 | UInt64 |
| enable_table_lock | 1 | 1 | DEFAULT | 在需要时启用表锁（默认启用）。 | UInt64 |
| enable_table_snapshot_stats | 0 | 0 | DEFAULT | 启用对快照的 analyze table 统计信息。 | UInt64 |
| enforce_broadcast_join | 0 | 0 | DEFAULT | 强制使用 broadcast join。 | UInt64 |
| enforce_local | 0 | 0 | DEFAULT | 强制使用本地计划。 | UInt64 |
| enforce_shuffle_join | 0 | 0 | DEFAULT | 强制使用 shuffle join。 | UInt64 |
| error_on_nondeterministic_update | 1 | 1 | DEFAULT | 在修改多重连接后的行时，是否返回错误。 | UInt64 |
| external_server_connect_timeout_secs | 10 | 10 | DEFAULT | 连接外部服务器的超时时间。 | UInt64 |
| external_server_request_batch_rows | 65536 | 65536 | DEFAULT | 向外部服务器请求的批量行数。 | UInt64 |
| external_server_request_max_threads | 256 | 256 | DEFAULT | 向外部服务器请求时使用的最大线程数。 | UInt64 |
| external_server_request_retry_times | 8 | 8 | DEFAULT | 向外部服务器请求的最大重试次数。 | UInt64 |
| external_server_request_timeout_secs | 180 | 180 | DEFAULT | 向外部服务器请求的超时时间。 | UInt64 |
| flight_client_keep_alive_interval_secs | 0 | 0 | DEFAULT | 设置两次 flight TCP keepalive 探测之间的间隔（秒）。0 表示禁用 keepalive。 | UInt64 |
| flight_client_keep_alive_retries | 0 | 0 | DEFAULT | 设置在将对端判定为不可达之前，flight 连接的 TCP keepalive 重试次数。0 表示禁用 keepalive。 | UInt64 |
| flight_client_keep_alive_time_secs | 0 | 0 | DEFAULT | 设置 flight TCP 连接在空闲多久后发送 keepalive 探测（秒）。0 表示禁用 keepalive。 | UInt64 |
| flight_client_timeout | 60 | 60 | DEFAULT | 设置 flight 客户端请求可被处理的最长时间（秒）。 | UInt64 |
| flight_connection_max_retry_times | 0 | 0 | DEFAULT | 集群 flight 的最大重试次数。设置为 0 表示禁用。 | UInt64 |
| flight_connection_retry_interval | 1 | 1 | DEFAULT | 集群 flight 的重试间隔（秒）。 | UInt64 |
| force_aggregate_data_spill | 0 | 0 | DEFAULT | 仅用于测试。启用后，聚合数据将被强制溢写到外部存储。 | UInt64 |
| force_aggregate_shuffle_mode | auto | auto | DEFAULT | 仅用于测试。聚合的 shuffle 模式。可选项：`'auto'`、`'row'`、`'bucket'`。 | String |
| force_eager_aggregate | 0 | 0 | DEFAULT | 强制应用 eager aggregate 规则。 | UInt64 |
| force_join_data_spill | 0 | 0 | DEFAULT | 仅用于测试。启用后，join 数据将被强制溢写到外部存储。 | UInt64 |
| force_materialized_cte_spill | 0 | 0 | DEFAULT | 仅用于测试。启用后，物化 CTE 数据将被强制溢写到外部存储。 | UInt64 |
| force_sort_data_spill | 0 | 0 | DEFAULT | 仅用于测试。启用后，排序数据将被强制溢写到外部存储。 | UInt64 |
| force_window_data_spill | 0 | 0 | DEFAULT | 仅用于测试。启用后，窗口数据将被强制溢写到外部存储。 | UInt64 |
| format_null_as_str | 0 | 0 | DEFAULT | 在 query api 响应中将 NULL 格式化为字符串。 | UInt64 |
| geometry_output_format | GeoJSON | GeoJSON | DEFAULT | GEOMETRY 值的显示格式。可选值：`"WKT"`、`"WKB"`、`"EWKT"`、`"EWKB"`、`"GeoJSON"`。 | String |
| group_by_shuffle_mode | before_merge | before_merge | DEFAULT | GROUP BY 的 shuffle 模式。`'before_partial'` 更均衡，但需要交换更多数据。 | String |
| grouping_sets_channel_size | 2 | 2 | DEFAULT | 设置 grouping sets 到 union 转换的通道大小。 | UInt64 |
| grouping_sets_to_union | 0 | 0 | DEFAULT | 启用 grouping sets 到 union 的转换。 | UInt64 |
| hash_shuffle_bytes_threshold | 4194304 | 4194304 | DEFAULT | 设置 hash shuffle block partition stream 的最大字节阈值。 | UInt64 |
| hash_shuffle_rows_threshold | 8192 | 8192 | DEFAULT | 设置 hash shuffle block partition stream 的最大行数阈值。 | UInt64 |
| hide_options_in_show_create_table | 1 | 1 | DEFAULT | 在 SHOW TABLE CREATE 结果末尾隐藏与表相关的信息，例如 SNAPSHOT_LOCATION 和 STORAGE_FORMAT。 | UInt64 |
| hilbert_clustering_min_bytes | 107374182400 | 107374182400 | DEFAULT | 设置 Hilbert Clustering 的最小数据块字节大小。 | UInt64 |
| hilbert_num_range_ids | 1000 | 1000 | DEFAULT | 指定 Hilbert clustering 中 range ID 的范围。值越大，粒度越细，但可能带来性能开销。 | UInt64 |
| hilbert_sample_size_per_block | 1000 | 1000 | DEFAULT | 指定 Hilbert clustering 中每个数据块使用的采样点数量。 | UInt64 |
| hive_parquet_chunk_size | 16384 | 16384 | DEFAULT | 每次从 parquet 读取到 {{{ .lake }}} 处理器的最大行数。 | UInt64 |
| http_handler_result_timeout_secs | 240 | 240 | DEFAULT | 设置 http 查询会话在没有任何轮询时过期的超时时间（秒）。 | UInt64 |
| http_json_result_mode | display | display | DEFAULT | 控制 HTTP 查询 JSON 数据的编码方式。可选值：`"display"`、`"driver"`。 | String |
| idle_transaction_timeout_secs | 14400 | 14400 | DEFAULT | 设置活动会话在没有任何查询时的超时时间（秒）。 | UInt64 |
| inlist_runtime_bloom_prune_threshold | 64 | 64 | DEFAULT | 设置 IN 列表中用于运行时数据块 bloom pruning 的最大值数量。 | UInt64 |
| inlist_runtime_filter_threshold | 1024 | 1024 | DEFAULT | 设置 IN 列表中用于生成运行时过滤器的最大值数量。 | UInt64 |
| inlist_to_join_threshold | 1024 | 1024 | DEFAULT | 设置将 IN 列表转换为 JOIN 的阈值。 | UInt64 |
| input_read_buffer_size | 4194304 | 4194304 | DEFAULT | 设置缓冲读取器从存储读取数据时所使用缓冲区分配的内存大小（字节）。 | UInt64 |
| join_runtime_filter_selectivity_threshold | 10 | 10 | DEFAULT | bloom join 运行时过滤器的选择率阈值（百分比）。默认值 10 表示 10%。 | UInt64 |
| join_spilling_buffer_threshold_per_proc_mb | 512 | 512 | DEFAULT | 设置每个 join 处理器的溢写缓冲阈值（MB）。 | UInt64 |
| join_spilling_memory_ratio | 60 | 60 | LOCAL | 设置 hash join 在将数据溢写到存储之前可使用的最大内存比例（按字节计）。0 表示无限制。 | UInt64 |
| join_spilling_partition_bits | 4 | 4 | DEFAULT | 设置 join 溢写的分区数。默认值为 4，表示 2^4 个分区。 | UInt64 |
| lazy_read_across_join_threshold | 10 | 10 | DEFAULT | 设置查询中启用跨 join 延迟读取优化的最大 LIMIT。设置为 0 可禁用该优化。 | UInt64 |
| lazy_read_threshold | 1000 | 1000 | DEFAULT | 设置查询中启用延迟读取优化的最大 LIMIT。设置为 0 可禁用该优化。 | UInt64 |
| load_file_metadata_expire_hours | 24 | 24 | DEFAULT | 设置通过 COPY INTO 加载的文件元信息的过期时间（小时）。 | UInt64 |
| materialized_cte_spilling_memory_ratio | 60 | 60 | DEFAULT | 设置物化 CTE 执行在将数据溢写到存储之前可使用的最大内存比例（按字节计）。0 表示无限制。 | UInt64 |
| max_aggregate_restore_worker | 16 | 16 | DEFAULT | 设置 aggregate restore 的最大 worker 数量。 | UInt64 |
| max_aggregate_spill_level | 3 | 3 | DEFAULT | aggregate spill 的最大递归深度。每一层都会将数据重新分区为 4 个更小部分。 | UInt64 |
| max_block_bytes | 52428800 | 52428800 | DEFAULT | 设置可读取的单个数据块的最大字节大小。 | UInt64 |
| max_block_size | 65536 | 65536 | DEFAULT | 设置可读取的单个数据块的最大行数。 | UInt64 |
| max_cte_recursive_depth | 1000 | 1000 | DEFAULT | 递归 CTE 的最大递归深度。 | UInt64 |
| max_execute_time_in_seconds | 0 | 0 | DEFAULT | 设置查询执行的最大时间（秒）。设置为 0 表示无限制。 | UInt64 |
| max_hash_join_spill_level | 1 | 1 | DEFAULT | hash join spill 的最大递归深度。每一层都会将数据重新分区为 16 个更小部分。 | UInt64 |
| max_inlist_to_or | 3 | 3 | DEFAULT | 设置 IN 表达式中可被转换为 OR 运算符的最大值数量。 | UInt64 |
| max_memory_usage | 51539607552 | 51539607552 | DEFAULT | 设置处理单个查询时的最大内存使用量（字节）。 | UInt64 |
| max_public_keys_per_user | 10 | 10 | DEFAULT | 每个用户在密钥对认证中允许的最大公钥数量。 | UInt64 |
| max_push_down_limit | 10000 | 10000 | DEFAULT | 设置可下推到叶子算子的最大行数限制。 | UInt64 |
| max_query_memory_usage | 25769803776 | 25769803776 | LOCAL | 查询的最大内存使用量。若设置为 0，则内存使用无限制。 | UInt64 |
| max_result_rows | 0 | 0 | DEFAULT | 设置查询结果中可返回的最大行数。设置为 0 表示无限制。 | UInt64 |
| max_set_operator_count | 18446744073709551615 | 18446744073709551615 | DEFAULT | 查询中集合运算符的最大数量。 | UInt64 |
| max_spill_io_requests | 8 | 8 | DEFAULT | 设置并发 spill I/O 请求的最大数量。 | UInt64 |
| max_storage_io_requests | 64 | 64 | DEFAULT | 设置并发存储 I/O 请求的最大数量。 | UInt64 |
| max_threads | 8 | 8 | DEFAULT | 设置执行请求的最大线程数。 | UInt64 |
| max_vacuum_temp_files_after_query | 18446744073709551615 | 18446744073709551615 | DEFAULT | 查询后将被删除的临时文件最大数量。设置为 0 表示禁用。 | UInt64 |
| max_vacuum_threads | 1 | 1 | DEFAULT | 设置执行 vacuum 操作的最大线程数。 | UInt64 |
| min_max_runtime_filter_threshold | 18446744073709551615 | 18446744073709551615 | DEFAULT | 设置生成 min-max 运行时过滤器的最大行数。 | UInt64 |
| nested_loop_join_threshold | 10000 | 10000 | DEFAULT | 设置使用嵌套循环连接的阈值。设置为 0 可禁用嵌套循环连接。 | UInt64 |
| network_policy |  |  | DEFAULT | 租户中所有用户的网络策略。 | String |
| numeric_cast_option | rounding | rounding | DEFAULT | 将数值 cast 模式设置为 `"rounding"` 或 `"truncating"`。 | String |
| optimizer_skip_list |  |  | DEFAULT | 在查询优化期间要跳过的优化器名称列表，以逗号分隔。 | String |
| parquet_fast_read_bytes | 1048576 | 1048576 | LOCAL | 较小的 Parquet 文件将作为整个文件读取，而不是按列读取。默认值：1MB。 | UInt64 |
| parquet_max_block_size | 8192 | 8192 | DEFAULT | parquet reader 的最大数据块大小。 | UInt64 |
| parquet_rowgroup_hint_bytes | 134217728 | 134217728 | DEFAULT | 将大型 Parquet 文件划分为多个 rowgroup 以供读取时的提示字节数。默认值：128MB。 | UInt64 |
| parse_datetime_ignore_remainder | 1 | 1 | GLOBAL | 将字符串解析为 datetime 时忽略尾随字符。 | UInt64 |
| persist_materialized_cte | 1 | 1 | DEFAULT | 决定是否将物化 CTE 持久化到磁盘。 | UInt64 |
| prefer_broadcast_join | 1 | 1 | DEFAULT | 启用 broadcast join。 | UInt64 |
| prewhere_selectivity_threshold | 100 | 100 | DEFAULT | 在 prewhere 期间，将行选择下推到剩余列读取中的最大选择率百分比。 | UInt64 |
| proxy_routing_model | statistics | statistics | DEFAULT | 控制 PROXY 如何选择目标表。可选值：`'statistics'`、`'prefix'`。 | String |
| purge_duplicated_files_in_copy | 0 | 0 | DEFAULT | 清理在执行 copy into table 期间检测到的重复文件。 | UInt64 |
| queries_queue_retry_timeout | 300 | 300 | DEFAULT | 查询队列超时的重试间隔。0 表示永不重试。 | UInt64 |
| query_flight_compression | LZ4 | LZ4 | DEFAULT | Flight 压缩方法。可选值：`"None"`、`"LZ4"`、`"ZSTD"`。 | String |
| query_out_of_memory_behavior | spilling | spilling | LOCAL | 如果查询内存限制被超出，系统将执行预定义操作。可选值：`"throw"`、`"spilling"`。 | String |
| query_result_cache_allow_inconsistent | 0 | 0 | DEFAULT | 决定 {{{ .lake }}} 是否返回与底层数据不一致的缓存查询结果。 | UInt64 |
| query_result_cache_max_bytes | 1048576 | 1048576 | DEFAULT | 设置单个查询结果缓存的最大字节大小。 | UInt64 |
| query_result_cache_min_execute_secs | 1 | 1 | DEFAULT | 查询要被缓存，获取第一个数据块所花费的时间必须至少达到该秒数。 | UInt64 |
| query_result_cache_ttl_secs | 300 | 300 | DEFAULT | 设置缓存查询结果的生存时间（TTL，秒）。 | UInt64 |
| query_tag |  |  | DEFAULT | 为当前会话设置查询标签。 | String |
| quoted_ident_case_sensitive | 1 | 1 | GLOBAL | 设置为 1 表示带引号名称按大小写敏感处理，设置为 0 表示大小写不敏感。 | UInt64 |
| random_function_seed | 0 | 0 | DEFAULT | random 函数的数据填充。 | UInt64 |
| recluster_block_size | 9277129359 | 9277129359 | DEFAULT | 设置 recluster 的数据块最大字节大小。 | UInt64 |
| recluster_timeout_secs | 43200 | 43200 | DEFAULT | 设置 recluster final 的超时时间（秒）。 | UInt64 |
| replace_into_bloom_pruning_max_column_number | 4 | 4 | DEFAULT | replace-into 语句中用于 bloom pruning 的最大列数。 | UInt64 |
| replace_into_shuffle_strategy | 0 | 0 | DEFAULT | 选择 shuffle 策略：0 表示 Block，1 表示 Segment 级别。 | UInt64 |
| s3_storage_class | STANDARD | STANDARD | DEFAULT | 默认 S3 存储类型。可选值：`"STANDARD"`、`"INTELLIGENT_TIERING"`。 | String |
| sandbox_tenant |  |  | DEFAULT | 向当前会话注入自定义的 `sandbox_tenant`。仅用于测试。 | String |
| script_max_steps | 10000 | 10000 | DEFAULT | 单次脚本执行允许的最大步数。 | UInt64 |
| short_sql_max_length | 2048 | 2048 | DEFAULT | 设置 short_sql 函数中截断 SQL 查询的最大长度。 | UInt64 |
| sort_spilling_batch_bytes | 20971520 | 20971520 | DEFAULT | 设置 merge sorter 将溢写到存储的未压缩数据大小。 | UInt64 |
| sort_spilling_memory_ratio | 60 | 60 | LOCAL | 设置排序器在查询执行期间将数据溢写到存储之前可使用的最大内存比例（按字节计）。 | UInt64 |
| spatial_runtime_filter_threshold | 1024 | 1024 | DEFAULT | 设置空间列表中用于生成运行时过滤器的最大值数量。 | UInt64 |
| spill_writer_memory_pool_size_mb | 20 | 20 | DEFAULT | 设置每个 spill writer 的内存池大小（MB）。 | UInt64 |
| spilling_file_format | parquet | parquet | DEFAULT | 设置溢写使用的存储文件格式。可选值：`"arrow"`、`"parquet"`。 | String |
| spilling_to_disk_vacuum_unknown_temp_dirs_limit | 18446744073709551615 | 18446744073709551615 | DEFAULT | 设置针对意外中断查询可清理的目录最大数量。 | UInt64 |
| sql_dialect | PostgreSQL | PostgreSQL | DEFAULT | 设置 SQL 方言。可用值：`"PostgreSQL"`、`"MySQL"`、`"Experimental"`、`"Hive"`、`"Prql"`。 | String |
| statement_queue_ttl_in_seconds | 15 | 15 | DEFAULT | 与 meta service 执行租约续期操作的间隔（秒）。 | UInt64 |
| statement_queued_timeout_in_seconds | 0 | 0 | DEFAULT | 在队列中的最大等待时间（秒）。默认值为 0（无限制）。 | UInt64 |
| storage_fetch_part_num | 2 | 2 | DEFAULT | 设置查询执行期间从存储并行获取的分区数量。 | UInt64 |
| storage_io_max_page_bytes_for_read | 524288 | 524288 | DEFAULT | 设置单次 I/O 操作可从存储读取的数据页最大字节大小。 | UInt64 |
| storage_io_min_bytes_for_seek | 48 | 48 | DEFAULT | 设置在定位到新位置时，单次 I/O 操作必须从存储读取的数据最小字节大小。 | UInt64 |
| storage_read_buffer_size | 1048576 | 1048576 | DEFAULT | 设置用于将数据读入内存的缓冲区字节大小。 | UInt64 |
| stream_consume_batch_size_hint | 0 | 0 | DEFAULT | 流消费期间的批大小提示。设置为 0 可禁用。 | UInt64 |
| system_tables_count_db_concurrency | 16 | 16 | DEFAULT | 设置 system.tables count 优化使用的数据库级并发数。 | UInt64 |
| table_lock_expire_secs | 30 | 30 | DEFAULT | 设置表锁的过期时间（秒）。 | UInt64 |
| timezone | UTC | UTC | DEFAULT | 设置时区。 | String |
| trace_sample_rate | 1 | 1 | DEFAULT | 设置 trace 采样率。该值应介于 `'0'` 和 `'100'` 之间。 | UInt64 |
| udf_cloud_import_presign_expire_secs | 259200 | 259200 | DEFAULT | 云 UDF stage 导入的预签名过期时间。 | UInt64 |
| unquoted_ident_case_sensitive | 0 | 0 | DEFAULT | 设置为 1 表示不带引号的名称大小写敏感，设置为 0 表示大小写不敏感。 | UInt64 |
| use_legacy_query_executor | 0 | 0 | DEFAULT | 回退到旧版查询执行器。 | UInt64 |
| use_parquet2 | 0 | 0 | DEFAULT | 此设置已弃用。 | UInt64 |
| warehouse |  |  | DEFAULT | 请使用 `USE WAREHOUSE` 语句来设置 warehouse。 | String |
| week_start | 1 | 1 | DEFAULT | 指定一周的第一天（由与 week 相关的日期函数使用）。 | UInt64 |
| window_num_partitions | 256 | 256 | DEFAULT | 设置窗口算子的分区数量。 | UInt64 |
| window_partition_sort_block_size | 65536 | 65536 | DEFAULT | 设置窗口分区中待排序数据块的数据块大小。 | UInt64 |
| window_partition_spilling_memory_ratio | 60 | 60 | GLOBAL | 设置窗口分区器在将数据溢写到存储之前可使用的最大内存比例（按字节计）。 | UInt64 |
| window_spill_unit_size_mb | 256 | 256 | DEFAULT | 设置窗口算子的溢写单元大小（MB）。 | UInt64 |