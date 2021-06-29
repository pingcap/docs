---
title: TiDB 5.0.3 Release Notes
---

# TiDB 5.0.3 Release Notes

Release date: June 30, 2021

TiDB version: 5.0.3

## New Features

+ Tools

    + TiCDC

        - Add an HTTP API to get the changefeed information and the health information of the node [#1955](https://github.com/pingcap/ticdc/pull/1955)
        - Add the SASL/SCRAM support for the kafka sink [#1942](https://github.com/pingcap/ticdc/pull/1942)
        - Makes TiCDC support `--data-dir` at the server level [#2070](https://github.com/pingcap/ticdc/pull/2070)

## Improvements

+ TiDB

    - Support pushing down the `TopN` operator to TiFlash [#25162](https://github.com/pingcap/tidb/pull/25162)
    - Support pushing down the built-in function `json_unquote()` to TiKV [#25720](https://github.com/pingcap/tidb/pull/25720)
    - Support removing the union branch from the dual table [#25614](https://github.com/pingcap/tidb/pull/25614)
    - Support pushing down the built-in function `replace()` to TiFlash [#25565](https://github.com/pingcap/tidb/pull/25565)
    - Support pushing down the built-in functions `unix_timestamp()`, `concat()`, `year()`, `day()`, `datediff()`, `datesub()`, `castTimeAsString()`, and `concat_ws()` to TiFlash [#25564](https://github.com/pingcap/tidb/pull/25564)
    - Change the aggregate operator's cost factor [#25241](https://github.com/pingcap/tidb/pull/25241)
    - Support pushing down the `Limit` operator to TiFlash [#25159](https://github.com/pingcap/tidb/pull/25159)
    - Support pushing down the built-in function `str_to_date` to TiFlash [#25148](https://github.com/pingcap/tidb/pull/25148)
    - Allow the MPP outer join to choose the build table based on the table row count [#25142](https://github.com/pingcap/tidb/pull/25142)
    - Support pushing down the built-in functions `left()`, `right()`, and `abs()` to TiFlash [#25133](https://github.com/pingcap/tidb/pull/25133)
    - Support pushing down the Broadcast Cartesian join to TiFlash [#25106](https://github.com/pingcap/tidb/pull/25106)
    - Support pushing down the `Union All` operator to TiFlash [#25051](https://github.com/pingcap/tidb/pull/25051)
    - Support balancing the MPP query workload among different TiFlash nodes based on Regions [#24724](https://github.com/pingcap/tidb/pull/24724)
    - Support invalidating stale Regions in the cache after the MPP query is executed [#24432](https://github.com/pingcap/tidb/pull/24432)

+ TiKV

    - Limit the TiCDC sink's memory consumption [#10305](https://github.com/tikv/tikv/pull/10305)
    - Add the memory-bounded upper limit for the TiCDC old value cache [#10313](https://github.com/tikv/tikv/pull/10313)

+ PD

    - Update TiDB Dashboard to v2021.06.15.1 [#3798](https://github.com/pingcap/pd/pull/3798)

+ TiFlash

    - Support casting the `STRING` type to the `DOUBLE` type
    - Support the `STR_TO_DATE` function
    - Optimize the non-joined data in right outer join using multiple threads
    - Support the Cartesian join
    - Support the `LEFT()` and `RIGHT()` functions
    - Support automatically invalidating stale Regions in MPP queries
    - Support the `ABS()` function

+ Tools

    + TiCDC

        - Refine gRPC's reconnection logic and increase the KV client's throughput [#1922](https://github.com/pingcap/ticdc/pull/1922)
        - Make the sorter I/O errors more user-friendly [#1977](https://github.com/pingcap/ticdc/pull/1977)

## Bug Fixes

+ TiDB

    - Fix the issue that an incorrect result is returned when using merge join on the `SET` type column [#25694](https://github.com/pingcap/tidb/pull/25694)
    - Fix the data corruption issue in the `IN` expression's arguments [#25666](https://github.com/pingcap/tidb/pull/25666)
    - Avoid the sessions of GC being affected by global variables [#25609](https://github.com/pingcap/tidb/pull/25609)
    - Fix the panic issue that occurs when using `limit` in the window function queries [#25517](https://github.com/pingcap/tidb/pull/25517)
    - Fix the wrong value returned when querying a partitioned table using `Limit` [#25139](https://github.com/pingcap/tidb/pull/25139)
    - Fix the issue that `IFNULL` does not correctly take effect on the `ENUM` or `SET` type column [#25116](https://github.com/pingcap/tidb/pull/25116)
    - Fix the wrong results caused by changing the `count` in the join subqueries to `first_row` [#25062](https://github.com/pingcap/tidb/pull/25062)
    - Fix the query hang issue that occurs when `ParallelApply` is used under the `TopN` operator [#25011](https://github.com/pingcap/tidb/pull/25011)
    - Fix the issue that more results than expected are returned when executing SQL statements using multi-column prefix indexes [#24635](https://github.com/pingcap/tidb/pull/24635)
    - Fix the issue that the `<=>` operator cannot correctly take effect [#24633](https://github.com/pingcap/tidb/pull/24633)
    - Fix the data race issue of the parallel `Apply` operator [#24345](https://github.com/pingcap/tidb/pull/24345)
    - Fix the issue that the `index out of range` error is reported when sorting the IndexMerge results of the PartitionUnion operator [#24155](https://github.com/pingcap/tidb/pull/24155)
    - Do not allow setting a read timestamp to a future time [#25761](https://github.com/pingcap/tidb/pull/25761)
    - Fix the issue that the ODBC-styled constant (for example, `{d '2020-01-01'}`) cannot be used as the expression [#25577](https://github.com/pingcap/tidb/pull/25577)
    - Fix the issue that `SELECT DISTINCT` converted to `Batch Get` causes incorrect results [#25533](https://github.com/pingcap/tidb/pull/25533)
    - Fix the issue that backing off queries from TiFlash to TiKV cannot be triggered [#24600](https://github.com/pingcap/tidb/pull/24600)
    - Fix the `index-out-of-range` error that occurs when checking `only_full_group_by` [#24016](https://github.com/pingcap/tidb/pull/24016)

+ TiKV

    - Fix the wrong `tikv_raftstore_hibernated_peer_state` metric [#10431](https://github.com/tikv/tikv/pull/10431)
    - Fix the wrong arguments type of the `json_unquote()` function in the coprocessor [#10424](https://github.com/tikv/tikv/pull/10424)
    - Fix the issue that Backup & Restore reports the error of "file already exists" when TDE is enabled during the restore [#10421](https://github.com/tikv/tikv/pull/10421)
    - Skip clearing callback during graceful shutdown to avoid breaking ACID in some cases [#10396](https://github.com/tikv/tikv/pull/10396)
    - Fix a bug that the read index is shared for replica reads on a Leader [#10391](https://github.com/tikv/tikv/pull/10391)
    - Fix the wrong function that casts `DOUBLE` to `DOUBLE` [#10388](https://github.com/tikv/tikv/pull/10388)

+ TiFlash

    - Fix the issue that TiFlash keeps restarting because of the split failure
    - Fix the potential issue that TiFlash cannot delete the delta data
    - Fix a bug that TiFlash adds wrong padding for non-binary characters in the `CAST` function
    - Fix the issue of incorrect results when handling aggregation queries with complex `GROUP BY` columns
    - Fix the TiFlash panic issue that occurs under heavy write pressure
    - Fix the panic that occurs when the right jon key is not nullalbe and the left join key is nullable
    - Fix the potential issue that the `read-index` requests take a long time

+ Tools

    + TiCDC

        - Fix the issue that TiCDC owner exits when refreshing the checkpoint [#2031](https://github.com/pingcap/ticdc/pull/2031)
        - Fix a bug that some MySQL connection might leak after MySQL sink meets the error and pauses [#1946](https://github.com/pingcap/ticdc/pull/1946)
        - Fix the panic issue that occurs when TiCDC fails to read `/proc/meminfo` [#2024](https://github.com/pingcap/ticdc/pull/2024)
        - Reduce TiCDC's runtime memory consumption [#2012](https://github.com/pingcap/ticdc/pull/2012), [#1958](https://github.com/pingcap/ticdc/pull/1958)
        - Fix a bug that might cause TiCDC server panic due to the late calculation of resolved ts [#2047](https://github.com/pingcap/ticdc/pull/2047)
        - Fix the potential deadlock issue for the processor [#2142](https://github.com/pingcap/ticdc/pull/2142)

    + Backup & Restore (BR)

        - Fix a bug that all system tables are filtered during restore [#1224](https://github.com/pingcap/br/pull/1224)

    + TiDB Lightning

        - Fix the TiDB Lightning panic issue for some special data [#1268](https://github.com/pingcap/br/pull/1268)
        - Fix the EOF error reported when TiDB Lightning splits the imported large CSV files [#1189](https://github.com/pingcap/br/pull/1189)
        ?- Fix a bug that TiDB Lightning rebase wrong `auto_increment` base when the `auto_increment` field type is `FLOAT` or `DOUBLE` [#1186](https://github.com/pingcap/br/pull/1186)
        - Fix the issue that TiDB fails to parse the `DECIMAL` type data in Parquet files [#1277](https://github.com/pingcap/br/pull/1277)
