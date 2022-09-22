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
- TiDB supports null-aware anti join.
- TiDB provides execution time metrics at a finer granularity.
- A new syntactic sugar is added to simplify Range partition definitions.
- Range COLUMNS partitioning supports defining multiple columns.

## New features

### SQL

* Add a new syntactic sugar (Range INTERVAL partitioning) to simplify Range partition definitions [#35683](https://github.com/pingcap/tidb/issues/35683) @[mjonss](https://github.com/mjonss)

    [Provides INTERVAL partitioning as a new way of defining Range partitions](/partitioned-table.md#range-interval-partitioning). You do not need to enumerate all partitions, which drastically reduces the lengthy way of writing Range partition statements. The semantic is equivalent to the original Range partition.

* Range COLUMNS partitioning supports defining multiple columns [#36636](https://github.com/pingcap/tidb/issues/36636) @[mjonss](https://github.com/mjonss)

    Support [PARTITION BY RANGE COLUMNS (column_list)](/partitioned-table.md#range-columns-partitioning). `column_list` is no longer limited to a single column. The basic feature is the same as MySQL.

* EXCHANGE PARTITION becomes GA [#35996](https://github.com/pingcap/tidb/issues/35996) @[ymkzpx](https://github.com/ymkzpx)

    [EXCHANGE PARTITION](/partitioned-table.md#partition-management) becomes GA after performance and stability improvements.

* TiDB supports two more [window functions](/tiflash/tiflash-supported-pushdown-calculations.md) [#5579](https://github.com/pingcap/tiflash/issues/5579) @[SeaRise](https://github.com/SeaRise) **tw：shichun-0415**

    * `LEAD()`
    * `LAG()`

* The `CREATE USER` statement supports the `ACCOUNT LOCK/UNLOCK` option [#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw：ran-huang**

    When you create a user using the [`CREATE USER`](/sql-statements/sql-statement-create-user.md) statement, you can specify whether the created user is locked using the `ACCOUNT LOCK/UNLOCK` option. A locked user cannot log in to the database.

* The `ALTER USER` statement supports the `ACCOUNT LOCK/UNLOCK` option [#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw：ran-huang**

    You can modify the lock state of an existing user using the `ACCOUNT LOCK/UNLOCK` option in the [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) statement.

* JSON data type and JSON functions become GA [#36993](https://github.com/pingcap/tidb/issues/36993) @[xiongjiwei](https://github.com/xiongjiwei) **tw: qiancai**

    JSON is a popular data format adopted by a large number of programs. TiDB has introduced the [JSON support](/data-type-json.md) as experimental since an earlier version, compatible with MySQL's JSON data type and some JSON functions. In v6.3.0, the JSON support becomes GA, providing TiDB with richer data types, and further improving TiDB compatibility with MySQL.

* Provide lightweight metadata lock to improve the DML success rate during DDL change (experimental) [#37275](https://github.com/pingcap/tidb/issues/37275) @[wjhuang2016](https://github.com/wjhuang2016) **tw: Oreoxmt**

    TiDB uses the online asynchronous schema change algorithm to support changing metadata objects. When a transaction is executed, it obtains the corresponding metadata snapshot at the transaction start. If the metadata is changed during a transaction, to ensure data consistency, TiDB returns an `Information schema is changed` error and the transaction fails to commit. To solve the problem, TiDB v6.3.0 introduces [metadata lock](/metadata-lock.md) into the online DDL algorithm. To avoid most DML errors, TiDB coordinates the priority of DMLs and DDLs during table metadata change and makes executing DDLs wait for the DMLs with old metadata to commit.

* Improve the performance of adding indexes and reduce its impact on DML transactions [#35983](https://github.com/pingcap/tidb/issues/35983) @[benjamin2037](https://github.com/benjamin2037) **tw: Oreoxmt**

    To improve the speed of backfilling when creating an index, TiDB v6.3.0 accelerates the `ADD INDEX` and `CREATE INDEX` DDL operations when the [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) system variable is enabled. When the feature is enabled, the performance of adding indexes is about three times faster than previously.

### Security

* TiKV supports the SM4 algorithm for encryption at rest [#13041](https://github.com/tikv/tikv/issues/13041) @[jiayang-zheng](https://github.com/jiayang-zheng)

    Add the [SM4 algorithm](/encryption-at-rest.md) for TiKV encryption at rest. When you configure encryption at rest, you can enable the SM4 encryption capacity by setting the value of the "data-encryption-method" configuration to "sm4-ctr".

* TiFlash supports the SM4 algorithm for encryption at rest [#5714](https://github.com/pingcap/tiflash/issues/5714) @[lidezhu](https://github.com/lidezhu)

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

    FastScan, introduced in TiFlash starting with v6.2.0, performed as expected, but lacked flexibility. Therefore, in v6.3.0 [the way of using FastScan has changed](/develop/dev-guide-use-fastscan.md). TiFlash does not support using the switch to control the FastScan feature. Instead, it uses the system variable [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630) to control whether to enable the FastScan function.

    When you upgrade from v6.2.0 to v6.3.0, all FastScan settings in v6.2.0 will become invalid, but will not affect the normal reading of data. You need to set the variable [`tiflash_fastscan`]. When you upgrade from an earlier version to v6.3.0, the FastScan feature is not enabled by default for all sessions to keep data consistency.

* TiFlash optimizes to improve data scanning performance in multiple concurrency scenarios [#5376](https://github.com/pingcap/tiflash/issues/5376) @[JinheLin](https://github.com/JinheLin)

    TiFlash reduces duplicate reads of the same data by combining read operations of the same data. It optimizes the resource overhead and [improves the performance of data scanning in the case of concurrent tasks](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file). It avoids the situation where the same data needs to be read separately in each task in multiple concurrent tasks, and avoids the possibility of multiple reads of the same data at the same time.

    This feature is experimental in v6.2.0, and becomes GA in v6.3.0.

* Improve performance of TiFlash data replication [#5237](https://github.com/pingcap/tiflash/issues/5237) @[breezewish](https://github.com/breezewish)

    TiFlash uses the Raft protocol for data replication with TiKV. Prior to v6.3.0, it often took long time to replicate large amounts of replica data. TiDB v6.3.0 optimizes the TiFlash data replication mechanism and significantly improves the replication speed. When you use BR to recover data, use TiDB Lightning to import data, or add new TiFlash replicas, the replicas can be replicated more quickly. You can query with TiFlash in a more timely manner. In addition, TiFlash replicas will also reach a secure and balanced state faster when you scale up, scale down, or modify the number of TiFlash replicas.

* TiKV supports log recycling [#214](https://github.com/tikv/raft-engine/issues/214) @[LykxSassinator](https://github.com/LykxSassinator) **tw：ran-huang**

    TiKV supports recycling log files in Raft Engine. This reduces the long tail latency in network disks during Raft log appending and improves performance under write workloads.

* TiDB supports null-aware anti join [#37525](https://github.com/pingcap/tidb/issues/37525) @[Arenatlx](https://github.com/Arenatlx) **tw: Oreoxmt**

    TiDB v6.3.0 introduces a new join type [Null-aware anti join (NAAJ)](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries). NAAJ can be aware of whether the collection is empty or `NULL` when processing collection operations. This optimizes the execution efficiency of operations such as `IN` and `= ANY` and improves SQL performance.

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

* Improve MySQL 8.0 compatibility by adding support for `REGEXP_INSTR()`, `REGEXP_LIKE()`, `REGEXP_REPLACE()`, and `REGEXP_SUBSTR()` regular expression functions [#23881](https://github.com/pingcap/tidb/issues/23881) @[windtalker](https://github.com/windtalker) **tw: Oreoxmt**

    For more details about the compatibility with MySQL, see [Regular expression compatibility with MySQL](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql).

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

    - One `PLAN REPLAYER` command can export information about execution plans of multiple SQL statements, which makes troubleshooting more efficient [#37798](https://github.com/pingcap/tidb/issues/37798) @[Yisaer](https://github.com/Yisaer)
    - improve warning log when new connection arrives [#34964](https://github.com/pingcap/tidb/issues/34964) @[xiongjiwei](https://github.com/xiongjiwei)

    - sql-infra

        - Extend partitioning syntax with INTERVAL for easier partitioning definition [#35827](https://github.com/pingcap/tidb/issues/35827) @[ymkzpx](https://github.com/ymkzpx)
        - Grant privilege of a table to an user checks the target table exist first, in the past, the table name comparison works in a case sensitive manner, now it's changed to case insensitive [#34610](https://github.com/pingcap/tidb/issues/34610) @[tiancaiamao](https://github.com/tiancaiamao)
        - Support AWS NLB proxy protocol [#36312](https://github.com/pingcap/tidb/issues/36312) @[hawkingrei](https://github.com/hawkingrei)
        - Previously, TiDB users can set `init_connect` without any checking. From now on, the value of `init_connect` should be checked by the sql parser [#35324](https://github.com/pingcap/tidb/issues/35324) @[CbcWestwolf](https://github.com/CbcWestwolf)
        - Add support `flashback database` command [#37386](https://github.com/pingcap/tidb/issues/37386) @[tiancaiamao](https://github.com/tiancaiamao)

    - execution

        - report error if json path has the wrong syntax [#22525](https://github.com/pingcap/tidb/issues/22525) @[xiongjiwei](https://github.com/xiongjiwei)
        - report error if json path has the wrong syntax [#34959](https://github.com/pingcap/tidb/issues/34959) @[xiongjiwei](https://github.com/xiongjiwei)

    - planner

        - planner: just pop cte's handleHelper map out since it shouldn't be considered [#35758](https://github.com/pingcap/tidb/issues/35758) @[AilinKid](https://github.com/AilinKid)

+ TiKV

    - Add a new option to make unreachable_backoff of raftstore configurable [#13054](https://github.com/tikv/tikv/issues/13054)
    - Implement TSO batch list to improve tolerance to TSO service fault [#12794](https://github.com/tikv/tikv/issues/12794) @[pingyu](https://github.com/pingyu)
    - Make max_subcompactions dynamically changeable [#13145](https://github.com/tikv/tikv/issues/13145) @[ethercflow](https://github.com/ethercflow)
    - Optimize the performance of merging empty regions [#12421](https://github.com/tikv/tikv/issues/12421) @[tabokie](https://github.com/tabokie)
    - Support more regular expression functions [#13483](https://github.com/tikv/tikv/issues/13483) @[gengliqi](https://github.com/gengliqi)
    - Support automatically scale read pool thread count based on the CPU usage [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)

+ PD

    - Updates metrics query. Renames `metrics` to `monitoring` on TiDB Dashboard [#5366](https://github.com/tikv/pd/issues/5366) @[YiniXu9506](https://github.com/YiniXu9506)

+ TiFlash

    - compute

        - Support to pushdown elt to TiFlash [#5104](https://github.com/pingcap/tiflash/issues/5104) @[Willendless](https://github.com/Willendless)
        - Support to pushdown leftShift to TiFlash [#5099](https://github.com/pingcap/tiflash/issues/5099) @[AnnieoftheStars](https://github.com/AnnieoftheStars)
        - Support to pushdown castTimeAsDuration to TiFlash [#5306](https://github.com/pingcap/tiflash/issues/5306) @[AntiTopQuark](https://github.com/AntiTopQuark)
        - Support to pushdown castTimeAsDuration to TiFlash [#5306](https://github.com/pingcap/tiflash/issues/5306) @[AntiTopQuark](https://github.com/AntiTopQuark)
        - Support Planner Interpreter [#4739](https://github.com/pingcap/tiflash/issues/4739) @[SeaRise](https://github.com/SeaRise)
        - Support to pushdown hexInt and hexStr to TiFlash [#5107](https://github.com/pingcap/tiflash/issues/5107), [#5462](https://github.com/pingcap/tiflash/issues/5462)
        - Support to pushdown elt to TiFlash [#5104](https://github.com/pingcap/tiflash/issues/5104) @[Willendless](https://github.com/Willendless)
        - Support to pushdown shiftLeft to TiFlash [#5099](https://github.com/pingcap/tiflash/issues/5099) @[AnnieoftheStars](https://github.com/AnnieoftheStars)
        - Suppress the "tcp set inq" loggings [#4940](https://github.com/pingcap/tiflash/issues/4940)
        - Support to pushdown CastTimeAsDuration to TiFlash [#5306](https://github.com/pingcap/tiflash/issues/5306) @[AntiTopQuark](https://github.com/AntiTopQuark)

    - storage

        - Calculate the io throughput in background in ReadLimiter [#5401](https://github.com/pingcap/tiflash/issues/5401), [#5091](https://github.com/pingcap/tiflash/issues/5091) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ Tools

    + TiDB Dashboard

        - Optimize the display of TiDB Dashboard [#issue]() @[Contributor GitHub ID]()
        - Display the row count on SQL statement summary and slow query pages [#issue]() @[Contributor GitHub ID]()
        - Optimize the display of some error messages  [#issue]() @[Contributor GitHub ID]()

    + Backup & Restore (BR)

        - note [#issue]() @[Contributor GitHub ID]()

    + TiDB Binlog

        - Fix a bug that Drainer cannot send requests correctly to Pump when compressor is set to gzip [#1152](https://github.com/pingcap/tidb-binlog/issues/1152) @[lichunzhu](https://github.com/lichunzhu)

    + TiCDC

        - Improve compatibility for MySQL 8.0 upstream [#6506](https://github.com/pingcap/tiflow/issues/6506) @[lance6716](https://github.com/lance6716)

    + TiDB Data Migration (DM)

        - Improve compatibility for MySQL 8.0 upstream [#6448](https://github.com/pingcap/tiflow/issues/6448) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Add query parameters for S3 external storage URL, in order to support accessing the S3 data in another account by assuming a given role [#36891](https://github.com/pingcap/tidb/issues/36891) [dsdashun](https://github.com/dsdashun)

    - TiUP

        - note [#issue]() @[Contributor GitHub ID]()

## Bug fixes

+ TiDB

    - Fix handling of prepared statement flags in the classic MySQL protocol [#36731](https://github.com/pingcap/tidb/issues/36731) @[hawkingrei](https://github.com/hawkingrei)
    - update pd-client to ensure tidb-server get clusterID correctly [#36505](https://github.com/pingcap/tidb/issues/36505), [#36478](https://github.com/pingcap/tidb/issues/36478) @[Defined2014](https://github.com/Defined2014)
    - Fix that incorrect TiDB states may appear on startup under very, very, very extreme cases [#36791](https://github.com/pingcap/tidb/issues/36791)
    - Fix a bug that UnionScan's Next() function skips reading data when the passed chunk's capacity is 0 [#36903](https://github.com/pingcap/tidb/issues/36903)
    - Fix a bug about variables information leak [#37586](https://github.com/pingcap/tidb/issues/37586)
    - Fix the issue that the action order of [#37058](https://github.com/pingcap/tidb/issues/37058) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that comparison between json opaque will cause panic [#37315](https://github.com/pingcap/tidb/issues/37315)
    - Fix the issue that the single precision float cannot be used in json aggregation funtions [#37287](https://github.com/pingcap/tidb/issues/37287) @[YangKeao](https://github.com/YangKeao)
    - fix that the result of expression castRealAsTime is inconsistent with mysql [#37462](https://github.com/pingcap/tidb/issues/37462)

    - sql-infra

        - fix the bug prepare will not check privilege [#35784](https://github.com/pingcap/tidb/issues/35784) @[lcwangchao](https://github.com/lcwangchao)
        - When set `tidb_enable_noop_variable` to `WARN`, an error will be returned [#36647](https://github.com/pingcap/tidb/issues/36647) @[lcwangchao](https://github.com/lcwangchao)
        - Fix the issue that when 'expression index' is defined, the value of `ORDINAL_POSITION` column of `INFORMAITON_SCHEMA`.`COLUMNS` table might be incorrect [#31200](https://github.com/pingcap/tidb/issues/31200) @[bb7133](https://github.com/bb7133)
        - Fix the issue that when setting a timestamp that is larger than `MAXINT32`, TiDB doesn't report an error like MySQL [#31585](https://github.com/pingcap/tidb/issues/31585) @[bb7133](https://github.com/bb7133)
        - flashback cluster shouldn't support expr in timestamp [#37495](https://github.com/pingcap/tidb/issues/37495) @[Defined2014](https://github.com/Defined2014)
        - Fix panic of enterprise plugin on 6.1 [#37319](https://github.com/pingcap/tidb/issues/37319)
        - Fix incorrect output of `show create placement policy` with a policy of double quotes [#37526](https://github.com/pingcap/tidb/issues/37526) @[xhebox](https://github.com/xhebox)
        - store flashback history in TiKV, avoid overlapped flashback TS range [#37585](https://github.com/pingcap/tidb/issues/37585) @[Defined2014](https://github.com/Defined2014)
        - When exchange partition with temporary table, an error will be returned [#37201](https://github.com/pingcap/tidb/issues/37201)
        - planner: fix partition table getting error result when select `TIKV_REGION_STATUS` with `table_id` [#37436](https://github.com/pingcap/tidb/issues/37436) @[zimulala](https://github.com/zimulala)
        - In test_driver, parser didn't deal with RestoreStringWithoutCharset and RestoreStringWithoutDefaultCharset flags, add support for those two flags [#37175](https://github.com/pingcap/tidb/issues/37175) @[Defined2014](https://github.com/Defined2014)
        - planner: fix show View Privilege behave for view table [#34326](https://github.com/pingcap/tidb/issues/34326) @[hawkingrei](https://github.com/hawkingrei)
        - Support send flashback RPC [#37651](https://github.com/pingcap/tidb/issues/37651) @[Defined2014](https://github.com/Defined2014)
        - Fix a wrong casting in building union plan [#31678](https://github.com/pingcap/tidb/issues/31678) @[bb7133](https://github.com/bb7133)
        - support some adminStmt in read-only mode [#37631](https://github.com/pingcap/tidb/issues/37631) @[Defined2014](https://github.com/Defined2014)
        - fix resume pd schedule and cancel for `flashback cluster` [#37584](https://github.com/pingcap/tidb/issues/37584) @[Defined2014](https://github.com/Defined2014)
        - fix resume pd schedule and cancel for `flashback cluster` [#37580](https://github.com/pingcap/tidb/issues/37580) @[Defined2014](https://github.com/Defined2014)
        - Fix the issue that the user cannot update from json 'null' to NULL [#37852](https://github.com/pingcap/tidb/issues/37852) @[YangKeao](https://github.com/YangKeao)
        - Optimize DDL history HTTP API, and add support for 'start_job_id' parameter [#35838](https://github.com/pingcap/tidb/issues/35838) @[tiancaiamao](https://github.com/tiancaiamao)
        - fix inaccuate row_count num [#25968](https://github.com/pingcap/tidb/issues/25968) @[Defined2014](https://github.com/Defined2014)

    - execution

        - Fix wrong result when enabling dynamic mode in partition table for tiflash [#37254](https://github.com/pingcap/tidb/issues/37254) @[wshwsh12](https://github.com/wshwsh12)
        - Fix the issue that the cast and comparison between binary string and json is incompatible with MySQL [#31918](https://github.com/pingcap/tidb/issues/31918) @[YangKeao](https://github.com/YangKeao)
        - Fix the issue that the cast and comparison between binary string and json is incompatible with MySQL [#25053](https://github.com/pingcap/tidb/issues/25053) @[YangKeao](https://github.com/YangKeao)
        - Fix the issue that the json_objectagg and json_arrayagg is not compatible with MySQL on binary value [#25053](https://github.com/pingcap/tidb/issues/25053) @[YangKeao](https://github.com/YangKeao)

    - transaction

        - bugfix: do not acquire pessimistic lock for non-unique index keys [#36235](https://github.com/pingcap/tidb/issues/36235)
        - Fix the auto-commit mode change related transaction commit behaviours [#36581](https://github.com/pingcap/tidb/issues/36581) @[cfzjywxk](https://github.com/cfzjywxk)

    - planner

        - fix update plan's projection elimination will cause column resolution error [#37568](https://github.com/pingcap/tidb/issues/37568) @[AilinKid](https://github.com/AilinKid)
        - planner: fix outer join reorder will push down its outer join condition [#37238](https://github.com/pingcap/tidb/issues/37238) @[AilinKid](https://github.com/AilinKid)
        - make the both side operand of NAAJ & refuse partial column substitute in projection elimination [#37032](https://github.com/pingcap/tidb/issues/37032) @[AilinKid](https://github.com/AilinKid)
        - planner: correct the redundant field meaning in join full schema when join coalesce [#36420](https://github.com/pingcap/tidb/issues/36420) @[AilinKid](https://github.com/AilinKid)

    - diagnosis

        - fix metric sql error [#35856](https://github.com/pingcap/tidb/issues/35856) @[Defined2014](https://github.com/Defined2014)

+ TiKV

    - fix the bug that the consume should be refresh if region heartbeat send failed [#12934](https://github.com/tikv/tikv/issues/12934) @[bufferflies](https://github.com/bufferflies)
    - Fix a bug that regions may be overlapped if raftstore is too busy [#13160](https://github.com/tikv/tikv/issues/13160) @[5kbpers](https://github.com/5kbpers)
    - Fix potential deadlock in `RpcClient` when two read locks are interleaved by a write lock [#12933](https://github.com/tikv/tikv/issues/12933) @[BurtonQin](https://github.com/BurtonQin)
    - Fix a double-lock bug in components/engine_test [#13186](https://github.com/tikv/tikv/issues/13186) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix plaintext iv debug assert while disable encryption [#13081](https://github.com/tikv/tikv/issues/13081) @[jiayang-zheng](https://github.com/jiayang-zheng)
    - Fix a expression error that causes unified read pool cpu cannot be shown correctly [#13086](https://github.com/tikv/tikv/issues/13086) @[glorv](https://github.com/glorv)
    - Fix the problem that QPS may drop to zero for several mintues when a tikv is partitioned [#12966](https://github.com/tikv/tikv/issues/12966) @[cosven](https://github.com/cosven)
    - remove call_option to avoid  deadlock(RWR) [#13191](https://github.com/tikv/tikv/issues/13191) @[bufferflies](https://github.com/bufferflies)
    - Reduce false-positive PessimisticLockNotFound errors in conflicting auto-commit workloads [#13425](https://github.com/tikv/tikv/issues/13425) @[sticnarf](https://github.com/sticnarf)
    - Fix a bug that may cause PiTR losing some data when there are too many adjacent short row putting [#13281](https://github.com/tikv/tikv/issues/13281) @[YuJuncen](https://github.com/YuJuncen)
    - Fix a bug that caused checkpoint not advanced when there are some long pessimistic transactions [#13304](https://github.com/tikv/tikv/issues/13304) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that TiKV doesn't distinguish the `DATETIME/DATE/TIMESTAMP/TIME` and `STRING` in json type [#13417](https://github.com/tikv/tikv/issues/13417) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that comparison between json bool and other json value is not compatible with TiDB and MySQL [#13386](https://github.com/tikv/tikv/issues/13386) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that comparison between json bool and other json value is not compatible with TiDB and MySQL [#37481](https://github.com/pingcap/tidb/issues/37481) @[YangKeao](https://github.com/YangKeao)

+ PD

    - grpc: fix the wrong error handler [#5373](https://github.com/tikv/pd/issues/5373) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that unhealthy region cause panic [#5491](https://github.com/tikv/pd/issues/5491) @[nolouch](https://github.com/nolouch)
    - Fix the bug where the Learner Peer of TiFlash Replica might not be created [#5401](https://github.com/tikv/pd/issues/5401) @[HunDunDM](https://github.com/HunDunDM)

+ TiFlash

    - compute

        - Fix the bug that window function may cause tiflash crash when canceled [#5814](https://github.com/pingcap/tiflash/issues/5814) @[SeaRise](https://github.com/SeaRise)
        - fix error data input for date(CAST(value AS DATETIME)) causing high TiFlash sys CPU [#5097](https://github.com/pingcap/tiflash/issues/5097) @[xzhangxian1008](https://github.com/xzhangxian1008)
        - fix that the result of expression casting real or decimal as time is inconsistent with mysql [#3779](https://github.com/pingcap/tiflash/issues/3779) @[mengxin9014](https://github.com/mengxin9014)

    - storage

        - fix the problem that there may be some obsolete data left in storage which cannot be deleted [#5570](https://github.com/pingcap/tiflash/issues/5570) @[JaySon-Huang](https://github.com/JaySon-Huang)
        - fix the problem that there may be some obsolete data left in storage which cannot be deleted [#5659](https://github.com/pingcap/tiflash/issues/5659) @[lidezhu](https://github.com/lidezhu)
        - Fix the bug that page GC may block creating tables [#5697](https://github.com/pingcap/tiflash/issues/5697) @[JaySon-Huang](https://github.com/JaySon-Huang)
        - Fix the panic issue after creating the primary index with a column containing `NULL` value [#5859](https://github.com/pingcap/tiflash/issues/5859) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix issues in "br/tests/up.sh" [#36743](https://github.com/pingcap/tidb/issues/36743) @[pingyu](https://github.com/pingyu)
        - br: raw restore fail in integration test "br_rawkv [#36490](https://github.com/pingcap/tidb/issues/36490) @[pingyu](https://github.com/pingyu)
        - Fix a bug that may cause the information of the checkpoint being stale [#36423](https://github.com/pingcap/tidb/issues/36423) @[YuJuncen](https://github.com/YuJuncen)
        - Fix a bug caused when restoring with high `concurrency` the regions aren't balanced [#37549](https://github.com/pingcap/tidb/issues/37549) @[3pointer](https://github.com/3pointer)
        - Fix a bug that may cause log backup checkpoint TS stuck when some weird ranged regions exist [#37822](https://github.com/pingcap/tidb/issues/37822) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - handle error correctly with wrong pd address but with a grpc service [#6458](https://github.com/pingcap/tiflow/issues/6458) @[crelax](https://github.com/crelax)

    + TiDB Data Migration (DM)

        - Fix a problem that DM will report `Specified key was too long` error [#5315](https://github.com/pingcap/tiflow/issues/5315) @[lance6716](https://github.com/lance6716)
        - Fix a bug that relay goroutine and upstream connections may leak when relay meet error [#6193](https://github.com/pingcap/tiflow/issues/6193) @[lance6716](https://github.com/lance6716)
        - Fix when use "strict" collation_compatible, DM sometimes generate SQL with duplicated collation [#6832](https://github.com/pingcap/tiflow/issues/6832) @[lance6716](https://github.com/lance6716)
        - Reduce the appearing time of the warning message "found error when getting timezone from binlog status_vars" in dm-worker log [#6628](https://github.com/pingcap/tiflow/issues/6628) @[lyzx2001](https://github.com/lyzx2001)
        - Fix a bug that latin1 data may be corrupt when replicating [#7028](https://github.com/pingcap/tiflow/issues/7028) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning does not support columns starting with slash, number, or non-ascii characters in Parquet files [#36980](https://github.com/pingcap/tidb/issues/36980) @[D3Hunter](https://github.com/D3Hunter)

    - TiUP

        - note [#issue]() @[Contributor GitHub ID]()

## Contributors

We would like to thank the following contributors from the TiDB community:

- @[AntiTopQuark](https://github.com/AntiTopQuark)
- @[eltociear](https://github.com/eltociear)
- @[morgo](https://github.com/morgo)
- @[fuzhe1989](https://github.com/fuzhe1989)
- @[crelax](https://github.com/crelax)
- @[Ziy1-Tan](https://github.com/Ziy1-Tan)
- @[AnnieoftheStars](https://github.com/AnnieoftheStars)
- @[An-DJ](https://github.com/An-DJ)
- @[erwadba](https://github.com/erwadba)
- @[whitekeepwork](https://github.com/whitekeepwork)
- @[blacktear23](https://github.com/blacktear23)
- @[rzrymiak](https://github.com/rzrymiak)
- @[AnnieoftheStars](https://github.com/AnnieoftheStars)
- @[jianzhiyao](https://github.com/jianzhiyao)
- @[peakji](https://github.com/peakji)
- @[joycse06](https://github.com/joycse06)
- @[onlyacat](https://github.com/onlyacat)
- @[tisonkun](https://github.com/tisonkun)
- @[BurtonQin](https://github.com/BurtonQin): First-time contributor
