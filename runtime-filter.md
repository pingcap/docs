---
title: Runtime Filter
summary: 了解 Runtime Filter 的工作原理及其使用方法。
---

# Runtime Filter

Runtime Filter 是在 TiDB v7.3 中引入的一项新功能，旨在提升在 MPP 场景下的 hash join 性能。通过在运行时动态生成过滤器，提前过滤 hash join 的数据，TiDB 可以减少扫描的数据量和 hash join 的计算量，最终提升查询性能。

## 概念

- Hash join：一种实现关系代数连接的方法。它通过在一侧构建哈希表，并在另一侧不断匹配哈希表来获得连接结果。
- Build side：hash join 中用来构建哈希表的一侧。在本文档中，默认将 hash join 的右表称为 build side。
- Probe side：hash join 中用来持续匹配哈希表的一侧。在本文档中，默认将 hash join 的左表称为 probe side。
- Filter：也称为 predicate，指本文档中的过滤条件。

## Runtime Filter 的工作原理

Hash join 通过在右表（build side）建立哈希表，并用左表（probe side）不断探测哈希表来执行连接操作。如果在探测过程中某些连接键值无法命中哈希表，意味着这些数据在右表中不存在，不会出现在最终的连接结果中。因此，如果 TiDB 能在扫描阶段**提前过滤掉连接键数据**，就能减少扫描时间和网络开销，从而大幅提升连接效率。

Runtime Filter 是在查询计划阶段生成的**动态谓词**。该谓词具有与 TiDB 选择操作符中的其他谓词相同的功能。这些谓词都应用于 Table Scan 操作，用于过滤不符合条件的行。唯一的区别在于，Runtime Filter 中的参数值来自于 hash join 构建过程中生成的结果。

### 示例

假设存在一个 `store_sales` 表与 `date_dim` 表的连接查询，连接方式为 hash join。`store_sales` 是主要存储门店销售数据的事实表，行数为 100 万。`date_dim` 是时间维度表，主要存储日期信息。你希望查询 2001 年的销售数据，因此在连接操作中涉及 `date_dim` 表的 365 行数据。

```sql
SELECT * FROM store_sales, date_dim
WHERE ss_date_sk = d_date_sk
    AND d_year = 2001;
```

hash join 的执行计划通常如下：

```
                 +-------------------+
                 | PhysicalHashJoin  |
        +------->|                   |<------+
        |        +-------------------+       |
        |                                    |
        |                                    |
  100w  |                                    | 365
        |                                    |
        |                                    |
+-------+-------+                   +--------+-------+
| TableFullScan |                   | TableFullScan  |
|  store_sales  |                   |    date_dim    |
+---------------+                   +----------------+
```

*(上述图省略了 exchange 节点及其他节点)*

Runtime Filter 的执行流程如下：

1. 扫描 `date_dim` 表的数据。
2. `PhysicalHashJoin` 根据 build side 的数据计算过滤条件，例如 `date_dim in (2001/01/01~2001/12/31)`。
3. 将过滤条件传递给等待扫描 `store_sales` 的 `TableFullScan` 操作符。
4. 过滤条件应用于 `store_sales`，过滤后数据传递给 `PhysicalHashJoin`，从而减少 probe side 扫描的数据量和匹配哈希表的计算量。

```
                         2. 构建 RF 值
            +-------->+-------------------+
            |         |PhysicalHashJoin   |<-----+
            |    +----+                   |      |
4. 生成 RF |    |    +-------------------+      | 1. 扫描 T2
    5000    |    |3. 传递 RF                     |      365
            |    | 过滤数据                       |
            |    |                               |
      +-----+----v------+                +-------+--------+
      |  TableFullScan  |                | TableFullScan  |
      |  store_sales    |                |    date_dim    |
      +-----------------+                +----------------+
```

*(RF 为 Runtime Filter 的缩写)*

从上图可以看出，`store_sales` 扫描的数据量由 100 万减少到 5000。通过减少 `TableFullScan` 扫描的数据量，Runtime Filter 可以降低匹配哈希表的次数，避免不必要的 I/O 和网络传输，从而显著提升连接操作的效率。

## 使用 Runtime Filter

要使用 Runtime Filter，你需要为表创建 TiFlash 副本，并将 [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) 设置为 `LOCAL`。

以 TPC-DS 数据集为例，本节使用 `catalog_sales` 表和 `date_dim` 表的连接操作，说明 Runtime Filter 如何提升查询效率。

### 步骤 1. 为待连接的表创建 TiFlash 副本

为 `catalog_sales` 表和 `date_dim` 表添加 TiFlash 副本。

```sql
ALTER TABLE catalog_sales SET tiflash REPLICA 1;
ALTER TABLE date_dim SET tiflash REPLICA 1;
```

等待两个表的 TiFlash 副本准备就绪，即其 `AVAILABLE` 和 `PROGRESS` 字段均为 `1`。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA WHERE TABLE_NAME='catalog_sales';
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME    | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | catalog_sales |     1055 |             1 |                 |         1 |        1 |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+

SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA WHERE TABLE_NAME='date_dim';
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | date_dim   |     1015 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
```

### 步骤 2. 开启 Runtime Filter

将系统变量 [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) 设置为 `LOCAL`。

```sql
SET tidb_runtime_filter_mode="LOCAL";
```

确认设置成功：

```sql
SHOW VARIABLES LIKE "tidb_runtime_filter_mode";
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| tidb_runtime_filter_mode | LOCAL |
+--------------------------+-------+
```

如果值为 `LOCAL`，说明 Runtime Filter 已开启。

### 步骤 3. 执行查询

在执行查询前，使用 [`EXPLAIN` 语句](/sql-statements/sql-statement-explain.md) 查看执行计划，确认 Runtime Filter 是否生效。

```sql
EXPLAIN SELECT cs_ship_date_sk FROM catalog_sales, date_dim
WHERE d_date = '2002-2-01' AND
     cs_ship_date_sk = d_date_sk;
```

当 Runtime Filter 生效时，会在 `HashJoin` 节点和 `TableScan` 节点挂载对应的 Runtime Filter，表示过滤器已成功应用。

```
TableFullScan: runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk
HashJoin: runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk |
```

完整的执行计划如下：

```
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| id                                     | estRows     | task         | access object       | operator info                                                                                                                                 |
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| TableReader_53                         | 37343.19    | root         |                     | MppVersion: 1, data:ExchangeSender_52                                                                                                         |
| └─ExchangeSender_52                    | 37343.19    | mpp[tiflash] |                     | ExchangeType: PassThrough                                                                                                                     |
|   └─Projection_51                      | 37343.19    | mpp[tiflash] |                     | tpcds50.catalog_sales.cs_ship_date_sk                                                                                                         |
|     └─HashJoin_48                      | 37343.19    | mpp[tiflash] |                     | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)], runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk |
|       ├─ExchangeReceiver_29(Build)     | 1.00        | mpp[tiflash] |                     |                                                                                                                                               |
|       │ └─ExchangeSender_28            | 1.00        | mpp[tiflash] |                     | ExchangeType: Broadcast, Compression: FAST                                                                                                    |
|       │   └─TableFullScan_26           | 1.00        | mpp[tiflash] | table:date_dim      | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false                                                  |
|       └─Selection_31(Probe)            | 71638034.00 | mpp[tiflash] |                     | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                                                                            |
|         └─TableFullScan_30             | 71997669.00 | mpp[tiflash] | table:catalog_sales | pushed down filter:empty, keep order:false, runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk                                     |
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
9 rows in set (0.01 sec)
```

执行查询，Runtime Filter 已应用。

```sql
SELECT cs_ship_date_sk FROM catalog_sales, date_dim
WHERE d_date = '2002-2-01' AND
     cs_ship_date_sk = d_date_sk;
