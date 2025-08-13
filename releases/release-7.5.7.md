---
title: TiDB 7.5.7 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.5.7.
---

# TiDB 7.5.7 Release Notes

Release date: xx xx, 2025

TiDB version: 7.5.7

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## Compatibility changes

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## Improvements

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > Improvements> TiDB - Add flow control interfaces for Region splitting and data ingestion during data import [#61553](https://github.com/pingcap/tidb/issues/61553) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.2.0.md > Improvements> TiDB - Optimize the performance of obtaining data distribution information when performing simple queries on tables with large data volumes [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)
    - (dup): release-8.5.3.md > Improvements> TiDB - Add a monitoring metric to observe the write speed to TiKV during index addition [#60925](https://github.com/pingcap/tidb/issues/60925) @[CbcWestwolf](https://github.com/CbcWestwolf)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > Improvements> TiKV - Optimize the handling of `CompactedEvent` in Raftstore by moving it to the `split-check` worker, reducing blocking on the main Raftstore thread [#18532](https://github.com/tikv/tikv/issues/18532) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.1.0.md > Improvements> TiKV - Add metrics for memory usage per thread [#15927](https://github.com/tikv/tikv/issues/15927) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-8.5.3.md > Improvements> TiKV - Log only `SST ingest is experiencing slowdowns` when SST ingest is too slow, and skip calling `get_sst_key_ranges` to avoid performance jitter [#18549](https://github.com/tikv/tikv/issues/18549) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.1.6.md > Improvements> TiKV - Optimize the jittery access delay when restarting TiKV due to waiting for the log to be applied, improving the stability of TiKV [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > Improvements> TiKV - Optimize the cleanup mechanism of residual data to mitigate the impact on request latency [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > Bug fixes> TiKV - Fix the issue that TiKV fails to terminate ongoing manual compaction tasks during graceful shutdown [#18396](https://github.com/tikv/tikv/issues/18396) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > Improvements> TiKV - Optimize the performance of `fetch_entries_to` in Raft Engine to reduce contention and improve performance under mixed workloads [#18605](https://github.com/tikv/tikv/issues/18605) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.4.0.md > Improvements> TiKV - Support dynamically modifying flow-control configurations for write operations [#17395](https://github.com/tikv/tikv/issues/17395) @[glorv](https://github.com/glorv)
    - (dup): release-8.5.3.md > Improvements> TiKV - Support ingesting SST files without blocking foreground writes, reducing the impact of latency [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - (dup): release-8.5.3.md > Improvements> TiKV - Support ingesting SST files without blocking foreground writes, reducing the impact of latency [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - (dup): release-8.5.3.md > Improvements> TiKV - Optimize the detection mechanism for I/O jitter on KvDB disks when KvDB and RaftDB use separate mount paths [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-6.5.9.md > Improvements> TiKV - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ PD

    - Add more metrics for Golang Runtime, details can be seen at the runtime panel [#8931](https://github.com/tikv/pd/issues/8931) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > Improvements> TiFlash - Enhance the observability for TiFlash OOM risks in wide table scenarios [#10272](https://github.com/pingcap/tiflash/issues/10272) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.3.md > Improvements> TiFlash - Increase the maximum retry count when acquiring storage snapshots to improve query stability for large tables [#10300](https://github.com/pingcap/tiflash/issues/10300) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.1.0.md > Improvements> TiFlash - Mitigate the issue that TiFlash might panic due to updating certificates after TLS is enabled [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.3.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that BR does not check whether the corresponding table exists in the cluster when filtering tables with `-f` [#61592](https://github.com/pingcap/tidb/issues/61592) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-8.5.3.md > Improvements> Tools> Backup & Restore (BR) - The Download API of TiKV supports filtering out data within a certain time range when downloading backup files, which avoids importing outdated or future data versions during restore [#18399](https://github.com/tikv/tikv/issues/18399) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.3.md > Bug fixes> Tools> TiCDC - Fix the issue that evaluating event filter expressions on tables containing virtual columns might cause a panic [#12206](https://github.com/pingcap/tiflow/issues/12206) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-8.5.3.md > Bug fixes> Tools> TiCDC - Fix the issue of case-sensitive matching for column and index names in the dispatcher configuration [#12103](https://github.com/pingcap/tiflow/issues/12103) @[wk989898](https://github.com/wk989898)
        - (dup): release-8.5.3.md > Bug fixes> Tools> TiCDC - Fix the issue that the resolved ts lag keeps increasing after scaling in or out TiKV nodes on the same IP address because of outdated store IDs [#12162](https://github.com/pingcap/tiflow/issues/12162) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## Bug fixes

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > Bug fixes> TiDB - Fix the issue that shared KV requests in `IndexMerge` and `IndexLookUp` operators cause data races when pushing down queries [#60175](https://github.com/pingcap/tidb/issues/60175) @[you06](https://github.com/you06)
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix a potential goroutine leak issue in the Hash Aggregation operator [#58004](https://github.com/pingcap/tidb/issues/58004) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that MPP plans might not be selected when indexes on generated columns are set as visible [#47766](https://github.com/pingcap/tidb/issues/47766) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-8.5.3.md > Bug fixes> TiDB - Fix the issue that SQL statements containing `_charset(xxx), _charset(xxx2), ...` generate different digests [#58447](https://github.com/pingcap/tidb/issues/58447) @[xhebox](https://github.com/xhebox)
    - (dup): release-8.5.3.md > Bug fixes> TiDB - Fix the issue that frequent Region merges prevent TTL jobs from starting [#61512](https://github.com/pingcap/tidb/issues/61512) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-8.5.3.md > Bug fixes> TiDB - Fix the issue that TiFlash query results are inconsistent after executing a lossy DDL statement [#61455](https://github.com/pingcap/tidb/issues/61455) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-8.5.3.md > Bug fixes> TiDB - Fix the issue of incorrect key range in `ALTER RANGE meta SET PLACEMENT POLICY` [#60888](https://github.com/pingcap/tidb/issues/60888) @[nolouch](https://github.com/nolouch)
    - (dup): release-8.5.2.md > Bug fixes> TiDB - Fix the issue that the data in the **Stats Healthy Distribution** panel of Grafana might be incorrect [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.5.3.md > Bug fixes> TiDB - Fix the issue that the comparison behavior of `latin1_bin` differs from that of `utf8mb4_bin` and `utf8_bin` [#60701](https://github.com/pingcap/tidb/issues/60701) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.5.3.md > Bug fixes> TiDB - Fix the issue that after disabling metadata locking (MDL), DDL operations get stuck after failing to update the schema version [#61210](https://github.com/pingcap/tidb/issues/61210) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-8.5.2.md > Bug fixes> TiDB - Fix the issue that enabling Redact log does not take effect in certain scenarios [#59279](https://github.com/pingcap/tidb/issues/59279) @[tangenta](https://github.com/tangenta)
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix the issue that a TiDB session might crash when Fix Control #44855 is enabled [#59762](https://github.com/pingcap/tidb/issues/59762) @[winoros](https://github.com/winoros)
    - (dup): release-8.5.3.md > Improvements> TiDB - Remove redundant log entries when the `IndexLookup` operator encounters a `context canceled` error [#61072](https://github.com/pingcap/tidb/issues/61072) @[yibin87](https://github.com/yibin87)
    - (dup): release-8.5.2.md > Bug fixes> TiDB - Fix the issue that improper exception handling for statistics causes in-memory statistics to be mistakenly deleted when background tasks time out [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.5.2.md > Bug fixes> TiDB - Fix the issue that executing `ADD UNIQUE INDEX` might cause data inconsistency [#60339](https://github.com/pingcap/tidb/issues/60339) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.5.3.md > Bug fixes> TiDB - Fix the issue that non-public indexes are shown in the statistics system table [#60430](https://github.com/pingcap/tidb/issues/60430) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.5.3.md > Bug fixes> TiDB - Fix the issue that the HashJoin operator causes Goroutine leaks due to memory overuse [#60926](https://github.com/pingcap/tidb/issues/60926) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > Bug fixes> TiKV - Fix the issue that TiKV might use a compression algorithm that the client cannot decode [#18079](https://github.com/tikv/tikv/issues/18079) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.5.3.md > Bug fixes> TiKV - Fix the issue that TiKV allows excessive SST ingest requests under high concurrency [#18452](https://github.com/tikv/tikv/issues/18452) @[hbisheng](https://github.com/hbisheng)
    - (dup): release-8.3.0.md > Bug fixes> TiKV - Fix the issue that `Ingestion picked level` and `Compaction Job Size(files)` are displayed incorrectly in the TiKV dashboard in Grafana [#15990](https://github.com/tikv/tikv/issues/15990) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-9.0.0.md > Bug fixes> TiKV - Fix the issue that the unexpected `Server is busy` error occurs after TiKV restarts [#18233](https://github.com/tikv/tikv/issues/18233) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-6.5.9.md > Bug fixes> TiKV - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - (dup): release-8.5.3.md > Bug fixes> TiKV - Fix misleading descriptions in `StoreMsg` log entries in slow logs [#18561](https://github.com/tikv/tikv/issues/18561) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-9.0.0.md > Bug fixes> TiKV - Fix incorrect thread memory metrics [#18125](https://github.com/tikv/tikv/issues/18125) @[Connor1996](https://github.com/Connor1996)

+ PD

    
    - Fix the issue that the default value of `lease` is not correctly set [#9156](https://github.com/tikv/pd/issues/9156) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the `split-merge-interval` configuration item might not take effect when you modify its value repeatedly (such as changing it from `1s` to `1h` and back to `1s`) [#8404](https://github.com/tikv/pd/issues/8404) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that pd goroutine leak due to the dashboard connections don't close well [#9402](https://github.com/tikv/pd/issues/9402) @[baurine](https://github.com/baurine)
    - Fix the issue that the new store cna't be balanced [#9145](https://github.com/tikv/pd/issues/9145) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that client can't get any tso after enabled the variable `tidb_enable_tso_follower_proxy`[#9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - Fix the panic issue caused by accidental deletion of SST files during running `IMPORT INTO` or `BR restore` [#10141](https://github.com/pingcap/tiflash/issues/10141) @[CalvinNeo](https://github.com/CalvinNeo)
    - (dup): release-8.5.3.md > Bug fixes> TiFlash - Fix the issue that creating an expression index in the form of `((NULL))` causes TiFlash to panic [#9891](https://github.com/pingcap/tiflash/issues/9891) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might panic when handling snapshots with irregular Region key-ranges [#10147](https://github.com/pingcap/tiflash/issues/10147) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might consume a large amount of memory when tables in a cluster contain a large number of `ENUM` type columns [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might fail to restart after inserting a single row of data larger than 16 MiB [#10052](https://github.com/pingcap/tiflash/issues/10052) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.3.md > Bug fixes> TiFlash - Fix the issue that missing resource control low token signals lead to query throttling [#10137](https://github.com/pingcap/tiflash/issues/10137) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might return the `Exception: Block schema mismatch` error when executing SQL statements containing `GROUP BY ... WITH ROLLUP` [#10110](https://github.com/pingcap/tiflash/issues/10110) @[gengliqi](https://github.com/gengliqi)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.2.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that PITR fails to restore indexes larger than 3072 bytes [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.5.3.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that log backup uploads to Azure Blob Storage are slow when transferring large volumes of data [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix a bug that may cause changefeed with storage sink getting stuck [#9162](https://github.com/pingcap/tiflow/issues/9162) @[asddongmen](https://github.com/asddongmen)
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.2.md > Bug fixes> Tools> TiCDC - Fix the issue that the changefeed might get stuck after the replication traffic exceeds the traffic threshold of the downstream Kafka [#12110](https://github.com/pingcap/tiflow/issues/12110) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.2.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that TiDB Lightning can get stuck for several hours when importing Parquet files from cloud storage into TiDB [#60224](https://github.com/pingcap/tidb/issues/60224) @[joechenrh](https://github.com/joechenrh)
        - (dup): release-8.5.3.md > 错误修复> Tools> TiDB Lightning - 修复 lightning 向 TiKV 发起的 RPC 请求超时后返回 context deadline 的问题 [#61326](https://github.com/pingcap/tidb/issues/61326) @[OliverS929](https://github.com/OliverS929)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + NG Monitoring

        - (dup): release-8.5.2.md > Bug fixes> Tools> NG Monitoring - Fix the issue that TSDB consumes too much memory under high cardinality of time series data, and provide a memory configuration option for TSDB [#295](https://github.com/pingcap/ng-monitoring/issues/295) @[mornyx](https://github.com/mornyx)
