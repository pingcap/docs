---
title: 创建二级索引
summary: 了解创建二级索引的步骤、规则和示例。
---

# 创建二级索引

本文档介绍了如何使用 SQL 及各种编程语言创建二级索引，并列出了索引创建的规则。以 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用为例，带你了解二级索引的创建步骤。

## 在开始之前

在创建二级索引之前，请完成以下操作：

- [构建一个 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读 [Schema 设计概述](/develop/dev-guide-schema-design-overview.md)。
- [创建数据库](/develop/dev-guide-create-database.md)。
- [创建表](/develop/dev-guide-create-table.md)。

## 什么是二级索引

二级索引是 TiDB 集群中的一个逻辑对象。你可以简单地将其视为 TiDB 用于提升查询性能的一种排序类型的数据。在 TiDB 中，创建二级索引是一个在线操作，不会阻塞对表的任何数据读写操作。对于每个索引，TiDB 会为表中的每一行创建引用，并按所选列进行排序，而不是直接对数据排序。

<CustomContent platform="tidb">

关于二级索引的更多信息，参见 [Secondary Indexes](/best-practices/tidb-best-practices.md#secondary-index)。

</CustomContent>

<CustomContent platform="tidb-cloud">

关于二级索引的更多信息，参见 [Secondary Indexes](https://docs.pingcap.com/tidb/stable/tidb-best-practices#secondary-index)。

</CustomContent>

在 TiDB 中，你可以选择 [为现有表添加二级索引](#add-a-secondary-index-to-an-existing-table)，或在 [创建新表时同时创建二级索引](#create-a-secondary-index-when-creating-a-new-table)。

## 为现有表添加二级索引

要为现有表添加二级索引，可以使用 [CREATE INDEX](/sql-statements/sql-statement-create-index.md) 语句，示例如下：

```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

参数说明：

- `{index_name}`：二级索引的名称。
- `{table_name}`：表名。
- `{column_names}`：要索引的列名，多个列名用半角逗号分隔。

## 在创建新表时同时创建二级索引

在创建表的同时支持创建二级索引，可以在 [CREATE TABLE](/sql-statements/sql-statement-create-table.md) 语句的末尾添加包含 `KEY` 关键字的子句：

```sql
KEY `{index_name}` (`{column_names}`)
```

参数说明：

- `{index_name}`：二级索引的名称。
- `{column_names}`：要索引的列名，多个列名用半角逗号分隔。

## 二级索引创建规则

请参阅 [索引最佳实践](/develop/dev-guide-index-best-practice.md)。

## 示例

假设你希望 `bookshop` 应用支持 **搜索某一年出版的所有书籍**。

`books` 表中的字段如下：

| 字段名       | 类型          | 字段描述                                                          |
|--------------|---------------|------------------------------------------------------------------|
| id           | bigint(20)    | 书籍的唯一 ID                                                    |
| title        | varchar(100)  | 书名                                                             |
| type         | enum          | 书籍类型（例如杂志、动画、教学辅助等）                            |
| stock        | bigint(20)    | 库存                                                             |
| price        | decimal(15,2) | 价格                                                             |
| published_at | datetime      | 出版日期                                                         |

`books` 表的创建 SQL 语句如下：

```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

为了支持按年份搜索的功能，你需要编写一条 SQL 语句，**搜索某一年出版的所有书籍**。以 2022 年为例，SQL 语句如下：

```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

你可以使用 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 语句查看该 SQL 的执行计划。

```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

以下是执行计划的示例输出：

```
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                            |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| TableReader_7           | 346.32   | root      |               | data:Selection_6                                                                                                         |
| └─Selection_6           | 346.32   | cop[tikv] |               | ge(bookshop.books.published_at, 2022-01-01 00:00:00.000000), lt(bookshop.books.published_at, 2023-01-01 00:00:00.000000) |
|   └─TableFullScan_5     | 20000.00 | cop[tikv] | table:books   | keep order:false                                                                                                         |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.61 sec)
```

在输出中，**TableFullScan** 出现在 `id` 列，表示 TiDB 计划对 `books` 表进行全表扫描。然而，对于大量数据的表，全表扫描可能会非常缓慢，带来严重影响。

为了避免这种影响，可以为 `published_at` 列在 `books` 表中添加索引，示例如下：

```sql
CREATE INDEX `idx_book_published_at` ON `bookshop`.`books` (`bookshop`.`books`.`published_at`);
```

添加索引后，再次执行 `EXPLAIN` 语句，查看执行计划。

示例输出如下：

```
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| id                            | estRows | task      | access object                                          | operator info                                                     |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| IndexLookUp_10                | 146.01  | root      |                                                        |                                                                   |
| ├─IndexRangeScan_8(Build)     | 146.01  | cop[tikv] | table:books, index:idx_book_published_at(published_at) | range:[2022-01-01 00:00:00,2023-01-01 00:00:00), keep order:false |
| └─TableRowIDScan_9(Probe)     | 146.01  | cop[tikv] | table:books                                            | keep order:false                                                  |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
3 rows in set (0.18 sec)
```

在输出中，显示了 **IndexRangeScan**，而非 **TableFullScan**，表示 TiDB 已经准备好使用索引进行此查询。

执行计划中的 **TableFullScan** 和 **IndexRangeScan** 等词是 TiDB 中的 [operators](/explain-overview.md#operator-overview)。关于执行计划和操作符的更多信息，参见 [TiDB 查询执行计划概述](/explain-overview.md)。

<CustomContent platform="tidb">

执行计划每次返回的操作符可能不同。这是因为 TiDB 使用了 **Cost-Based Optimization (CBO)** 方法，执行计划依赖于规则和数据分布。关于 TiDB SQL 性能的更多信息，参见 [SQL 调优概述](/sql-tuning-overview.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

执行计划每次返回的操作符可能不同。这是因为 TiDB 使用了 **Cost-Based Optimization (CBO)** 方法，执行计划依赖于规则和数据分布。关于 TiDB SQL 性能的更多信息，参见 [SQL 调优概述](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)。

</CustomContent>

> **Note:**
>
> TiDB 也支持在查询时显式使用索引，你可以使用 [Optimizer Hints](/optimizer-hints.md) 或 [SQL Plan Management (SPM)](/sql-plan-management.md) 来人为控制索引的使用。但如果你对索引、优化器提示或 SPM 不太了解，**不要**使用此功能，以避免出现意外结果。

要查询表上的索引，可以使用 [SHOW INDEXES](/sql-statements/sql-statement-show-indexes.md) 语句：

```sql
SHOW INDEXES FROM `bookshop`.`books`;
```

示例输出如下：

```
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name              | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| books |          0 | PRIMARY               |            1 | id           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
| books |          1 | idx_book_published_at |            1 | published_at | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | NO        |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
```

## 下一步

在创建数据库、添加表和二级索引之后，你可以开始为应用添加 [写入](/develop/dev-guide-insert-data.md) 和 [读取](/develop/dev-guide-get-data-from-single-table.md) 功能。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>