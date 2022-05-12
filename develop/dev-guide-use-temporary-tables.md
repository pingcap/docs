---
title: Temporary Tables
---

# Temporary Tables

Temporary tables can be thought of as a technique for reusing query results.

Suppose we want to know something about the eldest authors in the [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application, we may need to write multiple queries that use this list of eldest authors.

We can use the following SQL statement to find the top 50 eldest authors from the `authors` table for our research.

{{< copyable "sql" >}}

```sql
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

The query results are as follows:

```
+------------+---------------------+------+
| id         | name                | age  |
+------------+---------------------+------+
| 4053452056 | Dessie Thompson     |   80 |
| 2773958689 | Pedro Hansen        |   80 |
| 4005636688 | Wyatt Keeling       |   80 |
| 3621155838 | Colby Parker        |   80 |
| 2738876051 | Friedrich Hagenes   |   80 |
| 2299112019 | Ray Macejkovic      |   80 |
| 3953661843 | Brandi Williamson   |   80 |
...
| 4100546410 | Maida Walsh         |   80 |
+------------+---------------------+------+
50 rows in set (0.01 sec)
```

After finding the 50 oldest authors, we want to cache the results of this query so that subsequent queries can easily use this set of data. If we use general database tables for storage, when creating these tables, we need to consider how to avoid the problem of table name duplication between different sessions, and we may no longer need these tables after a batch of queries. We also need to be cleaned up the intermediate result tables timely.

## Create a temporary table

In order to meet the demand of caching intermediate results, TiDB has introduced the temporary table feature in v5.3.0. For the local temporary tables, TiDB will help us to clean up these useless temporary tables automatically after the session ends for a period of time, so users don't need to worry about the management trouble caused by the increase of intermediate result tables.

### Temporary table type

TiDB's temporary tables are divided into local temporary tables and global temporary tables.

- The table schema and data within the local temporary table are only visible to the current session and are suitable for staging intermediate data within the session.
- The table schema of the global temporary table is visible to the entire TiDB cluster, but the data is visible only to the current transaction, which is suitable for intermediate data in the transaction.

### Create a local temporary table

Before creating a local temporary table, you need to add `CREATE TEMPORARY TABLES` permission to the current database user.

<SimpleTab>
<div label="SQL" href="local-sql">

Temporary tables are created through the `CREATE TEMPORARY TABLE <table_name>` statement. The default temporary table type is local temporary table, which can only be accessed by the current session.

{{< copyable "sql" >}}

```sql
CREATE TEMPORARY TABLE top_50_eldest_authors (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
);
```

After creating the temporary table, you can use the `INSERT INTO table_name SELECT ...` statement to import the results of the above query into the temporary table you just created.

{{< copyable "sql" >}}

```sql
INSERT INTO top_50_eldest_authors
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

```
Query OK, 50 rows affected (0.03 sec)
Records: 50  Duplicates: 0  Warnings: 0
```

</div>
<div label="Java" href="local-java">

{{< copyable "java" >}}

```java
public List<Author> getTop50EldestAuthorInfo() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        stmt.executeUpdate("""
            CREATE TEMPORARY TABLE top_50_eldest_authors (
                id BIGINT,
                name VARCHAR(255),
                age INT,
                PRIMARY KEY(id)
            );
        """);

        stmt.executeUpdate("""
            INSERT INTO top_50_eldest_authors
            SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
            FROM authors a
            ORDER BY age DESC
            LIMIT 50;
        """);

        ResultSet rs = stmt.executeQuery("""
            SELECT id, name FROM top_50_eldest_authors;
        """);

        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

### Create a global temporary table

<SimpleTab>
<div label="SQL" href="global-sql">

You can declare that you are creating a global temporary table by adding the `GLOBAL` keyword. When creating a global temporary table, it must be decorated with `ON COMMIT DELETE ROWS` at the end, which indicates that all data rows of the this table will be deleted after the transaction ends.

{{< copyable "sql" >}}

```sql
CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors_global (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

When importing data to global temporary tables, you need to pay special attention, you must explicitly declare the start of the transaction via `BEGIN`. Otherwise, the imported data will be cleared after the `INSERT INTO` statement is executed, because in auto commit mode, the transaction is automatically committed at the end of the execution of the `INSERT INTO` statement, and the global temporary table is cleared when the transaction is finished.

</div>
<div label="Java" href="global-java">

When using global temporary tables, you need to turn off Auto Commit mode first. In Java, you can do this with the `conn.setAutoCommit(false);` statement, and when you are done using it, you can commit the transaction explicitly with `conn.commit();`. The data added to the global temporary table during the transaction will be cleared after the transaction is committed or cancelled.

{{< copyable "java" >}}

```java
public List<Author> getTop50EldestAuthorInfo() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        conn.setAutoCommit(false);

        Statement stmt = conn.createStatement();
        stmt.executeUpdate("""
            CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors (
                id BIGINT,
                name VARCHAR(255),
                age INT,
                PRIMARY KEY(id)
            ) ON COMMIT DELETE ROWS;
        """);

        stmt.executeUpdate("""
            INSERT INTO top_50_eldest_authors
            SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
            FROM authors a
            ORDER BY age DESC
            LIMIT 50;
        """);

        ResultSet rs = stmt.executeQuery("""
            SELECT id, name FROM top_50_eldest_authors;
        """);

        conn.commit();
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

## View temporary table information

Through the `SHOW [FULL] TABLES` statement, you can view the created global temporary table, but you cannot see the information of the local temporary table. For now, TiDB does not have a similar `information_schema.INNODB_TEMP_TABLE_INFO` system table for storing temporary table information.

For example, you can see the global temporary table `top_50_eldest_authors_global` in the table list, but not the `top_50_eldest_authors` table.

```
+-------------------------------+------------+
| Tables_in_bookshop            | Table_type |
+-------------------------------+------------+
| authors                       | BASE TABLE |
| book_authors                  | BASE TABLE |
| books                         | BASE TABLE |
| orders                        | BASE TABLE |
| ratings                       | BASE TABLE |
| top_50_eldest_authors_global  | BASE TABLE |
| users                         | BASE TABLE |
+-------------------------------+------------+
9 rows in set (0.00 sec)
```

## Query temporary table

Once the temporary table is ready, you can query the temporary table as if it were a normal data table.

{{< copyable "sql" >}}

```sql
SELECT * FROM top_50_eldest_authors;
```

You can reference data from temporary tables to your query via [join-tables](/develop/dev-guide-join-tables.md).

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT ANY_VALUE(ta.id) AS author_id, ANY_VALUE(ta.age), ANY_VALUE(ta.name), COUNT(*) AS books
FROM top_50_eldest_authors ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

Unlike [views](/develop/dev-guide-use-views.md), when querying a temporary table, instead of executing the original query used to import the data, you will get the data directly from the temporary table. In some cases, this will help you improve the efficiency of your queries.

## Drop temporary table

Local temporary tables are automatically purged after the **session** ends, along with both data and table structures. Global temporary tables are automatically purged of data at the end of a **session**, but the table structure remains and needs to be deleted manually.

To manually drop local temporary tables, use the `DROP TABLE` or `DROP TEMPORARY TABLE` syntax. For example:

{{< copyable "sql" >}}

```sql
DROP TEMPORARY TABLE top_50_eldest_authors;
```

To manually drop global temporary tables, use the `DROP TABLE` or `DROP GLOBAL TEMPORARY TABLE` syntax. For example:

{{< copyable "sql" >}}

```sql
DROP GLOBAL TEMPORARY TABLE top_50_eldest_authors_global;
```

## Limitation

To learn about the limitations of TiDB's temporary table feature, you can read the [Compatibility restrictions with other TiDB features](/temporary-tables.md#compatibility-restrictions-with-other-tidb-features) section in the reference documents.

## Read more

- [Temporary Tables](/temporary-tables.md)
