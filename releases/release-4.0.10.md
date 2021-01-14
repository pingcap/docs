---
title: TiDB 4.0.10 Release Notes
---

# TiDB 4.0.10 Release Notes

Release date: January 15, 2021

TiDB version: 4.0.10

## Compatibility Changes

## New Features

+ PD

    - Support configuration `enable-redact-log` to enable log desensitization or not [#3266](https://github.com/pingcap/pd/pull/3266)

+ TiFlash

    - Add `security.redact_info_log` config, which can redact user data from logs

## Improvements

+ TiDB

    - Make txn entry size limit configurable [#21843](https://github.com/pingcap/tidb/pull/21843)

+ PD

    - Optimize the store state filter metrics [#3100](https://github.com/tikv/pd/pull/3100)
    - Upgrade go.etcd.io/bbolt to v1.3.5 [#3331](https://github.com/tikv/pd/pull/3331)

## Bug Fixes

+ TiDB

    - Fix a concurrency bug that may cause the batch client timeout [#22336](https://github.com/pingcap/tidb/pull/22336)
    - Avoid duplicate bindings caused by concurrent baseline capture [#22295](https://github.com/pingcap/tidb/pull/22295)
    - Make baseline capture work when log level is 'debug' [#22293](https://github.com/pingcap/tidb/pull/22293)
    - Correctly GC locks when region merge happens during scanning & resolving locks [#22267](https://github.com/pingcap/tidb/pull/22267)
    - Return correct results for user variables of datetime type [#22143](https://github.com/pingcap/tidb/pull/22143)
    - Avoid using index merge when there are multiple table filters. [#22124](https://github.com/pingcap/tidb/pull/22124)
    - Fix the `wrong precision` problem in TiFlash caused by prepare plan cache. [#21960](https://github.com/pingcap/tidb/pull/21960)
    - Fix the bug that schema change will lead to incorrect results. [#21596](https://github.com/pingcap/tidb/pull/21596)
    - Avoid unnecessary column flag changes incurred by `ALTER TABLE`. [#21474](https://github.com/pingcap/tidb/pull/21474)
    - Set database name for table aliases of query blocks used in optimizer hint. [#21380](https://github.com/pingcap/tidb/pull/21380)
    - Generate proper hint for IndexHashJoin / IndexMergeJoin [#21020](https://github.com/pingcap/tidb/pull/21020)

+ TiKV

    - Fix wrong mapping between ready and peer [#9409](https://github.com/tikv/tikv/pull/9409)
    - Fix some logs are not redacted when `security.redact-info-log` is on [#9314](https://github.com/tikv/tikv/pull/9314)

+ PD

    - Fix the id allocation is not monotonic [#3308](https://github.com/tikv/pd/pull/3308) [#3323](https://github.com/tikv/pd/pull/3323)
    - Fix the pd client could be blocked in some cases [#3285](https://github.com/pingcap/pd/pull/3285)

+ TiFlash

    - Fixed an issue that TiFlash can't start because TiFlash failed to process the schema of TiDB with an old version
    - Fixed an issue where TiFlash can't start due to incorrect handling of cpu_time on the RedHat system
    - Fixed the issue that TiFlash fails to start when path_realtime_mode is true
    - Fixed the issue of incorrect results when calling the `substr` function with three parameters
    - Fixed the issue that TiFlash does not support Enum type change even if the change is lossless
 
## 未分类 notes。请对以下 Note 进行分类，挪动到上面 Compatibility changes、New features、Improvement 分类下

+ Tools

    - TiCDC

        * Fix a bug that MySQL connection is not recycled when some transactions executed with failure [#1285](https://github.com/pingcap/ticdc/pull/1285)
        * Fixed bug in passing `max-batch-size` to codec [#1253](https://github.com/pingcap/ticdc/pull/1253)
        * Enable Unified Sorter by default [#1230](https://github.com/pingcap/ticdc/pull/1230)
        * Fix a bug that the cdc owner might consume too much memory in the etcd watch client [#1227](https://github.com/pingcap/ticdc/pull/1227)
        * Fix a bug that outdated metadata could cause the newly created changefeed abnormal. [#1184](https://github.com/pingcap/ticdc/pull/1184)
