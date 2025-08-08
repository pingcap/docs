---
title: Delete Data
summary: データを削除するための SQL 構文、ベスト プラクティス、例について学習します。
---

# データを削除 {#delete-data}

このドキュメントでは、 [消去](/sql-statements/sql-statement-delete.md) SQL文を使用してTiDB内のデータを削除する方法について説明します。期限切れのデータを定期的に削除する必要がある場合は、 [生きる時間](/time-to-live.md)機能を使用してください。

## 始める前に {#before-you-start}

このドキュメントを読む前に、次のものを準備する必要があります。

-   [TiDB Cloudサーバーレスクラスタの構築](/develop/dev-guide-build-cluster-in-cloud.md)
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md) [データベースを作成する](/develop/dev-guide-create-database.md) [セカンダリインデックスを作成する](/develop/dev-guide-create-secondary-indexes.md) [テーブルを作成する](/develop/dev-guide-create-table.md)
-   [データの挿入](/develop/dev-guide-insert-data.md)

## SQL構文 {#sql-syntax}

`DELETE`ステートメントは、通常、次の形式になります。

```sql
DELETE FROM {table} WHERE {filter}
```

|   パラメータ名   |     説明     |
| :--------: | :--------: |
|  `{table}` |    テーブル名   |
| `{filter}` | フィルターの一致条件 |

この例では、 `DELETE`の単純な使用例のみを示しています。詳細については、 [DELETE構文](/sql-statements/sql-statement-delete.md)参照してください。

## ベストプラクティス {#best-practices}

データを削除するときに従うべきベスト プラクティスを次に示します。

-   `DELETE`ステートメントでは必ず`WHERE`句を指定してください。5 `WHERE`の句が指定されていない場合、TiDBはテーブル内の***すべての行***を削除します。

<CustomContent platform="tidb">

