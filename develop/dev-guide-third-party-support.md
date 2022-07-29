---
title: Third-Party Libraries Support Maintained by PingCAP
summary: Learn about third-party libraries support maintained by PingCAP.
---

# PingCAPによって維持されるサードパーティライブラリのサポート {#third-party-libraries-support-maintained-by-pingcap}

TiDBはMySQL 5.7プロトコルとの互換性が高いため、MySQLドライバー、ORMフレームワーク、およびMySQLに適応するその他のツールのほとんどはTiDBと互換性があります。このドキュメントでは、これらのツールとTiDBのサポートレベルに焦点を当てています。

## サポートレベル {#support-level}

PingCAPはコミュニティと連携し、サードパーティツールに対して次のサポートレベルを提供します。

-   ***フル***：TiDBが対応するサードパーティツールのほとんどの機能とすでに互換性があり、新しいバージョンとの互換性を維持していることを示します。 PingCAPは、ツールの最新バージョンとの互換性テストを定期的に実施します。
-   ***互換性***：対応するサードパーティツールがMySQLに適合しており、TiDBがMySQLプロトコルとの互換性が高いため、TiDBがツールのほとんどの機能を使用できることを示します。ただし、PingCAPはツールのすべての機能の完全なテストを完了していないため、予期しない動作が発生する可能性があります。

