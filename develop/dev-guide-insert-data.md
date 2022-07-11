---
title: Insert Data
summary: Learn about how to insert data.
---

<!-- markdownlint-disable MD029 -->

# データを挿入 {#insert-data}

このドキュメントでは、さまざまなプログラミング言語でSQL言語を使用してTiDBにデータを挿入する方法について説明します。

## 始める前に {#before-you-start}

このドキュメントを読む前に、以下を準備する必要があります。

-   [TiDB CloudでTiDBクラスターを構築する（DevTier）](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md) 、および[データベースを作成する](/develop/dev-guide-create-database.md) [セカンダリインデックスを作成する](/develop/dev-guide-create-secondary-indexes.md) [テーブルを作成する](/develop/dev-guide-create-table.md)

## 行を挿入する {#insert-rows}

複数行のデータを挿入する方法は2つあります。たとえば、 **3**人のプレーヤーのデータを挿入する必要がある場合。

-   **複数行の挿入ステートメント**：

    {{< copyable "" >}}

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2), (3, 300, 5);
    ```

-   複数**の単一行挿入ステートメント**：

    {{< copyable "" >}}

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (2, 230, 2);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (3, 300, 5);
    ```

通常、 `multi-line insertion statement`は複数の`single-line insertion statements`よりも高速に実行されます。

<SimpleTab>
<div label="SQL">

{{< copyable "" >}}

```sql
CREATE TABLE `player` (`id` INT, `coins` INT, `goods` INT);
INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2);
```

