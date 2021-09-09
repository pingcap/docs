---
title: TiDB 5.2.1 Release Notes
---

# TiDB 5.2.1 Release Notes

Release date: September 9, 2021

TiDB version: 5.2.1

## Bug Fixes

+ TiDB

    - Fix the error report of a wrong execution plan caused by the shallow copy of schema columns when pushing down the aggregation operators in partition tables [#27797](https://github.com/pingcap/tidb/issues/27797) [#26554](https://github.com/pingcap/tidb/issues/26554)

+ TiKV

    - Fix the issue of unavailable TiKV caused by Raftstore deadlock when migrating Regions. You can deal with this issue by closing the scheduling or restarting the unavailable TiKV [#10909](https://github.com/tikv/tikv/issues/10909)
