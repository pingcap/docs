---
title: TiDB 支持的第三方工具
summary: 了解 TiDB 支持的第三方工具。
---

# TiDB 支持的第三方工具

> **Note:**
>
> 本文档仅列出 TiDB 支持的常用 [第三方工具](https://en.wikipedia.org/wiki/Third-party_source)。其他一些第三方工具未列出，并非因为不支持，而是 PingCAP 不确定它们是否使用了与 TiDB 不兼容的功能。

TiDB 与 [MySQL 协议具有高度兼容性](/mysql-compatibility.md)，因此大部分适配 MySQL 的驱动程序、ORM 框架以及其他工具都可以与 TiDB 兼容。本文档重点介绍这些工具及其对 TiDB 的支持程度。

## 支持级别

PingCAP 与社区合作，为第三方工具提供以下支持级别：

- **_Full_**：表示 TiDB 已经与对应第三方工具的大部分功能兼容，并会维护其新版本的兼容性。PingCAP 会定期对最新版本的工具进行兼容性测试。
- **_Compatible_**：表示由于对应第三方工具是为 MySQL 设计，且 TiDB 与 MySQL 协议高度兼容，因此 TiDB 可以使用该工具的大部分功能。但 PingCAP 尚未对该工具的所有功能进行全面测试，可能会出现一些意料之外的行为。

> **Note:**
>
> 除非特别说明，否则对 [Application retry and error handling](/develop/dev-guide-transaction-troubleshoot.md#application-retry-and-error-handling) 的支持不包括在 **Driver** 或 **ORM 框架** 中。

如果在使用本文档列出的工具连接 TiDB 时遇到问题，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new?assignees=&labels=type%2Fquestion&template=general-question.md)，提供详细信息以促进对该工具的支持。

## Driver

<table>
   <thead>
      <tr>
         <th>Language</th>
         <th>Driver</th>
         <th>Latest tested version</th>
         <th>Support level</th>
         <th>TiDB adapter</th>
         <th>Tutorial</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td>Go</td>
         <td><a href="https://github.com/go-sql-driver/mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">Go-MySQL-Driver</a></td>
         <td>v1.6.0</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-golang-sql-driver">Connect to TiDB with Go-MySQL-Driver</a></td>
      </tr>
      <tr>
         <td>Java</td>
         <td><a href="https://dev.mysql.com/downloads/connector/j/" target="_blank" referrerpolicy="no-referrer-when-downgrade">JDBC</a></td>
         <td>8.0</td>
         <td>Full</td>
         <td>
            <ul>
               <li><a href="/tidb/v8.5/dev-guide-choose-driver-or-orm#java-drivers" data-href="/tidb/v8.5/dev-guide-choose-driver-or-orm#java-drivers">pingcap/mysql-connector-j</a></li>
               <li><a href="/tidb/v8.5/dev-guide-choose-driver-or-orm#tidb-loadbalance" data-href="/tidb/v8.5/dev-guide-choose-driver-or-orm#tidb-loadbalance">pingcap/tidb-loadbalance</a></li>
            </ul>
         </td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-java-jdbc">Connect to TiDB with JDBC</a></td>
      </tr>
   </tbody>
</table>

## ORM

<table>
   <thead>
      <tr>
         <th>Language</th>
         <th>ORM framework</th>
         <th>Latest tested version</th>
         <th>Support level</th>
         <th>TiDB adapter</th>
         <th>Tutorial</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td rowspan="4">Go</td>
         <td><a href="https://github.com/go-gorm/gorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">gorm</a></td>
         <td>v1.23.5</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-golang-gorm">Connect to TiDB with GORM</a></td>
      </tr>
      <tr>
         <td><a href="https://github.com/beego/beego" target="_blank" referrerpolicy="no-referrer-when-downgrade">beego</a></td>
         <td>v2.0.3</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://github.com/upper/db" target="_blank" referrerpolicy="no-referrer-when-downgrade">upper/db</a></td>
         <td>v4.5.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://gitea.com/xorm/xorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">xorm</a></td>
         <td>v1.3.1</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="4">Java</td>
         <td><a href="https://hibernate.org/orm/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Hibernate</a></td>
         <td>6.1.0.Final</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-java-hibernate">Connect to TiDB with Hibernate</a></td>
      </tr>
      <tr>
         <td><a href="https://mybatis.org/mybatis-3/" target="_blank" referrerpolicy="no-referrer-when-downgrade">MyBatis</a></td>
         <td>v3.5.10</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-java-mybatis">Connect to TiDB with MyBatis</a></td>
      </tr>
      <tr>
         <td><a href="https://spring.io/projects/spring-data-jpa/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Spring Data JPA</a></td>
         <td>2.7.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-java-spring-boot">Connect to TiDB with Spring Boot</a></td>
      </tr>
      <tr>
         <td><a href="https://github.com/jOOQ/jOOQ" target="_blank" referrerpolicy="no-referrer-when-downgrade">jOOQ</a></td>
         <td>v3.16.7 (Open Source)</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>Ruby</td>
         <td><a href="https://guides.rubyonrails.org/active_record_basics.html" target="_blank" referrerpolicy="no-referrer-when-downgrade">Active Record</a></td>
         <td>v7.0</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-ruby-rails">Connect to TiDB with Rails Framework and ActiveRecord ORM</a></td>
      </tr>
      <tr>
         <td rowspan="3">JavaScript / TypeScript</td>
         <td><a href="https://sequelize.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Sequelize</a></td>
         <td>v6.20.1</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-nodejs-sequelize">Connect to TiDB with Sequelize</a></td>
      </tr>
      <tr>
         <td><a href="https://www.prisma.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Prisma</a></td>
         <td>4.16.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-nodejs-prisma">Connect to TiDB with Prisma</a></td>
      </tr>
      <tr>
         <td><a href="https://typeorm.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">TypeORM</a></td>
         <td>v0.3.17</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-nodejs-typeorm">Connect to TiDB with TypeORM</a></td>
      </tr>
      <tr>
         <td rowspan="2">Python</td>
         <td><a href="https://pypi.org/project/Django/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Django</a></td>
         <td>v4.2</td>
         <td>Full</td>
         <td><a href="https://github.com/pingcap/django-tidb" target="_blank" referrerpolicy="no-referrer-when-downgrade">django-tidb</a></td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-python-django">Connect to TiDB with Django</a></td>
      </tr>
      <tr>
         <td><a href="https://www.sqlalchemy.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">SQLAlchemy</a></td>
         <td>v1.4.37</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/tidb/v8.5/dev-guide-sample-application-python-sqlalchemy">Connect to TiDB with SQLAlchemy</a></td>
      </tr>
   </tbody>
</table>

## GUI

| GUI                                                       | Latest tested version | Support level | Tutorial                                                                             |
|-----------------------------------------------------------|-----------------------|---------------|--------------------------------------------------------------------------------------|
| [Beekeeper Studio](https://www.beekeeperstudio.io/)       | 4.3.0                 | Full          | N/A                                                                                  |
| [JetBrains DataGrip](https://www.jetbrains.com/datagrip/) | 2023.2.1              | Full          | [Connect to TiDB with JetBrains DataGrip](/develop/dev-guide-gui-datagrip.md)        |
| [DBeaver](https://dbeaver.io/)                            | 23.0.3                | Full          | [Connect to TiDB with DBeaver](/develop/dev-guide-gui-dbeaver.md)                    |
| [Visual Studio Code](https://code.visualstudio.com/)      | 1.72.0                | Full          | [Connect to TiDB with Visual Studio Code](/develop/dev-guide-gui-vscode-sqltools.md) |
| [Navicat](https://www.navicat.com)                        | 17.1.6                | Full          | [Connect to TiDB with Navicat](/develop/dev-guide-gui-navicat.md)                   |

## Need help?

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>