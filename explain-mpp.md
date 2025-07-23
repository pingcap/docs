---
title: 解释在 MPP 模式下的 Statements
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 解释在 MPP 模式下的 Statements

TiDB 支持使用 [MPP mode](/tiflash/use-tiflash-mpp-mode.md) 来执行查询。在 MPP 模式下，TiDB 优化器为 MPP 生成执行计划。注意，MPP 模式仅适用于在 [TiFlash](/tiflash/tiflash-overview.md) 上具有副本的表。

本文中的示例基于以下样例数据：

```sql
CREATE TABLE t1 (id int, value int);
INSERT INTO t1 values(1,2),(2,3),(1,3);
ALTER TABLE t1 set tiflash replica 1;
ANALYZE TABLE t1;
SET tidb_allow_mpp = 1;
```

## MPP 查询片段与 MPP 任务

在 MPP 模式下，一个查询在逻辑上被切分成多个查询片段。以以下语句为例：

```sql
EXPLAIN SELECT COUNT(*) FROM t1 GROUP BY id;
```

该查询在 MPP 模式下被划分为两个片段：一个用于第一阶段的聚合，另一个用于第二阶段的聚合（也是最终的聚合）。当执行此查询时，每个查询片段会被实例化为一个或多个 MPP 任务。

## Exchange 操作符

`ExchangeReceiver` 和 `ExchangeSender` 是专门用于 MPP 执行计划的两个交换操作符。`ExchangeReceiver` 从下游查询片段读取数据，`ExchangeSender` 将数据从下游查询片段发送到上游查询片段。在 MPP 模式下，每个 MPP 查询片段的根操作符是 `ExchangeSender`，意味着查询片段由 `ExchangeSender` 操作符界定。

以下是一个简单的 MPP 执行计划示例：

```sql
EXPLAIN SELECT COUNT(*) FROM t1 GROUP BY id;
```

```sql
+------------------------------------+---------+-------------------+---------------+----------------------------------------------------+
| id                                 | estRows | task              | access object | operator info                                      |
+------------------------------------+---------+-------------------+---------------+----------------------------------------------------+
| TableReader_31                     | 2.00    | root              |               | data:ExchangeSender_30                             |
| └─ExchangeSender_30                | 2.00    | batchCop[tiflash] |               | ExchangeType: PassThrough                          |
|   └─Projection_26                  | 2.00    | batchCop[tiflash] |               | Column#4                                           |
|     └─HashAgg_27                   | 2.00    | batchCop[tiflash] |               | group by:test.t1.id, funcs:sum(Column#7)->Column#4 |
|       └─ExchangeReceiver_29        | 2.00    | batchCop[tiflash] |               |                                                    |
|         └─ExchangeSender_28        | 2.00    | batchCop[tiflash] |               | ExchangeType: HashPartition, Hash Cols: test.t1.id |
|           └─HashAgg_9              | 2.00    | batchCop[tiflash] |               | group by:test.t1.id, funcs:count(1)->Column#7      |
|             └─TableFullScan_25     | 3.00    | batchCop[tiflash] | table:t1      | keep order:false                                   |
+------------------------------------+---------+-------------------+---------------+----------------------------------------------------+
```

上述执行计划包含两个查询片段：

* 第一个为 `[TableFullScan_25, HashAgg_9, ExchangeSender_28]`，主要负责第一阶段的聚合。
* 第二个为 `[ExchangeReceiver_29, HashAgg_27, Projection_26, ExchangeSender_30]`，主要负责第二阶段的聚合。

`ExchangeSender` 操作符的 `operator info` 列显示了交换类型信息。目前有三种交换类型，见下：

* HashPartition：`ExchangeSender` 操作符首先根据 Hash 值对数据进行分区，然后将数据分发到上游 MPP 任务的 `ExchangeReceiver`。此交换类型常用于 Hash 聚合和 Shuffle Hash Join 算法。
* Broadcast：`ExchangeSender` 操作符通过广播将数据分发到上游 MPP 任务。此交换类型常用于 Broadcast Join。
* PassThrough：`ExchangeSender` 操作符将数据发送到唯一的上游 MPP 任务，与 Broadcast 类型不同。此交换类型常用于返回数据给 TiDB。

在示例执行计划中，`ExchangeSender_28` 的交换类型为 HashPartition，意味着它执行 Hash 聚合算法；`ExchangeSender_30` 的交换类型为 PassThrough，意味着它用于将数据返回给 TiDB。

MPP 也常用于连接操作。TiDB 中的 MPP 模式支持以下两种连接算法：

* Shuffle Hash Join：使用 HashPartition 交换类型对连接操作的输入数据进行洗牌，然后上游 MPP 任务在相同分区内进行连接。
* Broadcast Join：将连接操作中的小表数据广播到每个节点，然后每个节点分别进行连接。

以下是 Shuffle Hash Join 的典型执行计划示例：

```sql
SET tidb_broadcast_join_threshold_count=0;
SET tidb_broadcast_join_threshold_size=0;
EXPLAIN SELECT COUNT(*) FROM t1 a JOIN t1 b ON a.id = b.id;
```

