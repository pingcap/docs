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
    <td>Global indexes can effectively improve the efficiency of retrieving non-partitioned columns, and remove the restriction that a unique key must contain the partition key. This feature extends the usage scenarios of TiDB partitioned tables, and avoids some of the application modification work required for data migration.</td>
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
    <td>Companies that use TiDB to run multi-tenant or SaaS applications often need to store a large number of tables. In TiDB v8.5.0, significant efforts have been made to enhance the stability of large-scale clusters. <a href="https://docs.pingcap.com/tidb/v8.5/schema-cache">Schema cache control</a> and <a href="https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_stats_cache_mem_quota-new-in-v610">the memory quota for the TiDB statistics cache</a> become generally available (GA). They reduce stability problems caused by excessive memory consumption. PD uses <a href="https://docs.pingcap.com/tidb/v8.5/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">Active Follower</a> to address the pressures of a large number of Regions. It also <a href="https://docs.pingcap.com/tidb/v8.5/pd-microservices">decouples the services undertaken by the PD</a> and deploys them independently. You can <a href="https://docs.pingcap.com/zh/tidb/v8.5/system-variables#tidb_auto_analyze_concurrency-new-in-v840">increase concurrency</a> and <a href="https://docs.pingcap.com/zh/tidb/v8.5/statistics#collect-statistics-on-some-columns">reduce the number of collection objects</a> to improve the efficiency of statistics collection and loading, ensuring the stability of execution plans for large clusters.</td>
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
    <li><a href="https://docs.pingcap.com/tidb/v8.5/tiproxy-overview">	Built-in virtual IP management in TiProxy</a> (introduced in v8.3.0)</li>
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
    <td>Foreign keys are constraints in a database that establish relationships between tables, ensuring data consistency and integrity. They restrict the data referenced in a child table to exist in the parent table, preventing the insertion of invalid data. Foreign keys also support cascading operations (such as automatic synchronization during deletion or update), simplifying business logic implementation and reducing the complexity of manually maintaining data relationships.</td>
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

