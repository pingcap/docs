---
title: Third-Party Libraries Supported by PingCAP
summary: Learn about third-party libraries supported by PingCAP.
---

# Third-Party Libraries Supported by PingCAP

TiDB's support for the MySQL protocol makes most of the MySQL drivers, ORM frameworks, and other tools that adapt to MySQL compatible with TiDB. This document focuses on these tools and their support levels.

## Support Level

PingCAP works with community and provides the following levels of support:

- **_Full_**: Indicates that PingCAP is already compatible with most of the tool's functionalities, and maintains compatibility with its newer versions. PingCAP will periodically conduct compatibility tests with the latest version of third-party tools documented in the table below.
- **_Compatible_**: Indicates that because the tool is adapted to MySQL, and TiDB is highly compatible with the MySQL protocol. So it can use most of the tool's features. However, PingCAP has not complete test this tool's features. It may lead to some unexpected behavior.

> **Warning:**
>
> Unless specified, support for [Application retry and error handling](/develop/dev-guide-transaction-troubleshoot.md#application-retry-and-error-handling) are not included for **Driver** or **ORM frameworks**.

If you encounter problems connecting to TiDB using the tools listed in this document, please submit an [issue](https://github.com/pingcap/tidb/issues/new?assignees=&labels=type%2Fquestion&template=general-question.md) on GitHub with details to promote support on this tool.

## Driver

| Language       | Driver                                                                       | Latest tested version | Support level | TiDB adapter                                                                                   | Tutorial                                                                             |
|------------|--------------------------------------------------------------------------|---------|------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| C          | [MySQL Connector/C](https://downloads.mysql.com/archives/c-c/)           | 6.1.11  | Full | N/A                                                                                        | N/A                                                                            |
| C#(.Net)   | [MySQL Connector/NET](https://downloads.mysql.com/archives/c-net/)       | 8.0.28  | Compatible | N/A                                                                                        | N/A                                                                            |
| C#(.Net)   | [MySQL Connector/ODBC](https://downloads.mysql.com/archives/c-odbc/)     | 8.0.28  | Compatible | N/A                                                                                        | N/A                                                                            |
| Go         | [go-sql-driver/mysql](https://github.com/go-sql-driver/mysql)            | v1.6.0  | Full | N/A                                                                                        | [Build a Simple CRUD App with TiDB and Golang](/develop/dev-guide-sample-application-golang.md) |
| Java       | [JDBC](https://dev.mysql.com/downloads/connector/j/)                     | 5.1.46; 8.0.29  | Full | 5.1.46: N/A; 8.0.29: [pingcap/mysql-connector-j](https://github.com/pingcap/mysql-connector-j/tree/release/8.0)                                                                                     | [Build a Simple CRUD App with TiDB and Java](/develop/dev-guide-sample-application-java.md)     |
| JavaScript | [mysql](https://github.com/mysqljs/mysql)                                | v2.18.1 | Compatible | N/A                                                                                        | N/A                                                                            |
| PHP        | [MySQL Connector/PHP](https://downloads.mysql.com/archives/c-php/)       | 5.0.37  | Compatible | N/A                                                                                        | N/A                                                                            |
| Python     | [MySQL Connector/Python](https://downloads.mysql.com/archives/c-python/) | 8.0.28  | Compatible | N/A                                                                                        | N/A                                                                            |

## ORM

| Language                  | ORM framework                                                                                                                                                                        | Latest tested version     | Support level | TiDB adapter                                               | Tutorial                                                                             |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|------|--------------------------------------------------------|--------------------------------------------------------------------------------|
| Go                    | [gorm](https://github.com/go-gorm/gorm)                                                                                                                                       | v1.23.5     | Full | N/A                                                    | [Build a Simple CRUD App with TiDB and Golang](/develop/dev-guide-sample-application-golang.md) |
| Go                    | [beego](https://github.com/beego/beego)                                                                                                                                       | v2.0.3      | Full | N/A                                                    | N/A                                                                            |
| Go                    | [upper/db](https://github.com/upper/db)                                                                                                                                       | v4.5.2      | Full | N/A                                                    | N/A                                                                            |
| Go                    | [xorm](https://gitea.com/xorm/xorm)                                                                                                                                           | v1.3.1      | Full | N/A                                                    | N/A                                                                            |
| Java                  | [Hibernate](https://hibernate.org/orm/) | 6.1.0.Final | Full | N/A                                                    | [Build a Simple CRUD App with TiDB and Java](/develop/dev-guide-sample-application-java.md)     |
| Java                  | [MyBatis](https://mybatis.org/mybatis-3/)                                                                                                                                     | v3.5.10     | Full | N/A                                                    | [Build a Simple CRUD App with TiDB and Java](/develop/dev-guide-sample-application-java.md)                                                                            |
| Java                  | [Spring Data JPA](https://spring.io/projects/spring-data-jpa/) | 2.7.2 | Compatible | N/A                                                    |  [Build a TiDB Application Using Spring Boot](/develop/dev-guide-sample-application-spring-boot.md)   |
| jOOQ                  | [jOOQ](https://github.com/jOOQ/jOOQ)                                                                                                                                     | v3.16.7 (Open Source)     | Full | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [sequelize](https://www.npmjs.com/package/sequelize)                                                                                                                          | v6.20.1     | Compatible | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [Knex.js](https://knexjs.org/)                                                                                                                                                | v1.0.7      | Compatible | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [Prisma Client](https://www.prisma.io/)                                                                                                                                       | 3.15.1      | Compatible | N/A                                                    | N/A                                                                            |
| JavaScript/TypeScript | [TypeORM](https://www.npmjs.com/package/typeorm)                                                                                                                              | v0.3.6      | Compatible | N/A                                                    | N/A                                                                            |
| PHP                   | [laravel](https://laravel.com/)                                                                                                                                               | v9.1.10     | Compatible | [laravel-tidb](https://github.com/colopl/laravel-tidb) | N/A                                                                            |
| Python                | [Django](https://pypi.org/project/Django/)                                                  | v4.0.5      | Compatible | N/A                                                    | N/A                                                                            |
| Python                | [peewee](https://github.com/coleifer/peewee/)                                                                                                                                 | v3.14.10    | Compatible | N/A                                                    | N/A                                                                            |
| Python                | [PonyORM](https://ponyorm.org/)                                                                                                                                               | v0.7.16     | Compatible | N/A                                                    | N/A                                                                            |
| Python                | [SQLAlchemy](https://www.sqlalchemy.org/)                                                                                                                                     | v1.4.37     | Compatible | N/A                                                    | N/A                                                                            |

## GUI

| GUI                                           | Latest tested version  | Support level | Tutorial  |
|-----------------------------------------------|---------|------|-----|
| [DBeaver](https://dbeaver.io/)                | 22.1.0  | Compatible | N/A |
| [Navicat for MySQL](https://www.navicat.com/) | 16.0.14 | Compatible | N/A |

| IDE                                              | Latest tested version | Support level | Tutorial |
| ------------------------------------------------ | ------- | ---- | ---- |
| [DataGrip](https://www.jetbrains.com/datagrip/)  | N/A     | Compatible | N/A  |
| [IntelliJ IDEA](https://www.jetbrains.com/idea/) | N/A     | Compatible | N/A  |
