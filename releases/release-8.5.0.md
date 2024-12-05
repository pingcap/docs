---
title: TiDB 8.5.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.5.0.
---

# TiDB 8.5.0 Release Notes

<EmailSubscriptionWrapper />

Release date: xx xx, 2024

TiDB version: 8.5.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

TiDB 8.5.0 is a Long-Term Support Release (LTS).

Compared with the previous LTS 8.1.0, 8.5.0 includes new features, improvements, and bug fixes released in [8.2.0-DMR](/releases/release-8.2.0.md), [8.3.0-DMR](/releases/release-8.3.0.md), and [8.4.0-DMR](/releases/release-8.4.0.md). When you upgrade from 8.1.x to 8.5.0, you can download the [TiDB Release Notes PDF](https://download.pingcap.org/tidb-v8.1-to-v8.5-en-release-notes.pdf) to view all release notes between the two LTS versions. The following table lists some highlights from 8.1.0 to 8.5.0:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature/Enhancement</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="6">Scalability and Performance</td>
    <td>Reduce data processing latency in multiple dimensions **tw@qiancai**</td>
    <td>TiDB continuously refines data processing to improve performance, effectively meeting the low-latency SQL processing requirements in financial scenarios. Key updates include: 
    <li>Support <a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_executor_concurrency-new-in-v50">parallel sorting</a> (introduced in v8.2.0) </li>
    <li>Optimize <a href="https://docs.pingcap.com/zh/tidb/v8.5/tidb-configuration-file#batch-policy-new-in-v830">batch processing strategy for KV (key-value) requests </a> (introduced in v8.3.0) </li>
    <li>Support <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_tso_client_rpc_mode-new-in-v840">parallel mode for TSO requests</a> (introduced in v8.4.0) </li>
    <li>Reduce the resource overhead of <a href="https://docs.pingcap.com/tidb/v8.5/sql-statement-delete">DELETE</a> operations (introduced in v8.4.0) </li>
    <li>Improve query performance for <a href="https://docs.pingcap.com/tidb/v8.5/cached-tables">cached tables</a> (introduced in v8.4.0) </li>
    <li>Introduce <a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_hash_join_version-new-in-v840">an optimized version of Hash Join</a> (introduced in v8.4.0) </li>
    </td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">Use Active PD Followers to enhance PD's Region information query service</a> (GA in v8.5.0) **tw@Oreoxmt 2015**</td>
    <td>TiDB v7.6.0 introduces an experimental feature "Active PD Follower", which allows PD followers to provide Region information query services. This feature improves the capability of the PD cluster to handle <code>GetRegion</code> and <code>ScanRegions</code> requests in clusters with a large number of TiDB nodes and Regions, thereby reducing the CPU pressure on PD leaders. In v8.5.0, this feature becomes generally available (GA).</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_instance_plan_cache-new-in-v840">Instance-level execution plan cache</a> (experimental, introduced in v8.4.0) </td>
    <td>Instance-level plan cache allows all sessions within the same TiDB instance to share the plan cache. Compared with session-level plan cache, this feature reduces SQL compilation time by caching more execution plans in memory, decreasing overall SQL execution time. It improves OLTP performance and throughput while providing better control over memory usage and enhancing database stability.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/partitioned-table#global-indexes">Global indexes for partitioned tables</a> (GA in v8.4.0)</td>
    <td>Global indexes can effectively improve the efficiency of retrieving non-partitioned columns, and remove the restriction that a unique key must contain the partition key. This feature extends the usage scenarios of TiDB partitioned tables, improves the performance of partitioned tables, and reduces resource consumption in certain query scenarios.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_projection_push_down-new-in-v610">Default pushdown of the <code>Projection</code> operator to the storage engine</a> (introduced in v8.3.0) </td>
    <td>Pushing the <code>Projection</code> operator down to the storage engine can distribute the load across storage nodes while reducing data transfer between nodes. This optimization helps to reduce the execution time for certain SQL queries and improves the overall database performance.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/statistics#collect-statistics-on-some-columns">Ignoring unnecessary columns when collecting statistics</a> (introduced in v8.3.0) </td>
    <td>Under the premise of ensuring that the optimizer can obtain the necessary information, TiDB speeds up statistics collection, improves the timeliness of statistics, and thus ensures that the optimal execution plan is selected, improving the performance of the cluster. Meanwhile, TiDB also reduces the system overhead and improves the resource utilization.</td>
  </tr>
  <tr>
    <td rowspan="5">Reliability and availability</td>
    <td>Improve the stability of large-scale clusters **tw@hfxsd 1976**</td>
    <td>Companies that use TiDB to run multi-tenant or SaaS applications often need to store a large number of tables. In v8.5.0, TiDB significantly enhances the stability of large-scale clusters. <a href="https://docs.pingcap.com/tidb/v8.5/schema-cache">Schema cache control</a> and <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_stats_cache_mem_quota-new-in-v610">setting the memory quota for the TiDB statistics cache</a> are generally available (GA), reducing stability issues caused by excessive memory consumption. PD introduces <a href="https://docs.pingcap.com/tidb/v8.5/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">Active Follower</a> to handle the pressure brought by numerous Regions, and gradually <a href="https://docs.pingcap.com/tidb/v8.5/pd-microservices">decouples the services handled by PD</a> for independent deployment. You can <a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_auto_analyze_concurrency-new-in-v840">increase concurrency</a> and <a href="https://docs.pingcap.com/zh/tidb/v8.5/statistics#collect-statistics-on-some-columns">reduce the number of collected objects</a> to improve the efficiency of statistics collection and loading, ensuring the stability of execution plans in large clusters.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/tidb-resource-control#query_limit-parameters">Support more triggers for runaway queries, and support switching resource groups</a> (introduced in v8.4.0) </td>
    <td>Runaway Queries offer an effective way to mitigate the impact of unexpected SQL performance issues on systems. TiDB v8.4.0 introduces the number of keys processed by the Coprocessor (<code>PROCESSED_KEYS</code>) and request units (<code>RU</code>) as identifying conditions, and puts identified queries into the specified resource group for more precise identification and control of runaway queries.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/tidb-resource-control#background-parameters">Support setting the maximum limit on resource usage for background tasks of resource control</a> (experimental, introduced in v8.4.0) </td>
    <td>By setting a maximum percentage limit on background tasks of resource control, you can control their resource consumption based on the needs of different application systems. This keeps background task consumption at a low level and ensures the quality of online services.</td>
  </tr>
  <tr>
    <td>Enhance and expand TiProxy use cases **tw@Oreoxmt**</td>
    <td>As a crucial component of the high availability of TiDB, <a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-overview">TiProxy</a> extends its capabilities beyond SQL traffic access and forwarding to support cluster change evaluation. Key features include:
    <li><a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-traffic-replay">TiProxy supports traffic capture and replay</a> (experimental, introduced in v8.4.0)</li>
    <li><a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-overview">TiProxy supports built-in virtual IP management</a> (introduced in v8.3.0)</li>
    <li><a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-load-balance">TiProxy supports multiple load balancing policies</a> (introduced in v8.2.0)</li>
    </td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_enable_parallel_hashagg_spill-new-in-v800">The parallel HashAgg algorithm of TiDB supports disk spill</a> (GA in v8.2.0) </td>
    <td>HashAgg is a widely used aggregation operator in TiDB for efficiently aggregating rows with the same field values. TiDB v8.0.0 introduces parallel HashAgg as an experimental feature to further enhance processing speed. When memory resources are insufficient, parallel HashAgg spills temporary sorted data to disk, avoiding potential OOM risks caused by excessive memory usage. This improves query performance while maintaining node stability. In v8.2.0, this feature becomes generally available (GA) and is enabled by default, enabling you to safely configure the concurrency of parallel HashAgg using <code>tidb_executor_concurrency</code>.</td>
  </tr>
  <tr>
    <td rowspan="2"> SQL </td>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/foreign-key">Foreign key</a> (GA in v8.5.0) **tw@lilin90 1894**</td>
    <td>Foreign keys are constraints in a database that establish relationships between tables, ensuring data consistency and integrity. They ensure that the data referenced in a child table exist in the parent table, preventing the insertion of invalid data. Foreign keys also support cascading operations (such as automatic synchronization during deletion or update), simplifying business logic implementation and reducing the complexity of manually maintaining data relationships.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/vector-search-overview">Vector search</a> (experimental, introduced in v8.4.0) </td>
    <td>Vector search is a search method based on data semantics, which provides more relevant search results. As one of the core functions of AI and large language models (LLMs), vector search can be used in various scenarios such as Retrieval-Augmented Generation (RAG), semantic search, and recommendation systems.</td>
  </tr>
  <tr>
    <td rowspan="3">DB Operations and Observability</td>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/information-schema-processlist">Display TiKV and TiDB CPU times in memory tables</a> (introduced in v8.4.0) </td>
    <td>The CPU time is now integrated into a system table, displayed alongside other metrics for sessions or SQL, letting you observe high CPU consumption operations from multiple perspectives, and improving diagnostic efficiency. This is especially useful for diagnosing scenarios such as CPU spikes in instances or read/write hotspots in clusters.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/top-sql#use-top-sql">Support viewing aggregated TiKV CPU time by table or database</a> (introduced in v8.4.0) </td>
    <td>When hotspot issues are not caused by individual SQL statements, using the aggregated CPU time by table or database level in Top SQL can help you quickly identify the tables or applications responsible for the hotspots, significantly improving the efficiency of diagnosing hotspot and CPU consumption issues. </td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.5/backup-and-restore-storages#authentication">Support backing up TiKV instances with IMDSv2 service enabled</a> (introduced in v8.4.0) </td>
    <td><a href="https://aws.amazon.com/cn/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/">AWS EC2 now uses IMDSv2 as the default metadata service</a>. TiDB supports backing up data from TiKV instances that have IMDSv2 enabled, helping you run TiDB clusters more effectively in public cloud services.</td>
  </tr>
  <tr>
    <td rowspan="1">Security</td>
    <td>Client-side encryption of <a href="https://docs.pingcap.com/tidb/v8.5/br-snapshot-manual#encrypt-the-backup-data">snapshot backup data</a> and <a href="https://docs.pingcap.com/tidb/v8.5/br-pitr-manual#encrypt-log-backup-data">log backup data</a> (GA in v8.5.0)**tw@qiancai 1998**</td>
    <td>Before uploading backup data to your backup storage, you can encrypt the backup data to ensure its security during storage and transmission.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* Setting the memory limit for schema cache is now generally available (GA), reducing memory usage in large-scale data scenarios [#50959](https://github.com/pingcap/tidb/issues/50959) @[tiancaiamao](https://github.com/tiancaiamao) @[wjhuang2016](https://github.com/wjhuang2016) @[gmhdbjd](https://github.com/gmhdbjd) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--1976-->

    In some SaaS scenarios, where the number of tables reaches hundreds of thousands or even millions, schema metadata can consume a significant amount of memory. With this feature enabled, TiDB uses the Least Recently Used (LRU) algorithm to cache and evict the corresponding schema metadata, effectively reducing memory usage.

    Starting from v8.4.0, this feature is enabled by default with a default value of `536870912` (that is, 512 MiB). You can adjust it as needed using the variable [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800).

    For more information, see [documentation](/schema-cache.md).

* Provide the Active PD Follower feature to enhance the scalability of PD's Region information query service (GA) [#7431](https://github.com/tikv/pd/issues/7431) @[okJiang](https://github.com/okJiang) tw@Oreoxmt <!--2015-->

    In a TiDB cluster with a large number of Regions, the PD leader might experience high CPU load due to the increased overhead of handling heartbeats and scheduling tasks. If the cluster has many TiDB instances, and there is a high concurrency of requests for Region information, the CPU pressure on the PD leader increases further and might cause PD services to become unavailable.

    To ensure high availability, TiDB v7.6.0 introduces Active PD Follower as an experimental feature to enhance the scalability of PD's Region information query service. In v8.5.0, this feature becomes generally available (GA). You can enable the Active PD Follower feature by setting the system variable [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) to `ON`. After this feature is enabled, TiDB evenly distributes Region information requests to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader.

    For more information, see [documentation](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service).

### Performance

* TiDB accelerated table creation becomes generally available (GA), significantly reducing data migration and cluster initialization time [#50052](https://github.com/pingcap/tidb/issues/50052) @[D3Hunter](https://github.com/D3Hunter) @[gmhdbjd](https://github.com/gmhdbjd) tw@Oreoxmt <!--1977-->

    TiDB v7.6.0 introduces accelerated table creation as an experimental feature, controlled by the system variable [`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760). Staring from v8.0.0, this system variable is renamed to [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800).

    In v8.5.0, TiDB accelerated table creation becomes generally available (GA) and is enabled by default. During data migration and cluster initialization, this feature supports rapid creation of millions of tables, significantly reducing operation time.

    For more information, see [Documentation](/accelerated-table-creation.md).

* TiKV supports the MVCC in-memory engine (IME), which accelerates queries involving scans of extensive MVCC historical versions [#16141](https://github.com/tikv/tikv/issues/16141) [@SpadeA-Tang](https://github.com/SpadeA-Tang) [@glorv](https://github.com/glorv) [@overvenus](https://github.com/overvenus)

    When records are frequently updated, or TiDB is required to retain historical versions for extended periods (for example, 24 hours), the accumulation of MVCC versions can degrade scan performance. The TiKV MVCC in-memory engine improves scan performance by caching the latest MVCC versions in memory, and using a rapid GC mechanism to remove historical versions from memory.

    Starting from v8.5.0, TiKV introduces MVCC in-memory engine. If the accumulation of MVCC versions in the TiKV cluster leads to degraded scan performance, you can enable the TiKV MVCC in-memory engine to improve scan performance by setting the TiKV configuration parameter [`in-memory-engine.enable`](/tikv-in-memory-engine.md#usage).

    For more information, see [documentation](/tikv-in-memory-engine.md).

### Reliability

* Support limiting the maximum rate and concurrency of requests processed by PD [#5739](https://github.com/tikv/pd/issues/5739) @[rleungx](https://github.com/rleungx) **tw@qiancai** <!--2018-->

    When a sudden influx of requests is sent to PD, it can lead to high workloads and potentially affect PD performance. Starting from v8.5.0, you can use [`pd-ctl`](/pd-control.md) to limit the maximum rate and concurrency of requests processed by PD, improving its stability.

    For more information, see [documentation](/pd-control.md).

### SQL

* Support foreign keys (GA) [#36982](https://github.com/pingcap/tidb/issues/36982) @[YangKeao](https://github.com/YangKeao) @[crazycs520](https://github.com/crazycs520) tw@lilin90 <!--1894-->

    The foreign key feature becomes generally available (GA) in v8.5.0. Foreign key constraints help ensure data consistency and integrity. You can easily establish foreign key relationships between tables, with support for cascading updates and deletions, simplifying data management. This feature enhances support for applications with complex data relationships.

    For more information, see [documentation](/foreign-key.md).

* Introduce the `ADMIN ALTER DDL JOBS` statement to support modifying the DDL jobs online [#57229](https://github.com/pingcap/tidb/issues/57229) @[fzzf678](https://github.com/fzzf678) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--2016-->

    Starting from v8.3.0, you can set the variables [`tidb_ddl_reorg_batch_size`](/system-variables#tidb_ddl_reorg_batch_size) and [`tidb_ddl_reorg_worker_cnt`](/system-variables#tidb_ddl_reorg_worker_cnt) at the session level. As a result, setting these two variables globally no longer affects all running DDL jobs. To modify the values of these variables, you need to cancel the DDL job first, adjust the variables, and then resubmit the job.

    TiDB v8.5.0 introduces the `ADMIN ALTER DDL JOBS` statement, letting you adjust the variable values of specific DDL jobs online. This enables flexible balancing of resource consumption and performance. The changes are limited to individual jobs, making the impact more controllable. For example:

    - `ADMIN ALTER DDL JOBS job_id THREAD = 8;`: adjusts the `tidb_ddl_reorg_worker_cnt` of the specified DDL job online.
    - `ADMIN ALTER DDL JOBS job_id BATCH_SIZE = 256;`: adjusts the `tidb_ddl_reorg_batch_size` of the specified job online.
    - `ADMIN ALTER DDL JOBS job_id MAX_WRITE_SPEED = '200MiB';`: adjusts the write traffic of index data to each TiKV node online.

  For more information, see [documentation](/sql-statements/sql-statement-admin-alter-ddl.md).

### Security

* BR supports client-side encryption of both full backup data and log backup data (GA) [#28640](https://github.com/pingcap/tidb/issues/28640) [#56433](https://github.com/pingcap/tidb/issues/56433) @[joccau](https://github.com/joccau) @[Tristan1900](https://github.com/Tristan1900) tw@qiancai <!--1998-->

    * Client-side encryption of full backup data (introduced as experimental in TiDB v5.3.0) enables you to encrypt backup data on the client side using a custom fixed key.

    * Client-side encryption of log backup data (introduced as experimental in TiDB v8.4.0) enables you to encrypt log backup data on the client side using one of the following methods:

        * Encrypt using a custom fixed key
        * Encrypt using a master key stored on a local disk
        * Encrypt using a master key managed by a Key Management Service (KMS)

  Starting from v8.5.0, both encryption features become generally available (GA), offering enhanced client-side data security.

    For more information, see [Encrypt the backup data](/br/br-snapshot-manual.md#encrypt-the-backup-data) and [Encrypt the log backup data](/br/br-pitr-manual.md#encrypt-the-log-backup-data).

* TiKV encryption at rest supports [Google Cloud Key Management Service (Google Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive) (GA) [#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv) **tw@qiancai** <!--1876-->

    TiKV ensures data security by using the encryption at rest technique to encrypt stored data. The core aspect of this technique is proper key management. In v8.0.0, TiKV encryption at rest experimentally supports using Google Cloud KMS for master key management.

    Starting from v8.5.0, encryption at rest using Google Cloud KMS becomes generally available (GA). To use this feature, first create a key on Google Cloud, and then configure the `[security.encryption.master-key]` section in the TiKV configuration file.

    For more information, see [documentation](/encryption-at-rest.md#tikv-encryption-at-rest).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.1.0 to the current version (v8.2.0). If you are upgrading from v8.0.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

- In non-strict mode (`sql_mode = ''`), inserting `NULL` values into non-`NULL` columns now returns an error for MySQL compatibility. [#55457](https://github.com/pingcap/tidb/issues/55457) @[joechenrh](https://github.com/joechenrh)
- The `ALTER TABLE ... DROP FOREIGN KEY IF EXISTS ...` statement is no longer supported. [#56703](https://github.com/pingcap/tidb/pull/56703) @[YangKeao](https://github.com/YangKeao)

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that the [accelerated table creation](/accelerated-table-creation.md) feature is enabled by default. |
| [`tidb_ddl_reorg_max_write_speed`](/system-variables.md#tidb_ddl_reorg_max_write_speed-new-in-v850)  | Newly added | Limits the write bandwidth for each TiKV node and only takes effect when index creation acceleration is enabled (controlled by the [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630) variable). For example, setting the variable to `200MiB` limits the maximum write speed to 200 MiB/s.  |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`deprecate-integer-display-length`](/tidb-configuration-file.md#deprecate-integer-display-length) | Modified | Starting from v8.5.0, the integer display width feature is deprecated. The default value of this configuration item is changed from `false` to `true`. |
| TiKV | [`raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size) | Modified | Changes the default value from `8192` to `16384`. |

## Deprecated features

The following features are planned for deprecation in future versions:

* In v8.0.0, TiDB introduces the [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) system variable to control whether priority queues are enabled to optimize the ordering of tasks that automatically collect statistics. In future releases, the priority queue will be the only way to order tasks for automatically collecting statistics, so this system variable will be deprecated.
* In v7.5.0, TiDB introduces the [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) system variable. You can use it to set TiDB to use asynchronous merging of partition statistics to avoid OOM issues. In future releases, partition statistics will be merged asynchronously, so this system variable will be deprecated.
* It is planned to redesign [the automatic evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.
* In v8.0.0, TiDB introduces the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable to control whether TiDB supports disk spill for the concurrent HashAgg algorithm. In future versions, this system variable will be deprecated.
* In v5.1, TiDB introduces the [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) system variable to control whether to enable the dynamic pruning mode for partitioned tables. Starting from v8.5.0, a warning is returned when you set this variable to `static` or `static-only`. In future versions, this system variable will be deprecated.
* The TiDB Lightning parameter [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is planned for deprecation in a future release and will be subsequently removed. This parameter will be replaced by [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task), which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.
* Starting from v6.3.0, partitioned tables use [dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) by default. Compared with static pruning mode, dynamic pruning mode supports features such as IndexJoin and plan cache with better performance. Therefore, static pruning mode will be deprecated.

## Improvements

+ TiDB <!--tw@hfxsd: 12 notes-->

    - Improve the response speed of job cancellation for the `ADD INDEX` acceleration feature when disabling the Distributed eXecution Framework (DXF) [#56017](https://github.com/pingcap/tidb/issues/56017) @[lance6716](https://github.com/lance6716)
    - Improve the speed of adding indexes to small tables [#54230](https://github.com/pingcap/tidb/issues/54230) @[tangenta](https://github.com/tangenta)
    - Add a new system variable `tidb_ddl_reorg_max_write_speed` to limit the maximum speed of the ingest phase when adding indexes [#57156](https://github.com/pingcap/tidb/issues/57156) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Improve the performance of querying `information_schema.tables` in some cases [#57295](https://github.com/pingcap/tidb/issues/57295) @[tangenta](https://github.com/tangenta)
    - Support dynamically adjusting more DDL job parameters [#57526](https://github.com/pingcap/tidb/issues/57526) @[fzzf678](https://github.com/fzzf678)
    - Support global indexes that contain all columns from a partition expression [#56230](https://github.com/pingcap/tidb/issues/56230) @[Defined2014](https://github.com/Defined2014)
    - Support partition pruning for list partitioned tables in range query scenarios [#56673](https://github.com/pingcap/tidb/issues/56673) @[Defined2014](https://github.com/Defined2014)
    - Enable FixControl#46177 by default to fix the issue that a full table scan is incorrectly selected instead of an index range scan in some cases [#46177](https://github.com/pingcap/tidb/issues/46177) @[terry1purcell](https://github.com/terry1purcell)
    - Improve the internal estimation logic to better utilize statistics of multi-column and multi-value indexes, enhancing estimation accuracy for certain queries involving multi-value indexes [#56915](https://github.com/pingcap/tidb/issues/56915) @[time-and-fate](https://github.com/time-and-fate)
    - Improve the cost estimation for full table scans in specific scenarios, reducing the probability of incorrectly choosing a full table scan [#57085](https://github.com/pingcap/tidb/issues/57085) @[terry1purcell](https://github.com/terry1purcell)
    - Optimize the amount of data required for synchronous loading of statistics to improve loading performance [#56812](https://github.com/pingcap/tidb/issues/56812) @[winoros](https://github.com/winoros)
    - Optimize the execution plan in specific cases where an `OUTER JOIN` involves a unique index and an `ORDER BY ... LIMIT` clause, improving execution efficiency [#56321](https://github.com/pingcap/tidb/issues/56321) @[winoros](https://github.com/winoros)

+ TiKV <!--tw@hfxsd: 2 notes-->

    - Use a separate thread to clean up replicas, ensuring stable latency for critical paths of Raft reads and writes [#16001](https://github.com/tikv/tikv/issues/16001) @[hbisheng](https://github.com/hbisheng)
    - Improve the performance of the vector distance function by supporting SIMD [#17290](https://github.com/tikv/tikv/issues/17290) @[EricZequan](https://github.com/EricZequan)

+ PD <!--tw@qiancai: 2 notes-->

    - Support dynamic switching of the `tso` service between microservice and non-microservice modes [#8477](https://github.com/tikv/pd/issues/8477) @[rleungx](https://github.com/rleungx)
    - Optimize the case format of certain fields in the `pd-ctl config` output [#8694](https://github.com/tikv/pd/issues/8694) @[lhy1024](https://github.com/lhy1024)
    - [Store limit v2](/configure-store-limit.md#principles-of-store-limit-v2) becomes generally available (GA) [#8865](https://github.com/tikv/pd/issues/8865) @[lhy1024](https://github.com/lhy1024)
    - Support configuring Region inspection concurrency (experimental) [#8866](https://github.com/tikv/pd/issues/8866) @[lhy1024](https://github.com/lhy1024)

+ TiFlash <!--tw@Oreoxmt: 3 notes-->

    - (dup): release-7.1.6.md > Improvements> TiFlash - Improve the garbage collection speed of outdated data in the background for tables with clustered indexes [#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Improve query performance of vector search in data update scenarios [#9599](https://github.com/pingcap/tiflash/issues/9599) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Add monitoring metrics for CPU usage during vector index building [#9032](https://github.com/pingcap/tiflash/issues/9032) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Improve the execution efficiency of logical operators [#9146](https://github.com/pingcap/tiflash/issues/9146) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR) <!--tw@Oreoxmt: 4 notes-->

        - (dup): release-7.1.6.md > Improvements> Tools> Backup & Restore (BR) - Reduce unnecessary log printing during backup [#55902](https://github.com/pingcap/tidb/issues/55902) @[Leavrth](https://github.com/Leavrth)
        - Optimize the error message for the encryption key `--crypter.key` [#56388](https://github.com/pingcap/tidb/issues/56388) @[Tristan1900](https://github.com/Tristan1900)
        - Increase concurrency in BR when creating databases to improve data restore performance [#56866](https://github.com/pingcap/tidb/issues/56866) @[Leavrth](https://github.com/Leavrth)
        - During a full backup, the checksum for BR internal validation is disabled by default (`--checksum=false`) to improve backup performance. The checksum used to verify backup data integrity remains enabled [#56373](https://github.com/pingcap/tidb/issues/56373) @[Tristan1900](https://github.com/Tristan1900)
        - Add a mechanism to independently track and reset the connection timeout for each storage node, enhancing the handling of slow nodes and preventing backup operations from hanging [#57666](https://github.com/pingcap/tidb/issues/57666) @[3pointer](https://github.com/3pointer)

    + TiDB Data Migration (DM) <!--tw@lilin90: 1 note-->

        - Add retries for DM-worker to connect to DM-master during DM cluster startup [#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)

## Bug fixes

+ TiDB <!--tw@qiancai: the following 20 notes-->

    - Fix the issue that TiDB does not automatically retry requests when the Region metadata returned from PD lacks Leader information, potentially causing execution errors [#56757](https://github.com/pingcap/tidb/issues/56757) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-7.1.6.md > Bug fixes> TiDB - Fix the issue that TTL tasks cannot be canceled when there is a write conflict [#56422](https://github.com/pingcap/tidb/issues/56422) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.1.6.md > Bug fixes> TiDB - Fix the issue that when canceling a TTL task, the corresponding SQL is not killed forcibly [#56511](https://github.com/pingcap/tidb/issues/56511) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-7.1.6.md > Bug fixes> TiDB - Fix the issue that existing TTL tasks are executed unexpectedly frequently in a cluster that is upgraded from v6.5 to v7.5 or later [#56539](https://github.com/pingcap/tidb/issues/56539) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-7.1.6.md > Bug fixes> TiDB - Fix the issue that the `INSERT ... ON DUPLICATE KEY` statement is not compatible with `mysql_insert_id` [#55965](https://github.com/pingcap/tidb/issues/55965) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.1.6.md > Bug fixes> TiDB - Fix the issue that TTL might fail if TiKV is not selected as the storage engine [#56402](https://github.com/pingcap/tidb/issues/56402) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.1.6.md > Bug fixes> TiDB - Fix the issue that the `AUTO_INCREMENT` field is not correctly set after importing data using the `IMPORT INTO` statement [#56476](https://github.com/pingcap/tidb/issues/56476) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-7.1.6.md > Bug fixes> TiDB - Fix the issue that TiDB does not check the index length limitation when executing `ADD INDEX` [#56930](https://github.com/pingcap/tidb/issues/56930) @[fzzf678](https://github.com/fzzf678)
    - (dup): release-7.1.6.md > Bug fixes> TiDB - Fix the issue that executing `RECOVER TABLE BY JOB JOB_ID;` might cause TiDB to panic [#55113](https://github.com/pingcap/tidb/issues/55113) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-7.1.6.md > Bug fixes> TiDB - Fix the issue that stale read does not strictly verify the timestamp of the read operation, resulting in a small probability of affecting the consistency of the transaction when an offset exists between the TSO and the real physical time [#56809](https://github.com/pingcap/tidb/issues/56809) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that TiDB could not resume Reorg DDL tasks from the previous progress after the DDL owner node is switched [#56506](https://github.com/pingcap/tidb/issues/56506) @[tangenta](https://github.com/tangenta)
    - Fix the issue that some metrics in the monitoring panel of Distributed eXecution Framework (DXF) are inaccurate [#57172](https://github.com/pingcap/tidb/issues/57172) @[fzzf678](https://github.com/fzzf678) [#56942](https://github.com/pingcap/tidb/issues/56942) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that `REORGANIZE PARTITION` fails to return error reasons in certain cases [#56634](https://github.com/pingcap/tidb/issues/56634) @[mjonss](https://github.com/mjonss)
    - Fix the issue that querying `INFORMATION_SCHEMA.TABLES` returns incorrect results due to case sensitivity [#56987](https://github.com/pingcap/tidb/issues/56987) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue of illegal memory access that might occur when a Common Table Expression (CTE) has multiple data consumers and one consumer exits without reading any data [#55881](https://github.com/pingcap/tidb/issues/55881) @[windtalker](https://github.com/windtalker)
    - Fix the issue that `INDEX_HASH_JOIN` might hang during an abnormal exit [#54055](https://github.com/pingcap/tidb/issues/54055) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the `TRUNCATE` statement returns incorrect results when handling `NULL` values [#53546](https://github.com/pingcap/tidb/issues/53546) @[tuziemon](https://github.com/tuziemon)
    - Fix the issue that the `CAST AS CHAR` function returns incorrect results due to type inference errors [#56640](https://github.com/pingcap/tidb/issues/56640) @[zimulala](https://github.com/zimulala)
    - Fix the issue of truncated strings in the output of some functions due to type inference errors [#56587](https://github.com/pingcap/tidb/issues/56587) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that the `ADDTIME()` and `SUBTIME()` functions returns incorrect results when their first argument is a date type [#57569](https://github.com/pingcap/tidb/issues/57569) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that invalid `NULL` values can be inserted in non-strict mode (`sql_mode = ''`) [#56381](https://github.com/pingcap/tidb/issues/56381) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that the `UPDATE` statement incorrectly updates values of the `ENUM` type [#56832](https://github.com/pingcap/tidb/issues/56832) @[xhebox](https://github.com/xhebox)
    - Fix the issue that enabling the `tidb_low_resolution_tso` variable causes resource leaks during the execution of `SELECT FOR UPDATE` statements [#55468](https://github.com/pingcap/tidb/issues/55468) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `JSON_TYPE()` function does not validate the parameter type, causing no errors returned when a non-JSON data type is passed [#54029](https://github.com/pingcap/tidb/issues/54029) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that using JSON functions in `PREPARE` statements might cause execution failures [#54044](https://github.com/pingcap/tidb/issues/54044) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that converting data from the `BIT` type to the `CHAR` type might cause TiKV panics [#56494](https://github.com/pingcap/tidb/issues/56494) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that using variables or parameters in the `CREATE VIEW` statement does not report errors [#53176](https://github.com/pingcap/tidb/issues/53176) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the `JSON_VALID()` function returns incorrect results [#56293](https://github.com/pingcap/tidb/issues/56293) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that TTL tasks are not canceled after the `tidb_ttl_job_enable` variable is disabled [#57404](https://github.com/pingcap/tidb/issues/57404) @[YangKeao](https://github.com/YangKeao) <!--tw@lilin90: the following 20 notes-->
    - Fix the issue that using the `RANGE COLUMNS` partition function and the `utf8mb4_0900_ai_ci` collation at the same time could result in incorrect query results [#57261](https://github.com/pingcap/tidb/issues/57261) @[Defined2014](https://github.com/Defined2014)
    - Fix the runtime error caused by executing a prepared statement that begins with a newline character, resulting in an array out of bounds [#54283](https://github.com/pingcap/tidb/issues/54283) @[Defined2014](https://github.com/Defined2014)
    - Fix the precision issue in the `UTC_TIMESTAMP()` function, such as setting the precision too high [#56451](https://github.com/pingcap/tidb/issues/56451) @[chagelo](https://github.com/chagelo)
    - Fix the issue that foreign key errors are not omitted in `UPDATE`, `INSERT`, and `DELETE IGNORE` statements [#56678](https://github.com/pingcap/tidb/issues/56678) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that when querying the `information_schema.cluster_slow_query` table, if the time filter is not added, only the latest slow log file is queried [#56100](https://github.com/pingcap/tidb/issues/56100) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue of memory leaks in TTL tables [#56934](https://github.com/pingcap/tidb/issues/56934) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that foreign key constraints do not take effect for tables in `write_only` status, preventing using tables in `non-public` status [#55813](https://github.com/pingcap/tidb/issues/55813) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that using subqueries after the `NATURAL JOIN` or `USING` clause might result in errors [#53766](https://github.com/pingcap/tidb/issues/53766) @[dash12653](https://github.com/dash12653)
    - Fix the issue that if a CTE contains the `ORDER BY`, `LIMIT`, or `SELECT DISTINCT` clause and is referenced by the recursive part of another CTE, it might be incorrectly inlined and result in an execution error [#56603](https://github.com/pingcap/tidb/issues/56603) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that the CTE defined in `VIEW` is incorrectly inlined [#56582](https://github.com/pingcap/tidb/issues/56582) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that Plan Replayer might report an error when importing a table structure containing foreign keys [#56456](https://github.com/pingcap/tidb/issues/56456) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that Plan Replayer might report an error when importing a table structure containing Placement Rules [#54961](https://github.com/pingcap/tidb/issues/54961) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that when using `ANALYZE` to collect statistics for a table, if the table contains expression indexes of virtually generated columns, the execution reports an error [#57079](https://github.com/pingcap/tidb/issues/57079) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `DROP DATABASE` statement does not correctly trigger the corresponding update in statistics [#57227](https://github.com/pingcap/tidb/issues/57227) @[Rustin170506](https://github.com/Rustin170506)
    - Fix the issue that when parsing a database name in CTE, it returns a wrong database name [#54582](https://github.com/pingcap/tidb/issues/54582) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the upper bound and lower bound of the histogram are corrupted when `DUMP STATS` is transforming statistics into JSON [#56083](https://github.com/pingcap/tidb/issues/56083) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `EXISTS` subquery results, when further involved in algebraic operations, could differ from the results in MySQL [#56641](https://github.com/pingcap/tidb/issues/56641) @[windtalker](https://github.com/windtalker)
    - Fix the issue that execution plan bindings cannot be created for the multi-table `DELETE` statement with aliases [#56726](https://github.com/pingcap/tidb/issues/56726) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the optimizer does not take into account the character set and collations when simplifying complex predicates, resulting in possible execution errors [#56479](https://github.com/pingcap/tidb/issues/56479) @[dash12653](https://github.com/dash12653)
    - Fix the issue that the data in the **Stats Healthy Distribution** panel of Grafana might be incorrect [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that vector search might return incorrect results when querying tables with clustered indexes [#57627](https://github.com/pingcap/tidb/issues/57627) @[winoros](https://github.com/winoros)

+ TiKV <!--tw@Oreoxmt: 6 notes-->

    - (dup): release-7.1.6.md > Bug fixes> TiKV - Fix the panic issue that occurs when read threads access outdated indexes in the MemTable of the Raft Engine [#17383](https://github.com/tikv/tikv/issues/17383) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.5.4.md > Bug fixes> TiKV - Fix the issue that when a large number of transactions are queuing for lock release on the same key and the key is frequently updated, excessive pressure on deadlock detection might cause TiKV OOM issues [#17394](https://github.com/tikv/tikv/issues/17394) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that CPU usage for background tasks of resource control is counted twice [#17603](https://github.com/tikv/tikv/issues/17603) @[glorv](https://github.com/glorv)
    - Fix the issue that TiKV OOM might occur due to the accumulation of CDC internal tasks [#17696](https://github.com/tikv/tikv/issues/17696) @[3AceShowHand](https://github.com/3AceShowHand)
    - Fix the issue that large batch writes cause performance jitter when `raft-entry-max-size` is set too high [#17701](https://github.com/tikv/tikv/issues/17701) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix the issue that the leader could not be quickly elected after Region split [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that TiKV might panic when executing queries containing `RADIANS()` or `DEGREES()` functions [#17852](https://github.com/tikv/tikv/issues/17852) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that write jitter might occur when all hibernated Regions are awakened [#17101](https://github.com/tikv/tikv/issues/17101) @[hhwyt](https://github.com/hhwyt)

+ PD <!--tw@hfxsd: 3 notes-->

    - (dup): release-7.1.6.md > Bug fixes> PD - Fix the memory leak issue in hotspot cache [#8698](https://github.com/tikv/pd/issues/8698) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that the resource group selector does not take effect on any panel [#56572](https://github.com/pingcap/tidb/issues/56572) @[glorv](https://github.com/glorv)
    - Fix the issue that deleted resource groups still appear in the monitoring panel [#8716](https://github.com/tikv/pd/issues/8716) @[AndreMouche](https://github.com/AndreMouche)
    - Fix unclear log descriptions during the Region syncer loading process [#8717](https://github.com/tikv/pd/issues/8717) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-7.1.6.md > Bug fixes> PD - Fix the memory leak issue in label statistics [#8700](https://github.com/tikv/pd/issues/8700) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that configuring `tidb_enable_tso_follower_proxy` to `0` or `OFF` fails to disable the TSO Follower Proxy feature [#8709](https://github.com/tikv/pd/issues/8709) @[JmPotato](https://github.com/JmPotato)

+ TiFlash <!--tw@Oreoxmt: 4 notes-->

    - (dup): release-7.1.6.md > Bug fixes> TiFlash - Fix the issue that the `SUBSTRING()` function does not support the `pos` and `len` arguments for certain integer types, causing query errors [#9473](https://github.com/pingcap/tiflash/issues/9473) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that vector search performance might degrade after scaling out TiFlash write nodes in the disaggregated storage and compute architecture [#9637](https://github.com/pingcap/tiflash/issues/9637) @[kolafish](https://github.com/kolafish)
    - Fix the issue that the `SUBSTRING()` function returns incorrect results when the second parameter is negative [#9604](https://github.com/pingcap/tiflash/issues/9604) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the `REPLACE()` function returns an error when the first parameter is a constant [#9522](https://github.com/pingcap/tiflash/issues/9522) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that `LPAD()` and `RPAD()` functions return incorrect results in some cases [#9465](https://github.com/pingcap/tiflash/issues/9465) @[guo-shaoge](https://github.com/guo-shaoge)

+ Tools

    + Backup & Restore (BR) <!--tw@hfxsd: 4 notes-->

        - Fix the OOM issue during backups when there are too many uncompleted range gaps, reducing the amount of pre-allocated memory [#53529](https://github.com/pingcap/tidb/issues/53529) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that global indexes cannot be backed up [#57469](https://github.com/pingcap/tidb/issues/57469) @[Defined2014](https://github.com/Defined2014)
        - Fix the issue that logs might print out encrypted information [#57585](https://github.com/pingcap/tidb/issues/57585) @[kennytm](https://github.com/kennytm)
        - Fix the issue that the advancer cannot handle lock conflicts [#57134](https://github.com/pingcap/tidb/issues/57134) @[3pointer](https://github.com/3pointer)
        - Fix the issue that PITR tasks might fail for tables with millions of rows [#57743](https://github.com/pingcap/tidb/issues/57743) @[Tristan1900](https://github.com/Tristan1900)

    + TiCDC <!--tw@Oreoxmt: 3 notes-->

        - Fix the issue that the Kafka messages lack Key fields when using the Debezium protocol [#1799](https://github.com/pingcap/tiflow/issues/1799) @[wk989898](https://github.com/wk989898)
        - Fix the issue that the redo module fails to properly report errors [#11744](https://github.com/pingcap/tiflow/issues/11744) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC mistakenly discards DDL tasks when the schema versions of DDL tasks become non-incremental during TiDB DDL owner changes [#11714](https://github.com/pingcap/tiflow/issues/11714) @[wlwilliamx](https://github.com/wlwilliamx)

    + TiDB Lightning <!--tw@Oreoxmt: 1 note-->

        - (dup): release-7.1.6.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that TiDB Lightning fails to receive oversized messages sent from TiKV [#56114](https://github.com/pingcap/tidb/issues/56114) @[fishiu](https://github.com/fishiu)
        - Fix the issue that the `AUTO_INCREMENT` value is set too high after importing data using the physical import mode [#56814](https://github.com/pingcap/tidb/issues/56814) @[D3Hunter](https://github.com/D3Hunter)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [dash12653](https://github.com/dash12653) (First-time contributor)
- [chagelo](https://github.com/chagelo) (First-time contributor)
- [LindaSummer](https://github.com/LindaSummer)
- [songzhibin97](https://github.com/songzhibin97)
- [Hexilee](https://github.com/Hexilee)