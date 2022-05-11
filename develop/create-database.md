---
title: Create a Database
summary: Methods, rules to be followed and examples when creating a database.
---

# Create a Database

In this section, we will begin to cover how to create databases using SQL and various programming languages, and the rules to follow when creating databases. In this section, we will cover the database creation part of TiDB around the [Bookshop](/develop/bookshop-schema-design.md) application.

> **Note:**
>
> The `CREATE DATABASE` statement is only briefly described here; for detailed reference documentation (including additional examples), see the [CREATE DATABASE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-database) documentation.

## Before you start

Before reading this page, you need to prepare the following:

- [Build a TiDB Cluster in TiDB Cloud(DevTier)](/develop/build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/schema-design-overview.md).

## What is database

[Database](/develop/schema-design-overview.md) objects in TiDB can contain **tables**, **views**, **sequences**, and other objects.

## Create Database

You can use the `CREATE DATABASE` statement to create a database. This will create an empty file with a `.sql` file extension at the end of the file. We will use this file to initialize the database that will store all the data for the entire [Bookshop](/develop/bookshop-schema-design.md) sample application.

{{< copyable "shell-regular" >}}

```shell
touch dbinit.sql
```

Then, open `dbinit.sql` in a text editor and add the `CREATE DATABASE` statement to the top of the file.

{{< copyable "sql" >}}

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

This statement will create a database named `bookshop` (if it does not already exist).

To execute the library build statement in the `dbinit.sql` file as the **root user**, run the following command:

{{< copyable "shell-regular" >}}

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < dbinit.sql
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

- Follow the [Database Naming Guidelines](/develop/object-naming-guidelines.md) and give your database a meaningful name.
- The `test` database is a default database provided by TiDB. Try not to use it in a production environment if you don't have to. You can create the database yourself with the `CREATE DATABASE` statement and [change the current database](/common/sql-statements/sql-statement-use.md) with the `USE {databasename};` statement in the SQL session.
- Create the **database**, **roles**, **users**, etc. using the root user. and grant only the necessary privileges.
As a general rule, we do not recommend using Driver, ORM to define and change the database schema. Instead, please use **MySQL command-line client** or other **MySQL GUI client** of your choice to do so.

## One more step

At this point, you have finished preparing the `bookshop` database and can add **tables** to it.

You can continue reading [the create a table](/develop/create-table.md) for guidance.
