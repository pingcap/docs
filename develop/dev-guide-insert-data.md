---
title: Insert Data
summary: Learn about how to insert data.
---

<!-- markdownlint-disable MD029 -->

# データの挿入 {#insert-data}

このドキュメントでは、SQL 言語とさまざまなプログラミング言語を使用して TiDB にデータを挿入する方法について説明します。

## 始める前に {#before-you-start}

このドキュメントを読む前に、以下を準備する必要があります。

-   [TiDB サーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md) 、 [データベースを作成する](/develop/dev-guide-create-database.md) 、 [テーブルを作成する](/develop/dev-guide-create-table.md) 、および[セカンダリインデックスの作成](/develop/dev-guide-create-secondary-indexes.md)を読み取ります

## 行の挿入 {#insert-rows}

複数行のデータを挿入するには 2 つの方法があります。たとえば、 **3**人のプレイヤーのデータを挿入する必要がある場合です。

-   **複数行の挿入ステートメント**:

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2), (3, 300, 5);
    ```

-   複数の**単一行挿入ステートメント**:

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (2, 230, 2);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (3, 300, 5);
    ```

一般に、 `multi-line insertion statement`​​倍数の`single-line insertion statements`よりも高速に実行されます。

<SimpleTab>
<div label="SQL">

```sql
CREATE TABLE `player` (`id` INT, `coins` INT, `goods` INT);
INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2);
```

この SQL の使用方法の詳細については、 [TiDBクラスタへの接続](/develop/dev-guide-build-cluster-in-cloud.md#step-2-connect-to-a-cluster)を参照し、クライアントを使用して TiDB クラスターに接続した後、手順に従って SQL ステートメントを入力します。

</div>

<div label="Java">

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource
try (Connection connection = ds.getConnection()) {
    connection.setAutoCommit(false);

    PreparedStatement pstmt = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)"))

    // first player
    pstmt.setInt(1, 1);
    pstmt.setInt(2, 1000);
    pstmt.setInt(3, 1);
    pstmt.addBatch();

    // second player
    pstmt.setInt(1, 2);
    pstmt.setInt(2, 230);
    pstmt.setInt(3, 2);
    pstmt.addBatch();

    pstmt.executeBatch();
    connection.commit();
} catch (SQLException e) {
    e.printStackTrace();
}
```

デフォルトの MySQL JDBCDriver設定により、一括挿入のパフォーマンスを向上させるには、いくつかのパラメーターを変更する必要があります。

|            パラメータ           |                  手段                 |                                                                推奨シナリオ                                                                |        推奨されるコンフィグレーション        |
| :------------------------: | :---------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------: | :---------------------------: |
|    `useServerPrepStmts`    |   サーバー側を使用してプリペアドステートメントを有効にするかどうか  |                                                      プリペアドステートメントを複数回使用する必要がある場合                                                     |             `true`            |
|      `cachePrepStmts`      |   クライアントが準備されたステートメントをキャッシュするかどうか   |                                                      `useServerPrepStmts=true`時                                                      |             `true`            |
|   `prepStmtCacheSqlLimit`  | プリペアドステートメントの最大サイズ (デフォルトでは 256 文字) |                                                      プリペアドステートメントが 256 文字を超える場合                                                      | プリペアドステートメントの実際のサイズに応じて構成されます |
|     `prepStmtCacheSize`    |  プリペアドステートメントキャッシュの最大数 (デフォルトでは 25) |                                                       準備されたステートメントの数が 25 を超える場合                                                      |   実際の準備済みステートメントの数に応じて構成されます  |
| `rewriteBatchedStatements` |     **Batched**ステートメントを書き換えるかどうか    |                                                              バッチ操作が必要な場合                                                             |             `true`            |
|     `allowMultiQueries`    |              バッチ操作を開始する             | [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)は`rewriteBatchedStatements = true`と`useServerPrepStmts = true`のときにこれを設定する必要があるため |             `true`            |

MySQL JDBC Driver は、 `useConfigs`統合構成も提供します。 `maxPerformance`で構成すると、一連の構成を構成することと同じになります。 `mysql:mysql-connector-java:8.0.28`例にとると、 `useConfigs=maxPerformance`には次のものが含まれます。

```properties
cachePrepStmts=true
cacheCallableStmts=true
cacheServerConfiguration=true
useLocalSessionState=true
elideSetAutoCommits=true
alwaysSendSetIsolation=false
enableQueryTimeouts=false
connectionAttributes=none
useInformationSchema=true
```

`mysql-connector-java-{version}.jar!/com/mysql/cj/configurations/maxPerformance.properties`をチェックすると、MySQL JDBC Driverの対応するバージョンの`useConfigs=maxPerformance`に含まれる構成を取得できます。

以下は、JDBC 接続文字列構成の一般的なシナリオです。この例では、ホスト: `127.0.0.1` 、ポート: `4000` 、ユーザー名: `root` 、パスワード: null、デフォルトのデータベース: `test` :

    jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true

Javaの完全な例については、以下を参照してください。

-   [JDBC を使用して TiDB に接続する](/develop/dev-guide-sample-application-java-jdbc.md)
-   [Hibernate で TiDB に接続する](/develop/dev-guide-sample-application-java-hibernate.md)
-   [Spring Boot を使用して TiDB に接続する](/develop/dev-guide-sample-application-java-spring-boot.md)

</div>

<div label="Golang">

```go
package main

