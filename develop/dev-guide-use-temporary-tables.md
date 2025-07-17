---
title: 临时表
summary: 学习如何创建、查看、查询和删除临时表。
---

# 临时表

临时表可以被看作是一种重用查询结果的技术。

如果你想了解 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用中最年长作者的相关信息，可能会编写多个使用最年长作者列表的查询。

例如，你可以使用以下语句从 `authors` 表中获取前 50 位最年长的作者：

```sql
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

结果如下：

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
50 行结果（0.01 秒）
```

为了后续查询的便利，你需要缓存此查询的结果。在使用普通表存储时，应注意避免不同会话之间的表名重复问题，以及及时清理中间结果，因为这些表在批量查询后可能不再使用。

## 创建临时表

为了缓存中间结果，TiDB 在 v5.3.0 版本中引入了临时表功能。TiDB 会在会话结束后自动删除本地临时表，免除你管理因中间结果增加带来的麻烦。

### 临时表的类型

TiDB 中的临时表分为两种：本地临时表和全局临时表。

- 本地临时表：表定义和数据仅对当前会话可见。此类型适合在会话中临时存储中间数据。
- 全局临时表：表定义对整个 TiDB 集群可见，表中的数据仅对当前事务可见。此类型适合在事务中临时存储中间数据。

### 创建本地临时表

在创建本地临时表之前，你需要为当前数据库用户添加 `CREATE TEMPORARY TABLES` 权限。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

你可以使用 `CREATE TEMPORARY TABLE <table_name>` 语句创建临时表。默认类型为本地临时表，仅对当前会话可见。

```sql
CREATE TEMPORARY TABLE top_50_eldest_authors (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
);
```

创建临时表后，可以使用 `INSERT INTO table_name SELECT ...` 语句将上述查询的结果插入到刚创建的临时表中。

```sql
INSERT INTO top_50_eldest_authors
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

结果如下：

```
Query OK, 50 rows affected (0.03 sec)
Records: 50  Duplicates: 0  Warnings: 0
```

</div>
<div label="Java" value="java">

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

### 创建全局临时表

<SimpleTab groupId="language">
<div label="SQL" value="sql">

要创建全局临时表，可以添加 `GLOBAL` 关键字，并以 `ON COMMIT DELETE ROWS` 结尾，表示在当前事务结束后删除该表。

```sql
CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors_global (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

在向全局临时表插入数据时，必须显式声明事务的开始，使用 `BEGIN`。否则，数据在执行完 `INSERT INTO` 语句后会被清除。因为在自动提交模式下，`INSERT INTO` 语句执行完后事务会自动提交，事务结束时全局临时表会被清空。

</div>
<div label="Java" value="java">

在使用全局临时表时，你需要先关闭自动提交模式。在 Java 中，可以通过 `conn.setAutoCommit(false);` 来实现，并可以通过 `conn.commit();` 显式提交事务。在事务期间添加到全局临时表的数据，在事务提交或取消后会被清除。

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

## 查看临时表

使用 `SHOW [FULL] TABLES` 语句可以查看现有的全局临时表列表，但不能看到任何本地临时表。目前，TiDB 还没有类似 `information_schema.INNODB_TEMP_TABLE_INFO` 的系统表用以存储临时表信息。

例如，你可以在表列表中看到全局临时表 `top_50_eldest_authors_global`，但看不到 `top_50_eldest_authors` 表。

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
9 行结果（0.00 秒）
```

## 查询临时表

一旦临时表准备就绪，你可以像查询普通数据表一样查询它：

```sql
SELECT * FROM top_50_eldest_authors;
```

你也可以通过 [Multi-table join queries](/develop/dev-guide-join-tables.md) 引用临时表中的数据到你的查询中：

```sql
EXPLAIN SELECT ANY_VALUE(ta.id) AS author_id, ANY_VALUE(ta.age), ANY_VALUE(ta.name), COUNT(*) AS books
FROM top_50_eldest_authors ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

不同于 [view](/develop/dev-guide-use-views.md)，查询临时表会直接从临时表中获取数据，而不是执行插入时使用的原始查询。在某些情况下，这可以提升查询性能。

## 删除临时表

会话中的本地临时表在 **会话** 结束后会自动删除，包括数据和表结构。事务中的全局临时表在 **事务** 结束时会自动清空，但表结构仍然存在，需要手动删除。

要手动删除本地临时表，可以使用 `DROP TABLE` 或 `DROP TEMPORARY TABLE` 语法。例如：

```sql
DROP TEMPORARY TABLE top_50_eldest_authors;
```

要手动删除全局临时表，可以使用 `DROP TABLE` 或 `DROP GLOBAL TEMPORARY TABLE` 语法。例如：

```sql
DROP GLOBAL TEMPORARY TABLE top_50_eldest_authors_global;
```

## 限制

关于 TiDB 中临时表的限制，请参见 [Compatibility restrictions with other TiDB features](/temporary-tables.md#compatibility-restrictions-with-other-tidb-features)。

## 阅读更多

- [Temporary Tables](/temporary-tables.md)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>