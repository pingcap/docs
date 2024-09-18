---
title: Developer Guide Overview
summary: TiDB Cloudおよび TiDB Self-Managed の開発者ガイドの概要を紹介します。
---

# 開発者ガイドの概要 {#developer-guide-overview}

<CustomContent platform="tidb-cloud">

<IntroHero title="TiDB Cloudの基礎を学ぶ" content="TiDB Cloud is the fully-managed service built on top of TiDB, which is highly compatible with the MySQL protocol and supports most MySQL syntax and features." videoTitle="TiDB Cloud in 3 minutes"><IntroHeroVideo src="https://www.youtube.com/embed/skCV9BEmjbo?autoplay=1" title="3分でわかるTiDBクラウド" /></IntroHero>

## 言語とフレームワーク別のガイド {#guides-by-language-and-framework}

サンプル コード付きのガイドに従って、使用する言語でアプリケーションを構築します。

<DevLangAccordion label="JavaScript" defaultExpanded><DevToolCard title="サーバーレス ドライバー (ベータ版)" logo="tidb" docLink="/tidbcloud/serverless-driver" githubLink="https://github.com/tidbcloud/serverless-js">

Edge Function で HTTPS 経由でTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="次" logo="nextjs" docLink="/tidbcloud/dev-guide-sample-application-nextjs" githubLink="https://github.com/vercel/next.js">

Next.js を mysql2 でTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="プリズマ" logo="prisma" docLink="/tidbcloud/dev-guide-sample-application-nodejs-prisma" githubLink="https://github.com/prisma/prisma">

Prisma ORM を使用してTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="タイプORM" logo="typeorm" docLink="/tidbcloud/dev-guide-sample-application-nodejs-typeorm" githubLink="https://github.com/typeorm/typeorm">

TypeORM を使用してTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="続編" logo="sequelize" docLink="/tidbcloud/dev-guide-sample-application-nodejs-sequelize" githubLink="https://github.com/sequelize/sequelize">

Sequelize ORM を使用してTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="js の" logo="mysql" docLink="/tidbcloud/dev-guide-sample-application-nodejs-mysqljs" githubLink="https://github.com/mysqljs/mysql">

mysql.js モジュールを備えた Node.js をTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="ノード-mysql2" logo="mysql" docLink="/tidbcloud/dev-guide-sample-application-nodejs-mysql2" githubLink="https://github.com/sidorares/node-mysql2">

node-mysql2 モジュールを備えた Node.js をTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="AWS ラムダ" logo="aws-lambda" docLink="/tidbcloud/dev-guide-sample-application-aws-lambda" githubLink="https://github.com/sidorares/node-mysql2">

mysql2 を含む AWS Lambda 関数をTiDB Cloudに接続します。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Python" defaultExpanded><DevToolCard title="ジャンゴ" logo="django" docLink="/tidbcloud/dev-guide-sample-application-python-django" githubLink="https://github.com/pingcap/django-tidb">

django-tidb を使用して Django アプリケーションをTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="MySQL コネクタ/Python" logo="python" docLink="/tidbcloud/dev-guide-sample-application-python-mysql-connector" githubLink="https://github.com/mysql/mysql-connector-python">

MySQL 公式パッケージを使用してTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="pyMySQL の" logo="python" docLink="/tidbcloud/dev-guide-sample-application-python-pymysql" githubLink="https://github.com/PyMySQL/PyMySQL">

PyMySQL パッケージを使用してTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="mysqlクライアント" logo="python" docLink="/tidbcloud/dev-guide-sample-application-python-mysqlclient" githubLink="https://github.com/PyMySQL/mysqlclient">

mysqlclient パッケージを使用してTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="SQLアルケミー" logo="sqlalchemy" docLink="/tidbcloud/dev-guide-sample-application-python-sqlalchemy" githubLink="https://github.com/sqlalchemy/sqlalchemy">

SQLAlchemy ORM を使用してTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="ピーウィー" logo="peewee" docLink="/tidbcloud/dev-guide-sample-application-python-peewee" githubLink="https://github.com/coleifer/peewee">

Peewee ORM を使用してTiDB Cloudに接続します。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Java"><DevToolCard title="ODBC ドライバ" logo="java" docLink="/tidbcloud/dev-guide-sample-application-java-jdbc" githubLink="https://github.com/mysql/mysql-connector-j">

