---
title: EXPLAIN Walkthrough 
summary: Learn how to use `EXPLAIN` by walking through an example statement
---

# EXPLAIN Walkthrough

Because SQL is a declarative language, it is not possible to sight-check a query and tell if it is executing efficiently. We must first use [`EXPLAIN`](/sql-statements/sql-statement-explain.md) to understand what the current execution plan is.

The following statement from the [bikeshare example database](/import-example-data.md) counts how many trips were taken on the 1st July 2017:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| id                           | estRows  | task      | access object | operator info                                                                                                          |
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| StreamAgg_20                 | 1.00     | root      |               | funcs:count(Column#13)->Column#11                                                                                      |
| └─TableReader_21             | 1.00     | root      |               | data:StreamAgg_9                                                                                                       |
|   └─StreamAgg_9              | 1.00     | cop[tikv] |               | funcs:count(1)->Column#13                                                                                              |
|     └─Selection_19           | 250.00   | cop[tikv] |               | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) |
|       └─TableFullScan_18     | 10000.00 | cop[tikv] | table:trips   | keep order:false, stats:pseudo                                                                                         |
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

Working from the child operator `└─TableFullScan_18` back, you can see its execution process as follows, which is currently suboptimal:

1. The coprocessor (TiKV) reads the entire `trips` table as a `TableFullScan` operation. It then passes the rows that it reads to the `Selection_19` operator, which is still within TiKV.
2. The `WHERE start_date BETWEEN ..` predicate is then filtered in the `Selection_19` operator. Approximately `250` rows are estimated to meet this selection. Note that this number was produced from a heuristic; the `└─TableFullScan_18` operator shows `stats:pseudo`. After running `ANALYZE TABLE trips` the statistics should be more accurate.
3. The rows that meet the selection criteria then have a `count` function applied to them. This is also completed inside the `StreamAgg_9` operator, which is still inside TiKV (`cop[tikv]`). The TiKV coprocessor understands a number of MySQL built-in functions, `count` being one of them. It also understands that `count` is safe to apply Stream Aggregation to, even though the results are not in order.
4. The results from `StreamAgg_9` are then sent to `TableReader_21` which is now inside the TiDB server (task of `root`). The `estRows` does not make it entirely clear, but the `TableReader_21` operator will receive one row from each of the TiKV regions that had to be accessed. We can see more information about these requests in [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md).
5. The `StreamAgg_20` operator then has the task of applying a count function to each of the rows from the `└─TableReader_21` operator, which we can see from [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) will be about 56 rows. As this is the root operator, it can then return results to the client.

> **Note:**
> 
> For a general view of the regions a table contains, run [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md). 

## Assessing the current performance

[`EXPLAIN`](/sql-statements/sql-statement-explain.md) only returns the query execution plan, and does not execute the query. We can either run the query, or use [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) to get the actual execution time:

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+------------------------------+----------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| id                           | estRows  | actRows  | task      | access object | execution info                                                                                                                                                                                                                                    | operator info                                                                                                          | memory    | disk |
+------------------------------+----------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| StreamAgg_20                 | 1.00     | 1        | root      |               | time:1.031417203s, loops:2                                                                                                                                                                                                                        | funcs:count(Column#13)->Column#11                                                                                      | 632 Bytes | N/A  |
| └─TableReader_21             | 1.00     | 56       | root      |               | time:1.031408123s, loops:2, cop_task: {num: 56, max: 782.147269ms, min: 5.759953ms, avg: 252.005927ms, p95: 609.294603ms, max_proc_keys: 910371, p95_proc_keys: 704775, tot_proc: 11.524s, tot_wait: 580ms, rpc_num: 56, rpc_time: 14.111932641s} | data:StreamAgg_9                                                                                                       | 328 Bytes | N/A  |
|   └─StreamAgg_9              | 1.00     | 56       | cop[tikv] |               | proc max:640ms, min:8ms, p80:276ms, p95:480ms, iters:18695, tasks:56                                                                                                                                                                              | funcs:count(1)->Column#13                                                                                              | N/A       | N/A  |
|     └─Selection_19           | 250.00   | 11409    | cop[tikv] |               | proc max:640ms, min:8ms, p80:276ms, p95:476ms, iters:18695, tasks:56                                                                                                                                                                              | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) | N/A       | N/A  |
|       └─TableFullScan_18     | 10000.00 | 19117643 | cop[tikv] | table:trips   | proc max:612ms, min:8ms, p80:248ms, p95:460ms, iters:18695, tasks:56                                                                                                                                                                              | keep order:false, stats:pseudo                                                                                         | N/A       | N/A  |
+------------------------------+----------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
5 rows in set (1.03 sec)
```

The example query takes `1.03` seconds to execute. This is our benchmark to beat!

Importantly, we can also see some of the useful columns that [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) has added. `actRows` shows that some of our estimates were off. We knew this already because the `└─TableFullScan_18` showed `stats:pseudo`. But expecting 10 thousand rows and finding 19 million rows does not show that the estimate was very accurate. If we run [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md), and then [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) again we can see that the estimates are much closer:

{{< copyable "sql" >}}

```sql
ANALYZE TABLE trips;
EXPLAIN ANALYZE SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
Query OK, 0 rows affected (10.22 sec)

