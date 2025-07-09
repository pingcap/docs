---
title: Developer Guide Overview
summary: Introduce the overview of the developer guide for TiDB Cloud and TiDB Self-Managed.
---

# Developer Guide Overview

<CustomContent platform="tidb-cloud">

<IntroHero title="Learn TiDB Cloud basics" content="TiDB Cloud is the fully-managed service built on top of TiDB, which is highly compatible with the MySQL protocol and supports most MySQL syntax and features." videoTitle="TiDB Cloud in 3 minutes">
  <IntroHeroVideo src="https://www.youtube.com/embed/skCV9BEmjbo?autoplay=1" title="TiDB Cloud in 3 minutes" />
</IntroHero>

## Guides by language and framework

Build your application with the language you use by following the guides with sample codes.

<DevLangAccordion label="JavaScript" defaultExpanded>
<DevToolCard title="Serverless Driver (beta)" logo="tidb" docLink="/tidbcloud/serverless-driver" githubLink="https://github.com/tidbcloud/serverless-js">

Connect to TiDB Cloud over HTTPS from edge environments.

</DevToolCard>
<DevToolCard title="Next.js" logo="nextjs" docLink="/tidbcloud/dev-guide-sample-application-nextjs" githubLink="https://github.com/vercel/next.js">

Connect Next.js with mysql2 to TiDB Cloud.

</DevToolCard>
<DevToolCard title="Prisma" logo="prisma" docLink="/tidbcloud/dev-guide-sample-application-nodejs-prisma" githubLink="https://github.com/prisma/prisma">

Connect to TiDB Cloud with Prisma ORM.

</DevToolCard>
<DevToolCard title="TypeORM" logo="typeorm" docLink="/tidbcloud/dev-guide-sample-application-nodejs-typeorm" githubLink="https://github.com/typeorm/typeorm">

Connect to TiDB Cloud with TypeORM.

</DevToolCard>
<DevToolCard title="Sequelize" logo="sequelize" docLink="/tidbcloud/dev-guide-sample-application-nodejs-sequelize" githubLink="https://github.com/sequelize/sequelize">

Connect to TiDB Cloud with Sequelize ORM.

</DevToolCard>
<DevToolCard title="mysql.js" logo="mysql" docLink="/tidbcloud/dev-guide-sample-application-nodejs-mysqljs" githubLink="https://github.com/mysqljs/mysql">

Connect Node.js with mysql.js module to TiDB Cloud.

</DevToolCard>
<DevToolCard title="node-mysql2" logo="mysql" docLink="/tidbcloud/dev-guide-sample-application-nodejs-mysql2" githubLink="https://github.com/sidorares/node-mysql2">

Connect Node.js with node-mysql2 module to TiDB Cloud.

</DevToolCard>
<DevToolCard title="AWS Lambda" logo="aws-lambda" docLink="/tidbcloud/dev-guide-sample-application-aws-lambda" githubLink="https://github.com/sidorares/node-mysql2">

Connect AWS Lambda Function with mysql2 to TiDB Cloud.

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Python" defaultExpanded>
<DevToolCard title="Django" logo="django" docLink="/tidbcloud/dev-guide-sample-application-python-django" githubLink="https://github.com/pingcap/django-tidb">

Connect Django application with django-tidb to TiDB Cloud.

</DevToolCard>
<DevToolCard title="MySQL Connector/Python" logo="python" docLink="/tidbcloud/dev-guide-sample-application-python-mysql-connector" githubLink="https://github.com/mysql/mysql-connector-python">

Connect to TiDB Cloud with the official MySQL package.

</DevToolCard>
<DevToolCard title="PyMySQL" logo="python" docLink="/tidbcloud/dev-guide-sample-application-python-pymysql" githubLink="https://github.com/PyMySQL/PyMySQL">

Connect to TiDB Cloud with PyMySQL package.

</DevToolCard>
<DevToolCard title="mysqlclient" logo="python" docLink="/tidbcloud/dev-guide-sample-application-python-mysqlclient" githubLink="https://github.com/PyMySQL/mysqlclient">

Connect to TiDB Cloud with mysqlclient package.

