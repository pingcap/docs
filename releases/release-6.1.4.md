---
title: TiDB 6.1.4 Release Notes
---

# TiDB 6.1.4 Release Notes

Release date: February 8, 2023

TiDB version: 6.1.4

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.1.4#version-list)

## Compatibility changes

- Tools

    - TiCDC

        - 

## Improvements

- PD

    - 

- TiFlash

    - Reduce the IOPS and write amplification of TiFlash under high update throughput workloads. [#6460](https://github.com/pingcap/tiflash/issues/6460) @[flowbehappy](https://github.com/flowbehappy)

- Tools

    - TiCDC

        - Add the dml batch operation mode to improve the throughput in scenarios of running batch [#7653](https://github.com/pingcap/tiflow/issues/7653) @[asddongmen](https://github.com/asddongmen)
    
    - Lightning

        - Change severity of clusterResourceCheckItem,emptyRegionCheckItem from Critical to Warn [#37654](https://github.com/pingcap/tidb/issues/37654) @[lance6716](https://github.com/lance6716) 

## Bug fixes

+ TiDB

    tidb

    (dup: release-6.2.0.md > Bug fixes> TiDB)- Fix the issue that when you create a table, the default value and the type of a column are not consistent and are not automatically corrected [#34881](https://github.com/pingcap/tidb/issues/34881) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) @[mjonss](https://github.com/mjonss)

    transaction

    - Fix data race in the LazyTxn.LockKeys [#40355](https://github.com/pingcap/tidb/issues/40355) @[HuSharp](https://github.com/HuSharp)
    - Fix the case that INSERT/REPLACE might panic in a long session connection [#40351](https://github.com/pingcap/tidb/issues/40351) @[fanrenhoo](https://github.com/fanrenhoo)
    - Fix the issue that hcursor read being canceled by GC [#39447](https://github.com/pingcap/tidb/issues/39447)@[zyguan](https://github.com/zyguan)
    - Fix the issue that the pessimistic autocommit configuration does not work for point get plans [#39928](https://github.com/pingcap/tidb/issues/39928)@[zyguan](https://github.com/zyguan)

    sql-infra
    
    - Block modify column of partitioned table, even if it was not changing data when put into the DDL queue. [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss)
    - 

    planner

    (dup: release-6.3.0.md > Bug fixes> TiDB> Fix the issue that querying `INFORMATION_SCHEMA.TIKV_REGION_STATUS` returns an incorrect result @[zimulala](https://github.com/zimulala))- Fix the issue that the `IN` and `NOT IN` subqueries in some patterns report the `Can't find column` error [#37032](https://github.com/pingcap/tidb/issues/37032) @[AilinKid](https://github.com/AilinKid) @[lance6716](https://github.com/lance6716)

- PD

    - Fix an issue that PD may repeatedly add Learner to a Region. [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)   

+ TiKV

    (dup: release-6.4.0.md > Bug fixes> TiKV)- Fix the issue that TiDB fails to start on Gitpod when there are multiple `cgroup` and `mountinfo` records [#13660](https://github.com/tikv/tikv/issues/13660) @[tabokie](https://github.com/tabokie) @[ti-srebot](https://github.com/ti-srebot)
    (dup: release-6.5.0.md > Bug fixes> TiKV)- Fix the issue that tikv-ctl is terminated unexpectedly when executing the `reset-to-version` command [#13829](https://github.com/tikv/tikv/issues/13829) @[tabokie](https://github.com/tabokie) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix panic when the size of one single write exceeds 2GiB. [#13848](https://github.com/tikv/tikv/issues/13848) @[YuJuncen](https://github.com/YuJuncen)
    (dup: release-6.3.0.md > Bug fixes> TiKV)- Fix the issue that TiKV mistakenly reports a `PessimisticLockNotFound` error [#13425](https://github.com/tikv/tikv/issues/13425) @[sticnarf](https://github.com/sticnarf) @[ti-srebot](https://github.com/ti-srebot)
    - Fixed a problem that when a transaction in TiDB fails to execute a pessimistic DML and then executes another DML, if there are random network failures between TiDB and TiKV, it has risk to cause data inconsistency. [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)
    (dup: release-6.5.0.md > Bug fixes> TiKV)- Fix the issue that `_` in the `LIKE` operator cannot match non-ASCII characters when new collation is not enabled [#13769](https://github.com/tikv/tikv/issues/13769) @[YangKeao](https://github.com/YangKeao) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ TiFlash

    - Avoid tiflash global locks with small probability of long term blocking. [#6418](https://github.com/pingcap/tiflash/issues/6418) @[SeaRise](https://github.com/SeaRise)
    - Fix an issue that causes OOM with high throughput write [#6407](https://github.com/pingcap/tiflash/issues/6407) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix a bug that restore exits due to get region size failed. [#36053](https://github.com/pingcap/tidb/issues/36053) @[YuJuncen](https://github.com/YuJuncen)
        - Fix a issue that cause br debug backupmeta file panic.[#40878](https://github.com/pingcap/tidb/issues/40878) @[MoCuishle28](https://github.com/MoCuishle28) 

    + TiCDC

        - Fix an issue that checkpoint can not advance when replicating many tables. [#8004](https://github.com/pingcap/tiflow/issues/8004) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue of transaction-atomicity and protocol can't be updated via config file. [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)        
        (dup: release-6.5.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that TiCDC mistakenly reports an error when there is a later version of TiFlash [#7744](https://github.com/pingcap/tiflow/issues/7744) @[overvenus](https://github.com/overvenus) 
        - Fix an OOM issue when TiCDC replicates big transactions [#7913](https://github.com/pingcap/tiflow/issues/7913) @[overvenus](https://github.com/overvenus) 
        - Fix the bug that context deadline was exceeded when replicating data without split big txn [#7982](https://github.com/pingcap/tiflow/issues/7982) @[asddongmen](https://github.com/asddongmen)
        (dup: release-6.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that `sasl-password` in the `changefeed query` result is not masked [#7182](https://github.com/pingcap/tiflow/issues/7182) @[dveeden](https://github.com/dveeden)
        (dup: release-6.5.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that data is lost when a user quickly deletes a replication task and then creates another one with the same task name [#7657](https://github.com/pingcap/tiflow/issues/7657) @[overvenus](https://github.com/overvenus)

    + TiDB Data Migration (DM)

        - Fix a bug that DM may raise error at prechecking when downstream database name in SHOW GRANTS contains wildcard [#7645](https://github.com/pingcap/tiflow/issues/7645) @[lance6716]
        - Fix DM print too many log caused by "COMMIT" in binlog query event [#7525](https://github.com/pingcap/tiflow/issues/7525) @[liumengya94]
        - Fix dm failed to run when only "ssl-ca" is configured [#7941](https://github.com/pingcap/tiflow/issues/7941) @[liumengya94]
        - Fix a bug that when both "update" and "non-update" type expression filters are used in one table, all UPDATE row changes are skipped [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716]
        - Fix a bug when only one of `update-old-value-expr` or `update-new-value-expr` is set for a table, it does not take effect or panic [#7774](https://github.com/pingcap/tiflow/issues/7774) @[lance6716]
