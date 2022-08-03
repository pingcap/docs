---
title: Cost Model
summary: Introduce the principle of the cost model used by TiDB during physical optimization.
---

# Cost Model

TiDB uses the cost model to choose an index and operator during [Physical Optimization](/sql-physical-optimization.md). The diagram is as follows:

![CostModel](/media/cost-model.png)

TiDB calculates the access cost of each index and the execution cost of each physical operator in plans (such as HashJoin and IndexJoin) and chooses the minimum cost plan.

The following is a simplified example to explain the principle of the cost model. Suppose that there is a table `t`:

```sql
mysql> SHOW CREATE TABLE t;
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                        |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) DEFAULT NULL,
  KEY `b` (`b`),
  KEY `c` (`c`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

When executing the `SELECT * FROM t WHERE b < 100 and c < 100` command, suppose that TiDB estimates rows of `b < 100` and `c < 100` are 20 and 500 respectively, the length of `INT` type indexes is 8. Then TiDB calculates the cost for two indexes:

+ The cost of index `b` = `rows of b < 100` * `length of index b` = 20 * 8 = 160
+ The cost of index `c` = `rows of c < 100` * `length of index c` = 500 * 8 = 4000

Since the cost of index `b` is lower, TiDB chooses `b` as the index.

The preceding example is simplified and is used to explain the principle. The TiDB cost model is more complex in fact.

## Cost Model Version 2

> **Warning:**
>
> - Cost Model Version 2 is currently an experimental feature. It is not recommended that you use it for production environments.
> - Switching the version of the cost model might cause changes to query plans.

TiDB v6.2.0 introduces a new model Cost Model Version 2.

Cost Model Version 2 provides a more accurate regression calibration of the cost formula, adjusts some of the cost formulas, and is more accurate than previous versions of the cost formula.

To control the version of cost model, you can set the [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620) variable.
