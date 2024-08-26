---
title: TiDB 8.0.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.0.0.
---

# TiDB 8.0.0 Release Notes

Release date: March 29, 2024

TiDB version: 8.0.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.0/quick-start-with-tidb)

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
    <td><a href="https://docs.pingcap.com/tidb/v8.0/pd-microservices">Disaggregation of PD to improve scalability (experimental)</a> </td>
    <td>Placement Driver (PD) contains multiple critical modules to ensure the normal operation of TiDB clusters. As the workload of a cluster increases, the resource consumption of each module in PD also increases, causing mutual interference between these modules and ultimately affecting the overall service quality of the cluster. Starting from v8.0.0, TiDB addresses this issue by splitting the TSO and scheduling modules in PD into independently deployable microservices. This can significantly reduce the mutual interference between modules as the cluster scales. With this architecture, much larger clusters with much larger workloads are now possible.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.0/system-variables#tidb_dml_type-new-in-v800">Bulk DML for much larger transactions (experimental)</a></td>
    <td>Large batch DML jobs, such as extensive cleanup jobs, joins, or aggregations, can consume a significant amount of memory and have previously been limited at very large scales. Bulk DML (<code>tidb_dml_type = "bulk"</code>) is a new DML type for handling large batch DML tasks more efficiently while providing transaction guarantees and mitigating OOM issues. This feature differs from import, load, and restore operations when used for data loading.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.0/br-snapshot-guide#restore-cluster-snapshots">Acceleration of cluster snapshot restore speed (GA) </a></td>
    <td>With this feature, BR can fully leverage the scale advantage of a cluster, enabling all TiKV nodes in the cluster to participate in the preparation step of data restores. This feature can significantly improve the restore speed of large datasets in large-scale clusters. Real-world tests show that this feature can saturate the download bandwidth, with the download speed improving by 8 to 10 times, and the end-to-end restore speed improving by approximately 1.5 to 3 times.</td>
  </tr>
  <tr>
    <td>Enhance the stability of caching the schema information when there is a massive number of tables (experimental)</td>
    <td>SaaS companies using TiDB as the system of record for their multi-tenant applications often need to store a substantial number of tables. In previous versions, handling table counts in the order of a million or more was feasible, but it had the potential to degrade the overall user experience. TiDB v8.0.0 improves the situation by implementing a <a href="https://docs.pingcap.com/tidb/v8.0/system-variables#tidb_enable_auto_analyze_priority_queue-new-in-v800">priority queue</a> for <code>auto analyze</code>, making the process less rigid and enhancing stability across a wider array of tables.</td>
  </tr>
  <tr>
    <td rowspan="1">DB Operations and Observability</td>
    <td>Support monitoring index usage statistics </td>
    <td>Proper index design is a crucial prerequisite to maintaining database performance. TiDB v8.0.0 introduces the <a href="https://docs.pingcap.com/tidb/v8.0/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a> table and the <a href="https://docs.pingcap.com/tidb/v8.0/sys-schema-unused-indexes"><code>sys.schema_unused_indexes</code></a> view to provide usage statistics of indexes. This feature helps you assess the efficiency of indexes in the database and optimize the index design.</td>
  </tr>
  <tr>
    <td rowspan="2">Data Migration</td>
    <td>TiCDC adds support for <a href="https://docs.pingcap.com/tidb/v8.0/ticdc-simple-protocol">the Simple protocol</a> </td>
    <td>TiCDC introduces a new protocol, the Simple protocol. This protocol provides in-band schema tracking capabilities by embedding table schema information in DDL and BOOTSTRAP events.</td>
  </tr>
  <tr>
    <td>TiCDC adds support for <a href="https://docs.pingcap.com/tidb/v8.0/ticdc-debezium">the Debezium format protocol</a> </td>
    <td>TiCDC introduces a new protocol, the Debezium protocol. TiCDC can now publish data change events to a Kafka sink using a protocol that generates Debezium style messages.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