```sql
+----------------------------------------+---------+--------------+---------------+----------------------------------------------------+
| id                                     | estRows | task         | access object | operator info                                      |
+----------------------------------------+---------+--------------+---------------+----------------------------------------------------+
| StreamAgg_14                           | 1.00    | root         |               | funcs:count(1)->Column#7                           |
| └─TableReader_48                       | 9.00    | root         |               | data:ExchangeSender_47                             |
|   └─ExchangeSender_47                  | 9.00    | cop[tiflash] |               | ExchangeType: PassThrough                          |
|     └─HashJoin_44                      | 9.00    | cop[tiflash] |               | inner join, equal:[eq(test.t1.id, test.t1.id)]     |
|       ├─ExchangeReceiver_19(Build)     | 6.00    | cop[tiflash] |               |                                                    |
|       │ └─ExchangeSender_18            | 6.00    | cop[tiflash] |               | ExchangeType: HashPartition, Hash Cols: test.t1.id |
|       │   └─Selection_17               | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                            |
|       │     └─TableFullScan_16         | 6.00    | cop[tiflash] | table:a       | keep order:false                                   |
|       └─ExchangeReceiver_23(Probe)     | 6.00    | cop[tiflash] |               |                                                    |
|         └─ExchangeSender_22            | 6.00    | cop[tiflash] |               | ExchangeType: HashPartition, Hash Cols: test.t1.id |
|           └─Selection_21               | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                            |
|             └─TableFullScan_20         | 6.00    | cop[tiflash] | table:b       | keep order:false                                   |
+----------------------------------------+---------+--------------+---------------+----------------------------------------------------+
12 rows in set (0.00 sec)
```

在上述执行计划中：

* 查询片段 `[TableFullScan_20, Selection_21, ExchangeSender_22]` 从表 b 读取数据并将数据洗牌到上游 MPP 任务。
* 查询片段 `[TableFullScan_16, Selection_17, ExchangeSender_18]` 从表 a 读取数据并将数据洗牌到上游 MPP 任务。
* 查询片段 `[ExchangeReceiver_19, ExchangeReceiver_23, HashJoin_44, ExchangeSender_47]` 将所有数据连接后返回给 TiDB。

一个典型的 Broadcast Join 执行计划如下：

```sql
EXPLAIN SELECT COUNT(*) FROM t1 a JOIN t1 b ON a.id = b.id;
```

```sql
+----------------------------------------+---------+--------------+---------------+------------------------------------------------+
| id                                     | estRows | task         | access object | operator info                                  |
+----------------------------------------+---------+--------------+---------------+------------------------------------------------+
| StreamAgg_15                           | 1.00    | root         |               | funcs:count(1)->Column#7                       |
| └─TableReader_47                       | 9.00    | root         |               | data:ExchangeSender_46                         |
|   └─ExchangeSender_46                  | 9.00    | cop[tiflash] |               | ExchangeType: PassThrough                      |
|     └─HashJoin_43                      | 9.00    | cop[tiflash] |               | inner join, equal:[eq(test.t1.id, test.t1.id)] |
|       ├─ExchangeReceiver_20(Build)     | 6.00    | cop[tiflash] |               |                                                |
|       │ └─ExchangeSender_19            | 6.00    | cop[tiflash] |               | ExchangeType: Broadcast                        |
|       │   └─Selection_18               | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                        |
|       │     └─TableFullScan_17         | 6.00    | cop[tiflash] | table:a       | keep order:false                               |
|       └─Selection_22(Probe)            | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                        |
|         └─TableFullScan_21             | 6.00    | cop[tiflash] | table:b       | keep order:false                               |
+----------------------------------------+---------+--------------+---------------+------------------------------------------------+
```

在上述执行计划中：

* 查询片段 `[TableFullScan_17, Selection_18, ExchangeSender_19]` 从小表（表 a）读取数据，并将数据广播到每个包含大表（表 b）数据的节点。
* 查询片段 `[TableFullScan_21, Selection_22, ExchangeReceiver_20, HashJoin_43, ExchangeSender_46]` 将所有数据连接后返回给 TiDB。

## `EXPLAIN ANALYZE` 在 MPP 模式下的 Statements

`EXPLAIN ANALYZE` 语句类似于 `EXPLAIN`，但会输出一些运行时信息。

以下是一个简单的 `EXPLAIN ANALYZE` 示例的输出：

```sql
EXPLAIN ANALYZE SELECT COUNT(*) FROM t1 GROUP BY id;
```

