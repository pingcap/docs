---
title: 乐观事务与悲观事务
summary: 了解 TiDB 中的乐观事务和悲观事务。
---

# 乐观事务与悲观事务

[乐观事务](/optimistic-transaction.md) 模型直接提交事务，遇到冲突时回滚。相对地，[悲观事务](/pessimistic-transaction.md) 模型在实际提交事务之前，尝试锁定需要修改的资源，确保事务可以成功执行后才开始提交。

乐观事务模型适用于冲突率较低的场景，因为直接提交成功的概率较高。但一旦发生事务冲突，回滚的成本相对较高。

悲观事务模型的优势在于，对于冲突率较高的场景，提前加锁的成本小于之后的回滚成本。此外，它可以解决多个并发事务因冲突而无法提交的问题。然而，在冲突率低的场景中，悲观事务的效率不及乐观事务。

悲观事务模型更直观，且在应用端实现较为容易。乐观事务模型则需要复杂的应用端重试机制。

以下以[书店](/develop/dev-guide-bookshop-schema-design.md)为例，使用买书的场景，展示乐观和悲观事务的优缺点。买书的流程主要包括：

1. 更新库存数量
2. 创建订单
3. 付款

这些操作必须全部成功或全部失败。在并发事务的情况下，必须确保不会出现超卖。

## 悲观事务

以下代码使用两个线程模拟两个用户在悲观事务模式下购买同一本书的过程。书店剩余 10 本书。Bob 购买 6 本，Alice 购买 4 本。他们几乎同时完成订单，导致库存中的所有书都售罄。

<SimpleTab groupId="language">

<div label="Java" value="java">

