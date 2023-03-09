---
title: TiDB 6.5.1 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.1.
---

# TiDB 6.5.1 Release Notes

Release date: xx xx, 2023

TiDB version: 6.5.1

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.1#version-list)

## Compatibility changes

- Starting from February 20, 2023, the [telemetry feature](/telemetry.md) is disabled by default in new versions of TiDB and TiDB Dashboard, including v6.5.1, and usage information is not collected and shared with PingCAP. Before upgrading to these versions, if the cluster uses the default telemetry configuration, the telemetry feature is disabled after the upgrade. See [TiDB Release Timeline](/releases/release-timeline.md) for a specific version.

    - The default value of the [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402) system variable is changed from `ON` to `OFF`.
    - The default value of the TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) configuration item is changed from `true` to `false`.
    - The default value of the PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry) configuration item is changed from `true` to `false`.

- Starting from v1.11.3, the telemetry feature is disabled by default in newly deployed TiUP, and usage information is not collected. If you upgrade from a TiUP version earlier than v1.11.3 to v1.11.3 or a later version, the telemetry feature keeps the same status as before the upgrade.

- (dup: release-6.1.4.md > Compatibility changes> TiDB)- No longer support modifying column types on partitioned tables because of potential correctness issues [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss)

## 改进提升

+ TiDB

    - (dup: release-6.6.0.md > # DB operations)* Support specifying the SQL script executed upon TiDB cluster initialization [#35624](https://github.com/pingcap/tidb/issues/35624) @[morgo](https://github.com/morgo)

        When you start a TiDB cluster for the first time, you can specify the SQL script to be executed by configuring the command line parameter `--initialize-sql-file`. You can use this feature when you need to perform such operations as modifying the value of a system variable, creating a user, or granting privileges. For more information, see [documentation](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651).

    - (dup: release-6.6.0.md > Improvements> TiDB)- Clear expired region cache regularly to avoid memory leak and performance degradation [#40461](https://github.com/pingcap/tidb/issues/40461) @[sticnarf](https://github.com/sticnarf)
    - 添加 `-proxy protocol fallbackable` 选项，让 TiDB 可以处理客户端 IP 在 proxy 协议允许的 IP 列表中的原始连接。[#41409](https://github.com/pingcap/tidb/issues/41409) @[blacktear23](https://github.com/blacktear23)
    - 改进了 memory tracker 的准确度 [#40900](https://github.com/pingcap/tidb/issues/40900) [#40500](https://github.com/pingcap/tidb/issues/40500) @[wshwsh12](https://github.com/wshwsh12)
    - 当 Plan Cache 无法生效时通过 Warning 返回原因 [#40210](https://github.com/pingcap/tidb/issues/40210) @[qw4990](https://github.com/qw4990)
    - 条件优化器在进行越界估算时的策略 [#39011](https://github.com/pingcap/tidb/issues/39011) @[time-and-fate](https://github.com/time-and-fate)

+ TiKV

    - (dup: release-6.6.0.md > Improvements> TiKV)- Support starting TiKV on a CPU with less than 1 core [#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @[andreid-db](https://github.com/andreid-db)
    - 提高unified read pool的线程上限至CPU vCore的10倍 [#13690](https://github.com/tikv/tikv/issues/13690) @[v01dstar](https://github.com/v01dstar)
    - 延长resolved-ts.advance-ts-interval到20s， 从而节省跨域流量 [#14100](https://github.com/tikv/tikv/issues/14100) @[overvenus](https://github.com/overvenus)

+ TiFlash

    - 显著提升 TiFlash 在大数据量下的启动速度 [#6395](https://github.com/pingcap/tiflash/issues/6395) @[hehechen](https://github.com/hehechen)

+ Tools

    + Backup & Restore (BR)

        - (dup: release-6.6.0.md > Improvements> Tools> Backup & Restore (BR))- Optimize the concurrency of downloading log backup files on the TiKV side to improve the performance of PITR recovery in regular scenarios [#14206](https://github.com/tikv/tikv/issues/14206) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - (dup: release-6.6.0.md > Improvements> Tools> TiCDC)- Support batch `UPDATE` DML statements to improve TiCDC replication performance [#8084](https://github.com/pingcap/tiflow/issues/8084) @[amyangfei](https://github.com/amyangfei)
        - (dup: release-6.1.4.md > Improvements> Tools> TiCDC)- Support storing redo logs to GCS- or Azure-compatible object storage [#7987](https://github.com/pingcap/tiflow/issues/7987) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup: release-6.6.0.md > Improvements> Tools> TiCDC)- Implement MQ sink and MySQL sink in the asynchronous mode to improve the sink throughput [#5928](https://github.com/pingcap/tiflow/issues/5928) @[amyangfei](https://github.com/amyangfei) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 错误修复

+ TiDB

    - (dup: release-6.1.4.md > Bug fixes> TiDB)- Fix the issue that the [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600) configuration item does not take effect for point-get queries [#39928](https://github.com/pingcap/tidb/issues/39928) @[zyguan](https://github.com/zyguan)
    - (dup: release-6.1.4.md > Bug fixes> TiDB)- Fix the issue that the `INSERT` or `REPLACE` statements might panic in long session connections [#40351](https://github.com/pingcap/tidb/issues/40351) @[winoros](https://github.com/winoros)
    - (dup: release-6.6.0.md > Bug fixes> TiDB)- Fix the issue that `auto analyze` causes graceful shutdown to take a long time [#40038](https://github.com/pingcap/tidb/issues/40038) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - (dup: release-6.6.0.md > Bug fixes> TiDB)- Fix the issue that data race might occur during DDL ingestion [#40970](https://github.com/pingcap/tidb/issues/40970) @[tangenta](https://github.com/tangenta)
    - (dup: release-6.6.0.md > Bug fixes> TiDB)- Fix the issue that data race might occur when an index is added [#40879](https://github.com/pingcap/tidb/issues/40879) @[tangenta](https://github.com/tangenta)
    - (dup: release-6.6.0.md > Bug fixes> TiDB)- Fix the issue that the adding index operation is inefficient due to invalid Region cache when there are many Regions in a table [#38436](https://github.com/pingcap/tidb/issues/38436) @[tangenta](https://github.com/tangenta)
    - (dup: release-6.6.0.md > Bug fixes> TiDB)- Fix the issue that TiDB might deadlock during initialization [#40408](https://github.com/pingcap/tidb/issues/40408) @[Defined2014](https://github.com/Defined2014)
    - (dup: release-6.6.0.md > Bug fixes> TiDB)- Fix the issue that unexpected data is read because TiDB improperly handles `NULL` values when constructing key ranges [#40158](https://github.com/pingcap/tidb/issues/40158) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup: release-6.6.0.md > Bug fixes> TiDB)- Fix the issue that the value of system variables might be incorrectly modified in some cases due to memory reuse [#40979](https://github.com/pingcap/tidb/issues/40979) @[lcwangchao](https://github.com/lcwangchao)
    - (dup: release-6.6.0.md > Bug fixes> TiDB)- Fix the issue that a TTL task fails if the primary key of the table contains an `ENUM` column [#40456](https://github.com/pingcap/tidb/issues/40456) @[lcwangchao](https://github.com/lcwangchao)
    - (dup: release-6.6.0.md > Bug fixes> TiDB)- Fix the issue that TiDB panics when adding a unique index [#40592](https://github.com/pingcap/tidb/issues/40592) @[tangenta](https://github.com/tangenta)
    - (dup: release-6.6.0.md > Bug fixes> TiDB)- Fix the issue that some truncate operations cannot be blocked by MDL when truncating the same table concurrently [#40484](https://github.com/pingcap/tidb/issues/40484) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup: release-6.6.0.md > Bug fixes> TiDB)- Fix the issue that TiDB cannot restart after global bindings are created for partition tables in dynamic trimming mode [#40368](https://github.com/pingcap/tidb/issues/40368) @[Yisaer](https://github.com/Yisaer)
    - (dup: release-6.1.4.md > Bug fixes> TiDB)- Fix the issue that reading data using the "cursor read" method might return an error because of GC [#39447](https://github.com/pingcap/tidb/issues/39447) @[zyguan](https://github.com/zyguan)
    - Fix the issue that `EXECUTE` is missing in the result of `SHOW PROCESSLIST` [#41156](https://github.com/pingcap/tidb/issues/41156) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that when `globalMemoryControl` is killing a query, the `KILL` operation might not end [#41057](https://github.com/pingcap/tidb/issues/41057) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that TiDB might panic after `indexMerge` encounters an error [#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @[guo-shaoge](https://github.com/guo-shaoge) @[windtalker](https://github.com/windtalker)
    - Fix the issue that the `ANALYZE` statement might be terminated by `KILL` [#41825](https://github.com/pingcap/tidb/issues/41825) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that gorountine leak might occur in `indexMerge` [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue of potential wrong results when comparing unsigned `TINYINT`/`SMALLINT`/`INT` with `DECIMAL`/`FLOAT`/`DOUBLE` that is smaller than `0` [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - Fix the issue that enabling `tidb_enable_reuse_chunk` might lead to memory leak [#40987](https://github.com/pingcap/tidb/issues/40987) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that data race in time zone might cause data-index inconsistency [#40710](https://github.com/pingcap/tidb/issues/40710) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the scan detail information during the execution of `batch cop` might be inaccurate [#41582](https://github.com/pingcap/tidb/issues/41582) @[you06](https://github.com/you06)
    - Fix the issue that the upper concurrency of `cop` is not limited [#41134](https://github.com/pingcap/tidb/issues/41134) @[you06](https://github.com/you06)
    - Fix the issue that the `statement context` in `cursour read` is mistakenly cached [#39998](https://github.com/pingcap/tidb/issues/39998) @[zyguan](https://github.com/zyguan)
    - Periodically clean up stale Region cache to avoid memory leak and performance degradation [#40355](https://github.com/pingcap/tidb/issues/40355) @[sticnarf](https://github.com/sticnarf)
    - Fix the issue that using plan cache on queries that contain `year <cmp> const` might go wrong [#41628](https://github.com/pingcap/tidb/issues/41628) @[qw4990](https://github.com/qw4990)
    - 修复查询区间太多且数据改动量大时估算误差可能较大的问题 [#40472](https://github.com/pingcap/tidb/issues/40472) @[time-and-fate](https://github.com/time-and-fate)
    - 修复使用 Plan Cache 时部分条件无法被下推过 Join 算子的问题 [#40218](https://github.com/pingcap/tidb/issues/40218) @[qw4990](https://github.com/qw4990)
    - 修复 IndexMerge 计划在 SET 类型列上可能生成错误区间的问题 [#41361](https://github.com/pingcap/tidb/issues/41361) @[time-and-fate](https://github.com/time-and-fate)
    - 修复 Plan Cache 处理 `int_col <cmp> decimal` 条件时可能缓存 FullScan 计划的问题 [#41136](https://github.com/pingcap/tidb/issues/41136) @[qw4990](https://github.com/qw4990)
    - 修复 Plan Cache 处理 `int_col in (decimal...)` 条件时可能缓存 FullScan 计划的问题 [#40312](https://github.com/pingcap/tidb/issues/40312) @[qw4990](https://github.com/qw4990)
    - 修复 `ignore_plan_cache` hint 对 Insert 语句可能不生效的问题 [#40080](https://github.com/pingcap/tidb/issues/40080) @[qw4990](https://github.com/qw4990)
    - 修复 Auto Analyze 可能阻碍 TiDB 退出的问题 [#40284](https://github.com/pingcap/tidb/issues/40284) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复在分区表的 Unsigned Primary Key 上可能构造错误访问区间的问题 [#40313](https://github.com/pingcap/tidb/issues/40313) @[winoros](https://github.com/winoros)
    - 修复 Plan Cache 可能缓存 Shuffle 算子导致返回错误结果的问题 [#41185](https://github.com/pingcap/tidb/issues/41185) @[qw4990](https://github.com/qw4990)
    - 修复在分区表上创建 Global Binding 后可能导致 TiDB 启动错误的问题 [#40402](https://github.com/pingcap/tidb/issues/40402) @[Yisaer](https://github.com/Yisaer)
    - 修复慢日志中查询计划算子可能缺失的问题 [#41461](https://github.com/pingcap/tidb/issues/41461) @[time-and-fate](https://github.com/time-and-fate)
    - 修复错误下推包含虚拟列的 TopN 算子到 TiKV/TiFlash 导致结果错误的问题 [#41370](https://github.com/pingcap/tidb/issues/41370) @[Dousir9](https://github.com/Dousir9)
    - 修复添加索引时数据不一致的问题 [#40698](https://github.com/pingcap/tidb/issues/40698）[#40730](https://github.com/pingcap/tidb/issues/40730）[#41459](https://github.com/pingcap/tidb/issues/41459）[#40464](https://github.com/pingcap/tidb/issues/40464）[#40217](https://github.com/pingcap/tidb/issues/40217）@[tangenta](https://github.com/tangenta)
    - 修复添加索引时 Pessimistic lock not found 的报错问题 [#41515](https://github.com/pingcap/tidb/issues/41515) @[tangenta](https://github.com/tangenta)
    - 修复添加唯一索引时误报重复键的问题 [#41630](https://github.com/pingcap/tidb/issues/41630) @[tangenta](https://github.com/tangenta)
    - 修复 TiDB 使用 `paging` 时性能下降的问题 [#40741](https://github.com/pingcap/tidb/issues/40741) @[solotzg](https://github.com/solotzg)

+ TiKV

    - (dup: release-6.6.0.md > Bug fixes> TiKV)- Fix the issue that Resolved TS causes higher network traffic [#14092](https://github.com/tikv/tikv/issues/14092) @[overvenus](https://github.com/overvenus)
    - (dup: release-6.1.4.md > Bug fixes> TiKV)- Fix the data inconsistency issue caused by network failure between TiDB and TiKV during the execution of a DML after a failed pessimistic DML [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)
    - (dup: release-6.6.0.md > Bug fixes> TiKV)- Fix an error that occurs when casting the `const Enum` type to other types [#14156](https://github.com/tikv/tikv/issues/14156) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 cop task paging 计算相关问题 [#14254](https://github.com/tikv/tikv/issues/14254)  @[you06](https://github.com/you06)
    - 修复 batch cop scan details 不准确问题 [#14109](https://github.com/tikv/tikv/issues/14109) @[you06](https://github.com/you06)
    - 修复Raft-Engine一个潜在的错误可能导致TiKV因检测到Raft数据corrupt而无法重启[#14338](https://github.com/tikv/tikv/issues/14338) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD

    - (dup: release-6.6.0.md > Bug fixes> PD)- Fix the issue that the execution `replace-down-peer` slows down under certain conditions [#5788](https://github.com/tikv/pd/issues/5788) @[HundunDM](https://github.com/HunDunDM)
    - (dup: release-6.1.4.md > Bug fixes> PD)- Fix the issue that PD might unexpectedly add multiple Learners to a Region [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - (dup: release-6.6.0.md > Bug fixes> PD)- Fix the issue that the Region Scatter task generates redundant replicas unexpectedly [#5909](https://github.com/tikv/pd/issues/5909) @[HundunDM](https://github.com/HunDunDM)
    - (dup: release-6.1.5.md > Bug fixes> PD)- Fix the PD OOM issue that occurs when the calls of `ReportMinResolvedTS` are too frequent [#5965](https://github.com/tikv/pd/issues/5965) @[HundunDM](https://github.com/HunDunDM)
    - 修复 region scatter 接口会导致 leader 分布不均匀的问题  [#6017](https://github.com/tikv/pd/issues/6017) @[HunDunDM](https://github.com/HunDunDM)

+ TiFlash

    - (dup: release-6.6.0.md > Bug fixes> TiFlash)- Fix the issue that semi-joins use excessive memory when calculating Cartesian products [#6730](https://github.com/pingcap/tiflash/issues/6730) @[gengliqi](https://github.com/gengliqi)
    - 修复 TiFlash 日志搜索过慢的问题 [#6829](https://github.com/pingcap/tiflash/issues/6829) @[hehechen](https://github.com/hehechen)
    - 修复 TiFlash 在反复重启后由于文件错误被删除而无法启动的问题 [#6486](https://github.com/pingcap/tiflash/issues/6486) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 可能在添加新列后查询报错的问题 [#6726](https://github.com/pingcap/tiflash/issues/6726) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 配置不支持 ipv6 的问题 [#6734](https://github.com/pingcap/tiflash/issues/6734) @[ywqzzy](https://github.com/ywqzzy)

+ Tools

    + Backup & Restore (BR)

        - (dup: release-6.6.0.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that the connection failure between PD and tidb-server causes PITR backup progress not to advance [#41082](https://github.com/pingcap/tidb/issues/41082) @[YuJuncen](https://github.com/YuJuncen)
        - (dup: release-6.6.0.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that TiKV cannot listen to PITR tasks due to the connection failure between PD and TiKV [#14159](https://github.com/tikv/tikv/issues/14159) @[YuJuncen](https://github.com/YuJuncen)
        - (dup: release-6.6.0.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that PITR does not support configuration changes for PD clusters [#14165](https://github.com/tikv/tikv/issues/14165) @[YuJuncen](https://github.com/YuJuncen)
        - (dup: release-6.6.0.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that the PITR feature does not support CA-bundles [#38775](https://github.com/pingcap/tidb/issues/38775) @[3pointer](https://github.com/3pointer)
        - (dup: release-6.6.0.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that when a PITR backup task is deleted, the residual backup data causes data inconsistency in new tasks [#40403](https://github.com/pingcap/tidb/issues/40403) @[joccau](https://github.com/joccau)
        - (dup: release-6.1.4.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that causes panic when BR debugs the `backupmeta` file [#40878](https://github.com/pingcap/tidb/issues/40878) @[MoCuishle28](https://github.com/MoCuishle28)
        - (dup: release-6.1.4.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that restore is interrupted due to failure in getting the Region size [#36053](https://github.com/pingcap/tidb/issues/36053) @[YuJuncen](https://github.com/YuJuncen)
        - (dup: release-6.6.0.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that the frequency of `resolve lock` is too high when there is no PITR backup task in the TiDB cluster [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - (dup: release-6.6.0.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that restoring data to a cluster on which the log backup is running causes the log backup file to be unrecoverable [#40797](https://github.com/pingcap/tidb/issues/40797) @[Leavrth](https://github.com/Leavrth)
        - 修复全量备份失败后，从断点重启备份 panic 的问题 [#40704](https://github.com/pingcap/tidb/issues/40704) @[Leavrth](https://github.com/Leavrth)
        - 修复 PITR 错误被覆盖的问题 [#40576](https://github.com/pingcap/tidb/issues/40576)@[Leavrth](https://github.com/Leavrth)
        - 修复 PITR 备份任务在 advance owner 与 gc owner 不同情况下 checkpoint 不推进的问题 [#41806](https://github.com/pingcap/tidb/issues/41806) @[joccau](https://github.com/joccau)

    + TiCDC

        - (dup: release-6.6.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that changefeed might get stuck in special scenarios such as when scaling in or scaling out TiKV or TiCDC nodes [#8174](https://github.com/pingcap/tiflow/issues/8174) @[hicqu](https://github.com/hicqu)
        - (dup: release-6.6.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that precheck is not performed on the storage path of redo log [#6335](https://github.com/pingcap/tiflow/issues/6335) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup: release-6.6.0.md > Bug fixes> Tools> TiCDC)- Fix the issue of insufficient duration that redo log can tolerate for S3 storage failure [#8089](https://github.com/pingcap/tiflow/issues/8089)  @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup: release-6.1.4.md > Bug fixes> Tools> TiCDC)- Fix the issue that `transaction_atomicity` and `protocol` cannot be updated via the configuration file [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup: release-6.1.4.md > Bug fixes> Tools> TiCDC)- Fix the issue that the checkpoint cannot advance when TiCDC replicates an excessively large number of tables [#8004](https://github.com/pingcap/tiflow/issues/8004) @[overvenus](https://github.com/overvenus)
        - (dup: release-6.1.5.md > Bug fixes> Tools> TiCDC)- Fix the issue that applying redo log might cause OOM when the replication lag is excessively high [#8085](https://github.com/pingcap/tiflow/issues/8085) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup: release-6.1.5.md > Bug fixes> Tools> TiCDC)- Fix the issue that the performance degrades when redo log is enabled to write meta [#8074](https://github.com/pingcap/tiflow/issues/8074) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup: release-6.1.4.md > Bug fixes> Tools> TiCDC)- Fix a bug that the context deadline is exceeded when TiCDC replicates data without splitting large transactions [#7982](https://github.com/pingcap/tiflow/issues/7982) @[hi-rustin](https://github.com/hi-rustin)
        - 默认打开 pull-based sink 功能提升系统的吞吐 [#8232](https://github.com/pingcap/tiflow/issues/8232) @[hi-rustin](https://github.com/hi-rustin)
        - 修复在PD 异常时，暂停一个 changefeed 会错误设置状态的问题 [#8330](https://github.com/pingcap/tiflow/issues/8330) @[sdojjy](https://github.com/sdojjy)
        - 修复下游为 tidb/mysql ，无主键且非空唯一索引所在列指定了 CHARACTER SET 同步时可能会出现数据不一致的问题。[#8420](https://github.com/pingcap/tiflow/issues/8420) @[asddongmen](https://github.com/asddongmen)
        - Fix panics about table scheduling or blackhole sink [#8024](https://github.com/pingcap/tiflow/issues/8024) [#8142](https://github.com/pingcap/tiflow/issues/8142) @[hicqu](https://github.com/hicqu)

    + TiDB Data Migration (DM)

        - (dup: release-6.1.5.md > Bug fixes> Tools> TiDB Data Migration (DM))- Fix the issue that the `binlog-schema delete` command fails to execute [#7373](https://github.com/pingcap/tiflow/issues/7373) @[liumengya94](https://github.com/liumengya94)
        - (dup: release-6.1.5.md > Bug fixes> Tools> TiDB Data Migration (DM))- Fix the issue that the checkpoint does not advance when the last binlog is a skipped DDL [#8175](https://github.com/pingcap/tiflow/issues/8175) @[D3Hunter](https://github.com/D3Hunter)
        - (dup: release-6.1.4.md > Bug fixes> Tools> TiDB Data Migration (DM))- Fix a bug that when the expression filters of both "update" and "non-update" types are specified in one table, all `UPDATE` statements are skipped [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - (dup: release-6.1.4.md > Bug fixes> Tools> TiDB Lightning)- Fix the issue that TiDB Lightning prechecks cannot find dirty data left by previously failed imports [#39477](https://github.com/pingcap/tidb/issues/39477) @[dsdashun](https://github.com/dsdashun)
        - (dup: release-6.6.0.md > Bug fixes> Tools> TiDB Lightning)- Fix the issue that TiDB Lightning panics in the split-region phase [#40934](https://github.com/pingcap/tidb/issues/40934) @[lance6716](https://github.com/lance6716)
        - (dup: release-6.6.0.md > Bug fixes> Tools> TiDB Lightning)- Fix the issue that the conflict resolution logic (`duplicate-resolution`) might lead to inconsistent checksums [#40657](https://github.com/pingcap/tidb/issues/40657) @[gozssky](https://github.com/gozssky)
        - (dup: release-6.6.0.md > Bug fixes> Tools> TiDB Lightning)- Fix the issue that TiDB Lightning might incorrectly skip conflict resolution when all but the last TiDB Lightning instance encounters a local duplicate record during a parallel import [#40923](https://github.com/pingcap/tidb/issues/40923) @[lichunzhu](https://github.com/lichunzhu)
        - 修复了在使用 Local Backend 模式导入数据时，当导入目标表的复合主键中存在 `auto_random` 列，且源数据中没有指定该列的值时，相关列没有自动生成数据的问题。[#41454](https://github.com/pingcap/tidb/issues/41454) @[D3Hunter](https://github.com/D3Hunter)