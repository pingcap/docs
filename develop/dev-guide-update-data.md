---
title: Update Data
summary: データの更新方法と一括データ更新方法について学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-update-data/','/ja/tidb/dev/dev-guide-update-data/','/ja/tidbcloud/dev-guide-update-data/']
---

# データの更新 {#update-data}

このドキュメントでは、さまざまなプログラミング言語を使用して、以下のSQL文でTiDBのデータを更新する方法について説明します。

-   [アップデート](/sql-statements/sql-statement-update.md): 指定されたテーブル内のデータを変更するために使用されます。
-   キー[重複キー更新時に挿入](/sql-statements/sql-statement-insert.md): データの挿入、および主キーまたは一意キーの競合が発生した場合のデータの更新に使用します。複数の一意キー（主キーを含む）がある場合は、このステートメントの使用は**推奨されません**。これは、このステートメントが一意キー（主キーを含む）の競合を検出するとすぐにデータを更新するためです。複数の行で競合が発生した場合、更新されるのは1行のみです。

## 始める前に {#before-you-start}

この文書を読む前に、以下のものを準備してください。

-   [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)、データベース[データベースを作成する](/develop/dev-guide-create-database.md)、[テーブルを作成する](/develop/dev-guide-create-table.md)、 [セカンダリインデックスを作成する](/develop/dev-guide-create-secondary-indexes.md)読んでください。
-   `UPDATE`データを取得したい場合は、最初に[データを挿入する](/develop/dev-guide-insert-data.md)必要があります。

## <code>UPDATE</code>を使用する {#use-code-update-code}

テーブル内の既存の行を更新するには、更新対象の列をフィルタリングするために`WHERE`句を含む[`UPDATE`文](/sql-statements/sql-statement-update.md)使用する必要があります。

