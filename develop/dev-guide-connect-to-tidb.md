---
title: Connect to TiDB
summary: Describes how to connect to TiDB.
---

# Connect to TiDB

**TiDB** is highly compatible with **MySQL 5.7** protocol, for a full list of client link parameters, see [MySQL Client Options](https://dev.mysql.com/doc/refman/5.7/en/mysql-command-options.html).

TiDB supports the [MySQL Client/Server Protocol](https://dev.mysql.com/doc/internals/en/client-server-protocol.html). This allows most client drivers and ORM frameworks to connect to TiDB just as they connect to MySQL.

## MySQL Shell

You can use MySQL Shell as a command line tool for TiDB. You can find the installation method for different operating systems in the [MySQL Shell documentation](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html). After the installation you can connect to TiDB using the following command-line:

{{< copyable "shell-regular" >}}

```shell
mysql --host <tidb_server_host> --port 4000 -u root -p --comments
```

> **Note:**
>
> The MySQL command-line client cleared [Optimizer Hints](/optimizer-hints.md#optimizer-hints) by default before version 5.7.7. If you need to use the Hint syntax in these earlier versions of the client, you need to add the `--comments` option when starting the client.

## JDBC

You can connect to TiDB using the [JDBC](https://dev.mysql.com/doc/connector-j/8.0/en/) driver, which requires creating a `MysqlDataSource` or `MysqlConnectionPoolDataSource` object (both of which implement the `DataSource` interface) and set the connection string using the `setURL` function.

For example:

{{< copyable "" >}}

```java
MysqlDataSource mysqlDataSource = new MysqlDataSource();
mysqlDataSource.setURL("jdbc:mysql://{host}:{port}/{database}?user={username}&password={password}");
```

For more information on JDBC connections, refer to the official [JDBC documentation](https://dev.mysql.com/doc/connector-j/8.0/en/)

### Connection parameters

| Parameter Name | Description |
| :---: | :----------------------------: |
| `{username}` | [SQL users](/user-account-management.md) that need to connect to the TiDB cluster |
| `{password}` | The password of the `SQL user` |
| `{host}` | [Host](https://en.wikipedia.org/wiki/Host_(network)) of TiDB nodes |
| `{port}` | Port that the TiDB node is listening on |
| `{database}` | Name of the database (that already exists) |

## Hibernate

You can connect to TiDB using the [Hibernate ORM](https://hibernate.org/orm/). Set `hibernate.connection.url` in Hibernate configuration to a legal TiDB connection string.

For example, if you use the `hibernate.cfg.xml` configuration file, then your configuration file should be:

{{< copyable "" >}}

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://{host}:{port}/{database}?user={user}&amp;password={password}</property>
    </session-factory>
</hibernate-configuration>
```

Subsequently, the configuration file is read using the code to obtain the `SessionFactory` object:

{{< copyable "" >}}

```java
SessionFactory sessionFactory = new Configuration().configure("hibernate.cfg.xml").buildSessionFactory();
```

Here are a few points to note:

1. Since we are using the configuration file `hibernate.cfg.xml` is XML format, and the `&` character, which is a special character in XML, needs to be changed from `&` to `&amp;`. That means, our connection string `hibernate.connection.url` need changed from `jdbc:mysql://{host}:{port}/{database}?user={user}&password={password}` to `jdbc:mysql://{host}:{ port}/{database}?user={user}&amp;password={password}`.
2. When you use Hibernate, we recommend that you use the `TiDB` dialect, which is `hibernate.dialect` set to `org.hibernate.dialect.TiDBDialect`.
3. Hibernate supports TiDB dialects in version `6.0.0.Beta2` and above, so we recommend using `6.0.0.Beta2` and above for Hibernate

For more information about Hibernate connection parameters, see the [Hibernate documentation](https://hibernate.org/orm/documentation).

### Connection parameters

| Parameter Name | Description |
| :---: | :----------------------------: |
| `{username}` | [SQL users](/user-account-management.md) that need to connect to the TiDB cluster |
| `{password}` | The password of the `SQL user` |
| `{host}` | [Host](https://en.wikipedia.org/wiki/Host_(network)) of TiDB nodes |
| `{port}` | Port that the TiDB node is listening on |
| `{database}` | Name of the database (that already exists) |
