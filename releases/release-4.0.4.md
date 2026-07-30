---
title: TiDB 4.0.4 Release Notes
summary: TiDB 4.0.4 was released on July 31, 2020. Bug fixes include issues with querying `information_schema.columns`, errors with `PointGet` and `BatchPointGet` operators, wrong results with `BatchPointGet`, and incorrect query results with the `HashJoin` operator encountering `set` or `enum` type.
aliases: ['/tidb/dev/release-4.0.4/','/tidb/v4.0/release-4.0.4','/tidb/v5.4/release-4.0.4','/tidb/v6.1/release-4.0.4','/tidb/v6.5/release-4.0.4','/tidb/v7.1/release-4.0.4','/tidb/v7.5/release-4.0.4','/tidb/v8.1/release-4.0.4']
---

# TiDB 4.0.4 Release Notes

Release date: July 31, 2020

TiDB version: 4.0.4

## Bug Fixes

+ TiDB

    - Fix the issue of getting stuck when querying `information_schema.columns` [#18849](https://github.com/pingcap/tidb/pull/18849)
    - Fix the errors that occur when the `PointGet` and `BatchPointGet` operators encounter `in null` [#18848](https://github.com/pingcap/tidb/pull/18848)
    - Fix the wrong result of `BatchPointGet` [#18815](https://github.com/pingcap/tidb/pull/18815)
    - Fix the issue of incorrect query result that occurs when the `HashJoin` operator encounters the `set` or `enum` type [#18859](https://github.com/pingcap/tidb/pull/18859)