```sql
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
| id                                 | estRows | actRows | task              | access object | execution info                                                                                    | operator info                                                  | memory | disk |
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
| TableReader_31                     | 4.00    | 2       | root              |               | time:44.5ms, loops:2, cop_task: {num: 1, max: 0s, proc_keys: 0, copr_cache_hit_ratio: 0.00}       | data:ExchangeSender_30                                         | N/A    | N/A  |
| └─ExchangeSender_30                | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                                    | ExchangeType: PassThrough, tasks: [2, 3, 4]                    | N/A    | N/A  |
|   └─Projection_26                  | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                                    | Column#4                                                       | N/A    | N/A  |
|     └─HashAgg_27                   | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                                    | group by:test.t1.id, funcs:sum(Column#7)->Column#4             | N/A    | N/A  |
|       └─ExchangeReceiver_29        | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:14.5ms, loops:1, threads:20}                                                   |                                                                | N/A    | N/A  |
|         └─ExchangeSender_28        | 4.00    | 0       | batchCop[tiflash] |               | tiflash_task:{time:9.49ms, loops:0, threads:0}                                                    | ExchangeType: HashPartition, Hash Cols: test.t1.id, tasks: [1] | N/A    | N/A  |
|           └─HashAgg_9              | 4.00    | 0       | batchCop[tiflash] |               | tiflash_task:{time:9.49ms, loops:0, threads:0}                                                    | group by:test.t1.id, funcs:count(1)->Column#7                  | N/A    | N/A  |
|             └─TableFullScan_25     | 6.00    | 0       | batchCop[tiflash] | table:t1      | tiflash_task:{time:9.49ms, loops:0, threads:0}, tiflash_scan:{dtfile:{total_scanned_packs:1,...}} | keep order:false                                               | N/A    | N/A  |
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
```

与 `EXPLAIN` 的输出相比，`operator info` 列中的 `ExchangeSender` 还显示了 `tasks`，记录了查询片段实例化的 MPP 任务的编号。此外，每个 MPP 操作符在 `execution info` 列中还包含 `threads` 字段，记录了 TiDB 执行此操作符时的并发数。如果集群由多个节点组成，此并发数为所有节点并发数的总和。

## MPP 版本与交换数据压缩

从 v6.6.0 版本开始，`MPP` 执行计划中新增字段 `MPPVersion` 和 `Compression`。

- `MppVersion`：MPP 执行计划的版本号，可通过系统变量 [`mpp_version`](/system-variables.md#mpp_version-new-in-v660) 设置。
- `Compression`：`Exchange` 操作符的数据压缩模式，可通过系统变量 [`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-new-in-v660) 设置。如果未启用数据压缩，则在执行计划中不显示此字段。

示例如下：

```sql
mysql > EXPLAIN SELECT COUNT(*) AS count_order FROM lineitem GROUP BY l_returnflag, l_linestatus ORDER BY l_returnflag, l_linestatus;

+----------------------------------------+--------------+--------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                                     | estRows      | task         | access object  | operator info                                                                                                                                                                                                                                                                        |
+----------------------------------------+--------------+--------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Projection_6                           | 3.00         | root         |                | Column#18                                                                                                                                                                                                                                                                            |
| └─Sort_8                              | 3.00         | root         |                | tpch100.lineitem.l_returnflag, tpch100.lineitem.l_linestatus                                                                                                                                                                                                                         |
|   └─TableReader_36                     | 3.00         | root         |                | MppVersion: 1, data:ExchangeSender_35                                                                                                                                                                                                                                                |
|     └─ExchangeSender_35                | 3.00         | mpp[tiflash] |                | ExchangeType: PassThrough                                                                                                                                                                                                                                                            |
|       └─Projection_31                  | 3.00         | mpp[tiflash] |                | Column#18, tpch100.lineitem.l_returnflag, tpch100.lineitem.l_linestatus                                                                                                                                                                                                              |
|         └─HashAgg_32                   | 3.00         | mpp[tiflash] |                | group by:tpch100.lineitem.l_linestatus, tpch100.lineitem.l_returnflag, funcs:sum(Column#23)->Column#18, funcs:firstrow(tpch100.lineitem.l_returnflag)->tpch100.lineitem.l_returnflag, funcs:firstrow(tpch100.lineitem.l_linestatus)->tpch100.lineitem.l_linestatus, stream_count: 20 |
|           └─ExchangeReceiver_34        | 3.00         | mpp[tiflash] |                | stream_count: 20                                                                                                                                                                                                                                                                     |
|             └─ExchangeSender_33        | 3.00         | mpp[tiflash] |                | ExchangeType: HashPartition, Compression: FAST, Hash Cols: [name: tpch100.lineitem.l_returnflag, collate: utf8mb4_bin], [name: tpch100.lineitem.l_linestatus, collate: utf8mb4_bin], stream_count: 20                                                                                |
|               └─HashAgg_14             | 3.00         | mpp[tiflash] |                | group by:tpch100.lineitem.l_linestatus, tpch100.lineitem.l_returnflag, funcs:count(1)->Column#23                                                                                                                                                                                     |
|                 └─TableFullScan_30     | 600037902.00 | mpp[tiflash] | table:lineitem | keep order:false                                                                                                                                                                                                                                                                     |
+----------------------------------------+--------------+--------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

在上述执行计划结果中，TiDB 使用版本 `1` 的 MPP 执行计划构建 `TableReader`。`HashPartition` 类型的 `ExchangeSender` 操作符使用了 `FAST` 数据压缩模式，而 `PassThrough` 类型的 `ExchangeSender` 则未启用数据压缩。