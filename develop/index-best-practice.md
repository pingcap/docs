---
title: Best Practices for Indexing
---

<!-- markdownlint-disable MD029 -->

# Best Practices for Indexing

This section introduces some best practices for creating and using index in TiDB.

## Before you begin

This section will use the `books` table in the [bookshop](/develop/bookshop-schema-design.md) database as an example.

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

## Create Index Best Practices

1. Create combined index of all the columns of data you need to use. This optimization technique is called [covering index optimization](https://docs.pingcap.com/tidb/stable/explain-indexes#indexreader). `covering index optimization` will allow TiDB to get all required data for the query directly on the index data, which can greatly improve performance.

2. Avoid creating secondary index that you don't need. Useful secondary indexes can speed up queries, but be aware that adding an index has side effects. Every time you add an index, an additional key-value is added when you insert a row of data, so the more indexes you have, the slower you write, and the more space it takes up. In addition, too many indexes can affect optimizer runtime, and inappropriate indexes can mislead the optimizer. So more indexes aren't always better.

3. Create an appropriate index based on business characteristics. In principle, you need to create indexes on the columns you need to use in your query to improve performance. The following situations are suitable for creating an index:

- Columns with a high degree of distinction can significantly reduce the number of filtered rows. For example, it is recommended to create an index on the column of the person's ID number, but not on the column of the person's gender.
- If you have multiple search conditions, you can use combined index. Note that columns with equivalent conditions need to be placed in front of the combined index.

Here is an example. Assuming the query is `select* from t where c1 = 10 and c2 = 100 and c3 > 10`, then consider creating a combined index `Index cidx (c1, c2, c3)`, so that index prefix scan can be performed according to query conditions.

4. Use meaningful secondary index name, and we recommend that you follow your company's or organization's table naming conventions. If your company or organization does not have an appropriate naming convention, refer to [Index Naming Specification](/develop/object-naming-guidelines.md).

## Use Index Best Practices

1. Index is to speed up the query, so make sure the index can be used in some queries. If an index is not used by any query, the index is meaningless, so drop the index.

2. When using combined index, the leftmost prefix principle needs to be met.

For example, suppose you create a new combined index on the column `title, published_at`:

```sql
CREATE INDEX title_published_at_idx ON books (title, published_at);
```

The following query can still use the combined index:

```sql
SELECT * FROM books WHERE title = 'database';
```

However, the following query cannot use the combined index because the condition for the leftmost first column in the combined index is not specified:

```sql
SELECT * FROM books WHERE published_at = '2018-08-18 21:42:08';
```

3. If you use an index column as a condition in a query condition, do not perform calculations, function, or type conversion operations on the index column, which will prevent the TiDB optimizer from using the index.

For example, suppose you create a new index on the time-type column `published_at`:

```sql
CREATE INDEX published_at_idx ON books (published_at);
```

However, the following query cannot use the index on `published_at`:

```sql
SELECT * FROM books WHERE YEAR(published_at)=2022;
```

It can be rewritten as the following query to avoid doing function calculations on the index column, and then use the index on `published_at`:

```sql
SELECT * FROM books WHERE published_at >= '2022-01-01' AND published_at < '2023-01-01';
```

You can also use expression index, for example, to create an expression index for 'YEAR(Published at)' in the query condition:

```sql
CREATE INDEX published_year_idx ON books ((YEAR(published_at)));
```

Now `SELECT * FROM books WHERE YEAR(published_at)=2022;` can use `published_year_idx` index to speed up.

> **Warning:**
>
> Currently, expression index is an experimental feature, and it needs to be enabled in the TiDB configuration file, see more in [expression index](https://docs.pingcap.com/tidb/stable/sql-statement-create-index#expression-index).

4. Try to use covering index, which is the index columns contains query columns, and avoid `SELECT *` statements.

For example, the following query only needs to scan the index `title_published_at_idx` data to get the data of the query:

```sql
SELECT title, published_at FROM books WHERE title = 'database';
```

However, although the following query statement can use the combined index `(title, published_at)`, it will have extra cost to query the non-indexed column data. Querying the non-indexed column data in the table according to the reference stored in the index data (usually the primary key information).

```sql
SELECT * FROM books WHERE title = 'database';
```

5. Cannot use index when query condition is `! =` or `NOT IN`. For example, the following query cannot use any indexes:

```sql
SELECT * FROM books WHERE title != 'database';
```

6. Cannot use index when query condition is `LIKE`, and the condition starts with the wildcard `%`. For example, the following query cannot use any indexes:

```sql
SELECT * FROM books WHERE title LIKE '%database';
```

7. When the query condition has multiple indexes available, but you know which index is the best one to use, it is recommended to use [Optimizer Hint](https://docs.pingcap.com/tidb/stable/optimizer-hints) to force the TiDB optimizer to use this index. This can prevent the TiDB optimizer from selecting the wrong index due to inaccurate statistics or other problems.

For example, in the following query, assuming that there are indexes `id_idx` and `title_idx` on column `id` and column `title` respectively, you know that `id_idx` is better, you can use `USE INDEX` hint in SQL to force the TiDB optimizer to use the `id_idx` index.

```sql
SELECT * FROM t USE INDEX(id_idx) WHERE id = 1 and title = 'database';
```

8. When using the `IN` expression in a query condition, it is recommended that the number of value matched after it does not exceed 300, otherwise the execution efficiency will be poor.