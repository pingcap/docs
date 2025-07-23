---
title: Wrong Index Solution
summary: 学习如何解决错误索引问题。
---

# Wrong Index Solution

如果你发现某些查询的执行速度未达到预期，优化器可能选择了错误的索引来执行该查询。

导致优化器选择意外索引的原因可能有多种：

- **Outdated statistics**：优化器依赖统计信息来估算查询成本。如果统计信息过时，优化器可能会做出次优的选择。
- **Statistics mismatch**：即使统计信息是最新的，它们可能也不能准确反映数据分布，从而导致错误的成本估算。
- **Incorrect cost calculation**：由于复杂的查询结构或数据分布，优化器可能会误算使用索引的成本。
- **Inappropriate engine selection**：在某些情况下，优化器可能会选择不适合该查询的存储引擎。
- **Function pushdown limitations**：某些函数或操作可能无法被下推到存储引擎，可能会影响查询性能。

## Statistics health

你可以先查看 [statistics 中的 [health state of tables](/statistics.md#health-state-of-tables)]，然后根据不同的健康状态解决此问题。

### Low health state

低健康状态意味着 TiDB 长时间未执行 `ANALYZE` 语句。你可以通过运行 `ANALYZE` 命令来更新统计信息。更新后，如果优化器仍然使用错误的索引，请参考下一节。

### Near 100% health state

接近 100% 健康状态表明 `ANALYZE` 语句刚刚完成或不久前完成。在这种情况下，错误索引问题可能与 TiDB 对行数的估算逻辑有关。

对于等价查询，原因可能是 [Count-Min Sketch](/statistics.md#count-min-sketch)。你可以检查 Count-Min Sketch 是否是原因，并采取相应的解决方案。

如果上述原因不适用你的问题，你可以通过使用 `USE_INDEX` 或 `use index` 优化器提示强制选择索引（详见 [USE_INDEX](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-)）。此外，你还可以通过非侵入式的方式，使用 [SQL Plan Management](/sql-plan-management.md) 改变查询行为。

### Other situations

除了上述情况外，错误索引问题还可能由数据更新引起，这会导致所有索引不再适用。在这种情况下，你需要分析条件和数据分布，判断是否可以通过新增索引来加快查询速度。如果可以，可以通过运行 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 命令添加新索引。

## Statistics mismatch

当数据分布高度偏斜时，统计信息可能无法准确反映实际数据。在这种情况下，可以尝试配置 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 语句的参数，可能有助于提高统计信息的准确性，更好地匹配索引。

例如，假设你有一个 `orders` 表，并在 `customer_id` 列上建立了索引，而超过 50% 的订单具有相同的 `customer_id`。在这种情况下，统计信息可能无法很好地反映数据分布，从而影响查询性能。

## Cost information

要查看详细的执行成本信息，可以执行 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 和 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句，并加上 `FORMAT=verbose` 选项。根据这些信息，你可以看到不同执行路径之间的成本差异。

## Engine selection

默认情况下，TiDB 会根据成本估算选择 TiKV 或 TiFlash 作为表的访问引擎。你可以通过应用引擎隔离，尝试不同的引擎以测试相同查询的性能。

更多信息请参见 [Engine isolation](/tiflash/use-tidb-to-read-tiflash.md#engine-isolation)。

## Function pushdown

为了提升查询性能，TiDB 可以将某些函数下推到 TiKV 或 TiFlash 存储引擎中执行。然而，部分函数不支持下推，这可能限制可用的执行计划，并潜在影响查询性能。

支持下推的表达式请参见 [TiKV supported pushdown calculations](/functions-and-operators/expressions-pushed-down.md) 和 [TiFlash supported pushdown calculations](/tiflash/tiflash-supported-pushdown-calculations.md)。

注意，你也可以禁用特定表达式的下推。更多信息请参见 [Blocklist of optimization rules and expression pushdown](/blocklist-control-plan.md)。

## See also

- [Statistics](/statistics.md)
- [Index selection](/choose-index.md)
- [Optimizer hints](/optimizer-hints.md)
- [SQL Plan Management](/sql-plan-management.md)