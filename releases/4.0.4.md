---
title: TiDB 4.0.4 Release Notes
---

# TiDB 4.0.4 Release Notes

Release date: July 31, 2020

TiDB version: 4.0.4

## Bug Fixes

+ TiDB

    - Fix the issue of getting stuck when querying `information_schema.columns` [#18849](https://github.com/pingcap/tidb/pull/18849)
    - Resolve errors caused by `in null` in point/batch get operators [#18848](https://github.com/pingcap/tidb/pull/18848)
    - Fix the wrong result of `BatchPointGet` [#18815](https://github.com/pingcap/tidb/pull/18815)
    - Fix an encoding bug that causes the wrong result of HashJoin with `set` and `enum` [#18859](https://github.com/pingcap/tidb/pull/18859)