JDBC (MySQL Connector/J) を使用してTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="マイバティス" logo="mybatis" docLink="/tidbcloud/dev-guide-sample-application-java-mybatis" githubLink="https://github.com/mybatis/mybatis-3">

MyBatis ORM を使用してTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="休止状態" logo="hibernate" docLink="/tidbcloud/dev-guide-sample-application-java-hibernate" githubLink="https://github.com/hibernate/hibernate-orm">

Hibernate ORM を使用してTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="スプリングブート" logo="spring" docLink="/tidbcloud/dev-guide-sample-application-java-spring-boot" githubLink="https://github.com/spring-projects/spring-data-jpa">

Spring Data JPA を使用した Spring ベースのアプリケーションをTiDB Cloudに接続します。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Go"><DevToolCard title="Go-MySQL-ドライバー" logo="go" docLink="/tidbcloud/dev-guide-sample-application-golang-sql-driver" githubLink="https://github.com/go-sql-driver/mysql">

Go 用の MySQL ドライバーを使用してTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="ゴーム" logo="gorm" docLink="/tidbcloud/dev-guide-sample-application-golang-gorm" githubLink="https://github.com/go-gorm/gorm">

GORM を使用してTiDB Cloudに接続します。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Ruby"><DevToolCard title="ルビーオンレール" logo="rails" docLink="/tidbcloud/dev-guide-sample-application-ruby-rails" githubLink="https://github.com/rails/rails/tree/main/activerecord">

Active Record ORM を備えた Ruby on Rails アプリケーションをTiDB Cloudに接続します。

</DevToolCard><DevToolCard title="マイSQL2" logo="ruby" docLink="/tidbcloud/dev-guide-sample-application-ruby-mysql2" githubLink="https://github.com/brianmario/mysql2">

mysql2 ドライバーを使用してTiDB Cloudに接続します。

</DevToolCard>
</DevLangAccordion>

これらのガイドに加えて、PingCAP はコミュニティと協力して[サードパーティのMySQLドライバ、ORM、ツールをサポートする](/develop/dev-guide-third-party-support.md)に取り組んでいます。

## MySQLクライアントソフトウェアを使用する {#use-mysql-client-software}

TiDB は MySQL 互換のデータベースであるため、多くのクライアント ソフトウェア ツールを使用してTiDB Cloudに接続し、これまでと同じようにデータベースを管理できます。または、<a href="/tidbcloud/get-started-with-cli">コマンド ライン ツールを</a>使用してデータベースに接続し、管理することもできます。

<DevToolGroup><DevToolCard title="MySQL ワークベンチ" logo="mysql-1" docLink="/tidbcloud/dev-guide-gui-mysql-workbench">

MySQL Workbench を使用してTiDB Cloudデータベースに接続し、管理します。

</DevToolCard><DevToolCard title="ビジュアルスタジオコード" logo="vscode" docLink="/tidbcloud/dev-guide-gui-vscode-sqltools">

VSCode の SQLTools 拡張機能を使用して、 TiDB Cloudデータベースに接続および管理します。

</DevToolCard><DevToolCard title="DBeaver" logo="dbeaver" docLink="/tidbcloud/dev-guide-gui-dbeaver">

DBeaver を使用してTiDB Cloudデータベースに接続し、管理します。

</DevToolCard><DevToolCard title="データグリップ" logo="datagrip" docLink="/tidbcloud/dev-guide-gui-datagrip">

JetBrains の DataGrip を使用してTiDB Cloudデータベースに接続し、管理します。

</DevToolCard>
</DevToolGroup>

## 追加リソース {#additional-resources}

TiDB Cloudを使用した開発に関するその他のトピックを学習します。

-   <a href="/tidbcloud/get-started-with-cli">TiDB Cloud CLI を</a>使用して、アプリケーションを開発、管理、デプロイします。
-   TiDB Cloudとの一般的な<a href="/tidbcloud/integrate-tidbcloud-with-airbyte">サービス統合</a>を調べてください。
-   [TiDB データベース開発リファレンス](/develop/dev-guide-schema-design-overview.md)使用して、データとスキーマを設計、操作、最適化、トラブルシューティングします。
-   無料のオンラインコース[TiDB の紹介](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide)に従ってください。

</CustomContent>

<CustomContent platform="tidb">

