---
title: Wrong Index Solution
summary: Learn how to solve the wrong index issue.
---

# Wrong Index Solution

If you find that the execution speed of some query does not reach the expectation, the optimizer might choose the wrong index to run the query.

There are multiple reasons why the optimizer might choose an unexpected index:

- **Outdated statistics**: the optimizer relies on statistics to estimate query costs. If the statistics are outdated, the optimizer might make suboptimal choices.
- **Statistics mismatch**: even if statistics are current, they might not accurately reflect the data distribution, leading to incorrect cost estimations.
- **Incorrect cost calculation**: the optimizer might miscalculate the cost of using an index due to complex query structures or data distribution.
- **Inappropriate engine selection**: in some cases, the optimizer might select a storage engine that is not optimal for the query.
- **Function pushdown limitations**: certain functions or operations might not be pushed down to storage engines, potentially affecting query performance.

## Statistics health

You can first view the [health state of tables](/statistics.md#health-state-of-tables) in the statistics, and then solve this issue according to the different health states.

### Low health state

The low health state means TiDB has not performed the`ANALYZE` statement for a long time. You can update the statistics by running the `ANALYZE` command. After the update, if the optimizer still uses the wrong index, refer to the next section.

### Near 100% health state

The near 100% health state suggests that the `ANALYZE` statement is just completed or was completed a short time ago. In this case, the wrong index issue might be related to TiDB's estimation logic for the number of rows.

For equivalence queries, the cause might be [Count-Min Sketch](/statistics.md#count-min-sketch). You can check whether Count-Min Sketch is the cause and take corresponding solutions.

If the cause above does not apply to your problem, you can force-select indexes by using the `USE_INDEX` or `use index` optimizer hint (see [USE_INDEX](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-) for details). Also, you can change the query behavior by using [SQL Plan Management](/sql-plan-management.md) in a non-intrusive way.

### Other situations

Apart from the aforementioned situations, the wrong index issue might also be caused by data updates which renders all the indexes no longer applicable. In such cases, you need to perform analysis on the conditions and data distribution to see whether new indexes can speed up the query. If so, you can add new indexes by running the [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) command.

## Statistics mismatch

When data distribution is highly skewed, the statistics might not accurately reflect the actual data. In such cases, try configuring the options of the [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) statement. It might help improve the accuracy of statistics and better match the index.

For example, suppose you have an `orders` table with an index on the `customer_id` column, and more than 50% of the orders share the same `customer_id`. In this case, the statistics might not represent the data distribution well, affecting query performance.

## Cost information

To view detailed information on execution costs, you can execute the [`EXPLAIN`](/sql-statements/sql-statement-explain.md) and [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) statements with the `FORMAT=verbose` option. According to the information, you can see cost differences between different execution paths.

## Engine selection

By default, TiDB chooses TiKV or TiFlash for table access based on cost estimation. You can experiment with different engines for the same query by applying engine isolation.

For more information, see [Engine isolation](/tiflash/use-tidb-to-read-tiflash.md#engine-isolation).

## Function pushdown

To enhance query performance, TiDB can push down certain functions to the TiKV or TiFlash storage engine for execution. However, some functions do not support pushdown, which might limit available execution plans and potentially affect query performance.

For expressions that support pushdown, see [TiKV supported pushdown calculations](/functions-and-operators/expressions-pushed-down.md) and [TiFlash supported pushdown calculations](/tiflash/tiflash-supported-pushdown-calculations.md). 

Note that you can also disable the pushdown of specific expressions. For more information, see [Blocklist of optimization rules and expression pushdown](/blocklist-control-plan.md).

## See also

- [Statistics](/statistics.md)
- [Index selection](/choose-index.md)
- [Optimizer hints](/optimizer-hints.md)
- [SQL Plan Management](/sql-plan-management.md)