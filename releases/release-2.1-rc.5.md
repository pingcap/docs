---
title: TiDB 2.1 RC5 Release Notes
category: Releases
aliases: ['/docs/dev/releases/21rc5/']
---

<!-- markdownlint-disable MD032 -->

# TiDB 2.1 RC5 Release Notes

On November 12, 2018, TiDB 2.1 RC5 is released. Compared with TiDB 2.1 RC4, this release has great improvement in stability, SQL optimizer, statistics information, and execution engine.

## TiDB

+ SQL Optimizer
    - Fix the issue that `IndexReader` reads the wrong handle in some cases [#8132](https://github.com/pingcap/tidb/pull/8132)
    - Fix the issue occurred while the `IndexScan Prepared` statement uses `Plan Cache` [#8055](https://github.com/pingcap/tidb/pull/8055)
    - Fix the issue that the result of the `Union` statement is unstable [#8165](https://github.com/pingcap/tidb/pull/8165)
+ SQL Execution Engine
    - Improve the performance of TiDB on inserting or updating wide tables [#8024](https://github.com/pingcap/tidb/pull/8024)
    - Support the unsigned `int` flag in the `Truncate` built-in function [#8068](https://github.com/pingcap/tidb/pull/8068)
    - Fix the error occurred while converting JSON data to the decimal type [#8109](https://github.com/pingcap/tidb/pull/8109)
    - Fix the error occurred when you `Update` the float type [#8170](https://github.com/pingcap/tidb/pull/8170)
+ Statistics
    - Fix the incorrect statistics issue during point queries in some cases [#8035](https://github.com/pingcap/tidb/pull/8035)
    - Fix the selectivity estimation of statistics for primary key in some cases [#8149](https://github.com/pingcap/tidb/pull/8149)
    - Fix the issue that the statistics of deleted tables are not cleared up for a long period of time [#8182](https://github.com/pingcap/tidb/pull/8182)
+ Server
    + Improve the readability of logs and make logs better
        - [#8063](https://github.com/pingcap/tidb/pull/8063)
        - [#8053](https://github.com/pingcap/tidb/pull/8053)
        - [#8224](https://github.com/pingcap/tidb/pull/8224)
    - Fix the error occurred when obtaining the table data of `infoschema.profiling` [#8096](https://github.com/pingcap/tidb/pull/8096)
    - Replace the unix socket with the pumps client to write binlogs [#8098](https://github.com/pingcap/tidb/pull/8098)
    - Add the threshold value for the `tidb_slow_log_threshold` environment variable, which dynamically sets the slow log [#8094](https://github.com/pingcap/tidb/pull/8094)
    - Add the original length of a SQL statement truncated while the `tidb_query_log_max_len` environment variable dynamically sets logs [#8200](https://github.com/pingcap/tidb/pull/8200)
    - Add the `tidb_opt_write_row_id` environment variable to control whether to allow writing `_tidb_rowid` [#8218](https://github.com/pingcap/tidb/pull/8218)
    - Add an upper bound to the `Scan` command of ticlient, to avoid overbound scan [#8081](https://github.com/pingcap/tidb/pull/8081), [#8247](https://github.com/pingcap/tidb/pull/8247)
+ DDL
    - Fix the issue that executing DDL statements in transactions encounters an error in some cases [#8056](https://github.com/pingcap/tidb/pull/8056)
    - Fix the issue that executing `truncate table` in partition tables does not take effect [#8103](https://github.com/pingcap/tidb/pull/8103)
    - Fix the issue that the DDL operation does not roll back correctly after being cancelled in some cases [#8057](https://github.com/pingcap/tidb/pull/8057)
    - Add the `admin show next_row_id` command to return the next available row ID [#8268](https://github.com/pingcap/tidb/pull/8268)

## PD

+ Fix the issues related to `pd-ctl` reading the Region key
    - [#1298](https://github.com/pingcap/pd/pull/1298)
    - [#1299](https://github.com/pingcap/pd/pull/1299)
    - [#1308](https://github.com/pingcap/pd/pull/1308)
+ Fix the issue that the `regions/check` API returns the wrong result [#1311](https://github.com/pingcap/pd/pull/1311)
+ Fix the issue that PD cannot restart join after a PD join failure [#1279](https://github.com/pingcap/pd/pull/1279)
+ Fix the issue that `watch leader` might lose events in some cases [#1317](https://github.com/pingcap/pd/pull/1317)

## TiKV

+ Improve the error message of `WriteConflict` [#3750](https://github.com/tikv/tikv/pull/3750)
+ Add the panic mark file [#3746](https://github.com/tikv/tikv/pull/3746)
+ Downgrade grpcio to avoid the segment fault issue caused by the new version of gRPC [#3650](https://github.com/tikv/tikv/pull/3650)
+ Add an upper limit to the `kv_scan` interface [#3749](https://github.com/tikv/tikv/pull/3749)

## Tools

- Support the TiDB-Binlog cluster, which is not compatible with the older version of binlog [#8093](https://github.com/pingcap/tidb/pull/8093), [documentation](/tidb-binlog/tidb-binlog-overview.md)
