---
title: Choose Driver or ORM
summary: Learn how to choose a driver or ORM framework to connect to TiDB.
---

# Driverまたは ORM を選択 {#choose-driver-or-orm}

TiDB は MySQL プロトコルと高い互換性がありますが、一部の機能は MySQL と互換性がありません。

例えば：

-   TiDB でサポートされていない機能:

    -   ストアド プロシージャと関数
    -   トリガー
    -   `FOREIGN KEY`制約

-   MySQL とは異なる機能:

    -   自動インクリメント ID: 自動インクリメンタル列は、TiDB 内でグローバルに一意です。それらは単一の TiDBサーバー上では増分ですが***、必ずしも***複数の TiDB サーバー間で増分されたり、順次割り当てられるとは限りません。

互換性の相違点の完全なリストについては、 [MySQL の互換性](/mysql-compatibility.md)を参照してください。

## ジャワ {#java}

TiDB は、Java に対して次の 2 つのサポート レベルを提供します。

-   **完全**: このドライバーまたは ORM を使用しても、既知の問題がないことを示します。
-   **検証済み**: TiDB と MySQL の互換性の違いにより、このドライバーまたは ORM を使用するとエラーが発生する可能性があることを示します。

### Java ドライバー {#java-drivers}

**JDBC**

サポートレベル:**フル**

[MySQL ドキュメント](https://dev.mysql.com/doc/connector-j/5.1/en/)に従って、Java JDBC ドライバーをダウンロードして構成できます。

> **ノート：**
>
> JDBC 5.1 の最新バージョンであるバージョン 5.1.49 を使用することを強くお勧めします。現在のバージョン 8.0.29 には[未解決のバグ](https://bugs.mysql.com/bug.php?id=106252)があるため、TiDB の使用時にスレッドがハングする可能性があります。 MySQL JDBC 8.0 がこの修正をマージするまで、バージョン 8.0 にアップグレードしないことをお勧めします。

完全なアプリケーションを構築する方法の例については、 [TiDB と JDBC を使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-java.md)を参照してください。

### Java ORM フレームワーク {#java-orm-framework}

#### 休止状態 {#hibernate}

サポートレベル: `Full`

> **ノート：**
>
> 現在、Hibernate は[ネストされたトランザクションをサポートしない](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres)を実行し、TiDB は[セーブポイントをサポートしていません](https://github.com/pingcap/tidb/issues/6840)を実行します。 `Spring Data JPA`などのフレームワークを使用している場合は、 `@Transactional`で`Propagation.NESTED`トランザクション伝播オプションを使用しないでください。つまり、 `@Transactional( propagation = Propagation.NESTED)`を設定しないでください。
>
> [この例](https://github.com/Icemap/tidb-savepoint)を使用すると、TiDB と MySQL の Savepoint の出力をすばやく再現できます。

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

アプリケーションの異なる依存関係間の複雑な関係を手動で管理することを避けるために、 [グラドル](https://gradle.org/install)または[メイヴン](https://maven.apache.org/install.html)を使用して、間接的なものを含むアプリケーションのすべての依存関係を取得できます。 Hibernate `6.0.0.Beta2`以降のみが TiDB ダイアレクトをサポートすることに注意してください。

**Maven**を使用している場合は、次を`<dependencies></dependencies>`に追加します。

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
    <version>5.1.49</version>
</dependency>
```

**Gradle**を使用している場合は、以下を`dependencies`に追加します。

{{< copyable "" >}}

```gradle
implementation 'org.hibernate:hibernate-core:6.0.0.CR2'
implementation 'mysql:mysql-connector-java:5.1.49'
```

-   Hibernate を使用してネイティブ Java で TiDB アプリケーションを構築する例については、 [TiDB と Java を使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-java.md)を参照してください。
-   Spring Data JPA または Hibernate を使用して Spring で TiDB アプリケーションを構築する例については、 [Spring Boot を使用して TiDB アプリケーションを構築する](/develop/dev-guide-sample-application-spring-boot.md)を参照してください。

さらに、 [ハイバネート構成ファイル](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm) : `org.hibernate.dialect.TiDBDialect`で TiDB ダイアレクトを指定する必要があります。これは、Hibernate `6.0.0.Beta2`以降でのみサポートされています。 `Hibernate`バージョンが`6.0.0.Beta2`より前の場合は、最初にアップグレードしてください。

> **ノート：**
>
> バージョン`Hibernate`をアップグレードできない場合は、代わりにMySQL 5.7ダイアレクト`org.hibernate.dialect.MySQL57Dialect`を使用してください。ただし、この設定により、予測できない結果が生じたり、 [シーケンス](/sql-statements/sql-statement-create-sequence.md)などの TiDB 固有の機能が一部失われたりする可能性があります。