import (
    "database/sql"
    "strings"

    _ "github.com/go-sql-driver/mysql"
)

type Player struct {
    ID    string
    Coins int
    Goods int
}

func bulkInsertPlayers(db *sql.DB, players []Player, batchSize int) error {
    tx, err := db.Begin()
    if err != nil {
        return err
    }

    stmt, err := tx.Prepare(buildBulkInsertSQL(batchSize))
    if err != nil {
        return err
    }

    defer stmt.Close()

    for len(players) > batchSize {
        if _, err := stmt.Exec(playerToArgs(players[:batchSize])...); err != nil {
            tx.Rollback()
            return err
        }

        players = players[batchSize:]
    }

    if len(players) != 0 {
        if _, err := tx.Exec(buildBulkInsertSQL(len(players)), playerToArgs(players)...); err != nil {
            tx.Rollback()
            return err
        }
    }

    if err := tx.Commit(); err != nil {
        tx.Rollback()
        return err
    }

    return nil
}

func playerToArgs(players []Player) []interface{} {
    var args []interface{}
    for _, player := range players {
        args = append(args, player.ID, player.Coins, player.Goods)
    }
    return args
}

func buildBulkInsertSQL(amount int) string {
    return "INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)" + strings.Repeat(",(?,?,?)", amount-1)
}
```

Golangの完全な例については、以下を参照してください。

-   [Go-MySQL-Driver を使用して TiDB に接続する](/develop/dev-guide-sample-application-golang-sql-driver.md)
-   [GORM を使用して TiDB に接続する](/develop/dev-guide-sample-application-golang-gorm.md)

</div>

<div label="Python">

```python
import MySQLdb
connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)

