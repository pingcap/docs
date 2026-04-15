---
title: Delete Data
summary: SQL構文、ベストプラクティス、およびデータ削除の例について学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-delete-data/','/ja/tidb/dev/dev-guide-delete-data/','/ja/tidbcloud/dev-guide-delete-data/']
---

# データ削除 {#delete-data}

このドキュメントでは、[消去](/sql-statements/sql-statement-delete.md)SQL ステートメントを使用して TiDB 内のデータを削除する方法について説明します。期限切れのデータを定期的に削除する必要がある場合は、[生きる時間](/develop/dev-guide-time-to-live.md)機能を使用してください。

## 始める前に {#before-you-start}

この文書を読む前に、以下のものを準備してください。

-   [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)、データベース[データベースを作成する](/develop/dev-guide-create-database.md)、[テーブルを作成する](/develop/dev-guide-create-table.md)、 [セカンダリインデックスを作成する](/develop/dev-guide-create-secondary-indexes.md)を読む
-   [データを挿入する](/develop/dev-guide-insert-data.md)

## SQL構文 {#sql-syntax}

`DELETE`ステートメントは、一般的に次の形式になります。

```sql
DELETE FROM {table} WHERE {filter}
```

|   パラメータ名   |     説明     |
| :--------: | :--------: |
|  `{table}` |    テーブル名   |
| `{filter}` | フィルターの適合条件 |

この例は`DELETE`の簡単な使用例のみを示しています。詳細については、 [DELETE構文](/sql-statements/sql-statement-delete.md)参照してください。 。

## ベストプラクティス {#best-practices}

データを削除する際に従うべきベストプラクティスを以下に示します。

-   `WHERE`ステートメントには、必ず`DELETE`句を指定してください。 `WHERE`句が指定されていない場合、TiDB はテーブル内の***すべての行***を削除します。

