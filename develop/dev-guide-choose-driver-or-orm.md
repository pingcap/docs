---
title: 选择驱动或 ORM
summary: 了解如何选择驱动或 ORM 框架以连接到 TiDB。
---

# 选择驱动或 ORM

> **Note:**
>
> TiDB 对驱动和 ORM 提供以下两种支持级别：
>
> - **Full**：表示 TiDB 兼容该工具的大多数功能，并保持对其新版本的兼容性。PingCAP 会定期对 [TiDB 支持的第三方工具](/develop/dev-guide-third-party-support.md) 的最新版本进行兼容性测试。
> - **Compatible**：表示由于相应的第三方工具是为 MySQL 适配的，而 TiDB 高度兼容 MySQL 协议，因此 TiDB 可以使用该工具的大多数功能。但 PingCAP 尚未对该工具的所有功能进行完整测试，可能会导致一些意外行为。
>
> 更多信息请参考 [TiDB 支持的第三方工具](/develop/dev-guide-third-party-support.md)。

TiDB 高度兼容 MySQL 协议，但部分功能与 MySQL 不兼容。完整的兼容性差异列表请参见 [MySQL 兼容性](/mysql-compatibility.md)。

## Java

本节介绍如何在 Java 中使用驱动和 ORM 框架。

### Java 驱动

<SimpleTab>
<div label="MySQL-JDBC">

支持级别：**Full**

