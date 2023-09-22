---
title: Connect to TiDB with Spring Boot
summary: Learn how to connect to TiDB using Spring Boot. This tutorial gives Java sample code snippets that work with TiDB using Spring Boot.
aliases: ['/tidb/v7.1/dev-guide-sample-application-spring-boot']
---

# Spring Boot を使用して TiDB に接続する {#connect-to-tidb-with-spring-boot}

TiDB は MySQL 互換データベースであり、 Java用の人気の[春](https://spring.io/)オープンソース コンテナ フレームワークです。このドキュメントでは Spring の使用方法として[スプリングブーツ](https://spring.io/projects/spring-boot)を使用します。

このチュートリアルでは、TiDB を JPA プロバイダーとして[Spring Data JPA](https://spring.io/projects/spring-data-jpa)および[休止状態](https://hibernate.org/orm/)とともに使用して、次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   Hibernate と Spring Data JPA を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、TiDB サーバーレス、TiDB 専用、および TiDB セルフホストで動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   **Java開発キット (JDK) 17**以降。ビジネスや個人の要件に基づいて[OpenJDK](https://openjdk.org/)または[オラクルJDK](https://www.oracle.com/hk/java/technologies/downloads/)を選択できます。
-   [メイビン](https://maven.apache.org/install.html) **3.8**以上。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプル アプリを実行して TiDB に接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

### ステップ 1: サンプル アプリ リポジトリのクローンを作成する {#step-1-clone-the-sample-app-repository}

ターミナル ウィンドウで次のコマンドを実行して、サンプル コード リポジトリのクローンを作成します。

```shell
git clone https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart.git
cd tidb-java-springboot-jpa-quickstart
```

### ステップ 2: 接続情報を構成する {#step-2-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます

    -   **[接続先] は**`General`に設定されています

    -   **オペレーティング システムが**環境に一致します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  **「パスワードの作成」**をクリックしてランダムなパスワードを作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

5.  次のコマンドを実行して`env.sh.example`をコピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

6.  対応する接続​​文字列をコピーして`env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメーターに必ず置き換えてください。

    TiDB サーバーレスには安全な接続が必要です。したがって、 `USE_SSL` ～ `true`の値を設定する必要があります。

7.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **「どこからでもアクセスを許可」**をクリックし、 **「TiDB クラスター CA のダウンロード」**をクリックして CA 証明書をダウンロードします。

    接続文字列の取得方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

4.  次のコマンドを実行して`env.sh.example`をコピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

5.  対応する接続​​文字列をコピーして`env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメーターに必ず置き換えてください。

6.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Self-Hosted">

1.  次のコマンドを実行して`env.sh.example`をコピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

2.  対応する接続​​文字列をコピーして`env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    必ずプレースホルダー`{}`接続パラメーターに置き換えて、 `USE_SSL`を`false`に設定してください。 TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `env.sh`ファイルを保存します。

</div>
</SimpleTab>

### ステップ 3: コードを実行して結果を確認する {#step-3-run-the-code-and-check-the-result}

1.  次のコマンドを実行してサンプル コードを実行します。

    ```shell
    make
    ```

2.  別のターミナル セッションでリクエスト スクリプトを実行します。

    ```shell
    make request
    ```

3.  [予想される出力.txt](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart/blob/main/Expected-Output.txt)チェックして、出力が一致するかどうかを確認します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了できます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-java-springboot-jpa-quickstart](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart)リポジトリを確認してください。

### TiDB に接続する {#connect-to-tidb}

構成ファイル`application.yml`を編集します。

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

構成後、環境変数`TIDB_JDBC_URL` 、 `TIDB_USER` 、および`TIDB_PASSWORD`を TiDB クラスターの実際の値に設定します。構成ファイルは、これらの環境変数のデフォルト設定を提供します。環境変数を設定しない場合、デフォルト値は次のとおりです。

-   `TIDB_JDBC_URL` ： `"jdbc:mysql://localhost:4000/test"`
-   `TIDB_USER` ： `"root"`
-   `TIDB_PASSWORD` ： `""`

### データ管理: <code>@Repository</code> {#data-management-code-repository-code}

Spring Data JPA は`@Repository`インターフェイスを通じてデータを管理します。 `JpaRepository`によって提供される CRUD 操作を使用するには、 `JpaRepository`インターフェイスを拡張する必要があります。

```java
@Repository
public interface PlayerRepository extends JpaRepository<PlayerBean, Long> {
}
```

その後、 `PlayerRepository`を必要とするクラスで自動依存関係注入に`@Autowired`使用できます。これにより、CRUD関数を直接使用できるようになります。以下は例です。

```java
@Autowired
private PlayerRepository playerRepository;
```

### データの挿入または更新 {#insert-or-update-data}

```java
playerRepository.save(player);
```

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)および[データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### クエリデータ {#query-data}

```java
PlayerBean player = playerRepository.findById(id).orElse(null);
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの削除 {#delete-data}

```java
playerRepository.deleteById(id);
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   Hibernate の詳しい使い方を[Hibernate のドキュメント](https://hibernate.org/orm/documentation)から学びましょう。

-   このドキュメントで使用されているサードパーティのライブラリとフレームワークの使用方法の詳細については、その公式ドキュメントを参照してください。

    -   [Spring Frameworkのドキュメント](https://spring.io/projects/spring-framework)
    -   [Spring Boot のドキュメント](https://spring.io/projects/spring-boot)
    -   [Spring Data JPAのドキュメント](https://spring.io/projects/spring-data-jpa)
    -   [Hibernate のドキュメント](https://hibernate.org/orm/documentation)

-   TiDB アプリケーション[データの削除](/develop/dev-guide-delete-data.md) [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)ベスト プラクティス[SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)は、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) [データを更新する](/develop/dev-guide-update-data.md)参照[トランザクション](/develop/dev-guide-transaction-overview.md)てください。

-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

-   Java開発者向けのコースを通じて[Javaから TiDB を操作する](https://eng.edu.pingcap.com/catalog/info/id:212)を学びます。

## 助けが必要？ {#need-help}

[不和](https://discord.gg/vYU9h56kAX)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。
