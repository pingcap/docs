---
title: TiDB 4.0.5 Release Notes
---

# TiDB 4.0.5 Release Notes

Release date: August 11, 2020

TiDB version: 4.0.5

## Compatibility Changes

+ TiDB

    - Change `drop partition` and `truncate partition`'s job arguments to support the ID array of multiple partitions [#18930](https://github.com/pingcap/tidb/pull/18930)
    - Add the delete-only state for checking `add partition` replicas [#18865](https://github.com/pingcap/tidb/pull/18865)

## New Features

+ TiKV

    - Define error code for errors [#8387](https://github.com/tikv/tikv/pull/8387)

+ TiFlash

    - Support the unified log format with TiDB

+ Tools

    + TiCDC

        - Support Kafka SSL connection [#764](https://github.com/pingcap/ticdc/pull/764)
        - Support outputting the old value [#708](https://github.com/pingcap/ticdc/pull/708)
        - Add the column flags [#796](https://github.com/pingcap/ticdc/pull/796)
        - Support outputting the DDL statements and table schema of the previous version [#799](https://github.com/pingcap/ticdc/pull/799)

## Improvements

+ TiDB

    - Optimize the performance of `DecodePlan` for big union queries [#18941](https://github.com/pingcap/tidb/pull/18941)
    - Reduce GC scan locks when meeting Region cache miss [#18876](https://github.com/pingcap/tidb/pull/18876)
    - Ease the impact of stats feedback on cluster [#18772](https://github.com/pingcap/tidb/pull/18772)
    - Support canceling operations before the RPC response is returned [#18580](https://github.com/pingcap/tidb/pull/18580)
    - Add the HTTP API to generate the TiDB metric profile [#18531](https://github.com/pingcap/tidb/pull/18531)
    - Fix the partition table issue in table scatter API [#17863](https://github.com/pingcap/tidb/pull/17863)
    - Add detailed memory usage for each instance in Grafana
    - Add runtime information for the `batch-point-get` executor [#18892](https://github.com/pingcap/tidb/pull/18892)
    - Add executor runtime information for point-get [#18817](https://github.com/pingcap/tidb/pull/18817)
    - Warn potential deadlock for Consume in remove [#18395](https://github.com/pingcap/tidb/pull/18395)
    - Support the Action when memory exceed quota for TableReader Executor [#18392](https://github.com/pingcap/tidb/pull/18392)
    - Refine the behavior of StrToInt and StrToFloat and support convert JSON to date, time and timestamp [#18159](https://github.com/pingcap/tidb/pull/18159)
    - Avoid too many times of backoff when we retry for batch cop [#18999](https://github.com/pingcap/tidb/pull/18999)

+ PD

    - Support scattering Regions in stores with special engines (like TiFlash) [#2706](https://github.com/pingcap/pd/pull/2706)
    - Support Region HTTP API to promote Regions schedule by given key range [#2687](https://github.com/pingcap/pd/pull/2687)
    - Improve the leader distribution after Region scatter [#2684](https://github.com/pingcap/pd/pull/2684)
    - Add more tests and logs for TSO request [#2678](https://github.com/pingcap/pd/pull/2678)
    - Avoid invalid cache updates after the leader of a Region has changed [#2672](https://github.com/pingcap/pd/pull/2672)

+ TiFlash

    - Add more Grafana panels, like CPU/IO/RAM usage, metrics about storage engine
    - Reduce I/O operations by optimizing Raft logs processing logic
    - Accelerate Regions schedule for blocked add partition DDL
    - Optimize compactions of delta data in DeltaTree to reduce read and write amplification
    - Optimize the performance of applying Region snapshots by preprocessing them under multi-threads

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

    - Check `ErrTruncate/Overflow` locally for `builtinCastRealAsDecimalSig` to fix the `should ensure all columns have the same length` error [#18967](https://github.com/pingcap/tidb/pull/18967)
    - Fix issue that the `pre_split_regions` table option does not work in the partition table [#18837](https://github.com/pingcap/tidb/pull/18837)
    - Fixe the issue that might cause a large transaction to be terminated prematurely [#18813](https://github.com/pingcap/tidb/pull/18813)
    - Fix the incorrect collator when `getSignatureByPB` and remove unnecessary recover [#18735](https://github.com/pingcap/tidb/pull/18735)
    - Fix a bug `getAutoIncrementID()` function does not consider the `tidb_snapshot` session variable, this bug might cause dumper tool fail with 'table not exist' error [#18692](https://github.com/pingcap/tidb/pull/18692)
    - Fix unknown column error for sql like `select a from t having t.a` [#18434](https://github.com/pingcap/tidb/pull/18434)
    - Fix a panic on hash partition table when the query condition is that the partition column equals to a big number like 9223372036854775808 [#18186](https://github.com/pingcap/tidb/pull/18186)
    - Fix the wrong behavior of char function [#18122](https://github.com/pingcap/tidb/pull/18122)
    - Fix the issue that the `ADMIN REPAIR TABLE` statement cannot parse integer in the expressions on the range partition [#17988](https://github.com/pingcap/tidb/pull/17988)
    - Fix the wrong behavior of the `SET CHARSET` statement [#17289](https://github.com/pingcap/tidb/pull/17289)
    - Fix the bug caused by the wrong collation setting which leads to the wrong result of the `collation` function [#17231](https://github.com/pingcap/tidb/pull/17231)
    - Fix `STR_TO_DATE`'s handling for format token '%r', '%h' [#18727](https://github.com/pingcap/tidb/pull/18727)
    - Fix issues that TiDB version information is not consistent with PD/TiKV in the `cluster_info` table [#18413](https://github.com/pingcap/tidb/pull/18413)
    - Fix the existence checks for pessimistic transactions [#19004](https://github.com/pingcap/tidb/pull/19004)
    - Fix union select for update race [#19006](https://github.com/pingcap/tidb/pull/19006)
    - Fix the wrong query result when apply has a child of type PointGet [#19046](https://github.com/pingcap/tidb/pull/19046)

+ TiKV

    - Fix memory leak during scheduling [#8357](https://github.com/tikv/tikv/pull/8357)
    - Speed up leader election when Hibernate Region is enabled [#8292](https://github.com/tikv/tikv/pull/8292)

+ PD

    - Fix the bug that TSO request might fail at the time of leader changing [#2666](https://github.com/pingcap/pd/pull/2666)
    - Fix the issue that when enabling placement rules, sometimes Region replicas cannot schedule to optimal [#2720](https://github.com/pingcap/pd/pull/2720)
    - Fix the bug that balance-leader won't work when placement rule enabled [#2726](https://github.com/pingcap/pd/pull/2726)

+ TiFlash

    - Fix the issue that TiFlash cannot start normally after upgrading from an old version if the name of the database or table contains special characters
    - Fix the issue that TiFlash process can not exit if any exceptions are thrown during initialization

+ Tools

    + TiCDC

        - Fix the issue that the failed `changefeed` cannot be removed [#782](https://github.com/pingcap/ticdc/pull/782)
        - Fix invalid `delete` events by selecting one unique index as the handle index [#787](https://github.com/pingcap/ticdc/pull/787)
        - Fix the bug that GC safepoint will be forwarded beyond the checkpoint of stopped `changefeed` [#797](https://github.com/pingcap/ticdc/pull/797)
        - Fix the bug that network io wait blocks task exits [#825](https://github.com/pingcap/ticdc/pull/825)

    + TiDB Lightning

        - Fix syntax error on empty binary/hex literals when using TiDB backend [#357](https://github.com/pingcap/tidb-lightning/pull/357)
