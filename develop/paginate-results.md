---
title: Paginate Result
---

# Paginate Result

When the query results are large, we often want to return the desired part in a "paginated" manner.

## Paginate query results

In TiDB, we can use the `LIMIT` statement to implement the paging function, the regular paging statement is written as follows:

{{< copyable "sql" >}}

```sql
SELECT * FROM table_a t ORDER BY gmt_modified DESC LIMIT offset, row_count;
```

`offset` indicates the starting number of records and `row_count` indicates the number of records per page. Besides, TiDB also supports `LIMIT row_count OFFSET offset` syntax.

Unless explicitly requested not to use any sorting to randomize the data, you should specify how to sort the query results with the `ORDER BY` statement when using paged query statements.

<SimpleTab>
<div label="SQL" href="page-sql">

For example, in the [Bookshop](/develop/bookshop-schema-design.md) application, we want to return the latest book list to the user in a paginated form. With the `LIMIT 0, 10` statement, we can get the information about the books on page 1 of the list, with a maximum of 10 records per page. To get page 2, we can change it to `LIMIT 10, 10`, and so on.

{{< copyable "sql" >}}

```sql
SELECT *
FROM books
ORDER BY published_at DESC
LIMIT 0, 10;
```

</div>
<div label="Java" href="page-java">

In application development, the back-end program receives the  `page_number` parameter (which means the number of the page being requested) and the`page_size` parameter (which means how many records per page) from the front-end instead of `offset` parameter, so we need to do some conversions before making database queries.

{{< copyable "java" >}}

```java
public List<Book> getLatestBooksPage(Long pageNumber, Long pageSize) throws SQLException {
    pageNumber = pageNumber < 1L ? 1L : pageNumber;
    pageSize = pageSize < 10L ? 10L : pageSize;
    Long offset = (pageNumber - 1) * pageSize;
    Long limit = pageSize;
    List<Book> books = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        PreparedStatement stmt = conn.prepareStatement("""
        SELECT id, title, published_at
        FROM books
        ORDER BY published_at DESC
        LIMIT ?, ?;
        """);
        stmt.setLong(1, offset);
        stmt.setLong(2, limit);
        ResultSet rs = stmt.executeQuery();
        while (rs.next()) {
            Book book = new Book();
            book.setId(rs.getLong("id"));
            book.setTitle(rs.getString("title"));
            book.setPublishedAt(rs.getDate("published_at"));
            books.add(book);
        }
    }
    return books;
}
```

</div>
</SimpleTab>

## Paging batches for single-field primary key tables

Regular paged update SQL usually uses primary key or unique index for sorting, and then with `offset` in LIMIT syntax to split the pages by a fixed number of rows. Then the pages are wrapped into a separate transaction to achieve flexible paging updates. 

However, the disadvantage is also obvious: because of the need to sort the primary key or unique index, the more backward pages will be involved in sorting more rows, especially when the volume of data involved in batch processing is large, it may take up too much computing resources.

Below we will introduce a more efficient paging batching schema:

<SimpleTab>
<div label="SQL" href="offset-sql">

First sort the data by primary key, then call the window function `row_number()` to generate a row number for each row of data, then call the aggregation function to group the row numbers according to the set page size, and finally calculate the minimum and maximum values of each page.

{{< copyable "sql" >}}

```sql
SELECT
    floor((t.row_num - 1) / 1000) + 1 AS page_num,
    min(t.id) AS start_key,
    max(t.id) AS end_key,
    count(*) AS page_size
FROM (
    SELECT id, row_number() OVER (ORDER BY id) AS row_num
    FROM books
) t
GROUP BY page_num
ORDER BY page_num;
```

The query results are as follows:

```
+----------+------------+------------+-----------+
| page_num | start_key  | end_key    | page_size |
+----------+------------+------------+-----------+
|        1 |     268996 |  213168525 |      1000 |
|        2 |  213210359 |  430012226 |      1000 |
|        3 |  430137681 |  647846033 |      1000 |
|        4 |  647998334 |  848878952 |      1000 |
|        5 |  848899254 | 1040978080 |      1000 |
...
|       20 | 4077418867 | 4294004213 |      1000 |
+----------+------------+------------+-----------+
20 rows in set (0.01 sec)
```