</DevToolCard>
<DevToolCard title="SQLAlchemy" logo="sqlalchemy" docLink="/tidbcloud/dev-guide-sample-application-python-sqlalchemy" githubLink="https://github.com/sqlalchemy/sqlalchemy">

Connect to TiDB Cloud with SQLAlchemy ORM.

</DevToolCard>
<DevToolCard title="peewee" logo="peewee" docLink="/tidbcloud/dev-guide-sample-application-python-peewee" githubLink="https://github.com/coleifer/peewee">

Connect to TiDB Cloud with Peewee ORM.

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Java">
<DevToolCard title="JDBC" logo="java" docLink="/tidbcloud/dev-guide-sample-application-java-jdbc" githubLink="https://github.com/mysql/mysql-connector-j">

Connect to TiDB Cloud with JDBC (MySQL Connector/J).

</DevToolCard>
<DevToolCard title="MyBatis" logo="mybatis" docLink="/tidbcloud/dev-guide-sample-application-java-mybatis" githubLink="https://github.com/mybatis/mybatis-3">

Connect to TiDB Cloud with MyBatis ORM.

</DevToolCard>
<DevToolCard title="Hibernate" logo="hibernate" docLink="/tidbcloud/dev-guide-sample-application-java-hibernate" githubLink="https://github.com/hibernate/hibernate-orm">

Connect to TiDB Cloud with Hibernate ORM.

</DevToolCard>
<DevToolCard title="Spring Boot" logo="spring" docLink="/tidbcloud/dev-guide-sample-application-java-spring-boot" githubLink="https://github.com/spring-projects/spring-data-jpa">

Connect Spring based application with Spring Data JPA to TiDB Cloud.

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Go">
<DevToolCard title="Go-MySQL-Driver" logo="go" docLink="/tidbcloud/dev-guide-sample-application-golang-sql-driver" githubLink="https://github.com/go-sql-driver/mysql">

Connect to TiDB Cloud with MySQL driver for Go.

</DevToolCard>
<DevToolCard title="GORM" logo="gorm" docLink="/tidbcloud/dev-guide-sample-application-golang-gorm" githubLink="https://github.com/go-gorm/gorm">

Connect to TiDB Cloud with GORM.

</DevToolCard>
</DevLangAccordion>

<DevLangAccordion label="Ruby">
<DevToolCard title="Ruby on Rails" logo="rails" docLink="/tidbcloud/dev-guide-sample-application-ruby-rails" githubLink="https://github.com/rails/rails/tree/main/activerecord">

Connect Ruby on Rails application with Active Record ORM to TiDB Cloud.

</DevToolCard>
<DevToolCard title="mysql2" logo="ruby" docLink="/tidbcloud/dev-guide-sample-application-ruby-mysql2" githubLink="https://github.com/brianmario/mysql2">

Connect to TiDB Cloud with mysql2 driver.

</DevToolCard>
</DevLangAccordion>

In addition to these guides, PingCAP works with the community to support [third-party MySQL drivers, ORMs, and tools](/develop/dev-guide-third-party-support.md).

## Use MySQL client software

As TiDB is a MySQL-compatible database, you can use many familiar client software tools to connect to TiDB Cloud and manage your databases. Or, you can use our <a href="/tidbcloud/get-started-with-cli">command line tool</a> to connect and manage your databases.

<DevToolGroup>
<DevToolCard title="MySQL Workbench" logo="mysql-1" docLink="/tidbcloud/dev-guide-gui-mysql-workbench">

Connect and manage TiDB Cloud databases with MySQL Workbench.

</DevToolCard>
<DevToolCard title="Visual Studio Code" logo="vscode" docLink="/tidbcloud/dev-guide-gui-vscode-sqltools">

Connect and manage TiDB Cloud databases with the SQLTools extension in VS Code.

</DevToolCard>
<DevToolCard title="DBeaver" logo="dbeaver" docLink="/tidbcloud/dev-guide-gui-dbeaver">

Connect and manage TiDB Cloud databases with DBeaver.

</DevToolCard>
<DevToolCard title="DataGrip" logo="datagrip" docLink="/tidbcloud/dev-guide-gui-datagrip">

Connect and manage TiDB Cloud databases with DataGrip by JetBrains.

</DevToolCard>
</DevToolGroup>

## Additional resources

Learn other topics about developing with TiDB Cloud.

