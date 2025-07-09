---
title: Update Data
summary: データを更新する方法とデータを一括更新する方法について説明します。
---

# データの更新 {#update-data}

このドキュメントでは、さまざまなプログラミング言語で次の SQL ステートメントを使用して TiDB のデータを更新する方法について説明します。

-   [アップデート](/sql-statements/sql-statement-update.md) : 指定されたテーブル内のデータを変更するために使用されます。
-   [重複キー更新時の挿入](/sql-statements/sql-statement-insert.md) : 主キーまたは一意キーの競合がある場合に、データを挿入し、そのデータを更新するために使用されます。一意キー（主キーを含む）が複数ある場合は、このステートメントの使用は**推奨されません**。これは、このステートメントが一意キー（主キーを含む）の競合を検出すると、すぐにデータを更新するためです。複数の行の競合がある場合は、1行のみが更新されます。

## 始める前に {#before-you-start}

このドキュメントを読む前に、次のものを準備する必要があります。

-   [{{{ .starter }}}クラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md) [データベースを作成する](/develop/dev-guide-create-database.md)読ん[セカンダリインデックスを作成する](/develop/dev-guide-create-secondary-indexes.md)ください[テーブルを作成する](/develop/dev-guide-create-table.md)
-   `UPDATE`データが必要な場合は、まず[データを挿入する](/develop/dev-guide-insert-data.md)が必要です。

## <code>UPDATE</code>を使用する {#use-code-update-code}

テーブル内の既存の行を更新するには、 [`UPDATE`ステートメント](/sql-statements/sql-statement-update.md)と`WHERE`句を使用して更新する列をフィルターする必要があります。

