---
title: TiDB 7.1.6 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.1.6.
---

# TiDB 7.1.6 Release Notes

Release date: November 21, 2024

TiDB version: 7.1.6

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## Compatibility changes

- Set a default limit of 2048 for DDL historical tasks retrieved through the [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-7.1/docs/tidb_http_api.md) to prevent OOM issues caused by excessive historical tasks [#55711](https://github.com/pingcap/tidb/issues/55711) @[joccau](https://github.com/joccau)
- In earlier versions, when processing a transaction containing `UPDATE` changes, if the primary key or non-null unique index value is modified in an `UPDATE` event, TiCDC splits this event into `DELETE` and `INSERT` events. Starting from v7.1.6, when using the MySQL sink, TiCDC splits an `UPDATE` event into `DELETE` and `INSERT` events if the transaction `commitTS` for the `UPDATE` change is less than TiCDC `thresholdTS` (which is the current timestamp fetched from PD when TiCDC starts replicating the corresponding table to the downstream). This behavior change addresses the issue of downstream data inconsistencies caused by the potentially incorrect order of `UPDATE` events received by TiCDC, which can lead to an incorrect order of split `DELETE` and `INSERT` events. For more information, see [documentation](https://docs.pingcap.com/tidb/v7.1/ticdc-split-update-behavior#split-update-events-for-mysql-sinks). [#10918](https://github.com/pingcap/tiflow/issues/10918) @[lidezhu](https://github.com/lidezhu)
- Must set the line terminator when using TiDB Lightning `strict-format` to import CSV files [#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)

## Improvements

+ TiDB

    - Adjust estimation results from 0 to 1 for equality conditions that do not hit TopN when statistics are entirely composed of TopN and the modified row count in the corresponding table statistics is non-zero [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - Remove stores without Regions during MPP load balancing [#52313](https://github.com/pingcap/tidb/issues/52313) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Improve the MySQL compatibility of expression default values displayed in the output of `SHOW CREATE TABLE` [#52939](https://github.com/pingcap/tidb/issues/52939) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - By batch deleting TiFlash placement rules, improve the processing speed of data GC after performing the `TRUNCATE` or `DROP` operation on partitioned tables [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Improve sync load performance to reduce latency in loading statistics [#52294](https://github.com/pingcap/tidb/issues/52294) [hawkingrei](https://github.com/hawkingrei)

+ TiKV

    - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)
    - Optimize the compaction trigger mechanism of RocksDB to accelerate disk space reclamation when handling a large number of DELETE versions [#17269](https://github.com/tikv/tikv/issues/17269) @[AndreMouche](https://github.com/AndreMouche)
    - Optimize the jittery access delay when restarting TiKV due to waiting for the log to be applied, improving the stability of TiKV [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)
    - Remove unnecessary async blocks to reduce memory usage [#16540](https://github.com/tikv/tikv/issues/16540) @[overvenus](https://github.com/overvenus)

+ TiFlash

    - Optimize the execution efficiency of `LENGTH()` and `ASCII()` functions [#9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Mitigate the issue that TiFlash might panic due to updating certificates after TLS is enabled [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - Improve the cancel mechanism of the JOIN operator, so that the JOIN operator can respond to cancel requests in a timely manner [#9430](https://github.com/pingcap/tiflash/issues/9430) @[windtalker](https://github.com/windtalker)
    - Reduce lock conflicts under highly concurrent data read operations and optimize short query performance [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)
    - Improve the garbage collection speed of outdated data in the background for tables with clustered indexes [#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Enhance the tolerance of log backup to merge operations. When encountering a reasonably long merge operation, log backup tasks are less likely to enter the error state [#16554](https://github.com/tikv/tikv/issues/16554) @[YuJuncen](https://github.com/YuJuncen)
        - BR cleans up empty SST files during data recovery [#16005](https://github.com/tikv/tikv/issues/16005) @[Leavrth](https://github.com/Leavrth)
        - Increase the number of retries for failures caused by DNS errors [#53029](https://github.com/pingcap/tidb/issues/53029) @[YuJuncen](https://github.com/YuJuncen)
        - Increase the number of retries for failures caused by the absence of a leader in a Region [#54017](https://github.com/pingcap/tidb/issues/54017) @[Leavrth](https://github.com/Leavrth)
        - Except for the `br log restore` subcommand, all other `br log` subcommands support skipping the loading of the TiDB `domain` data structure to reduce memory consumption [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        - Support checking whether the disk space in TiKV is sufficient before TiKV downloads each SST file. If the space is insufficient, BR terminates the restore and returns an error [#17224](https://github.com/tikv/tikv/issues/17224) @[RidRisR](https://github.com/RidRisR)
        - Support setting Alibaba Cloud access credentials through environment variables [#45551](https://github.com/pingcap/tidb/issues/45551) @[RidRisR](https://github.com/RidRisR)
        - Reduce unnecessary log printing during backup [#55902](https://github.com/pingcap/tidb/issues/55902) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - Support directly outputting raw events when the downstream is a Message Queue (MQ) or cloud storage [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Improve memory stability during data recovery using redo logs to reduce the probability of OOM [#10900](https://github.com/pingcap/tiflow/issues/10900) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - When the downstream is TiDB with the `SUPER` permission granted, TiCDC supports querying the execution status of `ADD INDEX DDL` from the downstream database to avoid data replication failure due to timeout in retrying executing the DDL statement in some cases [#10682](https://github.com/pingcap/tiflow/issues/10682) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - Upgrade `go-mysql` to 1.9.1 to support connecting to MySQL server 8.0 using passwords longer than 19 characters [#11603](https://github.com/pingcap/tiflow/pull/11603) @[fishiu](https://github.com/fishiu)

## Bug fixes

+ TiDB

    - Fix the issue of inconsistent data indexes caused by concurrent DML operations when adding a unique index [#52914](https://github.com/pingcap/tidb/issues/52914) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that comparing a column of `YEAR` type with an unsigned integer that is out of range causes incorrect results [#50235](https://github.com/pingcap/tidb/issues/50235) @[qw4990](https://github.com/qw4990)
    - Fix the issue that `INDEX_HASH_JOIN` cannot exit properly when SQL is abnormally interrupted [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the network partition during adding indexes using the Distributed eXecution Framework (DXF) might cause inconsistent data indexes [#54897](https://github.com/pingcap/tidb/issues/54897) @[tangenta](https://github.com/tangenta)
    - Fix the issue that using `SHOW WARNINGS;` to obtain warnings might cause a panic [#48756](https://github.com/pingcap/tidb/issues/48756) @[xhebox](https://github.com/xhebox)
    - Fix the issue that querying the `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` table might cause TiDB to panic [#54324](https://github.com/pingcap/tidb/issues/54324) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue of abnormally high memory usage caused by `memTracker` not being detached when the `HashJoin` or `IndexLookUp` operator is the driven side sub-node of the `Apply` operator [#54005](https://github.com/pingcap/tidb/issues/54005) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that recursive CTE queries might result in invalid pointers [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that an empty projection causes TiDB to panic [#49109](https://github.com/pingcap/tidb/issues/49109) @[winoros](https://github.com/winoros)
    - Fix the issue that TiDB might return incorrect query results when you query tables with virtual columns in transactions that involve data modification operations [#53951](https://github.com/pingcap/tidb/issues/53951) @[qw4990](https://github.com/qw4990)
    - Fix the issue that for tables containing auto-increment columns with `AUTO_ID_CACHE=1`, setting `auto_increment_increment` and `auto_increment_offset` system variables to non-default values might cause incorrect auto-increment ID allocation [#52622](https://github.com/pingcap/tidb/issues/52622) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that subqueries included in the `ALL` function might cause incorrect results [#52755](https://github.com/pingcap/tidb/issues/52755) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that predicates cannot be pushed down properly when the filter condition of a SQL query contains virtual columns and the execution condition contains `UnionScan` [#54870](https://github.com/pingcap/tidb/issues/54870) @[qw4990](https://github.com/qw4990)
    - Fix the issue that subqueries in an `UPDATE` list might cause TiDB to panic [#52687](https://github.com/pingcap/tidb/issues/52687) @[winoros](https://github.com/winoros)
    - Fix the issue that indirect placeholder `?` references in a `GROUP BY` statement cannot find columns [#53872](https://github.com/pingcap/tidb/issues/53872) @[qw4990](https://github.com/qw4990)
    - Fix the issue that disk files might not be deleted after the `Sort` operator spills and a query error occurs [#55061](https://github.com/pingcap/tidb/issues/55061) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue of reusing wrong point get plans for `SELECT ... FOR UPDATE` [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)
    - Fix the issue that `max_execute_time` settings at multiple levels interfere with each other [#50914](https://github.com/pingcap/tidb/issues/50914) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that the histogram and TopN in the primary key column statistics are not loaded after restarting TiDB [#37548](https://github.com/pingcap/tidb/issues/37548) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the TopN operator might be pushed down incorrectly [#37986](https://github.com/pingcap/tidb/issues/37986) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the performance of the `SELECT ... WHERE ... ORDER BY ...` statement execution is poor in some cases [#54969](https://github.com/pingcap/tidb/issues/54969) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB reports an error in the log when closing the connection in some cases [#53689](https://github.com/pingcap/tidb/issues/53689) @[jackysp](https://github.com/jackysp)
    - Fix the issue that the illegal column type `DECIMAL(0,0)` can be created in some cases [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - Fix the issue that obtaining the column information using `information_schema.columns` returns warning 1356 when a subquery is used as a column definition in a view definition [#54343](https://github.com/pingcap/tidb/issues/54343) @[lance6716](https://github.com/lance6716)
    - Fix the issue that the optimizer incorrectly estimates the number of rows as 1 when accessing a unique index with the query condition `column IS NULL` [#56116](https://github.com/pingcap/tidb/issues/56116) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `SELECT INTO OUTFILE` does not work when clustered indexes are used as predicates [#42093](https://github.com/pingcap/tidb/issues/42093) @[qw4990](https://github.com/qw4990)
    - Fix the issue of incorrect WARNINGS information when using Optimizer Hints [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the Sync Load QPS monitoring metric is incorrect [#53558](https://github.com/pingcap/tidb/issues/53558) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that executing `CREATE OR REPLACE VIEW` concurrently might result in the `table doesn't exist` error [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    - Fix the issue that restoring a table with `AUTO_ID_CACHE=1` using the `RESTORE` statement might cause a `Duplicate entry` error [#52680](https://github.com/pingcap/tidb/issues/52680) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `SUB_PART` value in the `INFORMATION_SCHEMA.STATISTICS` table is `NULL` [#55812](https://github.com/pingcap/tidb/issues/55812) @[Defined2014](https://github.com/Defined2014)
    - Fix the overflow issue of the `Longlong` type in predicates [#45783](https://github.com/pingcap/tidb/issues/45783) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that incorrect results are returned when the cached execution plans contain the comparison between date types and `unix_timestamp` [#48165](https://github.com/pingcap/tidb/issues/48165) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the `LENGTH()` condition is unexpectedly removed when the collation is `utf8_bin` or `utf8mb4_bin` [#53730](https://github.com/pingcap/tidb/issues/53730) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that when an `UPDATE` or `DELETE` statement contains a recursive CTE, the statement might report an error or not take effect [#55666](https://github.com/pingcap/tidb/issues/55666) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that TiDB might hang or return incorrect results when executing a query containing a correlated subquery and CTE [#55551](https://github.com/pingcap/tidb/issues/55551) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that statistics for string columns with non-binary collations might fail to load when initializing statistics [#55684](https://github.com/pingcap/tidb/issues/55684) @[winoros](https://github.com/winoros)
    - Fix the issue that IndexJoin produces duplicate rows when calculating hash values in the Left Outer Anti Semi type [#52902](https://github.com/pingcap/tidb/issues/52902) @[yibin87](https://github.com/yibin87)
    - Fix the issue that a query statement that contains `UNION` might return incorrect results [#52985](https://github.com/pingcap/tidb/issues/52985) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that empty `groupOffset` in `StreamAggExec` might cause TiDB to panic [#53867](https://github.com/pingcap/tidb/issues/53867) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that RANGE partitioned tables that are not strictly self-incrementing can be created [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the query might get stuck when terminated because the memory usage exceeds the limit set by `tidb_mem_quota_query` [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    - Fix the issue that the `STATE` field in the `INFORMATION_SCHEMA.TIDB_TRX` table is empty due to the `size` of the `STATE` field not being defined [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the data race issue in `IndexNestedLoopHashJoin` [#49692](https://github.com/pingcap/tidb/issues/49692) @[solotzg](https://github.com/solotzg)
    - Fix the issue that a wrong TableDual plan causes empty query results [#50051](https://github.com/pingcap/tidb/issues/50051) @[onlyacat](https://github.com/onlyacat)
    - Fix the issue that the `tot_col_size` column in the `mysql.stats_histograms` table might be a negative number [#55126](https://github.com/pingcap/tidb/issues/55126) @[qw4990](https://github.com/qw4990)
    - Fix the issue that data conversion from the `FLOAT` type to the `UNSIGNED` type returns incorrect results [#41736](https://github.com/pingcap/tidb/issues/41736) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiDB fails to reject unauthenticated user connections in some cases when using the `auth_socket` authentication plugin [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the `memory_quota` hint might not work in subqueries [#53834](https://github.com/pingcap/tidb/issues/53834) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the metadata lock fails to prevent DDL operations from executing in the plan cache scenario [#51407](https://github.com/pingcap/tidb/issues/51407) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that using `CURRENT_DATE()` as the default value for a column results in incorrect query results [#53746](https://github.com/pingcap/tidb/issues/53746) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the `COALESCE()` function returns incorrect result type for `DATE` type parameters [#46475](https://github.com/pingcap/tidb/issues/46475) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Reset the parameters in the `Open` method of `PipelinedWindow` to fix the unexpected error that occurs when the `PipelinedWindow` is used as a child node of `Apply` due to the reuse of previous parameter values caused by repeated opening and closing operations [#53600](https://github.com/pingcap/tidb/issues/53600) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the incorrect result of the TopN operator in correlated subqueries [#52777](https://github.com/pingcap/tidb/issues/52777) @[yibin87](https://github.com/yibin87)
    - Fix the issue that the recursive CTE operator incorrectly tracks memory usage [#54181](https://github.com/pingcap/tidb/issues/54181) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that an error occurs when using `SHOW COLUMNS` to view columns in a view [#54964](https://github.com/pingcap/tidb/issues/54964) @[lance6716](https://github.com/lance6716)
    - Fix the issue that reducing the value of `tidb_ttl_delete_worker_count` during TTL job execution makes the job fail to complete [#55561](https://github.com/pingcap/tidb/issues/55561) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that using a view does not work in recursive CTE [#49721](https://github.com/pingcap/tidb/issues/49721) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that TiDB does not create corresponding statistics metadata (`stats_meta`) when creating a table with foreign keys [#53652](https://github.com/pingcap/tidb/issues/53652) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the query might return incorrect results instead of an error after being killed [#50089](https://github.com/pingcap/tidb/issues/50089) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that the statistics synchronous loading mechanism might fail unexpectedly under high query concurrency [#52294](https://github.com/pingcap/tidb/issues/52294) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that certain filter conditions in queries might cause the planner module to report an `invalid memory address or nil pointer dereference` error [#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the TiDB synchronously loading statistics mechanism retries to load empty statistics indefinitely and prints the `fail to get stats version for this histogram` log [#52657](https://github.com/pingcap/tidb/issues/52657) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `TIMESTAMPADD()` function goes into an infinite loop when the first argument is `month` and the second argument is negative [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that TiDB might crash when `tidb_mem_quota_analyze` is enabled and the memory used by updating statistics exceeds the limit [#52601](https://github.com/pingcap/tidb/issues/52601) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `duplicate entry` might occur when adding unique indexes [#56161](https://github.com/pingcap/tidb/issues/56161) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the query latency of stale reads increases, caused by information schema cache misses [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that the `Distinct_count` information in GlobalStats might be incorrect [#53752](https://github.com/pingcap/tidb/issues/53752) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that executing the `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` query might return incorrect results [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `read_from_storage` hint might not take effect when the query has an available Index Merge execution plan [#56217](https://github.com/pingcap/tidb/issues/56217) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the `TIMESTAMPADD()` function returns incorrect results [#41052](https://github.com/pingcap/tidb/issues/41052) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that `PREPARE`/`EXECUTE` statements with the `CONV` expression containing a `?` argument might result in incorrect query results when executed multiple times [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the memory used by transactions might be tracked multiple times [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - Fix the issue that column pruning without using shallow copies of slices might cause TiDB to panic [#52768](https://github.com/pingcap/tidb/issues/52768) @[winoros](https://github.com/winoros)
    - Fix the issue that a SQL binding containing window functions might not take effect in some cases [#55981](https://github.com/pingcap/tidb/issues/55981) @[winoros](https://github.com/winoros)
    - Fix the issue that TiDB might panic when parsing index data [#47115](https://github.com/pingcap/tidb/issues/47115) @[zyguan](https://github.com/zyguan)
    - Fix the issue that TiDB might report an error due to GC when loading statistics at startup [#53592](https://github.com/pingcap/tidb/issues/53592) @[you06](https://github.com/you06)
    - Fix the issue that an error occurs when a DML statement contains nested generated columns [#53967](https://github.com/pingcap/tidb/issues/53967) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that TiDB panics when executing the `SHOW ERRORS` statement with a predicate that is always `true` [#46962](https://github.com/pingcap/tidb/issues/46962) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that improper use of metadata locks might lead to writing anomalous data when using the plan cache under certain circumstances [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - Fix the issue of data index inconsistency caused by retries during index addition [#55808](https://github.com/pingcap/tidb/issues/55808) @[lance6716](https://github.com/lance6716)
    - Fix the issue that unstable unique IDs of columns might cause the `UPDATE` statement to return errors [#53236](https://github.com/pingcap/tidb/issues/53236) @[winoros](https://github.com/winoros)
    - Fix the issue that after a statement within a transaction is killed by OOM, if TiDB continues to execute the next statement within the same transaction, you might get an error `Trying to start aggressive locking while it's already started` and a panic occurs [#53540](https://github.com/pingcap/tidb/issues/53540) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that executing `RECOVER TABLE BY JOB JOB_ID;` might cause TiDB to panic [#55113](https://github.com/pingcap/tidb/issues/55113) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that executing `ADD INDEX` might fail after modifying the PD member in the distributed execution framework [#48680](https://github.com/pingcap/tidb/issues/48680) @[lance6716](https://github.com/lance6716)
    - Fix the issue that two DDL Owners might exist at the same time [#54689](https://github.com/pingcap/tidb/issues/54689) @[joccau](https://github.com/joccau)
    - Fix the issue that TiDB rolling restart during the execution of `ADD INDEX` might cause the adding index operation to fail [#52805](https://github.com/pingcap/tidb/issues/52805) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the `LOAD DATA ... REPLACE INTO` operation causes data inconsistency [#56408](https://github.com/pingcap/tidb/issues/56408) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that the `AUTO_INCREMENT` field is not correctly set after importing data using the `IMPORT INTO` statement [#56476](https://github.com/pingcap/tidb/issues/56476) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that TiDB does not check for the existence of local files before restoring from a checkpoint [#53009](https://github.com/pingcap/tidb/issues/53009) @[lance6716](https://github.com/lance6716)
    - Fix the issue that the DM schema tracker cannot create indexes longer than the default length [#55138](https://github.com/pingcap/tidb/issues/55138) @[lance6716](https://github.com/lance6716)
    - Fix the issue that `ALTER TABLE` does not handle the `AUTO_INCREMENT` field correctly [#47899](https://github.com/pingcap/tidb/issues/47899) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that unreleased session resources might lead to memory leaks [#56271](https://github.com/pingcap/tidb/issues/56271) @[lance6716](https://github.com/lance6716)
    - Fix the issue that float or integer overflow affects the plan cache [#46538](https://github.com/pingcap/tidb/issues/46538) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that part of the memory of the `IndexLookUp` operator is not tracked [#56440](https://github.com/pingcap/tidb/issues/56440) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that stale read does not strictly verify the timestamp of the read operation, resulting in a small probability of affecting the consistency of the transaction when an offset exists between the TSO and the real physical time [#56809](https://github.com/pingcap/tidb/issues/56809) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that TTL might fail if TiKV is not selected as the storage engine [#56402](https://github.com/pingcap/tidb/issues/56402) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that TTL tasks cannot be canceled when there is a write conflict [#56422](https://github.com/pingcap/tidb/issues/56422) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that inserting oversized numbers in scientific notation causes an error `ERROR 1264 (22003)`, to make the behavior consistent with MySQL [#47787](https://github.com/pingcap/tidb/issues/47787) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that when canceling a TTL task, the corresponding SQL is not killed forcibly [#56511](https://github.com/pingcap/tidb/issues/56511) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the `INSERT ... ON DUPLICATE KEY` statement is not compatible with `mysql_insert_id` [#55965](https://github.com/pingcap/tidb/issues/55965) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that audit log filtering does not take effect when SQL cannot build an execution plan [#50988](https://github.com/pingcap/tidb/issues/50988) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that existing TTL tasks are executed unexpectedly frequently in a cluster that is upgraded from v6.5 to v7.5 or later [#56539](https://github.com/pingcap/tidb/issues/56539) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the `CAST` function does not support explicitly setting the character set [#55677](https://github.com/pingcap/tidb/issues/55677) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that TiDB does not check the index length limitation when executing `ADD INDEX` [#56930](https://github.com/pingcap/tidb/issues/56930) @[fzzf678](https://github.com/fzzf678)

+ TiKV

    - Add the `RawKvMaxTimestampNotSynced` error, log detailed error information in `errorpb.Error.max_ts_not_synced`, and add a retry mechanism for the `must_raw_put` operation when this error occurs [#16789](https://github.com/tikv/tikv/issues/16789) @[pingyu](https://github.com/pingyu)
    - Fix a traffic control issue that might occur after deleting large tables or partitions [#17304](https://github.com/tikv/tikv/issues/17304) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix the panic issue that occurs when read threads access outdated indexes in the MemTable of the Raft Engine [#17383](https://github.com/tikv/tikv/issues/17383) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that CDC and log-backup do not limit the timeout of `check_leader` using the `advance-ts-interval` configuration, causing the `resolved_ts` lag to be too large when TiKV restarts normally in some cases [#17107](https://github.com/tikv/tikv/issues/17107) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix the issue that SST files imported by TiDB Lightning are lost after TiKV is restarted [#15912](https://github.com/tikv/tikv/issues/15912) @[lance6716](https://github.com/lance6716)
    - Fix the issue that TiKV might panic due to ingesting deleted `sst_importer` SST files [#15053](https://github.com/tikv/tikv/issues/15053) @[lance6716](https://github.com/lance6716)
    - Fix the issue that when there are a large number of Regions in a TiKV instance, TiKV might be OOM during data import [#16229](https://github.com/tikv/tikv/issues/16229) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix the issue that bloom filters are incompatible between earlier versions (earlier than v7.1) and later versions [#17272](https://github.com/tikv/tikv/issues/17272) @[v01dstar](https://github.com/v01dstar)
    - Fix the issue that setting the gRPC message compression method via `grpc-compression-type` does not take effect on messages sent from TiKV to TiDB [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - Fix the issue of unstable test cases, ensuring that each test uses an independent temporary directory to avoid online configuration changes affecting other test cases [#16871](https://github.com/tikv/tikv/issues/16871) @[glorv](https://github.com/glorv)
    - Fix the issue that when a large number of transactions are queuing for lock release on the same key and the key is frequently updated, excessive pressure on deadlock detection might cause TiKV OOM issues [#17394](https://github.com/tikv/tikv/issues/17394) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that the decimal part of the `DECIMAL` type is incorrect in some cases [#16913](https://github.com/tikv/tikv/issues/16913) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that the `CONV()` function in queries might overflow during numeric system conversion, leading to TiKV panic [#16969](https://github.com/tikv/tikv/issues/16969) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that TiKV might panic when a stale replica processes Raft snapshots, triggered by a slow split operation and immediate removal of the new replica [#17469](https://github.com/tikv/tikv/issues/17469) @[hbisheng](https://github.com/hbisheng)
    - Fix the issue that highly concurrent Coprocessor requests might cause TiKV OOM [#16653](https://github.com/tikv/tikv/issues/16653) @[overvenus](https://github.com/overvenus)
    - Fix the issue that prevents master key rotation when the master key is stored in a Key Management Service (KMS) [#17410](https://github.com/tikv/tikv/issues/17410) @[hhwyt](https://github.com/hhwyt)
    - Fix the issue that the output of the `raft region` command in tikv-ctl does not include the Region status information [#17037](https://github.com/tikv/tikv/issues/17037) @[glorv](https://github.com/glorv)
    - Fix the issue that the **Storage async write duration** monitoring metric on the TiKV panel in Grafana is inaccurate [#17579](https://github.com/tikv/tikv/issues/17579) @[overvenus](https://github.com/overvenus)
    - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)

+ PD

    - Fix the memory leak issue in label statistics [#8700](https://github.com/tikv/pd/issues/8700) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that resource groups print excessive logs [#8159](https://github.com/tikv/pd/issues/8159) @[nolouch](https://github.com/nolouch)
    - Fix the performance jitter issue caused by frequent creation of random number generator [#8674](https://github.com/tikv/pd/issues/8674) @[rleungx](https://github.com/rleungx)
    - Fix the memory leak issue in Region statistics [#8710](https://github.com/tikv/pd/issues/8710) @[rleungx](https://github.com/rleungx)
    - Fix the memory leak issue in hotspot cache [#8698](https://github.com/tikv/pd/issues/8698) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that `evict-leader-scheduler` fails to work properly when it is repeatedly created with the same Store ID [#8756](https://github.com/tikv/pd/issues/8756) @[okJiang](https://github.com/okJiang)
    - Fix the issue that setting `replication.strictly-match-label` to `true` causes TiFlash to fail to start [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)
    - Fix the issue that changing the log level via the configuration file does not take effect [#8117](https://github.com/tikv/pd/issues/8117) @[rleungx](https://github.com/rleungx)
    - Fix the issue that resource groups could not effectively limit resource usage under high concurrency [#8435](https://github.com/tikv/pd/issues/8435) @[nolouch](https://github.com/nolouch)
    - Fix the data race issue that PD encounters during operator checks [#8263](https://github.com/tikv/pd/issues/8263) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that a resource group encounters quota limits when requesting tokens for more than 500 ms [#8349](https://github.com/tikv/pd/issues/8349) @[nolouch](https://github.com/nolouch)
    - Fix the issue that some logs are not redacted [#8419](https://github.com/tikv/pd/issues/8419) @[rleungx](https://github.com/rleungx)
    - Fix the issue that no error is reported when binding a role to a resource group [#54417](https://github.com/pingcap/tidb/issues/54417) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that PD's Region API cannot be requested when a large number of Regions exist [#55872](https://github.com/pingcap/tidb/issues/55872) @[rleungx](https://github.com/rleungx)
    - Fix the issue that a large number of retries occur when canceling resource groups queries [#8217](https://github.com/tikv/pd/issues/8217) @[nolouch](https://github.com/nolouch)
    - Fix the issue that the encryption manager is not initialized before use [#8384](https://github.com/tikv/pd/issues/8384) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the `Filter target` monitoring metric for PD does not provide scatter range information [#8125](https://github.com/tikv/pd/issues/8125) @[HuSharp](https://github.com/HuSharp)
    - Fix the data race issue of resource groups [#8267](https://github.com/tikv/pd/issues/8267) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that setting the TiKV configuration item [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) to a value less than 1 MiB causes PD panic [#8323](https://github.com/tikv/pd/issues/8323) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that when using a wrong parameter in `evict-leader-scheduler`, PD does not report errors correctly and some schedulers are unavailable [#8619](https://github.com/tikv/pd/issues/8619) @[rleungx](https://github.com/rleungx)
    - Fix the issue that slots are not fully deleted in a resource group client, which causes the number of the allocated tokens to be less than the specified value [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that down peers might not recover when using Placement Rules [#7808](https://github.com/tikv/pd/issues/7808) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - Fix the issue that TiFlash metadata might become corrupted and cause the process to panic when upgrading a cluster from a version earlier than v6.5.0 to v6.5.0 or later [#9039](https://github.com/pingcap/tiflash/issues/9039) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that some queries might report a column type mismatch error after late materialization is enabled [#9175](https://github.com/pingcap/tiflash/issues/9175) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that some queries might report errors when late materialization is enabled [#9472](https://github.com/pingcap/tiflash/issues/9472) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that some JSON functions unsupported by TiFlash are pushed down to TiFlash [#9444](https://github.com/pingcap/tiflash/issues/9444) @[windtalker](https://github.com/windtalker)
    - Fix the issue that setting the SSL certificate configuration to an empty string in TiFlash incorrectly enables TLS and causes TiFlash to fail to start [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that a network partition (network disconnection) between TiFlash and any PD might cause read request timeout errors [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that a large number of duplicate rows might be read in FastScan mode after importing data via BR or TiDB Lightning [#9118](https://github.com/pingcap/tiflash/issues/9118) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that TiFlash fails to parse the table schema when the table contains Bit-type columns with a default value that contains invalid characters [#9461](https://github.com/pingcap/tiflash/issues/9461) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that queries with virtual generated columns might return incorrect results after late materialization is enabled [#9188](https://github.com/pingcap/tiflash/issues/9188) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that TiFlash might fail to synchronize schemas after executing `ALTER TABLE ... EXCHANGE PARTITION` across databases [#7296](https://github.com/pingcap/tiflash/issues/7296) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might panic when a database is deleted shortly after creation [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that when using the `CAST()` function to convert a string to a datetime with a time zone or invalid characters, the result is incorrect [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    - Fix the issue that TiFlash might return transiently incorrect results in high-concurrency read scenarios [#8845](https://github.com/pingcap/tiflash/issues/8845) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that the `SUBSTRING_INDEX()` function might cause TiFlash to crash in some corner cases [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that frequent `EXCHANGE PARTITION` and `DROP TABLE` operations over a long period in a cluster might slow down the replication of TiFlash table metadata and degrade the query performance [#9227](https://github.com/pingcap/tiflash/issues/9227) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that a query with an empty key range fails to correctly generate read tasks on TiFlash, which might block TiFlash queries [#9108](https://github.com/pingcap/tiflash/issues/9108) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that the sign in the result of the `CAST AS DECIMAL` function is incorrect in certain cases [#9301](https://github.com/pingcap/tiflash/issues/9301) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the `SUBSTRING()` function does not support the `pos` and `len` arguments for certain integer types, causing query errors [#9473](https://github.com/pingcap/tiflash/issues/9473) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that executing `DROP TABLE` on large tables might cause TiFlash OOM [#9437](https://github.com/pingcap/tiflash/issues/9437) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that BR integration test cases are unstable, and add a new test case to simulate snapshot or log backup file corruption [#53835](https://github.com/pingcap/tidb/issues/53835) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that DDLs requiring backfilling, such as `ADD INDEX` and `MODIFY COLUMN`, might not be correctly recovered during incremental restore [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)
        - Fix the issue that after a log backup PITR task fails and you stop it, the safepoints related to that task are not properly cleared in PD [#17316](https://github.com/tikv/tikv/issues/17316) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that log backup might be paused after the advancer owner migration [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)
        - Fix the inefficiency issue in scanning DDL jobs during incremental backups [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        - Fix the issue that the backup performance during checkpoint backups is affected due to interruptions in seeking Region leaders [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that BR logs might print sensitive credential information when log backup is enabled [#55273](https://github.com/pingcap/tidb/issues/55273) @[RidRisR](https://github.com/RidRisR)
        - Fix the issue that BR fails to correctly identify errors due to multiple nested retries during the restore process [#54053](https://github.com/pingcap/tidb/issues/54053) @[RidRisR](https://github.com/RidRisR)
        - Fix the issue that TiKV might panic when resuming a paused log backup task with unstable network connections to PD [#17020](https://github.com/tikv/tikv/issues/17020) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that backup tasks might get stuck if TiKV becomes unresponsive during the backup process [#53480](https://github.com/pingcap/tidb/issues/53480) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the checkpoint path of backup and restore is incompatible with some external storage [#55265](https://github.com/pingcap/tidb/issues/55265) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the Region fetched from PD does not have a Leader when restoring data using BR or importing data using TiDB Lightning in physical import mode [#51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the transfer of PD leaders might cause BR to panic when restoring data [#53724](https://github.com/pingcap/tidb/issues/53724) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that after pausing, stopping, and rebuilding the log backup task, the task status is normal, but the checkpoint does not advance [#53047](https://github.com/pingcap/tidb/issues/53047) @[RidRisR](https://github.com/RidRisR)
        - Fix the issue that log backups cannot resolve residual locks promptly, causing the checkpoint to fail to advance [#57134](https://github.com/pingcap/tidb/issues/57134) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Fix the issue that the default value of `TIMEZONE` type is not set according to the correct time zone [#10931](https://github.com/pingcap/tiflow/issues/10931) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that TiCDC might panic when the Sorter module reads disk data [#10853](https://github.com/pingcap/tiflow/issues/10853) @[hicqu](https://github.com/hicqu)
        - Fix the issue that data inconsistency might occur when restarting Changefeed repeatedly when performing a large number of `UPDATE` operations in a multi-node environment [#11219](https://github.com/pingcap/tiflow/issues/11219) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that after filtering out `add table partition` events is configured in `ignore-event`, TiCDC does not replicate other types of DML changes for related partitions to the downstream [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC might get stuck when replicating data to Kafka [#9855](https://github.com/pingcap/tiflow/issues/9855) @[hicqu](https://github.com/hicqu)
        - Fix the issue that `DROP PRIMARY KEY` and `DROP UNIQUE KEY` statements are not replicated correctly [#10890](https://github.com/pingcap/tiflow/issues/10890) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the Processor module might get stuck when the downstream Kafka is inaccessible [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - Fix the issue that DM does not set the default database when processing the `ALTER DATABASE` statement, which causes a replication error [#11503](https://github.com/pingcap/tiflow/issues/11503) @[lance6716](https://github.com/lance6716)
        - Fix the issue that multiple DM-master nodes might simultaneously become leaders, leading to data inconsistency [#11602](https://github.com/pingcap/tiflow/issues/11602) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the connection blocking issue by upgrading `go-mysql` [#11041](https://github.com/pingcap/tiflow/issues/11041) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that data replication is interrupted when the index length exceeds the default value of `max-index-length` [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        - Fix the issue that DM returns an error when replicating the `ALTER TABLE ... DROP PARTITION` statement for LIST partitioned tables [#54760](https://github.com/pingcap/tidb/issues/54760) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning fails to receive oversized messages sent from TiKV [#56114](https://github.com/pingcap/tidb/issues/56114) @[fishiu](https://github.com/fishiu)
        - Fix the issue that TiKV data might be corrupted when importing data after disabling the import mode of TiDB Lightning [#15003](https://github.com/tikv/tikv/issues/15003) [#47694](https://github.com/pingcap/tidb/issues/47694) @[lance6716](https://github.com/lance6716)
        - Fix the issue that transaction conflicts occur during data import using TiDB Lightning [#49826](https://github.com/pingcap/tidb/issues/49826) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning might fail to import data when EBS BR is running [#49517](https://github.com/pingcap/tidb/issues/49517) @[mittalrishabh](https://github.com/mittalrishabh)
        - Fix the issue that TiDB Lightning reports a `verify allocator base failed` error when two instances simultaneously start parallel import tasks and are assigned the same task ID [#55384](https://github.com/pingcap/tidb/issues/55384) @[ei-sugimoto](https://github.com/ei-sugimoto)
        - Fix the issue that killing the PD Leader causes TiDB Lightning to report the `invalid store ID 0` error during data import [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)

    + Dumpling

        - Fix the issue that Dumpling reports an error when exporting tables and views at the same time [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)

    + TiDB Binlog
    
        - Fix the issue that deleting rows during the execution of `ADD COLUMN` might report an error `data and columnID count not match` when TiDB Binlog is enabled [#53133](https://github.com/pingcap/tidb/issues/53133) @[tangenta](https://github.com/tangenta)
