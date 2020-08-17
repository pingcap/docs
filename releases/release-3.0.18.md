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
