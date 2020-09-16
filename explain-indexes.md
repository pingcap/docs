---
title: Explain Statements Using Indexes
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# Explain Statements Using Indexes

## Operator execution order

The execution plan in TiDB has a tree structure, with each node of the tree as an operator. Considering the concurrent execution of multiple threads in each operator, all operators consume CPU and memory resources to process data during the execution of a SQL statement. From this point of view, there is no execution order for the operator.

However, from the perspective of which operators process a row of data first, the execution of a piece of data is in order. The following rule roughly summarizes this order:

**`Build` is always executed before `Probe` and always appears before `Probe`.**

The first half of this rule means: if an operator has multiple child nodes, the operator with the `Build` keyword at the end of the child node ID is always executed before the operator with the `Probe` keyword. The second half means: when TiDB shows the execution plan, the `Build` side always appears first, followed by the `Probe` side.

The following examples illustrate this rule:

{{< copyable "sql" >}}

```sql
explain select * from t use index(idx_a) where a = 1;
```

```sql
+-------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| id                            | estRows | task      | access object           | operator info                               |
+-------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| IndexLookUp_7                 | 10.00   | root      |                         |                                             |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t, index:idx_a(a) | range:[1,1], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 10.00   | cop[tikv] | table:t                 | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+-------------------------+---------------------------------------------+
3 rows in set (0.00 sec)
```

The `IndexLookUp_7` operator has two child nodes: `IndexRangeScan_5 (Build)` and `TableRowIDScan_6 (Probe)`. `IndexRangeScan_5 (Build)` appears first.

To get a piece of data, first, you need to execute `IndexRangeScan_5 (Build)` to get a RowID. Then, use `TableRowIDScan_6 (Probe)` to get a complete row of data based on the RowID.

The implication of the above rule is: for nodes at the same level, the operator that appears first might be executed first, and the operator that appears last might be executed last. This can be illustrated in the following example:

{{< copyable "sql" >}}

```sql
explain select * from t t1 use index(idx_a) join t t2 use index() where t1.a = t2.a;
```

```sql
+----------------------------------+----------+-----------+--------------------------+------------------------------------------------------------------+
| id                               | estRows  | task      | access object            | operator info                                                    |
+----------------------------------+----------+-----------+--------------------------+------------------------------------------------------------------+
| HashJoin_22                      | 12487.50 | root      |                          | inner join, inner:TableReader_26, equal:[eq(test.t.a, test.t.a)] |
| ├─TableReader_26(Build)          | 9990.00  | root      |                          | data:Selection_25                                                |
| │ └─Selection_25                 | 9990.00  | cop[tikv] |                          | not(isnull(test.t.a))                                            |
| │   └─TableFullScan_24           | 10000.00 | cop[tikv] | table:t2                 | keep order:false, stats:pseudo                                   |
| └─IndexLookUp_29(Probe)          | 9990.00  | root      |                          |                                                                  |
|   ├─IndexFullScan_27(Build)      | 9990.00  | cop[tikv] | table:t1, index:idx_a(a) | keep order:false, stats:pseudo                                   |
|   └─TableRowIDScan_28(Probe)     | 9990.00  | cop[tikv] | table:t1                 | keep order:false, stats:pseudo                                   |
+----------------------------------+----------+-----------+--------------------------+------------------------------------------------------------------+
7 rows in set (0.00 sec)
```

To complete the `HashJoin_22` operation, you need to execute `TableReader_26(Build)`, and then execute `IndexLookUp_29(Probe)`.

When executing `IndexLookUp_29(Probe)`, you need to execute `IndexFullScan_27(Build)` and `TableRowIDScan_28(Probe)` one by one. Therefore, from the perspective of the whole execution link, `TableRowIDScan_28(Probe)` is the last one awoken to be executed.

### Task overview

Currently, calculation tasks of TiDB can be divided into two categories: cop tasks and root tasks. The cop tasks are performed by the Coprocessor in TiKV, and the root tasks are performed in TiDB.

One of the goals of SQL optimization is to push the calculation down to TiKV as much as possible. The Coprocessor in TiKV supports most of the built-in SQL functions (including the aggregate functions and the scalar functions), SQL `LIMIT` operations, index scans, and table scans. However, all `Join` operations can only be performed as root tasks in TiDB.

### Access Object overview

Access Object is the data item accessed by the operator, including `table`, `partition`, and `index` (if any). Only operators that directly access the data have this information.

### Range query

In the `WHERE`/`HAVING`/`ON` conditions, the TiDB optimizer analyzes the result returned by the primary key query or the index key query. For example, these conditions might include comparison operators of the numeric and date type, such as `>`, `<`, `=`, `>=`, `<=`, and the character type such as `LIKE`.

> **Note:**
>
> - Currently, TiDB only supports the case where a comparison operator is connected by a column (at one end) and a constant value (at the other end), or the case that the calculation result is a constant. You cannot use query conditions like `year(birth_day) < 1992` as the index.
> - It is recommended to compare data of the same type; otherwise, additional `cast` operations are introduced, which causes the index to be unavailable. For example, regarding the condition `user_id = 123456`, if `user_id` is a string, you must define `123456` as a string constant.

You can also use `AND` (intersection) and `OR` (union) to combine the range query conditions of one column. For a multi-dimensional composite index, you can use conditions in multiple columns. For example, regarding the composite index `(a, b, c)`:

- When `a` is an equivalent query, continue to figure out the query range of `b`; when `b` is also an equivalent query, continue to figure out the query range of `c`.
- Otherwise, if `a` is a non-equivalent query, you can only figure out the range of `a`.

## Operator overview

