---
title: TiDB 5.0.4 Release Notes
---

# TiDB 5.0.4 Release Notes

Release Date: September 27, 2021

TiDB version: 5.0.4

## Compatibility Changes

+ TiDB

    - Revert #19341 to avoid #24326 [#26258](https://github.com/pingcap/tidb/pull/26258)

## Improvements

+ TiDB

    - Trigger auto-analyze based on histogram row count [#26707](https://github.com/pingcap/tidb/pull/26707)

+ TiKV

    - separate read write ready to reduce read latency [#10620](https://github.com/tikv/tikv/pull/10620)

## Bug Fixes

+ TiDB

    - tidb panic while query hash partition table with is null condition [#26963](https://github.com/pingcap/tidb/pull/26963)
    - planner: fix the unstable test case TestAnalyzeIncremental [#26851](https://github.com/pingcap/tidb/pull/26851)
    - Keep the overflow check logic same with mysql [#26724](https://github.com/pingcap/tidb/pull/26724)
    - Fix wrong charset and collation for case when function [#26672](https://github.com/pingcap/tidb/pull/26672)
    - Fix the case that TiDB would return the wrong result when the children of the UNION contain pure NULL values [#26571](https://github.com/pingcap/tidb/pull/26571)
    - Fix the issue that greatest(datetime) union null returns empty string [#26565](https://github.com/pingcap/tidb/pull/26565)
    - fix incompatible last_day func behavior in sql mode [#26000](https://github.com/pingcap/tidb/pull/26000)
    - Fix the issue that committing pessimistic transactions may report write-conflict errors. [#25974](https://github.com/pingcap/tidb/pull/25974)
    - Fix the wrong result after "insert ignore on duplicate update" in the secondary index has the same column in primary key but has prefix length [#25905](https://github.com/pingcap/tidb/pull/25905)
    - Fix the wrong result for "insert ignore duplicate up" on partition table when handle changed and duplicated on secondary index [#25859](https://github.com/pingcap/tidb/pull/25859)
    - fix wrong enum key in point get [#24772](https://github.com/pingcap/tidb/pull/24772)
    - fix dml_batch_size doesn't load the global variable [#24731](https://github.com/pingcap/tidb/pull/24731)
    - planner: filter conflict read_from_storage hints [#24374](https://github.com/pingcap/tidb/pull/24374)
    - fix wrong type infer for agg function when type is null. [#24354](https://github.com/pingcap/tidb/pull/24354)
    - fix wrong flen infer for bit constant [#24267](https://github.com/pingcap/tidb/pull/24267)
    - fix some potential panic in statistics [#24061](https://github.com/pingcap/tidb/pull/24061)
    - fix approx_percent panic on bit column [#23703](https://github.com/pingcap/tidb/pull/23703)
    - fix get var expr when session var is hex literal [#23373](https://github.com/pingcap/tidb/pull/23373)
    - fix unexpected constant fold when year compare string. [#23336](https://github.com/pingcap/tidb/pull/23336)

+ PD

    - Fix the bug that PD would not fix down-peer in time. [#4082](https://github.com/tikv/pd/pull/4082)
    - Fix an issue where data is not stored when using max-replicas or location-labels to indirectly update default placement rule [#3914](https://github.com/tikv/pd/pull/3914)
    - Fix the bug that PD may panic during scaling out TiKV. [#3910](https://github.com/tikv/pd/pull/3910)

## 以下 note 未分类。请将以下 note 进行分类 (Feature enhancements, Improvements, Bug fixes, Compatibility Changes 四类)，并移动到上面对应的标题下。如果某条 note 为多余的，请删除。如果漏抓取了 note，请手动补充

+ TiDB

    - fix wrong selection push down when having above agg [#27742](https://github.com/pingcap/tidb/pull/27742)
    - fix expression rewrite makes between expr infers wrong collation. [#27548](https://github.com/pingcap/tidb/pull/27548)
    - make `group_concat` function consider the collation [#27528](https://github.com/pingcap/tidb/pull/27528)
    - Fix bug that count disctinct on multi-columns return wrong result when new collation is on. [#27507](https://github.com/pingcap/tidb/pull/27507)
    - Fix an issue that the `TABLESAMPLE` query result from partitioned tables is not sorted as expected. [#27412](https://github.com/pingcap/tidb/pull/27412)
    - expression: fix extract bug when argument is a negative duration [#27368](https://github.com/pingcap/tidb/pull/27368)
    - planner: add missing column for Apply convert to Join [#27283](https://github.com/pingcap/tidb/pull/27283)
    - The undocumented `/debug/sub-optimal-plan`  HTTP API has been removed. [#27263](https://github.com/pingcap/tidb/pull/27263)
    - executor: fix unexpected behavior when casting invalid string to date [#27110](https://github.com/pingcap/tidb/pull/27110)
    - Fix an issue that NO_ZERO_IN_DATE does not work on the default values. [#26903](https://github.com/pingcap/tidb/pull/26903)
    - store/copr: block the tiflash node for a period when it fails before. [#26757](https://github.com/pingcap/tidb/pull/26757)
    - Increasing the split region limit makes the split table and pre split more stable [#26657](https://github.com/pingcap/tidb/pull/26657)
    - Fix the issue that point get does not use lite version resolve lock [#26560](https://github.com/pingcap/tidb/pull/26560)
    - Fix the bug that index keys in a pessimistic transaction may be repeatedly committed. [#26495](https://github.com/pingcap/tidb/pull/26495)
    - store/copr: support retry for mpp query [#26483](https://github.com/pingcap/tidb/pull/26483)
    - Support set tidb_enforce_mpp=1 to enforce use mpp mode. [#26382](https://github.com/pingcap/tidb/pull/26382)
    - mpp: check the tiflash availabilities before launching mpp queries. [#26356](https://github.com/pingcap/tidb/pull/26356)
    - Fix copt-cache metrics, it will display the number of  hits/miss/evict on Grafana. [#26343](https://github.com/pingcap/tidb/pull/26343)
    - fix a bug on the query range of prefix index [#26261](https://github.com/pingcap/tidb/pull/26261)
    - Fix the issue that concurrently truncating the same partition hangs DDL. [#26238](https://github.com/pingcap/tidb/pull/26238)
    - Change the lock record into put record for the index keys using point/batch point get for update read. [#26224](https://github.com/pingcap/tidb/pull/26224)
    - load: fix load data with non-utf8 can succeed [#26143](https://github.com/pingcap/tidb/pull/26143)
    - planner: support stable result mode [#26084](https://github.com/pingcap/tidb/pull/26084)
    - TiDB now supports the mysql system variable init_connect and associated functionality. [#26072](https://github.com/pingcap/tidb/pull/26072)
    - Enlarge the variable tidb_stmt_summary_max_stmt_count default value from 200 to 3000 [#25873](https://github.com/pingcap/tidb/pull/25873)
    - Fix the issue that TiDB may panic when resolving async-commit locks. [#25863](https://github.com/pingcap/tidb/pull/25863)
    - planner/core: thoroughly push down count-distinct agg in the MPP mode. [#25861](https://github.com/pingcap/tidb/pull/25861)
    - planner: check filter condition in func convertToPartialTableScan [#25806](https://github.com/pingcap/tidb/pull/25806)
    - Log warnings when agg function can not be pushdown in explain statement [#25736](https://github.com/pingcap/tidb/pull/25736)
    - Important security issue for handling ALTER USER statements [#25348](https://github.com/pingcap/tidb/pull/25348)
    - metrics: Add err label for TiFlashQueryTotalCounter [#25327](https://github.com/pingcap/tidb/pull/25327)
    - Fix a bug that a new cluster's "tidb_gc_scan_lock_mode" global variable shows "PHYSICAL" instead of the actual default mode "LEGACY". [#25118](https://github.com/pingcap/tidb/pull/25118)
    - Fix the bug that TIKV_REGION_PEERS table did not have the correct DOWN status. [#24919](https://github.com/pingcap/tidb/pull/24919)
    - add table name in log [#24802](https://github.com/pingcap/tidb/pull/24802)
    - Handle a potential statistic object's memory leak when HTTP api is used [#24649](https://github.com/pingcap/tidb/pull/24649)
    - SQL Views now consider the default roles associated with the SQL DEFINER correctrly. [#24532](https://github.com/pingcap/tidb/pull/24532)
    - Support getting the MVCC key of the secondary index in a clustered index table by HTTP API. [#24470](https://github.com/pingcap/tidb/pull/24470)
    - Optimize the parser object allocation in the prepared statement. [#24371](https://github.com/pingcap/tidb/pull/24371)
    - Set the return value to 0 if --help is passed to cli, for golang below version 1.15 [#24074](https://github.com/pingcap/tidb/pull/24074)

+ TiKV

    - RaftStore Snapshot GC fix: fix the issue that snapshot GC missed GC snapshot files when there's one snapshot file failed to be GC-ed. [#10872](https://github.com/tikv/tikv/pull/10872)
    - TiKV coprocessor slow log will only consider time spent on processing the request. [#10864](https://github.com/tikv/tikv/pull/10864)
    - Drop log instead of blocking threads when slogger thread is overloaded and queue is filled up. [#10864](https://github.com/tikv/tikv/pull/10864)
    - Fix TiKV panic when enable Titan and upgrade from pre-5.0 version [#10843](https://github.com/tikv/tikv/pull/10843)
    - Fix newer TiKV can't rollback to 5.0.x [#10843](https://github.com/tikv/tikv/pull/10843)
    - Fix TiKV panic when Titan is enabled and upgrade from < 5.0 versions to >= 5.0 versions. A cluster may hit the issue if it was upgraded from TiKV 3.x and enabled Titan before the upgrade in the past. [#10778](https://github.com/tikv/tikv/pull/10778)
    - Support changing CDC configs dynamically [#10685](https://github.com/tikv/tikv/pull/10685)
    - Reduce resolved ts message size to save network bandwidth. [#10678](https://github.com/tikv/tikv/pull/10678)
    - Avoid false "GC can not work" alert under low write flow. [#10662](https://github.com/tikv/tikv/pull/10662)
    - Fix the resolve failures caused by the left pessimisic locks. [#10654](https://github.com/tikv/tikv/pull/10654)
    - Database restored from BR or Lightning Local-backend is now smaller, should be matching the original cluster size when backed up. [#10643](https://github.com/tikv/tikv/pull/10643)
    - Make prewrite as idempotent as possible to reduce the chance of undetermined errors. [#10587](https://github.com/tikv/tikv/pull/10587)
    - Fix duration calculation panics on certain platforms [#10571](https://github.com/tikv/tikv/pull/10571)
    - Fix unencoded keys of `batch_get_command` in load-base-split [#10564](https://github.com/tikv/tikv/pull/10564)
    - Ensure panic output is flushed to the log [#10487](https://github.com/tikv/tikv/pull/10487)

+ PD

    - Improved the performance of synchronizing Region information between PDs. [#3993](https://github.com/tikv/pd/pull/3993)
    - Improved the performance of synchronizing Region information between PDs. [#3934](https://github.com/tikv/pd/pull/3934)
    - TiDB Dashboard: Add OIDC based SSO support [#3884](https://github.com/tikv/pd/pull/3884)
    - Reduce the conflict due to multiple scheduler running in same time [#3856](https://github.com/tikv/pd/pull/3856)
    - Fix the issue that the scheduler may appear again even if we have already executed the delete operation [#3823](https://github.com/tikv/pd/pull/3823)

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
        - Fix the bug that table is not replicated when it changes from ineligible to eligible by DDL [#1488](https://github.com/pingcap/ticdc/pull/1488)
