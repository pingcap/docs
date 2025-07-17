---
title: EXPLAIN Walkthrough
summary: 通过示例语句学习如何使用 EXPLAIN
---

# `EXPLAIN` Walkthrough

由于 SQL 是一种声明式语言，你无法自动判断一个查询是否高效执行。你必须先使用 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 语句来了解当前的执行计划。

<CustomContent platform="tidb">

以下语句来自 [bikeshare example database](/import-example-data.md)，统计 2017 年 7 月 1 日的出行次数：

</CustomContent>

<CustomContent platform="tidb-cloud">

以下语句来自 [bikeshare example database](/tidb-cloud/import-sample-data.md)，统计 2017 年 7 月 1 日的出行次数：

</CustomContent>


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

从子操作符 `└─TableFullScan_18` 返回，你可以看到其执行过程如下，目前还不够理想：

1. 协程（TiKV）以 `TableFullScan` 操作读取整个 `trips` 表，然后将读取到的行传递给 `Selection_19` 操作符，仍在 TiKV 内部。
2. `WHERE start_date BETWEEN ..` 条件在 `Selection_19` 操作符中进行过滤。估算符合条件的行数大约为 `250` 行。注意，这个数字是根据统计信息和操作符的逻辑估算得出。`└─TableFullScan_18` 操作符显示 `stats:pseudo`，意味着该表没有实际的统计信息。运行 `ANALYZE TABLE trips` 收集统计信息后，统计数据会更准确。
3. 满足筛选条件的行随后会应用 `count` 函数。这也在 `StreamAgg_9` 操作符中完成，仍在 TiKV（`cop[tikv]`）内部。TiKV 的协程可以执行许多 MySQL 内置函数，`count` 就是其中之一。
4. `StreamAgg_9` 的结果随后传递给 `TableReader_21` 操作符，该操作符现在在 TiDB 服务器（`root`）内部。此操作符的 `estRows` 值为 `1`，意味着它会从每个 TiKV Region 接收一行数据。关于这些请求的更多信息，请参见 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)。
5. `StreamAgg_20` 操作符对来自 `└─TableReader_21` 操作符的每一行应用 `count` 函数，从 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) 可以看到大约有 56 行。由于这是根操作符，它会将结果返回给客户端。

> **Note:**
>
> 若要查看表包含的 Regions 的整体情况，可以执行 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)。

## 评估当前性能

`EXPLAIN` 只返回查询的执行计划，不会执行查询。若要获得实际的执行时间，可以直接执行查询或使用 `EXPLAIN ANALYZE`：


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

上述示例查询耗时 1.03 秒，性能尚不理想。

从 `EXPLAIN ANALYZE` 的结果可以看出，`actRows` 表示部分估算（`estRows`）不准确（预期 1 万行，实际找到 1900 万行），这在 `└─TableFullScan_18` 的 `operator info`（`stats:pseudo`）中已提示。如果先运行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)，再执行 `EXPLAIN ANALYZE`，可以看到估算值更接近实际：


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

执行 `ANALYZE TABLE` 后，可以看到 `└─TableFullScan_18` 的估算行数变得准确，`└─Selection_19` 的估算也更接近实际。在上述两种情况下，虽然执行计划（TiDB 用于执行此查询的操作符集合）没有变化，但过时的统计信息常常会导致次优的执行计划。

除了 `ANALYZE TABLE`，TiDB 还会在达到 [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) 阈值后，自动在后台重新生成统计信息。你可以通过执行 [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md) 来查看 TiDB 对统计信息的健康程度：


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

## 识别优化点

当前执行计划在以下方面是高效的：

* 大部分工作由 TiKV 协程内部处理。只需 56 行数据通过网络传回 TiDB 进行处理。每一行都很短，只包含符合条件的计数。
* 在 TiDB（`StreamAgg_20`）和 TiKV（`└─StreamAgg_9`）中对行数进行聚合，采用流式聚合，内存使用非常高效。

当前执行计划的最大问题在于条件 `start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'` 并未立即应用。所有行首先通过 `TableFullScan` 读取，然后再进行筛选。你可以通过 `SHOW CREATE TABLE trips` 的输出找到原因：


```sql
SHOW CREATE TABLE trips\G
```

