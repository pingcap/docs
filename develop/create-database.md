---
title: Create a Database
summary: The ways, best practices, and examples for creating databases.
---

# Create a Database

This page provides a best practice guide for creating a database and an example of a [bookshop](/develop/bookshop-schema-design.md) database based on TiDB.

> **Note:**
>
> Detailed reference document for the [CREATE DATABASE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-database) statement, with additional examples, can be found in the `CREATE DATABASE` documentation.

## Before you start

Before reading this page, you need to prepare the following:

- [Build a TiDB Cluster in TiDB Cloud(DevTier)](/develop/build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/schema-design-overview.md).

## Create Database

[Database](/develop/schema-design-overview.md) logical object is a collection of TiDB **tables**, **views**, **sequences**, etc.

To create a database, use the `CREATE DATABASE` statement and follow [Database Best Practices](#database-best-practices).

### Database Best Practices

Here are some best practices to follow when you create and use databases:

- Try not to use a `test` database that already exists. Instead, you should use the `CREATE DATABASE` statement to create the database and use the `USE {databasename};` statement in the SQL session to [change the current database](https://docs.pingcap.com/tidb/stable/sql-statement-use).
- Create the **database**, **roles**, **users**, etc. using the **root user**. and grant **_only_** the necessary privileges.
- As a general best practice, we do not recommend using Driver / ORM for database schema definition and changes. Instead, use the **MySQL command-line client** or other **MySQL GUI client** of your preferred.
- Following [Database Naming Guidelines](/develop/object-naming-guidelines.md)

### Example

Create an empty file with a `.sql` file extension at the end of the file. We will use this file to initialize the database that will store all the data for the entire `bookshop` sample application.

e.g.

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

At this point, you have finished preparing the `bookshop` database and can add **tables** to it.

You can continue reading [the create a table](/develop/create-table.md) for guidance.
