---
title: Common Table Expression
---

# Common Table Expression

Due to the objective complexity of the business, sometimes a single SQL statement as long as 2000 lines is written, which contains a large number of aggregations and multi-level sub-query nesting. Maintaining such SQL is a developer's nightmare.

In the previous subsections we have described how to use [views](/develop/dev-use-views.md) to simplify queries and how to use [temporary tables](/develop/dev-use-temporary-tables.md) to cache intermediate query results.

In this section, we will introduce the Common Table Expression (CTE) syntax in TiDB, which is a more convenient way to reuse query results.

Since version 5.1, TiDB supports ANSI SQL 99 standard CTE and its recursive form, which greatly improves the efficiency of developers and DBAs in writing complex business logic SQL, and enhances the maintainability of the code.

## Basic use

Common Table Expression (CTE) is a temporary intermediate result set that can be referenced multiple times in SQL statements to improve the readability and execution efficiency of SQL statements. In TiDB, common table expressions can be used through the `WITH` statement。

Common table expressions can be classified into non-recursive and recursive types.

### Non-recursive CTE

Non-recursive CTEs are defined using the following syntax:

```sql
WITH <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

For example, suppose we still want to know how many books each of the 50 oldest authors has written.

<SimpleTab>
<div label="SQL">

We can change the example in the [temporary tables](/develop/dev-use-temporary-tables.md) section to the following SQL statement:

{{< copyable "sql" >}}

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

The query results are as follows:

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
50 rows in set (0.01 sec)
```

</div>
<div label="Java">

{{< copyable "java" >}}

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

We found that the author named "Ray Macejkovic" wrote 4 books, let's go on to find out the orders and ratings of these 4 books by CTE query:

{{< copyable "sql" >}}

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

The query results are as follows:

```
+------------+-------------------------+----------------+--------+
| book_id    | book_title              | average_rating | orders |
+------------+-------------------------+----------------+--------+
|  481008467 | The Documentary of goat |         2.0000 |     16 |
| 2224531102 | Brandt Skiles           |         2.7143 |     17 |
| 2641301356 | Sheridan Bashirian      |         2.4211 |     12 |
| 4154439164 | Karson Streich          |         2.5833 |     19 |
+------------+-------------------------+----------------+--------+
4 rows in set (0.06 sec)
```

In this SQL statement, we define three CTE blocks, which are separated by `,`.

We first check out the books written by the author (The ID of the author is `2299112019`) in the CTE block `books_authored_by_rm`, then find the average rating and number of orders for these books in `books_with_average_ratings` and `books_with_orders` respectively, and finally aggregate the results by `JOIN` statement.

It is noteworthy that the query in `books_authored_by_rm` will only be executed once, and TiDB will open up a temporary space to cache the results of the query. When `books_with_average_ratings` and `books_with_orders` refer to, it will directly obtain data from this temporary space.

### Recursive CTE

Recursive common table expressions can be defined using the following syntax:

```sql
WITH RECURSIVE <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

A more classic example is to generate a set of [Fibonacci numbers](https://en.wikipedia.org/wiki/Fibonacci_number) through recursive CTE：

{{< copyable "sql" >}}

```sql
WITH RECURSIVE fibonacci (n, fib_n, next_fib_n) AS
(
  SELECT 1, 0, 1
  UNION ALL
  SELECT n + 1, next_fib_n, fib_n + next_fib_n FROM fibonacci WHERE n < 10
)
SELECT * FROM fibonacci;
```

The query results are as follows:

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
10 rows in set (0.00 sec)
```

## Read more

- [WITH](/common/sql-statements/sql-statement-with.md)
