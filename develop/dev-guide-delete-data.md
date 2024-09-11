---
title: Delete Data
summary: データを削除するための SQL 構文、ベスト プラクティス、および例について学習します。
---

# データを削除 {#delete-data}

このドキュメントでは、 [消去](/sql-statements/sql-statement-delete.md) SQL ステートメントを使用して TiDB 内のデータを削除する方法について説明します。期限切れのデータを定期的に削除する必要がある場合は、 [生きる時間](/time-to-live.md)機能を使用してください。

## 始める前に {#before-you-start}

このドキュメントを読む前に、次のものを準備する必要があります。

-   [TiDB Cloudサーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md)
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md) [データベースを作成する](/develop/dev-guide-create-database.md) [テーブルを作成する](/develop/dev-guide-create-table.md) [セカンダリインデックスを作成する](/develop/dev-guide-create-secondary-indexes.md)
-   [データの挿入](/develop/dev-guide-insert-data.md)

## SQL構文 {#sql-syntax}

`DELETE`ステートメントは通常、次の形式になります。

```sql
DELETE FROM {table} WHERE {filter}
```

|   パラメータ名   |     説明     |
| :--------: | :--------: |
|  `{table}` |    テーブル名   |
| `{filter}` | フィルターの一致条件 |

この例では、 `DELETE`の単純な使用例のみを示しています。詳細については、 [DELETE構文](/sql-statements/sql-statement-delete.md)を参照してください。

## ベストプラクティス {#best-practices}

データを削除する際に従うべきベスト プラクティスを次に示します。

-   `DELETE`ステートメントでは必ず`WHERE`句を指定`WHERE`ます。5 句が指定されていない場合、TiDB はテーブル内の***すべての行***を削除します。

<CustomContent platform="tidb">