Next, just use the `WHERE id BETWEEN start_key AND end_key` statement to query the data of each slice. When modifying the data, you can also use the above calculated slice information to achieve efficient data update.

For example, if we want to delete the basic information of all the books on page 1, we can fill the `start_key` and `end_key` corresponding to page 1 of the above table into the SQL statement.

{{< copyable "sql" >}}

```sql
DELETE FROM books
WHERE
    id BETWEEN 268996 AND 213168525
ORDER BY id;
```

</div>
<div label="Java" href="offset-java">

In the Java language, we can define a `PageMeta` class to store page meta information.

{{< copyable "java" >}}

```java
public class PageMeta<K> {
    private Long pageNum;
    private K startKey;
    private K endKey;
    private Long pageSize;

    // Skip the getters and setters.

}
```

We define a `getPageMetaList()` method to get the page meta information list, and then define a method `deleteBooksByPageMeta()` that can delete data in batches according to the page meta information.

{{< copyable "java" >}}

```java
public class BookDAO {
    public List<PageMeta<Long>> getPageMetaList() throws SQLException {
        List<PageMeta<Long>> pageMetaList = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT
                floor((t.row_num - 1) / 1000) + 1 AS page_num,
                min(t.id) AS start_key,
                max(t.id) AS end_key,
                count(*) AS page_size
            FROM (
                SELECT id, row_number() OVER (ORDER BY id) AS row_num
                FROM books
            ) t
            GROUP BY page_num
            ORDER BY page_num;
            """);
            while (rs.next()) {
                PageMeta<Long> pageMeta = new PageMeta<>();
                pageMeta.setPageNum(rs.getLong("page_num"));
                pageMeta.setStartKey(rs.getLong("start_key"));
                pageMeta.setEndKey(rs.getLong("end_key"));
                pageMeta.setPageSize(rs.getLong("page_size"));
                pageMetaList.add(pageMeta);
            }
        }
        return pageMetaList;
    }

    public void deleteBooksByPageMeta(PageMeta<Long> pageMeta) throws SQLException {
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("DELETE FROM books WHERE id >= ? AND id <= ?");
            stmt.setLong(1, pageMeta.getStartKey());
            stmt.setLong(2, pageMeta.getEndKey());
            stmt.executeUpdate();
        }
    }
}
```

If we wanted to delete the data on page 1, we could write:

{{< copyable "java" >}}

```java
List<PageMeta<Long>> pageMetaList = bookDAO.getPageMetaList();
if (pageMetaList.size() > 0) {
    bookDAO.deleteBooksByPageMeta(pageMetaList.get(0));
}
```

If we want to delete all book data in batches by paging, we can write:

{{< copyable "java" >}}

```java
List<PageMeta<Long>> pageMetaList = bookDAO.getPageMetaList();
pageMetaList.forEach((pageMeta) -> {
    try {
        bookDAO.deleteBooksByPageMeta(pageMeta);
    } catch (SQLException e) {
        e.printStackTrace();
    }
});
```

</div>
</SimpleTab>

The improved scheme significantly improves the efficiency of batch processing by avoiding the performance loss caused by frequent data sorting operations.

## Paging batch for composite primary key table

### Non-clustered index table

For non-clustered index tables (also known as "non-index-organized tables"), the hidden field `_tidb_rowid` can be used as a pagination key, and the pagination method is the same as that described in the single-column primary key table.

