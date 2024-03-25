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
    <td>TiCDC introduces support for a new protocol, the Simple protocol. This protocol includes support for in-band schema tracking capabilities by embedding schema information in DDL and BOOTSTRAP events.</td>
  </tr>
  <tr>
    <td>TiCDC adds support for the Debezium format protocol **tw@lilin90** <!--1652--></td>
    <td>TiCDC introduces support for a new protocol, the Debezium protocol. TiCDC can now publish replication events to a Kafka sink using a protocol that generates Debezium style messages.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

- PD supports the microservice mode (experimental) [#5766](https://github.com/tikv/pd/issues/5766) @[binshi-bing](https://github.com/binshi-bing) **tw@qiancai** <!--1553/1558-->

    Starting from v8.0.0, PD supports the microservice mode. This mode disaggregates the timestamp allocation and cluster scheduling functions of PD into separate microservices that can be deployed independently, thereby enhancing performance scalability for PD and addressing performance bottlenecks of PD in large-scale clusters.

    - `tso` microservice: provides monotonically increasing timestamp allocation for the entire cluster.
    - `scheduling` microservice: provides scheduling functions for the entire cluster, including but not limited to load balancing, hot spot handling, replica repair, and replica placement.

    Each microservice is deployed as an independent process. If you configure more than one replica for a microservice, the microservice automatically implements a primary-secondary fault-tolerant mode to ensure high availability and reliability of the service.

    Currently, PD microservices can only be deployed using TiDB Operator and TiUP playground. It is recommended to consider this mode when PD becomes a significant performance bottleneck that cannot be resolved by scaling up.

    For more information, see [documentation](https://docs.pingcap.com/tidb-in-kubernetes/dev/pd-microservices).

* Enhance the usability of the Titan engine [#16245](https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996) **tw@qiancai** <!--1708-->

    - Enable the shared cache for Titan blob files and RocksDB block files by default ([`shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-tidb-introduced-in-v800) defaults to `true`), eliminating the need to configure [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size) separately.
    - Support dynamically modifying [`min-blob-size`](/tikv-configuration-file.md#min-blob-size), [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression), and [`discardable-ratio`](/tikv-configuration-file.md#min-blob-size) to improve performance and flexibility when using the Titan engine.

    For more information, see [documentation](/storage-engine/titan-configuration.md).

### Performance

* BR improves snapshot restore speed by up to 10 times (GA) [#50701](https://github.com/pingcap/tidb/issues/50701) @[3pointer](https://github.com/3pointer) @[Leavrth](https://github.com/Leavrth) **tw@qiancai** <!--1681-->

  Starting from TiDB v8.0.0, the acceleration of snapshot restore speed has been generally available (GA) and enabled by default. BR improves snapshot restore speed by up to approximately 10 times while ensuring that data is sufficiently distributed, by implementing various optimizations such as adopting the coarse-grained region scattering algorithm, creating databases and tables in batches, reducing the mutual impact between SST file downloads and ingest operations, and accelerating the restore of table statistics. This feature fully utilizes all resources of each TiKV node, achieving parallel and rapid restore. According to test results from real-world cases, the data restore speed of a single TiKV node remains stable at 1.2 GB/s, enabling the restore of 100 TB of data within 1 hour.

  This means that even in high-load environments, BR can fully utilize the resources of each TiKV node, significantly reducing database restore time, enhancing the availability and reliability of databases, and reducing downtime and business losses caused by data loss or system failures.

  For more information, see [documentation](/br/br-snapshot-guide.md#restore-cluster-snapshots).

* Support pushing down the following functions to TiFlash [#50975](https://github.com/pingcap/tidb/issues/50975) [#50485](https://github.com/pingcap/tidb/issues/50485) @[yibin87](https://github.com/yibin87) @[windtalker](https://github.com/windtalker) **tw@Oreoxmt** <!--1662--><!--1664-->

    * `CAST(DECIMAL AS DOUBLE)`
    * `POWER()`

  For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* The concurrent HashAgg algorithm of TiDB supports disk spill (experimental) [#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1365-->

    In earlier versions of TiDB, the concurrency algorithm of the HashAgg operator does not support disk spill. If the execution plan of a SQL statement contains the concurrent HashAgg operator, all the data for that SQL statement can only be processed in memory. Consequently, TiDB has to process a large amount of data in memory. When the data size exceeds the memory limit, TiDB can only choose the non-concurrent algorithm, which does not leverage concurrency for performance improvement.

     In v8.0.0, the concurrent HashAgg algorithm of TiDB supports disk spill. Under any concurrent conditions, the HashAgg operator can automatically trigger data spill based on memory usage, thus balancing performance and data throughput. Currently, as an experimental feature, TiDB introduces the `tidb_enable_concurrent_hashagg_spill` variable to control whether to enable the concurrent HashAgg algorithm that supports disk spill. When this variable is `ON`, it means enabled. This variable will be deprecated when the feature is generally available in a future release.

    For more information, see [documentation](/system-variables.md#tidb_enable_concurrent_hashagg_spill-new-in-v760).

* Introduce the priority queue for automatic statistics update [#50132](https://github.com/pingcap/tidb/issues/50132) @[hi-rustin](https://github.com/hi-rustin) **tw@hfxsd** <!--1640-->

    Maintaining optimizer statistics up-to-date is the key to stabilizing database performance. Most users rely on the [automatic statistics update](/statistics.md#automatic-update) provided by TiDB to keep statistics up-to-date. Automatic statistics update polls the status of statistics for all objects, and adds objects with insufficient health to a queue for individual collection and update. In previous versions, the collection order is random, which could result in longer waits for more worthy objects to be updated, causing potential database performance regressions.

    Starting from v8.0.0, automatic statistics update dynamically sets priorities for objects in combination with a variety of conditions to ensure that more valuable objects for collection are processed first, such as newly created indexes and partitioned tables with partition changes. Additionally, TiDB prioritizes tables with lower health scores, placing them at the front of the queue. This enhancement improves the reasonableness of the collection order, and reduces performance problems caused by outdated statistics, therefore improving database stability.
    
    For more information, see [documentation](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800).

* Remove some limitations on execution plan cache [#49161](https://github.com/pingcap/tidb/pull/49161) @[mjonss](https://github.com/mjonss) @[qw4990](https://github.com/qw4990) **tw@hfxsd** <!--1622/1585-->

    TiDB supports [execution plan cache](/sql-prepared-plan-cache.md), which can effectively reduce the processing latency of transaction-intensive systems and is important for improving performance. In v8.0.0, TiDB removes several limitations on execution plan cache. Execution plans with the following contents can be cached:

    - [Partitioned tables](/partitioned-table.md)
    - [Generated columns](/generated-columns.md), including objects that depend on generated columns (such as [multi-valued indexes](/choose-index.md#multi-valued-indexes-and-plan-cache))

  This enhancement extends the usage scenarios of execution plan cache and improves the overall database performance in complex scenarios.

    For more information, see [documentation](/sql-prepared-plan-cache.md).

* Optimizer enhances support for multi-valued indexes [#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx) @[time-and-fate](https://github.com/time-and-fate) **tw@hfxsd** <!--1405/1584-->

    TiDB v6.6.0 introduces [multi-value indexes](/sql-statements/sql-statement-create-index.md#multi-valued-indexes) to improve query performance for JSON data types. In v8.0.0, the optimizer enhances its support for multi-valued indexes and can correctly identify and utilize them to optimize queries in complex scenarios.

    * The optimizer can collect statistics on multi-valued indexes and use this information for estimation. When a SQL statement might select from several multi-value indexes, the optimizer can identify the index with lower cost.
    * When using `OR` to connect multiple `member of` conditions, the optimizer can match an effective index partial path for each DNF item (a `member of` condition) and combine these paths using Union to form an `Index Merge`. This achieves more efficient condition filtering and data querying.

  For more information, see [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-indexes).
  
* Supports configuring the update interval for low-precision TSO [#51081](https://github.com/pingcap/tidb/issues/51081) @[Tema](https://github.com/Tema) **tw@hfxsd** <!--1725-->

    The [low-precision TSO feature](/system-variables.md#tidb_low_resolution_tso) in TiDB uses regularly updated TSO as the transaction timestamp. In scenarios where reading outdated data is acceptable, this feature reduces the overhead of obtaining TSO for small read-only transactions by sacrificing real-time performance and improves the ability of high-concurrency reads.

    Before v8.0.0, the TSO update interval of low-precision TSO feature is fixed and cannot be adjusted according to actual application requirements. In v8.0.0, TiDB introduces the system variable `tidb_low_resolution_tso_update_interval` to control the TSO update interval. This feature takes effect only when the low-precision TSO feature is enabled.

    For more information, see [documentation](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800).

### Reliability

* Support caching required schema information according to the LRU algorithm to reduce memory consumption on the TiDB server (experimental) [#50959](https://github.com/pingcap/tidb/issues/50959) @[gmhdbjd](https://github.com/gmhdbjd) **tw@hfxsd** <!--1691-->

    Before v8.0.0, each TiDB node caches the schema information of all tables. In scenarios with hundreds of thousands of tables, just caching these table schemas could consume a significant amount of memory. 
 
    Starting from v8.0.0, TiDB introduces the system variable [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800), which enables you to set an upper limit for caching schema information, thereby preventing excessive memory usage. When you enable this feature, TiDB uses the Least Recently Used (LRU) algorithm to cache the required tables, effectively reducing the memory consumed by the schema information.

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

* Support using some expressions to set default column values when creating a table (experimental) [#50936](https://github.com/pingcap/tidb/issues/50936) @[zimulala](https://github.com/zimulala) **tw@hfxsd** <!--1690-->

    Before v8.0.0, when you create a table, the default value of a column is limited to strings, numbers, and dates. Starting from v8.0.0, you can use some expressions as the default column values. For example, you can set the default value of a column to `UUID()`. This feature helps you meet more diverse requirements.
    
    For more information, see [documentation](/data-type-default-values.md#specify-expressions-as-default-values).

* Support the `div_precision_increment` system variable [#51501](https://github.com/pingcap/tidb/issues/51501) @[yibin87](https://github.com/yibin87) **tw@hfxsd** <!--1566-->

    MySQL 8.0 supports the variable `div_precision_increment`, which specifies the number of digits by which to increase the scale of the result of a division operation performed using the `/` operator. Before v8.0.0, TiDB does not support this variable, and division is performed to 4 decimal places. Starting from v8.0.0, TiDB supports this variable. You can specify the number of digits by which to increase the scale of the result of a division operation as desired.
    
    For more information, see [documentation](/system-variables.md#div_precision_increment-new-in-v800).
   
### DB operations

* PITR supports Amazon S3 Object Lock [#51184](https://github.com/pingcap/tidb/issues/51184) @[RidRisR](https://github.com/RidRisR) **tw@lilin90** <!--1604-->

    Amazon S3 Object Lock can help prevent backup data from being accidentally or intentionally deleted during a specified retention period, enhancing the security and integrity of data. Starting from v6.3.0, BR supports Amazon S3 Object Lock in snapshot backups, adding an additional layer of security for full backups. Starting from v8.0.0, PITR also supports Amazon S3 Object Lock. Whether full backups or log data backups, the Object Lock feature ensures a more reliable data protection, further strengthening the security of data backup and recovery and meeting regulatory requirements.

    For more information, see [documentation](/br/backup-and-restore-storages.md#other-features-supported-by-the-storage-service).

* Support making invisible indexes visible at the session level [#50653](https://github.com/pingcap/tidb/issues/50653) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1401-->

    By default, the optimizer does not select [invisible indexes](/sql-statements/sql-statement-create-index.md#invisible-index) to optimize query execution. This mechanism is usually used to evaluate whether to delete an index. If there is uncertainty about the potential performance impact of deleting an index, you have the option to set the index to invisible temporarily and promptly restore it to visible when needed.

    Starting from v8.0.0, you can set the session-level system variable [`tidb_opt_use_invisible_indexes`](/system-variables.md#) to `ON` to make the current session recognize and use invisible indexes. With this feature, you can create a new index and test its performance by setting the index to invisible first, and then modifying the system variable in the current session for testing without affecting other sessions. This improvement enhances the safety of performance tuning and helps to improve the stability of production databases.

    For more information, see [documentation](/sql-statements/sql-statement-create-index.md#invisible-index).

* Support writing general logs to a separate file [#51248](https://github.com/pingcap/tidb/issues/51248) @[Defined2014](https://github.com/Defined2014) **tw@hfxsd** <!--1632-->

    The general log is a MySQL-compatible feature that logs all executed SQL statements to help diagnose issues. TiDB also supports this feature. You can enable it by setting the variable [`tidb_general_log`](/system-variables.md#tidb_general_log). However, in previous versions, the content of general logs can only be written to the TiDB instance log along with other information, which is inconvenient for users who need to keep logs for a long time.

    Starting from v8.0.0, you can enable writing the general log to a specified file by setting the configuration item [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800) to a valid filename. The general log follows the same rotation and retention policies as the instance log.

    In addition, to reduce the disk space occupied by historical log files, TiDB v8.0.0 introduces a native log compression option. You can set the configuration item [`log.file.compression`](/tidb-configuration-file.md#compression-new-in-v800) to `gzip` to automatically compress rotated logs using the [`gzip`](https://www.gzip.org/) format.

    For more information, see [documentation](/tidb-configuration-file.md#general-log-file-new-in-v800).

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

* TiKV encryption at rest supports Google [Key Management Service (Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive?hl) (experimental) [#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv) **tw@qiancai** <!--1612-->

    TiKV ensures data security by encrypting stored data using the encryption at rest technique. The core of encryption at rest for security is key management. Starting from v8.0.0, you can manage the master key of TiKV using Google Cloud KMS to establish encryption-at-rest capabilities based on Cloud KMS, thereby enhancing the security of user data.

    To enable encryption at rest based on Google Cloud KMS, you need to create a key on Google Cloud and then configure the `[security.encryption.master-key]` section in the TiKV configuration file.

    For more information, see [documentation](/encryption-at-rest.md##tikv-encryption-at-rest).

* Enhance TiDB log desensitization [#51306](https://github.com/pingcap/tidb/issues/51306) @[xhebox](https://github.com/xhebox) **tw@hfxsd** <!--1229-->

    The enhancement of TiDB log desensitization is based on marking SQL text information in log files, facilitating the safe display of sensitive data when users view the logs. You can control whether to desensitize log information to enable secure use of TiDB logs in different scenarios, enhancing the security and flexibility of using log desensitization. To use this feature, set the system variable `tidb_redact_log` to `MARKER`. This marks the SQL text in TiDB logs. When you view the logs, sensitive data is securely displayed based on the markers, thus protecting the log information.

    For more information, see [documentation](/system-variables.md#tidb_redact_log).

### Data migration

* TiCDC adds support for the Simple protocol [#9898](https://github.com/pingcap/tiflow/issues/9898) @[3AceShowHand](https://github.com/3AceShowHand) **tw@lilin90** <!--1646-->

    TiCDC introduces support for a new protocol, the Simple protocol. This protocol includes support for in-band schema tracking capabilities by embedding schema information in DDL and BOOTSTRAP events.

    For more information, see [documentation](/ticdc/ticdc-simple-protocol.md).

* TiCDC adds support for the Debezium format protocol [#1799](https://github.com/pingcap/tiflow/issues/1799) @[breezewish](https://github.com/breezewish) **tw@lilin90** <!--1652-->

    TiCDC can now publish replication events to a Kafka sink using a protocol that generates event messages in a Debezium style format. This helps to simplify the migration from MySQL to TiDB for users who are currently using Debezium to pull data from MySQL for downstream processing.

    For more information, see [documentation](/ticdc/ticdc-debezium.md).

* TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (GA) [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) @[asddongmen](https://github.com/asddongmen) **tw@hfxsd** <!--1689/1682-->

    TiDB v7.6.0 introduces replicating DDL statements in BDR mode as an experimental feature. Previously, replicating DDL statements was not supported by TiCDC, so users of TiCDC bi-directional replication had to apply DDL statements to both TiDB clusters separately. With this feature, TiCDC allows for a cluster to be assigned the `PRIMARY` BDR role, and enables the replication of DDL statements from that cluster to the downstream cluster. In v8.0.0, this feature becomes generally available (GA).

    For more information, see [documentation](/ticdc/ticdc-bidirectional-replication.md).

* DM supports using a user-provided secret key to encrypt and decrypt passwords of source and target databases [#9492](https://github.com/pingcap/tiflow/issues/9492) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1497-->

    In earlier versions, DM uses a built-in fixed secret key with relatively low security. Starting from v8.0.0, you can upload and specify a secret key file for encrypting and decrypting passwords of upstream and downstream databases. In addition, you can replace the secret key file as needed to enhance data security.

    For more information, see [documentation](dm/dm-customized-secret-key.md).

* Supports the `IMPORT INTO ... FROM SELECT` syntax to enhance the `IMPORT INTO` functionality (experimental) [#49883](https://github.com/pingcap/tidb/issues/49883) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1680-->

    In earlier TiDB versions, importing query results into a target table could only be done using the `INSERT INTO ... SELECT` statement, which is relatively inefficient in some large dataset scenarios. Starting from v8.0.0, TiDB enables you to use `IMPORT INTO ... FROM SELECT` to import the results of a `SELECT` query into an empty TiDB target table, which achieves up to 8 times the performance of `INSERT INTO ... SELECT` and significantly reduces the import time.

    In addition, you can use `IMPORT INTO ... FROM SELECT` to import historical data queried with [`AS OF TIMESTAMP`](/as-of-timestamp.md).

   For more information, see [documentation](sql-statements/sql-statement-import-into.md).

* TiDB Lightning simplifies conflict resolution strategies and supports handling conflicting data using the `replace` strategy (experimental) [#51036](https://github.com/pingcap/tidb/issues/51036) @[lyzx2001](https://github.com/lyzx2001) **tw@qiancai** <!--1684-->

    In earlier versions, TiDB Lightning has [one data conflict resolution strategy](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md#conflict-detection) for the logical import mode and [two data conflict resolution strategies](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-data-detection) for the physical import mode, which are not easy to understand and configure.

    Starting from v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](tidb-lightning/tidb-lightning-configuration.md) parameter, and simplifies the configuration of this parameter. In addition, in the physical import mode, the `replace` strategy now supports retaining the latest data and overwriting the old data when the import detects data with primary key or unique key conflicts.

    For more information, see [documentation](tidb-lightning/tidb-lightning-configuration.md).

* Global Sort becomes generally available (GA), improving the performance and stability of  `IMPORT INTO` significantly [#45719](https://github.com/pingcap/tidb/issues/45719) @[lance6716](https://github.com/lance6716) **tw@qiancai** <!--1580-->

    Before v7.4.0, when executing `IMPORT INTO` tasks using the [Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md), TiDB only locally sorts part of the data before importing it into TiKV due to limited local storage space. This results in significant overlap of the imported data in TiKV, requiring TiKV to perform additional compaction operations during import and affecting the TiKV performance and stability.

    With the Global Sort experimental feature introduced in v7.4.0, TiDB can temporarily store the data to be imported in an external storage (such as Amazon S3) for global sorting before importing it into TiKV, which eliminates the need for TiKV compaction operations during import. In v8.0.0, Global sorting becomes GA. This feature reduces the resource consumption of TiKV and significantly improves the performance and stability of `IMPORT INTO`. If you enable the Global Sort, each `IMPORT INTO` task supports importing data within 40 TiB.

   For more information, see [documentation](/tidb-global-sort.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.6.0 to the current version (v8.0.0). If you are upgrading from v7.5.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

- Prohibit setting [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610) to `ON` in Security Enhanced Mode (SEM) to prevent potential connectivity issues for users [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
- DM removes the fixed secret key for encryption and decryption and enables you to customize a secret key for encryption and decryption. If encrypted passwords are used in [data source configurations](/dm/dm-source-configuration-file.md) and [migration task configurations](/dm/task-configuration-file-full.md) before the upgrade, you need to refer to the upgrade steps in [Customize a Secret Key for DM Encryption and Decryption](/dm/dm-customized-secret-key.md) for additional operations. [#9492](https://github.com/pingcap/tiflow/issues/9492) @[D3Hunter](https://github.com/D3Hunter)

### Behavior changes

* Before v8.0.0, after enabling the acceleration of `ADD INDEX` and `CREATE INDEX` (`tidb_ddl_enable_fast_reorg = ON`), the encoded index key ingests data to TiKV with a fixed concurrency of `16`, which cannot be dynamically adjusted according to the downstream TiKV capacity. Starting from v8.0.0, you can adjust the concurrency using the [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt-new-in-v800) system variable. The default value is `4`. Compared with the previous default value of `16`, the new default value reduces performance when ingesting indexed key-value pairs. You can adjust this system variable based on the workload of your cluster. **tw@hfxsd** <!--no FD-->

### MySQL compatibility 

* The `KEY` partition type supports statements with an empty list of partition fields, which is consistent with the behavior of MySQL. **tw@hfxsd** <!--No FD-->

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) | Deprecated | Starting from v8.0.0, this system variable is deprecated, and TiDB no longer supports automatic retries of optimistic transactions. It is recommended to use the [Pessimistic transaction mode](/pessimistic-transaction.md). If you encounter optimistic transaction conflicts, you can capture the error and retry transactions in your application. |
| `tidb_ddl_version` | Renamed | Controls whether to enable TiDB DDL V2. Starting from v8.0.0, this variable is renamed to [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800). |
| [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) | Modified | Adds a control to whether to record the [usage statistics of indexes](/information-schema/information-schema-tidb-index-usage.md). The default value is `ON`. |
| [`tidb_redact_log`](/system-variables.md#tidb_redact_log) | Modified | Controls how to handle user information in SAL text when logging TiDB logs and slow logs. Values can be `OFF` and `ON`, to support log information in plain text, and masking log information, respectively. To provide a richer way of processing user information in the log, the `MARKER` option is added in v8.0.0 to support marking log information. |
| [`div_precision_increment`](/system-variables.md#div_precision_increment-new-in-v800) | Newly added | Controls the number of digits by which to increase the scale of the result of a division operation performed using the `/` operator. This variable is the same as MySQL. |
| [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) | Newly added | Controls the execution mode of DML statements. The value options are `"standard"` and `"bulk"`. |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) | Newly added | Control whether to enable the priority queue to schedule the tasks of automatically collecting statistics. When this variable is enabled, TiDB prioritizes collecting statistics for the tables that most need statistics. |
| [`tidb_enable_concurrent_hashagg_spill`](/system-variables.md#tidb_enable_concurrent_hashagg_spill-new-in-v800) | Newly added | Controls whether TiDB supports disk spill for the concurrent HashAgg algorithm. When it is `ON`, disk spill can be triggered for the concurrent HashAgg algorithm. This variable will be deprecated when this feature is generally available in a future release. |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) | Newly added | Controls whether to enable [TiDB Accerates Table Creation](/fast-create-table.md). Set the value to `ON` to enable it and `OFF` to disable it. The default value is `ON`. When this variable is enabled, TiDB accelerates table creation by using [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md). |
| [`tidb_load_binding_timeout`](/system-variables.md#tidb_load_binding_timeout-new-in-v800) | Newly added | Controls the timeout of loading bindings. If the execution time of loading bindings exceeds this value, the loading will stop. |
| [`tidb_low_resolution_tso_update_interval`](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800) | Newly added | Controls the interval for updating TiDB [cache timestamp](/system-variables.md#tidb_low_resolution_tso). |
| [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800) | Newly added | Controls whether the optimizer can select [invisible indexes](/sql-statements/sql-statement-create-index.md#invisible-index) for query optimization in the current session. When the variable is set to `ON`, the optimizer can select invisible indexes for query optimization in the session. |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)  | Newly added | Controls the upper limit of memory that can be used for caching the schema information to avoid occupying too much memory. When this feature is enabled, the LRU algorithm is used to cache the required tables, effectively reducing the memory occupied by the schema information.    |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info) | Modified | Adds a control to whether to record the [usage statistics of indexes](/information-schema/information-schema-tidb-index-usage.md). The default value is `true`. |
| TiDB | [`tls-version`](/tidb-configuration-file.md#tls-version) | Modified | This parameter no longer supports `"TLSv1.0"` and `"TLSv1.1"`. Now it only supports `"TLSv1.2"` and `"TLSv1.3"`. |
| TiDB  | [`log.file.compression`](/tidb-configuration-file.md#compression-new-in-v800) | Newly added | Specifies the compression format of the polling log. The default value is null, which means that the polling log is not compressed. |
| TiDB  | [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800) | Newly added | Specifies the file to save the general log to. The default is null, which means that the general log will be written to the instance file. |
| TiDB | [`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-从-v800-版本开始引入) | 新增 | 控制是否使用 replica selector v2 版本，默认值为 `true`。 |
| TiKV | [`log-backup.initial-scan-rate-limit`](/system-variables.md#initial-scan-rate-limit-new-in-v620) | Modified | Add a limit of `1MiB` as the minimum value. |
| TiKV | [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) | Modified | Change the default value from `0` to `1` to improve TiKV performance, meaning that the size of the StoreWriter thread pool now defaults to `1`. |
| TiKV | [`security.encryption.master-key.vendor`] | 新增 | 指定住密钥的服务商类型，支持可选值为 `gcp`、`azure` |
| TiDB Lightning  | [`tikv-importer.duplicate-resolution`](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)  | Deprecated | Controls whether to detect and resolve unique key conflicts in physical import mode. Starting from v8.0.0, it is replaced by [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task). |
| TiDB Lightning  | [`conflict.precheck-conflict-before-import`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)  | Newly added | Controls whether to enable conflict prechecks, which means that TiDB Lightning checks data conflicts before importing data to TiDB. The default value of this parameter is `false`, which means that TiDB Lightning only checks conflicts after the data import. This parameter can be used only in the physical import mode (`tikv-importer.backend = "local"`).  |
| TiDB Lightning  | [`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Newly added | Controls the maximum number of rows inserted per transaction in Logical Import Mode. The default value is `65536` rows. |
| TiDB Lightning  | [`logical-import-batch-size`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Newly added | Controls the size of each SQL query executed on the downstream TiDB server in Logical Import Mode. The default value is `"96KiB"`. The unit can be KB, KiB, MB, or MiB. |
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

+ TiDB <!--tw@qiancai, 18 条-->

    - Improve the data spill performance of the `Sort` operator [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1609-->
    - Support canceling queries during the data spill process, which optimizes the exit mechanism of the data spill feature [#50511](https://github.com/pingcap/tidb/issues/50511) @[wshwsh12](https://github.com/wshwsh12) **tw@qiancai** <!--1635-->
    - Support using an index that matches partial conditions to construct Index Join when processing table join queries with multiple equal conditions [#47233](https://github.com/pingcap/tidb/issues/47233) @[winoros](https://github.com/winoros) **tw@Oreoxmt** <!--1601-->
    - Enhance the capability of Index Merge to identify sorting requirements in queries and select indexes that meet the sorting requirements [#48359](https://github.com/pingcap/tidb/issues/48359) @[AilinKid](https://github.com/AilinKid)
    - When the `Apply` operator is not executed concurrently, TiDB enables you to view the name of the operator that blocks the concurrency by executing `SHOW WARNINGS` [#50256](https://github.com/pingcap/tidb/issues/50256) @[hawkingrei](https://github.com/hawkingrei)
    - Optimize the index selection for `point get` queries by selecting the most optimal index for queries when all indexes support `point get` queries, which  @[elsa0520](https://github.com/elsa0520)
    - Temporarily adjust the priority of statistics synchronously loading tasks to high to avoid widespread timeouts during TiKV high loads, as these timeouts might result in statistics not being loaded [#50332](https://github.com/pingcap/tidb/issues/50332) @[winoros](https://github.com/winoros)
    - When the `PREPARE` statement fails to hit the execution plan cache, TiDB enables you to view the reason by executing `SHOW WARNINGS` [#50407](https://github.com/pingcap/tidb/issues/50407) @[hawkingrei](https://github.com/hawkingrei)
    - Improve the accuracy of query estimation information when the same row of data is updated multiple times [#47523](https://github.com/pingcap/tidb/issues/47523) @[terry1purcell](https://github.com/terry1purcell)
    - Index Merge supports embedding multi-value indexes and `OR` operators in `AND` predicates [#51778](https://github.com/pingcap/tidb/issues/51778) @[time-and-fate](https://github.com/time-and-fate)
    - Support submitting 16 `IMPORT INTO ... FROM FILE` tasks simultaneously, facilitating bulk data import into the target tables and significantly improving the efficiency and performance of data file import [#49008](https://github.com/pingcap/tidb/issues/49008) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1680-->
    - (dup): release-7.1.4.md > Improvements> TiDB -  When `force-init-stats` is set to `true`, TiDB waits for statistics initialization to finish before providing services during TiDB startup. This setting no longer blocks the startup of HTTP servers, which enables users to continue monitoring [#50854](https://github.com/pingcap/tidb/issues/50854) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue where blocked DDL is not displayed in MDL View when DDL tasks involve multiple tables [#47743](https://github.com/pingcap/tidb/issues/47743) @[wjhuang2016](https://github.com/wjhuang2016)
    - Improve the performance of executing the `CREATE TABLE` DDL statement by 10 times and support linear scalability [#50052](https://github.com/pingcap/tidb/issues/50052) @[GMHDBJD](https://github.com/GMHDBJD)

+ TiKV <!--tw@Oreoxmt, 13 条-->

    - Enhance TSO verification and detection to improve the robustness of the cluster TSO when the configuration or operation is improper [#16545](https://github.com/tikv/tikv/issues/16545) @[cfzjywxk](https://github.com/cfzjywxk)
    - Optimize the logic of cleaning up pessimistic locks to improve the processing performance of uncommitted transactions [#16158](https://github.com/tikv/tikv/issues/16158) @[cfzjywxk](https://github.com/cfzjywxk)
    - Introduce unified health control for TiKV to reduce the impact of abnormal single TiKV node on cluster access performance. You can disable this optimization by setting [`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800) to `false`. [#16297](https://github.com/tikv/tikv/issues/16297) [#1104](https://github.com/tikv/client-go/issues/1104) [#1167](https://github.com/tikv/client-go/issues/1167) @[MyonKeminta](https://github.com/MyonKeminta) @[zyguan](https://github.com/zyguan) @[crazycs520](https://github.com/crazycs520) **tw@qiancai** <!--1707-->
    - The PD client uses the metadata storage interface to replace the previous global configuration interface [#14484](https://github.com/tikv/tikv/issues/14484) @[HuSharp](https://github.com/HuSharp)
    - Enhance the scanning performance by determining the data loading behavior through write cf stats [#16245](https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996)
    - Check the latest heartbeat for nodes being deleted and voters being demoted during the Raft conf change process to ensure that this behavior does not make the Region inaccessible [#15799](https://github.com/tikv/tikv/issues/15799) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Add Flush and BufferBatchGet interfaces for Pipelined DML [#16291](https://github.com/tikv/tikv/issues/16291) @[ekexium](https://github.com/ekexium)
    - Add monitoring and alerting for cgroup CPU and memory limits [#16392](https://github.com/tikv/tikv/issues/16392) @[pingandb](https://github.com/pingandb)
    - Add CPU monitoring for Region workers and snapshot generation workers [#16562](https://github.com/tikv/tikv/issues/16562) @[Connor1996](https://github.com/Connor1996)
    - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ PD <!--tw@Oreoxmt, 11 条-->

    - Enhance the service discovery capability of the PD client to improve its high availability and load balancing [#7576](https://github.com/tikv/pd/issues/7576) @[CabinfeverB](https://github.com/CabinfeverB)
    - Enhance the retry mechanism of the PD client [#7673](https://github.com/tikv/pd/issues/7673) @[JmPotato](https://github.com/JmPotato)
    - Add monitoring and alerting for cgroup CPU and memory limits [#7716](https://github.com/tikv/pd/issues/7716) [#7918](https://github.com/tikv/pd/issues/7918) @[pingandb](https://github.com/pingandb) @[rleungx](https://github.com/rleungx)
    - Improve the performance and high availability when using etcd watch [#7738](https://github.com/tikv/pd/issues/7738) [#7724](https://github.com/tikv/pd/issues/7724) [#7689](https://github.com/tikv/pd/issues/7689) @[lhy1024](https://github.com/lhy1024)
    - Add more monitoring metrics for heartbeat to better analyze performance bottlenecks [#7868](https://github.com/tikv/pd/issues/7868) @[nolouch](https://github.com/nolouch)
    - Reduce the impact of the etcd leader on the PD leader [#7499](https://github.com/tikv/pd/issues/7499) @[JmPotato](https://github.com/JmPotato) @[HuSharp](https://github.com/HuSharp)
    - Enhance the detection mechanism for unhealthy etcd nodes [#7730](https://github.com/tikv/pd/issues/7730) @[JmPotato](https://github.com/JmPotato) @[HuSharp](https://github.com/HuSharp)
    - Optimize the output of GC safepoint in pd-ctl [#7767](https://github.com/tikv/pd/issues/7767) @[nolouch](https://github.com/nolouch)
    - Support dynamic modification of the historical window configuration in the hotspot scheduler [#7877](https://github.com/tikv/pd/issues/7877) @[lhy1024](https://github.com/lhy1024)
    - Reduce the lock contention issue in creating operators [#7837](https://github.com/tikv/pd/issues/7837) @[Leavrth](https://github.com/Leavrth)
    - Adjust GRPC configurations to improve availability [#7821](https://github.com/tikv/pd/issues/7821) @[rleungx](https://github.com/rleungx)

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai, 5 条-->

        - Support controlling whether to restore statistics using the newly added restore parameter `--load-stats` [#50568](https://github.com/pingcap/tidb/issues/50568) @[Leavrth](https://github.com/Leavrth)
        - Enhance restore performance by enabling the coarse-grained Region scatter algorithm to adaptively obtain concurrent parameters [#50701](https://github.com/pingcap/tidb/issues/50701) @[3pointer](https://github.com/3pointer)
        - Display the `log` command in the command-line help information of `br` [#50927](https://github.com/pingcap/tidb/issues/50927) @[RidRisR](https://github.com/RidRisR)
        - Support pre-allocating Table ID during the restore process to maximize the reuse of Table ID and improve restore performance [#51736](https://github.com/pingcap/tidb/issues/51736) @[Leavrth](https://github.com/Leavrth)
        - Disable the gc memory limit tuner feature within TiDB when using BR to avoid OOM issues [#51078](https://github.com/pingcap/tidb/issues/51078) @[Leavrth](https://github.com/Leavrth)

    + TiCDC <!--tw@hfxsd, 2 条-->

        - (dup): release-7.5.1.md > 改进提升> Tools> TiCDC - 支持[查询 changefeed 的下游同步状态](https://docs.pingcap.com/zh/tidb/v7.5/ticdc-open-api-v2#查询特定同步任务是否完成)，以确认 TiCDC 是否已将所接收到的上游变更完全同步到下游 [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)
        - Optimize the memory consumption of `RowChangedEvent` to reduce memory consumption when TiCDC replicates data [#10386](https://github.com/pingcap/tiflow/issues/10386) @[lidezhu](https://github.com/lidezhu)
        - Verify that the start-ts parameter is valid when creating and resuming a changefeed task [#10499](https://github.com/pingcap/tiflow/issues/10499) @[3AceShowHand](https://github.com/3AceShowHand)
    + TiDB Data Migration (DM)
        - In a MariaDB primary-secondary replication scenario, where the migration path is: MariaDB primary instance -> MariaDB secondary instance -> DM -> TiDB, when `gtid_strict_mode = off` and the GTID of the MariaDB secondary instance is not strictly incrementing (for example, there is data writing to the MariaDB secondary instance), the DM task will report an error `less than global checkpoint position`. Starting from v8.0.0, TiDB is compatible with this scenario and data can be migrated downstream normally. [#10741](https://github.com/pingcap/tiflow/issues/10741) @[okJiang](https://github.com/okJiang) **tw@hfxsd** <!--1683-->
        
    + TiDB Lightning
        
        - In logical import mode, you can configure the maximum number of rows in a batch using [`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) [#46607](https://github.com/pingcap/tidb/issues/46607) @[kennytm](https://github.com/kennytm)
        - If the space of TiFlash is insufficient, an error will be reported for TiFlash [#50324](https://github.com/pingcap/tidb/issues/50324) @[okJiang](https://github.com/okJiang)

## Bug fixes

+ TiDB

+ TiKV

    - (dup): release-7.5.1.md > 错误修复> TiKV - 修复开启 `tidb_enable_row_level_checksum` 可能导致 TiKV panic 的问题 [#16371](https://github.com/tikv/tikv/issues/16371) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-7.1.4.md > 错误修复> TiKV - 修复休眠的 Region 在异常情况下未被及时唤醒的问题 [#16368](https://github.com/tikv/tikv/issues/16368) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.1.4.md > 错误修复> TiKV - 通过在执行下线节点操作前检查该 Region 所有副本的上一次心跳时间，修复下线一个副本导致整个 Region 不可用的问题 [#16465](https://github.com/tikv/tikv/issues/16465) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - (dup): release-7.1.4.md > 错误修复> TiKV - 修复 JSON 整型数值在大于 `INT64` 最大值但小于 `UINT64` 最大值时会被 TiKV 解析成 `FLOAT64` 导致结果和 TiDB 不一致的问题 [#16512](https://github.com/tikv/tikv/issues/16512) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the monitoring metric `tikv_unified_read_pool_thread_count` has no data in some cases [#16629](https://github.com/tikv/tikv/issues/16629) @[YuJuncen](https://github.com/YuJuncen)
    
+ PD


+ TiFlash <!--tw@hfxsd, 2 条-->

    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复副本迁移时，因 TiFlash 与 PD 之间网络连接不稳定可能引发的 TiFlash panic 的问题 [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复慢查询导致内存使用显著增加的问题 [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复移除 TiFlash 副本后重新添加可能导致 TiFlash 数据损坏的问题 [#8695](https://github.com/pingcap/tiflash/issues/8695) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复在执行 PITR 恢复任务或 `FLASHBACK CLUSTER TO` 后，TiFlash 副本数据可能被意外删除，导致数据异常的问题 [#8777](https://github.com/pingcap/tiflash/issues/8777) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.1.md > 错误修复> TiFlash - 修复在执行 `ALTER TABLE ... MODIFY COLUMN ... NOT NULL` 时，将原本可为空的列修改为不可为空之后，导致 TiFlash panic 的问题 [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that in the disaggregated storage and compute architecture, queries might be permanently blocked after network isolation [#8806](https://github.com/pingcap/tiflash/issues/8806) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that in the disaggregated storage and compute architecture, TiFlash might panic during shutdown [#8837](https://github.com/pingcap/tiflash/issues/8837) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR) <!--tw@hfxsd, 3 条-->
    
        - Fix the issue that the PITR checkpoint gets stuck when a Region splits or merges immediately after it becomes a leader [#16469](https://github.com/tikv/tikv/issues/16469) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that TiKV panics when a full backup fails to find a peer in some extreme cases [#16394](https://github.com/tikv/tikv/issues/16394) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复在同一节点上更改 TiKV IP 地址导致日志备份卡住的问题 [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复从 S3 读文件内容时出错后无法重试的问题 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复数据恢复失败后，使用断点重启报错 `the target cluster is not fresh` 的问题 [#50232](https://github.com/pingcap/tidb/issues/50232) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复停止日志备份任务导致 TiDB crash 的问题 [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复由于某个 TiKV 节点缺少 Leader 导致数据恢复变慢的问题 [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > 错误修复> Tools> Backup & Restore (BR) - 修复全量恢复指定 `--filter` 选项后，仍然要求目标集群为空的问题 [#51009](https://github.com/pingcap/tidb/issues/51009) @[3pointer](https://github.com/3pointer)
        
    + TiCDC <!--tw@hfxsd, 4 条-->

        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复使用 storage sink 时，在存储服务生成的文件序号可能出现回退的问题 [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复并发创建多个 changefeed 时 TiCDC 返回 `ErrChangeFeedAlreadyExists` 错误的问题 [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复在 `ignore-event` 中设置了过滤掉 `add table partition` 事件后，TiCDC 未将相关分区的其它类型 DML 变更事件同步到下游的问题 [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复上游表执行了 `TRUNCATE PARTITION` 后 changefeed 报错的问题 [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-7.1.4.md > 错误修复> Tools> TiCDC - 修复恢复 changefeed 时 changefeed 的 `checkpoint-ts` 小于 TiDB 的 GC safepoint，没有及时报错 `snapshot lost caused by GC` 的问题 [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-7.1.4.md > 错误修复> Tools> TiCDC - 修复 TiCDC 在开启单行数据正确性校验后由于时区不匹配导致 `TIMESTAMP` 类型 checksum 验证失败的问题 [#10573](https://github.com/pingcap/tiflow/issues/10573) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复 Syncpoint 表可能被错误同步的问题 [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.5.1.md > 错误修复> Tools> TiCDC - 修复当使用 Apache Pulsar 作为下游时，无法正常启用 OAuth2.0、TLS 和 mTLS 的问题 [#10602](https://github.com/pingcap/tiflow/issues/10602) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that a changefeed might get stuck when TiKV upgrades, restarts, or evicts a leader [#10584](https://github.com/pingcap/tiflow/issues/10584) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that data is written to a wrong CSV file due to wrong BarrierTS in scenarios where DDL statements are executed frequently [#10668](https://github.com/pingcap/tiflow/issues/10668) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that data race in the KV client causes TiCDC to panic [#10718](https://github.com/pingcap/tiflow/issues/10718) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue TiCDC panics when scheduling table replication tasks [#10613](https://github.com/pingcap/tiflow/issues/10613) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - Fix the issue that data is lost when upstream is a primary key of binary type [[#10672](https://github.com/pingcap/tiflow/issues/10672) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - Fix the performance regression issue caused by checking TiKV space [#43636](https://github.com/pingcap/tidb/issues/43636) @[lance6716](https://github.com/lance6716)
        - Fix the issue that the value of `DATETIME` is incorrectly encoded in `NO_ZERO_IN_DATE` SQL mode [#50757](https://github.com/pingcap/tidb/issues/50757) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that broken symlinks are not ignored when importing data [#49423](https://github.com/pingcap/tidb/issues/49423) @[lance6716](https://github.com/lance6716)
        - (dup): release-7.1.4.md > 错误修复> Tools> TiDB Lightning - 修复在扫描数据文件时，遇到不合法符号链接文件而报错的问题 [#49423](https://github.com/pingcap/tidb/issues/49423) @[lance6716](https://github.com/lance6716)
        - (dup): release-7.1.4.md > 错误修复> Tools> TiDB Lightning - 修复当 `sql_mode` 中不包含 `NO_ZERO_IN_DATE` 时，TiDB Lightning 无法正确解析包含 `0` 的日期值的问题 [#50757](https://github.com/pingcap/tidb/issues/50757) @[GMHDBJD](https://github.com/GMHDBJD)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [Aoang](https://github.com/Aoang)
- [bufferflies](https://github.com/bufferflies)
- [daemon365](https://github.com/daemon365)
- [eltociear](https://github.com/eltociear)
- [lichunzhu](https://github.com/lichunzhu)
- [jiyfhust](https://github.com/jiyfhust)
- [pingandb](https://github.com/pingandb)
- [renovate](https://github.com/renovate)
- [shenqidebaozi](https://github.com/shenqidebaozi)
- [Smityz](https://github.com/Smityz)
- [songzhibin97](https://github.com/songzhibin97)
- [tangjingyu97](https://github.com/tangjingyu97)
- [Tema](https://github.com/Tema)
- [ub-3](https://github.com/ub-3)
- [yoshikipom](https://github.com/yoshikipom)
