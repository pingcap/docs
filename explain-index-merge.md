---
title: Explain Statements Using Index Merge
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# Explain Statements Using Index Merge

Index Merge is a method introduced in TiDB v4.0 to access tables. Using this method, the TiDB optimizer can use multiple indexes per table and merge the results returned by each index. In some scenarios, this method makes the query more efficient by avoiding full table scans.

```sql
mysql> EXPLAIN SELECT * FROM t WHERE a = 1 or b = 1;
+-------------------------+----------+-----------+---------------+--------------------------------------+
| id                      | estRows  | task      | access object | operator info                        |
+-------------------------+----------+-----------+---------------+--------------------------------------+
| TableReader_7           | 8000.00  | root      |               | data:Selection_6                     |
| └─Selection_6           | 8000.00  | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+----------+-----------+---------------+--------------------------------------+
EXPLAIN SELECT /*+ USE_INDEX_MERGE(t) */ * FROM t WHERE a > 1 OR b > 1;
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                             | estRows | task      | access object           | operator info                                  |
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_16                  | 6666.67 | root      |                         |                                                |
| ├─IndexRangeScan_13(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_14(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_15(Probe)     | 6666.67 | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

In the above query, the filter condition is a `WHERE` clause that uses `OR` as the connector. Without Index Merge, you can use only one index per table. `a = 1` cannot be pushed down to the index `a`; neither can `b = 1` be pushed down to the index `b`. The full table scan is inefficient when a huge volume of data exists in `t`. To handle such a scenario, Index Merge is introduced in TiDB to access tables.

Index Merge allows the optimizer to use multiple indexes per table, and merge the results returned by each index to generate the execution plan of the latter `IndexMerge` in the figure above. Here the `IndexMerge_16` operator has three child nodes, among which `IndexRangeScan_13` and `IndexRangeScan_14` get all the `RowID`s that meet the conditions based on the result of range scan, and then the `TableRowIDScan_15` operator accurately reads all the data that meets the conditions according to these `RowID`s.

For the scan operation that is performed on a specific range of data, such as `IndexRangeScan`/`TableRangeScan`, the `operator info` column in the result has additional information about the scan range compared with other scan operations like `IndexFullScan`/`TableFullScan`. In the above example, the `range:(1,+inf]` in the `IndexRangeScan_13` operator indicates that the operator scans the data from 1 to positive infinity.

> **Note:**
>
> - The Index Merge feature is enabled by default in TiDB 5.4.0 and later versions. That is, [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40) is `ON`.
>
> - When the SQL Hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) is used, Index Merge is enabled mandatorily, regardless of the setting of `tidb_enable_index_merge`. To enable Index Merge when the filtering conditions contain expressions that cannot be pushed down, use SQL Hint [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-).
>
> - Index Merge supports only disjunctive normal forms (DNFs, expressions connected by `or`) and does not support conjunctive normal forms (CNFs, expressions connected by `and`).
>
> - Index Merge is not applicable to temporary tables.