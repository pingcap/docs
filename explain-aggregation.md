---
title: Aggregation
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# Aggregation

Aggregation algorithms in TiDB include the following categories:

- [Hash Aggregate](#hash-aggregate-example)
- [Stream Aggregate](#stream-aggregate-example)

#### `Hash Aggregate` example

The `Hash Aggregation` operator is optimized in multi-threaded concurrency. It is quick to execute at the cost of more memory usage. The following is an example of `Hash Aggregate`:

{{< copyable "sql" >}}

```sql
explain select /*+ HASH_AGG() */ count(*) from t;
```

```sql
+---------------------------+----------+-----------+---------------+---------------------------------+
| id                        | estRows  | task      | access object | operator info                   |
+---------------------------+----------+-----------+---------------+---------------------------------+
| HashAgg_11                | 1.00     | root      |               | funcs:count(Column#7)->Column#4 |
| └─TableReader_12          | 1.00     | root      |               | data:HashAgg_5                  |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | funcs:count(1)->Column#7        |
|     └─TableFullScan_8     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo  |
+---------------------------+----------+-----------+---------------+---------------------------------+
4 rows in set (0.00 sec)
```

Generally speaking, `Hash Aggregate` is executed in two stages.

- One is on the Coprocessor of TiKV/TiFlash, with the intermediate results of the aggregation function calculated when the table scan operator reads the data.
- The other is at the TiDB layer, with the final result calculated through aggregating the intermediate results of all Coprocessor Tasks.

The operator info column in the `explain` table also records other information about `Hash Aggregation`. You need to pay attention to what aggregate function that `Hash Aggregation` uses. In the above example, the operator info of the `Hash Aggregation` operator is `funcs:count(Column#7)->Column#4`. It means that `Hash Aggregation` uses the aggregate function `count` for calculation. The operator info of the `Stream Aggregation` operator in the following example is the same with this one.

#### `Stream Aggregate` example

The `Stream Aggregation` operator usually takes up less memory than `Hash Aggregate`. In some scenarios, `Stream Aggregation` executes faster than `Hash Aggregate`. In the case of a large amount of data or insufficient system memory, it is recommended to use the `Stream Aggregate` operator. An example is as follows:

{{< copyable "sql" >}}

```sql
explain select /*+ STREAM_AGG() */ count(*) from t;
```

```sql
+----------------------------+----------+-----------+---------------+---------------------------------+
| id                         | estRows  | task      | access object | operator info                   |
+----------------------------+----------+-----------+---------------+---------------------------------+
| StreamAgg_16               | 1.00     | root      |               | funcs:count(Column#7)->Column#4 |
| └─TableReader_17           | 1.00     | root      |               | data:StreamAgg_8                |
|   └─StreamAgg_8            | 1.00     | cop[tikv] |               | funcs:count(1)->Column#7        |
|     └─TableFullScan_13     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo  |
+----------------------------+----------+-----------+---------------+---------------------------------+
4 rows in set (0.00 sec)
```

Similar to `Hash Aggregate`, `Stream Aggregate` is executed in two stages.

- One is on the Coprocessor of TiKV/TiFlash, with the intermediate results of the aggregation function calculated when the table scan operator reads the data.
- The other is at the TiDB layer, with the final result calculated through aggregating the intermediate results of all Coprocessor Tasks.


