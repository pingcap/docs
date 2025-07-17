---
title: 索引最佳实践
summary: 了解在 TiDB 中创建和使用索引的一些最佳实践。
---

<!-- markdownlint-disable MD029 -->

# 索引最佳实践

本文介绍在 TiDB 中创建和使用索引的一些最佳实践。

## 在开始之前

本节以 [bookshop](/develop/dev-guide-bookshop-schema-design.md) 数据库中的 `books` 表为例。

```sql
CREATE TABLE `books` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

## 创建索引的最佳实践

- 创建包含多个列的组合索引，这是一种优化方法，称为 [covering index optimization](/explain-indexes.md#indexreader)。**Covering index optimization** 允许 TiDB 直接在索引上查询数据，有助于提升性能。
- 避免在不常查询的列上创建辅助索引。一个有用的辅助索引可以加快查询速度，但也要注意它的副作用。每添加一个索引，在插入行时会额外增加 Key-Value。索引越多，写入越慢，占用空间也越大。此外，过多的索引会影响优化器的运行时间，不合适的索引还可能误导优化器。因此，索引越多并不一定意味着性能越好。
- 根据你的应用场景创建合适的索引。原则上，只在查询中会用到的列上创建索引以提升性能。以下情况适合创建索引：

    - 具有高区分度的列可以显著减少过滤的行数。例如，建议在身份证号码上创建索引，但不要在性别上创建。
    - 在使用多个条件查询时使用组合索引。注意，具有等值条件的列应放在组合索引的前面。示例：如果经常执行 `select * from t where c1 = 10 and c2 = 100 and c3 > 10`，可以考虑创建组合索引 `Index cidx (c1, c2, c3)`，这样可以通过索引前缀进行条件扫描。

- 给你的辅助索引起有意义的名字，建议遵循你所在公司或组织的命名规范。如果没有此类规范，可以参考 [Index Naming Specification](/develop/dev-guide-object-naming-guidelines.md) 中的规则。

## 使用索引的最佳实践

- 索引的目的是加快查询速度，因此要确保现有的索引确实被某些查询使用。如果某个索引没有被任何查询使用，则该索引没有意义，应将其删除。
- 使用组合索引时，遵循左前缀规则。

    假设你在 `title` 和 `published_at` 列上创建了新的组合索引：

    
    ```sql
    CREATE INDEX title_published_at_idx ON books (title, published_at);
    ```

    下面的查询仍然可以使用该组合索引：

    
    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

    但以下查询不能使用该组合索引，因为没有指定索引最左前缀的条件：

    
    ```sql
    SELECT * FROM books WHERE published_at = '2018-08-18 21:42:08';
    ```

- 在查询中使用索引列作为条件时，不要对其进行计算、函数调用或类型转换，否则会阻止 TiDB 优化器使用索引。

    假设你在 `published_at` 时间类型列上创建了索引：

    
    ```sql
    CREATE INDEX published_at_idx ON books (published_at);
    ```

    但以下查询无法利用 `published_at` 索引：

    
    ```sql
    SELECT * FROM books WHERE YEAR(published_at)=2022;
    ```

    为了使用 `published_at` 索引，可以将查询改写为避免在索引列上使用函数的形式：

    
    ```sql
    SELECT * FROM books WHERE published_at >= '2022-01-01' AND published_at < '2023-01-01';
    ```

    你也可以使用表达式索引，为 `YEAR(published_at)` 创建表达式索引：

    
    ```sql
    CREATE INDEX published_year_idx ON books ((YEAR(published_at)));
    ```

    这样，执行 `SELECT * FROM books WHERE YEAR(published_at)=2022;` 时，查询可以利用 `published_year_idx` 索引加快执行速度。

    > **Warning:**
    >
    > 目前，表达式索引是实验性功能，需要在 TiDB 配置文件中启用。更多详情请参见 [expression index](/sql-statements/sql-statement-create-index.md#expression-index)。

- 尽量使用覆盖索引，即索引中的列包含查询所需的列，避免使用 `SELECT *` 进行全列查询。

    下面的查询只需扫描索引 `title_published_at_idx` 即可获取数据：

    
    ```sql
    SELECT title, published_at FROM books WHERE title = 'database';
    ```

    虽然以下查询语句可以利用 `(title, published_at)` 组合索引，但会额外产生查询非索引列的开销，因为需要 TiDB 根据索引存储的引用（通常是主键信息）查询行数据。

    
    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

- 当查询条件中包含 `!=` 或 `NOT IN` 时，查询无法使用索引。例如，以下查询不能利用任何索引：

    
    ```sql
    SELECT * FROM books WHERE title != 'database';
    ```

- 当 `LIKE` 条件以通配符 `%` 开头时，查询也不能使用索引。例如，以下查询不能利用任何索引：

    
    ```sql
    SELECT * FROM books WHERE title LIKE '%database';
    ```

- 当查询条件存在多个可用索引，并且你知道哪个索引在实际中表现最佳时，建议使用 [Optimizer Hint](/optimizer-hints.md) 强制 TiDB 优化器使用该索引，以避免因统计信息不准确或其他问题导致选择了错误的索引。

    例如，假设 `id_idx` 和 `title_idx` 分别在 `id` 和 `title` 列上可用，如果你知道 `id_idx` 更优，可以在 SQL 中使用 `USE INDEX` 提示强制使用 `id_idx`：

    
    ```sql
    SELECT * FROM t USE INDEX(id_idx) WHERE id = 1 and title = 'database';
    ```

- 在使用 `IN` 表达式作为查询条件时，建议匹配的值数量不超过 300，否则执行效率会变差。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>