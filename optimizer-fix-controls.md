---
title: Optimizer Fix Controls
summary: Learn about the Optimizer Fix Controls feature and how to use `tidb_opt_fix_control` to control the TiDB optimizer in a more fine-grained way.
---

# Optimizer Fix Controls

The TiDB optimizer has lots of details in its behavior. As TiDB evolves, these details are changing. Usually, these changes are improvements of the optimizer. But sometimes, they might cause unexpected results, such as:

- For some implementation details, some behaviors are more suitable for certain scenarios. Changes that bring improvements for some scenarios might cause regressions for others.
- Sometimes, the relationship between changes in the behavior details and their consequences is very complicated. Even if it is an improvement in a certain behavior, it might cause execution plan regression as a whole.

## Introduction to `tidb_opt_fix_control`

Starting from v7.1.0, TiDB provides the [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710) system variable to control the behavior of the optimizer in a more fine-grained way.

A fix is denoted by a number that corresponds to a GitHub Issue. The GitHub issue contains the technical details. For example, Fix `44262` corresponds to [Issue 44262](https://github.com/pingcap/tidb/issues/44262).

This variable supports multiple fixes, separated by commas (`,`). The format is `"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`, where `<#issueN>` is the fix number. For example:

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## Optimizer Fix Controls reference

### [`44262`](https://github.com/pingcap/tidb/issues/44262) <span class="version-mark">New in v7.1.1</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- This variable controls whether to allow the use of [Dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) to access the partitioned table when the [GlobalStats](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode) are missing.

### [`44389`](https://github.com/pingcap/tidb/issues/44389) <span class="version-mark">New in v7.1.1</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- For filters such as `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))`, this variable controls whether to try to build more comprehensive scan ranges for `IndexRangeScan`.
