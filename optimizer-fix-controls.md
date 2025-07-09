---
title: Optimizer Fix Controls
summary: 了解 Optimizer Fix Controls 功能以及如何使用 `tidb_opt_fix_control` 更细粒度地控制 TiDB 优化器。
---

# Optimizer Fix Controls

随着产品的迭代发展，TiDB 优化器的行为也在不断变化，从而生成更合理的执行计划。然而，在某些特定场景下，新的行为可能会导致意想不到的结果。例如：

- 某些行为的效果依赖于特定场景。带来大部分场景改进的变更，可能会对其他场景造成回退。
- 有时候，行为细节的变化与其后果之间的关系非常复杂。某个行为的改进可能会导致整体回归。

因此，TiDB 提供了 Optimizer Fix Controls 功能，允许你通过设置一组修复项的值，对 TiDB 优化器的行为进行细粒度的控制。本文档介绍了 Optimizer Fix Controls 功能及其使用方法，并列出了 TiDB 当前支持的所有 Optimizer Fix Controls 修复项。

## `tidb_opt_fix_control` 介绍

从 v6.5.3 和 v7.1.0 版本开始，TiDB 提供了 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) 系统变量，用于更细粒度地控制优化器的行为。

每个修复项是用于调整 TiDB 优化器中特定行为的控制项，由一个数字表示，该数字对应包含行为变更技术细节的 GitHub Issue。例如，关于 fix `44262`，你可以在 [Issue 44262](https://github.com/pingcap/tidb/issues/44262) 中查看其控制内容。

[`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) 系统变量接受多个修复项作为一个值，用逗号（`,`）分隔。格式为 `"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`，其中 `<#issueN>` 是修复编号。例如：

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## Optimizer Fix Controls 参考列表

### [`33031`](https://github.com/pingcap/tidb/issues/33031) <span class="version-mark">New in v8.0.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 该变量控制是否允许分区表使用计划缓存。如果设置为 `ON`，则不会启用 [Prepared statement plan cache](/sql-prepared-plan-cache.md) 和 [Non-prepared statement plan cache](/sql-non-prepared-plan-cache.md) 来缓存 [partitioned tables](/partitioned-table.md)。

### [`44262`](https://github.com/pingcap/tidb/issues/44262) <span class="version-mark">New in v6.5.3 and v7.2.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 该变量控制在缺少 [GlobalStats](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode) 时，是否允许使用 [Dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) 访问分区表。

### [`44389`](https://github.com/pingcap/tidb/issues/44389) <span class="version-mark">New in v6.5.3 and v7.2.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 对于诸如 `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))` 这类过滤条件，该变量控制是否尝试为 `IndexRangeScan` 构建更全面的扫描范围。

### [`44823`](https://github.com/pingcap/tidb/issues/44823) <span class="version-mark">New in v7.3.0</span>

- 默认值：`200`
- 可能值：`[0, 2147483647]`
- 为节省内存，Plan Cache 不会缓存参数超过此变量指定数量的查询。`0` 表示无限制。

### [`44830`](https://github.com/pingcap/tidb/issues/44830) <span class="version-mark">New in v6.5.7 and v7.3.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 该变量控制是否允许 Plan Cache 缓存在物理优化过程中生成的 `PointGet` 操作的执行计划。

### [`44855`](https://github.com/pingcap/tidb/issues/44855) <span class="version-mark">New in v6.5.4 and v7.3.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 在某些场景下，当 `IndexJoin` 操作符的 `Probe` 端包含 `Selection` 操作符时，TiDB 会严重高估 `IndexScan` 的行数。这可能导致选择了次优的查询计划而非 `IndexJoin`。
- 为缓解此问题，TiDB 引入了改进措施，但由于存在查询计划回退的风险，默认情况下此改进是禁用的。
- 该变量控制是否启用上述改进。

### [`45132`](https://github.com/pingcap/tidb/issues/45132) <span class="version-mark">New in v7.4.0</span>

- 默认值：`1000`
- 可能值：`[0, 2147483647]`
- 该变量设置优化器启发式策略选择访问路径的阈值。如果某个访问路径（如 `Index_A`）的估算行数远小于其他访问路径（默认小于 1000 倍），优化器会跳过成本比较，直接选择 `Index_A`。
- `0` 表示禁用此启发式策略。

### [`45798`](https://github.com/pingcap/tidb/issues/45798) <span class="version-mark">New in v7.5.0</span>

- 默认值：`ON`
- 可能值：`ON`，`OFF`
- 该变量控制是否允许 Plan Cache 缓存访问 [generated columns](/generated-columns.md) 的执行计划。

### [`46177`](https://github.com/pingcap/tidb/issues/46177) <span class="version-mark">New in v6.5.6, v7.1.3 and v7.5.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 该变量控制在找到非强制执行计划后，优化器是否在查询优化过程中探索强制执行计划。

### [`52869`](https://github.com/pingcap/tidb/issues/52869) <span class="version-mark">New in v8.1.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 如 [Explain Statements Using Index Merge](/explain-index-merge.md#examples) 中的 **Note** 所述，如果优化器可以为某个查询计划选择单一索引扫描方式（非全表扫描），则不会自动使用索引合并。
- 你可以通过启用此修复项来取消此限制。取消限制后，优化器在更多查询中会自动选择索引合并，但可能导致优化器忽略最优的执行计划。因此，建议在实际使用场景中充分测试后再取消此限制，以确保不会引起性能回退。

### [`56318`](https://github.com/pingcap/tidb/issues/56318)

> **Note:**
>
> 这仅在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 中可用。

- 默认值：`ON`
- 可能值：`ON`，`OFF`
- 该变量控制是否避免对 `ORDER BY` 语句中使用的繁重表达式进行两次计算。
