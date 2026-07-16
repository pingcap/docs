---
title: TiDB Cloud HTAP 快速入门
summary: 了解如何在 TiDB Cloud 中开始使用 HTAP。
aliases: ['/tidbcloud/use-htap-cluster']
---

# TiDB Cloud HTAP 快速入门

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 指的是混合事务与分析处理。TiDB Cloud 中的 HTAP 架构由 [TiKV](https://tikv.org)（为事务处理设计的行存储引擎）和 [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)（为分析处理设计的列式存储引擎）组成。你的应用数据首先存储在 TiKV 中，然后通过 Raft 共识算法实时同步到 TiFlash。因此，这是从行存储到列存储的实时同步。

本教程将引导你以简单的方式体验 TiDB Cloud 的混合事务与分析处理（HTAP）特性。内容包括如何将表同步到 TiFlash、如何使用 TiFlash 运行查询，以及如何体验性能提升。

## 开始之前

在尝试 HTAP 特性之前，请按照 [TiDB Cloud 快速入门](/tidb-cloud/tidb-cloud-quickstart.md) 创建一个 {{{ .starter }}} 实例，然后按如下步骤将你的数据（本文档以 **Steam Games Dataset 2021-2025** 为例）导入到该实例中：

1. 从 Kaggle 下载 [Steam Games Dataset 2021-2025](https://www.kaggle.com/datasets/jypenpen54534/steam-games-dataset-2021-2025-65k)。
2. 打开你的 {{{ .starter }}} 实例的 **Import** 页面。

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .starter }}} 实例的名称，进入其实例概览页面。
    2. 在概览页面中，点击左侧导航栏中的 **Data** > **Import**。

3. 将下载的 CSV 文件导入到你的 {{{ .starter }}} 实例中。

    1. 在 **Import** 页面中，点击 **Upload a local file**，然后选择并上传下载的 CSV 文件。
    2. 在 **Destination** 部分的 **Database** 字段中输入 `steam`，在 **Table** 字段中输入 `games`。
    3. 点击 **Define Table**，将 `categories` 列的数据类型改为 `TEXT`，然后将 `developer` 列的数据类型改为 `TEXT`。
    4. 点击 **Start Import**。

        你可以在 **Import Task Detail** 页面查看导入进度。

## 操作步骤

### 步骤 1. 将示例数据同步到列存储引擎

创建一个 {{{ .starter }}} 实例后，TiDB 默认不会将数据从 TiKV 同步到 TiFlash。要将目标表同步到 TiFlash，请使用 MySQL 客户端连接到你的 {{{ .starter }}} 实例并执行 DDL 语句。随后，TiDB 会在 TiFlash 中创建指定表的副本。

例如，要将（**Steam Games Dataset 2021-2025** 中的）`games` 表同步到 TiFlash，可以执行以下语句：

```sql
USE steam;
```

```sql
ALTER TABLE games SET TIFLASH REPLICA 2;
```

要检查同步进度，可以执行以下语句：

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_ID, REPLICA_COUNT, LOCATION_LABELS, AVAILABLE, PROGRESS FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'steam' AND TABLE_NAME = 'games';
```

```sql
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| steam        | games      |      227 |             2 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.24 sec)
```

在上述语句的结果中：

- `AVAILABLE` 表示指定表的 TiFlash 副本是否可用。`1` 表示可用，`0` 表示不可用。一旦副本变为可用，该状态不会再变化。
- `PROGRESS` 表示同步的进度。取值范围为 `0` 到 `1`。`1` 表示至少有一个副本已完成同步。

### 步骤 2. 使用 HTAP 查询数据

同步完成后，你可以运行查询。

例如，你可以统计每年发布的游戏数量，以及平均价格和平均推荐数：

```sql
SELECT
  `release_year`,
  COUNT(*) AS `games_released`,
  AVG(`price`) AS `average_price`,
  AVG(`recommendations`) AS `average_recommendations`
FROM
  `games`
WHERE
  `release_year` IS NOT NULL
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
      `release_year`,
      `genres`,
      `developer`,
      COUNT(*) AS `games_released`,
      SUM(`recommendations`) AS `total_recommendations`,
      AVG(`recommendations`) AS `average_recommendations`,
      AVG(`price`) AS `average_price`,
      MAX(`recommendations`) AS `max_recommendations`
    FROM
      `games`
    WHERE
      `release_year` IS NOT NULL
      AND `genres` IS NOT NULL
      AND `developer` IS NOT NULL
    GROUP BY
      `release_year`,
      `genres`,
      `developer`
    HAVING
      COUNT(*) >= 2
    ORDER BY
      `total_recommendations` DESC,
      `games_released` DESC
    LIMIT 20;
    ```

    对于拥有 TiFlash 副本的表，TiDB 优化器会根据成本估算自动决定使用 TiKV 还是 TiFlash 副本。在上述 `EXPLAIN ANALYZE` 语句中，`/*+ READ_FROM_STORAGE(TIKV[games]) */` hint 用于强制优化器选择 TiKV，这样你可以查看 TiKV 的执行统计信息。

    > **注意：**
    >
    > 5.7.7 之前的 MySQL 命令行客户端默认会去除优化器 hint。如果你在这些早期版本中使用 `Hint` 语法，启动客户端时请加上 `--comments` 选项。例如：`mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

    在输出结果中，你可以从 `execution info` 列获取执行时间。

    ```sql
    id                                | estRows  | actRows | task      | access object | execution info                              | operator info                              | memory   | disk
    ----------------------------------+----------+---------+-----------+---------------+---------------------------------------------+--------------------------------------------+----------+---------
    Projection_10                     | 20.00    | 20      | root      |               | time:234.4ms, loops:2, RU:241.66, ...       | steam.games.release_year, ...              | 6.03 KB  | N/A
    └─TopN_13                         | 20.00    | 20      | root      |               | time:234.4ms, loops:2                       | Column#13:desc, Column#12:desc, ...        | 12.6 KB  | 0 Bytes
      └─Selection_18                  | 36774.40 | 2458    | root      |               | time:233.9ms, loops:5                       | ge(Column#12, ?)                           | 187.0 KB | N/A
        └─HashAgg_22                  | 45968.00 | 59883   | root      |               | time:228.4ms, loops:62, partial_worker:...  | group by:Column#39, Column#40, ...         | 31.7 MB  | 0 Bytes
          └─Projection_38             | 65521.00 | 65521   | root      |               | time:142.9ms, loops:66, Concurrency:5       | cast(steam.games.recommendations, ...      | 1.16 MB  | N/A
            └─TableReader_32          | 65521.00 | 65521   | root      |               | time:49.5ms, loops:66, cop_task:{num:9...   | data:Selection_31                          | 3.26 MB  | N/A
              └─Selection_31          | 65521.00 | 65521   | cop[tikv] |               | tikv_task:{proc max:20ms, min:0s, ...       | not(isnull(steam.games.developer)), ...    | N/A      | N/A
                └─TableFullScan_30    | 65521.00 | 65521   | cop[tikv] | table:games   | tikv_task:{proc max:10ms, min:0s, ...       | keep order:false                           | N/A      | N/A
    (8 rows)
    ```

