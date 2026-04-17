---
title: Insert Data
summary: データ挿入の方法について学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-insert-data/','/ja/tidb/dev/dev-guide-insert-data/','/ja/tidbcloud/dev-guide-insert-data/']
---

<!-- markdownlint-disable MD029 -->

# データを挿入する {#insert-data}

このドキュメントでは、さまざまなプログラミング言語でSQL言語を使用してTiDBにデータを挿入する方法について説明します。

## 始める前に {#before-you-start}

この文書を読む前に、以下のものを準備してください。

-   [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)、データベース[データベースを作成する](/develop/dev-guide-create-database.md)、[テーブルを作成する](/develop/dev-guide-create-table.md)、 [セカンダリインデックスを作成する](/develop/dev-guide-create-secondary-indexes.md)を読む

## 行を挿入する {#insert-rows}

複数の行のデータを挿入する方法は2つあります。たとえば、 **3人**の選手のデータを挿入する必要がある場合などです。

-   **複数行挿入ステートメント**：

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2), (3, 300, 5);
    ```

-   複数の**単一行挿入ステートメント**：

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (2, 230, 2);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (3, 300, 5);
    ```

一般的に`multi-line insertion statement`は、複数の`single-line insertion statements`よりも高速に動作します。

<SimpleTab>
<div label="SQL">

```sql
CREATE TABLE `player` (`id` INT, `coins` INT, `goods` INT);
INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2);
```

