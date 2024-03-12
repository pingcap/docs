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
    <td>PD (Placement Driver) has a lot of critical modules for the running of TiDB. Each module's resource consumption can increase as certain workloads scale, meaning they can each interfere with other functions in PD, ultimately impacting quality of service of the cluster.
By separating PD modules into separately-deployable services, their blast radii are massively mitigated as the cluster scales. Much larger clusters with much larger workloads are possible with this architecture.</td>
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
    <td>TiDB v8.0.0 introduces the <a href="https://docs.pingcap.com/tidb/v8.0/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a> table and the <a href="https://docs.pingcap.com/tidb/v8.0/sys-schema.md"><code>sys.schema_unused_index</code></a> view to provide usage statistics of indexes. This feature help you assess the importance of all indexes and optimize the index design.</td>
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

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Performance

* Support pushing down the following functions to TiFlash [#50975](https://github.com/pingcap/tidb/issues/50975) [#50485](https://github.com/pingcap/tidb/issues/50485) @[yibin87](https://github.com/yibin87) @[windtalker](https://github.com/windtalker) **tw@Oreoxmt** <!--1662--><!--1664-->

    * `CAST(DECIMAL AS DOUBLE)`
    * `POWER()`

  For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* Introduce priority queues for automatic statistics update [#50132](https://github.com/pingcap/tidb/issues/50132) @[hi-rustin](https://github.com/hi-rustin) **tw@hfxsd** <!--1640-->

    Maintaining the up-to-date nature of optimizer statistics is critical to stabilizing database performance. Most users rely on the [automatic statistics update](/statistics.md#automatic-update) provided by TiDB to keep statistics up-to-date. Automatic statistics update polls the status of statistics for all objects, and adds objects with insufficient health to a queue that is collected and updated one by one. In previous versions, the collection order is set randomly, which can result in longer waits for more worthy objects to be updated, causing potential database performance rollbacks.

    Starting from v8.0.0, automatic statistics update dynamically sets priorities for objects in combination with a variety of conditions to ensure that more valuable objects for collection are processed first, such as newly created indexes and partitioned tables with partition changes. Less healthy objects tend to be placed at the front of the queue. This enhancement improves the reasonableness of the collection order, and reduces performance problems caused by outdated statistics, therefore improving database stability.
    
    For more information, see [documentation](/statistics.md#automatic-update).

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

### DB operations

* PITR supports Amazon S3 Object Lock [#51184](https://github.com/pingcap/tidb/issues/51184) @[RidRisR](https://github.com/RidRisR) **tw@lilin90** <!--1604-->

    Amazon S3 Object Lock can help prevent backup data from being accidentally or intentionally deleted during a specified retention period, enhancing the security and integrity of data. Starting from v6.3.0, BR supports Amazon S3 Object Lock in snapshot backups, adding an additional layer of security for full backups. Starting from v8.0.0, PITR also supports Amazon S3 Object Lock. Whether full backups or log data backups, the Object Lock feature ensures a more reliable data protection, further strengthening the security of data backup and recovery and meeting regulatory requirements.

    For more information, see [documentation](/br/backup-and-restore-storages.md#other-features-supported-by-the-storage-service).

* Support making invisible indexes visible at the session level [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1401-->

    By default, the optimizer does not select [invisible indexes](/sql-statements/sql-statement-create-index.md#invisible-index) to optimize query execution. This mechanism is usually used to evaluate whether to delete an index. If there is uncertainty about whether deleting an index could degrade performance, you can set the index to invisible first and then quickly restore it to visible when necessary.

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
| [`initial-scan-rate-limit``](/system-variables.md#initial-scan-rate-limit-new-in-v620) | Modified | Add a limit of `1MiB` as the minimum value. |
| [`tidb_redact_log`](/system-variables.md#tidb_redact_log) | Modified | 控制在记录 TiDB 日志和慢日志时如何处理 SAL 文本中的用户信息，可选值为 `OFF`、`ON`、`MARKER`，以分别支持记录信息明文、信息屏蔽、信息标记。当变量值为 `MARKER` 时，日志中的用户信息将被标记处理，可以在之后决定是否对日志信息进行脱敏。 |
| [`tidb_low_resolution_tso_update_interval`](/system-variables.md#tidb_low_resolution_tso_update_interval-从-v800-版本开始引入) | Newly added | 设置更新 TiDB [缓存 timestamp](system-variables#tidb_low_resolution_tso) 的间隔。 |
| [`tidb_opt_use_invisible_indexes`](/system-variables.md#) | Newly added | 控制会话中是否能够选择[不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引)。当修改变量为`ON`时，针对该会话执行的查询，优化能够使用[不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引)进行优化。|
|  [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入)      |   Newly added                           |  设置缓存 schema 信息可以使用的内存上限，避免占用过多的内存。开启该功能后，将使用 LRU 算法来缓存所需的表，有效减小 schema 信息占用的内存。    |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
|          |          |          |          |

## Deprecated features

- Starting from v8.0.0, the [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) system variable is deprecated, and TiDB no longer supports automatic retries of optimistic transactions. As an alternative, when encountering optimistic transaction conflicts, you can capture the error and retry transactions in your application, or use the [Pessimistic transaction mode](/pessimistic-transaction.md) instead. **tw@lilin90** <!--1671-->
- Starting from v8.0.0, TiDB no longer supports the TLSv1.0 and TLSv1.1 protocols. You must upgrade TLS to TLSv1.2 or TLSv1.3.

## Improvements

+ Tools

    + TiDB Data Migration (DM)
    
        - In a MariaDB primary and secondary replication scenario, that is, a `MariaDB_primary_instance` -> `MariaDB_secondary_instance` -> `DM` -> `TiDB` migration scenario, when `gtid_strict_mode = off` and the GTID of the `MariaDB_secondary_instance` is not strictly incrementing (for example, there is data writing to the `MariaDB_secondary_instance`), then the DM task will report an error `less than global checkpoint position`, the DM task will report an error `less than global checkpoint position`. Starting from v8.0.0, TiDB is compatible with this scenario and data can be migrated downstream. [#10741](https://github.com/pingcap/tiflow/issues/10741) @[okJiang](https://github.com/okJiang) **tw@hfxsd** <!--1683-->
        
## Bug fixes

## Contributors
