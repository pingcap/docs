---
title: Optimizer Fix Controls
summary: Learn about the Optimizer Fix Controls and how to use tidb_opt_fix_control to control TiDB optimizer in a more fine-grained way
aliases: ['/docs/dev/optimizer-fix-controls/']
---

# Optimizer Fix Controls

The TiDB optimizer has lots of details in its behavior. As TiDB evolves, these details are changing. Usually, these changes are improvements of the optimizer. But sometimes, they would possibly cause unexpected results like execution plan regression:

- For some implementation details, different behaviors are more suitable to different scenarios.
- Sometimes, the relationship between changes in the behavior details and their consequences is very complicated. Even if it's an improvement in a certain behavior, it might cause execution plan regression as a whole.

So we provided the [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710) system variable to control the behavior of the optimizer in a more fine-grained way.

A Fix is usually denoted by a number, which usually corresponds to a GitHub Issue, in which there will be descriptions for the technical details. For example, Fix `44262` corresponds to [Issue 44262](https://github.com/pingcap/tidb/issues/44262).

This variable supports multiple Fixes, separated by commas (`,`). The format is `"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`, where `<#issueN>` is the Fix number. For example:

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## Optimizer Fix Controls Reference

### [`44262`](https://github.com/pingcap/tidb/issues/44262) <span class="version-mark">New in v7.1.1</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- This variable controls whether to allow the use of [Dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) to access the partitioned table when the [GlobalStats](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode) are missing.

### [`44389`](https://github.com/pingcap/tidb/issues/44389) <span class="version-mark">New in v7.1.1</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- For filters like `c = 10 and (a = 'xx' or (a = 'kk' and b = 1)`, whether to try to build more complete scan ranges for `IndexRangeScan`.
