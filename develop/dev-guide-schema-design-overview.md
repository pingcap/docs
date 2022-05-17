---
title: Overview
summary: Overview of TiDB database schema design.
---

# TiDB database schema design overview

This document provides an overview of database schema design in TiDB. In the subsequent documents, [Bookshop](/develop/dev-guide-bookshop-schema-design.md) is taken as an example to show you how to design a database and use the database for data read and write operations.

## About terms used in the database schema design

To avoid confusion with the general term, Here is a brief agreement on the term used in the database schema design documentation section:

To avoid confusion with the generic term [Database](https://en.wikipedia.org/wiki/Database), we will refer to the logical object as **Database**, TiDB will still use the **TiDB**, and the deployed instances of TiDB will be referred to as **Cluster**.

Because TiDB uses a MySQL-compatible syntax, under this syntax, **Schema** represents a [generic term definition only](https://en.wiktionary.org/wiki/schema), and there is no **logical object definition**, that can be found in this [official document](https://dev.mysql.com/doc/refman/8.0/en/create-database.html).

Please note this difference if you are migrating from other databases that have Schema logical objects (e.g. [PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html), [Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html), [Microsoft SQL Server](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15), etc.).

## Database

Database in the TiDB can be thought of as a collection of objects such as tables and indexes.

TiDB clusters contain a database named `test`. However, we recommend that you create your own database instead of using the `test` database.

## Table

A Table in the TiDB is subordinate to a [Database](#database).

A table contains **rows**. Each value in each row of data belongs to a specific **column**. Each column allows only a single data type. Columns can be further qualified by adding [constraints](/constraints.md). You can also add [generated columns (experimental feature)](/generated-columns.md) for calculations.

## Index

An index is a copy of selected columns in a table. You can create an index using one or more columns of a [table](#table). With indexes, TiDB can quickly locate data without having to search every row in a table every time, which greatly improves your query performance.

There are two common types of indexes:

- **Primary Key**: Indexes on the primary key column.
- **Secondary Index**: Indexes on non-primary key columns.

> **Note:**
>
> In TiDB, the default definition of **Primary Key** is different from [InnoDB](https://mariadb.com/kb/en/innodb/)(the common storage engine of MySQL). In **InnoDB**, The semantics of **Primary Key** is unique, not null, and **index clustered**.
>
> However, in TiDB, the definition of **Primary Key** is: unique, not null. But the primary key is not guaranteed to be a **clustered index**. Instead, another set of keywords `CLUSTERED` / `NONCLUSTERED` additionally controls whether the **Primary Key** is a **Clustered Index**, and if not specified, is affected by the system variable `@@global.tidb_enable_clustered_index`, as described in [this document](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes).

### Specialized indexes

To improve query performance of various user scenarios, TiDB provides some specialized types of indexes. For details of each type, see the following links:

- [Expression indexes](/common/sql-statements/sql-statement-create-index.md#expression-index) (Experimental)
- [Columnar storage (TiFlash)](/tiflash/tiflash-overview.md)
- [RocksDB engine](/storage-engine/rocksdb-overview.md)
- [Titan plugin](/storage-engine/titan-overview.md)
- [Invisible indexes](/common/sql-statements/sql-statement-add-index.md)
- [Composite `PRIMARY KEY`](/constraints.md#primary-key)
- [Unique indexes](/constraints.md#unique-key)
- [Clustered indexes on integer `PRIMARY KEY`](/constraints.md)
- [Clustered indexes on composite or non-integer key](/constraints.md)

## Other supported logical objects

TiDB supports several logical objects at the same level as **table**:

- [Views](/views.md): a view acts as a virtual table, whose schema is defined by the `SELECT` statement that creates the view.
- [Sequence](/common/sql-statements/sql-statement-create-sequence.md): a sequence generates and stores sequential data.
- [Temporary tables](/temporary-tables.md): a table whose data is not persistent.

## Access Control

TiDB supports both user-based and role-based access control. To allow users to view, modify, or delete data objects and data schemas, you can either grant [privileges](/privilege-management.md) to [users](/user-account-management.md) directly or grant [privileges](/privilege-management.md) to users through [roles](/role-based-access-control.md).

## Database schema changes

To change database schemas, using a Driver or ORM  is not recommended. Instead, it is recommended that you use a [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) or any GUI client, which is a best practice based on experience. In the subsequent documents, **MySQL client** will be used to execute database schema changes.

## Object limitations

This section describes the object limitations on identifier length, a single table, and string types. For more information, see [TiDB Limitations](/tidb-limitations.md).

### Limitations on identifier length

| Identifier type | Maximum length (number of characters allowed) |
|:---------|:--------------|
| Database | 64 |
| Table    | 64 |
| Column   | 64 |
| Index    | 64 |
| View     | 64 |
| Sequence | 64 |

### Limitations on a single table

| Type       | Upper limit (default value)  |
|:----------|:----------|
| Columns   | Defaults to 1017 and can be adjusted up to 4096     |
| Indexes   |  Defaults to 64 and can be adjusted up to 512        |
| Partitions | 8192     |
| Single Line Size | 6 MB by default. You can adjust the size limit via the [**txn-entry-size-limit**](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50) configuration item. |
| Single Column in a Line Size | 6 MB       |

### Limitations on string types

| Type       | Upper limit   |
|:----------|:----------|
| CHAR       | 256 characters      |
| BINARY     | 256 characters      |
| VARBINARY  | 65535 characters    |
| VARCHAR    | 16383 characters    |
| TEXT       | 6 MB                |
| BLOB       | 6 MB                |

## Number of rows

TiDB supports **unlimited** number of rows by adding nodes to the cluster. For the relevant principles, see [TiDB Best Practices](/best-practices/tidb-best-practices.md).
