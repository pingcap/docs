---
title: TiDB 3.0.0-rc.3 Release Notes
aliases: ['/docs/dev/releases/release-3.0.0-rc.3/','/docs/dev/releases/3.0.0-rc.3/']
---

# TiDB 3.0.0-rc.3 Release Notes

Release date: June 21, 2019

TiDB version: 3.0.0-rc.3

TiDB Ansible version: 3.0.0-rc.3

## Overview

On June 21, 2019, TiDB 3.0.0-rc.3 is released. The corresponding TiDB Ansible version is 3.0.0-rc.3. Compared with TiDB 3.0.0-rc.2, this release has greatly improved the stability, usability, features, the SQL optimizer, statistics, and the execution engine.

## TiDB

+ SQL Optimizer
    - Remove the feature of collecting virtual generated column statistics [#10629](https://github.com/pingcap/tidb/pull/10629)
    - Fix the issue that the primary key constant overflows during point queries [#10699](https://github.com/pingcap/tidb/pull/10699)
    - Fix the issue that using uninitialized information in `fast analyze` causes panic [#10691](https://github.com/pingcap/tidb/pull/10691)
    - Fix the issue that executing the `create view` statement using `prepare` causes panic because of wrong column information [#10713](https://github.com/pingcap/tidb/pull/10713)
    - Fix the issue that the column information is not cloned when handling window functions [#10720](https://github.com/pingcap/tidb/pull/10720)
    - Fix the wrong estimation for the selectivity rate of the inner table selection in index join [#10854](https://github.com/pingcap/tidb/pull/10854)
    - Support automatic loading statistics when the `stats-lease` variable value is 0 [#10811](https://github.com/pingcap/tidb/pull/10811)

+ Execution Engine
    - Fix the issue that resources are not correctly released when calling the `Close` function in `StreamAggExec` [#10636](https://github.com/pingcap/tidb/pull/10636)
    - Fix the issue that the order of `table_option` and `partition_options` is incorrect in the result of executing the `show create table` statement for partitioned tables [#10689](https://github.com/pingcap/tidb/pull/10689)
    - Improve the performance of `admin show ddl jobs` by supporting scanning data in reverse order [#10687](https://github.com/pingcap/tidb/pull/10687)
    - Fix the issue that the result of the `show grants` statement in RBAC is incompatible with that of MySQL when this statement has the `current_user` field [#10684](https://github.com/pingcap/tidb/pull/10684)
    - Fix the issue that UUIDs might generate duplicate values on multiple nodes [#10712](https://github.com/pingcap/tidb/pull/10712)
    - Fix the issue that the `show view` privilege is not considered in `explain` [#10635](https://github.com/pingcap/tidb/pull/10635)
    - Add the `split table region` statement to manually split the table Region to alleviate the hotspot issue [#10765](https://github.com/pingcap/tidb/pull/10765)
    - Add the `split index region` statement to manually split the index Region to alleviate the hotspot issue [#10764](https://github.com/pingcap/tidb/pull/10764)
    - Fix the incorrect execution issue when you execute multiple statements such as `create user`, `grant`, or `revoke` consecutively [#10737](https://github.com/pingcap/tidb/pull/10737)
    - Add a blacklist to prohibit pushing down expressions to Coprocessor [#10791](https://github.com/pingcap/tidb/pull/10791)
    - Add the feature of printing the `expensive query` log when a query exceeds the memory configuration limit [#10849](https://github.com/pingcap/tidb/pull/10849)
    - Add the `bind-info-lease` configuration item to control the update time of the modified binding execution plan [#10727](https://github.com/pingcap/tidb/pull/10727)
    - Fix the OOM issue in high concurrent scenarios caused by the failure to quickly release Coprocessor resources, resulted from the `execdetails.ExecDetails` pointer [#10832](https://github.com/pingcap/tidb/pull/10832)
    - Fix the panic issue caused by the `kill` statement in some cases [#10876](https://github.com/pingcap/tidb/pull/10876)

+ Server
    - Fix the issue that goroutine might leak when repairing GC [#10683](https://github.com/pingcap/tidb/pull/10683)
    - Support displaying the `host` information in slow queries [#10693](https://github.com/pingcap/tidb/pull/10693)
    - Support reusing idle links that interact with TiKV [#10632](https://github.com/pingcap/tidb/pull/10632)
    - Fix the support for enabling the `skip-grant-table` option in RBAC [#10738](https://github.com/pingcap/tidb/pull/10738)
    - Fix the issue that `pessimistic-txn` configuration goes invalid [#10825](https://github.com/pingcap/tidb/pull/10825)
    - Fix the issue that the actively canceled ticlient requests are still retried [#10850](https://github.com/pingcap/tidb/pull/10850)
    - Improve performance in the case where pessimistic transactions conflict with optimistic transactions [#10881](https://github.com/pingcap/tidb/pull/10881)

+ DDL
    - Fix the issue that modifying charset using `alter table` causes the `blob` type change [#10698](https://github.com/pingcap/tidb/pull/10698)
    - Add a feature to use `SHARD_ROW_ID_BITS` to scatter row IDs when the column contains an `AUTO_INCREMENT` attribute to alleviate the hotspot issue [#10794](https://github.com/pingcap/tidb/pull/10794)
    - Prohibit adding stored generated columns by using the `alter table` statement [#10808](https://github.com/pingcap/tidb/pull/10808)
    - Optimize the invalid survival time of DDL metadata to shorten the period during which the DDL operation is slower after cluster upgrade [#10795](https://github.com/pingcap/tidb/pull/10795)

## PD

- Add the `enable-two-way-merge` configuration item to allow only one-way merging [#1583](https://github.com/pingcap/pd/pull/1583)
- Add scheduling operations for `AddLightLearner` and `AddLightPeer` to make Region Scatter scheduling unrestricted by the limit mechanism [#1563](https://github.com/pingcap/pd/pull/1563)
- Fix the issue of insufficient reliability because the data might only have one replica replication when the system is started [#1581](https://github.com/pingcap/pd/pull/1581)
- Optimize configuration check logic to avoid configuration item errors [#1585](https://github.com/pingcap/pd/pull/1585)
- Adjust the definition of the `store-balance-rate` configuration to the upper limit of the number of balance operators generated per minute [#1591](https://github.com/pingcap/pd/pull/1591)
- Fix the issue that the store might have been unable to generate scheduled operations [#1590](https://github.com/pingcap/pd/pull/1590)

## TiKV

+ Engine
    - Fix the issue that incomplete snapshots are generated in the system caused by the iterator not checking the status [#4936](https://github.com/tikv/tikv/pull/4936)
    - Fix the data loss issue caused by a delay of flushing data to the disk when receiving snapshots after a power failure in abnormal conditions [#4850](https://github.com/tikv/tikv/pull/4850)

+ Server
    - Add a feature to check the validity of the `block-size` configuration [#4928](https://github.com/tikv/tikv/pull/4928)
    - Add `READ_INDEX`-related monitoring metrics [#4830](https://github.com/tikv/tikv/pull/4830)
    - Add GC worker-related monitoring metrics [#4922](https://github.com/tikv/tikv/pull/4922)

+ Raftstore
    - Fix the issue that the cache of the local reader is not cleared correctly [#4778](https://github.com/tikv/tikv/pull/4778)
    - Fix the issue that the request delay might be increased when transferring the leader and changing `conf` [#4734](https://github.com/tikv/tikv/pull/4734)
    - Fix the issue that a stale command is wrongly reported [#4682](https://github.com/tikv/tikv/pull/4682)
    - Fix the issue that the command might be pending for a long time [#4810](https://github.com/tikv/tikv/pull/4810)
    - Fix the issue that files are damaged after a power failure, which is caused by a delay of synchronizing the snapshot file to the disk [#4807](https://github.com/tikv/tikv/pull/4807), [#4850](https://github.com/tikv/tikv/pull/4850)

+ Coprocessor
    - Support Top-N in vector calculation [#4827](https://github.com/tikv/tikv/pull/4827)
    - Support `Stream` aggregation in vector calculation [#4786](https://github.com/tikv/tikv/pull/4786)
    - Support the `AVG` aggregate function in vector calculation [#4777](https://github.com/tikv/tikv/pull/4777)
    - Support the `First` aggregate function in vector calculation [#4771](https://github.com/tikv/tikv/pull/4771)
    - Support the `SUM` aggregate function in vector calculation [#4797](https://github.com/tikv/tikv/pull/4797)
    - Support the `MAX`/`MIN` aggregate function in vector calculation [#4837](https://github.com/tikv/tikv/pull/4837)
    - Support the `Like` expression in vector calculation [#4747](https://github.com/tikv/tikv/pull/4747)
    - Support the `MultiplyDecimal` expression in vector calculation [#4849](https://github.com/tikv/tikv/pull/4849 )
    - Support the `BitAnd`/`BitOr`/`BitXor` expression in vector calculation [#4724](https://github.com/tikv/tikv/pull/4724)
    - Support the `UnaryNot` expression in vector calculation [#4808](https://github.com/tikv/tikv/pull/4808)

+ Transaction
    - Fix the issue that an error occurs caused by non-pessimistic locking conflicts in pessimistic transactions [#4801](https://github.com/tikv/tikv/pull/4801), [#4883](https://github.com/tikv/tikv/pull/4883)
    - Reduce unnecessary calculation for optimistic transactions after enabling pessimistic transactions to improve the performance [#4813](https://github.com/tikv/tikv/pull/4813)
    - Add a feature of single statement rollback to ensure that the whole transaction does not need a rollback operation in a deadlock situation [#4848](https://github.com/tikv/tikv/pull/4848)
    - Add pessimistic transaction-related monitoring items [#4852](https://github.com/tikv/tikv/pull/4852)
    - Support using the `ResolveLockLite` command to resolve lightweight locks to improve the performance when severe conflicts exist [#4882](https://github.com/tikv/tikv/pull/4882)

+ tikv-ctl
    - Add the `bad-regions` command to support checking more abnormal conditions [#4862](https://github.com/tikv/tikv/pull/4862)
    - Add a feature of forcely executing the `tombstone` command [#4862](https://github.com/tikv/tikv/pull/4862)

+ Misc
    - Add the `dist_release` compiling command [#4841](https://github.com/tikv/tikv/pull/4841)

## Tools

+ TiDB Binlog
    - Fix the wrong offset issue caused by Pump not checking the returned value when it fails to write data [#640](https://github.com/pingcap/tidb-binlog/pull/640)
    - Add the `advertise-addr` configuration in Drainer to support the bridge mode in the container environment [#634](https://github.com/pingcap/tidb-binlog/pull/634)
    - Add the `GetMvccByEncodeKey` function in Pump to speed up querying the transaction status [#632](https://github.com/pingcap/tidb-binlog/pull/632)

## TiDB Ansible

- Add a monitoring item to predict the maximum QPS value of the cluster ("hide" by default) [#f5cfa4d](https://github.com/pingcap/tidb-ansible/commit/f5cfa4d903bbcd77e01eddc8d31eabb6e6157f73)
