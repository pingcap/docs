---
title: TiDB 8.0.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.0.0.
---

# TiDB 8.0.0 Release Notes

Release date: xx xx, 2024

TiDB version: 8.0.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.0/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v8.0.0#version-list)

8.0.0 introduces the following key features and improvements:

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
    <td rowspan="4">Scalability and Performance</td>
    <td>Disaggregation of PD to improve scale (experimental) **tw@qiancai** <!--1553, 1558--></td>
    <td>PD (Placement Driver) has a lot of critical modules for the running of TiDB. Each module's resource consumption can increase as certain workloads scale, meaning they can each interfere with other functions in PD, ultimately impacting quality of service of the cluster. By separating PD modules into separately-deployable services, their blast radii are massively mitigated as the cluster scales. Much larger clusters with much larger workloads are possible with this architecture.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.0/system-variables#tidb_dml_type-new-in-v800">Bulk DML for much larger transactions (experimental)</a>**tw@Oreoxmt** <!--1694--></td>
    <td>Large batch DML jobs, such as extensive cleanup jobs, joins, or aggregations, can consume a significant amount of memory and have previously been limited at very large scales. Bulk DML (<code>tidb_dml_type = "bulk"</code>) is a new DML type for handling large batch DML tasks more efficiently while providing transaction guarantees and mitigating OOM issues. This feature differs from import, load, and restore operations when used for data loading.</td>
  </tr>
  <tr>
    <td>Acceleration of cluster snapshot restore speed **tw@qiancai** <!--1681--></td>
    <td>An optimization to involve all TiKV nodes in the preparation step for cluster restores was introduced to leverage scale such that restore speeds for a cluster are much faster for larger sets of data on larger clusters. Real world tests exhibit restore acceleration of ~300% in slower cases.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.0/system-variables#tidb_schema_cache_size-new-in-v800">Enhance stability of caching the schema information when there are a massive number of tables (experimental)</a>**tw@hfxsd** <!--1691--></td>
    <td>SaaS companies using TiDB as the system of record for their multi-tenant applications often need to store a substantial number of tables. In previous versions, handling table counts in the order of a million or more was feasible, but it had the potential to degrade the overall user experience. TiDB v8.0.0 improves the situation with the following enhancements:
  <ul>
    <li>- Introduce a new <a href="https://docs.pingcap.com/tidb/v8.0/system-variables#tidb_schema_cache_size-new-in-v800">schema information caching system</a>, incorporating a lazy-loading Least Recently Used (LRU) cache for table metadata and more efficiently managing schema version changes.</li>
    <li>- Implement a <a href="https://docs.pingcap.com/tidb/v8.0/system-variables#tidb_enable_auto_analyze_priority_queue-new-in-v800">priority queue</a> for <code>auto analyze</code>, making the process less rigid and enhancing stability across a wider array of tables.</li>
  </ul>
    </td>
  </tr>
  <tr>
    <td rowspan="1">DB Operations and Observability</td>
    <td>Support monitoring index usage statistics **tw@Oreoxmt** <!--1400--></td>
    <td>TiDB v8.0.0 introduces the <a href="https://docs.pingcap.com/tidb/v8.0/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a> table and the <a href="https://docs.pingcap.com/tidb/v8.0/sys-schema.md"><code>sys.schema_unused_index</code></a> view to provide usage statistics of indexes. This feature helps you assess the importance of all indexes and optimize the index design.</td>
    </td>
  </tr>
  <tr>
    <td rowspan="3">Data Migration</td>
    <td><a href="https://docs.pingcap.com/tidb/v8.0/ticdc-bidirectional-replication">TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (GA) </a>**tw@hfxsd** <!--1682/1689--></td>
    <td>With this feature, TiCDC allows for a cluster to be assigned the <code>PRIMARY</code> BDR role, and enables the replication of DDL statements from that cluster to the downstream cluster.</td>
    </td>
  </tr>
  <tr>
    <td>TiCDC adds support for the Simple protocol **tw@lilin90** <!--1646--></td>
    <td>TiCDC introduces support for a new protocol, the Simple protocol. This protocol includes support for in-band schema tracking capabilities.</td>
  </tr>
  <tr>
    <td>TiCDC adds support for the Debezium format protocol **tw@lilin90** <!--1652--></td>
    <td>TiCDC can now publish replication events to a Kafka sink using a protocol that generates Debezium style messages.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

