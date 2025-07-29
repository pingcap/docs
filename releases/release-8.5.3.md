---
title: TiDB 8.5.3 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 8.5.3.
---

# TiDB 8.5.3 Release Notes

Release date: xx xx, 2025

TiDB version: 8.5.3

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## Compatibility changes

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

## Improvements

+ TiDB <!--tw@qiancai: 8 notes-->

    - (dup): release-7.5.5.md > Improvements> TiDB - Adjust estimation results from 0 to 1 for equality conditions that do not hit TopN when statistics are entirely composed of TopN and the modified row count in the corresponding table statistics is non-zero [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - Improve the performance of adding unique indexes using global sort, and refine the error message when adding duplicate unique indexes [#61689](https://github.com/pingcap/tidb/issues/61689) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Disable TiKV switching to import mode when `IMPORT INTO` enables global sort [#60361](https://github.com/pingcap/tidb/issues/60361) @[D3Hunter](https://github.com/D3Hunter)
    - Add a monitoring metric to observe the write speed to TiKV during index addition [#60925](https://github.com/pingcap/tidb/issues/60925) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Add a retry mechanism for EOF exceptions to improve data read stability [#59754](https://github.com/pingcap/tidb/issues/59754) @[lance6716](https://github.com/lance6716)
    - Optimize the scheduling logic of `merge sort` sub-tasks to improve sorting performance [#60375](https://github.com/pingcap/tidb/issues/60375) @[tangenta](https://github.com/tangenta)
    - Accelerate table creation when creating a large number of tables with foreign keys, and optimize memory usage efficiency [#61126](https://github.com/pingcap/tidb/issues/61126) @[GMHDBJD](https://github.com/GMHDBJD)
    - Improve the read performance of the `information_schema.tables` table [#62020](https://github.com/pingcap/tidb/issues/62020) @[tangenta](https://github.com/tangenta)
    - Add flow control interfaces for Region splitting and data ingestion during data import [#61553](https://github.com/pingcap/tidb/issues/61553) @[tangenta](https://github.com/tangenta)
    - Optimize the plan construction process for IndexScan by reducing `fmt.Sprintf()` calls [#56649](https://github.com/pingcap/tidb/issues/56649) @[crazycs520](https://github.com/crazycs520)

+ TiKV

    - Support ingesting SST files without blocking foreground writes to reduce latency impact. [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - Reduce latency jitter caused by the flow controller. [#18625](https://github.com/tikv/tikv/issues/18625) @[hhwyt](https://github.com/hhwyt)
    - Optimize tail request latency during TiDB `ADD INDEX` operations. [#18081](https://github.com/tikv/tikv/issues/18081) @[overvenus](https://github.com/overvenus)
    - Stop in-progress manual compaction jobs during TiKV's graceful shutdown. [#18396](https://github.com/tikv/tikv/issues/18396) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize the handling of `CompactedEvent` in raftstore by moving it to the `split-check` worker. [#18532](https://github.com/tikv/tikv/issues/18532) @[LykxSassinator](https://github.com/LykxSassinator)
    - Remove the log entry "sst ingest is too slow" to avoid latency jitters. [#18549](https://github.com/tikv/tikv/issues/18549) @[LykxSassinator](https://github.com/LykxSassinator)
    - Improve the detection of I/O jitters on kvdb disk when deployed with separate mount paths. [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize `fetch_entries_to` in Raft-Engine to reduce contention and improve performance under mixed workloads. [#18605](https://github.com/tikv/tikv/issues/18605) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-9.0.0.md > Improvements> TiKV - Optimize the cleanup mechanism of residual data to mitigate the impact on request latency [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - Increase the maximum retry count when acquiring storage snapshots to improve query stability for large tables [#10300](https://github.com/pingcap/tiflash/issues/10300) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Enhance the observability for TiFlash OOM risk under wide-column scenario [#10272](https://github.com/pingcap/tiflash/issues/10272) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 3 notes-->

        - (dup): release-9.0.0.md > Improvements> Tools> Backup & Restore (BR) - Improve the index restore speed during PITR by repairing indexes concurrently [#59158](https://github.com/pingcap/tidb/issues/59158) @[Leavrth](https://github.com/Leavrth)
        - The Download API of TiKV supports filtering out data within a certain time range when downloading backup files, which avoids importing outdated or future data versions during restore [#18399](https://github.com/tikv/tikv/issues/18399) @[3pointer](https://github.com/3pointer)
        - Support filtering log backup metadata files by timestamp to reduce the time spent on reading metadata during PITR restore [#61318](https://github.com/pingcap/tidb/issues/61318) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Fix panic when evaluating event-filter expressions on tables with virtual columns. [#12206](https://github.com/pingcap/tiflow/issues/12206) @[lidezhu](https://github.com/lidezhu)
        - Fix the continuously increasing resolved_ts lag caused by stale store IDs after scaling in/out TiKV instances on the same IP address. [#12162](https://github.com/pingcap/tiflow/issues/12162) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix case sensitivity issue in dispatcher configuration's column/index name matching. [#12103](https://github.com/pingcap/tiflow/issues/12103) @[wk989898](https://github.com/wk989898)
        - Fix panic when configuring column-selector in Debezium protocol.[#12208](https://github.com/pingcap/tiflow/issues/12208) @[wk989898](https://github.com/wk989898)
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

## Bug fixes

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix the issue that decreasing the number of workers during index creation might cause the task to hang [#59267](https://github.com/pingcap/tidb/issues/59267) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix the issue that the `ADMIN SHOW DDL JOBS` statement does not display the row count correctly [#59897](https://github.com/pingcap/tidb/issues/59897) @[tangenta](https://github.com/tangenta)
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix the issue that data race might occur when dynamically adjusting the number of workers during index creation [#59016](https://github.com/pingcap/tidb/issues/59016) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-7.5.5.md > Bug fixes> TiDB - Fix the issue that the data in the **Stats Healthy Distribution** panel of Grafana might be incorrect [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix the issue that an error might occur when using `IMPORT INTO ... FROM SELECT` to import data into TiFlash [#58443](https://github.com/pingcap/tidb/issues/58443) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix the issue that enabling `tidb_enable_dist_task` causes TiDB upgrade to fail [#54061](https://github.com/pingcap/tidb/issues/54061) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.5.6.md > Bug fixes> TiDB - Fix the issue that improper exception handling for statistics causes in-memory statistics to be mistakenly deleted when background tasks time out [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix the issue that the row count is not updated correctly when adding indexes in the TiDB Distributed eXecution Framework (DXF) [#58573](https://github.com/pingcap/tidb/issues/58573) @[D3Hunter](https://github.com/D3Hunter)

+ TiKV

    - Ensure `region-size` configurations are inherited correctly to avoid unexpected changes to the default region size. [#18503](https://github.com/tikv/tikv/issues/18503) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that TiKV may use a compression algorithm that the client side cannot decode. [#18079](https://github.com/tikv/tikv/issues/18079) @[ekexium](https://github.com/ekexium)
    - Fix the issue that Titan blob indices caused snapshot apply failures after Titan is turned off. [#18434](https://github.com/tikv/tikv/issues/18434) @[v01dstar](https://github.com/v01dstar)
    - Fix incorrect and misleading index logging in StoreMsg of slowlog. [#18561](https://github.com/tikv/tikv/issues/18561) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix over-admission of SST ingest requests in highly concurrent scenarios. [#18452](https://github.com/tikv/tikv/issues/18452) @[hbisheng](https://github.com/hbisheng)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - Fix the issue that TiFlash panic when meets expression index with format `((NULL))` [#9891](https://github.com/pingcap/tiflash/issues/9891) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 5 notes-->

        - (dup): release-9.0.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that available space on storage nodes is unnecessarily rechecked during breakpoint recovery [#54316](https://github.com/pingcap/tidb/issues/54316) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that PITR cannot restore indexes larger than 3072 bytes [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that RangeTree structure consumes memory inefficiently during full backups of a large number of tables [#58587](https://github.com/pingcap/tidb/issues/58587) @[3pointer](https://github.com/3pointer)
        - Fix the issue that data imports from external storage do not automatically retry when the HTTP/2 GOAWAY error occurs [#60143](https://github.com/pingcap/tidb/issues/60143) @[joechenrh](https://github.com/joechenrh)
        - Fix the `keepalive watchdog timedout` error that occurs during restore due to import mode switching [#18541](https://github.com/tikv/tikv/issues/18541) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that log backup uploads to Azure Blob Storage are slow when transferring large volumes of data [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that BR does not check whether the corresponding table exists in the cluster when filtering tables with `-f` [#61592](https://github.com/pingcap/tidb/issues/61592) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-9.0.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that PITR fails to restore indexes larger than 3072 bytes [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-9.0.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that RangeTree results consume memory inefficiently during full backup [#58587](https://github.com/pingcap/tidb/issues/58587) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Lightning <!--tw@qiancai: 1 note-->

        - Fix the issue that TiDB Lightning returns the `context deadline exceeded` error when the RPC request to TiKV times out [#60143](https://github.com/pingcap/tidb/issues/60143) @[joechenrh](https://github.com/joechenrh)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
