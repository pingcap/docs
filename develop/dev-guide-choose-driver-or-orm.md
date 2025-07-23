---
title: 选择 Driver 或 ORM
summary: 了解如何选择驱动程序或 ORM 框架以连接到 TiDB。
---

# 选择 Driver 或 ORM

> **Note:**
>
> TiDB 为驱动程序和 ORM 提供以下两个支持级别：
>
> - **Full**：表示 TiDB 与大部分工具功能兼容，并保持与其新版本的兼容性。PingCAP 会定期对支持的第三方工具（详见 [Third-party tools supported by TiDB](/develop/dev-guide-third-party-support.md)）的最新版本进行兼容性测试。
> - **Compatible**：表示由于对应的第三方工具已适配 MySQL，且 TiDB 与 MySQL 协议高度兼容，因此 TiDB 可以使用该工具的大部分功能。但 PingCAP 尚未对该工具的所有功能进行全面测试，可能会导致一些意外行为。
>
> 详细信息请参考 [Third-Party Tools Supported by TiDB](/develop/dev-guide-third-party-support.md)。

TiDB 与 MySQL 协议高度兼容，但某些功能与 MySQL 不兼容。完整的兼容性差异列表，请参见 [MySQL Compatibility](/mysql-compatibility.md)。

## Java

本节介绍在 Java 中如何使用驱动程序和 ORM 框架。

### Java 驱动程序

<SimpleTab>
<div label="MySQL-JDBC">

Support level: **Full**

