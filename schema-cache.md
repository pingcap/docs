---
title: Schema Cache
aliases: ['/docs-cn/dev/information-schema-cache']
summary: TiDB adopts an LRU-based (Least Recently Used) caching mechanism for schema information, which significantly reduces memory usage and improves performance in scenarios with a large number of databases and tables.
---

# Schema Cache

In some multi-tenant scenarios, there might be tens of thousands or even millions of databases and tables. Loading all the schema information of these databases and tables into memory can consume a large amount of memory and degrade access performance. To address this issue, TiDB introduces a schema caching mechanism similar to LRU (Least Recently Used). Only the schema information of the most recently accessed databases and tables is cached in memory.

> **Warning:**
>
> This feature is currently an experimental feature and it is not recommended to use in a production environment. This feature might change or be removed without prior notice. If you find a bug, please give feedback by raising an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Configure schema cache

You can enable the schema caching feature by configuring the system variable [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800).

## Best practices

- In scenarios with a large number of databases and tables (for example, more than 100,000 databases and tables) or when the number of databases and tables is large enough to impact system performance, it is recommended to enable the schema caching feature.
- You can monitor the hit rate of the schema cache by observing the subpanel **Infoschema v2 Cache Operation** under the **Schema load** section in TiDB Dashboard. If the hit rate is low, you can increase the value of [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800).
- You can monitor the current size of the schema cache being used by observing the subpanel **Infoschema v2 Cache Size** under the **Schema load** section in TiDB Dashboard.
- It is recommended to disable [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) to reduce TiDB startup time.
- If you need to create a large number of tables (for example, more than 100,000 tables), it is recommended to set this parameter [`split-table`](/tidb-configuration-file.md#split-table) to `false` to reduce the number of regions and thus decrease TiKV's memory usage.

## Known limitations

In scenarios with a large number of databases and tables, the following known issues exist:

- When the tables that need to be accessed are irregularly accessed, such as one set of tables accessed by `t1` and another set accessed by `t2`, and the `tidb_schema_cache_size` setting is small, the schema information might be frequently evicted and cached, leading to performance fluctuations. This feature is more suitable for scenarios where frequently accessed databases and tables are relatively fixed.
- Statistics information might not be collected in a timely manner.
- Access to some metadata information might become slower.
- Switching the schema cache on or off requires a waiting period.
- Operations that involve enumerating all metadata information might become slower, such as:

    - `SHOW FULL TABLES`
    - `FLASHBACK`
    - `ALTER TABLE ... SET TIFLASH MODE ...`
