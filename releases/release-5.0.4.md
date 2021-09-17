---
title: TiDB 5.0.4 Release Notes
---

# TiDB 5.0.4 Release Notes

Release Date: September 27, 2021

TiDB version: 5.0.4

## Compatibility Changes

+ TiDB

    - Revert #19341 to avoid #24326 [#26258](https://github.com/pingcap/tidb/pull/26258)
    - Enlarge the variable tidb_stmt_summary_max_stmt_count default value from 200 to 3000 [#25873](https://github.com/pingcap/tidb/pull/25873)
    - These bug fixes change execution results, which may result in upgrading incompatibility:
        - Fix the case that TiDB would return the wrong result when the children of the UNION contain pure NULL values [#26571](https://github.com/pingcap/tidb/pull/26571)
        - Fix the issue that greatest(datetime) union null returns empty string [#26565](https://github.com/pingcap/tidb/pull/26565)
        - fix incompatible last_day func behavior in sql mode [#26000](https://github.com/pingcap/tidb/pull/26000)
        - fix having clause might not work correctly [#27742](https://github.com/pingcap/tidb/pull/27742)
        - fix the result is wrong when the collations around the `between` expression are different. [#27548](https://github.com/pingcap/tidb/pull/27548)
        - fix the result is wrong when the column in the `group_concat` function has a non-bin collation [#27528](https://github.com/pingcap/tidb/pull/27528)
        - Fix bug that using a `count(distinct)` expression on multi-columns returns the wrong result when new collation is on. [#27507](https://github.com/pingcap/tidb/pull/27507)
        - fix the result is wrong when the argument of `extract` function is a negative duration [#27368](https://github.com/pingcap/tidb/pull/27368)
        - fix inserting an invalid date does not report an error when the `SQL_MODE` is 'STRICT_TRANS_TABLES' [#27110](https://github.com/pingcap/tidb/pull/27110)
        - Fix bug that using an invalid default date does not report an error when the `SQL_MODE` is 'NO_ZERO_IN_DATE'. [#26903](https://github.com/pingcap/tidb/pull/26903)
        - fix a bug on the query range of prefix index [#26261](https://github.com/pingcap/tidb/pull/26261)
        - Fix the issue that the `LOAD DATA` statement might abnormally import non-utf8 data [#26143](https://github.com/pingcap/tidb/pull/26143)
        - Fix the data might be wrong after "insert ignore on duplicate update" when the secondary index has the same column in the primary key [#25905](https://github.com/pingcap/tidb/pull/25905)
        - Fix the data might be wrong after "insert ignore duplicate update" on partition table when the table has a clustered index [#25859](https://github.com/pingcap/tidb/pull/25859)
        - fix the result is wrong when the key is `enum` type in point get or batch point get [#24772](https://github.com/pingcap/tidb/pull/24772)
        - fix the result is wrong when dividing a `bit` value [#24267](https://github.com/pingcap/tidb/pull/24267)
        - fix the result might be different between prepared statements and direct queries [#23373](https://github.com/pingcap/tidb/pull/23373)
        - fix the result might be wrong when a `year` type compares with a string or integer type. [#23336](https://github.com/pingcap/tidb/pull/23336)

## Feature enhancements

+ TiDB

- Support set `tidb_enforce_mpp=1` to enforce use mpp mode [#26382](https://github.com/pingcap/tidb/pull/26382)

+ TiKV

    - Support changing CDC configs dynamically [#10685](https://github.com/tikv/tikv/pull/10685)

+ PD

    - TiDB Dashboard: Add OIDC based SSO support [#3884](https://github.com/tikv/pd/pull/3884)

+ TiFlash

    - Support the `HAVING()` function in DAG requests
    - Support the `DATE()` function
    - Add Grafana panels for write throughput per instance

## Improvements

+ TiDB

    - Trigger auto-analyze based on histogram row count [#26707](https://github.com/pingcap/tidb/pull/26707)
    - block the tiflash node for a period when it fails before. [#26757](https://github.com/pingcap/tidb/pull/26757)
    - Increasing the split region limit makes the split table and pre split more stable [#26657](https://github.com/pingcap/tidb/pull/26657)
    - support retry for mpp query [#26483](https://github.com/pingcap/tidb/pull/26483)
    - check the tiflash availabilities before launching mpp queries. [#26356](https://github.com/pingcap/tidb/pull/26356)
    - support stable result mode [#26084](https://github.com/pingcap/tidb/pull/26084)
    - Support the MySQL system variable init_connect and its associated features. [#26072](https://github.com/pingcap/tidb/pull/26072)
    - thoroughly push down count-distinct agg in the MPP mode. [#25861](https://github.com/pingcap/tidb/pull/25861)
    - Log warnings when agg function can not be pushdown in explain statement [#25736](https://github.com/pingcap/tidb/pull/25736)
    - Add error label for TiFlashQueryTotalCounter [#25327](https://github.com/pingcap/tidb/pull/25327)
    - Support getting the MVCC key through a secondary index in a clustered index table by HTTP API. [#24470](https://github.com/pingcap/tidb/pull/24470)
    - Optimize the parser object allocation in the prepared statement. [#24371](https://github.com/pingcap/tidb/pull/24371)

+ TiKV

    - Reduce resolved ts message size to save network bandwidth. [#10678](https://github.com/tikv/tikv/pull/10678)
    - Drop log instead of blocking threads when slogger thread is overloaded and queue is filled up. [#10864](https://github.com/tikv/tikv/pull/10864)
    - TiKV coprocessor slow log will only consider time spent on processing the request. [#10864](https://github.com/tikv/tikv/pull/10864)
    - Make prewrite as idempotent as possible to reduce the chance of undetermined errors. [#10587](https://github.com/tikv/tikv/pull/10587)
    - Avoid false "GC can not work" alert under low write flow. [#10662](https://github.com/tikv/tikv/pull/10662)
    - Database restored from BR or Lightning Local-backend is now smaller, should be matching the original cluster size when backed up. [#10643](https://github.com/tikv/tikv/pull/10643)
    - Ensure panic output is flushed to the log [#10487](https://github.com/tikv/tikv/pull/10487)

+ PD

    - Improved the performance of synchronizing Region information between PDs. [#3993](https://github.com/tikv/pd/pull/3993)

+ Tools

    + Dumpling

        - Support for backing up MySQL compatible databases that don't support START TRANSACTION  ... WITH CONSISTENT SNAPSHOT
        - Support for backing up MySQL compatible databases that don't support SHOW CREATE TABLE [#327](https://github.com/pingcap/dumpling/pull/327)

    + TiCDC

        - Optimize memory management when unified sorter is using memory to sort. [#2711](https://github.com/pingcap/ticdc/pull/2711)
        - This PR make the old owner handle DDL in Async mode. [#2605](https://github.com/pingcap/ticdc/pull/2605)
        - Prohibit operating TiCDC clusters across major and minor versions [#2598](https://github.com/pingcap/ticdc/pull/2598)
        - Reduce goroutine usage when a table's region transfer away from a TiKV node [#2377](https://github.com/pingcap/ticdc/pull/2377)
        - Remove file sorter. [#2326](https://github.com/pingcap/ticdc/pull/2326)
        - puller,mounter,processor: always pull the old value internally [#2305](https://github.com/pingcap/ticdc/pull/2305)
        - Better err msg when PD endpoint missing certificate [#2185](https://github.com/pingcap/ticdc/pull/2185)
        - Cleanup changefeed metrics when changefeed is removed.
        - Cleanup processor metrics when processor exits. [#2177](https://github.com/pingcap/ticdc/pull/2177)
        - Optimize workerpool for fewer goroutines when concurrency is high. [#2487](https://github.com/pingcap/ticdc/pull/2487)
        - Don't resolve lock immediately after a region is initialized. [#2265](https://github.com/pingcap/ticdc/pull/2265)

## Bug Fixes

+ TiDB

    - Fix tidb might panic while query hash partition table with `IS NULL` condition [#26963](https://github.com/pingcap/tidb/pull/26963)
    - Fix the overflow check of `float64` type is different with MySQL [#26724](https://github.com/pingcap/tidb/pull/26724)
    - Fix wrong charset and collation for case when function [#26672](https://github.com/pingcap/tidb/pull/26672)
    - Fix the issue that committing pessimistic transactions may report write-conflict errors. [#25974](https://github.com/pingcap/tidb/pull/25974)
    - Fix the bug that index keys in a pessimistic transaction may be repeatedly committed. [#26495](https://github.com/pingcap/tidb/pull/26495)
    - Fix the issue that TiDB may panic when resolving async-commit locks. [#25863](https://github.com/pingcap/tidb/pull/25863)
    - Fix the bug that a column may not be found when using INDEX MERGE [#25806](https://github.com/pingcap/tidb/pull/25806)
    - Fix the bug that `ALTER USER REQUIRE SSL` clears the user's `authentication_string` [#25348](https://github.com/pingcap/tidb/pull/25348)
    - Fix a bug that a new cluster's "tidb_gc_scan_lock_mode" global variable shows "PHYSICAL" instead of the actual default mode "LEGACY". [#25118](https://github.com/pingcap/tidb/pull/25118)
    - Fix the bug that `TIKV_REGION_PEERS` table did not have the correct DOWN status. [#24919](https://github.com/pingcap/tidb/pull/24919)
    - Fix the bug that memory leaks when HTTP api is used [#24649](https://github.com/pingcap/tidb/pull/24649)
    - Fix the bug that views don't support `DEFINER`. [#24532](https://github.com/pingcap/tidb/pull/24532)
    - Fix the bug that `tidb-server --help` exits with code 2 [#24074](https://github.com/pingcap/tidb/pull/24074)
    - fix the bug that setting the global variable `dml_batch_size` doesn't take effect [#24731](https://github.com/pingcap/tidb/pull/24731)
    - Fix the bug that using `read_from_storage` and partition tables will report an error [#24374](https://github.com/pingcap/tidb/pull/24374)
    - fix using aggregation functions may panic. [#24354](https://github.com/pingcap/tidb/pull/24354)
    - fix queries may panic due to statistics [#24061](https://github.com/pingcap/tidb/pull/24061)
    - fix `approx_percentile` may panic on a bit column [#23703](https://github.com/pingcap/tidb/pull/23703)
    - Fix the metrics in `Coprocessor Cache` is wrong in Grafana. [#26343](https://github.com/pingcap/tidb/pull/26343)
    - Fix the issue that concurrently truncating the same partition hangs DDL. [#26238](https://github.com/pingcap/tidb/pull/26238)

+ TiKV

    - RaftStore Snapshot GC fix: fix the issue that snapshot GC missed GC snapshot files when there's one snapshot file failed to be GC-ed. [#10872](https://github.com/tikv/tikv/pull/10872)
    - Fix TiKV panic when enable Titan and upgrade from pre-5.0 version [#10843](https://github.com/tikv/tikv/pull/10843)
    - Fix newer TiKV can't rollback to 5.0.x [#10843](https://github.com/tikv/tikv/pull/10843)
    - Fix TiKV panic when Titan is enabled and upgrade from < 5.0 versions to >= 5.0 versions. A cluster may hit the issue if it was upgraded from TiKV 3.x and enabled Titan before the upgrade in the past. [#10778](https://github.com/tikv/tikv/pull/10778)
    - Fix the resolve failures caused by the left pessimisic locks. [#10654](https://github.com/tikv/tikv/pull/10654)
    - Fix duration calculation panics on certain platforms [#10571](https://github.com/tikv/tikv/pull/10571)
    - Fix unencoded keys of `batch_get_command` in load-base-split [#10564](https://github.com/tikv/tikv/pull/10564)

+ PD

    - Fix the bug that PD would not fix down-peer in time. [#4082](https://github.com/tikv/pd/pull/4082)
    - Fix an issue where data is not stored when using max-replicas or location-labels to indirectly update default placement rule [#3914](https://github.com/tikv/pd/pull/3914)
    - Fix the bug that PD may panic during scaling out TiKV. [#3910](https://github.com/tikv/pd/pull/3910)
    - Reduce the conflict due to multiple scheduler running in same time [#3856](https://github.com/tikv/pd/pull/3856)
    - Fix the issue that the scheduler may appear again even if we have already executed the delete operation [#3823](https://github.com/tikv/pd/pull/3823)

+ TiFlash

    - Fix the potential panic issue that occurs when running table scan tasks
    - Fix the potential memory leak issue that occurs when executing `MPP` tasks
    - Fix a bug that TiFlash raises the error about `duplicated region` when handling `DAQ` requests
    - Fix the issue of unexpected results when executing the aggregation functions `COUNT` or `COUNT DISTINCT`
    - Fix the potential panic issue that occurs when executing `MPP` tasks
    - Fix a potential bug that TiFlash cannot restore data when deployed on multiple disks
    - Fix the potential panic issue that occurs when deconstructing `SharedQueryBlockInputStream`
    - Fix the potential panic issue that occurs when deconstructing `MPPTask`
    - Fix the issue of unexpected results when TiFlash failed to establish `MPP` connections
    - Fix the potential panic issue that occurs when resolving locks
    - Fix the issue that store size in metrics is inaccurate under heavy writing
    - Fix a bug of incorrect results that occurs when queries contain filters like `CONSTANT` `<` | `<=` | `>` | `>=` `COLUMN`
    - Fix the potential issue that TiFlash cannot GC the delta data after running for a long time
    - Fix a potential bug that metrics display wrong value
    - Fix the potential issue of data inconsistency that occurs when deployed on multiple disks

+ PD

    - Fix the bug that PD would not fix down-peer in time. [#4082](https://github.com/tikv/pd/pull/4082)
    - Fix an issue where data is not stored when using max-replicas or location-labels to indirectly update default placement rule [#3914](https://github.com/tikv/pd/pull/3914)
    - Fix the bug that PD may panic during scaling out TiKV. [#3910](https://github.com/tikv/pd/pull/3910)

+ Tools

    + Dumpling

        - fix pending on show table status in some mysql version [#342](https://github.com/pingcap/dumpling/pull/342)
        - Support for backing up MySQL compatible databases that don't support START TRANSACTION  ... WITH CONSISTENT SNAPSHOT
        - Support for backing up MySQL compatible databases that don't support SHOW CREATE TABLE [#327](https://github.com/pingcap/dumpling/pull/327)

    + TiCDC

        - Fix json encoding could panic when processing a string type value in some cases. [#2782](https://github.com/pingcap/ticdc/pull/2782)
        - Fix a bug that multiple processors could write the same table when this table is re-scheduling [#2728](https://github.com/pingcap/ticdc/pull/2728)
        - Fix OOM when TiCDC captures too many regions [#2724](https://github.com/pingcap/ticdc/pull/2724)
        - Fix gRPC keepalive error when memory pressure is high. [#2719](https://github.com/pingcap/ticdc/pull/2719)
        - Optimize memory management when unified sorter is using memory to sort. [#2711](https://github.com/pingcap/ticdc/pull/2711)
        - Fix a bug that causes TiCDC to panic on an unsigned tinyint [#2655](https://github.com/pingcap/ticdc/pull/2655)
        - Fix open protocol, don't output an empty value when there is no change in one transaction. [#2620](https://github.com/pingcap/ticdc/pull/2620)
        - Fixed a bug in DDL handling when the owner restarts. [#2610](https://github.com/pingcap/ticdc/pull/2610)
        - This PR make the old owner handle DDL in Async mode. [#2605](https://github.com/pingcap/ticdc/pull/2605)
        - Prohibit operating TiCDC clusters across major and minor versions [#2598](https://github.com/pingcap/ticdc/pull/2598)
        - Fix a bug in metadata management [#2558](https://github.com/pingcap/ticdc/pull/2558)
        - Add a global gRPC connection pool and share gRPC connections among kv clients. [#2533](https://github.com/pingcap/ticdc/pull/2533)
        - Fix a bug that multiple processors could write the same table when this table is re-scheduling [#2492](https://github.com/pingcap/ticdc/pull/2492)
        - Optimize workerpool for fewer goroutines when concurrency is high. [#2487](https://github.com/pingcap/ticdc/pull/2487)
        - fix outdated capture info may appear in capture list command [#2466](https://github.com/pingcap/ticdc/pull/2466)
        - Fix a bug that owner could meet ErrSchemaStorageTableMiss error and reset a changefeed by accident. [#2458](https://github.com/pingcap/ticdc/pull/2458)
        - fix the bug that changefeed cannot be removed if meet GcTTL Exceeded Error [#2456](https://github.com/pingcap/ticdc/pull/2456)
        - fix a bug where synchronizing large tables to cdclog failed. [#2445](https://github.com/pingcap/ticdc/pull/2445)
        - Fix CLI back-compatibility [#2413](https://github.com/pingcap/ticdc/pull/2413)
        - Reduce goroutine usage when a table's region transfer away from a TiKV node [#2377](https://github.com/pingcap/ticdc/pull/2377)
        - Remove file sorter. [#2326](https://github.com/pingcap/ticdc/pull/2326)
        - puller,mounter,processor: always pull the old value internally [#2305](https://github.com/pingcap/ticdc/pull/2305)
        - Fix minor runtime panic risk [#2299](https://github.com/pingcap/ticdc/pull/2299)
        - Fix potential DDL loss when owner crashes while executing DDL [#2292](https://github.com/pingcap/ticdc/pull/2292)
        - Don't resolve lock immediately after a region is initialized. [#2265](https://github.com/pingcap/ticdc/pull/2265)
        - Fix extra partition dispatching when adding new table partition. [#2263](https://github.com/pingcap/ticdc/pull/2263)
        - Better err msg when PD endpoint missing certificate [#2185](https://github.com/pingcap/ticdc/pull/2185)
        - Cleanup changefeed metrics when changefeed is removed.
        - Cleanup processor metrics when processor exits. [#2177](https://github.com/pingcap/ticdc/pull/2177)
