---
title: TiDB 2.1.3 Release Notes
aliases: ['/docs/dev/releases/release-2.1.3/','/docs/dev/releases/2.1.3/']
---

# TiDB 2.1.3 Release Notes

On January 28, 2019, TiDB 2.1.3 is released. The corresponding TiDB Ansible 2.1.3 is also released. Compared with TiDB 2.1.2, this release has great improvement in system stability, SQL optimizer, statistics information, and execution engine.

## TiDB

+ SQL Optimizer/Executor
    - Fix the panic issue of Prepared Plan Cache in some cases [#8826](https://github.com/pingcap/tidb/pull/8826)
    - Fix the issue that Range computing is wrong when the index is a prefix index [#8851](https://github.com/pingcap/tidb/pull/8851)
    - Make `CAST(str AS TIME(N))` return null if the string is in the illegal `TIME` format when `SQL_MODE` is not strict [#8966](https://github.com/pingcap/tidb/pull/8966)
    - Fix the panic issue of Generated Column during the process of `UPDATE` in some cases [#8980](https://github.com/pingcap/tidb/pull/8980)
    - Fix the upper bound overflow issue of the statistics histogram in some cases [#8989](https://github.com/pingcap/tidb/pull/8989)
    - Support Range for `_tidb_rowid` construction queries, to avoid full table scan and reduce cluster stress [#9059](https://github.com/pingcap/tidb/pull/9059)
    - Return an error when the `CAST(AS TIME)` precision is too big [#9058](https://github.com/pingcap/tidb/pull/9058)
    - Allow using `Sort Merge Join` in the Cartesian product [#9037](https://github.com/pingcap/tidb/pull/9037)
    - Fix the issue that the statistics worker cannot resume after the panic in some cases [#9085](https://github.com/pingcap/tidb/pull/9085)
    - Fix the issue that `Sort Merge Join` returns the wrong result in some cases [#9046](https://github.com/pingcap/tidb/pull/9046)
    - Support returning the JSON type in the `CASE` clause [#8355](https://github.com/pingcap/tidb/pull/8355)
+ Server
    - Return a warning instead of an error when the non-TiDB hint exists in the comment [#8766](https://github.com/pingcap/tidb/pull/8766)
    - Verify the validity of the configured TIMEZONE value [#8879](https://github.com/pingcap/tidb/pull/8879)
    - Optimize the `QueryDurationHistogram` metrics item to display more statement types [#8875](https://github.com/pingcap/tidb/pull/8875)
    - Fix the lower bound overflow issue of bigint in some cases [#8544](https://github.com/pingcap/tidb/pull/8544)
    - Support the `ALLOW_INVALID_DATES` SQL mode [#9110](https://github.com/pingcap/tidb/pull/9110)
+ DDL
    - Fix a `RENAME TABLE` compatibility issue to keep the behavior consistent with that of MySQL [#8808](https://github.com/pingcap/tidb/pull/8808)
    - Support making concurrent changes of `ADD INDEX` take effect immediately [#8786](https://github.com/pingcap/tidb/pull/8786)
    - Fix the `UPDATE` panic issue during the process of `ADD COLUMN` in some cases [#8906](https://github.com/pingcap/tidb/pull/8906)
    - Fix the issue of concurrently creating Table Partition in some cases [#8902](https://github.com/pingcap/tidb/pull/8902)
    - Support converting the `utf8` character set to `utf8mb4` [#8951](https://github.com/pingcap/tidb/pull/8951) [#9152](https://github.com/pingcap/tidb/pull/9152)
    - Fix the issue of Shard Bits overflow [#8976](https://github.com/pingcap/tidb/pull/8976)
    - Support outputting the column character sets in `SHOW CREATE TABLE` [#9053](https://github.com/pingcap/tidb/pull/9053)
    - Fix the issue of the maximum length limit of the varchar type column in `utf8mb4` [#8818](https://github.com/pingcap/tidb/pull/8818)
    - Support `ALTER TABLE TRUNCATE TABLE PARTITION` [#9093](https://github.com/pingcap/tidb/pull/9093)
    - Resolve the charset when the charset is not provided [#9147](https://github.com/pingcap/tidb/pull/9147)

## PD

- Fix the Watch issue related to leader election [#1396](https://github.com/pingcap/pd/pull/1396)

## TiKV

- Support obtaining the monitoring information using the HTTP method [#3855](https://github.com/tikv/tikv/pull/3855)
- Fix the NULL issue of `data_format` [#4075](https://github.com/tikv/tikv/pull/4075)
- Add verifying the range for scan requests [#4124](https://github.com/tikv/tikv/pull/4124)

## Tools

+ TiDB Binlog
    - Fix the `no available pump` issue while TiDB is started or restarted [#157](https://github.com/pingcap/tidb-tools/pull/158)
    - Enable outputting the Pump client log [#165](https://github.com/pingcap/tidb-tools/pull/165)
    - Fix the data inconsistency issue caused by the unique key containing the NULL value when the table only has the unique key and does not have the primary key
