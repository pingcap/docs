---
title: TiDB 6.5.8 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.8.
---

# TiDB 6.5.8 Release Notes

Release date: xx xx, 2024

TiDB version: 6.5.8

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.8#version-list)

## Compatibility changes

<--tw @Oreoxmt (1)-->
- Introduce the TiKV configuration item [`gc.num-threads`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#num-threads-new-in-v658) to set the number of GC threads when `enable-compaction-filter` is `false`  [#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)

## Improvements

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiKV

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiFlash

    - (dup): release-7.6.0.md > 改进提升> TiFlash - Reduce the impact of background GC tasks on read and write task latency [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiCDC
        <--tw @qiancai (1)-->
        - Support [querying the downstream synchronization status of a changefeed](https://docs.pingcap.com/zh/tidb/v6.5/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed), which helps you determine whether the upstream data changes received by TiCDC have been synchronized to the downstream system completely [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning
        <--tw @hfxsd (1)-->
        - Improve performance of `ALTER TABLE` when importing a large number of tables [#50105](https://github.com/pingcap/tidb/issues/50105) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## Bug fixes

+ TiDB
    <--tw @Oreoxmt (6)-->
    - (dup): release-7.6.0.md > 错误修复> TiDB - Fix the issue that enforced sorting might become ineffective when a query uses optimizer hints (such as `STREAM_AGG()`) that enforce sorting and its execution plan contains `IndexMerge` [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.6.0.md > 错误修复> TiDB - Fix the issue that histogram statistics might not be parsed into readable strings when the histogram boundary contains `NULL` [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.6.0.md > 错误修复> TiDB - Fix the issue that hints cannot be used in `REPLACE INTO` statements [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.6.0.md > 错误修复> TiDB - Fix the issue that query results are incorrect due to `STREAM_AGG()` incorrectly handling CI [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the query result of a range partitioned table is incorrect in some cases due to wrong partition pruning [#50082](https://github.com/pingcap/tidb/issues/49823) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the auto-increment ID allocation reports an error due to concurrent conflicts when using an auto-increment column with `AUTO_ID_CACHE=1` [#50519](https://github.com/pingcap/tidb/issues/50519) @[tiancaiamao](https://github.com/tiancaiamao)
    - Mitigate the issue that TiDB nodes might encounter OOM errors when dealing with a large number of tables or partitions [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    - Fix the issue that data is inconsistent under the TiDB Distributed eXecution Framework (DXF) when executing `ADD INDEX` after the DDL Owner is network isolated [#49773](https://github.com/pingcap/tidb/issues/49773) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TiDB might panic when a query contains the Apply operator and the `fatal error: concurrent map writes` error occurs [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue that the COMMIT or ROLLBACK operation executed through `COM_STMT_EXECUTE` fails to terminate transactions that have timeout [#49151](https://github.com/pingcap/tidb/issues/49151) @[zyguan](https://github.com/zyguan)
    <--tw @hfxsd (3)-->
    - Fix the issue that executing `SELECT INTO OUTFILE` using the `PREPARE` method returns success instead of an error [#49166](https://github.com/pingcap/tidb/issues/49166) @[qw4990](https://github.com/qw4990)
    - Fix the issue that executing `UNIQUE` index lookup with `ORDER BY` might cause an error [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    - Fix the issue that the `DELETE` and `UPDATE` statements using index lookup might report an error when `tidb_multi_statement_mode` mode is enabled [#50012](https://github.com/pingcap/tidb/issues/50012) @[tangenta](https://github.com/tangenta)
    <--tw @ran-huang (3)-->
    - 修复短时间发送大量 DDL 语句时，CREATE TABLE 语句可能不会同步建立该表对心的统计信息元信息的问题 [#36004](https://github.com/pingcap/tidb/issues/36004) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复 LEADING hint 在 UNION ALL 语句中无法生效的问题 [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    - 修复使用旧接口导致表元信息可能不一致的问题 [#49751](https://github.com/pingcap/tidb/issues/49751) @[hawkingrei](https://github.com/hawkingrei)
    <--tw @qiancai (2)-->
    - Fix the issue that common hints do not take effect in `UNION ALL` statements [#50068](https://github.com/pingcap/tidb/issues/50068) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that TiDB returns wrong query results when processing invalid values in `ENUM` or `SET` types. This issue is caused by the fix for [#49487](https://github.com/pingcap/tidb/issues/49487) in v6.5.7 [#49440](https://github.com/pingcap/tidb/issues/49440) in TiDB 6.5.7 @[winoros](https://github.com/winoros)

+ TiKV

    - (dup): release-7.6.0.md > 错误修复> TiKV - Fix the issue that TiKV might panic when gRPC threads are checking `is_shutdown` [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)
    - (dup): release-7.6.0.md > 错误修复> TiKV - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.6.0.md > 错误修复> TiKV - Fix the issue that TiDB and TiKV might produce inconsistent results when processing `DECIMAL` arithmetic multiplication truncation [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)

+ PD
    <--tw @hfxsd (1)-->
    - Fix the issue that `pd-ctl` querying a Region without a leader might lead to PD to panic [#7630](https://github.com/tikv/pd/issues/7630) @[rleungx](https://github.com/rleungx)

+ TiFlash
    <--tw @hfxsd (2)-->
    - (dup): release-7.6.0.md > 错误修复> TiFlash - Fix the issue that the `lowerUTF8` and `upperUTF8` functions do not allow characters in different cases to occupy different bytes [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that after converting nullable columns to non-nullable ones, executing `ALTER TABLE ... MODIFY COLUMN ... NOT NULL` causes TiFlash to panic [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that after killing the query, TiFlash crashes due to concurrent data conflict when a large number of tasks on TiFlash are canceled at the same time [#7432](https://github.com/pingcap/tiflash/issues/7432) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR)
        <--tw @ran-huang (2)-->
        - (dup): release-7.6.0.md > 错误修复> Tools> Backup & Restore (BR) - Fix the issue that the `Unsupported collation` error is reported when you restore data from backups of an old version [#49466](https://github.com/pingcap/tidb/issues/49466) @[3pointer](https://github.com/3pointer)
        - 修复了从 S3 读文件内容时出错但无法重试的问题 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)
        - 修复了在同一节点上更改 TiKV IP 地址导致日志备份卡住的问题 [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)

    + TiCDC
        <--tw @qiancai (4)-->
        - Fix the issue that after filtering out `add table partition` events is configured in `ignore-event`, TiCDC does not replicate other types of DML changes for related partitions to the downstream [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the changefeed reports an error after `TRUNCATE PARTITION` is executed on the upstream table [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that the changefeed `resolved ts` does not advance in extreme cases [#10157](https://github.com/pingcap/tiflow/issues/10157) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC returns the `ErrChangeFeedAlreadyExists` error when concurrently creating multiple changefeeds [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning
        <--tw @ran-huang (2)-->
        - 修复 EBS BR 运行时 Lightning 可能导入失败的问题 [#49517](https://github.com/pingcap/tidb/issues/49517) @[mittalrishabh](https://github.com/mittalrishabh)
        - 修复以 MultiIngest 模式导入数据到 TiKV 时，数据可能丢失的问题 [#50198](https://github.com/pingcap/tidb/issues/50198) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