> **警告：**
>
> 特に指定がない限り、 [アプリケーションの再試行とエラー処理](/develop/dev-guide-transaction-troubleshoot.md#application-retry-and-error-handling)のサポートは**Driver**または<strong>ORMフレームワーク</strong>には含まれていません。

このドキュメントに記載されているツールを使用してTiDBに接続するときに問題が発生した場合は、このツールのサポートを促進するための詳細を記載した[問題](https://github.com/pingcap/tidb/issues/new?assignees=&#x26;labels=type%2Fquestion&#x26;template=general-question.md)をGitHubに送信してください。

## Driver {#driver}

| 言語         | Driver                                                             | 最新のテスト済みバージョン  | サポートレベル | TiDBアダプター                                                                                                          | チュートリアル                                                                              |
| ---------- | ------------------------------------------------------------------ | -------------- | ------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| C          | [MySQLコネクタ/C](https://downloads.mysql.com/archives/c-c/)           | 6.1.11         | 満杯      | 該当なし                                                                                                               | 該当なし                                                                                 |
| C＃（。Net）   | [MySQLコネクタ/NET](https://downloads.mysql.com/archives/c-net/)       | 8.0.28         | 互換性     | 該当なし                                                                                                               | 該当なし                                                                                 |
| C＃（。Net）   | [MySQLコネクタ/ODBC](https://downloads.mysql.com/archives/c-odbc/)     | 8.0.28         | 互換性     | 該当なし                                                                                                               | 該当なし                                                                                 |
| 行け         | [go-sql-driver / mysql](https://github.com/go-sql-driver/mysql)    | v1.6.0         | 満杯      | 該当なし                                                                                                               | [TiDBとGolangを使用してシンプルなCRUDアプリを構築する](/develop/dev-guide-sample-application-golang.md) |
| Java       | [JDBC](https://dev.mysql.com/downloads/connector/j/)               | 5.1.46; 8.0.29 | 満杯      | 5.1.46：N / A; 8.0.29： [pingcap / mysql-connector-j](https://github.com/pingcap/mysql-connector-j/tree/release/8.0) | [TiDBとJavaを使用してシンプルなCRUDアプリを構築する](/develop/dev-guide-sample-application-java.md)     |
| JavaScript | [mysql](https://github.com/mysqljs/mysql)                          | v2.18.1        | 互換性     | 該当なし                                                                                                               | 該当なし                                                                                 |
| PHP        | [MySQLコネクタ/PHP](https://downloads.mysql.com/archives/c-php/)       | 5.0.37         | 互換性     | 該当なし                                                                                                               | 該当なし                                                                                 |
| Python     | [MySQLコネクタ/Python](https://downloads.mysql.com/archives/c-python/) | 8.0.28         | 互換性     | 該当なし                                                                                                               | 該当なし                                                                                 |

## ORM {#orm}

| 言語                      | ORMフレームワーク                                                     | 最新のテスト済みバージョン    | サポートレベル | TiDBアダプター                                              | チュートリアル                                                                                  |
| ----------------------- | -------------------------------------------------------------- | ---------------- | ------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| 行け                      | [ゴーム](https://github.com/go-gorm/gorm)                         | v1.23.5          | 満杯      | 該当なし                                                   | [TiDBとGolangを使用してシンプルなCRUDアプリを構築する](/develop/dev-guide-sample-application-golang.md)     |
| 行け                      | [ビーゴ](https://github.com/beego/beego)                          | v2.0.3           | 満杯      | 該当なし                                                   | 該当なし                                                                                     |
| 行け                      | [アッパー/db](https://github.com/upper/db)                         | v4.5.2           | 満杯      | 該当なし                                                   | 該当なし                                                                                     |
| 行け                      | [xorm](https://gitea.com/xorm/xorm)                            | v1.3.1           | 満杯      | 該当なし                                                   | 該当なし                                                                                     |
| Java                    | [Hibernate](https://hibernate.org/orm/)                        | 6.1.0。最終         | 満杯      | 該当なし                                                   | [TiDBとJavaを使用してシンプルなCRUDアプリを構築する](/develop/dev-guide-sample-application-java.md)         |
| Java                    | [MyBatis](https://mybatis.org/mybatis-3/)                      | v3.5.10          | 満杯      | 該当なし                                                   | [TiDBとJavaを使用してシンプルなCRUDアプリを構築する](/develop/dev-guide-sample-application-java.md)         |
| Java                    | [Spring Data JPA](https://spring.io/projects/spring-data-jpa/) | 2.7.2            | 満杯      | 該当なし                                                   | [SpringBootを使用してTiDBアプリケーションを構築する](/develop/dev-guide-sample-application-spring-boot.md) |
| Java                    | [jOOQ](https://github.com/jOOQ/jOOQ)                           | v3.16.7（オープンソース） | 満杯      | 該当なし                                                   | 該当なし                                                                                     |
| JavaScript / TypeScript | [続編](https://www.npmjs.com/package/sequelize)                  | v6.20.1          | 互換性     | 該当なし                                                   | 該当なし                                                                                     |
| JavaScript / TypeScript | [Knex.js](https://knexjs.org/)                                 | v1.0.7           | 互換性     | 該当なし                                                   | 該当なし                                                                                     |
| JavaScript / TypeScript | [Prismaクライアント](https://www.prisma.io/)                         | 3.15.1           | 互換性     | 該当なし                                                   | 該当なし                                                                                     |
| JavaScript / TypeScript | [TypeORM](https://www.npmjs.com/package/typeorm)               | v0.3.6           | 互換性     | 該当なし                                                   | 該当なし                                                                                     |
| PHP                     | [laravel](https://laravel.com/)                                | v9.1.10          | 互換性     | [laravel-tidb](https://github.com/colopl/laravel-tidb) | 該当なし                                                                                     |
| Python                  | [ジャンゴ](https://pypi.org/project/Django/)                       | v4.0.5           | 互換性     | 該当なし                                                   | 該当なし                                                                                     |
| Python                  | [ピーウィー](https://github.com/coleifer/peewee/)                   | v3.14.10         | 互換性     | 該当なし                                                   | 該当なし                                                                                     |
| Python                  | [PonyORM](https://ponyorm.org/)                                | v0.7.16          | 互換性     | 該当なし                                                   | 該当なし                                                                                     |
| Python                  | [SQLAlchemy](https://www.sqlalchemy.org/)                      | v1.4.37          | 互換性     | 該当なし                                                   | 該当なし                                                                                     |

## GUI {#gui}

| GUI                                        | 最新のテスト済みバージョン | サポートレベル | チュートリアル |
| ------------------------------------------ | ------------- | ------- | ------- |
| [DBeaver](https://dbeaver.io/)             | 22.1.0        | 互換性     | 該当なし    |
| [MySQL用のNavicat](https://www.navicat.com/) | 16.0.14       | 互換性     | 該当なし    |

| IDE                                              | 最新のテスト済みバージョン | サポートレベル | チュートリアル |
| ------------------------------------------------ | ------------- | ------- | ------- |
| [DataGrip](https://www.jetbrains.com/datagrip/)  | 該当なし          | 互換性     | 該当なし    |
| [IntelliJ アイデア](https://www.jetbrains.com/idea/) | 該当なし          | 互換性     | 該当なし    |
