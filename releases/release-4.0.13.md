---
title: TiDB 4.0.13 Release Notes
---

# TiDB 4.0.13 Release Notes

Release date: May 28, 2021

TiDB version: 4.0.13

## Improvements

+ TiDB

    - Skip reading mysql.stats_histograms if cached stats is up-to-date [#24352](https://github.com/pingcap/tidb/pull/24352)

+ TiFlash

    - Automatically clean archive data to free up disk space [#1638](https://github.com/pingcap/tics/pull/1638)
    - No release notes [#1625](https://github.com/pingcap/tics/pull/1625)

## Bug Fixes

+ TiDB

    - Fix panic when subquery update stmt the table with generated columns [#24658](https://github.com/pingcap/tidb/pull/24658)
    - Fix the case that there could be duplicate ranges for multi-column index. [#24634](https://github.com/pingcap/tidb/pull/24634)
    - Fix wrong flen infer for bit constant [#24266](https://github.com/pingcap/tidb/pull/24266)
    - Fix an issue that `NO_ZERO_IN_DATE` SQL mode does not work in default value [#24185](https://github.com/pingcap/tidb/pull/24185)
    - Fix type merge about bit type. [#24026](https://github.com/pingcap/tidb/pull/24026)
    - Planner: fix wrong TableDual plans caused by comparing Binary and Bytes incorrectly [#23917](https://github.com/pingcap/tidb/pull/23917)
    - Fix insert ignore on duplicate may delete wrong record [#23825](https://github.com/pingcap/tidb/pull/23825)
    - Plugin: fix audit plugin will cause tidb panic [#23819](https://github.com/pingcap/tidb/pull/23819)
    - Fix collation for hash join building [#23812](https://github.com/pingcap/tidb/pull/23812)
    - Fix batch point lock maybe panic when condition value overflow [#23778](https://github.com/pingcap/tidb/pull/23778)
    - Fix text type decode for old row format [#23772](https://github.com/pingcap/tidb/pull/23772)
    - Fix bug when compare int_column with constant value [#23705](https://github.com/pingcap/tidb/pull/23705)
    - Fix approx_percent panic on bit column [#23702](https://github.com/pingcap/tidb/pull/23702)
    - Fix a bug that causes TiDB to report `TiKV server timeout` when executing TiFlash batch request. [#23700](https://github.com/pingcap/tidb/pull/23700)
    - Fix index join on prefix column index [#23691](https://github.com/pingcap/tidb/pull/23691)
    - Fix collation for binary literal [#23598](https://github.com/pingcap/tidb/pull/23598)
    - Fix update panic on join having statement. [#23575](https://github.com/pingcap/tidb/pull/23575)
    - Planner: fix inappropriate null flag of null constants [#23474](https://github.com/pingcap/tidb/pull/23474)
    - Fix unexpected constant fold when year compare string. [#23335](https://github.com/pingcap/tidb/pull/23335)
    - Group_concat aggr panic when session.group_concat_max_len is small. [#23257](https://github.com/pingcap/tidb/pull/23257)
    - Fix incorrect duration between compare [#23233](https://github.com/pingcap/tidb/pull/23233)
    - Fix the delete stmt privilege check. [#23215](https://github.com/pingcap/tidb/pull/23215)
    - Types: fix the bug about the wrong query result for decimal type [#23196](https://github.com/pingcap/tidb/pull/23196)
    - Fix wrong error info [#23152](https://github.com/pingcap/tidb/pull/23152)
    - Fix wrong index merge selection [#22924](https://github.com/pingcap/tidb/pull/22924)
    - Fix enum and set type expression in where clause [#22814](https://github.com/pingcap/tidb/pull/22814)
    - Fix a bug which causes panic when using the clustered index and the new collation [#21408](https://github.com/pingcap/tidb/pull/21408)
    - Fix the panic when analyze with collation enabled [#21299](https://github.com/pingcap/tidb/pull/21299)

+ TiFlash

    - Fix the bug that the number of storage delta-merge-tasks is not reported to Prometheus [#1838](https://github.com/pingcap/tics/pull/1838)
    - Fix a bug that causes TiFlash crash during Segment Split. [#1814](https://github.com/pingcap/tics/pull/1814)
    - Fix the bug that the Grafana panel `Region write Duration (write blocks)` may be shown in wrong place [#1804](https://github.com/pingcap/tics/pull/1804)
    - Fix a potential issue that the DeleteRange in the storage engine failed to remove some data. [#1789](https://github.com/pingcap/tics/pull/1789)
    - Fix problem that TiFlash coprocessor's cast time as int function may produce incorrect result. [#1785](https://github.com/pingcap/tics/pull/1785)
    - Fix problem that behavior of TiFlash coprocessor's bitwise operator is different from TiDB [#1773](https://github.com/pingcap/tics/pull/1773)
    - Fix the problem that TiFlash coprocessor's cast string as int function may produce incorrect result. [#1767](https://github.com/pingcap/tics/pull/1767)
    - Fix the issue that continuous and fast writing may make TiFlash OOM [#1737](https://github.com/pingcap/tics/pull/1737)
    - Fix the crash that causes by applying Raft commands to dropped tables [#1724](https://github.com/pingcap/tics/pull/1724)
    - Fix potential NPE in schema sync service when database is dropped between GC and getting the database info. [#1707](https://github.com/pingcap/tics/pull/1707)
    - Fix the issue that TiFlash may panic during br restore [#1697](https://github.com/pingcap/tics/pull/1697)
    - Fix the bug that some characters have wrong weights when using general CI collation [#1667](https://github.com/pingcap/tics/pull/1667)
    - Fix potential data loss when recovering a table that is previously dropped. [#1662](https://github.com/pingcap/tics/pull/1662)
    - Fix a string compare bug that sometimes >= and <= will return wrong result if the contains with `\0` [#1658](https://github.com/pingcap/tics/pull/1658)
    - Fix bug 1. logical function only accept numeric type as its input type, 2. logical function return wrong result if input column contains a null constant. [#1636](https://github.com/pingcap/tics/pull/1636)
    - Fix wrong return value of timestamp column if the timestamp value is `1970-01-01` and the timezone offset is negative [#1601](https://github.com/pingcap/tics/pull/1601)
    - Fix bug that Decimal256's hash value is not stable [#1597](https://github.com/pingcap/tics/pull/1597)

## 请对以下未分类的 PR 进行分类，并挪动到以上对应类别中（Compatibility Changes, New Features, Improvements, Bug Fixes）。如果某条 note 不属于本次发版，请删除

+ TiDB

    - Allow changing an `AUTO_INCREMENT` column to an `AUTO_RANDOM` one. [#24608](https://github.com/pingcap/tidb/pull/24608)
    - SQL Views now consider the default roles associated with the SQL DEFINER correctrly. [#24531](https://github.com/pingcap/tidb/pull/24531)
    - Ddl: fix the covert job to rollingback job [#24445](https://github.com/pingcap/tidb/pull/24445)
    - Fix wrong collation for concat function [#24300](https://github.com/pingcap/tidb/pull/24300)
    - Fix wrong results for in clause. [#24022](https://github.com/pingcap/tidb/pull/24022)
    - If bug that max(primary_key_col) may return wrong result on TiDB + TiFlash. [#23974](https://github.com/pingcap/tidb/pull/23974)
    - Fix a bug that point get plan returns wrong column name [#23970](https://github.com/pingcap/tidb/pull/23970)
    - Fix `show table status` for the database with upper-cased name. [#23958](https://github.com/pingcap/tidb/pull/23958)
    - Users now need both Insert and Delete privileges on a table to perform REPLACE. [#23938](https://github.com/pingcap/tidb/pull/23938)
    - Fix resource leak of Shuffle Executor. [#23888](https://github.com/pingcap/tidb/pull/23888)
    - Fix some string function get wrong result [#23878](https://github.com/pingcap/tidb/pull/23878)
    - Fix the panic when we calculate the partition range [#23689](https://github.com/pingcap/tidb/pull/23689)
    - Fix a panic on batch point get for non-partitioned table with partition meta information. When a cluster is upgrade from a old version, its partition meta information maybe not null, but the `Enable` field is false, it should be treat as a non-partitioned table. [#23682](https://github.com/pingcap/tidb/pull/23682)
    - When TiDB was configured to listen on TCP and UNIX sockets, connections over TCP did not correctly validate that the remote host was permitted to connect. [#23513](https://github.com/pingcap/tidb/pull/23513)
    - A set of client_errors_summary tables has been added to Information Schema. This helps keep track of which errors have been sent to clients. [#23267](https://github.com/pingcap/tidb/pull/23267)
    - Fix a bug may cause wrong constant propagation and get the wrong result. [#22923](https://github.com/pingcap/tidb/pull/22923)
    - Fix wrong bucket name of coprocessor cache. [#22617](https://github.com/pingcap/tidb/pull/22617)
    - Fix panic occurs when stats inconsistency [#22565](https://github.com/pingcap/tidb/pull/22565)

+ TiKV

    - Support back pressure CDC scan speed. [#10145](https://github.com/tikv/tikv/pull/10145)
    - Fix interference between connections to the same region. [#10144](https://github.com/tikv/tikv/pull/10144)
    - Cdc: skip seek old value for Put if cache returns None [#10141](https://github.com/tikv/tikv/pull/10141)
    - Reduce memory usage of CDC initial scan. [#10134](https://github.com/tikv/tikv/pull/10134)
    - Fix potential panics when input of cast_string_as_time is invalid UTF-8 bytes [#9994](https://github.com/tikv/tikv/pull/9994)
    - Cdc: limit scan speed (128MB/s by default) [#9983](https://github.com/tikv/tikv/pull/9983)
    - Fix the bug that TiKV cannot startup when the end of file dict file is damaged. [#9963](https://github.com/tikv/tikv/pull/9963)

+ PD

    - Metrics: let tso processing time not include consumption on the network [#3524](https://github.com/pingcap/pd/pull/3524)
    - Dashboard: update to v2021.03.12.1 [#3469](https://github.com/pingcap/pd/pull/3469)

+ Tools

    - BR

        * BR would check cluster version of backup now. [#1090](https://github.com/pingcap/br/pull/1090)
        * BR now support backing up user tables created in the `mysql` schema. [#1077](https://github.com/pingcap/br/pull/1077)
        * BR now can tolerate minor TiKV disconnection. [#1062](https://github.com/pingcap/br/pull/1062)

    - TiCDC

        * Fix bug in flow control [#1779](https://github.com/pingcap/ticdc/pull/1779)
        * Modified the update strategy of gcSafePoint.  Fix the problem that TiKV GC safe point is blocked indefinitely due to TiCDC changefeed checkpoint stagnation. [#1756](https://github.com/pingcap/ticdc/pull/1756)
        * Implement processor flow control to avoid OOM. [#1751](https://github.com/pingcap/ticdc/pull/1751)
        * Revert the update for explicit_defaults_for_timestamp which requires `SUPER` privilege when replicating to MySQL. [#1749](https://github.com/pingcap/ticdc/pull/1749)
        * Add stale temporary files clean-up in Unified Sorter, and forbids sharing sort-dir. [#1741](https://github.com/pingcap/ticdc/pull/1741)
        * Aadd http handler for failpoint [#1732](https://github.com/pingcap/ticdc/pull/1732)
