---
title: Connect to TiDB with Spring Boot
summary: Spring Bootを使用してTiDBに接続する方法を学びましょう。このチュートリアルでは、Spring Bootを使用してTiDBと連携するJavaのサンプルコードを紹介します。
aliases: ['/ja/tidbcloud/dev-guide-sample-application-spring-boot','/ja/tidb/dev/dev-guide-sample-application-spring-boot','/ja/tidb/stable/dev-guide-sample-application-java-spring-boot/','/ja/tidb/dev/dev-guide-sample-application-java-spring-boot/','/ja/tidbcloud/dev-guide-sample-application-java-spring-boot/']
---

# Spring Bootを使用してTiDBに接続する {#connect-to-tidb-with-spring-boot}

[春](https://spring.io/)は MySQL 互換データベースであり、 Java用の人気のあるオープンソース コンテナ フレームワークです。このドキュメントでは Spring の使用方法として[スプリングブーツ](https://spring.io/projects/spring-boot)を使用します。

このチュートリアルでは、TiDBを[Spring Data JPA](https://spring.io/projects/spring-data-jpa)およびJPAプロバイダとしての[ハイバネイト](https://hibernate.org/orm/)と組み合わせて使用​​し、以下のタスクを実行する方法を学びます。

-   環境をセットアップしてください。
-   HibernateとSpring Data JPAを使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Premium、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

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
git clone https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart.git
cd tidb-java-springboot-jpa-quickstart
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

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

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
<div label="TiDB Cloud Premium">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワークの**ページで、 **[パブリックエンドポイント****を有効にする]**をクリックし、次に**[IP アドレスの追加]**をクリックします。

    クライアントのIPアドレスがアクセスリストに追加されていることを確認してください。

4.  左側のナビゲーションペインで**「概要」**をクリックすると、インスタンスの概要ページに戻ります。

5.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

6.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    -   公開エンドポイントがまだ有効化中であることを示すメッセージが表示された場合は、処理が完了するまでお待ちください。
    -   まだパスワードを設定していない場合は、ダイアログの**「ルートパスワードを設定」**をクリックしてください。
    -   サーバー証明書を確認する必要がある場合、または接続に失敗して認証局（CA）証明書が必要な場合は、 **「CA証明書」**をクリックしてダウンロードしてください。
    -   **パブリック**接続タイプに加えて、 TiDB Cloud Premium は**プライベート エンドポイント**接続をサポートします。詳細については、 [AWS PrivateLink経由でTiDB Cloud Premiumに接続します。](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md)を参照してください。

7.  `env.sh.example`をコピーして`env.sh`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp env.sh.example env.sh
    ```

8.  対応する接続​​文字列`env.sh`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    必ずプレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに置き換えてください。

9.  `env.sh`ファイルを保存します。

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

2.  別のターミナルセッションでリクエストスクリプトを実行してください。

    ```shell
    make request
    ```

3.  [期待される出力.txt](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart/blob/main/Expected-Output.txt)をチェックして、出力が一致するかどうかを確認してください。

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-java-springboot-jpa-quickstart](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

設定ファイル`application.yml`を編集します。

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

設定後、環境変数`TIDB_JDBC_URL` 、 `TIDB_USER` 、および`TIDB_PASSWORD`を、ご使用の TiDB の実際の値に設定してください。設定ファイルには、これらの環境変数のデフォルト設定が記載されています。環境変数を設定しない場合、デフォルト値は次のようになります。

-   `TIDB_JDBC_URL` : `"jdbc:mysql://localhost:4000/test"`
-   `TIDB_USER` : `"root"`
-   `TIDB_PASSWORD` : `""`

### データ管理: <code>@Repository</code> {#data-management-code-repository-code}

Spring Data JPA は`@Repository`インターフェースを介してデータを管理します。 `JpaRepository`が提供する CRUD 操作を使用するには、 `JpaRepository`インターフェースを拡張する必要があります。

```java
@Repository
public interface PlayerRepository extends JpaRepository<PlayerBean, Long> {
}
```

次に、 `@Autowired`を必要とするクラスに`PlayerRepository`使用して自動依存性注入を行うことができます。これにより、CRUD関数を直接使用できるようになります。以下に例を示します。

```java
@Autowired
private PlayerRepository playerRepository;
```

### データを挿入または更新する {#insert-or-update-data}

```java
playerRepository.save(player);
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### クエリデータ {#query-data}

```java
PlayerBean player = playerRepository.findById(id).orElse(null);
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを削除する {#delete-data}

```java
playerRepository.deleteById(id);
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   このドキュメントで使用されているサードパーティライブラリおよびフレームワークの詳細については、それぞれの公式ドキュメントを参照してください。

    -   [Spring Frameworkのドキュメント](https://spring.io/projects/spring-framework)
    -   [Spring Bootのドキュメント](https://spring.io/projects/spring-boot)
    -   [Spring Data JPAのドキュメント](https://spring.io/projects/spring-data-jpa)
    -   [Hibernateのドキュメント](https://hibernate.org/orm/documentation)

-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。

-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

-   Java開発者向けのコース「 [JavaからTiDBを操作する](https://eng.edu.pingcap.com/catalog/info/id:212)を通じて学習します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