> **Tips:**
>
> You can use the `SHOW CREATE TABLE users;` statement to check whether the table primary key uses [clustered index](https://docs.pingcap.com/tidb/stable/clustered-indexes).

For example:

{{< copyable "sql" >}}

```sql
SELECT
    floor((t.row_num - 1) / 1000) + 1 AS page_num,
    min(t._tidb_rowid) AS start_key,
    max(t._tidb_rowid) AS end_key,
    count(*) AS page_size
FROM (
    SELECT _tidb_rowid, row_number () OVER (ORDER BY _tidb_rowid) AS row_num
    FROM users
) t
GROUP BY page_num
ORDER BY page_num;
```

The query results are as follows:

```
+----------+-----------+---------+-----------+
| page_num | start_key | end_key | page_size |
+----------+-----------+---------+-----------+
|        1 |         1 |    1000 |      1000 |
|        2 |      1001 |    2000 |      1000 |
|        3 |      2001 |    3000 |      1000 |
|        4 |      3001 |    4000 |      1000 |
|        5 |      4001 |    5000 |      1000 |
|        6 |      5001 |    6000 |      1000 |
|        7 |      6001 |    7000 |      1000 |
|        8 |      7001 |    8000 |      1000 |
|        9 |      8001 |    9000 |      1000 |
|       10 |      9001 |    9990 |       990 |
+----------+-----------+---------+-----------+
10 rows in set (0.00 sec)
```

### Clustered index table

For clustered index tables (also known as "index-organized tables"), we can use the `concat` function to concatenate the values ​​of multiple columns as a key, and then use the window function to get the paging information.

It should be noted that the key is a string at this time, and you must ensure that the length of the string is always the same, in order to obtain the correct `start_key` and `end_key` in the slice through the `min` and `max` aggregation functions. If the length of the field for string concatenation is not fixed, you can use the `LPAD` function to complete it.

For example, we want to do a paged batch of the data in the `ratings` table.

We can first create the meta information table by using the following SQL statement. Because the `book_id` and `user_id` columns that make up the key are both of type `bigint`, the conversion to string is not of equal width, so we need to use the `LPAD` function to fill in the length with `0` if it is not long enough according to the maximum number of bits 19 of type `bigint`.

{{< copyable "sql" >}}

```sql
SELECT
    floor((t1.row_num - 1) / 10000) + 1 AS page_num,
    min(mvalue) AS start_key,
    max(mvalue) AS end_key,
    count(*) AS page_size
FROM (
    SELECT
        concat('(', LPAD(book_id, 19, 0), ',', LPAD(user_id, 19, 0), ')') AS mvalue,
        row_number() OVER (ORDER BY book_id, user_id) AS row_num
    FROM ratings
) t1
GROUP BY page_num
ORDER BY page_num;
```

The query results are as follows:

```
+----------+-------------------------------------------+-------------------------------------------+-----------+
| page_num | start_key                                 | end_key                                   | page_size |
+----------+-------------------------------------------+-------------------------------------------+-----------+
|        1 | (0000000000000268996,0000000000092104804) | (0000000000140982742,0000000000374645100) |     10000 |
|        2 | (0000000000140982742,0000000000456757551) | (0000000000287195082,0000000004053200550) |     10000 |
|        3 | (0000000000287196791,0000000000191962769) | (0000000000434010216,0000000000237646714) |     10000 |
|        4 | (0000000000434010216,0000000000375066168) | (0000000000578893327,0000000002167504460) |     10000 |
|        5 | (0000000000578893327,0000000002457322286) | (0000000000718287668,0000000001502744628) |     10000 |
...
|       29 | (0000000004002523918,0000000000902930986) | (0000000004147203315,0000000004090920746) |     10000 |
|       30 | (0000000004147421329,0000000000319181561) | (0000000004294004213,0000000003586311166) |      9972 |
+----------+-------------------------------------------+-------------------------------------------+-----------+
30 rows in set (0.28 sec)
```

If we want to delete all rating records on page 1, we can fill in the `start_key` and `end_key` corresponding to page 1 of the above table into the SQL statement.

{{< copyable "sql" >}}

```sql
SELECT * FROM ratings
WHERE
    (book_id, user_id) >= (268996, 92104804)
    AND (book_id, user_id) <= (140982742, 374645100)
ORDER BY book_id, user_id;
```
