---
title: Third-Party Tools Supported by TiDB
summary: TiDB でサポートされているサードパーティ ツールについて説明します。
aliases: ['/ja/tidb/stable/dev-guide-third-party-support/','/ja/tidb/dev/dev-guide-third-party-support/','/ja/tidbcloud/dev-guide-third-party-support/']
---

# TiDB でサポートされているサードパーティ ツール {#third-party-tools-supported-by-tidb}

> **注記：**
>
> このドキュメントでは、TiDBでサポートされている一般的な[サードパーティツール](https://en.wikipedia.org/wiki/Third-party_source)をリストしています。その他のサードパーティ製ツールはリストされていませんが、これはサポートされていないからではなく、PingCAPがそれらのツールがTiDBと互換性のない機能を使用しているかどうかを確認できないためです。

TiDB は[MySQLプロトコルとの高い互換性](/mysql-compatibility.md)あるため、MySQL ドライバ、ORM フレームワーク、および MySQL に対応するその他のツールのほとんどは TiDB と互換性があります。このドキュメントでは、これらのツールと TiDB のサポートレベルに焦点を当てます。

## サポートレベル {#support-level}

PingCAP はコミュニティと連携し、サードパーティ ツールに対して次のサポート レベルを提供します。

-   ***完全***：TiDB は対応するサードパーティ製ツールのほとんどの機能と既に互換性があり、最新バージョンとの互換性も維持していることを示します。PingCAP は、ツールの最新バージョンとの互換性テストを定期的に実施します。
-   ***互換***：対応するサードパーティ製ツールがMySQLに適合しており、TiDBはMySQLプロトコルと高い互換性があるため、TiDBはツールのほとんどの機能を使用できることを示します。ただし、PingCAPはツールのすべての機能について完全なテストを完了していないため、予期しない動作が発生する可能性があります。

> **注記：**
>
> 特に指定がない限り、**Driver**または**ORM フレームワーク**では[アプリケーションの再試行とエラー処理](/develop/dev-guide-transaction-troubleshoot.md#application-retry-and-error-handling)のサポートは含まれません。

このドキュメントに記載されているツールを使用して TiDB に接続する際に問題が発生した場合は、詳細を記載した[問題](https://github.com/pingcap/tidb/issues/new?assignees=&#x26;labels=type%2Fquestion&#x26;template=general-question.md)を GitHub に送信して、このツールのサポートを促進してください。

## Driver {#driver}

| 言語   | Driver                                                        | 最新のテスト済みバージョン | サポートレベル | TiDBアダプタ                                                                                                                                                                                 | チュートリアル                                                                                    |
| ---- | ------------------------------------------------------------- | ------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| 行く   | [go-sql-driver/mysql](https://github.com/go-sql-driver/mysql) | バージョン1.6.0    | 満杯      | 該当なし                                                                                                                                                                                     | [Go-MySQL-Driver で TiDB に接続する](/develop/dev-guide-sample-application-golang-sql-driver.md) |
| Java | [MySQL コネクタ/J](https://dev.mysql.com/downloads/connector/j/)  | 8.0           | 満杯      | [pingcap/mysql-connector-j](/develop/dev-guide-choose-driver-or-orm.md#java-drivers) <br/> [pingcap/tidb-ロードバランス](/develop/dev-guide-choose-driver-or-orm.md#java-client-load-balancing) | [JDBC で TiDB に接続する](/develop/dev-guide-sample-application-java-jdbc.md)                    |

## ORM {#orm}

| 言語                    | ORMフレームワーク                                                            | 最新のテスト済みバージョン     | サポートレベル | TiDBアダプタ                                              | チュートリアル                                                                                            |
| --------------------- | --------------------------------------------------------------------- | ----------------- | ------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| 行く                    | [ゴーム](https://github.com/go-gorm/gorm)                                | バージョン1.23.5       | 満杯      | 該当なし                                                  | [GORMでTiDBに接続する](/develop/dev-guide-sample-application-golang-gorm.md)                             |
| 行く                    | [ビーゴ](https://github.com/beego/beego)                                 | バージョン2.0.3        | 満杯      | 該当なし                                                  | 該当なし                                                                                               |
| 行く                    | [上段/db](https://github.com/upper/db)                                  | バージョン4.5.2        | 満杯      | 該当なし                                                  | 該当なし                                                                                               |
| 行く                    | [xorm](https://gitea.com/xorm/xorm)                                   | バージョン1.3.1        | 満杯      | 該当なし                                                  | 該当なし                                                                                               |
| Java                  | [休止状態](https://hibernate.org/orm/)                                    | 6.1.0.最終版         | 満杯      | 該当なし                                                  | [Hibernate で TiDB に接続する](/develop/dev-guide-sample-application-java-hibernate.md)                  |
| Java                  | [マイバティス](https://mybatis.org/mybatis-3/)                              | バージョン3.5.10       | 満杯      | 該当なし                                                  | [MyBatisでTiDBに接続する](/develop/dev-guide-sample-application-java-mybatis.md)                         |
| Java                  | [スプリングデータ JPA](https://spring.io/projects/spring-data-jpa/)           | 2.7.2             | 満杯      | 該当なし                                                  | [Spring BootでTiDBに接続する](/develop/dev-guide-sample-application-java-spring-boot.md)                 |
| Java                  | [ジョーク](https://github.com/jOOQ/jOOQ)                                  | v3.16.7 (オープンソース) | 満杯      | 該当なし                                                  | 該当なし                                                                                               |
| ルビー                   | [アクティブレコード](https://guides.rubyonrails.org/active_record_basics.html) | バージョン7.0          | 満杯      | 該当なし                                                  | [RailsフレームワークとActiveRecord ORMを使用してTiDBに接続する](/develop/dev-guide-sample-application-ruby-rails.md) |
| JavaScript / タイプスクリプト | [続編](https://sequelize.org/)                                          | バージョン6.20.1       | 満杯      | 該当なし                                                  | [Sequelize で TiDB に接続する](/develop/dev-guide-sample-application-nodejs-sequelize.md)                |
| JavaScript / タイプスクリプト | [プリズマ](https://www.prisma.io/)                                        | 4.16.2            | 満杯      | 該当なし                                                  | [PrismaでTiDBに接続する](/develop/dev-guide-sample-application-nodejs-prisma.md)                         |
| JavaScript / タイプスクリプト | [タイプORM](https://typeorm.io/)                                         | v0.3.17           | 満杯      | 該当なし                                                  | [TypeORMでTiDBに接続する](/develop/dev-guide-sample-application-nodejs-typeorm.md)                       |
| パイソン                  | [ジャンゴ](https://www.djangoproject.com/)                                | バージョン4.2          | 満杯      | [django-tidb](https://github.com/pingcap/django-tidb) | [DjangoでTiDBに接続する](/develop/dev-guide-sample-application-python-django.md)                         |
| パイソン                  | [SQLアルケミー](https://www.sqlalchemy.org/)                               | バージョン1.4.37       | 満杯      | 該当なし                                                  | [SQLAlchemy で TiDB に接続する](/develop/dev-guide-sample-application-python-sqlalchemy.md)              |

## GUI {#gui}

| GUI                                                      | 最新のテスト済みバージョン | サポートレベル | チュートリアル                                                                      |
| -------------------------------------------------------- | ------------- | ------- | ---------------------------------------------------------------------------- |
| [養蜂家スタジオ](https://www.beekeeperstudio.io/)               | 4.3.0         | 満杯      | 該当なし                                                                         |
| [ジェットブレインズ データグリップ](https://www.jetbrains.com/datagrip/) | 2023年2月1日     | 満杯      | [JetBrains DataGrip で TiDB に接続する](/develop/dev-guide-gui-datagrip.md)        |
| [DBeaver](https://dbeaver.io/)                           | 23.0.3        | 満杯      | [DBeaverでTiDBに接続する](/develop/dev-guide-gui-dbeaver.md)                       |
| [ビジュアルスタジオコード](https://code.visualstudio.com/)           | 1.72.0        | 満杯      | [Visual Studio Code で TiDB に接続する](/develop/dev-guide-gui-vscode-sqltools.md) |
| [ナビキャット](https://www.navicat.com)                        | 17.1.6        | 満杯      | [NavicatでTiDBに接続する](/develop/dev-guide-gui-navicat.md)                       |

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
