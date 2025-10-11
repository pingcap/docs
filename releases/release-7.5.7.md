---
title: TiDB 7.5.7 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.5.7.
---

# TiDB 7.5.7 Release Notes

Release date: September 4, 2025

TiDB version: 7.5.7

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## Compatibility changes

- Change the default value of [`tidb_enable_historical_stats`](https://docs.pingcap.com/tidb/v7.5/system-variables/#tidb_enable_historical_stats) from `ON` to `OFF`, which turns off historical statistics to avoid potential stability issues [#53048](https://github.com/pingcap/tidb/issues/53048) @[hawkingrei](https://github.com/hawkingrei)
- TiKV deprecates the following configuration items and replaces them with the new [`gc.auto-compaction`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file/#gcauto-compaction) configuration group, which controls automatic compaction behavior [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)

    - Deprecated configuration items: [`region-compact-check-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-check-interval), [`region-compact-check-step`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-check-step), [`region-compact-min-tombstones`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-min-tombstones), [`region-compact-tombstones-percent`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-tombstones-percent), [`region-compact-min-redundant-rows`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-min-redundant-rows-new-in-v710), and [`region-compact-redundant-rows-percent`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-redundant-rows-percent-new-in-v710).
    - New configuration items: [`gc.auto-compaction.check-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#check-interval-new-in-v757), [`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#tombstone-num-threshold-new-in-v757), [`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#tombstone-percent-threshold-new-in-v757), [`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#redundant-rows-threshold-new-in-v757), [`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#redundant-rows-percent-threshold-new-in-v757), and [`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#bottommost-level-force-new-in-v757).

## Improvements

+ TiDB

    - Add flow control interfaces for Region splitting and data ingestion during data import [#61553](https://github.com/pingcap/tidb/issues/61553) @[tangenta](https://github.com/tangenta)
    - Optimize the performance of obtaining data distribution information when performing simple queries on tables with large data volumes [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)
    - Add a monitoring metric to observe the write speed to TiKV during index addition [#60925](https://github.com/pingcap/tidb/issues/60925) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Optimize the locking logic of DML during DDL execution to reduce lock conflicts between DML and DDL operations, improving DDL performance in some scenarios. However, due to the additional secondary index locking operations, DML performance might decrease slightly [#62337](https://github.com/pingcap/tidb/issues/62337) @[lcwangchao](https://github.com/lcwangchao)
    - Improve the behavior when the system variable [`tidb_opt_ordering_index_selectivity_threshold`](/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-new-in-v700) is set to `1`, enhancing the control capability of this variable [#60242](https://github.com/pingcap/tidb/issues/60242) @[time-and-fate](https://github.com/time-and-fate)
    - Avoid refreshing statistics across the entire cluster after `ANALYZE` statement execution, reducing the execution time of `ANALYZE` [#57631](https://github.com/pingcap/tidb/issues/57631) @[0xPoe](https://github.com/0xPoe)
    - Support constant folding for columns with `NOT NULL` constraints, folding `IS NULL` evaluations into `FALSE` [#62050](https://github.com/pingcap/tidb/issues/62050) @[hawkingrei](https://github.com/hawkingrei)
    - The optimizer supports constant propagation in more types of `JOIN` operations [#51700](https://github.com/pingcap/tidb/issues/51700) @[hawkingrei](https://github.com/hawkingrei)
    - Improve the performance of temporary index merging when extensive lock conflicts exist between DML and DDL operations [#61433](https://github.com/pingcap/tidb/issues/61433) @[tangenta](https://github.com/tangenta)

+ TiKV

    - Optimize the trigger logic of TiKV compaction to process all data segments in order of reclamation efficiency, reducing the performance impact of MVCC redundant data [#18571](https://github.com/tikv/tikv/issues/18571) @[v01dstar](https://github.com/v01dstar)
    - Optimize the tail latency of async snapshot and write operations in environments with a large number of SST files [#18743](https://github.com/tikv/tikv/issues/18743) @[Connor1996](https://github.com/Connor1996)
    - Improve the speed of Region Merge in scenarios with empty tables and small Regions [#17376](https://github.com/tikv/tikv/issues/17376) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize the handling of `CompactedEvent` in Raftstore by moving it to the `split-check` worker, reducing blocking on the main Raftstore thread [#18532](https://github.com/tikv/tikv/issues/18532) @[LykxSassinator](https://github.com/LykxSassinator)
    - Add metrics for memory usage per thread [#15927](https://github.com/tikv/tikv/issues/15927) @[Connor1996](https://github.com/Connor1996)
    - Log only `SST ingest is experiencing slowdowns` when SST ingest is too slow, and skip calling `get_sst_key_ranges` to avoid performance jitter [#18549](https://github.com/tikv/tikv/issues/18549) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize the jittery access delay when restarting TiKV due to waiting for the log to be applied, improving the stability of TiKV [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize the cleanup mechanism of residual data to mitigate the impact on request latency [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize the performance of `fetch_entries_to` in Raft Engine to reduce contention and improve performance under mixed workloads [#18605](https://github.com/tikv/tikv/issues/18605) @[LykxSassinator](https://github.com/LykxSassinator)
    - Support dynamically modifying flow-control configurations for write operations [#17395](https://github.com/tikv/tikv/issues/17395) @[glorv](https://github.com/glorv)
    - Support ingesting SST files without blocking foreground writes, reducing the impact of latency [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - Optimize the detection mechanism for I/O jitter on KvDB disks when KvDB and RaftDB use separate mount paths [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
    - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ PD

    - Add GO runtime-related monitoring metrics in Prometheus [#8931](https://github.com/tikv/pd/issues/8931) @[bufferflies](https://github.com/bufferflies)
    - Reduce unnecessary error logs [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - Enhance the observability for TiFlash OOM risks in wide table scenarios [#10272](https://github.com/pingcap/tiflash/issues/10272) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Increase the maximum retry count when acquiring storage snapshots to improve query stability for large tables [#10300](https://github.com/pingcap/tiflash/issues/10300) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - When deploying TiDB on Amazon EC2, BR supports AWS Instance Metadata Service Version 2 (IMDSv2). You can configure your EC2 instance to allow BR to use the IAM role associated with the instance for appropriate permissions to access Amazon S3 [#16443](https://github.com/tikv/tikv/issues/16443) @[pingyu](https://github.com/pingyu)
        - The Download API of TiKV supports filtering out data within a certain time range when downloading backup files, which avoids importing outdated or future data versions during restore [#18399](https://github.com/tikv/tikv/issues/18399) @[3pointer](https://github.com/3pointer)

## Bug fixes

+ TiDB

    - Fix the issue that shared KV requests in `IndexMerge` and `IndexLookUp` operators cause data races when pushing down queries [#60175](https://github.com/pingcap/tidb/issues/60175) @[you06](https://github.com/you06)
    - Fix a potential goroutine leak issue in the Hash Aggregation operator [#58004](https://github.com/pingcap/tidb/issues/58004) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that MPP plans might not be selected when indexes on generated columns are set as visible [#47766](https://github.com/pingcap/tidb/issues/47766) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that SQL statements containing `_charset(xxx), _charset(xxx2), ...` generate different digests [#58447](https://github.com/pingcap/tidb/issues/58447) @[xhebox](https://github.com/xhebox)
    - Fix the issue that frequent Region merges prevent TTL jobs from starting [#61512](https://github.com/pingcap/tidb/issues/61512) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that TiFlash query results are inconsistent after executing a lossy DDL statement [#61455](https://github.com/pingcap/tidb/issues/61455) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue of incorrect key range in `ALTER RANGE meta SET PLACEMENT POLICY` [#60888](https://github.com/pingcap/tidb/issues/60888) @[nolouch](https://github.com/nolouch)
    - Fix the issue that the data in the **Stats Healthy Distribution** panel of Grafana might be incorrect [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the comparison behavior of `latin1_bin` differs from that of `utf8mb4_bin` and `utf8_bin` [#60701](https://github.com/pingcap/tidb/issues/60701) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that after disabling metadata locking (MDL), DDL operations get stuck after failing to update the schema version [#61210](https://github.com/pingcap/tidb/issues/61210) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that enabling Redact log does not take effect in certain scenarios [#59279](https://github.com/pingcap/tidb/issues/59279) @[tangenta](https://github.com/tangenta)
    - Fix the issue that a TiDB session might crash when Fix Control #44855 is enabled [#59762](https://github.com/pingcap/tidb/issues/59762) @[winoros](https://github.com/winoros)
    - Remove redundant log entries when the `IndexLookup` operator encounters a `context canceled` error [#61072](https://github.com/pingcap/tidb/issues/61072) @[yibin87](https://github.com/yibin87)
    - Fix the issue that improper exception handling for statistics causes in-memory statistics to be mistakenly deleted when background tasks time out [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that executing `ADD UNIQUE INDEX` might cause data inconsistency [#60339](https://github.com/pingcap/tidb/issues/60339) @[tangenta](https://github.com/tangenta)
    - Fix the issue that non-public indexes are shown in the statistics system table [#60430](https://github.com/pingcap/tidb/issues/60430) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the `Close()` method of the Hash Join v1 operator fails to recover from a panic [#60926](https://github.com/pingcap/tidb/issues/60926) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that shallow copy of `PhysicalExchangeSender.HashCol` causes TiFlash to crash or generate incorrect results [#60517](https://github.com/pingcap/tidb/issues/60517) @[windtalker](https://github.com/windtalker)
    - Fix the issue that statistics for tables of the `BIT` type cannot be loaded [#62289](https://github.com/pingcap/tidb/issues/62289) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that statistics for `BIT` type columns fail to be loaded into memory [#59759](https://github.com/pingcap/tidb/issues/59759) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that when the disk-spilling operation of an `ANALYZE` statement takes too long in extreme cases, other TiDB nodes might fail to update the latest statistics [#54552](https://github.com/pingcap/tidb/issues/54552) @[0xPoe](https://github.com/0xPoe)
    - Fix the issue that when the collected column statistics are all in TopN, the row count estimation might remain 0 even after subsequent writes [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - Fix the issue that the estimated cost displayed in `explain format="cost_trace"` might be incorrect [#61155](https://github.com/pingcap/tidb/issues/61155) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the cost formulas displayed in `explain format="cost_trace"` might contain empty parentheses [#61127](https://github.com/pingcap/tidb/issues/61127) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that circular foreign key definitions cause infinite loops [#60985](https://github.com/pingcap/tidb/issues/60985) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that internal queries might fail to construct index range queries properly when using `NULL` [#62196](https://github.com/pingcap/tidb/issues/62196) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that Plan Cache stores an incorrect execution plan, causing execution errors [#56772](https://github.com/pingcap/tidb/issues/56772) @[dash12653](https://github.com/dash12653)
    - Fix the issue that row count estimates across months or years can be significantly overestimated [#50080](https://github.com/pingcap/tidb/issues/50080) @[terry1purcell](https://github.com/terry1purcell)
    - Fix the issue that the concurrency of `ANALYZE` subtasks greatly exceeds the configured limit [#61785](https://github.com/pingcap/tidb/issues/61785) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that an expression-based TopN sort item is incorrectly generated during TopN pushdown [#60655](https://github.com/pingcap/tidb/issues/60655) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that TiDB might print panic logs in the background when column or index statistics are missing [#61733](https://github.com/pingcap/tidb/issues/61733) @[winoros](https://github.com/winoros)
    - Fix the issue that row count estimation for `JOIN` can be highly inaccurate when column or index statistics are missing [#61602](https://github.com/pingcap/tidb/issues/61602) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the default value of the system variable `tidb_cost_model_version` is set incorrectly [#61565](https://github.com/pingcap/tidb/issues/61565) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that statistics might be incorrect when the first column of a table is a virtual generated column [#61606](https://github.com/pingcap/tidb/issues/61606) @[winoros](https://github.com/winoros)
    - Fix the issue that Plan Cache is incorrectly skipped with predicate simplification [#61513](https://github.com/pingcap/tidb/issues/61513) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that executing `ADMIN CANCEL DDL JOBS` while adding an index causes the index-adding process to hang [#61087](https://github.com/pingcap/tidb/issues/61087) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `ADMIN CHECK` still returns success even after some internal SQL executions fail [#61612](https://github.com/pingcap/tidb/issues/61612) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that data and indexes became inconsistent after adding multiple indexes through multi-schema change [#61255](https://github.com/pingcap/tidb/issues/61255) @[tangenta](https://github.com/tangenta)

+ TiKV

    - Fix the issue that a deadlock might be triggered during CPU profiling [#18474](https://github.com/tikv/tikv/issues/18474) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that Online Unsafe Recovery might be blocked by certain TiFlash replicas, preventing the commit index from advancing [#18197](https://github.com/tikv/tikv/issues/18197) @[v01dstar](https://github.com/v01dstar)
    - Fix the issue that TiKV might use a compression algorithm that the client cannot decode [#18079](https://github.com/tikv/tikv/issues/18079) @[ekexium](https://github.com/ekexium)
    - Fix the issue that TiKV allows excessive SST ingest requests under high concurrency [#18452](https://github.com/tikv/tikv/issues/18452) @[hbisheng](https://github.com/hbisheng)
    - Fix the issue that `Ingestion picked level` and `Compaction Job Size(files)` are displayed incorrectly in the TiKV dashboard in Grafana [#15990](https://github.com/tikv/tikv/issues/15990) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that the unexpected `Server is busy` error occurs after TiKV restarts [#18233](https://github.com/tikv/tikv/issues/18233) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - Fix misleading descriptions in `StoreMsg` log entries in slow logs [#18561](https://github.com/tikv/tikv/issues/18561) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix incorrect thread memory metrics [#18125](https://github.com/tikv/tikv/issues/18125) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that TiKV fails to terminate ongoing manual compaction tasks during graceful shutdown [#18396](https://github.com/tikv/tikv/issues/18396) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - Fix the issue that the `split-merge-interval` configuration item might not take effect when you modify its value repeatedly (such as changing it from `1s` to `1h` and back to `1s`) [#8404](https://github.com/tikv/pd/issues/8404) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that the default value of `lease` is not correctly set [#9156](https://github.com/tikv/pd/issues/9156) @[rleungx](https://github.com/rleungx)
    - Fix the issue that improperly closing TiDB Dashboard TCP connections could lead to PD goroutine leaks [#9402](https://github.com/tikv/pd/issues/9402) @[baurine](https://github.com/baurine)
    - Fix the issue that newly added TiKV nodes might fail to be scheduled [#9145](https://github.com/tikv/pd/issues/9145) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that enabling `tidb_enable_tso_follower_proxy` might cause the TSO service to become unavailable [#9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)

+ TiFlash

    - Fix the panic issue caused by accidental deletion of SST files during running `IMPORT INTO` or `BR restore` [#10141](https://github.com/pingcap/tiflash/issues/10141) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that creating an expression index in the form of `((NULL))` causes TiFlash to panic [#9891](https://github.com/pingcap/tiflash/issues/9891) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might panic when handling snapshots with irregular Region key-ranges [#10147](https://github.com/pingcap/tiflash/issues/10147) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might consume a large amount of memory when tables in a cluster contain a large number of `ENUM` type columns [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might fail to restart after inserting a single row of data larger than 16 MiB [#10052](https://github.com/pingcap/tiflash/issues/10052) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that missing resource control low token signals lead to query throttling [#10137](https://github.com/pingcap/tiflash/issues/10137) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiFlash might return the `Exception: Block schema mismatch` error when executing SQL statements containing `GROUP BY ... WITH ROLLUP` [#10110](https://github.com/pingcap/tiflash/issues/10110) @[gengliqi](https://github.com/gengliqi)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that PITR fails to restore indexes larger than 3072 bytes [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that log backup uploads to Azure Blob Storage are slow when transferring large volumes of data [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that BR does not check whether the corresponding table exists in the cluster when filtering tables with `-f` [#61592](https://github.com/pingcap/tidb/issues/61592) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - Fix the issue that the changefeed might get stuck when using external storage as the downstream [#9162](https://github.com/pingcap/tiflow/issues/9162) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the changefeed might get stuck after the replication traffic exceeds the traffic threshold of the downstream Kafka [#12110](https://github.com/pingcap/tiflow/issues/12110) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that using the `--overwrite-checkpoint-ts` parameter in the `changefeed pause` command might cause the changefeed to be stuck [#12055](https://github.com/pingcap/tiflow/issues/12055) @[hongyunyan](https://github.com/hongyunyan)
        - Fix the issue that evaluating event filter expressions on tables containing virtual columns might cause a panic [#12206](https://github.com/pingcap/tiflow/issues/12206) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue of case-sensitive matching for column and index names in the dispatcher configuration [#12103](https://github.com/pingcap/tiflow/issues/12103) @[wk989898](https://github.com/wk989898)
        - Fix the issue that the resolved ts lag keeps increasing after scaling in or out TiKV nodes on the same IP address because of outdated store IDs [#12162](https://github.com/pingcap/tiflow/issues/12162) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning can get stuck for several hours when importing Parquet files from cloud storage into TiDB [#60224](https://github.com/pingcap/tidb/issues/60224) @[joechenrh](https://github.com/joechenrh)
        - Fix the issue that TiDB Lightning returns the `context deadline exceeded` error when the RPC request to TiKV times out [#61326](https://github.com/pingcap/tidb/issues/61326) @[OliverS929](https://github.com/OliverS929)

    + NG Monitoring

        - Fix the issue that TSDB consumes too much memory under high cardinality of time series data, and provide a memory configuration option for TSDB [#295](https://github.com/pingcap/ng-monitoring/issues/295) @[mornyx](https://github.com/mornyx)
