---
title: TiDB 6.1.4 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.1.4.
---

# TiDB 6.1.4 Release Notes

Release date: February 8, 2023

TiDB version: 6.1.4

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.1.4#version-list)

## Compatibility changes

- TiDB

    - No longer support modifying column types on partitioned tables because of potential correctness issues [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss)

## Improvements

- TiFlash

    - Reduce the IOPS and write amplification of TiFlash under high update throughput workloads [#6460](https://github.com/pingcap/tiflash/issues/6460) @[flowbehappy](https://github.com/flowbehappy)

- Tools

    - TiCDC

        - Add the DML batch operation mode to improve the throughput in scenarios of running batches [#7653](https://github.com/pingcap/tiflow/issues/7653) @[asddongmen](https://github.com/asddongmen)
        - Support storing redo logs to GCS- or Azure-compatible object storage [#7987](https://github.com/pingcap/tiflow/issues/7987) @[CharlesCheung96](https://github.com/CharlesCheung96)

    - TiDB Lightning

        - Change severity of the precheck items `clusterResourceCheckItem` and `emptyRegionCheckItem` from `Critical` to `Warning` [#37654](https://github.com/pingcap/tidb/issues/37654) @[niubell](https://github.com/niubell)

## Bug fixes

+ TiDB

    - Fix the issue that when you create a table, the default value and the type of a column are not consistent and are not automatically corrected [#34881](https://github.com/pingcap/tidb/issues/34881) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) @[mjonss](https://github.com/mjonss)
    - Fix the data race issue in the `LazyTxn.LockKeys` function [#40355](https://github.com/pingcap/tidb/issues/40355) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that the `INSERT` or `REPLACE` statements might panic in long session connections [#40351](https://github.com/pingcap/tidb/issues/40351) @[fanrenhoo](https://github.com/fanrenhoo)
    - Fix the issue that reading data using the "cursor read" method might return error because of GC [#39447](https://github.com/pingcap/tidb/issues/39447)@[zyguan](https://github.com/zyguan)
    - Fix the issue that the [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit) configuration item does not take effect for point-get queries [#39928](https://github.com/pingcap/tidb/issues/39928)@[zyguan](https://github.com/zyguan)
    - Fix the issue that querying the `INFORMATION_SCHEMA.TIKV_REGION_STATUS` table returns an incorrect result @[zimulala](https://github.com/zimulala))
    - Fix the issue that the `IN` and `NOT IN` subqueries in some patterns report the `Can't find column` error [#37032](https://github.com/pingcap/tidb/issues/37032) @[AilinKid](https://github.com/AilinKid) @[lance6716](https://github.com/lance6716)

- PD

    - Fix the issue that PD might unexpectedly add multiple Learners to a Region [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)

+ TiKV

    - Fix the issue that TiDB fails to start on Gitpod when there are multiple `cgroup` and `mountinfo` records [#13660](https://github.com/tikv/tikv/issues/13660) @[tabokie](https://github.com/tabokie) @[ti-srebot](https://github.com/ti-srebot)
    - Fix the issue that tikv-ctl is terminated unexpectedly when executing the `reset-to-version` command [#13829](https://github.com/tikv/tikv/issues/13829) @[tabokie](https://github.com/tabokie) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the panic when the size of one single write exceeds 2 GiB. [#13848](https://github.com/tikv/tikv/issues/13848) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that TiKV mistakenly reports a `PessimisticLockNotFound` error [#13425](https://github.com/tikv/tikv/issues/13425) @[sticnarf](https://github.com/sticnarf)
    - Fix the issue that when a transaction in TiDB fails to execute a pessimistic DML and then executes another DML, if there are random network failures between TiDB and TiKV, it has risk to cause data inconsistency [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that `_` in the `LIKE` operator cannot match non-ASCII characters when new collation is not enabled [#13769](https://github.com/tikv/tikv/issues/13769) @[YangKeao](https://github.com/YangKeao) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ TiFlash

    - Avoid TiFlash global locks with small probability of long term blocking [#6418](https://github.com/pingcap/tiflash/issues/6418) @[SeaRise](https://github.com/SeaRise)
    - Fix an issue that causes OOM with high throughput write [#6407](https://github.com/pingcap/tiflash/issues/6407) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that restore exits due to getting the region size failed [#36053](https://github.com/pingcap/tidb/issues/36053) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that causes panic when BR debugs the backupmeta file [#40878](https://github.com/pingcap/tidb/issues/40878) @[MoCuishle28](https://github.com/MoCuishle28)

    + TiCDC

        - Fix the issue that checkpoint can not advance when replicating many tables [#8004](https://github.com/pingcap/tiflow/issues/8004) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue of transaction-atomicity and protocol can't be updated via config file [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC mistakenly reports an error when there is a later version of TiFlash [#7744](https://github.com/pingcap/tiflow/issues/7744) @[overvenus](https://github.com/overvenus)
        - Fix an OOM issue when TiCDC replicates big transactions [#7913](https://github.com/pingcap/tiflow/issues/7913) @[overvenus](https://github.com/overvenus)
        - Fix the bug that context deadline is exceeded when replicating data without splitting big txn [#7982](https://github.com/pingcap/tiflow/issues/7982) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that `sasl-password` in the `changefeed query` result is not masked [#7182](https://github.com/pingcap/tiflow/issues/7182) @[dveeden](https://github.com/dveeden)
        - Fix the issue that data is lost when a user quickly deletes a replication task and then creates another one with the same task name [#7657](https://github.com/pingcap/tiflow/issues/7657) @[overvenus](https://github.com/overvenus)

    + TiDB Data Migration (DM)

        - Fix a bug that DM might raise an error during prechecking when the downstream database name in `SHOW GRANTS` contains a wildcard [#7645](https://github.com/pingcap/tiflow/issues/7645) @[lance6716]
        - Fix the issue that DM prints too many logs caused by "COMMIT" in binlog query events [#7525](https://github.com/pingcap/tiflow/issues/7525) @[liumengya94]
        - Fix the issue that DM fails to run when only "ssl-ca" is configured [#7941](https://github.com/pingcap/tiflow/issues/7941) @[liumengya94]
        - Fix a bug that when both "update" and "non-update" type expression filters are used in one table, all UPDATE row changes are skipped [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716]
        - Fix a bug when only one of `update-old-value-expr` or `update-new-value-expr` is set for a table, it does not take effect or panic [#7774](https://github.com/pingcap/tiflow/issues/7774) @[lance6716]

    + TiDB Lightning

        - Fix the memory leak issue on Large Source Files [#39331](https://github.com/pingcap/tidb/issues/39331) @[dsdashun](https://github.com/dsdashun)
        - Fix the issue that Table Empty Check cannot find imported dirty data on previous failed imports [#39477](https://github.com/pingcap/tidb/issues/39477) @[dsdashun](https://github.com/dsdashun)