-   TiDB では単一トランザクションのサイズが制限されるため (デフォルトでは[トランザクションの合計サイズ制限](/tidb-configuration-file.md#txn-total-size-limit) MB)、多数の行 (たとえば、1 万行以上) を削除する場合は[一括削除](#bulk-delete)使用します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDB ではデフォルトで単一トランザクションのサイズが 100 MB に制限されるため、多数の行 (たとえば、1 万行以上) を削除する場合は[一括削除](#bulk-delete)使用します。

</CustomContent>

-   テーブル内のすべてのデータを削除する場合は、 `DELETE`ステートメントではなく、 [`TRUNCATE`](/sql-statements/sql-statement-truncate.md)ステートメントを使用してください。
-   パフォーマンスに関する考慮事項については、 [パフォーマンスに関する考慮事項](#performance-considerations)参照してください。
-   大量のデータを削除する必要がある場合、 [非トランザクション一括削除](#non-transactional-bulk-delete)選択するとパフォーマンスが大幅に向上します。ただし、削除のトランザクション性が失われるため、ロールバック**はできません**。正しい操作を選択してください。

## 例 {#example}

特定の期間内にアプリケーションエラーが発生し、その期間内の[評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table) （例えば`2022-04-15 00:00:00`から`2022-04-15 00:15:00` ）のデータをすべて削除する必要がある場合、 `SELECT`ステートメントを使用して削除するレコードの数を確認できます。

```sql
SELECT COUNT(*) FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

10,000 件を超えるレコードが返された場合は、 [一括削除](#bulk-delete)使用して削除します。

返されるレコード数が 10,000 件未満の場合は、次の例を使用してそれらを削除します。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

SQL では、例は次のようになります。

```sql
DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java" value="java">

Javaでは、例は次のようになります。

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

Golangでの例は次のようになります。

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

Python では、例は次のようになります。

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

<CustomContent platform="tidb">

`rated_at`フィールドは[日付と時刻の型](/data-type-date-and-time.md)の`DATETIME`型です。これは、タイムゾーンとは無関係に、TiDB にリテラル値として格納されていると想定できます。一方、 `TIMESTAMP`型はタイムスタンプを格納するため、異なる[タイムゾーン](/configure-time-zone.md)には異なる時刻文字列が表示されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

`rated_at`フィールドは[日付と時刻の型](/data-type-date-and-time.md)の`DATETIME`型です。これは、タイムゾーンに関係なく、TiDB にリテラル値として保存されていると想定できます。一方、 `TIMESTAMP`型はタイムスタンプを保存するため、タイムゾーンが異なると異なる時刻文字列が表示されます。

</CustomContent>

> **注記：**
>
> MySQLと同様に、 `TIMESTAMP`データ型は[2038年問題](https://en.wikipedia.org/wiki/Year_2038_problem)影響を受けます。2038を超える値を保存する場合は、 `DATETIME`データ型を使用することをお勧めします。

## パフォーマンスに関する考慮事項 {#performance-considerations}

### TiDB GCメカニズム {#tidb-gc-mechanism}

TiDBは、 `DELETE`ステートメントを実行した直後にデータを削除するのではなく、データを削除準備完了としてマークします。その後、TiDB GC（ガベージコレクション）が古いデータをクリーンアップするのを待ちます。したがって、 `DELETE`ステートメントを実行しても、ディスク使用量はすぐには削減され***ません***。

GCはデフォルトで10分ごとに実行されます。各GCは**safe_point**と呼ばれる時点を計算します。この時点より前のデータは再利用されないため、TiDBは安全にクリーンアップできます。

詳細については[GCメカニズム](/garbage-collection-overview.md)参照してください。

### 統計情報を更新する {#update-statistical-information}

TiDBは[統計情報](/statistics.md)使用してインデックスの選択を決定します。大量のデータが削除された後、インデックスが正しく選択されないリスクが高くなります。3 [手動収集](/statistics.md#manual-collection)使用して統計を更新できます。これにより、TiDBオプティマイザはSQLパフォーマンスの最適化のためにより正確な統計情報を得ることができます。

## 一括削除 {#bulk-delete}

テーブルから複数行のデータを削除する必要がある場合は、 [`DELETE`例](#example)選択し、 `WHERE`句を使用して削除する必要があるデータをフィルター処理できます。

<CustomContent platform="tidb">

ただし、大量の行（1万行以上）を削除する必要がある場合は、反復的にデータを削除することをお勧めします。つまり、各反復でデータの一部を削除し、削除が完了するまで繰り返します。これは、TiDBが単一トランザクションのサイズ（デフォルトでは[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) ）に制限があるためです。プログラムやスクリプトでループを使用することで、このような操作を実行できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

ただし、多数の行（1万行以上）を削除する必要がある場合は、反復的にデータを削除することをお勧めします。つまり、各反復処理でデータの一部を削除し、削除が完了するまで繰り返します。これは、TiDBがデフォルトで1トランザクションのサイズを100MBに制限しているためです。プログラムやスクリプトでループを使用することで、このような操作を実行できます。

</CustomContent>

このセクションでは、反復的な削除操作を処理するスクリプトの記述例を示し、一括削除を完了するために`SELECT`と`DELETE`組み合わせる方法を示します。

### 一括削除ループを書く {#write-a-bulk-delete-loop}

アプリケーションまたはスクリプトのループに`DELETE`ステートメントを記述し、 `WHERE`句を使用してデータをフィルター処理し、 `LIMIT`使用して 1 つのステートメントで削除する行数を制限できます。

### 一括削除の例 {#bulk-delete-example}

特定の期間内にアプリケーションエラーが発生したとします。この期間（例えば`2022-04-15 00:00:00`から`2022-04-15 00:15:00`の[評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)のデータをすべて削除する必要があり、15分間で10,000件以上のレコードが書き込まれたとします。この場合、以下の手順で実行できます。

<SimpleTab groupId="language">
<div label="Java" value="java">

Javaでの一括削除の例は次のとおりです。

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

各反復で、 `DELETE` `2022-04-15 00:00:00`から`2022-04-15 00:15:00`までの最大 1000 行を削除します。

</div>

<div label="Golang" value="golang">

Golangでの一括削除の例は次のとおりです。

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

各反復で、 `DELETE` `2022-04-15 00:00:00`から`2022-04-15 00:15:00`までの最大 1000 行を削除します。

</div>

<div label="Python" value="python">

Python での一括削除の例は次のとおりです。

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

各反復で、 `DELETE` `2022-04-15 00:00:00`から`2022-04-15 00:15:00`までの最大 1000 行を削除します。

</div>

</SimpleTab>

## 非トランザクション一括削除 {#non-transactional-bulk-delete}

> **注記：**
>
> TiDBはv6.1.0以降、 [非トランザクションDMLステートメント](/non-transactional-dml.md)サポートしています。この機能はTiDB v6.1.0より前のバージョンでは使用できません。

### 非トランザクション一括削除の前提条件 {#prerequisites-of-non-transactional-bulk-delete}

非トランザクション一括削除を使用する前に、必ず[非トランザクションDMLステートメントのドキュメント](/non-transactional-dml.md)お読みください。非トランザクション一括削除は、バッチデータ処理シナリオにおけるパフォーマンスと使いやすさを向上させますが、トランザクションの原子性と独立性は損なわれます。

したがって、誤った取り扱いによる重大な結果（データ損失など）を回避するために、慎重に使用する必要があります。

### 非トランザクション一括削除のSQL構文 {#sql-syntax-for-non-transactional-bulk-delete}

非トランザクション一括削除ステートメントの SQL 構文は次のとおりです。

```sql
BATCH ON {shard_column} LIMIT {batch_size} {delete_statement};
```

|        パラメータ名        |         説明         |
| :------------------: | :----------------: |
|   `{shard_column}`   | バッチを分割するために使用される列。 |
|    `{batch_size}`    |   各バッチのサイズを制御します。  |
| `{delete_statement}` |  `DELETE`のステートメント。 |

上記の例は、非トランザクション型の一括削除ステートメントの単純な使用例を示したものです。詳細については、 [非トランザクションDML文](/non-transactional-dml.md)参照してください。

### 非トランザクション一括削除の例 {#example-of-non-transactional-bulk-delete}

[一括削除の例](#bulk-delete-example)と同じシナリオで、次の SQL ステートメントは非トランザクションの一括削除を実行する方法を示しています。

```sql
BATCH ON `rated_at` LIMIT 1000 DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
