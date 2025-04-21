---
title: Best Practices for SaaS Multi-Tenant Scenarios
summary: Learn best practices for TiDB in SaaS (Software as a Service) multi-tenant scenarios, especially for environments where the number of tables in a single cluster exceeds one million.
---

# Best Practices for SaaS Multi-Tenant Scenarios

This document introduces best practices for TiDB in SaaS (Software as a Service) multi-tenant environments, especially in scenarios where the **number of tables in a single cluster exceeds one million**. By making reasonable configurations and choices, you can enable TiDB to run efficiently and stably in SaaS scenarios while reducing resource consumption and costs.

> **Note:**
>
> It is recommended to use TiDB v8.5.0 or later versions.

## TiDB hardware recommendations

It is recommended to use high-memory TiDB instances. For example:

- 32 GiB or more memory for 1 million tables
- 64 GiB or more memory for 3 million tables

High-memory TiDB instances can allocate more cache space for Infoschema, Statistics, and execution plan caches, thereby improving cache hit rates and consequently enhancing business performance. Additionally, larger memory can effectively mitigate fluctuation and stability issues caused by TiDB GC.

Recommended hardware configurations for TiKV and PD are as follows:

* TiKV: 8 vCPU 32 GiB or higher
* PD: 8 CPU 16 GiB or higher

## Control the number of Regions

If you need to create a large number of tables (for example, more than 100,000), it is recommended to set the TiDB configuration item [`split-table`](/tidb-configuration-file.md#split-table) to `false` to reduce the number of cluster Regions, thus alleviating memory pressure on TiKV.

## Configure caches

* Starting from TiDB v8.4.0, TiDB loads table information involved in SQL statements into the Infoschema cache on demand during SQL execution. 

    - You can monitor the **Schema Load** panel in TiDB monitoring, specifically the **Infoschema v2 Cache Size** and **Infoschema v2 Cache Operation** sub-panels, to view the size and hit rate of the Infoschema cache. 
    - You can use the [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800) system variable to adjust the memory limit of the Infoschema cache to meet business needs. The size of the Infoschema cache is linearly related to the number of different tables involved in SQL execution. In actual tests, fully caching metadata for 1 million tables (4 columns, 1 primary key, and 1 index) requires about 2.4 GiB memory.

* TiDB loads table statistics involved in SQL statements into the Statistics cache on demand during SQL execution. 

    - You can monitor the **Statistics & Plan Management** panel in TiDB monitoring, specifically the **Stats Cache Cost** and **Stats Cache OPS** sub-panels, to view the size and hit rate of the Statistics cache. 
    - You can use the [`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610) system variable to adjust the memory limit of the Statistics cache to meet business needs. In actual tests, executing simple SQL (using the IndexRangeScan operator) on 100,000 tables results in a Stats cache cost of about 3.96 GiB memory.

## Collect statistics

* Starting from TiDB v8.4.0, TiDB introduces the [`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-new-in-v840) system variable to control the concurrency of individual automatic statistics collection tasks. In multi-table scenarios, you can increase this concurrency as needed to improve the throughput of automatic analysis. As the concurrency value increases, the throughput of automatic analysis and the CPU usage of the TiDB Owner node increase linearly. In actual tests, using a concurrency value of 16 allows automatic analysis of 320 tables (each with 10,000 rows, 4 columns, and 1 index) within one minute, consuming one CPU core of the TiDB Owner node.
* [`tidb_auto_build_stats_concurrency`](/system-variables.md#tidb_auto_build_stats_concurrency-new-in-v650) and [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750) affect the concurrency of TiDB statistics construction. You can adjust them based on the scenario:
    - For scenarios with many partitioned tables, prioritize increasing the value of `tidb_auto_build_stats_concurrency`.
    - For scenarios with many columns, prioritize increasing the value of `tidb_build_sampling_stats_concurrency`.
* It is recommended that the product of the three values of `tidb_auto_analyze_concurrency`, `tidb_auto_build_stats_concurrency` and `tidb_build_sampling_stats_concurrency` does not exceed the number of TiDB CPU cores to avoid excessive resource usage.

## Query system tables efficiently

When querying system tables, it is recommended to add filters such as `TABLE_SCHEMA`, `TABLE_NAME`, or `TIDB_TABLE_ID` to avoid scanning a large amount of irrelevant data. This improves query speed and reduces resource consumption.

For example, in a scenario with 3 million tables:

- Executing the following SQL statement consumes about 8 GiB of memory.

    ```sql
    SELECT COUNT(*) FROM information_schema.tables;
    ```

- Executing the following SQL statement takes about 20 minutes.

    ```sql
    SELECT COUNT(*) FROM information_schema.views;
    ```

By adding the suggested query conditions to the above SQL statements, memory consumption becomes negligible, and query time is reduced to milliseconds.

## Handle connection-intensive scenarios

In SaaS multi-tenant scenarios, each user usually connects to TiDB to operate data in their own tenant (database). To save costs, users want TiDB nodes to support as many connections as possible.

* Increase the TiDB configuration item [`token-limit`](/tidb-configuration-file.md#token-limit) (`1000` by default) to support more concurrent requests.
* The memory usage of TiDB is roughly linear with the number of connections. In actual tests, 200,000 idle connections increase TiDB process memory by about 30 GiB. It is recommended to increase TiDB memory specifications.
* If you use `PREPARED` statements, each connection maintains a session-level Prepared Plan Cache. If the `DEALLOCATE` statement is not executed for a long time, the number of plans in the cache might grow excessively, increasing memory usage. In actual tests, 400,000 execution plans involving IndexRangeScan consume approximately 5 GiB of memory. It is recommended to increase memory specifications accordingly.

## Use stale read carefully

When you use [Stale Read](/stale-read.md), if the schema version used is too outdated, it might trigger a full load of historical schemas, significantly impacting performance. You can mitigate this issue by increasing the value of [`tidb_schema_version_cache_limit`](/system-variables.md#tidb_schema_version_cache_limit-new-in-v740), for example, change it to `255`.

## Optimize BR backup and restore

* In scenarios involving full recovery of millions of tables, it is recommended to use high-memory BR instances. For example:
    - For 1 million tables, use BR instances with 32 GiB or more memory.
    - For 3 million tables, use BR instances with 64 GiB or more memory.
* BR log backup and snapshot recovery consume additional TiKV memory. It is recommended to use TiKV with 32 GiB or higher memory specifications.
* Adjust the BR configurations [`pitr-batch-count` and `pitr-concurrency`](/br/use-br-command-line-tool.md#common-options) as needed to improve BR log recovery speed.

## Import data with TiDB Lightning

When using [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import data for millions of tables, it is recommended to do the following:

- For large tables (larger than 100 GiB), use TiDB Lightning [physical import mode](/tidb-lightning/tidb-lightning-physical-import-mode.md).
- For small tables (which are usually more numerous), use TiDB Lightning [logical import mode](/tidb-lightning/tidb-lightning-logical-import-mode.md).
