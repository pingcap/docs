---
title: TiDB 1.0.5 Release Notes
aliases: ['/docs/dev/releases/release-1.0.5/','/docs/dev/releases/105/']
---

# TiDB 1.0.5 Release Notes

On December 26, 2017, TiDB 1.0.5 is released with the following updates:

## TiDB

- [Add the max value for the current Auto_Increment ID in the `Show Create Table` statement.](https://github.com/pingcap/tidb/pull/5489)
- [Fix a potential goroutine leak.](https://github.com/pingcap/tidb/pull/5486)
- [Support outputting slow queries into a separate file.](https://github.com/pingcap/tidb/pull/5484)
- [Load the `TimeZone` variable from TiKV when creating a new session.](https://github.com/pingcap/tidb/pull/5479)
- [Support the schema state check so that the `Show Create Table`and `Analyze` statements process the public table/index only.](https://github.com/pingcap/tidb/pull/5474)
- [The `set transaction read only` should affect the `tx_read_only` variable.](https://github.com/pingcap/tidb/pull/5491)
- [Clean up incremental statistic data when rolling back.](https://github.com/pingcap/tidb/pull/5391)
- [Fix the issue of missing index length in the `Show Create Table` statement.](https://github.com/pingcap/tidb/pull/5421)

## PD

- Fix the issue that the leaders stop balancing under some circumstances.
    - [869](https://github.com/pingcap/pd/pull/869)
    - [874](https://github.com/pingcap/pd/pull/874)
- [Fix potential panic during bootstrapping.](https://github.com/pingcap/pd/pull/889)

## TiKV

- Fix the issue that it is slow to get the CPU ID using the [`get_cpuid`](https://github.com/pingcap/tikv/pull/2611) function.
- Support the [`dynamic-level-bytes`](https://github.com/pingcap/tikv/pull/2605) parameter to improve the space collection situation.

To upgrade from 1.0.4 to 1.0.5, follow the rolling upgrade order of PD -> TiKV -> TiDB.
