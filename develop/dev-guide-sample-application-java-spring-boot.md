---
title: Connect to TiDB with Spring Boot
summary: Spring Boot を使用して TiDB に接続する方法を学習します。このチュートリアルでは、Spring Boot を使用して TiDB で動作するJavaサンプル コード スニペットを紹介します。
---

# Spring Boot で TiDB に接続する {#connect-to-tidb-with-spring-boot}

TiDB は MySQL 互換のデータベースであり、 [春](https://spring.io/) Java用の人気のオープンソース コンテナ フレームワークです。このドキュメントでは、Spring の使用方法として[スプリングブート](https://spring.io/projects/spring-boot)使用します。

このチュートリアルでは、TiDB を JPA プロバイダーとして[スプリングデータ JPA](https://spring.io/projects/spring-data-jpa)および[休止状態](https://hibernate.org/orm/)とともに使用して、次のタスクを実行する方法を学習します。

-   環境を設定します。
-   Hibernate と Spring Data JPA を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)見つけることができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Serverless、 TiDB Cloud Dedicated、および TiDB Self-Managed で機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   **Java Development Kit (JDK) 17**以上。ビジネスおよび個人の要件に応じて[オープンJDK](https://openjdk.org/)または[オラクル](https://www.oracle.com/hk/java/technologies/downloads/)選択できます。
-   [メイヴン](https://maven.apache.org/install.html) **3.8**以上。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を示します。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプル コード リポジトリを複製するには、ターミナル ウィンドウで次のコマンドを実行します。

```shell
git clone https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart.git
cd tidb-java-springboot-jpa-quickstart
```

### ステップ2: 接続情報を構成する {#step-2-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています

    -   **ブランチは**`main`に設定されています

    -   **接続先は**`General`に設定されています

    -   **オペレーティング システムは**環境に適合します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」**をクリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成することができます。

5.  次のコマンドを実行して`env.sh.example`コピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

6.  対応する接続文字列をコピーして`env.sh`ファイルに貼り付けます。例の結果は次のようになります。

    ```shell
    export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメータに必ず置き換えてください。

    TiDB Cloud Serverless では安全な接続が必要です。そのため、 `USE_SSL`の値を`true`に設定する必要があります。

7.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、 **「IP アクセス リストの設定」**をクリックするか、手順[IPアクセスリストを構成する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って最初の接続の前に設定してください。

    **パブリック**接続タイプに加えて、TiDB Dedicated は**プライベートエンドポイント**と**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  次のコマンドを実行して`env.sh.example`コピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

5.  対応する接続文字列をコピーして`env.sh`ファイルに貼り付けます。例の結果は次のようになります。

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメータに必ず置き換えてください。

6.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Self-Managed">

1.  次のコマンドを実行して`env.sh.example`コピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

2.  対応する接続文字列をコピーして`env.sh`ファイルに貼り付けます。例の結果は次のようになります。

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    プレースホルダー`{}`接続パラメータに置き換え、 `USE_SSL`を`false`に設定してください。TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `env.sh`ファイルを保存します。

</div>
</SimpleTab>

### ステップ3: コードを実行して結果を確認する {#step-3-run-the-code-and-check-the-result}

1.  サンプル コードを実行するには、次のコマンドを実行します。

    ```shell
    make
    ```

2.  別のターミナル セッションでリクエスト スクリプトを実行します。

    ```shell
    make request
    ```

3.  [予想される出力.txt](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart/blob/main/Expected-Output.txt)をチェックして、出力が一致するかどうかを確認します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-java-springboot-jpa-クイックスタート](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

設定ファイル`application.yml`を編集します:

```yaml
spring:
  datasource:
    url: ${TIDB_JDBC_URL:jdbc:mysql://localhost:4000/test}
    username: ${TIDB_USER:root}
    password: ${TIDB_PASSWORD:}
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

設定後、環境変数`TIDB_JDBC_URL` `TIDB_USER` TiDB クラスターの実際の値に設定します。設定ファイルには`TIDB_PASSWORD`これらの環境変数のデフォルト設定が用意されています。環境変数を設定しない場合、デフォルト値は次のようになります。

-   `TIDB_JDBC_URL` : `"jdbc:mysql://localhost:4000/test"`
-   `TIDB_USER` : `"root"`
-   `TIDB_PASSWORD` : `""`

### データ管理: <code>@Repository</code> {#data-management-code-repository-code}

Spring Data JPA は`@Repository`インターフェースを通じてデータを管理します。 `JpaRepository`が提供する CRUD 操作を使用するには、 `JpaRepository`インターフェースを拡張する必要があります。

```java
@Repository
public interface PlayerRepository extends JpaRepository<PlayerBean, Long> {
}
```

次に、 `PlayerRepository`必要とするクラスで`@Autowired`使用して自動依存性注入を行うことができます。これにより、 CRUD関数を直接使用できるようになります。次に例を示します。

```java
@Autowired
private PlayerRepository playerRepository;
```

### データの挿入または更新 {#insert-or-update-data}

```java
playerRepository.save(player);
```

詳細については、 [データを挿入](/develop/dev-guide-insert-data.md)および[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### クエリデータ {#query-data}

```java
PlayerBean player = playerRepository.findById(id).orElse(null);
```

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを削除する {#delete-data}

```java
playerRepository.deleteById(id);
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   このドキュメントで使用されているサードパーティのライブラリとフレームワークの使用方法の詳細については、公式ドキュメントを参照してください。

    -   [Spring Frameworkのドキュメント](https://spring.io/projects/spring-framework)
    -   [Spring Bootのドキュメント](https://spring.io/projects/spring-boot)
    -   [Spring Data JPAのドキュメント](https://spring.io/projects/spring-data-jpa)
    -   [Hibernateのドキュメント](https://hibernate.org/orm/documentation)

-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブル読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。

-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

-   Java開発者向けコースを通じて学習します: [Javaから TiDB を操作する](https://eng.edu.pingcap.com/catalog/info/id:212) .

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
