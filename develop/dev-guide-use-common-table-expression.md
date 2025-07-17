---
title: Common Table Expression
summary: 了解 TiDB 的 CTE 特性，帮助你更高效地编写 SQL 语句。
---

# Common Table Expression

在某些事务场景中，由于应用复杂性，可能需要编写一条长达 2000 行的 SQL 语句。该语句可能包含大量的聚合和多层子查询嵌套。维护如此长的 SQL 语句可能让开发者头疼不已。

为了避免编写如此长的 SQL 语句，你可以通过使用 [Views](/develop/dev-guide-use-views.md) 简化查询，或通过使用 [Temporary tables](/develop/dev-guide-use-temporary-tables.md) 缓存中间查询结果。

本文介绍 TiDB 中的 Common Table Expression (CTE) 语法，这是一种更方便的复用查询结果的方法。

自 TiDB v5.1 起，TiDB 支持符合 ANSI SQL99 标准的 CTE 以及递归。借助 CTE，你可以更高效地编写复杂应用逻辑的 SQL 语句，并且更容易维护代码。

## 基本用法

Common Table Expression (CTE) 是一种临时结果集，可以在一条 SQL 语句中多次引用，以提高语句的可读性和执行效率。你可以应用 [`WITH`](/sql-statements/sql-statement-with.md) 语句来使用 CTE。

Common Table Expressions 可以分为两类：非递归 CTE 和递归 CTE。

### 非递归 CTE

非递归 CTE 可以使用以下语法定义：

```sql
WITH <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

例如，如果你想知道 50 位最老作者每人写了多少本书，可以按照以下步骤操作：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

将 [temporary tables](/develop/dev-guide-use-temporary-tables.md) 中的语句改为如下：

```sql
WITH top_50_eldest_authors_cte AS (
    SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
    FROM authors a
    ORDER BY age DESC
    LIMIT 50
)
SELECT
    ANY_VALUE(ta.id) AS author_id,
    ANY_VALUE(ta.age) AS author_age,
    ANY_VALUE(ta.name) AS author_name,
    COUNT(*) AS books
FROM top_50_eldest_authors_cte ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

结果如下：

```
+------------+------------+---------------------+-------+
| author_id  | author_age | author_name         | books |
+------------+------------+---------------------+-------+
| 1238393239 |         80 | Araceli Purdy       |     1 |
|  817764631 |         80 | Ivory Davis         |     3 |
| 3093759193 |         80 | Lysanne Harris      |     1 |
| 2299112019 |         80 | Ray Macejkovic      |     4 |
...
+------------+------------+---------------------+-------+
50 行，耗时 0.01 秒
```

</div>
<div label="Java" value = "java">

```java
public List<Author> getTop50EldestAuthorInfoByCTE() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
            WITH top_50_eldest_authors_cte AS (
                SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
                FROM authors a
                ORDER BY age DESC
                LIMIT 50
            )
            SELECT
                ANY_VALUE(ta.id) AS author_id,
                ANY_VALUE(ta.name) AS author_name,
                ANY_VALUE(ta.age) AS author_age,
                COUNT(*) AS books
            FROM top_50_eldest_authors_cte ta
            LEFT JOIN book_authors ba ON ta.id = ba.author_id
            GROUP BY ta.id;
        """);
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("author_id"));
            author.setName(rs.getString("author_name"));
            author.setAge(rs.getShort("author_age"));
            author.setBooks(rs.getInt("books"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

可以看到，作者 "Ray Macejkovic" 写了 4 本书。利用 CTE 查询后，还可以进一步获取这 4 本书的排序和评分信息，示例如下：

```sql
WITH books_authored_by_rm AS (
    SELECT *
    FROM books b
    LEFT JOIN book_authors ba ON b.id = ba.book_id
    WHERE author_id = 2299112019
), books_with_average_ratings AS (
    SELECT
        b.id AS book_id,
        AVG(r.score) AS average_rating
    FROM books_authored_by_rm b
    LEFT JOIN ratings r ON b.id = r.book_id
    GROUP BY b.id
), books_with_orders AS (
    SELECT
        b.id AS book_id,
        COUNT(*) AS orders
    FROM books_authored_by_rm b
    LEFT JOIN orders o ON b.id = o.book_id
    GROUP BY b.id
)
SELECT
    b.id AS `book_id`,
    b.title AS `book_title`,
    br.average_rating AS `average_rating`,
    bo.orders AS `orders`
FROM
    books_authored_by_rm b
    LEFT JOIN books_with_average_ratings br ON b.id = br.book_id
    LEFT JOIN books_with_orders bo ON b.id = bo.book_id
;
```

结果如下：

```
+------------+-------------------------+----------------+--------+
| book_id    | book_title              | average_rating | orders |
+------------+-------------------------+----------------+--------+
|  481008467 | The Documentary of goat |         2.0000 |     16 |
| 2224531102 | Brandt Skiles           |         2.7143 |     17 |
| 2641301356 | Sheridan Bashirian      |         2.4211 |     12 |
| 4154439164 | Karson Streich          |         2.5833 |     19 |
+------------+-------------------------+----------------+--------+
4 行，耗时 0.06 秒
```

在此 SQL 语句中定义了三个用逗号分隔的 CTE 块。

首先，在 `books_authored_by_rm` CTE 块中，查询作者（ID 为 `2299112019`）写的书。然后在 `books_with_average_ratings` 和 `books_with_orders` 中分别查找这些书的平均评分和订单数。最后通过 `JOIN` 语句汇总结果。

注意，`books_authored_by_rm` 中的查询只会执行一次，TiDB 会创建一个临时空间缓存其结果。当 `books_with_average_ratings` 和 `books_with_orders` 中的查询引用 `books_authored_by_rm` 时，TiDB 直接从这个临时空间获取结果。

> **Tip:**
>
> 如果默认的 CTE 查询效率不佳，可以使用 [`MERGE()`](/optimizer-hints.md#merge) 提示，将 CTE 子查询展开到外层查询中以提升效率。

### 递归 CTE

递归 CTE 可以使用以下语法定义：

```sql
WITH RECURSIVE <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

经典示例是用递归 CTE 生成一组 [Fibonacci 数列](https://en.wikipedia.org/wiki/Fibonacci_number)：

```sql
WITH RECURSIVE fibonacci (n, fib_n, next_fib_n) AS
(
  SELECT 1, 0, 1
  UNION ALL
  SELECT n + 1, next_fib_n, fib_n + next_fib_n FROM fibonacci WHERE n < 10
)
SELECT * FROM fibonacci;
```

结果如下：

```
+------+-------+------------+
| n    | fib_n | next_fib_n |
+------+-------+------------+
|    1 |     0 |          1 |
|    2 |     1 |          1 |
|    3 |     1 |          2 |
|    4 |     2 |          3 |
|    5 |     3 |          5 |
|    6 |     5 |          8 |
|    7 |     8 |         13 |
|    8 |    13 |         21 |
|    9 |    21 |         34 |
|   10 |    34 |         55 |
+------+-------+------------+
```

## 阅读更多

- [WITH](/sql-statements/sql-statement-with.md)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>