因为你使用多个线程模拟多个用户同时插入数据的场景，所以需要使用支持多线程的连接对象。这里用 Java 常用的连接池 [HikariCP](https://github.com/brettwooldridge/HikariCP) 作为示例。

</div>

<div label="Golang" value="golang">

Golang 中的 `sql.DB` 是并发安全的，因此无需导入第三方包。

为了适配 TiDB 事务，按照以下代码编写工具包 [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)：

```go
package util

import (
    "context"
    "database/sql"
)

type TiDBSqlTx struct {
    *sql.Tx
    conn        *sql.Conn
    pessimistic bool
}

func TiDBSqlBegin(db *sql.DB, pessimistic bool) (*TiDBSqlTx, error) {
    ctx := context.Background()
    conn, err := db.Conn(ctx)
    if err != nil {
        return nil, err
    }
    if pessimistic {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "pessimistic")
    } else {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "optimistic")
    }
    if err != nil {
        return nil, err
    }
    tx, err := conn.BeginTx(ctx, nil)
    if err != nil {
        return nil, err
    }
    return &TiDBSqlTx{
        conn:        conn,
        Tx:          tx,
        pessimistic: pessimistic,
    }, nil
}

func (tx *TiDBSqlTx) Commit() error {
    defer tx.conn.Close()
    return tx.Tx.Commit()
}

func (tx *TiDBSqlTx) Rollback() error {
    defer tx.conn.Close()
    return tx.Tx.Rollback()
}
```

</div>

<div label="Python" value="python">

为了保证线程安全，可以使用 mysqlclient 驱动打开多个连接，这些连接不会在不同线程间共享。

</div>

</SimpleTab>

### 编写悲观事务示例

<SimpleTab groupId="language">

<div label="Java" value="java">

**配置文件**

如果你用 Maven 管理包，在 `pom.xml` 的 `<dependencies>` 节点中添加以下依赖，引入 `HikariCP`，并设置打包目标和 JAR 包启动的主类。以下为 `pom.xml` 示例。

```xml
<?xml version="1.0" encoding="UTF-8"?>

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.pingcap</groupId>
  <artifactId>plain-java-txn</artifactId>
  <version>0.0.1</version>

  <name>plain-java-jdbc</name>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
  </properties>

  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.13.2</version>
      <scope>test</scope>
    </dependency>

    <!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
    <dependency>
      <groupId>mysql</groupId>
      <artifactId>mysql-connector-java</artifactId>
      <version>8.0.28</version>
    </dependency>

    <dependency>
      <groupId>com.zaxxer</groupId>
      <artifactId>HikariCP</artifactId>
      <version>5.0.1</version>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-assembly-plugin</artifactId>
        <version>3.3.0</version>
        <configuration>
          <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
          </descriptorRefs>
          <archive>
            <manifest>
              <mainClass>com.pingcap.txn.TxnExample</mainClass>
            </manifest>
          </archive>

        </configuration>
        <executions>
          <execution>
            <id>make-assembly</id>
            <phase>package</phase>
            <goals>
              <goal>single</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>

</project>
```

**编码**

然后编写代码：

```java
package com.pingcap.txn;

import com.zaxxer.hikari.HikariDataSource;

import java.math.BigDecimal;
import java.sql.*;
import java.util.Arrays;
import java.util.concurrent.*;

public class TxnExample {
    public static void main(String[] args) throws SQLException, InterruptedException {
        System.out.println(Arrays.toString(args));
        int aliceQuantity = 0;
        int bobQuantity = 0;

        for (String arg: args) {
            if (arg.startsWith("ALICE_NUM")) {
                aliceQuantity = Integer.parseInt(arg.replace("ALICE_NUM=", ""));
            }

            if (arg.startsWith("BOB_NUM")) {
                bobQuantity = Integer.parseInt(arg.replace("BOB_NUM=", ""));
            }
        }

        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:mysql://localhost:4000/bookshop?useServerPrepStmts=true&cachePrepStmts=true");
        ds.setUsername("root");
        ds.setPassword("");

        // 准备数据
        Connection connection = ds.getConnection();
        createBook(connection, 1L, "Designing Data-Intensive Application", "Science & Technology",
                Timestamp.valueOf("2018-09-01 00:00:00"), new BigDecimal(100), 10);
        createUser(connection, 1L, "Bob", new BigDecimal(10000));
        createUser(connection, 2L, "Alice", new BigDecimal(10000));

        CountDownLatch countDownLatch = new CountDownLatch(2);
        ExecutorService threadPool = Executors.newFixedThreadPool(2);

        final int finalBobQuantity = bobQuantity;
        threadPool.execute(() -> {
            buy(ds, 1, 1000L, 1L, 1L, finalBobQuantity);
            countDownLatch.countDown();
        });
        final int finalAliceQuantity = aliceQuantity;
        threadPool.execute(() -> {
            buy(ds, 2, 1001L, 1L, 2L, finalAliceQuantity);
            countDownLatch.countDown();
        });

        countDownLatch.await(5, TimeUnit.SECONDS);
    }

    public static void createUser(Connection connection, Long id, String nickname, BigDecimal balance) throws SQLException  {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (?, ?, ?)");
        insert.setLong(1, id);
        insert.setString(2, nickname);
        insert.setBigDecimal(3, balance);
        insert.executeUpdate();
    }

    public static void createBook(Connection connection, Long id, String title, String type, Timestamp publishedAt, BigDecimal price, Integer stock) throws SQLException {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `books` (`id`, `title`, `type`, `published_at`, `price`, `stock`) values (?, ?, ?, ?, ?, ?)");
        insert.setLong(1, id);
        insert.setString(2, title);
        insert.setString(3, type);
        insert.setTimestamp(4, publishedAt);
        insert.setBigDecimal(5, price);
        insert.setInt(6, stock);

        insert.executeUpdate();
    }

    public static void buy (HikariDataSource ds, Integer threadID, Long orderID, Long bookID,
                            Long userID, Integer quantity) {
        String txnComment = "/* txn " + threadID + " */ ";

        try (Connection connection = ds.getConnection()) {
            try {

                connection.setAutoCommit(false);
                connection.createStatement().executeUpdate(txnComment + "begin optimistic");

                // 等待其他线程执行完 'begin optimistic' 语句
                TimeUnit.SECONDS.sleep(1);

                BigDecimal price = null;

                // 读取书的价格
                PreparedStatement selectBook = connection.prepareStatement(txnComment + "SELECT `price`, `stock` FROM books where id = ? for update");
                selectBook.setLong(1, bookID);
                ResultSet res = selectBook.executeQuery();
                if (!res.next()) {
                    throw new RuntimeException("book not exist");
                } else {
                    price = res.getBigDecimal("price");
                    int stock = res.getInt("stock");
                    if (stock < quantity) {
                        throw new RuntimeException("book not enough");
                    }
                }

                // 更新书的库存
                String updateBookSQL = "update `books` set stock = stock - ? where id = ? and stock - ? >= 0";
                PreparedStatement updateBook = connection.prepareStatement(txnComment + updateBookSQL);
                updateBook.setInt(1, quantity);
                updateBook.setLong(2, bookID);
                updateBook.setInt(3, quantity);
                updateBook.executeUpdate();

                // 插入订单
                String insertOrderSQL = "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (?, ?, ?, ?)";
                PreparedStatement insertOrder = connection.prepareStatement(txnComment + insertOrderSQL);
                insertOrder.setLong(1, orderID);
                insertOrder.setLong(2, bookID);
                insertOrder.setLong(3, userID);
                insertOrder.setInt(4, quantity);
                insertOrder.executeUpdate();

                // 更新用户余额
                String updateUserSQL = "update `users` set `balance` = `balance` - ? where id = ?";
                PreparedStatement updateUser = connection.prepareStatement(txnComment + updateUserSQL);
                updateUser.setBigDecimal(1, price.multiply(new BigDecimal(quantity)));
                updateUser.setLong(2, userID);
                updateUser.executeUpdate();

                connection.createStatement().executeUpdate(txnComment + "commit");
            } catch (Exception e) {
                connection.createStatement().executeUpdate(txnComment + "rollback");
                e.printStackTrace();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

</div>

<div label="Golang" value="golang">

在 [写悲观事务示例](#write-a-pessimistic-transaction-example) 部分的 Golang 示例已支持乐观事务，无需修改即可直接使用。

</div>

<div label="Python" value="python">

在 [写悲观事务示例](#write-a-pessimistic-transaction-example) 部分的 Python 示例已支持乐观事务，无需修改即可直接使用。

</div>

</SimpleTab>

### 不涉及超卖的示例

运行示例程序：

<SimpleTab groupId="language">

<div label="Java" value="java">

```shell
mvn clean package
java -jar target/plain-java-txn-0.0.1-jar-with-dependencies.jar ALICE_NUM=4 BOB_NUM=6
```

</div>

<div label="Golang" value="golang">

```shell
go build -o bin/txn
./bin/txn -a 4 -b 6
```

</div>

<div label="Python" value="python">

```shell
OPTIMISTIC=False ALICE=4 BOB=6 python3 txn_example.py
```

</div>

</SimpleTab>

SQL 日志：

```sql
/* txn 1 */ BEGIN PESSIMISTIC
    /* txn 2 */ BEGIN PESSIMISTIC
    /* txn 2 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
    /* txn 2 */ UPDATE `books` SET `stock` = `stock` - 4 WHERE `id` = 1 AND `stock` - 4 >= 0
    /* txn 2 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1001, 1, 1, 4)
    /* txn 2 */ UPDATE `users` SET `balance` = `balance` - 400.0 WHERE `id` = 2
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
/* txn 1 */ UPDATE `books` SET `stock` = `stock` - 6 WHERE `id` = 1 AND `stock` - 6 >= 0
/* txn 1 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1000, 1, 1, 6)
/* txn 1 */ UPDATE `users` SET `balance` = `balance` - 600.0 WHERE `id` = 1
retry 1 times for 9007 Write conflict, txnStartTS=432618733006225412, conflictStartTS=432618733006225411, conflictCommitTS=432618733006225414, key={tableID=126, handle=1} primary={tableID=114, indexID=1, indexValues={1, 1000, }} [try again later]
/* txn 1 */ BEGIN OPTIMISTIC
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
/* txn 1 */ UPDATE `books` SET `stock` = `stock` - 6 WHERE `id` = 1 AND `stock` - 6 >= 0
/* txn 1 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1000, 1, 1, 6)
/* txn 1 */ UPDATE `users` SET `balance` = `balance` - 600.0 WHERE `id` = 1
/* txn 1 */ COMMIT
```

可以看到，在乐观事务模式下，由于中间状态不一定正确，不能像悲观事务那样通过 `affected_rows` 判断语句是否成功执行。需要将整个事务作为一个整体，通过检查最后的 `COMMIT` 是否抛出异常，来判断是否存在写冲突。

从上述 SQL 日志可以看出，由于两个事务并发执行且修改了相同的记录，`txn 1` 提交后抛出 `9007 Write conflict` 异常。对于乐观事务中的写冲突，可以在应用端安全重试。重试一次后，数据成功提交。最终执行结果符合预期：

```sql
mysql> SELECT * FROM books;
+----+--------------------------------------+----------------------+---------------------+-------+--------+
| id | title                                | type                 | published_at        | stock | price  |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
|  1 | Designing Data-Intensive Application | Science & Technology | 2018-09-01 00:00:00 |     0 | 100.00 |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
1 row in set (0.01 sec)

mysql> SELECT * FROM orders;
+------+---------+---------+---------+---------------------+
| id   | book_id | user_id | quality | ordered_at          |
+------+---------+---------+---------+---------------------+
| 1000 |       1 |       1 |       6 | 2022-04-19 03:18:19 |
| 1001 |       1 |       1 |       4 | 2022-04-19 03:18:17 |
+------+---------+---------+---------+---------------------+
2 rows in set (0.01 sec)

mysql> SELECT * FROM users;
+----+---------+----------+
| id | balance | nickname |
+----+---------+----------+
|  1 | 9400.00 | Bob      |
|  2 | 9600.00 | Alice    |
+----+---------+----------+
2 rows in set (0.00 sec)
```

### 不涉及超卖的示例

本节描述一个防止超卖的乐观事务示例。假设库存剩余 10 本。Bob 购买 7 本，Alice 购买 4 本，几乎同时下单。会发生什么？你可以复用之前的乐观事务代码，只需将 Bob 的购买数量由 6 改为 7。

运行示例程序：

<SimpleTab groupId="language">

<div label="Java" value="java">

```shell
mvn clean package
java -jar target/plain-java-txn-0.0.1-jar-with-dependencies.jar ALICE_NUM=4 BOB_NUM=7
```

</div>

<div label="Golang" value="golang">

```shell
go build -o bin/txn
./bin/txn -a 4 -b 7 -o true
```

</div>

<div label="Python" value="python">

```shell
OPTIMISTIC=True ALICE=4 BOB=7 python3 txn_example.py
```

</div>

</SimpleTab>

```sql
/* txn 1 */ BEGIN OPTIMISTIC
    /* txn 2 */ BEGIN OPTIMISTIC
    /* txn 2 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
    /* txn 2 */ UPDATE `books` SET `stock` = `stock` - 4 WHERE `id` = 1 AND `stock` - 4 >= 0
    /* txn 2 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1001, 1, 1, 4)
    /* txn 2 */ UPDATE `users` SET `balance` = `balance` - 400.0 WHERE `id` = 2
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
/* txn 1 */ UPDATE `books` SET `stock` = `stock` - 7 WHERE `id` = 1 AND `stock` - 7 >= 0
/* txn 1 */ ROLLBACK
```

由于 `txn 2` 预先获取了锁资源并更新了库存，`affected_rows` 在 `txn 1` 中的返回值为 0，进入了 `rollback` 流程。

让我们检查订单创建、用户余额扣减和库存扣减情况。Alice 成功订购了 4 本，Bob 由于库存不足未能订购 7 本，剩余 6 本库存符合预期。

```sql
mysql> SELECT * FROM books;
+----+--------------------------------------+----------------------+---------------------+-------+--------+
| id | title                                | type                 | published_at        | stock | price  |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
|  1 | Designing Data-Intensive Application | Science & Technology | 2018-09-01 00:00:00 |     6 | 100.00 |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
1 row in set (0.00 sec)

mysql> SELECT * FROM orders;
+------+---------+---------+---------+---------------------+
| id   | book_id | user_id | quality | ordered_at          |
+------+---------+---------+---------+---------------------+
| 1001 |       1 |       1 |       4 | 2022-04-19 11:03:03 |
+------+---------+---------+---------+---------------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM users;
+----+----------+----------+
| id | balance  | nickname |
+----+----------+----------+
|  1 | 10000.00 | Bob      |
|  2 |  9600.00 | Alice    |
+----+----------+----------+
2 rows in set (0.01 sec)
```