+------------------------------+-------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| id                           | estRows     | actRows  | task      | access object | execution info                                                                                                                                                                                                                                   | operator info                                                                                                          | memory    | disk |
+------------------------------+-------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| StreamAgg_20                 | 1.00        | 1        | root      |               | time:926.393612ms, loops:2                                                                                                                                                                                                                       | funcs:count(Column#13)->Column#11                                                                                      | 632 Bytes | N/A  |
| └─TableReader_21             | 1.00        | 56       | root      |               | time:926.384792ms, loops:2, cop_task: {num: 56, max: 850.94424ms, min: 6.042079ms, avg: 234.987725ms, p95: 495.474806ms, max_proc_keys: 910371, p95_proc_keys: 704775, tot_proc: 10.656s, tot_wait: 904ms, rpc_num: 56, rpc_time: 13.158911952s} | data:StreamAgg_9                                                                                                       | 328 Bytes | N/A  |
|   └─StreamAgg_9              | 1.00        | 56       | cop[tikv] |               | proc max:592ms, min:4ms, p80:244ms, p95:480ms, iters:18695, tasks:56                                                                                                                                                                             | funcs:count(1)->Column#13                                                                                              | N/A       | N/A  |
|     └─Selection_19           | 432.89      | 11409    | cop[tikv] |               | proc max:592ms, min:4ms, p80:244ms, p95:480ms, iters:18695, tasks:56                                                                                                                                                                             | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) | N/A       | N/A  |
|       └─TableFullScan_18     | 19117643.00 | 19117643 | cop[tikv] | table:trips   | proc max:564ms, min:4ms, p80:228ms, p95:456ms, iters:18695, tasks:56                                                                                                                                                                             | keep order:false                                                                                                       | N/A       | N/A  |
+------------------------------+-------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
5 rows in set (0.93 sec)
```

After [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) is executed, we can see that the estimated rows for the `└─TableFullScan_18` is accurate, and the estimate for `└─Selection_19` is now also much closer. While in this case the execution plan (i.e. the set of operators TiDB uses to execute this query) has not changed in between running [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md), quite frequently sub-optimal plans are caused by out of date statistics.

As well as [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md), TiDB will automatically regenerate statistics as a background operation after a [threshold is reached](/system-variables.md#tidb_auto_analyze_ratio). You can see how close TiDB is to this threshold (i.e. how healthy it considers the statistics to be) with the statement [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md):

{{< copyable "sql" >}}

```sql
SHOW STATS_HEALTHY;
```

```sql
+-----------+------------+----------------+---------+
| Db_name   | Table_name | Partition_name | Healthy |
+-----------+------------+----------------+---------+
| bikeshare | trips      |                |     100 |
+-----------+------------+----------------+---------+
1 row in set (0.00 sec)
```

## Identifying optimizations

There are some aspects of the current execution plan that are quite efficient:

* Most of the work is handled inside the TiKV coprocessor. Only 56 rows need to be sent across the network back to TiDB for processing. Each of these rows is short, and contains only the count that matched the selection.

* Both aggregating the count of rows in TiDB (`StreamAgg_20`), and aggregating in TiKV (`└─StreamAgg_9`) are using stream aggregation, which is very efficient in its memory usage.

The biggest issue with the current execution plan, is that the predicate `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` does not apply immediately. All rows are read first with a TableFullScan operator, and then a selection is applied afterwards. If we look at the output from `SHOW CREATE TABLE trips` we can see why this is:

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE trips\G
```

