---
title: Delete Data
summary: Learn about the SQL syntax, best practices, and examples for deleting data.
---

# データの削除 {#delete-data}

このドキュメントでは、 [消去](/sql-statements/sql-statement-delete.md) SQL ステートメントを使用して TiDB 内のデータを削除する方法について説明します。期限切れのデータを定期的に削除する必要がある場合は、 [有効期間](/time-to-live.md)機能を使用してください。

## 始める前に {#before-you-start}

このドキュメントを読む前に、以下を準備する必要があります。

-   [TiDB サーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md)
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md) 、 [データベースを作成する](/develop/dev-guide-create-database.md) 、 [テーブルを作成する](/develop/dev-guide-create-table.md) 、および[セカンダリインデックスの作成](/develop/dev-guide-create-secondary-indexes.md)を読み取ります
-   [データの挿入](/develop/dev-guide-insert-data.md)

## SQL 構文 {#sql-syntax}

`DELETE`ステートメントは通常、次の形式になります。

```sql
DELETE FROM {table} WHERE {filter}
```

|   パラメータ名   |       説明      |
| :--------: | :-----------: |
|  `{table}` |     テーブル名     |
| `{filter}` | フィルターのマッチング条件 |

この例では、 `DELETE`の単純な使用例のみを示します。詳細については、 [DELETE 構文](/sql-statements/sql-statement-delete.md)を参照してください。

## ベストプラクティス {#best-practices}

データを削除するときに従うべきいくつかのベスト プラクティスを次に示します。

-   `DELETE`ステートメントには必ず`WHERE`句を指定します。 `WHERE`句が指定されていない場合、TiDB はテーブル内の***すべての行を***削除します。

<CustomContent platform="tidb">

