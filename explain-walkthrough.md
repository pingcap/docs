---
title: EXPLAIN Walkthrough 
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
aliases: ['/docs/dev/query-execution-plan/','/docs/dev/reference/performance/understanding-the-query-execution-plan/','/docs/dev/index-merge/','/docs/dev/reference/performance/index-merge/','/tidb/dev/index-merge']
---

# EXPLAIN Walkthrough

Because SQL is a declarative language, it is not possible to sight-check a query and tell if it is executing efficiently. We must first [use `EXPLAIN`](/explain-overview.md) to understand what the current execution plan is.

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

Working from the child operator `└─TableFullScan_18` back, we can see that this query is currently suboptimal:

1. The coprocessor (TiKV) is reading the entire trips table, as a `TableFullScan`. It then passes the rows that it reads to `Selection_19`, still within TiKV.
2. The `WHERE start_date BETWEEN ..` predicate is then filtered in the `Selection_19` operator. It is estimated that approximately `250` rows will meet this selection. Note that this number was produced from a heuristic; the `└─TableFullScan_18` operator shows `stats:pseudo`. After running `ANALYZE TABLE trips` the statistics should be more accurate.
3. The rows that met the selection criteria then have a `count` function applied to them. This is also completed inside the `StreamAgg_9` operator, which is still inside TiKV (`cop[tikv]`). The TiKV coprocessor understands a number of MySQL built-in functions, `count` being one of them. It also understands that `count` is safe to apply Stream Aggregation to, even though the results are not in order.
4. The results from `StreamAgg_9` are then sent to `TableReader_21` which is now inside the TiDB server (task of `root`). The `estRows` does not make it entirely clear, but the `TableReader_21` operator will receive one row from each of the TiKV regions that had to be accessed. We can see more information about these requests in `EXPLAIN ANALYZE`. For a general view of the regions a table contains, [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) is also helpful:

  {{< copyable "sql" >}}
  
  ```sql
  SHOW TABLE trips REGIONS;
  ```

  ```sql
  +-----------+-----------------+-----------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY       | END_KEY         | LEADER_ID | LEADER_STORE_ID | PEERS | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+-----------------+-----------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
|       110 | t_51_           | t_51_r_704776   |       111 |               1 | 111   |          0 |             0 |          0 |                  135 |           705334 |
|        62 | t_51_r_704776   | t_51_r_1154568  |        63 |               1 | 63    |          0 |             0 |          0 |                   80 |           376894 |
|        52 | t_51_r_1154568  | t_51_r_1839484  |        53 |               1 | 53    |          0 |             0 |          0 |                  116 |           694346 |
|        50 | t_51_r_1839484  | t_51_r_1902684  |        51 |               1 | 51    |          0 |             0 |          0 |                   12 |            79863 |
|       188 | t_51_r_1902684  | t_51_r_2518439  |       189 |               1 | 189   |          0 |             0 |          0 |                   98 |           631896 |
|        82 | t_51_r_2518439  | t_51_r_2881555  |        83 |               1 | 83    |          0 |             0 |          0 |                   58 |           350944 |
|        54 | t_51_r_2881555  | t_51_r_3791926  |        55 |               1 | 55    |          0 |             0 |          0 |                  141 |           910371 |
|        80 | t_51_r_3791926  | t_51_r_3816442  |        81 |               1 | 81    |          0 |             0 |          0 |                    1 |             3830 |
|        56 | t_51_r_3816442  | t_51_r_3824381  |        57 |               1 | 57    |          0 |             0 |          0 |                   61 |           369785 |
|       112 | t_51_r_3824381  | t_51_r_4554633  |       113 |               1 | 113   |          0 |             0 |          0 |                  113 |           731346 |
|        64 | t_51_r_4554633  | t_51_r_5246251  |        65 |               1 | 65    |          0 |             0 |          0 |                  112 |           721705 |
|        58 | t_51_r_5246251  | t_51_r_5260563  |        59 |               1 | 59    |          0 |             0 |          0 |                    1 |             3001 |
|        92 | t_51_r_5260563  | t_51_r_5951474  |        93 |               1 | 93    |          0 |             0 |          0 |                  116 |           676704 |
|        70 | t_51_r_5951474  | t_51_r_6434265  |        71 |               1 | 71    |          0 |             0 |          0 |                   78 |           448956 |
|        72 | t_51_r_6434265  | t_51_r_6685804  |        73 |               1 | 73    |          0 |             0 |          0 |                   66 |           232429 |
|        74 | t_51_r_6685804  | t_51_r_6937298  |        75 |               1 | 75    |          0 |             0 |          0 |                   40 |           258390 |
|        76 | t_51_r_6937298  | t_51_r_7256843  |        77 |               1 | 77    |          0 |             0 |          0 |                   51 |           330897 |
|        66 | t_51_r_7256843  | t_51_r_7621128  |        67 |               1 | 67    |          0 |             0 |          0 |                   63 |           300860 |
|        68 | t_51_r_7621128  | t_51_r_8096904  |        69 |               1 | 69    |          0 |             0 |          0 |                  119 |           489758 |
|        84 | t_51_r_8096904  | t_51_r_8497748  |        85 |               1 | 85    |          0 |             0 |          0 |                  127 |           608278 |
|        86 | t_51_r_8497748  | t_51_r_8749107  |        87 |               1 | 87    |          0 |             0 |          0 |                   43 |           258184 |
|        88 | t_51_r_8749107  | t_51_r_9000869  |        89 |               1 | 89    |          0 |             0 |          0 |                   91 |           562195 |
|        90 | t_51_r_9000869  | t_51_r_9252632  |        91 |               1 | 91    |          0 |             0 |          0 |                  106 |           509818 |
|        94 | t_51_r_9252632  | t_51_r_9564595  |        95 |               1 | 95    |          0 |             0 |          0 |                   61 |           385556 |
|        96 | t_51_r_9564595  | t_51_r_9815441  |        97 |               1 | 97    |          0 |             0 |          0 |                   37 |           243881 |
|        98 | t_51_r_9815441  | t_51_r_10065966 |        99 |               1 | 99    |          0 |             0 |          0 |                   38 |           246647 |
|       102 | t_51_r_10065966 | t_51_r_10568331 |       103 |               1 | 103   |          0 |             0 |          0 |                   82 |           517591 |
|       104 | t_51_r_10568331 | t_51_r_10820702 |       105 |               1 | 105   |          0 |             0 |          0 |                   37 |           243639 |
|       106 | t_51_r_10820702 | t_51_r_11212812 |       107 |               1 | 107   |          0 |             0 |          0 |                   60 |           387558 |
|       108 | t_51_r_11212812 | t_51_r_11465062 |       109 |               1 | 109   |          0 |             0 |          0 |                   87 |           404936 |
|       182 | t_51_r_11465062 | t_51_r_12038387 |       185 |               1 | 185   |          0 |             0 |          0 |                   91 |           571625 |
|       114 | t_51_r_12038387 | t_51_r_12297594 |       115 |               1 | 115   |          0 |             0 |          0 |                   40 |           264038 |
|       183 | t_51_r_12297594 | t_51_r_12546883 |       184 |               1 | 184   |          0 |             0 |          0 |                   37 |           241845 |
|       116 | t_51_r_12546883 | t_51_r_12802161 |       117 |               1 | 117   |          0 |             0 |          0 |                   40 |           264954 |
|       186 | t_51_r_12802161 | t_51_r_13049012 |       187 |               1 | 187   |          0 |             0 |          0 |                   49 |           212905 |
|       118 | t_51_r_13049012 | t_51_r_13307901 |       119 |               1 | 119   |          0 |             0 |          0 |                   51 |           330909 |
|       122 | t_51_r_13307901 | t_51_r_13553188 |       123 |               1 | 123   |          0 |             0 |          0 |                   34 |           217729 |
|       190 | t_51_r_13553188 | t_51_r_13919113 |       191 |               1 | 191   |          0 |             0 |          0 |                   62 |           402596 |
|       192 | t_51_r_13919113 | t_51_r_14170587 |       193 |               1 | 193   |          0 |             0 |          0 |                   83 |           514516 |
|       194 | t_51_r_14170587 | t_51_r_14466819 |       195 |               1 | 195   |          0 |             0 |          0 |                   40 |           258893 |
|       196 | t_51_r_14466819 | t_51_r_14716282 |       197 |               1 | 197   |          0 |             0 |          0 |                   72 |           275276 |
|       198 | t_51_r_14716282 | t_51_r_15208331 |       199 |               1 | 199   |          0 |             0 |          0 |                   76 |           492049 |
|       200 | t_51_r_15208331 | t_51_r_15570436 |       201 |               1 | 201   |          0 |             0 |          0 |                   54 |           348130 |
|       202 | t_51_r_15570436 | t_51_r_15821866 |       203 |               1 | 203   |          0 |             0 |          0 |                   63 |           392444 |
|       204 | t_51_r_15821866 | t_51_r_16216719 |       205 |               1 | 205   |          0 |             0 |          0 |                   86 |           364254 |
|       206 | t_51_r_16216719 | t_51_r_16610992 |       207 |               1 | 207   |          0 |             0 |          0 |                   62 |           403069 |
|       208 | t_51_r_16610992 | t_51_r_16863445 |       209 |               1 | 209   |          0 |             0 |          0 |                   79 |           487553 |
|       210 | t_51_r_16863445 | t_51_r_17117332 |       211 |               1 | 211   |          0 |             0 |          0 |                   42 |           119784 |
|       214 | t_51_r_17117332 | t_51_r_17424612 |       215 |               1 | 215   |          0 |             0 |          0 |                   56 |           314847 |
|       216 | t_51_r_17424612 | t_51_r_17674333 |       217 |               1 | 217   |          0 |             0 |          0 |                   40 |           256769 |
|       218 | t_51_r_17674333 | t_51_r_17924393 |       219 |               1 | 219   |          0 |             0 |          0 |                   76 |           245536 |
|       220 | t_51_r_17924393 | t_51_r_18263777 |       221 |               1 | 221   |          0 |             0 |          0 |                   62 |           352413 |
|       222 | t_51_r_18263777 | t_51_r_18515551 |       223 |               1 | 223   |          0 |             0 |          0 |                   52 |           246384 |
|       224 | t_51_r_18515551 | t_51_r_18766909 |       225 |               1 | 225   |          0 |             0 |          0 |                   65 |           247324 |
|       226 | t_51_r_18766909 | t_51_r_19018621 |       227 |               1 | 227   |          0 |             0 |          0 |                  112 |           329047 |
|         2 | t_51_r_19018621 |                 |         3 |               1 | 3     |          0 |             0 |          0 |                   46 |           156542 |
+-----------+-----------------+-----------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
56 rows in set (0.01 sec)

  ```
