---
title: Third-Party Tools Supported by TiDB
summary: TiDB でサポートされているサードパーティ ツールについて説明します。
aliases: ['/ja/tidb/stable/dev-guide-third-party-support/','/ja/tidbcloud/dev-guide-third-party-support/']
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

<table><thead><tr><th>言語</th><th>Driver</th><th>最新のテスト済みバージョン</th><th>サポートレベル</th><th>TiDBアダプタ</th><th>チュートリアル</th></tr></thead><tbody><tr><td>行く</td><td><a href="https://github.com/go-sql-driver/mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">Go-MySQL-ドライバー</a></td><td>バージョン1.6.0</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/v8.5/dev-guide-sample-application-golang-sql-driver">Go-MySQL-Driver で TiDB に接続する</a></td></tr><tr><td>Java</td><td><a href="https://dev.mysql.com/downloads/connector/j/" target="_blank" referrerpolicy="no-referrer-when-downgrade">JDBC</a></td><td> 8.0</td><td>満杯</td><td><ul><li><a href="/tidb/v8.5/dev-guide-choose-driver-or-orm#java-drivers" data-href="/tidb/v8.5/dev-guide-choose-driver-or-orm#java-drivers">pingcap/mysql-connector-j</a></li><li> <a href="/tidb/v8.5/dev-guide-choose-driver-or-orm#tidb-loadbalance" data-href="/tidb/v8.5/dev-guide-choose-driver-or-orm#tidb-loadbalance">pingcap/tidb-ロードバランス</a></li></ul></td><td><a href="/tidb/v8.5/dev-guide-sample-application-java-jdbc">JDBC で TiDB に接続する</a></td></tr></tbody></table>

## ORM {#orm}

<table><thead><tr><th>言語</th><th>ORMフレームワーク</th><th>最新のテスト済みバージョン</th><th>サポートレベル</th><th>TiDBアダプタ</th><th>チュートリアル</th></tr></thead><tbody><tr><td rowspan="4">行く</td><td><a href="https://github.com/go-gorm/gorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">ゴーム</a></td><td>バージョン1.23.5</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/v8.5/dev-guide-sample-application-golang-gorm">GORMでTiDBに接続する</a></td></tr><tr><td><a href="https://github.com/beego/beego" target="_blank" referrerpolicy="no-referrer-when-downgrade">ビーゴ</a></td><td>バージョン2.0.3</td><td>満杯</td><td>該当なし</td><td>該当なし</td></tr><tr><td> <a href="https://github.com/upper/db" target="_blank" referrerpolicy="no-referrer-when-downgrade">上段/db</a></td><td>バージョン4.5.2</td><td>満杯</td><td>該当なし</td><td>該当なし</td></tr><tr><td><a href="https://gitea.com/xorm/xorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">xorm</a></td><td>バージョン1.3.1</td><td>満杯</td><td>該当なし</td><td>該当なし</td></tr><tr><td rowspan="4">Java</td><td><a href="https://hibernate.org/orm/" target="_blank" referrerpolicy="no-referrer-when-downgrade">休止状態</a></td><td>6.1.0.最終版</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/v8.5/dev-guide-sample-application-java-hibernate">Hibernate で TiDB に接続する</a></td></tr><tr><td><a href="https://mybatis.org/mybatis-3/" target="_blank" referrerpolicy="no-referrer-when-downgrade">マイバティス</a></td><td>バージョン3.5.10</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/v8.5/dev-guide-sample-application-java-mybatis">MyBatisでTiDBに接続する</a></td></tr><tr><td><a href="https://spring.io/projects/spring-data-jpa/" target="_blank" referrerpolicy="no-referrer-when-downgrade">スプリングデータ JPA</a></td><td> 2.7.2</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/v8.5/dev-guide-sample-application-java-spring-boot">Spring BootでTiDBに接続する</a></td></tr><tr><td> <a href="https://github.com/jOOQ/jOOQ" target="_blank" referrerpolicy="no-referrer-when-downgrade">ジョーク</a></td><td>v3.16.7 (オープンソース)</td><td>満杯</td><td>該当なし</td><td>該当なし</td></tr><tr><td>ルビー</td><td><a href="https://guides.rubyonrails.org/active_record_basics.html" target="_blank" referrerpolicy="no-referrer-when-downgrade">アクティブレコード</a></td><td>バージョン7.0</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/v8.5/dev-guide-sample-application-ruby-rails">RailsフレームワークとActiveRecord ORMを使用してTiDBに接続する</a></td></tr><tr><td rowspan="3">JavaScript / タイプスクリプト</td><td><a href="https://sequelize.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">続編</a></td><td>バージョン6.20.1</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/v8.5/dev-guide-sample-application-nodejs-sequelize">Sequelize で TiDB に接続する</a></td></tr><tr><td><a href="https://www.prisma.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">プリズマ</a></td><td>4.16.2</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/v8.5/dev-guide-sample-application-nodejs-prisma">PrismaでTiDBに接続する</a></td></tr><tr><td><a href="https://typeorm.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">タイプORM</a></td><td> v0.3.17</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/v8.5/dev-guide-sample-application-nodejs-typeorm">TypeORMでTiDBに接続する</a></td></tr><tr><td rowspan="2">パイソン</td><td><a href="https://pypi.org/project/Django/" target="_blank" referrerpolicy="no-referrer-when-downgrade">ジャンゴ</a></td><td>バージョン4.2</td><td>満杯</td><td><a href="https://github.com/pingcap/django-tidb" target="_blank" referrerpolicy="no-referrer-when-downgrade">django-tidb</a></td><td> <a href="/tidb/v8.5/dev-guide-sample-application-python-django">DjangoでTiDBに接続する</a></td></tr><tr><td><a href="https://www.sqlalchemy.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">SQLアルケミー</a></td><td>バージョン1.4.37</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/v8.5/dev-guide-sample-application-python-sqlalchemy">SQLAlchemy で TiDB に接続する</a></td></tr></tbody></table>

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
