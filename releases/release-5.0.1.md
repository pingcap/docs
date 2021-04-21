---
title: TiDB 5.0.1 Release Notes
---

# TiDB 5.0.1 Release Notes

Release date: April 23, 2021

TiDB version: 5.0.1

## Improvements

+ TiKV

    - Use `zstd` to compress the snapshot [#10005](https://github.com/tikv/tikv/pull/10005)

+ PD

    - Modify score calculator to satisfy isomerous stores [#3605](https://github.com/pingcap/pd/pull/3605)
    - Avoid unexpected statistic modify after adding scatter region scheduler [#3602](https://github.com/pingcap/pd/pull/3602)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the summary log is not clear [#1009](https://github.com/pingcap/br/pull/1009)

## Bug Fixes

+ TiDB

    - Do not prune all columns for Projection [#24093](https://github.com/pingcap/tidb/pull/24093)
    - Fix wrong query result when column contains null values [#24063](https://github.com/pingcap/tidb/pull/24063)
    - Do not build MPP plan for scan with virtual columns [#24058](https://github.com/pingcap/tidb/pull/24058)
    - Fix wrong PointGet / TableDual plan reused in plan cache [#24043](https://github.com/pingcap/tidb/pull/24043)
    - Append common handle columns into the schema of index merge table plan [#24042](https://github.com/pingcap/tidb/pull/24042)
    - Fix the type merging about BIT type [#24027](https://github.com/pingcap/tidb/pull/24027)
    - Fix wrong TableDual plans caused by comparing Binary and Bytes incorrectly [#23918](https://github.com/pingcap/tidb/pull/23918)
    - Fix the issue that planner hints don't work in some batch/point-get plans [#23685](https://github.com/pingcap/tidb/pull/23685)
    - Fix the cases that DDL would parse the args failed when converting job status to rolling back [#24080](https://github.com/pingcap/tidb/pull/24080)
    - Fix range building for binary literal [#24041](https://github.com/pingcap/tidb/pull/24041)
    - Fix wrong results for in clause [#24023](https://github.com/pingcap/tidb/pull/24023)
    - Fix the wrong result of some string functions  [#23879](https://github.com/pingcap/tidb/pull/23879)
    - Users now need both INSERT and DELETE privileges on a table to perform REPLACE [#23939](https://github.com/pingcap/tidb/pull/23939)
    - Fix performance regression of point select [#24070](https://github.com/pingcap/tidb/pull/24070)

+ TiKV

    - Fix IN expr(coprocessor) didn't handle unsigned/signed int properly [#10018](https://github.com/tikv/tikv/pull/10018)
    - Fix the issue that there are lots of empty regions after batch ingest. [#10015](https://github.com/tikv/tikv/pull/10015)
    - Fix potential panics when input of cast_string_as_time is invalid UTF-8 bytes [#9995](https://github.com/tikv/tikv/pull/9995)
    - Fix the bug that TiKV cannot startup when the end of file dict file is damaged. [#9992](https://github.com/tikv/tikv/pull/9992)

+ TiFlash

    - Fix the potential issue that storage engine fails to remove some data while executing `DeleteRange`
    - Fix a bug that the function to cast time as int may produce incorrect result
    - Fix a bug that receiver cannot find tasks within 10s
    - Fix the potential issue that there may be invalid iterators in `cancelMPPQuery`
    - Fix a bug that behavior of `bitwise` operator is different from TiDB
    - Fix the issue that alert about overlapped ranges will be raised when using prefix key
    - Fix a bug that the function to cast string as int may produce incorrect result
    - Fix the issue that continuous and fast writing may make TiFlash OOM
    - Fix the issue that duplicated column name will make TiFlash raise error
    - Fix the issue that TiFlash fails to decode MPP plan
    - Fix the potential issue that null pointer exception may be raised during table GC
    - Fix the issue that TiFlash may panic while applying raft commands to dropped tables
    - Fix the issue that TiFlash may panic during BR restore

+ Tools

    + TiDB Lightning

        - Fix the bug that the table count in the progress log is wrong. [#1005](https://github.com/pingcap/br/pull/1005)

    + Backup & Restore (BR)

        - Fix the bug that caused the real backup speed may go beyond far the `--ratelimit`. [#1026](https://github.com/pingcap/br/pull/1026)
        - Fix the issue that BR cannot tolerate minor TiKV disconnection [#1019](https://github.com/pingcap/br/pull/1019)

    + TiCDC

        - Fix data race and unhelpful error message in unified sorter. [#1678](https://github.com/pingcap/ticdc/pull/1678)
        - Fix the issue that creates the existing table directory on minio when initializing causes uploading objects to fail. [#1672]
        - Set session variable `explicit_defaults_for_timestamp` to `ON` to make downstream MySQL5.7 keeps the same behavior with upstream TiDB. [#1659](https://github.com/pingcap/ticdc/pull/1659)
        - Fix the error handling for io.EOF may cause replication interruption. [#1648](https://github.com/pingcap/ticdc/pull/1648)
        - Correct TiKV CDC endpoint CPU metric in TiCDC dashboard. [#1645](https://github.com/pingcap/ticdc/pull/1645)
        - Increase the defaultBufferChanSize of logSink to avoid blocking [#1632](https://github.com/pingcap/ticdc/pull/1632)