> **注記：**
>
> 多数の行（例えば1万行以上）を更新する必要がある場合は、一度にすべての行を更新***する***のではなく、すべての行が更新されるまで、部分的な更新を繰り返すことをお勧めします。この操作をループさせるスクリプトやプログラムを作成することもできます。詳細は[一括更新](#bulk-update)ご覧ください。

### <code>UPDATE</code> SQL構文 {#code-update-code-sql-syntax}

SQL では、 `UPDATE`文は通常次の形式になります。

```sql
UPDATE {table} SET {update_column} = {update_value} WHERE {filter_column} = {filter_value}
```

|       パラメータ名      |        説明       |
| :---------------: | :-------------: |
|     `{table}`     |      テーブル名      |
| `{update_column}` |     更新するカラム名    |
|  `{update_value}` |    更新するカラムの値    |
| `{filter_column}` |  フィルターに一致するカラム名 |
|  `{filter_value}` | フィルターに一致するカラムの値 |

詳細については[UPDATE構文](/sql-statements/sql-statement-update.md)参照してください。

### ベストプラクティス<code>UPDATE</code> {#code-update-code-best-practices}

次に、データを更新するためのベスト プラクティスをいくつか示します。

-   `UPDATE`ステートメントでは必ず`WHERE`句を指定してください。5 `UPDATE`ステートメントに`WHERE`句がない場合、TiDBはテーブル内の***すべての行***を更新します。

<CustomContent platform="tidb">

-   多数の行（例えば1万行以上）を更新する必要がある場合は、 [一括更新](#bulk-update)使用してください。TiDBは単一トランザクションのサイズ（ [トランザクションの合計サイズ制限](/tidb-configuration-file.md#txn-total-size-limit) 、デフォルトでは100MB）に制限を設けているため、一度に大量のデータ更新を行うと、ロックの保持時間が長くなりすぎたり（ [悲観的取引](/pessimistic-transaction.md) ）、競合が発生したり（ [楽観的取引](/optimistic-transaction.md) ）する可能性があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   多数の行（例えば1万行以上）を更新する必要がある場合は、 [一括更新](#bulk-update)使用してください。TiDBはデフォルトで1トランザクションのサイズを100MBに制限しているため、一度に大量のデータ更新を行うと、ロックが長時間保持される（ [悲観的取引](/pessimistic-transaction.md) ）か、競合が発生する（ [楽観的取引](/optimistic-transaction.md) ）可能性があります。

</CustomContent>

### <code>UPDATE</code>例 {#code-update-code-example}

ある著者が**Helen Haruki**に改名したとします。3 [著者](/develop/dev-guide-bookshop-schema-design.md#authors-table)テーブルを変更する必要があります。彼女の固有`id`が**1**だとすると、フィルターは`id = 1`になります。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
UPDATE `authors` SET `name` = "Helen Haruki" WHERE `id` = 1;
```

</div>

<div label="Java" value="java">

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

テーブルに新しいデータを挿入する必要があるが、一意キー（主キーも一意キー）の競合が発生した場合、最初に競合が発生したレコードが更新されます。1 `INSERT ... ON DUPLICATE KEY UPDATE ...`ステートメントで挿入または更新を実行できます。

### <code>INSERT ON DUPLICATE KEY UPDATE</code> SQL構文 {#code-insert-on-duplicate-key-update-code-sql-syntax}

SQL では、 `INSERT ... ON DUPLICATE KEY UPDATE ...`文は通常次の形式になります。

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

### <code>INSERT ON DUPLICATE KEY UPDATE</code>ベストプラクティス {#code-insert-on-duplicate-key-update-code-best-practices}

-   `INSERT ON DUPLICATE KEY UPDATE` 、一意のキーが 1 つしかないテーブルにのみ使用してください。このステートメントは、***一意のキー***（主キーを含む）の競合が検出された場合、データを更新します。競合行が複数ある場合、更新されるのは 1 行のみです。したがって、競合行が 1 行だけであることを保証できない限り、複数の一意のキーを持つテーブルで`INSERT ON DUPLICATE KEY UPDATE`ステートメントを使用することは推奨されません。
-   データを作成または更新するときにこのステートメントを使用します。

### <code>INSERT ON DUPLICATE KEY UPDATE</code>例 {#code-insert-on-duplicate-key-update-code-example}

例えば、 [評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)テーブルを更新して、ユーザーによる書籍の評価を含める必要があります。ユーザーがまだ書籍を評価していない場合は、新しい評価が作成されます。ユーザーがすでに評価している場合は、以前の評価が更新されます。

次の例では、主キーは`book_id`と`user_id`の結合主キーです。ユーザー`user_id = 1`書籍`book_id = 1000`に`5`の評価を付けています。

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

テーブル内の複数のデータ行を更新する必要がある場合は、 [`INSERT ON DUPLICATE KEY UPDATE`を使用する](#use-insert-on-duplicate-key-update)と`WHERE`句を使用して、更新する必要があるデータをフィルター処理できます。

<CustomContent platform="tidb">

ただし、多数の行（たとえば、1万行以上）を更新する必要がある場合は、データを繰り返し更新することをお勧めします。つまり、更新が完了するまで、各反復でデータの一部のみを更新します。これは、TiDBが単一トランザクションのサイズ（デフォルトでは[トランザクションの合計サイズ制限](/tidb-configuration-file.md#txn-total-size-limit) MB）を制限しているためです。一度にデータを更新しすぎると、ロックが長時間保持される（ [悲観的取引](/pessimistic-transaction.md) ）、または競合が発生する（ [楽観的取引](/optimistic-transaction.md) ）ことになります。プログラムまたはスクリプトでループを使用して、操作を完了することができます。

</CustomContent>

<CustomContent platform="tidb-cloud">

ただし、多数の行（たとえば1万行以上）を更新する必要がある場合は、データを繰り返し更新することをお勧めします。つまり、更新が完了するまで、各反復でデータの一部のみを更新します。これは、TiDBがデフォルトで1トランザクションのサイズを100 MBに制限しているためです。一度に多くのデータを更新すると、ロックが長時間保持される（ [悲観的取引](/pessimistic-transaction.md) ）、または競合が発生する（ [楽観的取引](/optimistic-transaction.md) ）ことになります。プログラムまたはスクリプトでループを使用して、操作を完了することができます。

</CustomContent>

このセクションでは、反復更新を処理するスクリプトの記述例を示します。この例では、 `SELECT`と`UPDATE`組み合わせて一括更新を実行する方法を示します。

### 一括更新ループを書く {#write-bulk-update-loop}

まず、アプリケーションまたはスクリプトのループ内に`SELECT`クエリを記述します。このクエリの戻り値は、更新が必要な行の主キーとして使用できます。この`SELECT`クエリを定義する際は、 `WHERE`番目の句を使用して更新が必要な行をフィルタリングする必要があることに注意してください。

### 例 {#example}

過去1年間、あなたのウェブサイト`bookshop`でユーザーから多くの書籍評価が寄せられたとします。しかし、当初の5段階評価の設計では、書籍評価の差別化が不十分でした。ほとんどの書籍は`3`評価です。そこで、評価を差別化するために、5段階評価から10段階評価に変更することにしました。

先ほどの5段階評価の`ratings`番目のテーブルのデータを`2`倍し、評価テーブルに新しい列を追加して、行が更新されたかどうかを示します。この列を使用することで、 `SELECT`に更新された行を除外できます。これにより、スクリプトがクラッシュして行を複数回更新し、不合理なデータが生成されることを防ぐことができます。

たとえば、10 点スケールかどうかの識別子として、データ型[ブール](/data-type-numeric.md#boolean-type)を持つ`ten_point`という名前の列を作成します。

```sql
ALTER TABLE `bookshop`.`ratings` ADD COLUMN `ten_point` BOOL NOT NULL DEFAULT FALSE;
```

> **注記：**
>
> この一括更新アプリケーションは、 **DDL**文を使用してデータテーブルのスキーマを変更します。TiDBのすべてのDDL変更操作はオンラインで実行されます。詳細については、 [列を追加](/sql-statements/sql-statement-add-column.md)参照してください。

<SimpleTab groupId="language">
<div label="Golang" value="golang">

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

各反復で、 `SELECT`主キーの順にクエリを実行します。10 段階評価 ( `ten_point`は`false` ) に更新されていない最大`1000`行の主キー値を選択します。各`SELECT`文では、重複を防ぐため、前の`SELECT`結果の最大値よりも大きい主キーを選択します。次に、一括更新を使用し、その`score`列を`2`で乗算して、 `ten_point`を`true`に設定します。 `ten_point`更新する目的は、クラッシュ後の再起動時に更新アプリケーションが同じ行を繰り返し更新してデータ破損を引き起こすのを防ぐことです。 `time.Sleep(time.Second)`各ループで、更新アプリケーションを 1 秒間一時停止して、更新アプリケーションがハードウェア リソースを過剰に消費するのを防ぎます。

</div>

<div label="Java (JDBC)" value="jdbc">

Java (JDBC) では、一括更新アプリケーションは次のようになります。

**コード：**

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

-   `hibernate.cfg.xml`構成:

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

各反復で、 `SELECT`主キーの順にクエリを実行します。10 段階評価 ( `ten_point`は`false` ) に更新されていない最大`1000`行の主キー値を選択します。各`SELECT`文では、重複を防ぐため、前の`SELECT`結果の最大値よりも大きい主キーを選択します。次に、一括更新を使用し、その`score`列を`2`で乗算して、 `ten_point`を`true`に設定します。 `ten_point`更新する目的は、クラッシュ後の再起動時に更新アプリケーションが同じ行を繰り返し更新してデータ破損を引き起こすのを防ぐことです。 `TimeUnit.SECONDS.sleep(1);`各ループで、更新アプリケーションを 1 秒間一時停止して、更新アプリケーションがハードウェア リソースを過剰に消費するのを防ぎます。

</div>

</SimpleTab>

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
