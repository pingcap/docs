---
title: Choose Driver or ORM
summary: Learn how to choose a driver or ORM framework to connect to TiDB.
---

# Driverまたは ORM を選択してください {#choose-driver-or-orm}

> **注記：**
>
> TiDB は、ドライバーと ORM に対して次の 2 つのサポート レベルを提供します。
>
> -   **Full** : TiDB がツールのほとんどの機能と互換性があり、新しいバージョンとの互換性が維持されていることを示します。 PingCAP は、最新バージョン[TiDB がサポートするサードパーティ ツール](/develop/dev-guide-third-party-support.md)との互換性テストを定期的に実施します。
> -   **互換性**: 対応するサードパーティ ツールが MySQL に適合しており、TiDB が MySQL プロトコルと高い互換性があるため、TiDB はツールのほとんどの機能を使用できることを示します。ただし、PingCAP はツールのすべての機能について完全なテストを完了していないため、予期しない動作が発生する可能性があります。
>
> 詳細については、 [TiDB がサポートするサードパーティ ツール](/develop/dev-guide-third-party-support.md)を参照してください。

TiDB は MySQL プロトコルと高い互換性がありますが、一部の機能は MySQL と互換性がありません。互換性の違いの完全なリストについては、 [MySQL の互換性](/mysql-compatibility.md)を参照してください。

## Java {#java}

このセクションでは、 Javaでドライバーと ORM フレームワークを使用する方法について説明します。

### Javaドライバー {#java-drivers}

<SimpleTab>
<div label="MySQL-JDBC">

サポートレベル:**フル**