5. The `StreamAgg_20` operator then has the task of applying a count function to each of the rows from the `└─TableReader_21` operator, which we can see from the `SHOW TABLE REGIONS` output above, will be about 56 rows. As this is the root operator, it can then return results to the client.

## Assessing the current performance

`EXPLAIN` only returns the query execution plan, and does not execute the query. We can either run the query, or use `EXPLAIN ANALYZE` to get the actual execution time:

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

Importantly, we can also see some of the useful columns that `EXPLAIN ANALYZE` has added. `actRows` shows that some of our estimates were off. We knew this already because the `└─TableFullScan_18` showed `stats:pseudo`. But expecting 10 thousand rows and finding 19 million rows does not show that the estimate was very accurate. If we run `ANALYZE TABLE`, and then `EXPLAIN ANALYZE` again we can see that the estimates are much closer:

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

After `ANALYZE TABLE` is executed, we can see that the estimated rows for the `└─TableFullScan_18` is accurate, and the estimate for `└─Selection_19` is now also much closer. While in this case the execution plan (i.e. the set of operators TiDB uses to execute this query) has not changed in between running `ANALYZE TABLE`, quite frequently sub-optimal plans are caused by out of date statistics.

As well as `ANALYZE TABLE`, TiDB will automatically regenerate statistics as a background operation after a [threshold is reached](/system-variables.md#tidb_auto_analyze_ratio). You can see how close TiDB is to this threshold (i.e. how healthy it considers the statistics to be) with the statement `SHOW STATS_HEALTHY`:

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

With the index added we can then repeat the query in `EXPLAIN`. In the following output, we can see that a new execution plan is chosen, and the `TableFullScan` and `Selection` operators have been eliminated:

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

To compare the actual execution time, we can again use `EXPLAIN ANALYZE`:


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

The query time has reduced from 1.03 seconds to 0.0 seconds. Not bad!

> **Tip:**
>
> Another optimization that applies here is the coprocessor cache. If you are unable to add indexes, consider enabling the [coprocessor cache](/coprocessor-cache.md). When enabled, as long as the region has not been modified since the operator was last executed, TiKV will return the value from cache. This will also help reduce much of the expense of the expensive `TableFullScan` and `Selection` operators.
