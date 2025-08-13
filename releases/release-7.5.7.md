---
title: TiDB 7.5.7 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.5.7.
---

# TiDB 7.5.7 Release Notes

Release date: xx xx, 2025

TiDB version: 7.5.7

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## Compatibility changes

<!--tw@Oreoxmt: 1 notes-->

- 将系统变量 `tidb_enable_historical_stats` 的默认值从 `ON` 修改为 `OFF`，即默认关闭历史统计信息，避免潜在的稳定性问题 [#53048](https://github.com/pingcap/tidb/issues/53048) @[hawkingrei](https://github.com/hawkingrei)

## Improvements

+ TiDB <!--tw@Oreoxmt: 6 notes-->

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > Improvements> TiDB - Add flow control interfaces for Region splitting and data ingestion during data import [#61553](https://github.com/pingcap/tidb/issues/61553) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.2.0.md > Improvements> TiDB - Optimize the performance of obtaining data distribution information when performing simple queries on tables with large data volumes [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)
    - (dup): release-8.5.3.md > Improvements> TiDB - Add a monitoring metric to observe the write speed to TiKV during index addition [#60925](https://github.com/pingcap/tidb/issues/60925) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 优化了 DML 在 DDL 执行期间的加锁逻辑，减少了 DML 和 DDL 操作的锁冲突，提高了某些场景下 DDL 的性能。但是由于在此过程中也会引入额外的二级索引加锁操作，可能会造成 DML 性能轻微下降 [#62337](https://github.com/pingcap/tidb/issues/62337) @[lcwangchao](https://github.com/lcwangchao)
    - 调整 `tidb_opt_ordering_index_selectivity_threshold` 值为 1 时的行为，增强变量的控制能力 [#60242](https://github.com/pingcap/tidb/issues/60242) @[time-and-fate](https://github.com/time-and-fate)
    - 避免 ANALYZE 执行完成后需要刷新整个集群的统计信息，从而导致 ANALYZE 执行时间过长的情况 [#57631](https://github.com/pingcap/tidb/issues/57631) @[0xPoe](https://github.com/0xPoe)
    - 常量折叠可以将带有 NOT NULL 约束的列上进行的 IS NULL 计算折叠为 FALSE [#62050](https://github.com/pingcap/tidb/issues/62050) @[hawkingrei](https://github.com/hawkingrei)
    - 优化器支持更多 JOIN 的常量传播 [#51700](https://github.com/pingcap/tidb/issues/51700) @[hawkingrei](https://github.com/hawkingrei)
    - 优化在 DML 与 DDL 存在较多锁冲突时，合并 temp index 的性能 [#61433](https://github.com/pingcap/tidb/issues/61433) @[tangenta](https://github.com/tangenta)

+ TiKV <!--tw@Oreoxmt: 2 notes-->

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 优化 TiKV compaction 触发逻辑，按回收效率排序对所有数据段依序处理，降低 MVCC 冗余数据对性能的影响 [#18571](https://github.com/tikv/tikv/issues/18571) @[v01dstar](https://github.com/v01dstar)
    - 优化 async snapshot 和 write 在有大量 SST 文件的环境中的尾延迟 [#18743](https://github.com/tikv/tikv/issues/18743) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-8.1.2.md > Improvements> TiKV - Improve the speed of Region Merge in scenarios with empty tables and small Regions [#17376](https://github.com/tikv/tikv/issues/17376) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > Improvements> TiKV - Optimize the handling of `CompactedEvent` in Raftstore by moving it to the `split-check` worker, reducing blocking on the main Raftstore thread [#18532](https://github.com/tikv/tikv/issues/18532) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.1.0.md > Improvements> TiKV - Add metrics for memory usage per thread [#15927](https://github.com/tikv/tikv/issues/15927) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-8.5.3.md > Improvements> TiKV - Log only `SST ingest is experiencing slowdowns` when SST ingest is too slow, and skip calling `get_sst_key_ranges` to avoid performance jitter [#18549](https://github.com/tikv/tikv/issues/18549) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.1.6.md > Improvements> TiKV - Optimize the jittery access delay when restarting TiKV due to waiting for the log to be applied, improving the stability of TiKV [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > Improvements> TiKV - Optimize the cleanup mechanism of residual data to mitigate the impact on request latency [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > Improvements> TiKV - Optimize the performance of `fetch_entries_to` in Raft Engine to reduce contention and improve performance under mixed workloads [#18605](https://github.com/tikv/tikv/issues/18605) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.4.0.md > Improvements> TiKV - Support dynamically modifying flow-control configurations for write operations [#17395](https://github.com/tikv/tikv/issues/17395) @[glorv](https://github.com/glorv)
    - (dup): release-8.5.3.md > Improvements> TiKV - Support ingesting SST files without blocking foreground writes, reducing the impact of latency [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - (dup): release-8.5.3.md > Improvements> TiKV - Support ingesting SST files without blocking foreground writes, reducing the impact of latency [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - (dup): release-8.5.3.md > Improvements> TiKV - Optimize the detection mechanism for I/O jitter on KvDB disks when KvDB and RaftDB use separate mount paths [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-6.5.9.md > Improvements> TiKV - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ PD <!--tw@Oreoxmt: 2 notes-->

    - Add more metrics for Golang Runtime, details can be seen at the runtime panel [#8931](https://github.com/tikv/pd/issues/8931) @[bufferflies](https://github.com/bufferflies)
    - 减少一些非必要 error 日志 [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > Improvements> TiFlash - Enhance the observability for TiFlash OOM risks in wide table scenarios [#10272](https://github.com/pingcap/tiflash/issues/10272) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.3.md > Improvements> TiFlash - Increase the maximum retry count when acquiring storage snapshots to improve query stability for large tables [#10300](https://github.com/pingcap/tiflash/issues/10300) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.1.0.md > Improvements> TiFlash - Mitigate the issue that TiFlash might panic due to updating certificates after TLS is enabled [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR) <!--tw@Oreoxmt: 1 note-->

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - 在 Amazon EC2 上部署 TiDB 时，BR 支持 AWS 的 Instance Metadata Service Version 2 (IMDSv2)。你可以在 EC2 实例上进行相关配置，使 BR 可以使用与实例关联的 IAM 角色以适当的权限访问 Amazon S3 [#16443](https://github.com/tikv/tikv/issues/16443) @[pingyu](https://github.com/pingyu)
        - (dup): release-8.5.3.md > Improvements> Tools> Backup & Restore (BR) - The Download API of TiKV supports filtering out data within a certain time range when downloading backup files, which avoids importing outdated or future data versions during restore [#18399](https://github.com/tikv/tikv/issues/18399) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

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

+ TiDB <!--tw@lilin90: the following 12 notes-->

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
    - 修复 PhysicalExchangeSender.HashCol 浅拷贝导致的 TiFlash crash 或者结果错误的问题 [#60517](https://github.com/pingcap/tidb/issues/60517) @[windtalker](https://github.com/windtalker)
    - 减少 IndexLookUp 算子在查询被 cancel 时打印的无用日志 [#61072](https://github.com/pingcap/tidb/issues/61072) @[yibin87](https://github.com/yibin87)
    - 修复 Aggregation 算子在发生内存超限时导致的 goroutine 泄漏问题 [#58004](https://github.com/pingcap/tidb/issues/58004) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 bit 类型表的 stats 无法加载的问题 [#62289](https://github.com/pingcap/tidb/issues/62289) @[YangKeao](https://github.com/YangKeao)
    - 修复 hashjoin v1 算子 Close() 方法没有 recovery panic 的问题 [#60926](https://github.com/pingcap/tidb/issues/60926) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 index merge/index lookup 算子下发查询时共享 kv request 导致的 data race [#60175](https://github.com/pingcap/tidb/issues/60175) @[you06](https://github.com/you06)
    - 修复极端情况下当 ANALYZE 语句的落盘操作耗时太长时可能导致其他 TiDB 节点无法更新最新的统计信息的问题 [#54552](https://github.com/pingcap/tidb/issues/54552) @[0xPoe](https://github.com/0xPoe)
    - 修复当收集的列统计信息完全为 TopN 时，即使有后续写入操作，估算也有可能一直为 0 的问题 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - 修复可能无法将 BIT 类型的列的统计信息加载入内存的问题 [#59759](https://github.com/pingcap/tidb/issues/59759) @[YangKeao](https://github.com/YangKeao)
    - 修复 `explain format="cost_trace"` 展示的估算代价可能有错的问题 [#61155](https://github.com/pingcap/tidb/issues/61155) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `explain format="cost_trace"` 展示的代价计算公式中可能包含空括号的问题 [#61127](https://github.com/pingcap/tidb/issues/61127) @[hawkingrei](https://github.com/hawkingrei)
    - 修复外键定义成环时的死循坏问题 [#60985](https://github.com/pingcap/tidb/issues/60985) @[hawkingrei](https://github.com/hawkingrei) <!--tw@hfxsd: the following 13 notes-->
    - 修复内部查询在使用 `NULL` 构造索引范围查询时可能构造能力不足的问题 [#62196](https://github.com/pingcap/tidb/issues/62196) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 Plan Cache 缓存了错误的执行计划导致执行报错的问题 [#56772](https://github.com/pingcap/tidb/issues/56772) @[dash12653](https://github.com/dash12653)
    - 修复跨月、跨年的行数估算可能过分偏大的问题 [#50080](https://github.com/pingcap/tidb/issues/50080) @[terry1purcell](https://github.com/terry1purcell)
    - 修复 ANALYZE 子任务并发数过于超出设置参数的问题 [#61785](https://github.com/pingcap/tidb/issues/61785) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在 TopN 下推过程中错误生成带表达式的TopN排序项 [#60655](https://github.com/pingcap/tidb/issues/60655) @[hawkingrei](https://github.com/hawkingrei)
    - 修复没有列、索引的统计信息时，TiDB 可能在后台打印 panic 日志的问题 [#61733](https://github.com/pingcap/tidb/issues/61733) @[winoros](https://github.com/winoros)
    - 正确设置内部会话的系统变量的 `tidb_cost_model_version` 的默认值 [#61565](https://github.com/pingcap/tidb/issues/61565) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当表的第一列为虚拟生成列时，统计信息可能出错的问题 [#61606](https://github.com/pingcap/tidb/issues/61606) @[winoros](https://github.com/winoros)
    - 修复错误的跳过 plan cache，当进行谓词简化 [#61513](https://github.com/pingcap/tidb/issues/61513) @[hawkingrei](https://github.com/hawkingrei)
    - 修复特定情况下当缺少列、索引的统计信息时，JOIN 的行数估算可能偏差过大的问题 [#61602](https://github.com/pingcap/tidb/issues/61602) @[qw4990](https://github.com/qw4990)
    - 修复加索引时 cancel ddl job 导致加索引卡住的问题  [#61087](https://github.com/pingcap/tidb/issues/61087) @[tangenta](https://github.com/tangenta)
    - 修复 fast admin check 在一些内部 SQL 执行失败后仍然返回成功的问题 [#61612](https://github.com/pingcap/tidb/issues/61612) @[joechenrh](https://github.com/joechenrh)
    - 修复通过 multi-schema change 加索引之后数据索引不一致的问题 [#61255](https://github.com/pingcap/tidb/issues/61255) @[tangenta](https://github.com/tangenta)

+ TiKV <!--tw@qiancai: 1 note-->

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 修复 Unsafe Recovery 被某些 TiFlash 副本阻塞，导致无法推进的问题 [18197](https://github.com/tikv/tikv/issues/18197) @[v01dstar](https://github.com/v01dstar)
    - (dup): release-8.5.3.md > Bug fixes> TiKV - Fix the issue that TiKV might use a compression algorithm that the client cannot decode [#18079](https://github.com/tikv/tikv/issues/18079) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.5.3.md > Bug fixes> TiKV - Fix the issue that TiKV allows excessive SST ingest requests under high concurrency [#18452](https://github.com/tikv/tikv/issues/18452) @[hbisheng](https://github.com/hbisheng)
    - (dup): release-8.3.0.md > Bug fixes> TiKV - Fix the issue that `Ingestion picked level` and `Compaction Job Size(files)` are displayed incorrectly in the TiKV dashboard in Grafana [#15990](https://github.com/tikv/tikv/issues/15990) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-9.0.0.md > Bug fixes> TiKV - Fix the issue that the unexpected `Server is busy` error occurs after TiKV restarts [#18233](https://github.com/tikv/tikv/issues/18233) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-6.5.9.md > Bug fixes> TiKV - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - (dup): release-8.5.3.md > Bug fixes> TiKV - Fix misleading descriptions in `StoreMsg` log entries in slow logs [#18561](https://github.com/tikv/tikv/issues/18561) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-9.0.0.md > Bug fixes> TiKV - Fix incorrect thread memory metrics [#18125](https://github.com/tikv/tikv/issues/18125) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-8.5.3.md > Bug fixes> TiKV - Fix the issue that TiKV fails to terminate ongoing manual compaction tasks during graceful shutdown [#18396](https://github.com/tikv/tikv/issues/18396) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD <!--tw@qiancai: 5 notes-->

    - Fix the issue that the `split-merge-interval` configuration item might not take effect when you modify its value repeatedly (such as changing it from `1s` to `1h` and back to `1s`) [#8404](https://github.com/tikv/pd/issues/8404) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that the default value of `lease` is not correctly set [#9156](https://github.com/tikv/pd/issues/9156) @[rleungx](https://github.com/rleungx)
    - Fix the issue that pd goroutine leak due to the dashboard connections don't close well [#9402](https://github.com/tikv/pd/issues/9402) @[baurine](https://github.com/baurine)
    - Fix the issue that the new store cna't be balanced [#9145](https://github.com/tikv/pd/issues/9145) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that client can't get any tso after enabled the variable `tidb_enable_tso_follower_proxy`[#9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)

+ TiFlash <!--tw@qiancai: 5 notes-->

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - Fix the panic issue caused by accidental deletion of SST files during running `IMPORT INTO` or `BR restore` [#10141](https://github.com/pingcap/tiflash/issues/10141) @[CalvinNeo](https://github.com/CalvinNeo)
    - (dup): release-8.5.3.md > Bug fixes> TiFlash - Fix the issue that creating an expression index in the form of `((NULL))` causes TiFlash to panic [#9891](https://github.com/pingcap/tiflash/issues/9891) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might panic when handling snapshots with irregular Region key-ranges [#10147](https://github.com/pingcap/tiflash/issues/10147) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might consume a large amount of memory when tables in a cluster contain a large number of `ENUM` type columns [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might fail to restart after inserting a single row of data larger than 16 MiB [#10052](https://github.com/pingcap/tiflash/issues/10052) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.3.md > Bug fixes> TiFlash - Fix the issue that missing resource control low token signals lead to query throttling [#10137](https://github.com/pingcap/tiflash/issues/10137) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might return the `Exception: Block schema mismatch` error when executing SQL statements containing `GROUP BY ... WITH ROLLUP` [#10110](https://github.com/pingcap/tiflash/issues/10110) @[gengliqi](https://github.com/gengliqi)
    - 降低因为 SSL 重新加载导致 TiFlash crash 的可能性(#8535) [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - 修复 TiFlash 报错 fmt::v10::format_error unmatched '}' in format string [#9087](https://github.com/pingcap/tiflash/issues/9087) @[windtalker](https://github.com/windtalker)
    - 修复执行包含 `GROUP BY ... WITH ROLLUP` 的 SQL 语句时，可能会出现 `Exception: Block schema mismatch` 报错的问题 [#10110](https://github.com/pingcap/tiflash/issues/10110) @[gengliqi](https://github.com/gengliqi)
    - 修复 TiFlash resource control 信号丢失导致的非预期的查询受限问题 [#10137](https://github.com/pingcap/tiflash/issues/10137) @[guo-shaoge](https://github.com/guo-shaoge)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.2.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that PITR fails to restore indexes larger than 3072 bytes [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.5.3.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that log backup uploads to Azure Blob Storage are slow when transferring large volumes of data [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.5.3.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that BR does not check whether the corresponding table exists in the cluster when filtering tables with `-f` [#61592](https://github.com/pingcap/tidb/issues/61592) @[RidRisR](https://github.com/RidRisR)

    + TiCDC <!--tw@qiancai: 1 note-->

        - Fix a bug that may cause changefeed with storage sink getting stuck [#9162](https://github.com/pingcap/tiflow/issues/9162) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-8.5.2.md > Bug fixes> Tools> TiCDC - Fix the issue that the changefeed might get stuck after the replication traffic exceeds the traffic threshold of the downstream Kafka [#12110](https://github.com/pingcap/tiflow/issues/12110) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.12.md > Bug fixes> Tools> TiCDC - Fix the issue that using the `--overwrite-checkpoint-ts` parameter in the `changefeed pause` command might cause the changefeed to be stuck [#12055](https://github.com/pingcap/tiflow/issues/12055) @[hongyunyan](https://github.com/hongyunyan)
        - (dup): release-8.5.3.md > Bug fixes> Tools> TiCDC - Fix the issue that evaluating event filter expressions on tables containing virtual columns might cause a panic [#12206](https://github.com/pingcap/tiflow/issues/12206) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-8.5.3.md > Bug fixes> Tools> TiCDC - Fix the issue of case-sensitive matching for column and index names in the dispatcher configuration [#12103](https://github.com/pingcap/tiflow/issues/12103) @[wk989898](https://github.com/wk989898)
        - (dup): release-8.5.3.md > Bug fixes> Tools> TiCDC - Fix the issue that the resolved ts lag keeps increasing after scaling in or out TiKV nodes on the same IP address because of outdated store IDs [#12162](https://github.com/pingcap/tiflow/issues/12162) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.2.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that TiDB Lightning can get stuck for several hours when importing Parquet files from cloud storage into TiDB [#60224](https://github.com/pingcap/tidb/issues/60224) @[joechenrh](https://github.com/joechenrh)
        - (dup): release-8.5.3.md > 错误修复> Tools> TiDB Lightning - 修复 TiDB Lightning 向 TiKV 发起的 RPC 请求超时后返回 `context deadline exceeded` 的问题 [#61326](https://github.com/pingcap/tidb/issues/61326) @[OliverS929](https://github.com/OliverS929)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + NG Monitoring

        - (dup): release-8.5.2.md > Bug fixes> Tools> NG Monitoring - Fix the issue that TSDB consumes too much memory under high cardinality of time series data, and provide a memory configuration option for TSDB [#295](https://github.com/pingcap/ng-monitoring/issues/295) @[mornyx](https://github.com/mornyx)
