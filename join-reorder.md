---
title: Introduction to Join Reorder
summary: Use the Join Reorder algorithm to join multiple tables in TiDB.
aliases: ['/docs/dev/join-reorder/','/docs/dev/reference/performance/join-reorder/']
---

# Introduction to Join Reorder

In real application scenarios, it is common to join multiple tables. The execution efficiency of join is associated with the order in which each table joins.

For example:

{{< copyable "sql" >}}

```sql
SELECT * FROM t1, t2, t3 WHERE t1.a=t2.a AND t3.a=t2.a;
```

In this query, tables can be joined in the following two orders:

- t1 joins t2, and then joins t3
- t2 joins t3, and then joins t1

As t1 and t3 have different data volumes and distribution, these two execution orders might show different performances.

Therefore, the optimizer needs an algorithm to determine the join order. Currently, the following two Join Reorder algorithms are used in TiDB:

- The greedy algorithm: among all the nodes participating in Join, select the table with the smallest number of rows and each of the other tables to do a Join result estimation, then select the pair with the smallest result for Join, then continue the process to the next round of selection and Join, until all the nodes have completed Join.
- The dynamic programming algorithm: among all nodes participating in Join, enumerate all possible Join orders and select the optimal Join order.

## Example of the greedy algorithm

Take the three tables above (t1, t2, and t3) as an example.

First, TiDB obtains all the nodes that participates in the join operation, and sorts the nodes in the ascending order of row numbers.

![join-reorder-1](/media/join-reorder-1.png)

After that, the table with the least rows is selected and joined with other two tables respectively. By comparing the sizes of the output result sets, TiDB selects the pair with a smaller result set.

![join-reorder-2](/media/join-reorder-2.png)

Then TiDB enters the next round of selection. If you try to join four tables, TiDB continues to compare the sizes of the output result sets and selects the pair with a smaller result set.

In this case only three tables are joined, so TiDB gets the final join result.

![join-reorder-3](/media/join-reorder-3.png)

## Example of the dynamic programming algorithm

Taking the tables in [Example of the greedy algorithm](#example-of-the-greedy-algorithm) as an example. The dynamic programming algorithm enumerates all possibilities, so the greedy algorithm, which must start with the `t1` table, the dynamic programming algorithm can enumerate the Join order as follows.

! [join-reorder-4](/media/join-reorder-4.png)

When this choice is better than the greedy algorithm, the dynamic programming algorithm can choose a better Join order.

Accordingly, because all possibilities are enumerated, the dynamic programming algorithm consumes more time and is more susceptible to statistical information.

## Control the Join Reorder algorithm

The Join Reorder algorithm is controlled by the [`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold) variable. If the number of nodes participating in Join Reorder is greater than this threshold, the greedy algorithm is selected. Otherwise, the dynamic programming algorithm is selected.

## Limitations of Join Reorder algorithm

The current Join Reorder algorithm has the following limitations:

- Limited by the calculation methods of the result sets, the algorithm cannot ensure it selects the optimum join order.
- Currently, the Join Reorder algorithm's support for Outer Join is disabled by default. To enable it, set the value of the system variable [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) to `ON`.
- Currently, the dynamic planning algorithm cannot perform Join Reorder for Outer Join.

Currently, the `STRAIGHT_JOIN` syntax is supported in TiDB to force a join order. For more information, refer to [Description of the syntax elements](/sql-statements/sql-statement-select.md#description-of-the-syntax-elements).
