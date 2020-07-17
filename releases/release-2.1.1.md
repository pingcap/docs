---
title: TiDB 2.1.1 Release Notes
aliases: ['/docs/dev/releases/release-2.1.1/','/docs/dev/releases/2.1.1/']
---

# TiDB 2.1.1 Release Notes

On December 12, 2018, TiDB 2.1.1 is released. Compared with TiDB 2.1.0, this release has great improvement in stability, SQL optimizer, statistics information, and execution engine.

## TiDB

+ SQL Optimizer/Executor
    - Fix the round error of the negative date [#8574](https://github.com/pingcap/tidb/pull/8574)
    - Fix the issue that the `uncompress` function does not check the data length [#8606](https://github.com/pingcap/tidb/pull/8606)
    - Reset bind arguments of the `prepare` statement after the `execute` command is executed [#8652](https://github.com/pingcap/tidb/pull/8652)
    - Support automatically collecting the statistics information of a partition table [#8649](https://github.com/pingcap/tidb/pull/8649)
    - Fix the wrongly configured integer type when pushing down the `abs` function [#8628](https://github.com/pingcap/tidb/pull/8628)
    - Fix the data race on the JSON column [#8660](https://github.com/pingcap/tidb/pull/8660)
+ Server
    - Fix the issue that the transaction obtained TSO is incorrect when PD breaks down [#8567](https://github.com/pingcap/tidb/pull/8567)
    - Fix the bootstrap failure caused by the statement that does not conform to ANSI standards [#8576](https://github.com/pingcap/tidb/pull/8576)
    - Fix the issue that incorrect parameters are used in transaction retries [#8638](https://github.com/pingcap/tidb/pull/8638)
+ DDL
    - Change the default character set and collation of tables into `utf8mb4` [#8590](https://github.com/pingcap/tidb/pull/8590)
    - Add the `ddl_reorg_batch_size` variable to control the speed of adding indexes [#8614](https://github.com/pingcap/tidb/pull/8614)
    - Make the character set and collation options content in DDL case-insensitive [#8611](https://github.com/pingcap/tidb/pull/8611)
    - Fix the issue of adding indexes for generated columns [#8655](https://github.com/pingcap/tidb/pull/8655)

## PD

- Fix the issue that some configuration items cannot be set to `0` in the configuration file [#1334](https://github.com/pingcap/pd/pull/1334)
- Check the undefined configuration when starting PD [#1362](https://github.com/pingcap/pd/pull/1362)
- Avoid transferring the leader to a newly created peer, to optimize the possible delay [#1339](https://github.com/pingcap/pd/pull/1339)
- Fix the issue that `RaftCluster` cannot stop caused by deadlock [#1370](https://github.com/pingcap/pd/pull/1370)

## TiKV

- Avoid transferring the leader to a newly created peer, to optimize the possible delay [#3878](https://github.com/tikv/tikv/pull/3878)

## Tools

+ Lightning
    - Optimize the `analyze` mechanism on imported tables to increase the import speed
    - Support storing the checkpoint information to a local file
+ TiDB Binlog
    - Fix the output bug of pb files that a table only with the primary key column cannot generate the pb event
