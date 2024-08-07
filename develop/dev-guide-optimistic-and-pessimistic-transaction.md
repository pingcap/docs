---
title: Optimistic Transactions and Pessimistic Transactions
summary: TiDB の楽観的トランザクションと悲観的トランザクションについて学習します。
---

# 楽観的なトランザクションと悲観的なトランザクション {#optimistic-transactions-and-pessimistic-transactions}

[楽観的取引](/optimistic-transaction.md)モデルはトランザクションを直接コミットし、競合が発生した場合はロールバックします。対照的に、 [悲観的取引](/pessimistic-transaction.md)モデルはトランザクションを実際にコミットする前に変更する必要があるリソースをロックしようとし、トランザクションが正常に実行できることを確認した後にのみコミットを開始します。

楽観的トランザクション モデルは、直接コミットの成功確率が高いため、競合率が低いシナリオに適しています。ただし、トランザクションの競合が発生すると、ロールバックのコストが比較的高くなります。

悲観的トランザクション モデルの利点は、競合率の高いシナリオでは、先行ロックのコストがその後のロールバックのコストよりも低いことです。さらに、競合のために複数の同時トランザクションがコミットに失敗するという問題を解決できます。ただし、競合率の低いシナリオでは、悲観的トランザクション モデルは楽観的トランザクション モデルほど効率的ではありません。

悲観的トランザクション モデルは、より直感的で、アプリケーション側での実装が簡単です。楽観的トランザクション モデルでは、複雑なアプリケーション側の再試行メカニズムが必要です。

以下は[書店](/develop/dev-guide-bookshop-schema-design.md)の例です。本を購入する例を使用して、楽観的取引と悲観的取引の長所と短所を示します。本を購入するプロセスは、主に次のものから構成されます。

1.  在庫数量を更新する
2.  注文を作成する
3.  支払いをする

これらの操作はすべて成功するか、すべて失敗するかのいずれかになります。同時トランザクションの場合は、過剰販売が発生しないようにする必要があります。

## 悲観的な取引 {#pessimistic-transactions}

次のコードは、2 つのスレッドを使用して、2 人のユーザーが悲観的トランザクション モードで同じ本を購入するプロセスをシミュレートします。書店には 10 冊の本が残っています。ボブは 6 冊、アリスは 4 冊の本を購入します。彼らはほぼ同時に注文を完了します。その結果、在庫にあるすべての本が売り切れます。

<SimpleTab groupId="language">

<div label="Java" value="java">

