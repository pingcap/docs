---
title: TiDB 8.5.3 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 8.5.3.
---

# TiDB 8.5.3 Release Notes

Release date: August 14, 2025

TiDB version: 8.5.3

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## Compatibility changes

- Add the following system variables for internal use by the [Cost Model](/cost-model.md). It is **NOT** recommended to modify these variables: [`tidb_opt_hash_agg_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_hash_agg_cost_factor-new-in-v853-and-v900), [`tidb_opt_hash_join_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_hash_join_cost_factor-new-in-v853-and-v900), [`tidb_opt_index_join_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_join_cost_factor-new-in-v853-and-v900), [`tidb_opt_index_lookup_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_lookup_cost_factor-new-in-v853-and-v900), [`tidb_opt_index_merge_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_merge_cost_factor-new-in-v853-and-v900), [`tidb_opt_index_reader_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_reader_cost_factor-new-in-v853-and-v900), [`tidb_opt_index_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_scan_cost_factor-new-in-v853-and-v900), [`tidb_opt_limit_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_limit_cost_factor-new-in-v853-and-v900), [`tidb_opt_merge_join_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_merge_join_cost_factor-new-in-v853-and-v900), [`tidb_opt_sort_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_sort_cost_factor-new-in-v853-and-v900), [`tidb_opt_stream_agg_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_stream_agg_cost_factor-new-in-v853-and-v900), [`tidb_opt_table_full_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_full_scan_cost_factor-new-in-v853-and-v900), [`tidb_opt_table_range_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_range_scan_cost_factor-new-in-v853-and-v900), [`tidb_opt_table_reader_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_reader_cost_factor-new-in-v853-and-v900), [`tidb_opt_table_rowid_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_rowid_cost_factor-new-in-v853-and-v900), [`tidb_opt_table_tiflash_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_tiflash_scan_cost_factor-new-in-v853-and-v900), and [`tidb_opt_topn_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_topn_cost_factor-new-in-v853-and-v900) [#60357](https://github.com/pingcap/tidb/issues/60357) @[terry1purcell](https://github.com/terry1purcell)
- Reintroduce the [telemetry](https://docs.pingcap.com/tidb/v8.5/telemetry) feature. However, it only logs telemetry-related information locally and no longer sends data to PingCAP over the network [#61766](https://github.com/pingcap/tidb/issues/61766) @[Defined2014](https://github.com/Defined2014)

## Improvements

+ TiDB

    - Adjust estimation results from 0 to 1 for equality conditions that do not hit TopN when statistics are entirely composed of TopN and the modified row count in the corresponding table statistics is non-zero [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - Improve the performance of adding unique indexes using global sort, and refine the error message when adding duplicate unique indexes [#61689](https://github.com/pingcap/tidb/issues/61689) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Disable TiKV switching to import mode when `IMPORT INTO` enables global sort [#60361](https://github.com/pingcap/tidb/issues/60361) @[D3Hunter](https://github.com/D3Hunter)
    - Add a monitoring metric to observe the write speed to TiKV during index addition [#60925](https://github.com/pingcap/tidb/issues/60925) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Optimize the scheduling logic of `merge sort` sub-tasks to improve sorting performance [#60375](https://github.com/pingcap/tidb/issues/60375) @[tangenta](https://github.com/tangenta)
    - Accelerate table creation when creating a large number of tables with foreign keys, and optimize memory usage efficiency [#61126](https://github.com/pingcap/tidb/issues/61126) @[GMHDBJD](https://github.com/GMHDBJD)
    - Improve the read performance of the `information_schema.tables` table [#62020](https://github.com/pingcap/tidb/issues/62020) @[tangenta](https://github.com/tangenta)
    - Add flow control interfaces for Region splitting and data ingestion during data import [#61553](https://github.com/pingcap/tidb/issues/61553) @[tangenta](https://github.com/tangenta)
    - Optimize the plan construction process for IndexScan by reducing `fmt.Sprintf()` calls [#56649](https://github.com/pingcap/tidb/issues/56649) @[crazycs520](https://github.com/crazycs520)
    - Add monitoring metrics for the merge sort stage when using Global Sort with indexes [#61025](https://github.com/pingcap/tidb/issues/61025) @[fzzf678](https://github.com/fzzf678)
    - Remove redundant log entries when the `IndexLookup` operator encounters a `context canceled` error [#61072](https://github.com/pingcap/tidb/issues/61072) @[yibin87](https://github.com/yibin87)
    - Improve the performance when `tidb_replica_read` is set to `closest-adaptive` [#61745](https://github.com/pingcap/tidb/issues/61745) @[you06](https://github.com/you06)
    - Reduce operational costs by decreasing the amount of monitoring metrics data in large-scale clusters [#59990](https://github.com/pingcap/tidb/issues/59990) @[zimulala](https://github.com/zimulala)

+ TiKV

    - Support ingesting SST files without blocking foreground writes, reducing the impact of latency [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - Reduce performance jitter caused by the flow controller [#18625](https://github.com/tikv/tikv/issues/18625) @[hhwyt](https://github.com/hhwyt)
    - Optimize tail latency during `ADD INDEX` operations in TiDB [#18081](https://github.com/tikv/tikv/issues/18081) @[overvenus](https://github.com/overvenus)
    - Optimize the handling of `CompactedEvent` in Raftstore by moving it to the `split-check` worker, reducing blocking on the main Raftstore thread [#18532](https://github.com/tikv/tikv/issues/18532) @[LykxSassinator](https://github.com/LykxSassinator)
    - Log only `SST ingest is experiencing slowdowns` when SST ingest is too slow, and skip calling `get_sst_key_ranges` to avoid performance jitter [#18549](https://github.com/tikv/tikv/issues/18549) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize the detection mechanism for I/O jitter on KvDB disks when KvDB and RaftDB use separate mount paths [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize the performance of `fetch_entries_to` in Raft Engine to reduce contention and improve performance under mixed workloads [#18605](https://github.com/tikv/tikv/issues/18605) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize the cleanup mechanism of residual data to mitigate the impact on request latency [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - Add GO runtime-related monitoring metrics in Prometheus [#8931](https://github.com/tikv/pd/issues/8931) @[bufferflies](https://github.com/bufferflies)
    - Extend the recovery time after triggering slow node leader eviction from 600 seconds to 900 seconds (15 minutes) [#9329](https://github.com/tikv/pd/issues/9329) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - Increase the maximum retry count when acquiring storage snapshots to improve query stability for large tables [#10300](https://github.com/pingcap/tiflash/issues/10300) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Enhance the observability for TiFlash OOM risks in wide table scenarios [#10272](https://github.com/pingcap/tiflash/issues/10272) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Improve the index restore speed during PITR by repairing indexes concurrently [#59158](https://github.com/pingcap/tidb/issues/59158) @[Leavrth](https://github.com/Leavrth)
        - The Download API of TiKV supports filtering out data within a certain time range when downloading backup files, which avoids importing outdated or future data versions during restore [#18399](https://github.com/tikv/tikv/issues/18399) @[3pointer](https://github.com/3pointer)
        - Support filtering log backup metadata files by timestamp to reduce the time spent on reading metadata during PITR [#61318](https://github.com/pingcap/tidb/issues/61318) @[3pointer](https://github.com/3pointer)

## Bug fixes

+ TiDB

    - Fix the issue of incorrect key range in `ALTER RANGE meta SET PLACEMENT POLICY` [#60888](https://github.com/pingcap/tidb/issues/60888) @[nolouch](https://github.com/nolouch)
    - Fix the issue that decreasing the number of workers during index creation might cause the task to hang [#59267](https://github.com/pingcap/tidb/issues/59267) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that the `ADMIN SHOW DDL JOBS` statement does not display the row count correctly [#59897](https://github.com/pingcap/tidb/issues/59897) @[tangenta](https://github.com/tangenta)
    - Fix the issue that data race might occur when dynamically adjusting the number of workers during index creation [#59016](https://github.com/pingcap/tidb/issues/59016) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that the data in the **Stats Healthy Distribution** panel of Grafana might be incorrect [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that an error might occur when using `IMPORT INTO ... FROM SELECT` to import data into TiFlash [#58443](https://github.com/pingcap/tidb/issues/58443) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that enabling `tidb_enable_dist_task` causes TiDB upgrade to fail [#54061](https://github.com/pingcap/tidb/issues/54061) @[tangenta](https://github.com/tangenta)
    - Fix the issue that improper exception handling for statistics causes in-memory statistics to be mistakenly deleted when background tasks time out [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the row count is not updated correctly when adding indexes in the TiDB Distributed eXecution Framework (DXF) [#58573](https://github.com/pingcap/tidb/issues/58573) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that TiFlash query results are inconsistent after executing a lossy DDL statement [#61455](https://github.com/pingcap/tidb/issues/61455) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiDB fails to retry when encountering EOF errors with GCS [#59754](https://github.com/pingcap/tidb/issues/59754) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue of invalid KV ranges when using Global Sort [#59841](https://github.com/pingcap/tidb/issues/59841) @[GMHDBJD](https://github.com/GMHDBJD)
    - Fix the issue that an empty index name is generated when executing the `CREATE INDEX IF NOT EXISTS` statement [#61265](https://github.com/pingcap/tidb/issues/61265) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that after disabling metadata locking (MDL), DDL operations get stuck after failing to update the schema version [#61210](https://github.com/pingcap/tidb/issues/61210) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that non-public indexes are shown in the statistics system table [#60430](https://github.com/pingcap/tidb/issues/60430) @[tangenta](https://github.com/tangenta)
    - Fix the issue that incorrect memory tracking in the HashAgg operator causes a large number of error logs [#58822](https://github.com/pingcap/tidb/issues/58822) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that a `nil` buffer in `basePartialResult4GroupConcat` causes a panic during disk spilling in the HashAgg operator [#61749](https://github.com/pingcap/tidb/issues/61749) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that incorrect return values in the encoding logic of aggregate expressions cause a panic during query execution [#61735](https://github.com/pingcap/tidb/issues/61735) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the HashJoin operator causes Goroutine leaks due to memory overuse [#60926](https://github.com/pingcap/tidb/issues/60926) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that shared KV requests in `IndexMerge` and `IndexLookUp` operators cause data races when pushing down queries [#60175](https://github.com/pingcap/tidb/issues/60175) @[you06](https://github.com/you06)
    - Fix the issue that SQL statements containing `_charset(xxx), _charset(xxx2), ...` generate different digests [#58447](https://github.com/pingcap/tidb/issues/58447) @[xhebox](https://github.com/xhebox)
    - Fix the issue that TiDB might panic when handling invalid UTF-8 characters [#47521](https://github.com/pingcap/tidb/issues/47521) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that inserting an invalid daylight saving time (DST) timestamp results in `0000-00-00` [#61334](https://github.com/pingcap/tidb/issues/61334) @[mjonss](https://github.com/mjonss)
    - Fix the issue that using `INSERT IGNORE` to insert an invalid daylight saving time timestamp in strict SQL mode results in a timestamp inconsistent with MySQL [#61439](https://github.com/pingcap/tidb/issues/61439) @[mjonss](https://github.com/mjonss)
    - Fix the issue that frequent Region merges prevent TTL jobs from starting [#61512](https://github.com/pingcap/tidb/issues/61512) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the column length returned by TiDB in the network protocol might be `0`. If it is `0`, TiDB returns the default length of each field type [#60503](https://github.com/pingcap/tidb/issues/60503) @[xhebox](https://github.com/xhebox)
    - Fix the issue that the returned type of `blob` in the network protocol is inconsistent with MySQL [#60195](https://github.com/pingcap/tidb/issues/60195) @[dveeden](https://github.com/dveeden)
    - Fix the issue that the length returned by `CAST()` is incompatible with MySQL [#61350](https://github.com/pingcap/tidb/issues/61350) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the comparison behavior of `latin1_bin` differs from that of `utf8mb4_bin` and `utf8_bin` [#60701](https://github.com/pingcap/tidb/issues/60701) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that pessimistic locks might remain when a query is terminated [#61454](https://github.com/pingcap/tidb/issues/61454) @[zyguan](https://github.com/zyguan)
    - Fix the issue that an error occurs when TiDB executes large queries due to loading too many Regions from PD in a single request [#1704](https://github.com/tikv/client-go/issues/1704) @[you06](https://github.com/you06)

+ TiKV

    - Fix the issue that TiKV fails to terminate ongoing manual compaction tasks during graceful shutdown [#18396](https://github.com/tikv/tikv/issues/18396) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that the default Region size is unexpectedly changed after a cluster upgrade [#18503](https://github.com/tikv/tikv/issues/18503) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that TiKV might use a compression algorithm that the client cannot decode [#18079](https://github.com/tikv/tikv/issues/18079) @[ekexium](https://github.com/ekexium)
    - Fix the issue that blob indexes might cause apply snapshot failures after Titan is disabled [#18434](https://github.com/tikv/tikv/issues/18434) @[v01dstar](https://github.com/v01dstar)
    - Fix misleading descriptions in `StoreMsg` log entries in slow logs [#18561](https://github.com/tikv/tikv/issues/18561) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that TiKV allows excessive SST ingest requests under high concurrency [#18452](https://github.com/tikv/tikv/issues/18452) @[hbisheng](https://github.com/hbisheng)
    - Fix the issue that TiKV might panic due to duplicate results during lock scanning [#16818](https://github.com/tikv/tikv/issues/16818) @[cfzjywxk](https://github.com/cfzjywxk)

+ PD

    - Fix the issue that `recovery-duration` does not take effect in the slow node detection mechanism [#9384](https://github.com/tikv/pd/issues/9384) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the Evict Leader scheduler might be incorrectly paused after a cluster upgrade [#9416](https://github.com/tikv/pd/issues/9416) @[rleungx](https://github.com/rleungx)
    - Fix the issue that improperly closing TiDB Dashboard TCP connections could lead to PD goroutine leaks [#9402](https://github.com/tikv/pd/issues/9402) @[baurine](https://github.com/baurine)
    - Fix the issue that newly added TiKV nodes might fail to be scheduled [#9145](https://github.com/tikv/pd/issues/9145) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - Fix the issue that creating an expression index in the form of `((NULL))` causes TiFlash to panic [#9891](https://github.com/pingcap/tiflash/issues/9891) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that misaligned mutex in the Join operator causes TiFlash to crash in certain environments [#10163](https://github.com/pingcap/tiflash/issues/10163) @[windtalker](https://github.com/windtalker)
    - Fix the issue that missing resource control low token signals lead to query throttling [#10137](https://github.com/pingcap/tiflash/issues/10137) @[guo-shaoge](https://github.com/guo-shaoge)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that available space on storage nodes is unnecessarily rechecked during breakpoint recovery [#54316](https://github.com/pingcap/tidb/issues/54316) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that data imports from external storage do not automatically retry when the HTTP/2 GOAWAY error occurs [#60143](https://github.com/pingcap/tidb/issues/60143) @[joechenrh](https://github.com/joechenrh)
        - Fix the `keepalive watchdog timedout` error that occurs during restore due to import mode switching [#18541](https://github.com/tikv/tikv/issues/18541) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that log backup uploads to Azure Blob Storage are slow when transferring large volumes of data [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that BR does not check whether the corresponding table exists in the cluster when filtering tables with `-f` [#61592](https://github.com/pingcap/tidb/issues/61592) @[RidRisR](https://github.com/RidRisR)
        - Fix the issue that PITR fails to restore indexes larger than 3072 bytes [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that RangeTree results consume memory inefficiently during full backup [#58587](https://github.com/pingcap/tidb/issues/58587) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Fix the issue that evaluating event filter expressions on tables containing virtual columns might cause a panic [#12206](https://github.com/pingcap/tiflow/issues/12206) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that the resolved ts lag keeps increasing after scaling in or out TiKV nodes on the same IP address because of outdated store IDs [#12162](https://github.com/pingcap/tiflow/issues/12162) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue of case-sensitive matching for column and index names in the dispatcher configuration [#12103](https://github.com/pingcap/tiflow/issues/12103) @[wk989898](https://github.com/wk989898)
        - Fix the issue that configuring `column-selector` with the Debezium protocol might cause a panic [#12208](https://github.com/pingcap/tiflow/issues/12208) @[wk989898](https://github.com/wk989898)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning returns the `context deadline exceeded` error when the RPC request to TiKV times out [#60143](https://github.com/pingcap/tidb/issues/60143) @[joechenrh](https://github.com/joechenrh)
