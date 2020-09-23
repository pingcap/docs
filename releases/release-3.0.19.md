---
title: TiDB 3.0.19 Release Notes
---

# TiDB 3.0.19 Release Notes

Release date: September 25, 2020

TiDB version: 3.0.19

## Improvements

+ TiDB

    - Mitigate the impact of failure recovery on QPS [#19764](https://github.com/pingcap/tidb/pull/19764)

## Bug Fixes

+ TiDB

    - Fix the `slow_query` error when the `slow-log` file does not exist [#20050](https://github.com/pingcap/tidb/pull/20050)
    - Add the privilege check for `SHOW STATS_META`, `SHOW STATS_BUCKET` [#19759](https://github.com/pingcap/tidb/pull/19759)
    - Forbid changing the decimal type to the integer type [#19681](https://github.com/pingcap/tidb/pull/19681)

## Others

+ TiDB

    - Fix the issue that alter enum/set type does not check constraint [#20045](https://github.com/pingcap/tidb/pull/20045)
    - Fix the panic that tidb-server does not release table locks [#20021](https://github.com/pingcap/tidb/pull/20021)
    - Fix the behavior of rewrite ScalarFunction IsTure . [#19901](https://github.com/pingcap/tidb/pull/19901)
    - Support adjusting the concurrency on the `union` operator [#19885](https://github.com/pingcap/tidb/pull/19885)

+ TiKV

    - Set `sync-log` to `true` always [#8636](https://github.com/tikv/tikv/pull/8636)
    - Fix the bug that TiKV panics when parsing responses with missing reason phrases [#8540](https://github.com/tikv/tikv/pull/8540)

+ PD

    - Add an alert rule for restart [#2789](https://github.com/pingcap/pd/pull/2789)
    - Change the import path from `pingcap/pd` to `tikv/pd` [#2779](https://github.com/pingcap/pd/pull/2779)
    - Change the copyright information from `PingCAP, Inc` to `TiKV Project Authors` [#2777](https://github.com/pingcap/pd/pull/2777)
