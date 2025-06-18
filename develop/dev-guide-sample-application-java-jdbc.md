---
title: Connect to TiDB with JDBC
summary: JDBCを使用してTiDBに接続する方法を学びます。このチュートリアルでは、JDBCを使用してTiDBを操作するJavaサンプルコードスニペットを紹介します。
---

# JDBC で TiDB に接続する {#connect-to-tidb-with-jdbc}

TiDB は MySQL 互換のデータベースであり、JDBC (Java Database Connectivity) はJavaのデータ アクセス API です。1 [MySQL コネクタ/J](https://dev.mysql.com/downloads/connector/j/) MySQL の JDBC 実装です。

このチュートリアルでは、TiDB と JDBC を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   JDBC を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的なCRUD操作用の[サンプルコードスニペット](#sample-code-snippets)見つけることもできます。

<CustomContent platform="tidb">

> **注記：**
>
> -   このチュートリアルは、 TiDB Cloud Serverless、 TiDB Cloud Dedicated、および TiDB Self-Managed で機能します。
> -   TiDB v7.4以降、JDBC URLで`connectionCollation`設定されておらず、 `characterEncoding`設定されていないか`UTF-8`に設定されている場合、JDBC接続で使用される照合順序はJDBCドライバーのバージョンによって異なります。詳細については、 [JDBC接続で使用される照合順序](/faq/sql-faq.md#collation-used-in-jdbc-connections)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   このチュートリアルは、 TiDB Cloud Serverless、 TiDB Cloud Dedicated、および TiDB Self-Managed で機能します。
> -   TiDB v7.4以降、JDBC URLで`connectionCollation`が設定されておらず、 `characterEncoding`設定されていないか`UTF-8`に設定されている場合、JDBC接続で使用される照合順序はJDBCドライバーのバージョンによって異なります。詳細については、 [JDBC接続で使用される照合順序](https://docs.pingcap.com/tidb/stable/sql-faq#collation-used-in-jdbc-connections)参照してください。

</CustomContent>

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   **Java Development Kit (JDK) 17**以上。ビジネスおよび個人の要件に応じて、 [オープンJDK](https://openjdk.org/)または[オラクル JDK](https://www.oracle.com/hk/java/technologies/downloads/)選択できます。
-   [メイヴン](https://maven.apache.org/install.html) **3.8**以上。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **注記：**
>
> セキュリティ上の理由から、インターネット経由でTiDBクラスタに接続する場合は、 `VERIFY_IDENTITY`使用してTLS接続を確立することをお勧めします。TiDB TiDB Cloud ServerlessとTiDB Cloud DedicatedはどちらもSubject Alternative Name（SAN）証明書を使用するため、MySQL Connector/Jのバージョンは[8.0.22](https://dev.mysql.com/doc/relnotes/connector-j/en/news-8-0-22.html)以上である必要があります。

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプル コード リポジトリのクローンを作成するには、ターミナル ウィンドウで次のコマンドを実行します。

```shell
git clone https://github.com/tidb-samples/tidb-java-jdbc-quickstart.git
cd tidb-java-jdbc-quickstart
```

### ステップ2: 接続情報を構成する {#step-2-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています

    -   **ブランチ**は`main`に設定されています

    -   **接続先が**`General`に設定されています

    -   **オペレーティング システムは**環境に適合します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

5.  次のコマンドを実行して`env.sh.example`コピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

6.  対応する接続文字列をコピーして、 `env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメータに置き換えてください。

    TiDB Cloud Serverless は安全な接続を必要とします。そのため、 `USE_SSL`値を`true`に設定する必要があります。

7.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストをまだ設定していない場合は、 **「IP アクセス リストの設定」を**クリックするか、手順[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って、最初の接続の前に設定してください。

    TiDB Cloud Dedicatedは、**パブリック**接続タイプに加えて、**プライベートエンドポイント**と**VPCピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)ご覧ください。

4.  次のコマンドを実行して`env.sh.example`コピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

5.  対応する接続文字列をコピーして、 `env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメータに置き換えてください。

6.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Self-Managed">

1.  次のコマンドを実行して`env.sh.example`コピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

2.  対応する接続文字列をコピーして、 `env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    プレースホルダー`{}`接続パラメータに置き換え、 `USE_SSL`を`false`に設定してください。TiDBをローカルで実行している場合、デフォルトのホストアドレスは`127.0.0.1`で、パスワードは空です。

3.  `env.sh`ファイルを保存します。

</div>
</SimpleTab>

### ステップ3: コードを実行して結果を確認する {#step-3-run-the-code-and-check-the-result}

1.  サンプル コードを実行するには、次のコマンドを実行します。

    ```shell
    make
    ```

2.  [期待出力.txt](https://github.com/tidb-samples/tidb-java-jdbc-quickstart/blob/main/Expected-Output.txt)チェックして、出力が一致するかどうかを確認します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-java-jdbc-クイックスタート](https://github.com/tidb-samples/tidb-java-jdbc-quickstart)リポジトリを参照してください。

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

この関数を使用する場合は、 `${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、 `${tidb_db_name}` TiDB クラスターの実際の値に置き換える必要があります。

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

詳細については[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

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

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

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

詳細については[データを更新する](/develop/dev-guide-update-data.md)を参照してください。

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

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役立つメモ {#useful-notes}

### ドライバーまたは ORM フレームワークを使用していますか? {#using-driver-or-orm-framework}

Javaドライバーはデータベースへの低レベルのアクセスを提供しますが、開発者は次の作業を行う必要があります。

-   データベース接続を手動で確立および解放します。
-   データベース トランザクションを手動で管理します。
-   データ行をデータ オブジェクトに手動でマップします。

複雑なSQL文を書く必要がない限り、開発には[休止状態](/develop/dev-guide-sample-application-java-hibernate.md) 、 [マイバティス](/develop/dev-guide-sample-application-java-mybatis.md) 、 [スプリングデータ JPA](/develop/dev-guide-sample-application-java-spring-boot.md)などのフレームワークを[ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping)使用することをお勧めします。これにより、次のようなメリットが得られます。

-   接続とトランザクションを管理するために[定型コード](https://en.wikipedia.org/wiki/Boilerplate_code)減らします。
-   多数の SQL ステートメントの代わりにデータ オブジェクトを使用してデータを操作します。

## 次のステップ {#next-steps}

-   MySQL Connector/J の使用方法を[MySQL Connector/J のドキュメント](https://dev.mysql.com/doc/connector-j/en/)から詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入する](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB認定](https://www.pingcap.com/education/certification/)獲得します。
-   Java開発者向けコースを通じて学習します: [JavaからTiDBを操作する](https://eng.edu.pingcap.com/catalog/info/id:212) .

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
