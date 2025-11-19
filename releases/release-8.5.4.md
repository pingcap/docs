---
title: TiDB 8.5.4 Release Notes
summary: Learn about the features, compatibility changes, improvements, and bug fixes in TiDB 8.5.4.
---

# TiDB 8.5.4 Release Notes

Release date: November xx, 2025

TiDB version: 8.5.4

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## Features

* Support redistributing data of a specific table (experimental) [#63260](https://github.com/pingcap/tidb/issues/63260) @[bufferflies](https://github.com/bufferflies)

    PD automatically schedules data to distribute it as evenly as possible across all TiKV nodes in a cluster. However, this automatic scheduling is based on the overall cluster. In some cases, even if the cluster-wide data distribution is balanced, the data of a specific table might still be unevenly distributed across TiKV nodes.

    Starting from v8.5.4, you can use the [`SHOW TABLE DISTRIBUTION`](https://docs.pingcap.com/tidb/v8.5/sql-statement-show-distribution-jobs) statement to check how the data of a specific table is distributed across all TiKV nodes. If the data distribution is unbalanced, you can use the [`DISTRIBUTE TABLE`](https://docs.pingcap.com/tidb/v8.5/sql-statement-distribute-table) statement to redistribute the table's data (experimental) to improve load balancing.

    Note that redistributing the data of a specific table is a one-time task with a timeout limit. If the distribution task is not completed before the timeout, it will automatically exit.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/sql-statement-distribute-table).

* Support `ANALYZE` embedded in DDL statements [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell) @[AilinKid](https://github.com/AilinKid)

    This feature applies to the following types of DDL statements:

    - DDL statements that create new indexes: [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
    - DDL statements that reorganize existing indexes: [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) and [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)

  When this feature is enabled, TiDB automatically runs an `ANALYZE` (statistics collection) operation before the new or reorganized index becomes visible to users. This prevents inaccurate optimizer estimates and potential plan changes caused by temporarily unavailable statistics after index creation or reorganization.

     For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/ddl_embedded_analyze).

* Support creating global indexes on non-unique columns of partitioned tables [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss)

    Starting from v8.3.0, you can create global indexes on unique columns of partitioned tables in TiDB to improve query performance. However, creating global indexes on non-unique columns was not supported. Starting from v8.5.4, TiDB removes this restriction, enabling you to create global indexes on non-unique columns of partitioned tables, which enhances the usability of global indexes.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/partitioned-table#global-indexes).

* Support gracefully shutting down TiFlash [#10266](https://github.com/pingcap/tiflash/issues/10266) @[gengliqi](https://github.com/gengliqi)

    When shutting down a TiFlash server, TiFlash now lets currently running MPP tasks continue for a configurable timeout duration, while rejecting new MPP task requests. The default timeout duration is 600 seconds, and you can adjust it using the [`graceful_wait_shutdown_timeout`](https://docs.pingcap.com/tidb/v8.5/tiflash-configuration#graceful_wait_shutdown_timeout-new-in-v854) configuration item.

    - If all running MPP tasks finish before the timeout duration expires, TiFlash shuts down immediately.
    - If there are still unfinished MPP tasks when the timeout duration expires, TiFlash shuts down forcibly.

  For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/tiflash-configuration#graceful_wait_shutdown_timeout-new-in-v854).

* Introduce a new TiCDC architecture option for improved performance, scalability, and stability [#442](https://github.com/pingcap/ticdc/issues/442) @[CharlesCheung96](https://github.com/CharlesCheung96)

    This new architecture redesigns TiCDC core components and optimizes its data processing workflows, while maintaining compatibility with the configuration, usage, and APIs of the [classic TiCDC architecture](/ticdc/ticdc-classic-architecture.md).

    When configured to use this new architecture, TiCDC achieves near-linear scalability and can replicate millions of tables with lower resource consumption. It also reduces changefeed latency and delivers more stable performance in scenarios with high write workloads, frequent DDL operations, and cluster scaling. Note that the new architecture currently has some [initial limitations](https://docs.pingcap.com/tidb/v8.5/ticdc-architecture#limitations).

    To use the new architecture, set the TiCDC configuration item [`newarch`](https://docs.pingcap.com/tidb/v8.5/ticdc-server-config#newarch-new-in-v854-release1) to `true`.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/ticdc-architecture).

## Compatibility changes

### System variables

- Change the default value of the [`tidb_mpp_store_fail_ttl`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_mpp_store_fail_ttl) system variable from `60s` to `0s`. This means TiDB no longer needs to wait before sending queries to newly started TiFlash nodes, as delays are no longer necessary to prevent query failures. [#61826](https://github.com/pingcap/tidb/issues/61826) @[gengliqi](https://github.com/gengliqi)

- Starting from v8.5.4, the [`tidb_replica_read`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_replica_read-new-in-v40) system variable only takes effect on read-only SQL statements. This change improves data read safety and reduces overlaps with other features. [#62856](https://github.com/pingcap/tidb/issues/62856) @[you06](https://github.com/you06)

- Add the following system variables:

    - [`tidb_opt_enable_no_decorrelate_in_select`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_enable_no_decorrelate_in_select-new-in-v854): controls whether to decorrelate subqueries in the `SELECT` list. The default value is `OFF`. [#51116](https://github.com/pingcap/tidb/issues/51116) @[terry1purcell](https://github.com/terry1purcell)
    - [`tidb_opt_enable_semi_join_rewrite`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_enable_semi_join_rewrite-new-in-v854): controls whether to rewrite `EXISTS` subqueries. The default value is `OFF`. [#44850](https://github.com/pingcap/tidb/issues/44850) @[terry1purcell](https://github.com/terry1purcell)
    - [`tidb_stats_update_during_ddl`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_stats_update_during_ddl-new-in-v854): controls whether to enable the embedded Analyze for DDL. The default value is `OFF`. [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell) @[AilinKid](https://github.com/AilinKid)

### Configuration parameters

- Deprecate the following TiKV configuration items and replace them with the new [`gc.auto-compaction`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file/#gcauto-compaction) configuration group, which controls automatic compaction behavior. [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)

    - Deprecated configuration items: [`region-compact-check-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-check-interval), [`region-compact-check-step`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-check-step), [`region-compact-min-tombstones`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-min-tombstones), [`region-compact-tombstones-percent`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-tombstones-percent), [`region-compact-min-redundant-rows`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-min-redundant-rows-new-in-v710), and [`region-compact-redundant-rows-percent`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-redundant-rows-percent-new-in-v710).
    - New configuration items: [`gc.auto-compaction.check-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#check-interval-new-in-v757-and-v854), [`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#tombstone-num-threshold-new-in-v757-and-v854), [`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#tombstone-percent-threshold-new-in-v757-and-v854), [`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#redundant-rows-threshold-new-in-v757-and-v854), [`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#redundant-rows-percent-threshold-new-in-v757-and-v854), and [`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#bottommost-level-force-new-in-v757-and-v854).

- Add a TiFlash configuration item [`graceful_wait_shutdown_timeout`](https://docs.pingcap.com/tidb/v8.5/tiflash-configuration#graceful_wait_shutdown_timeout-new-in-v854), which controls the maximum wait time when shutting down a TiFlash server. The default value is `600` seconds. During this period, TiFlash continues running unfinished MPP tasks but does not accept new ones. If all running MPP tasks finish before this timeout, TiFlash shuts down immediately; otherwise, it is forcibly shut down after the wait time expires. [#10266](https://github.com/pingcap/tiflash/issues/10266) @[gengliqi](https://github.com/gengliqi)

### MySQL compatibility

Starting from v8.5.4, TiDB aligns its behavior with MySQL when inserting data into a `DECIMAL` column: if the number of decimal places exceeds the column's defined scale, TiDB automatically truncates the extra digits and inserts the truncated data successfully, regardless of how many extra decimal places there are. In earlier TiDB versions, if the number of decimal places in the inserted `DECIMAL` value exceeded 72, the insertion fails and returns an error. For more information, see [Connect to TiDB using JDBC](https://docs.pingcap.com/tidb/v8.5/dev-guide-sample-application-java-jdbc#mysql-compatibility).

## Improvements

+ TiDB

    - Introduce significant performance improvements for certain lossy DDL operations (such as, `BIGINT` → `INT` or `CHAR(120)` → `VARCHAR(60)`), reducing execution time from hours to minutes, seconds, or even milliseconds, delivering performance gains ranging from tens to hundreds of thousands of times [#63366](https://github.com/pingcap/tidb/issues/63366) @[wjhuang2016](https://github.com/wjhuang2016) @[tangenta](https://github.com/tangenta) @[fzzf678](https://github.com/fzzf678)

       Optimization strategies: TiDB pre-checks for potential data truncation risks during type conversion in strict SQL mode; if no risk is detected, TiDB updates only the metadata and avoids index rebuilding whenever possible; if index rebuilding is required, TiDB uses a more efficient ingest process to significantly improve index rebuild performance.

        Performance improvement examples (based on a 100 GiB table benchmark):

        - Non-indexed column: `BIGINT` → `INT` execution time reduced from 2 hours 34 minutes to 1 minute 5 seconds, achieving a 142× speedup
        - Indexed column: `BIGINT` → `INT` execution time reduced from 6 hours 25 minutes to 0.05 seconds, achieving a 460,000× speedup
        - Indexed column: `CHAR(120)` → `VARCHAR(60)` execution time reduced from 7 hours 16 minutes to 12 minutes 56 seconds, achieving a 34× speedup

      Note that the preceding results are based on the precondition that no data truncation occurs during the DDL execution.

    - Support applying the `semi_join_rewrite` hint to Semi Joins in `IN` subqueries [#58829](https://github.com/pingcap/tidb/issues/58829) @[qw4990](https://github.com/qw4990)
    - Optimize the estimation strategy when the `tidb_opt_ordering_index_selectivity_ratio` system variable takes effect [#62817](https://github.com/pingcap/tidb/issues/62817) @[terry1purcell](https://github.com/terry1purcell)
    - Adjust the optimizer selection logic to make newly created indexes more likely to be chosen in certain scenarios [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell)
    - Optimize the query estimation logic for columns with a small number of distinct values (NDV) [#61792](https://github.com/pingcap/tidb/issues/61792) @[terry1purcell](https://github.com/terry1purcell)
    - Optimize the estimation strategy for Index Join queries that include `LIMIT OFFSET` [#45077](https://github.com/pingcap/tidb/issues/45077) @[qw4990](https://github.com/qw4990)
    - Optimize the out-of-range estimation strategy when statistics are not collected in time [#58068](https://github.com/pingcap/tidb/issues/58068) @[terry1purcell](https://github.com/terry1purcell)
    - Add the `backoff` metric to the **Performance Overview** > **SQL Execute Time Overview** panel in Grafana to facilitate debugging [#61441](https://github.com/pingcap/tidb/issues/61441) @[dbsid](https://github.com/dbsid)
    - Add statement ID information to the audit log plugin [#63525](https://github.com/pingcap/tidb/issues/63525) @[YangKeao](https://github.com/YangKeao)

+ TiKV

    - Change the log level of certain automatically recoverable errors in the BR module from `ERROR` to `WARN` to reduce unnecessary alerts [#18493](https://github.com/tikv/tikv/issues/18493) @[YuJuncen](https://github.com/YuJuncen)
    - Change the log level of certain TiKV errors from `ERROR` to `WARN` to reduce unnecessary alerts [#18745](https://github.com/tikv/tikv/issues/18745) @[exit-code-1](https://github.com/exit-code-1)
    - Split the GC check process in the Raft module into two phases to improve the efficiency of garbage collection for redundant MVCC versions in Regions [#18695](https://github.com/tikv/tikv/issues/18695) @[v01dstar](https://github.com/v01dstar)
    - Calculate MVCC redundancy based on GC safe points and RocksDB statistics to improve the efficiency and accuracy of compaction [#18697](https://github.com/tikv/tikv/issues/18697) @[v01dstar](https://github.com/v01dstar)
    - Change the GC handling logic for Region MVCC to be executed by GC worker threads, unifying the overall GC processing logic [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)
    - Optimize the calculation method of the default gRPC thread pool size by making it dynamically calculated based on total CPU quota instead of a fixed value, avoiding performance bottlenecks caused by insufficient gRPC threads [#18613](https://github.com/tikv/tikv/issues/18613) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize the tail latency of async snapshot and write operations in environments with a large number of SST files [#18743](https://github.com/tikv/tikv/issues/18743) @[Connor1996](https://github.com/Connor1996)

+ PD

    - Reduce unnecessary error logs [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)
    - Upgrade the Golang version from 1.23.0 to 1.23.12 and update related dependencies [#9788](https://github.com/tikv/pd/issues/9788) @[JmPotato](https://github.com/JmPotato)
    - Support scattering Regions at the table level to achieve balanced distribution across `scatter-role` and `engine` dimensions [#8986](https://github.com/tikv/pd/issues/8986) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - Skip unnecessary data reads to improve `TableScan` performance [#9875](https://github.com/pingcap/tiflash/issues/9875) @[gengliqi](https://github.com/gengliqi)
    - Optimize `TableScan` performance on wide tables with many columns and sparse data (that is, lots of `NULL` or empty values) in TiFlash [#10361](https://github.com/pingcap/tiflash/issues/10361) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Reduce TiFlash CPU overhead caused by adding vector indexes in clusters with many tables [#10357](https://github.com/pingcap/tiflash/issues/10357) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Minimize unnecessary log output when processing useless Raft commands to reduce log volume [#10467](https://github.com/pingcap/tiflash/issues/10467) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Improve `TableScan` performance on small partitioned tables in TiFlash [#10487](https://github.com/pingcap/tiflash/issues/10487) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiDB Data Migration (DM)

        - Support case-insensitive matching when retrieving the upstream `GTID_MODE` [#12167](https://github.com/pingcap/tiflow/issues/12167) @[OliverS929](https://github.com/OliverS929)

## Bug fixes

+ TiDB

    - Fix the issue that the `use index` hint does not take effect when `tidb_isolation_read_engines` is set to `tiflash` [#60869](https://github.com/pingcap/tidb/issues/60869) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that `max_execution_time` does not take effect for `SELECT FOR UPDATE` statements [#62960](https://github.com/pingcap/tidb/issues/62960) @[ekexium](https://github.com/ekexium)
    - Fix the issue that row count estimates across months or years can be significantly overestimated [#50080](https://github.com/pingcap/tidb/issues/50080) @[terry1purcell](https://github.com/terry1purcell)
    - Fix the issue that the handling of `Decimal` types in prepared statements is inconsistent with MySQL [#62602](https://github.com/pingcap/tidb/issues/62602) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    - Fix the issue that the short path in the `TRUNCATE()` function is incorrectly processed [#57608](https://github.com/pingcap/tidb/issues/57608) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that spilled files might not be fully deleted when the `Out Of Quota For Local Temporary Space` error is triggered [#63216](https://github.com/pingcap/tidb/issues/63216) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that queries using regular expressions against `INFORMATION_SCHEMA` tables might return incorrect results [#62347](https://github.com/pingcap/tidb/issues/62347) @[River2000i](https://github.com/River2000i)
    - Fix the issue that TiDB does not return an error when it fails to get a timestamp from PD [#58871](https://github.com/pingcap/tidb/issues/58871) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that query results differ between the owner TiDB and non-owner TiDB instances during executing `MODIFY COLUMN` statements [#60264](https://github.com/pingcap/tidb/issues/60264) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `ADMIN ALTER DDL JOBS` statements display incorrect parameter values after dynamically modifying parameters [#63201](https://github.com/pingcap/tidb/issues/63201) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that the GC safe point does not advance when adding an index within a transaction [#62424](https://github.com/pingcap/tidb/issues/62424) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that ingesting excessively large SST files into L0 triggers flow control [#63466](https://github.com/pingcap/tidb/issues/63466) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that global sorting is blocked when the CPU-to-memory ratio is 1:2 [#60951](https://github.com/pingcap/tidb/issues/60951) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that pending Distributed eXecution Framework (DXF) tasks cannot be canceled when the number of tasks exceeds 16 [#63896](https://github.com/pingcap/tidb/issues/63896) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that after the DXF task is canceled, other tasks fail to exit [#63927](https://github.com/pingcap/tidb/issues/63927) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that enabling the `Apply` operator concurrency (`tidb_enable_parallel_apply = on`) causes plan generation failure due to a missing clone implementation [#59863](https://github.com/pingcap/tidb/issues/59863) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that using the `ATAN2` function might produce incorrect results [#60093](https://github.com/pingcap/tidb/issues/60093) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that `select 1 from duml` cannot use the instance-level plan cache [#63075](https://github.com/pingcap/tidb/issues/63075) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that changing the join order might cause the planner to fail [#61715](https://github.com/pingcap/tidb/issues/61715) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that using the `set_var` hint with bindings prevents variables from being restored to their original settings [#59822](https://github.com/pingcap/tidb/issues/59822) @[wddevries](https://github.com/wddevries)
    - Fix the issue that setting `ONLY_FULL_GROUP_BY` to a negative value causes validation failure [#62617](https://github.com/pingcap/tidb/issues/62617) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the `ONLY_FULL_GROUP_BY` check is case-insensitive [#62672](https://github.com/pingcap/tidb/issues/62672) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the DP join order algorithm might generate an incorrect plan [#63353](https://github.com/pingcap/tidb/issues/63353) @[winoros](https://github.com/winoros)
    - Fix the issue that rewriting an outer join to an inner join might produce incorrect results [#61327](https://github.com/pingcap/tidb/issues/61327) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that executing certain queries might cause an internal panic [#58600](https://github.com/pingcap/tidb/issues/58600) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the global index might read incorrect data during certain `ALTER PARTITION` operations [#64084](https://github.com/pingcap/tidb/pull/64084) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the global index might return incorrect results in some cases [#61083](https://github.com/pingcap/tidb/issues/61083) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that `character_set_results` truncates incorrect characters instead of replacing them [#61085](https://github.com/pingcap/tidb/issues/61085) @[xhebox](https://github.com/xhebox)
    - Fix the issue that running `ADD COLUMN` and `UPDATE` statements concurrently might cause errors [#60047](https://github.com/pingcap/tidb/issues/60047) @[L-maple](https://github.com/L-maple)
    - Fix the issue that Merge Join might omit filter conditions when calculating costs [#62917](https://github.com/pingcap/tidb/issues/62917) @[qw4990](https://github.com/qw4990)

+ PD

    - Fix the issue that the PD Client retry strategy is not initialized correctly [#9013](https://github.com/tikv/pd/issues/9013) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the TSO HTTP API `/config` and `/members` return incorrect results [#9797](https://github.com/tikv/pd/issues/9797) @[lhy1024](https://github.com/lhy1024)
    - Fix the incorrect error handling logic of TSO Follower Proxy [#9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)
    - Fix the issue that splitting buckets still works even after bucket reporting is disabled [#9726](https://github.com/tikv/pd/issues/9726) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that the Resource Manager incorrectly allocates tokens, causing queries to be stuck [#9455](https://github.com/tikv/pd/issues/9455) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that Placement Rules do not take effect after PD leader switches [#9602](https://github.com/tikv/pd/issues/9602) @[okJiang](https://github.com/okJiang)
    - Fix the issue that PD might fail to parse large numeric values in scientific notation, which consequently causes some TTL-related configurations to not take effect [#9343](https://github.com/tikv/pd/issues/9343) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - Fix the issue that queries might fail when queried columns contain a large number of `NULL` values [#10340](https://github.com/pingcap/tiflash/issues/10340) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash generates inflated statistics for RU consumption [#10380](https://github.com/pingcap/tiflash/issues/10380) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that TiFlash might encounter OOM when slow queries exist under the disaggregated storage and compute architecture [#10278](https://github.com/pingcap/tiflash/issues/10278) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might retry indefinitely when a network partition occurs between TiFlash and S3 under the disaggregated storage and compute architecture [#10424](https://github.com/pingcap/tiflash/issues/10424) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the `FLOOR()` and `CEIL()` functions might return incorrect results when their parameters are of the `DECIMAL` type [#10365](https://github.com/pingcap/tiflash/issues/10365) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that zstd compression in log backup does not take effect, causing the output to remain uncompressed [#18836](https://github.com/tikv/tikv/issues/18836) @[3pointer](https://github.com/3pointer)
        - Fix the issue that the flush operation occasionally becomes slow when backing up data to Azure Blob Storage [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that `log truncate` might occur when file deletion fails [#63358](https://github.com/pingcap/tidb/issues/63358) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that setting `--checksum` to `false` during backup might cause the `count` column in the `mysql.stats_meta` table to become `0` after restore [#60978](https://github.com/pingcap/tidb/issues/60978) @[Leavrth](https://github.com/Leavrth)
        - Reduce the possibility of BR failing to restore data from S3-compatible storage services when the bandwidth limits on these services are enabled [#18846](https://github.com/tikv/tikv/issues/18846) @[kennytm](https://github.com/kennytm)
        - Fix the issue that `log backup observer` might lose the observation on a Region, causing the log backup progress to fail to advance [#18243](https://github.com/tikv/tikv/issues/18243) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that causes `restore point` creation to fail when backed-up tables include certain special schemas [#63663](https://github.com/pingcap/tidb/issues/63663) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - Fix a panic that could occur when configuring a column-type partition dispatcher that includes virtual columns [#12241](https://github.com/pingcap/tiflow/issues/12241) @[wk989898](https://github.com/wk989898)
        - Fix a panic that could occur when closing the DDL puller [#12244](https://github.com/pingcap/tiflow/issues/12244) @[wk989898](https://github.com/wk989898)
        - Support filtering unsupported DDL types through the `ignore-txn-start-ts` parameter in the `filter` configuration [#12286](https://github.com/pingcap/tiflow/issues/12286) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that changefeed tasks might get stuck when using Azure Blob Storage as the downstream [#12277](https://github.com/pingcap/tiflow/issues/12277) @[zurakutsia](https://github.com/zurakutsia)
        - Fix the issue that `DROP FOREIGN KEY` DDL is not replicated to the downstream [#12328](https://github.com/pingcap/tiflow/issues/12328) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that TiCDC might panic when encountering rollback and prewrite entries during Region subscription [#19048](https://github.com/tikv/tikv/issues/19048) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that assertion errors in TiKV might cause TiCDC to panic [#18498](https://github.com/tikv/tikv/issues/18498) @[tharanga](https://github.com/tharanga)
