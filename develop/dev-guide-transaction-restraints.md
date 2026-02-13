---
title: Transaction Restraints
summary: TiDB のトランザクション制約について学習します。
aliases: ['/ja/tidb/stable/dev-guide-transaction-restraints/','/ja/tidb/dev/dev-guide-transaction-restraints/','/ja/tidbcloud/dev-guide-transaction-restraints/']
---

# トランザクション制限 {#transaction-restraints}

このドキュメントでは、TiDB におけるトランザクション制約について簡単に説明します。

## 分離レベル {#isolation-levels}

TiDB でサポートされている分離レベルは**RC (Read Committed)**と**SI (Snapshot Isolation)**です。SI**は**基本的に**RR (Repeatable Read)**分離レベルと同等です。

![isolation level](/media/develop/transaction_isolation_level.png)

## スナップショット分離によりファントムリードを回避できる {#snapshot-isolation-can-avoid-phantom-reads}

TiDB の分離レベル`SI`では**ファントム リードは**回避できますが、ANSI/ISO SQL 標準の`RR`では回避できません。

次の 2 つの例は**、ファントム リードが**どのようなものであるかを示しています。

-   例1：**トランザクションAは**まずクエリに従って`n`行を取得します。その後、**トランザクションBは**これらの`n`行以外の`m`行を変更するか、**トランザクションA**のクエリに一致する`m`行を追加します。**トランザクションAが**再度クエリを実行すると、条件に一致する行が`n+m`行あることがわかります。これはファントムリードに似ているため、**ファントムリード**と呼ばれます。

-   例2：**管理者Aは**データベース内のすべての生徒の成績を特定スコアからABCDEスコアに変更しましたが、**管理者Bは**同時に特定のスコアを持つレコードを挿入しました。**管理者Aが**変更を終えると、まだ変更されていないレコード（**管理者B**が挿入したレコード）が残っていることに気づきます。これが**ファントムリード**です。

## SIは書き込みスキューを回避できない {#si-cannot-avoid-write-skew}

TiDBのSI分離レベルでは`SELECT FOR UPDATE`**書き込みスキュー**例外を回避できません。3構文を使用することで、**書き込みスキュー**例外を回避できます。

**書き込みスキュー**例外は、2つの同時トランザクションが異なるものの関連するレコードを読み取り、各トランザクションが読み取ったデータを更新し、最終的にトランザクションをコミットしたときに発生します。これらの関連レコード間に、複数のトランザクションによる同時変更が不可能な制約がある場合、最終結果はその制約に違反することになります。

例えば、病院の医師シフト管理プログラムを作成するとします。病院では通常、複数の医師が同時にオンコール対応することが求められますが、最低要件として、少なくとも1人の医師がオンコール対応していることが挙げられます。医師は、例えば体調が優れない場合など、そのシフト中に少なくとも1人の医師がオンコール対応していれば、シフトを中断することができます。

医師`Alice`と医師`Bob`がオンコールで待機している状況があります。二人とも体調が悪く、病気休暇を取ることにしました。そして、偶然にも同時にボタンをクリックしてしまいました。このプロセスを次のプログラムでシミュレートしてみましょう。

<SimpleTab groupId="language">

<div label="Java" value="java">

