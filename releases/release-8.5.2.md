---
title: TiDB 8.5.2 Release Notes
summary: Learn about the operating system and platform requirement changes, improvements, and bug fixes in TiDB 8.5.2.
---

# TiDB 8.5.2 Release Notes

Release date: xx xx, 2025

TiDB version: 8.5.2

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

## Compatibility changes

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## Improvements

+ TiDB <!--tw@Oreoxmt: 1 note--> 

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.6.md > 改进提升> TiDB - 将 TTL 表的 GC 及相关统计信息收集任务限定在 owner 节点执行，从而降低开销 [#59357](https://github.com/pingcap/tidb/issues/59357) @[lcwangchao](https://github.com/lcwangchao)
    - TiDB supports compilation and building on the Loongson loong64 architecture [#59051](https://github.com/pingcap/tidb/issues/59051) @[D3Hunter](https://github.com/D3Hunter)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.1.2.md > 改进提升> TiKV - 支持在线修改 `import.num-threads` 配置项 [#17807](https://github.com/tikv/tikv/issues/17807) @[RidRisR](https://github.com/RidRisR)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 1 note-->

        - Remove the check on AWS region names to avoid backup errors caused by newly supported AWS regions failing the validation [#18159](https://github.com/tikv/tikv/issues/18159) @[3pointer](https://github.com/3pointer)
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.12.md > 改进提升> Tools> TiDB Lightning - 在解析 CSV 文件时，新增行宽检查以防止 OOM 问题 [#58590](https://github.com/pingcap/tidb/issues/58590) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## Bug fixes

+ TiDB

    - Fix the issue that obtaining TSO fails during timestamp verification after setting the `zone` label [#59402](https://github.com/pingcap/tidb/issues/59402) @[ekexium](https://github.com/ekexium)
    - Fix the issue that Hash Join returns incorrect results without reporting an error when execution fails [#59377](https://github.com/pingcap/tidb/issues/59377) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that TiFlash might crash or return incorrect results [#60517](https://github.com/pingcap/tidb/issues/60517) @[wintalker](https://github.com/wintalker)
    - Fix the issue that execution hangs during parallel sorting with ORDER BY [#59655](https://github.com/pingcap/tidb/issues/59655) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复在查询包含生成列的分区表时报错的问题 [#58475](https://github.com/pingcap/tidb/issues/58475) @[joechenrh](https://github.com/joechenrh)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复创建两个相同名称的视图而没有报错的问题 [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 Join 的等值条件两边数据类型不同，可能导致 TiFlash 产生错误结果的问题 [#59877](https://github.com/pingcap/tidb/issues/59877) @[yibin87](https://github.com/yibin87)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 Hash 类型分区表在查询 `is null` 条件时 panic 的问题 [#58374](https://github.com/pingcap/tidb/issues/58374) @[Defined2014](https://github.com/Defined2014/)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复当集群中存在存算分离架构 TiFlash 节点时，执行 `ALTER TABLE ... PLACEMENT POLICY ...` 之后，Region peer 可能会被意外地添加到 TiFlash Compute 节点的问题 [#58633](https://github.com/pingcap/tidb/issues/58633) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-6.5.12.md > 错误修复> TiDB - 修复手动加载统计信息时，统计信息文件中包含 null 可能导致加载失败的问题 [#53966](https://github.com/pingcap/tidb/issues/53966) @[King-Dylan](https://github.com/King-Dylan)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 TTL 任务可能被忽略或处理多次的问题 [#59347](https://github.com/pingcap/tidb/issues/59347) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复 exchange partition 错误判断导致执行失败的问题 [#59534](https://github.com/pingcap/tidb/issues/59534) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.5.6.md > 错误修复> TiDB - 修复对统计信息的异常处理不当导致后台任务超时的时候，内存内的统计信息被误删除的问题 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.5.md > 错误修复> TiDB - 修复 Grafana 中 **Stats Healthy Distribution** 面板的数据可能错误的问题 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that a canceled TTL task might put a not-committed session to the global session pool [#58900](https://github.com/pingcap/tidb/issues/58900) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that enabling Redact log does not take effect in certain scenarios [#59279](https://github.com/pingcap/tidb/issues/59279) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `rowContainer` might cause TiDB to panic [#59976](https://github.com/pingcap/tidb/issues/59976) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that partition pruning might be incorrect for partitioned tables in `Point_Get` scenarios [#59827](https://github.com/pingcap/tidb/issues/59827) @[mjonss](https://github.com/mjonss)
    - Fix the issue that updating records in partitioned tables during DDL execution might lead to data inconsistency [#57588](https://github.com/pingcap/tidb/issues/57588) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that affects the performance and stability of `information_schema` in certain scenarios [#58142](https://github.com/pingcap/tidb/issues/58142) [#58363](https://github.com/pingcap/tidb/issues/58363) [#58712](https://github.com/pingcap/tidb/issues/58712) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that `tidb_txn_entry_size_limit` cannot be dynamically adjusted in internal TiDB sessions when the Distributed eXecution Framework (DXF) is enabled [#59506](https://github.com/pingcap/tidb/issues/59506)@[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that the `IMPORT INTO` feature fails to properly handle unique key conflicts when global sorting is enabled [#59650](https://github.com/pingcap/tidb/issues/59650) @[lance6716](https://github.com/lance6716)
    - Fix the issue that network latency failure in the global sorting data path causes IMPORT INTO to fail  [#50451](https://github.com/pingcap/tidb/issues/50451) @[D3Hunter](https://github.com/D3Hunter) 
    - Fix the issue that executing `ADD UNIQUE INDEX` might cause data inconsistency [#60339](https://github.com/pingcap/tidb/issues/60339) @[tangenta](https://github.com/tangenta)     
    <!--tw@Oreoxmt: the following 9 notes-->
    - Fix the issue that the value of the `LABELS` column is incorrectly displayed in the `BINLOG_STATUS` column when querying `INFORMATION_SCHEMA.TIDB_SERVERS_INFO` [#59245](https://github.com/pingcap/tidb/issues/59245) @[lance6716](https://github.com/lance6716)
    - Fix the issue that injecting a kill PD Leader fault during index creation might cause data inconsistency [#59701](https://github.com/pingcap/tidb/issues/59701) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TiDB runs out of memory (OOM) after creating approximately 6.5 million tables [#58368](https://github.com/pingcap/tidb/issues/58368) @[lance6716](https://github.com/lance6716)
    - Fix the issue that adding a unique key might fail when importing a large amount of data with the Global Sort feature enabled [#59725](https://github.com/pingcap/tidb/issues/59725) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that TiDB returns unreadable error messages after failing to access S3 external storage [#59326](https://github.com/pingcap/tidb/issues/59326) @[lance6716](https://github.com/lance6716)
    - Fix the issue that querying `infoschema.tables` returns mismatched `table_schema` and `table_name` values [#60593](https://github.com/pingcap/tidb/issues/60593) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the DDL notifier might deliver incorrect notifications when internal SQL commits fail [#59055](https://github.com/pingcap/tidb/issues/59055) @[lance6716](https://github.com/lance6716)
    - Fix the issue that `ADD INDEX` DDL operations still split SST files by 96 MiB when the Global Sort feature is enabled, despite the Region size is 256 MiB [#59962](https://github.com/pingcap/tidb/issues/59962) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that TiDB servers run out of memory (OOM) when memory usage exceeds 80% during data import with the Global Sort feature enabled [#59508](https://github.com/pingcap/tidb/issues/59508) @[D3Hunter](https://github.com/D3Hunter)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.6.md > 错误修复> TiKV - 修复 Resolved-TS 监控和日志可能显示异常的问题 [#17989](https://github.com/tikv/tikv/issues/17989) @[ekexium](https://github.com/ekexium)
    - (dup): release-7.5.6.md > 错误修复> TiKV - 修复 Region 合并时可能因 Raft index 匹配异常而导致 TiKV 异常退出的问题 [#18129](https://github.com/tikv/tikv/issues/18129) @[glorv](https://github.com/glorv)
    - (dup): release-8.1.2.md > 错误修复> TiKV - 修复磁盘卡住时，TiKV 无法向 PD 上报心跳的问题 [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复 GC Worker 负载过高时可能出现的死锁问题 [#18214](https://github.com/tikv/tikv/issues/18214) @[zyguan](https://github.com/zyguan)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复时钟回退导致 RocksDB 流控异常，进而引发性能抖动的问题 [#17995](https://github.com/tikv/tikv/issues/17995) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.5.6.md > 错误修复> TiKV - 修复 CDC 连接在遇到异常时可能发生资源泄漏的问题 [#18245](https://github.com/tikv/tikv/issues/18245) @[wlwilliamx](https://github.com/wlwilliamx)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复 Region Split 后可能无法快速选出 Leader 的问题 [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-6.5.12.md > 错误修复> TiKV - 修复在仅启用一阶段提交 (1PC) 而未启用异步提交 (Async Commit) 时，可能无法读取最新写入数据的问题 [#18117](https://github.com/tikv/tikv/issues/18117) @[zyguan](https://github.com/zyguan)

+ PD <!--tw@lilin90: 5 notes-->

    - Fix the concurrency issue that might arise when forwarding TSO in microservice scenarios [#9091](https://github.com/tikv/pd/issues/9091) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that the result returned by `BatchScanRegions` was not properly limited [#9216](https://github.com/tikv/pd/issues/9216) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that an unexpected election occurs when one follower experiences a network partition from the leader [#9020](https://github.com/tikv/pd/issues/9020) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that `COOLDOWN` or `SWITCH_GROUP` cannot be triggered when `QUERY_LIMIT` is set in resource control [#60404](https://github.com/pingcap/tidb/issues/60404) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that `StoreInfo` might be incorrectly overridden [#9185](https://github.com/tikv/pd/issues/9185) @[okJiang](https://github.com/okJiang)
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.6.md > 错误修复> PD - 修复在导入或添加索引场景中，因 PD 网络不稳定可能导致操作失败的问题 [#8962](https://github.com/tikv/pd/issues/8962) @[okJiang](https://github.com/okJiang)
    - (dup): release-7.5.6.md > 错误修复> PD - 修复单个日志文件 `max-size` 默认值未被正确设置的问题 [#9037](https://github.com/tikv/pd/issues/9037) @[rleungx](https://github.com/rleungx)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复 TSO 分配过程中可能出现的内存泄漏问题 [#9004](https://github.com/tikv/pd/issues/9004) @[rleungx](https://github.com/rleungx)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复设置 `tidb_enable_tso_follower_proxy` 系统变量可能不生效的问题 [#8947](https://github.com/tikv/pd/issues/8947) @[JmPotato](https://github.com/JmPotato)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复当某个 PD 节点不是 Leader 时，仍可能生成 TSO 的问题 [#9051](https://github.com/tikv/pd/issues/9051) @[rleungx](https://github.com/rleungx)
    - (dup): release-6.5.12.md > 错误修复> PD - 修复 PD Leader 切换过程中，Region syncer 未能及时退出的问题 [#9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)

+ TiFlash <!--tw@qiancai: 9 notes-->

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - Fix the issue that data spill during sorting might cause TiFlash to crash [#9999](https://github.com/pingcap/tiflash/issues/9999) @[windtalker](https://github.com/windtalker)
    - Fix the issue that TiFlash might return the `Exception: Block schema mismatch` error when executing SQL statements containing `GROUP BY ... WITH ROLLUP` [#10110](https://github.com/pingcap/tiflash/issues/10110) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在存算分离架构下，TiFlash 计算节点可能被错误选为添加 Region peer 的目标节点的问题 [#9750](https://github.com/pingcap/tiflash/issues/9750) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在某些情况下 TiFlash 意外退出时无法打印错误堆栈的问题 [#9902](https://github.com/pingcap/tiflash/issues/9902) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-6.5.12.md > 错误修复> TiFlash - 修复在导入大量数据后，TiFlash 可能持续占用较高内存的问题 [#9812](https://github.com/pingcap/tiflash/issues/9812) @[CalvinNeo](https://github.com/CalvinNeo)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复当 `profiles.default.init_thread_count_scale` 设置为 `0` 时，TiFlash 启动可能会卡住的问题 [#9906](https://github.com/pingcap/tiflash/issues/9906) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在分区表上执行 `ALTER TABLE ... RENAME COLUMN` 后，查询该表可能报错的问题 [#9787](https://github.com/pingcap/tiflash/issues/9787) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-7.5.6.md > 错误修复> TiFlash - 修复在查询涉及虚拟列并且触发远程读时，可能会出现 `Not found column` 错误的问题 [#9561](https://github.com/pingcap/tiflash/issues/9561) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiFlash might consume memory greatly when tables in a cluster contain a large number of `ENUM` type columns [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might fail to restart after inserting a single row of data larger than 16 MiB [#10052](https://github.com/pingcap/tiflash/issues/10052) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might not clean some disk data correctly after new data is inserted to tables with vector indexes, causing abnormal disk space consumption [#9946](https://github.com/pingcap/tiflash/issues/9946) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might delete previously created vector indexes unexpectedly after multiple vector indexes are created on the same table, causing performance degradation [#9971](https://github.com/pingcap/tiflash/issues/9971) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash might fail to use vector indexes to accelerate vector search queries in a disaggregated storage and compute architecture [#9847](https://github.com/pingcap/tiflash/issues/9847) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash might print a large number of `unknown enum` logs in a disaggregated storage and compute architecture [#9955](https://github.com/pingcap/tiflash/issues/9955) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash does not skip Learner Read as expected when executing `SELECT ... AS OF TIMESTAMP` queries [#10046](https://github.com/pingcap/tiflash/issues/10046) @[CalvinNeo](https://github.com/CalvinNeo)

+ Tools

    + Backup & Restore (BR) <!--tw@lilin90: 1 note-->

        - Fix the issue that repeated downloading of SST files during data restore could cause TiKV to panic in extreme cases [#18335](https://github.com/tikv/tikv/issues/18335) @[3pointer](https://github.com/3pointer)
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.12.md > 错误修复> Tools> Backup & Restore (BR) - 修复使用 `br log status --json` 查询日志备份任务时，返回结果中缺少任务状态 `status` 字段的问题 [#57959](https://github.com/pingcap/tidb/issues/57959) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.12.md > 错误修复> Tools> Backup & Restore (BR) - 修复 BR 向 TiKV 发送请求时收到 `rpcClient is idle` 错误导致恢复失败的问题 [#58845](https://github.com/pingcap/tidb/issues/58845) @[Tristan1900](https://github.com/Tristan1900)
        - (dup): release-7.5.6.md > 错误修复> Tools> Backup & Restore (BR) - 修复日志备份在无法访问 PD 时，遇到致命错误无法正确退出的问题 [#18087](https://github.com/tikv/tikv/issues/18087) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.6.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PITR 无法恢复大于 3072 字节的索引的问题 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC <!--tw@qiancai: 3 notes-->

        - Fix the issue that the changefeed might get stuck after the replication traffic exceeds the traffic threshold of the downstream Kafka [#12110](https://github.com/pingcap/tiflow/issues/12110) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the dispatch rule for the Kafka sink does not take effect when the `pulsar+http` or `pulsar+https` protocol is used [#12068](https://github.com/pingcap/tiflow/issues/12068) @[SandeepPadhi](https://github.com/SandeepPadhi)
        - Fix the issue that TiCDC fails to observe the PD leader migration in time, causing the replication latency to increase [#11997](https://github.com/pingcap/tiflow/issues/11997) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复 TiCDC 通过 Avro 协议同步 `default NULL` SQL 语句时报错的问题 [#11994](https://github.com/pingcap/tiflow/issues/11994) @[wk989898](https://github.com/wk989898)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复当上游将一个新增的列的默认值从 `NOT NULL` 修改为 `NULL` 后，下游默认值错误的问题 [#12037](https://github.com/pingcap/tiflow/issues/12037) @[wk989898](https://github.com/wk989898)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复 PD 缩容后 TiCDC 无法正确连接 PD 的问题 [#12004](https://github.com/pingcap/tiflow/issues/12004) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiCDC - 修复 TiCDC 同步 `CREATE TABLE IF NOT EXISTS` 或 `CREATE DATABASE IF NOT EXISTS` 语句时可能出现 panic 的问题 [#11839](https://github.com/pingcap/tiflow/issues/11839) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.12.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复当同时配置 TLS 和 `shard-mode` 时，`start-task` 会在前置检查中报错的问题 [#11842](https://github.com/pingcap/tiflow/issues/11842) @[sunxiaoguang](https://github.com/sunxiaoguang)

    + TiDB Lightning <!--tw@lilin90: 4 notes-->

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.12.md > 错误修复> Tools> TiDB Lightning - 修复在高并发场景下，从云存储导入数据时性能下降的问题 [#57413](https://github.com/pingcap/tidb/issues/57413) @[xuanyu66](https://github.com/xuanyu66)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiDB Lightning - 修复使用 TiDB Lightning 导入数据时，错误报告输出被截断的问题 [#58085](https://github.com/pingcap/tidb/issues/58085) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.5.12.md > 错误修复> Tools> TiDB Lightning - 修复日志没有正确脱敏的问题 [#59086](https://github.com/pingcap/tidb/issues/59086) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that authentication would fail with an `context canceled` error when using an external account to perform any GCS storage operation [#60155](https://github.com/pingcap/tidb/issues/60155) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning can get stuck for several hours when importing Parquet files from cloud storage into TiDB [#60224](https://github.com/pingcap/tidb/issues/60224) @[joechenrh](https://github.com/joechenrh)
        - Fix the issue that TiDB Lightning could run out of memory (OOM) during writing or ingesting SST files into the TiKV cluster when importing large volumes of data [#59947](https://github.com/pingcap/tidb/issues/59947) @[OliverS929](https://github.com/OliverS929)
        - Fix the issue that low maximum QPS during table creation and slow access to `information_schema.tables` cause TiDB Lightning to dispatch schema jobs slower in scenarios with millions of tables [#58141](https://github.com/pingcap/tidb/issues/58141) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + NG Monitoring <!--tw@hfxsd: 2 notes-->

        - Fix the issue that DocDB consumes too much memory under high workloads, and use SQLite as an optional backend for DocDB [#267](https://github.com/pingcap/ng-monitoring/issues/267) @[mornyx](https://github.com/mornyx)
        - Fix the issue that TSDB consumes too much memory under high cardinality of time series, and privode a memory configuration option for TSDB [#295](https://github.com/pingcap/ng-monitoring/issues/295) @[mornyx](https://github.com/mornyx)
