---
title: Choose Driver or ORM
summary: TiDB に接続するためのドライバーまたは ORM フレームワークを選択する方法を学習します。
---

# DriverまたはORMを選択 {#choose-driver-or-orm}

> **注記：**
>
> TiDB は、ドライバーと ORM に対して次の 2 つのサポート レベルを提供します。
>
> -   **完全**: TiDB がツールのほとんどの機能と互換性があり、最新バージョンとの互換性を維持していることを示します。PingCAP は、最新バージョン[TiDB でサポートされているサードパーティ ツール](/develop/dev-guide-third-party-support.md)との互換性テストを定期的に実施します。
> -   **互換**：対応するサードパーティ製ツールがMySQLに適合しており、TiDBはMySQLプロトコルと高い互換性があるため、TiDBはツールのほとんどの機能を使用できることを示します。ただし、PingCAPはツールのすべての機能について完全なテストを完了していないため、予期しない動作が発生する可能性があります。
>
> 詳細については[TiDB でサポートされているサードパーティ ツール](/develop/dev-guide-third-party-support.md)を参照してください。

TiDBはMySQLプロトコルと高い互換性がありますが、一部の機能はMySQLと互換性がありません。互換性の違いに関する完全なリストについては、 [MySQLの互換性](/mysql-compatibility.md)参照してください。

## Java {#java}

このセクションでは、 Javaでドライバーと ORM フレームワークを使用する方法について説明します。

### Javaドライバー {#java-drivers}

<SimpleTab>
<div label="MySQL-JDBC">

サポートレベル:**フル**

