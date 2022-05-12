---
title: Subqueries
---

# Subqueries

## Overview

Subqueries are SQL expressions nested within another query, with the help of subqueries, we can use the query results of another query in one query.

Below we will take the [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application as an example to introduce subqueries:

## Subquery statement

Typically, subquery statements are divided into the following forms:

- Scalar Subquery (Scalar Subquery), such as `SELECT (SELECT s1 FROM t2) FROM t1`.
- Derived Tables, such as `SELECT t1.s1 FROM (SELECT s1 FROM t2) t1`.
- Existential Test, e.g. `WHERE NOT EXISTS(SELECT ... FROM t2)`, `WHERE t1.a IN (SELECT ... FROM t2)`.
- Quantified Comparison, e.g. `WHERE t1.a = ANY(SELECT ... FROM t2)`, `WHERE t1.a = ANY(SELECT ... FROM t2)`.
- Subquery as a comparison operator operand, e.g. `WHERE t1.a > (SELECT ... FROM t2)`.

## The category of subqueries

Generally speaking, we can divide subqueries into two categories: [Correlated Subquery](https://en.wikipedia.org/wiki/Correlated_subquery) and Self-contained Subquery. TiDB treats these two types of subqueries differently.

The basis for determining whether a subquery is related or not is whether we refer to the columns of the outer query in the subquery.

### Self-contained subquery

For unrelated subqueries that use subqueries as operand of comparison operators (`>` / `>=`/ `<` / `<=` / `=` / `! =`), the inner subquery needs to be queried only once, and TiDB rewrites the inner subquery as a constant during the execution plan generation phase.

For example, if we want to find authors in the `authors` table whose age is greater than the overall average age, we can do so by using the subquery as the operand of the comparison operator.

{{< copyable "sql" >}}

```sql
SELECT * FROM authors a1 WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > (
    SELECT
        AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age
    FROM
        authors a2
)
```

First of all, the inner subquery is executed once when TiDB executes the above query in advance:

{{< copyable "sql" >}}

```sql
SELECT AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age FROM authors a2;
```

Suppose the result of the query is 34, i.e., the overall average age is 34, and 34 will be used as a constant to replace the original subquery.

{{< copyable "sql" >}}

```sql
SELECT * FROM authors a1
WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > 34;
```

```
+--------+-------------------+--------+------------+------------+
| id     | name              | gender | birth_year | death_year |
+--------+-------------------+--------+------------+------------+
| 13514  | Kennith Kautzer   | 1      | 1956       | 2018       |
| 13748  | Dillon Langosh    | 1      | 1985       | NULL       |
| 99184  | Giovanny Emmerich | 1      | 1954       | 2012       |
| 180191 | Myrtie Robel      | 1      | 1958       | 2009       |
| 200969 | Iva Renner        | 0      | 1977       | NULL       |
| 209671 | Abraham Ortiz     | 0      | 1943       | 2016       |
| 229908 | Wellington Wiza   | 1      | 1932       | 1969       |
| 306642 | Markus Crona      | 0      | 1969       | NULL       |
| 317018 | Ellis McCullough  | 0      | 1969       | 2014       |
| 322369 | Mozelle Hand      | 0      | 1942       | 1977       |
| 325946 | Elta Flatley      | 0      | 1933       | 1986       |
| 361692 | Otho Langosh      | 1      | 1931       | 1997       |
| 421294 | Karelle VonRueden | 0      | 1977       | NULL       |
...
```

For unrelated column subqueries in both existence test and quantified comparison cases, TiDB rewrites and equivalently replaces them for better execution performance, you can read the [Subquery Related Optimizations](/subquery-optimization.md) chapter for more implementation details.

## Correlated subquery

For correlated subquery, since the inner subquery references the columns of the outer query, the subquery needs to be executed on every row obtained by the outer query. That is, assuming that the outer query gets 10 million results, the subquery will also be executed 10 million times, which will cause the query to consume more time and resources.

Therefore, in the process of processing, TiDB will try to [Decorrelate of Correlated Subquery](/correlated-subquery-optimization.md) to improve the query efficiency in the execution plan level.

For example, if we want to find authors who are older than the average age of other writers of the same gender, the SQL statement could be written like this.

{{< copyable "sql" >}}

```sql
SELECT * FROM authors a1 WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > (
    SELECT
        AVG(
            IFNULL(a2.death_year, YEAR(NOW())) - IFNULL(a2.birth_year, YEAR(NOW()))
        ) AS average_age
    FROM
        authors a2
    WHERE a1.gender = a2.gender
);
```

When TiDB processes this SQL statement, it will rewrite it into an equivalent join query:

{{< copyable "sql" >}}

```sql
SELECT *
FROM
    authors a1,
    (
        SELECT
            gender, AVG(
                IFNULL(a2.death_year, YEAR(NOW())) - IFNULL(a2.birth_year, YEAR(NOW()))
            ) AS average_age
        FROM
            authors a2
        GROUP BY gender
    ) a2
WHERE
    a1.gender = a2.gender
    AND (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > a2.average_age;
```

As a best practice, in actual development, it is recommended to avoid querying through correlated subqueries when it is clear that there is a better equivalent way of writing.

## Read more

- [Subquery Related Optimizations](/subquery-optimization.md)
- [Decorrelation of Correlated Subquery](/correlated-subquery-optimization.md)
- [Subquery Optimization in TiDB](https://en.pingcap.com/blog/subquery-optimization-in-tidb/)