-   TiDB では 1 つのトランザクションのサイズが制限されているため (たとえば、1 万行以上)、大量の行を削除する場合は[一括削除](#bulk-delete)を使用します (段階[トランザクションの合計サイズ制限](/tidb-configuration-file.md#txn-total-size-limit)、デフォルトでは 100 MB)。

-   テーブル内のすべてのデータを削除する場合は、 `DELETE`ステートメントを使用しないでください。代わりに、 [`TRUNCATE`](/sql-statements/sql-statement-truncate.md)ステートメントを使用してください。

-   パフォーマンスに関する考慮事項については、[パフォーマンスに関する考慮事項](#performance-considerations)を参照してください。

-   大量のデータを削除する必要があるシナリオでは、[非トランザクション一括削除](#non-transactional-bulk-delete)パフォーマンスが大幅に向上します。ただし、これにより削除のトランザクションが失われるため、ロールバック**できません**。正しい操作を選択していることを確認してください。

## 例 {#example}

特定の期間内にアプリケーションエラーが見つかり、その期間内の[評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)に関するすべてのデータ（例えば、 `2022-04-15 00:00:00`から`2022-04-15 00:15:00`まで）を削除する必要がある場合を考えてみましょう。この場合、 `SELECT`ステートメントを使用して、削除するレコードの数を確認できます。

```sql
SELECT COUNT(*) FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

10,000 件を超えるレコードが返された場合は、[一括削除](#bulk-delete)を使用して削除します。

返されたレコード数が10,000件未満の場合は、以下の例を参考に削除してください。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

SQLにおける例は以下のとおりです。

```sql
DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java" value="java">

Javaでは、例は以下のとおりです。

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource

try (Connection connection = ds.getConnection()) {
    String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ?";
    PreparedStatement preparedStatement = connection.prepareStatement(sql);
    Calendar calendar = Calendar.getInstance();
    calendar.set(Calendar.MILLISECOND, 0);

    calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
    preparedStatement.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

    calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
    preparedStatement.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));

    preparedStatement.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>

<div label="Golang" value="golang">

Golangでは、例は以下のとおりです。

```go
package main

import (
    "database/sql"
    "fmt"
    "time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    startTime := time.Date(2022, 04, 15, 0, 0, 0, 0, time.UTC)
    endTime := time.Date(2022, 04, 15, 0, 15, 0, 0, time.UTC)

    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ?")
    result, err := db.Exec(bulkUpdateSql, startTime, endTime)
    if err != nil {
        panic(err)
    }
    _, err = result.RowsAffected()
    if err != nil {
        panic(err)
    }
}
```

</div>

<div label="Python" value="python">

Pythonでは、例は以下のとおりです。

```python
import MySQLdb
import datetime
import time
connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)
with connection:
    with connection.cursor() as cursor:
        start_time = datetime.datetime(2022, 4, 15)
        end_time = datetime.datetime(2022, 4, 15, 0, 15)
        delete_sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= %s AND `rated_at` <= %s"
        affect_rows = cursor.execute(delete_sql, (start_time, end_time))
        print(f'delete {affect_rows} data')
```

</div>

</SimpleTab>

> **注記：**
>
> -   `rated_at`フィールドは、[日付と時刻の種類](/data-type-date-and-time.md)種類の`DATETIME`タイプです。タイムゾーンに関係なく、TiDB にリテラル数量として保存されていると想定できます。一方、 `TIMESTAMP`タイプはタイムスタンプを保存するため、異なるタイム[タイムゾーン](/configure-time-zone.md)には異なる時刻文字列が表示されます。
> -   MySQLと同様に、 `TIMESTAMP`データ型は[2038年の問題](https://en.wikipedia.org/wiki/Year_2038_problem)の影響を受けます。2038より大きい値を格納する場合は、 `DATETIME`型を使用することをお勧めします。

## パフォーマンスに関する考慮事項 {#performance-considerations}

### TiDB GCメカニズム {#tidb-gc-mechanism}

TiDB は`DELETE`ステートメントを実行した直後にデータを削除するわけではありません。代わりに、削除準備完了としてデータをマークします。その後、TiDB GC (ガベージ コレクション) が古いデータをクリーンアップするまで待機します。したがって、 `DELETE`ステートメントを実行しても、ディスク使用量はすぐには削減さ***れません***。

デフォルトでは、GC（ガベージコレクション）は10分ごとに実行されます。各GCでは、 **safe_point**と呼ばれる時点が計算されます。この時点より前のデータは再利用されないため、TiDBは安全にクリーンアップできます。

詳細については、 [GCメカニズム](/garbage-collection-overview.md)を参照してください。

### 統計情報を更新する {#update-statistical-information}

TiDBは[統計情報](/statistics.md)を使用してインデックスの選択を決定します。大量のデータが削除された後、インデックスが正しく選択されないリスクが高くなります。この問題を解決するには、統計情報を更新してください。これにより、[手動収集](/statistics.md#manual-collection)オプティマイザはSQLパフォーマンス最適化のためのより正確な統計情報を取得できます。

## 一括削除 {#bulk-delete}

テーブルから複数のデータ行を削除する必要がある場合は、 [`DELETE`例](#example)選択し、 `WHERE`句を使用して削除する必要のあるデータをフィルタリングできます。

ただし、大量の行（1万行以上）を削除する必要がある場合は、反復的にデータを削除することをお勧めします。つまり、削除が完了するまで、各反復処理でデータの一部を削除していく方法です。これは、TiDBが単一トランザクションのサイズを制限しているためです（ [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 、デフォルトでは100MB）。このような操作を実行するには、プログラムやスクリプトでループを使用できます。

このセクションでは、反復削除操作を処理するスクリプトの書き方の例を示し、 `SELECT`と`DELETE`を組み合わせて一括削除を完了する方法を示します。

### 一括削除ループを作成する {#write-a-bulk-delete-loop}

アプリケーションまたはスクリプトのループ内に`DELETE`ステートメントを記述し、 `WHERE`句を使用してデータをフィルタリングし、 `LIMIT`を使用して単一のステートメントで削除する行数を制限できます。

### 一括削除の例 {#bulk-delete-example}

特定の期間内にアプリケーションエラーが見つかったとします。この期間内の[評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)に関するすべてのデータ（例えば、 `2022-04-15 00:00:00`から`2022-04-15 00:15:00`まで）を削除する必要があり、15 分で 10,000 件以上のレコードが書き込まれるとします。次のように実行できます。

<SimpleTab groupId="language">
<div label="Java" value="java">

Javaにおける一括削除の例は以下のとおりです。

```java
package com.pingcap.bulkDelete;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.*;
import java.util.*;
import java.util.concurrent.TimeUnit;

public class BatchDeleteExample
{
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

        while (true) {
            batchDelete(mysqlDataSource);
            TimeUnit.SECONDS.sleep(1);
        }
    }

    public static void batchDelete (MysqlDataSource ds) {
        try (Connection connection = ds.getConnection()) {
            String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ? LIMIT 1000";
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            Calendar calendar = Calendar.getInstance();
            calendar.set(Calendar.MILLISECOND, 0);

            calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
            preparedStatement.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

            calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
            preparedStatement.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));

            int count = preparedStatement.executeUpdate();
            System.out.println("delete " + count + " data");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

各反復処理で、 `DELETE`は`2022-04-15 00:00:00`から`2022-04-15 00:15:00`まで最大 1000 行を削除します。

</div>

<div label="Golang" value="golang">

Golangにおける一括削除の例は以下のとおりです。

```go
package main

import (
    "database/sql"
    "fmt"
    "time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    affectedRows := int64(-1)
    startTime := time.Date(2022, 04, 15, 0, 0, 0, 0, time.UTC)
    endTime := time.Date(2022, 04, 15, 0, 15, 0, 0, time.UTC)

    for affectedRows != 0 {
        affectedRows, err = deleteBatch(db, startTime, endTime)
        if err != nil {
            panic(err)
        }
    }
}

// deleteBatch delete at most 1000 lines per batch
func deleteBatch(db *sql.DB, startTime, endTime time.Time) (int64, error) {
    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ? LIMIT 1000")
    result, err := db.Exec(bulkUpdateSql, startTime, endTime)
    if err != nil {
        return -1, err
    }
    affectedRows, err := result.RowsAffected()
    if err != nil {
        return -1, err
    }

    fmt.Printf("delete %d data\n", affectedRows)
    return affectedRows, nil
}
```

各反復処理で、 `DELETE`は`2022-04-15 00:00:00`から`2022-04-15 00:15:00`まで最大 1000 行を削除します。

</div>

<div label="Python" value="python">

Pythonにおける一括削除の例は以下のとおりです。

```python
import MySQLdb
import datetime
import time
connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)
with connection:
    with connection.cursor() as cursor:
        start_time = datetime.datetime(2022, 4, 15)
        end_time = datetime.datetime(2022, 4, 15, 0, 15)
        affect_rows = -1
        while affect_rows != 0:
            delete_sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= %s AND  `rated_at` <= %s LIMIT 1000"
            affect_rows = cursor.execute(delete_sql, (start_time, end_time))
            print(f'delete {affect_rows} data')
            time.sleep(1)
```

各反復処理で、 `DELETE`は`2022-04-15 00:00:00`から`2022-04-15 00:15:00`まで最大 1000 行を削除します。

</div>

</SimpleTab>

## 非トランザクション一括削除 {#non-transactional-bulk-delete}

> **注記：**
>
> v6.1.0 以降、TiDB は[非トランザクションDMLステートメント](/non-transactional-dml.md)ステートメントをサポートします。この機能は、TiDB v6.1.0 より前のバージョンでは使用できません。

### 非トランザクション一括削除の前提条件 {#prerequisites-of-non-transactional-bulk-delete}

非トランザクション一括削除を使用する前に、[非トランザクションDMLステートメントのドキュメント](/non-transactional-dml.md)ドキュメントを必ず読んでください。非トランザクション一括削除により、バッチ データ処理シナリオのパフォーマンスと使いやすさが向上しますが、トランザクションの原子性と分離性が損なわれます。

したがって、誤った取り扱いによる重大な結果（データ損失など）を避けるため、慎重に使用する必要があります。

### トランザクション処理を伴わない一括削除のためのSQL構文 {#sql-syntax-for-non-transactional-bulk-delete}

トランザクション処理を行わない一括削除ステートメントのSQL構文は以下のとおりです。

```sql
BATCH ON {shard_column} LIMIT {batch_size} {delete_statement};
```

|        パラメータ名        |         説明         |
| :------------------: | :----------------: |
|   `{shard_column}`   | バッチを分割するために使用される列。 |
|    `{batch_size}`    |   各バッチのサイズを制御する。   |
| `{delete_statement}` |  `DELETE`ステートメント。  |

前述の例は、非トランザクション一括削除ステートメントの単純な使用例のみを示しています。詳細については、[非トランザクションDMLステートメント](/non-transactional-dml.md)を参照してください。

### トランザクション処理を伴わない一括削除の例 {#example-of-non-transactional-bulk-delete}

[一括削除の例](#bulk-delete-example)と同じシナリオで、次の SQL ステートメントは非トランザクション一括削除を実行する方法を示しています。

```sql
BATCH ON `rated_at` LIMIT 1000 DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