-   大量の行 (たとえば、1 万行以上) を削除する場合は、 [一括削除](#bulk-delete)を使用します。これは、TiDB が単一トランザクションのサイズを制限しているためです (デフォルトでは[txn 合計サイズ制限](/tidb-configuration-file.md#txn-total-size-limit) MB)。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDB は単一トランザクションのサイズをデフォルトで 100 MB に制限しているため、大量の行 (たとえば、1 万行以上) を削除する場合は[一括削除](#bulk-delete)使用します。

</CustomContent>

-   テーブル内のすべてのデータを削除する場合は、 `DELETE`ステートメントを使用しないでください。代わりに、 [`TRUNCATE`](/sql-statements/sql-statement-truncate.md)ステートメントを使用してください。
-   パフォーマンスに関する考慮事項については、 [パフォーマンスに関する考慮事項](#performance-considerations)を参照してください。
-   大量のデータを削除する必要があるシナリオでは、 [非トランザクション一括削除](#non-transactional-bulk-delete)指定するとパフォーマンスが大幅に向上します。ただし、これにより削除のトランザクションが失われるため、ロールバックでき**ません**。正しい操作を選択していることを確認してください。

## 例 {#example}

特定の期間内にアプリケーション エラーが見つかり、この期間内の[評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)のすべてのデータ (たとえば`2022-04-15 00:00:00`から`2022-04-15 00:15:00`を削除する必要があるとします。この場合、 `SELECT`ステートメントを使用して、削除されるレコードの数を確認できます。

```sql
SELECT COUNT(*) FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

10,000 を超えるレコードが返された場合は、 [一括削除](#bulk-delete)を使用して削除します。

返されるレコードが 10,000 未満の場合は、次の例を使用してレコードを削除します。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

SQL の例は次のとおりです。

```sql
DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java" value="java">

Javaの例は次のとおりです。

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

Golangの例は次のとおりです。

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

Python の例は次のとおりです。

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

`rated_at`フィールドは[日付と時刻のタイプ](/data-type-date-and-time.md)の`DATETIME`タイプです。タイムゾーンに関係なく、TiDB にリテラル数量として保存されていると想定できます。一方、 `TIMESTAMP`タイプはタイムスタンプを格納するため、異なる[タイムゾーン](/configure-time-zone.md)で異なる時刻文字列を表示します。

</CustomContent>

<CustomContent platform="tidb-cloud">

`rated_at`フィールドは[日付と時刻のタイプ](/data-type-date-and-time.md)の`DATETIME`タイプです。タイムゾーンに関係なく、TiDB にリテラル数量として保存されていると想定できます。一方、 `TIMESTAMP`タイプはタイムスタンプを格納するため、タイムゾーンが異なると異なる時刻文字列を表示します。

</CustomContent>

> **注記：**
>
> MySQL と同様に、 `TIMESTAMP`データ型は[2038年問題](https://en.wikipedia.org/wiki/Year_2038_problem)の影響を受けます。 2038 より大きい値を保存する場合は、 `DATETIME`タイプを使用することをお勧めします。

## パフォーマンスに関する考慮事項 {#performance-considerations}

### TiDB GC メカニズム {#tidb-gc-mechanism}

TiDB は、 `DELETE`ステートメントを実行した直後にはデータを削除しません。代わりに、データを削除準備完了としてマークします。次に、TiDB GC (ガベージ コレクション) が古いデータをクリーンアップするのを待ちます。したがって、 `DELETE`ステートメントによってディスク使用量がすぐに削減される***わけではありません***。

GC はデフォルトで 10 分ごとにトリガーされます。各 GC は、 **safe_point**と呼ばれる時点を計算します。この時点より前のデータは再使用されないため、TiDB は安全にクリーンアップできます。

詳細については、 [GC機構](/garbage-collection-overview.md)を参照してください。

### 統計情報を更新する {#update-statistical-information}

TiDB は[統計情報](/statistics.md)を使用してインデックスの選択を決定します。大量のデータが削除された後は、インデックスが正しく選択されない可能性が高くなります。 [手動収集](/statistics.md#manual-collection)使用して統計を更新できます。これは、SQL パフォーマンスを最適化するためのより正確な統計情報を TiDB オプティマイザーに提供します。

## 一括削除 {#bulk-delete}

テーブルから複数のデータ行を削除する必要がある場合は、 [`DELETE`例](#example)を選択し、 `WHERE`句を使用して、削除する必要があるデータをフィルタリングできます。

<CustomContent platform="tidb">

ただし、大量の行 (1 万行を超える) を削除する必要がある場合は、データを反復的に削除することをお勧めします。つまり、削除が完了するまで反復ごとにデータの一部を削除します。これは、TiDB が単一トランザクションのサイズを制限しているためです (デフォルトでは[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) MB)。プログラムまたはスクリプトでループを使用して、このような操作を実行できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

ただし、大量の行 (1 万行を超える) を削除する必要がある場合は、データを反復的に削除することをお勧めします。つまり、削除が完了するまで反復ごとにデータの一部を削除します。これは、TiDB がデフォルトで 1 つのトランザクションのサイズを 100 MB に制限しているためです。プログラムまたはスクリプトでループを使用して、このような操作を実行できます。

</CustomContent>

このセクションでは、反復削除操作を処理するスクリプトの作成例を示し、一括削除を完了するために`SELECT`と`DELETE`を組み合わせて実行する方法を示します。

### 一括削除ループを作成する {#write-a-bulk-delete-loop}

アプリケーションまたはスクリプトのループに`DELETE`ステートメントを記述し、 `WHERE`句を使用してデータをフィルタリングし、 `LIMIT`句を使用して 1 つのステートメントで削除する行数を制限できます。

### 一括削除の例 {#bulk-delete-example}

特定の期間内にアプリケーション エラーが見つかったとします。この期間内に[評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)のデータをすべて削除する必要があります (たとえば、 `2022-04-15 00:00:00`から`2022-04-15 00:15:00`まで)。15 分間に 10,000 件を超えるレコードが書き込まれます。以下のように実行できます。

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
> v6.1.0 以降、TiDB は[非トランザクション DML ステートメント](/non-transactional-dml.md)をサポートします。この機能は、TiDB v6.1.0 より前のバージョンでは使用できません。

### 非トランザクション一括削除の前提条件 {#prerequisites-of-non-transactional-bulk-delete}

非トランザクション一括削除を使用する前に、必ず最初に[非トランザクション DML ステートメントのドキュメント](/non-transactional-dml.md)をお読みください。非トランザクション一括削除により、バッチ データ処理シナリオのパフォーマンスと使いやすさが向上しますが、トランザクションの原子性と分離性が損なわれます。

したがって、誤った取り扱いによる重大な結果 (データ損失など) を避けるために、慎重に使用する必要があります。

### 非トランザクション一括削除の SQL 構文 {#sql-syntax-for-non-transactional-bulk-delete}

非トランザクション一括削除ステートメントの SQL 構文は次のとおりです。

```sql
BATCH ON {shard_column} LIMIT {batch_size} {delete_statement};
```

|        パラメータ名        |          説明          |
| :------------------: | :------------------: |
|   `{shard_column}`   | バッチを分割するために使用されるカラム。 |
|    `{batch_size}`    |    各バッチのサイズを制御します。   |
| `{delete_statement}` |   `DELETE`ステートメント。   |

前述の例は、非トランザクション一括削除ステートメントの単純な使用例のみを示しています。詳細については、 [非トランザクション DML ステートメント](/non-transactional-dml.md)を参照してください。

### 非トランザクション一括削除の例 {#example-of-non-transactional-bulk-delete}

[一括削除の例](#bulk-delete-example)と同じシナリオで、次の SQL ステートメントは非トランザクション一括削除を実行する方法を示しています。

```sql
BATCH ON `rated_at` LIMIT 1000 DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```
