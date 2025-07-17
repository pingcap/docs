---
title: HTAP 查询
summary: 介绍 TiDB 中的 HTAP 查询。
---

# HTAP 查询

HTAP 代表混合事务与分析处理（Hybrid Transactional and Analytical Processing）。传统上，数据库通常为事务场景或分析场景设计，因此数据平台常常需要拆分为事务处理（Transactional Processing）和分析处理（Analytical Processing），并将数据从事务数据库复制到分析数据库，以快速响应分析查询。TiDB 数据库可以同时执行事务和分析任务，这极大简化了数据平台的构建，并允许用户使用更新更快的数据进行分析。

TiDB 使用 TiKV，基于行的存储引擎，进行在线事务处理（OLTP）；同时使用 TiFlash，基于列的存储引擎，进行在线分析处理（OLAP）。行存储引擎和列存储引擎共存于 HTAP 中。两者都能自动复制数据并保持强一致性。行存储引擎优化 OLTP 性能，列存储引擎优化 OLAP 性能。

[创建表](/develop/dev-guide-create-table.md#use-htap-capabilities) 小节介绍了如何启用 TiDB 的 HTAP 功能。以下内容描述了如何利用 HTAP 更快地进行数据分析。

## 数据准备

在开始之前，你可以通过 [tiup demo 命令](/develop/dev-guide-bookshop-schema-design.md#method-1-via-tiup-demo) 导入更多示例数据。例如：

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --host 127.0.0.1 --port 4000 --drop-tables
```

或者，你也可以 [使用 TiDB Cloud 的导入功能](/develop/dev-guide-bookshop-schema-design.md#method-2-via-tidb-cloud-import) 导入预先准备好的示例数据。

## 窗口函数

在使用数据库时，除了存储数据和提供应用功能（如排序和评分图书）之外，你可能还需要在数据库中分析数据，以进行后续操作和决策。

[从单个表查询数据](/develop/dev-guide-get-data-from-single-table.md) 文档介绍了如何使用聚合查询对数据进行整体分析。在更复杂的场景中，你可能希望将多个聚合查询的结果合并成一个查询。如果你想了解某本书的历史订单金额趋势，可以对每个月的所有订单数据进行 `sum` 聚合，然后将这些 `sum` 结果合并，得到历史趋势。

为了方便此类分析，自 TiDB v3.0 起，TiDB 支持窗口函数。该函数为每一行数据提供跨多行访问数据的能力。不同于普通的聚合查询，窗口函数在聚合行时不会将结果集合并成单行。

与聚合函数类似，使用窗口函数时也需要遵循固定的语法：

```sql
SELECT
    window_function() OVER ([partition_clause] [order_clause] [frame_clause]) AS alias
FROM
    table_name
```

### `ORDER BY` 子句

利用聚合窗口函数 `sum()`，你可以分析某本书的历史订单金额趋势。例如：

```sql
WITH orders_group_by_month AS (
  SELECT DATE_FORMAT(ordered_at, '%Y-%c') AS month, COUNT(*) AS orders
  FROM orders
  WHERE book_id = 3461722937
  GROUP BY 1
)
SELECT
month,
SUM(orders) OVER(ORDER BY month ASC) as acc
FROM orders_group_by_month
ORDER BY month ASC;
```

`sum()` 函数会根据 `OVER` 子句中的 `ORDER BY` 指定的顺序累加数据。结果如下：

```
+---------+-------+
| month   | acc   |
+---------+-------+
| 2011-5  |     1 |
| 2011-8  |     2 |
| 2012-1  |     3 |
| 2012-2  |     4 |
| 2013-1  |     5 |
| 2013-3  |     6 |
| 2015-11 |     7 |
| 2015-4  |     8 |
| 2015-8  |     9 |
| 2017-11 |    10 |
| 2017-5  |    11 |
| 2019-5  |    13 |
| 2020-2  |    14 |
+---------+-------+
```

通过时间作为横轴、累计订单金额作为纵轴，用折线图可直观展示该书的历史订单趋势，坡度的变化反映了订单量的变化。

### `PARTITION BY` 子句

假设你想分析不同类型图书的历史订单趋势，并在同一折线图中显示多个系列。

你可以使用 `PARTITION BY` 子句，将图书按类型分组，分别统计每个类型的历史订单。

```sql
WITH orders_group_by_month AS (
    SELECT
        b.type AS book_type,
        DATE_FORMAT(ordered_at, '%Y-%c') AS month,
        COUNT(*) AS orders
    FROM orders o
    LEFT JOIN books b ON o.book_id = b.id
    WHERE b.type IS NOT NULL
    GROUP BY book_type, month
), acc AS (
    SELECT
        book_type,
        month,
        SUM(orders) OVER(PARTITION BY book_type ORDER BY book_type, month ASC) as acc
    FROM orders_group_by_month
    ORDER BY book_type, month ASC
)
SELECT * FROM acc;
```

结果示例：

```
+------------------------------+---------+------+
| book_type                    | month   | acc  |
+------------------------------+---------+------+
| Magazine                     | 2011-10 |    1 |
| Magazine                     | 2011-8  |    2 |
| Magazine                     | 2012-5  |    3 |
| Magazine                     | 2013-1  |    4 |
| Magazine                     | 2013-6  |    5 |
...
| Novel                        | 2011-3  |   13 |
| Novel                        | 2011-4  |   14 |
| Novel                        | 2011-6  |   15 |
| Novel                        | 2011-8  |   17 |
| Novel                        | 2012-1  |   18 |
| Novel                        | 2012-2  |   20 |
...
| Sports                       | 2021-4  |   49 |
| Sports                       | 2021-7  |   50 |
| Sports                       | 2022-4  |   51 |
+------------------------------+---------+------+
1500 rows in set (1.70 sec)
```

### 非聚合窗口函数

TiDB 还提供一些非聚合的 [窗口函数](/functions-and-operators/window-functions.md)，用于更丰富的分析。

例如，[分页查询](/develop/dev-guide-paginate-results.md) 文档介绍了如何使用 `row_number()` 函数实现高效分页批量处理。

## 混合工作负载

在使用 TiDB 进行实时在线分析处理（HTAP）场景下的混合负载时，你只需提供 TiDB 的入口点，TiDB 会根据具体业务自动选择不同的处理引擎。

### 创建 TiFlash 副本

TiDB 默认使用基于行的存储引擎 TiKV。若要使用列存储引擎 TiFlash，详见 [启用 HTAP 功能](/develop/dev-guide-create-table.md#use-htap-capabilities)。在通过 TiFlash 查询数据之前，需要为 `books` 和 `orders` 表创建 TiFlash 副本，使用以下语句：

```sql
ALTER TABLE books SET TIFLASH REPLICA 1;
ALTER TABLE orders SET TIFLASH REPLICA 1;
```

你可以用以下语句检查 TiFlash 副本的进度：

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'books';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'orders';
```

`PROGRESS` 列为 1 表示进度已达 100%，`AVAILABLE` 列为 1 表示副本当前可用。

```
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| bookshop     | books      |      143 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.07 sec)
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| bookshop     | orders     |      147 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.07 sec)
```

副本创建完成后，可以使用 `EXPLAIN` 语句检查上述窗口函数 [PARTITION BY 子句](#partition-by-clause) 的执行计划。如果在执行计划中出现 `cop[tiflash]`，表示 TiFlash 引擎已开始工作。

然后，再次执行 [PARTITION BY 子句](#partition-by-clause) 中的示例 SQL 语句，结果如下：

```
+------------------------------+---------+------+
| book_type                    | month   | acc  |
+------------------------------+---------+------+
| Magazine                     | 2011-10 |    1 |
| Magazine                     | 2011-8  |    2 |
| Magazine                     | 2012-5  |    3 |
| Magazine                     | 2013-1  |    4 |
| Magazine                     | 2013-6  |    5 |
...
| Novel                        | 2011-3  |   13 |
| Novel                        | 2011-4  |   14 |
| Novel                        | 2011-6  |   15 |
| Novel                        | 2011-8  |   17 |
| Novel                        | 2012-1  |   18 |
| Novel                        | 2012-2  |   20 |
...
| Sports                       | 2021-4  |   49 |
| Sports                       | 2021-7  |   50 |
| Sports                       | 2022-4  |   51 |
+------------------------------+---------+------+
1500 rows in set (0.79 sec)
```

通过对比两次执行结果，可以发现使用 TiFlash 后查询速度显著提升（数据量大的情况下提升更明显）。这是因为窗口函数通常依赖全表扫描某些列，而列存的 TiFlash 更适合处理此类分析任务。对于 TiKV，如果使用主键或索引减少查询行数，查询速度也会很快，且资源消耗少于 TiFlash。

### 指定查询引擎

TiDB 使用基于成本的优化器（CBO）根据成本估算自动选择是否使用 TiFlash 副本。但如果你确定查询是事务性还是分析性的，可以通过 [优化器提示](/optimizer-hints.md) 指定使用的查询引擎。

要在查询中指定使用的引擎，可以使用 `/*+ read_from_storage(engine_name[table_name]) */` 提示，如下所示。

> **注意：**
>
> - 如果表有别名，提示中应使用别名而非表名，否则提示无效。
> - `read_from_storage` 提示不支持 [公共表表达式](/develop/dev-guide-use-common-table-expression.md)。

```sql
WITH orders_group_by_month AS (
    SELECT
        /*+ read_from_storage(tikv[o]) */
        b.type AS book_type,
        DATE_FORMAT(ordered_at, '%Y-%c') AS month,
        COUNT(*) AS orders
    FROM orders o
    LEFT JOIN books b ON o.book_id = b.id
    WHERE b.type IS NOT NULL
    GROUP BY book_type, month
), acc AS (
    SELECT
        book_type,
        month,
        SUM(orders) OVER(PARTITION BY book_type ORDER BY book_type, month ASC) as acc
    FROM orders_group_by_month mo
    ORDER BY book_type, month ASC
)
SELECT * FROM acc;
```

你可以用 `EXPLAIN` 语句检查上述 SQL 的执行计划。如果在任务列中同时出现 `cop[tiflash]` 和 `cop[tikv]`，表示 TiFlash 和 TiKV 都在调度完成此查询。注意，TiFlash 和 TiKV 存储引擎通常使用不同的 TiDB 节点，因此两者的查询类型不会相互影响。

关于 TiDB 如何选择使用 TiFlash 的更多信息，请参见 [使用 TiDB 读取 TiFlash 副本](/tiflash/use-tidb-to-read-tiflash.md)。

## 阅读更多

<CustomContent platform="tidb">

- [TiDB HTAP 快速入门](/quick-start-with-htap.md)
- [探索 HTAP](/explore-htap.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [TiDB Cloud HTAP 快速入门](/tidb-cloud/tidb-cloud-htap-quickstart.md)

</CustomContent>

- [窗口函数](/functions-and-operators/window-functions.md)
- [使用 TiFlash](/tiflash/tiflash-overview.md#use-tiflash)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>