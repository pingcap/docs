---
title: TiDB Smooth Upgrade
summary: This document introduces the smooth upgrade feature of TiDB, which supports upgrading TiDB clusters without manually canceling DDL operations.
---

# TiDB Smooth Upgrade

> **Warning:**
>
> Smooth upgrade is still an experimental feature.

This document introduces the smooth upgrade feature of TiDB, which supports upgrading TiDB clusters without manually canceling DDL operations.

You can upgrade from TiDB v7.1.0 to a higher version with the smooth upgrade feature, which removes the restrictions during the upgrade process and provides a smoother upgrade experience. This feature is enabled by default and cannot be disabled.

## Feature introduction

Before the smooth upgrade feature is introduced, there are the following restrictions on DDL operations during the upgrade process (see the *warning* section in [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md#upgrade-tidb-using-tiup)):

- Running DDL operations during the upgrade process might cause undefined behavior in TiDB.
- Upgrading TiDB during the DDL operation might cause undefined behavior in TiDB.

After the smooth upgrade feature is enabled, the upgrade process is no longer restricted by the above limitations.

During the upgrade process, TiDB automatically performs the following operations without user intervention:

1. Pauses user DDL operations.
2. Performs system DDL operations during the upgrade process.
3. Resumes the paused user DDL operations.
4. Completes the upgrade.

The resumed DDL jobs are still executed in the order before the upgrade.

## Limitations

When using the smooth upgrade feature, note the following limitations.

### Limitations on user operations

* Before upgrading, if there is a canceling DDL job in the cluster, that is, an ongoing DDL job is canceled by the user, because the job in the canceling state cannot be paused, TiDB will retry. If the retry fails, an error is reported and the upgrade is exited.

* During the upgrade, the following operations are not allowed:

    * Run DDL operations on system tables (`mysql.*`, `information_schema.*`, `performance_schema.*`, `metrics_schema.*`).

    * Manually cancel, pause, or resume DDL jobs: `ADMIN CANCEL/PAUSE/RESUME DDL JOBS job_id [, job_id] ...;`.

### Limitations on component operations

* During the upgrade, the following component operations are not supported:

    * BR、Import Data 和通过 ingest 方式导入数据等组件：由于这些操作可能会将处于 paused 状态的 DDL 拷贝到 TiDB 中，而此状态的 DDL 不能自动 resume，可能导致后续 DDL 卡住的情况。因此无法处理此类组件的操作。

    * DM、Import Data 和 TiCDC 等组件。如果在升级过程中使用这些组件向 TiDB 导入 SQL，并且其中包含 DDL 操作，则会阻塞该导入操作，并可能出现未定义错误。
