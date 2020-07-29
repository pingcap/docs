---
title: TiDB v3.0.17 Release Notes
---

# TiDB v3.0.17 Release Notes

Release date: Aug 03, 2020

TiDB version: 3.0.17

## Bug Fixes

+ TiDB

    - Return the actual error message instead of empty set when a query which contains IndexHashJoin or IndexMergeJoin encounter a panic [#18498](https://github.com/pingcap/tidb/pull/18498)
    - Fix unknown column error for sql like `select a from t having t.a` [#18432](https://github.com/pingcap/tidb/pull/18432)
    - Forbid adding primary key for a table when the table has no primary key or the table has an integer primary key already [#18342](https://github.com/pingcap/tidb/pull/18342)
    - Return empty set when executing `explain format="dot" for connection` [#17157](https://github.com/pingcap/tidb/pull/17157)
    - Fix STR_TO_DATE's handling for format token '%r', '%h' [#18725](https://github.com/pingcap/tidb/pull/18725)

+ TiKV

    - Fix a bug that may read stale data during region merging [#8111](https://github.com/tikv/tikv/pull/8111)

+ TiDB-Lightning

    - Fix the issue that the `log-file` flag is ignored. [#345](https://github.com/pingcap/tidb-lightning/pull/345)

## Improvements

+ TiDB

    - Ease the impact of stats feedback on cluster [#18770](https://github.com/pingcap/tidb/pull/18770)
    - Limit batch split count for one request [#18694](https://github.com/pingcap/tidb/pull/18694)
    - Accelerate `/tiflash/replica` HTTP API when there are many history DDL jobs in TiDB cluster [#18386](https://github.com/pingcap/tidb/pull/18386)
    - Improve row count estimation for index equal condition [#17609](https://github.com/pingcap/tidb/pull/17609)
    - Speed up the executing of `kill tidb conn_id` [#18506](https://github.com/pingcap/tidb/pull/18506)

+ TiKV

    - Add `hibernate-timeout` config that allows region being hibernated later to improve rolling update performance [#8207](https://github.com/tikv/tikv/pull/8207)

+ TiDB-Lightning

    - `[black-white-list]` has been deprecated with a newer, easier-to-understand filter format. [#332](https://github.com/pingcap/tidb-lightning/pull/332)

## Others

+ TiDB

    - Types: fix STR_TO_DATE's handling for format token '%r', '%h' [#18725](https://github.com/pingcap/tidb/pull/18725)
    - To speed up canceling a query [#18506](https://github.com/pingcap/tidb/pull/18506)
    - Util/memory: warn potential deadlock for Consume in remove [#18393](https://github.com/pingcap/tidb/pull/18393)
