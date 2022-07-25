---
title: Update Data
summary: Learn about how to update data and batch update data.
---

# データの更新 {#update-data}

このドキュメントでは、次のSQLステートメントを使用して、さまざまなプログラミング言語でTiDBのデータを更新する方法について説明します。

-   [アップデート](/sql-statements/sql-statement-update.md) ：指定されたテーブルのデータを変更するために使用されます。
-   [重複するキーの更新時に挿入](/sql-statements/sql-statement-insert.md) ：主キーまたは一意キーの競合がある場合に、データを挿入してこのデータを更新するために使用されます。複数の一意のキー（主キーを含む）がある場合は、このステートメントを使用することは**お勧め**しません。これは、このステートメントが一意のキー（主キーを含む）の競合を検出すると、データを更新するためです。複数の行の競合がある場合、1つの行のみが更新されます。

## 始める前に {#before-you-start}

このドキュメントを読む前に、以下を準備する必要があります。

-   [TiDB CloudでTiDBクラスターを構築する（DevTier）](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md) 、および[データベースを作成する](/develop/dev-guide-create-database.md)を[セカンダリインデックスを作成する](/develop/dev-guide-create-secondary-indexes.md) [テーブルを作成する](/develop/dev-guide-create-table.md) 。
-   `UPDATE`のデータが必要な場合は、最初に[データを挿入](/develop/dev-guide-insert-data.md)にする必要があります。

## <code>UPDATE</code>を使用する {#use-code-update-code}

テーブル内の既存の行を更新するには、 [`UPDATE`ステートメント](/sql-statements/sql-statement-update.md)と`WHERE`の句を使用して、更新する列をフィルタリングする必要があります。

