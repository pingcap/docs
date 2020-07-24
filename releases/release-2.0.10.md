---
title: TiDB 2.0.10 Release Notes
aliases: ['/docs/dev/releases/release-2.0.10/','/docs/dev/releases/2.0.10/']
---

# TiDB 2.0.10 Release Notes

On December 18, 2018, TiDB 2.0.10 is released. The corresponding TiDB Ansible 2.0.10 is also released. Compared with TiDB 2.0.9, this release has great improvement in system compatibility and stability.

## TiDB

- Fix the possible issue caused by canceling a DDL job [#8513](https://github.com/pingcap/tidb/pull/8513)
- Fix the issue that the `ORDER BY` and `UNION` clauses cannot quote the column including a table name [#8514](https://github.com/pingcap/tidb/pull/8514)
- Fix the issue that the `UNCOMPRESS` function does not judge the incorrect input length [#8607](https://github.com/pingcap/tidb/pull/8607)
- Fix the issue encountered by `ANSI_QUOTES SQL_MODE` when upgrading TiDB [#8575](https://github.com/pingcap/tidb/pull/8575)
- Fix the issue that `select` returns the wrong result in some cases [#8570](https://github.com/pingcap/tidb/pull/8570)
- Fix the possible issue that TiDB cannot exit when it receives the exit signal [#8501](https://github.com/pingcap/tidb/pull/8501)
- Fix the issue that `IndexLookUpJoin` returns the wrong result in some cases [#8508](https://github.com/pingcap/tidb/pull/8508)
- Avoid pushing down the filter containing `GetVar` or `SetVar` [#8454](https://github.com/pingcap/tidb/pull/8454)
- Fix the issue that the result length of the `UNION` clauses is incorrect in some cases [#8491](https://github.com/pingcap/tidb/pull/8491)
- Fix the issue of `PREPARE FROM @var_name` [#8488](https://github.com/pingcap/tidb/pull/8488)
- Fix the panic issue when dumping statistics information in some cases [#8464](https://github.com/pingcap/tidb/pull/8464)
- Fix the statistics estimation issue of point queries in some cases [#8493](https://github.com/pingcap/tidb/pull/8493)
- Fix the panic issue when the returned default `enum` value is a string [#8476](https://github.com/pingcap/tidb/pull/8476)
- Fix the issue that too much memory is consumed in the scenario of wide tables [#8467](https://github.com/pingcap/tidb/pull/8467)
- Fix the issue encountered when Parser incorrectly formats the mod opcode [#8431](https://github.com/pingcap/tidb/pull/8431)
- Fix the panic issue caused by adding foreign key constraints in some cases [#8421](https://github.com/pingcap/tidb/pull/8421), [#8410](https://github.com/pingcap/tidb/pull/8410)
- Fix the issue that the `YEAR` column type incorrectly converts the zero value [#8396](https://github.com/pingcap/tidb/pull/8396)
- Fix the panic issue occurred when the argument of the `VALUES` function is not a column [#8404](https://github.com/pingcap/tidb/pull/8404)
- Disable Plan Cache for statements containing subqueries [#8395](https://github.com/pingcap/tidb/pull/8395)

## PD

- Fix the possible issue that RaftCluster cannot stop caused by deadlock [#1370](https://github.com/pingcap/pd/pull/1370)

## TiKV

- Avoid transferring the leader to a newly created peer, to optimize the possible delay [#3929](https://github.com/tikv/tikv/pull/3929)
- Fix redundant Region heartbeats [#3930](https://github.com/tikv/tikv/pull/3930)