このガイドはアプリケーション開発者向けに書かれていますが、TiDB の内部動作に興味がある場合や TiDB 開発に参加したい場合は、TiDB の詳細については[TiDB カーネル開発ガイド](https://pingcap.github.io/tidb-dev-guide/)をお読みください。

このチュートリアルでは、TiDB を使用してアプリケーションをすばやく構築する方法、TiDB の考えられる使用例、一般的な問題の処理方法を説明します。

このページを読む前に、 [TiDB データベース プラットフォームのクイック スタート ガイド](/quick-start-with-tidb.md)を読むことをお勧めします。

## TiDBの基礎 {#tidb-basics}

TiDB の使用を開始する前に、TiDB の動作に関するいくつかの重要なメカニズムを理解する必要があります。

-   TiDB でのトランザクションの仕組みを理解するには[TiDBトランザクションの概要](/transaction-overview.md) 、アプリケーション開発に必要なトランザクションの知識については[アプリケーション開発者向けトランザクションノート](/develop/dev-guide-transaction-overview.md)読んでください。
-   [アプリケーションがTiDBとやりとりする方法](#the-way-applications-interact-with-tidb)理解する。
-   分散データベース TiDB およびTiDB Cloud を構築するためのコア コンポーネントと概念を学習するには、無料のオンライン コース[TiDB の紹介](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide)を参照してください。

## TiDB トランザクション メカニズム {#tidb-transaction-mechanisms}

TiDB は分散トランザクションをサポートし、モード[楽観的取引](/optimistic-transaction.md)と[悲観的取引](/pessimistic-transaction.md)両方を提供します。現在のバージョンの TiDB では、デフォルトで**悲観的トランザクション**モードが使用され、従来のモノリシック データベース (MySQL など) と同様に TiDB でトランザクションを実行できます。

[`BEGIN`](/sql-statements/sql-statement-begin.md)使用してトランザクションを開始したり、 `BEGIN PESSIMISTIC`使用して**悲観的トランザクション**を明示的に指定したり、 `BEGIN OPTIMISTIC`使用して**楽観的トランザクション**を明示的に指定したりできます。その後、トランザクションをコミット ( [`COMMIT`](/sql-statements/sql-statement-commit.md) ) するか、ロールバック ( [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) ) することができます。

TiDB は、 `BEGIN`の開始から`COMMIT`または`ROLLBACK`の終了までのすべてのステートメントのアトミック性を保証します。つまり、この期間中に実行されるすべてのステートメントは、全体として成功するか失敗します。これは、アプリケーション開発に必要なデータの一貫性を確保するために使用されます。

**楽観的トランザクション**が何であるかよくわからない場合は、まだ使用し***ないで***ください。楽観的トランザクションでは、アプリケーションが`COMMIT`ステートメントによって返された[すべてのエラー](/error-codes.md)を正しく処理できることが求められるためです。アプリケーションが**楽観的トランザクション**をどのように処理するかよくわからない場合は、代わりに**悲観的トランザクションを**使用してください。

## アプリケーションがTiDBとやりとりする方法 {#the-way-applications-interact-with-tidb}

TiDB は MySQL プロトコルとの互換性が高く、 [ほとんどのMySQL構文と機能](/mysql-compatibility.md)サポートしているため、ほとんどの MySQL 接続ライブラリは TiDB と互換性があります。アプリケーション フレームワークまたは言語に PingCAP からの公式の適応がない場合は、MySQL のクライアント ライブラリを使用することをお勧めします。ますます多くのサードパーティ ライブラリが、TiDB のさまざまな機能を積極的にサポートしています。

TiDB は MySQL プロトコルおよび MySQL 構文と互換性があるため、MySQL をサポートする ORM のほとんどは TiDB とも互換性があります。

## 続きを読む {#read-more}

-   [クイックスタート](/develop/dev-guide-build-cluster-in-cloud.md)
-   [DriverまたはORMを選択](/develop/dev-guide-choose-driver-or-orm.md)
-   [TiDBに接続する](/develop/dev-guide-connect-to-tidb.md)
-   [データベーススキーマ設計](/develop/dev-guide-schema-design-overview.md)
-   [データの書き込み](/develop/dev-guide-insert-data.md)
-   [データの読み取り](/develop/dev-guide-get-data-from-single-table.md)
-   [トランザクション](/develop/dev-guide-transaction-overview.md)
-   [最適化する](/develop/dev-guide-optimize-sql-overview.md)
-   [アプリケーション例](/develop/dev-guide-sample-application-java-spring-boot.md)

## ヘルプが必要ですか? {#need-help}

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>
