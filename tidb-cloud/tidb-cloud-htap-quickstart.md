---
title: TiDB Cloud HTAP 快速入门
summary: 了解如何在 TiDB Cloud 中开始使用 HTAP。
aliases: ['/tidbcloud/use-htap-cluster']
---

# TiDB Cloud HTAP 快速入门

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 指的是混合事务与分析处理。TiDB Cloud 中的 HTAP 集群由 [TiKV](https://tikv.org)（为事务处理设计的行存储引擎）和 [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)（为分析处理设计的列存储引擎）组成。你的应用数据首先存储在 TiKV 中，然后通过 Raft 共识算法实时同步到 TiFlash。因此，这是从行存储到列存储的实时复制。

本教程将引导你以简单的方式体验 TiDB Cloud 的混合事务与分析处理（HTAP）特性。内容包括如何将表复制到 TiFlash、如何使用 TiFlash 运行查询，以及如何体验性能提升。

## 开始之前

在体验 HTAP 特性之前，请按照 [TiDB Cloud 快速入门](/tidb-cloud/tidb-cloud-quickstart.md) 创建一个 TiDB Cloud Serverless 集群，并将 **Steam Game Stats** 示例数据集导入到该集群中。

## 操作步骤

### 步骤 1. 将示例数据复制到列存储引擎

创建包含 TiFlash 节点的集群后，TiKV 默认不会将数据复制到 TiFlash。你需要在 TiDB 的 MySQL 客户端中执行 DDL 语句，指定需要复制的表。之后，TiDB 会在 TiFlash 中相应地创建指定表的副本。

例如，要将（**Steam Game Stats** 示例数据集中的）`games` 表复制到 TiFlash，可以执行以下语句：

```sql
USE game;
```

```sql
ALTER TABLE games SET TIFLASH REPLICA 2;
```

要检查复制进度，可以执行以下语句：

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_ID, REPLICA_COUNT, LOCATION_LABELS, AVAILABLE, PROGRESS FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'game' and TABLE_NAME = 'games';
```

```sql
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| game         | games      |       88 |             2 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.20 sec)
```

在上述语句的结果中：

- `AVAILABLE` 表示指定表的 TiFlash 副本是否可用。`1` 表示可用，`0` 表示不可用。一旦副本变为可用，该状态不会再变化。
- `PROGRESS` 表示复制的进度。取值范围为 `0` 到 `1`。`1` 表示至少有一个副本已完成复制。

### 步骤 2. 使用 HTAP 查询数据

当复制过程完成后，你就可以开始运行一些查询了。

例如，你可以统计每年发布的游戏数量，以及平均价格和平均游玩时长：

```sql
SELECT
  YEAR(`release_date`) AS `release_year`,
  COUNT(*) AS `games_released`,
  AVG(`price`) AS `average_price`,
  AVG(`average_playtime_forever`) AS `average_playtime`
FROM
  `games`
GROUP BY
  `release_year`
ORDER BY
  `release_year` DESC;
```

### 步骤 3. 对比行存储与列存储的查询性能

在此步骤中，你可以对比 TiKV（行存储）和 TiFlash（列存储）的执行统计信息。

- 若要获取该查询在 TiKV 上的执行统计信息，执行以下语句：

    ```sql
    EXPLAIN ANALYZE SELECT /*+ READ_FROM_STORAGE(TIKV[games]) */
      YEAR(`release_date`) AS `release_year`,
      COUNT(*) AS `games_released`,
      AVG(`price`) AS `average_price`,
      AVG(`average_playtime_forever`) AS `average_playtime`
    FROM
      `games`
    GROUP BY
      `release_year`
    ORDER BY
      `release_year` DESC;
    ```

    对于拥有 TiFlash 副本的表，TiDB 优化器会根据成本估算自动决定使用 TiKV 还是 TiFlash 副本。在上述 `EXPLAIN ANALYZE` 语句中，`/*+ READ_FROM_STORAGE(TIKV[games]) */` hint 用于强制优化器选择 TiKV，这样你可以查看 TiKV 的执行统计信息。

    > **注意：**
    >
    > 5.7.7 之前的 MySQL 命令行客户端默认会去除优化器 hint。如果你在这些早期版本中使用 `Hint` 语法，启动客户端时请加上 `--comments` 选项。例如：`mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

    在输出结果中，你可以从 `execution info` 列获取执行时间。

    ```sql
    id                         | estRows  | actRows | task      | access object | execution info                             | operator info                                 | memory  | disk    
    ---------------------------+----------+---------+-----------+---------------+--------------------------------------------+-----------------------------------------------+---------+---------
    Sort_5                     | 4019.00  | 28      | root      |               | time:672.7ms, loops:2, RU:1159.679690      | Column#36:desc                                | 18.0 KB | 0 Bytes 
    └─Projection_7             | 4019.00  | 28      | root      |               | time:672.7ms, loops:6, Concurrency:5       | year(game.games.release_date)->Column#36, ... | 35.5 KB | N/A     
      └─HashAgg_15             | 4019.00  | 28      | root      |               | time:672.6ms, loops:6, partial_worker:...  | group by:Column#38, funcs:count(Column#39)... | 56.7 KB | N/A     
        └─TableReader_16       | 4019.00  | 28      | root      |               | time:672.4ms, loops:2, cop_task: {num:...  | data:HashAgg_9                                | 3.60 KB | N/A     
          └─HashAgg_9          | 4019.00  | 28      | cop[tikv] |               | tikv_task:{proc max:300ms, min:0s, avg...  | group by:year(game.games.release_date), ...   | N/A     | N/A     
            └─TableFullScan_14 | 68223.00 | 68223   | cop[tikv] | table:games   | tikv_task:{proc max:290ms, min:0s, avg...  | keep order:false                              | N/A     | N/A     
    (6 rows)
    ```

