---
title: Connect to TiDB with JDBC
summary: JDBCを使用してTiDBに接続する方法を学びましょう。このチュートリアルでは、JDBCを使用してTiDBと連携するJavaのサンプルコードを紹介します。
aliases: ['/ja/tidb/dev/sample-application-java','/ja/tidb/dev/dev-guide-sample-application-java','/ja/tidb/stable/dev-guide-sample-application-java-jdbc/','/ja/tidb/dev/dev-guide-sample-application-java-jdbc/','/ja/tidbcloud/dev-guide-sample-application-java-jdbc/']
---

# JDBCを使用してTiDBに接続する {#connect-to-tidb-with-jdbc}

TiDBはMySQL互換データベースであり、JDBC（Java Database Connectivity）はJavaのデータアクセスAPIです。MySQL [MySQL Connector/J](https://dev.mysql.com/downloads/connector/j/)は、MySQLにおけるJDBCの実装です。

このチュートリアルでは、TiDBとJDBCを使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   JDBCを使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> -   このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。
> -   TiDB v7.4 以降、 `connectionCollation`が構成されておらず、JDBC URL で`characterEncoding`が構成されていないか、または`UTF-8`に設定されている場合、JDBC 接続で使用される照合順序は JDBC ドライバーのバージョンによって異なります。詳細については、 [JDBC接続で使用される照合順序](/faq/sql-faq.md#collation-used-in-jdbc-connections)を参照してください。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   **Java Development Kit (JDK) 17**以降が必要です。業務要件や個人のニーズに応じて、 [OpenJDK](https://openjdk.org/)または[Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)を選択できます。
-   [メイブン](https://maven.apache.org/install.html)**3.8**以上。
-   [Git](https://git-scm.com/downloads) 。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## TiDBに接続するには、サンプルアプリを実行してください。 {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプルアプリケーションコードを実行してTiDBに接続する方法を説明します。

### ステップ1：サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプルコードリポジトリをクローンするには、ターミナルウィンドウで以下のコマンドを実行してください。

```shell
git clone https://github.com/tidb-samples/tidb-java-jdbc-quickstart.git
cd tidb-java-jdbc-quickstart
```

### ステップ2：接続情報を設定する {#step-2-configure-connection-information}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **Connect With は**`General`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **ヒント：**
    >
    > プログラムがWindows Subsystem for Linux（WSL）上で実行されている場合は、対応するLinuxディストリビューションに切り替えてください。

4.  **「パスワード生成」をクリックすると、ランダムなパスワード**が生成されます。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

5.  `env.sh.example`をコピーして`env.sh`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp env.sh.example env.sh
    ```

6.  対応する接続​​文字列`env.sh`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    必ずプレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに置き換えてください。

    TiDB Cloud Starter は安全な接続を必要とします。そのため、 `USE_SSL`の値を`true`に設定する必要があります。

7.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、「**接続タイプ」**ドロップダウンリストから**「パブリック」**を選択し、 **「CA証明書」**をクリックしてCA証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)。

    TiDB Cloud Dedicated は、**パブリック**接続タイプに加えて、**プライベート エンドポイント**および**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  `env.sh.example`をコピーして`env.sh`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp env.sh.example env.sh
    ```

5.  対応する接続​​文字列`env.sh`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    必ずプレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに置き換えてください。

6.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  `env.sh.example`をコピーして`env.sh`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp env.sh.example env.sh
    ```

2.  対応する接続​​文字列`env.sh`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    プレースホルダー`{}`を接続パラメータに置き換え、 `USE_SSL` `false`に設定してください。TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `env.sh`ファイルを保存します。

</div>
</SimpleTab>

### ステップ3：コードを実行して結果を確認する {#step-3-run-the-code-and-check-the-result}

1.  サンプルコードを実行するには、以下のコマンドを実行してください。

    ```shell
    make
    ```

2.  [期待される出力.txt](https://github.com/tidb-samples/tidb-java-jdbc-quickstart/blob/main/Expected-Output.txt)をチェックして、出力が一致するかどうかを確認してください。

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-java-jdbc-quickstart](https://github.com/tidb-samples/tidb-java-jdbc-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

```java
public MysqlDataSource getMysqlDataSource() throws SQLException {
    MysqlDataSource mysqlDataSource = new MysqlDataSource();

    mysqlDataSource.setServerName(${tidb_host});
    mysqlDataSource.setPortNumber(${tidb_port});
    mysqlDataSource.setUser(${tidb_user});
    mysqlDataSource.setPassword(${tidb_password});
    mysqlDataSource.setDatabaseName(${tidb_db_name});
    if (${tidb_use_ssl}) {
        mysqlDataSource.setSslMode(PropertyDefinitions.SslMode.VERIFY_IDENTITY.name());
        mysqlDataSource.setEnabledTLSProtocols("TLSv1.2,TLSv1.3");
    }

    return mysqlDataSource;
}
```

この機能を使用する場合は、 `${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、および`${tidb_db_name}` TiDBの実際の値に置き換える必要があります。

### データを挿入する {#insert-data}

```java
public void createPlayer(PlayerBean player) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSource();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement preparedStatement = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)");
        preparedStatement.setString(1, player.getId());
        preparedStatement.setInt(2, player.getCoins());
        preparedStatement.setInt(3, player.getGoods());

        preparedStatement.execute();
    }
}
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

```java
public void getPlayer(String id) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSourceByEnv();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM player WHERE id = ?");
        preparedStatement.setString(1, id);
        preparedStatement.execute();

        ResultSet res = preparedStatement.executeQuery();
        if(res.next()) {
            PlayerBean player = new PlayerBean(res.getString("id"), res.getInt("coins"), res.getInt("goods"));
            System.out.println(player);
        }
    }
}
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

```java
public void updatePlayer(String id, int amount, int price) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSourceByEnv();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement transfer = connection.prepareStatement("UPDATE player SET goods = goods + ?, coins = coins + ? WHERE id=?");
        transfer.setInt(1, -amount);
        transfer.setInt(2, price);
        transfer.setString(3, id);
        transfer.execute();
    }
}
```

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

```java
public void deletePlayer(String id) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSourceByEnv();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement deleteStatement = connection.prepareStatement("DELETE FROM player WHERE id=?");
        deleteStatement.setString(1, id);
        deleteStatement.execute();
    }
}
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役立つメモ {#useful-notes}

### ドライバーまたはORMフレームワークを使用していますか？ {#using-driver-or-orm-framework}

Javaドライバはデータベースへの低レベルアクセスを提供するが、開発者には以下のことが必要となる。

-   データベース接続を手動で確立および解放します。
-   データベースのトランザクションを手動で管理する。
-   データ行をデータオブジェクトに手動でマッピングします。

複雑なSQL文を書く必要がない限り、 [ハイバネイト](/develop/dev-guide-sample-application-java-hibernate.md)、 [MyBatis](/develop/dev-guide-sample-application-java-mybatis.md) 、 [Spring Data JPA](/develop/dev-guide-sample-application-java-spring-boot.md)などの[ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping)フレームワークを開発に利用することをお勧めします。これにより、以下のようなメリットが得られます。

-   接続とトランザクションを管理するための[定型コード](https://en.wikipedia.org/wiki/Boilerplate_code)を削減します。
-   多数のSQL文の代わりに、データオブジェクトを使用してデータを操作します。

### MySQLとの互換性 {#mysql-compatibility}

MySQL では、 `DECIMAL`列にデータを挿入する際に、小数点以下の桁数が列で定義されているスケールを超えた場合、MySQL は余分な桁を自動的に切り捨て、切り捨てられたデータを正常に挿入します。余分な小数点以下の桁数に関係なく、この処理が行われます。

TiDB v8.5.3以前のバージョンでは：

-   小数点以下の桁数が定義されたスケールを超えているが72を超えていない場合、TiDBは余分な桁を自動的に切り捨て、切り捨てられたデータを正常に挿入します。
-   ただし、小数点以下の桁数が72を超えると、挿入は失敗し、エラーが返されます。

TiDB v8.5.4以降、TiDBはMySQLの動作に準拠するようになりました。つまり、小数点以下の桁数がいくつ多くても、余分な桁を自動的に切り捨て、切り捨てられたデータを正常に挿入します。

## 次のステップ {#next-steps}

-   MySQL Connector/J の使用法の詳細については[MySQL Connector/J のドキュメント](https://dev.mysql.com/doc/connector-j/en/)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。
-   Java開発者向けのコース「 [JavaからTiDBを操作する](https://eng.edu.pingcap.com/catalog/info/id:212)を通じて学習します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
