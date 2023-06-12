---
title: TiDB 6.5.3 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.3.
---

# TiDB 6.5.3 Release Notes

Release date: xxx, 2023

TiDB version: 6.5.3

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.3#version-list)

## Compatibility changes

- note 1

## Improvements

+ TiDB

    - note 1
    <!--tw:oreoxmt-->
    - Add `Stale Read OPS` and `Stale Read MBps` metrics to track hit rate and traffic when using Stale Read [#43325](https://github.com/pingcap/tidb/issues/43325) @[you06](https://github.com/you06)

+ TiKV

    - note 1

+ PD

    - note 1

+ TiFlash

    - note 1

+ Tools

    + Backup & Restore (BR)

        - note 1

    + TiCDC

        <!--tw:hfxsd-->
        - Optimize the way TiCDC handles DDLs so that DDLs do not block the use of other unrelated DML Events, and reduce memory usage [#8106](https://github.com/pingcap/tiflow/issues/8106) [asddongmen](https://github.com/asddongmen)
        - Optimize the Decoder interface and add a new method `AddKeyValue` [#8861](https://github.com/pingcap/tiflow/issues/8861) [3AceShowHand](https://github.com/3AceShowHand)
        - Optimize the directory structure when DDL events occur in the scenario of replicating data to object storage [#8890](https://github.com/pingcap/tiflow/issues/8890) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Support replicating data to the Kafka-on-Pulsar downstream [#8892](https://github.com/pingcap/tiflow/issues/8892) @[hi-rustin](https://github.com/hi-rustin)

    + TiDB Data Migration (DM)

        - note 1

    + TiDB Lightning

        - note 1

    + Dumpling

        - note 1

## Bug fixes

+ TiDB

    - note 1
    <!--tw:oreoxmt-->
    - Fix the issue that TiDB sends duplicate requests to PD during placement rules recycling, causing numerous `full config reset` entries in the PD log [#33069](https://github.com/pingcap/tidb/issues/33069) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `SHOW PRIVILEGES` statement returns an incomplete privilege list [#40591](https://github.com/pingcap/tidb/issues/40591) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that `ADMIN SHOW DDL JOBS LIMIT` returns incorrect results [#42298](https://github.com/pingcap/tidb/issues/42298) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that the `tidb_auth_token` user fails to be created when the password complexity check is enabled [#44098](https://github.com/pingcap/tidb/issues/44098) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue of not finding the partition during inner join in dynamic pruning mode [#43686](https://github.com/pingcap/tidb/issues/43686) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the `Data Truncated` warning occurs when executing `MODIFY COLUMN` on a partitioned table [#41118](https://github.com/pingcap/tidb/issues/41118) @[mjonss](https://github.com/mjonss)
    - Fix the issue of displaying the incorrect TiDB address in IPv6 environment [#43260](https://github.com/pingcap/tidb/issues/43260) @[nexustar](https://github.com/nexustar)
    - Fix the issue that CTE results are incorrect when pushing down predicates [#43645](https://github.com/pingcap/tidb/issues/43645) @[winoros](https://github.com/winoros)
    - Fix the issue that incorrect results might be returned when using CTE in statements with non-correlated subqueries [#44051](https://github.com/pingcap/tidb/issues/44051) @[winoros](https://github.com/winoros)
    - Fix the issue that Join Reorder might cause incorrect outer join results [#44314](https://github.com/pingcap/tidb/issues/44314) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that in some extreme cases, when the first statement of a pessimistic transaction is retried, resolving locks on this transaction might affect transaction correctness [#42937](https://github.com/pingcap/tidb/issues/42937) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that in some rare cases, residual pessimistic locks of pessimistic transactions might affect data correctness when GC resolves locks [#43243](https://github.com/pingcap/tidb/issues/43243) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that the scan detail information during the execution of `batch cop` might be inaccurate [#41582](https://github.com/pingcap/tidb/issues/41582) @[you06](https://github.com/you06)
    - Fix the issue that data updates cannot be read when Stale Read and `PREPARE` statements are used at the same time [#43044](https://github.com/pingcap/tidb/issues/43044) @[you06](https://github.com/you06)
    - Fix the issue that an `assertion failed` error might be mistakenly reported when executing the `LOAD DATA` statement [#43849](https://github.com/pingcap/tidb/issues/43849) @[you06](https://github.com/you06)
    - Fix the issue that the coprocessor does not fall back to the leader when a `region data not ready` error occurs during the use of Stale Read [#43365](https://github.com/pingcap/tidb/issues/43365) @[you06](https://github.com/you06)

+ TiKV

    - note 1

+ PD

    - note 1

+ TiFlash

    <!--tw:hfxsd-->
    - Fix the performance degradation issue of the partition TableScan operator during Region transfer [#7519](https://github.com/pingcap/tiflash/issues/7519) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that a TiFlash query might report an error if the `GENERATED` type field is present along with a `TIMESTAMP` or `TIME` [#7468](https://github.com/pingcap/tiflash/issues/7468) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that large update transactions might cause TiFlash to repeatedly report errors and restart [#7316](https://github.com/pingcap/tiflash/issues/7316) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the error "Truncate error cast decimal as decimal" occurs when reading data from TiFlash with the INSERT SELECT statement [#7348](https://github.com/pingcap/tiflash/issues/7348) @[windtalker](https://github.com/windtalker)
    - Fix the issue that queries might consume more memory than needed when the data on the Join build side is very large and contains many small string type columns [#7416](https://github.com/pingcap/tiflash/issues/7416) @[yibin87](https://github.com/yibin87)

+ Tools

    + Backup & Restore (BR)

        - note 1

    + TiCDC

        <!--tw:hfxsd-->
        - Fix an OOM issue that might occur when there are as many as 50,000 tables [#7872](https://github.com/pingcap/tiflow/issues/7872) [sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC gets stuck when an OOM occurs in upstream TiDB [#8561](https://github.com/pingcap/tiflow/issues/8561) [overvenus](https://github.com/overvenus)
        - Fix the issue that TiCDC gets stuck when PD fails such as network isolation or PD Owner node reboot [#8808](https://github.com/pingcap/tiflow/issues/8808) [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) [asddongmen](https://github.com/asddongmen)
        - Fix the issue of TiCDC time zone setting [#8798](https://github.com/pingcap/tiflow/issues/8798) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that checkpoint lag increases when one of the upstream TiKV nodes crashes [#8858](https://github.com/pingcap/tiflow/issues/8858) @[hicqu](https://github.com/hicqu)

    + TiDB Data Migration (DM)

        - note 1

    + TiDB Lightning

        - note 1

    + Dumpling

        - note 1
