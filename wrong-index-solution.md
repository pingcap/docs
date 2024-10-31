---
title: Wrong Index Solution
summary: Learn how to solve the wrong index issue.
---

# Wrong Index Solution

If you find that the execution speed of some query does not reach the expectation, the optimizer might choose the wrong index to run the query.

There are multiple reason why the optimizer might choose a different index than expected:

1. Statistics not being up to date
2. The statistics not matching the data closely
3. The calculated cost being wrong
4. Engine selection
5. Function pushdown limitations

## Statistics

You can first view the [health state of tables](/statistics.md#health-state-of-tables) in the statistics, and then solve this issue according to the different health states.

### Low health state

The low health state means TiDB has not performed the`ANALYZE` statement for a long time. You can update the statistics by running the `ANALYZE` command. After the update, if the optimizer still uses the wrong index, refer to the next section.

### Near 100% health state

The near 100% health state suggests that the `ANALYZE` statement is just completed or was completed a short time ago. In this case, the wrong index issue might be related to TiDB's estimation logic for the number of rows.

For equivalence queries, the cause might be [Count-Min Sketch](/statistics.md#count-min-sketch). You can check whether Count-Min Sketch is the cause and take corresponding solutions.

If the cause above does not apply to your problem, you can force-select indexes by using the `USE_INDEX` or `use index` optimzer hint (see [USE_INDEX](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-) for details). Also, you can change the query behavior by using [SQL Plan Management](/sql-plan-management.md) in a non-intrusive way.

### Other situations

Apart from the aforementioned situations, the wrong index issue might also be caused by data updates which renders all the indexes no longer applicable. In such cases, you need to perform analysis on the conditions and data distribution to see whether new indexes can speed up the query. If so, you can add new indexes by running the [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) command.

## Statistics mismatch

If the data is very skewed then the statistics might not reflect this. If this is the case then it might help to try the options of [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) to improve how well the statistics match the index.

An examples of this would be an index on a table with orders with an index on `customer_id`. And then having more than 50% of the orders with the same `customer_id`.

## Cost information

The [`EXPLAIN`](/sql-statements/sql-statement-explain.md) and [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) can show cost information with the `FORMAT=verbose` option. This can help to see the cost difference between two different execution paths.

## Engine selection

TiDB might have the option to use TiKV or TiFlash to access a table. By using engine isolation different engines can be tried out for the same query.

See [Engine isolation](/tiflash/use-tidb-to-read-tiflash.md#engine-isolation)

## Function pushdown

Functions be pushed down to storage engines if they are supported for the storage engine. Some functions can't be pushed down and this might limit the available execution plans.

Note that there is a blocklist of expression pushdown and optimization rules.

- [TiKV Supported Pushdown Calculations](/functions-and-operators/expressions-pushed-down.md)
- [TiFlash Supported Pushdown Calculations](/tiflash/tiflash-supported-pushdown-calculations.md)
- [The Blocklist of Optimization Rules and Expression Pushdown](/blocklist-control-plan.md)

## See also

- [Statistics](/statistics.md)
- [Index selection](/choose-index.md)
- [Optimizer hints](/optimizer-hints.md)
- [SQL Plan Management](/sql-plan-management.md)