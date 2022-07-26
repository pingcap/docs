---
title: TiDB 1.0.6 Release Notes
aliases: ['/docs/dev/releases/release-1.0.6/','/docs/dev/releases/106/']
---

# TiDB 1.0.6 Release Notes

On January 08, 2018, TiDB 1.0.6 is released with the following updates:

## TiDB

- [Support the `Alter Table Auto_Increment` syntax](https://github.com/pingcap/tidb/pull/5511)
- [Fix the bug in Cost Based computation and the `Null Json` issue in statistics](https://github.com/pingcap/tidb/pull/5556)
- [Support the extension syntax to shard the implicit row ID to avoid write hot spot for a single table](https://github.com/pingcap/tidb/pull/5559)
- [Fix a potential DDL issue](https://github.com/pingcap/tidb/pull/5562)
- [Consider the timezone setting in the `curtime`, `sysdate` and `curdate` functions](https://github.com/pingcap/tidb/pull/5564)
- [Support the `SEPARATOR` syntax in the `GROUP_CONCAT` function](https://github.com/pingcap/tidb/pull/5569)
- [Fix the wrong return type issue of the `GROUP_CONCAT` function.](https://github.com/pingcap/tidb/pull/5582)

## PD

- [Fix store selection problem of hot-region scheduler](https://github.com/pingcap/pd/pull/898)

## TiKV

None.

To upgrade from 1.0.5 to 1.0.6, follow the rolling upgrade order of PD -> TiKV -> TiDB.
