---
title: SQL 性能调优
summary: 介绍 TiDB 的 SQL 性能调优方案和分析方法。
---

# SQL 性能调优

本文档介绍一些导致 SQL 语句变慢的常见原因以及调优 SQL 性能的技巧。

## 在开始之前

你可以使用 [`tiup demo` import](/develop/dev-guide-bookshop-schema-design.md#method-1-via-tiup-demo) 来准备数据：

```shell
tiup demo bookshop prepare --host 127.0.0.1 --port 4000 --books 1000000
```

或者 [使用 TiDB Cloud 的 Import 功能](/develop/dev-guide-bookshop-schema-design.md#method-2-via-tidb-cloud-import) 导入预先准备好的示例数据。

## 问题：全表扫描

导致 SQL 查询变慢的最常见原因是 `SELECT` 语句执行了全表扫描或使用了不正确的索引。

当 TiDB 根据非主键列或二级索引中的列，从一个大型表中检索少量行时，性能通常较差：

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+------------+-------------+-----------------------+---------------------+-------+--------+
| id         | title       | type                  | published_at        | stock | price  |
+------------+-------------+-----------------------+---------------------+-------+--------+
| 65670536   | Marian Yost | Arts                  | 1950-04-09 06:28:58 | 542   | 435.01 |
| 1164070689 | Marian Yost | Education & Reference | 1916-05-27 12:15:35 | 216   | 328.18 |
| 1414277591 | Marian Yost | Arts                  | 1932-06-15 09:18:14 | 303   | 496.52 |
| 2305318593 | Marian Yost | Arts                  | 2000-08-15 19:40:58 | 398   | 402.90 |
| 2638226326 | Marian Yost | Sports                | 1952-04-02 12:40:37 | 191   | 174.64 |
+------------+-------------+-----------------------+---------------------+-------+--------+
5 rows in set
Time: 0.582s
```

要理解为何此查询较慢，可以使用 `EXPLAIN` 查看执行计划：

```sql
EXPLAIN SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------+------------+-----------+---------------+-----------------------------------------+
| id                  | estRows    | task      | access object | operator info                           |
+---------------------+------------+-----------+---------------+-----------------------------------------+
| TableReader_7       | 1.27       | root      |               | data:Selection_6                        |
| └─Selection_6       | 1.27       | cop[tikv] |               | eq(bookshop.books.title, "Marian Yost") |
|   └─TableFullScan_5 | 1000000.00 | cop[tikv] | table:books   | keep order:false                        |
+---------------------+------------+-----------+---------------+-----------------------------------------+
```

从执行计划中的 `TableFullScan_5` 可以看出，TiDB 对 `books` 表执行了全表扫描，并逐行检查 `title` 是否满足条件。`TableFullScan_5` 的 `estRows` 值为 `1000000.00`，意味着优化器估算此全表扫描会扫描 100 万行数据。

关于 `EXPLAIN` 的更多用法信息，请参见 [`EXPLAIN` Walkthrough](/explain-walkthrough.md)。

### 解决方案：使用二级索引

为了加快上述查询的速度，可以在 `books.title` 列上添加二级索引：

```sql
CREATE INDEX title_idx ON books (title);
```

查询的执行速度会明显提升：

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+------------+-------------+-----------------------+---------------------+-------+--------+
| id         | title       | type                  | published_at        | stock | price  |
+------------+-------------+-----------------------+---------------------+-------+--------+
| 1164070689 | Marian Yost | Education & Reference | 1916-05-27 12:15:35 | 216   | 328.18 |
| 1414277591 | Marian Yost | Arts                  | 1932-06-15 09:18:14 | 303   | 496.52 |
| 2305318593 | Marian Yost | Arts                  | 2000-08-15 19:40:58 | 398   | 402.90 |
| 2638226326 | Marian Yost | Sports                | 1952-04-02 12:40:37 | 191   | 174.64 |
| 65670536   | Marian Yost | Arts                  | 1950-04-09 06:28:58 | 542   | 435.01 |
+------------+-------------+-----------------------+---------------------+-------+--------+
5 rows in set
Time: 0.007s
```

为了理解性能提升的原因，可以用 `EXPLAIN` 查看新的执行计划：

```sql
EXPLAIN SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| id                        | estRows | task      | access object                       | operator info                                         |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| IndexLookUp_10            | 1.27    | root      |                                     |                                                       |
| ├─IndexRangeScan_8(Build) | 1.27    | cop[tikv] | table:books, index:title_idx(title) | range:["Marian Yost","Marian Yost"], keep order:false |
| └─TableRowIDScan_9(Probe) | 1.27    | cop[tikv] | table:books                         | keep order:false                                      |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
```

从执行计划中的 `IndexLookUp_10` 可以看出，TiDB 通过 `title_idx` 索引进行数据查询。其 `estRows` 为 `1.27`，意味着优化器估算只会扫描大约 1.27 行数据。相比全表扫描的 100 万行，显著减少了扫描行数。

`IndexLookup_10` 的执行流程是：先通过 `IndexRangeScan_8` 操作读取满足条件的索引数据，然后通过存储在索引中的 Row ID，使用 `TableLookup_9` 操作查询对应的行。

关于 TiDB 执行计划的更多信息，请参见 [TiDB Query Execution Plan Overview](/explain-overview.md)。

### 解决方案：使用覆盖索引

如果索引是覆盖索引，且包含所有 SQL 语句查询的列，则只扫描索引数据即可满足查询。

例如，以下查询只需要根据 `title` 查询对应的 `price`：

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+-------------+--------+
| title       | price  |
+-------------+--------+
| Marian Yost | 435.01 |
| Marian Yost | 328.18 |
| Marian Yost | 496.52 |
| Marian Yost | 402.90 |
| Marian Yost | 174.64 |
+-------------+--------+
5 rows in set
Time: 0.007s
```

由于 `title_idx` 索引只包含 `title` 列的数据，TiDB 仍需先扫描索引数据，然后再从表中查询 `price` 列。

用 `EXPLAIN` 查看执行计划：

```sql
EXPLAIN SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| id                        | estRows | task      | access object                       | operator info                                         |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| IndexLookUp_10            | 1.27    | root      |                                     |                                                       |
| ├─IndexRangeScan_8(Build) | 1.27    | cop[tikv] | table:books, index:title_idx(title) | range:["Marian Yost","Marian Yost"], keep order:false |
| └─TableRowIDScan_9(Probe) | 1.27    | cop[tikv] | table:books                         | keep order:false                                      |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
```

为了优化性能，可以删除旧的索引 `title_idx`，并创建一个新的覆盖索引 `title_price_idx`：

```sql
ALTER TABLE books DROP INDEX title_idx;
```

```sql
CREATE INDEX title_price_idx ON books (title, price);
```

因为 `price` 数据存储在 `title_price_idx` 索引中，以下查询只需扫描索引数据：

```sql
EXPLAIN SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
| id                  | estRows | task      | access object                                    | operator info                                         |
+---------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
| IndexReader_6       | 1.27    | root      |                                                  | index:IndexRangeScan_5                                |
| └─IndexRangeScan_5  | 1.27    | cop[tikv] | table:books, index:title_price_idx(title, price) | range:["Marian Yost","Marian Yost"], keep order:false |
+---------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
```

此时，查询运行速度更快：

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+-------------+--------+
| title       | price  |
+-------------+--------+
| Marian Yost | 174.64 |
| Marian Yost | 328.18 |
| Marian Yost | 402.90 |
| Marian Yost | 435.01 |
| Marian Yost | 496.52 |
+-------------+--------+
5 rows in set
Time: 0.004s
```

由于 `books` 表会在后续示例中使用，建议删除 `title_price_idx` 索引：

```sql
ALTER TABLE books DROP INDEX title_price_idx;
```

### 解决方案：使用主键索引

如果查询使用主键过滤数据，查询会非常快。例如，`books` 表的主键是 `id` 列，可以用 `id` 列进行查询：

```sql
SELECT * FROM books WHERE id = 896;
```

```sql
+-----+----------------+----------------------+---------------------+-------+--------+
| id  | title          | type                 | published_at        | stock | price  |
+-----+----------------+----------------------+---------------------+-------+--------+
| 896 | Kathryne Doyle | Science & Technology | 1969-03-18 01:34:15 | 468   | 281.32 |
+-----+----------------+----------------------+---------------------+-------+--------+
1 row in set
Time: 0.004s
```

用 `EXPLAIN` 查看执行计划：

```sql
EXPLAIN SELECT * FROM books WHERE id = 896;
```

```sql
+--------------+---------+------+---------------+---------------+
| id           | estRows | task | access object | operator info |
+--------------+---------+------+---------------+---------------+
| Point_Get_1  | 1.00    | root | table:books   | handle:896    |
+--------------+---------+------+---------------+---------------+
```

`Point_Get` 是一种非常快速的执行计划。

## 使用正确的连接类型

请参见 [JOIN 执行计划](/explain-joins.md)。

### 另请参见

* [EXPLAIN Walkthrough](/explain-walkthrough.md)
* [使用索引的 Explain 语句](/explain-indexes.md)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>