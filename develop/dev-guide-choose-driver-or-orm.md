---
title: Choose Driver or ORM
summary: Learn how to choose a driver or ORM framework to connect to TiDB.
---

# DriverまたはORMを選択します {#choose-driver-or-orm}

TiDBはMySQLプロトコルとの互換性が高いですが、一部の機能はMySQLと互換性がありません。

例えば：

-   TiDBでサポートされていない機能：

    -   ストアドプロシージャと関数
    -   トリガー
    -   `FOREIGN KEY`制約

-   MySQLとは異なる機能：

    -   自動インクリメントID：自動インクリメンタル列はTiDBでグローバルに一意です。これらは単一のTiDBサーバーではインクリメンタルですが、複数のTiDBサーバー間でインクリメンタルである必要***はなく***、順番に割り当てられる必要もありません。

互換性の違いの完全なリストについては、 [MySQLの互換性](/mysql-compatibility.md)を参照してください。

## Java {#java}

TiDBは、Javaに対して次の2つのサポートレベルを提供します。

-   **フル**：このドライバーまたはORMの使用に既知の問題がないことを示します。
-   **確認済み**：TiDBとMySQLの互換性の違いにより、このドライバーまたはORMを使用するとエラーが発生する可能性があることを示します。

### Javaドライバー {#java-drivers}

**JDBC**

サポートレベル：**フル**

[MySQLドキュメント](https://dev.mysql.com/doc/connector-j/8.0/en/)に従って、JavaJDBCドライバーをダウンロードして構成できます。

> **ノート：**
>
> バージョン`8.0.16`以降を強くお勧めします。これにより、2つのCommon Vulnerabilities and Exposures（CVE）が修正されます。
>
> -   CVE-2019-2692を直接修正する
> -   CVE-2021-22569を間接的に修正

完全なアプリケーションを構築する方法の例については、 [TiDBとJDBCを使用してシンプルなCRUDアプリを構築する](/develop/dev-guide-sample-application-java.md)を参照してください。

### JavaORMフレームワーク {#java-orm-framework}

#### Hibernate {#hibernate}

サポートレベル： `Full`

> **ノート：**
>
> 現在、Hibernateは[ネストされたトランザクションをサポートしていません](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres)を実行し、TiDBは[セーブポイントをサポートしていません](https://github.com/pingcap/tidb/issues/6840)を実行します。 `Spring Data JPA`などのフレームワークを使用している場合は、 `@Transactional`で`Propagation.NESTED`トランザクション伝播オプションを使用しないでください。つまり、 `@Transactional( propagation = Propagation.NESTED)`を設定しないでください。
>
> [この例](https://github.com/Icemap/tidb-savepoint)を使用すると、セーブポイント用のTiDBとMySQLの出力をすばやく再現できます。

> ```
> MySQL:
> id: 1, coins: 1, goods: 1
> id: 3, coins: 1, goods: 1
>
> TiDB:
>
> 2022/04/02 13:59:48 /<path>/go/pkg/mod/gorm.io/driver/mysql@v1.3.2/mysql.go:397 Error 1064: You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 9 near "SAVEPOINT sp0x102cf8960"
> [1.119ms] [rows:0] SAVEPOINT sp0x102cf8960
>
> 2022/04/02 13:59:48 /<path>/go/pkg/mod/gorm.io/driver/mysql@v1.3.2/mysql.go:397 Error 1064: You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 9 near "SAVEPOINT sp0x102cf8960"
> [0.001ms] [rows:0] SAVEPOINT sp0x102cf8a00
> id: 1, coins: 1, goods: 1
> ```

アプリケーションのさまざまな依存関係間の複雑な関係を手動で管理することを回避するために、 [Gradle](https://gradle.org/install)または[Maven](https://maven.apache.org/install.html)を使用して、間接的な依存関係を含む、アプリケーションのすべての依存関係を取得できます。 `6.0.0.Beta2`ダイアレクトをサポートしているのはHibernate5以降のみであることに注意してください。

**Maven**を使用している場合は、 `<dependencies></dependencies>`に以下を追加します。

{{< copyable "" >}}

```xml
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>6.0.0.CR2</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.28</version>
</dependency>
```

**Gradle**を使用している場合は、 `dependencies`に以下を追加します。

{{< copyable "" >}}

```gradle
implementation 'org.hibernate:hibernate-core:6.0.0.CR2'
implementation 'mysql:mysql-connector-java:8.0.28'
```

-   Hibernateを使用してネイティブJavaでTiDBアプリケーションを構築する例については、 [TiDBとJavaを使用してシンプルなCRUDアプリを構築する](/develop/dev-guide-sample-application-java.md)を参照してください。
-   Spring Data JPAまたはHibernateを使用してSpringでTiDBアプリケーションを構築する例については、 [SpringBootを使用してTiDBアプリケーションを構築する](/develop/dev-guide-sample-application-spring-boot.md)を参照してください。

さらに、 [Hibernate構成ファイル](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm) ： `org.hibernate.dialect.TiDBDialect`でTiDBダイアレクトを指定する必要があります。これは、Hibernate5以降でのみサポートされて`6.0.0.Beta2`ます。 `Hibernate`バージョンが`6.0.0.Beta2`より前の場合は、最初にアップグレードしてください。

> **ノート：**
>
> `Hibernate`のバージョンをアップグレードできない場合は、代わりにMySQL 5.7ダイアレクト`org.hibernate.dialect.MySQL57Dialect`を使用してください。ただし、この設定により、予期しない結果が発生したり、 [シーケンス](/sql-statements/sql-statement-create-sequence.md)などのTiDB固有の機能が失われたりする可能性があります。