[MySQL ドキュメント](https://dev.mysql.com/doc/connector-j/8.0/en/)に従って、 Java JDBC ドライバーをダウンロードして構成できます。 TiDB v6.3.0 以降では MySQL Connector/J 8.0.33 以降を使用することをお勧めします。

> **ヒント：**
>
> 8.0.32 より前の Connector/J 8.0 バージョンには[バグ](https://bugs.mysql.com/bug.php?id=106252)あり、v6.3.0 より前の TiDB バージョンを使用するとスレッドがハングする可能性があります。この問題を回避するには、MySQL Connector/J 8.0.32 以降のバージョン、または TiDB JDBC ( *「TiDB-JDBC」*タブを参照) を使用することをお勧めします。

完全なアプリケーションを構築する方法の例については、 [TiDB と JDBC を使用してシンプルな CRUD アプリを構築する](/develop/dev-guide-sample-application-java-jdbc.md)を参照してください。

</div>
<div label="TiDB-JDBC">

サポートレベル:**フル**

[TiDB-JDBC](https://github.com/pingcap/mysql-connector-j) MySQL 8.0.29 に基づいてカスタマイズされたJavaドライバーです。 MySQL 正式バージョン 8.0.29 に基づいてコンパイルされた TiDB-JDBC は、オリジナルの JDBC の準備モードにおけるマルチパラメータおよびマルチフィールド EOF のバグを修正し、自動 TiCDC スナップショット メンテナンスや SM3 認証プラグインなどの機能を追加します。

SM3 に基づく認証は、TiDB の TiDB-JDBC でのみサポートされています。

Maven を使用する場合は、次の内容を`pom.xml`ファイルの`<dependencies></dependencies>`セクションに追加します。

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
```

SM3 認証を有効にする必要がある場合は、 `pom.xml`ファイルの`<dependencies></dependencies>`セクションに次の内容を追加します。

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcprov-jdk15on</artifactId>
    <version>1.67</version>
</dependency>
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcpkix-jdk15on</artifactId>
    <version>1.67</version>
</dependency>
```

Gradle を使用する場合は、次の内容を`dependencies`に追加します。

```gradle
implementation group: 'io.github.lastincisor', name: 'mysql-connector-java', version: '8.0.29-tidb-1.0.0'
implementation group: 'org.bouncycastle', name: 'bcprov-jdk15on', version: '1.67'
implementation group: 'org.bouncycastle', name: 'bcpkix-jdk15on', version: '1.67'
```

</div>
</SimpleTab>

### Java ORM フレームワーク {#java-orm-frameworks}

> **注記：**
>
> -   現在、Hibernate は[ネストされたトランザクションはサポートされていません](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres)を実行します。
>
> -   v6.2.0 以降、TiDB は[セーブポイント](/sql-statements/sql-statement-savepoint.md)をサポートします。 `@Transactional`で`Propagation.NESTED`トランザクション伝播オプションを使用するには、つまり`@Transactional(propagation = Propagation.NESTED)`を設定するには、TiDB が v6.2.0 以降であることを確認してください。

<SimpleTab>
<div label="Hibernate">

サポートレベル:**フル**

アプリケーションのさまざまな依存関係間の複雑な関係を手動で管理することを避けるために、 [グラドル](https://gradle.org/install)または[メイビン](https://maven.apache.org/install.html)を使用して、間接的な依存関係を含むアプリケーションのすべての依存関係を取得できます。 Hibernate `6.0.0.Beta2`以降のみが TiDB ダイアレクトをサポートしていることに注意してください。

**Maven を**使用している場合は、以下を`<dependencies></dependencies>`に追加します。

```xml
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>6.0.0.CR2</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.49</version>
</dependency>
```

**Gradle を**使用している場合は、次を`dependencies`に追加します。

```gradle
implementation 'org.hibernate:hibernate-core:6.0.0.CR2'
implementation 'mysql:mysql-connector-java:5.1.49'
```

-   Hibernate を使用してネイティブJavaによって TiDB アプリケーションを構築する例については、 [TiDB と Hibernate を使用してシンプルな CRUD アプリを構築する](/develop/dev-guide-sample-application-java-hibernate.md)を参照してください。
-   Spring Data JPA または Hibernate を使用して Spring で TiDB アプリケーションを構築する例については、 [Spring Boot を使用して TiDB アプリを構築する](/develop/dev-guide-sample-application-java-spring-boot.md)を参照してください。

さらに、 TiDB ダイアレクトを[Hibernate 構成ファイル](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm) : `org.hibernate.dialect.TiDBDialect`で指定する必要があります。これは Hibernate `6.0.0.Beta2`以降でのみサポートされます。 `Hibernate`バージョンが`6.0.0.Beta2`より前の場合は、まずそれをアップグレードしてください。

> **注記：**
>
> バージョン`Hibernate`をアップグレードできない場合は、代わりにMySQL 5.7ダイアレクト`org.hibernate.dialect.MySQL57Dialect`を使用してください。ただし、この設定により、予期しない結果が発生したり、 TiDB 固有の機能 ( [シーケンス](/sql-statements/sql-statement-create-sequence.md)など) が欠如したりする可能性があります。

</div>

<div label="MyBatis">

サポートレベル:**フル**

アプリケーションのさまざまな依存関係間の複雑な関係を手動で管理することを避けるために、 [グラドル](https://gradle.org/install)または[メイビン](https://maven.apache.org/install.html)を使用して、間接的な依存関係を含むアプリケーションのすべての依存関係を取得できます。

Maven を使用している場合は、次の行を`<dependencies></dependencies>`に追加します。

```xml
<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis</artifactId>
    <version>3.5.9</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.49</version>
</dependency>
```

Gradle を使用している場合は、次の行を`dependencies`に追加します。

```gradle
implementation 'org.mybatis:mybatis:3.5.9'
implementation 'mysql:mysql-connector-java:5.1.49'
```

MyBatis を使用して TiDB アプリケーションを構築する例については、 [TiDB と MyBatis を使用してシンプルな CRUD アプリを構築する](/develop/dev-guide-sample-application-java-mybatis.md)を参照してください。

</div>

</SimpleTab>

### Javaクライアントのロード バランシング {#java-client-load-balancing}

**tidb-ロードバランス**

サポートレベル:**フル**

[tidb-ロードバランス](https://github.com/pingcap/tidb-loadbalance)はアプリケーション側の負荷分散コンポーネントです。 tidb-loadbalance を使用すると、TiDBサーバーのノード情報を自動的に維持し、tidb-loadbalance ポリシーを使用してクライアント上で JDBC 接続を分散できます。クライアント アプリケーションと TiDBサーバーの間で直接 JDBC 接続を使用すると、負荷分散コンポーネントを使用するよりも高いパフォーマンスが得られます。

現在、 tidb-loadbalance は、ラウンドロビン、ランダム、および重みのポリシーをサポートしています。

> **注記：**
>
> tidb-loadbalance は[mysql-コネクタ-j](https://github.com/pingcap/mysql-connector-j)とともに使用する必要があります。

Maven を使用する場合は、 `pom.xml`ファイルの`<dependencies></dependencies>`の要素本体に次の内容を追加します。

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>tidb-loadbalance</artifactId>
  <version>0.0.5</version>
</dependency>
```

Gradle を使用する場合は、次の内容を`dependencies`に追加します。

```gradle
implementation group: 'io.github.lastincisor', name: 'mysql-connector-java', version: '8.0.29-tidb-1.0.0'
implementation group: 'io.github.lastincisor', name: 'tidb-loadbalance', version: '0.0.5'
```

## Golang {#golang}

このセクションでは、 Golangでドライバーと ORM フレームワークを使用する方法について説明します。

### Golangドライバー {#golang-drivers}

**go-sql-ドライバー/mysql**

サポートレベル:**フル**

Golangドライバーをダウンロードして構成するには、 [go-sql-driver/mysql ドキュメント](https://github.com/go-sql-driver/mysql)を参照してください。

完全なアプリケーションを構築する方法の例については、 [Go-MySQL-Driver を使用して TiDB に接続する](/develop/dev-guide-sample-application-golang-sql-driver.md)を参照してください。

### Golang ORM フレームワーク {#golang-orm-frameworks}

**ゴーム**

サポートレベル:**フル**

GORM は、 Golangの人気のある ORM フレームワークです。アプリケーション内のすべての依存関係を取得するには、 `go get`コマンドを使用できます。

```shell
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```

GORM を使用して TiDB アプリケーションを構築する例については、 [GORM を使用して TiDB に接続する](/develop/dev-guide-sample-application-golang-gorm.md)を参照してください。

## パイソン {#python}

このセクションでは、Python でドライバーと ORM フレームワークを使用する方法について説明します。

### Python ドライバー {#python-drivers}

<SimpleTab>
<div label="PyMySQL">

サポートレベル:**互換性あり**

[PyMySQL ドキュメント](https://pypi.org/project/PyMySQL/)に従ってドライバーをダウンロードして設定できます。 PyMySQL 1.0.2 以降のバージョンを使用することをお勧めします。

PyMySQL を使用して TiDB アプリケーションを構築する例については、 [PyMySQL を使用して TiDB に接続する](/develop/dev-guide-sample-application-python-pymysql.md)を参照してください。

</div>
<div label="mysqlclient">

サポートレベル:**互換性あり**

[mysqlクライアントのドキュメント](https://pypi.org/project/mysqlclient/)に従ってドライバーをダウンロードして設定できます。 mysqlclient 2.1.1 以降のバージョンを使用することをお勧めします。

mysqlclient を使用して TiDB アプリケーションを構築する例については、 [mysqlclient を使用して TiDB に接続する](/develop/dev-guide-sample-application-python-mysqlclient.md)を参照してください。

</div>
<div label="MySQL Connector/Python">

サポートレベル:**互換性あり**

[MySQL コネクタ/Python ドキュメント](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)に従ってドライバーをダウンロードして設定できます。 Connector/Python 8.0.31 以降のバージョンを使用することをお勧めします。

MySQL コネクタ/Python を使用して TiDB アプリケーションを構築する例については、 [MySQL コネクタ/Python を使用して TiDB に接続する](/develop/dev-guide-sample-application-python-mysql-connector.md)を参照してください。

</div>
</SimpleTab>

### Python ORM フレームワーク {#python-orm-frameworks}

<SimpleTab>
<div label="Django">

サポートレベル:**フル**

[ジャンゴ](https://docs.djangoproject.com/)は人気のある Python Web フレームワークです。 TiDB と Django の間の互換性の問題を解決するために、PingCAP は TiDB 方言`django-tidb`を提供します。インストールするには、 [`django-tidb`ドキュメント](https://github.com/pingcap/django-tidb#installation-guide)が表示されます。

Django を使用して TiDB アプリケーションを構築する例については、 [Django を使用して TiDB に接続する](/develop/dev-guide-sample-application-python-django.md)を参照してください。

</div>
<div label="SQLAlchemy">

サポートレベル:**フル**

[SQLアルケミー](https://www.sqlalchemy.org/)は、Python の人気のある ORM フレームワークです。アプリケーション内のすべての依存関係を取得するには、 `pip install SQLAlchemy==1.4.44`コマンドを使用します。 SQLAlchemy 1.4.44 以降のバージョンを使用することをお勧めします。

SQLAlchemy を使用して TiDB アプリケーションを構築する例については、 [SQLAlchemy を使用して TiDB に接続する](/develop/dev-guide-sample-application-python-sqlalchemy.md)を参照してください。

</div>
<div label="peewee">

サポートレベル:**互換性あり**

[ピーピー](http://docs.peewee-orm.com/en/latest/)は、Python の人気のある ORM フレームワークです。アプリケーション内のすべての依存関係を取得するには、 `pip install peewee==3.15.4`コマンドを使用します。 peewee 3.15.4 以降のバージョンを使用することをお勧めします。

peewee を使用して TiDB アプリケーションを構築する例については、 [peewee で TiDB に接続する](/develop/dev-guide-sample-application-python-peewee.md)を参照してください。

</div>
</SimpleTab>

<CustomContent platform="tidb-cloud">

ドライバーまたは ORM を決定したら、 [TiDB クラスターに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)を行うことができます。

</CustomContent>
