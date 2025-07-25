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
    - (dup): release-8.5.3.md > 改进提升> TiDB - 新增导入期间分裂 region 和 ingest 数据的流控接口 [#61553](https://github.com/pingcap/tidb/issues/61553) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.2.0.md > Improvements> TiDB - Optimize the performance of obtaining data distribution information when performing simple queries on tables with large data volumes [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)
    - (dup): release-8.5.3.md > 改进提升> TiDB - 新增加索引的导入速度监控 [#60925](https://github.com/pingcap/tidb/issues/60925) @[CbcWestwolf](https://github.com/CbcWestwolf)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > 改进提升> TiKV - 优化 raftstore 中 `CompactedEvent` 的处理逻辑，将其移至 `split-check` worker 执行 [#18532](https://github.com/tikv/tikv/issues/18532) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.1.0.md > Improvements> TiKV - Add metrics for memory usage per thread [#15927](https://github.com/tikv/tikv/issues/15927) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 移除 “sst ingest is too slow” 的日志，避免引发性能抖动 [#18549](https://github.com/tikv/tikv/issues/18549) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.1.6.md > Improvements> TiKV - Optimize the jittery access delay when restarting TiKV due to waiting for the log to be applied, improving the stability of TiKV [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > 改进提升> TiKV - (dup): release-9.0.0.md > 改进提升> TiKV - 优化残留数据清理机制，减少对请求延迟的影响 [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 修复 TiKV 正常退出时未能中止正在进行的手动 Compaction 任务的问题 [#18396](https://github.com/tikv/tikv/issues/18396) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 优化 Raft-Engine 中 `fetch_entries_to` 的性能，减少竞争，提升混合负载下的执行性能 [#18605](https://github.com/tikv/tikv/issues/18605) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.4.0.md > Improvements> TiKV - Support dynamically modifying flow-control configurations for write operations [#17395](https://github.com/tikv/tikv/issues/17395) @[glorv](https://github.com/glorv)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 支持在不阻塞前台写入的情况下导入 SST 文件，降低延迟影响 [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 支持在不阻塞前台写入的情况下导入 SST 文件，降低延迟影响 [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    - (dup): release-8.5.3.md > 改进提升> TiKV - 改进分盘部署场景下 kvdb 磁盘 I/O 抖动的检测机制 [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-6.5.9.md > Improvements> TiKV - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > 改进提升> PD - 优化了 balance region 调度器的算分公式 [#9145](https://github.com/tikv/pd/issues/9145) @[bufferflies](https://github.com/bufferflies)
    - (dup): release-8.5.3.md > 改进提升> PD - 增加了 GO Runtime 相关监控 [#8931](https://github.com/tikv/pd/issues/8931) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > 改进提升> TiFlash - 增强 TiFlash 在宽表场景下 OOM 风险相关的监测指标 [#10272](https://github.com/pingcap/tiflash/issues/10272) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.3.md > 改进提升> TiFlash - 增加 TiFlash 获取存储层快照重试次数来增强大表上查询的稳定性 [#10300](https://github.com/pingcap/tiflash/issues/10300) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.1.0.md > Improvements> TiFlash - Mitigate the issue that TiFlash might panic due to updating certificates after TLS is enabled [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.3.md > 改进提升> Tools> Backup & Restore (BR) - 如今即便指定了 `-f` 来过滤表，BR 也会对集群内是否存在表进行检查 [#61592](https://github.com/pingcap/tidb/issues/61592) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-8.5.3.md > 改进提升> Tools> Backup & Restore (BR) - 如今，TiKV 的 Download API 支持裁切掉 SST 中某段时间的数据 [#18399](https://github.com/tikv/tikv/issues/18399) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.3.md > 改进提升> Tools> TiCDC - 修复在包含虚拟列的表中计算事件过滤表达式时出现的 Panic 错误 [#12206](https://github.com/pingcap/tiflow/issues/12206) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-8.5.3.md > 改进提升> Tools> TiCDC - 修复 dispatcher 配置中列名/索引名大小写敏感匹配的问题 [#12103](https://github.com/pingcap/tiflow/issues/12103) @[wk989898](https://github.com/wk989898)
        - (dup): release-8.5.3.md > 改进提升> Tools> TiCDC - 修复在相同 IP 地址上扩缩容 TiKV 节点后，因使用过期的 store ID 导致 resolved ts 延迟持续上升的问题 [#12162](https://github.com/pingcap/tiflow/issues/12162) @[3AceShowHand](https://github.com/3AceShowHand)

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
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复 IndexMerge/IndexLookUp 算子下发查询时共享 kv request 导致的 data race [#60175](https://github.com/pingcap/tidb/issues/60175) @[you06](https://github.com/you06)
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix a potential goroutine leak issue in the Hash Aggregation operator [#58004](https://github.com/pingcap/tidb/issues/58004) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that MPP plans might not be selected when indexes on generated columns are set as visible [#47766](https://github.com/pingcap/tidb/issues/47766) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 为包含 `_charset(xxx), _charset(xxx2), ...` 的 SQL 生成同样的 digest [#58447](https://github.com/pingcap/tidb/issues/58447) @[xhebox](https://github.com/xhebox)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复频繁合并 region 导致 TTL 任务无法启动的问题 [#61512](https://github.com/pingcap/tidb/issues/61512) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复执行有损 DDL 后，查询 TiFlash 数据不一致的问题 [#61455](https://github.com/pingcap/tidb/issues/61455) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复了 `ALTER RANGE meta SET PLACEMENT POLICY` key 范围错误的问题 [#60888](https://github.com/pingcap/tidb/issues/60888) @[nolouch](https://github.com/nolouch)
    - (dup): release-8.5.2.md > Bug fixes> TiDB - Fix the issue that the data in the **Stats Healthy Distribution** panel of Grafana might be incorrect [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复 latin1_bin   与 utf8mb4_bin, utf8_bin 的比较方式不相同的问题 [#60701](https://github.com/pingcap/tidb/issues/60701) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复禁用 MDL 后，DDL 更新 schema 版本失败后卡住的问题 [#61210](https://github.com/pingcap/tidb/issues/61210) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-8.5.2.md > Bug fixes> TiDB - Fix the issue that enabling Redact log does not take effect in certain scenarios [#59279](https://github.com/pingcap/tidb/issues/59279) @[tangenta](https://github.com/tangenta)
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix the issue that a TiDB session might crash when Fix Control #44855 is enabled [#59762](https://github.com/pingcap/tidb/issues/59762) @[winoros](https://github.com/winoros)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 删除 IndexLookup 算子发生 context cancel 错误时没用的日志信息 [#61072](https://github.com/pingcap/tidb/issues/61072) @[yibin87](https://github.com/yibin87)
    - (dup): release-8.5.2.md > Bug fixes> TiDB - Fix the issue that improper exception handling for statistics causes in-memory statistics to be mistakenly deleted when background tasks time out [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.5.2.md > Bug fixes> TiDB - Fix the issue that executing `ADD UNIQUE INDEX` might cause data inconsistency [#60339](https://github.com/pingcap/tidb/issues/60339) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复统计信息系统表展示非 public 索引的问题 [#60430](https://github.com/pingcap/tidb/issues/60430) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.5.3.md > 错误修复> TiDB - 修复 HashJoin 算子因为内存超限导致的 goroutine leak 问题 [#60926](https://github.com/pingcap/tidb/issues/60926) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.3.md > 错误修复> TiKV - 修复 TiKV 可能使用客户端无法解码的压缩算法的问题 [#18079](https://github.com/tikv/tikv/issues/18079) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.5.3.md > 错误修复> TiKV - 修复高并发场景下 TiKV 过量放行 SST 导入请求的问题 [#18452](https://github.com/tikv/tikv/issues/18452) @[hbisheng](https://github.com/hbisheng)
    - (dup): release-8.3.0.md > Bug fixes> TiKV - Fix the issue that `Ingestion picked level` and `Compaction Job Size(files)` are displayed incorrectly in the TiKV dashboard in Grafana [#15990](https://github.com/tikv/tikv/issues/15990) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-9.0.0.md > Bug fixes> TiKV - Fix the issue that the unexpected `Server is busy` error occurs after TiKV restarts [#18233](https://github.com/tikv/tikv/issues/18233) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-6.5.9.md > Bug fixes> TiKV - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - (dup): release-8.5.3.md > 错误修复> TiKV - 修复 slowlog 中 `StoreMsg` 的误导性日志问题 [#18561](https://github.com/tikv/tikv/issues/18561) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-9.0.0.md > Bug fixes> TiKV - Fix incorrect thread memory metrics [#18125](https://github.com/tikv/tikv/issues/18125) @[Connor1996](https://github.com/Connor1996)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.2.md > Bug fixes> PD - Fix the issue that the default value of `lease` is not correctly set [#9156](https://github.com/tikv/pd/issues/9156) @[rleungx](https://github.com/rleungx)
    - (dup): release-8.3.0.md > Bug fixes> PD - Fix the issue that the `split-merge-interval` configuration item might not take effect when you modify its value repeatedly (such as changing it from `1s` to `1h` and back to `1s`) [#8404](https://github.com/tikv/pd/issues/8404) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-8.5.3.md > 错误修复> PD - 修复了 TiDB Dashboard 导致的 goroutine 泄露问题 [#9402](https://github.com/tikv/pd/issues/9402) @[baurine](https://github.com/baurine)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - Fix the panic issue caused by accidental deletion of SST files during running `IMPORT INTO` or `BR restore` [#10141](https://github.com/pingcap/tiflash/issues/10141) @[CalvinNeo](https://github.com/CalvinNeo)
    - (dup): release-8.5.3.md > 错误修复> TiFlash - 修复创建 `((NULL))` 形式的表达式索引会导致 TiFlash panic 的问题 [#9891](https://github.com/pingcap/tiflash/issues/9891) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might panic when handling snapshots with irregular Region key-ranges [#10147](https://github.com/pingcap/tiflash/issues/10147) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might consume a large amount of memory when tables in a cluster contain a large number of `ENUM` type columns [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might fail to restart after inserting a single row of data larger than 16 MiB [#10052](https://github.com/pingcap/tiflash/issues/10052) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.5.3.md > 错误修复> TiFlash - 修复 resource control low token signal 丢失导致查询被限速的问题 [#10137](https://github.com/pingcap/tiflash/issues/10137) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-8.5.2.md > Bug fixes> TiFlash - Fix the issue that TiFlash might return the `Exception: Block schema mismatch` error when executing SQL statements containing `GROUP BY ... WITH ROLLUP` [#10110](https://github.com/pingcap/tiflash/issues/10110) @[gengliqi](https://github.com/gengliqi)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.2.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that PITR fails to restore indexes larger than 3072 bytes [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.5.3.md > 错误修复> Tools> Backup & Restore (BR) - 修复了日志备份上传较大数据到 Azure Blob Storage 时会非常缓慢的问题。 [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.2.md > Bug fixes> Tools> TiCDC - Fix the issue that the changefeed might get stuck after the replication traffic exceeds the traffic threshold of the downstream Kafka [#12110](https://github.com/pingcap/tiflow/issues/12110) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.12.md > Bug fixes> Tools> TiCDC - Fix the issue that using the `--overwrite-checkpoint-ts` parameter in the `changefeed pause` command might cause the changefeed to be stuck [#12055](https://github.com/pingcap/tiflow/issues/12055) @[hongyunyan](https://github.com/hongyunyan)

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
