---
title: Third-Party Tools Supported by TiDB
summary: Learn about third-party tools supported by TiDB.
---

# TiDB がサポートするサードパーティ ツール {#third-party-tools-supported-by-tidb}

> **ノート：**
>
> このドキュメントでは、TiDB でサポートされている一般的なサードパーティ ツールのみをリストしています。サポートされていないためではなく、PingCAP が TiDB と互換性のない機能を使用しているかどうかわからないため、その他のサードパーティ製ツールがいくつかリストされていません。

TiDB は[MySQL プロトコルとの高い互換性](/mysql-compatibility.md)であるため、MySQL ドライバー、ORM フレームワーク、および MySQL に適応するその他のツールのほとんどは TiDB と互換性があります。このドキュメントでは、これらのツールと TiDB のサポート レベルに焦点を当てています。

## サポートレベル {#support-level}

PingCAP はコミュニティと協力して、サードパーティ ツールに次のサポート レベルを提供します。

-   ***Full*** : TiDB は、対応するサードパーティ ツールのほとんどの機能と既に互換性があり、新しいバージョンとの互換性を維持していることを示します。 PingCAP は、ツールの最新バージョンとの互換性テストを定期的に実施します。
-   ***互換性***: 対応するサードパーティ ツールは MySQL に適合しており、TiDB は MySQL プロトコルとの互換性が高いため、TiDB はツールのほとんどの機能を使用できることを示します。ただし、PingCAP はツールのすべての機能について完全なテストを完了していないため、予期しない動作が発生する可能性があります。