with get_connection(autocommit=True) as connection:
    with connection.cursor() as cur:
        player_list = random_player(1919)
        for idx in range(0, len(player_list), 114):
            cur.executemany("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player_list[idx:idx + 114])
```

Python の完全な例については、以下を参照してください。

-   [PyMySQL を使用して TiDB に接続する](/develop/dev-guide-sample-application-python-pymysql.md)
-   [mysqlclient を使用して TiDB に接続する](https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart)
-   [MySQL コネクタ/Python を使用して TiDB に接続する](/develop/dev-guide-sample-application-python-mysql-connector.md)
-   [SQLAlchemy を使用して TiDB に接続する](/develop/dev-guide-sample-application-python-sqlalchemy.md)
-   [peewee で TiDB に接続する](/develop/dev-guide-sample-application-python-peewee.md)

</div>

</SimpleTab>

## 一括挿入 {#bulk-insert}

大量のデータを TiDB クラスターに迅速にインポートする必要がある場合は、データ移行用に**PingCAP**が提供するさまざまなツールを使用することをお勧めします。 `INSERT`ステートメントの使用は、効率的ではなく、例外やその他の問題を自分で処理する必要があるため、最良の方法ではありません。

一括挿入に推奨されるツールは次のとおりです。

-   データのエクスポート: [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) . MySQL または TiDB データをローカルまたは Amazon S3 にエクスポートできます。

<CustomContent platform="tidb">

-   データインポート: [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) . **Dumpling の**エクスポート データ、 **CSV**ファイル、または[Amazon Auroraから TiDB へのデータの移行](/migrate-aurora-to-tidb.md)をインポートできます。ローカル ディスクまたは Amazon S3 クラウド ディスクからのデータの読み取りもサポートします。
-   データ複製: [TiDB データ移行](/dm/dm-overview.md) 。 MySQL、MariaDB、Amazon Auroraデータベースを TiDB にレプリケートできます。また、ソース データベースからのシャード化されたインスタンスとテーブルのマージと移行もサポートします。
-   データのバックアップと復元: [バックアップと復元 (BR)](/br/backup-and-restore-overview.md) . **Dumpling**と比較して、 **BR は*****ビッグデータの***シナリオにより適しています。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   データインポート: [TiDB Cloudコンソール](https://tidbcloud.com/)の[インポートの作成](/tidb-cloud/import-sample-data.md)ページ。 **Dumpling の**エクスポート データをインポートしたり、ローカルの**CSV**ファイルをインポートしたり、 [Amazon S3 または GCS からTiDB Cloudに CSV ファイルをインポート](/tidb-cloud/import-csv-files.md)実行したりできます。ローカル ディスク、Amazon S3 クラウド ディスク、または GCS クラウド ディスクからのデータの読み取りもサポートします。
-   データ複製: [TiDB データ移行](https://docs.pingcap.com/tidb/stable/dm-overview) 。 MySQL、MariaDB、Amazon Auroraデータベースを TiDB にレプリケートできます。また、ソース データベースからのシャード化されたインスタンスとテーブルのマージと移行もサポートします。
-   データのバックアップと復元: TiDB Cloudコンソールの[バックアップ](/tidb-cloud/backup-and-restore.md)ページ。 **Dumpling**と比較して、バックアップと復元は***ビッグ データの***シナリオにより適しています。

</CustomContent>

## ホットスポットを避ける {#avoid-hotspots}

テーブルを設計するときは、多数の挿入操作があるかどうかを考慮する必要があります。その場合、テーブルの設計中にホットスポットを回避する必要があります。 [主キーを選択](/develop/dev-guide-create-table.md#select-primary-key)セクションを参照し、 [主キーを選択する際のルール](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)に従ってください。

<CustomContent platform="tidb">

ホットスポットの問題の処理方法の詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

</CustomContent>

## <code>AUTO_RANDOM</code>主キーを使用してテーブルにデータを挿入する {#insert-data-to-a-table-with-the-code-auto-random-code-primary-key}

挿入するテーブルの主キーに`AUTO_RANDOM`属性がある場合、デフォルトでは主キーを指定できません。たとえば、データベース[`bookshop`](/develop/dev-guide-bookshop-schema-design.md)では、 [`users`テーブル](/develop/dev-guide-bookshop-schema-design.md#users-table)の`id`フィールドに`AUTO_RANDOM`属性が含まれていることがわかります。

この場合、次のような SQL を使用して挿入する**ことはできません**。

```sql
INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
```

エラーが発生します:

    ERROR 8216 (HY000): Invalid auto random: Explicit insertion on auto_random column is disabled. Try to set @@allow_auto_random_explicit_insert = true.

挿入時に`AUTO_RANDOM`列を手動で指定することはお勧めできません。

このエラーを処理するには 2 つの解決策があります。

-   (推奨) この列を挿入ステートメントから削除し、TiDB が初期化した値`AUTO_RANDOM`を使用します。これは`AUTO_RANDOM`のセマンティクスに適合します。

    ```sql
    INSERT INTO `bookshop`.`users` (`balance`, `nickname`) VALUES (0.00, 'nicky');
    ```

-   この列を指定する***必要がある***ことが確実な場合は、ユーザー変数を変更することで、 [`SET`ステートメント](https://docs.pingcap.com/zh/tidb/stable/sql-statement-set-variable)使用して挿入時に`AUTO_RANDOM`の列を指定できるようにすることができます。

    ```sql
    SET @@allow_auto_random_explicit_insert = true;
    INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
    ```

## HTAP を使用する {#use-htap}

TiDB では、HTAP 機能により、データの挿入時に追加の操作を実行する必要がなくなります。追加の挿入ロジックはありません。 TiDB はデータの一貫性を自動的に保証します。テーブルを作成した後、列指向レプリカ[列指向のレプリカ同期を有効にする](/develop/dev-guide-create-table.md#use-htap-capabilities)使用してクエリを直接高速化するだけです。
