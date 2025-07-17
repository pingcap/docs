---
title: Multi-table Join Queries
summary: 本文档描述了如何使用多表连接查询。
---

# Multi-table Join Queries

在许多场景中，你需要用一条查询语句从多个表中获取数据。你可以使用 `JOIN` 语句将两个或多个表中的数据结合起来。

## Join types

本节详细介绍各种连接类型。

### INNER JOIN

内连接的结果只返回满足连接条件的行。

![Inner Join](/media/develop/inner-join.png)

例如，如果你想知道最 prolific 的作者，你需要将名为 `authors` 的作者表与名为 `book_authors` 的图书作者表进行连接。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在以下 SQL 语句中，使用关键字 `JOIN` 来声明你希望将左表 `authors` 和右表 `book_authors` 作为内连接连接，连接条件为 `a.id = ba.author_id`。结果集只包含满足连接条件的行。如果某个作者没有写过任何书，那么他在 `authors` 表中的记录将不满足连接条件，因此不会出现在结果集中。

```sql
SELECT ANY_VALUE(a.id) AS author_id, ANY_VALUE(a.name) AS author_name, COUNT(ba.book_id) AS books
FROM authors a
JOIN book_authors ba ON a.id = ba.author_id
GROUP BY ba.author_id
ORDER BY books DESC
LIMIT 10;
```

查询结果如下：

```
+------------+----------------+-------+
| author_id  | author_name    | books |
+------------+----------------+-------+
|  431192671 | Emilie Cassin  |     7 |
|  865305676 | Nola Howell    |     7 |
|  572207928 | Lamar Koch     |     6 |
| 3894029860 | Elijah Howe    |     6 |
| 1150614082 | Cristal Stehr  |     6 |
| 4158341032 | Roslyn Rippin  |     6 |
| 2430691560 | Francisca Hahn |     6 |
| 3346415350 | Leta Weimann   |     6 |
| 1395124973 | Albin Cole     |     6 |
| 2768150724 | Caleb Wyman    |     6 |
+------------+----------------+-------+
10 rows in set (0.01 sec)
```

</div>
<div label="Java" value="java">

```java
public List<Author> getTop10AuthorsOrderByBooks() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
        SELECT ANY_VALUE(a.id) AS author_id, ANY_VALUE(a.name) AS author_name, COUNT(ba.book_id) AS books
        FROM authors a
        JOIN book_authors ba ON a.id = ba.author_id
        GROUP BY ba.author_id
        ORDER BY books DESC
        LIMIT 10;
        """);
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("author_id"));
            author.setName(rs.getString("author_name"));
            author.setBooks(rs.getInt("books"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

### LEFT OUTER JOIN

左外连接返回左表中的所有行，以及满足连接条件的右表中的值。如果右表中没有匹配的行，则用 `NULL` 填充。

![Left Outer Join](/media/develop/left-outer-join.png)

在某些情况下，你希望用多张表完成数据查询，但又不希望因为连接条件不满足而导致数据集变得过小。

例如，在 Bookshop 应用的首页，你想展示一份带有平均评分的新书列表。在这种情况下，新书可能还没有被任何人评分。使用内连接会导致这些未评分的书籍信息被过滤掉，这不是你想要的。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在以下 SQL 语句中，使用 `LEFT JOIN` 关键字声明左表 `books` 将与右表 `ratings` 进行左外连接，从而确保返回 `books` 表中的所有行。

```sql
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

查询结果如下：

```
+------------+---------------------------------+---------------+
| book_id    | book_title                      | average_score |
+------------+---------------------------------+---------------+
| 3438991610 | The Documentary of lion         |        2.7619 |
| 3897175886 | Torey Kuhn                      |        3.0000 |
| 1256171496 | Elmo Vandervort                 |        2.5500 |
| 1036915727 | The Story of Munchkin           |        2.0000 |
|  270254583 | Tate Kovacek                    |        2.5000 |
| 1280950719 | Carson Damore                   |        3.2105 |
| 1098041838 | The Documentary of grasshopper  |        2.8462 |
| 1476566306 | The Adventures of Vince Sanford |        2.3529 |
| 4036300890 | The Documentary of turtle       |        2.4545 |
| 1299849448 | Antwan Olson                    |        3.0000 |
+------------+---------------------------------+---------------+
10 rows in set (0.30 sec)
```

似乎最新出版的书已经有很多评分了。为了验证上述方法，让我们通过以下 SQL 语句删除 _The Documentary of lion_ 这本书的所有评分：

```sql
DELETE FROM ratings WHERE book_id = 3438991610;
```

再次查询。 _The Documentary of lion_ 这本书仍然出现在结果集中，但由右表 `ratings` 的 `score` 计算得出的 `average_score` 列变成了 `NULL`。

