---
title: Best Practices for Indexing
summary: Introducing best practices for indexing in TiDB.
---

<!-- markdownlint-disable MD029 -->

# Best Practices for Indexing

This document introduces some best practices for creating and using indexes in TiDB.

## Before you begin

This section takes the `books` table in the [bookshop](/develop/dev-guide-bookshop-schema-design.md) database as an example.

{{< copyable "sql" >}}

```sql
CREATE TABLE `books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

## Best practices for creating indexes

- Creating combined index with multiple columns, which is a optimization called [covering index optimization](/explain-indexes.md#indexreader). **Covering index optimization** allows TiDB to query data directly on the index, which helps improve performance.
- Avoid creating a secondary index on columns that you don't query often. A useful secondary index can speed up queries, but be aware that it also has side effects. Each time you add an index, an additional Key-Value is added when you insert a row. The more indexes you have, the slower you write, and the more space it takes up. In addition, too many indexes affect optimizer runtime, and inappropriate indexes can mislead the optimizer. So, more indexes aren't always better.
- Create an appropriate index based on business. In principle, you need to create indexes on the columns needed to be used in queries to improve performance. The following situations are suitable for creating an index:

    - Columns with a high distinction degree can significantly reduce the number of filtered rows. For example, it is recommended to create an index on the personal ID number, but not on the gender.
    - Use combined indexes when querying with multiple conditions. Note that columns with equivalent conditions need to be placed in the front of the combined index. Here is an example: assuming the query is `select* from t where c1 = 10 and c2 = 100 and c3 > 10`, then consider creating a combined index `Index cidx (c1, c2, c3)`, so that index prefix can be constructed to Scan by query conditions.

- Name your secondary index meaningfully, and it is recommended to follow the table naming conventions of your company or organization. If not, refer to [Index Naming Specification](/develop/dev-guide-object-naming-guidelines.md).

## Best practices for using indexes

- Index is to speed up the query, so make sure the index can be used in some queries. If an index is not used by any query, the index is meaningless, so, drop it.
- When using a combined index, satisfy the left-prefix rule.

    Suppose that you create a new combined index on the column `title, published_at`:

    {{< copyable "sql" >}}

    ```sql
    CREATE INDEX title_published_at_idx ON books (title, published_at);
    ```

    The following query can still use the combined index:

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

    However, the following query cannot use the combined index because the condition for the leftmost first column is not specified:

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE published_at = '2018-08-18 21:42:08';
    ```

- When using an index column as a condition in a query, do not use calculation, function, or type conversion on it, which will prevent the TiDB optimizer from using the index.

    Suppose that you create a new index `published_at` on the time type column:

    {{< copyable "sql" >}}

    ```sql
    CREATE INDEX published_at_idx ON books (published_at);
    ```

    However, the following query cannot use the index on `published_at`:

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE YEAR(published_at)=2022;
    ```

    It can be rewritten as the following query to avoid using function on the index column, and then use the index on `published_at`:

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE published_at >= '2022-01-01' AND published_at < '2023-01-01';
    ```

    You can also use the expression index, for example, to create an expression index for `YEAR(Published at)` in the query condition:

    {{< copyable "sql" >}}

    ```sql
    CREATE INDEX published_year_idx ON books ((YEAR(published_at)));
    ```

    Now, query with `SELECT * FROM books WHERE YEAR(published_at)=2022;` you can use `published_year_idx` index to speed up.

    > **Warning:**
    >
    > Currently, expression index is an experimental feature, and it needs to be enabled in the TiDB configuration file. For more details, see [expression index](/common/sql-statements/sql-statement-create-index.md#expression-index).

- Try to use covering index, which is the index columns contain query columns and avoid querying all columns with `SELECT *` statements.

    The following query only needs to scan the index `title_published_at_idx` to get the data:

    {{< copyable "sql" >}}

    ```sql
    SELECT title, published_at FROM books WHERE title = 'database';
    ```

    Although the following query statement can use the combined index `(title, published_at)`, it will have an extra cost to query the non-indexed column. Querying the non-indexed column in the table according to the reference stored in the index data (usually the primary key information).

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

- Cannot use indexes when the query condition is `!=` or `NOT IN`. For example, the following query cannot use any indexes:

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title != 'database';
    ```

- Cannot use indexes when the query condition is `LIKE`, and the condition starts with the wildcard `%`. For example, the following query cannot use any indexes:

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM books WHERE title LIKE '%database';
    ```

- When the query condition has multiple indexes available, and you know which index is the best in practice, it is recommended to use [Optimizer Hint](/optimizer-hints.md) to force the TiDB optimizer to use this index. This can prevent the TiDB optimizer from selecting the wrong index due to inaccurate statistics or other problems.

    In the following query, assuming that there are indexes `id_idx` and `title_idx` on the column `id` and `title` respectively, you know that `id_idx` is better, you can use `USE INDEX` hint in SQL to force the TiDB optimizer to use the `id_idx` index.

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM t USE INDEX(id_idx) WHERE id = 1 and title = 'database';
    ```

- When using the `IN` expression in a query condition, it is recommended that the number of value matched after it does not exceed 300, otherwise the execution efficiency will be poor.
