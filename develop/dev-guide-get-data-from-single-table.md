---
title: Get Data from Single Table
---

<!-- markdownlint-disable MD029 -->

# Get Data from Single Table

In this chapter, we will begin to explain how to use SQL and various programming languages to query data in TiDB.

## Before you begin

Next, we will introduce the data query section of TiDB around the [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application.

Before reading this chapter, you need to do the following:

1. Build a TiDB cluster (recommended to use [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md) or [TiUP](/production-deployment-using-tiup.md)).
2. [Import table schema and sample data of Bookshop application](/develop/dev-guide-bookshop-schema-design.md#import-table-structures-and-data).
3. [Connect to TiDB](/develop/dev-guide-connect-to-tidb.md).

## A simple query

In the database of the Bookshop application, the `authors` table stores the basic information of writers. We can use the `SELECT ... FROM ...` statement retrieves data from the database.

<SimpleTab>
<div label="SQL" href="simple-sql">

In a client such as MySQL Client, you can input and execute the following SQL statement:

{{< copyable "sql" >}}

```sql
SELECT id, name FROM authors;
```

The output results are as follows:

```
+------------+--------------------------+
| id         | name                     |
+------------+--------------------------+
|       6357 | Adelle Bosco             |
|     345397 | Chanelle Koepp           |
|     807584 | Clementina Ryan          |
|     839921 | Gage Huel                |
|     850070 | Ray Armstrong            |
|     850362 | Ford Waelchi             |
|     881210 | Jayme Gutkowski          |
|    1165261 | Allison Kuvalis          |
|    1282036 | Adela Funk               |
...
| 4294957408 | Lyla Nitzsche            |
+------------+--------------------------+
20000 rows in set (0.05 sec)
```

</div>
<div label="Java" href="simple-java">

In the Java language, we define how to store the author's basic information by declaring a `Author` class. We can select the appropriate data type according to the [type](/data-type-overview.md) and [value range](https://docs.pingcap.com/zh/tidb/stable/data-type-numeric) of the data in the database, to store the corresponding data in the Java language, for example:

- Use a variable of type `Int` to store data of type `int`.
- Use a variable of type `Long` to store data of type `bigint`.
- Use `Short` type variable to store data of type `tinyint`.
- Use a variable of type `String` to store data of type `varchar`.
- ...

{{< copyable "java" >}}

```java
public class Author {
    private Long id;
    private String name;
    private Short gender;
    private Short birthYear;
    private Short deathYear;

    public Author() {}

     // Skip the getters and setters.
}
```

{{< copyable "java" >}}

```java
public class AuthorDAO {

    // Omit initialization of instance variables...

    public List<Author> getAuthors() throws SQLException {
        List<Author> authors = new ArrayList<>();

        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT id, name FROM authors");
            while (rs.next()) {
                Author author = new Author();
                author.setId( rs.getLong("id"));
                author.setName(rs.getString("name"));
                authors.add(author);
            }
        }
        return authors;
    }
}
```

- After [getting the database connection](/develop/dev-guide-connect-to-tidb.md#jdbc), you can create a `Statement` instance object using the `conn.createStatus()` statement.
- Then call the `stmt.executeQuery("query_sql")` method to initiate a database query request to TiDB.
- The query results return by the database will be stored in `ResultSet` object. By traversing the `ResultSet` object, the return result can be mapped to the `Author` class object prepared earlier.

</div>
</SimpleTab>

## Filter results

The query got a lot of results, but not all of them were what we wanted? We can filter the results of the query with the `WHERE` statement to find the part we want to query.

For example, we want to find the writers born in 1998 among a lot of writers:

<SimpleTab>
<div label="SQL" href="filter-sql">

We can add filter conditions in the `WHERE` clause:

{{< copyable "sql" >}}

```sql
SELECT * FROM authors WHERE birth_year = 1998;
```

</div>
<div label="Java" href="filter-java">

For Java programs, we want to use the same SQL to handle data query request with dynamic parameters.

Splicing parameters into a SQL statement may be a method, but it is not a good idea, as it poses a potential [SQL Injection](https://en.wikipedia.org/wiki/SQL_injection) risk to our application.

When dealing with such queries, we should use [preparedStatement](/develop/dev-guide-prepared-statement.md) instead of a normal Statement.

{{< copyable "java" >}}

```java
public List<Author> getAuthorsByBirthYear(Short birthYear) throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        PreparedStatement stmt = conn.prepareStatement("""
        SELECT * FROM authors WHERE birth_year = ?;
        """);
        stmt.setShort(1, birthYear);
        ResultSet rs = stmt.executeQuery();
        while (rs.next()) {
            Author author = new Author();
            author.setId( rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

## Sorting results

Using the `ORDER BY` statement can make the query results sort in the way we expect.

For example, we can use the following SQL statement to sort the `authors` table in descending order (`DESC`) according to the `birth_year` column to get a list of the youngest authors.

{{< copyable "sql" >}}

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC;
```

The query results are as follows:

```
+-----------+------------------------+------------+
| id        | name                   | birth_year |
+-----------+------------------------+------------+
| 83420726  | Terrance Dach          | 2000       |
| 57938667  | Margarita Christiansen | 2000       |
| 77441404  | Otto Dibbert           | 2000       |
| 61338414  | Danial Cormier         | 2000       |
| 49680887  | Alivia Lemke           | 2000       |
| 45460101  | Itzel Cummings         | 2000       |
| 38009380  | Percy Hodkiewicz       | 2000       |
| 12943560  | Hulda Hackett          | 2000       |
| 1294029   | Stanford Herman        | 2000       |
| 111453184 | Jeffrey Brekke         | 2000       |
...
300000 rows in set (0.23 sec)
```

## Limit the number of query results

If we want TiDB to return only partial results, we can use the `LIMIT` statement to limit the number of records return by the query result.

{{< copyable "java" >}}

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC
LIMIT 10;
```

The query results are as follows:

```
+-----------+------------------------+------------+
| id        | name                   | birth_year |
+-----------+------------------------+------------+
| 83420726  | Terrance Dach          | 2000       |
| 57938667  | Margarita Christiansen | 2000       |
| 77441404  | Otto Dibbert           | 2000       |
| 61338414  | Danial Cormier         | 2000       |
| 49680887  | Alivia Lemke           | 2000       |
| 45460101  | Itzel Cummings         | 2000       |
| 38009380  | Percy Hodkiewicz       | 2000       |
| 12943560  | Hulda Hackett          | 2000       |
| 1294029   | Stanford Herman        | 2000       |
| 111453184 | Jeffrey Brekke         | 2000       |
+-----------+------------------------+------------+
10 rows in set (0.11 sec)
```

By observing the query results, you can see that after using the `LIMIT` statement, the query time is significantly shortened. This is the result of TiDB's optimization of the LIMIT clause. You can push down [TopN and Limit](/topn-limit-push-down.md) for more details.

## Aggregate Queries

If you want to focus on the data as a whole rather than a portion of the data, you can use the `GROUP BY` statement with the aggregate function to construct an aggregate query to help you have a better understanding of the overall situation of the data.

For example, if you want to know which years have more writers born, you can group the basic information of writers according to the `birth_year` column, and then count the number of writers born in that year separately:

{{< copyable "java" >}}

```sql
SELECT birth_year, COUNT (DISTINCT id) AS author_count
FROM authors
GROUP BY birth_year
ORDER BY author_count DESC;
```

The query results are as follows:

```
+------------+--------------+
| birth_year | author_count |
+------------+--------------+
|       1932 |          317 |
|       1947 |          290 |
|       1939 |          282 |
|       1935 |          289 |
|       1968 |          291 |
|       1962 |          261 |
|       1961 |          283 |
|       1986 |          289 |
|       1994 |          280 |
...
|       1972 |          306 |
+------------+--------------+
71 rows in set (0.00 sec)
```

In addition to the `COUNT` function, TiDB also supports many useful aggregate functions. You can do this by checking the [Aggregate (GROUP BY) Functions](/functions-and-operators/aggregate-group-by-functions.md) section to learn more.