```

### 步骤 4. 性能对比

本例使用 50 GB 的 TPC-DS 数据。开启 Runtime Filter 后，查询时间由 0.38 秒缩短至 0.17 秒，效率提升约 50%。你可以使用 `ANALYZE` 语句查看 Runtime Filter 生效后各操作符的执行时间。

未开启 Runtime Filter 时的执行信息如下：

```sql
EXPLAIN ANALYZE SELECT cs_ship_date_sk FROM catalog_sales, date_dim WHERE d_date = '2002-2-01' AND cs_ship_date_sk = d_date_sk;
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
| id                                     | estRows     | actRows  | task         | access object       | execution info                                                                                                                                                                                                                                                                                                                                                                                    | operator info                                                                                | memory  | disk |
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
| TableReader_53                         | 37343.19    | 59574    | root         |                     | time:379.7ms, loops:83, RU:0.000000, cop_task: {num: 48, max: 0s, min: 0s, avg: 0s, p95: 0s, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                                                          | MppVersion: 1, data:ExchangeSender_52                                                        | 12.0 KB | N/A  |
| └─ExchangeSender_52                    | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | ExchangeType: PassThrough                                                                    | N/A     | N/A  |
|   └─Projection_51                      | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | tpcds50.catalog_sales.cs_ship_date_sk                                                        | N/A     | N/A  |
|     └─HashJoin_48                      | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)]    | N/A     | N/A  |
|       ├─ExchangeReceiver_29(Build)     | 1.00        | 2        | mpp[tiflash] |                     | tiflash_task:{proc max:291.3ms, min:290ms, avg: 290.6ms, p80:291.3ms, p95:291.3ms, iters:2, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  |                                                                                              | N/A     | N/A  |
|       │ └─ExchangeSender_28            | 1.00        | 1        | mpp[tiflash] |                     | tiflash_task:{proc max:290.9ms, min:0s, avg: 145.4ms, p80:290.9ms, p95:290.9ms, iters:1, tasks:2, threads:1}                                                                                                                                                                                                                                                                                      | ExchangeType: Broadcast, Compression: FAST                                                   | N/A     | N/A  |
|       │   └─TableFullScan_26           | 1.00        | 1        | mpp[tiflash] | table:date_dim      | tiflash_task:{proc max:3.88ms, min:0s, avg: 1.94ms, p80:3.88ms, p95:3.88ms, iters:1, tasks:2, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:2, total_skipped_packs:12, total_scanned_rows:16384, total_skipped_rows:97625, total_rs_index_load_time: 0ms, total_read_time: 0ms}, total_create_snapshot_time: 0ms, total_local_region_num: 1, total_remote_region_num: 0}                     | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false | N/A     | N/A  |
|       └─Selection_31(Probe)            | 71638034.00 | 71638034 | mpp[tiflash] |                     | tiflash_task:{proc max:47ms, min:34.3ms, avg: 40.6ms, p80:47ms, p95:47ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                        | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                           | N/A     | N/A  |
|         └─TableFullScan_30             | 71997669.00 | 71997669 | mpp[tiflash] | table:catalog_sales | tiflash_task:{proc max:34ms, min:17.3ms, avg: 25.6ms, p80:34ms, p95:34ms, iters:1160, tasks:2, threads:16}, tiflash_scan:{dtfile:{total_scanned_packs:8893, total_skipped_packs:4007, total_scanned_rows:72056474, total_skipped_rows:32476901, total_rs_index_load_time: 8ms, total_read_time: 579ms}, total_create_snapshot_time: 0ms, total_local_region_num: 194, total_remote_region_num: 0} | pushed down filter:empty, keep order:false                                                   | N/A     | N/A  |
+----------------------------------------+-------------+----------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
9 rows in set (0.38 sec)
```

对比两次查询的执行信息，可以发现以下改进：

* IO 减少：通过比较 `TableFullScan` 操作符的 `total_scanned_rows`，可以看到开启 Runtime Filter 后，扫描量减少了三分之二。
* Hash join 性能提升：`HashJoin` 操作符的执行时间由 376.1 ms 降至 157.6 ms。

### 最佳实践

Runtime Filter 适用于大表与小表连接的场景，例如事实表与维度表的连接查询。当维度表的命中数据较少时，意味着过滤值较少，因此可以更有效地过滤掉不符合条件的数据。相比默认扫描整个事实表的方式，这可以显著提升查询性能。

以 TPC-DS 中 `Sales` 表与 `date_dim` 表的连接操作为典型示例。

## 配置 Runtime Filter

在使用 Runtime Filter 时，可以配置 Runtime Filter 的模式和谓词类型。

### Runtime Filter 模式

Runtime Filter 的模式是**过滤器发送端操作符**与**过滤器接收端操作符**之间的关系。共有三种模式：`OFF`、`LOCAL` 和 `GLOBAL`。在 v7.3.0 版本中，仅支持 `OFF` 和 `LOCAL` 模式。Runtime Filter 的模式由系统变量 [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) 控制。

- `OFF`：关闭 Runtime Filter。关闭后，查询行为与之前版本相同。
- `LOCAL`：启用本地模式的 Runtime Filter。在本地模式下，**过滤器发送端操作符**和**过滤器接收端操作符**处于同一 MPP 任务中。换句话说，Runtime Filter 可应用于 HashJoin 和 TableScan 在同一任务中的场景。目前，Runtime Filter 仅支持本地模式。要启用此模式，将其设置为 `LOCAL`。
- `GLOBAL`：目前不支持全局模式，不能将 Runtime Filter 设置为此模式。

### Runtime Filter 类型

Runtime Filter 的类型是由生成的 Filter 操作符所使用的谓词类型。目前仅支持一种类型：`IN`，表示生成的谓词类似于 `k1 in (xxx)`。Runtime Filter 的类型由系统变量 [`tidb_runtime_filter_type`](/system-variables.md#tidb_runtime_filter_type-new-in-v720) 控制。

- `IN`：默认类型。表示生成的 Runtime Filter 使用 `IN` 类型的谓词。

## 限制

- Runtime Filter 是在 MPP 架构中的一种优化，只能应用于推送到 TiFlash 的查询。
- 连接类型：左外连接、全外连接和 Anti 连接（左表为 probe side）不支持 Runtime Filter。因为 Runtime Filter 会提前过滤连接涉及的数据，前述类型的连接不会丢弃不匹配的数据，因此不能使用 Runtime Filter。
- 相等连接表达式：当等值连接表达式中的 probe 列为复杂表达式，或 probe 列类型为 JSON、Blob、Array 或其他复杂数据类型时，不会生成 Runtime Filter。主要原因是上述类型的列很少作为连接列使用，即使生成了过滤器，过滤率也通常较低。

对于上述限制，如果你需要确认 Runtime Filter 是否正确生成，可以使用 [`EXPLAIN` 语句](/sql-statements/sql-statement-explain.md) 来验证执行计划。