```java
package com.pingcap.txn.write.skew;

import com.zaxxer.hikari.HikariDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Semaphore;

public class EffectWriteSkew {
    public static void main(String[] args) throws SQLException, InterruptedException {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:mysql://localhost:4000/test?useServerPrepStmts=true&cachePrepStmts=true");
        ds.setUsername("root");

        // prepare data
        Connection connection = ds.getConnection();
        createDoctorTable(connection);
        createDoctor(connection, 1, "Alice", true, 123);
        createDoctor(connection, 2, "Bob", true, 123);
        createDoctor(connection, 3, "Carol", false, 123);

        Semaphore txn1Pass = new Semaphore(0);
        CountDownLatch countDownLatch = new CountDownLatch(2);
        ExecutorService threadPool = Executors.newFixedThreadPool(2);

        threadPool.execute(() -> {
            askForLeave(ds, txn1Pass, 1, 1);
            countDownLatch.countDown();
        });

        threadPool.execute(() -> {
            askForLeave(ds, txn1Pass, 2, 2);
            countDownLatch.countDown();
        });

        countDownLatch.await();
    }

    public static void createDoctorTable(Connection connection) throws SQLException {
        connection.createStatement().executeUpdate("CREATE TABLE `doctors` (" +
                "    `id` int NOT NULL," +
                "    `name` varchar(255) DEFAULT NULL," +
                "    `on_call` tinyint DEFAULT NULL," +
                "    `shift_id` int DEFAULT NULL," +
                "    PRIMARY KEY (`id`)," +
                "    KEY `idx_shift_id` (`shift_id`)" +
                "  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin");
    }

    public static void createDoctor(Connection connection, Integer id, String name, Boolean onCall, Integer shiftID) throws SQLException {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `doctors` (`id`, `name`, `on_call`, `shift_id`) VALUES (?, ?, ?, ?)");
        insert.setInt(1, id);
        insert.setString(2, name);
        insert.setBoolean(3, onCall);
        insert.setInt(4, shiftID);
        insert.executeUpdate();
    }

    public static void askForLeave(HikariDataSource ds, Semaphore txn1Pass, Integer txnID, Integer doctorID) {
        try(Connection connection = ds.getConnection()) {
            try {
                connection.setAutoCommit(false);

                String comment = txnID == 2 ? "    " : "" + "/* txn #{txn_id} */ ";
                connection.createStatement().executeUpdate(comment + "BEGIN");

                // Txn 1 should be waiting for txn 2 done
                if (txnID == 1) {
                    txn1Pass.acquire();
                }

                PreparedStatement currentOnCallQuery = connection.prepareStatement(comment +
                        "SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = ? AND `shift_id` = ?");
                currentOnCallQuery.setBoolean(1, true);
                currentOnCallQuery.setInt(2, 123);
                ResultSet res = currentOnCallQuery.executeQuery();

                if (!res.next()) {
                    throw new RuntimeException("error query");
                } else {
                    int count = res.getInt("count");
                    if (count >= 2) {
                        // If current on-call doctor has 2 or more, this doctor can leave
                        PreparedStatement insert = connection.prepareStatement( comment +
                                "UPDATE `doctors` SET `on_call` = ? WHERE `id` = ? AND `shift_id` = ?");
                        insert.setBoolean(1, false);
                        insert.setInt(2, doctorID);
                        insert.setInt(3, 123);
                        insert.executeUpdate();

                        connection.commit();
                    } else {
                        throw new RuntimeException("At least one doctor is on call");
                    }
                }

                // Txn 2 done, let txn 1 run again
                if (txnID == 2) {
                    txn1Pass.release();
                }
            } catch (Exception e) {
                // If got any error, you should roll back, data is priceless
                connection.rollback();
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

TiDB トランザクションを適応させるには、次のコードに従って[ユーティリティ](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)を記述します。

```go
package main

import (
    "database/sql"
    "fmt"
    "sync"

    "github.com/pingcap-inc/tidb-example-golang/util"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    openDB("mysql", "root:@tcp(127.0.0.1:4000)/test", func(db *sql.DB) {
        writeSkew(db)
    })
}

func openDB(driverName, dataSourceName string, runnable func(db *sql.DB)) {
    db, err := sql.Open(driverName, dataSourceName)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    runnable(db)
}

func writeSkew(db *sql.DB) {
    err := prepareData(db)
    if err != nil {
        panic(err)
    }

    waitingChan, waitGroup := make(chan bool), sync.WaitGroup{}

    waitGroup.Add(1)
    go func() {
        defer waitGroup.Done()
        err = askForLeave(db, waitingChan, 1, 1)
        if err != nil {
            panic(err)
        }
    }()

    waitGroup.Add(1)
    go func() {
        defer waitGroup.Done()
        err = askForLeave(db, waitingChan, 2, 2)
        if err != nil {
            panic(err)
        }
    }()

    waitGroup.Wait()
}

