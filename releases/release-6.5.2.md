---
title: TiDB 6.5.2 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.2.
---

# TiDB 6.5.2 Release Notes

Release date: April x, 2023

TiDB version: 6.5.2

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.2#version-list)

## Compatibility changes

- (dup): release-7.0.0.md > # 行为变更 * TiCDC 修复了 Avro 编码 `FLOAT` 类型数据错误的问题 [#8490](https://github.com/pingcap/tiflow/issues/8490) @[3AceShowHand](https://github.com/3AceShowHand)

    在升级 TiCDC 集群到 v6.5.2 或更高的 v6.5.x 版本时，如果使用 Avro 同步的表包含 `FLOAT` 类型数据，请在升级前手动调整 Confluent Schema Registry 的兼容性策略为 `None`，使 changefeed 能够成功更新 schema。否则，在升级之后 changefeed 将无法更新 schema 并进入错误状态。

## Improvements

+ TiDB

    - (dup): release-6.1.6.md > 提升改进> TiDB - Prepared Plan Cache 支持缓存 BatchPointGet 计划 [#42125](https://github.com/pingcap/tidb/issues/42125) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.0.0.md > 改进提升> TiDB - Index Join 支持更多的 SQL 格式 [#40505](https://github.com/pingcap/tidb/issues/40505) @[Yisaer](https://github.com/Yisaer)
    - Change the level for some Index Merge Reader logs from `"info"` to `"debug"` [#41949](https://github.com/pingcap/tidb/issues/41949) @[yibin87](https://github.com/yibin87)
    - Optimize the `distsql_concurrency` setting for Range partitioned tables with limits to reduce query latency [#41480](https://github.com/pingcap/tidb/issues/41480) @[you06](https://github.com/you06)

+ TiKV

    - note 1
    - note 2

+ PD

    - note 1
    - note 2

+ TiFlash

    - Reduce CPU consumption of task scheduling during TiFlash reads [#6495](https://github.com/pingcap/tiflash/issues/6495) @[JinheLin](https://github.com/JinheLin)
    - Improve performance of data import from BR and TiDB Lightning to TiFlash with default parameters [#7272](https://github.com/pingcap/tiflash/issues/7272) @[breezewish](https://github.com/breezewish)
    - note 2

+ Tools

    + Backup & Restore (BR)

        - note 1

    + TiCDC

        - Release TiCDC Open API v2.0 [#8743](https://github.com/pingcap/tiflow/issues/8743) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-7.0.0.md > 改进提升> Tools> TiCDC - 支持在 redo applier 中拆分事务以提升 apply 吞吐，降低灾难场景的 RTO [#8318](https://github.com/pingcap/tiflow/issues/8318) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.0.0.md > 改进提升> Tools> TiCDC - 支持在 redo log 里 apply DDL 事件 [#8361](https://github.com/pingcap/tiflow/issues/8361) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - note 1

    + TiDB Lightning

        - (dup): release-6.6.0.md > 改进提升> Tools> TiDB Lightning - 支持导入带有 BOM header 的 CSV 数据文件 [#40744](https://github.com/pingcap/tidb/issues/40744) @[dsdashun](https://github.com/dsdashun)

    + Dumpling

## Bug fixes

+ TiDB
    - Fix the issue that after a new column is added in the cache table, the value is `NULL` instead of the default value of the column [#42928](https://github.com/pingcap/tidb/issues/42928) @[lqs](https://github.com/lqs)
    - Fix the issue of DDL retry caused by write conflict when executing `TRUNCATE TABLE` for partitioned tables with many partitions and TiFlash copies [#42940](https://github.com/pingcap/tidb/issues/42940) @[mjonss](https://github.com/mjonss)
    - Fix the issue of missing table names in the result of `ADMIN SHOW DDL JOBS` when the `DROP TABLE` operation is being executed [#42268](https://github.com/pingcap/tidb/issues/42268) @[tiancaiamao ](https://github.com/tiancaiamao)
    - Fix the issue that TiDB Server cannot start due to an error in reading the cgroup information and reports the following error message "can't read file memory.stat from cgroup v1: open /sys/memory.stat no such file or directory" [#42659](https://github.com/pingcap/tidb/issues/42659) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that data truncation does not give correct warnings when you modify columns on a partitioned table [#24427](https://github.com/pingcap/tidb/issues/24427) @[mjonss](https://github.com/mjonss)
    - (dup): release-6.1.6.md > Bug 修复> TiDB - 修复了生成执行计划过程中，因为获取的 InfoSchema 不一致而导致的 TiDB panic 的问题 [#41622](https://github.com/pingcap/tidb/issues/41622) [@tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.1.6.md > Bug 修复> TiDB - 修复了使用 DDL 修改浮点类型时，保持长度不变且减少小数位后，旧数据仍然保持原样的问题 [#41281](https://github.com/pingcap/tidb/issues/41281) [@zimulala](https://github.com/zimulala)
    - (dup): release-6.1.6.md > Bug 修复> TiDB - 修复事务内执行 PointUpdate 之后，`SELECT` 结果不正确的问题 [#28011](https://github.com/pingcap/tidb/issues/28011) @[zyguan](https://github.com/zyguan)
    - (dup): release-6.1.6.md > Bug 修复> TiDB - 修复在使用 Cursor Fetch 且在 Execute、Fetch、Close 之间运行其它语句后，Fetch 与 Close 命令可能会返回错误结果或造成 TiDB Panic 的问题 [#40094](https://github.com/pingcap/tidb/issues/40094) [@YangKeao](https://github.com/YangKeao)
    - (dup): release-7.0.0.md > 错误修复> TiDB - 修复 `INSERT IGNORE` 和 `REPLACE` 语句对不修改 value 的 key 没有加锁的问题 [#42121](https://github.com/pingcap/tidb/issues/42121) @[zyguan](https://github.com/zyguan)
    - (dup): release-7.0.0.md > 错误修复> TiDB - 修复 TiFlash 执行中遇到生成列会报错的问题 [#40663](https://github.com/pingcap/tidb/issues/40663) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-7.0.0.md > 错误修复> TiDB - 修复当同一个 SQL 中出现多个不同的分区表时，TiDB 可能执行得到错误结果的问题 [#42135](https://github.com/pingcap/tidb/issues/42135) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.0.0.md > 错误修复> TiDB - 修复在开启 Prepared Plan Cache 的情况下，索引全表扫可能会报错的问题 [#42150](https://github.com/pingcap/tidb/issues/42150) @[fzzf678](https://github.com/fzzf678)
    - (dup): release-7.0.0.md > 错误修复> TiDB - 修复在开启 Prepared Plan Cache 时 Index Merge 可能得到错误结果的问题 [#41828](https://github.com/pingcap/tidb/issues/41828) @[qw4990](https://github.com/qw4990)
    - Fix the issue that global memory control might incorrectly kill SQL with memory usage less than `tidb_server_memory_limit_sess_min_size` [#42662](https://github.com/pingcap/tidb/issues/41828) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that Index Join might cause panic in dynamic trimming mode of partition tables [#40596](https://github.com/pingcap/tidb/issues/40596) @[tiancaiamao](https://github.com/tiancaiamao)

+ TiKV

    - Fix the issue that TiKV does not resolve the `:` character correctly when parsing the cgroup path [#14538](https://github.com/tikv/tikv/issues/14538) @[SpadeA-Tang](https://github.com/SpadeA-Tang)

+ PD

    - (dup): release-6.1.4.md > Bug 修复> PD - 修复 PD 可能会非预期地向 Region 添加多个 Learner 的问题 [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - (dup): release-7.0.0.md > 错误修复> PD - 修复了切换 Placement Rule 时可能存在的 leader 分布不均衡的问题 [#6195](https://github.com/tikv/pd/issues/6195) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - (dup): release-6.1.6.md > Bug 修复> TiFlash - 修复 TiFlash 无法识别生成列的问题 [#6801](https://github.com/pingcap/tiflash/issues/6801) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-7.0.0.md > 错误修复> TiFlash - 修复了 Decimal 除法在某些情况下最后一位未进位的问题 [#7022](https://github.com/pingcap/tiflash/issues/7022) @[LittleFall](https://github.com/LittleFall)
    - (dup): release-7.0.0.md > 错误修复> TiFlash - 修复了 Decimal 转换在某些情况下进位错误的问题 [#6994](https://github.com/pingcap/tiflash/issues/6994) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.0.0.md > 错误修复> TiFlash - 修复了开启 new collation 后 TopN/Sort 算子结果可能出错的问题 [#6807](https://github.com/pingcap/tiflash/issues/6807) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue of TiFlash process failures due to TiCDC incompatibility [#7212](https://github.com/pingcap/tiflash/issues/7212) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-6.6.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复当 TiDB 集群不存在 PITR 备份任务时，`resolve lock` 频率过高的问题 [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - (dup): release-7.0.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复了在 PITR 恢复过程中等待 split Region 重试的时间不足的问题 [#42001](https://github.com/pingcap/tidb/issues/42001) @[joccau](https://github.com/joccau)

    + TiCDC

        - Fix the issue that the partition delimiter does not work when TiCDC replicates data to object storage [#8581](https://github.com/pingcap/tiflow/issues/8581) @[CharlesCheung96](https://github.com/CharlesCheung96) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that table scheduling might cause data loss when TiCDC replicates data to object storage [#8256](https://github.com/pingcap/tiflow/issues/8256) @[zhaoxinyu](https://github.com/zhaoxinyu)
        - Fix the issue that non-reentrant DDL statements get stuck [#8662](https://github.com/pingcap/tiflow/issues/8662) @[hicqu](https://github.com/hicqu)
        - Fix the issue that TiCDC scaling might cause data loss when TiCDC replicates data to object storage [#8666](https://github.com/pingcap/tiflow/issues/8666) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the memory limit of cgroup does not take effect in some scenarios  [#8588](https://github.com/pingcap/tiflow/issues/8588) @[amyangfei](https://github.com/amyangfei)
        - Fix the issue that data loss might occur in special cases during the apply of Redo log [#8591](https://github.com/pingcap/tiflow/issues/8591) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Introduce gomemlimit to prevent TiCDC from experiencing OOM issues [#8675](https://github.com/pingcap/tiflow/issues/8675) @[amyangfei](https://github.com/amyangfei)
        - Use the multi-statement approach to optimize the replication performance in scenarios involving batch execution of `UPDATE` statements [#8057](https://github.com/pingcap/tiflow/issues/8057) @[amyangfei](https://github.com/amyangfei)
        - (dup): release-6.1.6.md > Bug 修复> Tools> TiCDC - 修复 `db sorter` 使用内存时未受 `cgroup memory limit` 限制的问题 [#8588](https://github.com/pingcap/tiflow/issues/8588) @[amyangfei](https://github.com/amyangfei)
        - (dup): release-6.1.6.md > Bug 修复> Tools> TiCDC - 修复同步数据时由于 `UPDATE` 和 `INSERT` 语句乱序可能导致 `Duplicate entry` 错误的问题 [#8597](https://github.com/pingcap/tiflow/issues/8597) @[sdojjy](https://github.com/sojjy)
        - (dup): release-6.1.6.md > Bug 修复> Tools> TiCDC - 修复由于 PD 和 TiCDC 之间的网络隔离引起 TiCDC 程序异常退出的问题 [#8562](https://github.com/pingcap/tiflow/issues/8562) @[overvenus](https://github.com/overvenus)
        - (dup): release-7.0.0.md > 错误修复> Tools> TiCDC - 修复了 Kubernetes 上不能平滑升级 (graceful upgrade) TiCDC 集群的问题 [#8484](https://github.com/pingcap/tiflow/issues/8484) @[overvenus](https://github.com/overvenus)
        - (dup): release-7.0.0.md > 错误修复> Tools> TiCDC - 修复了当所有 Kafka server 不可访问时会导致 TiCDC server panic 的问题 [#8523](https://github.com/pingcap/tiflow/issues/8523) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-7.0.0.md > 错误修复> Tools> TiCDC - 修复了重启 changefeed 可能导致数据丢失或者 checkpoint 无法推进的问题 [#8242](https://github.com/pingcap/tiflow/issues/8242) @[overvenus](https://github.com/overvenus)

    + TiDB Data Migration (DM)

        - note 1

    + TiDB Lightning

        - note 1

    + Dumpling