```sql
*************************** 1. row ***************************
       Table: trips
Create Table: CREATE TABLE `trips` (
  `trip_id` bigint NOT NULL AUTO_INCREMENT,
  `duration` int NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `start_station_number` int DEFAULT NULL,
  `start_station` varchar(255) DEFAULT NULL,
  `end_station_number` int DEFAULT NULL,
  `end_station` varchar(255) DEFAULT NULL,
  `bike_number` varchar(255) DEFAULT NULL,
  `member_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`trip_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=20477318
1 row in set (0.00 sec)
```

在 `start_date` 上没有索引。你需要添加索引，将此条件推入索引读取操作符。可以如下添加索引：


```sql
ALTER TABLE trips ADD INDEX (start_date);
```

```sql
Query OK, 0 rows affected (2 min 10.23 sec)
```

> **Note:**
>
> 你可以使用 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 命令监控 DDL 任务的进度。TiDB 中的默认设置经过精心设计，添加索引不会对生产环境的工作负载造成太大影响。对于测试环境，可以考虑增加 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size) 和 [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt) 的值。在参考系统中，批次大小为 `10240`，工作线程数为 `32`，可以比默认值提升 10 倍的性能。

添加索引后，可以再次在 `EXPLAIN` 中执行该查询。以下输出显示，已选择新的执行计划，`TableFullScan` 和 `Selection` 操作符已被消除：


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

为了比较实际的执行时间，你可以再次使用 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)：


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

从上面的结果可以看出，查询耗时已从 1.03 秒缩短到 0.0 秒。

> **Note:**
>
> 这里的另一个优化点是协程缓存（coprocessor cache）。如果你无法添加索引，可以考虑启用 [coprocessor cache](/coprocessor-cache.md)。启用后，只要 Region 自上次操作后未被修改，TiKV 就会返回缓存中的值。这也有助于减少昂贵的 `TableFullScan` 和 `Selection` 操作符的成本。

## 禁用子查询的提前执行

在查询优化过程中，TiDB 会预先执行可以直接计算的子查询。例如：

```sql
CREATE TABLE t1(a int);
INSERT INTO t1 VALUES(1);
CREATE TABLE t2(a int);
EXPLAIN SELECT * FROM t2 WHERE a = (SELECT a FROM t1);
```

```sql
+--------------------------+----------+-----------+---------------+--------------------------------+
| id                       | estRows  | task      | access object | operator info                  |
+--------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_14           | 10.00    | root      |               | data:Selection_13              |
| └─Selection_13           | 10.00    | cop[tikv] |               | eq(test.t2.a, 1)               |
|   └─TableFullScan_12     | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo |
+--------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

在上述示例中，子查询 `a = (SELECT a FROM t1)` 在优化阶段被计算，并重写为 `t2.a=1`。这允许在优化过程中进行常量传播和折叠等优化。然而，这会影响 `EXPLAIN` 语句的执行时间。当子查询本身执行时间较长时，`EXPLAIN` 可能无法完成，从而影响线上排查。

从 v7.3.0 版本开始，TiDB 引入了 [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) 系统变量，用于控制是否禁用 `EXPLAIN` 中此类子查询的预执行。该变量的默认值为 `OFF`，表示会预先计算子查询。你可以将其设置为 `ON` 来禁用子查询的预执行：


```sql
SET @@tidb_opt_enable_non_eval_scalar_subquery = ON;
EXPLAIN SELECT * FROM t2 WHERE a = (SELECT a FROM t1);
```

```sql
+---------------------------+----------+-----------+---------------+---------------------------------+
| id                        | estRows  | task      | access object | operator info                   |
+---------------------------+----------+-----------+---------------+---------------------------------+
| Selection_13              | 8000.00  | root      |               | eq(test.t2.a, ScalarQueryCol#5) |
| └─TableReader_15          | 10000.00 | root      |               | data:TableFullScan_14           |
|   └─TableFullScan_14      | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo  |
| ScalarSubQuery_10         | N/A      | root      |               | Output: ScalarQueryCol#5        |
| └─MaxOneRow_6             | 1.00     | root      |               |                                 |
|   └─TableReader_9         | 1.00     | root      |               | data:TableFullScan_8            |
|     └─TableFullScan_8     | 1.00     | cop[tikv] | table:t1      | keep order:false, stats:pseudo  |
+---------------------------+----------+-----------+---------------+---------------------------------+
7 rows in set (0.00 sec)
```

可以看到，标量子查询在执行过程中没有展开，这样更容易理解此类 SQL 的具体执行流程。

> **Note:**
>
> [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) 仅影响 `EXPLAIN` 语句的行为，`EXPLAIN ANALYZE` 仍会提前执行子查询。