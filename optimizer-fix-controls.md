---
title: Optimizer Fix Controls
summary: Learn about the Optimizer Fix Controls feature and how to use `tidb_opt_fix_control` to control the TiDB optimizer in a more fine-grained way.
---

# Optimizer Fix Controls

As the product evolves iteratively, the behavior of the TiDB optimizer changes, which in turn generates more reasonable execution plans. However, in some particular scenarios, the new behavior might lead to unexpected results. For example:

- The effect of some behaviors relies on a specific scenario. Changes that bring improvements to most scenarios might cause regressions to others.
- Sometimes, the relationship between changes in the behavior details and their consequences is very complicated. An improvement in a certain behavior might cause overall regression.

Therefore, TiDB provides the Optimizer Fix Controls feature that allows you to make fine-grained control of TiDB optimizer behaviors by setting values for a group of fixes. This document describes the Optimizer Fix Controls feature and how to use them, and lists all the fixes that TiDB currently supports for Optimizer Fix Controls.

## Introduction to `tidb_opt_fix_control`

Starting from v6.5.3 and v7.1.0, TiDB provides the [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) system variable to control the behavior of the optimizer in a more fine-grained way.

Each fix is a control item used to adjust the behavior in the TiDB optimizer for one particular purpose. It is denoted by a number that corresponds to a GitHub Issue that contains the technical details of the behavior change. For example, for fix `44262`, you can review what it controls in [Issue 44262](https://github.com/pingcap/tidb/issues/44262).

The [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) system variable accepts multiple fixes as one value, separated by commas (`,`). The format is `"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`, where `<#issueN>` is the fix number. For example:

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## Optimizer Fix Controls reference

### [`33031`](https://github.com/pingcap/tidb/issues/33031) <span class="version-mark">New in v8.0.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- This variable controls whether to allow plan cache for partitioned tables. If it is set to `ON`, neither [Prepared statement plan cache](/sql-prepared-plan-cache.md) nor [Non-prepared statement plan cache](/sql-non-prepared-plan-cache.md) will be enabled for [partitioned tables](/partitioned-table.md).

### [`44262`](https://github.com/pingcap/tidb/issues/44262) <span class="version-mark">New in v6.5.3 and v7.2.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- This variable controls whether to allow the use of [Dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) to access a partitioned table when the [global statistics](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode) of that table are missing.

### [`44389`](https://github.com/pingcap/tidb/issues/44389) <span class="version-mark">New in v6.5.3 and v7.2.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- For filters such as `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))`, this variable controls whether to try to build more comprehensive scan ranges for `IndexRangeScan`.

### [`44823`](https://github.com/pingcap/tidb/issues/44823) <span class="version-mark">New in v7.3.0</span>

- Default value: `200`
- Possible values: `[0, 2147483647]`
- To save memory, Plan Cache does not cache queries with parameters exceeding the specified number of this variable. `0` means no limit.

### [`44830`](https://github.com/pingcap/tidb/issues/44830) <span class="version-mark">New in v6.5.7 and v7.3.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- This variable controls whether Plan Cache is allowed to cache execution plans with the `PointGet` operator generated during physical optimization.

### [`44855`](https://github.com/pingcap/tidb/issues/44855) <span class="version-mark">New in v6.5.4 and v7.3.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- In some scenarios, when the `Probe` side of an `IndexJoin` operator contains a `Selection` operator, TiDB severely overestimates the row count of `IndexScan`. This might cause suboptimal query plans to be selected instead of `IndexJoin`.
- To mitigate this issue, TiDB has introduced an improvement. However, due to potential query plan fallback risks, this improvement is disabled by default.
- This variable controls whether to enable the preceding improvement.

### [`45132`](https://github.com/pingcap/tidb/issues/45132) <span class="version-mark">New in v7.4.0</span>

- Default value: `1000`
- Possible values: `[0, 2147483647]`
- This variable sets the threshold for the optimizer's heuristic strategy to select access paths. If the estimated rows for an access path (such as `Index_A`) is much smaller than that of other access paths (default `1000` times), the optimizer skips the cost comparison and directly selects `Index_A`.
- `0` means to disable this heuristic strategy.

### [`45798`](https://github.com/pingcap/tidb/issues/45798) <span class="version-mark">New in v7.5.0</span>

- Default value: `ON`
- Possible values: `ON`, `OFF`
- This variable controls whether Plan Cache is allowed to cache execution plans that access [generated columns](/generated-columns.md).

### [`46177`](https://github.com/pingcap/tidb/issues/46177) <span class="version-mark">New in v6.5.6, v7.1.3 and v7.5.0</span>

- Default value: `ON`. Before v8.5.0, the default value is `OFF`.
- Possible values: `ON`, `OFF`
- This variable controls whether the optimizer explores enforced plans during query optimization after finding an unenforced plan.

### [`47400`](https://github.com/pingcap/tidb/issues/47400) <span class="version-mark">New in v8.4.0</span>

- Default value: `ON`
- Possible values: `ON`, `OFF`
- Due to challenges in accurately estimating the number of qualified rows for each plan step in a query plan, the optimizer might estimate a smaller value for `estRows`. This variable controls whether to limit the minimum value of `estRows`.
- `ON`: limits the minimum value of `estRows` to 1, which is the new behavior introduced in v8.4.0 and is consistent with other databases, such as Oracle and Db2.
- `OFF`: disables the minimum row estimate limit, which maintains the behavior consistent with versions before v8.4.0. In this case, `estRows` might be zero.

### [`52592`](https://github.com/pingcap/tidb/issues/52592) <span class="version-mark">New in v8.4.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- This variable controls whether to disable the `Point Get` and `Batch Point Get` operators for query execution. The default value `OFF` means that `Point Get` and `Batch Point Get` can be used for query execution. If set to `ON`, the optimizer disables `Point Get` and `Batch Point Get`, forcing the selection of Coprocessor for query execution.
- `Point Get` and `Batch Point Get` do not support column projection (that is, they cannot return only a subset of the columns), so in some scenarios, their execution efficiency might be lower than that of the Coprocessor, and setting this variable to `ON` can improve query performance. The following are recommended scenarios for setting this variable to `ON`:

    - Wide tables with many columns, where only a few columns are queried.
    - Tables with large JSON values, where the JSON column is not queried, or only a small portion of the JSON column is queried.

### [`52869`](https://github.com/pingcap/tidb/issues/52869) <span class="version-mark">New in v8.1.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- As stated in the **Note** of [Explain Statements Using Index Merge](/explain-index-merge.md#examples), if the optimizer can choose the single index scan method (other than full table scan) for a query plan, the optimizer will not automatically use index merge.
- You can remove this limitation by enabling this fix control. Removing this limitation enables the optimizer to choose index merge automatically in more queries, but might cause the optimizer to ignore the optimal execution plans. Therefore, it is recommended to conduct sufficient tests on actual use cases before removing this limitation to make sure that it will not cause performance regressions.

### [`54337`](https://github.com/pingcap/tidb/issues/54337) <span class="version-mark">New in v8.3.0</span>

- Default value: `OFF`
- Possible values: `ON`, `OFF`
- Currently, the TiDB optimizer has limitations in deriving index ranges for complex conjunctive conditions where each conjunct comprises a list of ranges. This can be addressed by applying general range intersection.
- You can remove this limitation by enabling this fix control, allowing the optimizer to handle complex range intersections. However, for conditions with a large number of conjuncts (more than 10), there is a slight risk of increased optimization time.