* The schema cache memory limit feature is now generally available (GA), reducing memory usage in scenarios with hundreds of thousands or even millions of databases or tables. [#50959](https://github.com/pingcap/tidb/issues/50959) @[tiancaiamao](https://github.com/tiancaiamao) @[wjhuang2016](https://github.com/wjhuang2016) @[gmhdbjd](https://github.com/gmhdbjd) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--1976-->

    In some SaaS scenarios, when the number of tables reaches hundreds of thousands or even millions, the schema meta can consume significant memory. Enabling this feature allows TiDB to use the LRU algorithm to cache and evict the corresponding schema meta information, effectively reducing memory usage. 
    
    Starting from v8.4.0, this feature is enabled by default with a default value of `536870912` (that is, 512 MiB). You can adjust it as needed through the variable [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800).

    For more information, see [documentation](/schema-cache.md).

* Use the Active PD Follower feature to enhance the scalability of PD's Region information query service (GA) [#7431](https://github.com/tikv/pd/issues/7431) @[okJiang](https://github.com/okJiang) tw@Oreoxmt <!--2015-->

    In a TiDB cluster with a large number of Regions, the PD leader might experience high CPU load due to the increased overhead of handling heartbeats and scheduling tasks. If the cluster has many TiDB instances, and there is a high concurrency of requests for Region information, the CPU pressure on the PD leader increases further and might cause PD services to become unavailable.

    To ensure high availability, TiDB v7.6.0 introduces Active PD Follower as an experimental feature to enhance the scalability of PD's Region information query service. In v8.5.0, this feature becomes generally available (GA). You can enable the Active PD Follower feature by setting the system variable [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) to `ON`. After this feature is enabled, TiDB evenly distributes Region information requests to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader.

    For more information, see [documentation](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service).

### Performance

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

* TiDB accelerated table creation becomes generally available (GA), significantly reducing data migration and cluster initialization time [#50052](https://github.com/pingcap/tidb/issues/50052) @[D3Hunter](https://github.com/D3Hunter) @[gmhdbjd](https://github.com/gmhdbjd) tw@Oreoxmt <!--1977-->

    TiDB v7.6.0 introduces accelerated table creation as an experimental feature, controlled by the system variable [`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760). Staring from v8.0.0, this system variable is renamed to [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800).

    In v8.5.0, TiDB accelerated table creation becomes generally available (GA) and is enabled by default. During data migration and cluster initialization, this feature supports rapid creation of millions of tables, significantly reducing operation time.

    For more information, see [Documentation](/accelerated-table-creation.md).

* TiKV supports MVCC In-memory Engine (IME). It can accelerate queries that require scanning of a large number of MVCC historical versions. [#16141](https://github.com/tikv/tikv/issues/16141) [@SpadeA-Tang](https://github.com/SpadeA-Tang) [@glorv](https://github.com/glorv) [@overvenus](https://github.com/overvenus)

    In scenarios where records are updated frequently or TiDB is required to retain historical versions for a long period of time (for example, 24 hours), a buildup of MVCC versions can lead to degradation of scanning performance. TiKV MVCC In-memory Engine improves scanning performance by caching the most recent MVCC versions in memory and deleting the historical versions from memory through a fast GC mechanism.

    Starting from v8.5.0, TiKV introduces MVCC In-memory Engine. When scanning performance is degraded due to the buildup of MVCC versions in a TiKV cluster, you can enable the TiKV MVCC memory engine to improve scanning performance by setting the TiKV configuration parameter [`in-memory-engine.enable`](/tikv-in-memory-engine.md#usage).

    For more information, see [documentation](/tikv-in-memory-engine.md).
### Reliability

* Support limiting the maximum rate and concurrency of requests processed by PD [#5739](https://github.com/tikv/pd/issues/5739) @[rleungx](https://github.com/rleungx) **tw@qiancai** <!--2018-->

    When a sudden influx of requests is sent to PD, it can lead to high workloads and potentially affect PD performance. Starting from v8.5.0, you can use [`pd-ctl`](/pd-control.md) to limit the maximum rate and concurrency of requests processed by PD, improving its stability.

    For more information, see [documentation](/pd-control.md).

### Availability

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### SQL

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

* Support foreign keys (GA) [#36982](https://github.com/pingcap/tidb/issues/36982) @[YangKeao](https://github.com/YangKeao) @[crazycs520](https://github.com/crazycs520) tw@lilin90 <!--1894-->

    The foreign key feature becomes generally available (GA) in v8.5.0. Foreign key constraints help ensure data consistency and integrity. You can easily establish foreign key relationships between tables, with support for cascading updates and deletions, simplifying data management. This feature enhances support for applications with complex data relationships.

    For more information, see [Documentation](/foreign-key.md).

* Introduce the `ADMIN ALTER DDL JOBS` statement to support modifying the DDL jobs online [#57229](https://github.com/pingcap/tidb/issues/57229) @[fzzf678](https://github.com/fzzf678) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--2016--> 

    Starting from v8.3.0, you can set the variables [`tidb_ddl_reorg_batch_size`](/system-variables#tidb_ddl_reorg_batch_size) and [`tidb_ddl_reorg_worker_cnt`](/system-variables#tidb_ddl_reorg_worker_cnt) at the session level. As a result, setting these two variables globally no longer affects all running DDL jobs. To modify the values of these variables, you need to cancel the DDL job first, adjust the variables, and then resubmit the job.

    TiDB v8.5.0 introduces the `ADMIN ALTER DDL JOBS` statement, allowing online adjustment of variable values for specific DDL jobs. This enables flexible balancing of resource consumption and performance, with changes limited to an individual job, making the impact more controllable. For example:

    - `ADMIN ALTER DDL JOBS job_id THREAD = 8;`: adjusts the `tidb_ddl_reorg_worker_cnt` for the specified DDL task.
    - `ADMIN ALTER DDL JOBS job_id BATCH_SIZE = 256;`: adjusts the `tidb_ddl_reorg_batch_size` for the specified DDL task.
    - `ADMIN ALTER DDL JOBS job_id MAX_WRITE_SPEED = '200MiB';`: adjusts the write traffic size for index data on each TiKV node.

  For more information, see [documentation](/sql-statements/sql-statement-admin-alter-ddl.md).

### DB operations

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Observability

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

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

### Data migration

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.1.0 to the current version (v8.2.0). If you are upgrading from v8.0.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

### MySQL compatibility

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
|tidb_ddl_reorg_max_write_speed  | Newly added |Used to control the speed at which TiDB writes index data to a single TiKV node. For example, setting the value to 200 MiB limits the maximum write speed to 200 MiB/s.  |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that the [accelerated table creation](/accelerated-table-creation.md) feature is enabled by default. |
|  |  |  |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV | [`raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size) | Modified | Changes the default value from `8192` to `16384`. |
|  |  |  |  |
|  |  |  |  |

### System tables

### Other changes

## Offline package changes

## Removed features

## Deprecated features

The following features are planned for deprecation in future versions:

* TiDB introduces the system variable [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800), which controls whether priority queues are enabled to optimize the ordering of tasks that automatically collect statistics. In future releases, the priority queue will be the only way to order tasks for automatically collecting statistics, so this system variable will be deprecated.
* TiDB introduces the system variable [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) in v7.5.0. You can use it to set TiDB to use asynchronous merging of partition statistics to avoid OOM issues. In future releases, partition statistics will be merged asynchronously, so this system variable will be deprecated.
* It is planned to redesign [the automatic evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.
* In v8.0.0, TiDB introduces the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable to control whether TiDB supports disk spill for the concurrent HashAgg algorithm. In future versions, the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable will be deprecated.
* In v5.1, TiDB introduces the system variable [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) to set whether to enable the dynamic pruning mode for partitioned tables. Starting from v8.5.0, a warning is returned when you set this variable to `static` or `static-only`. In future versions, this system variable will be deprecated.
* The TiDB Lightning parameter [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is planned for deprecation in a future release and will be subsequently removed. This parameter will be replaced by [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task), which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.
* Starting from v6.3.0, partitioned tables use [dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) by default. Compared with static pruning mode, dynamic pruning mode supports features such as IndexJoin and plan cache with better performance. Therefore, static pruning mode will be deprecated.

## Improvements

+ TiDB

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Lightning

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiUP

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

## Bug fixes

+ TiDB

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Lightning

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiUP

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [Contributor-GitHub-ID](id-link)
