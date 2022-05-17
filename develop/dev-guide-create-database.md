---
title: Create a Database
summary: Learn methods, rules, and examples to create a database.
---

# Create a Database

In this section, we will begin to cover how to create databases using SQL and various programming languages, and the rules to follow when creating databases. In this section, we will cover the database creation part of TiDB around the [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application.

> **Note:**
>
> The `CREATE DATABASE` statement is only briefly described here; for detailed reference documentation (including additional examples), see the [CREATE DATABASE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-database) documentation.

## Before you start

Before reading this page, you need to prepare the following:

- [Build a TiDB Cluster in TiDB Cloud(DevTier)](/develop/dev-guide-build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/dev-guide-schema-design-overview.md).

## What is database

[Database](/develop/dev-guide-schema-design-overview.md) objects in TiDB can contain **tables**, **views**, **sequences**, and other objects.

## Create Database

You can use the `CREATE DATABASE` statement to create a database.

{{< copyable "sql" >}}

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

This statement will create a database named `bookshop` (if it does not already exist).

To execute the library build statement as the **root user**, run the following command:

{{< copyable "shell-regular" >}}

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "CREATE DATABASE IF NOT EXISTS bookshop;"
```

To view the databases in the cluster, execute a `SHOW DATABASES` statement.

{{< copyable "shell-regular" >}}

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "SHOW DATABASES;"
```

```
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| bookshop           |
| mysql              |
| test               |
+--------------------+
```

## Rules to follow when creating a database

- Follow the [Database Naming Guidelines](/develop/dev-guide-object-naming-guidelines.md) and give your database a meaningful name.
- The `test` database is a default database provided by TiDB. Try not to use it in a production environment if you don't have to. You can create the database yourself with the `CREATE DATABASE` statement and [change the current database](/common/sql-statements/sql-statement-use.md) with the `USE {databasename};` statement in the SQL session.
- Create the **database**, **roles**, **users**, etc. using the root user. and grant only the necessary privileges.
- As a general rule, we do not recommend using Driver, ORM to define and change the database schema. Instead, please use **MySQL command-line client** or other **MySQL GUI client** of your choice to do so.

## One more step

At this point, you have finished preparing the `bookshop` database and can add **tables** to it.

You can continue reading [the create a table](/develop/dev-guide-create-table.md) for guidance.
