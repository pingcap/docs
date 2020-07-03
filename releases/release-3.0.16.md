---
title: TiDB 3.0.16 Release Notes
category: Releases
---

# TiDB 3.0.16 Release Notes

Release date: July 03, 2020

TiDB version: 3.0.16

## Improvements

+ TiDB

    - Planner: support `is null` filter condition in hash partition pruning [#17308](https://github.com/pingcap/tidb/pull/17308)
    - Assign different `Backoffer` for each region to avoid the SQL command timeout issue when multiple region requests fail at the same time [#17583](https://github.com/pingcap/tidb/pull/17583)
    - Split partition region when adding a new partition [#17668](https://github.com/pingcap/tidb/pull/17668)
    - Discard feedbacks generated from `delete` / `update` statements [#17841](https://github.com/pingcap/tidb/pull/17841)
    - Correct the usage of json.Unmarshal in job.DecodeArgs to be compatible with future Go versions [#17887](https://github.com/pingcap/tidb/pull/17887)
    - Remove sensitive information in slow-log and statement [#18128](https://github.com/pingcap/tidb/pull/18128)
    - Datetime parsing now matches MySQL 5.7 behavior for delimiters [#17499](https://github.com/pingcap/tidb/pull/17499)
    - `%h` in date formats should now be in 1..12 range [#17496](https://github.com/pingcap/tidb/pull/17496)

+ TiKV

    - Do not send store heartbeat when snapshot received [#8145](https://github.com/tikv/tikv/pull/8145)
    - Improve PD client log [#8091](https://github.com/tikv/tikv/pull/8091)

## Bug Fixes

+ TiDB

    - Fix read/write inconsistent result when meet lock that point to a primary key has be insert/delete in own txn [#18248](https://github.com/pingcap/tidb/pull/18248)
    - Fix "Got too many pings" grpc error log in PD-server follower [#17944](https://github.com/pingcap/tidb/pull/17944)
    - Fix panic when the child of HashJoin returns TypeNull column [#17935](https://github.com/pingcap/tidb/pull/17935)
    - Fix error message when access denied [#17722](https://github.com/pingcap/tidb/pull/17722)
    - Fix JSON comparison for int and float [#17715](https://github.com/pingcap/tidb/pull/17715)
    - Failpoint: update failpoint which will cause data race before [#17710](https://github.com/pingcap/tidb/pull/17710)
    - Fix pre-split region timeout constraint not work when create table [#17617](https://github.com/pingcap/tidb/pull/17617)
    - Fix the panic caused by ambiguous error messages after the sending failure [#17378](https://github.com/pingcap/tidb/pull/17378)
    - Fix flashback table failed in some special cases [#17165](https://github.com/pingcap/tidb/pull/17165)
    - Util: fix the wrong result when where stmt only have string column [#16658](https://github.com/pingcap/tidb/pull/16658)
    - Fix error of query when `only_full_group_by` SQL mode is set [#16620](https://github.com/pingcap/tidb/pull/16620)
    - Fix wrong return length for case when function [#16562](https://github.com/pingcap/tidb/pull/16562)
    - Fix the `typeInfer` issue for the decimal property in the `count` aggregate function [#17702](https://github.com/pingcap/tidb/pull/17702)

+ TiKV

    - Fix potential wrong result read from ingested file [#8039](https://github.com/tikv/tikv/pull/8039)
    - Fix a case that a peer can not be removed when its store is isolated during multiple merge process [#8005](https://github.com/tikv/tikv/pull/8005)

+ PD

    - Fix the 404 problem when using region key in pd-ctl [#2577](https://github.com/pingcap/pd/pull/2577)