> **注記：**
>
> 多数の行（例えば1万行以上）を更新する必要がある場合は、一度にすべてを更新するのではなく、すべての行が更新されるまで、一部ずつ繰り返し更新することをお***勧め***します。この操作をループさせるスクリプトやプログラムを作成できます。詳しくは[一括更新](#bulk-update)ご覧ください。

### <code>UPDATE</code> SQL構文 {#code-update-code-sql-syntax}

SQLでは、 `UPDATE`ステートメントは一般的に次の形式になります。

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

詳細については、 [UPDATE構文](/sql-statements/sql-statement-update.md)を参照してください。

### ベストプラクティス<code>UPDATE</code> {#code-update-code-best-practices}

データ更新に関するベストプラクティスを以下に示します。

-   `WHERE`ステートメントには、必ず`UPDATE`句を指定してください。 `UPDATE`ステートメントに`WHERE`句がない場合、TiDB はテーブル内の***すべての行***を更新します。
-   大量の行 (たとえば、1 万行以上) を更新する必要がある場合は[一括更新](#bulk-update)使用します。 TiDB は 1 つのトランザクションのサイズを制限しているため ( [トランザクションの合計サイズ制限](/tidb-configuration-file.md#txn-total-size-limit)、デフォルトでは 100 MB)、一度にあまりにも多くのデータ更新が行われると、長時間ロックが保持されすぎたり ([悲観的取引](/pessimistic-transaction.md))、競合が発生したり ([楽観的取引](/optimistic-transaction.md)) されます。

### <code>UPDATE</code>例 {#code-update-code-example}

[著者](/develop/dev-guide-bookshop-schema-design.md#authors-table)が名前を**ヘレン・ハルキ**に変更したとします。テーブルを変更する必要があります。彼女の固有の`id`が**1で**あると仮定すると、フィルターは`id = 1`になります。

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

## <code>INSERT ON DUPLICATE KEY UPDATE</code>使用する {#use-code-insert-on-duplicate-key-update-code}

テーブルに新しいデータを挿入する必要があるが、一意キー（主キーも一意キーです）の競合がある場合、最初に競合したレコードが更新されます。挿入または更新には`INSERT ... ON DUPLICATE KEY UPDATE ...`ステートメントを使用できます。

### <code>INSERT ON DUPLICATE KEY UPDATE</code> SQL構文 {#code-insert-on-duplicate-key-update-code-sql-syntax}

SQLでは、 `INSERT ... ON DUPLICATE KEY UPDATE ...`ステートメントは一般的に次の形式になります。

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

-   `INSERT ON DUPLICATE KEY UPDATE`は、一意キーが 1 つだけのテーブルでのみ使用してください。このステートメントは***、一意キー***(主キーを含む) の競合が検出された場合、データを更新します。競合する行が複数ある場合、更新されるのは 1 行のみです。したがって、競合する行が 1 つだけであることを保証できない限り、一意キーが複数あるテーブルで`INSERT ON DUPLICATE KEY UPDATE`ステートメントを使用することはお勧めしません。
-   データを作成または更新する際に、このステートメントを使用してください。

### <code>INSERT ON DUPLICATE KEY UPDATE</code>例 {#code-insert-on-duplicate-key-update-code-example}

例えば、 [評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)テーブルを更新して、ユーザーが書籍に付けた評価を含める必要があるとします。ユーザーがまだ書籍を評価していない場合は、新しい評価が作成されます。ユーザーが既に評価している場合は、以前の評価が更新されます。

次の例では、主キーは`book_id`と`user_id`の結合主キーです。ユーザー`user_id = 1`書籍`5`に`book_id = 1000`という評価を与えます。

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

テーブル内の複数のデータ行を更新する必要がある場合は、 [`INSERT ON DUPLICATE KEY UPDATE`使用する](#use-insert-on-duplicate-key-update)`WHERE`句を使用して、更新する必要のあるデータをフィルタリングできます。

ただし、多数の行 (たとえば、1 万行以上) を更新する必要がある場合は、データを繰り返し更新すること、つまり、更新が完了するまで各繰り返しでデータの一部のみを更新することをお勧めします。これは、TiDB が単一トランザクションのサイズを制限しているためです ( [トランザクションの合計サイズ制限](/tidb-configuration-file.md#txn-total-size-limit)、デフォルトでは 100 MB)。一度にあまりに多くのデータ更新を行うと、長時間ロックが保持されたり ([悲観的取引](/pessimistic-transaction.md)、競合が発生したり ([楽観的取引](/optimistic-transaction.md)) されます。プログラムまたはスクリプトでループを使用すると、操作を完了できます。

このセクションでは、反復的な更新を処理するスクリプトの記述例を示します。この例では`SELECT`と`UPDATE`を組み合わせて一括更新を完了する方法を示します。

### 一括更新ループを書き込む {#write-bulk-update-loop}

まず、アプリケーションまたはスクリプトのループ内に`SELECT`クエリを記述してください。このクエリの戻り値は、更新が必要な行の主キーとして使用できます。この`SELECT`クエリを定義する際には、更新が必要な行をフィルタリングするために`WHERE`句を使用する必要があることに注意してください。

### 例 {#example}

過去 1 年間`bookshop`ウェブサイトでユーザーから多くの書籍評価が寄せられたとします。しかし、当初の 5 段階評価では書籍評価の区別がつきにくく、ほとんどの書籍が`3`と評価されています。そこで、評価を区別するために、5 段階評価から 10 段階評価に変更することにしました。

前の5段階評価の`2`テーブルのデータに`ratings`を乗算し、評価テーブルに行が更新されたかどうかを示す新しい列を追加する必要があります。この列を使用すると、 `SELECT`で更新された行を除外できるため、スクリプトがクラッシュして行が複数回更新され、不合理なデータが生成されることを防ぐことができます。

例えば、データ型が[ブール](/data-type-numeric.md#boolean-type)である列を`ten_point`として作成し、それが10点スケールであるかどうかの識別子とします。

```sql
ALTER TABLE `bookshop`.`ratings` ADD COLUMN `ten_point` BOOL NOT NULL DEFAULT FALSE;
```

> **注記：**
>
> この一括更新アプリケーションは、 **DDL**ステートメントを使用してデータテーブルのスキーマを変更します。TiDB のすべての DDL 変更操作はオンラインで実行されます。詳細については、[列を追加](/sql-statements/sql-statement-add-column.md)参照してください。

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

各イテレーションでは、 `SELECT`主キーの順にクエリを実行します。10 ポイントスケールに更新されていない行 ( `1000`は { `ten_point`の最大`false` PLACEHOLDER-1-PLACEHOLDER-E}} まで主キー値を選択します。 `SELECT`ステートメントは、重複を防ぐために、前の`SELECT`の結果の中で最大の主キーよりも大きい主キーを選択します。次に、一括更新を使用して、 `score`列に`2`を掛け、 `ten_point`を`true`に設定します。 `ten_point`を更新する目的は、クラッシュ後に再起動した場合に更新アプリケーションが同じ行を繰り返し更新してデータ破損を引き起こすのを防ぐためです。各ループの`time.Sleep(time.Second)`は、更新アプリケーションがハードウェア リソースを過剰に消費するのを防ぐために、更新アプリケーションを 1 秒間一時停止させます。

</div>

<div label="Java (JDBC)" value="jdbc">

Java （JDBC）における一括更新アプリケーションは、以下のようなものになるかもしれません。

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

-   `hibernate.cfg.xml`設定:

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

各イテレーションでは、 `SELECT`主キーの順にクエリを実行します。10 ポイントスケールに更新されていない行 ( `1000`は { `ten_point`の最大`false` PLACEHOLDER-1-PLACEHOLDER-E}} まで主キー値を選択します。 `SELECT`ステートメントは、重複を防ぐために、前の`SELECT`の結果の中で最大の主キーよりも大きい主キーを選択します。次に、一括更新を使用して、 `score`列に`2`を掛け、 `ten_point`を`true`に設定します。 `ten_point`を更新する目的は、クラッシュ後に再起動した場合に更新アプリケーションが同じ行を繰り返し更新してデータ破損を引き起こすのを防ぐためです。各ループの`TimeUnit.SECONDS.sleep(1);`は、更新アプリケーションがハードウェア リソースを過剰に消費するのを防ぐために、更新アプリケーションを 1 秒間一時停止させます。

</div>

</SimpleTab>

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
