---
title: TiDB 6.1.5 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.1.5.
---

# TiDB 6.1.5 Release Notes

Release date: February 28, 2023

TiDB version: 6.1.5

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.1.5#version-list)

## Compatibility changes

- Starting from February 20, 2023, the telemetry feature is disabled by default in new versions of TiDB and TiDB Dashboard, including v6.1.5, and usage information is not collected and shared with PingCAP. Before upgrading to these versions, if the cluster uses the default telemetry configuration, the telemetry feature is disabled after the upgrade. See [TiDB Release Timeline](/releases/release-timeline.md) for the specific version.

    - The default value of the [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-introduced-from-v402-version) system variable is changed from `ON` to `OFF`.
    - The default value of the TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-introduced-from-v402-version) configuration item is changed from `true` to `false`
    - The default value of the PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry) configuration item is changed from `true` to `false`.

- Starting from v1.11.3, the telemetry feature is disabled by default in newly deployed TiUP, and usage information is not collected. If you upgrade from a TiUP version earlier than v1.11.3 to v1.11.3 or a later version, the telemetry feature keeps the same status as before the upgrade.

## Improvements

- TiDB

    - dup Support the `AUTO_RANDOM` column as the first column of the clustered composite index [#38572](https://github.com/pingcap/tidb/issues/38572) @[tangenta](https://github.com/tangenta)

## Bug fixes

+ TiDB

    - 修复 data race 可能导致 TiDB 重启的问题 [#27725](https://github.com/pingcap/tidb/issues/27725) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复使用 Read Committed 隔离级别 update 时可能读不到最新数据的问题 [#41581](https://github.com/pingcap/tidb/issues/41581) @ [cfzjywxk](https://github.com/cfzjywxk)

- PD

    - dup 修复 PD 可能会非预期地向 Region 添加多个 Learner 的问题 [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - dup 修复调用 `ReportMinResolvedTS` 过于频繁导致 PD OOM 的问题 [#5965](https://github.com/tikv/pd/issues/5965) @[HundunDM](https://github.com/HunDunDM)

+ Tools

    + Backup & Restore (BR)

        - dup 修复使用 `br debug` 命令解析 backupmeta 文件导致的 panic 的问题 [#40878](https://github.com/pingcap/tidb/issues/40878) @[MoCuishle28](https://github.com/MoCuishle28)

    + TiCDC

        - 修复在延迟过大时 apply redo log 可能会出现 OOM 的问题 [#8085](https://github.com/pingcap/tiflow/issues/8085)
        - 修复部分 DML 执行出错时重试无效的逻辑 [#8087](https://github.com/pingcap/tiflow/issues/8087)
        - 修复开启 redo log 写 meta 时性能下降的问题 [#8074](https://github.com/pingcap/tiflow/issues/8074)

    + TiDB Data Migration (DM)

        - dup 修复 `binlog-schema delete` 命令执行失败的问题 [#7373](https://github.com/pingcap/tiflow/issues/7373) @[liumengya94](https://github.com/liumengya94)
        - dup 修复当最后一个 binlog 是被 skip 的 DDL 时，checkpoint 不推进的问题 [#8175](https://github.com/pingcap/tiflow/issues/8175) @[D3Hunter](https://github.com/D3Hunter)