```
+------------+---------------------------------+---------------+
| book_id    | book_title                      | average_score |
+------------+---------------------------------+---------------+
| 3438991610 | The Documentary of lion         |          NULL |
| 3897175886 | Torey Kuhn                      |        3.0000 |
| 1256171496 | Elmo Vandervort                 |        2.5500 |
| 1036915727 | The Story of Munchkin           |        2.0000 |
|  270254583 | Tate Kovacek                    |        2.5000 |
| 1280950719 | Carson Damore                   |        3.2105 |
| 1098041838 | The Documentary of grasshopper  |        2.8462 |
| 1476566306 | The Adventures of Vince Sanford |        2.3529 |
| 4036300890 | The Documentary of turtle       |        2.4545 |
| 1299849448 | Antwan Olson                    |        3.0000 |
+------------+---------------------------------+---------------+
```

如果你用 `INNER JOIN` 会发生什么？可以自己试试。

</div>
<div label="Java" value="java">

```java
public List<Book> getLatestBooksWithAverageScore() throws SQLException {
    List<Book> books = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
        SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
        FROM books b
        LEFT JOIN ratings r ON b.id = r.book_id
        GROUP BY b.id
        ORDER BY b.published_at DESC
        LIMIT 10;
        """);
        while (rs.next()) {
            Book book = new Book();
            book.setId(rs.getLong("book_id"));
            book.setTitle(rs.getString("book_title"));
            book.setAverageScore(rs.getFloat("average_score"));
            books.add(book);
        }
    }
    return books;
}
```

</div>
</SimpleTab>

### RIGHT OUTER JOIN

右外连接返回右表中的所有记录，以及满足连接条件的左表中的值。如果没有匹配的值，则用 `NULL` 填充。

![Right Outer Join](/media/develop/right-outer-join.png)

### CROSS JOIN

当连接条件为常数时，两个表之间的内连接称为 [cross join](https://en.wikipedia.org/wiki/Join_(SQL)#Cross_join)。交叉连接会将左表的每一条记录与右表的所有记录进行连接。如果左表的记录数为 `m`，右表的记录数为 `n`，那么结果集中会生成 `m * n` 条记录。

### LEFT SEMI JOIN

TiDB 不支持 `LEFT SEMI JOIN table_name` 作为 SQL 语法。但在执行计划层面，[子查询相关的优化](/subquery-optimization.md) 会将 `semi join` 作为重写后等价 JOIN 查询的默认连接方式。

## Implicit join

在 SQL 标准加入显式声明 `JOIN` 语句之前，可以在 SQL 语句中使用 `FROM t1, t2` 子句连接两个或多个表，并用 `WHERE t1.id = t2.id` 子句指定连接条件。可以理解为一种隐式连接，实际上是用内连接连接表。

## Join related algorithms

TiDB 支持以下通用的表连接算法。

- [Index Join](/explain-joins.md#index-join)
- [Hash Join](/explain-joins.md#hash-join)
- [Merge Join](/explain-joins.md#merge-join)

优化器会根据连接表中的数据量等因素选择合适的连接算法执行。你可以通过使用 `EXPLAIN` 语句查看查询使用了哪种连接算法。

如果 TiDB 的优化器没有按照最优的连接算法执行，你可以使用 [Optimizer Hints](/optimizer-hints.md) 强制 TiDB 使用更优的连接算法。

例如，假设上面左连接查询的示例使用 Hash Join 算法会更快，但未被优化器选择，你可以在 `SELECT` 关键字后添加提示 `/*+ HASH_JOIN(b, r) */`。注意，如果表有别名，提示中也要使用别名。

```sql
EXPLAIN SELECT /*+ HASH_JOIN(b, r) */ b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

与连接算法相关的提示：

- [MERGE_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#merge_joint1_name--tl_name-)
- [INL_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#inl_joint1_name--tl_name-)
- [INL_HASH_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#inl_hash_join)
- [HASH_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#hash_joint1_name--tl_name-)

## Join orders

在实际业务场景中，多表连接语句非常常见。连接的执行效率与各个表在连接中的顺序有关。TiDB 使用 Join Reorder 算法来确定多表连接的顺序。

如果优化器选择的连接顺序不如预期的最优，你可以使用 `STRAIGHT_JOIN` 强制 TiDB 按照 `FROM` 子句中表的顺序进行连接。

```sql
EXPLAIN SELECT *
FROM authors a STRAIGHT_JOIN book_authors ba STRAIGHT_JOIN books b
WHERE b.id = ba.book_id AND ba.author_id = a.id;
```

关于此 Join Reorder 算法的实现细节和限制，详见 [Introduction to Join Reorder Algorithm](/join-reorder.md)。

## See also

- [Explain Statements That Use Joins](/explain-joins.md)
- [Introduction to Join Reorder](/join-reorder.md)

## Need help?

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>