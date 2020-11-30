---
title: EXPLAIN Overview
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
aliases: ['/docs/dev/query-execution-plan/','/docs/dev/reference/performance/understanding-the-query-execution-plan/','/docs/dev/index-merge/','/docs/dev/reference/performance/index-merge/','/tidb/dev/index-merge','/tidb/dev/query-execution-plan']
---

# `EXPLAIN` Overview

Because SQL is a declarative language, it describes what the results of a query should look like, **not the methodology** to actually retrieve those results. TiDB considers all the possible ways in which a query could be executed, including using what order to join tables and whether any potential indexes can be used. The process of _considering query execution plans_ is known as SQL optimization.

The `EXPLAIN` statement shows the selected execution plan for a given statement. That is, after considering hundreds or thousands of ways in which the query could be executed, TiDB believes that this _plan_ will consume the least resources and execute in the shortest amount of time:

{{< copyable "sql" >}}

```sql
CREATE TABLE t (id INT NOT NULL PRIMARY KEY auto_increment, a INT NOT NULL, pad1 VARCHAR(255), INDEX(a));
INSERT INTO t VALUES (1, 1, 'aaa'),(2,2, 'bbb');
EXPLAIN SELECT * FROM t WHERE a = 1;
```

```sql
Query OK, 0 rows affected (0.96 sec)

Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0

+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
| id                            | estRows | task      | access object       | operator info                               |
+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
| IndexLookUp_10                | 10.00   | root      |                     |                                             |
| ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t, index:a(a) | range:[1,1], keep order:false, stats:pseudo |
| └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:t             | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
3 rows in set (0.00 sec)
```

`EXPLAIN` does not execute the actual query. [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) can be used to both `EXPLAIN` _and_ execute the query. This can be useful in diagnosing cases where the execution plan selected is suboptimal.

## Understand EXPLAIN output

The following describes the output of the `EXPLAIN` statement above:

* `id` describes the name of an operator, or sub-task that is required to execute the SQL statement. While the structure appears as a tree, executing the query does not strictly require the child nodes to be completed before the parent nodes. TiDB supports intra-query parallelism, so a more accurate way to describe the execution flow is that the child nodes _feed into_ their parent nodes. Parent, child and sibling operators _might_ potentially be executing parts of the query in parallel.

  In this case, the `build` operator finds the internal `RowID` for rows that match in the index `idx_a`. The `probe` operator then retrieves these rows from the table.

* `estRows` shows an estimate of the number of rows TiDB expects to process. This number might be based on dictionary information, such as when the access method is based on a primary or unique key, or it could be based on statistics such as a CMSketch or histogram.

* `task` shows where an operator is performing the work. A task of `cop[tikv]` indicates that work is being completed inside TiKV as part of the coprocessor. TiDB attempts to push as much of the query to the data as possible, which can reduce the amount of data sent across the network. `root` tasks indicate that the operator is executed inside TiDB.

* `access object` shows the table, partition and index that is being accessed. The parts of the index will also be shown, as in the case above the column `a` from the index was used. This can be useful in cases where you have composite indexes.

* `operator info` shows additional details about the access, such as which conditions were able to be pushed down:

    * `range: [1,1]` shows that the predicate from the where clause of the query (`a = 1`) was pushed right down to TiKV (the task is of `cop[tikv]`).
    * `keep order:false` shows that the semantics of this query did not require TiKV to return the results in order. If the query were to be modified to require an order (such as `SELECT * FROM t WHERE a = 1 ORDER BY id`), then this condition would be `keep order:true`.
    * `stats:pseudo` shows that the estimates shown in `estRows` might not be accurate. TiDB periodically updates statistics as part of a background operation. A manual update can also be performed by running `ANALYZE TABLE t`.
