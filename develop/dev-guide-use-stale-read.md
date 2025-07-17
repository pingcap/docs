---
title: Stale Read
summary: 了解如何在特定条件下使用 Stale Read 来加快查询速度。
---

# Stale Read

Stale Read 是 TiDB 应用的一种机制，用于读取存储在 TiDB 中的历史版本数据。通过该机制，你可以在特定时间或指定时间范围内读取对应的历史数据，从而节省存储节点之间数据复制带来的延迟。当你使用 Stale Read 时，TiDB 会随机选择一个副本进行数据读取，这意味着所有副本都可以用于数据读取。

在实际应用中，应根据 [usage scenarios](/stale-read.md#usage-scenarios-of-stale-read) 小心考虑是否启用 Stale Read。若你的应用不能容忍读取非实时数据，则不应启用。

TiDB 提供三种级别的 Stale Read：语句级、事务级和会话级。

## 介绍

在 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用中，你可以通过以下 SQL 语句查询最新发布的图书及其价格：

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

查询结果如下：

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 100.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.02 sec)
```

此时（2022-04-20 15:20:00），“The Story of Droolius Caesar”的价格为 100.0。

同时，卖家发现该书非常受欢迎，通过以下 SQL 语句将价格提升至 150.0：

```sql
UPDATE books SET price = 150 WHERE id = 3181093216;
```

执行结果如下：

```
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

通过查询最新图书列表，可以看到该书的价格已变为 150.00。

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 150.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.01 sec)
```

如果不需要使用最新数据，可以通过 Stale Read 查询，可能返回过时数据，以避免在强一致性读取期间由数据复制引起的延迟。

假设在 Bookshop 应用中，图书的实时价格在图书列表页并不必要，只在图书详情和订单页面需要。使用 Stale Read 可以提升应用的吞吐量。

## Statement level

<SimpleTab groupId="language">
<div label="SQL" value="sql">

要在特定时间之前查询图书价格，在上述查询语句中添加 `AS OF TIMESTAMP <datetime>` 子句。

```sql
SELECT id, title, type, price FROM books AS OF TIMESTAMP '2022-04-20 15:20:00' ORDER BY published_at DESC LIMIT 5;
```

查询结果如下：

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 100.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.01 sec)
```

除了指定具体时间外，还可以使用以下方式：

- `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND` 查询 10 秒前的最新数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` 查询在 `2016-10-08 16:45:26` 和 `2016-10-08 16:45:29` 之间的最新数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() -INTERVAL 20 SECOND, NOW())` 查询在 20 秒范围内的最新数据。

注意，指定的时间戳或时间间隔不能早于或晚于当前时间。此外，`NOW()` 默认为秒级精度。若需更高精度，可添加参数，例如 `NOW(3)` 表示毫秒级。更多信息请参见 [MySQL documentation](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_now)。

