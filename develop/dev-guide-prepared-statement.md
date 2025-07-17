---
title: Prepared Statements
summary: 了解如何使用 TiDB 预处理语句。
---

# Prepared Statements

[prepared statement](/sql-statements/sql-statement-prepare.md) 模板化了多个 SQL 语句，其中只有参数不同。它将 SQL 语句与参数分离开来。你可以用它来改善 SQL 语句的以下方面：

- **安全性**：由于参数和语句分离，避免了 [SQL 注入](https://en.wikipedia.org/wiki/SQL_injection) 攻击的风险。
- **性能**：因为在 TiDB 服务器端提前解析了语句，后续执行时只需传递参数，节省了解析整个 SQL 语句、拼接 SQL 字符串和网络传输的开销。

在大多数应用中，SQL 语句可以枚举。你可以用有限数量的 SQL 语句完成整个应用的数据查询。因此，使用预处理语句是一种最佳实践。

## SQL 语法

本节描述创建、执行和删除预处理语句的 SQL 语法。

### 创建预处理语句

```sql
PREPARE {prepared_statement_name} FROM '{prepared_statement_sql}';
```

| 参数名称 | 描述 |
| :-------------------------: | :------------------------------------: |
| `{prepared_statement_name}` | 预处理语句的名称 |
| `{prepared_statement_sql}`  | 带有问号占位符的预处理 SQL 语句 |

更多信息请参见 [PREPARE 语句](/sql-statements/sql-statement-prepare.md)。

### 使用预处理语句

预处理语句只能使用 **用户变量** 作为参数，因此在调用 [`EXECUTE` 语句](/sql-statements/sql-statement-execute.md) 之前，需使用 [`SET` 语句](/sql-statements/sql-statement-set-variable.md) 设置变量。

```sql
SET @{parameter_name} = {parameter_value};
EXECUTE {prepared_statement_name} USING @{parameter_name};
```

| 参数名称 | 描述 |
| :-------------------------: | :-------------------------------------------------------------------: |
| `{parameter_name}` | 用户变量名 |
| `{parameter_value}` | 用户变量值 |
| `{prepared_statement_name}` | 预处理语句的名称，必须与 [创建预处理语句](#create-a-prepared-statement) 中定义的名称一致 |

更多信息请参见 [`EXECUTE` 语句](/sql-statements/sql-statement-execute.md)。

### 删除预处理语句

```sql
DEALLOCATE PREPARE {prepared_statement_name};
```

| 参数名称 | 描述 |
| :-------------------------: | :-------------------------------------------------------------------: |
| `{prepared_statement_name}` | 预处理语句的名称，必须与 [创建预处理语句](#create-a-prepared-statement) 中定义的名称一致 |

更多信息请参见 [`DEALLOCATE` 语句](/sql-statements/sql-statement-deallocate.md)。

## 示例

本节介绍两个预处理语句的示例：`SELECT` 数据和 `INSERT` 数据。

### `SELECT` 示例

例如，在 [`bookshop` 应用](/develop/dev-guide-bookshop-schema-design.md#books-table) 中，需要查询 `id = 1` 的书。

<SimpleTab groupId="language">

<div label="SQL" value="sql">

```sql
PREPARE `books_query` FROM 'SELECT * FROM `books` WHERE `id` = ?';
```

运行结果：

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
SET @id = 1;
```

运行结果：

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
EXECUTE `books_query` USING @id;
```

运行结果：

```
+---------+---------------------------------+--------+---------------------+-------+--------+
| id      | title                           | type   | published_at        | stock | price  |
+---------+---------------------------------+--------+---------------------+-------+--------+
| 1       | The Adventures of Pierce Wehner | Comics | 1904-06-06 20:46:25 |   586 | 411.66 |
+---------+---------------------------------+--------+---------------------+-------+--------+
1 row in set (0.05 sec)
```

</div>

<div label="Java" value="java">

```java
// ds 是 com.mysql.cj.jdbc.MysqlDataSource 的实体
try (Connection connection = ds.getConnection()) {
    PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM `books` WHERE `id` = ?");
    preparedStatement.setLong(1, 1);

    ResultSet res = preparedStatement.executeQuery();
    if(!res.next()) {
        System.out.println("表中没有 id 为 1 的书");
    } else {
        // 获取书的信息，id 为 1
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

### `INSERT` 示例

以 [`books` 表](/develop/dev-guide-bookshop-schema-design.md#books-table) 为例，需要插入一本书，内容为：`title = TiDB Developer Guide`，`type = Science & Technology`，`stock = 100`，`price = 0.0`，`published_at = NOW()`（插入的当前时间）。注意，在 `books` 表的 **主键** 中不需要指定 `AUTO_RANDOM` 属性。关于插入数据的更多信息，请参见 [Insert Data](/develop/dev-guide-insert-data.md)。

<SimpleTab groupId="language">

<div label="SQL" value="sql">

```sql
PREPARE `books_insert` FROM 'INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);';
```

运行结果：

```
Query OK, 0 rows affected (0.03 sec)
```

```sql
SET @title = 'TiDB Developer Guide';
SET @type = 'Science & Technology';
SET @stock = 100;
SET @price = 0.0;
SET @published_at = NOW();
```

运行结果：

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
EXECUTE `books_insert` USING @title, @type, @stock, @price, @published_at;
```

运行结果：

```
Query OK, 1 row affected (0.03 sec)
```

</div>

<div label="Java" value="java">

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

可以看到，JDBC 帮助你控制预处理语句的生命周期，你无需在应用中手动创建、使用或删除预处理语句。然而，需要注意的是，由于 TiDB 兼容 MySQL，客户端使用 MySQL JDBC Driver 时，默认配置并未启用 **_server-side_** 预处理语句选项，而是使用客户端预处理语句。

以下配置可以帮助你在 JDBC 下使用 TiDB 服务器端预处理语句：

|            参数            |                 含义                  |   推荐场景   | 推荐配置 |
| :------------------------: | :-----------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------: |
|    `useServerPrepStmts`    |    是否使用服务器端启用预处理语句    |  当你需要多次使用预处理语句时                                                             |          `true`          |
|      `cachePrepStmts`      |       客户端是否缓存预处理语句        |                                                           `useServerPrepStmts=true`                                                             |          `true`          |
|  `prepStmtCacheSqlLimit`   |  预处理语句最大长度（默认 256 字符）  | 当预处理语句长度超过 256 字符时 | 根据实际预处理语句长度配置 |
|    `prepStmtCacheSize`     |  预处理语句最大数量（默认 25 个） | 当预处理语句数量超过 25 个时  | 根据实际预处理语句数量配置 |

以下是 JDBC 连接字符串配置的典型场景示例。主机：`127.0.0.1`，端口：`4000`，用户名：`root`，密码：null，默认数据库：`test`：

```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

如果在插入数据时需要更改其他 JDBC 参数，也可以参考 [insert rows](/develop/dev-guide-insert-data.md#insert-rows)。

完整的 Java 示例请参见：

- [Connect to TiDB with JDBC](/develop/dev-guide-sample-application-java-jdbc.md)
- [Connect to TiDB with Hibernate](/develop/dev-guide-sample-application-java-hibernate.md)
- [Connect to TiDB with Spring Boot](/develop/dev-guide-sample-application-java-spring-boot.md)

</div>

</SimpleTab>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>