Different operators output different information after the `EXPLAIN` statement is executed. This section focuses on the execution plan of different operators, ranging from table scans, table aggregation, to table join.

You can use optimizer hints to control the behavior of the optimizer, and thereby controlling the selection of the physical operators. For example, `/*+ HASH_JOIN(t1, t2) */` means that the optimizer uses the `Hash Join` algorithm. For more details, see [Optimizer Hints](/optimizer-hints.md).

### Read the execution plan of table scans

The operators that perform table scans (of the disk or the TiKV Block Cache) are listed as follows:

- **TableFullScan**: Full table scan.
- **TableRangeScan**: Table scans with the specified range.
- **TableRowIDScan**: Accurately scans the table data based on the RowID passed down from the upper layer.
- **IndexFullScan**: Another type of "full table scan", except that the index data is scanned, rather than the table data.
- **IndexRangeScan**: Index scans with the specified range.

TiDB aggregates the data or calculation results scanned from TiKV/TiFlash. The data aggregation operators can be divided into the following categories:

- **TableReader**: Aggregates the data obtained by the underlying operators like `TableFullScan` or `TableRangeScan` in TiKV.
- **IndexReader**: Aggregates the data obtained by the underlying operators like `IndexFullScan` or `IndexRangeScan` in TiKV.
- **IndexLookUp**: First aggregates the RowID (in TiKV) scanned by the `Build` side. Then at the `Probe` side, accurately reads the data from TiKV based on these RowIDs. At the `Build` side, there are operators like `IndexFullScan` or `IndexRangeScan`; at the `Probe` side, there is the `TableRowIDScan` operator.
- **IndexMerge**: Similar to `IndexLookUp`. `IndexMerge` can be seen as an extension of `IndexLookupReader`. `IndexMerge` supports reading multiple indexes at the same time. There are many `Build`s and one `Probe`. The execution process of `IndexMerge` the same as that of `IndexLookUp`.

#### Table data and index data

Table data refers to the original data of a table stored in TiKV. For each row of the table data, its `key` is a 64-bit integer called `RowID`. If a primary key of a table is an integer, TiDB uses the value of the primary key as the `RowID` of the table data; otherwise, the system automatically generates `RowID`. The `value` of the table data is encoded from all the data in this row. When reading table data, data is returned in the order of increasing `RowID`s.

Similar to the table data, the index data is also stored in TiKV. Its `key` is the ordered bytes encoded from the index column. `value` is the `RowID` corresponding to a row of index data. The non-index column of the row can be read using `RowID`. When reading index data, TiKV returns data in ascending order of index columns. If there are multiple index columns, firstly, ensure that the first column is incremented; if the i-th column is equivalent, make sure that the (i+1)-th column is incremented.

#### `IndexLookUp` example

{{< copyable "sql" >}}

```sql
explain select * from t use index(idx_a);
```

```sql
+-------------------------------+----------+-----------+-------------------------+--------------------------------+
| id                            | estRows  | task      | access object           | operator info                  |
+-------------------------------+----------+-----------+-------------------------+--------------------------------+
| IndexLookUp_6                 | 10000.00 | root      |                         |                                |
| ├─IndexFullScan_4(Build)      | 10000.00 | cop[tikv] | table:t, index:idx_a(a) | keep order:false, stats:pseudo |
| └─TableRowIDScan_5(Probe)     | 10000.00 | cop[tikv] | table:t                 | keep order:false, stats:pseudo |
+-------------------------------+----------+-----------+-------------------------+--------------------------------+
3 rows in set (0.00 sec)
```

The `IndexLookUp_6` operator has two child nodes: `IndexFullScan_4(Build)` and `TableRowIDScan_5(Probe)`.

+ `IndexFullScan_4(Build)` performs an index full scan and scans all the data of index `a`. Because it is a full scan, this operation gets the `RowID` of all the data in the table.
+ `TableRowIDScan_5(Probe)` scans all table data using `RowID`s.

This execution plan is not as efficient as using `TableReader` to perform a full table scan, because `IndexLookUp` performs an extra index scan (which comes with additional overhead), apart from the table scan.

For table scan operations, the operator info column in the `explain` table shows whether the data is sorted. In the above example, the `keep order:false` in the `IndexFullScan` operator indicates that the data is unsorted. The `stats:pseudo` in the operator info means that there is no statistics, or that the statistics will not be used for estimation because it is outdated. For other scan operations, the operator info involves similar information.

#### `TableReader` example

{{< copyable "sql" >}}

```sql
explain select * from t where a > 1 or b >100;
```

```sql
+-------------------------+----------+-----------+---------------+----------------------------------------+
| id                      | estRows  | task      | access object | operator info                          |
+-------------------------+----------+-----------+---------------+----------------------------------------+
| TableReader_7           | 8000.00  | root      |               | data:Selection_6                       |
| └─Selection_6           | 8000.00  | cop[tikv] |               | or(gt(test.t.a, 1), gt(test.t.b, 100)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo         |
+-------------------------+----------+-----------+---------------+----------------------------------------+
3 rows in set (0.00 sec)
```

In the above example, the child node of the `TableReader_7` operator is `Selection_6`. The subtree rooted at this child node is seen as a `Cop Task` and is delivered to the corresponding TiKV. This `Cop Task` uses the `TableFullScan_5` operator to perform the table scan. `Selection` represents the selection condition in the SQL statement, namely, the `WHERE`/`HAVING`/`ON` clause.

`TableFullScan_5` performs a full table scan, and the load on the cluster increases accordingly, which might affect other queries running in the cluster. If an appropriate index is built and the `IndexMerge` operator is used, these will greatly improve query performance and reduce load on the cluster.
