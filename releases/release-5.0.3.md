---
title: TiDB 5.0.3 Release Notes
---

# TiDB 5.0.3 Release Notes

Release date: June 30, 2021

TiDB version: 5.0.3

## Compatibility Changes

## New Features

## Improvements

+ TiDB

    - Support planner pushing down the TopN operator to MPP. [#25162](https://github.com/pingcap/tidb/pull/25162)
    - Enable the pushdown of builtin function `json_unquote()` to TiKV. [#25720](https://github.com/pingcap/tidb/pull/25720)
    - Planner/core: remove the union branch with dual table. [#25614](https://github.com/pingcap/tidb/pull/25614)
    - Support push down function replace to TiFlash. [#25565](https://github.com/pingcap/tidb/pull/25565)
    - Support push fucntion unix_timestamp,concat,year,day,datediff,datesub,castTimeAsString,concat_ws down to TiFlash. [#25564](https://github.com/pingcap/tidb/pull/25564)
    - Planner/core: change agg cost factor [#25241](https://github.com/pingcap/tidb/pull/25241)
    - Planner/core: support limit push down [#25159](https://github.com/pingcap/tidb/pull/25159)
    - Support pushing down the `str_to_date` functions to TiFlash [#25148](https://github.com/pingcap/tidb/pull/25148)
    - Allow mpp outer join to choose the build table based on table row count [#25142](https://github.com/pingcap/tidb/pull/25142)
    - Push down left/right/abs to tiflash [#25133](https://github.com/pingcap/tidb/pull/25133)
    - Support push down broadcast cartesian join to TiFlash [#25106](https://github.com/pingcap/tidb/pull/25106)
    - Planner/core: support union all for mpp. [#25051](https://github.com/pingcap/tidb/pull/25051)
    - Balance region for batch cop task [#24724](https://github.com/pingcap/tidb/pull/24724)
    - Store/copr: invalidate stale regions for Mpp query. [#24432](https://github.com/pingcap/tidb/pull/24432)

+ TiKV

    - CDC: limit CDC sink memory consumption [#10305](https://github.com/tikv/tikv/pull/10305)
    - CDC: change old value cache to memory-bounded [#10313](https://github.com/tikv/tikv/pull/10313)

+ TiFlash

    - Support casting the `STRING`  type to `DOUBLE` type
    - Support `STR_TO_DATE` function
    - Optimize non-joined data in right outer join by multi-threads
    - Support cartesian join
    - Support `LEFT` and `RIGHT` function
    - Invalidate stale regions for MPP queries
    - Support `ABS` function

## Bug Fixes

+ TiDB

    - Fix the issue that an incorrect result is returned when using merge join on the `SET` types. [#25694](https://github.com/pingcap/tidb/pull/25694)
    - Fix the `IN` expression arguments corruption issue. [#25666](https://github.com/pingcap/tidb/pull/25666)
    - Avoid sessions of GC being affected by global variables [#25609](https://github.com/pingcap/tidb/pull/25609)
    - Make sure limit outputs no more columns than its child [#25517](https://github.com/pingcap/tidb/pull/25517)
    - Planner: fix a panic caused by sinking a Limit with inlined Proj into IndexLookUp when accessing a partition table [#25139](https://github.com/pingcap/tidb/pull/25139)
    - Executor: fix ifnull bug when arg is enum/set [#25116](https://github.com/pingcap/tidb/pull/25116)
    - Generate correct number of rows when all agg funcs are pruned [#25062](https://github.com/pingcap/tidb/pull/25062)
    - Executor: make the ParallelApply be safe to be called again after returning empty results [#25011](https://github.com/pingcap/tidb/pull/25011)
    - Fix the case that there could be duplicate ranges for multi-column index. [#24635](https://github.com/pingcap/tidb/pull/24635)
    - Fix a nulleq bug [#24633](https://github.com/pingcap/tidb/pull/24633)
    - Executor: fix data race of parallel apply operator [#24345](https://github.com/pingcap/tidb/pull/24345)
    - Fix an issue that sorting on index-merge results in partition union reports 'index out of range'. [#24155](https://github.com/pingcap/tidb/pull/24155)
    - Do not allow setting read timestamp to a future time. [#25761](https://github.com/pingcap/tidb/pull/25761)
    - Fix the issue that ODBC-styled literal(like `{d '2020-01-01'}`...) cannot be used as the expression. [#25577](https://github.com/pingcap/tidb/pull/25577)
    - Planner: select distinct should bypass batchget [#25533](https://github.com/pingcap/tidb/pull/25533)
    - Store/tikv: change backoff type for missed tiflash peer. [#24600](https://github.com/pingcap/tidb/pull/24600)
    - Fix index-out-of-range error when checking only_full_group_by [#24016](https://github.com/pingcap/tidb/pull/24016)

+ TiKV

    - Fix wrong tikv_raftstore_hibernated_peer_state metric [#10431](https://github.com/tikv/tikv/pull/10431)
    - Copr: fix the wrong arguments type of json_unquote [#10424](https://github.com/tikv/tikv/pull/10424)
    - Fix the issue that br reports file already exists error when TDE enabled during restoration [#10421](https://github.com/tikv/tikv/pull/10421)
    - Skip clearing callback during graceful shutdown to avoid breaking ACID in some cases [#10396](https://github.com/tikv/tikv/pull/10396)
    - Fix the bug that share read index for replica reads on a leader [#10391](https://github.com/tikv/tikv/pull/10391)
    - Copr: fix wrong function cast double to double [#10388](https://github.com/tikv/tikv/pull/10388)

+ TiFlash

    - Fix the issue that TiFlash keeps restarting because of split failure
    - Fix the potential issue that TiFlash can not GC delta data
    - Fix the bug that TiFlash adds wrong padding for non-binary chars in `CAST` function
    - Fix the issue of incorrect results when handling aggregation queries with complex `GROUP BY` columns
    - Fix the TiFlash panic issue that occurs under heavy write pressure
    - Fix the panic that occurs when right join if the right jon key is not nullalbe and the left join key is nullable
    - Fix the potential issue that read-index requests cost long time

+ Tools

    - BR

        * Fix parquet parse when parse decimal type [#1277](https://github.com/pingcap/br/pull/1277)
        * Fix the bug that lightning returns EOF error when CSV file without '\r\n' at the last line and `strict-format = true` [#1189](https://github.com/pingcap/br/pull/1189)
        * Fix the bug that lightning rebase wrong auto_increment base when the auto_increment field type is float or double [#1186](https://github.com/pingcap/br/pull/1186)

## 以下 note 未分类。请将以下 note 进行分类 (New feature, Improvements, Bug fixes, Compatibility Changes 四类)，并移动到上面对应的标题下。如果某条 note 为多余的，请删除。如果漏抓取了 note，请手动补充

+ PD

    - release-note [#3798](https://github.com/pingcap/pd/pull/3798)

+ Tools

    - TiCDC

        * Fix potential deadlocks [#2142](https://github.com/pingcap/ticdc/pull/2142)
        * Fix a bug that could cause cdc server panic because of the late calculation of resolved ts [#2047](https://github.com/pingcap/ticdc/pull/2047)
        * Fix panic when TiCDC fails to read `/proc/meminfo` [#2024](https://github.com/pingcap/ticdc/pull/2024)
        * Reduce unnecessary memory consumption [#2012](https://github.com/pingcap/ticdc/pull/2012)
        * Make sorter IO errors more user-friendly. [#1977](https://github.com/pingcap/ticdc/pull/1977)
        * Fix Unified Sorter memory consumption when tables are many. [#1958](https://github.com/pingcap/ticdc/pull/1958)
        * Decrease the default gRPC connection pool size to decrease goroutines count. [#1951](https://github.com/pingcap/ticdc/pull/1951)
        * Fix a bug that some MySQL connection could leak after MySQL sink meets error and pauses. [#1946](https://github.com/pingcap/ticdc/pull/1946)
