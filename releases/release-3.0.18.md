---
title: TiDB 3.0.18 Release Notes
---

# TiDB 3.0.18 Release Notes

Release date: August 21, 2020

TiDB version: 3.0.18

## Bug Fixes

+ TiDB

    - Fix wrong hash key for decimal [#19185](https://github.com/pingcap/tidb/pull/19185)
    - Fix an encode bug that causing the wrong result of hashJoin with set and enum [#19172](https://github.com/pingcap/tidb/pull/19172)

+ TiKV

    - Change GC failure log to Warning level [#8444](https://github.com/tikv/tikv/pull/8444)

+ TiDB Lightning

    - Fix the issue that the argument `--log-file` does not take effect [#345](https://github.com/pingcap/tidb-lightning/pull/345)
    - Fix syntax error on empty binary/hex literals when using TiDB backend [#357](https://github.com/pingcap/tidb-lightning/pull/357)
    - Fix the unexpected `switch-mode` in TiDB backend [#368](https://github.com/pingcap/tidb-lightning/pull/368)

## Improvements

+ TiDB Binlog

    - Support go time duration format for pump GC configuration [#996](https://github.com/pingcap/tidb-binlog/pull/996)
