---
title: Explain Statements Using Index Merge
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# Explain Statements Using Index Merge

`IndexMerge` is a method introduced in TiDB v4.0 to access tables. Using this method, the TiDB optimizer can use multiple indexes per table and merge the results returned by each index. In some scenarios, this method makes the query more efficient by avoiding full table scans.

## Enable `IndexMerge`

In v5.4.0 or a later TiDB version, `IndexMerge` is enabled by default. In other situations, if `IndexMerge` is not enabled, you need to set the variable [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40) to `ON` to enable this feature.

The `IndexMerge` in TiDB has two types: the intersection type and the union type. The former is suitable for the `AND` expression, while the latter is suitable for the `OR` expression. The union type `IndexMerge` is introduced in TiDB v4.0. The intersection type is introduced in TiDB v6.5.0, and can only be used when the [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) hint is specified.

```sql
SET session tidb_enable_index_merge = ON;
```

```sql
CREATE TABLE t(a int, b int, c int, d int, INDEX idx_a(a), INDEX idx_b(b), INDEX idx_c(c), INDEX idx_d(d));
```

```sql
EXPLAIN SELECT /*+ NO_INDEX_MERGE() */  * FROM t WHERE a = 1 OR b = 1;

+-------------------------+----------+-----------+---------------+--------------------------------------+
| id                      | estRows  | task      | access object | operator info                        |
+-------------------------+----------+-----------+---------------+--------------------------------------+
| TableReader_7           | 19.99    | root      |               | data:Selection_6                     |
| └─Selection_6           | 19.99    | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+----------+-----------+---------------+--------------------------------------+
EXPLAIN SELECT /*+ USE_INDEX_MERGE(t) */ * FROM t WHERE a > 1 OR b > 1;
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                            | estRows | task      | access object           | operator info                                  |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_8                  | 5555.56 | root      |                         | type: union                                    |
| ├─IndexRangeScan_5(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_7(Probe)     | 5555.56 | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

In the preceding query, the filter condition is a `WHERE` clause that uses `OR` as the connector. Without `IndexMerge`, you can use only one index per table. `a = 1` cannot be pushed down to the index `a`; neither can `b = 1` be pushed down to the index `b`. The full table scan is inefficient when a huge volume of data exists in `t`. To handle such a scenario, `IndexMerge` is introduced in TiDB to access tables.

For the preceding query, the optimizer chooses the intersection type `IndexMerge` to access the table.`IndexMerge` allows the optimizer to use multiple indexes per table, and merge the results returned by each index to generate the execution plan of the latter `IndexMerge` in the figure above.

At this time, the `type: union` information in `operator info` of the `IndexMerge_8` operator indicates that this operator is a union type `IndexMerge`. It has three child nodes. `IndexRangeScan_5` and `IndexRangeScan_6` scan the `RowID`s that meet the condition according to the range, and then the `TableRowIDScan_7` operator reads all the data that meets the condition according to these `RowID`s.

For the scan operation that is performed on a specific range of data, such as `IndexRangeScan`/`TableRangeScan`, the `operator info` column in the result has additional information about the scan range compared with other scan operations like `IndexFullScan`/`TableFullScan`. In the above example, the `range:(1,+inf]` in the `IndexRangeScan_13` operator indicates that the operator scans the data from 1 to positive infinity.

```sql
EXPLAIN SELECT /*+ NO_INDEX_MERGE() */ * FROM t WHERE a > 1 AND b > 1 AND c = 1;  -- Does not use IndexMerge

+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| id                             | estRows | task      | access object           | operator info                               |
+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| IndexLookUp_19                 | 1.11    | root      |                         |                                             |
| ├─IndexRangeScan_16(Build)     | 10.00   | cop[tikv] | table:t, index:idx_c(c) | range:[1,1], keep order:false, stats:pseudo |
| └─Selection_18(Probe)          | 1.11    | cop[tikv] |                         | gt(test.t.a, 1), gt(test.t.b, 1)            |
|   └─TableRowIDScan_17          | 10.00   | cop[tikv] | table:t                 | keep order:false, stats:pseudo              |
+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+

EXPLAIN SELECT /*+ USE_INDEX_MERGE(t, idx_a, idx_b, idx_c) */ * FROM t WHERE a > 1 AND b > 1 AND c = 1;  -- Uses IndexMerge
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                            | estRows | task      | access object           | operator info                                  |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_9                  | 1.11    | root      |                         | type: intersection                             |
| ├─IndexRangeScan_5(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t, index:idx_c(c) | range:[1,1], keep order:false, stats:pseudo    |
| └─TableRowIDScan_8(Probe)     | 1.11    | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

From the preceding example, you can see that the filter condition is a `WHERE` clause that uses `AND` as the connector. Before `IndexMerge` is enabled, you can only choose one of the three indexes `idx_a`, `idx_b`, and `idx_c` to use.

If one of the filter conditions has a very good filtering performance, you can directly select the corresponding index to achieve the ideal execution efficiency. However, if the data distribution meets all of the following three conditions, you can consider using the intersection type `IndexMerge`:

- The data size of the full table is large, and directly reading the full table is inefficient.
- For each one of the three filter conditions, the respective filtering performance is not good enough, so the execution efficiency of `IndexLookUp` using a single index is not ideal.
- The overall filtering performance of the three filter conditions is good.

When using the intersection type `IndexMerge` to access table, the optimizer can choose to use multiple indexes on a table, and merge the results returned by each index to generate the execution plan of the latter `IndexMerge` in the preceding example. The `type: intersection` in the `operator info` of the `IndexMerge_9` operator indicates that this operator is an intersection type `IndexMerge`. The other parts of the execution plan are similar to the preceding union type `IndexMerge` example.

> **Note:**
>
> - The Index Merge feature is enabled by default from v5.4.0. That is, [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40) is `ON`.
>
> - You can use the SQL hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) to force the optimizer to apply Index Merge, regardless of the setting of `tidb_enable_index_merge`. To enable Index Merge when the filtering conditions contain expressions that cannot be pushed down, you must use the SQL hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-).
>
> - If there is a single index scan method (other than full table scan) can be selected for a query plan, the optimizer will not automatically select `IndexMerge`. You can only use the optimizer hint to specify using `IndexMerge`.
>
> - Index Merge is not supported in [tempoaray tables](/temporary-tables.md) for now.
>
> - The intersection type `IndexMerge` will not automatically be selected by the optimizer. You must specify the **table name and index name** using the [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) hint for it to be selected.
