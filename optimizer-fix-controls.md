---
title: Optimizer Fix Controls
summary: Learn about the Optimizer Fix Controls feature and how to use `tidb_opt_fix_control` to control the TiDB optimizer in a more fine-grained way.
---

# Optimizer Fix Controls

As the product evolves iteratively, the behavior of the TiDB optimizer changes, which in turn generates more reasonable execution plans. However, in some specific scenarios, the new behavior may lead to unintended results. For example:

- The effect of some behaviors relies on a specific scenario. Changes that bring improvements for some scenarios might cause regressions for others.
- Sometimes, the relationship between changes in the behavior details and their consequences is very complicated. An improvement in a certain behavior might cause execution plan regression as a whole.

Therefore, TiDB provides the Optimizer Fix Controls feature that allows you to control the details of TiDB optimizer behaviors by setting a series of fixes. This document describes the Optimizer Fix Controls feature and how to use them, and lists all the fixes that TiDB currently supports.

## Introduction to `tidb_opt_fix_control`

Starting from v7.1.0, TiDB provides the [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710) system variable to control the behavior of the optimizer in a more fine-grained way.

A fix is a control item used to adjust the behavior in the TiDB optimizer at one point. It is denoted by a number that corresponds to a GitHub Issue. The GitHub issue contains the technical details. For example, Fix `44262` corresponds to [Issue 44262](https://github.com/pingcap/tidb/issues/44262).

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