- 若要获取该查询在 TiFlash 上的执行统计信息，执行以下语句：

    ```sql
    EXPLAIN ANALYZE SELECT
      YEAR(`release_date`) AS `release_year`,
      COUNT(*) AS `games_released`,
      AVG(`price`) AS `average_price`,
      AVG(`average_playtime_forever`) AS `average_playtime`
    FROM
      `games`
    GROUP BY
      `release_year`
    ORDER BY
      `release_year` DESC;
    ```

    在输出结果中，你可以从 `execution info` 列获取执行时间。

    ```sql
    id                                   | estRows  | actRows | task         | access object | execution info                                        | operator info                              | memory  | disk    
    -------------------------------------+----------+---------+--------------+---------------+-------------------------------------------------------+--------------------------------------------+---------+---------
    Sort_5                               | 4019.00  | 28      | root         |               | time:222.2ms, loops:2, RU:25.609675                   | Column#36:desc                             | 3.77 KB | 0 Bytes 
    └─TableReader_39                     | 4019.00  | 28      | root         |               | time:222.1ms, loops:2, cop_task: {num: 2, max: 0s,... | MppVersion: 1, data:ExchangeSender_38      | 4.64 KB | N/A     
      └─ExchangeSender_38                | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | ExchangeType: PassThrough                  | N/A     | N/A     
        └─Projection_8                   | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | year(game.games.release_date)->Column#3... | N/A     | N/A     
          └─Projection_34                | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | Column#33, div(Column#34, cast(case(eq(... | N/A     | N/A     
            └─HashAgg_35                 | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | group by:Column#63, funcs:sum(Column#64... | N/A     | N/A     
              └─ExchangeReceiver_37      | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:8}       |                                            | N/A     | N/A     
                └─ExchangeSender_36      | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:210.6ms, loops:1, threads:1}       | ExchangeType: HashPartition, Compressio... | N/A     | N/A     
                  └─HashAgg_33           | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:210.6ms, loops:1, threads:1}       | group by:Column#75, funcs:count(1)->Col... | N/A     | N/A     
                    └─Projection_40      | 68223.00 | 68223   | mpp[tiflash] |               | tiflash_task:{time:210.6ms, loops:2, threads:8}       | game.games.price, game.games.price, gam... | N/A     | N/A     
                      └─TableFullScan_23 | 68223.00 | 68223   | mpp[tiflash] | table:games   | tiflash_task:{time:210.6ms, loops:2, threads:8}, ...  | keep order:false                           | N/A     | N/A     
    (11 rows)
    ```

> **注意：**
>
> 由于示例数据量较小，且本文档中的查询非常简单，如果你已经强制优化器选择 TiKV 并再次运行相同查询，TiKV 可能会复用其缓存，因此查询速度可能会更快。如果数据经常更新，则缓存会失效。

## 了解更多

- [TiFlash 概述](/tiflash/tiflash-overview.md)
- [创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)
- [从 TiFlash 读取数据](/tiflash/use-tidb-to-read-tiflash.md)
- [使用 MPP 模式](/tiflash/use-tiflash-mpp-mode.md)
- [支持下推的计算](/tiflash/tiflash-supported-pushdown-calculations.md)
