---
title: TiDB 4.0.11 Release Notes
---

# TiDB 4.0.11 Release Notes

Release date: February 4, 2021

TiDB version: 4.0.11

## New Features

+ TiDB

    - Implement `utf8_unicode_ci` and `utf8mb4_unicode_ci` collation [#22558](https://github.com/pingcap/tidb/pull/22558)

+ TiKV

    - Add `utf8mb4_unicode_ci` implement [#9577](https://github.com/tikv/tikv/pull/9577)
    - Add `cast_year_as_time` [#9299](https://github.com/tikv/tikv/pull/9299)

+ TiFlash

    - A coprocessor thread pool was added to queue coprocessor requests for execution, which can avoid OOM in some cases. Added two configs `cop_pool_size` and `batch_cop_pool_size`, default `NumOfPhysicalCores*2` [#1312](https://github.com/pingcap/tics/pull/1312)

## Improvements

+ TiDB

    - Reorder inner joins simplified from outer joins [#22402](https://github.com/pingcap/tidb/pull/22402)
    - Metrics: grafana dashboards support multiple clusters [#22534](https://github.com/pingcap/tidb/pull/22534)
    - server, sessionctx: add multi statement workaround. [#22468](https://github.com/pingcap/tidb/pull/22468)
    - Metrics slow query is divided into internal and general [#22405](https://github.com/pingcap/tidb/pull/22405)
    - Add `utf8_unicode_ci` and `utf8mb4_unicode_ci` interface. [#22099](https://github.com/pingcap/tidb/pull/22099)

+ TiKV

    - Add server info metrics for DBasS [#9591](https://github.com/tikv/tikv/pull/9591)
    - Grafana dashboards support multiple clusters [#9572](https://github.com/tikv/tikv/pull/9572)
    - Report RocksDB metrics to TiDB [#9316](https://github.com/tikv/tikv/pull/9316)
    - Record suspend time for coprocessor task [#9277](https://github.com/tikv/tikv/pull/9277)
    - Add key and size threshold for load-base-split [#9354](https://github.com/tikv/tikv/pull/9354)
    - Check whether file exist before importing [#9544](https://github.com/tikv/tikv/pull/9544)
    - Improve Fast Tune panels [#9180](https://github.com/tikv/tikv/pull/9180)

+ PD

    - Metrics: grafana dashboards support multiple clusters [#3398](https://github.com/pingcap/pd/pull/3398)

+ TiFlash

    - Optimize the performance of date_format function in TiFlash [#1339](https://github.com/pingcap/tics/pull/1339)
    - Optimize memory consumption of handling ingest SST

+ Tools

    + TiCDC

        - Add version in capture info and changefeed info [#1342](https://github.com/pingcap/ticdc/pull/1342)

    + TiDB Lightning

        - Improve import performance by creating tables in parallel [#502](https://github.com/pingcap/tidb-lightning/pull/502)
        - Improve import performance by skipping split regions if engine total size is smaller than region size [#524](https://github.com/pingcap/tidb-lightning/pull/524)
        - Add importing progress and optimize the accuracy of restore progress [#506](https://github.com/pingcap/tidb-lightning/pull/506)

## Bug Fixes

+ TiDB

    - Incorporate unicode_ci into constant propagation [#22614](https://github.com/pingcap/tidb/pull/22614)
    - Fix an issue that cause wrong collation and coercibility [#22602](https://github.com/pingcap/tidb/pull/22602)
    - Fix an issue that may get wrong collation result [#22599](https://github.com/pingcap/tidb/pull/22599)
    - Refine `CollationStrictness` to support incompatible strictnessship [#22582](https://github.com/pingcap/tidb/pull/22582)
    - Fix a bug that the `like` function returns the wrong result when using collation [#22531](https://github.com/pingcap/tidb/pull/22531)
    - Expression: handle duration type infer in least and greatest [#22580](https://github.com/pingcap/tidb/pull/22580)
    - Fixed LIKE expressions when a single character (`_`) wildcard follows a multiple character wildcard (`%`). [#22575](https://github.com/pingcap/tidb/pull/22575)
    - Expression: fix type infer for TiDB's builtin compare(least and greatest) [#22562](https://github.com/pingcap/tidb/pull/22562)
    - Fix a bug that makes the `like` function get the wrong result if pattern string is a Unicode string [#22529](https://github.com/pingcap/tidb/pull/22529)
    - Fix a bug that point get query does not get the snapshot data when the `@@tidb_snapshot` variable is set. [#22527](https://github.com/pingcap/tidb/pull/22527)
    - Avoid potential panic when generating hints from joins [#22518](https://github.com/pingcap/tidb/pull/22518)
    - Convert string to MySQL BIT correctly [#22420](https://github.com/pingcap/tidb/pull/22420)
    - Fix the 'index out of range ' issue when insert values to `tidb_rowid`. [#22359](https://github.com/pingcap/tidb/pull/22359)
    - Fix a bug about incorrectly reuse cached plan [#22353](https://github.com/pingcap/tidb/pull/22353)
    - Fix runtime panic in WEIGHT_STRING function when the length of binary/char is too large [#22332](https://github.com/pingcap/tidb/pull/22332)
    - Forbidden the invalid generated column with incorrect argument count. [#22174](https://github.com/pingcap/tidb/pull/22174)
    - Show process info when building plan. [#22148](https://github.com/pingcap/tidb/pull/22148)
    - Fix issue of runtime stats of index lookup reader doesn't accurate. [#22136](https://github.com/pingcap/tidb/pull/22136)
    - Add a cache for memory info when the cluster is deployed in container. [#22116](https://github.com/pingcap/tidb/pull/22116)
    - Fix issue of decode plan error cause by without escape special char. [#22022](https://github.com/pingcap/tidb/pull/22022)
    - Report error for invalid window specifications which are not used in window functions. [#21976](https://github.com/pingcap/tidb/pull/21976)
    - Throw error when prepared statement is execute, deallocate or prepare [#21972](https://github.com/pingcap/tidb/pull/21972)
    - Fix `insert ignore` into not exists partition should not report error [#21971](https://github.com/pingcap/tidb/pull/21971)
    - Unify the plan code for explain result and slow log. [#21964](https://github.com/pingcap/tidb/pull/21964)
    - Fix unknown columns in join using below agg [#21957](https://github.com/pingcap/tidb/pull/21957)
    - Fix wrong type inferring for ceiling function. [#21936](https://github.com/pingcap/tidb/pull/21936)
    - Double type column from table should ignore its decimal [#21916](https://github.com/pingcap/tidb/pull/21916)
    - Fix correlated aggregates which should be evaluated in outer query instead of in subqueries. [#21877](https://github.com/pingcap/tidb/pull/21877)
    - Report error for json object with key length >= 65536. [#21870](https://github.com/pingcap/tidb/pull/21870)
    - Fix compatibility issue with MySQL for function `dayname` [#21850](https://github.com/pingcap/tidb/pull/21850)
    - When using input types longer than blob (such as a longblob or longtext), the function `to_base64` always returned `NULL`. It now returns the correct value. [#21813](https://github.com/pingcap/tidb/pull/21813)
    - Fix the fail when we compare multi fields in the subquery [#21808](https://github.com/pingcap/tidb/pull/21808)
    - Fix compare float64 with float64 in json [#21785](https://github.com/pingcap/tidb/pull/21785)
    - Fix compare object json type [#21718](https://github.com/pingcap/tidb/pull/21718)
    - Fix the coercibility of the cast function [#21714](https://github.com/pingcap/tidb/pull/21714)
    - Fix unexpected panic when using IF function [#21711](https://github.com/pingcap/tidb/pull/21711)
    - Fix #20161, json search result null is not compatible with mysql [#21700](https://github.com/pingcap/tidb/pull/21700)
    - Check for only_full_group_by in ORDER BY and HAVING for query without group clause. [#21697](https://github.com/pingcap/tidb/pull/21697)
    - Fix the compatibility of extract day_time unit functions [#21676](https://github.com/pingcap/tidb/pull/21676)
    - Fix LEAD and LAG's default value can not adapt to field type [#21665](https://github.com/pingcap/tidb/pull/21665)
    - TiDB now checks to make sure that the `LOAD DATA` statement can only load data into base tables. [#21638](https://github.com/pingcap/tidb/pull/21638)
    - Handle invalid argument for addtime and subtime function [#21635](https://github.com/pingcap/tidb/pull/21635)
    - Use “round to nearest even” rule instead of “round half away from zero” for approximate-value numbers [#21628](https://github.com/pingcap/tidb/pull/21628)
    - The single-argument `WEEK()` call now recognize the global `@@default_week_format` even when the session one is not set explicitly. [#21623](https://github.com/pingcap/tidb/pull/21623)

+ TiKV

    - Fix failed to build TiKV with PROST=1 [#9604](https://github.com/tikv/tikv/pull/9604)
    - Fix unmatched memory information [#9589](https://github.com/tikv/tikv/pull/9589)
    - Fix the issue that end key of a partial rawkv-restore range is inclusive [#9583](https://github.com/tikv/tikv/pull/9583)
    - Fix the issue that when loading old value for CDC's incremental scan on a key where there's a rolled back transaction, in some cases TiKV may panic. [#9569](https://github.com/tikv/tikv/pull/9569)
    - Fix old value config glitch when changefeeds with different settings connect to one region [#9565](https://github.com/tikv/tikv/pull/9565)
    - Fix a crash problem when running a TiKV on a machine with a network interface lacking MAC address since v4.0.9. [#9516](https://github.com/tikv/tikv/pull/9516)
    - Fix the problem that TiKV OOM when we backup a huge region. [#9448](https://github.com/tikv/tikv/pull/9448)
    - Fix `region-split-check-diff` can not be customized [#9530](https://github.com/tikv/tikv/pull/9530)
    - Fix TiKV panicked when system time go back [#9542](https://github.com/tikv/tikv/pull/9542)

+ PD

    - Fix the issue that member health metrics not correct [#3368](https://github.com/pingcap/pd/pull/3368)
    - If a tombstone store still has peers, make it cannot be removed. [#3352](https://github.com/pingcap/pd/pull/3352)
    - Fix the issue that the store limit cannot be persisted [#3403](https://github.com/pingcap/pd/pull/3403)
    - Fix the limit constriction of the scatter range scheduler [#3401](https://github.com/pingcap/pd/pull/3401)

+ TiFlash

    - Fix the bug that `min/max` result is wrong for decimal types
    - Fix the bug that TiFlash may crash when reading data [#1358](https://github.com/pingcap/tics/pull/1358)
    - Fix the issue that some data written after DDL operation may be lost after data compaction [#1350](https://github.com/pingcap/tics/pull/1350)

+ Tools

    + TiCDC

        - Fix a bug that cdc server could exit unexpected when meeting ErrTaskStatusNotExists and the capture session is disconnected at the same time [#1240](https://github.com/pingcap/ticdc/pull/1240)
        - Fix the old-value switch of a changefeed could be affected by another changefeed [#1347](https://github.com/pingcap/ticdc/pull/1347)
        - Fix a bug that TiCDC server could hang when processing a new changefeed with invalid sort-engine parameter [#1309](https://github.com/pingcap/ticdc/pull/1309)
        - fix debug info panic on none owner node [#1349](https://github.com/pingcap/ticdc/pull/1349)
        - Fix metric `ticdc_processor_num_of_tables` and `ticdc_processor_table_resolved_ts` are properly updated when processor removes a table or the processor itself stops [#1351](https://github.com/pingcap/ticdc/pull/1351)
        - Fix potential data loss if a processor crashes when starting up a table [#1363](https://github.com/pingcap/ticdc/pull/1363)
        - Fix a bug in the owner that could lead to abnormal CDC server exits during table migrations [#1352](https://github.com/pingcap/ticdc/pull/1352)
        - Fix a bug TiCDC does not fail in time after service safepoint is lost [#1367](https://github.com/pingcap/ticdc/pull/1367)
        - Fix a bug that kv client may skip to recreate event feed receiving routine by accident [#1336](https://github.com/pingcap/ticdc/pull/1336)
        - Fix a bug that atomicity of transactions is broken in the downstream [#1375](https://github.com/pingcap/ticdc/pull/1375)

    + Backup & Restore (BR)

        - Fix the issue that missing file size in SSTMeta might cause TiKV to generate a big region [#702](https://github.com/pingcap/br/pull/702)
        - Fix the issue that br restores table auto id even if the table does not have one [#720](https://github.com/pingcap/br/pull/720)

    + TiDB Lightning

        - Fix the bug that TiDB-Lightning will trim all the empty sep when trim-last-sep is true, which causes "column count mismatch" in tidb backend [#535](https://github.com/pingcap/tidb-lightning/pull/535)
        - Fix the bug that tidb backend will panics if source file columns are more than target    table columns [#528](https://github.com/pingcap/tidb-lightning/pull/528)
        - Fix the bug that TiKV may panics if TiDB-Lightning retry ingest with retry write [#554](https://github.com/pingcap/tidb-lightning/pull/554)