> **ノート：**
>
> 指定されていない限り、 [アプリケーションの再試行とエラー処理](/develop/dev-guide-transaction-troubleshoot.md#application-retry-and-error-handling)のサポートは**Driver**または<strong>ORM フレームワーク</strong>には含まれていません。

このドキュメントに記載されているツールを使用して[問題](https://github.com/pingcap/tidb/issues/new?assignees=&#x26;labels=type%2Fquestion&#x26;template=general-question.md)に接続するときに問題が発生した場合は、このツールのサポートを促進するための詳細を GitHub に送信してください。

## Driver {#driver}

| 言語         | Driver                                                                           | テスト済みの最新バージョン | サポートレベル | TiDB アダプター                                                                                                                                                                                   | チュートリアル                                                                               |
| ---------- | -------------------------------------------------------------------------------- | ------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| ハ          | [libmysqlclient](https://dev.mysql.com/doc/c-api/8.0/en/c-api-introduction.html) | 8.0           | 互換性     | なし                                                                                                                                                                                           | なし                                                                                    |
| C#(.Net)   | [MySQL コネクタ/NET](https://downloads.mysql.com/archives/c-net/)                    | 8.0           | 互換性     | なし                                                                                                                                                                                           | なし                                                                                    |
| ODBC       | [MySQL コネクタ/ODBC](https://downloads.mysql.com/archives/c-odbc/)                  | 8.0           | 互換性     | なし                                                                                                                                                                                           | なし                                                                                    |
| 行け         | [go-sql-driver/mysql](https://github.com/go-sql-driver/mysql)                    | v1.6.0        | 満杯      | なし                                                                                                                                                                                           | [TiDB とGolangを使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-golang.md) |
| Java       | [JDBC](https://dev.mysql.com/downloads/connector/j/)                             | 8.0           | 満杯      | [pingcap/mysql-connector-j](/develop/dev-guide-choose-driver-or-orm.md#java-drivers) <br/> [pingcap/tidb-loadbalance](/develop/dev-guide-choose-driver-or-orm.md#java-client-load-balancing) | [TiDB とJavaを使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-java.md)     |
| JavaScript | [mysql](https://github.com/mysqljs/mysql)                                        | v2.18.1       | 互換性     | なし                                                                                                                                                                                           | なし                                                                                    |
| PHP        | [mysqlnd](https://dev.mysql.com/downloads/connector/php-mysqlnd/)                | PHP 5.4+      | 互換性     | なし                                                                                                                                                                                           | なし                                                                                    |
| パイソン       | [MySQL コネクタ/Python](https://downloads.mysql.com/archives/c-python/)              | 8.0           | 互換性     | なし                                                                                                                                                                                           | なし                                                                                    |

## ORM {#orm}

| 言語                    | ORM フレームワーク                                                            | テスト済みの最新バージョン     | サポートレベル | TiDB アダプター                                             | チュートリアル                                                                                      |
| --------------------- | ---------------------------------------------------------------------- | ----------------- | ------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| 行け                    | [ゴーム](https://github.com/go-gorm/gorm)                                 | v1.23.5           | 満杯      | なし                                                     | [TiDB とGolangを使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-golang.md)        |
| 行け                    | [ビーゴ](https://github.com/beego/beego)                                  | v2.0.3            | 満杯      | なし                                                     | なし                                                                                           |
| 行け                    | [アッパー/デシベル](https://github.com/upper/db)                               | v4.5.2            | 満杯      | なし                                                     | なし                                                                                           |
| 行け                    | [ゾーム](https://gitea.com/xorm/xorm)                                     | v1.3.1            | 満杯      | なし                                                     | なし                                                                                           |
| 行け                    | [エント](https://github.com/ent/ent)                                      | v0.11.0           | 互換性     | なし                                                     | なし                                                                                           |
| Java                  | [休止状態](https://hibernate.org/orm/)                                     | 6.1.0.最終          | 満杯      | なし                                                     | [TiDB とJavaを使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-java.md)            |
| Java                  | [マイバティス](https://mybatis.org/mybatis-3/)                               | v3.5.10           | 満杯      | なし                                                     | [TiDB とJavaを使用して単純な CRUD アプリを構築する](/develop/dev-guide-sample-application-java.md)            |
| Java                  | [春のデータ JPA](https://spring.io/projects/spring-data-jpa/)               | 2.7.2             | 満杯      | なし                                                     | [Spring Boot を使用して TiDB アプリケーションを構築する](/develop/dev-guide-sample-application-spring-boot.md) |
| Java                  | [jOOQ](https://github.com/jOOQ/jOOQ)                                   | v3.16.7 (オープンソース) | 満杯      | なし                                                     | なし                                                                                           |
| ルビー                   | [アクティブ レコード](https://guides.rubyonrails.org/active_record_basics.html) | v7.0              | 満杯      | なし                                                     | なし                                                                                           |
| JavaScript/TypeScript | [続編](https://www.npmjs.com/package/sequelize)                          | v6.20.1           | 互換性     | なし                                                     | なし                                                                                           |
| JavaScript/TypeScript | [Knex.js](https://knexjs.org/)                                         | v1.0.7            | 互換性     | なし                                                     | なし                                                                                           |
| JavaScript/TypeScript | [Prisma クライアント](https://www.prisma.io/)                                | 3.15.1            | 互換性     | なし                                                     | なし                                                                                           |
| JavaScript/TypeScript | [タイプORM](https://www.npmjs.com/package/typeorm)                        | v0.3.6            | 互換性     | なし                                                     | なし                                                                                           |
| PHP                   | [ララベル](https://laravel.com/)                                           | v9.1.10           | 互換性     | [laravel-tidb](https://github.com/colopl/laravel-tidb) | なし                                                                                           |
| パイソン                  | [ジャンゴ](https://pypi.org/project/Django/)                               | v4.0.5            | 互換性     | [ジャンゴ tidb](https://github.com/pingcap/django-tidb)    | なし                                                                                           |
| パイソン                  | [ピーウィー](https://github.com/coleifer/peewee/)                           | v3.14.10          | 互換性     | なし                                                     | なし                                                                                           |
| パイソン                  | [ポニーORM](https://ponyorm.org/)                                         | v0.7.16           | 互換性     | なし                                                     | なし                                                                                           |
| パイソン                  | [SQL錬金術](https://www.sqlalchemy.org/)                                  | v1.4.37           | 互換性     | なし                                                     | なし                                                                                           |

## GUI {#gui}

| GUI                                                       | テスト済みの最新バージョン | サポートレベル | チュートリアル |
| --------------------------------------------------------- | ------------- | ------- | ------- |
| [DBeaver](https://dbeaver.io/)                            | 22.1.0        | 互換性     | なし      |
| [MySQL 用 Navicat](https://www.navicat.com/)               | 16.0.14       | 互換性     | なし      |
| [MySQL ワークベンチ](https://www.mysql.com/products/workbench/) | 8.0           | 互換性     | なし      |

| IDE                                              | プラグイン                                                                                   | サポートレベル | チュートリアル |
| ------------------------------------------------ | --------------------------------------------------------------------------------------- | ------- | ------- |
| [データグリップ](https://www.jetbrains.com/datagrip/)   | なし                                                                                      | 互換性     | なし      |
| [IntelliJ アイデア](https://www.jetbrains.com/idea/) | なし                                                                                      | 互換性     | なし      |
| [ビジュアル スタジオ コード](https://code.visualstudio.com/) | [潮](https://marketplace.visualstudio.com/items?itemName=dragonly.ticode)                | 互換性     | なし      |
| [ビジュアル スタジオ コード](https://code.visualstudio.com/) | [MySQL](https://marketplace.visualstudio.com/items?itemName=formulahendry.vscode-mysql) | 互換性     | なし      |
