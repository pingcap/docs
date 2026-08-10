---
title: TiDB 3.0.13 Release Notes
summary: TiDB 3.0.13 was released on April 22, 2020. The bug fixes include resolving issues with the `INSERT ... ON DUPLICATE KEY UPDATE` statement and fixing the system getting stuck and becoming unavailable during `Region Merge` in TiKV.
aliases: ['/tidb/dev/release-3.0.13/','/tidb/v3.0/release-3.0.13','/docs/dev/releases/release-3.0.13/','/docs/dev/releases/3.0.13/','/tidb/v5.4/release-3.0.13','/tidb/v6.1/release-3.0.13','/tidb/v6.5/release-3.0.13','/tidb/v7.1/release-3.0.13','/tidb/v7.5/release-3.0.13','/tidb/v8.1/release-3.0.13']
---

# TiDB 3.0.13 Release Notes

Release date: April 22, 2020

TiDB version: 3.0.13

## Bug Fixes

+ TiDB

    - Fix the issue caused by unchecked `MemBuffer` that the `INSERT ... ON DUPLICATE KEY UPDATE` statement might be executed incorrectly within a transaction when users need to insert multiple rows of duplicate data [#16690](https://github.com/pingcap/tidb/pull/16690)

+ TiKV

    - Fix the issue that the system might get stuck and the service is unavailable if `Region Merge` is executed repeatedly [#7612](https://github.com/tikv/tikv/pull/7612)