- PD supports the microservice mode (experimental) [#5766](https://github.com/tikv/pd/issues/5766) @[binshi-bing](https://github.com/binshi-bing)

    Starting from v8.0.0, PD supports the microservice mode. This mode splits the timestamp allocation and cluster scheduling functions of PD into separate microservices that can be deployed independently, thereby enhancing performance scalability for PD and addressing performance bottlenecks of PD in large-scale clusters.

    - `tso` microservice: provides monotonically increasing timestamp allocation for the entire cluster.
    - `scheduling` microservice: provides scheduling functions for the entire cluster, including but not limited to load balancing, hot spot handling, replica repair, and replica placement.

  Each microservice is deployed as an independent process. If you configure more than one replica for a microservice, the microservice automatically implements a primary-secondary fault-tolerant mode to ensure high availability and reliability of the service.

    Currently, PD microservices can only be deployed using TiDB Operator. It is recommended to consider this mode when PD becomes a significant performance bottleneck that cannot be resolved by scaling up.

    For more information, see [documentation](/pd-microservices.md).

* Enhance the usability of the Titan engine [#16245](https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996)

    - Enable the shared cache for Titan blob files and RocksDB block files by default ([`shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-new-in-v800) defaults to `true`), eliminating the need to configure [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size) separately.
    - Support dynamically modifying [`min-blob-size`](/tikv-configuration-file.md#min-blob-size), [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression), and [`discardable-ratio`](/tikv-configuration-file.md#min-blob-size) to improve performance and flexibility when using the Titan engine.

  For more information, see [documentation](/storage-engine/titan-configuration.md).

### Performance

* BR improves snapshot restore speed (GA) [#50701](https://github.com/pingcap/tidb/issues/50701) @[3pointer](https://github.com/3pointer) @[Leavrth](https://github.com/Leavrth)

  Starting from TiDB v8.0.0, the acceleration of snapshot restore speed is now generally available (GA) and enabled by default. BR improves the snapshot restore speed significantly by implementing various optimizations such as adopting the coarse-grained Region scattering algorithm, creating databases and tables in batches, reducing the mutual impact between SST file downloads and ingest operations, and accelerating the restore of table statistics. According to test results from real-world cases, the data restore speed of a single TiKV node stabilizes at 1.2 GiB/s, and 100 TiB of data can be restored within one hour.

  This means that even in high-load environments, BR can fully utilize the resources of each TiKV node, significantly reducing database restore time, enhancing the availability and reliability of databases, and reducing downtime and business losses caused by data loss or system failures. Note that the increase in restore speed is attributed to the parallel execution of a large number of goroutines, which can result in significant memory consumption, especially when there are many tables or Regions. It is recommended to use machines with higher memory capacity to run the BR client. If the memory capacity of the machine is limited, it is recommended to use a finer-grained Region scattering algorithm. In addition, because the coarse-grained Region scattering algorithm might consume a significant amount of external storage bandwidth, you need to avoid any impact on other applications due to insufficient external bandwidth.

  For more information, see [documentation](/br/br-snapshot-guide.md#restore-cluster-snapshots).

* Support pushing down the following functions to TiFlash [#50975](https://github.com/pingcap/tidb/issues/50975) [#50485](https://github.com/pingcap/tidb/issues/50485) @[yibin87](https://github.com/yibin87) @[windtalker](https://github.com/windtalker)

    * `CAST(DECIMAL AS DOUBLE)`
    * `POWER()`

  For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* The parallel HashAgg algorithm of TiDB supports disk spill (experimental) [#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008)

    In earlier versions of TiDB, the concurrency algorithm of the HashAgg operator does not support disk spill. If the execution plan of a SQL statement contains the parallel HashAgg operator, all the data for that SQL statement can only be processed in memory. Consequently, TiDB has to process a large amount of data in memory. When the data size exceeds the memory limit, TiDB can only choose the non-parallel algorithm, which does not leverage concurrency for performance improvement.

     In v8.0.0, the parallel HashAgg algorithm of TiDB supports disk spill. Under any parallel conditions, the HashAgg operator can automatically trigger data spill based on memory usage, thus balancing performance and data throughput. Currently, as an experimental feature, TiDB introduces the `tidb_enable_parallel_hashagg_spill` variable to control whether to enable the parallel HashAgg algorithm that supports disk spill. When this variable is `ON`, it means enabled. This variable will be deprecated after the feature is generally available in a future release.

    For more information, see [documentation](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800).

* Introduce the priority queue for automatic statistics collection [#50132](https://github.com/pingcap/tidb/issues/50132) @[hi-rustin](https://github.com/Rustin170506)

    Maintaining optimizer statistics up-to-date is the key to stabilizing database performance. Most users rely on the [automatic statistics collection](/statistics.md#automatic-update) provided by TiDB to collect the latest statistics. Automatic statistics collection checks the status of statistics for all objects, and adds unhealthy objects to a queue for sequential collections. In previous versions, the order is random, which could result in excessive waits for more worthy candidates to be updated, causing potential performance regressions.

    Starting from v8.0.0, automatic statistics collection dynamically sets priorities for objects in combination with a variety of conditions to ensure that more deserving candidates are processed in priority, such as newly created indexes and partitioned tables with definition changes. Additionally, TiDB prioritizes tables with lower health scores, placing them at the top of the queue. This enhancement makes the order of collection more reasonable, and reduces performance problems caused by outdated statistics, therefore improving database stability.

    For more information, see [documentation](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800).

* Remove some limitations on execution plan cache [#49161](https://github.com/pingcap/tidb/pull/49161) @[mjonss](https://github.com/mjonss) @[qw4990](https://github.com/qw4990)

    TiDB supports [plan cache](/sql-prepared-plan-cache.md), which can effectively reduce the latency of OLTP systems and is important for performance. In v8.0.0, TiDB removes several limitations on plan cache. Execution plans with the following items can be cached now:

    - [Partitioned tables](/partitioned-table.md)
    - [Generated columns](/generated-columns.md), including objects that depend on generated columns (such as [multi-valued indexes](/choose-index.md#multi-valued-indexes-and-plan-cache))

  This enhancement extends the use cases of plan cache and improves the overall database performance in complex scenarios.

    For more information, see [documentation](/sql-prepared-plan-cache.md).

* Optimizer enhances support for multi-valued indexes [#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx) @[time-and-fate](https://github.com/time-and-fate)

    TiDB v6.6.0 introduces [multi-value indexes](/sql-statements/sql-statement-create-index.md#multi-valued-indexes) to improve query performance for JSON data types. In v8.0.0, the optimizer enhances its support for multi-valued indexes and can correctly identify and utilize them to optimize queries in complex scenarios.

    * The optimizer collects statistics on multi-valued indexes and decides execution plans with the statistics. If several multi-value indexes can be selected by a SQL statement, the optimizer can identify the one with lower cost.
    * When using `OR` to connect multiple `member of` conditions, the optimizer can match an effective index partial path for each DNF item (a `member of` condition) and combine these paths using Union to form an `Index Merge`. This achieves more efficient condition filtering and data fetch.

  For more information, see [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-indexes).

* Support configuring the update interval for low-precision TSO [#51081](https://github.com/pingcap/tidb/issues/51081) @[Tema](https://github.com/Tema)

    The [low-precision TSO feature](/system-variables.md#tidb_low_resolution_tso) in TiDB uses regularly updated TSO as the transaction timestamp. In scenarios where reading outdated data is acceptable, this feature reduces the overhead of obtaining TSO for small read-only transactions by sacrificing real-time performance and improves the ability of high-concurrency reads.

    Before v8.0.0, the TSO update interval of low-precision TSO feature is fixed and cannot be adjusted according to actual application requirements. In v8.0.0, TiDB introduces the system variable `tidb_low_resolution_tso_update_interval` to control the TSO update interval. This feature takes effect only when the low-precision TSO feature is enabled.

    For more information, see [documentation](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800).

### Availability

* The proxy component TiProxy becomes generally available (GA) [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox)

    TiDB v7.6.0 introduces the proxy component TiProxy as an experimental feature. TiProxy is the official proxy component of TiDB, located between the client and TiDB server. It provides load balancing and connection persistence functions for TiDB, making the workload of the TiDB cluster more balanced and not affecting user access to the database during maintenance operations.

    In v8.0.0, TiProxy becomes generally available and enhances the automatic generation of signature certificates and monitoring functions.

    The usage scenarios of TiProxy are as follows:

    - During maintenance operations such as rolling restarts, rolling upgrades, and scaling-in in a TiDB cluster, changes occur in the TiDB servers which result in interruptions in connections between clients and the TiDB servers. By using TiProxy, connections can be smoothly migrated to other TiDB servers during these maintenance operations so that clients are not affected.
    - Client connections to a TiDB server cannot be dynamically migrated to other TiDB servers. When the workload of multiple TiDB servers is unbalanced, it might result in a situation where the overall cluster resources are sufficient, but certain TiDB servers experience resource exhaustion leading to a significant increase in latency. To address this issue, TiProxy provides dynamic migration for connection, which allows connections to be migrated from one TiDB server to another without any impact on the clients, thereby achieving load balancing for the TiDB cluster.

  TiProxy has been integrated into TiUP, TiDB Operator, and TiDB Dashboard, making it easy to configure, deploy, and maintain.

    For more information, see [documentation](/tiproxy/tiproxy-overview.md).

### SQL

* Support a new DML type for handling a large amount of data (experimental) [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium)

    Before v8.0.0, TiDB stores all transaction data in memory before committing. When processing a large amount of data, the memory required for transactions becomes a bottleneck that limits the transaction size that TiDB can handle. Although TiDB introduces non-transactional DML to attempt to solve the transaction size limitation by splitting SQL statements, this feature has various limitations and does not provide an ideal experience in actual scenarios.

    Starting from v8.0.0, TiDB supports a DML type for handling a large amount of data. This DML type writes data to TiKV in a timely manner during execution, avoiding the continuous storage of all transaction data in memory, and thus supports handling a large amount of data that exceeds the memory limit. This DML type ensures transaction integrity and uses the same syntax as standard DML. `INSERT`, `UPDATE`, `REPLACE`, and `DELETE` statements can use this new DML type to execute large-scale DML operations.

    This DML type is implemented by the [Pipelined DML](https://github.com/pingcap/tidb/blob/master/docs/design/2024-01-09-pipelined-DML.md) feature and only takes effect on statements with auto-commit enabled. You can control whether to enable this DML type by setting the system variable [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800).

    For more information, see [documentation](/system-variables.md#tidb_dml_type-new-in-v800).

* Support using some expressions to set default column values when creating a table (experimental) [#50936](https://github.com/pingcap/tidb/issues/50936) @[zimulala](https://github.com/zimulala)

    Before v8.0.0, when you create a table, the default value of a column is limited to strings, numbers, and dates. Starting from v8.0.0, you can use some expressions as the default column values. For example, you can set the default value of a column to `UUID()`. This feature helps you meet more diverse requirements.

    For more information, see [documentation](/data-type-default-values.md#specify-expressions-as-default-values).

* Support the `div_precision_increment` system variable [#51501](https://github.com/pingcap/tidb/issues/51501) @[yibin87](https://github.com/yibin87)

    MySQL 8.0 supports the variable `div_precision_increment`, which specifies the number of digits by which to increase the scale of the result of a division operation performed using the `/` operator. Before v8.0.0, TiDB does not support this variable, and division is performed to 4 decimal places. Starting from v8.0.0, TiDB supports this variable. You can specify the number of digits by which to increase the scale of the result of a division operation as desired.

    For more information, see [documentation](/system-variables.md#div_precision_increment-new-in-v800).

### DB operations

* PITR supports Amazon S3 Object Lock [#51184](https://github.com/pingcap/tidb/issues/51184) @[RidRisR](https://github.com/RidRisR)

    Amazon S3 Object Lock can help prevent backup data from accidental or intentional deletion during a specified retention period, enhancing the security and integrity of data. Starting from v6.3.0, BR supports Amazon S3 Object Lock for snapshot backups, adding an additional layer of security for full backups. Starting from v8.0.0, PITR also supports Amazon S3 Object Lock. Whether for full backups or log data backups, the Object Lock feature ensures more reliable data protection, further strengthening the security of data backup and recovery and meeting regulatory requirements.

    For more information, see [documentation](/br/backup-and-restore-storages.md#other-features-supported-by-the-storage-service).

* Support making invisible indexes visible at the session level [#50653](https://github.com/pingcap/tidb/issues/50653) @[hawkingrei](https://github.com/hawkingrei)

    By default, the optimizer does not select [invisible indexes](/sql-statements/sql-statement-create-index.md#invisible-index). This mechanism is usually used to evaluate whether to delete an index. If there is uncertainty about the potential performance impact of deleting an index, you have the option to set the index to invisible temporarily and promptly restore it to visible when needed.

    Starting from v8.0.0, you can set the session-level system variable [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800) to `ON` to make the current session aware of invisible indexes. With this feature, you can create a new index and test its performance by making the index visible first, and then modifying the system variable in the current session for testing without affecting other sessions. This improvement enhances the safety of SQL tuning and helps to improve the stability of production databases.

    For more information, see [documentation](/sql-statements/sql-statement-create-index.md#invisible-index).

* Support writing general logs to a separate file [#51248](https://github.com/pingcap/tidb/issues/51248) @[Defined2014](https://github.com/Defined2014)

    The general log is a MySQL-compatible feature that logs all executed SQL statements to help diagnose issues. TiDB also supports this feature. You can enable it by setting the variable [`tidb_general_log`](/system-variables.md#tidb_general_log). However, in previous versions, the content of general logs can only be written to the TiDB instance log along with other information, which is inconvenient for users who need to keep logs for a long time.

    Starting from v8.0.0, you can write the general log to a specified file by setting the configuration item [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800) to a valid filename. The general log follows the same rotation and retention policies as the instance log.

    In addition, to reduce the disk space occupied by historical log files, TiDB v8.0.0 introduces a native log compression option. You can set the configuration item [`log.file.compression`](/tidb-configuration-file.md#compression-new-in-v800) to `gzip` to automatically compress rotated logs using the [`gzip`](https://www.gzip.org/) format.

    For more information, see [documentation](/tidb-configuration-file.md#general-log-file-new-in-v800).

### Observability

* Support monitoring index usage statistics [#49830](https://github.com/pingcap/tidb/issues/49830) @[YangKeao](https://github.com/YangKeao)

    Proper index design is a crucial prerequisite to maintaining database performance. TiDB v8.0.0 introduces the [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) table, which records the statistics of all indexes on the current TiDB node, including the following information:

    * The cumulative execution count of statements that scan the index
    * The total number of rows scanned when accessing the index
    * The selectivity distribution when scanning the index
    * The time of the most recent access to the index

  With this information, you can identify indexes that are not used by the optimizer and indexes with poor selectivity, thereby optimizing index design to improve database performance.

    Additionally, TiDB v8.0.0 introduces a view [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md), which is compatible with MySQL. This view shows indexes that have not been used since the last start of TiDB instances. For clusters upgraded from versions earlier than v8.0.0, the `sys` schema and the views are not created automatically. You can manually create them by referring to [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md#manually-create-the-schema_unused_indexes-view).

    For more information, see [documentation](/information-schema/information-schema-tidb-index-usage.md).

### Security

* TiKV encryption at rest supports Google [Key Management Service (Cloud KMS)](https://cloud.google.com/docs/security/key-management-deep-dive?hl) (experimental) [#8906](https://github.com/tikv/tikv/issues/8906) @[glorv](https://github.com/glorv)

    TiKV ensures data security by encrypting stored data using the encryption at rest technique. The core of encryption at rest for security is key management. Starting from v8.0.0, you can manage the master key of TiKV using Google Cloud KMS to establish encryption-at-rest capabilities based on Cloud KMS, thereby enhancing the security of user data.

    To enable encryption at rest based on Google Cloud KMS, you need to create a key on Google Cloud and then configure the `[security.encryption.master-key]` section in the TiKV configuration file.

    For more information, see [documentation](/encryption-at-rest.md#tikv-encryption-at-rest).

* Enhance TiDB log desensitization [#51306](https://github.com/pingcap/tidb/issues/51306) @[xhebox](https://github.com/xhebox)

    The enhancement of TiDB log desensitization is based on marking SQL text information in log files, facilitating the safe display of sensitive data when users view the logs. You can control whether to desensitize log information to enable secure use of TiDB logs in different scenarios, enhancing the security and flexibility of using log desensitization. To use this feature, set the system variable `tidb_redact_log` to `MARKER`. This marks the SQL text in TiDB logs. When you view the logs, sensitive data is securely displayed based on the markers, thus protecting the log information.

    For more information, see [documentation](/system-variables.md#tidb_redact_log).

### Data migration

* TiCDC adds support for the Simple protocol [#9898](https://github.com/pingcap/tiflow/issues/9898) @[3AceShowHand](https://github.com/3AceShowHand)

    TiCDC introduces a new protocol, the Simple protocol. This protocol provides in-band schema tracking capabilities by embedding table schema information in DDL and BOOTSTRAP events.

    For more information, see [documentation](/ticdc/ticdc-simple-protocol.md).

* TiCDC adds support for the Debezium format protocol [#1799](https://github.com/pingcap/tiflow/issues/1799) @[breezewish](https://github.com/breezewish)

    TiCDC can now publish data change events to a Kafka sink using a protocol that generates event messages in a Debezium style format. This helps to simplify the migration from MySQL to TiDB for users who are currently using Debezium to pull data from MySQL for downstream processing.

    For more information, see [documentation](/ticdc/ticdc-debezium.md).

* DM supports using a user-provided secret key to encrypt and decrypt passwords of source and target databases [#9492](https://github.com/pingcap/tiflow/issues/9492) @[D3Hunter](https://github.com/D3Hunter)

    In earlier versions, DM uses a built-in fixed secret key with relatively low security. Starting from v8.0.0, you can upload and specify a secret key file for encrypting and decrypting passwords of upstream and downstream databases. In addition, you can replace the secret key file as needed to enhance data security.

    For more information, see [documentation](/dm/dm-customized-secret-key.md).

* Supports the `IMPORT INTO ... FROM SELECT` syntax to enhance the `IMPORT INTO` functionality (experimental) [#49883](https://github.com/pingcap/tidb/issues/49883) @[D3Hunter](https://github.com/D3Hunter)

    In earlier TiDB versions, importing query results into a target table could only be done using the `INSERT INTO ... SELECT` statement, which is relatively inefficient in some large dataset scenarios. Starting from v8.0.0, TiDB enables you to use `IMPORT INTO ... FROM SELECT` to import the results of a `SELECT` query into an empty TiDB target table, which achieves up to 8 times the performance of `INSERT INTO ... SELECT` and significantly reduces the import time.

    In addition, you can use `IMPORT INTO ... FROM SELECT` to import historical data queried with [`AS OF TIMESTAMP`](/as-of-timestamp.md).

   For more information, see [documentation](/sql-statements/sql-statement-import-into.md).

* TiDB Lightning simplifies conflict resolution strategies and supports handling conflicting data using the `replace` strategy (experimental) [#51036](https://github.com/pingcap/tidb/issues/51036) @[lyzx2001](https://github.com/lyzx2001)

    In earlier versions, TiDB Lightning has [one data conflict resolution strategy](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md#conflict-detection) for the logical import mode and [two data conflict resolution strategies](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection) for the physical import mode, which are not easy to understand and configure.

    Starting from v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) parameter, and simplifies the configuration of this parameter. In addition, in the physical import mode, the `replace` strategy now supports retaining the latest data and overwriting the old data when the import detects data with primary key or unique key conflicts.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-configuration.md).

* Global Sort becomes generally available (GA), improving the performance and stability of  `IMPORT INTO` significantly [#45719](https://github.com/pingcap/tidb/issues/45719) @[lance6716](https://github.com/lance6716)

    Before v7.4.0, when executing `IMPORT INTO` tasks using the [Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md), TiDB only locally sorts part of the data before importing it into TiKV due to limited local storage space. This results in significant overlap of the imported data in TiKV, requiring TiKV to perform additional compaction operations during import and affecting the TiKV performance and stability.

    With the Global Sort experimental feature introduced in v7.4.0, TiDB can temporarily store the data to be imported in an external storage (such as Amazon S3) for global sorting before importing it into TiKV, which eliminates the need for TiKV compaction operations during import. In v8.0.0, Global Sort becomes GA. This feature reduces the resource consumption of TiKV and significantly improves the performance and stability of `IMPORT INTO`. If you enable the Global Sort, each `IMPORT INTO` task supports importing data within 40 TiB.

   For more information, see [documentation](/tidb-global-sort.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.6.0 to the current version (v8.0.0). If you are upgrading from v7.5.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

- Upgrade the default Prometheus version deployed by TiUP from 2.27.1 to 2.49.1.
- Upgrade the default Grafana version deployed by TiUP from 7.5.11 to 7.5.17.
- Remove witness-related schedulers that are not GA but are enabled by default [#7765](https://github.com/tikv/pd/pull/7765) @[rleungx](https://github.com/rleungx)

### Behavior changes

* Prohibit setting [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610) to `ON` in Security Enhanced Mode (SEM) to prevent potential connectivity issues for users. [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
* DM removes the fixed secret key for encryption and decryption and enables you to customize a secret key for encryption and decryption. If encrypted passwords are used in [data source configurations](/dm/dm-source-configuration-file.md) and [migration task configurations](/dm/task-configuration-file-full.md) before the upgrade, you need to refer to the upgrade steps in [Customize a Secret Key for DM Encryption and Decryption](/dm/dm-customized-secret-key.md) for additional operations. [#9492](https://github.com/pingcap/tiflow/issues/9492) @[D3Hunter](https://github.com/D3Hunter)
* Before v8.0.0, after enabling the acceleration of `ADD INDEX` and `CREATE INDEX` (`tidb_ddl_enable_fast_reorg = ON`), the encoded index key ingests data to TiKV with a fixed concurrency of `16`, which cannot be dynamically adjusted according to the downstream TiKV capacity. Starting from v8.0.0, you can adjust the concurrency using the [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt) system variable. The default value is `4`. Compared with the previous default value of `16`, the new default value reduces performance when ingesting indexed key-value pairs. You can adjust this system variable based on the workload of your cluster.

### MySQL compatibility

* The `KEY` partition type supports statements with an empty list of partition fields, which is consistent with the behavior of MySQL.

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) | Deprecated | Starting from v8.0.0, this system variable is deprecated, and TiDB no longer supports automatic retries of optimistic transactions. It is recommended to use the [Pessimistic transaction mode](/pessimistic-transaction.md). If you encounter optimistic transaction conflicts, you can capture the error and retry transactions in your application. |
| `tidb_ddl_version` | Renamed | Controls whether to enable TiDB DDL V2. Starting from v8.0.0, this variable is renamed to [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) to better reflect its purpose. |
| [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) | Modified | Adds a control to whether to record the [usage statistics of indexes](/information-schema/information-schema-tidb-index-usage.md). The default value is `ON`. |
| [`tidb_redact_log`](/system-variables.md#tidb_redact_log) | Modified | Controls how to handle user information in SAL text when logging TiDB logs and slow logs. The value options are `OFF` (indicating not processing user information in the log) and `ON` (indicating hiding user information in the log). To provide a richer way of processing user information in the log, the `MARKER` option is added in v8.0.0 to support marking log information. |
| [`div_precision_increment`](/system-variables.md#div_precision_increment-new-in-v800) | Newly added | Controls the number of digits by which to increase the scale of the result of a division operation performed using the `/` operator. This variable is the same as MySQL. |
| [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) | Newly added | Controls the execution mode of DML statements. The value options are `"standard"` and `"bulk"`. |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) | Newly added | Controls whether to enable the priority queue to schedule the tasks of automatically collecting statistics. When this variable is enabled, TiDB prioritizes collecting statistics for the tables that most need statistics. |
| [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) | Newly added | Controls whether TiDB supports disk spill for the parallel HashAgg algorithm. When it is `ON`, disk spill can be triggered for the parallel HashAgg algorithm. This variable will be deprecated when this feature is generally available in a future release. |
| [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) | Newly added | Controls whether to enable [TiDB Accerates Table Creation](/accelerated-table-creation.md). Set the value to `ON` to enable it and `OFF` to disable it. The default value is `ON`. When this variable is enabled, TiDB accelerates table creation by using [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md). |
| [`tidb_load_binding_timeout`](/system-variables.md#tidb_load_binding_timeout-new-in-v800) | Newly added | Controls the timeout of loading bindings. If the execution time of loading bindings exceeds this value, the loading will stop. |
| [`tidb_low_resolution_tso_update_interval`](/system-variables.md#tidb_low_resolution_tso_update_interval-new-in-v800) | Newly added | Controls the interval for updating TiDB [cache timestamp](/system-variables.md#tidb_low_resolution_tso). |
| [`tidb_opt_ordering_index_selectivity_ratio`](/system-variables.md#tidb_opt_ordering_index_selectivity_ratio-new-in-v800) | Newly added | Controls the estimated number of rows for an index that matches the SQL statement `ORDER BY` when there are `ORDER BY` and `LIMIT` clauses in a SQL statement, but some filter conditions not covered by the index. The default value is `-1`, which means to disable this system variable. |
| [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800) | Newly added | Controls whether the optimizer can select [invisible indexes](/sql-statements/sql-statement-create-index.md#invisible-index) for query optimization in the current session. When the variable is set to `ON`, the optimizer can select invisible indexes for query optimization in the session. |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)  | Newly added | Controls the upper limit of memory that can be used for caching the schema information to avoid occupying too much memory. When this feature is enabled, the LRU algorithm is used to cache the required tables, effectively reducing the memory occupied by the schema information.    |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info) | Modified | Adds a control to whether to record the [usage statistics of indexes](/information-schema/information-schema-tidb-index-usage.md). The default value is `true`. |
| TiDB | [`tls-version`](/tidb-configuration-file.md#tls-version) | Modified | This parameter no longer supports `"TLSv1.0"` and `"TLSv1.1"`. Now it only supports `"TLSv1.2"` and `"TLSv1.3"`. |
| TiDB  | [`log.file.compression`](/tidb-configuration-file.md#compression-new-in-v800) | Newly added | Specifies the compression format of the polling log. The default value is null, which means that the polling log is not compressed. |
| TiDB  | [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800) | Newly added | Specifies the file to save the general log to. The default is null, which means that the general log will be written to the instance file. |
| TiDB | [`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800) | Newly added | Controls whether to use the new version of the Region replica selector when sending RPC requests to TiKV. The default value is `true`. |
| TiKV | [`log-backup.initial-scan-rate-limit`](/tikv-configuration-file.md#initial-scan-rate-limit-new-in-v620) | Modified | Adds a limit of `1MiB` as the minimum value. |
| TiKV | [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) | Modified | Changes the default value from `0` to `1` to improve TiKV performance, meaning that the size of the StoreWriter thread pool now defaults to `1`. |
| TiKV | [`rocksdb.defaultcf.titan.blob-cache-size`](/tikv-configuration-file.md#blob-cache-size) | Modified | Starting from v8.0.0, TiKV introduces the `shared-blob-cache` configuration item and enables it by default, so there is no need to set `blob-cache-size` separately. The configuration of `blob-cache-size` only takes effect when `shared-blob-cache` is set to `false`. |
| TiKV | [`security.encryption.master-key.vendor`](/encryption-at-rest.md#specify-a-master-key-via-kms) | Modified | Adds `gcp` as an available type for the service provider. |
| TiKV | [`rocksdb.defaultcf.titan.shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-new-in-v800) | Newly added | Controls whether to enable the shared cache for Titan blob files and RocksDB block files. The default value is `true`. |
| TiKV | [`security.encryption.master-key.gcp.credential-file-path`](/encryption-at-rest.md#specify-a-master-key-via-kms) | Newly added | Specifies the path to the Google Cloud authentication credentials file when `security.encryption.master-key.vendor` is `gcp`. |
| TiDB Lightning  | [`tikv-importer.duplicate-resolution`](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)  | Deprecated | Controls whether to detect and resolve unique key conflicts in physical import mode. Starting from v8.0.0, it is replaced by [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task). |
| TiDB Lightning  | [`conflict.precheck-conflict-before-import`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)  | Newly added | Controls whether to enable preprocess conflict detection, which checks conflicts in data before importing it to TiDB. The default value of this parameter is `false`, which means that TiDB Lightning only checks conflicts after the data import. This parameter can be used only in the physical import mode (`tikv-importer.backend = "local"`).  |
| TiDB Lightning  | [`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Newly added | Controls the maximum number of rows inserted per transaction in the logical import mode. The default value is `65536` rows. |
| TiDB Lightning  | [`logical-import-batch-size`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Newly added | Controls the maximum size of each SQL query executed on the downstream TiDB server in the logical import mode. The default value is `"96KiB"`. The unit can be KB, KiB, MB, or MiB. |
| Data Migration  |  [`secret-key-path`](/dm/dm-master-configuration-file.md) | Newly added | Specifies the file path of the secret key, which is used to encrypt and decrypt upstream and downstream passwords. The file must contain a 64-character hexadecimal AES-256 secret key. |
| TiCDC | [`tls-certificate-file`](/ticdc/ticdc-sink-to-pulsar.md) | Newly added | Specifies the path to the encrypted certificate file on the client, which is required when Pulsar enables TLS encrypted transmission. |
| TiCDC | [`tls-key-file-path`](/ticdc/ticdc-sink-to-pulsar.md) | Newly added | Specifies the path to the encrypted private key on the client, which is required when Pulsar enables TLS encrypted transmission. |

### System tables

* Add new system tables [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) and [`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage) to record index usage statistics on TiDB nodes.
* Add a new system schema [`sys`](/sys-schema/sys-schema.md) and a new view [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md), which records indexes that have not been used since the last start of TiDB.

## Deprecated features

- Starting from v8.0.0, the [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) system variable is deprecated, and TiDB no longer supports automatic retries of optimistic transactions. As an alternative, when encountering optimistic transaction conflicts, you can capture the error and retry transactions in your application, or use the [Pessimistic transaction mode](/pessimistic-transaction.md) instead.
- Starting from v8.0.0, TiDB no longer supports the TLSv1.0 and TLSv1.1 protocols. You must upgrade TLS to TLSv1.2 or TLSv1.3.
- Starting from v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, and enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) parameter. The [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) parameter for the old version of conflict detection will be removed in a future release.
- It is planned to redesign [the auto-evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.

## Improvements

+ TiDB

    - Improve the performance of executing the `CREATE TABLE` DDL statement by 10 times and support linear scalability [#50052](https://github.com/pingcap/tidb/issues/50052) @[GMHDBJD](https://github.com/GMHDBJD)
    - Support submitting 16 `IMPORT INTO ... FROM FILE` tasks simultaneously, facilitating bulk data import into target tables and significantly improving the efficiency and performance of importing data files [#49008](https://github.com/pingcap/tidb/issues/49008) @[D3Hunter](https://github.com/D3Hunter)
    - Improve the performance of spilling data to disk for the `Sort` operator [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Support canceling queries during spilling data to disk, which optimizes the exit mechanism of the data spill feature [#50511](https://github.com/pingcap/tidb/issues/50511) @[wshwsh12](https://github.com/wshwsh12)
    - Support using an index that matches partial conditions to construct Index Join when processing table join queries with multiple equal conditions [#47233](https://github.com/pingcap/tidb/issues/47233) @[winoros](https://github.com/winoros)
    - Enhance the capability of Index Merge to identify sorting requirements in queries and select indexes that meet the sorting requirements [#48359](https://github.com/pingcap/tidb/issues/48359) @[AilinKid](https://github.com/AilinKid)
    - When the `Apply` operator is not executed concurrently, TiDB enables you to view the name of the operator that blocks the concurrency by executing `SHOW WARNINGS` [#50256](https://github.com/pingcap/tidb/issues/50256) @[hawkingrei](https://github.com/hawkingrei)
    - Optimize the index selection for `point get` queries by selecting the most optimal index for queries when all indexes support `point get` queries [#50184](https://github.com/pingcap/tidb/issues/50184) @[elsa0520](https://github.com/elsa0520)
    - Temporarily adjust the priority of statistics synchronously loading tasks to high to avoid widespread timeouts during TiKV high loads, as these timeouts might result in statistics not being loaded [#50332](https://github.com/pingcap/tidb/issues/50332) @[winoros](https://github.com/winoros)
    - When the `PREPARE` statement fails to hit the execution plan cache, TiDB enables you to view the reason by executing `SHOW WARNINGS` [#50407](https://github.com/pingcap/tidb/issues/50407) @[hawkingrei](https://github.com/hawkingrei)
    - Improve the accuracy of query estimation information when the same row of data is updated multiple times [#47523](https://github.com/pingcap/tidb/issues/47523) @[terry1purcell](https://github.com/terry1purcell)
    - Index Merge supports embedding multi-value indexes and `OR` operators in `AND` predicates [#51778](https://github.com/pingcap/tidb/issues/51778) @[time-and-fate](https://github.com/time-and-fate)
    - When `force-init-stats` is set to `true`, TiDB waits for statistics initialization to finish before providing services during TiDB startup. This setting no longer blocks the startup of HTTP servers, which enables users to continue monitoring [#50854](https://github.com/pingcap/tidb/issues/50854) @[hawkingrei](https://github.com/hawkingrei)
    - MemoryTracker can track the memory usage of the `IndexLookup` operator [#45901](https://github.com/pingcap/tidb/issues/45901) @[solotzg](https://github.com/solotzg)
    - MemoryTracker can track the memory usage of the `MemTableReaderExec` operator [#51456](https://github.com/pingcap/tidb/issues/51456) @[wshwsh12](https://github.com/wshwsh12)
    - Support loading Regions in batch from PD to speed up the conversion process from the KV range to Regions when querying large tables [#51326](https://github.com/pingcap/tidb/issues/51326) @[SeaRise](https://github.com/SeaRise)
    - Optimize the query performance of the system tables `INFORMATION_SCHEMA.TABLES`, `INFORMATION_SCHEMA.STATISTICS`, `INFORMATION_SCHEMA.KEY_COLUMN_USAGE`, and `INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`. Compared with earlier versions, the performance has been improved by up to 100 times. [#50305](https://github.com/pingcap/tidb/issues/50305) @[ywqzzy](https://github.com/ywqzzy)

+ TiKV

    - Enhance TSO verification and detection to improve the robustness of the cluster TSO when the configuration or operation is improper [#16545](https://github.com/tikv/tikv/issues/16545) @[cfzjywxk](https://github.com/cfzjywxk)
    - Optimize the logic of cleaning up pessimistic locks to improve the processing performance of uncommitted transactions [#16158](https://github.com/tikv/tikv/issues/16158) @[cfzjywxk](https://github.com/cfzjywxk)
    - Introduce unified health control for TiKV to reduce the impact of abnormal single TiKV node on cluster access performance. You can disable this optimization by setting [`tikv-client.enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800) to `false`. [#16297](https://github.com/tikv/tikv/issues/16297) [#1104](https://github.com/tikv/client-go/issues/1104) [#1167](https://github.com/tikv/client-go/issues/1167) @[MyonKeminta](https://github.com/MyonKeminta) @[zyguan](https://github.com/zyguan) @[crazycs520](https://github.com/crazycs520)
    - The PD client uses the metadata storage interface to replace the previous global configuration interface [#14484](https://github.com/tikv/tikv/issues/14484) @[HuSharp](https://github.com/HuSharp)
    - Enhance the scanning performance by determining the data loading behavior through write cf stats [#16245](https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996)
    - Check the latest heartbeat for nodes being deleted and voters being demoted during the Raft conf change process to ensure that this behavior does not make the Region inaccessible [#15799](https://github.com/tikv/tikv/issues/15799) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Add Flush and BufferBatchGet interfaces for Pipelined DML [#16291](https://github.com/tikv/tikv/issues/16291) @[ekexium](https://github.com/ekexium)
    - Add monitoring and alerting for cgroup CPU and memory limits [#16392](https://github.com/tikv/tikv/issues/16392) @[pingandb](https://github.com/pingandb)
    - Add CPU monitoring for Region workers and snapshot generation workers [#16562](https://github.com/tikv/tikv/issues/16562) @[Connor1996](https://github.com/Connor1996)
    - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ PD

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

+ TiFlash

    - Support using non-constant values for the `json_path` argument in the `JSON_EXTRACT()` function [#8510](https://github.com/pingcap/tiflash/issues/8510) @[SeaRise](https://github.com/SeaRise)
    - Support the `JSON_LENGTH(json, path)` function [#8711](https://github.com/pingcap/tiflash/issues/8711) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR)

        - Introduce a new restore parameter `--load-stats` for the `br` command-line tool, which controls whether to restore statistics [#50568](https://github.com/pingcap/tidb/issues/50568) @[Leavrth](https://github.com/Leavrth)
        - Introduce a new restore parameter `--tikv-max-restore-concurrency` for the `br` command-line tool, which controls the maximum number of download and ingest files for each TiKV node. This parameter also controls the memory consumption of a BR node by controlling the maximum length of the job queue. [#51621](https://github.com/pingcap/tidb/issues/51621) @[3pointer](https://github.com/3pointer)
        - Enhance restore performance by enabling the coarse-grained Region scatter algorithm to adaptively obtain concurrent parameters [#50701](https://github.com/pingcap/tidb/issues/50701) @[3pointer](https://github.com/3pointer)
        - Display the `log` command in the command-line help information of `br` [#50927](https://github.com/pingcap/tidb/issues/50927) @[RidRisR](https://github.com/RidRisR)
        - Support pre-allocating Table ID during the restore process to maximize the reuse of Table ID and improve restore performance [#51736](https://github.com/pingcap/tidb/issues/51736) @[Leavrth](https://github.com/Leavrth)
        - Disable the GC memory limit tuner feature within TiDB when using BR to avoid OOM issues [#51078](https://github.com/pingcap/tidb/issues/51078) @[Leavrth](https://github.com/Leavrth)
        - Improve the speed of merging SST files during data restore by using a more efficient algorithm [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - Support creating databases in batch during data restore [#50767](https://github.com/pingcap/tidb/issues/50767) @[Leavrth](https://github.com/Leavrth)
        - Print the information of the slowest Region that affects global checkpoint advancement in logs and metrics during log backups [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - Improve the table creation performance of the `RESTORE` statement in scenarios with large datasets [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - Optimize the memory consumption of `RowChangedEvent` to reduce memory consumption when TiCDC replicates data [#10386](https://github.com/pingcap/tiflow/issues/10386) @[lidezhu](https://github.com/lidezhu)
        - Verify that the start-ts parameter is valid when creating and resuming a changefeed task [#10499](https://github.com/pingcap/tiflow/issues/10499) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - In a MariaDB primary-secondary replication scenario, where the migration path is: MariaDB primary instance -> MariaDB secondary instance -> DM -> TiDB, when `gtid_strict_mode = off` and the GTID of the MariaDB secondary instance is not strictly incrementing (for example, there is data writing to the MariaDB secondary instance), the DM task will report an error `less than global checkpoint position`. Starting from v8.0.0, TiDB is compatible with this scenario and data can be migrated downstream normally. [#10741](https://github.com/pingcap/tiflow/issues/10741) @[okJiang](https://github.com/okJiang)

    + TiDB Lightning

        - Support configuring the maximum number of rows in a batch in logical import mode using [`logical-import-batch-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) [#46607](https://github.com/pingcap/tidb/issues/46607) @[kennytm](https://github.com/kennytm)
        - TiDB Lightning reports an error when the space of TiFlash is insufficient [#50324](https://github.com/pingcap/tidb/issues/50324) @[okJiang](https://github.com/okJiang)

## Bug fixes

+ TiDB

    - Fix the issue that `auto analyze` is triggered multiple times when there is no data change [#51775](https://github.com/pingcap/tidb/issues/51775) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that the `auto analyze` concurrency is set incorrectly [#51749](https://github.com/pingcap/tidb/issues/51749) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue of index inconsistency caused by adding multiple indexes using a single SQL statement [#51746](https://github.com/pingcap/tidb/issues/51746) @[tangenta](https://github.com/tangenta)
    - Fix the `Column ... in from clause is ambiguous` error that might occur when a query uses `NATURAL JOIN` [#32044](https://github.com/pingcap/tidb/issues/32044) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue of wrong query results due to TiDB incorrectly eliminating constant values in `group by` [#38756](https://github.com/pingcap/tidb/issues/38756) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that the `LEADING` hint does not take effect in `UNION ALL` statements [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `BIT` type columns might cause query errors due to decode failures when they are involved in calculations of some functions [#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that TiDB might panic when performing a rolling upgrade using `tiup cluster upgrade/start` due to an interaction issue with PD [#50152](https://github.com/pingcap/tidb/issues/50152) @[zimulala](https://github.com/zimulala)
    - Fix the issue that executing `UNIQUE` index lookup with an `ORDER BY` clause might cause an error [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    - Fix the issue that TiDB returns wrong query results when processing `ENUM` or `SET` types by constant propagation [#49440](https://github.com/pingcap/tidb/issues/49440) @[winoros](https://github.com/winoros)
    - Fix the issue that TiDB might panic when a query contains the Apply operator and the `fatal error: concurrent map writes` error occurs [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue that the control of `SET_VAR` for variables of the string type might become invalid [#50507](https://github.com/pingcap/tidb/issues/50507) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the `SYSDATE()` function incorrectly uses the time in the plan cache when `tidb_sysdate_is_now` is set to `1` [#49299](https://github.com/pingcap/tidb/issues/49299) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that when executing the `CREATE GLOBAL BINDING` statement, if the schema name is in uppercase, the binding does not take effect [#50646](https://github.com/pingcap/tidb/issues/50646) @[qw4990](https://github.com/qw4990)
    - Fix the issue that `Index Path` selects duplicated indexes [#50496](https://github.com/pingcap/tidb/issues/50496) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that `PLAN REPLAYER` fails to load bindings when the `CREATE GLOBAL BINDING` statement contains `IN()` [#43192](https://github.com/pingcap/tidb/issues/43192) @[King-Dylan](https://github.com/King-Dylan)
    - Fix the issue that when multiple `analyze` tasks fail, the failure reasons are not recorded correctly [#50481](https://github.com/pingcap/tidb/issues/50481) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that `tidb_stats_load_sync_wait` does not take effect [#50872](https://github.com/pingcap/tidb/issues/50872) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that `max_execute_time` settings at multiple levels interfere with each other [#50914](https://github.com/pingcap/tidb/issues/50914) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue of thread safety caused by concurrent updating of statistics [#50835](https://github.com/pingcap/tidb/issues/50835) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that executing `auto analyze` on a partition table might cause TiDB to panic [#51187](https://github.com/pingcap/tidb/issues/51187) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that SQL bindings might not work when `IN()` in a SQL statement contains a different number of values [#51222](https://github.com/pingcap/tidb/issues/51222) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that TiDB cannot correctly convert the type of a system variable in an expression [#43527](https://github.com/pingcap/tidb/issues/43527) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that TiDB does not listen to the corresponding port when `force-init-stats` is configured [#51473](https://github.com/pingcap/tidb/issues/51473) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that in `determinate` mode (`tidb_opt_objective='determinate'`), if a query does not contain predicates, statistics might not be loaded [#48257](https://github.com/pingcap/tidb/issues/48257) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that the `init-stats` process might cause TiDB to panic and the `load stats` process to quit [#51581](https://github.com/pingcap/tidb/issues/51581) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the query result is incorrect when the `IN()` predicate contains `NULL` [#51560](https://github.com/pingcap/tidb/issues/51560) @[winoros](https://github.com/winoros)
    - Fix the issue that blocked DDL statements are not displayed in the MDL View when a DDL task involves multiple tables [#47743](https://github.com/pingcap/tidb/issues/47743) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the `processed_rows` of the `ANALYZE` task on a table might exceed the total number of rows in that table [#50632](https://github.com/pingcap/tidb/issues/50632) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the goroutine leak issue that might occur when the `HashJoin` operator fails to spill to disk [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the goroutine leak issue that occurs when the memory usage of CTE queries exceed limits [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the `Can't find column ...` error that might occur when aggregate functions are used for group calculations [#50926](https://github.com/pingcap/tidb/issues/50926) @[qw4990](https://github.com/qw4990)
    - Fix the issue that DDL operations such as renaming tables are stuck when the `CREATE TABLE` statement contains specific partitions or constraints [#50972](https://github.com/pingcap/tidb/issues/50972) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the monitoring metric `tidb_statistics_auto_analyze_total` on Grafana is not displayed as an integer [#51051](https://github.com/pingcap/tidb/issues/51051) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `tidb_gogc_tuner_threshold` system variable is not adjusted accordingly after the `tidb_server_memory_limit` variable is modified [#48180](https://github.com/pingcap/tidb/issues/48180) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `index out of range` error might occur when a query involves JOIN operations [#42588](https://github.com/pingcap/tidb/issues/42588) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that getting the default value of a column returns an error if the column default value is dropped [#50043](https://github.com/pingcap/tidb/issues/50043) [#51324](https://github.com/pingcap/tidb/issues/51324) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that wrong results might be returned when TiFlash late materialization processes associated columns [#49241](https://github.com/pingcap/tidb/issues/49241) [#51204](https://github.com/pingcap/tidb/issues/51204) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that the `LIKE()` function might return wrong results when processing binary collation inputs [#50393](https://github.com/pingcap/tidb/issues/50393) @[yibin87](https://github.com/yibin87)
    - Fix the issue that the `JSON_LENGTH()` function returns wrong results when the second parameter is `NULL` [#50931](https://github.com/pingcap/tidb/issues/50931) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue that `CAST(AS DATETIME)` might lose time precision under certain circumstances [#49555](https://github.com/pingcap/tidb/issues/49555) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue that parallel `Apply` might generate incorrect results when the table has a clustered index [#51372](https://github.com/pingcap/tidb/issues/51372) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that `ALTER TABLE ... COMPACT TIFLASH REPLICA` might incorrectly end when the primary key type is `VARCHAR` [#51810](https://github.com/pingcap/tidb/issues/51810) @[breezewish](https://github.com/breezewish)
    - Fix the issue that the check on the `NULL` value of the `DEFAULT NULL` attribute is incorrect when exchanging partitioned tables using the `EXCHANGE PARTITION` statement [#47167](https://github.com/pingcap/tidb/issues/47167) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that the partition table definition might cause wrong behavior when using a non-UTF8 character set [#49251](https://github.com/pingcap/tidb/issues/49251) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that incorrect default values are displayed in the `INFORMATION_SCHEMA.VARIABLES_INFO` table for some system variables [#49461](https://github.com/pingcap/tidb/issues/49461) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that no error is reported when empty strings are used as database names in some cases [#45873](https://github.com/pingcap/tidb/issues/45873) @[yoshikipom](https://github.com/yoshikipom)
    - Fix the issue that the `SPLIT TABLE ... INDEX` statement might cause TiDB to panic [#50177](https://github.com/pingcap/tidb/issues/50177) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that querying a partitioned table of `KeyPartition` type might cause an error [#50206](https://github.com/pingcap/tidb/issues/50206) [#51313](https://github.com/pingcap/tidb/issues/51313) [#51196](https://github.com/pingcap/tidb/issues/51196) @[time-and-fate](https://github.com/time-and-fate) @[jiyfhust](https://github.com/jiyfhust) @[mjonss](https://github.com/mjonss)
    - Fix the issue that querying a Hash partitioned table might produce incorrect results [#50427](https://github.com/pingcap/tidb/issues/50427) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that opentracing does not work correctly [#50508](https://github.com/pingcap/tidb/issues/50508) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the error message is not complete when `ALTER INSTANCE RELOAD TLS` reports an error [#50699](https://github.com/pingcap/tidb/issues/50699) @[dveeden](https://github.com/dveeden)
    - Fix the issue that the `AUTO_INCREMENT` attribute causes non-consecutive IDs due to unnecessary transaction conflicts when assigning auto-increment IDs [#50819](https://github.com/pingcap/tidb/issues/50819) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue of incomplete stack information in TiDB logs for some errors [#50849](https://github.com/pingcap/tidb/issues/50849) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue of excessive memory usage in some queries when the number in the `LIMIT` clause is too large [#51188](https://github.com/pingcap/tidb/issues/51188) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the TTL feature causes data hotspots due to incorrect data range splitting in some cases [#51527](https://github.com/pingcap/tidb/issues/51527) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the `SET` statement does not take effect when it appears on the first line of an explicit transaction [#51387](https://github.com/pingcap/tidb/issues/51387) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that querying JSON of `BINARY` type might cause an error in some cases [#51547](https://github.com/pingcap/tidb/issues/51547) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that TTL does not handle the transition for daylight saving time adjustments correctly when calculating expiration times [#51675](https://github.com/pingcap/tidb/issues/51675) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the `SURVIVAL_PREFERENCES` attribute might not appear in the output of the `SHOW CREATE PLACEMENT POLICY` statement under certain conditions [#51699](https://github.com/pingcap/tidb/issues/51699) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the configuration file does not take effect when it contains an invalid configuration item [#51399](https://github.com/pingcap/tidb/issues/51399) @[Defined2014](https://github.com/Defined2014)

+ TiKV

    - Fix the issue that enabling `tidb_enable_row_level_checksum` might cause TiKV to panic [#16371](https://github.com/tikv/tikv/issues/16371) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue that hibernated Regions are not promptly awakened in exceptional circumstances [#16368](https://github.com/tikv/tikv/issues/16368) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that the entire Region becomes unavailable when one replica is offline, by checking the last heartbeat time of all replicas of the Region before taking a node offline [#16465](https://github.com/tikv/tikv/issues/16465) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Fix the issue that JSON integers greater than the maximum `INT64` value but less than the maximum `UINT64` value are parsed as `FLOAT64` by TiKV, resulting in inconsistency with TiDB [#16512](https://github.com/tikv/tikv/issues/16512) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the monitoring metric `tikv_unified_read_pool_thread_count` has no data in some cases [#16629](https://github.com/tikv/tikv/issues/16629) @[YuJuncen](https://github.com/YuJuncen)

+ PD

    - Fix the issue that data race occurs when the `MergeLabels` function is called [#7535](https://github.com/tikv/pd/issues/7535) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that there is no output when the `evict-leader-scheduler` interface is called [#7672](https://github.com/tikv/pd/issues/7672) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that the PD monitoring item `learner-peer-count` does not synchronize the old value after a leader switch [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the memory leak issue that occurs when `watch etcd` is not turned off correctly [#7807](https://github.com/tikv/pd/issues/7807) @[rleungx](https://github.com/rleungx)
    - Fix the issue that some TSO logs do not print the error cause [#7496](https://github.com/tikv/pd/issues/7496) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that there are unexpected negative monitoring metrics after restart [#4489](https://github.com/tikv/pd/issues/4489) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that the Leader lease expires later than the log time [#7700](https://github.com/tikv/pd/issues/7700) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that TiDB panics when TLS switches between TiDB (the PD client) and PD are inconsistent [#7900](https://github.com/tikv/pd/issues/7900) [#7902](https://github.com/tikv/pd/issues/7902) [#7916](https://github.com/tikv/pd/issues/7916) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that Goroutine leaks when it is not closed properly [#7782](https://github.com/tikv/pd/issues/7782) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that pd-ctl cannot remove a scheduler that contains special characters [#7798](https://github.com/tikv/pd/issues/7798) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that the PD client might be blocked when obtaining TSO [#7864](https://github.com/tikv/pd/issues/7864) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiFlash

    - Fix the issue that TiFlash might panic due to unstable network connections with PD during replica migration [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the memory usage increases significantly due to slow queries [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that removing and then re-adding TiFlash replicas might lead to data corruption in TiFlash [#8695](https://github.com/pingcap/tiflash/issues/8695) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash replica data might be accidentally deleted after performing point-in-time recovery (PITR) or executing `FLASHBACK CLUSTER TO`, which might result in data anomalies [#8777](https://github.com/pingcap/tiflash/issues/8777) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash panics after executing `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`, which changes nullable columns to non-nullable [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that in the disaggregated storage and compute architecture, queries might be permanently blocked after network isolation [#8806](https://github.com/pingcap/tiflash/issues/8806) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that in the disaggregated storage and compute architecture, TiFlash might panic during shutdown [#8837](https://github.com/pingcap/tiflash/issues/8837) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might crash due to data race in case of remote reads [#8685](https://github.com/pingcap/tiflash/issues/8685) @[solotzg](https://github.com/solotzg)
    - Fix the issue that the `CAST(AS JSON)` function does not de-duplicate the JSON object key [#8712](https://github.com/pingcap/tiflash/issues/8712) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue that the `ENUM` column might cause TiFlash to crash during chunk encoding [#8674](https://github.com/pingcap/tiflash/issues/8674) @[yibin87](https://github.com/yibin87)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the log backup checkpoint gets stuck when a Region is split or merged immediately after it becomes a leader [#16469](https://github.com/tikv/tikv/issues/16469) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that TiKV panics when a full backup fails to find a peer in some extreme cases [#16394](https://github.com/tikv/tikv/issues/16394) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that log backup gets stuck after changing the TiKV IP address on the same node [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)
        - Fix the issue that BR cannot retry when encountering an error while reading file content from S3 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that when resuming from a checkpoint after data restore fails, an error `the target cluster is not fresh` occurs [#50232](https://github.com/pingcap/tidb/issues/50232) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that stopping a log backup task causes TiDB to crash [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that data restore is slowed down due to absence of a leader on a TiKV node [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that full restore still requires the target cluster to be empty after the `--filter` option is specified [#51009](https://github.com/pingcap/tidb/issues/51009) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Fix the issue that the file sequence number generated by the storage service might not increment correctly when using the storage sink [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC returns the `ErrChangeFeedAlreadyExists` error when concurrently creating multiple changefeeds [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that after filtering out `add table partition` events is configured in `ignore-event`, TiCDC does not replicate other types of DML changes for related partitions to the downstream [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the changefeed reports an error after `TRUNCATE PARTITION` is executed on the upstream table [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that `snapshot lost caused by GC` is not reported in time when resuming a changefeed and the `checkpoint-ts` of the changefeed is smaller than the GC safepoint of TiDB [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC fails to validate `TIMESTAMP` type checksum due to time zone mismatch after data integrity validation for single-row data is enabled [#10573](https://github.com/pingcap/tiflow/issues/10573) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the Syncpoint table might be incorrectly replicated [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that OAuth2.0, TLS, and mTLS cannot be enabled properly when using Apache Pulsar as the downstream [#10602](https://github.com/pingcap/tiflow/issues/10602) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that a changefeed might get stuck when TiKV upgrades, restarts, or evicts a leader [#10584](https://github.com/pingcap/tiflow/issues/10584) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that data is written to a wrong CSV file due to wrong BarrierTS in scenarios where DDL statements are executed frequently [#10668](https://github.com/pingcap/tiflow/issues/10668) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that data race in the KV client causes TiCDC to panic [#10718](https://github.com/pingcap/tiflow/issues/10718) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue TiCDC panics when scheduling table replication tasks [#10613](https://github.com/pingcap/tiflow/issues/10613) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - Fix the issue that data is lost when the upstream primary key is of binary type [#10672](https://github.com/pingcap/tiflow/issues/10672) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - Fix the performance regression issue caused by checking TiKV space [#43636](https://github.com/pingcap/tidb/issues/43636) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning reports an error when encountering invalid symbolic link files during file scanning [#49423](https://github.com/pingcap/tidb/issues/49423) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning fails to correctly parse date values containing `0` when `NO_ZERO_IN_DATE` is not included in `sql_mode` [#50757](https://github.com/pingcap/tidb/issues/50757) @[GMHDBJD](https://github.com/GMHDBJD)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [Aoang](https://github.com/Aoang)
- [bufferflies](https://github.com/bufferflies)
- [daemon365](https://github.com/daemon365)
- [eltociear](https://github.com/eltociear)
- [lichunzhu](https://github.com/lichunzhu)
- [jiyfhust](https://github.com/jiyfhust)
- [pingandb](https://github.com/pingandb)
- [shenqidebaozi](https://github.com/shenqidebaozi)
- [Smityz](https://github.com/Smityz)
- [songzhibin97](https://github.com/songzhibin97)
- [tangjingyu97](https://github.com/tangjingyu97)
- [Tema](https://github.com/Tema)
- [ub-3](https://github.com/ub-3)
- [yoshikipom](https://github.com/yoshikipom)
