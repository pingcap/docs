---
title: TiDB 7.5.1 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.5.1.
---

# TiDB 7.5.1 Release Notes

Release date: February 29, 2024

TiDB version: 7.5.1

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## Compatibility changes

- Prohibit setting [`require_secure_transport`](https://docs.pingcap.com/tidb/v7.5/system-variables#require_secure_transport-new-in-v610) to `ON` in Security Enhanced Mode (SEM) to prevent potential connectivity issues for users [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
- To reduce the overhead of log printing, TiFlash changes the default value of `logger.level` from `"debug"` to `"info"` [#8641](https://github.com/pingcap/tiflash/issues/8641) @[JaySon-Huang](https://github.com/JaySon-Huang)
- Introduce the TiKV configuration item [`gc.num-threads`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#num-threads-new-in-v658-and-v751) to set the number of GC threads when `enable-compaction-filter` is `false`  [#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)
- TiCDC Changefeed introduces the following new configuration items:
    - [`compression`](/ticdc/ticdc-changefeed-config.md): enables you to configure the compression behavior of redo log files [#10176](https://github.com/pingcap/tiflow/issues/10176) @[sdojjy](https://github.com/sdojjy)
    - [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md): enables you to set the automatic cleanup of historical data when replicating data to object storage [#10109](https://github.com/pingcap/tiflow/issues/10109) @[CharlesCheung96](https://github.com/CharlesCheung96)
    - [`consistent.flush-concurrency`](/ticdc/ticdc-changefeed-config.md): enables you to set the concurrency for uploading a single redo file [#10226](https://github.com/pingcap/tiflow/issues/10226) @[sdojjy](https://github.com/sdojjy)

## Improvements

+ TiDB

    - Use `tikv_client_read_timeout` during the DDL schema reload process to reduce the impact of Meta Region Leader read unavailability on the cluster [#48124](https://github.com/pingcap/tidb/issues/48124) @[cfzjywxk](https://github.com/cfzjywxk)
    - Enhance observability related to resource control [#49318](https://github.com/pingcap/tidb/issues/49318) @[glorv](https://github.com/glorv) @[bufferflies](https://github.com/bufferflies) @[nolouch](https://github.com/nolouch)

        As more and more users use resource groups to isolate application workloads, Resource Control provides enhanced data based on resource groups. This helps you monitor resource group workloads and settings, ensuring that you can quickly identify and accurately diagnose problems, including:

        - [Slow Queries](/identify-slow-queries.md): add the resource group name, resource unit (RU) consumption, and time for waiting for resources.
        - [Statement Summary Tables](/statement-summary-tables.md): add the resource group name, RU consumption, and time for waiting for resources.
        - In the system variable [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014), add a new entry `ru_consumption` to indicate the consumed [RU](/tidb-resource-control.md#what-is-request-unit-ru) by SQL statements. You can use this variable to get the resource consumption of the last statement in the session.
        - Add database metrics based on resource groups: QPS/TPS, execution time (P999/P99/P95), number of failures, and number of connections.

    - Modify the `CANCEL IMPORT JOB` statement to a synchronous statement [#48736](https://github.com/pingcap/tidb/issues/48736) @[D3Hunter](https://github.com/D3Hunter)
    - Support the [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v7.5/sql-statement-flashback-cluster) syntax [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger)
    - Optimize the TiDB implementation when handling some type conversions and fix related issues [#47945](https://github.com/pingcap/tidb/issues/47945) [#47864](https://github.com/pingcap/tidb/issues/47864) [#47829](https://github.com/pingcap/tidb/issues/47829) [#47816](https://github.com/pingcap/tidb/issues/47816) @[YangKeao](https://github.com/YangKeao) @[lcwangchao](https://github.com/lcwangchao)
    - When a non-binary collation is set and the query includes `LIKE`, the optimizer generates an `IndexRangeScan` to improve the execution efficiency [#48181](https://github.com/pingcap/tidb/issues/48181) [#49138](https://github.com/pingcap/tidb/issues/49138) @[time-and-fate](https://github.com/time-and-fate)
    - Enhance the ability to convert `OUTER JOIN` to `INNER JOIN` in specific scenarios [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)
    - Support multiple accelerated `ADD INDEX` DDL tasks to be queued for execution, instead of falling back to normal `ADD INDEX` tasks [#47758](https://github.com/pingcap/tidb/issues/47758) @[tangenta](https://github.com/tangenta)
    - Improve the speed of adding indexes to empty tables [#49682](https://github.com/pingcap/tidb/issues/49682) @[zimulala](https://github.com/zimulala)

+ TiKV

    - Enhance the slow store detection algorithm by improving its sensitivity and reducing the false-positive rate, especially in intensive read and write load scenarios [#15909](https://github.com/tikv/tikv/issues/15909) @[LykxSassinator](https://github.com/LykxSassinator)

+ TiFlash

    - Improve the calculation method for [Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru) to make RU values more stable [#8391](https://github.com/pingcap/tiflash/issues/8391) @[guo-shaoge](https://github.com/guo-shaoge)
    - Reduce the impact of disk performance jitter on read latency [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Reduce the impact of background GC tasks on read and write task latency [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Improve the speed of merging SST files during data restore by using a more efficient algorithm [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - Support creating databases in batch during data restore [#50767](https://github.com/pingcap/tidb/issues/50767) @[Leavrth](https://github.com/Leavrth)
        - Support ingesting SST files in batch during data restore [#16267](https://github.com/tikv/tikv/issues/16267) @[3pointer](https://github.com/3pointer)
        - Print the information of the slowest Region that affects global checkpoint advancement in logs and metrics during log backups [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - Improve the table creation performance of the `RESTORE` statement in scenarios with large datasets [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - BR can pause Region merging by setting the `merge-schedule-limit` configuration to `0` [#7148](https://github.com/tikv/pd/issues/7148) @[BornChanger](https://github.com/3pointer)
        - Refactor the BR exception handling mechanism to increase tolerance for unknown errors [#47656](https://github.com/pingcap/tidb/issues/47656) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Support searching TiCDC logs in the TiDB Dashboard [#10263](https://github.com/pingcap/tiflow/issues/10263) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Support [querying the downstream synchronization status of a changefeed](https://docs.pingcap.com/tidb/v7.5/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed), which helps you determine whether the upstream data changes received by TiCDC have been synchronized to the downstream system completely [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)
        - Improve the performance of TiCDC replicating data to object storage by increasing parallelism [#10098](https://github.com/pingcap/tiflow/issues/10098) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Lightning

        - Improve the performance of `ALTER TABLE` when importing a large number of small tables [#50105](https://github.com/pingcap/tidb/issues/50105) @[D3Hunter](https://github.com/D3Hunter)

## Bug fixes

+ TiDB

    - Fix the issue that setting the system variable `tidb_service_scope` does not take effect [#49245](https://github.com/pingcap/tidb/issues/49245) @[ywqzzy](https://github.com/ywqzzy)
    - Fix the issue that the communication protocol cannot handle packets larger than or equal to 16 MB when compression is enabled [#47157](https://github.com/pingcap/tidb/issues/47157) [#47161](https://github.com/pingcap/tidb/issues/47161) @[dveeden](https://github.com/dveeden)
    - Fix the issue that the `approx_percentile` function might cause TiDB panic [#40463](https://github.com/pingcap/tidb/issues/40463) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that TiDB might implicitly insert the `from_binary` function when the argument of a string function is a `NULL` constant, causing some expressions unable to be pushed down to TiFlash [#49526](https://github.com/pingcap/tidb/issues/49526) @[YangKeao](https://github.com/YangKeao)
    - Fix the goroutine leak issue that might occur when the `HashJoin` operator fails to spill to disk [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that `BIT` type columns might cause query errors due to decode failures when they are involved in calculations of some functions [#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the goroutine leak issue that occurs when the memory usage of CTE queries exceed limits [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that wrong results might be returned when TiFlash late materialization processes associated columns [#49241](https://github.com/pingcap/tidb/issues/49241) [#51204](https://github.com/pingcap/tidb/issues/51204) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that the background job thread of TiDB might panic when TiDB records historical statistics [#49076](https://github.com/pingcap/tidb/issues/49076) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the error that might occur when TiDB merges histograms of global statistics for partitioned tables [#49023](https://github.com/pingcap/tidb/issues/49023) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the historical statistics of the `stats_meta` table are not updated after a partition is dropped [#49334](https://github.com/pingcap/tidb/issues/49334) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue of incorrect query results caused by multi-valued indexes mistakenly selected as the `Index Join` probe side [#50382](https://github.com/pingcap/tidb/issues/50382) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the `USE_INDEX_MERGE` hint does not take effect on multi-valued indexes [#50553](https://github.com/pingcap/tidb/issues/50553) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that users might get errors when querying the `INFORMATION_SCHEMA.ANALYZE_STATUS` system table [#48835](https://github.com/pingcap/tidb/issues/48835) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue of wrong query results due to TiDB incorrectly eliminating constant values in `group by` [#38756](https://github.com/pingcap/tidb/issues/38756) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that the `processed_rows` of the `ANALYZE` task on a table might exceed the total number of rows in that table [#50632](https://github.com/pingcap/tidb/issues/50632) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that TiDB might panic when using the `EXECUTE` statement to execute `PREPARE STMT` after the `tidb_enable_prepared_plan_cache` system variable is enabled and then disabled [#49344](https://github.com/pingcap/tidb/issues/49344) @[qw4990](https://github.com/qw4990)
    - Fix the `Column ... in from clause is ambiguous` error that might occur when a query uses `NATURAL JOIN` [#32044](https://github.com/pingcap/tidb/issues/32044) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that using a multi-valued index to access an empty JSON array might return incorrect results [#50125](https://github.com/pingcap/tidb/issues/50125) @[YangKeao](https://github.com/YangKeao)
    - Fix the `Can't find column ...` error that might occur when aggregate functions are used for group calculations [#50926](https://github.com/pingcap/tidb/issues/50926) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the control of `SET_VAR` for variables of the string type might become invalid [#50507](https://github.com/pingcap/tidb/issues/50507) @[qw4990](https://github.com/qw4990)
    - Fix the issue that high CPU usage of TiDB occurs due to long-term memory pressure caused by `tidb_server_memory_limit` [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that the completion times of two DDL tasks with dependencies are incorrectly sequenced [#49498](https://github.com/pingcap/tidb/issues/49498) @[tangenta](https://github.com/tangenta)
    - Fix the issue that illegal optimizer hints might cause valid hints to be ineffective [#49308](https://github.com/pingcap/tidb/issues/49308) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that DDL statements with the `CHECK` constraint are stuck [#47632](https://github.com/pingcap/tidb/issues/47632) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that the behavior of the `ENFORCED` option in the `CHECK` constraint is inconsistent with MySQL 8.0 [#47567](https://github.com/pingcap/tidb/issues/47567) [#47631](https://github.com/pingcap/tidb/issues/47631) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that CTE queries might report an error `type assertion for CTEStorageMap failed` during the retry process [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `DELETE` and `UPDATE` statements using index lookup might report an error when `tidb_multi_statement_mode` mode is enabled [#50012](https://github.com/pingcap/tidb/issues/50012) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `UPDATE` or `DELETE` statements containing `WITH RECURSIVE` CTEs might produce incorrect results [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - Fix the issue that the optimizer incorrectly converts TiFlash selection path to the DUAL table in specific scenarios [#49285](https://github.com/pingcap/tidb/issues/49285) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the same query plan has different `PLAN_DIGEST` values in some cases [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - Fix the issue that after the time window for automatic statistics updates is configured, statistics might still be updated outside that time window [#49552](https://github.com/pingcap/tidb/issues/49552) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the query result is incorrect when an `ENUM` type column is used as the join key [#48991](https://github.com/pingcap/tidb/issues/48991) @[winoros](https://github.com/winoros)
    - Fix the issue that executing `UNIQUE` index lookup with an `ORDER BY` clause might cause an error [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    - Fix the issue that `LIMIT` in multi-level nested `UNION` queries might become ineffective [#49874](https://github.com/pingcap/tidb/issues/49874) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the result of `COUNT(INT)` calculated by MPP might be incorrect [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that parsing invalid values of `ENUM` or `SET` types would directly cause SQL statement errors [#49487](https://github.com/pingcap/tidb/issues/49487) @[winoros](https://github.com/winoros)
    - Fix the issue that TiDB panics and reports an error `invalid memory address or nil pointer dereference` [#42739](https://github.com/pingcap/tidb/issues/42739) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that executing `UNION ALL` with the DUAL table as the first subnode might cause an error [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - Fix the issue that common hints do not take effect in `UNION ALL` statements [#50068](https://github.com/pingcap/tidb/issues/50068) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that TiDB server might panic during graceful shutdown [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    - Fix the issue that Daylight Saving Time is displayed incorrectly in some time zones [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    - Fix the issue that static `CALIBRATE RESOURCE` relies on the Prometheus data [#49174](https://github.com/pingcap/tidb/issues/49174) @[glorv](https://github.com/glorv)
    - Fix the issue that hints cannot be used in `REPLACE INTO` statements [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that executing queries containing the `GROUP_CONCAT(ORDER BY)` syntax might return errors [#49986](https://github.com/pingcap/tidb/issues/49986) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that TiDB server might consume a significant amount of resources when the enterprise plugin for audit logging is used [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that using old interfaces might cause inconsistent metadata for tables [#49751](https://github.com/pingcap/tidb/issues/49751) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that disabling `tidb_enable_collect_execution_info` causes the coprocessor cache to panic [#48212](https://github.com/pingcap/tidb/issues/48212) @[you06](https://github.com/you06)
    - Fix the issue that executing `ALTER TABLE ... LAST PARTITION` fails when the partition column type is `DATETIME` [#48814](https://github.com/pingcap/tidb/issues/48814) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that the `COMMIT` or `ROLLBACK` operation executed through `COM_STMT_EXECUTE` fails to terminate transactions that have timed out [#49151](https://github.com/pingcap/tidb/issues/49151) @[zyguan](https://github.com/zyguan)
    - Fix the issue that histogram statistics might not be parsed into readable strings when the histogram boundary contains `NULL` [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that queries containing common table expressions (CTEs) unexpectedly get stuck when the memory limit is exceeded [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that data is inconsistent under the TiDB Distributed eXecution Framework (DXF) when executing `ADD INDEX` after the DDL Owner is network isolated [#49773](https://github.com/pingcap/tidb/issues/49773) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the auto-increment ID allocation reports an error due to concurrent conflicts when using an auto-increment column with `AUTO_ID_CACHE=1` [#50519](https://github.com/pingcap/tidb/issues/50519) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB might panic when a query contains the Apply operator and the `fatal error: concurrent map writes` error occurs [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    - Fix the TiDB node panic issue that occurs when DDL `jobID` is restored to 0 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that query results are incorrect due to `STREAM_AGG()` incorrectly handling CI [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - Mitigate the issue that TiDB nodes might encounter OOM errors when dealing with a large number of tables or partitions [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    - Fix the issue that the `LEADING` hint does not take effect in `UNION ALL` statements [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `LIMIT` and `OPRDERBY` might be invalid in nested `UNION` queries [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that a query containing the IndexHashJoin operator gets stuck when memory exceeds `tidb_mem_quota_query` [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that TiDB returns wrong query results when processing `ENUM` or `SET` types by constant propagation [#49440](https://github.com/pingcap/tidb/issues/49440) @[winoros](https://github.com/winoros)
    - Fix the issue that executing `SELECT INTO OUTFILE` using the `PREPARE` method incorrectly returns a success message instead of an error [#49166](https://github.com/pingcap/tidb/issues/49166) @[qw4990](https://github.com/qw4990)
    - Fix the issue that enforced sorting might become ineffective when a query uses optimizer hints (such as `STREAM_AGG()`) that enforce sorting and its execution plan contains `IndexMerge` [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that tables with `AUTO_ID_CACHE=1` might lead to gRPC client leaks when there are a large number of tables [#48869](https://github.com/pingcap/tidb/issues/48869) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that in non-strict mode (`sql_mode = ''`), truncation during executing `INSERT` still reports an error [#49369](https://github.com/pingcap/tidb/issues/49369) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that using the `_` wildcard in `LIKE` when the data contains trailing spaces can result in incorrect query results [#48983](https://github.com/pingcap/tidb/issues/48983) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that executing `ADMIN CHECK` after updating the `tidb_mem_quota_query` system variable returns `ERROR 8175` [#49258](https://github.com/pingcap/tidb/issues/49258) @[tangenta](https://github.com/tangenta)
    - Fix the issue of excessive statistical error in constructing statistics caused by Golang's implicit conversion algorithm [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - Fix the issue that queries containing CTEs report `runtime error: index out of range [32] with length 32` when `tidb_max_chunk_size` is set to a small value [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)

+ TiKV

    - Fix the issue that enabling `tidb_enable_row_level_checksum` might cause TiKV to panic [#16371](https://github.com/tikv/tikv/issues/16371) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue that TiKV might panic when gRPC threads are checking `is_shutdown` [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)
    - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - Fix the issue that `blob-run-mode` in Titan cannot be updated online [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Fix the issue that TiDB and TiKV might produce inconsistent results when processing `DECIMAL` arithmetic multiplication truncation [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)
    - Fix the issue that Flashback might get stuck when encountering `notLeader` or `regionNotFound` [#15712](https://github.com/tikv/tikv/issues/15712) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that damaged SST files might be spread to other TiKV nodes [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that if TiKV runs extremely slowly, it might panic after Region merge [#16111](https://github.com/tikv/tikv/issues/16111) @[overvenus](https://github.com/overvenus)
    - Fix the issue that the joint state of DR Auto-Sync might time out when scaling out [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that Resolved TS might be blocked for two hours [#11847](https://github.com/tikv/tikv/issues/11847) [#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - Fix the issue that `cast_duration_as_time` might return incorrect results [#16211](https://github.com/tikv/tikv/issues/16211) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that TiKV hangs in corner cases (for example, when disk I/O operations are blocked), which affects availability [#16368](https://github.com/tikv/tikv/issues/16368) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - Fix the issue that querying resource groups in batch might cause PD to panic [#7206](https://github.com/tikv/pd/issues/7206) @[nolouch](https://github.com/nolouch)
    - Fix the issue that PD cannot read resource limitations when it is started with `systemd` [#7628](https://github.com/tikv/pd/issues/7628) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that continuous jitter in PD disk latency might cause PD to fail to select a new leader [#7251](https://github.com/tikv/pd/issues/7251) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that a network partition in PD might cause scheduling not to be started immediately [#7016](https://github.com/tikv/pd/issues/7016) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that the PD monitoring item `learner-peer-count` does not synchronize the old value after a leader switch [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that when PD leader is transferred and there is a network partition between the new leader and the PD client, the PD client fails to update the information of the leader [#7416](https://github.com/tikv/pd/issues/7416) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix some security issues by upgrading the version of Gin Web Framework from v1.8.1 to v1.9.1 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)
    - Fix the issue that the orphan peer is deleted when the number of replicas does not meet the requirements [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that querying a Region without a leader using `pd-ctl` might cause PD to panic [#7630](https://github.com/tikv/pd/issues/7630) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - Fix the issue that TiFlash might panic due to unstable network connections with PD during replica migration [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that removing and then re-adding TiFlash replicas might lead to data corruption in TiFlash [#8695](https://github.com/pingcap/tiflash/issues/8695) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix a potential issue that `FLASHBACK TABLE` or `RECOVER TABLE` might fail to recover data of some TiFlash replicas if `DROP TABLE` is executed immediately after data insertion [#8395](https://github.com/pingcap/tiflash/issues/8395) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix incorrect display of maximum percentile time for some panels in Grafana [#8076](https://github.com/pingcap/tiflash/issues/8076) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might crash during remote reads [#8685](https://github.com/pingcap/tiflash/issues/8685) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiFlash incorrectly handles `ENUM` when the `ENUM` value is 0 [#8311](https://github.com/pingcap/tiflash/issues/8311) @[solotzg](https://github.com/solotzg)
    - Fix the issue that short queries executed successfully print excessive info logs [#8592](https://github.com/pingcap/tiflash/issues/8592) @[windtalker](https://github.com/windtalker)
    - Fix the issue that the memory usage increases significantly due to slow queries [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that the `lowerUTF8` and `upperUTF8` functions do not allow characters in different cases to occupy different bytes [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - Fix the potential OOM issue that might occur when scanning multiple partitioned tables during stream read [#8505](https://github.com/pingcap/tiflash/issues/8505) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue of memory leak when TiFlash encounters memory limitation during query [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - Fix the TiFlash panic issue when TiFlash encounters conflicts during concurrent DDL execution [#8578](https://github.com/pingcap/tiflash/issues/8578) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash panics after executing `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`, which changes nullable columns to non-nullable [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that query results are incorrect when querying with filtering conditions like `ColumnRef in (Literal, Func...)` [#8631](https://github.com/pingcap/tiflash/issues/8631) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that data of TiFlash replicas would still be garbage collected after executing `FLASHBACK DATABASE` [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might not be able to select the GC owner of object storage data under the disaggregated storage and compute architecture [#8519](https://github.com/pingcap/tiflash/issues/8519) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the random invalid memory access issue that might occur with `GREATEST` or `LEAST` functions containing constant string parameters [#8604](https://github.com/pingcap/tiflash/issues/8604) @[windtalker](https://github.com/windtalker)
    - Fix the issue that TiFlash replica data might be accidentally deleted after performing point-in-time recovery (PITR) or executing `FLASHBACK CLUSTER TO`, which might result in data anomalies [#8777](https://github.com/pingcap/tiflash/issues/8777) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash Anti Semi Join might return incorrect results when the join includes non-equivalent conditions [#8791](https://github.com/pingcap/tiflash/issues/8791) @[windtalker](https://github.com/windtalker)
+ Tools

    + Backup & Restore (BR)

        - Fix the issue that data restore is slowed down due to absence of a leader on a TiKV node [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that full restore still requires the target cluster to be empty after the `--filter` option is specified [#51009](https://github.com/pingcap/tidb/issues/51009) @[3pointer](https://github.com/3pointer)
        - Fix the issue that when resuming from a checkpoint after data restore fails, an error `the target cluster is not fresh` occurs [#50232](https://github.com/pingcap/tidb/issues/50232) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that stopping a log backup task causes TiDB to crash [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the `Unsupported collation` error is reported when you restore data from backups of an old version [#49466](https://github.com/pingcap/tidb/issues/49466) @[3pointer](https://github.com/3pointer)
        - Fix the issue that the log backup task can start but does not work properly if failing to connect to PD during task initialization [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that BR generates incorrect URIs for external storage files [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that log backup gets stuck after changing the TiKV IP address on the same node [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)
        - Fix the issue that BR cannot retry when encountering an error while reading file content from S3 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - Fix the issue that the sink module fails to restart correctly after encountering an error when Syncpoint is enabled (`enable-sync-point = true`) [#10091](https://github.com/pingcap/tiflow/issues/10091) @[hicqu](https://github.com/hicqu)
        - Fix the issue that the file sequence number generated by the storage service might not increment correctly when using the storage sink [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the Syncpoint table might be incorrectly replicated [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that OAuth2.0, TLS, and mTLS cannot be enabled properly when using Apache Pulsar as the downstream [#10602](https://github.com/pingcap/tiflow/issues/10602) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that TiCDC returns the `ErrChangeFeedAlreadyExists` error when concurrently creating multiple changefeeds [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the changefeed `resolved ts` does not advance in extreme cases [#10157](https://github.com/pingcap/tiflow/issues/10157) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC mistakenly closes the connection with TiKV in certain special scenarios [#10239](https://github.com/pingcap/tiflow/issues/10239) @[hicqu](https://github.com/hicqu)
        - Fix the issue that the TiCDC server might panic when replicating data to an object storage service [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that the changefeed reports an error after `TRUNCATE PARTITION` is executed on the upstream table [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that after filtering out `add table partition` events is configured in `ignore-event`, TiCDC does not replicate other types of DML changes for related partitions to the downstream [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the potential data race issue during `kv-client` initialization [#10095](https://github.com/pingcap/tiflow/issues/10095) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - Fix the issue that a migration task error occurs when the downstream table structure contains `shard_row_id_bits` [#10308](https://github.com/pingcap/tiflow/issues/10308) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that DM encounters "event type truncate not valid" error that causes the upgrade to fail [#10282](https://github.com/pingcap/tiflow/issues/10282) @[GMHDBJD](https://github.com/GMHDBJD)
