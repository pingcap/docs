---
title: Update Data
summary: The ways, best practices and examples for updating data, batch update data.
---

# Update Data

This page will show the following SQL statements to update the data in TiDB with various programming languages:

- [UPDATE](https://docs.pingcap.com/tidb/stable/sql-statement-update): Used to modify the data in the specified table.
- [INSERT ON DUPLICATE KEY UPDATE](https://docs.pingcap.com/tidb/stable/sql-statement-insert): Used to insert data and update this data if there is a primary key or unique key conflict. Note that **_NOT RECOMMENDED_** to use this statement if there are multiple unique keys (including primary keys). This is because this statement will update the data if any unique key (including primary key) conflicts are detected. When more than one row is matched to a conflict, only one row of data will be updated.

## Before you start

Before reading this page, you need to prepare the following:

- [Build a TiDB Cluster in TiDB Cloud(DevTier)](/develop/build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/schema-design-overview.md), [Create a Database](/develop/create-database.md), [Create a Table](/develop/create-table.md), and [Create Secondary Indexes](/develop/create-secondary-indexes.md).
- If you need to `UPDATE` data, you need to [insert data](/develop/insert-data.md) first.

## Using `UPDATE`

To update an existing row in a table, you need to use a [UPDATE statement](https://docs.pingcap.com/tidb/stable/sql-statement-update) with a `WHERE` clause, i.e., you need to filter the columns for updating.

> **Note:**
>
> If you need to update a large number of rows, say tens of thousands or more, then we recommend **_NOT_** doing a complete update at once, but rather updating a portion at a time iteratively until all rows are updated. You can write scripts or programs that use loops to do this.
> You can refer to [Bulk-update](#bulk-update) for guidelines.

### `UPDATE` SQL Syntax

In SQL, the `UPDATE` statement is generally of the following form:

{{< copyable "sql" >}}

```sql
UPDATE {table} SET {update_column} = {update_value} WHERE {filter_column} = {filter_value}
```

| Parameter Name | Description |
| :---------------: | :------------------: |
|     `{table}`     |         Table Name         |
| `{update_column}` |     Column names to be updated     |
| `{update_value}`  |   Column values to be updated   |
| `{filter_column}` | Column names used by conditional filters |
| `{filter_value}`  | Column values used by conditional filters |

This only shows a simple usage of `UPDATE`. For detailed documentation, refer to TiDB's [UPDATE syntax](https://docs.pingcap.com/tidb/stable/sql-statement-update) page.

### `UPDATE` Best Practices

There are some best practices to follow when updating rows as follows:

- Always specify the `WHERE` clause in the update statement. If the `UPDATE` does not have a `WHERE` clause, TiDB will update **_ALL ROWS_** within this table.
- Use [bulk-update](#bulk-update) when you need to update a large number of rows (tens of thousands or more), because TiDB has a single transaction size limit of [txn-total-size-limit](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) (default is 100MB) and too many data updates at once will result in holding locks for too long ([pessimistic transactions](https://docs.pingcap.com/tidb/stable/pessimistic-transaction)) or creating a lot of conflicts ([optimistic transactions](https://docs.pingcap.com/tidb/stable/optimistic-transaction)).

### `UPDATE` Example

Suppose an author changes his/her name to **Helen Haruki** and needs to change our [authors](/develop/bookshop-schema-design.md#authors-table) table. Assume that his/her unique `id` is **1**, i.e. the filter should be: `id = 1`.

<SimpleTab>
<div label="SQL" href="update-sql">

{{< copyable "sql" >}}

```sql
UPDATE `authors` SET `name` = "Helen Haruki" WHERE `id` = 1;
```

</div>

<div label="Java" href="update-java">

{{< copyable "" >}}

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource
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

## Using `INSERT ON DUPLICATE KEY UPDATE`

If you need to insert new data into a table, but if any unique key (primary key is also a unique key) conflicts, the first conflicting data will be updated, you can use `INSERT ... ON DUPLICATE KEY UPDATE ...` statement to insert or update.

### `INSERT ON DUPLICATE KEY UPDATE` SQL Syntax

In SQL, the `INSERT ... ON DUPLICATE KEY UPDATE ...` statement is generally of the following form:

{{< copyable "sql" >}}

```sql
INSERT INTO {table} ({columns}) VALUES ({values})
    ON DUPLICATE KEY UPDATE {update_column} = {update_value};
```

| Parameter Name | Description |
| :---------------: | :--------------: |
|     `{table}`     |       Table Name       |
|    `{columns}`    |   Column names to be inserted   |
|    `{values}`     | Column values to be inserted |
| `{update_column}` |   Column names to be updated   |
| `{update_value}`  | Column values to be updated |

### `INSERT ON DUPLICATE KEY UPDATE` Best Practices

- Only wse `INSERT ON DUPLICATE KEY UPDATE` on a table with one unique key. This statement will update the data if any **_UNIQUE KEY_** (including the primary key) conflicts are detected. If more than one row is matched for a conflict, only one row of data will be matched. Therefore, it is not recommended to use the `INSERT ON DUPLICATE KEY UPDATE` statement in tables with multiple unique keys unless you can guarantee that there is only one row of conflict.
- Use this statement in a create or update scenario.

### `INSERT ON DUPLICATE KEY UPDATE` Example

For example, we need to update the [ratings](/develop/bookshop-schema-design.md#ratings-table) table to include the user's ratings for the book, so that if the user has not yet rated the book, a new rating will be created, and if the user has already rated it, then his previous rating will be updated.

The primary key here is the joint primary key of `book_id` and `user_id`. `user_id` is `1` and gives a rating of `5` to a book with a `book_id` of `1000`.

<SimpleTab>
<div label="SQL" href="upsert-sql">

{{< copyable "sql" >}}

```sql
INSERT INTO `ratings`
    (`book_id`, `user_id`, `score`, `rated_at`)
VALUES
    (1000, 1, 5, NOW())
ON DUPLICATE KEY UPDATE `score` = 5, `rated_at` = NOW();
```

</div>

<div label="Java" href="upsert-java">

{{< copyable "" >}}

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource

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

## Bulk-update

When you need to update multiple rows of data in a table, you can choose to [use `UPDATE`](#using-update) and use the `WHERE` clause to filter the data that needs to be updated.

However, if you need to update a large number of rows (tens of thousands or more), we recommend using an iteration that updates only a portion of the data at a time until the update is all done. This is because TiDB has a single transaction size limit of [txn-total-size-limit](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) (100MB by default), and too many data updates at once will result in holding locks for too long ([pessimistic transactions](https://docs.pingcap.com/tidb/stable/pessimistic-transaction), or creating a lot of conflicts ([optimistic transactions](https://docs.pingcap.com/tidb/stable/optimistic-transaction)). You can use a loop in your program or script to complete the operation.

This page provides examples of writing scripts to handle recurring updates. This example shows how a combination of `SELECT` and `UPDATE` should be done to complete a bulk-update.

### Write bulk-update loop

First, you should write a `SELECT` query in a loop of your application or script. The return value of this query can be used as the primary key for the rows that need to be updated. Note that when defining this `SELECT` query, you need to be careful to use the `WHERE` clause to filter the rows that need to be updated.

### Example

Suppose that we have had a lot of book ratings from users on our `bookshop` site over the past year, but the original design of a 5-point scale has resulted in a lack of differentiation in book ratings, with a large number of books rated around a `3`, so we decided to change the 5-point scale to a 10-point scale. We decided to switch from a 5-point scale to a 10-point scale to increase the differentiation of book ratings.

At this point, we need to multiply by `2` the data in the `ratings` table from the previous 5-point scale and add a new column to the ratings table to indicate whether the rows have been updated. Using this column, we can filter out rows that have been updated in `SELECT`, which will prevent the script from crashing and updating the rows multiple times, resulting in unreasonable data.

For example, you could create a column named `ten_point` with the data type [BOOL](https://docs.pingcap.com/tidb/stable/data-type-numeric#boolean-type) as an identifier of whether it is a 10-point scale:

{{< copyable "sql" >}}

```sql
ALTER TABLE `bookshop`.`ratings` ADD COLUMN `ten_point` BOOL NOT NULL DEFAULT FALSE;
```

> **Note:**
>
> This bulk-update application will use **DDL** statements to make schema changes to the data tables. all DDL change operations for TiDB are online, see here for the [ADD COLUMN](https://docs.pingcap.com/tidb/stable/sql-statement-add-column) statements used here.

<SimpleTab>
<div label="Golang">

In Golang, a bulk-update application might be similar to the following:

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
    fmt.Println("first time batch update success")
    for {
        time.Sleep(time.Second)
        bookID, userID = updateBatch(db, false, bookID, userID)
        fmt.Printf("batch update success, [bookID] %d, [userID] %d\n", bookID, userID)
    }
}

// updateBatch select at most 1000 lines data to update score
func updateBatch(db *sql.DB, firstTime bool, lastBookID, lastUserID int64) (bookID, userID int64) {
    // select at most 1000 primary keys in five-point scale data
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
        panic(fmt.Errorf("error occurred or rows nil: %+v", err))
    }

    // joint all id with a list
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

// placeHolder format SQL place holder
func placeHolder(n int) string {
    holderList := make([]string, n/2, n/2)
    for i := range holderList {
        holderList[i] = "(?,?)"
    }
    return strings.Join(holderList, ",")
}
```

In each iteration, `SELECT` queries in primary key order, selecting primary key values for up to `1000` rows of data that have not been updated to the 10-point scale (`ten_point` is `false`). Each `SELECT` with a primary key larger than the largest of the previous `SELECT` results to prevent duplication. Then, using a bulk-update, multiply its `score` column by `2` and set `ten_point` to `true`. The point of updating `ten_point` is to prevent our update application from crashing and restarting and repeatedly updating the same row of data, which can lead to data corruption. `time.Sleep(time.Second)` in each loop will make the update application pause for 1 second to prevent the update application from taking up too much hardware resources.

</div>

<div label="Java (JDBC)">

In Java (JDBC), a bulk-update application might be similar to the following:

**Code：**

{{< copyable "" >}}

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
        // Configure the example database connection.

        // Create a mysql data source instance.
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // Set server name, port, database name, username and password.
        mysqlDataSource.setServerName("localhost");
        mysqlDataSource.setPortNumber(4000);
        mysqlDataSource.setDatabaseName("bookshop");
        mysqlDataSource.setUser("root");
        mysqlDataSource.setPassword("");

        UpdateID lastID = batchUpdate(mysqlDataSource, null);

        System.out.println("first time batch update success");
        while (true) {
            TimeUnit.SECONDS.sleep(1);
            lastID = batchUpdate(mysqlDataSource, lastID);
            System.out.println("batch update success, [lastID] " + lastID);
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
                System.out.println("no data should update");
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
            System.out.println("update " + count + " data");

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

- `hibernate.cfg.xml` configuration:

{{< copyable "" >}}

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://localhost:4000/movie</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password"></property>
        <property name="hibernate.connection.autocommit">false</property>
        <property name="hibernate.jdbc.batch_size">20</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

In each iteration, `SELECT` queries in primary key order, selecting primary key values for up to `1000` rows of data that have not been updated to the 10-point scale (`ten_point` is `false`). Each `SELECT` with a primary key larger than the largest of the previous `SELECT` results to prevent duplication. Then, using a bulk-update, multiply its `score` column by `2` and set `ten_point` to `true`. The point of updating `ten_point` is to prevent our update application from crashing and restarting and repeatedly updating the same row of data, which can lead to data corruption. `TimeUnit.SECONDS.sleep(1);` in each loop will make the update application pause for 1 second to prevent the update application from taking up too much hardware resources.

</div>

</SimpleTab>
