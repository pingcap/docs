---
title: Overview
summary: Overview of TiDB database schema design.
---

# Overview

This page gives an overview of the database schema in TiDB. We will start from this page, design a database, and use this database for subsequent data writing and reading examples.

> **Note:**
>
> To avoid confusion with the general term, Here is a brief agreement on the term used in the database schema design documentation section:
>
> 1. To avoid confusion with the generic term [Database](https://en.wikipedia.org/wiki/Database), we will refer to the logical object as **Database**, TiDB will still use the **TiDB**, and the deployed instances of TiDB will be referred to as **Cluster**.
> 2. Because TiDB uses a MySQL-compatible syntax, under this syntax, **Schema** represents a [generic term definition only](https://en.wiktionary.org/wiki/schema), and there is no **logical object definition**, that can be found in this [official document](https://dev.mysql.com/doc/refman/8.0/en/create-database.html). Please note this difference if you are migrating from other databases that have Schema logical objects (e.g. [PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html), [Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html), [Microsoft SQL Server](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15), etc.).

## Database

Database in the TiDB can be thought of as a collection of objects such as tables and indexes.

TiDB clusters contain a database named `test`. However, we recommend that you create your own database instead of using the `test` database.

## Table

A Table in the TiDB is subordinate to a [Database](#database).

A table contains **rows**. Each value in each row of data belongs to a specific **column**. Each column allows only a single data type. Columns can be further qualified by adding [constraints](https://docs.pingcap.com/tidb/stable/constraints). You can also add [generated columns (experimental feature)](https://docs.pingcap.com/tidb/stable/generated-columns) for calculations.

## Index

An index is a copy of rows in a single table, sorted by a column or set of columns.TiDB queries use indexes to find data in a table more efficiently while giving values for specific columns. Each index is subordinate to a particular [table](#table).

There are two common types of indexes:

1. **Primary Key**: Indexes that are identified on the primary key column.
2. **Secondary Index**: Indexes identified on non-primary keys

> **Note:**
>
> In TiDB, the default definition of **Primary Key** is different from [InnoDB](https://mariadb.com/kb/en/innodb/)(the common storage engine of MySQL). In **InnoDB**, The semantics of **Primary Key** is unique, not null, and **index clustered**.
>
> However, in TiDB, the definition of **Primary Key** is: unique, not null. But the primary key is not guaranteed to be a **clustered index**. Instead, another set of keywords `CLUSTERED` / `NONCLUSTERED` additionally controls whether the **Primary Key** is a **Clustered Index**, and if not specified, is affected by the system variable `@@global.tidb_enable_clustered_index`, as described in [this document](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes).

### Specialized indexes

TiDB supports some specialized types of indexes, designed to improve query performance in specific use cases. For guidance on specialized indexes, see the following table:

| Indexing and constraints                                     | **5.4**          |   **5.3**    |   **5.2**    |   **5.1**    |   **5.0**    |   **4.0**    |
| ------------------------------------------------------------ | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [Expression indexes](/common/sql-statements/sql-statement-create-index.md#expression-index) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [Columnar storage (TiFlash)](/tiflash/tiflash-overview.md)   | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [RocksDB engine](/storage-engine/rocksdb-overview.md)        | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Titan plugin](/storage-engine/titan-overview.md)            | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Invisible indexes](/common/sql-statements/sql-statement-add-index.md) | Y            |      Y       |      Y       |      Y       |      Y       |      N       |
| [Composite `PRIMARY KEY`](/constraints.md)                   | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Unique indexes](/constraints.md)                            | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Clustered index on integer `PRIMARY KEY`](/constraints.md)  | Y            |      Y       |      Y       |      Y       |      Y       |      Y       |
| [Clustered index on composite or non-integer key](/constraints.md) | Y            |      Y       |      Y       |      Y       |      Y       |      N       |

## Other logical objects

TiDB supports several logical objects at the same level as **table**:

1. [Views](https://docs.pingcap.com/tidb/stable/views): A view acts as a virtual table, whose schema is defined by the `SELECT` statement that creates the view.
2. [Sequence](https://docs.pingcap.com/tidb/stable/sql-statement-create-sequence): Create and store sequential data.
3. [Temporary tables](https://docs.pingcap.com/tidb/stable/temporary-tables): Temporary table is a table whose data is not persistent.

## Access Control

TiDB supports user-based or role-based access control. You can grant **users** [permission](https://docs.pingcap.com/tidb/stable/privilege-management) to view, modify, or delete data objects and data schemas through [roles](https://docs.pingcap.com/tidb/stable/role-based-access-control) or directly to [users](https://docs.pingcap.com/tidb/stable/user-account-management).

## Execute database schema changes

We do not recommend using a Driver or ORM to change database schemas. As a best practice from experience, we recommend using a [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) or using any GUI client you like. In this document, we will execute database schema changes using the **MySQL client**.

## Object Limitations

These are some of the common object size restrictions, please refer to [tidb limitations](https://docs.pingcap.com/tidb/stable/tidb-limitations) for detailed usage restrictions.

## Limitations on identifier length

| Identifier type | Maximum length (number of characters allowed) |
|:---------|:--------------|
| Database | 64 |
| Table    | 64 |
| Column   | 64 |
| Index    | 64 |
| View     | 64 |
| Sequence | 64 |

## Limitations on a single table

| Type       | Upper limit (default value)  |
|:----------|:----------|
| Columns   | Defaults to 1017 and can be adjusted up to 4096     |
| Indexes   |  Defaults to 64 and can be adjusted up to 512        |
| Partitions | 8192     |
| Single Line Size | 6 MB by default. You can adjust the size limit via the [**txn-entry-size-limit**](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50) configuration item. |
| Single Column in a Line Size | 6 MB       |

## Limitations on string types

| Type       | Upper limit   |
|:----------|:----------|
| CHAR       | 256 characters      |
| BINARY     | 256 characters      |
| VARBINARY  | 65535 characters    |
| VARCHAR    | 16383 characters    |
| TEXT       | 6 MB                |
| BLOB       | 6 MB                |

### Number of rows

TiDB can support **any** number of rows by adding nodes in the cluster, see the [tidb best practices](https://docs.pingcap.com/tidb/stable/tidb-best-practices) for the mechanics.
