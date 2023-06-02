---
title: CRUD SQL in TiDB
summary: A brief introduction to TiDB's CURD SQL.
---

# CRUD SQL in TiDB

This document briefly introduces how to use TiDB's CURD SQL.

## Before you start

Please make sure you are connected to a TiDB cluster. If not, refer to [Build a TiDB Serverless Cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster) to create a TiDB Serverless cluster.

## Explore SQL with TiDB

> **Note:**
>
> This document references and simplifies [Explore SQL with TiDB](/basic-sql-operations.md). For more details, see [Explore SQL with TiDB](/basic-sql-operations.md).

TiDB is compatible with MySQL, you can use MySQL statements directly in most cases. For unsupported features, see [Compatibility with MySQL](/mysql-compatibility.md#unsupported-features).

To experiment with SQL and test out TiDB compatibility with MySQL queries, you can try Chat2Query (beta) in your [TiDB Cloud console](https://tidbcloud.com/). To access Chat2Query, go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click your cluster name, and then click **Chat2Query** in the left navigation pane. In Chat2Query, you can either let AI generate SQL queries automatically or write SQL queries manually, and run SQL queries against databases without a terminal.

> **Note:**
>
> Chat2Query currently has limited support on SQL statements. DDLs such as `CREATE TABLE` or `DROP TABLE` are not supported yet.
>
> <CustomContent platform="tidb">
>
> If you want to explore all SQL statements with TiDB, you can deploy a TiDB cluster and then run SQL statements in it.
>
> </CustomContent>
>
> <CustomContent platform="tidb-cloud">
>
> If you want to explore all SQL statements with TiDB, you can [connect to your TiDB Cloud cluster](/tidb-cloud/connect-to-tidb-cluster.md) and then run SQL statements from a SQL client.
>
> </CustomContent>

This page walks you through the basic TiDB SQL statements such as DDL, DML, and CRUD operations. For a complete list of TiDB statements, see [TiDB SQL Syntax Diagram](https://pingcap.github.io/sqlgram/).

## Category

SQL is divided into the following 4 types according to their functions:

- **DDL (Data Definition Language)**: It is used to define database objects, including databases, tables, views, and indexes.

- **DML (Data Manipulation Language)**: It is used to manipulate application related records.

- **DQL (Data Query Language)**: It is used to query the records after conditional filtering.

- **DCL (Data Control Language)**: It is used to define access privileges and security levels.

The following mainly introduces DML and DQL. For more information about DDL and DCL, see [Explore SQL with TiDB](/basic-sql-operations.md) or [TiDB SQL syntax detailed explanation](https://pingcap.github.io/sqlgram/).

## Data Manipulation Language

Common DML features are adding, modifying, and deleting table records. The corresponding commands are `INSERT`, `UPDATE`, and `DELETE`.

To insert data into a table, use the `INSERT` statement:

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

To insert a record containing data of some fields into a table, use the `INSERT` statement:

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

To update some fields of a record in a table, use the `UPDATE` statement:

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

To delete the data in a table, use the `DELETE` statement:

```sql
DELETE FROM person WHERE id=2;
```

> **Note:**
>
> The `UPDATE` and `DELETE` statements without the `WHERE` clause as a filter operate on the entire table.

## Data Query Language

DQL is used to retrieve the desired data rows from a table or multiple tables.

To view the data in a table, use the `SELECT` statement:

```sql
SELECT * FROM person;
```

To query a specific column, add the column name after the `SELECT` keyword:

```sql
SELECT name FROM person;
```

The result is as follows:

```
+------+
| name |
+------+
| tom  |
+------+
1 rows in set (0.00 sec)
```

Use the `WHERE` clause to filter all records that match the conditions and then return the result:

```sql
SELECT * FROM person WHERE id < 5;
```
