---
title: system.caches
summary: {{{ .lake }}} 中管理的各种缓存概览。
---

# system.caches

对 {{{ .lake }}} 中管理的各种缓存的概览，包括使用情况和命中率统计信息。

## 列 {#columns}

| 列 | 描述 |
|-----------|--------------------------------------------------------------------------|
| node      | 节点名称 |
| name      | 缓存名称（与 `system$set_cache_capacity` 中的第一个参数相同） |
| num_items | 已缓存条目的数量 |
| size      | 已缓存条目的大小（根据 `unit`，单位为数量或字节） |
| capacity  | 最大容量（根据 `unit`，单位为数量或字节） |
| unit      | `size` 和 `capacity` 的单位：`count` 或 `bytes` |
| access    | 缓存访问总次数 |
| hit       | 缓存命中次数 |
| miss      | 缓存未命中次数 |

## 缓存列表 {#cache-list}

| 缓存名称 | 缓存对象 | 单位 | 说明 |
|----------------------------------------------|----------------------------------------------------|-------|-------|
| memory_cache_table_snapshot                  | 表快照 | count | 默认启用；默认容量通常已足够 |
| memory_cache_table_statistics                | 表统计信息 | count | |
| memory_cache_compact_segment_info            | 压缩表 segment 元信息 | bytes | |
| memory_cache_segment_statistics              | segment 级别统计信息 | bytes | |
| memory_cache_column_oriented_segment_info    | 列式 segment 元信息 | bytes | |
| disk_cache_column_data                       | 磁盘上的列数据缓存 | bytes | 无法通过 `system$set_cache_capacity` 调整 |
| memory_cache_bloom_index_filter              | 布隆过滤器数据 | bytes | 每个 block 的每一列对应一个条目。内存占用较小。对于点查工作负载，请监控命中率。 |
| memory_cache_bloom_index_file_meta_data      | 布隆过滤器元信息 | count | 每张表最多可缓存与其 block 数量相同的条目数。内存占用较小。对于点查工作负载，请监控命中率。 |
| memory_cache_inverted_index_file_meta_data   | 倒排索引元信息 | count | |
| memory_cache_inverted_index_file             | 倒排索引数据 | bytes | |
| memory_cache_vector_index_file_meta_data     | 向量索引元信息 | count | |
| memory_cache_vector_index_file               | 向量索引数据 | bytes | |
| memory_cache_spatial_index_file_meta_data    | 空间索引元信息 | count | |
| memory_cache_spatial_index_file              | 空间索引数据 | bytes | |
| memory_cache_virtual_column_file_meta_data   | 虚拟列文件元信息 | count | |
| memory_cache_prune_partitions                | 分区裁剪缓存 | count | 默认启用。为确定性查询缓存裁剪结果。将容量设置为 0 可在分区裁剪测试中绕过该缓存。 |
| memory_cache_parquet_meta_data               | Parquet 文件元信息 | count | 由 Hive 表和其他数据源使用 |
| memory_cache_iceberg_table                   | Iceberg 表元信息 | count | |

## 示例 {#example}

```sql
SELECT * FROM system.caches;
```

检查所有缓存的利用率和命中率：

```sql
SELECT
    node,
    name,
    capacity,
    if(unit = 'count', (num_items + 1) / (capacity + 1),
       unit = 'bytes', (size + 1) / (capacity + 1), -1) AS utilization,
    if(access = 0, 0, hit / access)  AS hit_rate,
    if(access = 0, 0, miss / access) AS miss_rate,
    num_items,
    size,
    unit,
    access,
    hit,
    miss
FROM system.caches;
```