- Use <a href="/tidbcloud/get-started-with-cli">TiDB Cloud CLI</a> to develop, manage and deploy your applications.
- Explore popular <a href="/tidbcloud/integrate-tidbcloud-with-airbyte">service integrations</a> with TiDB Cloud.
- Follow [TiDB database development reference](/develop/dev-guide-schema-design-overview.md) to design, interact with, optimize, and troubleshoot your data and schema.
- Follow the free online course [Introduction to TiDB](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide).

</CustomContent>

<CustomContent platform="tidb">

This guide is written for application developers, but if you are interested in the inner workings of TiDB or want to get involved in TiDB development, read the [TiDB Kernel Development Guide](https://pingcap.github.io/tidb-dev-guide/) for more information about TiDB.

This tutorial shows how to quickly build an application using TiDB, the possible use cases of TiDB and how to handle common problems.

Before reading this page, it is recommended that you read the [Quick Start with TiDB Self-Managed](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb/).

## TiDB basics

Before you start working with TiDB, you need to understand some important mechanisms of how TiDB works:

- Read the [TiDB Transaction Overview](/transaction-overview.md) to understand how transactions work in TiDB, or check out the [Transaction Notes for Application Developers](/develop/dev-guide-transaction-overview.md) to learn about transaction knowledge required for application development.
- Understand [the way applications interact with TiDB](#the-way-applications-interact-with-tidb).
- To learn core components and concepts of building up the distributed database TiDB and TiDB Cloud, refer to the free online course [Introduction to TiDB](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide).

## TiDB transaction mechanisms

TiDB supports distributed transactions and offers both [optimistic transaction](/optimistic-transaction.md) and [pessimistic transaction](/pessimistic-transaction.md) modes. The current version of TiDB uses the **pessimistic transaction** mode by default, which allows you to transact with TiDB as you would with a traditional monolithic database (for example, MySQL).

You can start a transaction using [`BEGIN`](/sql-statements/sql-statement-begin.md), explicitly specify a **pessimistic transaction** using `BEGIN PESSIMISTIC`, or explicitly specify an **optimistic transaction** using `BEGIN OPTIMISTIC`. After that, you can either commit ([`COMMIT`](/sql-statements/sql-statement-commit.md)) or roll back ([`ROLLBACK`](/sql-statements/sql-statement-rollback.md)) the transaction.

TiDB guarantees atomicity for all statements between the start of `BEGIN` and the end of `COMMIT` or `ROLLBACK`, that is, all statements that are executed during this period either succeed or fail as a whole. This is used to ensure data consistency you need for application development.

If you are not sure what an **optimistic transaction** is, do **_NOT_** use it yet. Because **optimistic transactions** require that the application can correctly handle [all errors](https://docs.pingcap.com/tidb/v8.5/error-codes/) returned by the `COMMIT` statement. If you are not sure how your application handles them, use a **pessimistic transaction** instead.

## The way applications interact with TiDB

TiDB is highly compatible with the MySQL protocol and supports [most MySQL syntax and features](/mysql-compatibility.md), so most MySQL connection libraries are compatible with TiDB. If your application framework or language does not have an official adaptation from PingCAP, it is recommended that you use MySQL's client libraries. More and more third-party libraries are actively supporting TiDB's different features.

Since TiDB is compatible with the MySQL protocol and MySQL syntax, most of the ORMs that support MySQL are also compatible with TiDB.

## Read more

- [Quick Start](/develop/dev-guide-build-cluster-in-cloud.md)
- [Choose Driver or ORM](/develop/dev-guide-choose-driver-or-orm.md)
- [Connect to TiDB](https://docs.pingcap.com/tidb/v8.5/dev-guide-connect-to-tidb/)
- [Database Schema Design](/develop/dev-guide-schema-design-overview.md)
- [Write Data](/develop/dev-guide-insert-data.md)
- [Read Data](/develop/dev-guide-get-data-from-single-table.md)
- [Transaction](/develop/dev-guide-transaction-overview.md)
- [Optimize](/develop/dev-guide-optimize-sql-overview.md)
- [Example Applications](/develop/dev-guide-sample-application-java-spring-boot.md)

## Need help?

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](https://docs.pingcap.com/tidb/v8.5/support/).

</CustomContent>