> **ノート：**
>
> 1万を超えるなど、多数の行を更新する必要がある場合は、一度に完全な***更新***を行うのではなく、すべての行が更新されるまで一度に一部を繰り返し更新することをお勧めします。この操作をループするスクリプトまたはプログラムを作成できます。詳細については、 [一括更新](#bulk-update)を参照してください。

### <code>UPDATE</code>構文 {#code-update-code-sql-syntax}

SQLでは、 `UPDATE`ステートメントは通常次の形式になります。

{{< copyable "" >}}

```sql
UPDATE {table} SET {update_column} = {update_value} WHERE {filter_column} = {filter_value}
```

|       パラメータ名      |       説明       |
| :---------------: | :------------: |
|     `{table}`     |      テーブル名     |
| `{update_column}` |    更新するカラム名    |
|  `{update_value}` |    更新するカラムの値   |
| `{filter_column}` |  フィルタに一致するカラム名 |
|  `{filter_value}` | フィルタに一致するカラムの値 |

詳細については、 [UPDATE構文](/sql-statements/sql-statement-update.md)を参照してください。

### ベストプラクティスを<code>UPDATE</code>する {#code-update-code-best-practices}

以下は、データを更新するためのいくつかのベストプラクティスです。

-   `UPDATE`ステートメントでは常に`WHERE`句を指定してください。 `UPDATE`ステートメントに`WHERE`句がない場合、TiDBはテーブル内の***すべてのROWS***を更新します。
-   多数の行（たとえば、1万を超える）を更新する必要がある場合は、 [一括更新](#bulk-update)を使用します。 TiDBは単一のトランザクションのサイズを制限しているため（デフォルトでは[txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit) MB）、一度に多くのデータ更新を行うと、ロックが長時間保持されたり（ [悲観的な取引](/pessimistic-transaction.md) ）、競合が発生したりします（ [楽観的な取引](/optimistic-transaction.md) ）。

### <code>UPDATE</code>例 {#code-update-code-example}

著者が彼女の名前を**HelenHaruki**に変更するとします。 [著者](/develop/dev-guide-bookshop-schema-design.md#authors-table)のテーブルを変更する必要があります。彼女の一意の`id`が<strong>1</strong>であり、フィルターが`id = 1`であると想定します。

<SimpleTab>
<div label="SQL">

{{< copyable "" >}}

```sql
UPDATE `authors` SET `name` = "Helen Haruki" WHERE `id` = 1;
```

</div>

<div label="Java">

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

## <code>INSERT ON DUPLICATE KEY UPDATE</code>を使用する {#use-code-insert-on-duplicate-key-update-code}

テーブルに新しいデータを挿入する必要があるが、一意のキー（主キーも一意のキー）の競合がある場合、最初に競合したレコードが更新されます。 `INSERT ... ON DUPLICATE KEY UPDATE ...`のステートメントを使用して、挿入または更新できます。

### <code>INSERT ON DUPLICATE KEY UPDATE</code>構文 {#code-insert-on-duplicate-key-update-code-sql-syntax}

SQLでは、 `INSERT ... ON DUPLICATE KEY UPDATE ...`ステートメントは通常次の形式になります。

{{< copyable "" >}}

```sql
INSERT INTO {table} ({columns}) VALUES ({values})
    ON DUPLICATE KEY UPDATE {update_column} = {update_value};
```

|       パラメータ名      |     説明    |
| :---------------: | :-------: |
|     `{table}`     |   テーブル名   |
|    `{columns}`    |  挿入するカラム名 |
|     `{values}`    | 挿入するカラムの値 |
| `{update_column}` |  更新するカラム名 |
|  `{update_value}` | 更新するカラムの値 |

### 重複する<code>INSERT ON DUPLICATE KEY UPDATE</code>のベストプラクティス {#code-insert-on-duplicate-key-update-code-best-practices}

-   `INSERT ON DUPLICATE KEY UPDATE`は、一意のキーが1つあるテーブルにのみ使用します。このステートメントは、 ***UNIQUE KEY*** （主キーを含む）の競合が検出された場合にデータを更新します。競合の行が複数ある場合は、1行のみが更新されます。したがって、競合の行が1つしかないことを保証できない限り、複数の一意キーを持つテーブルで`INSERT ON DUPLICATE KEY UPDATE`ステートメントを使用することはお勧めしません。
-   このステートメントは、データを作成するとき、またはデータを更新するときに使用します。

### <code>INSERT ON DUPLICATE KEY UPDATE</code> {#code-insert-on-duplicate-key-update-code-example}

たとえば、本に対するユーザーの評価を含めるために[評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)テーブルを更新する必要があります。ユーザーがまだ本を評価していない場合は、新しい評価が作成されます。ユーザーがすでに評価している場合は、以前の評価が更新されます。

次の例では、主キーは`book_id`と`user_id`の共同主キーです。ユーザー`user_id = 1`は、本`book_id = 1000`に`5`の評価を与える。

<SimpleTab>
<div label="SQL">

{{< copyable "" >}}

```sql
INSERT INTO `ratings`
    (`book_id`, `user_id`, `score`, `rated_at`)
VALUES
    (1000, 1, 5, NOW())
ON DUPLICATE KEY UPDATE `score` = 5, `rated_at` = NOW();
```

</div>

<div label="Java">

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

## 一括更新 {#bulk-update}

テーブル内のデータの複数の行を更新する必要がある場合は、 `WHERE`句を使用して[`INSERT ON DUPLICATE KEY UPDATE`を使用します](#use-insert-on-duplicate-key-update)を実行し、更新する必要のあるデータをフィルタリングできます。

ただし、多数の行（たとえば、1万を超える行）を更新する必要がある場合は、データを繰り返し更新することをお勧めします。つまり、更新が完了するまで、各反復でデータの一部のみを更新します。 。これは、 [txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit)が単一のトランザクションのサイズを制限しているためです（デフォルトでは1、100 MB）。一度にデータの更新が多すぎると、ロックの保持時間が長すぎます（ [悲観的な取引](/pessimistic-transaction.md) 、または競合が発生します（ [楽観的な取引](/optimistic-transaction.md) ）。プログラムまたはスクリプトでループを使用して、操作を完了することができます。

このセクションでは、反復更新を処理するスクリプトの作成例を示します。この例は、一括更新を完了するために`SELECT`と`UPDATE`の組み合わせを実行する方法を示しています。

### 一括更新ループの記述 {#write-bulk-update-loop}

まず、アプリケーションまたはスクリプトのループに`SELECT`のクエリを記述する必要があります。このクエリの戻り値は、更新が必要な行の主キーとして使用できます。この`SELECT`クエリを定義するときは、 `WHERE`句を使用して、更新が必要な行をフィルタリングする必要があることに注意してください。

### 例 {#example}

過去1年間に、 `bookshop`のWebサイトでユーザーからの本の評価が多かったが、5段階のスケールの元の設計により、本の評価に差異がなかったとします。ほとんどの本は`3`と評価されています。評価を区別するために、5ポイントスケールから10ポイントスケールに切り替えることにしました。

前の5ポイントスケールの`ratings`テーブルのデータに`2`を掛け、新しい列を評価テーブルに追加して、行が更新されたかどうかを示す必要があります。この列を使用すると、 `SELECT`で更新された行を除外できます。これにより、スクリプトがクラッシュして行が複数回更新され、データが不合理になるのを防ぐことができます。

たとえば、10ポイントのスケールであるかどうかの識別子としてデータ型[BOOL](/data-type-numeric.md#boolean-type)を使用して`ten_point`という名前の列を作成します。

{{< copyable "" >}}

```sql
ALTER TABLE `bookshop`.`ratings` ADD COLUMN `ten_point` BOOL NOT NULL DEFAULT FALSE;
```

> **ノート：**
>
> この一括更新アプリケーションは、 **DDL**ステートメントを使用してデータテーブルにスキーマを変更します。 TiDBのすべてのDDL変更操作はオンラインで実行されます。詳細については、 [列を追加](/sql-statements/sql-statement-add-column.md)を参照してください。

<SimpleTab>
<div label="Golang">

Golangでは、一括更新アプリケーションは次のようになります。

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

各反復で、主キーの順序で`SELECT`のクエリを実行します。 10ポイントスケール（ `ten_point`は`false` ）に更新されていない最大`1000`行の主キー値を選択します。各`SELECT`ステートメントは、重複を防ぐために、前の`SELECT`の結果の最大のものよりも大きい主キーを選択します。次に、一括更新を使用し、 `score`列に`2`を掛け、 `ten_point`を`true`に設定します。更新`ten_point`の目的は、クラッシュ後に再起動した場合に、更新アプリケーションが同じ行を繰り返し更新することを防ぐことです。これにより、データが破損する可能性があります。各ループの`time.Sleep(time.Second)`は、更新アプリケーションが1秒間一時停止して、更新アプリケーションが多くのハードウェアリソースを消費するのを防ぎます。

</div>

<div label="Java (JDBC)">

Java（JDBC）では、一括更新アプリケーションは次のようになります。

**コード：**

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

-   `hibernate.cfg.xml`構成：

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

各反復で、主キーの順序で`SELECT`のクエリを実行します。 10ポイントスケール（ `ten_point`は`false` ）に更新されていない最大`1000`行の主キー値を選択します。各`SELECT`ステートメントは、重複を防ぐために、前の`SELECT`の結果の最大のものよりも大きい主キーを選択します。次に、一括更新を使用し、 `score`列に`2`を掛け、 `ten_point`を`true`に設定します。更新`ten_point`の目的は、クラッシュ後に再起動した場合に、更新アプリケーションが同じ行を繰り返し更新することを防ぐことです。これにより、データが破損する可能性があります。各ループの`TimeUnit.SECONDS.sleep(1);`は、更新アプリケーションが1秒間一時停止して、更新アプリケーションが多くのハードウェアリソースを消費するのを防ぎます。

</div>

</SimpleTab>
