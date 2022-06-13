---
title: Build a TiDB Application Using Spring Boot
summary: Learn an example of how to build a TiDB application using Spring Boot.
---

<!-- markdownlint-disable MD029 -->

# SpringBootを使用してTiDBアプリケーションを構築する {#build-a-tidb-application-using-spring-boot}

このチュートリアルでは、TiDBを使用して[スプリングブーツ](https://spring.io/projects/spring-boot)のWebアプリケーションを構築する方法を示します。 [Spring Data JPA](https://spring.io/projects/spring-data-jpa)モジュールは、データアクセス機能のフレームワークとして使用されます。このサンプルアプリケーションのコードは[GitHub](https://github.com/pingcap-inc/tidb-example-java)からダウンロードできます。

これは、RESTful APIを構築するためのサンプルアプリケーションであり、データベースとして**TiDB**を使用する一般的な<strong>SpringBoot</strong>バックエンドサービスを示しています。次のプロセスは、実際のシナリオを再現するために設計されました。

これは、各プレーヤーが`coins`と`goods`の2つの属性を持つゲームの例です。各プレーヤーは、 `id`のフィールドによって一意に識別されます。十分なコインや商品があれば、プレイヤーは自由に取引できます。

この例に基づいて、独自のアプリケーションを構築できます。

## ステップ1：TiDBクラスタを起動する {#step-1-launch-your-tidb-cluster}

このステップでは、TiDBクラスタを開始する方法について説明します。

### TiDB Cloudフリークラスタの使用 {#using-a-tidb-cloud-free-cluster}

[無料のクラスタを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-free-cluster) 。

### ローカルクラスタの使用 {#using-a-local-cluster}

ローカルクラスタは、 [ローカルテストクラスタのデプロイ](/quick-start-with-tidb.md)または[TiDBクラスタを本番環境にデプロイする](/production-deployment-using-tiup.md)のいずれかで開始できます。

## ステップ2：JDKをインストールする {#step-2-install-jdk}

コンピュータに**JavaDevelopmentKit** （JDK）をダウンロードしてインストールします。 Java開発に必要なツールです。 <strong>Spring Boot</strong>は、JDK forJava8以降のバージョンをサポートします。ただし、 <strong>Hibernate</strong>バージョンのため、Java11以降のバージョンではJDKを使用することをお勧めします。

**OracleJDK**と<strong>OpenJDK</strong>の両方がサポートされています。あなたはあなた自身の裁量で選ぶことができます。このチュートリアルでは、 <strong>OpenJDK</strong>のJDK17を使用します。

## ステップ3：Mavenをインストールする {#step-3-install-maven}

このサンプルアプリケーションは、 **ApacheMaven**を使用してアプリケーションの依存関係を管理します。 SpringはMaven3.3以降のバージョンをサポートしています。依存関係管理ソフトウェアとして、 <strong>Maven</strong>の最新の安定バージョンをお勧めします。

コマンドラインから**Maven**をインストールするには。

-   マックOS：

    {{< copyable "" >}}

    ```shell
    brew install maven
    ```

-   DebianベースのLinuxディストリビューション（Ubuntuなど）：

    {{< copyable "" >}}

    ```shell
    apt-get install maven
    ```

-   Red HatベースのLinuxディストリビューション（Fedora、CentOSなど）：

    -   dnf：

        {{< copyable "" >}}

        ```shell
        dnf install maven
        ```

    -   yum：

        {{< copyable "" >}}

        ```shell
        yum install maven
        ```

その他のインストール方法については、 [Mavenの公式ドキュメント](https://maven.apache.org/install.html)を参照してください。

## ステップ4：アプリケーションコードを取得する {#step-4-get-the-application-code}

[サンプルコードリポジトリ](https://github.com/pingcap-inc/tidb-example-java)をダウンロードまたは複製し、 `spring-jpa-hibernate`ディレクトリに移動します。

### 同じ依存関係で空のアプリケーションを作成する（オプション） {#create-a-blank-application-with-the-same-dependency-optional}

このアプリケーションは[Spring Initializr](https://start.spring.io/)を使用して構築されています。次のオプションをクリックし、いくつかの構成項目を変更することで、このサンプルアプリケーションと同じ依存関係を持つ空のアプリケーションをすばやく取得できます。

**計画**

-   Mavenプロジェクト

**言語**

-   Java

**スプリングブーツ**

-   3.0.0-M2

**プロジェクトメタデータ**

-   グループ：com.pingcap
-   アーティファクト：spring-jpa-hibernate
-   名前：spring-jpa-hibernate
-   パッケージ名：com.pingcap
-   包装：瓶
-   Java：17

**依存関係**

-   春のウェブ
-   Spring Data JPA
-   MySQLドライバー

完全な構成は次のとおりです。

![Spring Initializr Configuration](/media/develop/develop-spring-initializr-configuration.png)

> **ノート：**
>
> SQLは比較的標準化されていますが、各データベースベンダーは、ANSISQLで定義された構文のサブセットとスーパーセットを使用しています。これは、データベースの方言と呼ばれます。 Hibernateは、各データベースベンダーの`org.hibernate.dialect.Dialect`のクラスとさまざまなサブクラスを通じて、これらの方言全体のバリエーションを処理します。
>
> ほとんどの場合、Hibernateは、ブートストラップ中にJDBC接続についていくつか質問することにより、使用する適切なダイアレクトを決定できます。使用する適切な方言を決定するHibernateの機能（およびその解像度に影響を与える能力）については、 [方言の解決](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#portability-dialectresolver)を参照してください。
>
> 何らかの理由で適切な方言を判別できない場合、またはカスタム方言を使用する場合は、 `hibernate.dialect`の設定を行う必要があります。
>
> *-Hibernateの公式ドキュメントからの抜粋： <a href="https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#database-dialect">データベース方言</a>*

構成後、プロジェクトは通常どおりに使用できますが、MySQLで使用するのと同じ方法、つまり**MySQL方言**を使用する場合に限ります。これは、 <strong>Hibernate</strong>が`6.0.0.Beta2`以降のバージョンで<strong>TiDBダイアレクト</strong>をサポートしているためですが、SpringDataJPAのHibernateへのデフォルトの依存関係は`5.6.4.Final`です。したがって、 `pom.xml`に次の変更を加えることをお勧めします。

1.  この[依存関係ファイル](https://github.com/pingcap-inc/tidb-example-java/blob/main/spring-jpa-hibernate/pom.xml#L26)に示すように、 `Spring Data JPA`で導入された`jakarta`のパッケージを除外します。

    依存関係ファイルを次の場所から変更します。

    {{< copyable "" >}}

    ```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    ```

    に：

    {{< copyable "" >}}

    ```xml
    <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.hibernate</groupId>
            <artifactId>hibernate-core-jakarta</artifactId>
        </exclusion>
    </exclusions>
    </dependency>
    ```

2.  この[依存関係ファイル](https://github.com/pingcap-inc/tidb-example-java/blob/main/spring-jpa-hibernate/pom.xml#L53)に示すように、 `6.0.0.Beta2`以降のバージョンから**Hibernate**の依存関係を導入します。

    {{< copyable "" >}}

    ```xml
    <dependency>
        <groupId>org.hibernate.orm</groupId>
        <artifactId>hibernate-core</artifactId>
        <version>6.0.0.CR2</version>
    </dependency>
    ```

    変更が行われると、サンプルアプリケーションと同じ依存関係を持つ空**のSpringBoot**アプリケーションを取得できます。

## ステップ5：アプリケーションを実行します {#step-5-run-the-application}

このステップでは、アプリケーションコードをコンパイルして実行し、Webアプリケーションを作成します。 Hibernateは`test`のデータベース内に`player_jpa`のテーブルを作成します。アプリケーションのRESTfulAPIを使用してリクエストを行う場合、これらのリクエストはTiDBクラスタで実行され[データベーストランザクション](/develop/dev-guide-transaction-overview.md) 。

このアプリケーションのコードについて詳しく知りたい場合は、 [実装の詳細](#implementation-details)を参照してください。

### ステップ5.1パラメータを変更する {#step-5-1-change-parameters}

非ローカルのデフォルトクラスタ、 TiDB Cloudクラスタ、またはリモートクラスタを使用する場合は、 `application.yml` （ `spring.datasource.password`にある）の`spring.datasource.url` `src/main/resources`を変更し`spring.datasource.username` 。

{{< copyable "" >}}

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:4000/test
    username: root
    #    password: xxx
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

パスワードを`123456`に設定すると、 TiDB Cloudで取得する接続文字列は次のようになります。

{{< copyable "" >}}

```shell
mysql --connect-timeout 15 -u root -h tidb.e049234d.d40d1f8b.us-east-1.prod.aws.tidbcloud.com -P 4000 -p
```

したがって、パラメータは次のように設定する必要があります。

{{< copyable "" >}}

```yaml
spring:
  datasource:
    url: jdbc:mysql://tidb.e049234d.d40d1f8b.us-east-1.prod.aws.tidbcloud.com:4000/test
    username: root
    password: 123456
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

### ステップ5.2実行 {#step-5-2-run}

ターミナルセッションを開き、 `spring-jpa-hibernate`ディレクトリにいることを確認します。まだこのディレクトリにいない場合は、次のコマンドを使用してディレクトリに移動します。

{{< copyable "" >}}

```shell
cd <path>/tidb-example-java/spring-jpa-hibernate
```

#### Makeでビルドして実行する（推奨） {#build-and-run-with-make-recommended}

{{< copyable "" >}}

```shell
make
```

#### 手動でビルドして実行 {#build-and-run-manually}

手動でビルドする場合は、次の手順に従います。

1.  キャッシュとパッケージをクリアします。

    {{< copyable "" >}}

    ```shell
    mvn clean package
    ```

2.  JARファイルを使用してアプリケーションを実行します。

    {{< copyable "" >}}

    ```shell
    java -jar target/spring-jpa-hibernate-0.0.1.jar
    ```

### ステップ5.3出力 {#step-5-3-output}

出力の最後の部分は次のようになります。

```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::             (v3.0.0-M1)

2022-03-28 18:46:01.429  INFO 14923 --- [           main] com.pingcap.App                          : Starting App v0.0.1 using Java 17.0.2 on CheesedeMacBook-Pro.local with PID 14923 (/path/code/tidb-example-java/spring-jpa-hibernate/target/spring-jpa-hibernate-0.0.1.jar started by cheese in /path/code/tidb-example-java/spring-jpa-hibernate)
2022-03-28 18:46:01.430  INFO 14923 --- [           main] com.pingcap.App                          : No active profile set, falling back to default profiles: default
2022-03-28 18:46:01.709  INFO 14923 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2022-03-28 18:46:01.733  INFO 14923 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 20 ms. Found 1 JPA repository interfaces.
2022-03-28 18:46:02.010  INFO 14923 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port(s): 8080 (http)
2022-03-28 18:46:02.016  INFO 14923 --- [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2022-03-28 18:46:02.016  INFO 14923 --- [           main] org.apache.catalina.core.StandardEngine  : Starting Servlet engine: [Apache Tomcat/10.0.16]
2022-03-28 18:46:02.050  INFO 14923 --- [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2022-03-28 18:46:02.051  INFO 14923 --- [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 598 ms
2022-03-28 18:46:02.143  INFO 14923 --- [           main] o.hibernate.jpa.internal.util.LogHelper  : HHH000204: Processing PersistenceUnitInfo [name: default]
2022-03-28 18:46:02.173  INFO 14923 --- [           main] org.hibernate.Version                    : HHH000412: Hibernate ORM core version 6.0.0.CR2
2022-03-28 18:46:02.262  WARN 14923 --- [           main] org.hibernate.orm.deprecation            : HHH90000021: Encountered deprecated setting [javax.persistence.sharedCache.mode], use [jakarta.persistence.sharedCache.mode] instead
2022-03-28 18:46:02.324  INFO 14923 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2022-03-28 18:46:02.415  INFO 14923 --- [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Added connection com.mysql.cj.jdbc.ConnectionImpl@2575f671
2022-03-28 18:46:02.416  INFO 14923 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
2022-03-28 18:46:02.443  INFO 14923 --- [           main] SQL dialect                              : HHH000400: Using dialect: org.hibernate.dialect.TiDBDialect
Hibernate: drop table if exists player_jpa
Hibernate: drop sequence player_jpa_id_seq
Hibernate: create sequence player_jpa_id_seq start with 1 increment by 1
Hibernate: create table player_jpa (id bigint not null, coins integer, goods integer, primary key (id)) engine=InnoDB
2022-03-28 18:46:02.883  INFO 14923 --- [           main] o.h.e.t.j.p.i.JtaPlatformInitiator       : HHH000490: Using JtaPlatform implementation: [org.hibernate.engine.transaction.jta.platform.internal.NoJtaPlatform]
2022-03-28 18:46:02.888  INFO 14923 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2022-03-28 18:46:03.125  WARN 14923 --- [           main] org.hibernate.orm.deprecation            : HHH90000021: Encountered deprecated setting [javax.persistence.lock.timeout], use [jakarta.persistence.lock.timeout] instead
2022-03-28 18:46:03.132  WARN 14923 --- [           main] org.hibernate.orm.deprecation            : HHH90000021: Encountered deprecated setting [javax.persistence.lock.timeout], use [jakarta.persistence.lock.timeout] instead
2022-03-28 18:46:03.168  WARN 14923 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2022-03-28 18:46:03.307  INFO 14923 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2022-03-28 18:46:03.311  INFO 14923 --- [           main] com.pingcap.App                          : Started App in 2.072 seconds (JVM running for 2.272)
```

出力ログは、起動時のアプリケーションの動作を示します。この例では、アプリケーションは[Tomcat](https://tomcat.apache.org/)を使用して**サーブレット**を起動し、ORMとしてHibernateを使用し、データベース接続プールの実装として[HikariCP](https://github.com/brettwooldridge/HikariCP)を使用し、データベースダイアレクトとして`org.hibernate.dialect.TiDBDialect`を使用します。起動後、Hibernateは`player_jpa`テーブルと`player_jpa_id_seq`シーケンスを削除して再作成します。起動の最後に、アプリケーションはポート`8080`でリッスンして、外部にHTTPサービスを提供します。

このアプリケーションのコードについて詳しく知りたい場合は、 [実装の詳細](#implementation-details)を参照してください。

## ステップ6：HTTPリクエスト {#step-6-http-requests}

サービスが起動して実行されたら、HTTPリクエストをバックエンドアプリケーションに送信できます。 [http：// localhost：8080](http://localhost:8080)は、サービスを提供するベースURLです。このチュートリアルでは、一連のHTTPリクエストを使用して、サービスの使用方法を示します。

### ステップ6.1Postmanリクエストを使用する（推奨） {#step-6-1-use-postman-requests-recommended}

次に示すように、この[構成ファイル](https://raw.githubusercontent.com/pingcap-inc/tidb-example-java/main/spring-jpa-hibernate/Player.postman_collection.json)をローカルにダウンロードして、 [郵便配達員](https://www.postman.com/)にインポートできます。

![import the collection into Postman](/media/develop/IMG_20220402-003303222.png)

#### プレーヤーを作成する {#create-players}

[**作成**]タブと[<strong>送信</strong>]ボタンをクリックして、POSTリクエストを`http://localhost:8080/player/`に送信します。戻り値は、追加されたプレーヤーの数であり、1と予想されます。

![Postman-Create a player](/media/develop/IMG_20220402-003350731.png)

#### IDでプレーヤー情報を取得する {#get-player-information-by-id}

[ **GetByID** ]タブと[<strong>送信</strong>]ボタンをクリックして、GETリクエストを`http://localhost:8080/player/1`に送信します。戻り値は、 `1`のプレーヤーの情報です。

![Postman-GetByID](/media/develop/IMG_20220402-003416079.png)

#### 制限によってプレーヤー情報をまとめて取得する {#get-player-information-in-bulk-by-limit}

[ **GetByLimit** ]タブと[<strong>送信</strong>]ボタンをクリックして、GETリクエストを`http://localhost:8080/player/limit/3`に送信します。戻り値は、最大3人のプレーヤーの情報のリストです。

![Postman-GetByLimit](/media/develop/IMG_20220402-003505846.png)

#### ページごとにプレーヤー情報を取得する {#get-player-information-by-page}

[ **GetByPage** ]タブと[<strong>送信</strong>]ボタンをクリックして、GETリクエストを`http://localhost:8080/player/page?index=0&size=2`に送信します。戻り値は、インデックスが`0`のページで、1ページあたり`2`人のプレーヤーがいます。戻り値には、offset、totalPages、sortなどのページング情報も含まれます。

![Postman-GetByPage](/media/develop/IMG_20220402-003528474.png)

#### プレーヤーを数える {#count-players}

[**カウント**]タブと[<strong>送信</strong>]ボタンをクリックして、GETリクエストを`http://localhost:8080/player/count`に送信します。戻り値はプレーヤーの数です。

![Postman-Count](/media/develop/IMG_20220402-003549966.png)

#### プレイヤー取引 {#player-trading}

[**トレード**]タブと[<strong>送信</strong>]ボタンをクリックして、PUTリクエストを`http://localhost:8080/player/trade`に送信します。リクエストパラメータは、売り手のID `sellID` 、買い手のID `buyID` 、購入した商品の数`amount` 、購入のために消費されたコインの数`price`です。

戻り値は、トランザクションが成功したかどうかです。売り手にとって不十分な商品、買い手にとって不十分なコイン、またはデータベースエラーがある場合、 [データベーストランザクション](/develop/dev-guide-transaction-overview.md)は取引が成功せず、プレーヤーのコインや商品が失われないことを保証します。

![Postman-Trade](/media/develop/IMG_20220402-003659102.png)

### ステップ6.2curlリクエストの使用 {#step-6-2-using-curl-requests}

curlを使用して直接リクエストを行うこともできます。

#### プレーヤーを作成する {#create-players}

プレーヤーを作成するには、 **POST**リクエストを`/player`エンドポイントに送信できます。例えば：

{{< copyable "" >}}

```shell
curl --location --request POST 'http://localhost:8080/player/' --header 'Content-Type: application/json' --data-raw '[{"coins":100,"goods":20}]'
```

リクエストはペイロードとしてJSONを使用します。上記の例は、1001と`goods`でプレーヤーを作成することを示してい`coins` 。戻り値は、作成されたプレーヤーの数です。

```json
1
```

#### IDでプレーヤー情報を取得する {#get-player-information-by-id}

プレーヤー情報を取得するために、 **GET**リクエストを`/player`エンドポイントに送信できます。次のように、pathパラメーターでプレーヤーの`id`を指定する必要があります`/player/{id}` 。次の例は、91のプレーヤーの情報を取得する方法を示してい`id` 。

{{< copyable "" >}}

```shell
curl --location --request GET 'http://localhost:8080/player/1'
```

戻り値はプレーヤーの情報です。

```json
{
  "coins": 200,
  "goods": 10,
  "id": 1
}
```

#### 制限によってプレーヤー情報をまとめて取得する {#get-player-information-in-bulk-by-limit}

プレーヤー情報をまとめて取得するには、 **GET**リクエストを`/player/limit`エンドポイントに送信します。次のように、pathパラメーターでプレーヤーの総数を指定する必要があります`/player/limit/{limit}` 。次の例は、最大3人のプレーヤーの情報を取得する方法を示しています。

{{< copyable "" >}}

```shell
curl --location --request GET 'http://localhost:8080/player/limit/3'
```

戻り値は、プレーヤー情報のリストです。

```json
[
  {
    "coins": 200,
    "goods": 10,
    "id": 1
  },
  {
    "coins": 0,
    "goods": 30,
    "id": 2
  },
  {
    "coins": 100,
    "goods": 20,
    "id": 3
  }
]
```

#### ページごとにプレーヤー情報を取得する {#get-player-information-by-page}

ページ付けされたプレーヤー情報を取得するには、 `/player/page`エンドポイントに**GET**リクエストを送信できます。追加のパラメーターを指定するには、URLパラメーターを使用する必要があります。次の例は、 `index`が0で、各ページに最大`size`人のプレーヤーがいるページから情報を取得する方法を示しています。

{{< copyable "" >}}

```shell
curl --location --request GET 'http://localhost:8080/player/page?index=0&size=2'
```

戻り値は`index`のページで、ページごとに2人のプレーヤーがリストされます。さらに、戻り値には、オフセット、合計ページ数、結果がソートされているかどうかなどのページネーション情報が含まれています。

```json
{
  "content": [
    {
      "coins": 200,
      "goods": 10,
      "id": 1
    },
    {
      "coins": 0,
      "goods": 30,
      "id": 2
    }
  ],
  "empty": false,
  "first": true,
  "last": false,
  "number": 0,
  "numberOfElements": 2,
  "pageable": {
    "offset": 0,
    "pageNumber": 0,
    "pageSize": 2,
    "paged": true,
    "sort": {
      "empty": true,
      "sorted": false,
      "unsorted": true
    },
    "unpaged": false
  },
  "size": 2,
  "sort": {
    "empty": true,
    "sorted": false,
    "unsorted": true
  },
  "totalElements": 4,
  "totalPages": 2
}
```

#### プレーヤーを数える {#count-players}

プレーヤーの数を取得するには、 `/player/count`のエンドポイントに**GET**リクエストを送信できます。

{{< copyable "" >}}

```shell
curl --location --request GET 'http://localhost:8080/player/count'
```

戻り値はプレーヤーの数です。

```json
4
```

#### プレイヤー取引 {#player-trading}

プレーヤー間のトランザクションを開始するには、 `/player/trade`エンドポイントに**PUT**リクエストを送信できます。例えば：

{{< copyable "" >}}

```shell
curl --location --request PUT 'http://localhost:8080/player/trade' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'sellID=1' \
  --data-urlencode 'buyID=2' \
  --data-urlencode 'amount=10' \
  --data-urlencode 'price=100'
```

リクエストは、ペイロードとして**フォームデータ**を使用します。リクエストの例は、売り手のID（ `sellID` ）が1、買い手のID（ `buyID` ）が2、購入した商品の数（ `amount` ）が10、購入に消費されたコインの数（ `price` ）が100であることを示しています。

戻り値は、トランザクションが成功したかどうかです。売り手にとって不十分な商品、買い手にとって不十分なコイン、またはデータベースエラーがある場合、 [データベーストランザクション](/develop/dev-guide-transaction-overview.md)は取引が成功せず、プレーヤーのコインや商品が失われないことを保証します。

```json
true
```

### ステップ6.3シェルスクリプトを使用したリクエスト {#step-6-3-requests-with-shell-script}

テスト目的で[このシェルスクリプト](https://github.com/pingcap-inc/tidb-example-java/blob/main/spring-jpa-hibernate/request.sh)をダウンロードできます。スクリプトは次の操作を実行します。

1.  ループ内に10人のプレーヤーを作成します。
2.  `id`の1でプレイヤーの情報を取得します。
3.  最大3人のプレーヤーのリストを取得します。
4.  1of0と`index`のプレーヤーのページを取得し`size` 。
5.  プレーヤーの総数を取得します。
6.  `id` of 1のプレーヤーが売り手で、 `id` of 2のプレーヤーが買い手であり、105が`coins`のコストで購入されるトランザクションを実行し`goods` 。

このスクリプトは、 `make request`または`./request.sh`で実行できます。結果は次のようになります。

```shell
cheese@CheesedeMacBook-Pro spring-jpa-hibernate % make request
./request.sh
loop to create 10 players:
1111111111

get player 1:
{"id":1,"coins":200,"goods":10}

get players by limit 3:
[{"id":1,"coins":200,"goods":10},{"id":2,"coins":0,"goods":30},{"id":3,"coins":100,"goods":20}]

get first players:
{"content":[{"id":1,"coins":200,"goods":10},{"id":2,"coins":0,"goods":30}],"pageable":{"sort":{"empty":true,"unsorted":true,"sorted":false},"offset":0,"pageNumber":0,"pageSize":2,"paged":true,"unpaged":false},"last":false,"totalPages":7,"totalElements":14,"first":true,"size":2,"number":0,"sort":{"empty":true,"unsorted":true,"sorted":false},"numberOfElements":2,"empty":false}

get players count:
14

trade by two players:
false
```

## 実装の詳細 {#implementation-details}

このサブセクションでは、サンプルアプリケーションプロジェクトのコンポーネントについて説明します。

### 概要 {#overview}

このサンプルプロジェクトのカタログツリーを以下に示します（理解できない部分がいくつか削除されています）。

```
.
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── pingcap
        │           ├── App.java
        │           ├── controller
        │           │   └── PlayerController.java
        │           ├── dao
        │           │   ├── PlayerBean.java
        │           │   └── PlayerRepository.java
        │           └── service
        │               ├── PlayerService.java
        │               └── impl
        │                   └── PlayerServiceImpl.java
        └── resources
            └── application.yml
```

-   `pom.xml`は、依存関係やパッケージ化など、プロジェクトのMaven構成を宣言します。
-   `application.yml`は、使用されるデータベースアドレス、パスワード、データベースダイアレクトなどのプロジェクトのユーザー構成を宣言します。
-   `App.java`はプロジェクトのエントリポイントです。
-   `controller`は、HTTPインターフェースを外部に公開するパッケージです。
-   `service`は、プロジェクトのインターフェイスとロジックを実装するパッケージです。
-   `dao`は、データベースへの接続とデータの永続性を実装するパッケージです。

### Configuration / コンフィグレーション {#configuration}

このパートでは、 `pom.xml`ファイルのMaven構成と`application.yml`ファイルのユーザー構成について簡単に説明します。

#### Maven構成 {#maven-configuration}

`pom.xml`ファイルは、プロジェクトのMaven依存関係、パッケージ化メソッド、およびパッケージ化情報を宣言するMaven構成ファイルです。この構成ファイルを生成するプロセスを[同じ依存関係を持つ空のアプリケーションを作成する](#create-a-blank-application-with-the-same-dependency-optional)で複製するか、プロジェクトに直接コピーすることができます。

{{< copyable "" >}}

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
   <modelVersion>4.0.0</modelVersion>
   <parent>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-parent</artifactId>
      <version>3.0.0-M1</version>
      <relativePath/> <!-- lookup parent from repository -->
   </parent>

   <groupId>com.pingcap</groupId>
   <artifactId>spring-jpa-hibernate</artifactId>
   <version>0.0.1</version>
   <name>spring-jpa-hibernate</name>
   <description>an example for spring boot, jpa, hibernate and TiDB</description>

   <properties>
      <java.version>17</java.version>
      <maven.compiler.source>17</maven.compiler.source>
      <maven.compiler.target>17</maven.compiler.target>
   </properties>

   <dependencies>
      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-data-jpa</artifactId>
         <exclusions>
            <exclusion>
               <groupId>org.hibernate</groupId>
               <artifactId>hibernate-core-jakarta</artifactId>
            </exclusion>
         </exclusions>
      </dependency>

      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-web</artifactId>
      </dependency>

      <dependency>
         <groupId>mysql</groupId>
         <artifactId>mysql-connector-java</artifactId>
         <scope>runtime</scope>
      </dependency>

      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-test</artifactId>
         <scope>test</scope>
      </dependency>

      <dependency>
         <groupId>org.hibernate.orm</groupId>
         <artifactId>hibernate-core</artifactId>
         <version>6.0.0.CR2</version>
      </dependency>
   </dependencies>

   <build>
      <plugins>
         <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
         </plugin>
      </plugins>
   </build>

   <repositories>
      <repository>
         <id>spring-milestones</id>
         <name>Spring Milestones</name>
         <url>https://repo.spring.io/milestone</url>
         <snapshots>
            <enabled>false</enabled>
         </snapshots>
      </repository>
   </repositories>
   <pluginRepositories>
      <pluginRepository>
         <id>spring-milestones</id>
         <name>Spring Milestones</name>
         <url>https://repo.spring.io/milestone</url>
         <snapshots>
            <enabled>false</enabled>
         </snapshots>
      </pluginRepository>
   </pluginRepositories>
</project>
```

#### ユーザー構成 {#user-configuration}

`application.yml`構成ファイルは、データベースアドレス、パスワード、使用されるデータベースダイアレクトなどのユーザー構成を宣言します。

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:4000/test
    username: root
    #    password: xxx
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

構成は[YAML](https://yaml.org/)で記述されます。フィールドは次のように説明されています。

-   `spring.datasource.url` ：データベース接続のURL。
-   `spring.datasource.username` ：データベースのユーザー名。
-   `spring.datasource.password` ：データベースのパスワード。空の。このフィールドをコメントアウトまたは削除する必要があります。
-   `spring.datasource.driver-class-name` ：データベースドライバー。 TiDBはMySQLと互換性があるため、mysql-connector-javaドライバークラス`com.mysql.cj.jdbc`を使用します。
-   `jpa.show-sql` ：このフィールドが`true`に設定されている場合、JPAによって実行されるSQLステートメントが出力されます。
-   `jpa.database-platform` ：選択されたデータベースダイアレクト。アプリケーションはTiDBに接続するため、 **TiDB方言**を選択します。この方言は`6.0.0.Beta2`以降のバージョンでのみ使用可能であるため、該当する依存関係のバージョンを選択してください。
-   `jpa.hibernate.ddl-auto` ： `create-drop`は、プログラムの開始時にテーブルを作成し、終了時にテーブルを削除します。実稼働環境ではこのオプションを設定しないでください。これはサンプルアプリケーションであるため、このオプションはデータベースデータへの影響を最小限に抑えるために設定されています。

### エントリーポイント {#entry-point}

`App.java`のファイルがエントリポイントです。

{{< copyable "" >}}

```java
package com.pingcap;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.ApplicationPidFileWriter;

@SpringBootApplication
public class App {
   public static void main(String[] args) {
      SpringApplication springApplication = new SpringApplication(App.class);
      springApplication.addListeners(new ApplicationPidFileWriter("spring-jpa-hibernate.pid"));
      springApplication.run(args);
   }
}
```

エントリクラスは、SpringBootアプリケーションの標準構成アノテーション[`@SpringBootApplication`](https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/SpringBootApplication.html)で始まります。詳細については、SpringBootの公式ドキュメントの[`@SpringBootApplication`アノテーションの使用](https://docs.spring.io/spring-boot/docs/current/reference/html/using-spring-boot.html#using-boot-using-springbootapplication-annotation)を参照してください。次に、プログラムは`ApplicationPidFileWriter`を使用して、アプリケーションの起動時に`spring-jpa-hibernate.pid`という名前のPID（プロセス識別番号）ファイルを書き込みます。 PIDファイルを使用して、外部ソースからこのアプリケーションを閉じることができます。

### データアクセスオブジェクト {#data-access-object}

`dao` （データアクセスオブジェクト）パッケージは、データオブジェクトの永続性を実装します。

#### エンティティオブジェクト {#entity-objects}

`PlayerBean.java`ファイルはエンティティオブジェクトであり、データベース内のテーブルに対応します。

{{< copyable "" >}}

```java
package com.pingcap.dao;

import jakarta.persistence.*;

/**
 * it's core entity in hibernate
 * @Table appoint to table name
 */
@Entity
@Table(name = "player_jpa")
public class PlayerBean {
    /**
     * @ID primary key
     * @GeneratedValue generated way. this field will use generator named "player_id"
     * @SequenceGenerator using `sequence` feature to create a generator,
     *    and it named "player_jpa_id_seq" in database, initial form 1 (by `initialValue`
     *    parameter default), and every operator will increase 1 (by `allocationSize`)
     */
    @Id
    @GeneratedValue(generator="player_id")
    @SequenceGenerator(name="player_id", sequenceName="player_jpa_id_seq", allocationSize=1)
    private Long id;

    /**
     * @Column field
     */
    @Column(name = "coins")
    private Integer coins;
    @Column(name = "goods")
    private Integer goods;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Integer getCoins() {
        return coins;
    }

    public void setCoins(Integer coins) {
        this.coins = coins;
    }

    public Integer getGoods() {
        return goods;
    }

    public void setGoods(Integer goods) {
        this.goods = goods;
    }
}
```

エンティティクラスには、エンティティクラスをテーブルにバインドするためのHibernateの追加情報を提供するいくつかのアノテーションがあります。

-   `@Entity`は、 `PlayerBean`がエンティティクラスであることを宣言します。
-   `@Table`は、注釈属性`name`を使用して、このエンティティクラスを`player_jpa`テーブルに関連付けます。
-   `@Id`は、このプロパティがテーブルの主キー列に関連していることを宣言します。
-   `@GeneratedValue`は、この列の値が自動的に生成され、手動で設定しないことを示します。属性`generator`は、ジェネレーターの名前を`player_id`として指定するために使用されます。
-   `@SequenceGenerator`は、 [順序](/sql-statements/sql-statement-create-sequence.md)を使用するジェネレーターを宣言し、アノテーション属性`name`を使用してジェネレーターの名前を`player_id`として宣言します（ `@GeneratedValue`で指定された名前と一致します）。アノテーション属性`sequenceName`は、データベース内のシーケンスの名前を指定するために使用されます。最後に、注釈属性`allocationSize`を使用して、シーケンスのステップサイズを1として宣言します。
-   `@Column`は、各プライベート属性を`player_jpa`テーブルの列として宣言し、注釈属性`name`を使用して、属性に対応する列の名前を決定します。

#### リポジトリ {#repository}

データベース層を抽象化するために、Springアプリケーションは[`Repository`](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories)インターフェース、または`Repository`のサブインターフェースを使用します。このインターフェイスは、テーブルなどのデータベースオブジェクトにマップされます。 JPAは、primayキーを使用して、 [`INSERT`](/sql-statements/sql-statement-insert.md)や[`SELECT`](/sql-statements/sql-statement-select.md)などのいくつかのビルド済みメソッドを実装します。

{{< copyable "" >}}

```java
package com.pingcap.dao;

import jakarta.persistence.LockModeType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PlayerRepository extends JpaRepository<PlayerBean, Long> {
    /**
     * use HQL to query by page
     * @param pageable a pageable parameter required by hibernate
     * @return player list package by page message
     */
    @Query(value = "SELECT player_jpa FROM PlayerBean player_jpa")
    Page<PlayerBean> getPlayersByPage(Pageable pageable);

    /**
     * use SQL to query by limit, using named parameter
     * @param limit sql parameter
     * @return player list (max size by limit)
     */
    @Query(value = "SELECT * FROM player_jpa LIMIT :limit", nativeQuery = true)
    List<PlayerBean> getPlayersByLimit(@Param("limit") Integer limit);

    /**
     * query player and add a lock for update
     * @param id player id
     * @return player
     */
    @Lock(value = LockModeType.PESSIMISTIC_WRITE)
    @Query(value = "SELECT player FROM PlayerBean player WHERE player.id = :id")
    // @Query(value = "SELECT * FROM player_jpa WHERE id = :id FOR UPDATE", nativeQuery = true)
    PlayerBean getPlayerAndLock(@Param("id") Long id);
}
```

`PlayerRepository`インターフェースは、SpringがJPAデータアクセスに使用する`JpaRepository`インターフェースを拡張します。 `@Query`アノテーションは、このインターフェースでクエリを実装する方法をHibernateに指示するために使用されます。 2つのクエリ構文が使用されます。

-   `getPlayersByPage`インターフェースでは、 [Hibernateクエリ言語](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#hql) （HQL）が使用されます。
-   `getPlayersByLimit`インターフェースでは、ネイティブSQLが使用されます。インターフェイスがネイティブSQL構文を使用する場合、 `@Query`注釈パラメータ`nativeQuery`を`true`に設定する必要があります。

`getPlayersByLimit`アノテーションのSQLでは、Hibernateでは`:limit`は[名前付きパラメーター](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#jpql-query-parameters)と呼ばれます。 Hibernateは、アノテーションが存在するインターフェース内でパラメーターを名前で自動的に検出してスプライスします。 `@Param`を使用して、インジェクションのパラメーターとは異なる名前を指定することもできます。

`getPlayerAndLock`では、注釈[`@Lock`](https://docs.spring.io/spring-data/jpa/docs/current/api/org/springframework/data/jpa/repository/Lock.html)を使用して、悲観的ロックが適用されていることを宣言します。その他のロック方法の詳細については、 [エンティティのロック](https://openjpa.apache.org/builds/2.2.2/apache-openjpa/docs/jpa_overview_em_locking.html)を参照してください。 `@Lock`アノテーションは`HQL`とともに使用する必要があります。そうしないと、エラーが発生します。ロックにSQLを直接使用する場合は、コメントの注釈を使用できます。

{{< copyable "" >}}

```java
@Query(value = "SELECT * FROM player_jpa WHERE id = :id FOR UPDATE", nativeQuery = true)
```

上記のSQLステートメントは、 `FOR UPDATE`を使用してロックを直接追加します。 TiDB [`SELECT`ステートメント](/sql-statements/sql-statement-select.md)を使用して、原則をさらに深く掘り下げることもできます。

### ロジックの実装 {#logic-implementation}

ロジック実装レイヤーは`service`のパッケージであり、プロジェクトによって実装されたインターフェイスとロジックが含まれています。

#### インターフェース {#interface}

`PlayerService.java`ファイルは、論理インターフェースを定義し、クラスを直接記述するのではなく、インターフェースを実装します。これは、例を可能な限り実際の使用に近づけ、設計の[オープンクローズ原則](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle)を反映するためです。このインターフェースを省略して、実装クラスを依存関係クラスに直接挿入することもできますが、このアプローチはお勧めしません。

{{< copyable "" >}}

```java
package com.pingcap.service;

import com.pingcap.dao.PlayerBean;
import org.springframework.data.domain.Page;

import java.util.List;

public interface PlayerService {
    /**
     * create players by passing in a List of PlayerBean
     *
     * @param players will create players list
     * @return The number of create accounts
     */
    Integer createPlayers(List<PlayerBean> players);

    /**
     * buy goods and transfer funds between one player and another in one transaction
     * @param sellId sell player id
     * @param buyId buy player id
     * @param amount goods amount, if sell player has not enough goods, the trade will break
     * @param price price should pay, if buy player has not enough coins, the trade will break
     */
    void buyGoods(Long sellId, Long buyId, Integer amount, Integer price) throws RuntimeException;

    /**
     * get the player info by id.
     *
     * @param id player id
     * @return the player of this id
     */
    PlayerBean getPlayerByID(Long id);

    /**
     * get a subset of players from the data store by limit.
     *
     * @param limit return max size
     * @return player list
     */
    List<PlayerBean> getPlayers(Integer limit);

    /**
     * get a page of players from the data store.
     *
     * @param index page index
     * @param size page size
     * @return player list
     */
    Page<PlayerBean> getPlayersByPage(Integer index, Integer size);

    /**
     * count players from the data store.
     *
     * @return all players count
     */
    Long countPlayers();
}
```

#### 実装（重要） {#implementation-important}

`PlayerService.java`ファイルは、すべてのデータ処理ロジックを含む`PlayerService`インターフェイスを実装します。

{{< copyable "" >}}

```java
package com.pingcap.service.impl;

import com.pingcap.dao.PlayerBean;
import com.pingcap.dao.PlayerRepository;
import com.pingcap.service.PlayerService;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * PlayerServiceImpl implements PlayerService interface
 * @Transactional it means every method in this class, will package by a pair of
 *     transaction.begin() and transaction.commit(). and it will be call
 *     transaction.rollback() when method throw an exception
 */
@Service
@Transactional
public class PlayerServiceImpl implements PlayerService {
    @Autowired
    private PlayerRepository playerRepository;

    @Override
    public Integer createPlayers(List<PlayerBean> players) {
        return playerRepository.saveAll(players).size();
    }

    @Override
    public void buyGoods(Long sellId, Long buyId, Integer amount, Integer price) throws RuntimeException {
        PlayerBean buyPlayer = playerRepository.getPlayerAndLock(buyId);
        PlayerBean sellPlayer = playerRepository.getPlayerAndLock(sellId);
        if (buyPlayer == null || sellPlayer == null) {
            throw new RuntimeException("sell or buy player not exist");
        }

        if (buyPlayer.getCoins() < price || sellPlayer.getGoods() < amount) {
            throw new RuntimeException("coins or goods not enough, rollback");
        }

        buyPlayer.setGoods(buyPlayer.getGoods() + amount);
        buyPlayer.setCoins(buyPlayer.getCoins() - price);
        playerRepository.save(buyPlayer);

        sellPlayer.setGoods(sellPlayer.getGoods() - amount);
        sellPlayer.setCoins(sellPlayer.getCoins() + price);
        playerRepository.save(sellPlayer);
    }

    @Override
    public PlayerBean getPlayerByID(Long id) {
        return playerRepository.findById(id).orElse(null);
    }

    @Override
    public List<PlayerBean> getPlayers(Integer limit) {
        return playerRepository.getPlayersByLimit(limit);
    }

    @Override
    public Page<PlayerBean> getPlayersByPage(Integer index, Integer size) {
        return playerRepository.getPlayersByPage(PageRequest.of(index, size));
    }

    @Override
    public Long countPlayers() {
        return playerRepository.count();
    }
}
```

`@Service`アノテーションは、このオブジェクトのライフサイクルが`Spring`によって管理されていることを宣言するために使用されます。

`PlayerServiceImpl`の実装クラスには、 `@Service`つのアノテーションに加えて[`@Transactional`](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#transaction-declarative-annotations)のアノテーションもあります。アプリケーションでトランザクション管理が有効になっている場合（ [`@EnableTransactionManagement`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/EnableTransactionManagement.html)を使用してオンにできますが、デフォルトでは`Spring Boot`でオンになっています。手動で構成する必要はありません）、 `Spring`は、プロキシ内の`@Transactional`アノテーションを持つすべてのオブジェクトを自動的にラップします。このプロキシをオブジェクト呼び出し処理に使用します。

エージェントが`@Transactional`のアノテーションを持つオブジェクト内の関数を呼び出すとき、次のように単純に想定できます。

-   関数の先頭で、 `transaction.begin()`からトランザクションを開始します。
-   関数が戻ると、 `transaction.commit()`を呼び出してトランザクションをコミットします。
-   ランタイムエラーが発生すると、エージェントは`transaction.rollback()`を呼び出してロールバックします。

トランザクションの詳細については[データベーストランザクション](/develop/dev-guide-transaction-overview.md)を参照するか、 `Spring`のWebサイトで[SpringFrameworkの宣言型トランザクションの実装を理解する](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#tx-decl-explained)を参照してください。

すべての実装クラスで、 `buyGoods`の関数に注意が必要です。関数が非論理的な操作に遭遇すると、例外をスローし、不正なデータを防ぐためにトランザクションロールバックを実行するようにHibernateに指示します。

### 外部HTTPインターフェース {#external-http-interface}

`controller`パッケージは、HTTPインターフェースを外部に公開し、 [REST API](https://www.redhat.com/en/topics/api/what-is-a-rest-api#)を介してサービスにアクセスできるようにします。

{{< copyable "" >}}

```java
package com.pingcap.controller;

import com.pingcap.dao.PlayerBean;
import com.pingcap.service.PlayerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.lang.NonNull;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/player")
public class PlayerController {
    @Autowired
    private PlayerService playerService;

    @PostMapping
    public Integer createPlayer(@RequestBody @NonNull List<PlayerBean> playerList) {
        return playerService.createPlayers(playerList);
    }

    @GetMapping("/{id}")
    public PlayerBean getPlayerByID(@PathVariable Long id) {
        return playerService.getPlayerByID(id);
    }

    @GetMapping("/limit/{limit_size}")
    public List<PlayerBean> getPlayerByLimit(@PathVariable("limit_size") Integer limit) {
        return playerService.getPlayers(limit);
    }

    @GetMapping("/page")
    public Page<PlayerBean> getPlayerByPage(@RequestParam Integer index, @RequestParam("size") Integer size) {
        return playerService.getPlayersByPage(index, size);
    }

    @GetMapping("/count")
    public Long getPlayersCount() {
        return playerService.countPlayers();
    }

    @PutMapping("/trade")
    public Boolean trade(@RequestParam Long sellID, @RequestParam Long buyID, @RequestParam Integer amount, @RequestParam Integer price) {
        try {
            playerService.buyGoods(sellID, buyID, amount, price);
        } catch (RuntimeException e) {
            return false;
        }

        return true;
    }
}
```

`PlayerController`は、機能を示すために可能な限り多くの注釈を使用します。実際のプロジェクトでは、会社またはチームのルールに従いながら、スタイルの一貫性を保ちます。 `PlayerController`の注釈は次のように説明されています。

-   [`@RestController`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RestController.html)は`PlayerController`を[Webコントローラー](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)として宣言し、戻り値を`JSON`出力としてシリアル化します。
-   [`@RequestMapping`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RequestMapping.html)はURLエンドポイントを`/player`にマップします。つまり、この`Web Controller`は`/player`のURLに送信されたリクエストのみをリッスンします。
-   `@Autowired`は、 `Spring`のコンテナーがコラボレーションBean間の関係を自動配線できることを意味します。宣言には`PlayerService`オブジェクトが必要です。これはインターフェイスであり、使用する実装クラスを指定しません。これはSpringによって組み立てられます。このアセンブリのルールについては、Springの公式Webサイトの[IoCコンテナ](https://docs.spring.io/spring-framework/docs/3.2.x/spring-framework-reference/html/beans.html)を参照してください。
-   [`@PostMapping`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PostMapping.html)は、この関数がHTTPの[役職](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST)要求に応答することを宣言します。
    -   `@RequestBody`は、HTTPペイロード全体が`playerList`パラメーターに解析されることを宣言します。
    -   `@NonNull`は、パラメーターがnullであってはならないことを宣言します。それ以外の場合は、エラーを返します。
-   [`@GetMapping`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/GetMapping.html)は、この関数がHTTPの[得る](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET)要求に応答することを宣言します。
    -   [`@PathVariable`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PathVariable.html)は、注釈に`{id}`や`{limit_size}`のようなプレースホルダーがあり、 `@PathVariable`で注釈が付けられた変数にバインドされていることを示します。このようなバインディングは、アノテーション属性`name`に基づいています。注釈属性`name`が指定されていない場合は、変数名と同じです。変数名は省略できます。つまり、 `@PathVariable(name="limit_size")`は`@PathVariable("limit_size")`と書くことができます。
-   [`@PutMapping`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PutMapping.html)は、この関数がHTTPの[置く](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT)要求に応答することを宣言します。
-   [`@RequestParam`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RequestParam.html)は、この関数がリクエスト内のURLパラメーター、フォームパラメーター、およびその他のパラメーターを解析し、それらを注釈付き変数にバインドすることを宣言します。
