---
title: Transaction Restraints
summary: 了解 TiDB 中的事务限制。
---

# Transaction Restraints

本文简要介绍了 TiDB 中的事务限制。

## Isolation levels

TiDB 支持的隔离级别为 **RC (Read Committed)** 和 **SI (Snapshot Isolation)**，其中 **SI** 基本等同于 **RR (Repeatable Read)** 隔离级别。

![isolation level](/media/develop/transaction_isolation_level.png)

## Snapshot Isolation can avoid phantom reads

TiDB 的 `SI` 隔离级别可以避免 **Phantom Reads**，但在 ANSI/ISO SQL 标准中，`RR` 不能。

以下两个示例说明了什么是 **phantom reads**。

- 示例 1：**事务 A** 首先根据查询获取 `n` 行，然后 **事务 B** 改变除了这 `n` 行之外的 `m` 行，或添加与 **事务 A** 查询条件匹配的 `m` 行。当 **事务 A** 再次运行查询时，会发现有 `n+m` 行符合条件。这就像一个幻影，所以称为 **phantom read**。

- 示例 2：**管理员 A** 将数据库中所有学生的成绩从特定分数改为 ABCDE 等级，但此时 **管理员 B** 插入了一条具有特定分数的记录。当 **管理员 A** 完成修改后，发现仍有一条（由 **管理员 B** 插入的）未被修改的记录。这也是一种 **phantom read**。

## SI cannot avoid write skew

TiDB 的 `SI` 隔离级别不能避免 **write skew** 异常。你可以使用 `SELECT FOR UPDATE` 语法来避免 **write skew**。

**write skew** 异常发生在两个并发事务读取不同但相关的记录，然后各自更新自己读取的数据并最终提交事务时。如果这些相关记录之间存在不能被多个事务同时修改的约束，最终可能导致违反约束。

例如，假设你在为医院编写医生值班管理程序。医院通常要求多名医生同时值班，但最少要求至少一名医生值班。医生可以请假（例如，感觉不适），只要在该班次期间至少有一名医生在值班。

现在有一种情况，医生 `Alice` 和 `Bob` 都在值班。两人都感觉不适，决定请病假。恰巧他们同时点击了请假按钮。以下用程序模拟此过程：

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

        // 准备数据
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

                // 事务 1 应等待事务 2 完成
                if (txnID == 1) {
                    txn1Pass.acquire();
                }

                PreparedStatement currentOnCallQuery = connection.prepareStatement(comment +
                        "SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = ? AND `shift_id` = ?");
                currentOnCallQuery.setBoolean(1, true);
                currentOnCallQuery.setInt(2, 123);
                ResultSet res = currentOnCallQuery.executeQuery();

                if (!res.next()) {
                    throw new RuntimeException("查询出错");
                } else {
                    int count = res.getInt("count");
                    if (count >= 2) {
                        // 如果当前值班医生人数 >= 2，则该医生可以请假
                        PreparedStatement insert = connection.prepareStatement( comment +
                                "UPDATE `doctors` SET `on_call` = ? WHERE `id` = ? AND `shift_id` = ?");
                        insert.setBoolean(1, false);
                        insert.setInt(2, doctorID);
                        insert.setInt(3, 123);
                        insert.executeUpdate();

                        connection.commit();
                    } else {
                        throw new RuntimeException("至少有一名医生在值班");
                    }
                }

                // 事务 2 完成，允许事务 1 继续
                if (txnID == 2) {
                    txn1Pass.release();
                }
            } catch (Exception e) {
                // 出错时回滚，数据无价
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

    // 事务 1 应等待事务 2 完成
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
            return fmt.Errorf("至少有一名医生在值班")
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
        fmt.Println("[runTxn] 提交成功")
    } else {
        txn.Rollback()
        fmt.Printf("[runTxn] 出错，回滚： %+v\n", err)
    }

    // 事务 2 完成，允许事务 1 继续
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

SQL log:

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

运行结果：

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

## Support for `savepoint` and nested transactions

> **Note:**
>
> 从 v6.2.0 版本开始，TiDB 支持 [`savepoint`](/sql-statements/sql-statement-savepoint.md) 功能。如果你的 TiDB 集群早于 v6.2.0，则不支持 `PROPAGATION_NESTED` 行为。建议升级到 v6.2.0 或更高版本。如果无法升级 TiDB，且你的应用基于使用 `PROPAGATION_NESTED` 传播行为的 **Java Spring** 框架，则需要在应用端进行适配，移除嵌套事务的相关逻辑。

**Spring** 支持的 `PROPAGATION_NESTED` 传播行为会触发嵌套事务，即一个独立于当前事务启动的子事务。子事务开始时会记录一个 `savepoint`。如果子事务失败，事务会回滚到该 `savepoint` 状态。嵌套事务是外层事务的一部分，会与外层事务一同提交。

以下示例演示了 `savepoint` 机制：

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

## Large transaction restrictions

基本原则是限制事务的大小。在 KV 层，TiDB 对单个事务的大小有限制。在 SQL 层，一行数据映射为一个 KV 条目，每增加一个索引会增加一个 KV 条目。SQL 层的限制如下：

- 单行最大记录大小为 120 MiB。

    - 你可以通过调整 [`performance.txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500) 配置参数（适用于 TiDB v4.0.10 及以上的 v4.0.x 版本，以及 v5.0.0 及以上版本）来调整。早期版本（低于 v4.0.10）默认值为 `6 MB`。
    - 从 v7.6.0 开始，可以使用 [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760) 系统变量动态修改此配置项的值。

- 支持的最大单个事务大小为 1 TiB。

    - 对于 TiDB v4.0 及以上版本，可以通过 [`performance.txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) 配置，早期版本的默认值为 `100 MB`。
    - 对于 v6.5.0 及以上版本，不再推荐使用此配置。更多信息请参见 [`performance.txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit)。

注意，在考虑大小限制和行数限制时，还应考虑在事务执行过程中编码开销和额外键的影响。为了获得最佳性能，建议每 100 ~ 500 行写入一次事务。

## Auto-committed `SELECT FOR UPDATE` statements do NOT wait for locks

目前，自动提交的 `SELECT FOR UPDATE` 语句不会加锁。效果如下图所示：

![The situation in TiDB](/media/develop/autocommit_selectforupdate_nowaitlock.png)

这是 MySQL 的已知不兼容问题。你可以通过使用显式的 `BEGIN; COMMIT;` 语句解决此问题。

## Need help?

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>