-   TiDB では単一トランザクションのサイズが制限されるため (デフォルトでは[トランザクションの合計サイズ制限](/tidb-configuration-file.md#txn-total-size-limit) 、100 MB)、多数の行 (たとえば、1 万行以上) を削除する場合は[一括削除](#bulk-delete)使用します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDB では、デフォルトで 1 つのトランザクションのサイズが 100 MB に制限されるため、多数の行 (たとえば、1 万行以上) を削除する場合は[一括削除](#bulk-delete)使用します。

</CustomContent>

-   テーブル内のすべてのデータを削除する場合は、 `DELETE`ステートメントを使用しないでください。代わりに、 [`TRUNCATE`](/sql-statements/sql-statement-truncate.md)ステートメントを使用します。
-   パフォーマンスに関する考慮事項については、 [パフォーマンスに関する考慮事項](#performance-considerations)参照してください。
-   大量のデータを削除する必要があるシナリオでは、 [非トランザクション一括削除](#non-transactional-bulk-delete)使用するとパフォーマンスが大幅に向上します。ただし、削除のトランザクションが失われるため、ロールバック**できません**。正しい操作を選択していることを確認してください。

## 例 {#example}

特定の期間内にアプリケーション エラーが見つかり、この期間内の[評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)データ (たとえば`2022-04-15 00:00:00`から`2022-04-15 00:15:00` ) をすべて削除する必要があるとします。この場合、 `SELECT`ステートメントを使用して、削除するレコードの数を確認できます。

```sql
SELECT COUNT(*) FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

10,000 件を超えるレコードが返された場合は、 [一括削除](#bulk-delete)使用して削除します。

返されるレコードが 10,000 件未満の場合は、次の例を使用してそれらを削除します。

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

Golangでは、例は次のようになります。

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

`rated_at`フィールドは[日付と時刻の種類](/data-type-date-and-time.md)の`DATETIME`タイプです。タイムゾーンに関係なく、TiDB にリテラル量として格納されていると想定できます。一方、 `TIMESTAMP`タイプはタイムスタンプを格納するため、異なる[タイムゾーン](/configure-time-zone.md)に異なる時間文字列が表示されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

`rated_at`フィールドは[日付と時刻の種類](/data-type-date-and-time.md)の`DATETIME`タイプです。タイム ゾーンに関係なく、TiDB にリテラル量として格納されていると想定できます。一方、 `TIMESTAMP`タイプはタイムスタンプを格納するため、異なるタイム ゾーンでは異なる時間文字列が表示されます。

</CustomContent>

> **注記：**
>
> MySQL と同様に、 `TIMESTAMP`データ型は[2038年問題](https://en.wikipedia.org/wiki/Year_2038_problem)の影響を受けます。2038 より大きい値を保存する場合は、 `DATETIME`型を使用することをお勧めします。

## パフォーマンスに関する考慮事項 {#performance-considerations}

### TiDB GC メカニズム {#tidb-gc-mechanism}

TiDB は、 `DELETE`ステートメントを実行してもすぐにデータを削除しません。代わりに、データを削除準備完了としてマークします。その後、TiDB GC (ガベージ コレクション) が古いデータをクリーンアップするまで待機します。したがって、 `DELETE`ステートメントでは、ディスク使用量はすぐには削減されませ***ん***。

GC は、デフォルトでは 10 分ごとに 1 回トリガーされます。各 GC は**safe_point**と呼ばれるタイム ポイントを計算します。このタイム ポイントより前のデータは再度使用されないため、TiDB は安全にクリーンアップできます。

詳細については[GCメカニズム](/garbage-collection-overview.md)参照してください。

### 統計情報を更新する {#update-statistical-information}

TiDB は[統計情報](/statistics.md)使用してインデックスの選択を決定します。大量のデータが削除された後、インデックスが正しく選択されないリスクが高くなります。統計を更新するには[手動収集](/statistics.md#manual-collection)使用できます。これにより、TiDB オプティマイザーに SQL パフォーマンスの最適化のためのより正確な統計情報が提供されます。

## 一括削除 {#bulk-delete}

テーブルから複数行のデータを削除する必要がある場合は、 [`DELETE`例](#example)を選択し、 `WHERE`句を使用して削除する必要があるデータをフィルター処理できます。

<CustomContent platform="tidb">

ただし、多数の行 (1 万行以上) を削除する必要がある場合は、データを繰り返し削除することをお勧めします。つまり、削除が完了するまで、各反復でデータの一部を削除します。これは、TiDB が単一トランザクションのサイズを制限しているためです (デフォルトでは[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) MB)。プログラムまたはスクリプトでループを使用して、このような操作を実行できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

ただし、多数の行 (1 万行以上) を削除する必要がある場合は、データを繰り返し削除することをお勧めします。つまり、削除が完了するまで、各反復でデータの一部を削除します。これは、TiDB が 1 つのトランザクションのサイズをデフォルトで 100 MB に制限しているためです。プログラムまたはスクリプトでループを使用して、このような操作を実行できます。

</CustomContent>

このセクションでは、反復削除操作を処理するスクリプトの記述例を示し、一括削除を完了するために`SELECT`と`DELETE`を組み合わせる方法を示します。

### 一括削除ループを書く {#write-a-bulk-delete-loop}

アプリケーションまたはスクリプトのループ内に`DELETE`ステートメントを記述し、 `WHERE`句を使用してデータをフィルター処理し、 `LIMIT`を使用して単一のステートメントで削除する行数を制限できます。

### 一括削除の例 {#bulk-delete-example}

特定の期間内にアプリケーション エラーが見つかったとします。この期間内の[評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)のデータをすべて削除する必要があり、たとえば`2022-04-15 00:00:00`から`2022-04-15 00:15:00`まで、15 分間に 10,000 件を超えるレコードが書き込まれているとします。次のように実行できます。

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
> v6.1.0 以降、TiDB は[非トランザクションDMLステートメント](/non-transactional-dml.md)サポートします。この機能は、TiDB v6.1.0 より前のバージョンでは使用できません。

### 非トランザクション一括削除の前提条件 {#prerequisites-of-non-transactional-bulk-delete}

非トランザクション一括削除を使用する前に、まず[非トランザクション DML ステートメントのドキュメント](/non-transactional-dml.md)必ずお読みください。非トランザクション一括削除により、バッチ データ処理シナリオでのパフォーマンスと使いやすさが向上しますが、トランザクションの原子性と分離性が損なわれます。

したがって、誤った取り扱いによる重大な結果（データ損失など）を回避するために、慎重に使用する必要があります。

### 非トランザクション一括削除のSQL構文 {#sql-syntax-for-non-transactional-bulk-delete}

非トランザクション一括削除ステートメントの SQL 構文は次のとおりです。

```sql
BATCH ON {shard_column} LIMIT {batch_size} {delete_statement};
```

|        パラメータ名        |          説明         |
| :------------------: | :-----------------: |
|   `{shard_column}`   |  バッチを分割するために使用される列。 |
|    `{batch_size}`    |   各バッチのサイズを制御します。   |
| `{delete_statement}` | `DELETE`番目のステートメント。 |

上の例は、非トランザクション一括削除ステートメントの単純な使用例のみを示しています。詳細については、 [非トランザクションDMLステートメント](/non-transactional-dml.md)を参照してください。

### 非トランザクション一括削除の例 {#example-of-non-transactional-bulk-delete}

[一括削除の例](#bulk-delete-example)と同じシナリオで、次の SQL ステートメントは非トランザクションの一括削除を実行する方法を示しています。

```sql
BATCH ON `rated_at` LIMIT 1000 DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
