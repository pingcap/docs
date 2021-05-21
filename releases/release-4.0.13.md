---
title: TiDB 4.0.13 Release Notes
---

# TiDB 4.0.13 Release Notes

Release date: May 28, 2021

TiDB version: 4.0.13

## New Feature

+ TiDB

    - Allow changing an `AUTO_INCREMENT` column to an `AUTO_RANDOM` one. [#24608](https://github.com/pingcap/tidb/pull/24608)
    - A set of client_errors_summary tables has been added to Information Schema. This helps keep track of which errors have been sent to clients. [#23267](https://github.com/pingcap/tidb/pull/23267)

## Improvements

+ TiDB

    - Skip reading mysql.stats_histograms if cached stats is up-to-date [#24352](https://github.com/pingcap/tidb/pull/24352)

+ TiKV

    - Make the calculation process of store used size precise [9904](https://github.com/tikv/tikv/pull/9904)
    - Set more regions in `EpochNotMatch` to reduce region miss [9731](https://github.com/tikv/tikv/pull/9731)
    - Speed up memory freeing [10035](https://github.com/tikv/tikv/pull/10035)

+ PD

    - Metrics: let tso processing time not include consumption on the network [#3524](https://github.com/pingcap/pd/pull/3524)
    - Dashboard: update to v2021.03.12.1 [#3469](https://github.com/pingcap/pd/pull/3469)

+ TiFlash

    - Automatically clean archive data to free up disk space

+ Tools

    + Backup & Restore (BR)

        - BR now supports backing up user tables created in the `mysql` schema. [#1077](https://github.com/pingcap/br/pull/1077)
        - Update the `checkVersion` to check both cluster and backup data. [#1090](https://github.com/pingcap/br/pull/1090)
        - BR now can tolerate minor TiKV disconnection during backup. [#1062](https://github.com/pingcap/br/pull/1062)

    + TiCDC

        - Implement processor flow control to avoid OOM. [#1751](https://github.com/pingcap/ticdc/pull/1751)
        - Add stale temporary files clean-up in Unified Sorter, and forbids sharing sort-dir. [#1741](https://github.com/pingcap/ticdc/pull/1741)
        - Add HTTP handler for failpoint [#1732](https://github.com/pingcap/ticdc/pull/1732)

## Bug Fixes

+ TiDB

    - Fix panic when subquery update stmt the table with generated columns. [#24658](https://github.com/pingcap/tidb/pull/24658)
    - Fix an issue which causes wrong duplicate query results when using multi-column index. [#24634](https://github.com/pingcap/tidb/pull/24634)
    - Fix an issue which causes wrong query result when using bit constant in expression DIV. [#24266](https://github.com/pingcap/tidb/pull/24266)
    - Fix an issue that `NO_ZERO_IN_DATE` SQL mode does not work in default value. [#24185](https://github.com/pingcap/tidb/pull/24185)
    - Fix an issue which causes wrong query result when using `UNION` between a bit column and a integer column. [#24026](https://github.com/pingcap/tidb/pull/24026)
    - Fix wrong TableDual plans caused by comparing Binary and Bytes incorrectly. [#23917](https://github.com/pingcap/tidb/pull/23917)
    - Fix `insert ignore on duplicate` may delete wrong record. [#23825](https://github.com/pingcap/tidb/pull/23825)
    - Fix the issue that audit plugin will cause tidb panic. [#23819](https://github.com/pingcap/tidb/pull/23819)
    - Fix collation for hash join building [#23812](https://github.com/pingcap/tidb/pull/23812)
    - Fix batch point lock maybe panic when condition value overflow. [#23778](https://github.com/pingcap/tidb/pull/23778)
    - Fix text type decode for old row format. [#23772](https://github.com/pingcap/tidb/pull/23772)
    - Fix bug when compare int_column with constant value [#23705](https://github.com/pingcap/tidb/pull/23705)
    - Fix `approx_percent` panic on bit column. [#23702](https://github.com/pingcap/tidb/pull/23702)
    - Fix a bug that causes TiDB to report `TiKV server timeout` when executing TiFlash batch request. [#23700](https://github.com/pingcap/tidb/pull/23700)
    - Fix index join return wrong result on prefix column index. [#23691](https://github.com/pingcap/tidb/pull/23691)
    - Fix an issue which causes wrong query result because of not take collation for binary literal into consideration. [#23598](https://github.com/pingcap/tidb/pull/23598)
    - Fix update panic on join having statement. [#23575](https://github.com/pingcap/tidb/pull/23575)
    - Fix an issue which causes TiFlash returns wrong result when using NULL constant in comparison expression. [#23474](https://github.com/pingcap/tidb/pull/23474)
    - Fix unexpected result when comparing year column with string constant. [#23335](https://github.com/pingcap/tidb/pull/23335)
    - Fix the issue that `Group_concat` panics when session.group_concat_max_len is small. [#23257](https://github.com/pingcap/tidb/pull/23257)
    - Fix incorrect duration between compare. [#23233](https://github.com/pingcap/tidb/pull/23233)
    - Fix the delete stmt privilege check. [#23215](https://github.com/pingcap/tidb/pull/23215)
    - Fix an issue that query return wrong query result for decimal type. [#23196](https://github.com/pingcap/tidb/pull/23196)
    - Fix some wrong error info when an the result of an expression out of range. [#23152](https://github.com/pingcap/tidb/pull/23152)
    - Fix a bug that IndexMerge is not used even the hint `USE_INDEX_MERGE` is specified. [#22924](https://github.com/pingcap/tidb/pull/22924)
    - Fix the bug that query returns wrong result when using enum or set column in where clause as an filter. [#22814](https://github.com/pingcap/tidb/pull/22814)
    - Fix a bug which causes panic when using the clustered index and the new collation [#21408](https://github.com/pingcap/tidb/pull/21408)
    - Fix the panic when analyze with collation enabled. [#21299](https://github.com/pingcap/tidb/pull/21299)
    - Fix the issue that SQL Views does not consider the default roles associated with the SQL DEFINER correctly. [#24531](https://github.com/pingcap/tidb/pull/24531)
    - Fix the bug that cancelling DDL job stalls. [#24445](https://github.com/pingcap/tidb/pull/24445)
    - Fix wrong collation for the function `Concat`. [#24300](https://github.com/pingcap/tidb/pull/24300)
    - Fix the bug that query returns wrong results when there is an in-subquery in the select field, and the outer side contains null tuples. [#24022](https://github.com/pingcap/tidb/pull/24022)
    - Fix the bug that TiFlash is chosen wrongly by the optimizer when TableScan is of decrease order. [#23974](https://github.com/pingcap/tidb/pull/23974)
    - Fix a bug that point_get plan returns different column name with MySQL. [#23970](https://github.com/pingcap/tidb/pull/23970)
    - Fix `show table status` for the database with upper-cased name. [#23958](https://github.com/pingcap/tidb/pull/23958)
    - Fix the bug that users do not need both Insert and Delete privileges on a table to perform REPLACE. [#23938](https://github.com/pingcap/tidb/pull/23938)
    - Fix some string function get wrong result. [#23878](https://github.com/pingcap/tidb/pull/23878)
    - Fix the panic when we calculate the partition range. [#23689](https://github.com/pingcap/tidb/pull/23689)
    - Fix a panic on batch point get for non-partitioned table with partition meta information. When a cluster is upgrade from a old version, its partition meta information maybe not null, but the `Enable` field is false, it should be treat as a non-partitioned table. [#23682](https://github.com/pingcap/tidb/pull/23682)
    - When TiDB was configured to listen on TCP and UNIX sockets, connections over TCP did not correctly validate that the remote host was permitted to connect. [#23513](https://github.com/pingcap/tidb/pull/23513)
    - Fix the bug that non-default collation causes wrong query result. [#22923](https://github.com/pingcap/tidb/pull/22923)
    - Fix the bug that the grafana panel of coprocessor cache does not work. [#22617](https://github.com/pingcap/tidb/pull/22617)
    - Fix panic occurs when stats inconsistency. [#22565](https://github.com/pingcap/tidb/pull/22565)

+ TiKV

    - Fix the bug that TiKV cannot startup when the end of file dict file is damaged [9963](https://github.com/tikv/tikv/pull/9963)
    - Limit CDC scan speed (128MB/s by default) [9983](https://github.com/tikv/tikv/pull/9983)
    - Reduce memory usage of CDC initial scan [10133](https://github.com/tikv/tikv/pull/10133)
    - Support back pressure CDC scan speed [10142](https://github.com/tikv/tikv/pull/10142)
    - Fix a potential OOM issue by avoiding unnecessary read for getting CDC old values [10031](https://github.com/tikv/tikv/pull/10031)
    - Fix a CDC OOM issue caused by reading old values [10197](https://github.com/tikv/tikv/pull/10197)
    - Add a timeout for s3 storage client to avoid client hangs without responses [10132](https://github.com/tikv/tikv/pull/10132)

+ TiFlash

    - Fix the issue that number of `delta-merge-tasks` is not reported to Prometheus
    - Fix the TiFlash panic issue that occurs during `Segment Split`
    - Fix the issue that panel `Region write Duration (write blocks)` in Grafana is shown in wrong place
    - Fix the potential issue that `DeleteRange` in storage engine fail to remove data
    - Fix the issue of incorrect results when casting the time type to the integer type
    - Fix a bug that the behavior of the bitwise operator is different from that of TiDB
    - Fix the issue of incorrect results when casting the string type to the integer type
    - Fix the issue that consecutive and fast writes might make TiFlash out of memory
    - Fix the TiFlash panic issue that occurs when writing data to dropped tables
    - Fix the potential issue that the exception of null pointer might be raised during the table GC
    - Fix the issue that TiFlash might panic during BR restore
    - Fix a bug that weights of some characters are wrong when using general CI collation
    - Fix the potential issue that data will be lost in tombstoned table
    - Fix the issue of incorrect results when comparing string which contains zero bytes
    - Fix the issue that logical function returns wrong result if input column contains null constants
    - Fix the issue that logical function only accept numeric type
    - Fix the issue of incorrect results when timestamp value is `1970-01-01` and the timezone offset is negative
    - Fix the issue that hash value of Decimal256 is not stable

+ Tools

    + TiCDC

        - Fix the deadlock caused by flow-control when the sorter's input channel has been blocked. [#1779](https://github.com/pingcap/ticdc/pull/1779)
        - Fix the problem that TiKV GC safe point is blocked indefinitely due to TiCDC changefeed checkpoint stagnation. [#1756](https://github.com/pingcap/ticdc/pull/1756)
        - Revert the update for explicit_defaults_for_timestamp which requires `SUPER` privilege when replicating to MySQL. [#1749](https://github.com/pingcap/ticdc/pull/1749)
