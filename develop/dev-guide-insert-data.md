---
title: Insert Data
summary: データの挿入方法について学習します。
aliases: ['/ja/tidb/stable/dev-guide-insert-data/','/ja/tidbcloud/dev-guide-insert-data/']
---

<!-- markdownlint-disable MD029 -->

# データの挿入 {#insert-data}

このドキュメントでは、さまざまなプログラミング言語で SQL 言語を使用して TiDB にデータを挿入する方法について説明します。

## 始める前に {#before-you-start}

このドキュメントを読む前に、次のものを準備する必要があります。

-   [TiDB Cloudスタータークラスタを作成する](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md) [テーブルを作成する](/develop/dev-guide-create-table.md) [セカンダリインデックスを作成する](/develop/dev-guide-create-secondary-indexes.md) [データベースを作成する](/develop/dev-guide-create-database.md)

## 行を挿入する {#insert-rows}

複数行のデータを挿入する方法は2つあります。例えば、 **3人**の選手のデータを挿入する必要がある場合などです。

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

一般的に、 `multi-line insertion statement` `single-line insertion statements`倍数よりも速く実行されます。

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

デフォルトの MySQL JDBCDriver設定により、一括挿入のパフォーマンスを向上させるにはいくつかのパラメータを変更する必要があります。

|            パラメータ           |                 手段                 |                                                                 推奨シナリオ                                                                |          推奨コンフィグレーション         |
| :------------------------: | :--------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------: | :---------------------------: |
|    `useServerPrepStmts`    |   サーバー側を使用して準備済みステートメントを有効にするかどうか  |                                                      プリペアドステートメントを複数回使用する必要がある場合                                                      |             `true`            |
|      `cachePrepStmts`      |   クライアントが準備されたステートメントをキャッシュするかどうか  |                                                       `useServerPrepStmts=true`                                                       |             `true`            |
|   `prepStmtCacheSqlLimit`  | プリペアドステートメントの最大サイズ（デフォルトでは 256 文字） |                                                        プリペアドステートメントが256文字を超える場合                                                       | プリペアドステートメントの実際のサイズに応じて構成されます |
|     `prepStmtCacheSize`    | プリペアドステートメントキャッシュの最大数 (デフォルトでは 25) |                                                           準備された文の数が25を超える場合                                                           |  準備されたステートメントの実際の数に応じて構成されます  |
| `rewriteBatchedStatements` |      **バッチ**ステートメントを書き換えるかどうか      |                                                              バッチ操作が必要な場合                                                              |             `true`            |
|     `allowMultiQueries`    |             バッチ操作を開始する             | [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)場合は`rewriteBatchedStatements = true`と`useServerPrepStmts = true`ときにこれを設定する必要があるため |             `true`            |

MySQL JDBCDriverは統合設定も提供しています： `useConfigs` 。3 `maxPerformance`設定すると、設定セットを設定するのと同等になります。5 `mysql:mysql-connector-java:8.0.28`例にとると、 `useConfigs=maxPerformance`には以下の内容が含まれます。

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

以下は、JDBC接続文字列の設定の典型的なシナリオです。この例では、ホスト: `127.0.0.1` 、ポート: `4000` 、ユーザー名: `root` 、パスワード: null、デフォルトデータベース: `test`です。

    jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true

Javaの完全な例については、以下を参照してください。

-   [JDBC で TiDB に接続する](/develop/dev-guide-sample-application-java-jdbc.md)
-   [Hibernate で TiDB に接続する](/develop/dev-guide-sample-application-java-hibernate.md)
-   [Spring BootでTiDBに接続する](/develop/dev-guide-sample-application-java-spring-boot.md)

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

大量のデータをTiDBクラスターに迅速にインポートする必要がある場合は、 **PingCAP**が提供するデータ移行ツールを使用することをお勧めします。3 `INSERT`の使用は効率的ではなく、例外やその他の問題を自分で処理する必要があるため、最適な方法ではありません。

一括挿入に推奨されるツールは次のとおりです。

<SimpleTab groupId="platform">
<div label="TiDB Cloud" value="tidb-cloud">

