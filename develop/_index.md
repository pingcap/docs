---
title: Developer Guide Overview
summary: TiDB Cloudおよび TiDB Self-Managed の開発者ガイドの概要を紹介します。
aliases: ['/ja/tidb/stable/dev-guide-overview/','/ja/tidbcloud/dev-guide-overview/']
---

# 開発者ガイドの概要 {#developer-guide-overview}

[ティドブ](https://github.com/pingcap/tidb)は、ハイブリッド トランザクションおよび分析処理 (HTAP) ワークロードをサポートするオープン ソースの分散 SQL データベースです。

このガイドは、アプリケーション開発者が TiDB への接続、データベースの設計、データの書き込みとクエリ、TiDB 上での信頼性の高い高パフォーマンスのアプリケーションの構築方法を迅速に習得するのに役立ちます。

> **注記：**
>
> このガイドはアプリケーション開発者向けに書かれていますが、TiDB の内部動作に興味がある場合や、TiDB 開発に参加したい場合は、TiDB の詳細情報については[TiDB カーネル開発ガイド](https://pingcap.github.io/tidb-dev-guide/)をお読みください。

## 言語とフレームワーク別のガイド {#guides-by-language-and-framework}

サンプル コード付きのガイドに従って、使用する言語でアプリケーションを構築します。

<DevLangAccordion label="JavaScript" defaultExpanded>
<DevToolCard title="Serverless Driver (beta)" logo="tidb" docLink="/developer/serverless-driver" githubLink="https://github.com/tidbcloud/serverless-js">

エッジ環境から HTTPS 経由で TiDB に接続します。

</DevToolCard>
<DevToolCard title="Next.js" logo="nextjs" docLink="/developer/dev-guide-sample-application-nextjs" githubLink="https://github.com/vercel/next.js">

Next.js を mysql2 で TiDB に接続します。

</DevToolCard>
<DevToolCard title="Prisma" logo="prisma" docLink="/developer/dev-guide-sample-application-nodejs-prisma" githubLink="https://github.com/prisma/prisma">

Prisma ORM を使用して TiDB に接続します。

</DevToolCard>
<DevToolCard title="TypeORM" logo="typeorm" docLink="/developer/dev-guide-sample-application-nodejs-typeorm" githubLink="https://github.com/typeorm/typeorm">

TypeORM を使用して TiDB に接続します。

</DevToolCard>
<DevToolCard title="Sequelize" logo="sequelize" docLink="/developer/dev-guide-sample-application-nodejs-sequelize" githubLink="https://github.com/sequelize/sequelize">

Sequelize ORM を使用して TiDB に接続します。

</DevToolCard>
<DevToolCard title="mysql.js" logo="mysql" docLink="/developer/dev-guide-sample-application-nodejs-mysqljs" githubLink="https://github.com/mysqljs/mysql">

mysql.js モジュールを備えた Node.js を TiDB に接続します。

</DevToolCard>
<DevToolCard title="node-mysql2" logo="mysql" docLink="/developer/dev-guide-sample-application-nodejs-mysql2" githubLink="https://github.com/sidorares/node-mysql2">

node-mysql2 モジュールを備えた Node.js を TiDB に接続します。

</DevToolCard>
<DevToolCard title="AWS Lambda" logo="aws-lambda" docLink="/developer/dev-guide-sample-application-aws-lambda" githubLink="https://github.com/sidorares/node-mysql2">

mysql2 を含む AWS Lambda 関数を TiDB に接続します。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Python" defaultExpanded>
<DevToolCard title="Django" logo="django" docLink="/developer/dev-guide-sample-application-python-django" githubLink="https://github.com/pingcap/django-tidb">

django-tidb を使用して Django アプリケーションを TiDB に接続します。

</DevToolCard>
<DevToolCard title="MySQL Connector/Python" logo="python" docLink="/developer/dev-guide-sample-application-python-mysql-connector" githubLink="https://github.com/mysql/mysql-connector-python">

公式 MySQL パッケージを使用して TiDB に接続します。

</DevToolCard>
<DevToolCard title="PyMySQL" logo="python" docLink="/developer/dev-guide-sample-application-python-pymysql" githubLink="https://github.com/PyMySQL/PyMySQL">

PyMySQL パッケージを使用して TiDB に接続します。

</DevToolCard>
<DevToolCard title="mysqlclient" logo="python" docLink="/developer/dev-guide-sample-application-python-mysqlclient" githubLink="https://github.com/PyMySQL/mysqlclient">

mysqlclient パッケージを使用して TiDB に接続します。

</DevToolCard>
<DevToolCard title="SQLAlchemy" logo="sqlalchemy" docLink="/developer/dev-guide-sample-application-python-sqlalchemy" githubLink="https://github.com/sqlalchemy/sqlalchemy">

SQLAlchemy ORM を使用して TiDB に接続します。

</DevToolCard>
<DevToolCard title="peewee" logo="peewee" docLink="/developer/dev-guide-sample-application-python-peewee" githubLink="https://github.com/coleifer/peewee">

Peewee ORM を使用して TiDB に接続します。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Java">
<DevToolCard title="JDBC" logo="java" docLink="/developer/dev-guide-sample-application-java-jdbc" githubLink="https://github.com/mysql/mysql-connector-j">

JDBC (MySQL Connector/J) を使用して TiDB に接続します。

</DevToolCard>
<DevToolCard title="MyBatis" logo="mybatis" docLink="/developer/dev-guide-sample-application-java-mybatis" githubLink="https://github.com/mybatis/mybatis-3">

MyBatis ORM を使用して TiDB に接続します。

</DevToolCard>
<DevToolCard title="Hibernate" logo="hibernate" docLink="/developer/dev-guide-sample-application-java-hibernate" githubLink="https://github.com/hibernate/hibernate-orm">

Hibernate ORM を使用して TiDB に接続します。

</DevToolCard>
<DevToolCard title="Spring Boot" logo="spring" docLink="/developer/dev-guide-sample-application-java-spring-boot" githubLink="https://github.com/spring-projects/spring-data-jpa">

Spring Data JPA を使用した Spring ベースのアプリケーションを TiDB に接続します。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Go">
<DevToolCard title="Go-MySQL-Driver" logo="go" docLink="/developer/dev-guide-sample-application-golang-sql-driver" githubLink="https://github.com/go-sql-driver/mysql">

Go 用の MySQL ドライバーを使用して TiDB に接続します。

</DevToolCard>
<DevToolCard title="GORM" logo="gorm" docLink="/developer/dev-guide-sample-application-golang-gorm" githubLink="https://github.com/go-gorm/gorm">

GORM を使用して TiDB に接続します。

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Ruby">
<DevToolCard title="Ruby on Rails" logo="rails" docLink="/developer/dev-guide-sample-application-ruby-rails" githubLink="https://github.com/rails/rails/tree/main/activerecord">

Active Record ORM を備えた Ruby on Rails アプリケーションを TiDB に接続します。

</DevToolCard>
<DevToolCard title="mysql2" logo="ruby" docLink="/developer/dev-guide-sample-application-ruby-mysql2" githubLink="https://github.com/brianmario/mysql2">

mysql2 ドライバーを使用して TiDB に接続します。

</DevToolCard>
</DevLangAccordion>

これらのガイドに加えて、PingCAP はコミュニティと協力して[サードパーティのMySQLドライバ、ORM、ツール](/develop/dev-guide-third-party-support.md)サポートします。

## MySQLクライアントソフトウェアを使用する {#use-mysql-client-software}

TiDBはMySQL互換データベースであるため、多くの使い慣れたクライアントソフトウェアツールを使用してTiDBに接続し、データベースを管理できます。また、<a href="/tidbcloud/get-started-with-cli">コマンドラインツール</a>を使用してデータベースに接続し、管理することもできます。

<DevToolGroup>
<DevToolCard title="MySQL Workbench" logo="mysql-1" docLink="/developer/dev-guide-gui-mysql-workbench">

MySQL Workbench を使用して TiDB データベースに接続および管理します。

</DevToolCard>
<DevToolCard title="Visual Studio Code" logo="vscode" docLink="/developer/dev-guide-gui-vscode-sqltools">

VS Code の SQLTools 拡張機能を使用して、TiDB データベースに接続および管理します。

</DevToolCard>
<DevToolCard title="DBeaver" logo="dbeaver" docLink="/developer/dev-guide-gui-dbeaver">

DBeaver を使用して TiDB データベースに接続し、管理します。

</DevToolCard>
<DevToolCard title="DataGrip" logo="datagrip" docLink="/developer/dev-guide-gui-datagrip">

JetBrains の DataGrip を使用して TiDB データベースに接続し、管理します。

</DevToolCard>
</DevToolGroup>

## 追加リソース {#additional-resources}

TiDB を使用した開発に関するその他のトピックを学習します。

-   <a href="/tidbcloud/get-started-with-cli">TiDB Cloud CLI</a>を使用して、アプリケーションを開発、管理、デプロイします。
-   TiDB Cloudとの人気の<a href="/tidbcloud/integrate-tidbcloud-with-airbyte">サービス統合</a>をご覧ください。
-   [TiDB データベース開発リファレンス](/develop/dev-guide-schema-design-overview.md)に従って、データとスキーマを設計、操作、最適化、およびトラブルシューティングします。
-   無料のオンラインコース[TiDBの紹介](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide)を受講してください。