このSQLの使用方法の詳細については、 [TiDBクラスターへの接続](/develop/dev-guide-build-cluster-in-cloud.md#step-2-connect-to-a-cluster)を参照し、クライアントを使用してTiDBクラスタに接続した後にSQLステートメントを入力する手順に従ってください。

</div>

<div label="Java">

{{< copyable "" >}}

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

デフォルトのMySQLJDBCDriver設定により、一括挿入のパフォーマンスを向上させるには、いくつかのパラメーターを変更する必要があります。

|            パラメータ           |                意味                |                                                                   推奨シナリオ                                                                  | 推奨されるConfiguration / コンフィグレーション |
| :------------------------: | :------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------: |
|    `useServerPrepStmts`    | サーバー側を使用してプリペアドステートメントを有効にするかどうか |                                                        プリペアドステートメントを複数回使用する必要がある場合                                                        |              `true`             |
|      `cachePrepStmts`      |  クライアントがプリペアドステートメントをキャッシュするかどうか |                                                         `useServerPrepStmts=true`時                                                        |              `true`             |
|   `prepStmtCacheSqlLimit`  | プリペアドステートメントの最大サイズ（デフォルトでは256文字） |                                                          プリペアドステートメントが256文字を超える場合                                                         |  プリペアドステートメントの実際のサイズに従って構成されます  |
|     `prepStmtCacheSize`    | プリペアドステートメントキャッシュの最大数（デフォルトでは25） |                                                          プリペアドステートメントの数が25を超える場合                                                          |   プリペアドステートメントの実際の数に応じて構成されます   |
| `rewriteBatchedStatements` |     **バッチ**ステートメントを書き換えるかどうか     |                                                                バッチ操作が必要な場合                                                                |              `true`             |
|     `allowMultiQueries`    |            バッチ操作を開始します           | [クライアントのバグ](https://bugs.mysql.com/bug.php?id=96623)は、 `rewriteBatchedStatements = true`と`useServerPrepStmts = true`のときにこれを設定する必要があるためです。 |              `true`             |

MySQL JDBC Driverは、統合構成も提供します： `useConfigs` 。 `maxPerformance`で構成されている場合は、一連の構成を構成するのと同じです。 `mysql:mysql-connector-java:8.0.28`を例にとると、 `useConfigs=maxPerformance`には次のものが含まれます。

{{< copyable "" >}}

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

`mysql-connector-java-{version}.jar!/com/mysql/cj/configurations/maxPerformance.properties`をチェックすると、対応するバージョンのDriverの`useConfigs=maxPerformance`に含まれる構成を取得できます。

以下は、JDBC接続文字列構成の一般的なシナリオです。この例では、ホスト： `127.0.0.1` 、ポート： `4000` 、ユーザー名： `root` 、パスワード：null、デフォルトのデータベース： `test` ：

{{< copyable "" >}}

```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

Javaの完全な例については、以下を参照してください。

-   [TiDBとJavaを使用してシンプルなCRUDアプリを構築する-JDBCを使用する](/develop/dev-guide-sample-application-java.md#step-2-get-the-code)
-   [TiDBとJavaを使用してシンプルなCRUDアプリを構築する-Hibernateを使用する](/develop/dev-guide-sample-application-java.md#step-2-get-the-code)
-   [SpringBootを使用してTiDBアプリケーションを構築する](/develop/dev-guide-sample-application-spring-boot.md)

</div>

</SimpleTab>

## 一括挿入 {#bulk-insert}

大量のデータをTiDBクラスタにすばやくインポートする必要がある場合は、データ移行に**PingCAP**が提供するさまざまなツールを使用することをお勧めします。 `INSERT`ステートメントを使用するのは効率的ではなく、例外やその他の問題を自分で処理する必要があるため、最善の方法ではありません。

一括挿入に推奨されるツールは次のとおりです。

-   データのエクスポート： [Dumpling](/dumpling-overview.md) 。 MySQLまたはTiDBデータをローカルまたはAmazonS3にエクスポートできます。
-   データのインポート： [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 。**Dumpling**のエクスポートされたデータ、 <strong>CSV</strong>ファイル、または[AuroraからTiDBへのデータの移行](/migrate-aurora-to-tidb.md)をインポートできます。また、ローカルディスクまたは[AmazonS3クラウドディスク](/br/backup-and-restore-storages.md)からのデータの読み取りもサポートしています。
-   データ複製： [TiDBデータ移行](/dm/dm-overview.md) 。 MySQL、MariaDB、およびAuroraデータベースをTiDBに複製できます。また、シャーディングされたインスタンスとテーブルのソースデータベースからのマージと移行もサポートしています。
-   データのバックアップと復元： [バックアップと復元（BR）](/br/backup-and-restore-overview.md) 。**Dumpling**と比較して、 <strong>BR</strong>は*<strong>ビッグデータ</strong>*のシナリオに適しています。

## ホットスポットを避ける {#avoid-hotspots}

テーブルを設計するときは、挿入操作が多数あるかどうかを考慮する必要があります。その場合、テーブルの設計中にホットスポットを回避する必要があります。 [主キーを選択します](/develop/dev-guide-create-table.md#select-primary-key)のセクションを参照し、 [主キーを選択する際のルール](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)に従ってください。

ホットスポットの問題を処理する方法の詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

## <code>AUTO_RANDOM</code>主キーを使用してテーブルにデータを挿入します {#insert-data-to-a-table-with-the-code-auto-random-code-primary-key}

挿入するテーブルの主キーに`AUTO_RANDOM`属性がある場合、デフォルトでは主キーを指定できません。たとえば、 [`bookshop`](/develop/dev-guide-bookshop-schema-design.md)データベースでは、 [`users`テーブル](/develop/dev-guide-bookshop-schema-design.md#users-table)の`id`フィールドに`AUTO_RANDOM`属性が含まれていることがわかります。

この場合、次のようなSQLを使用して挿入する**ことはできません**。

{{< copyable "" >}}

```sql
INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
```

エラーが発生します：

```
ERROR 8216 (HY000): Invalid auto random: Explicit insertion on auto_random column is disabled. Try to set @@allow_auto_random_explicit_insert = true.
```

挿入時に`AUTO_RANDOM`列を手動で指定することはお勧めしません。

このエラーを処理するには、次の2つの解決策があります。

-   （推奨）この列を挿入ステートメントから削除し、TiDBが初期化した`AUTO_RANDOM`の値を使用します。これは`AUTO_RANDOM`のセマンティクスに適合します。

    {{< copyable "" >}}

    ```sql
    INSERT INTO `bookshop`.`users` (`balance`, `nickname`) VALUES (0.00, 'nicky');
    ```

-   この列を指定する***必要***があることが確実な場合は、 [`SET`ステートメント](https://docs.pingcap.com/zh/tidb/stable/sql-statement-set-variable)を使用して、ユーザー変数を変更することにより、挿入時に`AUTO_RANDOM`の列を指定できるようにすることができます。

    {{< copyable "" >}}

    ```sql
    SET @@allow_auto_random_explicit_insert = true;
    INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
    ```

## HTAPを使用する {#use-htap}

TiDBでは、HTAP機能により、データを挿入するときに追加の操作を実行する必要がなくなります。追加の挿入ロジックはありません。 TiDBは、データの一貫性を自動的に保証します。テーブルを作成した後は[列指向のレプリカ同期をオンにする](/develop/dev-guide-create-table.md#use-htap-capabilities)を実行するだけで、列指向のレプリカを使用してクエリを直接高速化できます。
