---
title: Optimizer Fix Controls
summary: 了解 Optimizer Fix Controls 功能以及如何使用 `tidb_opt_fix_control` 更细粒度地控制 TiDB 优化器。
---

# Optimizer Fix Controls

随着产品的迭代发展，TiDB 优化器的行为也在不断变化，从而生成更合理的执行计划。然而，在某些特定场景下，新的行为可能会导致意想不到的结果。例如：

- 某些行为的效果依赖于特定场景。带来大部分场景改进的变更，可能会对其他场景造成回归。
- 有时，行为细节的变化与其后果之间的关系非常复杂。某个行为的改进可能会导致整体回归。

因此，TiDB 提供了 Optimizer Fix Controls 功能，允许你通过设置一组修复项的值，对 TiDB 优化器的行为进行细粒度的控制。本文档介绍了 Optimizer Fix Controls 功能及其使用方法，并列出了 TiDB 当前支持的所有 Optimizer Fix Controls 修复项。

## `tidb_opt_fix_control` 介绍

从 v6.5.3 和 v7.1.0 版本开始，TiDB 提供了 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) 系统变量，用于更细粒度地控制优化器的行为。

每个修复项是用于调整 TiDB 优化器中特定行为的控制项，由一个数字表示，该数字对应包含行为变更技术细节的 GitHub Issue。例如，关于修复 `44262`，你可以在 [Issue 44262](https://github.com/pingcap/tidb/issues/44262) 中查看其控制内容。

[`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) 系统变量接受多个修复项作为一个值，用逗号（`,`）分隔。格式为 `"<#issue1>:<value1>,<#issue2>:<value2>,...,<#issueN>:<valueN>"`，其中 `<#issueN>` 是修复编号。例如：

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,44389:ON';
```

## Optimizer Fix Controls 参考列表

### [`33031`](https://github.com/pingcap/tidb/issues/33031) <span class="version-mark">New in v8.0.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 该变量控制是否允许分区表使用计划缓存。如果设置为 `ON`，则不会启用 [Prepared statement plan cache](/sql-prepared-plan-cache.md) 和 [Non-prepared statement plan cache](/sql-non-prepared-plan-cache.md) 来缓存 [partitioned tables](/partitioned-table.md)。

### [`44262`](https://github.com/pingcap/tidb/issues/44262) <span class="version-mark">New in v6.5.3 和 v7.2.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 该变量控制在缺少 [global statistics](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode) 时，是否允许使用 [Dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) 来访问分区表。

### [`44389`](https://github.com/pingcap/tidb/issues/44389) <span class="version-mark">New in v6.5.3 和 v7.2.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 对于诸如 `c = 10 and (a = 'xx' or (a = 'kk' and b = 1))` 之类的过滤条件，该变量控制是否尝试为 `IndexRangeScan` 构建更全面的扫描范围。

### [`44823`](https://github.com/pingcap/tidb/issues/44823) <span class="version-mark">New in v7.3.0</span>

- 默认值：`200`
- 可能值：`[0, 2147483647]`
- 为节省内存，计划缓存（Plan Cache）不会缓存参数数量超过此变量指定值的查询。`0` 表示无限制。

### [`44830`](https://github.com/pingcap/tidb/issues/44830) <span class="version-mark">New in v6.5.7 和 v7.3.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 该变量控制是否允许计划缓存缓存在物理优化过程中生成的 `PointGet` 操作的执行计划。

### [`44855`](https://github.com/pingcap/tidb/issues/44855) <span class="version-mark">New in v6.5.4 和 v7.3.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 在某些场景下，当 `IndexJoin` 操作符的 `Probe` 端包含 `Selection` 操作符时，TiDB 会严重高估 `IndexScan` 的行数。这可能导致选择了次优的查询计划而非 `IndexJoin`。
- 为缓解此问题，TiDB 引入了改进措施，但由于存在查询计划回退的风险，默认情况下禁用。
- 该变量控制是否启用上述改进。

### [`45132`](https://github.com/pingcap/tidb/issues/45132) <span class="version-mark">New in v7.4.0</span>

- 默认值：`1000`
- 可能值：`[0, 2147483647]`
- 该变量设置优化器启发式策略选择访问路径的阈值。如果某个访问路径（如 `Index_A`）的估算行数远小于其他访问路径（默认 `1000` 倍），优化器会跳过成本比较，直接选择 `Index_A`。
- `0` 表示禁用此启发式策略。

### [`45798`](https://github.com/pingcap/tidb/issues/45798) <span class="version-mark">New in v7.5.0</span>

- 默认值：`ON`
- 可能值：`ON`，`OFF`
- 该变量控制是否允许计划缓存缓存 [generated columns](/generated-columns.md) 的执行计划。

### [`46177`](https://github.com/pingcap/tidb/issues/46177) <span class="version-mark">New in v6.5.6、v7.1.3 和 v7.5.0</span>

- 默认值：`ON`。在 v8.5.0 之前，默认值为 `OFF`。
- 可能值：`ON`，`OFF`
- 该变量控制在查询优化过程中，是否在找到非强制执行计划后探索强制执行计划。

### [`47400`](https://github.com/pingcap/tidb/issues/47400) <span class="version-mark">New in v8.4.0</span>

- 默认值：`ON`
- 可能值：`ON`，`OFF`
- 由于在查询计划中准确估算每个步骤的符合条件行数存在挑战，优化器可能会对 `estRows` 估算得更小。该变量控制是否限制 `estRows` 的最小值。
- `ON`：将 `estRows` 的最小值限制为 1，这是在 v8.4.0 引入的新行为，与 Oracle 和 Db2 等其他数据库保持一致。
- `OFF`：不限制 `estRows` 的最小值，保持 v8.4.0 之前的行为，此时 `estRows` 可能为零。

### [`52592`](https://github.com/pingcap/tidb/issues/52592) <span class="version-mark">New in v8.4.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 该变量控制是否禁用查询执行中的 `Point Get` 和 `Batch Point Get` 操作符。默认值 `OFF` 表示可以使用 `Point Get` 和 `Batch Point Get` 进行查询执行。若设置为 `ON`，优化器会禁用这两种操作符，强制选择使用协处理器（Coprocessor）进行查询。
- `Point Get` 和 `Batch Point Get` 不支持列投影（即不能只返回部分列），因此在某些场景下，它们的执行效率可能低于协处理器，设置此变量为 `ON` 可以提升查询性能。推荐在以下场景下启用：

    - 列较多但只查询少量列的宽表。
    - JSON 值较大的表，且未查询 JSON 列或只查询部分 JSON 列。

### [`52869`](https://github.com/pingcap/tidb/issues/52869) <span class="version-mark">New in v8.1.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 如 [Explain Statements Using Index Merge](/explain-index-merge.md#examples) 中的 **Note** 所述，如果优化器可以为某个查询计划选择单索引扫描（非全表扫描）方式，则不会自动使用索引合并。
- 你可以通过启用此修复项，移除此限制。移除后，优化器在更多查询中会自动选择索引合并，但可能导致优化器忽略最优执行计划。因此，建议在实际用例中充分测试后再移除此限制，以确保不会引起性能回退。

### [`54337`](https://github.com/pingcap/tidb/issues/54337) <span class="version-mark">New in v8.3.0</span>

- 默认值：`OFF`
- 可能值：`ON`，`OFF`
- 目前，TiDB 优化器在为复杂的合取条件（每个合取子句由范围列表组成）推导索引范围时存在限制。这可以通过应用通用范围交集来解决。
- 你可以通过启用此修复项，移除此限制，使优化器能够处理复杂的范围交集。但对于包含大量合取子句（超过 10 个）的条件，存在优化时间略有增加的风险。
