---
title: Choose Driver or ORM
summary: Learn how to choose a driver or ORM framework to connect to TiDB.
---

# Driverまたは ORM を選択 {#choose-driver-or-orm}

> **ノート：**
>
> TiDB は、ドライバーと ORM に対して次の 2 つのサポート レベルを提供します。
>
> -   **完全**: このドライバーまたは ORM を使用しても、既知の問題がないことを示します。
> -   **検証済み**: TiDB と MySQL の互換性の違いにより、このドライバーまたは ORM を使用するとエラーが発生する可能性があることを示します。
>
> 詳細については、 [TiDB がサポートするサードパーティ ツール](/develop/dev-guide-third-party-support.md)を参照してください。

TiDB は MySQL プロトコルと高い互換性がありますが、一部の機能は MySQL と互換性がありません。

例えば：

-   TiDB でサポートされていない機能:

    -   ストアド プロシージャと関数
    -   トリガー
    -   `FOREIGN KEY`制約

-   MySQL とは異なる機能:

    -   自動インクリメント ID: 自動インクリメント列は、TiDB 内でグローバルに一意です。それらは単一の TiDBサーバー上では増分ですが***、必ずしも***複数の TiDB サーバー間で増分されたり、順次割り当てられるとは限りません。

互換性の相違点の完全なリストについては、 [MySQL の互換性](/mysql-compatibility.md)を参照してください。

## Java {#java}

このセクションでは、 Javaでドライバーと ORM フレームワークを使用する方法について説明します。

### Javaドライバー {#java-drivers}

<SimpleTab>
<div label="MySQL-JDBC">

サポートレベル:**フル**

