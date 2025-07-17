---
title: TiDB 7.5.2 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.5.2.
---

# TiDB 7.5.2 Release Notes

Release date: June 13, 2024

TiDB version: 7.5.2

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## Compatibility changes

- Add a TiKV configuration item [`track-and-verify-wals-in-manifest`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#track-and-verify-wals-in-manifest-new-in-v659-v715-and-v752) for RocksDB, which helps you investigate possible corruption of Write Ahead Log (WAL) [#16549](https://github.com/tikv/tikv/issues/16549) @[v01dstar](https://github.com/v01dstar)
- Must set the line terminator when using TiDB Lightning `strict-format` or `SPLIT_FILE` to import CSV files [#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)
- Add the `sink.open.output-old-value` configuration item for TiCDC Open Protocol to control whether to output the value before the update to the downstream [#10916](https://github.com/pingcap/tiflow/issues/10916) @[sdojjy](https://github.com/sdojjy)
- In earlier versions, when processing a transaction containing `UPDATE` changes, if the primary key or non-null unique index value is modified in an `UPDATE` event, TiCDC splits this event into `DELETE` and `INSERT` events. Starting from v7.5.2, when using the MySQL sink, TiCDC splits an `UPDATE` event into `DELETE` and `INSERT` events if the transaction `commitTS` for the `UPDATE` change is less than TiCDC `thresholdTS` (which is the current timestamp fetched from PD when TiCDC starts replicating the corresponding table to the downstream). This behavior change addresses the issue of downstream data inconsistencies caused by the potentially incorrect order of `UPDATE` events received by TiCDC, which can lead to an incorrect order of split `DELETE` and `INSERT` events. For more information, see [documentation](https://docs.pingcap.com/tidb/v7.5/ticdc-split-update-behavior#split-update-events-for-mysql-sinks). [#10918](https://github.com/pingcap/tiflow/issues/10918) @[lidezhu](https://github.com/lidezhu)

## Improvements

+ TiDB

    - Optimize the issue that the `ANALYZE` statement blocks the metadata lock [#47475](https://github.com/pingcap/tidb/issues/47475) @[wjhuang2016](https://github.com/wjhuang2016)
    - Improve the MySQL compatibility of expression default values displayed in the output of `SHOW CREATE TABLE` [#52939](https://github.com/pingcap/tidb/issues/52939) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Enhance the handling of DNF items that are always `false` by directly ignoring such filter conditions, thus avoiding unnecessary full table scans [#40997](https://github.com/pingcap/tidb/issues/40997) @[hi-rustin](https://github.com/Rustin170506)
    - Optimize the statistics for the execution process of the TiFlash `TableScan` operator in `EXPLAIN ANALYZE` [#51727](https://github.com/pingcap/tidb/issues/51727) @[JinheLin](https://github.com/JinheLin)
    - Remove stores without Regions during MPP load balancing [#52313](https://github.com/pingcap/tidb/issues/52313) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Support loading Regions in batch from PD to speed up the conversion process from the KV range to Regions when querying large tables [#51326](https://github.com/pingcap/tidb/issues/51326) @[SeaRise](https://github.com/SeaRise)
    - On the `Resource Control` monitoring page, add a new panel `RU(Max)` to show the maximum RU consumption rate for each resource group [#49318](https://github.com/pingcap/tidb/issues/49318) @[nolouch](https://github.com/nolouch)
    - Improve sync load performance to reduce latency in loading statistics [#52994](https://github.com/pingcap/tidb/issues/52294) [hawkingrei](https://github.com/hawkingrei)
    - Increase concurrency of statistics initialization to speed up startup [#52466](https://github.com/pingcap/tidb/issues/52466) [#52102](https://github.com/pingcap/tidb/issues/52102) [#52553](https://github.com/pingcap/tidb/issues/52553) [hawkingrei](https://github.com/hawkingrei)

+ TiKV

    - Adjust the log level of coprocessor errors from `warn` to `debug` to reduce unnecessary logs of the cluster [#15881](https://github.com/tikv/tikv/issues/15881) @[cfzjywxk](https://github.com/cfzjywxk)
    - Add monitoring metrics for the queue time for processing CDC events to facilitate troubleshooting downstream CDC event latency issues [#16282](https://github.com/tikv/tikv/issues/16282) @[hicqu](https://github.com/hicqu)
    - Avoid performing IO operations on snapshot files in raftstore threads to improve TiKV stability [#16564](https://github.com/tikv/tikv/issues/16564) @[Connor1996](https://github.com/Connor1996)
    - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)
    - When TiKV detects the existence of corrupted SST files, it logs the specific reasons for the corruption [#16308](https://github.com/tikv/tikv/issues/16308) @[overvenus](https://github.com/overvenus)
    - Remove unnecessary async blocks to reduce memory usage [#16540](https://github.com/tikv/tikv/issues/16540) @[overvenus](https://github.com/overvenus)
    - Accelerate the shutdown speed of TiKV [#16680](https://github.com/tikv/tikv/issues/16680) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - Upgrade the etcd version to v3.4.30 [#7904](https://github.com/tikv/pd/issues/7904) @[JmPotato](https://github.com/JmPotato)
    - Add the monitoring metric for the maximum Request Unit (RU) per second [#7908](https://github.com/tikv/pd/issues/7908) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - Mitigate the issue that TiFlash might panic due to updating certificates after TLS is enabled [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - BR cleans up empty SST files during data recovery [#16005](https://github.com/tikv/tikv/issues/16005) @[Leavrth](https://github.com/Leavrth)
        - Add PITR integration test cases to cover compatibility testing for log backup and adding index acceleration [#51987](https://github.com/pingcap/tidb/issues/51987) @[Leavrth](https://github.com/Leavrth)
        - Enhance the tolerance of log backup to merge operations. When encountering a reasonably long merge operation, log backup tasks are less likely to enter the error state [#16554](https://github.com/tikv/tikv/issues/16554) @[YuJuncen](https://github.com/YuJuncen)
        - Improve the table creation performance of the `RESTORE` statement in scenarios with large datasets [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - Support pre-allocating Table ID during the restore process to maximize the reuse of Table ID and improve restore performance [#51736](https://github.com/pingcap/tidb/issues/51736) @[Leavrth](https://github.com/Leavrth)
        - Remove the invalid verification for active DDL jobs when log backup starts [#52733](https://github.com/pingcap/tidb/issues/52733) @[Leavrth](https://github.com/Leavrth)
        - Remove an outdated compatibility check when using Google Cloud Storage (GCS) as the external storage [#50533](https://github.com/pingcap/tidb/issues/50533) @[lance6716](https://github.com/lance6716)
        - Increase the number of retries for failures caused by DNS errors [#53029](https://github.com/pingcap/tidb/issues/53029) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Improve memory stability during data recovery using redo logs to reduce the probability of OOM [#10900](https://github.com/pingcap/tiflow/issues/10900) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Significantly improve the stability of data replication in transaction conflict scenarios, with up to 10 times performance improvement [#10896](https://github.com/pingcap/tiflow/issues/10896) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Enable the PD client forwarding function to make TiCDC more stable during network isolation between TiCDC and the PD leader [#10849](https://github.com/pingcap/tiflow/issues/10849) @[asddongmen](https://github.com/asddongmen)
        - Improve the initialization speed of replication tasks [#11124](https://github.com/pingcap/tiflow/issues/11124) @[asddongmen](https://github.com/asddongmen)
        - Initialize replication tasks asynchronously to reduce initialization time for the processor and owner [#10845](https://github.com/pingcap/tiflow/issues/10845) @[sdojjy](https://github.com/sdojjy)
        - Detect the Kafka cluster version automatically to improve compatibility with Kafka [#10852](https://github.com/pingcap/tiflow/issues/10852) @[wk989898](https://github.com/wk989898)

## Bug fixes

+ TiDB

    - Fix the issue of inconsistent data indexes caused by concurrent DML operations when adding a unique index [#52914](https://github.com/pingcap/tidb/issues/52914) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue of inconsistent data indexes caused by adding indexes with multi-schema changes on partitioned tables [#52080](https://github.com/pingcap/tidb/issues/52080) @[tangenta](https://github.com/tangenta)
    - Fix the issue of inconsistent data indexes caused by adding multi-valued indexes [#51162](https://github.com/pingcap/tidb/issues/51162) @[ywqzzy](https://github.com/ywqzzy)
    - Fix the issue that DDL operations get stuck due to network problems [#47060](https://github.com/pingcap/tidb/issues/47060) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that TiDB might report an error due to GC when loading statistics at startup [#53592](https://github.com/pingcap/tidb/issues/53592) @[you06](https://github.com/you06)
    - Fix the issue that TiDB might send requests to unready TiKV nodes [#50758](https://github.com/pingcap/tidb/issues/50758) @[zyguan](https://github.com/zyguan)
    - Fix the issue that Stale Read might miss after a TiKV rolling restart [#52193](https://github.com/pingcap/tidb/issues/52193) @[zyguan](https://github.com/zyguan)
    - Fix the issue that data race might occur during KV request retries, leading to TiDB panics [#51921](https://github.com/pingcap/tidb/issues/51921) @[zyguan](https://github.com/zyguan)
    - Fix the issue that TiDB might panic when parsing index data [#47115](https://github.com/pingcap/tidb/issues/47115) @[zyguan](https://github.com/zyguan)
    - Fix the issue that TiDB might panic when the JOIN condition contains an implicit type conversion [#46556](https://github.com/pingcap/tidb/issues/46556) @[qw4990](https://github.com/qw4990)
    - Fix the issue that comparing a column of `YEAR` type with an unsigned integer that is out of range causes incorrect results [#50235](https://github.com/pingcap/tidb/issues/50235) @[qw4990](https://github.com/qw4990)
    - Fix the issue that subqueries in an `UPDATE` list might cause TiDB to panic [#52687](https://github.com/pingcap/tidb/issues/52687) @[winoros](https://github.com/winoros)
    - Fix the overflow issue of the `Longlong` type in predicates [#45783](https://github.com/pingcap/tidb/issues/45783) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `SELECT INTO OUTFILE` does not work when clustered indexes are used as predicates [#42093](https://github.com/pingcap/tidb/issues/42093) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the TopN operator might be pushed down incorrectly [#37986](https://github.com/pingcap/tidb/issues/37986) @[qw4990](https://github.com/qw4990)
    - Fix the issue that an empty projection causes TiDB to panic [#49109](https://github.com/pingcap/tidb/issues/49109) @[winoros](https://github.com/winoros)
    - Fix the issue that Index Merge incorrectly pushes partial limit down when index plans are kept ordered [#52947](https://github.com/pingcap/tidb/issues/52947) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that using a view does not work in recursive CTE [#49721](https://github.com/pingcap/tidb/issues/49721) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that unstable unique IDs of columns might cause the `UPDATE` statement to return errors [#53236](https://github.com/pingcap/tidb/issues/53236) @[winoros](https://github.com/winoros)
    - Fix the issue that TiDB panics when executing the `SHOW ERRORS` statement with a predicate that is always `true` [#46962](https://github.com/pingcap/tidb/issues/46962) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that the `final` AggMode and the `non-final` AggMode cannot coexist in Massively Parallel Processing (MPP) [#51362](https://github.com/pingcap/tidb/issues/51362) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that a wrong TableDual plan causes empty query results [#50051](https://github.com/pingcap/tidb/issues/50051) @[onlyacat](https://github.com/onlyacat)
    - Fix the issue that TiDB might panic when initializing statistics after enabling both `lite-init-stats` and `concurrently-init-stats` [#52223](https://github.com/pingcap/tidb/issues/52223) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `NO_JOIN` hints do not work with `CREATE BINDING` [#52813](https://github.com/pingcap/tidb/issues/52813) @[qw4990](https://github.com/qw4990)
    - Fix the issue that subqueries included in the `ALL` function might cause incorrect results [#52755](https://github.com/pingcap/tidb/issues/52755) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `VAR_SAMP()` cannot be used as a window function [#52933](https://github.com/pingcap/tidb/issues/52933) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that column pruning without using shallow copies of slices might cause TiDB to panic [#52768](https://github.com/pingcap/tidb/issues/52768) @[winoros](https://github.com/winoros)
    - Fix the issue that adding a unique index might cause TiDB to panic [#52312](https://github.com/pingcap/tidb/issues/52312) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the TiDB server is marked as health before the initialization is complete [#51596](https://github.com/pingcap/tidb/issues/51596) @[shenqidebaozi](https://github.com/shenqidebaozi)
    - Fix the issue that the type returned by the `IFNULL` function is inconsistent with MySQL [#51765](https://github.com/pingcap/tidb/issues/51765) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that parallel `Apply` might generate incorrect results when the table has a clustered index [#51372](https://github.com/pingcap/tidb/issues/51372) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that query results might be incorrect when the `HAVING` clause in a subquery contains correlated columns [#51107](https://github.com/pingcap/tidb/issues/51107) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that querying the `TIDB_HOT_REGIONS` table might incorrectly return `INFORMATION_SCHEMA` tables [#50810](https://github.com/pingcap/tidb/issues/50810) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that automatic statistics collection is triggered before the initialization of statistics finishes [#52346](https://github.com/pingcap/tidb/issues/52346) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that AutoID Leader change might cause the value of the auto-increment column to decrease in the case of `AUTO_ID_CACHE=1` [#52600](https://github.com/pingcap/tidb/issues/52600) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that query results might be incorrect when you use Common Table Expressions (CTE) to access partitioned tables with missing statistics [#51873](https://github.com/pingcap/tidb/issues/51873) @[qw4990](https://github.com/qw4990)
    - Fix the incorrect calculation and display of the number of connections (Connection Count) on the TiDB Dashboard Monitoring page [#51889](https://github.com/pingcap/tidb/issues/51889) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that DDL operations get stuck when restoring a table with the foreign key [#51838](https://github.com/pingcap/tidb/issues/51838) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that getting the default value of a column returns an error if the column default value is dropped [#50043](https://github.com/pingcap/tidb/issues/50043) [#51324](https://github.com/pingcap/tidb/issues/51324) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that TiDB does not listen to the corresponding port when `force-init-stats` is configured [#51473](https://github.com/pingcap/tidb/issues/51473) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the query result is incorrect when the `IN()` predicate contains `NULL` [#51560](https://github.com/pingcap/tidb/issues/51560) @[winoros](https://github.com/winoros)
    - Fix the issue that the TiDB synchronously loading statistics mechanism retries to load empty statistics indefinitely and prints the `fail to get stats version for this histogram` log [#52657](https://github.com/pingcap/tidb/issues/52657) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `EXCHANGE PARTITION` incorrectly processes foreign keys [#51807](https://github.com/pingcap/tidb/issues/51807) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that `LIMIT` might not be pushed down to the `OR` type `Index Merge` [#48588](https://github.com/pingcap/tidb/issues/48588) @[AilinKid](https://github.com/AilinKid)
    - Fix the incorrect result of the TopN operator in correlated subqueries [#52777](https://github.com/pingcap/tidb/issues/52777) @[yibin87](https://github.com/yibin87)
    - Fix the issue that the `CPS by type` metric displays incorrect values [#52605](https://github.com/pingcap/tidb/issues/52605) @[nolouch](https://github.com/nolouch)
    - Fix the issue that the `EXPLAIN` statement might display incorrect column IDs in the result when statistics for certain columns are not fully loaded [#52207](https://github.com/pingcap/tidb/issues/52207) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that expressions containing different collations might cause the query to panic when the new framework for collations is disabled [#52772](https://github.com/pingcap/tidb/issues/52772) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that executing SQL statements containing tables with multi-valued indexes might return the `Can't find a proper physical plan for this query` error [#49438](https://github.com/pingcap/tidb/issues/49438) @[qw4990](https://github.com/qw4990)
    - Fix the issue that TiDB cannot correctly convert the type of a system variable in an expression [#43527](https://github.com/pingcap/tidb/issues/43527) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that executing `INSERT IGNORE` might result in inconsistency between the unique index and the data [#51784](https://github.com/pingcap/tidb/issues/51784) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that automatic statistics collection gets stuck after an OOM error occurs [#51993](https://github.com/pingcap/tidb/issues/51993) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that TiDB might crash when `tidb_mem_quota_analyze` is enabled and the memory used by updating statistics exceeds the limit [#52601](https://github.com/pingcap/tidb/issues/52601) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `max_execute_time` settings at multiple levels interfere with each other [#50914](https://github.com/pingcap/tidb/issues/50914) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue of index inconsistency caused by adding multiple indexes using a single SQL statement [#51746](https://github.com/pingcap/tidb/issues/51746) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the Window function might panic when there is a related subquery in it [#42734](https://github.com/pingcap/tidb/issues/42734) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that TiDB crashes when `shuffleExec` quits unexpectedly [#48230](https://github.com/pingcap/tidb/issues/48230) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the status gets stuck when rolling back the partition DDL tasks [#51090](https://github.com/pingcap/tidb/issues/51090) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that querying JSON of `BINARY` type might cause an error in some cases [#51547](https://github.com/pingcap/tidb/issues/51547) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that adding indexes to large tables fails after enabling the Distributed eXecution Framework (DXF) [#52640](https://github.com/pingcap/tidb/issues/52640) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the TTL feature causes data hotspots due to incorrect data range splitting in some cases [#51527](https://github.com/pingcap/tidb/issues/51527) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that `ALTER TABLE ... COMPACT TIFLASH REPLICA` might incorrectly end when the primary key type is `VARCHAR` [#51810](https://github.com/pingcap/tidb/issues/51810) @[breezewish](https://github.com/breezewish)
    - Fix the issue of inconsistent data indexes caused by cluster upgrade during adding indexes [#52411](https://github.com/pingcap/tidb/issues/52411) @[tangenta](https://github.com/tangenta)
    - Fix the performance regression issue caused by disabling predicate pushdown in TableDual [#50614](https://github.com/pingcap/tidb/issues/50614) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that the TiDB server adds a label via the HTTP interface and returns success, but does not take effect [#51427](https://github.com/pingcap/tidb/issues/51427) @[you06](https://github.com/you06)
    - Fix the issue that adding indexes in the ingest mode might cause inconsistent data index in some corner cases [#51954](https://github.com/pingcap/tidb/issues/51954) @[lance6716](https://github.com/lance6716)
    - Fix the issue that the `init-stats` process might cause TiDB to panic and the `load stats` process to quit [#51581](https://github.com/pingcap/tidb/issues/51581) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the configuration file does not take effect when it contains an invalid configuration item [#51399](https://github.com/pingcap/tidb/issues/51399) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that query execution using MPP might lead to incorrect query results when a SQL statement contains `JOIN` and the `SELECT` list in the statement contains only constants [#50358](https://github.com/pingcap/tidb/issues/50358) @[yibin87](https://github.com/yibin87)
    - Fix the issue that in `determinate` mode (`tidb_opt_objective='determinate'`), if a query does not contain predicates, statistics might not be loaded [#48257](https://github.com/pingcap/tidb/issues/48257) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that the `SURVIVAL_PREFERENCES` attribute might not appear in the output of the `SHOW CREATE PLACEMENT POLICY` statement under certain conditions [#51699](https://github.com/pingcap/tidb/issues/51699) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that IndexJoin produces duplicate rows when calculating hash values in the Left Outer Anti Semi type [#52902](https://github.com/pingcap/tidb/issues/52902) @[yibin87](https://github.com/yibin87)
    - Fix the issue that the `TIMESTAMPADD()` function returns incorrect results [#41052](https://github.com/pingcap/tidb/issues/41052) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that data conversion from the `FLOAT` type to the `UNSIGNED` type returns incorrect results [#41736](https://github.com/pingcap/tidb/issues/41736) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the `TRUNCATE()` function returns incorrect results when its second argument is a large negative number [#52978](https://github.com/pingcap/tidb/issues/52978) @[yibin87](https://github.com/yibin87)
    - Fix the issue that duplicated panel IDs in Grafana might cause abnormal display [#51556](https://github.com/pingcap/tidb/issues/51556) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that TiDB unexpectedly restarts when logging gRPC errors [#51301](https://github.com/pingcap/tidb/issues/51301) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiDB loading statistics during startup might cause OOM [#52219](https://github.com/pingcap/tidb/issues/52219) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the TTL job for a table does not stop after the table is deleted [#51540](https://github.com/pingcap/tidb/issues/51540) @[YangKeao](https://github.com/YangKeao)

+ TiKV

    - Fix the issue that `thread_id` values are incorrectly displayed as `0x5` in TiKV logs [#16398](https://github.com/tikv/tikv/issues/16398) @[overvenus](https://github.com/overvenus)
    - Fix the issue of unstable test cases, ensuring that each test uses an independent temporary directory to avoid online configuration changes affecting other test cases [#16871](https://github.com/tikv/tikv/issues/16871) @[glorv](https://github.com/glorv)
    - Fix the issue that TiKV might panic during the conversion from Binary to JSON [#16616](https://github.com/tikv/tikv/issues/16616) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the output of the `raft region` command in tikv-ctl does not include the Region status information [#17037](https://github.com/tikv/tikv/issues/17037) @[glorv](https://github.com/glorv)
    - Fix the issue that slow `check-leader` operations on one TiKV node cause `resolved-ts` on other TiKV nodes to fail to advance normally [#15999](https://github.com/tikv/tikv/issues/15999) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that after the process of destroying Peer is interrupted by applying snapshots, it does not resume even after applying snapshots is complete [#16561](https://github.com/tikv/tikv/issues/16561) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Fix the issue that the decimal part of the `DECIMAL` type is incorrect in some cases [#16913](https://github.com/tikv/tikv/issues/16913) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that the `CONV()` function in queries might overflow during numeric system conversion, leading to TiKV panic [#16969](https://github.com/tikv/tikv/issues/16969) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - Fix the issue that the monitoring metric `tikv_unified_read_pool_thread_count` has no data in some cases [#16629](https://github.com/tikv/tikv/issues/16629) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that inactive Write Ahead Logs (WALs) in RocksDB might corrupt data [#16705](https://github.com/tikv/tikv/issues/16705) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that resolve-ts is blocked when a stale Region peer ignores the GC message [#16504](https://github.com/tikv/tikv/issues/16504) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that during the execution of an optimistic transaction, if other transactions initiate the resolving lock operation on it, there is a small chance that the atomicity of the transaction might be broken if the transaction's primary key has data that was previously committed in Async Commit or 1PC mode [#16620](https://github.com/tikv/tikv/issues/16620) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - Fix the issue of connection panic after fault recovery in the TiDB network partition [#7926](https://github.com/tikv/pd/issues/7926) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that scheduling might be incorrectly paused after online data recovery [#8095](https://github.com/tikv/pd/issues/8095) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that the CPS By Type monitoring types display incorrectly after enabling resource groups [#52605](https://github.com/pingcap/tidb/issues/52605) @[nolouch](https://github.com/nolouch)
    - Fix the issue that changing the log level via the configuration file does not take effect [#8117](https://github.com/tikv/pd/issues/8117) @[rleungx](https://github.com/rleungx)
    - Fix the issue that a large number of retries occur when canceling resource groups queries [#8217](https://github.com/tikv/pd/issues/8217) @[nolouch](https://github.com/nolouch)
    - Fix the issue that `ALTER PLACEMENT POLICY` cannot modify the placement policy [#52257](https://github.com/pingcap/tidb/issues/52257) [#51712](https://github.com/pingcap/tidb/issues/51712) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that down peers might not recover when using Placement Rules [#7808](https://github.com/tikv/pd/issues/7808) @[rleungx](https://github.com/rleungx)
    - Fix the issue that manually transferring the PD leader might fail [#8225](https://github.com/tikv/pd/issues/8225) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that the scheduling of write hotspots might break placement policy constraints [#7848](https://github.com/tikv/pd/issues/7848) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that slots are not fully deleted in a resource group client, which causes the number of the allocated tokens to be less than the specified value [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the scaling progress is not correctly displayed [#7726](https://github.com/tikv/pd/issues/7726) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that the Leader fails to transfer when you switch it between two deployed data centers [#7992](https://github.com/tikv/pd/issues/7992) @[TonsnakeLin](https://github.com/TonsnakeLin)
    - Fix the issue that the `Filter target` monitoring metric for PD does not provide scatter range information [#8125](https://github.com/tikv/pd/issues/8125) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that the query result of `SHOW CONFIG` includes the deprecated configuration item `trace-region-flow` [#7917](https://github.com/tikv/pd/issues/7917) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - Fix the issue that in the disaggregated storage and compute architecture, null values might be incorrectly returned in queries after adding non-null columns in DDL operations [#9084](https://github.com/pingcap/tiflash/issues/9084) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue of query timeout when executing queries on partitioned tables that contain empty partitions [#9024](https://github.com/pingcap/tiflash/issues/9024) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that in the disaggregated storage and compute architecture, TiFlash might panic when the compute node process is stopped [#8860](https://github.com/pingcap/tiflash/issues/8860) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that querying generated columns returns an error [#8787](https://github.com/pingcap/tiflash/issues/8787) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiFlash metadata might become corrupted and cause the process to panic when upgrading a cluster from a version earlier than v6.5.0 to v6.5.0 or later [#9039](https://github.com/pingcap/tiflash/issues/9039) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the `ENUM` column might cause TiFlash to crash during chunk encoding [#8674](https://github.com/pingcap/tiflash/issues/8674) @[yibin87](https://github.com/yibin87)
    - Fix incorrect `local_region_num` values in logs [#8895](https://github.com/pingcap/tiflash/issues/8895) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that in the disaggregated storage and compute architecture, TiFlash might panic during shutdown [#8837](https://github.com/pingcap/tiflash/issues/8837) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might return transiently incorrect results in high-concurrency read scenarios [#8845](https://github.com/pingcap/tiflash/issues/8845) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that in the disaggregated storage and compute architecture, the disk `used_size` metric displayed in Grafana is incorrect after you modify the value of the `storage.remote.cache.capacity` configuration item for TiFlash compute nodes [#8920](https://github.com/pingcap/tiflash/issues/8920) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that in the disaggregated storage and compute architecture, queries might be permanently blocked after network isolation [#8806](https://github.com/pingcap/tiflash/issues/8806) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that TiFlash might panic when you insert data to columns with invalid default values in non-strict `sql_mode` [#8803](https://github.com/pingcap/tiflash/issues/8803) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ Tools

    + Backup & Restore (BR)

        - Fix a rare issue that special event timing might cause the data loss in log backup [#16739](https://github.com/tikv/tikv/issues/16739) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that too many logs are printed when a full backup fails [#51572](https://github.com/pingcap/tidb/issues/51572) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that a PD connection failure could cause the TiDB instance where the log backup advancer owner is located to panic [#52597](https://github.com/pingcap/tidb/issues/52597) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the global checkpoint of log backup is advanced ahead of the actual backup file write point due to TiKV restart, which might cause a small amount of backup data loss [#16809](https://github.com/tikv/tikv/issues/16809) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that TiKV might panic when resuming a paused log backup task with unstable network connections to PD [#17020](https://github.com/tikv/tikv/issues/17020) @[YuJuncen](https://github.com/YuJuncen)
        - Fix an unstable test case [#52547](https://github.com/pingcap/tidb/issues/52547) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the Region fetched from PD does not have a Leader when restoring data using BR or importing data using TiDB Lightning in physical import mode [#51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that TiKV panics when a full backup fails to find a peer in some extreme cases [#16394](https://github.com/tikv/tikv/issues/16394) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that removing a log backup task after it is paused does not immediately restore the GC safepoint [#52082](https://github.com/pingcap/tidb/issues/52082) @[3pointer](https://github.com/3pointer)
        - Fix the unstable test case `TestClearCache` [#50743](https://github.com/pingcap/tidb/issues/50743) @[3pointer](https://github.com/3pointer)
        - Fix the issue that BR fails to restore a transactional KV cluster due to an empty `EndKey` [#52574](https://github.com/pingcap/tidb/issues/52574) @[3pointer](https://github.com/3pointer)
        - Fix the issue that the transfer of PD leaders might cause BR to panic when restoring data [#53724](https://github.com/pingcap/tidb/issues/53724) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that BR could not back up the `AUTO_RANDOM` ID allocation progress in a union clustered index that contains an `AUTO_RANDOM` column [#52255](https://github.com/pingcap/tidb/issues/52255) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - Fix the issue that high latency in the PD disk I/O causes severe latency in data replication [#9054](https://github.com/pingcap/tiflow/issues/9054) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that calling the API (`/api/v2/owner/resign`) that evicts the TiCDC owner node causes the TiCDC task to restart unexpectedly [#10781](https://github.com/pingcap/tiflow/issues/10781) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that data is written to a wrong CSV file due to wrong BarrierTS in scenarios where DDL statements are executed frequently [#10668](https://github.com/pingcap/tiflow/issues/10668) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that TiCDC fails to validate `TIMESTAMP` type checksum due to time zone mismatch after data integrity validation for single-row data is enabled [#10573](https://github.com/pingcap/tiflow/issues/10573) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that a changefeed with eventual consistency enabled might fail when the object storage sink encounters a temporary failure [#10710](https://github.com/pingcap/tiflow/issues/10710) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that `DROP PRIMARY KEY` and `DROP UNIQUE KEY` statements are not replicated correctly [#10890](https://github.com/pingcap/tiflow/issues/10890) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue TiCDC panics when scheduling table replication tasks [#10613](https://github.com/pingcap/tiflow/issues/10613) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that when the downstream Pulsar is stopped, removing the changefeed causes the normal TiCDC process to get stuck, which causes other changefeed processes to get stuck [#10629](https://github.com/pingcap/tiflow/issues/10629) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that restarting PD might cause the TiCDC node to restart with an error [#10799](https://github.com/pingcap/tiflow/issues/10799) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the old value part of `open-protocol` incorrectly outputs the default value according to the `STRING` type instead of its actual type [#10803](https://github.com/pingcap/tiflow/issues/10803) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the default value of `TIMEZONE` type is not set according to the correct time zone [#10931](https://github.com/pingcap/tiflow/issues/10931) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that TiCDC fails to execute the `Exchange Partition ... With Validation` DDL downstream after it is written upstream, causing the changefeed to get stuck [#10859](https://github.com/pingcap/tiflow/issues/10859) @[hongyunyan](https://github.com/hongyunyan)
        - Fix the issue that data race in the KV client causes TiCDC to panic [#10718](https://github.com/pingcap/tiflow/issues/10718) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that updating the primary key or the unique key in upstream might cause data inconsistency between upstream and downstream [#10918](https://github.com/pingcap/tiflow/issues/10918) @[lidezhu](https://github.com/lidezhu)

    + TiDB Data Migration (DM)

        - Fix the connection blocking issue by upgrading `go-mysql` [#11041](https://github.com/pingcap/tiflow/issues/11041) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that data is lost when the upstream primary key is of binary type [#10672](https://github.com/pingcap/tiflow/issues/10672) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning might fail to import data when EBS BR is running [#49517](https://github.com/pingcap/tidb/issues/49517) @[mittalrishabh](https://github.com/mittalrishabh)
        - Fix the issue that TiDB Lightning reports `no database selected` during data import due to incompatible SQL statements in the source files [#51800](https://github.com/pingcap/tidb/issues/51800) @[lance6716](https://github.com/lance6716)
        - Fix the issue that killing the PD Leader causes TiDB Lightning to report the `invalid store ID 0` error during data import [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that TiDB Lightning panics when importing an empty table of Parquet format [#52518](https://github.com/pingcap/tidb/issues/52518) @[kennytm](https://github.com/kennytm)
