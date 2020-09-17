---
title: Explain Statements Using Joins
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# Explain Statements Using Joins

In TiDB, the SQL Optimizer needs to decide which order tables should be joined in, and what is the most efficient join algorithm for a particular SQL statement. The examples are based on the following sample data:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, pad1 BLOB, pad2 BLOB, pad3 BLOB);
CREATE TABLE t2 (id INT NOT NULL PRIMARY KEY auto_increment, t1_id INT NOT NULL, pad1 BLOB, pad2 BLOB, pad3 BLOB, INDEX(t1_id));
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM dual;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
SELECT SLEEP(1);
ANALYZE TABLE t1, t2;
```

## Index Join (Index Nested Loop Join)

If the estimated rows that need to be joined is small (typically less than 10000 rows), using the Index Join method is preferable. This method of join works similar to the primary method of join used in MySQL. In the following example, the operator `IndexReader_31(Build)` first reads the table `t1`. For each row that matches, TiDB will probe the table `t2`:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id;
```

```sql
+---------------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                | operator info                                                                   |
+---------------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
| IndexJoin_11                    | 6000.00 | root      |                              | inner join, inner:IndexLookUp_10, outer key:test.t1.id, inner key:test.t2.t1_id |
| ├─TableReader_29(Build)         | 20.00   | root      |                              | data:TableFullScan_28                                                           |
| │ └─TableFullScan_28            | 20.00   | cop[tikv] | table:t1                     | keep order:false                                                                |
| └─IndexLookUp_10(Probe)         | 300.00  | root      |                              |                                                                                 |
|   ├─IndexRangeScan_8(Build)     | 300.00  | cop[tikv] | table:t2, index:t1_id(t1_id) | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:false             |
|   └─TableRowIDScan_9(Probe)     | 300.00  | cop[tikv] | table:t2                     | keep order:false                                                                |
+---------------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

Index join is efficient in memory usage, but may be slower to execute than other join methods when a large number of probe operations are required. Consider also the following query:

```sql
SELECT * FROM t1 INNER JOIN t2 ON t1.id=t2.t1_id WHERE t1.pad1 = 'value' and t2.pad1='value';
```

On an inner join, TiDB will apply join reordering and might access either `t1` or `t2` first. Assuming that TiDB selects `t1` as the first table to apply the `Build` step, it will be able to filter on the predicate `t1.col = 'value'` before probing the table `t2`. The filter for the predicate `t2.col='value'` will be applied on each probe of table `t2`, which may be less efficient than other join methods.

## Hash Join

A hash join reads and caches the data on the `Build` side of the join in a hash table, and then reads the data on the `Probe` side of the join, probing the hash table to access required rows. Hash joins require more memory to execute than Index Joins, but execute much faster when there are a lot of rows that need to be joined. The Hash Join operator is multi-threaded in TiDB, and executes in parallel.

An example Hash Join is as follows:

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

### Runtime Statistics

If the size of the hash table exceeds `tidb_mem_quota_query`, it will overflow to disk provided that `oom-use-tmp-storage=TRUE` (the default). Similarly, hash tables work most efficiently when the rate of hash collisions is relatively low. These runtime statistics can be observed in `EXPLAIN ANALYZE`:

```sql
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+---------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+----------------------+---------+
| id                          | estRows | actRows | task      | access object | execution info                                                                                                                                                                                  | operator info                                  | memory               | disk    |
+-----------------------------+---------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+----------------------+---------+
| HashJoin_27                 | 20.00   | 10      | root      |               | time:16.793524ms, loops:2, build_hash_table:{total:569.736µs, fetch:565.386µs, build:4.35µs}, probe:{concurrency:5, total:83.482002ms, max:16.749324ms, probe:296.137µs, fetch:83.185865ms}     | inner join, equal:[eq(test.t1.id, test.t2.id)] | 68.92578125 KB       | 0 Bytes |
| ├─TableReader_29(Build)     | 20.00   | 10      | root      |               | time:496.427µs, loops:2, cop_task: {num: 1, max:526.566µs, proc_keys: 10, rpc_num: 1, rpc_time: 502.026µs, copr_cache_hit_ratio: 0.00}                                                          | data:TableFullScan_28                          | 30.5556640625 KB     | N/A     |
| │ └─TableFullScan_28        | 20.00   | 10      | cop[tikv] | table:t1      | time:0s, loops:1                                                                                                                                                                                | keep order:false                               | N/A                  | N/A     |
| └─TableReader_31(Probe)     | 6000.00 | 3000    | root      |               | time:16.615265ms, loops:4, cop_task: {num: 1, max:15.95008ms, proc_keys: 3000, rpc_num: 1, rpc_time: 15.930511ms, copr_cache_hit_ratio: 0.00}                                                   | data:TableFullScan_30                          | 8.904180526733398 MB | N/A     |
|   └─TableFullScan_30        | 6000.00 | 3000    | cop[tikv] | table:t2      | time:8ms, loops:7                                                                                                                                                                               | keep order:false                               | N/A                  | N/A     |
+-----------------------------+---------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+----------------------+---------+
5 rows in set (0.01 sec)
```

## Merge Join

Merge join is a special sort of join that applies when both sides of the join can be read in sorted order. It can be described as similar to an _efficient zipper merge_, in that as data is read on both the `Build` and the `Probe` side of the join it can be compared as a streaming operation. Merge joins require far less memory than hash join, but do not execute in parallel.

The following is an example:

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
EXPLAIN SELECT /*+ INL_HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.t1_id;
```

```sql
+---------------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                | operator info                                                                   |
+---------------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
| IndexHashJoin_13                | 6000.00 | root      |                              | inner join, inner:IndexLookUp_10, outer key:test.t1.id, inner key:test.t2.t1_id |
| ├─TableReader_29(Build)         | 20.00   | root      |                              | data:TableFullScan_28                                                           |
| │ └─TableFullScan_28            | 20.00   | cop[tikv] | table:t1                     | keep order:false                                                                |
| └─IndexLookUp_10(Probe)         | 300.00  | root      |                              |                                                                                 |
|   ├─IndexRangeScan_8(Build)     | 300.00  | cop[tikv] | table:t2, index:t1_id(t1_id) | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:false             |
|   └─TableRowIDScan_9(Probe)     | 300.00  | cop[tikv] | table:t2                     | keep order:false                                                                |
+---------------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

## Index Merge Join (Index Nested Loop Merge Join)

`Index Merge Join` is used in similar scenarios as Index Join. However, the index prefix used by the inner table is the inner table column collection in the join keys. `Index Merge Join` saves more memory than `INL_JOIN`.

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT /*+ INL_MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.t1_id;
```

```sql
+----------------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
| id                               | estRows | task      | access object                | operator info                                                                   |
+----------------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
| IndexMergeJoin_18                | 6000.00 | root      |                              | inner join, inner:IndexLookUp_16, outer key:test.t1.id, inner key:test.t2.t1_id |
| ├─TableReader_29(Build)          | 20.00   | root      |                              | data:TableFullScan_28                                                           |
| │ └─TableFullScan_28             | 20.00   | cop[tikv] | table:t1                     | keep order:false                                                                |
| └─IndexLookUp_16(Probe)          | 300.00  | root      |                              |                                                                                 |
|   ├─IndexRangeScan_14(Build)     | 300.00  | cop[tikv] | table:t2, index:t1_id(t1_id) | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:true              |
|   └─TableRowIDScan_15(Probe)     | 300.00  | cop[tikv] | table:t2                     | keep order:false                                                                |
+----------------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```