- 若要获取该查询在 TiFlash 上的执行统计信息，执行相同的语句，但不带 `/*+ READ_FROM_STORAGE(TIKV[games]) */` hint：

    ```sql
    EXPLAIN ANALYZE SELECT
      `release_year`,
      `genres`,
      `developer`,
      COUNT(*) AS `games_released`,
      SUM(`recommendations`) AS `total_recommendations`,
      AVG(`recommendations`) AS `average_recommendations`,
      AVG(`price`) AS `average_price`,
      MAX(`recommendations`) AS `max_recommendations`
    FROM
      `games`
    WHERE
      `release_year` IS NOT NULL
      AND `genres` IS NOT NULL
      AND `developer` IS NOT NULL
    GROUP BY
      `release_year`,
      `genres`,
      `developer`
    HAVING
      COUNT(*) >= 2
    ORDER BY
      `total_recommendations` DESC,
      `games_released` DESC
    LIMIT 20;
    ```

    在输出结果中，你可以从 `execution info` 列获取执行时间。

    ```sql
    id                                      | estRows  | actRows | task         | access object | execution info                              | operator info                              | memory  | disk
    ----------------------------------------+----------+---------+--------------+---------------+---------------------------------------------+--------------------------------------------+---------+---------
    Projection_10                           | 20.00    | 20      | root         |               | time:92.5ms, loops:2, RU:120.42, ...        | steam.games.release_year, ...              | 6.03 KB | N/A
    └─TopN_14                               | 20.00    | 20      | root         |               | time:92.4ms, loops:2                        | Column#13:desc, Column#12:desc, ...        | 4.32 KB | 0 Bytes
      └─TableReader_68                      | 20.00    | 20      | root         |               | time:92.4ms, loops:2, cop_task:{num:2...    | MppVersion: 2, data:ExchangeSender_67      | 7.99 KB | N/A
        └─ExchangeSender_67                 | 20.00    | 20      | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | ExchangeType: PassThrough                  | N/A     | N/A
          └─TopN_66                         | 20.00    | 20      | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | Column#13:desc, Column#12:desc, ...        | N/A     | N/A
            └─Selection_65                  | 36774.40 | 2458    | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | ge(Column#12, ?)                           | N/A     | N/A
              └─Projection_58               | 45968.00 | 59883   | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | Column#12, Column#13, div(Column#14, ...   | N/A     | N/A
                └─HashAgg_56                | 45968.00 | 59883   | mpp[tiflash] |               | tiflash_task:{time:71ms, loops:1, ...       | group by:Column#79, Column#80, ...         | N/A     | N/A
                  └─Projection_71           | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:31ms, loops:7, ...       | cast(steam.games.recommendations, ...      | N/A     | N/A
                    └─ExchangeReceiver_41   | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:31ms, loops:7, ...       |                                            | N/A     | N/A
                      └─ExchangeSender_40   | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:31.2ms, loops:7, ...     | ExchangeType: HashPartition, ...           | N/A     | N/A
                        └─Selection_39      | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:21.2ms, loops:7, ...     | not(isnull(steam.games.developer)), ...    | N/A     | N/A
                          └─TableFullScan_38| 65521.00 | 65521   | mpp[tiflash] | table:games   | tiflash_task:{time:21.2ms, loops:7, ...     | pushed down filter:empty, keep order:false | N/A     | N/A
    (13 rows)
    ```

> **注意：**
>
> 由于示例数据集较小，且本文档中的查询相对简单，如果你强制优化器为该查询选择 TiKV，然后再次运行相同的查询，TiKV 会复用其缓存，从而使查询速度更快。如果数据经常更新，则缓存会失效。

## 了解更多

- [TiFlash 概述](/tiflash/tiflash-overview.md)
- [创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)
- [从 TiFlash 读取数据](/tiflash/use-tidb-to-read-tiflash.md)
- [使用 MPP 模式](/tiflash/use-tiflash-mpp-mode.md)
- [支持下推的计算](/tiflash/tiflash-supported-pushdown-calculations.md)
