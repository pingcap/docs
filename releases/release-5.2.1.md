---
title: TiDB 5.2.1 Release Notes
summary: TiDB 5.2.1 was released on September 9, 2021. Bug fixes include resolving an error in TiDB caused by a wrong execution plan and fixing the issue of unavailable TiKV caused by Raftstore deadlock when migrating Regions.
aliases: ['/tidb/dev/release-5.2.1/','/tidb/v5.2/release-5.2.1','/tidb/v5.4/release-5.2.1','/tidb/v6.1/release-5.2.1','/tidb/v6.5/release-5.2.1','/tidb/v7.1/release-5.2.1','/tidb/v7.5/release-5.2.1','/tidb/v8.1/release-5.2.1']
---

# TiDB 5.2.1 Release Notes

Release date: September 9, 2021

TiDB version: 5.2.1

## Bug fixes

+ TiDB

    - Fix an error that occurs during execution caused by the wrong execution plan. The wrong execution plan is caused by the shallow copy of schema columns when pushing down the aggregation operators on partitioned tables. [#27797](https://github.com/pingcap/tidb/issues/27797) [#26554](https://github.com/pingcap/tidb/issues/26554)

+ TiKV

    - Fix the issue of unavailable TiKV caused by Raftstore deadlock when migrating Regions. The workaround is to disable the scheduling and restart the unavailable TiKV. [#10909](https://github.com/tikv/tikv/issues/10909)