[MySQL ドキュメント](https://dev.mysql.com/doc/connector-j/8.0/en/)に従って、 Java JDBC ドライバーをダウンロードして構成できます。 TiDB v6.3.0 以降では、MySQL Connector/J 8.0.29 以降を使用することをお勧めします。

> **ヒント：**
>
> 現在のバージョン 8.0.30 には[未解決のバグ](https://bugs.mysql.com/bug.php?id=106252)があるため、v6.3.0 より前のバージョンの TiDB を使用すると、スレッドがハングする可能性があります。 TiDB v6.3.0 以降のバージョンをまだ使用していない場合は、MySQL Connector/J 8.0 でこのバグが修正されるまでバージョン 8.0 にアップグレードしないか、これに対処する MySQL Connector/J の TiDB バージョンを使用することをお勧めします。バグ ( *TiDB-JDBC*タブを参照)。

完全なアプリケーションを構築する方法の例については、 [TiDB と JDBC を使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-java.md)を参照してください。

</div>
<div label="TiDB-JDBC">

サポートレベル:**フル**

[TiDB-JDBC](https://github.com/pingcap/mysql-connector-j)は、MySQL 8.0.29 に基づくカスタマイズされたJavaドライバーです。 MySQL 公式バージョン 8.0.29 に基づいてコンパイルされた TiDB-JDBC は、元の JDBC の準備モードでのマルチパラメータおよびマルチフィールド EOF のバグを修正し、自動 TiCDC スナップショット メンテナンスおよび SM3 認証プラグインなどの機能を追加します。

SM3 ベースの認証の使用は、MySQL Connector/J の TiDB バージョンでのみサポートされています。

Maven を使用する場合は、次の内容を`pom.xml`ファイルの`<dependencies></dependencies>`セクションに追加します。

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
```

SM3 認証を有効にする必要がある場合は、次の内容を`pom.xml`ファイルの`<dependencies></dependencies>`セクションに追加します。

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

> **ノート：**
>
> -   現在、Hibernate は[ネストされたトランザクションをサポートしない](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres)を実行します。
>
> -   v6.2.0 以降、TiDB は[セーブポイント](/sql-statements/sql-statement-savepoint.md)をサポートしています。 `@Transactional`で`Propagation.NESTED`トランザクション伝播オプションを使用する、つまり`@Transactional(propagation = Propagation.NESTED)`を設定するには、TiDB が v6.2.0 以降であることを確認してください。

<SimpleTab>
<div label="Hibernate">

サポートレベル:**フル**

アプリケーションの異なる依存関係間の複雑な関係を手動で管理することを避けるために、 [グラドル](https://gradle.org/install)または[メイヴン](https://maven.apache.org/install.html)を使用して、間接的なものを含むアプリケーションのすべての依存関係を取得できます。 Hibernate `6.0.0.Beta2`以降のみが TiDB ダイアレクトをサポートすることに注意してください。

**Maven**を使用している場合は、次を`<dependencies></dependencies>`に追加します。

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

**Gradle**を使用している場合は、以下を`dependencies`に追加します。

```gradle
implementation 'org.hibernate:hibernate-core:6.0.0.CR2'
implementation 'mysql:mysql-connector-java:5.1.49'
```

-   Hibernate を使用してネイティブJavaで TiDB アプリケーションを構築する例については、 [TiDB とJavaを使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-java.md)を参照してください。
-   Spring Data JPA または Hibernate を使用して Spring で TiDB アプリケーションを構築する例については、 [Spring Boot を使用して TiDB アプリケーションを構築する](/develop/dev-guide-sample-application-spring-boot.md)を参照してください。

さらに、 [ハイバネート構成ファイル](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm) : `org.hibernate.dialect.TiDBDialect`で TiDB ダイアレクトを指定する必要があります。これは、Hibernate `6.0.0.Beta2`以降でのみサポートされています。 `Hibernate`バージョンが`6.0.0.Beta2`より前の場合は、最初にアップグレードしてください。

> **ノート：**
>
> バージョン`Hibernate`をアップグレードできない場合は、代わりにMySQL 5.7ダイアレクト`org.hibernate.dialect.MySQL57Dialect`を使用してください。ただし、この設定により、予測できない結果が生じたり、 [シーケンス](/sql-statements/sql-statement-create-sequence.md)などの TiDB 固有の機能が一部失われたりする可能性があります。

</div>

<div label="MyBatis">

サポートレベル:**フル**

アプリケーションの異なる依存関係間の複雑な関係を手動で管理することを避けるために、 [グラドル](https://gradle.org/install)または[メイヴン](https://maven.apache.org/install.html)を使用して、間接的な依存関係を含むアプリケーションのすべての依存関係を取得できます。

Maven を使用している場合は、以下を`<dependencies></dependencies>`に追加します。

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

Gradle を使用している場合は、以下を`dependencies`に追加します。

```gradle
implementation 'org.mybatis:mybatis:3.5.9'
implementation 'mysql:mysql-connector-java:5.1.49'
```

MyBatis を使用して TiDB アプリケーションを構築する例については、 [TiDB とJavaを使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-java.md)を参照してください。

</div>

</SimpleTab>

### Javaクライアントの負荷分散 {#java-client-load-balancing}

**tidb-loadbalance**

サポートレベル:**フル**

[tidb-loadbalance](https://github.com/pingcap/tidb-loadbalance)は、アプリケーション側の負荷分散コンポーネントです。 tidb-loadbalance を使用すると、TiDBサーバーのノード情報を自動的に維持し、tidb-loadbalance ポリシーを使用してクライアントに JDBC 接続を分散できます。クライアント アプリケーションと TiDBサーバー間で直接 JDBC 接続を使用すると、負荷分散コンポーネントを使用するよりも高いパフォーマンスが得られます。

現在、tidb-loadbalance は次のポリシーをサポートしています: roundrobin、random、および weight。

> **ノート：**
>
> tidb-loadbalance は[mysql-コネクタ-j](https://github.com/pingcap/mysql-connector-j)と共に使用する必要があります。

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

**go-sql-driver/mysql**

サポートレベル:**フル**

Golangドライバーをダウンロードして構成するには、 [go-sql-driver/mysql ドキュメント](https://github.com/go-sql-driver/mysql)を参照してください。

完全なアプリケーションを構築する方法の例については、 [TiDB とGolangを使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-golang.md)を参照してください。

### Golang ORM フレームワーク {#golang-orm-frameworks}

**ゴーム**

サポートレベル:**フル**

GORM はGolangの一般的な ORM フレームワークです。アプリケーションのすべての依存関係を取得するには、 `go get`コマンドを使用できます。

```shell
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```

GORM を使用して TiDB アプリケーションを構築する例については、 [TiDB とGolangを使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-golang.md)を参照してください。
