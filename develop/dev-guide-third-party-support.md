---
title: Third-Party Tools Supported by TiDB
summary: Learn about third-party tools supported by TiDB.
---

# TiDB がサポートするサードパーティ ツール {#third-party-tools-supported-by-tidb}

> **注記：**
>
> このドキュメントでは、TiDB でサポートされる一般的な[サードパーティツール](https://en.wikipedia.org/wiki/Third-party_source)のみをリストします。他のサードパーティ ツールの一部はリストされていません。これは、それらがサポートされていないためではなく、TiDB と互換性のない機能を使用しているかどうか PingCAP が不明であるためです。

TiDB は[MySQLプロトコルとの高い互換性](/mysql-compatibility.md)なので、ほとんどの MySQL ドライバー、ORM フレームワーク、および MySQL に適応するその他のツールは TiDB と互換性があります。このドキュメントでは、これらのツールと TiDB のサポート レベルに焦点を当てます。

## サポートレベル {#support-level}

PingCAP はコミュニティと連携し、サードパーティ ツールに次のサポート レベルを提供します。

-   ***Full*** : TiDB が対応するサードパーティ ツールのほとんどの機能とすでに互換性があり、その新しいバージョンとの互換性が維持されていることを示します。 PingCAP は、ツールの最新バージョンとの互換性テストを定期的に実施します。
-   ***互換性***: 対応するサードパーティ ツールが MySQL に適合しており、TiDB が MySQL プロトコルと高い互換性があるため、TiDB はツールのほとんどの機能を使用できることを示します。ただし、PingCAP はツールのすべての機能について完全なテストを完了していないため、予期しない動作が発生する可能性があります。

> **注記：**
>
> 特に指定しない限り、**Driver**または**ORM フレームワーク**には[アプリケーションの再試行とエラー処理](/develop/dev-guide-transaction-troubleshoot.md#application-retry-and-error-handling)のサポートは含まれません。

このドキュメントに記載されているツールを使用して TiDB に接続するときに問題が発生した場合は、このツールのサポートを促進するための詳細を記載して GitHub に[問題](https://github.com/pingcap/tidb/issues/new?assignees=&#x26;labels=type%2Fquestion&#x26;template=general-question.md)を送信してください。

## Driver {#driver}

<table><thead><tr><th>言語</th><th>Driver</th><th>最新のテスト済みバージョン</th><th>サポートレベル</th><th>TiDBアダプター</th><th>チュートリアル</th></tr></thead><tbody><tr><td>行く</td><td><a href="https://github.com/go-sql-driver/mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">Go-MySQL-ドライバー</a></td><td>v1.6.0</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/dev/dev-guide-sample-application-golang-sql-driver">Go-MySQL-Driver を使用して TiDB に接続する</a></td></tr><tr><td>Java</td><td><a href="https://dev.mysql.com/downloads/connector/j/" target="_blank" referrerpolicy="no-referrer-when-downgrade">JDBC</a></td><td> 8.0</td><td>満杯</td><td><ul><li><a href="/tidb/dev/dev-guide-choose-driver-or-orm#java-drivers" data-href="/tidb/dev/dev-guide-choose-driver-or-orm#java-drivers">pingcap/mysql-connector-j</a></li><li> <a href="/tidb/dev/dev-guide-choose-driver-or-orm#tidb-loadbalance" data-href="/tidb/dev/dev-guide-choose-driver-or-orm#tidb-loadbalance">pingcap/tidb-loadbalance</a></li></ul></td><td> <a href="/tidb/dev/dev-guide-sample-application-java-jdbc">JDBC を使用して TiDB に接続する</a></td></tr></tbody></table>

## ORM {#orm}

<table><thead><tr><th>言語</th><th>ORMフレームワーク</th><th>最新のテスト済みバージョン</th><th>サポートレベル</th><th>TiDBアダプター</th><th>チュートリアル</th></tr></thead><tbody><tr><td rowspan="4">行く</td><td><a href="https://github.com/go-gorm/gorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">ゴーム</a></td><td>v1.23.5</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/dev/dev-guide-sample-application-golang-gorm">GORM を使用して TiDB に接続する</a></td></tr><tr><td><a href="https://github.com/beego/beego" target="_blank" referrerpolicy="no-referrer-when-downgrade">ビーゴ</a></td><td>v2.0.3</td><td>満杯</td><td>該当なし</td><td>該当なし</td></tr><tr><td> <a href="https://github.com/upper/db" target="_blank" referrerpolicy="no-referrer-when-downgrade">アッパー/データベース</a></td><td>v4.5.2</td><td>満杯</td><td>該当なし</td><td>該当なし</td></tr><tr><td><a href="https://gitea.com/xorm/xorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">xorm</a></td><td> v1.3.1</td><td>満杯</td><td>該当なし</td><td>該当なし</td></tr><tr><td rowspan="4">Java</td><td><a href="https://hibernate.org/orm/" target="_blank" referrerpolicy="no-referrer-when-downgrade">休止状態</a></td><td>6.1.0.最終回</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/dev/dev-guide-sample-application-java-hibernate">Hibernate で TiDB に接続する</a></td></tr><tr><td><a href="https://mybatis.org/mybatis-3/" target="_blank" referrerpolicy="no-referrer-when-downgrade">マイバティス</a></td><td>v3.5.10</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/dev/dev-guide-sample-application-java-mybatis">MyBatis を使用して TiDB に接続する</a></td></tr><tr><td><a href="https://spring.io/projects/spring-data-jpa/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Spring Data JPA</a></td><td> 2.7.2</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/dev/dev-guide-sample-application-java-spring-boot">Spring Boot を使用して TiDB に接続する</a></td></tr><tr><td> <a href="https://github.com/jOOQ/jOOQ" target="_blank" referrerpolicy="no-referrer-when-downgrade">ジョーク</a></td><td>v3.16.7 (オープンソース)</td><td>満杯</td><td>該当なし</td><td>該当なし</td></tr><tr><td>ルビー</td><td><a href="https://guides.rubyonrails.org/active_record_basics.html" target="_blank" referrerpolicy="no-referrer-when-downgrade">アクティブなレコード</a></td><td>v7.0</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/dev/dev-guide-sample-application-ruby-rails">Rails Framework と ActiveRecord ORM を使用して TiDB に接続する</a></td></tr><tr><td rowspan="3">JavaScript / TypeScript</td><td><a href="https://sequelize.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">続編</a></td><td>v6.20.1</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/dev/dev-guide-sample-application-nodejs-sequelize">Sequelize で TiDB に接続する</a></td></tr><tr><td><a href="https://www.prisma.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">プリズマ</a></td><td>4.16.2</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/dev/dev-guide-sample-application-nodejs-prisma">Prisma を使用して TiDB に接続する</a></td></tr><tr><td><a href="https://typeorm.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">TypeORM</a></td><td> v0.3.17</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/dev/dev-guide-sample-application-nodejs-typeorm">TypeORM で TiDB に接続する</a></td></tr><tr><td rowspan="2">パイソン</td><td><a href="https://pypi.org/project/Django/" target="_blank" referrerpolicy="no-referrer-when-downgrade">ジャンゴ</a></td><td>v4.2</td><td>満杯</td><td><a href="https://github.com/pingcap/django-tidb" target="_blank" referrerpolicy="no-referrer-when-downgrade">ジャンゴティブ</a></td><td><a href="/tidb/dev/dev-guide-sample-application-python-django">Django を使用して TiDB に接続する</a></td></tr><tr><td><a href="https://www.sqlalchemy.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">SQLアルケミー</a></td><td>v1.4.37</td><td>満杯</td><td>該当なし</td><td><a href="/tidb/dev/dev-guide-sample-application-python-sqlalchemy">SQLAlchemy を使用して TiDB に接続する</a></td></tr></tbody></table>

## GUI {#gui}

| GUI                                                      | 最新のテスト済みバージョン | サポートレベル | チュートリアル                                                                          |
| -------------------------------------------------------- | ------------- | ------- | -------------------------------------------------------------------------------- |
| [JetBrains データグリップ](https://www.jetbrains.com/datagrip/) | 2023.2.1      | 満杯      | [JetBrains DataGrip を使用して TiDB に接続する](/develop/dev-guide-gui-datagrip.md)        |
| [Dビーバー](https://dbeaver.io/)                             | 23.0.3        | 満杯      | [DBeaver を使用して TiDB に接続する](/develop/dev-guide-gui-dbeaver.md)                    |
| [Visual Studioコード](https://code.visualstudio.com/)       | 1.72.0        | 満杯      | [Visual Studio Code を使用して TiDB に接続する](/develop/dev-guide-gui-vscode-sqltools.md) |