この SQL の使用方法の詳細については、 [TiDB Cloud Starterインスタンスに接続します](/develop/dev-guide-build-cluster-in-cloud.md#step-2-connect-to-a-starter-instance)を参照し、クライアントを使用してTiDB Cloud Starterインスタンスに接続した後、SQL ステートメントを入力する手順に従ってください。

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

MySQL JDBCDriverのデフォルト設定では、一括挿入のパフォーマンスを向上させるために、いくつかのパラメータを変更する必要があります。

|            パラメータ           |                手段                |                                                                    推奨シナリオ                                                                   |          推奨コンフィグレーション         |
| :------------------------: | :------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------: |
|    `useServerPrepStmts`    | サーバー側を使用してプリペアドステートメントを有効にするかどうか |                                                         プリペアドステートメントを複数回使用する必要がある場合                                                         |             `true`            |
|      `cachePrepStmts`      |  クライアントが準備済みステートメントをキャッシュするかどうか  |                                                          `useServerPrepStmts=true`                                                          |             `true`            |
|   `prepStmtCacheSqlLimit`  |  プリペアドステートメントの最大サイズ（デフォルトは256文字） |                                                           プリペアドステートメントが256文字を超える場合                                                          | プリペアドステートメントの実際のサイズに応じて構成されます |
|     `prepStmtCacheSize`    |  プリペアドステートメントキャッシュの最大数（デフォルトは25） |                                                           準備されたステートメントの数が25を超える場合                                                           |   準備済みステートメントの実際の数に応じて構成されます  |
| `rewriteBatchedStatements` |     **バッチ**ステートメントを書き換えるかどうか     |                                                                 バッチ処理が必要な場合                                                                 |             `true`            |
|     `allowMultiQueries`    |            バッチ操作を開始します           | [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)により`rewriteBatchedStatements = true`および`useServerPrepStmts = true`の場合にこれを設定する必要があるためです。 |             `true`            |

MySQL JDBCDriverは、 `useConfigs`という統合構成も提供しています。 `maxPerformance`で構成すると、一連の構成を構成するのと同等になります。 `mysql:mysql-connector-java:8.0.28`を例にとると、 `useConfigs=maxPerformance`には以下が含まれます。

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

`mysql-connector-java-{version}.jar!/com/mysql/cj/configurations/maxPerformance.properties`を確認すると、対応するバージョンの MySQL JDBCDriverの`useConfigs=maxPerformance`に含まれる設定を取得できます。

以下は、JDBC接続文字列構成の典型的なシナリオです。この例では、ホスト: `127.0.0.1` 、ポート: `4000` 、ユーザー名: `root` 、パスワード: null、デフォルトデータベース: `test` :

    jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true

Javaでの完全な例については、以下を参照してください。

-   [JDBCを使用してTiDBに接続する](/develop/dev-guide-sample-application-java-jdbc.md)
-   [Hibernateを使用してTiDBに接続する](/develop/dev-guide-sample-application-java-hibernate.md)
-   [Spring Bootを使用してTiDBに接続する](/develop/dev-guide-sample-application-java-spring-boot.md)

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

Golangでの完全な例については、以下を参照してください。

-   [Go-MySQL-Driverを使用してTiDBに接続する](/develop/dev-guide-sample-application-golang-sql-driver.md)
-   [GORMを使用してTiDBに接続する](/develop/dev-guide-sample-application-golang-gorm.md)

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

Pythonでの完全な例については、以下を参照してください。

-   [PyMySQLを使用してTiDBに接続する](/develop/dev-guide-sample-application-python-pymysql.md)
-   [mysqlclientを使用してTiDBに接続します。](https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart)
-   [MySQL Connector/Pythonを使用してTiDBに接続する](/develop/dev-guide-sample-application-python-mysql-connector.md)
-   [SQLAlchemyを使用してTiDBに接続する](/develop/dev-guide-sample-application-python-sqlalchemy.md)
-   [peeweeを使用してTiDBに接続します。](/develop/dev-guide-sample-application-python-peewee.md)

</div>

</SimpleTab>

## バルク挿入 {#bulk-insert}

TiDBに大量のデータを迅速にインポートする必要がある場合は、 **PingCAP**が提供するデータ移行ツール群を使用することをお勧めします。 `INSERT`ステートメントを使用する方法は、効率が悪く、例外処理やその他の問題を自分で処理する必要があるため、最適な方法ではありません。

大量挿入に推奨されるツールは以下のとおりです。

<SimpleTab groupId="platform">
<div label="TiDB Cloud" value="tidb-cloud">

-   データエクスポート： [Dumpling](/dumpling-overview.md)を使用して、MySQLまたはTiDBデータをローカルストレージまたはクラウドstorageにエクスポートします。TiDB Cloud StarterまたはEssentialインスタンスの場合は、 [TiDB Cloudコンソール](https://tidbcloud.com/)の[輸出](/tidb-cloud/serverless-export.md)機能を使用して、より効率的にデータをエクスポートすることもできます。
-   データのインポート: [TiDB Cloudコンソール](https://tidbcloud.com/)の[輸入](/tidb-cloud/import-sample-data.md)機能を使用します。 Dumplingでエクスポートしたデータをインポートしたり、ローカルの CSV ファイルをインポートしたり、[クラウドstorageからCSVファイルをTiDB Cloudにインポートする](/tidb-cloud/import-csv-files.md)ことができます。
-   データレプリケーション： [TiDB Cloudコンソール](https://tidbcloud.com/)の[TiDBデータ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能を使用します。 MySQL 互換データベースを TiDB にレプリケートできます。また、ソースデータベースからのシャーディングされたインスタンスとテーブルのマージおよび移行もサポートしています。
-   データのバックアップと復元: [TiDB Cloudコンソール](https://tidbcloud.com/)の[バックアップ](/tidb-cloud/backup-and-restore.md)機能を使用します。 Dumplingと比較して、バックアップと復元はビッグ データのシナリオにより適しています。

</div>
<div label="TiDB Self-Managed" value="tidb">

-   データエクスポート： [Dumpling](/dumpling-overview.md) 。MySQLまたはTiDBのデータをローカルまたはAmazon S3にエクスポートできます。
-   データインポート: [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 。 **Dumpling**でエクスポートされたデータ、 **CSV**ファイル、 [Amazon AuroraからTiDBへのデータ移行](/migrate-aurora-to-tidb.md)をインポートできます。ローカル ディスクまたは Amazon S3 クラウド ディスクからのデータの読み取りもサポートします。
-   データレプリケーション： [TiDBデータ移行](/dm/dm-overview.md)MySQL、MariaDB、Amazon AuroraデータベースをTiDBにレプリケートできます。また、ソースデータベースからのシャーディングされたインスタンスとテーブルのマージおよび移行もサポートしています。
-   データのバックアップと復元:[バックアップと復元 (BR)](/br/backup-and-restore-overview.md) 。 **Dumpling**と比較して、 **BR**は***ビッグデータの***シナリオにより適しています。

</div>
</SimpleTab>

## ホットスポットは避ける {#avoid-hotspots}

テーブルを設計するときは、多数の挿入操作があるかどうかを考慮する必要があります。その場合、テーブルの設計中にホットスポットを回避する必要があります。 [主キーを選択](/develop/dev-guide-create-table.md#select-primary-key)セクションを参照し、 [主キーを選択する際のルール](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)に従ってください。

TiDB セルフマネージドでホットスポットの問題を処理する方法の詳細については、[ホットスポットの問題をトラブルシューティングする](/troubleshoot-hot-spot-issues.md)。

## <code>AUTO_RANDOM</code>を主キーとするテーブルにデータを挿入する {#insert-data-to-a-table-with-the-code-auto-random-code-primary-key}

挿入するテーブルの主キーに`AUTO_RANDOM`属性がある場合、デフォルトでは主キーを指定できません。たとえば、 [`bookshop`](/develop/dev-guide-bookshop-schema-design.md)データベースでは、 [`users`テーブル](/develop/dev-guide-bookshop-schema-design.md#users-table)の`id`フィールドに`AUTO_RANDOM`属性が含まれていることがわかります。

この場合、以下のようなSQLを使用して挿入すること**はできません**。

```sql
INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
```

エラーが発生します:

    ERROR 8216 (HY000): Invalid auto random: Explicit insertion on auto_random column is disabled. Try to set @@allow_auto_random_explicit_insert = true.

挿入時に`AUTO_RANDOM`列を手動で指定することは推奨されません。

このエラーに対処するには、2つの解決策があります。

-   （推奨）挿入ステートメントからこの列を削除し、TiDB が初期化した`AUTO_RANDOM`の値を使用してください。これは`AUTO_RANDOM`のセマンティクスに適合します。

    ```sql
    INSERT INTO `bookshop`.`users` (`balance`, `nickname`) VALUES (0.00, 'nicky');
    ```

-   この列を指定する***必要が***あることが確実な場合は、 [`SET`ステートメント](https://docs.pingcap.com/tidb/stable/sql-statement-set-variable)使用できます。 ユーザー変数を変更することで、挿入時に`AUTO_RANDOM`の列を指定できるようにします。

    ```sql
    SET @@allow_auto_random_explicit_insert = true;
    INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
    ```

## HTAPを使用する {#use-htap}

TiDB では、HTAP 機能により、データの挿入時に追加の操作を実行する必要がなくなります。追加の挿入ロジックはありません。 TiDB はデータの一貫性を自動的に保証します。必要なのは、テーブルの作成後に[列指向レプリカ同期を有効にする](/develop/dev-guide-create-table.md#use-htap-capabilities)、列指向レプリカを使用してクエリを直接高速化することだけです。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
