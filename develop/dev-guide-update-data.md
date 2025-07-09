---
title: 更新数据
summary: 了解如何更新数据和批量更新数据。
---

# 更新数据

本文档介绍如何使用以下 SQL 语句结合各种编程语言在 TiDB 中更新数据：

- [UPDATE](/sql-statements/sql-statement-update.md)：用于修改指定表中的数据。
- [INSERT ON DUPLICATE KEY UPDATE](/sql-statements/sql-statement-insert.md)：用于插入数据，如果存在主键或唯一键冲突，则更新该数据。如果表中存在多个唯一键（包括主键），**不推荐**使用此语句。因为该语句在检测到任何唯一键（包括主键）冲突时会更新数据。当存在多个冲突行时，只会更新其中一行。

## 开始之前

在阅读本文档之前，你需要准备以下内容：

- [搭建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读 [Schema Design Overview](/develop/dev-guide-schema-design-overview.md)、[创建数据库](/develop/dev-guide-create-database.md)、[创建表](/develop/dev-guide-create-table.md) 和 [创建二级索引](/develop/dev-guide-create-secondary-indexes.md)。
- 如果你想要 `UPDATE` 数据，首先需要 [插入数据](/develop/dev-guide-insert-data.md)。

## 使用 `UPDATE`

要更新表中的现有行，你需要使用带有 `WHERE` 子句的 [`UPDATE` 语句](/sql-statements/sql-statement-update.md)，以筛选需要更新的列。

> **注意：**
>
> 如果你需要更新大量行，例如超过一万行，建议不要一次性全部更新，而应逐步分批次迭代更新，直到所有行都更新完毕。你可以编写脚本或程序循环执行此操作。
> 详见 [Bulk-update](#bulk-update)。

### `UPDATE` SQL 语法

在 SQL 中，`UPDATE` 语句通常如下所示：

```sql
UPDATE {table} SET {update_column} = {update_value} WHERE {filter_column} = {filter_value}
```

| 参数名称 | 描述 |
| :--------------: | :------------------: |
| `{table}` | 表名 |
| `{update_column}` | 需要更新的列名 |
| `{update_value}` | 需要更新的列值 |
| `{filter_column}` | 用于筛选的列名 |
| `{filter_value}` | 用于筛选的列值 |

详细信息请参见 [UPDATE 语法](/sql-statements/sql-statement-update.md)。

### `UPDATE` 最佳实践

以下是一些更新数据的最佳实践：

- 始终在 `UPDATE` 语句中指定 `WHERE` 子句。如果没有 `WHERE` 子句，TiDB 将会更新 **_所有行_**。

<CustomContent platform="tidb">

- 当你需要更新大量行（例如超过一万行）时，建议使用 [bulk-update](#bulk-update)。因为 TiDB 限制了单个事务的大小（[txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit)，默认100 MB），一次性更新过多数据会导致持锁时间过长（[悲观事务](/pessimistic-transaction.md)）或引发冲突（[乐观事务](/optimistic-transaction.md)）。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 当你需要更新大量行（例如超过一万行）时，建议使用 [bulk-update](#bulk-update)。因为 TiDB 默认将单个事务的大小限制为 100 MB，过多的数据一次性更新会导致持锁时间过长（[悲观事务](/pessimistic-transaction.md)）或引发冲突（[乐观事务](/optimistic-transaction.md)）。

</CustomContent>

### `UPDATE` 示例

假设一位作者将她的名字改为 **Helen Haruki**，你需要更新 [authors](/develop/dev-guide-bookshop-schema-design.md#authors-table) 表。假设她的唯一 `id` 为 **1**，筛选条件为：`id = 1`。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
UPDATE `authors` SET `name` = "Helen Haruki" WHERE `id` = 1;
```

</div>

<div label="Java" value="java">

```java
// ds 是 com.mysql.cj.jdbc.MysqlDataSource 的实体
try (Connection connection = ds.getConnection()) {
    PreparedStatement pstmt = connection.prepareStatement("UPDATE `authors` SET `name` = ? WHERE `id` = ?");
    pstmt.setString(1, "Helen Haruki");
    pstmt.setInt(2, 1);
    pstmt.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>
</SimpleTab>

## 使用 `INSERT ON DUPLICATE KEY UPDATE`

如果你需要向表中插入新数据，但如果存在唯一键（包括主键）冲突，则会更新冲突的那条记录。你可以使用 `INSERT ... ON DUPLICATE KEY UPDATE ...` 语句实现插入或更新。

### `INSERT ON DUPLICATE KEY UPDATE` SQL 语法

在 SQL 中，`INSERT ... ON DUPLICATE KEY UPDATE ...` 语句通常如下所示：

```sql
INSERT INTO {table} ({columns}) VALUES ({values})
    ON DUPLICATE KEY UPDATE {update_column} = {update_value};
```

| 参数名称 | 描述 |
| :--------------: | :--------------: |
| `{table}` | 表名 |
| `{columns}` | 要插入的列名 |
| `{values}` | 要插入的列值 |
| `{update_column}` | 要更新的列名 |
| `{update_value}` | 要更新的列值 |

### `INSERT ON DUPLICATE KEY UPDATE` 最佳实践

- 仅在表中只有一个唯一键时使用 `INSERT ON DUPLICATE KEY UPDATE`。该语句在检测到任何 **_UNIQUE KEY_**（包括主键）冲突时会更新数据。如果存在多行冲突，只会更新其中一行。因此，除非你能保证冲突只有一行，否则不建议在具有多个唯一键的表中使用此语句。
- 在创建数据或更新数据时使用此语句。

### `INSERT ON DUPLICATE KEY UPDATE` 示例

例如，你需要更新 [ratings](/develop/dev-guide-bookshop-schema-design.md#ratings-table) 表，以包含用户对书的评分。如果用户尚未评分，则会创建新评分；如果已评分，则会更新之前的评分。

在下面的示例中，主键是 `book_id` 和 `user_id` 的联合主键。用户 `user_id = 1` 给一本书 `book_id = 1000` 评分为 `5`。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
INSERT INTO `ratings`
    (`book_id`, `user_id`, `score`, `rated_at`)
VALUES
    (1000, 1, 5, NOW())
ON DUPLICATE KEY UPDATE `score` = 5, `rated_at` = NOW();
```

</div>

<div label="Java" value="java">

```java
// ds 是 com.mysql.cj.jdbc.MysqlDataSource 的实体

try (Connection connection = ds.getConnection()) {
    PreparedStatement p = connection.prepareStatement("INSERT INTO `ratings` (`book_id`, `user_id`, `score`, `rated_at`)
VALUES (?, ?, ?, NOW()) ON DUPLICATE KEY UPDATE `score` = ?, `rated_at` = NOW()");
    p.setInt(1, 1000);
    p.setInt(2, 1);
    p.setInt(3, 5);
    p.setInt(4, 5);
    p.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>
</SimpleTab>

## 批量更新

当你需要在表中更新多行数据时，可以结合 [use `INSERT ON DUPLICATE KEY UPDATE`](#use-insert-on-duplicate-key-update) 和 `WHERE` 子句筛选需要更新的数据。

<CustomContent platform="tidb">

然而，如果你需要更新大量行（例如超过一万行），建议逐步迭代更新，即每次只更新部分数据，直到全部完成。这是因为 TiDB 限制了单个事务的大小（[txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit)，默认100 MB）。一次性更新过多数据会导致持锁时间过长（[悲观事务](/pessimistic-transaction.md)）或引发冲突（[乐观事务](/optimistic-transaction.md)）。你可以在程序或脚本中使用循环完成此操作。

</CustomContent>

<CustomContent platform="tidb-cloud">

然而，如果你需要更新大量行（例如超过一万行），建议逐步迭代更新，即每次只更新部分数据，直到全部完成。这是因为 TiDB 默认将单个事务的大小限制为 100 MB。一次性更新过多数据会导致持锁时间过长（[悲观事务](/pessimistic-transaction.md)）或引发冲突（[乐观事务](/optimistic-transaction.md)）。你可以在程序或脚本中使用循环完成此操作。

</CustomContent>

此部分提供了编写脚本进行迭代更新的示例。示例展示了如何结合 `SELECT` 和 `UPDATE` 完成批量更新。

### 编写批量更新循环

首先，你应在你的应用或脚本中编写一个 `SELECT` 查询。该查询的返回值可以作为需要更新行的主键。注意在定义此 `SELECT` 查询时，必须使用 `WHERE` 子句筛选需要更新的行。

### 示例

假设你在 `bookshop` 网站上过去一年收集了大量用户对书的评分，但原本的 5 分制设计导致评分缺乏差异化，大部分书的评分都为 `3`。你决定将评分从 5 分制切换到 10 分制，以实现更细腻的区分。

你需要将 `ratings` 表中的数据乘以 `2`，并在评分表中添加一个新列，用于标识是否已更新。利用此列，你可以在 `SELECT` 时筛选未更新的行，避免脚本崩溃或多次更新同一行导致数据异常。

例如，你创建一个名为 `ten_point` 的列，数据类型为 [BOOL](/data-type-numeric.md#boolean-type)，用作是否为 10 分制的标识：

```sql
ALTER TABLE `bookshop`.`ratings` ADD COLUMN `ten_point` BOOL NOT NULL DEFAULT FALSE;
```

> **注意：**
>
> 这个批量更新应用使用了 **DDL** 语句对数据表进行模式变更。所有 TiDB 的 DDL 变更操作都在线执行。更多信息请参见 [ADD COLUMN](/sql-statements/sql-statement-add-column.md)。

<SimpleTab groupId="language">
<div label="Golang" value="golang">

在 Golang 中，批量更新的示例程序类似如下：

```go
package main

import (
    "database/sql"
    "fmt"
    _ "github.com/go-sql-driver/mysql"
    "strings"
    "time"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    bookID, userID := updateBatch(db, true, 0, 0)
    fmt.Println("首次批量更新成功")
    for {
        time.Sleep(time.Second)
        bookID, userID = updateBatch(db, false, bookID, userID)
        fmt.Printf("批量更新成功，[bookID] %d，[userID] %d\n", bookID, userID)
    }
}

// updateBatch 在最多 1000 行数据中选择，更新评分
func updateBatch(db *sql.DB, firstTime bool, lastBookID, lastUserID int64) (bookID, userID int64) {
    // 选择最多 1000 个未更新到 10 分制的主键
    var err error
    var rows *sql.Rows

    if firstTime {
        rows, err = db.Query("SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` " +
            "WHERE `ten_point` != true ORDER BY `book_id`, `user_id` LIMIT 1000")
    } else {
        rows, err = db.Query("SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` "+
            "WHERE `ten_point` != true AND `book_id` > ? AND `user_id` > ? "+
            "ORDER BY `book_id`, `user_id` LIMIT 1000", lastBookID, lastUserID)
    }

    if err != nil || rows == nil {
        panic(fmt.Errorf("发生错误或行为空： %+v", err))
    }

    // 将所有ID合并成列表
    var idList []interface{}
    for rows.Next() {
        var tempBookID, tempUserID int64
        if err := rows.Scan(&tempBookID, &tempUserID); err != nil {
            panic(err)
        }
        idList = append(idList, tempBookID, tempUserID)
        bookID, userID = tempBookID, tempUserID
    }

    bulkUpdateSql := fmt.Sprintf("UPDATE `bookshop`.`ratings` SET `ten_point` = true, "+
        "`score` = `score` * 2 WHERE (`book_id`, `user_id`) IN (%s)", placeHolder(len(idList)))
    db.Exec(bulkUpdateSql, idList...)

    return bookID, userID
}

// placeHolder 格式化SQL占位符
func placeHolder(n int) string {
    holderList := make([]string, n/2, n/2)
    for i := range holderList {
        holderList[i] = "(?,?)"
    }
    return strings.Join(holderList, ",")
}
```

每次循环中，`SELECT` 按主键顺序查询未更新到 10 分制（`ten_point` 为 `false`）的最多 1000 行数据。每个 `SELECT` 语句会选择比上次最大主键值更大的主键，以避免重复。然后，利用批量更新，将 `score` 列乘以 `2`，并将 `ten_point` 设置为 `true`。更新 `ten_point` 的目的是为了防止在重启后重复更新同一行，导致数据损坏。`time.Sleep(time.Second)` 让每次循环暂停 1 秒，以减少硬件资源消耗。

</div>

<div label="Java (JDBC)" value="jdbc">

在 Java (JDBC) 中，批量更新的示例可能如下：

**代码：**

```java
package com.pingcap.bulkUpdate;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.*;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class BatchUpdateExample {
    static class UpdateID {
        private Long bookID;
        private Long userID;

        public UpdateID(Long bookID, Long userID) {
            this.bookID = bookID;
            this.userID = userID;
        }

        public Long getBookID() {
            return bookID;
        }

        public void setBookID(Long bookID) {
            this.bookID = bookID;
        }

        public Long getUserID() {
            return userID;
        }

        public void setUserID(Long userID) {
            this.userID = userID;
        }

        @Override
        public String toString() {
            return "[bookID] " + bookID + ", [userID] " + userID ;
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // 配置示例数据库连接。

        // 创建 MysqlDataSource 实例。
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // 设置服务器名、端口、数据库名、用户名和密码。
        mysqlDataSource.setServerName("localhost");
        mysqlDataSource.setPortNumber(4000);
        mysqlDataSource.setDatabaseName("bookshop");
        mysqlDataSource.setUser("root");
        mysqlDataSource.setPassword("");

        UpdateID lastID = batchUpdate(mysqlDataSource, null);

        System.out.println("首次批量更新成功");
        while (true) {
            TimeUnit.SECONDS.sleep(1);
            lastID = batchUpdate(mysqlDataSource, lastID);
            System.out.println("批量更新成功，[lastID] " + lastID);
        }
    }

    public static UpdateID batchUpdate (MysqlDataSource ds, UpdateID lastID) {
        try (Connection connection = ds.getConnection()) {
            UpdateID updateID = null;

            PreparedStatement selectPs;

            if (lastID == null) {
                selectPs = connection.prepareStatement(
                        "SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` " +
                        "WHERE `ten_point` != true ORDER BY `book_id`, `user_id` LIMIT 1000");
            } else {
                selectPs = connection.prepareStatement(
                        "SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` "+
                            "WHERE `ten_point` != true AND `book_id` > ? AND `user_id` > ? "+
                            "ORDER BY `book_id`, `user_id` LIMIT 1000");

                selectPs.setLong(1, lastID.getBookID());
                selectPs.setLong(2, lastID.getUserID());
            }

            List<Long> idList = new LinkedList<>();
            ResultSet res = selectPs.executeQuery();
            while (res.next()) {
                updateID = new UpdateID(
                        res.getLong("book_id"),
                        res.getLong("user_id")
                );
                idList.add(updateID.getBookID());
                idList.add(updateID.getUserID());
            }

            if (idList.isEmpty()) {
                System.out.println("没有需要更新的数据");
                return null;
            }

            String updateSQL = "UPDATE `bookshop`.`ratings` SET `ten_point` = true, "+
                    "`score` = `score` * 2 WHERE (`book_id`, `user_id`) IN (" +
                    placeHolder(idList.size() / 2) + ")";
            PreparedStatement updatePs = connection.prepareStatement(updateSQL);
            for (int i = 0; i < idList.size(); i++) {
                updatePs.setLong(i + 1, idList.get(i));
            }
            int count = updatePs.executeUpdate();
            System.out.println("更新了 " + count + " 条数据");

            return updateID;
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return null;
    }

    public static String placeHolder(int n) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n ; i++) {
            sb.append(i == 0 ? "(?,?)" : ",(?,?)");
        }

        return sb.toString();
    }
}
```

- `hibernate.cfg.xml` 配置：

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- 数据库连接设置 -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://localhost:4000/movie</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password"></property>
        <property name="hibernate.connection.autocommit">false</property>
        <property name="hibernate.jdbc.batch_size">20</property>

        <!-- 可选：显示 SQL 输出用于调试 -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

每次循环中，`SELECT` 按主键顺序查询未更新到 10 分制（`ten_point` 为 `false`）的最多 1000 行数据。每个 `SELECT` 语句会选择比上次最大主键值更大的主键，以避免重复。然后，利用批量更新，将 `score` 列乘以 `2`，并将 `ten_point` 设置为 `true`。更新 `ten_point` 的目的是为了防止在重启后重复更新同一行，导致数据损坏。`TimeUnit.SECONDS.sleep(1);` 让每次循环暂停 1 秒，以减少硬件资源消耗。

</div>

</SimpleTab>