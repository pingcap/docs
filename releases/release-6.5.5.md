---
title: TiDB 6.5.5 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.5.
---

# TiDB 6.5.5 Release Notes

Release date: xx, 2023

TiDB version: 6.5.5

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.5#version-list)

## Improvements

+ TiDB **tw@qiancai**

    - 支持从高版本回退到 6.5 [#45570](https://github.com/pingcap/tidb/issues/45570) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-7.3.0.md > # 稳定性 * 新增部分优化器提示 [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)
    - 添加 coprocessor 相关 request source 信息 [#46514](https://github.com/pingcap/tidb/issues/46514) @[you06](https://github.com/you06)

+ TiKV **tw@qiancai**

    - 增加 pd-client中连接重试过程中backoff的功能，减小PD压力 [#15428](https://github.com/tikv/tikv/issues/15428) @[nolouch](https://github.com/nolouch)
    - Titan：避免写Titan manifest文件时持有锁 [#15351](https://github.com/tikv/tikv/issues/15351) @[Connor1996](https://github.com/Connor1996)
    - 压缩check_leader请求. [#14839](https://github.com/tikv/tikv/issues/14839) @[you06](https://github.com/you06)
    - 增加snapshot相关的监控 [#15401](https://github.com/tikv/tikv/issues/15401) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 当leader转移时提高PiTR checkpoint lag的稳定性. [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)
    - 增加safe-ts相关的日志和监控 [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - 更多resolved-ts相关的日志和监控. [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - (dup): release-7.3.0.md > 改进提升> TiKV - 添加 `Max gap of safe-ts` 和 `Min safe ts region` 监控项以及 `tikv-ctl get_region_read_progress` 命令，用于更好地观测和诊断 resolved-ts 和 safe-ts 的状态 [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)

+ Tools **tw@Oreoxmt**

    + Backup & Restore (BR)

        - 减少日志备份 resolve lock 的 cpu 开销 [40759](https://github.com/pingcap/tidb/issues/40759) @[3pointer](https://github.com/3pointer)

    + TiDB Lightning

        - 修复 TiDB Lightning 在目标服务器部署 TiCDC 时无法启动的问题 [#41040](https://github.com/pingcap/tidb/issues/41040) @[lance6716](https://github.com/lance6716)
        - 修复 TiDB Lightning 在 PD 拓扑变更时无法启动的问题 [#46688](https://github.com/pingcap/tidb/issues/46688) @[lance6716](https://github.com/lance6716)

## Bug fixes

+ TiDB **tw@Oreoxmt**

    - 修复读副本选择会可能选到不可用副本的问题 [#46198](https://github.com/pingcap/tidb/issues/46198) @[zyguan](https://github.com/zyguan)
    - 修复 Stale Read 和 Schema Cache 不适配导致额外开销的问题 [#43481](https://github.com/pingcap/tidb/issues/43481) @[crazycs520](https://github.com/crazycs520)

+ TiKV **tw@Oreoxmt**

    - 修复错误: 当tikv一个节点失败时，对应region的peers不应该不正确的进入休眠模式 [#14547](https://github.com/tikv/tikv/issues/14547) @[hicqu](https://github.com/hicqu)
    - 当size based split触发时发现没有可以分裂的key时，触发一次手动compaction用来消除过多的MVCC版本 [#15282](https://github.com/tikv/tikv/issues/15282) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复在线恢复数据时无法处理merge abort的问题 [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - 修复PiTR潜在可能被阻塞的问题，当PD和TiKV之间网络隔离时. [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)

+ PD **tw@ran-huang**

    - Fix the issue that the scheduler takes a long time to start up [#6920](https://github.com/tikv/pd/issues/6920) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that the logic for handling Leaders and Peers in Scatter Region is inconsistent [#6962](https://github.com/tikv/pd/issues/6962) @[bufferflies](https://github.com/bufferflies)

+ Tools

    + Backup & Restore (BR) **tw@ran-huang**

        - Fix the issue that restoring implicit primary keys by PITR might lead to conflicts [#46520](https://github.com/pingcap/tidb/issues/46520) @[3pointer](https://github.com/3pointer)
        - Fix the issue that an error occurs when PITR recovers the meta-kv [#46578](https://github.com/pingcap/tidb/issues/46578) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue of wrong integration test cases in br [#45561](https://github.com/pingcap/tidb/issues/46561) @[purelind](https://github.com/purelind)
        - (dup): release-7.0.0.md > 错误修复> Tools> Backup & Restore (BR) - Alleviate the issue that the latency of the PITR log backup progress increases when Region leadership migration occurs [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix the issue of high TiCDC replication latency caused by network isolation of PD nodes [#9565](https://github.com/pingcap/tiflow/issues/9565)
        - Fix the issue that TiCDC incorrectly changes the `UPDATE` operation to `INSERT` when using the CSV format [#9658](https://github.com/pingcap/tiflow/issues/9658)
        <!--以上 **tw@ran-huang**-->
        - Fix the issue that user passwords are recorded in some logs [#9690](https://github.com/pingcap/tiflow/issues/9690)
        - Fix the issue that using the SASL authentication might cause TiCDC to panic [#9669](https://github.com/pingcap/tiflow/issues/9669)
        - Fix the issue that TiCDC replication tasks might fail in some scenarios [#9685](https://github.com/pingcap/tiflow/issues/9685)[#9697](https://github.com/pingcap/tiflow/issues/9697)[#9695](https://github.com/pingcap/tiflow/issues/9695)[#9736](https://github.com/pingcap/tiflow/issues/9736)
        - Fix the issue that TiCDC cannot replicate tasks and recover quickly from TiKV node failures when there are a lot of Regions upstream [#9741](https://github.com/pingcap/tiflow/issues/9741)
         <!--以上 **tw@hfxsd**-->
    + TiDB Lightning **tw@hfxsd**

        - Fix the issue that TiDB Lightning fails to start when TiCDC is deployed on the target server [#41040](https://github.com/pingcap/tidb/issues/41040) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning fails to start when PD topology is changed [#46688](https://github.com/pingcap/tidb/issues/46688) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning cannot continue importing data after PD switching Leaders [#46540](https://github.com/pingcap/tidb/issues/46540) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.6.0.md > 错误修复> Tools> TiDB Lightning - Fix the issue that precheck cannot accurately detect the presence of a running TiCDC in the target cluster [#41040](https://github.com/pingcap/tidb/issues/41040) @[lance6716](https://github.com/lance6716)
