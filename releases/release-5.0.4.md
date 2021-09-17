---
title: TiDB 5.0.4 Release Notes
---

# TiDB 5.0.4 Release Notes

Release Date: September 27, 2021

TiDB version: 5.0.4

## Compatibility changes

+ TiDB

    - Fix the issue that executing `SHOW VARIABLES` in a new session is slow. This fix reverts some changes made in [#19341](https://github.com/pingcap/tidb/pull/19341) and might cause compatibility issues. [#24326](https://github.com/pingcap/tidb/issues/24326)
    - Change the default value of the `tidb_stmt_summary_max_stmt_count` variable from `200` to `3000` [#25873](https://github.com/pingcap/tidb/pull/25873)
    + The following bug fixes change execution results, which might cause upgrade incompatibilities:
        - Fix the issue that TiDB returns wrong result when the children of `UNION` contain the `NULL` value [#26571](https://github.com/pingcap/tidb/pull/26571)
        - Fix the issue that `greatest(datetime) union null` returns empty string [#26565](https://github.com/pingcap/tidb/pull/26565)
        - Fix the issue that the behavior of the `last_day` function is incompatible in SQL mode [#26000](https://github.com/pingcap/tidb/pull/26000)
        - Fix the issue that the `having` clause might not work correctly [#27742](https://github.com/pingcap/tidb/pull/27742)
        - Fix the wrong execution results that occur when the collations around the `between` expression are different [#27548](https://github.com/pingcap/tidb/pull/27548)
        - Fix the wrong execution results that occur when the column in the `group_concat` function has a non-bin collation [#27528](https://github.com/pingcap/tidb/pull/27528)
        - Fix an issue that using a `count(distinct)` expression on multiple columns returns wrong result when the new collation is enabled [#27507](https://github.com/pingcap/tidb/pull/27507)
        - Fix the result wrong that occurs when the argument of the `extract` function is a negative duration [#27368](https://github.com/pingcap/tidb/pull/27368)
        - Fix the issue that inserting an invalid date does not report an error when the `SQL_MODE` is 'STRICT_TRANS_TABLES' [#27110](https://github.com/pingcap/tidb/pull/27110)
        - Fix the issue that using an invalid default date does not report an error when the `SQL_MODE` is 'NO_ZERO_IN_DATE' [#26903](https://github.com/pingcap/tidb/pull/26903)
        - Fix a bug on the query range of prefix index [#26261](https://github.com/pingcap/tidb/pull/26261)
        - Fix the issue that the `LOAD DATA` statement might abnormally import non-utf8 data [#26143](https://github.com/pingcap/tidb/pull/26143)
        - Fix the issue that `insert ignore on duplicate update` might insert wrong data when the secondary index has the same column as in the primary key [#25905](https://github.com/pingcap/tidb/pull/25905)
        - Fix the issue that `insert ignore duplicate update` might insert wrong data when a partitioned table has a clustered index [#25859](https://github.com/pingcap/tidb/pull/25859)
        - Fix the issue that the query result might be wrong when the key is the `ENUM` type in point get or batch point get [#24772](https://github.com/pingcap/tidb/pull/24772)
        - Fix the wrong result that occurs when dividing a `BIT`-type value [#24267](https://github.com/pingcap/tidb/pull/24267)
        - Fix the issue that the results of `prepared` statements and direct queries might be inconsistent [#23373](https://github.com/pingcap/tidb/pull/23373)
        - Fix the issue that the query result might be wrong when a `YEAR` type is compared with a string or an integer type [#23336](https://github.com/pingcap/tidb/pull/23336)

## Feature enhancements

+ TiDB

    - Support setting `tidb_enforce_mpp=1` to ignore the optimizer estimation and forcibly use the MPP mode [#26382](https://github.com/pingcap/tidb/pull/26382)

+ TiKV

    - Support changing TiCDC configurations dynamically [#10685](https://github.com/tikv/tikv/pull/10685)

+ PD

    - Add OIDC-based SSO support for TiDB Dashboard [#3884](https://github.com/tikv/pd/pull/3884)

+ TiFlash

    - Support the `HAVING()` function in DAG requests
    - Support the `DATE()` function
    - Add Grafana panels for write throughput per instance

## Improvements

+ TiDB

    - Trigger auto-analyze based on the histogram row count [#26707](https://github.com/pingcap/tidb/pull/26707)
    - Do not send requests to a TiFlash node for a period if it has failed and restarted before [#26757](https://github.com/pingcap/tidb/pull/26757)
    - Increase the `split region` limit to make `split table` and `presplit` more stable [#26657](https://github.com/pingcap/tidb/pull/26657)
    - Support retry for MPP queries [#26483](https://github.com/pingcap/tidb/pull/26483)
    - Check the availability of TiFlash before launching MPP queries [#26356](https://github.com/pingcap/tidb/pull/26356)
    - Support the stable result mode to make the query result more stable [#26084](https://github.com/pingcap/tidb/pull/26084)
    - Support the MySQL system variable `init_connect` and its associated features [#26072](https://github.com/pingcap/tidb/pull/26072)
    - Thoroughly push down the `COUNT(DISTINCT)` aggregation function in the MPP mode [#25861](https://github.com/pingcap/tidb/pull/25861)
    - Print log warnings when the aggregation function cannot be pushed down in `EXPLAIN` statements [#25736](https://github.com/pingcap/tidb/pull/25736)
    - Add error labels for `TiFlashQueryTotalCounter` in Grafana dashboard [#25327](https://github.com/pingcap/tidb/pull/25327)
    - Support getting the MVCC data of a clustered index table through a secondary index by HTTP API [#24470](https://github.com/pingcap/tidb/pull/24470)
    - Optimize the memory allocation of `prepared` statement in parser [#24371](https://github.com/pingcap/tidb/pull/24371)

+ TiKV

    - Handle read ready and write ready separately to reduce read latency [#10620](https://github.com/tikv/tikv/pull/10620)
    - Reduce the size of Resolved TS messages to save network bandwidth [#10678](https://github.com/tikv/tikv/pull/10678)
    - Drop log instead of blocking threads when the slogger thread is overloaded and the queue is filled up [#10864](https://github.com/tikv/tikv/pull/10864)
    - The slow log of TiKV coprocessor only considers the time spent on processing requests [#10864](https://github.com/tikv/tikv/pull/10864)
    - Make prewrite as idempotent as possible to reduce the chance of undetermined errors [#10587](https://github.com/tikv/tikv/pull/10587)
    - Avoid the false "GC can not work" alert under low write flow [#10662](https://github.com/tikv/tikv/pull/10662)
    - The database to be restored always matches the original cluster size during backup. [#10643](https://github.com/tikv/tikv/pull/10643)
    - Ensure that the panic output is flushed to the log [#10487](https://github.com/tikv/tikv/pull/10487)

+ PD

    - Improve the performance of synchronizing Region information between PDs [#3993](https://github.com/tikv/pd/pull/3993)

+ Tools

    + Dumpling

        - Support backing up MySQL-compatible databases that do not support the `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` or the `SHOW CREATE DATABASE` syntax

    + TiCDC

        - Optimize memory management when unified sorter is using memory to sort [#2711](https://github.com/pingcap/ticdc/pull/2711)
        - Prohibit operating TiCDC clusters across major or minor versions [#2598](https://github.com/pingcap/ticdc/pull/2598)
        - Reduce the goroutine usage when a table's Regions are all transferred away from a TiKV node [#2377](https://github.com/pingcap/ticdc/pull/2377)
        - Remove `file sorter` [#2326](https://github.com/pingcap/ticdc/pull/2326)
        - Always pull the old values from TiKV and the output is adjusted according to `enable-old-value` [#2305](https://github.com/pingcap/ticdc/pull/2305)
        - Improve the error message returned when a PD endpoint misses the certificate [#2185](https://github.com/pingcap/ticdc/pull/2185)
        - Optimize workerpool for fewer goroutines when concurrency is high [#2487](https://github.com/pingcap/ticdc/pull/2487)
        - Add a global gRPC connection pool and share gRPC connections among KV clients [#2533](https://github.com/pingcap/ticdc/pull/2533)

## Bug Fixes

+ TiDB

    - Fix the issue that TiDB might panic when querying a partitioned table and the partition key has the `IS NULL` condition [#26963](https://github.com/pingcap/tidb/pull/26963)
    - Fix the issue that the overflow check of the `FLOAT64` type is different with that of MySQL [#26724](https://github.com/pingcap/tidb/pull/26724)
    - Fix the wrong character set and collation for the `case when` function [#26672](https://github.com/pingcap/tidb/pull/26672)
    - Fix the issue that committing pessimistic transactions might cause write conflicts [#25974](https://github.com/pingcap/tidb/pull/25974)
    - Fix a bug that the index keys in a pessimistic transaction might be repeatedly committed [#26495](https://github.com/pingcap/tidb/pull/26495)
    - Fix the issue that TiDB might panic when resolving the async commit locks [#25863](https://github.com/pingcap/tidb/pull/25863)
    - Fix a bug that a column might not be found when using `INDEX MERGE` [#25806](https://github.com/pingcap/tidb/pull/25806)
    - Fix a bug that `ALTER USER REQUIRE SSL` clears users' `authentication_string` [#25348](https://github.com/pingcap/tidb/pull/25348)
    - Fix a bug that the value of the `tidb_gc_scan_lock_mode` global variable on a new cluster shows "PHYSICAL" instead of the actual default mode "LEGACY" [#25118](https://github.com/pingcap/tidb/pull/25118)
    - Fix the bug that the `TIKV_REGION_PEERS` system table does not show the correct `DOWN` status [#24919](https://github.com/pingcap/tidb/pull/24919)
    - Fix the issue of memory leaks that occurs when HTTP API is used [#24649](https://github.com/pingcap/tidb/pull/24649)
    - Fix the issue that views does not support `DEFINER` [#24532](https://github.com/pingcap/tidb/pull/24532)
    - Fix the issue that `tidb-server --help` exits with the code `2` [#24074](https://github.com/pingcap/tidb/pull/24074)
    - Fix the issue that setting the global variable `dml_batch_size` does not take effect [#24731](https://github.com/pingcap/tidb/pull/24731)
    - Fix the issue that using `read_from_storage` and partitioned table at the same time causes an error [#24374](https://github.com/pingcap/tidb/pull/24374)
    - Fix the issue that TiDB panics when executing the projection operator [#24354](https://github.com/pingcap/tidb/pull/24354)
    - Fix the issue that queries might panic due to statistics [#24061](https://github.com/pingcap/tidb/pull/24061)
    - Fix the issue that using the `approx_percentile` function might panic on a `BIT` column [#23703](https://github.com/pingcap/tidb/pull/23703)
    - Fix the issue that the metrics on the **Coprocessor Cache** panel are wrong in Grafana [#26343](https://github.com/pingcap/tidb/pull/26343)
    - Fix the issue that concurrently truncating the same partition causes DDL statements to stuck [#26238](https://github.com/pingcap/tidb/pull/26238)
    - Fix the issue of wrong query results that occurs when the session variable is used as the `GROUP BY` item [#27637](https://github.com/pingcap/tidb/pull/27637)
    - Fix the wrong implicit conversion between `VARCHAR` and timestamp when joining tables [#25990](https://github.com/pingcap/tidb/pull/25990)
    - Fix the wrong results in associated subquery statements [#27283](https://github.com/pingcap/tidb/pull/27283)

+ TiKV

    ?- Fix the issue that snapshot GC might miss GC snapshot files when there is a snapshot file failed to be garbage-collected [#10872](https://github.com/tikv/tikv/pull/10872)
    - Fix the TiKV panic issue that occurs when upgrading from a pre-5.0 version with Titan enabled [#10843](https://github.com/tikv/tikv/pull/10843)
    - Fix the issue that TiKV of a newer version cannot be rolled back to v5.0.x [#10843](https://github.com/tikv/tikv/pull/10843)
    - Fix the TiKV panic issue that occurs when upgrading from a pre-5.0 versions to a 5.0 version or later. If a cluster was upgraded from TiKV v3.x with Titan enabled before the upgrade in the past, this cluster might encounter the issue. [#10778](https://github.com/tikv/tikv/pull/10778)
    - Fix the parsing failure caused by the left pessimistic locks [#10654](https://github.com/tikv/tikv/pull/10654)
    - Fix the panic that occurs when calculating duration on certain platforms [#10571](https://github.com/tikv/tikv/pull/10571)
    - Fix the issue that the keys of `batch_get_command` in Load Base Split are unencoded [#10564](https://github.com/tikv/tikv/pull/10564)

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
        - Fix a bug that causes TiCDC to panic on an unsigned tinyint [#2655](https://github.com/pingcap/ticdc/pull/2655)
        - Fix open protocol, don't output an empty value when there is no change in one transaction. [#2620](https://github.com/pingcap/ticdc/pull/2620)
        - Fixed a bug in DDL handling when the owner restarts. [#2610](https://github.com/pingcap/ticdc/pull/2610)
        - This PR make the old owner handle DDL in Async mode. [#2605](https://github.com/pingcap/ticdc/pull/2605)
        - Fix a bug in metadata management [#2558](https://github.com/pingcap/ticdc/pull/2558)
        - Fix a bug that multiple processors could write the same table when this table is re-scheduling [#2492](https://github.com/pingcap/ticdc/pull/2492)
        - fix outdated capture info may appear in capture list command [#2466](https://github.com/pingcap/ticdc/pull/2466)
        - Fix a bug that owner could meet ErrSchemaStorageTableMiss error and reset a changefeed by accident. [#2458](https://github.com/pingcap/ticdc/pull/2458)
        - fix the bug that changefeed cannot be removed if meet GcTTL Exceeded Error [#2456](https://github.com/pingcap/ticdc/pull/2456)
        - fix a bug where synchronizing large tables to cdclog failed. [#2445](https://github.com/pingcap/ticdc/pull/2445)
        - Fix CLI back-compatibility [#2413](https://github.com/pingcap/ticdc/pull/2413)
        - Fix minor runtime panic risk [#2299](https://github.com/pingcap/ticdc/pull/2299)
        - Fix potential DDL loss when owner crashes while executing DDL [#2292](https://github.com/pingcap/ticdc/pull/2292)
        - Don't resolve lock immediately after a region is initialized. [#2265](https://github.com/pingcap/ticdc/pull/2265)
        - Fix extra partition dispatching when adding new table partition. [#2263](https://github.com/pingcap/ticdc/pull/2263)
        - Cleanup changefeed metrics when changefeed is removed.
        - Cleanup processor metrics when processor exits. [#2177](https://github.com/pingcap/ticdc/pull/2177)
