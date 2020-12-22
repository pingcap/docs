---
title: TiDB 3.0.20 Release Notes
---

# TiDB 3.0.20 Release Notes

Release date: December 23, 2020

TiDB version: 3.0.20

## Compatibility Change

+ TiDB

    - Deprecate `enable-streaming` [#21054](https://github.com/pingcap/tidb/pull/21054)

## Improvement

+ TiKV

    - Add the `end_point_slow_log_threshold` configuration item [#9145](https://github.com/tikv/tikv/pull/9145)

## Bug Fixes

+ TiDB

    - Fix the resolved txn status cache for pessimistic transactions. [#21706](https://github.com/pingcap/tidb/pull/21706)
    - Fix the statistics are inaccurate when querying `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` [#21319](https://github.com/pingcap/tidb/pull/21319)
    - Raise an error when preparing the `load data` statement [#21222](https://github.com/pingcap/tidb/pull/21222)
    - `DELETE` may not delete data correctly when the database name is not in pure lower representation [#21205](https://github.com/pingcap/tidb/pull/21205)
    - Fix stack overflow when building recursive view [#21000](https://github.com/pingcap/tidb/pull/21000)
    - Fix an goroutine leak issue in TiKV client [#20863](https://github.com/pingcap/tidb/pull/20863)
    - Fix wrong default zero value for year type [#20828](https://github.com/pingcap/tidb/pull/20828)
    - Avoid goroutine leak in index lookup join [#20791](https://github.com/pingcap/tidb/pull/20791)
    - Fix "insert select for update" return malformed packet in pessimistic txn [#20681](https://github.com/pingcap/tidb/pull/20681)
    - Fix unknown time zone 'posixrules' [#20605](https://github.com/pingcap/tidb/pull/20605)
    - Fix a problem of data too long when converting from unsigned integer to bit [#20362](https://github.com/pingcap/tidb/pull/20362)
    - Fix corrupted default value for bit type column [#20339](https://github.com/pingcap/tidb/pull/20339)
    - Fix potentially incorrect results when one of the equal condition is Enum of Set type [#20296](https://github.com/pingcap/tidb/pull/20296)
    - Fix wrong behavior for `!= any()` [#20061](https://github.com/pingcap/tidb/pull/20061)
    - Fix an issue that invalid results using BETWEEN...AND... with type conversion [#21503](https://github.com/pingcap/tidb/pull/21503)
    - Fix compatibility for `ADDDATE` function [#21008](https://github.com/pingcap/tidb/pull/21008)
    - Set correct default value for new added enum column. [#20999](https://github.com/pingcap/tidb/pull/20999)
    - Fix the result of SQL `select DATE_ADD('2007-03-28 22:08:28',INTERVAL "-2.-2" SECOND)` to be same with the MySQL; [#20627](https://github.com/pingcap/tidb/pull/20627)
    - Fix incorrect default value when modify column [#20532](https://github.com/pingcap/tidb/pull/20532)
    - Fix function timestamp() get wrong result when input argument is type of float/decimal [#20469](https://github.com/pingcap/tidb/pull/20469)
    - Fix a potentially deadlock problem in statistic [#20424](https://github.com/pingcap/tidb/pull/20424)
    - Fix FLOAT data type: out of range data should not be inserted [#20251](https://github.com/pingcap/tidb/pull/20251)

+ TiKV

    - Fix the issue that reports a key-exist error when a key is locked and deleted by a committed transaction [#8931](https://github.com/tikv/tikv/pull/8931)

+ PD

    - Change the log level of the stale Region when loading Regions [#3064](https://github.com/pingcap/pd/pull/3064)
