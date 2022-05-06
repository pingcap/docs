---
title: Prepared Statement
summary: This page describes the TiDB prepared statement function.
---

# Prepared Statement

[Prepared statement](https://docs.pingcap.com/tidb/stable/sql-statement-prepare) is a statement that templates multiple SQL statements with only different parameters. It separates the SQL statements from the parameters. We can use it to improve our SQL statements:

- **Security**: Because parameters and statements are separated, the risk of [SQL injection](https://en.wikipedia.org/wiki/SQL_injection) attacks is avoided.
- **Performance**: Because the statement is pre-parsed on the TiDB server-side, only parameters need to be passed for subsequent execution, saving the cost of complete SQL parse, splicing SQL statement strings, and network transmission.

In most applications, SQL statements can be enumerated, and a limited number of SQL statements can be used to complete data queries for the entire application, so using prepared statement is one of the best practices.

## SQL Syntax

This section describes the SQL syntax for creating, running and deleting prepared statements.

### Create prepared statement

{{< copyable "sql" >}}

```sql
PREPARE {prepared_statement_name} FROM '{prepared_statement_sql}';
```

| Parameter Name | Description |
| :-------------------------: | :------------------------------------: |
| `{prepared_statement_name}` | Prepared statement name|
| `{prepared_statement_sql}`  | Prepared statement SQL with a question mark as a placeholder |

You can see the [PREPARE statement](https://docs.pingcap.com/tidb/stable/sql-statement-prepare) for more information.

### Use prepared statement

Prepared statements can only use **user variables** as parameters, so use the [SET statement](https://docs.pingcap.com/tidb/stable/sql-statement-set-variable) to set the variables before the [EXECUTE statement](https://docs.pingcap.com/tidb/stable/sql-statement-execute) can call the prepared statement.

{{< copyable "sql" >}}

```sql
SET @{parameter_name} = {parameter_value};
EXECUTE {prepared_statement_name} USING @{parameter_name};
```

| Parameter Name | Description |
| :-------------------------: | :-------------------------------------------------------------------: |
|     `{parameter_name}`      |                              user variables name                               |
|     `{parameter_value}`     |                              user variables value                               |
| `{prepared_statement_name}` | The name of the preprocessing statement, which must be the same as the name defined in the [create prepared statement](#create-prepared-statement) |

You can see the [EXECUTE statement](https://docs.pingcap.com/tidb/stable/sql-statement-execute) for more information.

### Delete prepared statement

{{< copyable "sql" >}}

```sql
DEALLOCATE PREPARE {prepared_statement_name};
```

| Parameter Name | Description |
| :-------------------------: | :-------------------------------------------------------------------: |
| `{prepared_statement_name}` | The name of the preprocessing statement, which must be the same as the name defined in the [create prepared statement](#create-prepared-statement) |

You can see the [DEALLOCATE statement](https://docs.pingcap.com/tidb/stable/sql-statement-deallocate) for more information.

## Example

This section uses prepared statements to complete two scenarios with examples of `SELECT` data and `INSERT` data.

### `SELECT` Example

For example, we need to query the `bookshop` application for [books](/develop/bookshop-schema-design.md#books-table) with `id` is `1`.

<SimpleTab>

<div label="SQL" href="read-sql">

{{< copyable "sql" >}}

```sql
PREPARE `books_query` FROM 'SELECT * FROM `books` WHERE `id` = ?';
```

Running result:

```
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SET @id = 1;
```

Running result:

```
Query OK, 0 rows affected (0.04 sec)
```

{{< copyable "sql" >}}

```sql
EXECUTE `books_query` USING @id;
```

Running result:

```
+---------+---------------------------------+--------+---------------------+-------+--------+
| id      | title                           | type   | published_at        | stock | price  |
+---------+---------------------------------+--------+---------------------+-------+--------+
| 1       | The Adventures of Pierce Wehner | Comics | 1904-06-06 20:46:25 |   586 | 411.66 |
+---------+---------------------------------+--------+---------------------+-------+--------+
1 row in set (0.05 sec)
```

</div>

<div label="Java" href="read-java">

{{< copyable "" >}}

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource
try (Connection connection = ds.getConnection()) {
    PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM `books` WHERE `id` = ?");
    preparedStatement.setLong(1, 1);

    ResultSet res = preparedStatement.executeQuery();
    if(!res.next()) {
        System.out.println("No books in the table with id 1");
    } else {
        // got book's info, which id is 1
        System.out.println(res.getLong("id"));
        System.out.println(res.getString("title"));
        System.out.println(res.getString("type"));
    }
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>

</SimpleTab>

### `INSERT` Example

Using the [books table](/develop/bookshop-schema-design.md#books-table) as an example, we need to insert a book with a `title` of `TiDB Developer Guide`, `type` of `Science & Technology`, `stock` of `100`, `price` of `0.0`, and `published_at` the `current time of insertion`. Note that the **primary key** of our `books` table contains the `AUTO_RANDOM` attribute, which we don't need to specify. If you are not familiar with inserting data, you can learn more about inserting data in the [Insert Data](/develop/insert-data.md) document.

<SimpleTab>

<div label="SQL" href="write-sql">

{{< copyable "sql" >}}

```sql
PREPARE `books_insert` FROM 'INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);';
```

Running result:

```
Query OK, 0 rows affected (0.03 sec)
```

{{< copyable "sql" >}}

```sql
SET @title = 'TiDB Developer Guide';
SET @type = 'Science & Technology';
SET @stock = 100;
SET @price = 0.0;
SET @published_at = NOW();
```

Running result:

```
Query OK, 0 rows affected (0.04 sec)
```

{{< copyable "sql" >}}

```sql
EXECUTE `books_insert` USING @title, @type, @stock, @price, @published_at;
```

Running result:

```
Query OK, 1 row affected (0.03 sec)
```

</div>

<div label="Java" href="write-java">

{{< copyable "" >}}

```java
try (Connection connection = ds.getConnection()) {
    String sql = "INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);";
    PreparedStatement preparedStatement = connection.prepareStatement(sql);

    preparedStatement.setString(1, "TiDB Developer Guide");
    preparedStatement.setString(2, "Science & Technology");
    preparedStatement.setInt(3, 100);
    preparedStatement.setBigDecimal(4, new BigDecimal("0.0"));
    preparedStatement.setTimestamp(5, new Timestamp(Calendar.getInstance().getTimeInMillis()));

    preparedStatement.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

As you can see, JDBC helps you control the life cycle of prepared statements without the need for you to manually use prepared statements in your application to create, use, delete, etc. However, it is worth noting that because TiDB is compatible with MySQL protocol, the default configuration for using MySQL JDBC Driver on the client-side is not to enable the **_server-side_** prepared statement option but to use the client-side prepared statement. You need to focus on the following configuration items to get support for TiDB server-side prepared statements under JDBC and the best configuration for your usage scenario:

|            Parameter            |                 Means                  |   Recommended Scenario   | Recommended Configuration|
| :------------------------: | :-----------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------: |
|    `useServerPrepStmts`    |    Whether to use the server side to enable prepared statement support    |  When you need to use a prepared statement more than once                                                             |          `true`          |
|      `cachePrepStmts`      |       Whether the client caches prepared statement        |                                                           `useServerPrepStmts=true` 时                                                            |          `true`          |
|  `prepStmtCacheSqlLimit`   |  Maximum size of a prepared statement (default 256 characters)  | When the prepared statement is greater than 256 characters | Configured according to the actual size of the prepared statement |
|    `prepStmtCacheSize`     | Maximum number of prepared statement caches (default 25) | When the number of prepared statement is greater than 25  | Configured according to the actual number of prepared statements |

A more generic scenario of JDBC connection string configuration is given here, with Host: `127.0.0.1`, Port: `4000`, User name: `root`, Password: null, Default database: `test` as an example:

```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

You can also see the [insert rows](/develop/insert-data.md#insert-rows) chapter if you need to change other JDBC parameters in the insert data scenario.

For a complete example in Java, see:

- [Build a Simple CRUD App with TiDB and Java - Using JDBC](/develop/sample-application-java.md#step-2-get-the-code)
- [Build a Simple CRUD App with TiDB and Java - Using Hibernate](/develop/sample-application-java.md#step-2-get-the-code)
- [Build the TiDB Application using Spring Boot](/develop/sample-application-spring-boot.md)

</div>

</SimpleTab>