func askForLeave(db *sql.DB, waitingChan chan bool, goroutineID, doctorID int) error {
    txnComment := fmt.Sprintf("/* txn %d */ ", goroutineID)
    if goroutineID != 1 {
        txnComment = "\t" + txnComment
    }

    txn, err := util.TiDBSqlBegin(db, true)
    if err != nil {
        return err
    }
    fmt.Println(txnComment + "start txn")

    // Txn 1 should be waiting until txn 2 is done.
    if goroutineID == 1 {
        <-waitingChan
    }

    txnFunc := func() error {
        queryCurrentOnCall := "SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = ? AND `shift_id` = ?"
        rows, err := txn.Query(queryCurrentOnCall, true, 123)
        if err != nil {
            return err
        }
        defer rows.Close()
        fmt.Println(txnComment + queryCurrentOnCall + " successful")

        count := 0
        if rows.Next() {
            err = rows.Scan(&count)
            if err != nil {
                return err
            }
        }
        rows.Close()

        if count < 2 {
            return fmt.Errorf("at least one doctor is on call")
        }

        shift := "UPDATE `doctors` SET `on_call` = ? WHERE `id` = ? AND `shift_id` = ?"
        _, err = txn.Exec(shift, false, doctorID, 123)
        if err == nil {
            fmt.Println(txnComment + shift + " successful")
        }
        return err
    }

    err = txnFunc()
    if err == nil {
        txn.Commit()
        fmt.Println("[runTxn] commit success")
    } else {
        txn.Rollback()
        fmt.Printf("[runTxn] got an error, rollback: %+v\n", err)
    }

    // Txn 2 is done. Let txn 1 run again.
    if goroutineID == 2 {
        waitingChan <- true
    }

    return nil
}

func prepareData(db *sql.DB) error {
    err := createDoctorTable(db)
    if err != nil {
        return err
    }

    err = createDoctor(db, 1, "Alice", true, 123)
    if err != nil {
        return err
    }
    err = createDoctor(db, 2, "Bob", true, 123)
    if err != nil {
        return err
    }
    err = createDoctor(db, 3, "Carol", false, 123)
    if err != nil {
        return err
    }
    return nil
}

func createDoctorTable(db *sql.DB) error {
    _, err := db.Exec("CREATE TABLE IF NOT EXISTS `doctors` (" +
        "    `id` int NOT NULL," +
        "    `name` varchar(255) DEFAULT NULL," +
        "    `on_call` tinyint DEFAULT NULL," +
        "    `shift_id` int DEFAULT NULL," +
        "    PRIMARY KEY (`id`)," +
        "    KEY `idx_shift_id` (`shift_id`)" +
        "  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin")
    return err
}

func createDoctor(db *sql.DB, id int, name string, onCall bool, shiftID int) error {
    _, err := db.Exec("INSERT INTO `doctors` (`id`, `name`, `on_call`, `shift_id`) VALUES (?, ?, ?, ?)",
        id, name, onCall, shiftID)
    return err
}
```

</div>

</SimpleTab>

SQL ログ:

```sql
/* txn 1 */ BEGIN
    /* txn 2 */ BEGIN
    /* txn 2 */ SELECT COUNT(*) as `count` FROM `doctors` WHERE `on_call` = 1 AND `shift_id` = 123
    /* txn 2 */ UPDATE `doctors` SET `on_call` = 0 WHERE `id` = 2 AND `shift_id` = 123
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = 1 and `shift_id` = 123
/* txn 1 */ UPDATE `doctors` SET `on_call` = 0 WHERE `id` = 1 AND `shift_id` = 123
/* txn 1 */ COMMIT
```

実行結果:

```sql
mysql> SELECT * FROM doctors;
+----+-------+---------+----------+
| id | name  | on_call | shift_id |
+----+-------+---------+----------+
|  1 | Alice |       0 |      123 |
|  2 | Bob   |       0 |      123 |
|  3 | Carol |       0 |      123 |
+----+-------+---------+----------+
```

どちらのトランザクションでも、アプリケーションはまず2人以上の医師が待機中かどうかを確認します。待機中の場合、1人の医師は安全に休暇を取得できると想定します。データベースはスナップショット分離を使用しているため、両方のチェックで`2`返され、両方のトランザクションが次の段階に進みます。3 `Alice`自身のレコードを非番として更新し、 `Bob`同様に更新します。両方のトランザクションが正常にコミットされました。これで、待機中の医師がいなくなり、少なくとも1人の医師が待機中であるという要件に違反します。次の図（ ***『Designing Data-Intensive Applications*** 』より引用）は、実際に何が起こるかを示しています。

![Write Skew](/media/develop/write-skew.png)

ここで、書き込みスキューの問題を回避するために、サンプル プログラムを変更して`SELECT FOR UPDATE`使用します。

<SimpleTab groupId="language">

<div label="Java" value="java">

```java
package com.pingcap.txn.write.skew;

