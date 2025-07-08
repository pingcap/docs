---
title: Third-Party Tools Supported by TiDB
summary: Learn about third-party tools supported by TiDB.
---

# Third-Party Tools Supported by TiDB

> **Note:**
>
> This document only lists common [third-party tools](https://en.wikipedia.org/wiki/Third-party_source) supported by TiDB. Some other third-party tools are not listed, not because they are not supported, but because PingCAP is not sure whether they use features that are incompatible with TiDB.

TiDB is [highly compatible with the MySQL protocol](/mysql-compatibility.md), so most of the MySQL drivers, ORM frameworks, and other tools that adapt to MySQL are compatible with TiDB. This document focuses on these tools and their support levels for TiDB.

## Support Level

PingCAP works with the community and provides the following support levels for third-party tools:

- **_Full_**: Indicates that TiDB is already compatible with most functionalities of the corresponding third-party tool, and maintains compatibility with its newer versions. PingCAP will periodically conduct compatibility tests with the latest version of the tool.
- **_Compatible_**: Indicates that because the corresponding third-party tool is adapted to MySQL and TiDB is highly compatible with the MySQL protocol, so TiDB can use most features of the tool. However, PingCAP has not completed a full test on all features of the tool, which might lead to some unexpected behaviors.

> **Note:**
>
> Unless specified, support for [Application retry and error handling](/develop/dev-guide-transaction-troubleshoot.md#application-retry-and-error-handling) is not included for **Driver** or **ORM frameworks**.

If you encounter problems when connecting to TiDB using the tools listed in this document, please submit an [issue](https://github.com/pingcap/tidb/issues/new?assignees=&labels=type%2Fquestion&template=general-question.md) on GitHub with details to promote support on this tool.

## Driver

| Language | Driver | Latest tested version | Support level | TiDB adapter | Tutorial |
|----------|--------|-----------------------|---------------|--------------|----------|
| Go | [go-sql-driver/mysql](https://github.com/go-sql-driver/mysql) | v1.6.0 | Full | N/A | [Connect to TiDB with Go-MySQL-Driver](/develop/dev-guide-sample-application-golang-sql-driver.md) |
| Java | [MySQL Connector/J](https://dev.mysql.com/downloads/connector/j/) | 8.0 | Full | [pingcap/mysql-connector-j](/develop/dev-guide-choose-driver-or-orm.md#java-drivers) <br/> [pingcap/tidb-loadbalance](/develop/dev-guide-choose-driver-or-orm.md#java-client-load-balancing) | [Connect to TiDB with JDBC](/develop/dev-guide-sample-application-java-jdbc.md) |

## ORM

| Language                | ORM framework                             | Latest tested version | Support level | TiDB adapter | Tutorial |
|-------------------------|-------------------------------------------|-----------------------|-------------|--------------|----------|
| Go                      | [gorm](https://github.com/go-gorm/gorm)   | v1.23.5               | Full      | N/A           | [Connect to TiDB with GORM](/develop/dev-guide-sample-application-golang-gorm.md) |
| Go                      | [beego](https://github.com/beego/beego)   | v2.0.3                | Full      | N/A           | N/A |
| Go                      | [upper/db](https://github.com/upper/db)   | v4.5.2                | Full      | N/A           | N/A |
| Go                      | [xorm](https://gitea.com/xorm/xorm)       | v1.3.1                | Full      | N/A           | N/A |
| Java                    | [Hibernate](https://hibernate.org/orm/)   | 6.1.0.Final           | Full      | N/A           | [Connect to TiDB with Hibernate](/develop/dev-guide-sample-application-java-hibernate.md) |
| Java                    | [MyBatis](https://mybatis.org/mybatis-3/) | v3.5.10               | Full      | N/A           | [Connect to TiDB with MyBatis](/develop/dev-guide-sample-application-java-mybatis.md) |
| Java                    | [Spring Data JPA](https://spring.io/projects/spring-data-jpa/) | 2.7.2 | Full | N/A           | [Connect to TiDB with Spring Boot](/develop/dev-guide-sample-application-java-spring-boot.md) |
| Java                    | [jOOQ](https://github.com/jOOQ/jOOQ)      | v3.16.7 (Open Source) | Full      | N/A           | N/A |
| Ruby                    | [Active Record](https://guides.rubyonrails.org/active_record_basics.html) | v7.0 | Full | N/A | [Connect to TiDB with Rails Framework and ActiveRecord ORM](/develop/dev-guide-sample-application-ruby-rails.md) |
| JavaScript / TypeScript | [Sequelize](https://sequelize.org/)       | v6.20.1               | Full      | N/A           | [Connect to TiDB with Sequelize](/develop/dev-guide-sample-application-nodejs-sequelize.md) |
| JavaScript / Typescript | [Prisma](https://www.prisma.io/)          | 4.16.2                | Full      | N/A           | [Connect to TiDB with Prisma](/develop/dev-guide-sample-application-nodejs-prisma.md) |
| JavaScript / Typescript | [TypeORM](https://typeorm.io/)            | v0.3.17               | Full      | N/A           | [Connect to TiDB with TypeORM](/develop/dev-guide-sample-application-nodejs-typeorm.md) |
| Python                  | [Django](https://www.djangoproject.com/)  | v4.2                  | Full      | [django-tidb](https://github.com/pingcap/django-tidb) | [Connect to TiDB with Django](/develop/dev-guide-sample-application-python-django.md) |
| Python                  | [SQLAlchemy](https://www.sqlalchemy.org/) | v1.4.37               | Full      | N/A           | [Connect to TiDB with SQLAlchemy](/develop/dev-guide-sample-application-python-sqlalchemy.md) |

## GUI

| GUI                                                       | Latest tested version | Support level | Tutorial                                                                             |
|-----------------------------------------------------------|-----------------------|---------------|--------------------------------------------------------------------------------------|
| [Beekeeper Studio](https://www.beekeeperstudio.io/)       | 4.3.0                 | Full          | N/A                                                                                  |
| [JetBrains DataGrip](https://www.jetbrains.com/datagrip/) | 2023.2.1              | Full          | [Connect to TiDB with JetBrains DataGrip](/develop/dev-guide-gui-datagrip.md)        |
| [DBeaver](https://dbeaver.io/)                            | 23.0.3                | Full          | [Connect to TiDB with DBeaver](/develop/dev-guide-gui-dbeaver.md)                    |
| [Visual Studio Code](https://code.visualstudio.com/)      | 1.72.0                | Full          | [Connect to TiDB with Visual Studio Code](/develop/dev-guide-gui-vscode-sqltools.md) |
| [Navicat](https://www.navicat.com)                        | 17.1.6                | Full          | [Connect to TiDB with Navicat](/develop/dev-guide-gui-navicat.md) |

## Need help?

<CustomContent platform="tidb">

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](https://tidb.support.pingcap.com/).

</CustomContent>