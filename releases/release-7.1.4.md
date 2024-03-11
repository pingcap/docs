---
title: TiDB 7.1.4 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.1.4.
---

# TiDB 7.1.4 Release Notes

Release date: March 11, 2024

TiDB version: 7.1.4

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v7.1.4#version-list)

## Compatibility changes

- To reduce the overhead of log printing, TiFlash changes the default value of `logger.level` from `"debug"` to `"info"` [#8641](https://github.com/pingcap/tiflash/issues/8641) @[JaySon-Huang](https://github.com/JaySon-Huang)
- Introduce the TiKV configuration item [`gc.num-threads`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#num-threads-new-in-v658) to set the number of GC threads when `enable-compaction-filter` is `false`  [#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)

## Improvements

+ TiDB

    - Enhance the ability to convert `OUTER JOIN` to `INNER JOIN` in specific scenarios [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)
    - When `force-init-stats` is set to `true`, TiDB waits for statistics initialization to finish before providing services during TiDB startup. This setting no longer blocks the startup of HTTP servers, which enables users to continue monitoring [#50854](https://github.com/pingcap/tidb/issues/50854) @[hawkingrei](https://github.com/hawkingrei)

+ TiKV

    - When TiKV detects the existence of corrupted SST files, it logs the specific reasons for the corruption [#16308](https://github.com/tikv/tikv/issues/16308) @[overvenus](https://github.com/overvenus)

+ PD

    - Improve the speed of PD automatically updating cluster status when the backup cluster is disconnected [#6883](https://github.com/tikv/pd/issues/6883) @[disksing](https://github.com/disksing)

+ TiFlash

    - Reduce the impact of background GC tasks on read and write task latency [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Reduce the impact of disk performance jitter on read latency [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Support creating databases in batch during data restore [#50767](https://github.com/pingcap/tidb/issues/50767) @[Leavrth](https://github.com/Leavrth)
        - Improve the table creation performance of the `RESTORE` statement in scenarios with large datasets [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - Improve the speed of merging SST files during data restore by using a more efficient algorithm [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - Support ingesting SST files in batch during data restore [#16267](https://github.com/tikv/tikv/issues/16267) @[3pointer](https://github.com/3pointer)
        - Print the information of the slowest Region that affects global checkpoint advancement in logs and metrics during log backups [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - Remove an outdated compatibility check when using Google Cloud Storage (GCS) as the external storage [#50533](https://github.com/pingcap/tidb/issues/50533) @[lance6716](https://github.com/lance6716)
        - Implement a lock mechanism to avoid executing multiple log backup truncation tasks (`br log truncate`) simultaneously [#49414](https://github.com/pingcap/tidb/issues/49414) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - When the downstream is Kafka, the topic expression allows `schema` to be optional and supports specifying a topic name directly [#9763](https://github.com/pingcap/tiflow/issues/9763) @[3AceShowHand](https://github.com/3AceShowHand)
        - Support [querying the downstream synchronization status of a changefeed](https://docs.pingcap.com/tidb/v7.1/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed), which helps you determine whether the upstream data changes received by TiCDC have been synchronized to the downstream system completely [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)
        - Support searching TiCDC logs in the TiDB Dashboard [#10263](https://github.com/pingcap/tiflow/issues/10263) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Lightning

        - Improve the performance in scenarios where multiple tables are imported by canceling the lock operation when executing `ALTER TABLE` [#50105](https://github.com/pingcap/tidb/issues/50105) @[D3Hunter](https://github.com/D3Hunter)

## Bug fixes

+ TiDB

    - Fix the issue that the `DELETE` and `UPDATE` statements using index lookup might report an error when `tidb_multi_statement_mode` mode is enabled [#50012](https://github.com/pingcap/tidb/issues/50012) @[tangenta](https://github.com/tangenta)
    - Fix the issue that CTE queries might report an error `type assertion for CTEStorageMap failed` during the retry process [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue of excessive statistical error in constructing statistics caused by Golang's implicit conversion algorithm [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - Fix the issue that errors might be returned during the concurrent merging of global statistics for partitioned tables [#48713](https://github.com/pingcap/tidb/issues/48713) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue of wrong query results due to TiDB incorrectly eliminating constant values in `group by` [#38756](https://github.com/pingcap/tidb/issues/38756) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that `BIT` type columns might cause query errors due to decode failures when they are involved in calculations of some functions [#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that `LIMIT` in multi-level nested `UNION` queries might become ineffective [#49874](https://github.com/pingcap/tidb/issues/49874) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the auto-increment ID allocation reports an error due to concurrent conflicts when using an auto-increment column with `AUTO_ID_CACHE=1` [#50519](https://github.com/pingcap/tidb/issues/50519) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the `Column ... in from clause is ambiguous` error that might occur when a query uses `NATURAL JOIN` [#32044](https://github.com/pingcap/tidb/issues/32044) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that enforced sorting might become ineffective when a query uses optimizer hints (such as `STREAM_AGG()`) that enforce sorting and its execution plan contains `IndexMerge` [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that query results are incorrect due to `STREAM_AGG()` incorrectly handling CI [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the goroutine leak issue that might occur when the `HashJoin` operator fails to spill to disk [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that hints cannot be used in `REPLACE INTO` statements [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that executing queries containing the `GROUP_CONCAT(ORDER BY)` syntax might return errors [#49986](https://github.com/pingcap/tidb/issues/49986) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that using a multi-valued index to access an empty JSON array might return incorrect results [#50125](https://github.com/pingcap/tidb/issues/50125) @[YangKeao](https://github.com/YangKeao)
    - Fix the goroutine leak issue that occurs when the memory usage of CTE queries exceed limits [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that using old interfaces might cause inconsistent metadata for tables [#49751](https://github.com/pingcap/tidb/issues/49751) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that executing `UNIQUE` index lookup with an `ORDER BY` clause might cause an error [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    - Fix the issue that common hints do not take effect in `UNION ALL` statements [#50068](https://github.com/pingcap/tidb/issues/50068) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that a query containing the IndexHashJoin operator gets stuck when memory exceeds `tidb_mem_quota_query` [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that `UPDATE` or `DELETE` statements containing `WITH RECURSIVE` CTEs might produce incorrect results [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - Fix the issue that histogram statistics might not be parsed into readable strings when the histogram boundary contains `NULL` [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that TiDB might panic when a query contains the Apply operator and the `fatal error: concurrent map writes` error occurs [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    - Fix the `Can't find column ...` error that might occur when aggregate functions are used for group calculations [#50926](https://github.com/pingcap/tidb/issues/50926) @[qw4990](https://github.com/qw4990)
    - Fix the issue that TiDB returns wrong query results when processing `ENUM` or `SET` types by constant propagation [#49440](https://github.com/pingcap/tidb/issues/49440) @[winoros](https://github.com/winoros)
    - Fix the issue that the completion times of two DDL tasks with dependencies are incorrectly sequenced [#49498](https://github.com/pingcap/tidb/issues/49498) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TiDB might panic when using the `EXECUTE` statement to execute `PREPARE STMT` after the `tidb_enable_prepared_plan_cache` system variable is enabled and then disabled [#49344](https://github.com/pingcap/tidb/issues/49344) @[qw4990](https://github.com/qw4990)
    - Fix the issue that `LIMIT` and `OPRDERBY` might be invalid in nested `UNION` queries [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the `LEADING` hint does not take effect in `UNION ALL` statements [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `COMMIT` or `ROLLBACK` operation executed through `COM_STMT_EXECUTE` fails to terminate transactions that have timed out [#49151](https://github.com/pingcap/tidb/issues/49151) @[zyguan](https://github.com/zyguan)
    - Fix the issue that illegal optimizer hints might cause valid hints to be ineffective [#49308](https://github.com/pingcap/tidb/issues/49308) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that Daylight Saving Time is displayed incorrectly in some time zones [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    - Fix the issue that executing `SELECT INTO OUTFILE` using the `PREPARE` method incorrectly returns a success message instead of an error [#49166](https://github.com/pingcap/tidb/issues/49166) @[qw4990](https://github.com/qw4990)
    - Fix the issue that TiDB might panic when performing a rolling upgrade using `tiup cluster upgrade/start` due to an interaction issue with PD [#50152](https://github.com/pingcap/tidb/issues/50152) @[zimulala](https://github.com/zimulala)
    - Fix the issue that the expected optimization does not take effect when adding an index to an empty table [#49682](https://github.com/pingcap/tidb/issues/49682) @[zimulala](https://github.com/zimulala)
    - Fix the issue that TiDB might OOM when a large number of tables or partitions are created [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    - Fix the issue that adding an index might cause inconsistent index data when the network is unstable [#49773](https://github.com/pingcap/tidb/issues/49773) @[tangenta](https://github.com/tangenta)
    - Fix the execution order of DDL jobs to prevent TiCDC from receiving out-of-order DDLs [#49498](https://github.com/pingcap/tidb/issues/49498) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the `tidb_gogc_tuner_threshold` system variable is not adjusted accordingly after the `tidb_server_memory_limit` variable is modified [#48180](https://github.com/pingcap/tidb/issues/48180) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the query result of a range partitioned table is incorrect in some cases due to wrong partition pruning [#50082](https://github.com/pingcap/tidb/issues/50082) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that DDL operations such as renaming tables are stuck when the `CREATE TABLE` statement contains specific partitions or constraints [#50972](https://github.com/pingcap/tidb/issues/50972) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that getting the default value of a column returns an error if the column default value is deleted [#50043](https://github.com/pingcap/tidb/issues/50043) [#51324](https://github.com/pingcap/tidb/issues/51324) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that the monitoring metric `tidb_statistics_auto_analyze_total` on Grafana is not displayed as an integer [#51051](https://github.com/pingcap/tidb/issues/51051) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `tidb_merge_partition_stats_concurrency` variable does not take effect when `auto analyze` is processing partitioned tables [#47594](https://github.com/pingcap/tidb/issues/47594) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `index out of range` error might occur when a query involves JOIN operations [#42588](https://github.com/pingcap/tidb/issues/42588) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that wrong results might be returned when TiFlash late materialization processes associated columns [#49241](https://github.com/pingcap/tidb/issues/49241) [#51204](https://github.com/pingcap/tidb/issues/51204) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ TiKV

    - Fix the issue that hibernated Regions are not promptly awakened in exceptional circumstances [#16368](https://github.com/tikv/tikv/issues/16368) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that the entire Region becomes unavailable when one replica is offline, by checking the last heartbeat time of all replicas of the Region before taking a node offline [#16465](https://github.com/tikv/tikv/issues/16465) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Fix the issue that table properties stored in RocksDB might be inaccurate when Titan is enabled [#16319](https://github.com/tikv/tikv/issues/16319) @[hicqu](https://github.com/hicqu)
    - Fix the issue that executing `tikv-ctl compact-cluster` fails when a cluster has TiFlash nodes [#16189](https://github.com/tikv/tikv/issues/16189) @[frew](https://github.com/frew)
    - Fix the issue that TiKV might panic when gRPC threads are checking `is_shutdown` [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)
    - Fix the issue that TiDB and TiKV might produce inconsistent results when processing `DECIMAL` arithmetic multiplication truncation [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)
    - Fix the issue that `cast_duration_as_time` might return incorrect results [#16211](https://github.com/tikv/tikv/issues/16211) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - Fix the issue that JSON integers greater than the maximum `INT64` value but less than the maximum `UINT64` value are parsed as `FLOAT64` by TiKV, resulting in inconsistency with TiDB [#16512](https://github.com/tikv/tikv/issues/16512) @[YangKeao](https://github.com/YangKeao)

+ PD

    - Fix the issue that slots are not fully deleted in a resource group client, which causes the number of the allocated tokens to be less than the specified value [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that some TSO logs do not print the error cause [#7496](https://github.com/tikv/pd/issues/7496) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that the default resource group accumulates unnecessary tokens when `BURSTABLE` is enabled [#7206](https://github.com/tikv/pd/issues/7206) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that there is no output when the `evict-leader-scheduler` interface is called [#7672](https://github.com/tikv/pd/issues/7672) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the memory leak issue that occurs when `watch etcd` is not turned off correctly [#7807](https://github.com/tikv/pd/issues/7807) @[rleungx](https://github.com/rleungx)
    - Fix the issue that data race occurs when the `MergeLabels` function is called [#7535](https://github.com/tikv/pd/issues/7535) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that TiDB Dashboard fails to get the TiKV profile when TLS is enabled [#7561](https://github.com/tikv/pd/issues/7561) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that the orphan peer is deleted when the number of replicas does not meet the requirements [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that `available_stores` is calculated incorrectly for clusters adopting the Data Replication Auto Synchronous (DR Auto-Sync) mode [#7221](https://github.com/tikv/pd/issues/7221) @[disksing](https://github.com/disksing)
    - Fix the issue that `canSync` and `hasMajority` might be calculated incorrectly for clusters adopting the Data Replication Auto Synchronous (DR Auto-Sync) mode when the configuration of Placement Rules is complex [#7201](https://github.com/tikv/pd/issues/7201) @[disksing](https://github.com/disksing)
    - Fix the issue that the primary AZ cannot add TiKV nodes when the secondary AZ is down for clusters adopting the Data Replication Auto Synchronous (DR Auto-Sync) mode [#7218](https://github.com/tikv/pd/issues/7218) @[disksing](https://github.com/disksing)
    - Fix the issue that querying resource groups in batch might cause PD to panic [#7206](https://github.com/tikv/pd/issues/7206) @[nolouch](https://github.com/nolouch)
    - Fix the issue that querying a Region without a leader using `pd-ctl` might cause PD to panic [#7630](https://github.com/tikv/pd/issues/7630) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the PD monitoring item `learner-peer-count` does not synchronize the old value after a leader switch [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that PD cannot read resource limitations when it is started with `systemd` [#7628](https://github.com/tikv/pd/issues/7628) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - Fix the issue that TiFlash might panic due to unstable network connections with PD during replica migration [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash incorrectly handles `ENUM` when the `ENUM` value is 0 [#8311](https://github.com/pingcap/tiflash/issues/8311) @[solotzg](https://github.com/solotzg)
    - Fix the random invalid memory access issue that might occur with `GREATEST` or `LEAST` functions containing constant string parameters [#8604](https://github.com/pingcap/tiflash/issues/8604) @[windtalker](https://github.com/windtalker)
    - Fix the issue that the `lowerUTF8` and `upperUTF8` functions do not allow characters in different cases to occupy different bytes [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that short queries executed successfully print excessive info logs [#8592](https://github.com/pingcap/tiflash/issues/8592) @[windtalker](https://github.com/windtalker)
    - Fix the issue that the memory usage increases significantly due to slow queries [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that TiFlash panics after executing `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`, which changes nullable columns to non-nullable [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that after terminating a query, TiFlash crashes due to concurrent data conflicts when a large number of tasks on TiFlash are canceled at the same time [#7432](https://github.com/pingcap/tiflash/issues/7432) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue that TiFlash might crash during remote reads [#8685](https://github.com/pingcap/tiflash/issues/8685) @[zanmato1984](https://github.com/zanmato1984)
    - Fix the issue that TiFlash Anti Semi Join might return incorrect results when the join includes non-equivalent conditions [#8791](https://github.com/pingcap/tiflash/issues/8791) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that stopping a log backup task causes TiDB to crash [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that data restore is slowed down due to absence of a leader on a TiKV node [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that log backup gets stuck after changing the TiKV IP address on the same node [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)
        - Fix the issue that BR cannot retry when encountering an error while reading file content from S3 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the `Unsupported collation` error is reported when you restore data from backups of an old version [#49466](https://github.com/pingcap/tidb/issues/49466) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Fix the issue that the changefeed reports an error after `TRUNCATE PARTITION` is executed on the upstream table [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that the changefeed `resolved ts` does not advance in extreme cases [#10157](https://github.com/pingcap/tiflow/issues/10157) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that the Syncpoint table might be incorrectly replicated [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that after filtering out `add table partition` events is configured in `ignore-event`, TiCDC does not replicate other types of DML changes for related partitions to the downstream [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the file sequence number generated by the storage service might not increment correctly when using the storage sink [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC returns the `ErrChangeFeedAlreadyExists` error when concurrently creating multiple changefeeds [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that `snapshot lost cased by GC` is not reported in time when resuming a changefeed and the `checkpoint-ts` of the changefeed is smaller than the GC safepoint of TiDB [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC fails to validate `TIMESTAMP` type checksum due to time zone mismatch after data integrity validation for single-row data is enabled [#10573](https://github.com/pingcap/tiflow/issues/10573) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - Fix the issue that a wrong binlog event type in the task configuration causes upgrade failures [#10282](https://github.com/pingcap/tiflow/issues/10282) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that a table with `shard_row_id_bits` causes the schema tracker to fail to initialize [#10308](https://github.com/pingcap/tiflow/issues/10308) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning reports an error when encountering invalid symbolic link files during file scanning [#49423](https://github.com/pingcap/tidb/issues/49423) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning fails to correctly parse date values containing `0` when `NO_ZERO_IN_DATE` is not included in `sql_mode` [#50757](https://github.com/pingcap/tidb/issues/50757) @[GMHDBJD](https://github.com/GMHDBJD)