import com.zaxxer.hikari.HikariDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Semaphore;

public class EffectWriteSkew {
    public static void main(String[] args) throws SQLException, InterruptedException {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:mysql://localhost:4000/test?useServerPrepStmts=true&cachePrepStmts=true");
        ds.setUsername("root");

        // prepare data
        Connection connection = ds.getConnection();
        createDoctorTable(connection);
        createDoctor(connection, 1, "Alice", true, 123);
        createDoctor(connection, 2, "Bob", true, 123);
        createDoctor(connection, 3, "Carol", false, 123);

        Semaphore txn1Pass = new Semaphore(0);
        CountDownLatch countDownLatch = new CountDownLatch(2);
        ExecutorService threadPool = Executors.newFixedThreadPool(2);

        threadPool.execute(() -> {
            askForLeave(ds, txn1Pass, 1, 1);
            countDownLatch.countDown();
        });

        threadPool.execute(() -> {
            askForLeave(ds, txn1Pass, 2, 2);
            countDownLatch.countDown();
        });

        countDownLatch.await();
    }

    public static void createDoctorTable(Connection connection) throws SQLException {
        connection.createStatement().executeUpdate("CREATE TABLE `doctors` (" +
                "    `id` int NOT NULL," +
                "    `name` varchar(255) DEFAULT NULL," +
                "    `on_call` tinyint DEFAULT NULL," +
                "    `shift_id` int DEFAULT NULL," +
                "    PRIMARY KEY (`id`)," +
                "    KEY `idx_shift_id` (`shift_id`)" +
                "  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin");
    }

    public static void createDoctor(Connection connection, Integer id, String name, Boolean onCall, Integer shiftID) throws SQLException {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `doctors` (`id`, `name`, `on_call`, `shift_id`) VALUES (?, ?, ?, ?)");
        insert.setInt(1, id);
        insert.setString(2, name);
        insert.setBoolean(3, onCall);
        insert.setInt(4, shiftID);
        insert.executeUpdate();
    }