-   データのエクスポート：MySQLまたはTiDBのデータをローカルストレージまたはクラウドstorageにエクスポートするには、 [Dumpling](/dumpling-overview.md)使用します。TiDB TiDB Cloud StarterまたはEssentialクラスターの場合は、 [TiDB Cloudコンソール](https://tidbcloud.com/)の[輸出](/tidb-cloud/serverless-export.md)機能を使用して、より効率的にデータをエクスポートすることもできます。
-   データのインポート： [TiDB Cloudコンソール](https://tidbcloud.com/)の[輸入](/tidb-cloud/import-sample-data.md)機能を使用します。DumplingDumplingエクスポートしたデータ、ローカルの CSV ファイル、または[クラウドstorageからTiDB CloudにCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)インポートできます。
-   データレプリケーション： [TiDB Cloudコンソール](https://tidbcloud.com/)の[TiDBデータ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能を使用します。MySQL 互換データベースを TiDB に複製できます。また、ソースデータベースからシャードインスタンスとテーブルをマージおよび移行することもできます。
-   データのバックアップと復元： [TiDB Cloudコンソール](https://tidbcloud.com/)の[バックアップ](/tidb-cloud/backup-and-restore.md)機能を使用します。Dumplingと比較して、バックアップと復元はビッグデータのシナリオに適しています。

</div>
<div label="TiDB Self-Managed" value="tidb">

-   データのエクスポート: [Dumpling](/dumpling-overview.md) MySQL または TiDB データをローカルまたは Amazon S3 にエクスポートできます。
-   データのインポート： [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) . **Dumpling**でエクスポートしたデータ、 **CSV**ファイル、または[Amazon Auroraから TiDB へのデータ移行](/migrate-aurora-to-tidb.md)をインポートできます。また、ローカルディスクまたはAmazon S3クラウドディスクからのデータの読み取りもサポートしています。
-   データレプリケーション： [TiDBデータ移行](/dm/dm-overview.md) . MySQL、MariaDB、Amazon AuroraデータベースをTiDBに複製できます。また、ソースデータベースからシャード化されたインスタンスとテーブルのマージと移行もサポートしています。
-   データのバックアップと復元: [バックアップと復元 (BR)](/br/backup-and-restore-overview.md) **Dumpling**と比較して、 **BR は*****ビッグデータの***シナリオに適しています。

</div>
</SimpleTab>

## ホットスポットを避ける {#avoid-hotspots}

テーブルを設計する際には、挿入操作が多数発生するかどうかを考慮する必要があります。もしそうであれば、テーブル設計中にホットスポットを回避する必要があります。1 [主キーを選択](/develop/dev-guide-create-table.md#select-primary-key)セクションを参照し、 [主キーを選択する際のルール](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)セクションに従ってください。

TiDB Self-Managed でホットスポットの問題を処理する方法の詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。

## <code>AUTO_RANDOM</code>主キーを持つテーブルにデータを挿入する {#insert-data-to-a-table-with-the-code-auto-random-code-primary-key}

挿入するテーブルの主キーに属性`AUTO_RANDOM`がある場合、デフォルトでは主キーを指定できません。例えば、データベース[`bookshop`](/develop/dev-guide-bookshop-schema-design.md)では、 [`users`テーブル](/develop/dev-guide-bookshop-schema-design.md#users-table)のフィールド`id`に属性`AUTO_RANDOM`が含まれていることがわかります。

この場合、次のような SQL を使用して挿入すること**はできません**。

```sql
INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
```

エラーが発生します:

    ERROR 8216 (HY000): Invalid auto random: Explicit insertion on auto_random column is disabled. Try to set @@allow_auto_random_explicit_insert = true.

挿入時に`AUTO_RANDOM`列を手動で指定することはお勧めしません。

このエラーを処理するには 2 つの解決策があります。

-   （推奨）挿入文からこの列を削除し、TiDBによって初期化された値`AUTO_RANDOM`を使用してください。これは`AUTO_RANDOM`のセマンティクスに適合します。

    ```sql
    INSERT INTO `bookshop`.`users` (`balance`, `nickname`) VALUES (0.00, 'nicky');
    ```

-   この列を指定する***必要がある***ことが確実な場合は、ユーザー変数を変更することで、挿入時に[`SET`ステートメント](https://docs.pingcap.com/tidb/stable/sql-statement-set-variable)列を使用して`AUTO_RANDOM`列を指定できるようにすることができます。

    ```sql
    SET @@allow_auto_random_explicit_insert = true;
    INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
    ```

## HTAPを使用する {#use-htap}

TiDBでは、HTAP機能により、データ挿入時に追加の操作を実行する必要がなくなります。追加の挿入ロジックは不要です。TiDBはデータの一貫性を自動的に保証します。テーブル作成後に[列指向レプリカ同期をオンにする](/develop/dev-guide-create-table.md#use-htap-capabilities)実行するだけで、列指向レプリカを使用してクエリを直接高速化できます。

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
