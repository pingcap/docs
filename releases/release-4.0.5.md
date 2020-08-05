---
title: TiDB 4.0.5 Release Notes
---

# TiDB 4.0.5 Release Notes

Release date: August 10, 2020

TiDB version: 4.0.5

## Compatibility Changes

+ TiDB

    - Change drop partition and truncate partition's job args to support multi partition id array [#18930](https://github.com/pingcap/tidb/pull/18930)
    - Add delete only state for add partition replica check [#18865](https://github.com/pingcap/tidb/pull/18865)

## New Features

+ TiKV

    - Define error code for errors [#8387](https://github.com/tikv/tikv/pull/8387)

+ TiFlash

    - Support unified log format [#977](https://github.com/pingcap/tics/pull/977), [#978](https://github.com/pingcap/tics/pull/978)

+ Tools

    + TiCDC

        - Support Kafka SSL connection [#764](https://github.com/pingcap/ticdc/pull/764)
        - Support to output old value [#708](https://github.com/pingcap/ticdc/pull/708)
        - Support the column flags [#796](https://github.com/pingcap/ticdc/pull/796)
        - Support to output previous table info in ddl events [#799](https://github.com/pingcap/ticdc/pull/799)

## Improvements

+ TiDB

    - Optimize the performance of decodePlan for big union query [#18941](https://github.com/pingcap/tidb/pull/18941)
    - Reduce GC scan locks when meeting region cache miss [#18876](https://github.com/pingcap/tidb/pull/18876)
    - Ease the impact of stats feedback on cluster [#18772](https://github.com/pingcap/tidb/pull/18772)
    - Support cancel before RPC response return. [#18580](https://github.com/pingcap/tidb/pull/18580)
    - Add HTTP API to generate TiDB metric profile. [#18531](https://github.com/pingcap/tidb/pull/18531)
    - Fix the partition table issue in table scatter API. [#17863](https://github.com/pingcap/tidb/pull/17863)
    - Add detailed memory usage for each instance in grafana.
    - Add runtime information for the batch-point-get executor [#18892](https://github.com/pingcap/tidb/pull/18892)
    - Add executor runtime information for point-get. [#18817](https://github.com/pingcap/tidb/pull/18817)
    - Warn potential deadlock for Consume in remove [#18395](https://github.com/pingcap/tidb/pull/18395)
    - Support the Action when memory exceed quota for TableReader Executor. [#18392](https://github.com/pingcap/tidb/pull/18392)
    - Refine the behavior of StrToInt and StrToFloat and support convert JSON to date, time and timestamp [#18159](https://github.com/pingcap/tidb/pull/18159)

+ PD

    - Support scattering regions in stores with special engines (like TiFlash). [#2706](https://github.com/pingcap/pd/pull/2706)
    - Support Region HTTP API to promote regions schedule by given key range. [#2687](https://github.com/pingcap/pd/pull/2687)
    - Improve the leader distribution after region scatter. [#2684](https://github.com/pingcap/pd/pull/2684)
    - Add more tests and logs for TSO request. [#2678](https://github.com/pingcap/pd/pull/2678)
    - Avoid invalid cache updates after the leader of a region has changed. [#2672](https://github.com/pingcap/pd/pull/2672)

+ TiFlash

    - Add more Grafana panels, like CPU/IO/RAM usage, metrics about storage engine, etc.  [#965](https://github.com/pingcap/tics/pull/965)
    - Reduce IO operations by optimizing Raft logs processing logic. [#960](https://github.com/pingcap/tics/pull/960)
    - Accelerate regions schedule for blocked add partition ddl [#959](https://github.com/pingcap/tics/pull/959)
    - Optimize compactions of delta data in DeltaTree to reduce read and write amplification [#952](https://github.com/pingcap/tics/pull/952)
    - Optimize applying snapshot by preprocessing under multi-thread. [#944](https://github.com/pingcap/tics/pull/944)

+ Tools

    + TiCDC

        - Optimize get tso frequency [#801](https://github.com/pingcap/ticdc/pull/801)

    + Backup & Restore (BR)

        - Optimize some logs [#428](https://github.com/pingcap/br/pull/428)

    + Dumpling

        - Release FTWRL after connections are created to reduce lock time for mysql [#121](https://github.com/pingcap/dumpling/pull/121)

    + TiDB Lightning

        - Optimize some logs [#352](https://github.com/pingcap/tidb-lightning/pull/352)

## Bug Fixes

+ TiDB

    - Check ErrTruncate/Overflow locally for builtinCastRealAsDecimalSig to fix the "should ensure all columns have the same length" error [#18967](https://github.com/pingcap/tidb/pull/18967)
    - Fix a encode bug causes the wrong result of hashJoin with set and enum [#18859](https://github.com/pingcap/tidb/pull/18859)
    - Fix issue `pre_split_regions` table option doesn't work in the partition table. [#18837](https://github.com/pingcap/tidb/pull/18837)
    - Fixed an issue that could cause a large transaction to be terminated prematurely. [#18813](https://github.com/pingcap/tidb/pull/18813)
    - Fix incorrect collator when `getSignatureByPB` and remove unnecessary recover [#18735](https://github.com/pingcap/tidb/pull/18735)
    - Fix a bug `getAutoIncrementID()` function does not consider the `tidb_snapshot` session variable, this bug may cause dumper tool fail with 'table not exist' error. [#18692](https://github.com/pingcap/tidb/pull/18692)
    - Fix unknown column error for sql like `select a from t having t.a` [#18434](https://github.com/pingcap/tidb/pull/18434)
    - Fix a panic on hash partition table when the query condition is that the partition column equals to a big number like 9223372036854775808 [#18186](https://github.com/pingcap/tidb/pull/18186)
    - Fix the wrong behavior of char function. [#18122](https://github.com/pingcap/tidb/pull/18122)
    - Ddl: fix admin repair table with range partition expr will parseInt fail [#17988](https://github.com/pingcap/tidb/pull/17988)
    - Fix wrong behavior of set charset statement [#17289](https://github.com/pingcap/tidb/pull/17289)
    - Fix a bug caused by the wrong collation setting which leads to the wrong result of collation function. [#17231](https://github.com/pingcap/tidb/pull/17231)
    - Fix STR_TO_DATE's handling for format token '%r', '%h' [#18727](https://github.com/pingcap/tidb/pull/18727)
    - Fix issues of TiDB version information formation doesn't consistent with PD/TiKV in cluster_info table. [#18413](https://github.com/pingcap/tidb/pull/18413)

+ TiKV

    - Fix memory leak during scheduling [#8357](https://github.com/tikv/tikv/pull/8357)
    - Speed up leader election when hibernate region is enabled [#8292](https://github.com/tikv/tikv/pull/8292)

+ PD

    - Fix the bug that TSO request may fail at the time of leader changing. [#2666](https://github.com/pingcap/pd/pull/2666)
    - Fix the issue that when enabling placement rules, sometimes region replicas cannot schedule to optimal [#2720](https://github.com/pingcap/pd/pull/2720)

+ TiFlash

    - Fix the issue that TiFlash cannot start normally after upgrading from an old version if the name of the database or table contains special characters. [#971](https://github.com/pingcap/tics/pull/971)
    - Fix the issue that TiFlash process can not exit if any exceptions are thrown during initialization [#953](https://github.com/pingcap/tics/pull/953)

+ Tools

    + TiCDC

        - Fix a issue that failed changefeed can't be removed [#782](https://github.com/pingcap/ticdc/pull/782)
        - Fix invalid delete evenets by selecting one unique index as the handle index [#787](https://github.com/pingcap/ticdc/pull/787)
        - Fix the bug that GC safepoint will be forwarded beyond the checkpoint of stopped changefeed [#797](https://github.com/pingcap/ticdc/pull/797)

    + TiDB Lightning

        - Fix syntax error on empty binary/hex literals when using TiDB backend [#357](https://github.com/pingcap/tidb-lightning/pull/357)