Java JDBCドライバをダウンロードして設定するには、 [MySQLドキュメント](https://dev.mysql.com/doc/connector-j/en/)手順に従ってください。TiDB v6.3.0以降では、MySQL Connector/Jの最新GAバージョンを使用することをお勧めします。

> **警告：**
>
> MySQL Connector/J 8.0 の 8.0.31 より前のバージョンには[バグ](https://bugs.mysql.com/bug.php?id=106252)問題があり（詳細は[MySQL JDBC のバグ](/develop/dev-guide-third-party-tools-compatibility.md#mysql-jdbc-bugs)参照）、TiDB バージョン 6.3.0 より前のバージョンを使用するとスレッドがハングする可能性があります。この問題を回避するには、MySQL Connector/J 8.0.31 以前のバージョンを使用し**ない**でください。

完全なアプリケーションを構築する方法の例については、 [TiDBとJDBCを使用してシンプルなCRUDアプリを構築する](/develop/dev-guide-sample-application-java-jdbc.md)参照してください。

</div>
<div label="TiDB-JDBC">

サポートレベル:**フル**

TiDB-JDBC [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j) 、MySQL 8.0.29をベースにカスタマイズされたJavaドライバです。MySQL公式バージョン8.0.29をベースにコンパイルされたTiDB-JDBCは、元のJDBCにおける準備モードにおける複数パラメータおよび複数フィールドのEOFのバグを修正し、TiCDCスナップショットの自動メンテナンスやSM3認証プラグインなどの機能を追加しています。

SM3 に基づく認証は、TiDB の TiDB-JDBC でのみサポートされます。

Maven を使用している場合は、 `pom.xml`ファイルの`<dependencies></dependencies>`セクションに次のコンテンツを追加します。

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
```

SM3 認証を有効にする必要がある場合は、 `pom.xml`ファイルの`<dependencies></dependencies>`セクションに次のコンテンツを追加します。

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

### Java ORMフレームワーク {#java-orm-frameworks}

<SimpleTab>
<div label="Hibernate">

> **注記：**
>
> -   現在、Hibernate は[ネストされたトランザクションをサポートしていない](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres)実行します。
>
> -   TiDBはv6.2.0以降、 [セーブポイント](/sql-statements/sql-statement-savepoint.md)サポートしています。5 `@Transactional` `Propagation.NESTED`トランザクション伝播オプションを使用するには、つまり`@Transactional(propagation = Propagation.NESTED)`設定するには、TiDBがv6.2.0以降であることを確認してください。

サポートレベル:**フル**

アプリケーション内の異なる依存関係間の複雑な関係を手動で管理する手間を省くため、 [グラドル](https://gradle.org/install)または[メイヴン](https://maven.apache.org/install.html)使用することで、間接的な依存関係も含め、アプリケーションのすべての依存関係を取得できます。なお、TiDB 方言は Hibernate `6.0.0.Beta2`以降でのみサポートされています。

Maven を使用している場合は、 `<dependencies></dependencies>`に以下を追加します。

```xml
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>6.2.3.Final</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
```

Gradle を使用している場合は、 `dependencies`に以下を追加します。

```gradle
implementation 'org.hibernate:hibernate-core:6.2.3.Final'
implementation 'mysql:mysql-connector-java:8.0.33'
```

-   Hibernate を使用してネイティブJavaで TiDB アプリケーションを構築する例については、 [TiDBとHibernateを使ったシンプルなCRUDアプリの構築](/develop/dev-guide-sample-application-java-hibernate.md)参照してください。
-   Spring Data JPA または Hibernate を使用して Spring で TiDB アプリケーションを構築する例については、 [Spring Bootを使用してTiDBアプリを構築する](/develop/dev-guide-sample-application-java-spring-boot.md)参照してください。

さらに、 [Hibernate設定ファイル](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm) : `org.hibernate.dialect.TiDBDialect`で TiDB 方言を指定する必要があります。これは Hibernate `6.0.0.Beta2`以降でのみサポートされます。7 `Hibernate`バージョンが`6.0.0.Beta2`より前の場合は、まずアップグレードしてください。

> **注記：**
>
> `Hibernate`バージョンをアップグレードできない場合は、代わりにMySQL 5.7方言`org.hibernate.dialect.MySQL57Dialect`使用してください。ただし、この設定では予期しない結果が生じる可能性があり、 [シーケンス](/sql-statements/sql-statement-create-sequence.md)などの TiDB 固有の機能が一部利用できなくなる可能性があります。

</div>

<div label="MyBatis">

サポートレベル:**フル**

アプリケーションのさまざまな依存関係間の複雑な関係を手動で管理することを避けるために、 [グラドル](https://gradle.org/install)または[メイヴン](https://maven.apache.org/install.html)使用して、間接的な依存関係も含め、アプリケーションのすべての依存関係を取得できます。

Maven を使用している場合は、 `<dependencies></dependencies>`に以下を追加します。

```xml
<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis</artifactId>
    <version>3.5.13</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
```

Gradle を使用している場合は、 `dependencies`に以下を追加します。

```gradle
implementation 'org.mybatis:mybatis:3.5.13'
implementation 'mysql:mysql-connector-java:8.0.33'
```

MyBatis を使用して TiDB アプリケーションを構築する例については、 [TiDBとMyBatisを使ったシンプルなCRUDアプリの構築](/develop/dev-guide-sample-application-java-mybatis.md)参照してください。

</div>

</SimpleTab>

### Javaクライアント負荷分散 {#java-client-load-balancing}

**tidb-ロードバランス**

サポートレベル:**フル**

tidb-loadbalance は、アプリケーション側の負荷分散コンポーネント[tidb-ロードバランス](https://github.com/pingcap/tidb-loadbalance) 。tidb-loadbalance を使用すると、TiDBサーバーのノード情報を自動的に管理し、tidb-loadbalance ポリシーに基づいてクライアント側の JDBC 接続を分散できます。クライアントアプリケーションと TiDBサーバー間の直接 JDBC 接続を使用すると、負荷分散コンポーネントを使用するよりも高いパフォーマンスが得られます。

現在、tidb-loadbalance はラウンドロビン、ランダム、重み付けのポリシーをサポートしています。

> **注記：**
>
> tidb-loadbalance は[mysql-コネクタ-j](https://github.com/pingcap/mysql-connector-j)で使用する必要があります。

Maven を使用している場合は、 `pom.xml`ファイルの`<dependencies></dependencies>`要素本体に次のコンテンツを追加します。

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

Gradle を使用している場合は、次の内容を`dependencies`に追加します。

```gradle
implementation group: 'io.github.lastincisor', name: 'mysql-connector-java', version: '8.0.29-tidb-1.0.0'
implementation group: 'io.github.lastincisor', name: 'tidb-loadbalance', version: '0.0.5'
```

## Golang {#golang}

このセクションでは、 Golangでドライバーと ORM フレームワークを使用する方法について説明します。

### Golangドライバー {#golang-drivers}

**go-sql-driver/mysql**

サポートレベル:**フル**

Golangドライバーをダウンロードして設定するには、 [go-sql-driver/mysql ドキュメント](https://github.com/go-sql-driver/mysql)を参照してください。

完全なアプリケーションを構築する方法の例については、 [Go-MySQL-Driver で TiDB に接続する](/develop/dev-guide-sample-application-golang-sql-driver.md)参照してください。

### Golang ORMフレームワーク {#golang-orm-frameworks}

**ゴーム**

サポートレベル:**フル**

GORMはGolangで人気のORMフレームワークです。アプリケーション内のすべての依存関係を取得するには、 `go get`コマンドを使用します。

```shell
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```

GORM を使用して TiDB アプリケーションを構築する例については、 [GORMでTiDBに接続する](/develop/dev-guide-sample-application-golang-gorm.md)参照してください。

## パイソン {#python}

このセクションでは、Python でドライバーと ORM フレームワークを使用する方法について説明します。

### Pythonドライバー {#python-drivers}

<SimpleTab>
<div label="PyMySQL">

サポートレベル:**互換**

[PyMySQLドキュメント](https://pypi.org/project/PyMySQL/)に従ってドライバをダウンロードし、設定してください。PyMySQL 1.0.2以降のバージョンの使用をお勧めします。

PyMySQL を使用して TiDB アプリケーションを構築する例については、 [PyMySQLでTiDBに接続する](/develop/dev-guide-sample-application-python-pymysql.md)参照してください。

</div>
<div label="mysqlclient">

サポートレベル:**互換**

[mysqlclient ドキュメント](https://pypi.org/project/mysqlclient/)に従ってドライバをダウンロードし、設定してください。mysqlclient 2.1.1以降のバージョンの使用をお勧めします。

mysqlclient を使用して TiDB アプリケーションを構築する例については、 [mysqlclientでTiDBに接続する](/develop/dev-guide-sample-application-python-mysqlclient.md)参照してください。

</div>
<div label="MySQL Connector/Python">

サポートレベル:**互換**

[MySQLコネクタ/Pythonドキュメント](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)に従ってドライバをダウンロードし、設定してください。Connector/Python 8.0.31以降のバージョンを使用することをお勧めします。

MySQL Connector/Python を使用して TiDB アプリケーションを構築する例については、 [MySQL Connector/Python で TiDB に接続する](/develop/dev-guide-sample-application-python-mysql-connector.md)参照してください。

</div>
</SimpleTab>

### Python ORMフレームワーク {#python-orm-frameworks}

<SimpleTab>
<div label="Django">

サポートレベル:**フル**

[ジャンゴ](https://docs.djangoproject.com/)は人気のPythonウェブフレームワークです。TiDBとDjangoの互換性問題を解決するため、PingCAPはTiDB方言`django-tidb`提供しています。インストールするには、 [`django-tidb`ドキュメント](https://github.com/pingcap/django-tidb#installation-guide)参照してください。

Django を使用して TiDB アプリケーションを構築する例については、 [DjangoでTiDBに接続する](/develop/dev-guide-sample-application-python-django.md)参照してください。

</div>
<div label="SQLAlchemy">

サポートレベル:**フル**

[SQLアルケミー](https://www.sqlalchemy.org/) Pythonで人気のORMフレームワークです。アプリケーション内のすべての依存関係を取得するには、 `pip install SQLAlchemy==1.4.44`コマンドを使用します。SQLAlchemy 1.4.44以降のバージョンの使用をお勧めします。

SQLAlchemy を使用して TiDB アプリケーションを構築する例については、 [SQLAlchemy で TiDB に接続する](/develop/dev-guide-sample-application-python-sqlalchemy.md)参照してください。

</div>
<div label="peewee">

サポートレベル:**互換**

[ピーウィー](http://docs.peewee-orm.com/en/latest/)はPythonで人気のORMフレームワークです。アプリケーション内のすべての依存関係を取得するには、 `pip install peewee==3.15.4`コマンドを使用します。peewee 3.15.4以降のバージョンの使用をお勧めします。

peewee を使用して TiDB アプリケーションを構築する例については、 [peeweeでTiDBに接続する](/develop/dev-guide-sample-application-python-peewee.md)参照してください。

</div>
</SimpleTab>

<CustomContent platform="tidb-cloud">

ドライバーまたは ORM を決定したら、 [TiDBクラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)実行できます。

</CustomContent>

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