複数のユーザーが同時にデータを挿入する状況をシミュレートするために複数のスレッドを使用するため、安全なスレッドを持つ接続オブジェクトを使用する必要があります。ここでは、デモ用に Java の一般的な接続プール[HikariCP](https://github.com/brettwooldridge/HikariCP)を使用します。

</div>

<div label="Golang" value="golang">

Golangの`sql.DB`並行処理に対して安全であるため、サードパーティのパッケージをインポートする必要はありません。

TiDB トランザクションを適応させるには、次のコードに従ってツールキット[ユーティリティ](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)を記述します。

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

スレッドの安全性を確保するために、mysqlclient ドライバーを使用して、スレッド間で共有されない複数の接続を開くことができます。

</div>

</SimpleTab>

### 悲観的トランザクションの例を書く {#write-a-pessimistic-transaction-example}

<SimpleTab groupId="language">

<div label="Java" value="java">

**コンフィグレーションファイル**

Maven を使用してパッケージを管理する場合は、 `pom.xml`の`<dependencies>`ノードで、次の依存関係を追加して`HikariCP`をインポートし、パッケージ化ターゲットを設定し、JAR パッケージの起動のメインクラスを設定します。以下は`pom.xml`の例です。

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

**コーディング**

次にコードを記述します。

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

        // prepare data
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

    public static void buy (HikariDataSource ds, Integer threadID,
                            Long orderID, Long bookID, Long userID, Integer quantity) {
        String txnComment = "/* txn " + threadID + " */ ";

        try (Connection connection = ds.getConnection()) {
            try {
                connection.setAutoCommit(false);
                connection.createStatement().executeUpdate(txnComment + "begin pessimistic");

                // waiting for other thread ran the 'begin pessimistic' statement
                TimeUnit.SECONDS.sleep(1);

                BigDecimal price = null;

                // read price of book
                PreparedStatement selectBook = connection.prepareStatement(txnComment + "select price from books where id = ? for update");
                selectBook.setLong(1, bookID);
                ResultSet res = selectBook.executeQuery();
                if (!res.next()) {
                    throw new RuntimeException("book not exist");
                } else {
                    price = res.getBigDecimal("price");
                }

                // update book
                String updateBookSQL = "update `books` set stock = stock - ? where id = ? and stock - ? >= 0";
                PreparedStatement updateBook = connection.prepareStatement(txnComment + updateBookSQL);
                updateBook.setInt(1, quantity);
                updateBook.setLong(2, bookID);
                updateBook.setInt(3, quantity);
                int affectedRows = updateBook.executeUpdate();

                if (affectedRows == 0) {
                    // stock not enough, rollback
                    connection.createStatement().executeUpdate(txnComment + "rollback");
                    return;
                }

                // insert order
                String insertOrderSQL = "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (?, ?, ?, ?)";
                PreparedStatement insertOrder = connection.prepareStatement(txnComment + insertOrderSQL);
                insertOrder.setLong(1, orderID);
                insertOrder.setLong(2, bookID);
                insertOrder.setLong(3, userID);
                insertOrder.setInt(4, quantity);
                insertOrder.executeUpdate();

                // update user
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

必要なデータベース操作を含む`helper.go`ファイルを作成します。

```go
package main

import (
    "context"
    "database/sql"
    "fmt"
    "time"

    "github.com/go-sql-driver/mysql"
    "github.com/pingcap-inc/tidb-example-golang/util"
    "github.com/shopspring/decimal"
)

type TxnFunc func(txn *util.TiDBSqlTx) error

const (
    ErrWriteConflict      = 9007 // Transactions in TiKV encounter write conflicts.
    ErrInfoSchemaChanged  = 8028 // table schema changes
    ErrForUpdateCantRetry = 8002 // "SELECT FOR UPDATE" commit conflict
    ErrTxnRetryable       = 8022 // The transaction commit fails and has been rolled back
)

const retryTimes = 5

var retryErrorCodeSet = map[uint16]interface{}{
    ErrWriteConflict:      nil,
    ErrInfoSchemaChanged:  nil,
    ErrForUpdateCantRetry: nil,
    ErrTxnRetryable:       nil,
}

func runTxn(db *sql.DB, optimistic bool, optimisticRetryTimes int, txnFunc TxnFunc) {
    txn, err := util.TiDBSqlBegin(db, !optimistic)
    if err != nil {
        panic(err)
    }

    err = txnFunc(txn)
    if err != nil {
        txn.Rollback()
        if mysqlErr, ok := err.(*mysql.MySQLError); ok && optimistic && optimisticRetryTimes != 0 {
            if _, retryableError := retryErrorCodeSet[mysqlErr.Number]; retryableError {
                fmt.Printf("[runTxn] got a retryable error, rest time: %d\n", optimisticRetryTimes-1)
                runTxn(db, optimistic, optimisticRetryTimes-1, txnFunc)
                return
            }
        }

        fmt.Printf("[runTxn] got an error, rollback: %+v\n", err)
    } else {
        err = txn.Commit()
        if mysqlErr, ok := err.(*mysql.MySQLError); ok && optimistic && optimisticRetryTimes != 0 {
            if _, retryableError := retryErrorCodeSet[mysqlErr.Number]; retryableError {
                fmt.Printf("[runTxn] got a retryable error, rest time: %d\n", optimisticRetryTimes-1)
                runTxn(db, optimistic, optimisticRetryTimes-1, txnFunc)
                return
            }
        }

        if err == nil {
            fmt.Println("[runTxn] commit success")
        }
    }
}

func prepareData(db *sql.DB, optimistic bool) {
    runTxn(db, optimistic, retryTimes, func(txn *util.TiDBSqlTx) error {
        publishedAt, err := time.Parse("2006-01-02 15:04:05", "2018-09-01 00:00:00")
        if err != nil {
            return err
        }

        if err = createBook(txn, 1, "Designing Data-Intensive Application",
            "Science & Technology", publishedAt, decimal.NewFromInt(100), 10); err != nil {
            return err
        }

        if err = createUser(txn, 1, "Bob", decimal.NewFromInt(10000)); err != nil {
            return err
        }

        if err = createUser(txn, 2, "Alice", decimal.NewFromInt(10000)); err != nil {
            return err
        }

        return nil
    })
}

func buyPessimistic(db *sql.DB, goroutineID, orderID, bookID, userID, amount int) {
    txnComment := fmt.Sprintf("/* txn %d */ ", goroutineID)
    if goroutineID != 1 {
        txnComment = "\t" + txnComment
    }

    fmt.Printf("\nuser %d try to buy %d books(id: %d)\n", userID, amount, bookID)

    runTxn(db, false, retryTimes, func(txn *util.TiDBSqlTx) error {
        time.Sleep(time.Second)

        // read the price of book
        selectBookForUpdate := "select `price` from books where id = ? for update"
        bookRows, err := txn.Query(selectBookForUpdate, bookID)
        if err != nil {
            return err
        }
        fmt.Println(txnComment + selectBookForUpdate + " successful")
        defer bookRows.Close()

        price := decimal.NewFromInt(0)
        if bookRows.Next() {
            err = bookRows.Scan(&price)
            if err != nil {
                return err
            }
        } else {
            return fmt.Errorf("book ID not exist")
        }
        bookRows.Close()

        // update book
        updateStock := "update `books` set stock = stock - ? where id = ? and stock - ? >= 0"
        result, err := txn.Exec(updateStock, amount, bookID, amount)
        if err != nil {
            return err
        }
        fmt.Println(txnComment + updateStock + " successful")

        affected, err := result.RowsAffected()
        if err != nil {
            return err
        }

        if affected == 0 {
            return fmt.Errorf("stock not enough, rollback")
        }

        // insert order
        insertOrder := "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (?, ?, ?, ?)"
        if _, err := txn.Exec(insertOrder,
            orderID, bookID, userID, amount); err != nil {
            return err
        }
        fmt.Println(txnComment + insertOrder + " successful")

        // update user
        updateUser := "update `users` set `balance` = `balance` - ? where id = ?"
        if _, err := txn.Exec(updateUser,
            price.Mul(decimal.NewFromInt(int64(amount))), userID); err != nil {
            return err
        }
        fmt.Println(txnComment + updateUser + " successful")

        return nil
    })
}

func buyOptimistic(db *sql.DB, goroutineID, orderID, bookID, userID, amount int) {
    txnComment := fmt.Sprintf("/* txn %d */ ", goroutineID)
    if goroutineID != 1 {
        txnComment = "\t" + txnComment
    }

    fmt.Printf("\nuser %d try to buy %d books(id: %d)\n", userID, amount, bookID)

    runTxn(db, true, retryTimes, func(txn *util.TiDBSqlTx) error {
        time.Sleep(time.Second)

        // read the price and stock of book
        selectBookForUpdate := "select `price`, `stock` from books where id = ? for update"
        bookRows, err := txn.Query(selectBookForUpdate, bookID)
        if err != nil {
            return err
        }
        fmt.Println(txnComment + selectBookForUpdate + " successful")
        defer bookRows.Close()

        price, stock := decimal.NewFromInt(0), 0
        if bookRows.Next() {
            err = bookRows.Scan(&price, &stock)
            if err != nil {
                return err
            }
        } else {
            return fmt.Errorf("book ID not exist")
        }
        bookRows.Close()

        if stock < amount {
            return fmt.Errorf("book not enough")
        }

        // update book
        updateStock := "update `books` set stock = stock - ? where id = ? and stock - ? >= 0"
        result, err := txn.Exec(updateStock, amount, bookID, amount)
        if err != nil {
            return err
        }
        fmt.Println(txnComment + updateStock + " successful")

        affected, err := result.RowsAffected()
        if err != nil {
            return err
        }

        if affected == 0 {
            return fmt.Errorf("stock not enough, rollback")
        }

        // insert order
        insertOrder := "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (?, ?, ?, ?)"
        if _, err := txn.Exec(insertOrder,
            orderID, bookID, userID, amount); err != nil {
            return err
        }
        fmt.Println(txnComment + insertOrder + " successful")

        // update user
        updateUser := "update `users` set `balance` = `balance` - ? where id = ?"
        if _, err := txn.Exec(updateUser,
            price.Mul(decimal.NewFromInt(int64(amount))), userID); err != nil {
            return err
        }
        fmt.Println(txnComment + updateUser + " successful")

        return nil
    })
}

func createBook(txn *util.TiDBSqlTx, id int, title, bookType string,
    publishedAt time.Time, price decimal.Decimal, stock int) error {
    _, err := txn.ExecContext(context.Background(),
        "INSERT INTO `books` (`id`, `title`, `type`, `published_at`, `price`, `stock`) values (?, ?, ?, ?, ?, ?)",
        id, title, bookType, publishedAt, price, stock)
    return err
}

func createUser(txn *util.TiDBSqlTx, id int, nickname string, balance decimal.Decimal) error {
    _, err := txn.ExecContext(context.Background(),
        "INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (?, ?, ?)",
        id, nickname, balance)
    return err
}
```

次に、 `helper.go`を呼び出して受信したコマンド ライン引数を処理する`txn.go`と`main`関数を記述します。

```go
package main

import (
    "database/sql"
    "flag"
    "fmt"
    "sync"
)

func main() {
    optimistic, alice, bob := parseParams()

    openDB("mysql", "root:@tcp(127.0.0.1:4000)/bookshop?charset=utf8mb4", func(db *sql.DB) {
        prepareData(db, optimistic)
        buy(db, optimistic, alice, bob)
    })
}

func buy(db *sql.DB, optimistic bool, alice, bob int) {
    buyFunc := buyOptimistic
    if !optimistic {
        buyFunc = buyPessimistic
    }

    wg := sync.WaitGroup{}
    wg.Add(1)
    go func() {
        defer wg.Done()
        buyFunc(db, 1, 1000, 1, 1, bob)
    }()

    wg.Add(1)
    go func() {
        defer wg.Done()
        buyFunc(db, 2, 1001, 1, 2, alice)
    }()

    wg.Wait()
}

func openDB(driverName, dataSourceName string, runnable func(db *sql.DB)) {
    db, err := sql.Open(driverName, dataSourceName)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    runnable(db)
}

func parseParams() (optimistic bool, alice, bob int) {
    flag.BoolVar(&optimistic, "o", false, "transaction is optimistic")
    flag.IntVar(&alice, "a", 4, "Alice bought num")
    flag.IntVar(&bob, "b", 6, "Bob bought num")

    flag.Parse()

    fmt.Println(optimistic, alice, bob)

    return optimistic, alice, bob
}
```

Golang の例にはすでに楽観的トランザクションが含まれています。

</div>

<div label="Python" value="python">

```python
import time

import MySQLdb
import os
import datetime
from threading import Thread

REPEATABLE_ERROR_CODE_SET = {
    9007,  # Transactions in TiKV encounter write conflicts.
    8028,  # table schema changes
    8002,  # "SELECT FOR UPDATE" commit conflict
    8022   # The transaction commit fails and has been rolled back
}


def create_connection():
    return MySQLdb.connect(
        host="127.0.0.1",
        port=4000,
        user="root",
        password="",
        database="bookshop",
        autocommit=False
    )


def prepare_data() -> None:
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO `books` (`id`, `title`, `type`, `published_at`, `price`, `stock`) "
                           "values (%s, %s, %s, %s, %s, %s)",
                           (1, "Designing Data-Intensive Application", "Science & Technology",
                            datetime.datetime(2018, 9, 1), 100, 10))

            cursor.executemany("INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (%s, %s, %s)",
                               [(1, "Bob", 10000), (2, "ALICE", 10000)])
            connection.commit()


def buy_optimistic(thread_id: int, order_id: int, book_id: int, user_id: int, amount: int,
                   optimistic_retry_times: int = 5) -> None:
    connection = create_connection()

    txn_log_header = f"/* txn {thread_id} */"
    if thread_id != 1:
        txn_log_header = "\t" + txn_log_header

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("BEGIN OPTIMISTIC")
            print(f'{txn_log_header} BEGIN OPTIMISTIC')
            time.sleep(1)

            try:
                # read the price of book
                select_book_for_update = "SELECT `price`, `stock` FROM books WHERE id = %s FOR UPDATE"
                cursor.execute(select_book_for_update, (book_id,))
                book = cursor.fetchone()
                if book is None:
                    raise Exception("book_id not exist")
                price, stock = book
                print(f'{txn_log_header} {select_book_for_update} successful')

                if stock < amount:
                    raise Exception("book not enough, rollback")

                # update book
                update_stock = "update `books` set stock = stock - %s where id = %s and stock - %s >= 0"
                rows_affected = cursor.execute(update_stock, (amount, book_id, amount))
                print(f'{txn_log_header} {update_stock} successful')

                if rows_affected == 0:
                    raise Exception("stock not enough, rollback")

                # insert order
                insert_order = "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (%s, %s, %s, %s)"
                cursor.execute(insert_order, (order_id, book_id, user_id, amount))
                print(f'{txn_log_header} {insert_order} successful')

                # update user
                update_user = "update `users` set `balance` = `balance` - %s where id = %s"
                cursor.execute(update_user, (amount * price, user_id))
                print(f'{txn_log_header} {update_user} successful')

            except Exception as err:
                connection.rollback()

                print(f'something went wrong: {err}')
            else:
                # important here! you need deal the Exception from the TiDB
                try:
                    connection.commit()
                except MySQLdb.MySQLError as db_err:
                    code, desc = db_err.args
                    if code in REPEATABLE_ERROR_CODE_SET and optimistic_retry_times > 0:
                        print(f'retry, rest {optimistic_retry_times - 1} times, for {code} {desc}')
                        buy_optimistic(thread_id, order_id, book_id, user_id, amount, optimistic_retry_times - 1)


def buy_pessimistic(thread_id: int, order_id: int, book_id: int, user_id: int, amount: int) -> None:
    connection = create_connection()

    txn_log_header = f"/* txn {thread_id} */"
    if thread_id != 1:
        txn_log_header = "\t" + txn_log_header

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("BEGIN PESSIMISTIC")
            print(f'{txn_log_header} BEGIN PESSIMISTIC')
            time.sleep(1)

            try:
                # read the price of book
                select_book_for_update = "SELECT `price` FROM books WHERE id = %s FOR UPDATE"
                cursor.execute(select_book_for_update, (book_id,))
                book = cursor.fetchone()
                if book is None:
                    raise Exception("book_id not exist")
                price = book[0]
                print(f'{txn_log_header} {select_book_for_update} successful')

                # update book
                update_stock = "update `books` set stock = stock - %s where id = %s and stock - %s >= 0"
                rows_affected = cursor.execute(update_stock, (amount, book_id, amount))
                print(f'{txn_log_header} {update_stock} successful')

                if rows_affected == 0:
                    raise Exception("stock not enough, rollback")

                # insert order
                insert_order = "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (%s, %s, %s, %s)"
                cursor.execute(insert_order, (order_id, book_id, user_id, amount))
                print(f'{txn_log_header} {insert_order} successful')

                # update user
                update_user = "update `users` set `balance` = `balance` - %s where id = %s"
                cursor.execute(update_user, (amount * price, user_id))
                print(f'{txn_log_header} {update_user} successful')

            except Exception as err:
                connection.rollback()
                print(f'something went wrong: {err}')
            else:
                connection.commit()


optimistic = os.environ.get('OPTIMISTIC')
alice = os.environ.get('ALICE')
bob = os.environ.get('BOB')

if not (optimistic and alice and bob):
    raise Exception("please use \"OPTIMISTIC=<is_optimistic> ALICE=<alice_num> "
                    "BOB=<bob_num> python3 txn_example.py\" to start this script")

prepare_data()

if bool(optimistic) is True:
    buy_func = buy_optimistic
else:
    buy_func = buy_pessimistic

bob_thread = Thread(target=buy_func, kwargs={
    "thread_id": 1, "order_id": 1000, "book_id": 1, "user_id": 1, "amount": int(bob)})
alice_thread = Thread(target=buy_func, kwargs={
    "thread_id": 2, "order_id": 1001, "book_id": 1, "user_id": 2, "amount": int(alice)})

bob_thread.start()
alice_thread.start()
bob_thread.join(timeout=10)
alice_thread.join(timeout=10)
```

Python の例にはすでに楽観的トランザクションが含まれています。

</div>

</SimpleTab>

### 過剰販売を伴わない例 {#an-example-that-does-not-involve-overselling}

サンプルプログラムを実行します。

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

SQL ログ:

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
/* txn 1 */ COMMIT
```

最後に、注文が作成され、ユーザー残高が差し引かれ、書籍在庫が期待どおりに差し引かれることを確認します。

```sql
mysql> SELECT * FROM `books`;
+----+--------------------------------------+----------------------+---------------------+-------+--------+
| id | title                                | type                 | published_at        | stock | price  |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
|  1 | Designing Data-Intensive Application | Science & Technology | 2018-09-01 00:00:00 |     0 | 100.00 |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
1 row in set (0.00 sec)

mysql> SELECT * FROM orders;
+------+---------+---------+---------+---------------------+
| id   | book_id | user_id | quality | ordered_at          |
+------+---------+---------+---------+---------------------+
| 1000 |       1 |       1 |       6 | 2022-04-19 10:58:12 |
| 1001 |       1 |       1 |       4 | 2022-04-19 10:58:11 |
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

### 過剰販売を防ぐ例 {#an-example-that-prevents-overselling}

この例のタスクはより困難です。在庫が 10 冊残っているとします。ボブは 7 冊、アリスは 4 冊を購入し、ほぼ同時に注文します。何が起こるでしょうか? この課題を解決するには、前の例のコードを再利用し、ボブの購入数量を 6 から 7 に変更できます。

サンプルプログラムを実行します。

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
./bin/txn -a 4 -b 7
```

</div>

<div label="Python" value="python">

```shell
OPTIMISTIC=False ALICE=4 BOB=7 python3 txn_example.py
```

</div>

</SimpleTab>

```sql
/* txn 1 */ BEGIN PESSIMISTIC
    /* txn 2 */ BEGIN PESSIMISTIC
    /* txn 2 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
    /* txn 2 */ UPDATE `books` SET `stock` = `stock` - 4 WHERE `id` = 1 AND `stock` - 4 >= 0
    /* txn 2 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) values (1001, 1, 1, 4)
    /* txn 2 */ UPDATE `users` SET `balance` = `balance` - 400.0 WHERE `id` = 2
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
/* txn 1 */ UPDATE `books` SET `stock` = `stock` - 7 WHERE `id` = 1 AND `stock` - 7 >= 0
/* txn 1 */ ROLLBACK
```

`txn 2`先行してロックリソースを取得し、ストックを更新するため、 `txn 1`の`affected_rows`の戻り値は0となり、 `rollback`処理に入ります。

注文の作成、ユーザー残高の減額、書籍在庫の減額を確認しましょう。アリスは 4 冊の注文に成功しましたが、ボブは 7 冊の注文に失敗し、残りの 6 冊は予想どおり在庫があります。

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

## 楽観的な取引 {#optimistic-transactions}

次のコードでは、悲観的トランザクションの例と同様に、2 つのスレッドを使用して、2 人のユーザーが楽観的トランザクションで同じ本を購入するプロセスをシミュレートします。在庫には 10 冊の本が残っています。ボブは 6 冊、アリスは 4 冊を購入します。彼らはほぼ同時に注文を完了します。最終的に、在庫には本が残っていません。

### 楽観的トランザクションの例を書く {#write-an-optimistic-transaction-example}

<SimpleTab groupId="language">

<div label="Java" value="java">

**コーディング**

```java
package com.pingcap.txn.optimistic;

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

        // prepare data
        Connection connection = ds.getConnection();
        createBook(connection, 1L, "Designing Data-Intensive Application", "Science & Technology",
                Timestamp.valueOf("2018-09-01 00:00:00"), new BigDecimal(100), 10);
        createUser(connection, 1L, "Bob", new BigDecimal(10000));
        createUser(connection, 2L, "Alice", new BigDecimal(10000));

        CountDownLatch countDownLatch = new CountDownLatch(2);
        ExecutorService threadPool = Executors.newFixedThreadPool(2);

        final int finalBobQuantity = bobQuantity;
        threadPool.execute(() -> {
            buy(ds, 1, 1000L, 1L, 1L, finalBobQuantity, 5);
            countDownLatch.countDown();
        });
        final int finalAliceQuantity = aliceQuantity;
        threadPool.execute(() -> {
            buy(ds, 2, 1001L, 1L, 2L, finalAliceQuantity, 5);
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
                            Long userID, Integer quantity, Integer retryTimes) {
        String txnComment = "/* txn " + threadID + " */ ";

        try (Connection connection = ds.getConnection()) {
            try {

                connection.setAutoCommit(false);
                connection.createStatement().executeUpdate(txnComment + "begin optimistic");

                // waiting for other thread ran the 'begin optimistic' statement
                TimeUnit.SECONDS.sleep(1);

                BigDecimal price = null;

                // read price of book
                PreparedStatement selectBook = connection.prepareStatement(txnComment + "SELECT * FROM books where id = ? for update");
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

                // update book
                String updateBookSQL = "update `books` set stock = stock - ? where id = ? and stock - ? >= 0";
                PreparedStatement updateBook = connection.prepareStatement(txnComment + updateBookSQL);
                updateBook.setInt(1, quantity);
                updateBook.setLong(2, bookID);
                updateBook.setInt(3, quantity);
                updateBook.executeUpdate();

                // insert order
                String insertOrderSQL = "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (?, ?, ?, ?)";
                PreparedStatement insertOrder = connection.prepareStatement(txnComment + insertOrderSQL);
                insertOrder.setLong(1, orderID);
                insertOrder.setLong(2, bookID);
                insertOrder.setLong(3, userID);
                insertOrder.setInt(4, quantity);
                insertOrder.executeUpdate();

                // update user
                String updateUserSQL = "update `users` set `balance` = `balance` - ? where id = ?";
                PreparedStatement updateUser = connection.prepareStatement(txnComment + updateUserSQL);
                updateUser.setBigDecimal(1, price.multiply(new BigDecimal(quantity)));
                updateUser.setLong(2, userID);
                updateUser.executeUpdate();

                connection.createStatement().executeUpdate(txnComment + "commit");
            } catch (Exception e) {
                connection.createStatement().executeUpdate(txnComment + "rollback");
                System.out.println("error occurred: " + e.getMessage());

                if (e instanceof SQLException sqlException) {
                    switch (sqlException.getErrorCode()) {
                        // You can get all error codes at https://docs.pingcap.com/tidb/stable/error-codes
                        case 9007: // Transactions in TiKV encounter write conflicts.
                        case 8028: // table schema changes
                        case 8002: // "SELECT FOR UPDATE" commit conflict
                        case 8022: // The transaction commit fails and has been rolled back
                            if (retryTimes != 0) {
                                System.out.println("rest " + retryTimes + " times. retry for " + e.getMessage());
                                buy(ds, threadID, orderID, bookID, userID, quantity, retryTimes - 1);
                            }
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

**コンフィグレーションの変更**

`pom.xml`の起動クラスを変更します。

```xml
<mainClass>com.pingcap.txn.TxnExample</mainClass>
```

楽観的トランザクションの例を指すように、次のように変更します。

```xml
<mainClass>com.pingcap.txn.optimistic.TxnExample</mainClass>
```

</div>

<div label="Golang" value="golang">

セクション[悲観的トランザクションの例を書く](#write-a-pessimistic-transaction-example)のGolangの例では、すでに楽観的トランザクションがサポートされており、変更せずに直接使用できます。

</div>

<div label="Python" value="python">

セクション[悲観的トランザクションの例を書く](#write-a-pessimistic-transaction-example)の Python の例では、すでに楽観的トランザクションがサポートされており、変更せずに直接使用できます。

</div>

</SimpleTab>

### 過剰販売を伴わない例 {#an-example-that-does-not-involve-overselling}

サンプルプログラムを実行します。

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
./bin/txn -a 4 -b 6 -o true
```

</div>

<div label="Python" value="python">

```shell
OPTIMISTIC=True ALICE=4 BOB=6 python3 txn_example.py
```

</div>

</SimpleTab>

SQL ステートメントの実行プロセス:

```sql
    /* txn 2 */ BEGIN OPTIMISTIC
/* txn 1 */ BEGIN OPTIMISTIC
    /* txn 2 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
    /* txn 2 */ UPDATE `books` SET `stock` = `stock` - 4 WHERE `id` = 1 AND `stock` - 4 >= 0
    /* txn 2 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1001, 1, 1, 4)
    /* txn 2 */ UPDATE `users` SET `balance` = `balance` - 400.0 WHERE `id` = 2
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 for UPDATE
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

楽観的トランザクションモードでは、中間状態が必ずしも正しいとは限らないため、悲観的トランザクションモードのように`affected_rows`まで文が正常に実行されたかどうかを判定することはできません。トランザクション全体をとらえ、最後の`COMMIT`文が例外を返すかどうかで、現在のトランザクションに書き込み競合があるかどうかを判断する必要があります。

上記の SQL ログからわかるように、2 つのトランザクションが同時に実行され、同じレコードが変更されているため、 `txn 1` COMMIT の後に`9007 Write conflict`例外がスローされます。楽観的トランザクション モードでの書き込み競合については、アプリケーション側で安全に再試行できます。1 回の再試行後、データが正常にコミットされます。最終的な実行結果は予想どおりです。

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

### 過剰販売を防ぐ例 {#an-example-that-prevents-overselling}

このセクションでは、過剰販売を防ぐ楽観的トランザクションの例について説明します。在庫に 10 冊の本が残っているとします。ボブは 7​​ 冊、アリスは 4 冊を購入します。彼らはほぼ同時に注文をします。何が起こるでしょうか? この要件に対処するために、楽観的トランザクションの例のコードを再利用できます。ボブの購入数を 6 から 7 に変更します。

サンプルプログラムを実行します。

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
/* txn 1 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1000, 1, 1, 7)
/* txn 1 */ UPDATE `users` SET `balance` = `balance` - 700.0 WHERE `id` = 1
retry 1 times for 9007 Write conflict, txnStartTS=432619094333980675, conflictStartTS=432619094333980676, conflictCommitTS=432619094333980678, key={tableID=126, handle=1} primary={tableID=114, indexID=1, indexValues={1, 1000, }} [try again later]
/* txn 1 */ BEGIN OPTIMISTIC
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
Fail -> out of stock
/* txn 1 */ ROLLBACK
```

上記のSQLログから、初回実行時の書き込み競合によりアプリケーション側で`txn 1`再試行されていることがわかります。最新のスナップショットを比較すると、在庫が不足していることがわかります。アプリケーション側は`out of stock`をスローし、異常終了します。

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
| 1001 |       1 |       1 |       4 | 2022-04-19 03:41:16 |
+------+---------+---------+---------+---------------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM users;
+----+----------+----------+
| id | balance  | nickname |
+----+----------+----------+
|  1 | 10000.00 | Bob      |
|  2 |  9600.00 | Alice    |
+----+----------+----------+
2 rows in set (0.00 sec)
```

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
