---
title: system.caches
summary: An overview of various caches being managed in {{{ .lake }}}.
---

# system.caches

An overview of various caches managed in {{{ .lake }}}, including usage and hit rate statistics.

## Columns

| Column    | Description                                                              |
|-----------|--------------------------------------------------------------------------|
| node      | The node name                                                            |
| name      | Cache name (same as the first parameter in `system$set_cache_capacity`)  |
| num_items | Number of cached entries                                                 |
| size      | Size of cached entries (count or bytes depending on `unit`)              |
| capacity  | Maximum capacity (count or bytes depending on `unit`)                    |
| unit      | Unit of `size` and `capacity`: `count` or `bytes`                       |
| access    | Total number of cache accesses                                           |
| hit       | Number of cache hits                                                     |
| miss      | Number of cache misses                                                   |

## Cache List

| Cache Name                                   | Cached Object                                      | Unit  | Notes |
|----------------------------------------------|----------------------------------------------------|-------|-------|
| memory_cache_table_snapshot                  | Table snapshot                                     | count | Enabled by default; default capacity is usually sufficient |
| memory_cache_table_statistics                | Table statistics                                   | count | |
| memory_cache_compact_segment_info            | Compressed table segment metadata                  | bytes | |
| memory_cache_segment_statistics              | Segment-level statistics                           | bytes | |
| memory_cache_column_oriented_segment_info    | Column-oriented segment metadata                   | bytes | |
| disk_cache_column_data                       | On-disk column data cache                          | bytes | Cannot be adjusted via `system$set_cache_capacity` |
| memory_cache_bloom_index_filter              | Bloom filter data                                  | bytes | One entry per column per block. Memory usage is small. Monitor hit rate for point-lookup workloads. |
| memory_cache_bloom_index_file_meta_data      | Bloom filter metadata                              | count | Each table can cache up to as many entries as it has blocks. Memory usage is small. Monitor hit rate for point-lookup workloads. |
| memory_cache_inverted_index_file_meta_data   | Inverted index metadata                            | count | |
| memory_cache_inverted_index_file             | Inverted index data                                | bytes | |
| memory_cache_vector_index_file_meta_data     | Vector index metadata                              | count | |
| memory_cache_vector_index_file               | Vector index data                                  | bytes | |
| memory_cache_spatial_index_file_meta_data    | Spatial index metadata                             | count | |
| memory_cache_spatial_index_file              | Spatial index data                                 | bytes | |
| memory_cache_virtual_column_file_meta_data   | Virtual column file metadata                       | count | |
| memory_cache_prune_partitions                | Partition pruning cache                            | count | Enabled by default. Caches pruning results for deterministic queries. Set capacity to 0 to bypass for pruning testing. |
| memory_cache_parquet_meta_data               | Parquet file metadata                              | count | Used by Hive tables and other sources |
| memory_cache_iceberg_table                   | Iceberg table metadata                             | count | |

## Example

```sql
SELECT * FROM system.caches;
```

Check utilization and hit rate for all caches:

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