```sql
*************************** 1. row ***************************
       Table: trips
Create Table: CREATE TABLE `trips` (
  `trip_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `duration` int(11) NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `start_station_number` int(11) DEFAULT NULL,
  `start_station` varchar(255) DEFAULT NULL,
  `end_station_number` int(11) DEFAULT NULL,
  `end_station` varchar(255) DEFAULT NULL,
  `bike_number` varchar(255) DEFAULT NULL,
  `member_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`trip_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=20477318
1 row in set (0.00 sec)
```

There is no index on `start_date`! We would need an index in order to push this predicate into an index reader operator. Let's go ahead and add one:

{{< copyable "sql" >}}

```sql
ALTER TABLE trips ADD INDEX (start_date);
```

```sql
Query OK, 0 rows affected (2 min 10.23 sec)
```

> **Tip:**
> 
> The progress of DDL jobs can be monitored with the command [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin.md). The defaults in TiDB are carefully chosen so that adding an index does not impact production workloads too much. For testing environments, consider increasing [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size) and [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt). On a reference system, a batch size of 10240 and worker count of 32 achieved a 10x improvement over the defaults.

After adding an index, you can then repeat the query in `EXPLAIN`. In the following output, you can see that a new execution plan is chosen, and the `TableFullScan` and `Selection` operators have been eliminated:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+-----------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------------------+
| id                          | estRows | task      | access object                             | operator info                                                     |
+-----------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------------------+
| StreamAgg_17                | 1.00    | root      |                                           | funcs:count(Column#13)->Column#11                                 |
| └─IndexReader_18            | 1.00    | root      |                                           | index:StreamAgg_9                                                 |
|   └─StreamAgg_9             | 1.00    | cop[tikv] |                                           | funcs:count(1)->Column#13                                         |
|     └─IndexRangeScan_16     | 8471.88 | cop[tikv] | table:trips, index:start_date(start_date) | range:[2017-07-01 00:00:00,2017-07-01 23:59:59], keep order:false |
+-----------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------------------+
4 rows in set (0.00 sec)
```

To compare the actual execution time, you can again use [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md):

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+-----------------------------+---------+---------+-----------+-------------------------------------------+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+------+
| id                          | estRows | actRows | task      | access object                             | execution info                                                                                                   | operator info                                                     | memory    | disk |
+-----------------------------+---------+---------+-----------+-------------------------------------------+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+------+
| StreamAgg_17                | 1.00    | 1       | root      |                                           | time:4.516728ms, loops:2                                                                                         | funcs:count(Column#13)->Column#11                                 | 372 Bytes | N/A  |
| └─IndexReader_18            | 1.00    | 1       | root      |                                           | time:4.514278ms, loops:2, cop_task: {num: 1, max:4.462288ms, proc_keys: 11409, rpc_num: 1, rpc_time: 4.457148ms} | index:StreamAgg_9                                                 | 238 Bytes | N/A  |
|   └─StreamAgg_9             | 1.00    | 1       | cop[tikv] |                                           | time:4ms, loops:12                                                                                               | funcs:count(1)->Column#13                                         | N/A       | N/A  |
|     └─IndexRangeScan_16     | 8471.88 | 11409   | cop[tikv] | table:trips, index:start_date(start_date) | time:4ms, loops:12                                                                                               | range:[2017-07-01 00:00:00,2017-07-01 23:59:59], keep order:false | N/A       | N/A  |
+-----------------------------+---------+---------+-----------+-------------------------------------------+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+------+
4 rows in set (0.00 sec)
```

From the result above, the query time has reduced from 1.03 seconds to 0.0 seconds.

> **Note:**
>
> Another optimization that applies here is the coprocessor cache. If you are unable to add indexes, consider enabling the [coprocessor cache](/coprocessor-cache.md). When it is enabled, as long as the Region has not been modified since the operator is last executed, TiKV will return the value from the cache. This will also help reduce much of the cost of the expensive `TableFullScan` and `Selection` operators.
