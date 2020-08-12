---
title: TiDB 4.0.5 Release Notes
---

# TiDB 4.0.5 Release Notes

Release date: August 13, 2020

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
    - Reduce the number of GC lock scans when meeting the `Region cache miss` error [#18876](https://github.com/pingcap/tidb/pull/18876)
    - Ease the impact of statistical feedback on cluster performance [#18772](https://github.com/pingcap/tidb/pull/18772)
    - Support canceling operations before the RPC response is returned [#18580](https://github.com/pingcap/tidb/pull/18580)
    - Add the HTTP API to generate the TiDB metric profile [#18531](https://github.com/pingcap/tidb/pull/18531)
    - Support scattering partitioned tables [#17863](https://github.com/pingcap/tidb/pull/17863)
    - Add detailed memory usage of each instance in Grafana [#18679](https://github.com/pingcap/tidb/pull/18679)
    - Show the detailed runtime information of the `BatchPointGet` executor in the result of `EXPLAIN` [#18892](https://github.com/pingcap/tidb/pull/18892)
    - Show the detailed runtime information of the `PointGet` executor in the result of `EXPLAIN` [#18817](https://github.com/pingcap/tidb/pull/18817)
    - Warn the potential deadlock for `Consume` in `remove()` [#18395](https://github.com/pingcap/tidb/pull/18395)
    - Support the Action when memory exceed quota for TableReader Executor [#18392](https://github.com/pingcap/tidb/pull/18392)
    - Refine the behaviors of `StrToInt` and `StrToFloat` and support converting JSON to the `date`, `time`, and `timestamp` types [#18159](https://github.com/pingcap/tidb/pull/18159)
    - Support limiting the memory usage of the `TableReader` executor [#18392](https://github.com/pingcap/tidb/pull/18392)
    - Avoid too many times of backoff when retrying the `batch cop` request [#18999](https://github.com/pingcap/tidb/pull/18999)

+ PD

    - Support scattering Regions in stores with special engines (like TiFlash) [#2706](https://github.com/pingcap/pd/pull/2706)
    - Support the Region HTTP API to prioritize Region scheduling of a given key range [#2687](https://github.com/pingcap/pd/pull/2687)
    - Improve the leader distribution after Region scattering [#2684](https://github.com/pingcap/pd/pull/2684)
    - Add more tests and logs for the TSO request [#2678](https://github.com/pingcap/pd/pull/2678)
    - Avoid invalid cache updates after the leader of a Region has changed [#2672](https://github.com/pingcap/pd/pull/2672)

+ TiFlash

    - Add more Grafana panels to display metrics of CPU, I/O, RAM usages and metrics of the storage engine
    - Reduce I/O operations by optimizing the processing logic of Raft logs
    - Accelerate Region scheduling for the blocked `add partition` DDL statement
    - Optimize compactions of delta data in DeltaTree to reduce read and write amplification
    - Optimize the performance of applying Region snapshots by preprocessing the snapshots using multiple threads

+ Tools

    + TiCDC

        - Lower the frequency of getting TSO [#801](https://github.com/pingcap/ticdc/pull/801)

    + Backup & Restore (BR)

        - Optimize some logs [#428](https://github.com/pingcap/br/pull/428)

    + Dumpling

        - Release FTWRL after connections are created to reduce the lock time for MySQL [#121](https://github.com/pingcap/dumpling/pull/121)

    + TiDB Lightning

        - Optimize some logs [#352](https://github.com/pingcap/tidb-lightning/pull/352)

## Bug Fixes

+ TiDB

    - Fix the `should ensure all columns have the same length` error that occurs because the `ErrTruncate/Overflow` error is incorrectly handled in the `builtinCastRealAsDecimalSig` function [#18967](https://github.com/pingcap/tidb/pull/18967)
    - Fix the issue that the `pre_split_regions` table option does not work in the partitioned table [#18837](https://github.com/pingcap/tidb/pull/18837)
    - Fixe the issue that might cause a large transaction to be terminated prematurely [#18813](https://github.com/pingcap/tidb/pull/18813)
    - Fix the issue that using the `collation` functions get wrong query results [#18735](https://github.com/pingcap/tidb/pull/18735)
    - Fix the bug that the `getAutoIncrementID()` function does not consider the `tidb_snapshot` session variable, which might cause the dumper tool to fail with the `table not exist` error [#18692](https://github.com/pingcap/tidb/pull/18692)
    - Fix the `unknown column error` for SQL statement like `select a from t having t.a` [#18434](https://github.com/pingcap/tidb/pull/18434)
    - Fix the panic issue that writing the 64-bit unsigned type into the hash partitioned table causes overflow and gets an unexpected negative number when the partition key is the integer type [#18186](https://github.com/pingcap/tidb/pull/18186)
    - Fix the wrong behavior of the `char` function [#18122](https://github.com/pingcap/tidb/pull/18122)
    - Fix the issue that the `ADMIN REPAIR TABLE` statement cannot parse integer in the expressions on the range partition [#17988](https://github.com/pingcap/tidb/pull/17988)
    - Fix the wrong behavior of the `SET CHARSET` statement [#17289](https://github.com/pingcap/tidb/pull/17289)
    - Fix the bug caused by the wrong collation setting which leads to the wrong result of the `collation` function [#17231](https://github.com/pingcap/tidb/pull/17231)
    - Fix the issue that `STR_TO_DATE`'s handling of the format tokens '%r', '%h' is inconsistent with that of MySQL [#18727](https://github.com/pingcap/tidb/pull/18727)
    - Fix issues that the TiDB version information is inconsistent with that of PD/TiKV in the `cluster_info` table [#18413](https://github.com/pingcap/tidb/pull/18413)
    - Fix the existent checks for pessimistic transactions [#19004](https://github.com/pingcap/tidb/pull/19004)
    - Fix the issue that executing `union select for update` might cause concurrent race [#19006](https://github.com/pingcap/tidb/pull/19006)
    - Fix the wrong query result when `apply` has a child of the `PointGet` operator [#19046](https://github.com/pingcap/tidb/pull/19046)

+ TiKV

    - Fix the memory leak issue during scheduling [#8357](https://github.com/tikv/tikv/pull/8357)
    - Speed up leader election when Hibernate Region is enabled [#8292](https://github.com/tikv/tikv/pull/8292)

+ PD

    - Fix the bug that the TSO request might fail at the time of leader change [#2666](https://github.com/pingcap/pd/pull/2666)
    - Fix the issue that sometimes Region replicas cannot be scheduled to the optimal state when placement rules are enabled [#2720](https://github.com/pingcap/pd/pull/2720)
    - Fix the issue that `Balance Leader` does not work when placement rules are enabled [#2726](https://github.com/pingcap/pd/pull/2726)

+ TiFlash

    - Fix the issue that TiFlash cannot start normally after upgrading from an earlier version if the name of the database or table contains special characters
    - Fix the issue that the TiFlash process can not exit if any exceptions are thrown during initialization

+ Tools

    + TiCDC

        - Fix the issue that the failed `changefeed` cannot be removed [#782](https://github.com/pingcap/ticdc/pull/782)
        - Fix invalid `delete` events by selecting one unique index as the handle index [#787](https://github.com/pingcap/ticdc/pull/787)
        - Fix the bug that GC safepoint is forwarded beyond the checkpoint of stopped `changefeed` [#797](https://github.com/pingcap/ticdc/pull/797)
        - Fix the bug that the network I/O waiting blocks tasks to exit [#825](https://github.com/pingcap/ticdc/pull/825)

    + TiDB Lightning

        - Fix the syntax error on empty binary/hex literals when using TiDB backend [#357](https://github.com/pingcap/tidb-lightning/pull/357)
