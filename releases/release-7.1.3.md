---
title: TiDB 7.1.3 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.1.3.
---

# TiDB 7.1.3 Release Notes

Release date: x x, 2023

TiDB version: 7.1.3

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v7.1.3#version-list)

## Compatibility changes

<!-- **tw:@qiancai** 1 -->

- (dup): release-6.5.6.md > Compatibility changes - Prohibit setting [`require_secure_transport`](https://docs.pingcap.com/tidb/v6.5/system-variables#require_secure_transport-new-in-v610) to `ON` in Security Enhanced Mode (SEM) to prevent potential connectivity issues for users [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
- (dup): release-6.5.6.md > Compatibility changes - After further testing, the default value of the TiCDC Changefeed configuration item [`case-sensitive`](/ticdc/ticdc-changefeed-config.md) is changed from `true` to `false`. This means that by default, table and database names in the TiCDC configuration file are case-insensitive [#10047](https://github.com/pingcap/tiflow/issues/10047) @[sdojjy](https://github.com/sdojjy)
- (dup): release-6.5.6.md > Compatibility changes> TiCDC Changefeed introduces the following new configuration items: - [`compression`](/ticdc/ticdc-changefeed-config.md): enables you to configure the compression behavior of redo log files [#10176](https://github.com/pingcap/tiflow/issues/10176) @[sdojjy](https://github.com/sdojjy)
- (dup): release-6.5.6.md > Compatibility changes> TiCDC Changefeed introduces the following new configuration items: - [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md) and [`flush-worker-num`](/ticdc/ticdc-changefeed-config.md): enable you to set different concurrency parameters for the redo module based on specifications of different machines [#10048](https://github.com/pingcap/tiflow/issues/10048) @[CharlesCheung96](https://github.com/CharlesCheung96)
- (dup): release-6.5.6.md > Compatibility changes> TiCDC Changefeed introduces the following new configuration items: - [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md): enables you to set the automatic cleanup of historical data when replicating data to object storage [#10109](https://github.com/pingcap/tiflow/issues/10109) @[CharlesCheung96](https://github.com/CharlesCheung96)
- 将自动支持平滑升级功能修改成通过 `/upgrade/start` 和 `upgrade/finish` HTTP 接口支持此功能 @[zimulala](https://github.com/zimulala)

## Improvements

+ TiDB <!-- **tw:@oreoxmt** 2 -->

    - When a non-binary collation is set and the query condition includes `LIKE`, the optimizer generates an IndexRangeScan to improve the execution efficiency [#48181](https://github.com/pingcap/tidb/issues/48181) @[time-and-fate](https://github.com/time-and-fate)

+ TiKV

    - (dup): release-7.3.0.md > Improvements> TiKV - Add the `Max gap of safe-ts` and `Min safe ts region` metrics and introduce the `tikv-ctl get-region-read-progress` command to better observe and diagnose the status of resolved-ts and safe-ts [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)

+ PD

    - (dup): release-7.4.0.md > 改进提升> PD - 改进 resource control client 的配置获取方式，使其可以动态获取最新配置 [#7043](https://github.com/tikv/pd/issues/7043) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - (none)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-6.5.6.md > Improvements> Tools> Backup & Restore (BR) - Enable automatic retry of Region scatter during snapshot recovery when encountering timeout failures or cancellations of Region scatter [#47236](https://github.com/pingcap/tidb/issues/47236) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.0.md > Improvements> Tools> Backup & Restore (BR) - During restoring a snapshot backup, BR retries when it encounters certain network errors [#48528](https://github.com/pingcap/tidb/issues/48528) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.6.md > Improvements> Tools> Backup & Restore (BR) - Support the [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v6.5/sql-statement-flashback-cluster) syntax [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger)
        - (dup): release-6.5.6.md > Improvements> Tools> Backup & Restore (BR) - Introduce a new integration test for Point-In-Time Recovery (PITR) in the `delete range` scenario, enhancing PITR stability  [#47738](https://github.com/pingcap/tidb/issues/47738) @[Leavrth](https://github.com/Leavrth)

    + TiCDC <!-- **tw:@ran-huang** 5 -->

        - 优化同步到 tidb 场景下 CDC 节点的内存消耗 [#9935](https://github.com/pingcap/tiflow/issues/9935)
        - 优化部分报警规则 [#9266](https://github.com/pingcap/tiflow/issues/9266)
        - 优化了 Redo log 的相关性能，如并行写 S3 和采用压缩的模式。[#10176](https://github.com/pingcap/tiflow/issues/10176)[#10226](https://github.com/pingcap/tiflow/issues/10226)
        - 通过增加并行的方式优化了 CDC 同步到对象存储的性能[#10098](https://github.com/pingcap/tiflow/issues/10098)
        - (dup): release-6.5.6.md > Improvements> Tools> TiCDC - Reduce the impact of TiCDC incremental scanning on upstream TiKV [#11390](https://github.com/tikv/tikv/issues/11390) @[hicqu](https://github.com/hicqu)
        - (dup): release-6.5.6.md > Improvements> Tools> TiCDC - Support making TiCDC Canal-JSON content format [compatible with the content format of the official Canal output](https://docs.pingcap.com/tidb/v6.5/ticdc-canal-json#compatibility-with-the-official-canal) by setting `content-compatible=true` in the `sink-uri` configuration [#10106](https://github.com/pingcap/tiflow/issues/10106) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - (none)

    + TiDB Lightning <!-- **tw:@hfxsd** 1 -->

        - Add a retry mechanism for `GetTS` failure caused by PD leader change [#45301](https://github.com/pingcap/tidb/issues/45301) @[lance6716](https://github.com/lance6716)

    + Dumpling

        - (none)

    + TiUP

        - (none)

    + TiDB Binlog

        - (none)

## Bug fixes

+ TiDB

    <!-- **tw:@Oreoxmt** 12-->
    - Fix the issue that the query containing common table expressions (CTEs) unexpectedly gets stuck when the query is killed due to over-limit [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid})
    - Fix the issue that high CPU usage of TiDB occurs due to long-term memory pressure caused by `tidb_server_memory_limit` [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that queries containing CTEs report a `runtime error: index out of range [32] with length 32` error when `tidb_max_chunk_size` is set to a small value [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the query result is incorrect when an `ENUM` type column is used as the join key [#48991](https://github.com/pingcap/tidb/issues/48991) @[winoros](https://github.com/winoros)
    - Fix the parsing error caused by aggregate or window functions in recursive CTEs [#47711](https://github.com/pingcap/tidb/issues/47711) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that `UPDATE` statements might be incorrectly converted to PointGet [#47445](https://github.com/pingcap/tidb/issues/47445) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the OOM issue that might occur when TiDB performs garbage collection on the `stats_history` table [#48431](https://github.com/pingcap/tidb/issues/48431) @[hawkingrei](https://github.com/hawkingrei)
    <!-- **tw:@qiancai** 12 -->
    - 修复某些情况下相同的查询计划拥有不同的 digest 的问题 [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - 修复内存大量使用时无法 kill GenJSONTableFromStats 的问题 [#47779](https://github.com/pingcap/tidb/issues/47779) @[hawkingrei](https://github.com/hawkingrei)
    - 修复可能将过滤条件错误地下推到 CTE 的问题 [#47881](https://github.com/pingcap/tidb/issues/47881) @[winoros](https://github.com/winoros)
    - 修复 AUTO_ID_CACHE=1 时可能导致 Duplicate entry 的问题 [#46444](https://github.com/pingcap/tidb/issues/46444) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 TiDB server 在使用企业插件审计日志时可能导致高资源使用的问题 [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 TiDB server 在优雅关闭（graceful shutdown）时可能 panic 的问题 [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    - 修复在有大量表时，AUTO_ID_CACHE=1 表可能造成 gRPC 客户端泄漏的问题 [#48869](https://github.com/pingcap/tidb/issues/48869) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复使用 ErrLoadDataInvalidURI （使用无效的 S3 URL 的错误）的错误信息内容 [#48164](https://github.com/pingcap/tidb/issues/48164) @[lance6716](https://github.com/lance6716)
    - 修复了当分区列类型为 datetime 时，执行 "alter table ... last partition " 会失败的问题 [#48814](https://github.com/pingcap/tidb/issues/48814) @[crazycs520](https://github.com/crazycs520)
    - 修复了 "import into" 时，真实错误信息可能被其它错误覆盖的问题 [#47992](https://github.com/pingcap/tidb/issues/47992)，[#47781](https://github.com/pingcap/tidb/issues/47781) @[D3Hunter](https://github.com/D3Hunter)
    - 修复无法检测到 TiDB 部署在 cgroup v2 容器的问题 [#48342](https://github.com/pingcap/tidb/issues/48342) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-6.5.6.md > Bug fixes> TiDB - Fix the issue that executing `UNION ALL` with the DUAL table as the first subnode might cause an error [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.6.md > Bug fixes> TiDB - Fix the TiDB node panic issue that occurs when DDL `jobID` is restored to 0 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-6.5.6.md > Bug fixes> TiDB - Fix the issue of unsorted row data returned by `TABLESAMPLE` [#48253](https://github.com/pingcap/tidb/issues/48253) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.5.6.md > Bug fixes> TiDB - Fix the issue that panic might occur when `tidb_enable_ordered_result_mode` is enabled [#45044](https://github.com/pingcap/tidb/issues/45044) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.0.md > Bug fixes> TiDB - Fix the issue that the optimizer mistakenly selects IndexFullScan to reduce sort introduced by window functions [#46177](https://github.com/pingcap/tidb/issues/46177) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.6.md > Bug fixes> TiDB - Fix the issue of not handling locks in the MVCC interface when reading schema diff commit versions from the TiDB schema cache [#48281](https://github.com/pingcap/tidb/issues/48281) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-7.5.0.md > Bug fixes> TiDB - Fix the issue of incorrect memory usage estimation in `INDEX_LOOKUP_HASH_JOIN` [#47788](https://github.com/pingcap/tidb/issues/47788) @[SeaRise](https://github.com/SeaRise)
    - (dup): release-6.5.6.md > Bug fixes> TiDB - Fix the issue of `IMPORT INTO` task failure caused by PD leader malfunction for 1 minute [#48307](https://github.com/pingcap/tidb/issues/48307) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-7.5.0.md > Bug fixes> TiDB - Fix the panic issue of `batch-client` in `client-go` [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.6.md > Bug fixes> TiDB - Fix the issue that column pruning can cause panic in specific situations [#47331](https://github.com/pingcap/tidb/issues/47331) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-7.5.0.md > Bug fixes> TiDB - Fix the issue that TiDB does not read `cgroup` resource limits when it is started with `systemd` [#47442](https://github.com/pingcap/tidb/issues/47442) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.6.md > Bug fixes> TiDB - Fix the issue of possible syntax error when a common table expression (CTE) containing aggregate or window functions is referenced by other recursive CTEs [#47603](https://github.com/pingcap/tidb/issues/47603) [#47711](https://github.com/pingcap/tidb/issues/47711)  @[elsa0520](https://github.com/elsa0520)
    - (dup): release-6.5.6.md > Bug fixes> TiDB - Fix the panic issue that might occur when constructing TopN structure for statistics [#35948](https://github.com/pingcap/tidb/issues/35948) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-6.5.6.md > Bug fixes> TiDB - Fix the issue that the result of `COUNT(INT)` calculated by MPP might be incorrect [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.0.md > Bug fixes> TiDB - Fix the issue that the chunk cannot be reused when the HashJoin operator performs probe [#48082](https://github.com/pingcap/tidb/issues/48082) @[wshwsh12](https://github.com/wshwsh12)

+ TiKV <!-- **tw:@hfxsd** 4 -->

    - Fix the issue that if TiKV runs extremely slow, it might panic after Region merge [#16111](https://github.com/tikv/tikv/issues/16111) @[overvenus](https://github.com/overvenus)
    - Fix the issue that Resolved TS might be blocked for two hours [#15520](https://github.com/tikv/tikv/issues/15520) @[overvenus](https://github.com/overvenus)
    - Fix the issue that TiKV reports the `ServerIsBusy` error because it can not append the raft log [#15800](https://github.com/tikv/tikv/issues/15800) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Fix the issue that snapshot restore might get stuck when BR crashes [#15684](https://github.com/tikv/tikv/issues/15684) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that Resolved TS in stale read might cause TiKV OOM issues when tracking large transactions [#14864](https://github.com/tikv/tikv/issues/14864) @[overvenus](https://github.com/overvenus)
    - Fix the issue that damaged SST files might be spreaded to other TiKV nodes [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-6.5.6.md > Bug fixes> TiKV - Fix the issue that resolved-ts might be blocked for 2 hours [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.6.md > Bug fixes> TiKV - Fix the issue that the joint state of DR Auto-Sync might time out when scaling out [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-6.5.6.md > Bug fixes> TiKV - Fix the issue that the scheduler command variables are incorrect in Grafana on the cloud environment [#15832](https://github.com/tikv/tikv/issues/15832) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-6.5.6.md > Bug fixes> TiKV - Fix the issue that stale peers are retained and block resolved-ts after Regions are merged [#15919](https://github.com/tikv/tikv/issues/15919) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.5.md > Bug fixes> TiKV - Fix the issue that Online Unsafe Recovery cannot handle merge abort [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - (dup): release-6.5.6.md > Bug fixes> TiKV - Fix the TiKV OOM issue that occurs when restarting TiKV and there are a large number of Raft logs that are not applied [#15770](https://github.com/tikv/tikv/issues/15770) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.6.md > Bug fixes> TiKV - Fix security issues by upgrading the version of `lz4-sys` to 1.9.4  [#15621](https://github.com/tikv/tikv/issues/15621) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - (dup): release-6.5.6.md > Bug fixes> TiKV - Fix the issue that `blob-run-mode` in Titan cannot be updated online [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - (dup): release-6.5.4.md > Bug fixes> TiKV - Fix the issue that network interruption between PD and TiKV might cause PITR to get stuck [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - (dup): release-6.5.6.md > Bug fixes> TiKV - Fix the issue that TiKV coprocessor might return stale data when removing a Raft peer [#16069](https://github.com/tikv/tikv/issues/16069) @[overvenus](https://github.com/overvenus)

+ PD <!-- **tw:@hfxsd** 4 -->

    - Fix the issue that the `resource_manager_resource_unit` metric is empty in TiDB Dashboard when executing `CALIBRATE RESOURCE` [#45166](https://github.com/pingcap/tidb/issues/45166) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that the Calibrate by Workload page reports an error [#48162](https://github.com/pingcap/tidb/issues/48162) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that deleting a resource group can damage DDL atomicity [#45050](https://github.com/pingcap/tidb/issues/45050) @[glorv](https://github.com/glorv)
    - Fix the issue that when PD leader is transferred and there is a network partition between the new leader and the PD client, the PD client fails to update the information of the leader [#7416](https://github.com/tikv/pd/issues/7416) @[CabinfeverB](https://github.com/CabinfeverB)
    - (dup): release-7.5.0.md > Bug fixes> PD - Fix the issue that adding multiple TiKV nodes to a large cluster might cause TiKV heartbeat reporting to become slow or stuck [#7248](https://github.com/tikv/pd/issues/7248) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.0.md > Bug fixes> PD - Fix the issue that TiDB Dashboard cannot read PD `trace` data correctly [#7253](https://github.com/tikv/pd/issues/7253) @[nolouch](https://github.com/nolouch)
    - (dup): release-6.5.6.md > Bug fixes> PD - Upgrade the version of Gin Web Framework from v1.8.1 to v1.9.1 to fix some security issues [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)
    - (dup): release-7.5.0.md > Bug fixes> PD - Fix the issue that the rule checker does not add Learners according to the configuration of Placement Rules [#7185](https://github.com/tikv/pd/issues/7185) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.5.0.md > Bug fixes> PD - Fix the issue that PD might delete normal Peers when TiKV nodes are unavailable [#7249](https://github.com/tikv/pd/issues/7249) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-6.5.6.md > Bug fixes> PD - Fix the issue that it takes a long time to switch the leader in DR Auto-Sync mode [#6988](https://github.com/tikv/pd/issues/6988) @[HuSharp](https://github.com/HuSharp)

+ TiFlash <!-- **tw:@ran-huang** 4 -->

    - (dup): release-6.5.6.md > Bug fixes> TiFlash - Fix the issue that executing the `ALTER TABLE ... EXCHANGE PARTITION ...` statement causes panic [#8372](https://github.com/pingcap/tiflash/issues/8372) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复当查询遇到 memory limit 限制后发生内存泄漏的问题 [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - 修复在执行 `FLASHBACK DATABASE` 后 TiFlash 副本的数据仍会被 GC 回收的问题 [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 Grafana 中部分面板的最大分位数耗时显示不正确的问题 [#8076](https://github.com/pingcap/tiflash/issues/8076) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复查询非预期报错 `Block schema mismatch in FineGrainedShuffleWriter-V1` 的问题 [#8111](https://github.com/pingcap/tiflash/issues/8111}) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR) <!-- **tw:@hfxsd** 1 -->

        - (dup): release-6.5.6.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the default values for BR SQL commands and CLI are different, which might cause OOM issues [#48000](https://github.com/pingcap/tidb/issues/48000) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the log backup might get stuck in some scenarios when backing up large wide tables [#15714](https://github.com/tikv/tikv/issues/15714) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.6.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that BR generates incorrect URIs for external storage files [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.6.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the retry after an EC2 metadata connection reset cause degraded backup and restore performance [#46750](https://github.com/pingcap/tidb/issues/47650) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the log backup task can start but does not work properly if failing to connect to PD during task initialization [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC <!-- **tw:@ran-huang** 6 -->

        - 修复了在同步 delete 语句时某些场景下 where 条件没有采用主键作为条件的问题 [#9812](https://github.com/pingcap/tiflow/issues/9812)
        - 修复 Redo log 功能开启时，同步 DDL 语句间隔时间较长的问题 [#9960](https://github.com/pingcap/tiflow/issues/9960)
        - 修复在 BDR 模式时，delete & create 同名的 table 后，DML 不能正确同步的问题  [#10079](https://github.com/pingcap/tiflow/issues/10079)
        - 修复同步到对象存储时，某些特殊场景到值同步任务卡住的问题 [#10041](https://github.com/pingcap/tiflow/issues/10041)[#10044](https://github.com/pingcap/tiflow/issues/10044)
        - 修复在开启 sync-point & redo log 时在某些特殊场景下 ，同步任务卡住的问题 [#10091](https://github.com/pingcap/tiflow/issues/10091)
        - 修复了在某些特殊场景下，CDC 关闭与 tikv 的断开链接处理方式。[#10239](https://github.com/pingcap/tiflow/issues/10239)
        - (dup): release-6.5.6.md > Bug fixes> Tools> TiCDC - Fix the issue that the changefeed cannot replicate DML events in bidirectional replication mode if the target table is dropped and then recreated in upstream [#10079](https://github.com/pingcap/tiflow/issues/10079) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.5.0.md > Bug fixes> Tools> TiCDC - Fix the performance issue caused by accessing NFS directories when replicating data to an object store sink [#10041](https://github.com/pingcap/tiflow/issues/10041) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.5.6.md > Bug fixes> Tools> TiCDC - Fix the issue that the TiCDC server might panic when replicating data to an object storage service [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.6.md > Bug fixes> Tools> TiCDC - Fix the issue that the interval between replicating DDL statements is too long when redo log is enabled [#9960](https://github.com/pingcap/tiflow/issues/9960) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.5.0.md > Bug fixes> Tools> TiCDC - Fix the issue that an owner node gets stuck due to NFS failure when the redo log is enabled [#9886](https://github.com/pingcap/tiflow/issues/9886) @[3AceShowHand](https://github.com/3AceShowHand)
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM) <!-- **tw:@hfxsd** 1 -->

        - Fix the issue that DM performance is degraded due to an inappropriate algorithm used for `CompareGTID` [#9676](https://github.com/pingcap/tiflow/issues/9676) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning <!-- **tw:@hfxsd** 2 -->

        - Fix the issue that data import fails due to the PD leader being killed or slow processing of PD requests [#46950](https://github.com/pingcap/tidb/issues/46950) [#48075](https://github.com/pingcap/tidb/issues/48075) @[D3Hunter](https://github.com/D3Hunter)
        - (dup): release-6.5.6.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that TiDB Lightning gets stuck during `writeToTiKV` [#46321](https://github.com/pingcap/tidb/issues/46321) [#48352](https://github.com/pingcap/tidb/issues/48352) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.5.6.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that data import fails because HTTP retry requests do not use the current request content [#47930](https://github.com/pingcap/tidb/issues/47930) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.5.6.md > Bug fixes> Tools> TiDB Lightning - Remove unnecessary `get_regions` calls in physical import mode [#45507](https://github.com/pingcap/tidb/issues/45507) @[mittalrishabh](https://github.com/mittalrishabh)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
