---
title: Database Schema
summary: Learn about database schema concepts for TiDB Cloud.
---

# Database Schema

A database schema defines the structure and organization of data within databases, tables, columns, indexes, and other objects.

This document introduces the key concepts of database schemas, such as databases, tables, columns, data types, constraints, and indexes. It also introduces advanced features such as temporary tables for managing intermediate data seamlessly, vector indexes for efficient approximate nearest neighbor (ANN) searches, and cached tables to improve read performance.

## Databases

A database in TiDB is a collection of objects such as tables and indexes.

### System databases

System databases are default databases created by TiDB to store system tables. TiDB provides the following system databases:

- [`INFORMATION_SCHEMA`](/information-schema/information-schema.md)

- [`mysql`](/mysql-schema/mysql-schema.md)

- [`performance_schema`](/performance-schema/performance-schema.md)

- [`sys`](/sys-schema/sys-schema.md)

### `test` database

TiDB comes with a default database named `test`. However, it is recommended that you create your own database instead of using the `test` database.

## Tables

A table is a collection of related data in a [database](/develop/dev-guide-schema-design-overview.md#database).

Each table consists of rows and columns. Each value in a row belongs to a specific column. Each column allows only a single data type. To further qualify columns, you can add some [constraints](/constraints.md). To accelerate calculations, you can add [generated columns](/generated-columns.md).

### System table

- The `mysql` schema contains TiDB system tables. The design is similar to the `mysql` schema in MySQL, where tables such as `mysql.user` can be edited directly. It also contains a number of tables that are extensions to MySQL.

- Information Schema provides an ANSI-standard way of viewing system metadata. TiDB also provides a number of custom `INFORMATION_SCHEMA` tables, in addition to the tables included for MySQL compatibility. Many `INFORMATION_SCHEMA` tables have a corresponding `SHOW` command. The benefit of querying `INFORMATION_SCHEMA` is that it is possible to join between tables.

- Performance Schema. TiDB implements performance schema tables for MySQL compatibility.

### Cached table

TiDB introduces the [cached table](/cached-tables.md) feature for frequently accessed but rarely updated small hotspot tables. When this feature is used, the data of an entire table is loaded into the memory of the TiDB server, and TiDB directly gets the table data from the memory without accessing TiKV, which improves the read performance.

### Temporary table

The temporary tables feature solves the issue of temporarily storing the intermediate results of an application, which frees you from frequently creating and dropping tables. You can store the intermediate calculation data in temporary tables. When the intermediate data is no longer needed, TiDB automatically cleans up and recycles the temporary tables. This avoids user applications being too complicated, reduces table management overhead, and improves performance.

### Partitioned table

In TiDB, [partitioning](/partitioned-table.md) enables you to divide a large table into one or more manageable pieces called partitions. Each partition is independent and can be managed individually.

## Columns

A column is subordinate to a table. Each table has at least one column. Columns provide a structure to a table by dividing the values in each row into small cells of a single data type.

For more information, see [Define columns](/develop/dev-guide-create-table.md#define-columns).

## Generated columns

TiDB lets you extract data from the JSON data type as a [generated column](/generated-columns.md).

Unlike general columns, the value of the generated column is calculated by the expression in the column definition. When inserting or updating a generated column, you cannot assign a value, but only use `DEFAULT`.

There are two kinds of generated columns: virtual and stored. A virtual generated column occupies no storage and is computed when it is read. A stored generated column is computed when it is written (inserted or updated) and occupies storage. Compared with the virtual generated columns, the stored generated columns have better read performance, but take up more disk space.

## Data types

TiDB supports all the data types in MySQL except the `SPATIAL` type. This includes all the [numeric types](/data-type-numeric.md), [string types](/data-type-string.md), [date & time types](/data-type-date-and-time.md), and [the JSON type](/data-type-json.md).

## Indexes

An index is a copy of selected columns in a table. You can create an index using one or more columns of a [table](/develop/dev-guide-schema-design-overview.md#table). With indexes, TiDB can quickly locate data without having to search every row in a table every time, which greatly improves your query performance.

There are two common types of indexes:

- Primary Key: indexes on the primary key column.

- Secondary Index: indexes on non-primary key column

### Unique indexes

A unique index in TiDB enforces uniqueness on one or more columns, ensuring that no two rows in a table can have the same values in the indexed column(s). This constraint provides a way to maintain data integrity by preventing duplicate values, making unique indexes ideal for fields that should naturally be unique, like email addresses, usernames, or product codes.

### Primary key index

A primary key index is a unique index on one or more columns in a table, which serves as the primary identifier for each row. In TiDB, every table must have a primary key, and it can be defined explicitly by the user or implicitly by TiDB if no primary key is specified.

### Composite index

A composite index is an index built on two or more columns of a table, which is particularly useful for queries that filter or sort data by multiple fields. For example, creating a composite index on `last_name` and `first_name` in a person table allows TiDB to quickly locate records based on both names.

### Invisible indexes

Invisible indexes are indexes that exist in the database but are hidden from the query optimizer, meaning they are ignored in query plans. In TiDB, invisible indexes are useful for testing and debugging, allowing you to assess the impact of an index on performance without fully dropping it.

Starting from TiDB v8.0.0, you can make the optimizer select invisible indexes by modifying the [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800) system variable.

### Clustered indexes

In clustered indexes, the term clustered refers to the organization of how data is stored and not a group of database servers working together. Some database management systems refer to clustered indexes as index-organized tables (IOT).

This feature controls how data is stored in tables containing primary keys. It provides TiDB with the ability to organize tables in a way that can improve the performance of certain queries.

For more information, see [Clustered Indexes](/clustered-indexes.md).

### Secondary index

A secondary index is a logical object in a TiDB cluster. You can simply regard it as a sorting type of data that TiDB uses to improve the query performance. In TiDB, creating a secondary index is an online operation, which does not block any data read and write operations on a table. For each index, TiDB creates references for each row in a table and sorts the references by selected columns instead of by data directly.

For more information about secondary indexes, see [Secondary Indexes](https://docs.pingcap.com/tidb/stable/tidb-best-practices#secondary-index).

In TiDB, you can either [add a secondary index to an existing table](/develop/dev-guide-create-secondary-indexes.md#add-a-secondary-index-to-an-existing-table) or [create a secondary index when creating a new table](/develop/dev-guide-create-secondary-indexes.md#create-a-secondary-index-when-creating-a-new-table).

### Vector index

For the following TiDB deployment options, TiDB supports vector data types and vector search indexes.

- TiDB Cloud Serverless

- TiDB Self-Managed v8.4.0 or later versions

In TiDB, a vector index is a specialized index designed for efficient approximate nearest neighbor (ANN) searches over columns containing vector data. Vector indexes, particularly the HNSW (Hierarchical Navigable Small World) algorithm, allow K-nearest neighbors (KNN) searches to identify the closest data points in a vector space quickly. This significantly speeds up query performance, enabling results in milliseconds compared to brute-force methods.

Vector indexes rely on TiFlash replicas for data storage and search functionality. Before creating and using vector indexes, make sure that TiFlash nodes are available in your cluster.

## Constraints

TiDB supports almost the same constraints as MySQL.

### NOT NULL constraints

A `NOT NULL` constraint ensures that a column cannot contain `NULL` values.

When a column is defined with the `NOT NULL` constraint, TiDB ensures that any attempt to insert or update a row with a `NULL` value in that column will result in an error. This behavior is consistent with MySQL's implementation of `NOT NULL` constraints.

### CHECK constraints

A `CHECK` constraint restricts the values of a column in a table to meet your specified conditions. When the `CHECK` constraint is added to a table, TiDB checks whether the constraint is satisfied during the insertion or updates of data into the table. If the constraint is not met, an error is returned.

### Primary key constraints

Like MySQL, primary key constraints in TiDB contain unique constraints, that is, creating a primary key constraint is equivalent to having a unique constraint. In addition, other primary key constraints of TiDB are also similar to those of MySQL.

### Unique key constraints

Unique constraints mean that all non-null values in a unique index and a primary key column are unique.

### FOREIGN KEY constraints

A FOREIGN KEY is a database constraint that enforces referential integrity between two tables by linking a column in one table (the child table) to a column in another table (the parent table). This ensures that the values in the foreign key column of the child table match values in the primary or unique key column of the parent table. For example, a record in an `orders` table might have a foreign key linking to a customer in a `customers` table, which ensures that each order is associated with a valid customer.

Starting from v6.6.0, TiDB supports foreign key constraints as an experimental feature. This feature allows cross-table referencing of related data and helps maintain data consistency by enforcing referential integrity. However, it is important to note that this feature is experimental and not recommended for production environments due to potential performance issues, especially with large data volumes.

For more information, see [FOREIGN KEY constraints](/foreign-key.md).

## Views

A view acts as a virtual table, whose schema is defined by the `SELECT` statement that creates the view. Using views has the following benefits:

- Exposing only safe fields and data to users to ensure the security of sensitive fields and data stored in the underlying table.

- Defining complex queries that frequently appear as views to make complex queries easier and more convenient.

For more information, see [Views](/views.md).

## Sequence

A sequence is a database object designed to generate a sequence of numbers according to a specified set of rules. This feature is especially useful in scenarios where unique identifiers are required, such as in the creation of primary keys for database tables.

For more information, see [sequence](/sql-statements/sql-statement-create-sequence.md).