你可以按照 [MySQL 官方文档](https://dev.mysql.com/doc/connector-j/en/) 下载并配置 Java JDBC 驱动。推荐在 TiDB v6.3.0 或更高版本中使用最新的 GA 版本 MySQL Connector/J。

> **Warning:**
>
> 在 8.0.31 之前的 MySQL Connector/J 8.0 版本中存在一个 [bug](https://bugs.mysql.com/bug.php?id=106252)（详见 [MySQL JDBC bugs](/develop/dev-guide-third-party-tools-compatibility.md#mysql-jdbc-bugs)），在使用 TiDB v6.3.0 之前的版本时，可能导致线程挂起。为避免此问题，请**不要**使用 8.0.31 或更早版本的 MySQL Connector/J。

关于如何构建完整应用的示例，请参见 [使用 TiDB 和 JDBC 构建简单 CRUD 应用](/develop/dev-guide-sample-application-java-jdbc.md)。

</div>
<div label="TiDB-JDBC">

支持级别：**Full**

[TiDB-JDBC](https://github.com/pingcap/mysql-connector-j) 是基于 MySQL 8.0.29 定制的 Java 驱动。TiDB-JDBC 基于 MySQL 官方 8.0.29 版本编译，修复了原 JDBC 在 prepare 模式下多参数多字段 EOF 的 bug，并增加了 TiCDC 快照自动维护、SM3 认证插件等功能。

基于 SM3 的认证仅在 TiDB 的 TiDB-JDBC 中支持。

如果你使用 Maven，请在 `pom.xml` 文件的 `<dependencies></dependencies>` 部分添加以下内容：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.2</version>
</dependency>
```

如果你需要启用 SM3 认证，请在 `pom.xml` 文件的 `<dependencies></dependencies>` 部分添加以下内容：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.2</version>
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

如果你使用 Gradle，请在 `dependencies` 中添加以下内容：

```gradle
implementation group: 'io.github.lastincisor', name: 'mysql-connector-java', version: '8.0.29-tidb-1.0.2'
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
> - 目前，Hibernate [不支持嵌套事务](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres)。
>
> - 从 v6.2.0 起，TiDB 支持 [savepoint](/sql-statements/sql-statement-savepoint.md)。如需在 `@Transactional` 中使用 `Propagation.NESTED` 事务传播选项，即设置 `@Transactional(propagation = Propagation.NESTED)`，请确保你的 TiDB 版本为 v6.2.0 或更高。

支持级别：**Full**

为避免手动管理应用中不同依赖之间的复杂关系，你可以使用 [Gradle](https://gradle.org/install) 或 [Maven](https://maven.apache.org/install.html) 获取应用的所有依赖（包括间接依赖）。注意，只有 Hibernate `6.0.0.Beta2` 及以上版本支持 TiDB 方言。

如果你使用 Maven，请在 `<dependencies></dependencies>` 中添加以下内容：

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

如果你使用 Gradle，请在 `dependencies` 中添加以下内容：

```gradle
implementation 'org.hibernate:hibernate-core:6.2.3.Final'
implementation 'mysql:mysql-connector-java:8.0.33'
```

- 关于如何使用 Hibernate 通过原生 Java 构建 TiDB 应用的示例，请参见 [使用 TiDB 和 Hibernate 构建简单 CRUD 应用](/develop/dev-guide-sample-application-java-hibernate.md)。
- 关于如何使用 Spring Data JPA 或 Hibernate 通过 Spring 构建 TiDB 应用的示例，请参见 [使用 Spring Boot 构建 TiDB 应用](/develop/dev-guide-sample-application-java-spring-boot.md)。

此外，你需要在 [Hibernate 配置文件](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm) 中指定 TiDB 方言：`org.hibernate.dialect.TiDBDialect`，该方言仅在 Hibernate `6.0.0.Beta2` 及以上版本支持。如果你的 `Hibernate` 版本早于 `6.0.0.Beta2`，请先升级。

> **Note:**
>
> 如果你无法升级 `Hibernate` 版本，请使用 MySQL 5.7 方言 `org.hibernate.dialect.MySQL57Dialect`。但此设置可能导致不可预期的结果，并缺失部分 TiDB 特有功能，如 [sequences](/sql-statements/sql-statement-create-sequence.md)。

</div>

<div label="MyBatis">

支持级别：**Full**

为避免手动管理应用中不同依赖之间的复杂关系，你可以使用 [Gradle](https://gradle.org/install) 或 [Maven](https://maven.apache.org/install.html) 获取应用的所有依赖（包括间接依赖）。

如果你使用 Maven，请在 `<dependencies></dependencies>` 中添加以下内容：

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

如果你使用 Gradle，请在 `dependencies` 中添加以下内容：

```gradle
implementation 'org.mybatis:mybatis:3.5.13'
implementation 'mysql:mysql-connector-java:8.0.33'
```

关于如何使用 MyBatis 构建 TiDB 应用的示例，请参见 [使用 TiDB 和 MyBatis 构建简单 CRUD 应用](/develop/dev-guide-sample-application-java-mybatis.md)。

</div>

</SimpleTab>

### Java 客户端负载均衡

**tidb-loadbalance**

支持级别：**Full**

[tidb-loadbalance](https://github.com/pingcap/tidb-loadbalance) 是应用侧的负载均衡组件。通过 tidb-loadbalance，你可以自动维护 TiDB server 节点信息，并在客户端使用 tidb-loadbalance 策略分配 JDBC 连接。客户端应用与 TiDB server 之间直接使用 JDBC 连接的性能高于使用负载均衡组件。

目前，tidb-loadbalance 支持以下策略：roundrobin、random 和 weight。

> **Note:**
>
> tidb-loadbalance 必须与 [mysql-connector-j](https://github.com/pingcap/mysql-connector-j) 搭配使用。

如果你使用 Maven，请在 `pom.xml` 文件的 `<dependencies></dependencies>` 元素体中添加以下内容：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.2</version>
</dependency>
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>tidb-loadbalance</artifactId>
  <version>0.0.5</version>
</dependency>
```

如果你使用 Gradle，请在 `dependencies` 中添加以下内容：

```gradle
implementation group: 'io.github.lastincisor', name: 'mysql-connector-java', version: '8.0.29-tidb-1.0.2'
implementation group: 'io.github.lastincisor', name: 'tidb-loadbalance', version: '0.0.5'
```

## Golang

本节介绍如何在 Golang 中使用驱动和 ORM 框架。

### Golang 驱动

**go-sql-driver/mysql**

支持级别：**Full**

关于如何下载和配置 Golang 驱动，请参考 [go-sql-driver/mysql 文档](https://github.com/go-sql-driver/mysql)。

关于如何构建完整应用的示例，请参见 [使用 Go-MySQL-Driver 连接 TiDB](/develop/dev-guide-sample-application-golang-sql-driver.md)。

### Golang ORM 框架

**GORM**

支持级别：**Full**

GORM 是 Golang 中流行的 ORM 框架。你可以使用 `go get` 命令获取应用的所有依赖。

```shell
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```

关于如何使用 GORM 构建 TiDB 应用的示例，请参见 [使用 GORM 连接 TiDB](/develop/dev-guide-sample-application-golang-gorm.md)。

## Python

本节介绍如何在 Python 中使用驱动和 ORM 框架。

### Python 驱动

<SimpleTab>
<div label="PyMySQL">

支持级别：**Compatible**

你可以按照 [PyMySQL 文档](https://pypi.org/project/PyMySQL/) 下载并配置驱动。推荐使用 PyMySQL 1.0.2 或更高版本。

关于如何使用 PyMySQL 构建 TiDB 应用的示例，请参见 [使用 PyMySQL 连接 TiDB](/develop/dev-guide-sample-application-python-pymysql.md)。

</div>
<div label="mysqlclient">

支持级别：**Compatible**

你可以按照 [mysqlclient 文档](https://pypi.org/project/mysqlclient/) 下载并配置驱动。推荐使用 mysqlclient 2.1.1 或更高版本。

关于如何使用 mysqlclient 构建 TiDB 应用的示例，请参见 [使用 mysqlclient 连接 TiDB](/develop/dev-guide-sample-application-python-mysqlclient.md)。

</div>
<div label="MySQL Connector/Python">

支持级别：**Compatible**

你可以按照 [MySQL Connector/Python 文档](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html) 下载并配置驱动。推荐使用 Connector/Python 8.0.31 或更高版本。

关于如何使用 MySQL Connector/Python 构建 TiDB 应用的示例，请参见 [使用 MySQL Connector/Python 连接 TiDB](/develop/dev-guide-sample-application-python-mysql-connector.md)。

</div>
</SimpleTab>

### Python ORM 框架

<SimpleTab>
<div label="Django">

支持级别：**Full**

[Django](https://docs.djangoproject.com/) 是流行的 Python Web 框架。为解决 TiDB 与 Django 的兼容性问题，PingCAP 提供了 TiDB 方言 `django-tidb`。安装方法请参见 [`django-tidb` 文档](https://github.com/pingcap/django-tidb#installation-guide)。

关于如何使用 Django 构建 TiDB 应用的示例，请参见 [使用 Django 连接 TiDB](/develop/dev-guide-sample-application-python-django.md)。

</div>
<div label="SQLAlchemy">

支持级别：**Full**

[SQLAlchemy](https://www.sqlalchemy.org/) 是 Python 中流行的 ORM 框架。你可以使用 `pip install SQLAlchemy==1.4.44` 命令获取应用的所有依赖。推荐使用 SQLAlchemy 1.4.44 或更高版本。

关于如何使用 SQLAlchemy 构建 TiDB 应用的示例，请参见 [使用 SQLAlchemy 连接 TiDB](/develop/dev-guide-sample-application-python-sqlalchemy.md)。

</div>
<div label="peewee">

支持级别：**Compatible**

[peewee](http://docs.peewee-orm.com/en/latest/) 是 Python 中流行的 ORM 框架。你可以使用 `pip install peewee==3.15.4` 命令获取应用的所有依赖。推荐使用 peewee 3.15.4 或更高版本。

关于如何使用 peewee 构建 TiDB 应用的示例，请参见 [使用 peewee 连接 TiDB](/develop/dev-guide-sample-application-python-peewee.md)。

</div>
</SimpleTab>

<CustomContent platform="tidb-cloud">

在你确定了驱动或 ORM 之后，可以 [连接到你的 TiDB 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

</CustomContent>

## 需要帮助？

<CustomContent platform="tidb">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>