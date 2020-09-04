---
title: Joins
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# Joins

In TiDB, the SQL Optimizer needs to decide which order tables should be joined in, and what is the most efficient join algorithm for a particular SQL statement. The following examples explain the use of each join algorithm, and describe likely reasons why it was chosen.

## Index Join (Index Nested Loop Join)

If the result set (obtained after the outer tables are filtered by the `WHERE` condition) is small, it is recommended to use `Index Join`. Here "small" means data is less than 10,000 rows.

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                                                  |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| IndexJoin_11                | 12487.50 | root      |                        | inner join, inner:IndexReader_10, outer key:test.t1.id, inner key:test.t2.id   |
| ├─IndexReader_31(Build)     | 9990.00  | root      |                        | index:IndexFullScan_30                                                         |
| │ └─IndexFullScan_30        | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                                                 |
| └─IndexReader_10(Probe)     | 1.00     | root      |                        | index:Selection_9                                                              |
|   └─Selection_9             | 1.00     | cop[tikv] |                        | not(isnull(test.t2.id))                                                        |
|     └─IndexRangeScan_8      | 1.00     | cop[tikv] | table:t2, index:id(id) | range: decided by [eq(test.t2.id, test.t1.id)], keep order:false, stats:pseudo |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

## Hash Join

```
Pre-materializes some data into a hash table, and then efficient for access purposes. Works much faster than nested loop join when there are a lot of rows that need to be joined, or there are predicates that can filter rows on both tables.

Show an example:
```

The `Hash Join` operator uses multi-thread. Its execution speed is fast at the cost of more memory usage. An example of `Hash Join` is as follows:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+----------+-----------+------------------------+------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                  |
+-----------------------------+----------+-----------+------------------------+------------------------------------------------+
| HashJoin_30                 | 12487.50 | root      |                        | inner join, equal:[eq(test.t1.id, test.t2.id)] |
| ├─IndexReader_35(Build)     | 9990.00  | root      |                        | index:IndexFullScan_34                         |
| │ └─IndexFullScan_34        | 9990.00  | cop[tikv] | table:t2, index:id(id) | keep order:false, stats:pseudo                 |
| └─IndexReader_33(Probe)     | 9990.00  | root      |                        | index:IndexFullScan_32                         |
|   └─IndexFullScan_32        | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                 |
+-----------------------------+----------+-----------+------------------------+------------------------------------------------+
5 rows in set (0.01 sec)
```

The execution process of `Hash Join` is as follows:

1. Cache the data of the `Build` side in memory.
2. Construct a Hash Table on the `Build` side based on the cached data.
3. Read the data at the `Probe` side.
4. Use the data of the `Probe` side to probe the Hash Table.
5. Return qualified data to the user.

The operator info column in the `explain` table also records other information about `Hash Join`, including whether the query is Inner Join or Outer Join, and what are the conditions of Join. In the above example, the query is an Inner Join, where the Join condition `equal:[eq(test.t1.id, test.t2.id)]` partly corresponds with the query statement `where t1.id = t2. id`. The operator info of the other Join operators in the following examples is similar to this one.

## Merge Join
```
Like an efficient zipper merge. Requires little memory, usually very efficient but currently single threaded in TiDB.

Requires the data on both sides to be pre-sorted, otherwise a hash join will be prefered.

Show an example:
```

The `Merge Join` operator usually uses less memory than `Hash Join`. However, `Merge Join` might take longer to be executed. When the amount of data is large, or the system memory is insufficient, it is recommended to use `Merge Join`. The following is an example:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                         |
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------+
| MergeJoin_7                 | 12487.50 | root      |                        | inner join, left key:test.t1.id, right key:test.t2.id |
| ├─IndexReader_12(Build)     | 9990.00  | root      |                        | index:IndexFullScan_11                                |
| │ └─IndexFullScan_11        | 9990.00  | cop[tikv] | table:t2, index:id(id) | keep order:true, stats:pseudo                         |
| └─IndexReader_10(Probe)     | 9990.00  | root      |                        | index:IndexFullScan_9                                 |
|   └─IndexFullScan_9         | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:true, stats:pseudo                         |
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------+
5 rows in set (0.01 sec)
```

The execution of the `Merge Join` operator is as follows:

1. Read all the data of a Join Group from the `Build` side into the memory
2. Read the data of the `Probe` side.
3. Compare whether each row of data on the `Probe` side matches a complete Join Group on the `Build` side. Apart from equivalent conditions, there are non-equivalent conditions. Here "match" mainly refers to checking whether non-equivalent conditions are met. Join Group refers to the data with the same value among all Join Keys.

## Index Hash Join (Index Nested Loop Hash Join)

`Index Hash Join` uses the same conditions as `Index Join`. However, `Index Hash Join` saves more memory in some scenarios.

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ INL_HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                                                  |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
| IndexHashJoin_18            | 12487.50 | root      |                        | inner join, inner:IndexReader_10, outer key:test.t1.id, inner key:test.t2.id   |
| ├─IndexReader_31(Build)     | 9990.00  | root      |                        | index:IndexFullScan_30                                                         |
| │ └─IndexFullScan_30        | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                                                 |
| └─IndexReader_10(Probe)     | 1.00     | root      |                        | index:Selection_9                                                              |
|   └─Selection_9             | 1.00     | cop[tikv] |                        | not(isnull(test.t2.id))                                                        |
|     └─IndexRangeScan_8      | 1.00     | cop[tikv] | table:t2, index:id(id) | range: decided by [eq(test.t2.id, test.t1.id)], keep order:false, stats:pseudo |
+-----------------------------+----------+-----------+------------------------+--------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

## Index Merge Join (Index Nested Loop Merge Join)

`Index Merge Join` is used in similar scenarios as Index Join. However, the index prefix used by the inner table is the inner table column collection in the join keys. `Index Merge Join` saves more memory than `INL_JOIN`.

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ INL_MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object          | operator info                                                                 |
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------------------------------+
| IndexMergeJoin_16           | 12487.50 | root      |                        | inner join, inner:IndexReader_14, outer key:test.t1.id, inner key:test.t2.id  |
| ├─IndexReader_31(Build)     | 9990.00  | root      |                        | index:IndexFullScan_30                                                        |
| │ └─IndexFullScan_30        | 9990.00  | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                                                |
| └─IndexReader_14(Probe)     | 1.00     | root      |                        | index:Selection_13                                                            |
|   └─Selection_13            | 1.00     | cop[tikv] |                        | not(isnull(test.t2.id))                                                       |
|     └─IndexRangeScan_12     | 1.00     | cop[tikv] | table:t2, index:id(id) | range: decided by [eq(test.t2.id, test.t1.id)], keep order:true, stats:pseudo |
+-----------------------------+----------+-----------+------------------------+-------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```
