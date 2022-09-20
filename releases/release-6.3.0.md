---
title: TiDB 6.3.0 Release Notes
---

# TiDB v6.3.0 Release Notes

Release date: xx xx, 2022

TiDB version: 6.3.0-DMR

In v6.3.0-DMR, the key new features and improvements are as follows:

- TiKV and TiFlash support SM4 encryption at rest.
- TiDB supports authentication with the SM3 algorithm.
- The `CREATE USER` and `ALTER USER` statements support the `ACCOUNT LOCK/UNLOCK` option.
- JSON data type and functions become generally available (GA).
- TiDB supports Null Aware Anti Join.
- TiDB provides execution time metrics at a finer granularity.
- A new syntactic sugar is added to simplify Range partition definitions.
- Range Columns partitioning supports defining multiple columns.

## New features

### SQL

* Add a new syntactic sugar (Range INTERVAL partitioning) to simplify Range partition definitions [#35683](https://github.com/pingcap/tidb/issues/35683) @[mjonss](https://github.com/mjonss)

    [Provides INTERVAL partitioning as a new way of defining Range partitions](/partitioned-table.md#range-interval-partitioning). You do not need to enumerate all partitions, which drastically reduces the lengthy way of writing Range partition statements. The semantic is equivalent to the original Range partition.

* Range Columns partitioning supports defining multiple columns [#36636](https://github.com/pingcap/tidb/issues/36636) @[mjonss](https://github.com/mjonss)

    Support [PARTITION BY RANGE COLUMNS (column_list)](/partitioned-table.md#range-columns-partitioning). `column_list` is no longer limited to a single column. The basic feature is the same as MySQL.

* EXCHANGE PARTITION becomes GA [#35996](https://github.com/pingcap/tidb/issues/35996) @[ymkzpx](https://github.com/ymkzpx)

    [EXCHANGE PARTITION](/partitioned-table.md#partition-management) becomes GA after performance and stability improvements.

* TiDB supports two more [window functions](/tiflash/tiflash-supported-pushdown-calculations.md) [#5579](https://github.com/pingcap/tiflash/issues/5579) @[SeaRise](https://github.com/SeaRise) **tw：shichun-0415**

    * `LEAD`
    * `LAG`

* The `CREATE USER` statement supports the `ACCOUNT LOCK/UNLOCK` option [#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw：ran-huang**

    When you create a user using the [`CREATE USER`](/sql-statements/sql-statement-create-user.md) statement, you can specify whether the created user is locked using the `ACCOUNT LOCK/UNLOCK` option. A locked user cannot log in to the database.

* The `ALTER USER` statement supports the `ACCOUNT LOCK/UNLOCK` option [#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw：ran-huang**

    You can modify the lock state of an existing user using the `ACCOUNT LOCK/UNLOCK` option in the [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) statement.

* JSON data type and JSON functions become GA [#36993](https://github.com/pingcap/tidb/issues/36993) @[xiongjiwei](https://github.com/xiongjiwei) **tw: qiancai**

    JSON is a popular data format adopted by a large number of programs. TiDB has introduced the [JSON support](/data-type-json.md) as experimental since an earlier version, compatible with MySQL's JSON data type and some JSON functions. In v6.3.0, the JSON support becomes GA, providing TiDB with richer data types, and further improving TiDB compatibility with MySQL.

* Provide lightweight metadata lock to improve the DML success rate during DDL change (experimental) [#37275](https://github.com/pingcap/tidb/issues/37275) @[wjhuang2016](https://github.com/wjhuang2016) **tw: Oreoxmt**

    TiDB uses the online asynchronous schema change algorithm to support changing metadata objects. When a transaction is executed, the transaction obtains the corresponding metadata snapshot at transaction start. If the metadata is changed during transaction, to ensure the data consistency, TiDB returns an `Information schema is changed` error and the transaction fails to commit. To solve the problem, TiDB v6.3.0 introduces [metadata lock](/metadata-lock.md) into the online DDL algorithm. To avoid most DML errors, TiDB coordinates the priority of DMLs and DDLs during table metadata change, and makes executing DDLs wait for the DMLs with old metadata to commit.

* Improve the performance of adding indexes and reduce its impact on DML transactions [#35983](https://github.com/pingcap/tidb/issues/35983) @[benjamin2037](https://github.com/benjamin2037) **tw: Oreoxmt**

    To improve the speed of backfilling when creating an index, TiDB v6.3.0 accelerates the `ADD INDEX` and `CREATE INDEX` DDL operations when the [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) system variable is enabled. The performance of adding indexes is about three times faster than the original when the feature is enabled.

* Improve MySQL 8.0 compatibility by adding support for `REGEXP_INSTR()`, `REGEXP_LIKE()`, `REGEXP_REPLACE()`, and `REGEXP_SUBSTR()` regular expression functions [#23881](https://github.com/pingcap/tidb/issues/23881) @[windtalker](https://github.com/windtalker) **tw: Oreoxmt**

    For more details about the compatibility with MySQL, see [Regular expression compatibility with MySQL](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql).

### Security

* TiKV supports the SM4 algorithm for encryption at rest. [#13041](https://github.com/tikv/tikv/issues/13041) @[jiayang-zheng](https://github.com/jiayang-zheng)

    Add the [SM4 algorithm](/encryption-at-rest.md) for TiKV encryption at rest. When you configure encryption at rest, you can enable the SM4 encryption capacity by setting the value of the "data-encryption-method" configuration to "sm4-ctr".

* TiFlash supports the SM4 algorithm for encryption at rest. [#5714](https://github.com/pingcap/tiflash/issues/5714) @[lidezhu](https://github.com/lidezhu)

    Add the [SM4 algorithm](/encryption-at-rest.md) for TiFlash encryption at rest. When you configure encryption at rest, you can enable the SM4 encryption capacity by setting the value of the "data-encryption-method" configuration to "sm4-ctr".

* TiDB supports authentication with the SM3 algorithm [#36192](https://github.com/pingcap/tidb/issues/36192) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw：ran-huang**

    TiDB adds an authentication plugin [`tidb_sm3_password`](/system-variables.md#default_authentication_plugin) based on the SM3 algorithm. When this plugin is enabled, the user password is encrypted and validated using the SM3 algorithm.

* JDBC supports authentication with the SM3 algorithm [issue]() @[lastincisor](https://github.com/lastincisor) **tw：ran-huang**

    Authenticating the user password needs client-side support. Now because [JDBC supports the SM3 algorithm](/develop/dev-guide-choose-driver-or-orm.md#java-drivers), you can connect to TiDB using SM3 authentication via JDBC.

### Observability

* TiDB provides fine-grained metrics of SQL query execution time [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk) **tw: Oreoxmt**

    TiDB v6.3.0 provides fine-grained data metrics for [detailed observation of execution time](/latency-breakdown.md). Through the complete and segmented metrics, you can clearly understand the main time consumption of SQL queries, and then quickly find key problems and save time in troubleshooting.

* Enhanced output for slow logs and `TRACE` statements [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk) **tw: Oreoxmt**

    TiDB v6.3.0 enhances the output of slow logs and `TRACE`. You can observe the [full-link duration](/latency-breakdown.md) of SQL queries from TiDB parsing to KV RocksDB writing to disk, which further enhances the diagnostic capabilities.

* TiDB Dashboard provides deadlock history information [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk) **tw: shichun-0415**

    From v6.3.0, TiDB Dashboard will provide deadlock history. If you find excessively long SQL lock waiting by analyzing slow logs or other information on TiDB Dashboard, you can turn to deadlock history for problem locating, which delivers better diagnosis experience.

### Performance

* TiFlash changes the way FastScan is used (experimental) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

    FastScan, introduced in TiFlash starting with v6.2.0, performed as expected, but lacked flexibility in how it was used. Therefore, in v6.3.0 [the way of using FastScan has changed](/develop/dev-guide-use-fastscan.md). TiFlash does not support using the switch to control the FastScan feature. Instead, it uses the system variable [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630) to control whether to turn on the FastScan function.
    
    When you upgrade from v6.2.0 to v6.3.0, all FastScan settings in v6.2.0 will become invalid, but will not affect the normal reading of data. You need to set the variable [`tiflash_fastscan`]. When you upgrade from an earlier version to v6.3.0, the FastScan feature is not enabled by default for all sessions to keep data consistency.

* TiFlash optimizes to improve data scanning performance in multiple concurrency scenarios [#5376](https://github.com/pingcap/tiflash/issues/5376) @[JinheLin](https://github.com/JinheLin)

    TiFlash reduces duplicate reads of the same data by combining read operations of the same data. It optimizes the resource overhead and improves the performance of data scanning in the case of concurrent tasks (/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file). It avoids the situation where the same data needs to be read separately in each task in multiple concurrent tasks, and avoids the possibility of multiple reads of the same data at the same time.

    This feature is experimental in v6.2.0, and becomes GA in v6.3.0.

* Improve performance of TiFlash data replication [#5237](https://github.com/pingcap/tiflash/issues/5237) @[breezewish](https://github.com/breezewish) 

    TiFlash uses the Raft protocol for data replication with TiKV. Prior to v6.3.0, it often took long time to replicate large amounts of replica data. TiDB v6.3.0 optimizes the TiFlash data replication mechanism and significantly improves the replication speed. When you use BR to recover data, use TiDB Lightning to import data, or add new TiFlash replicas, the replicas can be replicated more quickly. You can query with TiFlash in a more timely manner. In addition, TiFlash replicas will also reach a secure and balanced state faster when you scale up, scale down, or modify the number of TiFlash replicas.

* TiKV supports log recycling [#214](https://github.com/tikv/raft-engine/issues/214) @[LykxSassinator](https://github.com/LykxSassinator) **tw：ran-huang**

    TiKV recycles log files in Raft Engine by default. This reduces the long tail latency during Raft log appending and improves performance under write workloads.

* TiDB supports Null-Aware Anti Join] [#issue]() @[Arenatlx](https://github.com/Arenatlx) **tw: Oreoxmt**

    TiDB v6.3.0 introduces a new join type [Null-Aware Anti Join (NAAJ)](/explain-subqueries.md#null-aware-semi-joinin-any). NAAJ can be aware of whether the collection is empty or `NULL` when processing collection operations. This optimizes the execution efficiency of operations such as `IN` and `= ANY` and improves SQL performance.

* Add optimizer hints to control the build end of Hash Join [#issue]() @[Reminiscent](https://github.com/Reminiscent) **tw: TomShawn**

    In v6.3.0, the TiDB optimizer introduces 2 hints, `HASH_JOIN_BUILD()` and `HASH_JOIN_PROBE()`, to specify the Hash Join, its probe end, and its build end. When the optimizer fails to select the optimal execution plan, you can use these hints to intervene with the plan. 

* Support session-level CTE inline [#36514](https://github.com/pingcap/tidb/issues/36514) @[elsa0520](https://github.com/elsa0520) **tw: shichun-0415**

    TiDB v6.2.0 introduced the `MERGE` hint in optimizers to allow CTE inline, so that the consumers of a CTE query result can be executed in parallel in TiFlash. In v6.3.0, a session variable [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630) in introduced to allow CTE inline in sessions. This improves ease of use greatly.

### Transactions

* Support deferring unique constraints in pessimistic transactions [#36579](https://github.com/pingcap/tidb/issues/36579) @[ekexium](https://github.com/ekexium) **tw: qiancai**

    You can use the [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) system variable to control when TiDB checks [unique constraints](/constraints.md#pessimistic-transactions) in pessimistic transactions. This variable is disabled by default. When the variable is set to `ON`, TiDB will defer locking operations and unique constraint checks in pessimistic transactions until necessary, thus improving the performance of bulk DML operations.

* Optimize the way of fetching TSO in the Read-Committed isolation level [#36812](https://github.com/pingcap/tidb/issues/36812) @[TonsnakeLin](https://github.com/TonsnakeLin) **tw: TomShawn**

    In the Read-Committed isolation level, the system variable [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630) is introduced to control how TSO is fetched. In the case of Plan Cache hit, TiDB improves the execution efficiency of batch DML statements by reducing the frequency of fetching TSO, and reduces the execution time of running tasks in batches.

### Stability

* Modify the default policy of loading statistics when statistics become outdated [#issue]() @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw: TomShawn**

    In v5.3.0, TiDB introduces the system variable [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530) to control how the optimizer behaves when the statistics become outdated. The default value is `ON`, which means keeping the behavior of the old version: When statistics on objects involved in SQL are outdated, the optimizer considers that statistics (other than the total number of rows on the table) are no longer reliable and uses pseudo statistics instead. After tests and analyses of actual user scenarios, the default value of `tidb_enable_pseudo_for_outdated_stats` is changed to `OFF` in v6.3.0. Even if the statistics become outdated, the optimizer will still use the statistics on the table, which is good for the execution program stability.

* The feature of disabling Titan becomes GA [#issue]() @[tabokie](https://github.com/tabokie) **tw：ran-huang**

    You can [disable Titan](/titan-configuration#disable-titan) for online TiKV nodes.

### Ease of use

### MySQL compatibility

* Improve compatibility of SQL-based data Placement Rules [#37171](https://github.com/pingcap/tidb/issues/37171) @[lcwangchao](https://github.com/lcwangchao)

    TiDB v6.0.0 provides SQL-based data Placement Rules. But this feature is not compatible with TiFlash due to conflicts in implementation mechanisms. TiDB v6.3.0 optimizes this feature, and [improves compatibility of SQL-based data Placement Rules and TiFlash](/placement-rules-in-sql.md#known-limitations). 

### Backup and restore

* PITR supports GCS and Azure Blob Storage as backup storage [#issue]() @[joccau](https://github.com/joccau) **tw: shichun-0415**

    PITR supports [GCS and Azure Blob Storage as backup storage](). If your TiDB is deployed on GCP or Azure, you can use the PITR feature after upgrading your cluster to v6.3.0.

* BR supports AWS S3 Object Lock [#issue]() @[3pointer](https://github.com/3pointer) **tw: shichun-0415**

    After enabling [Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) , you can protect backup data from being tampered with or deleted.

### Data migration

* TiDB Lightning supports importing Parquet files exported by Apache Hive into TiDB [#issue]() @[buchuitoudegou](https://github.com/buchuitoudegou) **tw：ran-huang**

    TiDB Lightning supports importing Parquet files exported by Apache Hive into TiDB, thereby achieving data migration from Hive to TiDB.

* DM supports adding a field to a table migrated to TiDB and assigning values to the field [#3262](https://github.com/pingcap/tiflow/pull/3262), [#3340](https://github.com/pingcap/tiflow/issues/3340) @[yufan022](https://github.com/yufan022) **tw：ran-huang**

    DM supports [adding a field to a table migrated to TiDB and assigning values to the field](link). When you merge and migrate MySQL shards to TiDB, you can use the field to distinguish which shard the record is migrated from.

### TiDB data share subscription

* TiCDC supports a deployment topology that can replicate data from multiple geo-distributed data sources [#issue]() @[sdojjy](https://github.com/sdojjy) **tw：ran-huang**

    To support replicating data from a single TiDB cluster to multiple geo-distributed data systems, starting from v6.3.0, [TiCDC can be deployed in multiple IDCs](link) to replicate data for each IDC. This feature helps deliver the capability of geo-distributed data replication and deployment topology.

* TiCDC supports keeping the snapshots consistent between the upstream and the downstream (sync point) [#issue]() @[asddongmen](https://github.com/asddongmen) **tw: TomShawn**

    In the scenarios of data replication for disaster recovery, TiCDC supports periodically maintaining a downstream data snapshot so that the downstream snapshot is consistent with the upstream snapshot. With this feature, TiCDC can better match the scenarios where reads and writes are separate, and help you lower the cost.

* TiCDC supports graceful upgrade [#4757](https://github.com/pingcap/tiflow/issues/4757) @[overvenus](https://github.com/overvenus) @[3AceShowHand](https://github.com/3AceShowHand) **tw:ran-huang**

    When TiCDC is deployed using TiUP (>=v1.11.0) or TiDB Operator (>=v1.3.8), you can gracefully upgrade the TiCDC cluster. During the upgrade, data replication latency is kept as low as 30 seconds. This improves stability, empowering TiCDC to better support latency-sensitive applications.

## Compatibility changes

### System variables

| Variable name | Change type (newly added, modified, or deleted) | Description |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

### Configuration file parameters

| Configuration file | Configuration | Change type | Description |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### Others

## Removed feature

## Improvements

+ TiDB

    - note [#issue]() @[Contributor GitHub ID]()

+ TiKV

    - note [#issue]() @[Contributor GitHub ID]()

+ PD

    - note [#issue]() @[Contributor GitHub ID]()

+ TiFlash

    - note [#issue]() @[Contributor GitHub ID]()

+ Tools

    - Backup & Restore (BR)

        - note [#issue]() @[Contributor GitHub ID]()

    - TiCDC

        - note [#issue]() @[Contributor GitHub ID]()

    - TiDB Data Migration (DM)

        - note [#issue]() @[Contributor GitHub ID]()

    - TiDB Lightning

        - note [#issue]() @[Contributor GitHub ID]()

    - TiUP

        - note [#issue]() @[Contributor GitHub ID]()

## Bug fixes

+ TiDB

    - note [#issue]() @[Contributor GitHub ID]()

+ TiKV

    - note [#issue]() @[Contributor GitHub ID]()

+ PD

    - note [#issue]() @[Contributor GitHub ID]()

+ TiFlash

    - note [#issue]() @[Contributor GitHub ID]()

+ Tools

    + Backup & Restore (BR)

        - note [#issue]() @[Contributor GitHub ID]()

    - TiCDC

        - note [#issue]() @[Contributor GitHub ID]()

    - TiDB Data Migration (DM)

        - note [#issue]() @[Contributor GitHub ID]()

    - TiDB Lightning

        - note [#issue]() @[Contributor GitHub ID]()

    - TiUP

        - note [#issue]() @[Contributor GitHub ID]()

## Contributors

We would like to thank the following contributors from the TiDB community:

- [Contributor GitHub ID]()
