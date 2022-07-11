---
title: Delete Data
summary: Learn about the SQL syntax, best practices, and examples for deleting data.
---

# データの削除 {#delete-data}

このドキュメントでは、 [消去](/sql-statements/sql-statement-delete.md)ステートメントを使用してTiDBのデータを削除する方法について説明します。

## 始める前に {#before-you-start}

このドキュメントを読む前に、以下を準備する必要があります。

-   [TiDB CloudでTiDBクラスターを構築する（DevTier）](/develop/dev-guide-build-cluster-in-cloud.md)
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md) 、および[データベースを作成する](/develop/dev-guide-create-database.md) [セカンダリインデックスを作成する](/develop/dev-guide-create-secondary-indexes.md) [テーブルを作成する](/develop/dev-guide-create-table.md)
-   [データを挿入](/develop/dev-guide-insert-data.md)

## SQL構文 {#sql-syntax}

`DELETE`ステートメントは、通常、次の形式です。

{{< copyable "" >}}

```sql
DELETE FROM {table} WHERE {filter}
```

|   パラメータ名   |      説明      |
| :--------: | :----------: |
|  `{table}` |     テーブル名    |
| `{filter}` | フィルタのマッチング条件 |

この例は、 `DELETE`の単純なユースケースのみを示しています。詳細については、 [DELETE構文](/sql-statements/sql-statement-delete.md)を参照してください。

## ベストプラクティス {#best-practices}

データを削除するときに従うべきいくつかのベストプラクティスは次のとおりです。

-   `DELETE`ステートメントでは常に`WHERE`句を指定してください。 `WHERE`句が指定されていない場合、TiDBはテーブル内の***すべて***の行を削除します。
-   TiDBは単一のトランザクションのサイズ（デフォルトでは[txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit) MB）を制限しているため、多数の行（たとえば、1万を超える行）を削除する場合は[一括削除](#bulk-delete)を使用します。
-   テーブル内のすべてのデータを削除する場合は、 `DELETE`ステートメントを使用しないでください。代わりに、 [`TRUNCATE`](/sql-statements/sql-statement-truncate.md)ステートメントを使用してください。
-   パフォーマンスの考慮事項については、 [パフォーマンスに関する考慮事項](#performance-considerations)を参照してください。

## 例 {#example}

特定の期間内にアプリケーションエラーが見つかり、この期間内の[評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)のすべてのデータ（たとえば、 `2022-04-15 00:00:00`から`2022-04-15 00:15:00` ）を削除する必要があるとします。この場合、 `SELECT`ステートメントを使用して、削除するレコードの数を確認できます。

{{< copyable "" >}}

```sql
SELECT COUNT(*) FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```

10,000を超えるレコードが返された場合は、 [一括削除](#bulk-delete)を使用してそれらを削除します。

10,000未満のレコードが返される場合は、次の例を使用してそれらを削除します。

<SimpleTab>
<div label="SQL" href="delete-sql">

{{< copyable "" >}}

```sql
DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java" href="delete-java">

{{< copyable "" >}}

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource

try (Connection connection = ds.getConnection()) {
    String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND  `rated_at` <= ?";
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
</SimpleTab>

> **ノート：**
>
> `rated_at`フィールドは[日付と時刻のタイプ](/data-type-date-and-time.md)の`DATETIME`タイプであることに注意してください。タイムゾーンに関係なく、文字通りの量としてTiDBに保存されていると見なすことができます。一方、 `TIMESTAMP`タイプはタイムスタンプを格納するため、別の[タイムゾーン](/configure-time-zone.md)に別の時間文字列を表示します。
>
> また、MySQLと同様に、 `TIMESTAMP`データ型は[2038年問題](https://en.wikipedia.org/wiki/Year_2038_problem)の影響を受けます。 2038より大きい値を格納する場合は、 `DATETIME`タイプを使用することをお勧めします。

## パフォーマンスに関する考慮事項 {#performance-considerations}

### TiDBGCメカニズム {#tidb-gc-mechanism}

TiDBは、 `DELETE`ステートメントを実行した直後にデータを削除しません。代わりに、データを削除の準備ができているとマークします。次に、TiDB GC（ガベージコレクション）が古いデータをクリーンアップするのを待ちます。したがって、 `DELETE`ステートメントはディスク使用量をすぐには削減し***ません***。

GCは、デフォルトで10分ごとに1回トリガーされます。各GCは、 **safe_point**と呼ばれる時点を計算します。この時点より前のデータは再度使用されないため、TiDBは安全にデータをクリーンアップできます。

詳細については、 [GCメカニズム](/garbage-collection-overview.md)を参照してください。

### 統計情報を更新する {#update-statistical-information}

TiDBは[統計情報](/statistics.md)を使用してインデックスの選択を決定します。大量のデータを削除した後、インデックスが正しく選択されない可能性が高くなります。 [手動収集](/statistics.md#manual-collection)を使用して統計を更新できます。これは、SQLパフォーマンス最適化のためのより正確な統計情報をTiDBオプティマイザーに提供します。

## 一括削除 {#bulk-delete}

テーブルから複数行のデータを削除する必要がある場合は、 [`DELETE`例](#example)を選択し、 `WHERE`句を使用して、削除する必要のあるデータをフィルタリングできます。

ただし、多数の行（1万を超える）を削除する必要がある場合は、データを反復的に削除することをお勧めします。つまり、削除が完了するまで、各反復でデータの一部を削除します。これは、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)が単一のトランザクションのサイズを制限しているためです（デフォルトでは1、100 MB）。プログラムまたはスクリプトでループを使用して、このような操作を実行できます。

このセクションでは、一括削除を完了するために`SELECT`と`DELETE`の組み合わせを実行する方法を示す、反復削除操作を処理するスクリプトを作成する例を示します。

### 一括削除ループを作成する {#write-a-bulk-delete-loop}

まず、アプリケーションまたはスクリプトのループに`SELECT`のクエリを記述します。このクエリの戻り値を、削除する必要のある行の主キーとして使用します。この`SELECT`クエリを定義するときは、 `WHERE`句を使用して、削除する必要のある行をフィルタリングする必要があることに注意してください。

### 一括削除の例 {#bulk-delete-example}

特定の期間内にアプリケーションエラーを見つけたとします。この期間内の[評価](/develop/dev-guide-bookshop-schema-design.md#ratings-table)のすべてのデータ（たとえば、 `2022-04-15 00:00:00`から`2022-04-15 00:15:00` ）を削除する必要があり、10,000を超えるレコードが15分で書き込まれます。次のように実行できます。

{{< copyable "" >}}

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
            String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND  `rated_at` <= ? LIMIT 1000";
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

各反復で、 `SELECT`は`2022-04-15 00:00:00`から`2022-04-15 00:15:00`までの期間のデータに対して最大1000行の主キー値を選択します。次に、一括削除を実行します。各ループの最後に`TimeUnit.SECONDS.sleep(1);`があると、一括削除操作が1秒間一時停止し、一括削除操作が多くのハードウェアリソースを消費するのを防ぐことに注意してください。
