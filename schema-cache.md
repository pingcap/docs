---
title: Schema Cache
summary: TiDB adopts an LRU-based (Least Recently Used) caching mechanism for schema information, which significantly reduces memory usage and improves performance in scenarios with a large number of databases and tables.
---

# Schema Cache

In some multi-tenant scenarios, there might be hundreds of thousands or even millions of databases and tables. Loading the schema information of all these databases and tables into memory would not only consume a large amount of memory but also degrade access performance. To address this issue, TiDB introduces a schema caching mechanism similar to LRU (Least Recently Used). Only the schema information of the most recently accessed databases and tables is cached in memory.

> **Warning:**
>
> This feature is currently an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Configure schema cache

You can enable the schema caching feature by configuring the system variable [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800).

## Best practices

- In scenarios with a large number of databases and tables (for example, more than 100,000 databases and tables) or when the number of databases and tables is large enough to affect system performance, it is recommended to enable the schema caching feature.
- You can monitor the hit rate of the schema cache by observing the subpanel **Infoschema v2 Cache Operation** under the **Schema load** section in TiDB Dashboard. If the hit rate is low, you can increase the value of [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800).
- You can monitor the current size of the schema cache being used by observing the subpanel **Infoschema v2 Cache Size** under the **Schema load** section in TiDB Dashboard.
- It is recommended to disable [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) to reduce TiDB startup time.
- If you need to create a large number of tables (for example, more than 100,000 tables), it is recommended to set the [`split-table`](/tidb-configuration-file.md#split-table) parameter to `false` to reduce the number of Regions and thus decrease TiKV's memory usage.

## Known limitations

In scenarios with a large number of databases and tables, the following known issues exist:

- When the tables are irregularly accessed, such as one set of tables are accessed at time1 while another set are accessed at time2, and the value of `tidb_schema_cache_size` is small, the schema information might be frequently evicted and cached, leading to performance fluctuations. This feature is more suitable for scenarios where frequently accessed databases and tables are relatively fixed.
- Statistics information might not be collected in a timely manner.
- Access to some metadata information might become slower.
- Switching the schema cache on or off requires a waiting period.
- Operations that involve enumerating all metadata information might become slower, such as:

    - `SHOW FULL TABLES`
    - `FLASHBACK`
    - `ALTER TABLE ... SET TIFLASH MODE ...`
- When you use tables with the [`AUTO_INCREMENT`](/auto-increment.md) or [`AUTO_RANDOM`](/auto-random.md) attribute, a small schema cache size might cause the meta data of these tables to frequently enter and leave the cache. This can result in the allocated ID range becoming invalid before being fully used, leading to ID jumps. In write-intensive scenarios, this might even exhaust the ID range. To minimize abnormal ID allocation behavior and improve system stability, it is recommended to take the following measures:

    - View the hit rate and size of the schema cache on the monitoring panel to assess whether the cache settings are reasonable. Increase the schema cache size properly to reduce frequent evictions.
    - Set [`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) to `1` to prevent ID jumps.
    - Properly configure the shard bits and reserved bits of `AUTO_RANDOM` to avoid a too small ID range.