---
title: TiDB 6.3.0 Release Notes
---

# TiDB 6.3.0 Release Notes

Release date: xx xx, 2022

TiDB version: 6.3.0-DMR

In v6.3.0-DMR, the key new features and improvements are as follows:

- TiKV support SM4 encryption at rest.
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

    TiDB provides [INTERVAL partitioning](/partitioned-table.md#range-interval-partitioning) as a new way of defining Range partitions. You do not need to enumerate all partitions, which drastically reduces the length of Range partitioning DDL statements. The syntax is equivalent to that of the original Range partitioning.

* Range COLUMNS partitioning supports defining multiple columns [#36636](https://github.com/pingcap/tidb/issues/36636) @[mjonss](https://github.com/mjonss)

    Support [PARTITION BY RANGE COLUMNS (column_list)](/partitioned-table.md#range-columns-partitioning). `column_list` is no longer limited to a single column. The basic feature is the same as MySQL.

* EXCHANGE PARTITION becomes GA [#35996](https://github.com/pingcap/tidb/issues/35996) @[ymkzpx](https://github.com/ymkzpx)

    [EXCHANGE PARTITION](/partitioned-table.md#partition-management) becomes GA after performance and stability improvements.

* TiDB supports two more [window functions](/tiflash/tiflash-supported-pushdown-calculations.md) [#5579](https://github.com/pingcap/tiflash/issues/5579) @[SeaRise](https://github.com/SeaRise) **tw：shichun-0415**

    * `LEAD()`
    * `LAG()`

* Provide lightweight metadata lock to improve the DML success rate during DDL change (experimental) [#37275](https://github.com/pingcap/tidb/issues/37275) @[wjhuang2016](https://github.com/wjhuang2016) **tw: Oreoxmt**

    TiDB uses the online asynchronous schema change algorithm to support changing metadata objects. When a transaction is executed, it obtains the corresponding metadata snapshot at the transaction start. If the metadata is changed during a transaction, to ensure data consistency, TiDB returns an `Information schema is changed` error and the transaction fails to commit. To solve the problem, TiDB v6.3.0 introduces [metadata lock](/metadata-lock.md) into the online DDL algorithm. To avoid DML errors whenever possible, TiDB coordinates the priority of DMLs and DDLs during table metadata change, and makes executing DDLs wait for the DMLs with old metadata to commit.

* Improve the performance of adding indexes and reduce its impact on DML transactions [#35983](https://github.com/pingcap/tidb/issues/35983) @[benjamin2037](https://github.com/benjamin2037) **tw: Oreoxmt**

    To improve the speed of backfilling when creating an index, TiDB v6.3.0 accelerates the `ADD INDEX` and `CREATE INDEX` DDL operations when the [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) system variable is enabled. When the feature is enabled, the performance of adding indexes is about trippled.

### Security

* TiKV supports the SM4 algorithm for encryption at rest [#13041](https://github.com/tikv/tikv/issues/13041) @[jiayang-zheng](https://github.com/jiayang-zheng)

    Add the [SM4 algorithm](/encryption-at-rest.md) for TiKV encryption at rest. When you configure encryption at rest, you can enable the SM4 encryption capacity by setting the value of the `data-encryption-method` configuration to `sm4-ctr`.

* TiDB supports authentication with the SM3 algorithm [#36192](https://github.com/pingcap/tidb/issues/36192) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw：ran-huang**

    TiDB adds an authentication plugin [`tidb_sm3_password`](/security-compatibility-with-mysql.md) based on the SM3 algorithm. When this plugin is enabled, the user password is encrypted and validated using the SM3 algorithm.

* TiDB JDBC supports authentication with the SM3 algorithm [#25](https://github.com/pingcap/mysql-connector-j/issues/25) @[lastincisor](https://github.com/lastincisor) **tw：ran-huang**

    Authenticating the user password needs client-side support. Now because [JDBC supports the SM3 algorithm](/develop/dev-guide-choose-driver-or-orm.md#java-drivers), you can connect to TiDB using SM3 authentication via TiDB-JDBC.

### Observability

* TiDB provides fine-grained metrics of SQL query execution time [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk) **tw: Oreoxmt**

    TiDB v6.3.0 provides fine-grained data metrics for [detailed observation of execution time](/latency-breakdown.md). Through the complete and segmented metrics, you can clearly understand the main time consumption of SQL queries, and then quickly find key problems and save time in troubleshooting.

* Enhanced output for slow logs and `TRACE` statements [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk) **tw: Oreoxmt**

    TiDB v6.3.0 enhances the output of slow logs and `TRACE`. You can observe the [full-link duration](/latency-breakdown.md) of SQL queries from TiDB parsing to KV RocksDB writing to disk, which further enhances the diagnostic capabilities.

* TiDB Dashboard provides deadlock history information [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk) **tw: shichun-0415**

    From v6.3.0, TiDB Dashboard provides deadlock history. If you check the slow log in TiDB Dashboard and find the lock waiting time of some SQL statements to be excessively long, you can check the deadlock history to locate the root cause, which makes your diagnosis easier.

### Performance

* TiFlash changes the way of using FastScan (experimental) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

    In v6.2.0, TiFlash introduces the FastScan feature, which brings expected performance improvements but lacks flexibility in use. Therefore, in v6.3.0, TiFlash changes [the way of using FastScan](/develop/dev-guide-use-fastscan.md): the `ALTER TABLE ... SET TIFLASH MODE ...` syntax to enable or disable FastScan is deprecated. Instead, you can use the system variable [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630) to easily control whether to enable FastScan.

    When you upgrade from v6.2.0 to v6.3.0, all FastScan settings in v6.2.0 will become invalid, but will not affect the normal reading of data. You need to set the variable [`tiflash_fastscan`]. When you upgrade from v6.2.0 or an earlier version to v6.3.0, the FastScan feature is not enabled by default for all sessions to keep data consistency.

* TiFlash optimizes data scanning performance in scenarios of multiple concurrency tasks [#5376](https://github.com/pingcap/tiflash/issues/5376) @[JinheLin](https://github.com/JinheLin)

    TiFlash reduces duplicate reads of the same data by combining read operations of the same data. It optimizes the resource overhead and [improves the performance of data scanning in the case of concurrent tasks](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file). For multiple concurrent tasks, it avoids the situation where each task needs to read the same data separately, and avoids the possibility of multiple reads of the same data at the same time.

    This feature is experimental in v6.2.0, and becomes GA in v6.3.0.

* Improve performance of TiFlash data replication [#5237](https://github.com/pingcap/tiflash/issues/5237) @[breezewish](https://github.com/breezewish)

    TiFlash uses the Raft protocol for data replication from TiKV. Prior to v6.3.0, it often took a long time to replicate large amounts of replica data. TiDB v6.3.0 optimizes the TiFlash data replication mechanism and significantly improves the replication speed. When you use BR to recover data, use TiDB Lightning to import data, or add new TiFlash replicas, the TiFlash replicas can be replicated more quickly. You can query with TiFlash in a more timely manner. In addition, TiFlash replicas will also reach a secure and balanced state faster when you scale up, scale down, or modify the number of TiFlash replicas.

* TiKV supports log recycling [#214](https://github.com/tikv/raft-engine/issues/214) @[LykxSassinator](https://github.com/LykxSassinator) **tw：ran-huang**

    TiKV supports [recycling log files](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) in Raft Engine. This reduces the long tail latency in network disks during Raft log appending and improves performance under write workloads.

* TiDB supports null-aware anti join [#37525](https://github.com/pingcap/tidb/issues/37525) @[Arenatlx](https://github.com/Arenatlx) **tw: Oreoxmt**

    TiDB v6.3.0 introduces a new join type [Null-aware anti join (NAAJ)](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries). NAAJ can be aware of whether the collection is empty or `NULL` when processing collection operations. This optimizes the execution efficiency of operations such as `IN` and `= ANY` and improves SQL performance.

* Add optimizer hints to control the build end of Hash Join [#issue]() @[Reminiscent](https://github.com/Reminiscent) **tw: TomShawn**

    In v6.3.0, the TiDB optimizer introduces 2 hints, `HASH_JOIN_BUILD()` and `HASH_JOIN_PROBE()`, to specify the Hash Join, its probe end, and its build end. When the optimizer fails to select the optimal execution plan, you can use these hints to intervene with the plan.

* Support session-level common table expressions (CTE) inline [#36514](https://github.com/pingcap/tidb/issues/36514) @[elsa0520](https://github.com/elsa0520) **tw: shichun-0415**

    TiDB v6.2.0 introduced the `MERGE` hint in optimizers to allow CTE inline, so that the consumers of a CTE query result can execute it in parallel in TiFlash. In v6.3.0, a session variable [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630) is introduced to allow CTE inline in sessions. This can greatly improve the ease of use.

### Transactions

* Support deferring checks of unique constraints in pessimistic transactions [#36579](https://github.com/pingcap/tidb/issues/36579) @[ekexium](https://github.com/ekexium) **tw: qiancai**

    You can use the [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) system variable to control when TiDB checks [unique constraints](/constraints.md#pessimistic-transactions) in pessimistic transactions. This variable is disabled by default. When the variable is enabled (set to `ON`), TiDB will defer locking operations and unique constraint checks in pessimistic transactions until necessary, thus improving the performance of bulk DML operations.

* Optimize the way of fetching TSO in the Read-Committed isolation level [#36812](https://github.com/pingcap/tidb/issues/36812) @[TonsnakeLin](https://github.com/TonsnakeLin) **tw: TomShawn**

    In the Read-Committed isolation level, the system variable [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630) is introduced to control how TSO is fetched. In the case of Plan Cache hit, TiDB improves the execution efficiency of batch DML statements by reducing the frequency of fetching TSO, and reduces the execution time of running tasks in batch.

### Stability

* Modify the default policy of loading statistics when statistics become outdated [#issue]() @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw: TomShawn**

    In v5.3.0, TiDB introduced the system variable [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530) to control how the optimizer behaves when the statistics become outdated. The default value is `ON`, which means keeping the behavior of the old version: When the statistics on objects that are involved in a SQL statement are outdated, the optimizer considers that statistics (other than the total number of rows on the table) are no longer reliable and uses pseudo statistics instead. After tests and analyses of actual user scenarios, the default value of `tidb_enable_pseudo_for_outdated_stats` is changed to `OFF` since v6.3.0. Even if the statistics become outdated, the optimizer will still use the statistics on the table, which makes the execution plan more stable.

* The feature of disabling Titan becomes GA [#issue]() @[tabokie](https://github.com/tabokie) **tw：ran-huang**

    You can [disable Titan](/titan-configuration.md#disable-titan) for online TiKV nodes.

* Use `static` partition pruning when GlobalStats are not ready [#37535](https://github.com/pingcap/tidb/issues/37535) @[Yisaer](https://github.com/Yisaer)

    When [`dynamic pruning`](/partitioned-table.md#dynamic-pruning-mode) is enabled, the optimizer selects execution plans based on [GlobalStats](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode). Before GlobalStats are fully collected, using pseudo statistics might cause performance regression. In v6.3.0, this issue is addressed by maintaining the `static` mode if you enable dynamic pruning before GlobalStats are collected. TiDB remains in the `static` mode until GlobalStats are collected. This ensures performance stability when you change the partition pruning settings.

### Ease of use

### MySQL compatibility

* Improve MySQL 8.0 compatibility by adding support for four regular expression functions: `REGEXP_INSTR()`, `REGEXP_LIKE()`, `REGEXP_REPLACE()`, and `REGEXP_SUBSTR()` [#23881](https://github.com/pingcap/tidb/issues/23881) @[windtalker](https://github.com/windtalker) **tw: Oreoxmt**

    For more details about the compatibility with MySQL, see [Regular expression compatibility with MySQL](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql).

* Improve compatibility of SQL-based data Placement Rules [#37171](https://github.com/pingcap/tidb/issues/37171) @[lcwangchao](https://github.com/lcwangchao)

    TiDB v6.0.0 provides SQL-based data Placement Rules. But this feature is not compatible with TiFlash due to conflicts in implementation mechanisms. TiDB v6.3.0 optimizes this feature, and [improves compatibility of SQL-based data Placement Rules and TiFlash](/placement-rules-in-sql.md#known-limitations).

* The `CREATE USER` and `ALTER USER` statements support the `ACCOUNT LOCK/UNLOCK` option [#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw：ran-huang**

    When you create a user using the [`CREATE USER`](/sql-statements/sql-statement-create-user.md) statement, you can specify whether the created user is locked using the `ACCOUNT LOCK/UNLOCK` option. A locked user cannot log in to the database.

    You can modify the lock state of an existing user using the `ACCOUNT LOCK/UNLOCK` option in the [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) statement.

* JSON data type and JSON functions become GA [#36993](https://github.com/pingcap/tidb/issues/36993) @[xiongjiwei](https://github.com/xiongjiwei) **tw: qiancai**

    JSON is a popular data format adopted by a large number of programs. TiDB has introduced the [JSON support](/data-type-json.md) as an experimental feature since an earlier version, compatible with MySQL's JSON data type and some JSON functions.

    In TiDB v6.3.0, the JSON data type and functions become GA, which enriches TiDB’s data types, supports using JSON functions in [expression indexes](/sql-statements/sql-statement-create-index.md#expression-index) and [generated-columns](/generated-columns.md), and further improves TiDB’s compatibility with MySQL.

### Backup and restore

* PITR supports GCS and Azure Blob Storage as backup storages [#issue]() @[joccau](https://github.com/joccau) **tw: shichun-0415**

    PITR supports [GCS and Azure Blob Storage as backup storage](). If your TiDB is deployed on GCP or Azure, you can use the PITR feature after upgrading your cluster to v6.3.0.

* BR supports AWS S3 Object Lock [#issue]() @[3pointer](https://github.com/3pointer) **tw: shichun-0415**

    After enabling [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html), you can protect backup data from being tampered with or deleted.

### Data migration

* TiDB Lightning supports importing Parquet files exported by Apache Hive into TiDB [#issue]() @[buchuitoudegou](https://github.com/buchuitoudegou) **tw：ran-huang**

    TiDB Lightning supports [importing Parquet files exported by Apache Hive into TiDB](/tidb-lightning/tidb-lightning-data-source.md#parquet), thereby achieving data migration from Hive to TiDB.

* DM adds a new configuration item `safe-mode-duration` in the task configuration file [#6224] (https://github.com/pingcap/tiflow/issues/6224) @[[okJiang](https://github.com/okJiang)] **tw：ran-huang**

    DM adds a new configuration item `safe-mode-duration` in the [task configuration file](/task-configuration-file-full.md). You can adjust the automatic safe mode duration after DM exits abnormally. The default value is 60 seconds. When `safe-mode-duration` is set to `"0s"`, DM does not automatically enter safe mode after an abnormal restart.

### TiDB data share subscription

* TiCDC supports a deployment topology that can replicate data from multiple geo-distributed data sources [#issue]() @[sdojjy](https://github.com/sdojjy) **tw：ran-huang**

    To support replicating data from a single TiDB cluster to multiple geo-distributed data systems, starting from v6.3.0, [you can deploy TiCDC in multiple IDCs](link) to replicate data for each IDC. This feature helps deliver the capability of geo-distributed data replication and deployment topology.

* TiCDC supports keeping the snapshots consistent between the upstream and the downstream (sync point) [#issue]() @[asddongmen](https://github.com/asddongmen) **tw: TomShawn**

    In the scenarios of data replication for disaster recovery, TiCDC supports periodically maintaining a downstream data snapshot so that the downstream snapshot is consistent with the upstream snapshot. With this feature, TiCDC can better support the scenarios where reads and writes are separate, and help you lower the cost.

* TiCDC supports graceful upgrade [#4757](https://github.com/pingcap/tiflow/issues/4757) @[overvenus](https://github.com/overvenus) @[3AceShowHand](https://github.com/3AceShowHand) **tw:ran-huang**

    When TiCDC is deployed using [TiUP](/ticdc/deploy-ticdc.md#rolling-upgrade-ticdc-using-tiup) (>=v1.11.0) or [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/v1.3/configure-a-tidb-cluster#configure-graceful-upgrade-for-ticdc-cluster) (>=v1.3.8), you can gracefully upgrade the TiCDC cluster. During the upgrade, data replication latency is kept as low as 30 seconds. This improves stability, empowering TiCDC to better support latency-sensitive applications.

## Compatibility changes

### System variables

| Variable name | Change type (newly added, modified, or deleted) | Description |
| --- | --- | --- |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) | Modified | Added a new option `tidb_sm3_password`. When this variable is set to `tidb_sm3_password`, the `tidb_sm3_password` method is used as the encryption algorithm. |
| [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630) | Newly added | This variable is used to control the threshold at which the TiDB server prefers to send read requests to the replica in the same region as the TiDB server when [`tidb_replica_read`](#tidb_replica_read-new-in-v40) is set to `closest-adaptive`. |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) | Newly added | This variable is used to control when TiDB checks [unique constraints](/constraints.md#pessimistic-transactions) in pessimistic transactions |
| [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630) | Newly added | This variable only takes effect when [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) is enabled. It sets the usage limit of local storage during backfilling when creating an index.  |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) | Newly added | This variable controls whether to enable the acceleration of `ADD INDEX` and `CREATE INDEX` DDl operations to improve the speed of backfilling when creating an index. |
| [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50) | Modified | The default value of this variable changes from `INT_ONLY` to `ON`. |
| [`tidb_enable_exchange_partition`](/system-variables.md#tidb_enable_exchange_partition) | Deprecated | This variable controls whether to enable the [`exchange partitions with tables`](/partitioned-table.md#partition-management) feature. The default value is `ON`, that is, exchange partitions with tables is enabled by default.  |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)| Newly added | This variable is used to set whether to enable the [Metadata lock](/metadata-lock.md) feature. |
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530) | Modified | This variable controls the behavior of the optimizer on using statistics of a table when the statistics are outdated. The default value changes from `ON` to `OFF`, which means the optimizer still keeps using the statistics of the table even if the statistics of this table is outdated. |
| [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action) | Modified | This variable controls whether to enable the dynamic memory control feature for the operator that reads data. When this variable is set to `ON`, the memory usage might not be under the control of [tidb_mem_quota_query](/system-variables.md#tidb_mem_quota_query). Therefore, the default value is changed from `ON` to `OFF`. |
| [`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630) | Newly added | This variable controls whether to replace expressions with generated columns in an unsafe way. |
| [`tidb_last_plan_replayer_token`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630) | Newly added | This variable is read-only and is used to obtain the result of the last `PLAN REPLAYER DUMP` execution in the current session. |
| [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630) | Newly added | This variable is used to control whether common table expressions (CTEs) in the entire session are inlined or not. The default value is `OFF`, which means that inlining CTE is not enforced by default. |
| [`tidb_opt_three_stage_distinct_agg`](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630) | Newly added | This variable specifies whether to rewrite a `COUNT(DISTINCT)` aggregation into a three-stage aggregation in MPP mode. The default value is `ON`. |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-从-v51-版本开始引入) | Modified | Specifies whether to enable dynamic pruning. Since v6.3.0, the default value changes to `dynamic`. |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600) | Modified | This variable is used to optimize the timestamp acquisition, which is suitable for scenarios with read-committed isolation level where read-write conflicts are rare. This feature is oriented to specific service workloads and might cause performance regression in other scenarios. For this reason, since v6.3.0, the scope of this variable changes from `GLOBAL | SESSION` to `INSTANCE`. That means you can enable this feature for specific TiDB instances. |
| [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)  | Newly added | This variable is used to optimize the acquisition of timestamps and is suitable for scenarios with few point-write conflicts in `READ-COMMITTED` isolation level of pessimistic transactions. Enabling this variable can avoid the latency and overhead brought by obtaining the global timestamps during the execution of point-write statements |
| [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630) | Newly added | This variable controls whether to enable FastScan. If [FastScan](/develop/dev-guide-use-fastscan.md) is enabled (set to `ON`), TiFlash provides more efficient query performance, but does not guarantee the accuracy of the query results or data consistency. |

### Configuration file parameters

| Configuration file | Configuration | Change type | Description |
| --- | --- | --- | --- |
| TiDB | [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630) | Newly added | Specifies the file system location used by TiDB to store temporary data. If a feature requires local storage in TiDB nodes, TiDB stores the corresponding temporary data in this location. The default value is `/tmp/tidb`. |
| TiKV | [`auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630) | Newly added | Controls whether to automatically adjust the thread pool size. When it is enabled, the read performance of TiKV is optimized by automatically adjusting the UnifyReadPool thread pool size based on the current CPU usage.|
| TiKV | [`data-encryption-method`](/tikv-configuration-file.md#data-encryption-method) | Modified | Introduces a new value option `sm4-ctr`. When this configuration item is set to `sm4-ctr`, data is encrypted using SM4 before being stored. |
| TiKV | [`enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) | Newly added | Determines whether to recycle stale log files in Raft Engine. When it is enabled, logically purged log files will be reserved for recycling. This reduces the long tail latency on write workloads. This configuration item is only available when [format-version](/tikv-configuration-file.md#format-version-new-in-v630) is >= 2. |
| TiKV | [`format-version`](/tikv-configuration-file.md#format-version-new-in-v630) | Newly added | Specifies the version of log files in Raft Engine. The default log file version is `1` for TiKV earlier than v6.3.0. The log files can be read by TiKV >= v6.1.0. The default log file version is `2` for TiKV v6.3.0 and later. TiKV v6.3.0 and later can read the log files. |
| TiKV | [`log-backup.enable`](/tikv-configuration-file.md#enable-new-in-v620) | Modified | Since v6.3.0, the default value changes from `false` to `true`. |
| TiKV | [`log-backup.max-flush-interval`](/tikv-configuration-file.md#max-flush-interval-new-in-v620) | Modified | Since v6.3.0, the default value changes from `5min` to `3min`. |
| PD | [enable-diagnostic](/pd-configuration-file.md#enable-diagnostic-new-in-v630) | Newly added | Controls whether to enable the diagnostic feature. The default value is `false`. |
| TiFlash | [`dt_enable_read_thread`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | Deprecated | Since v6.3.0, this configuration item is deprecated. The thread pool is used to handle read requests from the storage engine by default and cannot be disabled. |
| DM | [`safe-mode-duration`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | Newly added | Specifies the duration of the automatic safe mode. |
| TiCDC | [`enable-sync-point`](/ticdc/manage-ticdc.md#task-configuration-file) | Newly added | Specifies whether to enable the Syncpoint feature. |
| TiCDC | [`sync-point-interval`](/ticdc/manage-ticdc.md#task-configuration-file) | Newly added | Specifies the interval at which Syncpoint aligns the upstream and downstream snapshots. |
| TiCDC | [`sync-point-retention`](/ticdc/manage-ticdc.md#task-configuration-file) | Newly added | Specifies how long the data is retained by Syncpoint in the downstream table. When this duration is exceeded, the data is cleaned up. |
| TiCDC | [`sink-uri.memory`](/ticdc/manage-ticdc.md#create-a-replication-task) | Deprecated | This configuration item is deprecated. It is not recommended to use it in any situation. |

### Others

* Improve MySQL compatibility by supporting the `ACCOUNT LOCK` and `ACCOUNT UNLOCK` options.
* Log backup supports GCS and Azure Blob Storage as backup storage.
* Log backup is now compatible with the `exchange partition` DDL.
* The SQL statement `ALTER TABLE ...SET TiFLASH MODE ...` previously used for enabling [fastscan](/develop/dev-guide-use-fastscan.md) is deprecated, and replaced by the system variable [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630). When you upgrade from v6.2.0 to v6.3.0, all FastScan settings in v6.2.0 will become invalid, but will not affect the normal reading of data. You need to set the variable [`tiflash_fastscan`]. When you upgrade from an earlier version to v6.3.0, the FastScan feature is not enabled by default for all sessions to keep data consistency.

## Removed feature

Since v6.3.0, TiCDC no longer supports configuring Pulsar sink. [kop](https://github.com/streamnative/kop) provided by StreamNative can be used as an alternative.

## Improvements

+ TiDB

    - [`PLAN REPLAYER`](/sql-plan-replayer) can be used on multiple SQL statements, which makes troubleshooting more efficient [#37798](https://github.com/pingcap/tidb/issues/37798) @[Yisaer](https://github.com/Yisaer)
    - Improve warning log when new connection arrives [#34964](https://github.com/pingcap/tidb/issues/34964) @[xiongjiwei](https://github.com/xiongjiwei)

    - sql-infra

        - Grant privilege of a table to an user checks the target table exist first, in the past, the table name comparison works in a case sensitive manner, now it's changed to case insensitive [#34610](https://github.com/pingcap/tidb/issues/34610) @[tiancaiamao](https://github.com/tiancaiamao)
        - Previously, TiDB users can set `init_connect` without any checking. From now on, the value of `init_connect` should be checked by the sql parser [#35324](https://github.com/pingcap/tidb/issues/35324) @[CbcWestwolf](https://github.com/CbcWestwolf)

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
        - Support Planner Interpreter [#4739](https://github.com/pingcap/tiflash/issues/4739) @[SeaRise](https://github.com/SeaRise)
        - Support to pushdown hex to TiFlash [#5107](https://github.com/pingcap/tiflash/issues/5107) @[YangKeao](https://github.com/YangKeao)
        - Suppress the "tcp set inq" loggings [#4940](https://github.com/pingcap/tiflash/issues/4940)
        - Improve the accuracy of memory tracker in TiFlash [#5610](https://github.com/pingcap/tiflash/pull/5610)
        - Improve the performance of string column with `UTF8_BIN/ASCII_BIN/LATIN1_BIN/UTF8MB4_BIN` collation [#5294](https://github.com/pingcap/tiflash/issues/5294)

    - storage

        - Calculate the io throughput in background in ReadLimiter [#5401](https://github.com/pingcap/tiflash/issues/5401), [#5091](https://github.com/pingcap/tiflash/issues/5091) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ Tools

    + Backup & Restore (BR)

        - PITR now aggregates a batch of files, which would greatly reduce the number of backup file. [#13232](https://github.com/tikv/tikv/issues/13232) @[Leavrth](https://github.com/Leavrth)
        - PITR now supports automatically config TiFlash replica number after the restoration. [#37208](https://github.com/pingcap/tidb/issues/37208) @[YuJuncen](https://github.com/YuJuncen)

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

        - Fix the issue that `PREAPRE` statements do not check privileges [#35784](https://github.com/pingcap/tidb/issues/35784) @[lcwangchao](https://github.com/lcwangchao)
        - System variable `tidb_enable_noop_variable` cannot be set to `WARN` [#36647](https://github.com/pingcap/tidb/issues/36647) @[lcwangchao](https://github.com/lcwangchao)
        - Fix the issue that when 'expression index' is defined, the value of `ORDINAL_POSITION` column of `INFORMAITON_SCHEMA`.`COLUMNS` table might be incorrect [#31200](https://github.com/pingcap/tidb/issues/31200) @[bb7133](https://github.com/bb7133)
        - Fix the issue that when setting a timestamp that is larger than `MAXINT32`, TiDB doesn't report an error like MySQL [#31585](https://github.com/pingcap/tidb/issues/31585) @[bb7133](https://github.com/bb7133)
        - Fix the panic issue of enterprise plugin on 6.1 [#37319](https://github.com/pingcap/tidb/issues/37319) @[xhebox](https://github.com/xhebox)
        - Fix the incorrect output of `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526) @[xhebox](https://github.com/xhebox)
        - Disallow exchange partition with temporary table [#37201](https://github.com/pingcap/tidb/issues/37201) @[lcwangchao](https://github.com/lcwangchao)
        - Fix the issue that query on `INFORMATION_SCHEMA.TIKV_REGION_STATUS` returns an incorrect result @[zimulala](https://github.com/zimulala)
        - Fix the issue that `EXPLAIN` query on views does not check privileges [#34326](https://github.com/pingcap/tidb/issues/34326) @[hawkingrei](https://github.com/hawkingrei)
        - Fix the issue that the user cannot update from JSON 'null' to NULL [#37852](https://github.com/pingcap/tidb/issues/37852) @[YangKeao](https://github.com/YangKeao)
        - Optimize DDL history HTTP API, and add support for 'start_job_id' parameter [#35838](https://github.com/pingcap/tidb/issues/35838) @[tiancaiamao](https://github.com/tiancaiamao)
        - Fix the issue that `row_count` of DDL jobs is inaccurate [#25968](https://github.com/pingcap/tidb/issues/25968) @[Defined2014](https://github.com/Defined2014)
        - Fix the issue that `FLASHBACK TABLE` does not work properly [#37386](https://github.com/pingcap/tidb/issues/37386) @[tiancaiamao](https://github.com/tiancaiamao)

    - execution

        - Fix wrong result when enabling dynamic mode in partition table for tiflash [#37254](https://github.com/pingcap/tidb/issues/37254) @[wshwsh12](https://github.com/wshwsh12)
        - Fix the issue that the cast and comparison between binary string and json is incompatible with MySQL [#31918](https://github.com/pingcap/tidb/issues/31918) @[YangKeao](https://github.com/YangKeao)
        - Fix the issue that the cast and comparison between binary string and json is incompatible with MySQL [#25053](https://github.com/pingcap/tidb/issues/25053) @[YangKeao](https://github.com/YangKeao)
        - Fix the issue that the json_objectagg and json_arrayagg is not compatible with MySQL on binary value [#25053](https://github.com/pingcap/tidb/issues/25053) @[YangKeao](https://github.com/YangKeao)

    - transaction

        - bugfix: do not acquire pessimistic lock for non-unique index keys [#36235](https://github.com/pingcap/tidb/issues/36235)
        - Fix the auto-commit mode change related transaction commit behaviours [#36581](https://github.com/pingcap/tidb/issues/36581) @[cfzjywxk](https://github.com/cfzjywxk)
        - Fix the issue explain analyze with DML executors may respond to the client before the transaction commit has finished [#37273](https://github.com/pingcap/tidb/issues/37373) @[cfzjywxk](https://github.com/cfzjywxk)

    - planner

        - fix update plan's projection elimination will cause column resolution error [#37568](https://github.com/pingcap/tidb/issues/37568) @[AilinKid](https://github.com/AilinKid)
        - planner: fix outer join reorder will push down its outer join condition [#37238](https://github.com/pingcap/tidb/issues/37238) @[AilinKid](https://github.com/AilinKid)
        - make the both side operand of NAAJ & refuse partial column substitute in projection elimination [#37032](https://github.com/pingcap/tidb/issues/37032) @[AilinKid](https://github.com/AilinKid)
        - planner: correct the redundant field meaning in join full schema when join coalesce [#36420](https://github.com/pingcap/tidb/issues/36420) @[AilinKid](https://github.com/AilinKid)
        - Fix a wrong casting in building union plan [#31678](https://github.com/pingcap/tidb/issues/31678) @[bb7133](https://github.com/bb7133)

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
        - Fix the bug that wrong data input for `cast(value as datetime)` causing high TiFlash sys CPU [#5097](https://github.com/pingcap/tiflash/issues/5097) @[xzhangxian1008](https://github.com/xzhangxian1008)
        - fix that the result of expression casting real or decimal as time is inconsistent with mysql [#3779](https://github.com/pingcap/tiflash/issues/3779) @[mengxin9014](https://github.com/mengxin9014)

    - storage

        - fix the problem that there may be some obsolete data left in storage which cannot be deleted [#5659](https://github.com/pingcap/tiflash/issues/5659) @[lidezhu](https://github.com/lidezhu)
        - Fix the bug that page GC may block creating tables [#5697](https://github.com/pingcap/tiflash/issues/5697) @[JaySon-Huang](https://github.com/JaySon-Huang)
        - Fix the panic issue after creating the primary index with a column containing `NULL` value [#5859](https://github.com/pingcap/tiflash/issues/5859) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix issues in "br/tests/up.sh" [#36743](https://github.com/pingcap/tidb/issues/36743) @[pingyu](https://github.com/pingyu)
        - br: raw restore fail in integration test "br_rawkv [#36490](https://github.com/pingcap/tidb/issues/36490) @[pingyu](https://github.com/pingyu)
        - Fix a bug that may cause the information of the checkpoint being stale [#36423](https://github.com/pingcap/tidb/issues/36423) @[YuJuncen](https://github.com/YuJuncen)
        - Fix a bug caused when restoring with high `concurrency` the regions aren't balanced [#37549](https://github.com/pingcap/tidb/issues/37549) @[3pointer](https://github.com/3pointer)
        - Fix a bug that may cause log backup checkpoint TS stuck when TiCDC exists in cluster [#37822](https://github.com/pingcap/tidb/issues/37822) @[YuJuncen](https://github.com/YuJuncen)
        Fix a bug that caused: when the backup meta v2 enabled, there may be too many meta files. [#37244](https://github.com/pingcap/tidb/issues/37244) [@MoCuishle28](https://github.com/MoCuishle28)
        - Fix a bug that may lead to the backup / restore failure if some special character in the authorize key of external storages. [#37469](https://github.com/pingcap/tidb/issues/37469) [@MoCuishle28](https://github.com/MoCuishle28)

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