过期数据会由 TiDB 中的 [Garbage Collection](/garbage-collection-overview.md) 回收，数据会在短时间内保留后被清除。该时间段称为 [GC Life Time (default 10 minutes)](/system-variables.md#tidb_gc_life_time-new-in-v50)。当 GC 开始时，当前时间减去该时间段即为 **GC Safe Point**。如果尝试读取 GC Safe Point 之前的数据，TiDB 会报错：

```
ERROR 9006 (HY000): GC life time is shorter than transaction duration...
```

如果指定的时间戳是未来时间，TiDB 会报错：

```
ERROR 9006 (HY000): cannot set read timestamp to a future time.
```

</div>
<div label="Java" value="java">

```java
public class BookDAO {

    // 省略部分代码...

    public List<Book> getTop5LatestBooksWithStaleRead(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("""
            SELECT id, title, type, price FROM books AS OF TIMESTAMP NOW() - INTERVAL ? SECOND ORDER BY published_at DESC LIMIT 5;
            """);
            stmt.setInt(1, seconds);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }
        } catch (SQLException e) {
            if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 1105) {
                System.out.println("WARN: cannot set read timestamp to a future time.");
            } else if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 9006) {
                System.out.println("WARN: GC life time is shorter than transaction duration.");
            } else {
                throw e;
            }
        }
        return books;
    }
}
```

```java
List<Book> top5LatestBooks = bookDAO.getTop5LatestBooks();

if (top5LatestBooks.size() > 0) {
    System.out.println("The latest book price (before update): " + top5LatestBooks.get(0).getPrice());

    Book book = top5LatestBooks.get(0);
    bookDAO.updateBookPriceByID(book.getId(), book.price + 10);

    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after update): " + top5LatestBooks.get(0).getPrice());

    // 使用过期数据读取（stale read）。
    top5LatestBooks = bookDAO.getTop5LatestBooksWithStaleRead(5);
    System.out.println("The latest book price (maybe stale): " + top5LatestBooks.get(0).getPrice());

    // 在事务提交后，再次读取最新数据。
    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after the transaction commit): " + top5LatestBooks.get(0).getPrice());
}
```

输出结果如下：

```
The latest book price (before update): 100.00
The latest book price (after update): 150.00
The latest book price (maybe stale): 100.00
The latest book price (after the transaction commit): 150
```

</div>
</SimpleTab>

通过 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 语句，可以将开启的事务或下一次事务设置为基于指定历史时间的只读事务。事务将读取基于提供的历史时间的历史数据。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

例如，可以使用以下 `AS OF TIMESTAMP` 语句，将正在进行的事务切换为只读模式，并读取 5 秒前的历史数据。

```sql
SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

</div>
<div label="Java" value="java">

你可以定义一个事务助手类，将启用事务级 Stale Read 的命令封装为辅助方法。

```java
public static class TxnHelper {

    public static void setTxnWithStaleRead(Connection conn, Integer seconds) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL ? SECOND;"
        );
        stmt.setInt(1, seconds);
        stmt.execute();
    }

}
```

然后在 `BookDAO` 类中定义一个方法，通过事务启用 Stale Read 功能。使用该方法进行查询，而不是在查询语句中添加 `AS OF TIMESTAMP`。

```java
public class BookDAO {

    // 省略部分代码...

    public List<Book> getTop5LatestBooksWithTxnStaleRead(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            // 开启只读事务。
            TxnHelper.setTxnWithStaleRead(conn, seconds);

            // 设置事务为只读。
            conn.setAutoCommit(false);

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
            """);
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }

            // 提交事务。
            conn.commit();
        } catch (SQLException e) {
            if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 1105) {
                System.out.println("WARN: cannot set read timestamp to a future time.");
            } else if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 9006) {
                System.out.println("WARN: GC life time is shorter than transaction duration.");
            } else {
                throw e;
            }
        }
        return books;
    }
}
```

</div>
</SimpleTab>

## Session level

为了支持读取历史数据，TiDB 自 v5.4 版本起引入了新的系统变量 `tidb_read_staleness`，你可以用它设置当前会话允许读取的历史数据范围。其数据类型为 `int`，作用域为 `SESSION`。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在会话中启用 Stale Read：

```sql
SET @@tidb_read_staleness="-5";
```

例如，如果设置为 `-5`，且 TiKV 或 TiFlash 存在对应的历史数据，TiDB 会在 5 秒的时间范围内选择尽可能接近当前时间的时间戳。

在会话中禁用 Stale Read：

```sql
set @@tidb_read_staleness="";
```

</div>
<div label="Java" value="java">

```java
public static class StaleReadHelper{

    public static void enableStaleReadOnSession(Connection conn, Integer seconds) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET @@tidb_read_staleness= ?;"
        );
        stmt.setString(1, String.format("-%d", seconds));
        stmt.execute();
    }

    public static void disableStaleReadOnSession(Connection conn) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET @@tidb_read_staleness=\"\";"
        );
        stmt.execute();
    }

}
```

</div>
</SimpleTab>

## 阅读更多

- [Usage Scenarios of Stale Read](/stale-read.md)
- [Read Historical Data Using the `AS OF TIMESTAMP` Clause](/as-of-timestamp.md)
- [Read Historical Data Using the `tidb_read_staleness` System Variable](/tidb-read-staleness.md)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>