    public static void askForLeave(HikariDataSource ds, Semaphore txn1Pass, Integer txnID, Integer doctorID) {
        try(Connection connection = ds.getConnection()) {
            try {
                connection.setAutoCommit(false);

                String comment = txnID == 2 ? "    " : "" + "/* txn #{txn_id} */ ";
                connection.createStatement().executeUpdate(comment + "BEGIN");

                // Txn 1 should be waiting for txn 2 done
                if (txnID == 1) {
                    txn1Pass.acquire();
                }

                PreparedStatement currentOnCallQuery = connection.prepareStatement(comment +
                        "SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = ? AND `shift_id` = ? FOR UPDATE");
                currentOnCallQuery.setBoolean(1, true);
                currentOnCallQuery.setInt(2, 123);
                ResultSet res = currentOnCallQuery.executeQuery();

                if (!res.next()) {
                    throw new RuntimeException("error query");
                } else {
                    int count = res.getInt("count");
                    if (count >= 2) {
                        // If current on-call doctor has 2 or more, this doctor can leave
                        PreparedStatement insert = connection.prepareStatement( comment +
                                "UPDATE `doctors` SET `on_call` = ? WHERE `id` = ? AND `shift_id` = ?");
                        insert.setBoolean(1, false);
                        insert.setInt(2, doctorID);
                        insert.setInt(3, 123);
                        insert.executeUpdate();

                        connection.commit();
                    } else {
                        throw new RuntimeException("At least one doctor is on call");
                    }
                }

                // Txn 2 done, let txn 1 run again
                if (txnID == 2) {
                    txn1Pass.release();
                }
            } catch (Exception e) {
                // If got any error, you should roll back, data is priceless
                connection.rollback();
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

```go
package main

import (
    "database/sql"
    "fmt"
    "sync"

    "github.com/pingcap-inc/tidb-example-golang/util"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    openDB("mysql", "root:@tcp(127.0.0.1:4000)/test", func(db *sql.DB) {
        writeSkew(db)
    })
}

func openDB(driverName, dataSourceName string, runnable func(db *sql.DB)) {
    db, err := sql.Open(driverName, dataSourceName)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    runnable(db)
}

func writeSkew(db *sql.DB) {
    err := prepareData(db)
    if err != nil {
        panic(err)
    }

    waitingChan, waitGroup := make(chan bool), sync.WaitGroup{}

    waitGroup.Add(1)
    go func() {
        defer waitGroup.Done()
        err = askForLeave(db, waitingChan, 1, 1)
        if err != nil {
            panic(err)
        }
    }()

    waitGroup.Add(1)
    go func() {
        defer waitGroup.Done()
        err = askForLeave(db, waitingChan, 2, 2)
        if err != nil {
            panic(err)
        }
    }()

    waitGroup.Wait()
}

func askForLeave(db *sql.DB, waitingChan chan bool, goroutineID, doctorID int) error {
    txnComment := fmt.Sprintf("/* txn %d */ ", goroutineID)
    if goroutineID != 1 {
        txnComment = "\t" + txnComment
    }

    txn, err := util.TiDBSqlBegin(db, true)
    if err != nil {
        return err
    }
    fmt.Println(txnComment + "start txn")

    // Txn 1 should be waiting until txn 2 is done.
    if goroutineID == 1 {
        <-waitingChan
    }

    txnFunc := func() error {
        queryCurrentOnCall := "SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = ? AND `shift_id` = ?"
        rows, err := txn.Query(queryCurrentOnCall, true, 123)
        if err != nil {
            return err
        }
        defer rows.Close()
        fmt.Println(txnComment + queryCurrentOnCall + " successful")

        count := 0
        if rows.Next() {
            err = rows.Scan(&count)
            if err != nil {
                return err
            }
        }
        rows.Close()

        if count < 2 {
            return fmt.Errorf("at least one doctor is on call")
        }

        shift := "UPDATE `doctors` SET `on_call` = ? WHERE `id` = ? AND `shift_id` = ?"
        _, err = txn.Exec(shift, false, doctorID, 123)
        if err == nil {
            fmt.Println(txnComment + shift + " successful")
        }
        return err
    }

    err = txnFunc()
    if err == nil {
        txn.Commit()
        fmt.Println("[runTxn] commit success")
    } else {
        txn.Rollback()
        fmt.Printf("[runTxn] got an error, rollback: %+v\n", err)
    }

    // Txn 2 is done. Let txn 1 run again.
    if goroutineID == 2 {
        waitingChan <- true
    }

    return nil
}

func prepareData(db *sql.DB) error {
    err := createDoctorTable(db)
    if err != nil {
        return err
    }

    err = createDoctor(db, 1, "Alice", true, 123)
    if err != nil {
        return err
    }
    err = createDoctor(db, 2, "Bob", true, 123)
    if err != nil {
        return err
    }
    err = createDoctor(db, 3, "Carol", false, 123)
    if err != nil {
        return err
    }
    return nil
}

func createDoctorTable(db *sql.DB) error {
    _, err := db.Exec("CREATE TABLE IF NOT EXISTS `doctors` (" +
        "    `id` int NOT NULL," +
        "    `name` varchar(255) DEFAULT NULL," +
        "    `on_call` tinyint DEFAULT NULL," +
        "    `shift_id` int DEFAULT NULL," +
        "    PRIMARY KEY (`id`)," +
        "    KEY `idx_shift_id` (`shift_id`)" +
        "  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin")
    return err
}

func createDoctor(db *sql.DB, id int, name string, onCall bool, shiftID int) error {
    _, err := db.Exec("INSERT INTO `doctors` (`id`, `name`, `on_call`, `shift_id`) VALUES (?, ?, ?, ?)",
        id, name, onCall, shiftID)
    return err
}
```

</div>

</SimpleTab>

SQL ログ:

```sql
/* txn 1 */ BEGIN
    /* txn 2 */ BEGIN
    /* txn 2 */ SELECT COUNT(*) AS `count` FROM `doctors` WHERE on_call = 1 AND `shift_id` = 123 FOR UPDATE
    /* txn 2 */ UPDATE `doctors` SET on_call = 0 WHERE `id` = 2 AND `shift_id` = 123
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = 1 FOR UPDATE
At least one doctor is on call
/* txn 1 */ ROLLBACK
```

実行結果:

```sql
mysql> SELECT * FROM doctors;
+----+-------+---------+----------+
| id | name  | on_call | shift_id |
+----+-------+---------+----------+
|  1 | Alice |       1 |      123 |
|  2 | Bob   |       0 |      123 |
|  3 | Carol |       0 |      123 |
+----+-------+---------+----------+
```

## <code>savepoint</code>とネストされたトランザクションのサポート {#support-for-code-savepoint-code-and-nested-transactions}

> **注記：**
>
> TiDBはv6.2.0以降、 [`savepoint`](/sql-statements/sql-statement-savepoint.md)機能をサポートします。v6.2.0より前のバージョンのTiDBクラスタでは、 `PROPAGATION_NESTED`動作はサポートされません。v6.2.0以降のバージョンへのアップグレードをお勧めします。TiDBのアップグレードが不可能で、アプリケーションが`PROPAGATION_NESTED`伝播動作を使用する**Java Spring**フレームワークをベースにしている場合は、アプリケーション側でネストされたトランザクションのロジックを削除する必要があります。

**Spring**がサポートする`PROPAGATION_NESTED`伝播動作は、ネストされたトランザクション（現在のトランザクションとは独立して開始される子トランザクション）をトリガーします。ネストされたトランザクションの開始時に`savepoint`が記録されます。ネストされたトランザクションが失敗した場合、トランザクションは`savepoint`状態にロールバックされます。ネストされたトランザクションは外側のトランザクションの一部であり、外側のトランザクションと同時にコミットされます。

次の例は、 `savepoint`メカニズムを示しています。

```sql
mysql> BEGIN;
mysql> INSERT INTO T2 VALUES(100);
mysql> SAVEPOINT svp1;
mysql> INSERT INTO T2 VALUES(200);
mysql> ROLLBACK TO SAVEPOINT svp1;
mysql> RELEASE SAVEPOINT svp1;
mysql> COMMIT;
mysql> SELECT * FROM T2;
+------+
|  ID   |
+------+
|  100 |
+------+
```

## 大規模取引制限 {#large-transaction-restrictions}

基本原則は、トランザクションのサイズを制限することです。TiDBはKVレベルでは、単一トランザクションのサイズに制限を設けています。SQLレベルでは、1行のデータに1つのKVエントリがマッピングされ、インデックスを追加するごとに1つのKVエントリが追加されます。SQLレベルでの制限は次のとおりです。

-   単一行レコードの最大サイズは 120 MiB です。

    -   TiDB v4.0.10以降のv4.0.xバージョン、およびTiDB v5.0.0以降のバージョンでは、tidb-serverの設定パラメータ[`performance.txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)を使用して調整できます。v4.0.10より前のバージョンでは、値は`6 MB`です。
    -   v7.6.0 以降では、 [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)システム変数を使用して、この構成項目の値を動的に変更できます。

-   サポートされる単一トランザクションの最大サイズは 1 TiB です。

    -   TiDB v4.0 以降のバージョンでは、 [`performance.txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit)で設定できます。それより前のバージョンでは、値は`100 MB`です。
    -   TiDB v6.5.0以降のバージョンでは、この構成は推奨されません。詳細については、 [`performance.txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) )を参照してください。

サイズ制限と行制限の両方において、トランザクション実行中のエンコードと追加キーのオーバーヘッドも考慮する必要があります。最適なパフォーマンスを実現するには、100～500行ごとに1つのトランザクションを書き込むことをお勧めします。

## 自動コミットされた<code>SELECT FOR UPDATE</code>文はロックを待機しません。 {#auto-committed-code-select-for-update-code-statements-do-not-wait-for-locks}

現在、自動コミットされた`SELECT FOR UPDATE`ステートメントにはロックは追加されません。次のスクリーンショットは、2つの別々のセッションにおける効果を示しています。

![The situation in TiDB](/media/develop/autocommit_selectforupdate_nowaitlock.png)

これはMySQLとの既知の非互換性問題です。明示的な`BEGIN;COMMIT;`文を使用することでこの問題を解決できます。

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