- PD supports the microservice mode [#5766](https://github.com/tikv/pd/issues/5766) @[binshi-bing](https://github.com/binshi-bing) **tw@qiancai** <!--1553/1558-->

    Starting from v8.0.0, PD supports the microservice mode. This mode disaggregates the timestamp allocation and cluster scheduling functions of PD into separate microservices that can be deployed independently, thereby achieving performance scalability for PD and addressing performance bottlenecks of PD in large-scale clusters.

    - TSO microservice: provides monotonically increasing timestamp allocation for the entire cluster.
    - Scheduling microservice: provides scheduling functions for the entire cluster, including but not limited to load balancing, hot spot handling, replica repair, and replica placement.

    Each microservice is deployed as an independent process. If you configure more than one replica for a microservice, the microservice automatically implements a primary-secondary fault-tolerant mode to ensure high availability and reliability of the service.

    Currently, PD microservices can only be deployed by TiDB Operator. It is recommended to consider using this mode when PD encounters significant performance bottlenecks that cannot be resolved by scaling up.

    For more information, see [documentation](https://docs.pingcap.com/tidb-in-kubernetes/dev/pd-microservices).

* Enhance the usability of the Titan engine [#16245](https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996) **tw@qiancai** <!--1708-->

    - Enable the shared cache for Titan blob files and RocksDB block files by default ([`shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-tidb-introduced-in-v800) defaults to `true`), eliminating the need to configure [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size) separately.
    - Support dynamically modifying [`min-blob-size`](/tikv-configuration-file.md#min-blob-size), [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression), and [`discardable-ratio`](/tikv-configuration-file.md#min-blob-size) to improve performance and flexibility when using the Titan engine.

    For more information, see [documentation](/storage-engine/titan-configuration.md).

### Performance

* BR improves snapshot restore speed by up to 10 times (GA) [#50701](https://github.com/pingcap/tidb/issues/50701) @[3pointer](https://github.com/3pointer) @[Leavrth](https://github.com/Leavrth) **tw@qiancai** <!--1681-->

  Starting from TiDB v8.0.0, the improvement in snapshot restore speed has been generally available (GA) and enabled by default. By implementing various optimizations such as adopting the coarse-grained region scattering algorithm, creating databases and tables in batches, reducing the mutual impact between SST file downloads and ingest operations, and accelerating the restore of table statistics, BR improves snapshot restore speed by up to approximately 10 times while ensuring that the data is sufficiently distributed. This feature fully utilizes all resources of each TiKV node, achieving parallel and rapid restore. According to test results from real-world cases, the data restore speed of a single TiKV node remains stable at 1.2 GB/s, enabling the restore of 100 TB of data within 1 hour.

  This means that even in high-load environments, BR can fully utilize the resources of each TiKV node, significantly reducing database restore time, enhancing the availability and reliability of the database, and reducing downtime and business losses caused by data loss or system failures.

  For more information, see [documentation](/br/br-snapshot-guide.md#restore-cluster-snapshots).

* Support pushing down the following functions to TiFlash [#50975](https://github.com/pingcap/tidb/issues/50975) [#50485](https://github.com/pingcap/tidb/issues/50485) @[yibin87](https://github.com/yibin87) @[windtalker](https://github.com/windtalker) **tw@Oreoxmt** <!--1662--><!--1664-->

    * `CAST(DECIMAL AS DOUBLE)`
    * `POWER()`

  For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* The concurrent HashAgg algorithm of TiDB supports disk spill (experimental) [#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1365-->

    In earlier versions of TiDB, the concurrency algorithm of the HashAgg operator does not support disk spill. If the execution plan of a SQL statement contains the concurrent HashAgg operator, all the data for that SQL statement can only be processed in memory. Consequently, TiDB has to process a large amount of data in memory. When the data size exceeds the memory limit, TiDB can only choose the non-concurrent algorithm, which does not leverage concurrency for performance improvement.

     In v8.0.0, the concurrent HashAgg algorithm of TiDB supports disk spill. Under any concurrent conditions, the HashAgg operator can automatically trigger data spill based on memory usage, thus balancing performance and data throughput. Currently, as an experimental feature, TiDB introduces the `tidb_enable_concurrent_hashagg_spill` variable to control whether to enable the concurrent HashAgg algorithm that supports disk spill. When this variable is `ON`, it means enabled. This variable will be deprecated when the feature is generally available in a future release.

    For more information, see [documentation](/system-variables.md#tidb_enable_concurrent_hashagg_spill-new-in-v760).

* Introduce priority queues for automatic statistics update [#50132](https://github.com/pingcap/tidb/issues/50132) @[hi-rustin](https://github.com/hi-rustin) **tw@hfxsd** <!--1640-->

    Maintaining the up-to-date nature of optimizer statistics is critical to stabilizing database performance. Most users rely on the [automatic statistics update](/statistics.md#automatic-update) provided by TiDB to keep statistics up-to-date. Automatic statistics update polls the status of statistics for all objects, and adds objects with insufficient health to a queue that is collected and updated one by one. In previous versions, the collection order is set randomly, which can result in longer waits for more worthy objects to be updated, causing potential database performance rollbacks.

    Starting from v8.0.0, automatic statistics update dynamically sets priorities for objects in combination with a variety of conditions to ensure that more valuable objects for collection are processed first, such as newly created indexes and partitioned tables with partition changes. Less healthy objects tend to be placed at the front of the queue. This enhancement improves the reasonableness of the collection order, and reduces performance problems caused by outdated statistics, therefore improving database stability.
    
    For more information, see [documentation](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800).

* Remove some limitations on execution plan cache [#49161](https://github.com/pingcap/tidb/pull/49161) @[mjonss](https://github.com/mjonss) @[qw4990](https://github.com/qw4990) **tw@hfxsd** <!--1622/1585-->

    TiDB supports [execution plan cache](/sql-prepared-plan-cache.md), which can effectively reduce the processing latency of the transaction-intensive system and provides an important means to improve performance. In v8.0.0, TiDB removes several restrictions on execution plan cache. Execution plans with the following contents can be cached:

    - [Partitioned tables](/partitioned-table.md)
    - [Generated columns](/generated-columns.md), including objects that depend on the generated columns (such as [multi-valued indexes](/choose-index.md))

  This enhancement extends the usage scenarios of execution plan cache and improves the overall performance of the database in complex scenarios.

    For more information, see [documentation](/sql-prepared-plan-cache.md).

* The optimizer enhances support for multi-valued indexes [#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx) @[time-and-fate](https://github.com/time-and-fate) **tw@hfxsd** <!--1405/1584-->

    TiDB introduced [multi-value indexes](/sql-statements/sql-statement-create-index.md#multi-valued-indexes) in in v6.6.0 to improve query performance for JSON data types. In v8.0.0, the optimizer enhances its support for multi-valued indexes and can correctly identify and utilize them to optimize queries in complex scenarios.

    * Statistics on multi-valued indexes are collected and applied by the optimizer for estimation. When a SQL statement might select multiple multi-valued indexes, the optimizer can identify the index with lower cost.
    * When there are multiple `member of` conditions connected by `OR`, the optimizer is able to match an effective index partial path for each DNF item (a `member of` condition) and combine multiple paths using Union to form an `Index Merge`. This allows more efficient condition filtering and data querying.

  For more information, see [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-indexes).
  
  * Supports configuring the update interval for low-precision TSO [#51081](https://github.com/pingcap/tidb/issues/51081) @[Tema](https://github.com/Tema) **tw@hfxsd** <!--1725-->

    The TiDB [low-precision TSO feature](/system-variables.md#tidb_low_resolution_tso) uses regularly updated TSO as transaction timestamps. Although this feature sacrifices real-time performance while tolerating reading old data, it reduces the overhead of obtaining TSO for small read-only transactions and improves the ability of high-concurrency reads.

    Before v8.0.0, the TSO update interval of low-precision TSO feature is fixed and cannot be adjusted according to actual business needs. In v8.0.0, TiDB introduces the system variable `tidb_low_resolution_tso_update_interval` to control the TSO update interval. This feature is valid only when the low-precision TSO feature is enabled.

    For more information, see [documentation](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800).

### Reliability

* Support caching required schema information according to the Least Recently Used (LRU) algorithm to reduce memory consumption on the TiDB server (experimental) [#50959](https://github.com/pingcap/tidb/issues/50959) @[gmhdbjd](https://github.com/gmhdbjd) **tw@hfxsd** <!--1691-->

    Before v8.0.0, each TiDB node caches the schema information of all tables. Once the number of tables is large, for example, in a scenario that involves hundreds of thousands of tables, caching the schema information of these tables alone will take up a lot of memory. 
    
    Starting from v8.0.0, the system variable [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800) is introduced, which allows you to set an upper limit on the amount of memory that can be used for caching the schema information, so that it does not take up too much memory. When you enable this feature, TiDB uses the LRU algorithm to cache the required tables, effectively reducing the memory consumed by the schema information.

    For more information, see [documentation](/system-variables.md#tidb_schema_cache_size-new-in-v800).

### Availability

* The proxy component TiProxy becomes generally available (GA) [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox) **tw@Oreoxmt** <!--1698-->

    TiDB v7.6.0 introduces the proxy component TiProxy as an experimental feature. TiProxy is the official proxy component of TiDB, located between the client and TiDB server. It provides load balancing and connection persistence functions for TiDB, making the workload of the TiDB cluster more balanced and not affecting user access to the database during maintenance operations.
    
    In v8.0.0, TiProxy becomes generally available and enhances the automatic generation of signature certificates and monitoring functions.

    The usage scenarios of TiProxy are as follows:

    - During maintenance operations such as rolling restarts, rolling upgrades, and scaling-in in a TiDB cluster, changes occur in the TiDB servers which result in interruptions in connections between clients and the TiDB servers. By using TiProxy, connections can be smoothly migrated to other TiDB servers during these maintenance operations so that clients are not affected.
    - Client connections to a TiDB server cannot be dynamically migrated to other TiDB servers. When the workload of multiple TiDB servers is unbalanced, it might result in a situation where the overall cluster resources are sufficient, but certain TiDB servers experience resource exhaustion leading to a significant increase in latency. To address this issue, TiProxy provides dynamic migration for connection, which allows connections to be migrated from one TiDB server to another without any impact on the clients, thereby achieving load balancing for the TiDB cluster.

  TiProxy has been integrated into TiUP, TiDB Operator, and TiDB Dashboard, making it easy to configure, deploy and maintain.

    For more information, see [documentation](/tiproxy/tiproxy-overview.md).

### SQL

* Support a new DML type for handling a large amount of data (experimental) [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium) **tw@Oreoxmt** <!--1694-->

    Before v8.0.0, TiDB stores all transaction data in memory before committing. When processing a large amount of data, the memory required for transactions becomes a bottleneck that limits the transaction size that TiDB can handle. Although TiDB introduces non-transactional DML to attempt to solve the transaction size limitation by splitting SQL statements, this feature has various limitations and does not provide an ideal experience in actual scenarios.

    Starting from v8.0.0, TiDB supports a DML type for handling a large amount of data. This DML type writes data to TiKV in a timely manner during execution, avoiding the continuous storage of all transaction data in memory, and thus supports handling a large amount of data that exceeds the memory limit. This DML type ensures transaction integrity and uses the same syntax as standard DML. `INSERT`, `UPDATE`, `REPLACE`, and `DELETE` statements can use this new DML type to execute large-scale DML operations.

    This DML type is implemented by the [Pipelined DML](https://github.com/pingcap/tidb/blob/master/docs/design/2024-01-09-pipelined-DML.md) feature and only takes effect on statements with auto-commit enabled. You can control whether to enable this DML type by setting the system variable [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800).

    For more information, see [documentation](/system-variables.md#tidb_dml_type-new-in-v800).

* Support using some expressions to set the default values for columns when a table is created (experimental) [#50936](https://github.com/pingcap/tidb/issues/50936) @[zimulala](https://github.com/zimulala) **tw@hfxsd** <!--1690-->

    Before v8.0.0, when you create a table, the default values of columns can only be fixed strings, numbers, and dates. Starting from v8.0.0, you can use some expressions as the default values of columns, such as setting the default value of columns to `UUID()`. This feature helps you meet your diverse requirements.
    
    For more information, see [documentation](/data-type-default-values.md#specify-expressions-as-default-values).

* Support the `div_precision_increment` system variable [#51501](https://github.com/pingcap/tidb/issues/51501) @[yibin87](https://github.com/yibin87) **tw@hfxsd** <!--1566-->

    MySQL 8.0 supports the variable `div_precision_increment`, which specifies the number of digits by which to increase the scale of the result of a division operation performed using the `/` operator. Before v8.0.0, TiDB does not support this variable, and division is performed to 4 decimal places. Starting with v8.0.0, TiDB supports this variable. You can specify the number of digits by which to increase the scale of the result of a division operation as desired.
    
    For more information, see [documentation](/system-variables.md#div_precision_increment-new-in-v800).
   
### DB operations

* PITR supports Amazon S3 Object Lock [#51184](https://github.com/pingcap/tidb/issues/51184) @[RidRisR](https://github.com/RidRisR) **tw@lilin90** <!--1604-->

    Amazon S3 Object Lock can help prevent backup data from being accidentally or intentionally deleted during a specified retention period, enhancing the security and integrity of data. Starting from v6.3.0, BR supports Amazon S3 Object Lock in snapshot backups, adding an additional layer of security for full backups. Starting from v8.0.0, PITR also supports Amazon S3 Object Lock. Whether full backups or log data backups, the Object Lock feature ensures a more reliable data protection, further strengthening the security of data backup and recovery and meeting regulatory requirements.

    For more information, see [documentation](/br/backup-and-restore-storages.md#other-features-supported-by-the-storage-service).

* Support making invisible indexes visible at the session level [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1401-->

    By default, the optimizer does not select [invisible indexes](/sql-statements/sql-statement-create-index.md#invisible-index) to optimize query execution. This mechanism is usually used to evaluate whether to delete an index. If there is uncertainty about the potential performance impact of deleting an index, you have the option to set the index to invisible temporarily and promptly restore it to visible when needed.

    Starting from v8.0.0, you can set the session-level system variable [`tidb_opt_use_invisible_indexes`](/system-variables.md#) to `ON` to make the current session recognize and use invisible indexes. With this feature, you can create a new index and test its performance by setting the index to invisible first, and then modifying the system variable in the current session for testing without affecting other sessions. This improvement enhances the safety of performance tuning and helps to improve the stability of production databases.

    For more information, see [documentation](/sql-statements/sql-statement-create-index.md#invisible-index).

* Support writing general logs to a separate file [#51248](https://github.com/pingcap/tidb/issues/51248) @[Defined2014](https://github.com/Defined2014) **tw@hfxsd** <!--1632-->

    The general log is a MySQL-compatible feature. When you enable it, it logs all SQL statements executed by the database to help you diagnose problems. TiDB also supports this feature. You can enable it by setting the variable [`tidb_general_log`](/system-variables.md#tidb_general_log). However, in previous versions, the content of general logs can only be written to the TiDB instance log together with other information, which is not friendly to keep it for a long time.

    Starting from v8.0.0, you can enable TiDB to write the general log to a specified file by setting the configuration item [`log.general-log-file`](/tidb-configuration-file.md#general-log-file) to a valid filename. The general log also conforms to the same polling and saving policies for instance logs.

    In addition, to reduce the amount of disk space taken up by history log files, TiDB supports a native log compression option in v8.0.0. You can set the configuration item [`log.file.compression`](/tidb-configuration-file.md#compression) to `gzip`, and the polled history logs will be automatically compressed in [`gzip`](https://www.gzip.org/) format.

    For more information, see [documentation](/tidb-configuration-file.md#general-log-file).

### Observability

* Support monitoring index usage statistics [#49830](https://github.com/pingcap/tidb/issues/49830) @[YangKeao](https://github.com/YangKeao) **tw@Oreoxmt** <!--1400-->

    Proper index design is a crucial prerequisite for improving database performance. TiDB v8.0.0 introduces the [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) table, which records usage statistics of all indexes on the current TiDB node, including the following information:

    * The cumulative execution count of statements that scan the index
    * The total number of rows scanned when accessing the index
    * The selectivity distribution when scanning the index
    * The time of the most recent access to the index

  With this information, you can identify indexes that are not used by the optimizer and indexes with poor filtering effects, thereby optimizing index design to improve database performance.
  
    Additionally, TiDB v8.0.0 introduces a view [`sys.schema_unused_index`](/sys-schema.md), which is compatible with MySQL. This view records indexes that have not been used since the last start of TiDB. For clusters upgraded from versions earlier than v8.0.0, the `sys` schema and the views in it are not created automatically. You can manually create them by referring to [`sys`](/sys-schema.md).

    For more information, see [documentation](/information-schema/information-schema-tidb-index-usage.md).

### Security

* TiKV encryption at rest supports Google [Key Management Service (Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive?hl) [#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv) **tw@qiancai** <!--1612-->

    TiKV ensures data security through encryption at rest mechanisms. The core of encryption at rest for security lies in key management. Starting from v8.0.0, you can manage the master key of TiKV using Google Cloud KMS to establish encryption-at-rest capabilities based on Cloud KMS, thereby enhancing the security of user data.

    To enable encryption at rest based on Google Cloud KMS, you need to create a key on Google Cloud and then configure the `[security.encryption.master-key]` section in the TiKV configuration file.

    For more information, see [documentation](/encryption-at-rest.md##tikv-encryption-at-rest).

* TiDB 日志脱敏增强 [#51306](https://github.com/pingcap/tidb/issues/51306) @[xhebox](https://github.com/xhebox) **tw@hfxsd** <!--1229-->

    TiDB 日志脱敏增强是基于对日志文件中 SQL 文本信息的数据进行标记，以便支持用户在查看时进行敏感数据的安全展示。用户可以更灵活自主地在展示环节控制是否对日志信息进行脱敏，以支持 TiDB 日志在不同场景下的安全使用，提升了客户使用日志脱敏能力的安全性和灵活性。要使用此功能请通过修改系统变量 `tidb_redact_log` 的值设置为 `marker`，此时 TiDB 的运行日志将对 SQL 文本进行标记，查看时将基于标记进行数据的安全展示，从而实现日志信息的保护。

    更多信息，请参考[用户文档](链接)。

### Data migration

* TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (GA) [#10301](https://github.com/pingcap/tiflow/issues/10301) @[asddongmen](https://github.com/asddongmen) **tw@hfxsd** <!--1689/1682-->

    TiDB v7.6.0 introduces replicating DDL statements in BDR mode as an experimental feature. Previously, replicating DDL statements was not supported by TiCDC, so users of TiCDC bi-directional replication had to apply DDL statements to both TiDB clusters separately. With this feature, TiCDC allows for a cluster to be assigned the `PRIMARY` BDR role, and enables the replication of DDL statements from that cluster to the downstream cluster. In v8.0.0, this feature becomes GA.

    For more information, see [documentation](/ticdc/ticdc-bidirectional-replication.md).

* TiCDC adds support for the Simple protocol [#9898](https://github.com/pingcap/tiflow/issues/9898) @[3AceShowHand](https://github.com/3AceShowHand) **tw@lilin90** <!--1646-->

    TiCDC introduces support for a new protocol, the Simple protocol. This protocol includes support for in-band schema tracking capabilities.

    For more information, see [documentation](/ticdc/ticdc-simple-protocol.md).

* TiCDC adds support for the Debezium format protocol [#1799](https://github.com/pingcap/tiflow/issues/1799) @[breezewish](https://github.com/breezewish) **tw@lilin90** <!--1652-->

    TiCDC can now publish replication events to a Kafka sink using a protocol that generates event messages in a Debezium style format. This helps to simplify the migration from MySQL to TiDB for users who are currently using Debezium to pull data from MySQL for downstream processing.

    For more information, see [documentation](/ticdc/ticdc-debezium.md).

* DM 支持使用用户提供的密钥对源数据库和目标数据库的密码进行加密和解密 [#9492](https://github.com/pingcap/tiflow/issues/9492) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1497-->

    在之前的版本中，DM 使用了一个内置的一个固定秘钥，安全性相对较低。从 v8.0.0 开始，你可以上传并指定一个密钥文件，用于对上下游数据库的密码进行加密和解密操作。此外，你还可以按需替换秘钥文件，以提升数据的安全性。

    更多信息，请参考[用户文档](dm/dm-customized-secret-key.md)。

* 支持 `IMPORT INTO ... FROM SELECT` 语法，增强 `IMPORT INTO` 功能（实验特性） [#49883](https://github.com/pingcap/tidb/issues/49883) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1680-->

    在之前的 TiDB 版本中，将查询结果导入目标表只能通过 `INSERT INTO ... SELECT` 语句，但该语句在一些大数据量的场景中的导入效率较低。从 v8.0.0 开始，TiDB 新增支持通过 `IMPORT INTO ... FROM SELECT` 将 `SELECT` 的查询结果导入到一张空的 TiDB 目标表中，其性能最高可达 `INSERT INTO ... SELECT` 的 8 倍，可以大幅缩短导入所需的时间。

    此外，你还可以通过 `IMPORT INTO ... FROM SELECT` 导入使用 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 查询的历史数据。

    更多信息，请参考[用户文档](sql-statements/sql-statement-import-into.md)。

* TiDB Lightning 冲突策略简化，同时支持 Replace 的方式处理冲突的数据（实验特性） [#51036](https://github.com/pingcap/tidb/issues/51036) @[lyzx2001](https://github.com/lyzx2001) **tw@qiancai** <!--1684-->

    原先 TiDB Lightning 逻辑导入模式时有一套冲突处理策略，物理导入模式时也有一套冲突策略，同时物理导入模式还有一套前置冲突策略，导致配置复杂。从 v8.0.0 开始，将这三种冲突策略合并成了一套，简化了配置操作。同时在物理导入模式下，还首次引入了通过 `replace` 的方式处理导入过程中冲突的数据，遇到主键或唯一键冲突的数据时，保留最新的数据、覆盖旧的数据。最新数据的定义取决于 TiDB Lightning 内部机制。

    更多信息，请参考[用户文档](链接)。

* 全局排序成为正式功能 (GA)，可显著提升 `IMPORT INTO` 任务的导入性能和稳定性，支持 40 TiB 的数据导入 [#45719](https://github.com/pingcap/tidb/issues/45719) @[lance6716](https://github.com/lance6716) **tw@qiancai** <!--1580-->

    在 v7.4.0 以前，当使用[分布式执行框架](/tidb-distributed-execution-framework.md) 执行 `IMPORT INTO` 任务时，由于本地存储空间有限，TiDB 只能对部分数据进行局部排序后再导入到 TiKV。这导致了导入到 TiKV 的数据存在较多的重叠，需要 TiKV 在导入过程中执行额外的 compaction 操作，影响了 TiKV 的性能和稳定性。

    随着 v7.4.0 引入全局排序实验特性，TiDB 支持将需要导入的数据暂时存储在外部存储（如 Amazon S3）中进行全局排序后再导入到 TiKV 中，使 TiKV 无需在导入过程中执行 compaction 操作。全局排序在 v8.0.0 成为正式功能 (GA)，可以降低 TiKV 对资源的额外消耗，显著提升 `IMPORT INTO` 的性能和稳定性。

    更多信息，请参考[用户文档](/tidb-global-sort.md)。

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.6.0 to the current version (v8.0.0). If you are upgrading from v7.5.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

* When you enable `tidb_ddl_enable_fast_reorg` for index acceleration, the encoded index key ingests data to TiKV with fixed concurrency (`16`), which cannot be dynamically adjusted according to the downstream TiKV capacity. Starting from v8.0.0, you can adjust concurrency using the [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt-new-in-v800) system variable. The default value is `4`. Compared with the previous default value of `16`, the new default value reduces performance when ingesting indexed key-value pairs. You can adjust this system variable based on the workload of the cluster. **tw@hfxsd** <!--no FD-->

### MySQL compatibility 

* The `KEY` partition type supports statements with empty list of partition fields, which is consistent with the behavior of MySQL. **tw@hfxsd** <!--No FD-->

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) | Deprecated | Starting from v8.0.0, this system variable is deprecated, and TiDB no longer supports automatic retries of optimistic transactions. It is recommended to use the [Pessimistic transaction mode](/pessimistic-transaction.md). If you encounter optimistic transaction conflicts, you can capture the error and retry transactions in your application. |
| `tidb_ddl_version` | Renamed | Controls whether to enable TiDB DDL V2. Starting from v8.0.0, this variable is renamed to [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800). |
| [`initial-scan-rate-limit`](/system-variables.md#initial-scan-rate-limit-new-in-v620) | Modified | Add a limit of `1MiB` as the minimum value. |
| [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) | Modified | Adds a control to whether to record the [usage statistics of indexes](/information-schema/information-schema-tidb-index-usage.md). The default value is `ON`. |
| [`tidb_redact_log`](/system-variables.md#tidb_redact_log) | Modified | Controls how to handle user information in SAL text when logging TiDB logs and slow logs. Values can be `OFF` and `ON`, to support log information in plain text, and masking log information, respectively. To provide a richer way of processing user information in the log, the `MARKER` option is added in v8.0.0 to support marking log information. When you set the variable to `MARKER`, the user information in the log will be marked for processing, and you can decide later whether to desensitize the log information. |
| [`div_precision_increment`](/system-variables.md#div_precision_increment-new-in-v800) | Newly added | Controls the number of decimal places in the result of a division operation `/` performed using the operator. |
| [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) | Newly added | Controls the execution mode of DML statements. The value options are `"standard"` and `"bulk"`. |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) | Newly added | Control whether to enable the priority queue to schedule the tasks of automatically collecting statistics. When this variable is enabled, TiDB prioritizes collecting statistics for the tables that most need statistics. |
| [`tidb_enable_concurrent_hashagg_spill`](/system-variables.md#tidb_enable_concurrent_hashagg_spill-new-in-v800) | Newly added | Controls whether TiDB supports disk spill for the concurrent HashAgg algorithm. When it is `ON`, disk spill can be triggered for the concurrent HashAgg algorithm. This variable will be deprecated when this feature is generally available in a future release. |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) | Newly added | Controls whether to enable Fast [`CREATE TABLE`](/fast-create-table.md). Set the value to `ON` to enable it and `OFF` to disable it. The default value is `ON`. When this variable is enabled, DDL statements will be executed using Fast `CREATE TABLE`. |
| [`tidb_load_binding_timeout`](/system-variables.md#tidb_load_binding_timeout-new-in-v800) | Newly added | Controls the timeout of binding loading. If the execution time of loading bindings exceeds this value, the loading will be stopped. |
| [`tidb_low_resolution_tso_update_interval`](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800) | Newly added | Controls the interval for updating TiDB [cache timestamp](/system-variables.md#tidb_low_resolution_tso). |
| [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800) | Newly added | Controls whether the optimizer can select [invisible indexes](/sql-statements/sql-statement-create-index.md#invisible-index) for query optimization in the current session. When the variable is set to `ON`, the optimizer can select invisible indexes for query optimization in the session. |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)  | Newly added | Controls the upper limit of memory that can be used for caching the schema information to avoid occupying too much memory. When this feature is enabled, the LRU algorithm is used to cache the required tables, effectively reducing the memory occupied by schema information.    |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info) | Modified | Adds a control to whether to record the [usage statistics of indexes](/information-schema/information-schema-tidb-index-usage.md). The default value is `true`. |
| TiDB | [`tls-version`](/tidb-configuration-file.md#tls-version) | Modified | This parameter no longer supports `"TLSv1.0"` and `"TLSv1.1"`. Now it only supports `"TLSv1.2"` and `"TLSv1.3"`. |
| TiDB  | [`log.file.compression`](/tidb-configuration-file.md#compression-new-in-v800) | Newly added | Specifies the compression format of the polling log. The default value is null, which means that the polling log is not compressed. |
| TiDB  | [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800) | Newly added | Specifies the file to save the general log to. The default is null, which means that the general log will be written to the instance file. |
| TiKV | [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) | Modified | Change the default value from `0` to `1` to improve TiKV performance, meaning that the size of the StoreWriter thread pool now defaults to `1`. |
| TiKV | [`security.encryption.master-key.vendor`] | 新增 | 指定住密钥的服务商类型，支持可选值为 `gcp`、`azure` |
| TiDB Lightning  | [`tikv-importer.duplicate-resolution`](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)  | Deprecated | Controls whether to detect and resolve unique key conflicts in physical import mode. Starting from v8.0.0, it is replaced by [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task). |
| TiDB Lightning  | [`conflict.precheck-conflict-before-import`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)  | Newly added | Controls whether to enable conflict prechecks, which means that TiDB Lightning checks data conflicts before importing data to TiDB. The default value of this parameter is `false`, which means that TiDB Lightning only checks conflicts after the data import. This parameter can be used only in the physical import mode (`tikv-importer.backend = "local"`).  |
| TiDB Lightning  | `logical-import-batch-rows` | 新增 | 用于在逻辑导入模式下设置一个 batch 里提交的数据行数，默认值为 `65536`。 |
| TiDB Lightning  | `logical-import-batch-size` | 新增 | 用于在逻辑导入模式下设置一个 batch 里提交的数据大小，取值为字符串类型，默认值为 `"96KiB"`，单位可以为 KB、KiB、MB、MiB 等存储单位。 |
| Data Migration  |  [`secret-key-path`](/dm/dm-master-configuration-file.md) | Newly added | Specifies the file path of the key, which is used to encrypt and decrypt upstream and downstream passwords. The file must contain a 64-character hexadecimal AES-256 key. |
| TiCDC | [`tls-key-file-path`](ticdc/ticdc-sink-to-pulsar.md) | Newly added | Specifies the path to the encrypted private key on the client, which is required when Pulsar enables TLS encrypted transmission. |
| TiCDC | [`tls-certificate-file`](ticdc/ticdc-sink-to-pulsar.md) | Newly added | Specifies the path to the encrypted certificate file on the client, which is required when Pulsar enables TLS encrypted transmission. |

### System tables

* Add new system tables [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) and [`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage) to record index usage statistics on TiDB nodes. **tw@Oreoxmt**
* Add a new system schema [`sys`](/sys-schema.md) and a new view [`sys.schema_unused_index`](/sys-schema.md#schema_unused_index), which records indexes that have not been used since the last start of TiDB. **tw@Oreoxmt**

## Deprecated features

- Starting from v8.0.0, the [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) system variable is deprecated, and TiDB no longer supports automatic retries of optimistic transactions. As an alternative, when encountering optimistic transaction conflicts, you can capture the error and retry transactions in your application, or use the [Pessimistic transaction mode](/pessimistic-transaction.md) instead. **tw@lilin90** <!--1671-->
- Starting from v8.0.0, TiDB no longer supports the TLSv1.0 and TLSv1.1 protocols. You must upgrade TLS to TLSv1.2 or TLSv1.3.

## Improvements

+ Tools

    + TiDB Data Migration (DM)
    
        - In a MariaDB primary and secondary replication scenario, that is, a `MariaDB_primary_instance` -> `MariaDB_secondary_instance` -> `DM` -> `TiDB` migration scenario, when `gtid_strict_mode = off` and the GTID of the `MariaDB_secondary_instance` is not strictly incrementing (for example, there is data writing to the `MariaDB_secondary_instance`), then the DM task will report an error `less than global checkpoint position`, the DM task will report an error `less than global checkpoint position`. Starting from v8.0.0, TiDB is compatible with this scenario and data can be migrated downstream. [#10741](https://github.com/pingcap/tiflow/issues/10741) @[okJiang](https://github.com/okJiang) **tw@hfxsd** <!--1683-->
        
## Bug fixes

## Contributors
