---
title: Insert Data
summary: データを挿入する方法について学習します。
---

<!-- markdownlint-disable MD029 -->

# データの挿入 {#insert-data}

このドキュメントでは、さまざまなプログラミング言語で SQL 言語を使用して TiDB にデータを挿入する方法について説明します。

## 始める前に {#before-you-start}

このドキュメントを読む前に、次のものを準備する必要があります。

-   [TiDB Cloudサーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md) [データベースを作成する](/develop/dev-guide-create-database.md) [セカンダリインデックスを作成する](/develop/dev-guide-create-secondary-indexes.md) [テーブルを作成する](/develop/dev-guide-create-table.md)ください

## 行を挿入 {#insert-rows}

複数行のデータを挿入する方法は 2 つあります。たとえば、 **3 人**のプレーヤーのデータを挿入する必要がある場合などです。

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

一般的に、 `multi-line insertion statement`は`single-line insertion statements`倍数よりも速く実行されます。

<SimpleTab>
<div label="SQL">

```sql
CREATE TABLE `player` (`id` INT, `coins` INT, `goods` INT);
INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2);
```

この SQL の使用方法の詳細については、 [TiDBクラスタへの接続](/develop/dev-guide-build-cluster-in-cloud.md#step-2-connect-to-a-cluster)参照し、クライアントを使用して TiDB クラスターに接続した後、SQL ステートメントを入力する手順に従ってください。

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

デフォルトの MySQL JDBCDriver設定により、一括挿入のパフォーマンスを向上させるには、いくつかのパラメータを変更する必要があります。

|            パラメータ           |                 手段                 |                                                                 推奨シナリオ                                                                |          推奨コンフィグレーション         |
| :------------------------: | :--------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------: | :---------------------------: |
|    `useServerPrepStmts`    |   サーバー側を使用して準備済みステートメントを有効にするかどうか  |                                                      プリペアドステートメントを複数回使用する必要がある場合                                                      |             `true`            |
|      `cachePrepStmts`      |   クライアントが準備されたステートメントをキャッシュするかどうか  |                                                       `useServerPrepStmts=true`                                                       |             `true`            |
|   `prepStmtCacheSqlLimit`  | プリペアドステートメントの最大サイズ（デフォルトでは 256 文字） |                                                        プリペアドステートメントが256文字を超える場合                                                       | プリペアドステートメントの実際のサイズに応じて構成されます |
|     `prepStmtCacheSize`    | プリペアドステートメントキャッシュの最大数 (デフォルトでは 25) |                                                        準備されたステートメントの数が25を超える場合                                                        |  準備されたステートメントの実際の数に応じて構成されます  |
| `rewriteBatchedStatements` |      **バッチ**ステートメントを書き換えるかどうか      |                                                              バッチ操作が必要な場合                                                              |             `true`            |
|     `allowMultiQueries`    |             バッチ操作を開始する             | [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)場合は`rewriteBatchedStatements = true`と`useServerPrepStmts = true`ときにこれを設定する必要があるため |             `true`            |

MySQL JDBCDriverは統合構成も提供します: `useConfigs` 。 `maxPerformance`で構成されると、構成セットを構成するのと同等になります。 `mysql:mysql-connector-java:8.0.28`例にとると、 `useConfigs=maxPerformance`には次のものが含まれます:

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

`mysql-connector-java-{version}.jar!/com/mysql/cj/configurations/maxPerformance.properties`チェックすると、対応するバージョンの MySQL JDBCDriverの`useConfigs=maxPerformance`に含まれる構成を取得できます。

以下は、JDBC 接続文字列構成の一般的なシナリオです。この例では、ホスト: `127.0.0.1` 、ポート: `4000` 、ユーザー名: `root` 、パスワード: null、デフォルト データベース: `test`です。

    jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true

Javaの完全な例については、以下を参照してください。

-   [JDBC で TiDB に接続する](/develop/dev-guide-sample-application-java-jdbc.md)
-   [Hibernate で TiDB に接続する](/develop/dev-guide-sample-application-java-hibernate.md)
-   [Spring Boot で TiDB に接続する](/develop/dev-guide-sample-application-java-spring-boot.md)

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

-   [Go-MySQL-Driver で TiDB に接続する](/develop/dev-guide-sample-application-golang-sql-driver.md)
-   [GORMでTiDBに接続する](/develop/dev-guide-sample-application-golang-gorm.md)

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

-   [PyMySQLでTiDBに接続する](/develop/dev-guide-sample-application-python-pymysql.md)
-   [mysqlclientでTiDBに接続する](https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart)
-   [MySQL Connector/Python で TiDB に接続する](/develop/dev-guide-sample-application-python-mysql-connector.md)
-   [SQLAlchemy で TiDB に接続する](/develop/dev-guide-sample-application-python-sqlalchemy.md)
-   [peeweeでTiDBに接続する](/develop/dev-guide-sample-application-python-peewee.md)

</div>

</SimpleTab>

## 一括挿入 {#bulk-insert}

大量のデータを TiDB クラスターにすばやくインポートする必要がある場合は、 **PingCAP**が提供するデータ移行用のさまざまなツールを使用することをお勧めします`INSERT`ステートメントを使用することは、効率的ではなく、例外やその他の問題を自分で処理する必要があるため、最適な方法ではありません。

一括挿入に推奨されるツールは次のとおりです。

-   データのエクスポート: [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) MySQL または TiDB データをローカルまたは Amazon S3 にエクスポートできます。

<CustomContent platform="tidb">

-   データのインポート: [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) **Dumpling**でエクスポートしたデータ、 **CSV**ファイル、または[Amazon Auroraから TiDB へのデータ移行](/migrate-aurora-to-tidb.md)をインポートできます。ローカル ディスクまたは Amazon S3 クラウド ディスクからのデータの読み取りもサポートされています。
-   データレプリケーション: [TiDB データ移行](/dm/dm-overview.md) MySQL、MariaDB、Amazon Auroraデータベースを TiDB にレプリケートできます。また、ソースデータベースからシャードされたインスタンスとテーブルをマージおよび移行することもサポートしています。
-   データのバックアップと復元: [バックアップと復元 (BR)](/br/backup-and-restore-overview.md) **Dumpling**と比較して、 **BR は*****ビッグデータの***シナリオに適しています。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   データのインポート: [TiDB Cloudコンソール](https://tidbcloud.com/)ページの[インポートの作成](/tidb-cloud/import-sample-data.md)ページ。Dumpling**で**エクスポートしたデータをインポートしたり、ローカルの**CSV**ファイルをインポートしたり、 [Amazon S3 または GCS から CSV ファイルをTiDB Cloudにインポートする](/tidb-cloud/import-csv-files.md)のインポートを行うことができます。また、ローカル ディスク、Amazon S3 クラウド ディスク、または GCS クラウド ディスクからのデータの読み取りもサポートしています。
-   データレプリケーション: [TiDB データ移行](https://docs.pingcap.com/tidb/stable/dm-overview) MySQL、MariaDB、Amazon Auroraデータベースを TiDB にレプリケートできます。また、ソースデータベースからシャードされたインスタンスとテーブルをマージおよび移行することもサポートしています。
-   データのバックアップと復元: TiDB Cloudコンソールの[バックアップ](/tidb-cloud/backup-and-restore.md)ページ。Dumpling と比較する**と**、バックアップと復元は***ビッグ データの***シナリオに適しています。

</CustomContent>

## ホットスポットを避ける {#avoid-hotspots}

テーブルを設計する際には、挿入操作が多数あるかどうかを考慮する必要があります。 多数ある場合は、テーブル設計中にホットスポットを回避する必要があります。 [主キーを選択](/develop/dev-guide-create-table.md#select-primary-key)セクションを参照し、 [主キーを選択する際のルール](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)に従ってください。

<CustomContent platform="tidb">

ホットスポットの問題の処理方法の詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。

</CustomContent>

## <code>AUTO_RANDOM</code>主キーを持つテーブルにデータを挿入する {#insert-data-to-a-table-with-the-code-auto-random-code-primary-key}

挿入するテーブルの主キーに`AUTO_RANDOM`属性がある場合、デフォルトでは主キーを指定できません。たとえば、 [`bookshop`](/develop/dev-guide-bookshop-schema-design.md)データベースでは、 [`users`テーブル](/develop/dev-guide-bookshop-schema-design.md#users-table)の`id`フィールドに`AUTO_RANDOM`属性が含まれていることがわかります。

この場合、次のような SQL を使用して挿入すること**はできません**。

```sql
INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
```

エラーが発生します:

    ERROR 8216 (HY000): Invalid auto random: Explicit insertion on auto_random column is disabled. Try to set @@allow_auto_random_explicit_insert = true.

挿入時に`AUTO_RANDOM`列を手動で指定することはお勧めしません。

このエラーを処理するには 2 つの解決策があります。

-   (推奨) この列を INSERT ステートメントから削除し、TiDB によって初期化された`AUTO_RANDOM`値を使用します。これは`AUTO_RANDOM`のセマンティクスに適合します。

    ```sql
    INSERT INTO `bookshop`.`users` (`balance`, `nickname`) VALUES (0.00, 'nicky');
    ```

-   この列を指定する***必要がある***ことが確実な場合は、ユーザー変数を変更することで、挿入時に[`SET`ステートメント](https://docs.pingcap.com/tidb/stable/sql-statement-set-variable)列を使用して`AUTO_RANDOM`列を指定できるようにすることができます。

    ```sql
    SET @@allow_auto_random_explicit_insert = true;
    INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
    ```

## HTAPを使用する {#use-htap}

TiDB では、HTAP 機能により、データを挿入するときに追加の操作を実行する必要がなくなります。追加の挿入ロジックはありません。TiDB はデータの一貫性を自動的に保証します。テーブルを作成した後[列指向レプリカ同期をオンにする](/develop/dev-guide-create-table.md#use-htap-capabilities)列指向のレプリカを使用してクエリを直接高速化するだけで済みます。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
