---
title: SQL
summary: Learn about SQL concepts for TiDB.
---

# SQL

TiDB is highly compatible with the MySQL protocol and the common features and syntax of MySQL 5.7 and MySQL 8.0. The ecosystem tools for MySQL (PHPMyAdmin, Navicat, MySQL Workbench, DBeaver and [more](https://docs.pingcap.com/tidb/v7.2/dev-guide-third-party-support#gui)) and the MySQL client can be used for TiDB.

However, some features of MySQL are not supported in TiDB. This could be because there is now a better way to solve the problem (such as the use of JSON instead of XML functions) or a lack of current demand versus effort required (such as stored procedures and functions). Additionally, some features might be difficult to implement in a distributed system. For more information, see [MySQL Compatibility](/mysql-compatibility.md).

## SQL statements

A SQL statement is a command or instruction in SQL (Structured Query Language) composed of identifiers, parameters, variables, data types, and reserved SQL keywords. It directs the database to perform specific actions, such as retrieving, modifying, or managing data and database structures.

TiDB uses SQL statements that aim to follow ISO/IEC SQL standards, with extensions for MySQL and TiDB-specific statements where necessary.

SQL is divided into the following 4 types according to their functions:

- DDL (Data Definition Language): It is used to define database objects, including databases, tables, views, and indexes. For DDL statements in TiDB, see [Schema management / Data definition statements (DDL)](/sql-statements/sql-statement-overview.md#schema-management--data-definition-statements-ddl).

- DML (Data Manipulation Language): It is used to manipulate application related records. For DML statements in TiDB, see [Data manipulation statements (DML)](/sql-statements/sql-statement-overview.md#data-manipulation-statements-dml).

- DQL (Data Query Language): It is used to query the records after conditional filtering.

- DCL (Data Control Language): It is used to define access privileges and security levels.

To get an overview of SQL statements in TiDB, see [SQL Statement Overview](/sql-statements/sql-statement-overview.md).

## SQL mode

TiDB servers operate in different SQL modes and apply these modes differently for different clients. SQL mode defines the SQL syntax that TiDB supports and the type of data validation check to perform.

For more information, see [SQL Mode](/sql-mode.md).

## Row ID generation attributes

TiDB provides three SQL attributes to optimize row ID generation and data distribution to address performance and scalability challenges.

- AUTO_INCREMENT

- AUTO_RANDOM

- SHARD_ROW_ID_BITS

### AUTO_INCREMENT

`AUTO_INCREMENT` is a column attribute that is used to automatically fill in default column values. When the `INSERT` statement does not specify values for the `AUTO_INCREMENT` column, the system automatically assigns values to this column.

For performance reasons, `AUTO_INCREMENT` numbers are allocated in a batch of values (30 thousand by default) to each TiDB server. This means that while `AUTO_INCREMENT` numbers are guaranteed to be unique, values assigned to an `INSERT` statement will only be monotonic on a per TiDB server basis.

If you want the `AUTO_INCREMENT` numbers to be monotonic on all TiDB servers and your TiDB version is v6.5.0 or later, it is recommended to enable the [MySQL compatibility mode](/auto-increment.md#mysql-compatibility-mode).

For more information, see [AUTO_INCREMENT](/auto-increment.md).

### AUTO_RANDOM

`AUTO_RANDOM` is a column attribute that is used to automatically assign values to a `BIGINT` column. Values assigned automatically are random and unique. Since the value of `AUTO_RANDOM` is random and unique, `AUTO_RANDOM` is often used in place of [`AUTO_INCREMENT`](/auto-increment.md) to avoid write hotspot in a single storage node caused by TiDB assigning consecutive IDs.

Since the value of `AUTO_RANDOM` is random and unique, `AUTO_RANDOM` is often used in place of [`AUTO_INCREMENT`](/auto-increment.md)to avoid write hotspot in a single storage node caused by TiDB assigning consecutive IDs. If the current `AUTO_INCREMENT` column is a primary key and the type is `BIGINT`, you can execute the `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);` statement to switch from `AUTO_INCREMENT` to `AUTO_RANDOM`.

For more information, see [AUTO_RANDOM](/auto-random.md).

### SHARD_ROW_ID_BITS

For the tables with a non-clustered primary key or no primary key, TiDB uses an implicit auto-increment row ID. When a large number of `INSERT` operations are performed, the data is written into a single Region, causing a write hot spot.

To mitigate the hot spot issue, you can configure [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md). The row IDs are scattered and the data are written into multiple different Regions.

## Keywords

Keywords are words that have special meanings in SQL statements, such as `SELECT`, `UPDATE`, and `DELETE`.

- Some of them can be used as identifiers directly, which are called non-reserved keywords.

- Some of them require special treatment before being used as identifiers, which are called reserved keywords.

However, there are special non-reserved keywords that might still require special treatment. It is recommended that you treat them as reserved keywords.

For more information, see [Keywords](/keywords.md).

## User-defined variables

TiDB lets you set and read the user-defined variables. The format of the user-defined variables is `@var_name`. The characters that compose `var_name` can be any characters that can compose an identifier, including the numbers `0-9`, the letters `a-zA-Z`, the underscore `_`, the dollar sign `$`, and the UTF-8 characters. In addition, it also includes the English period `.`. The user-defined variables are case-insensitive.

The user-defined variables are session-specific, which means a user variable defined by one client connection cannot be seen or used by other client connections.

For more information, see [User-Defined Variables](/user-defined-variables.md).

## Metadata lock

In TiDB, a metadata lock is a mechanism introduced to manage changes to table metadata during online schema changes. When a transaction begins, it locks onto a snapshot of the current metadata. If the metadata changes during the transaction, TiDB throws an "Information schema is changed" error, preventing the transaction from committing. The metadata lock coordinates Data Manipulation Language (DML) and Data Definition Language (DDL) operations by prioritizing DMLs, ensuring that in-progress DML transactions with outdated metadata commit before applying new DDL changes, thus minimizing errors and maintaining data consistency.

For more information, see [Metadata Lock](/metadata-lock.md).