你可以按照 [MySQL 文档](https://dev.mysql.com/doc/connector-j/en/) 下载并配置 Java JDBC 驱动程序。建议使用与 TiDB v6.3.0 及以上版本兼容的最新 GA 版本的 MySQL Connector/J。

> **Warning:**
>
> 在 8.0.31 之前的 MySQL Connector/J 8.0 版本（详见 [MySQL JDBC bugs](/develop/dev-guide-third-party-tools-compatibility.md#mysql-jdbc-bugs)）存在一个 [bug](https://bugs.mysql.com/bug.php?id=106252)，可能导致在使用 TiDB 早于 v6.3.0 版本时出现线程挂起的问题。为避免此问题，请 **不要** 使用 MySQL Connector/J 8.0.31 或更早版本。

关于如何构建完整应用的示例，请参见 [Build a simple CRUD app with TiDB and JDBC](/develop/dev-guide-sample-application-java-jdbc.md)。

</div>
<div label="TiDB-JDBC">

Support level: **Full**

[TiDB-JDBC](https://github.com/pingcap/mysql-connector-j) 是基于 MySQL 8.0.29 定制的 Java 驱动程序。该驱动基于 MySQL 官方版本 8.0.29 编译，修复了原生 JDBC 在 prepare 模式下多参数和多字段 EOF 的 bug，并新增了自动维护 TiCDC 快照和 SM3 认证插件等功能。

基于 SM3 的认证仅支持在 TiDB 的 TiDB-JDBC 中。

如果你使用 Maven，请在 `pom.xml` 文件的 `<dependencies></dependencies>` 部分添加以下内容：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
```

如果需要启用 SM3 认证，请在 `<dependencies></dependencies>` 中添加：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcprov-jdk15on</artifactId>
    <version>1.67</version>
</dependency>
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcpkix-jdk15on</artifactId>
    <version>1.67</version>
</dependency>
```

如果使用 Gradle，请在 `dependencies` 中添加：

```gradle
implementation group: 'io.github.lastincisor', name: 'mysql-connector-java', version: '8.0.29-tidb-1.0.0'
implementation group: 'org.bouncycastle', name: 'bcprov-jdk15on', version: '1.67'
implementation group: 'org.bouncycastle', name: 'bcpkix-jdk15on', version: '1.67'
```

</div>
</SimpleTab>

### Java ORM 框架

<SimpleTab>
<div label="Hibernate">

> **Note:**
>
> - 目前，Hibernate 不支持 [嵌套事务](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres)。
>
> - 自 v6.2.0 起，TiDB 支持 [savepoint](/sql-statements/sql-statement-savepoint.md)。在 `@Transactional` 中使用 `Propagation.NESTED` 事务传播选项，即设置 `@Transactional(propagation = Propagation.NESTED)`，请确保你的 TiDB 版本为 v6.2.0 或更高。

Support level: **Full**

为了避免手动管理应用中不同依赖之间的复杂关系，你可以使用 [Gradle](https://gradle.org/install) 或 [Maven](https://maven.apache.org/install.html) 获取所有依赖（包括间接依赖）。注意，只有 Hibernate `6.0.0.Beta2` 及以上版本支持 TiDB 方言。

如果你使用 Maven，请在 `<dependencies></dependencies>` 中添加：

```xml
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>6.2.3.Final</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
```

如果你使用 Gradle，请在 `dependencies` 中添加：

```gradle
implementation 'org.hibernate:hibernate-core:6.2.3.Final'
implementation 'mysql:mysql-connector-java:8.0.33'
```

- 关于使用 Hibernate 通过原生 Java 构建 TiDB 应用的示例，请参见 [Build a simple CRUD app with TiDB and Hibernate](/develop/dev-guide-sample-application-java-hibernate.md)。
- 关于使用 Spring Data JPA 或 Hibernate 通过 Spring 构建 TiDB 应用的示例，请参见 [Build a TiDB app using Spring Boot](/develop/dev-guide-sample-application-java-spring-boot.md)。

此外，你还需要在你的 [Hibernate 配置文件](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm) 中指定 TiDB 方言：`org.hibernate.dialect.TiDBDialect`，该配置仅在 Hibernate `6.0.0.Beta2` 及以上版本支持。如果你的 Hibernate 版本早于 `6.0.0.Beta2`，请先升级。

> **Note:**
>
> 如果无法升级 Hibernate 版本，可以使用 MySQL 5.7 方言 `org.hibernate.dialect.MySQL57Dialect`。但此设置可能导致结果不可预期，且可能缺少一些 TiDB 特有的功能，例如 [sequences](/sql-statements/sql-statement-create-sequence.md)。

</div>

<div label="MyBatis">

Support level: **Full**

为了避免手动管理应用中不同依赖之间的复杂关系，你可以使用 [Gradle](https://gradle.org/install) 或 [Maven](https://maven.apache.org/install.html) 获取所有依赖（包括间接依赖）。

如果你使用 Maven，请在 `<dependencies></dependencies>` 中添加：

```xml
<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis</artifactId>
    <version>3.5.13</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
```

如果你使用 Gradle，请在 `dependencies` 中添加：

```gradle
implementation 'org.mybatis:mybatis:3.5.13'
implementation 'mysql:mysql-connector-java:8.0.33'
```

关于使用 MyBatis 构建 TiDB 应用的示例，请参见 [Build a simple CRUD app with TiDB and MyBatis](/develop/dev-guide-sample-application-java-mybatis.md)。

</div>
</SimpleTab>

### Java 客户端负载均衡

**tidb-loadbalance**

Support level: **Full**

[tidb-loadbalance](https://github.com/pingcap/tidb-loadbalance) 是应用端的负载均衡组件。使用 tidb-loadbalance，可以自动维护 TiDB 服务器的节点信息，并根据策略在客户端分发 JDBC 连接。直接使用客户端应用与 TiDB 服务器的 JDBC 连接，性能优于使用负载均衡组件。

目前，tidb-loadbalance 支持的策略包括：roundrobin、random 和 weight。

> **Note:**
>
> tidb-loadbalance 必须与 [mysql-connector-j](https://github.com/pingcap/mysql-connector-j) 一起使用。

如果你使用 Maven，请在 `pom.xml` 文件的 `<dependencies></dependencies>` 中添加：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>tidb-loadbalance</artifactId>
  <version>0.0.5</version>
</dependency>
```

如果你使用 Gradle，请在 `dependencies` 中添加：

```gradle
implementation group: 'io.github.lastincisor', name: 'mysql-connector-java', version: '8.0.29-tidb-1.0.0'
implementation group: 'io.github.lastincisor', name: 'tidb-loadbalance', version: '0.0.5'
```

## Golang

本节介绍在 Golang 中如何使用驱动程序和 ORM 框架。

### Golang 驱动程序

**go-sql-driver/mysql**

Support level: **Full**

要下载并配置 Golang 驱动程序，请参考 [go-sql-driver/mysql 文档](https://github.com/go-sql-driver/mysql)。

关于如何构建完整应用的示例，请参见 [Connect to TiDB with Go-MySQL-Driver](/develop/dev-guide-sample-application-golang-sql-driver.md)。

### Golang ORM 框架

**GORM**

Support level: **Full**

GORM 是 Golang 中流行的 ORM 框架。要获取所有依赖，可以使用 `go get` 命令。

```shell
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```

关于使用 GORM 构建 TiDB 应用的示例，请参见 [Connect to TiDB with GORM](/develop/dev-guide-sample-application-golang-gorm.md)。

## Python

本节介绍在 Python 中如何使用驱动程序和 ORM 框架。

### Python 驱动程序

<SimpleTab>
<div label="PyMySQL">

Support level: **Compatible**

你可以按照 [PyMySQL 文档](https://pypi.org/project/PyMySQL/) 下载并配置驱动程序。建议使用 PyMySQL 1.0.2 及以上版本。

关于如何使用 PyMySQL 构建 TiDB 应用的示例，请参见 [Connect to TiDB with PyMySQL](/develop/dev-guide-sample-application-python-pymysql.md)。

</div>
<div label="mysqlclient">

Support level: **Compatible**

你可以按照 [mysqlclient 文档](https://pypi.org/project/mysqlclient/) 下载并配置驱动程序。建议使用 mysqlclient 2.1.1 及以上版本。

关于如何使用 mysqlclient 构建 TiDB 应用的示例，请参见 [Connect to TiDB with mysqlclient](/develop/dev-guide-sample-application-python-mysqlclient.md)。

</div>
<div label="MySQL Connector/Python">

Support level: **Compatible**

你可以按照 [MySQL Connector/Python 文档](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html) 下载并配置驱动程序。建议使用 Connector/Python 8.0.31 及以上版本。

关于如何使用 MySQL Connector/Python 构建 TiDB 应用的示例，请参见 [Connect to TiDB with MySQL Connector/Python](/develop/dev-guide-sample-application-python-mysql-connector.md)。

</div>
</SimpleTab>

### Python ORM 框架

<SimpleTab>
<div label="Django">

Support level: **Full**

[django](https://docs.djangoproject.com/) 是流行的 Python Web 框架。为解决 TiDB 与 Django 之间的兼容性问题，PingCAP 提供了 TiDB 方言 `django-tidb`。你可以参考 [django-tidb 安装指南](https://github.com/pingcap/django-tidb#installation-guide)。

关于使用 Django 构建 TiDB 应用的示例，请参见 [Connect to TiDB with Django](/develop/dev-guide-sample-application-python-django.md)。

</div>
<div label="SQLAlchemy">

Support level: **Full**

[SQLAlchemy](https://www.sqlalchemy.org/) 是流行的 Python ORM 框架。要获取所有依赖，可以使用 `pip install SQLAlchemy==1.4.44` 命令。建议使用 SQLAlchemy 1.4.44 及以上版本。

关于使用 SQLAlchemy 构建 TiDB 应用的示例，请参见 [Connect to TiDB with SQLAlchemy](/develop/dev-guide-sample-application-python-sqlalchemy.md)。

</div>
<div label="peewee">

Support level: **Compatible**

[peewee](http://docs.peewee-orm.com/en/latest/) 是流行的 Python ORM 框架。要获取所有依赖，可以使用 `pip install peewee==3.15.4` 命令。建议使用 peewee 3.15.4 及以上版本。

关于使用 peewee 构建 TiDB 应用的示例，请参见 [Connect to TiDB with peewee](/develop/dev-guide-sample-application-python-peewee.md)。

</div>
</SimpleTab>

<CustomContent platform="tidb-cloud">

在确定了驱动程序或 ORM 后，你可以 [连接到你的 TiDB 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

</CustomContent>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>