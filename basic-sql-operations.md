---
title: Basic SQL operations
summary: Learn about the basic SQL statements for the TiDB database.
aliases: ['/docs/dev/basic-sql-operations/','/docs/dev/how-to/get-started/explore-sql/']
---

# Basic SQL Operations

TiDB is compatible with MySQL, you can use MySQL statements directly in most of the cases. For unsupported features, see [Compatibility with MySQL](/mysql-compatibility.md#unsupported-features).

Structured Query Language (SQL) is a declarative language which defines the way that users interact with databases. You can use SQL just as a natural language to talk to the database. This page walks you through the basic SQL statements in TiDB. For a complete list of TiDB statements, see [TiDB SQL Syntax Diagram](https://pingcap.github.io/sqlgram/).

## Category

SQL is divided into the following 4 types according to their functions:

- DDL (Data Definition Language): It is used to define database objects, including databases, tables, views, and indexes.

- DML (Data Manipulation Language): It is used to manipulate application related records.

- DCL (Data Control Language): It is used to define access privileges and security levels

Common DDL features are creating, modifying, and deleting objects (such as tables and indexes). The corresponding commands are `CREATE`, `ALTER`, and `DROP`.

## Show, create and drop a database

Database in TiDB can be considered as a collection of objects such as tables and indexes.

To show the list of databases, use the `SHOW DATABASES` statement:

{{< copyable "sql" >}}

```sql
SHOW DATABASES;
```

Use the database named `mysql`:

{{< copyable "sql" >}}

```sql
use mysql;
```

To show all the tables in a database, use the `SHOW TABLES` statement:

{{< copyable "sql" >}}

```sql
SHOW TABLES FROM mysql;
```

To create a database named `samp_db`, use the `CREATE DATABASE` statement:

{{< copyable "sql" >}}

```sql
CREATE DATABASE IF NOT EXISTS samp_db;
```

Add `IF NOT EXISTS` to  prevent an error if the database exists.

To delete a database, use the `DROP DATABASE` statement:

{{< copyable "sql" >}}

```sql
DROP DATABASE samp_db;
```

## Create, show, and drop a table

To create a table, use the `CREATE TABLE` statement:

{{< copyable "sql" >}}

```sql
CREATE TABLE table_name column_name data_type constraint;
```

For example, to create a table named `person` which includes fields such as number, name, and birthday, use the following statement:

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    number INT(11),
    name VARCHAR(255),
    birthday DATE
    );
```

To view the statement that creates the table (DDL), use the `SHOW CREATE` statement:

{{< copyable "sql" >}}

```sql
SHOW CREATE table person;
```

To delete a table, use the `DROP TABLE` statement:

{{< copyable "sql" >}}

```sql
DROP TABLE person;
```

## Create, show, and drop an index

### Create an index

Indexes are used to speed up queries on indexed columns. To create an index for the column whose value is not unique, use the `CREATE INDEX` or `ALTER TABLE` statement:

{{< copyable "sql" >}}

```sql
CREATE INDEX person_id ON person (id);
```

or

{{< copyable "sql" >}}

```sql
ALTER TABLE person ADD INDEX person_id (id);
```

To create a unique index for the column whose value is unique, use the `CREATE UNIQUE INDEX` statement:

{{< copyable "sql" >}}

```sql
CREATE UNIQUE INDEX person_unique_id ON person (id);
```

or use the `ALTER TABLE` statement:

{{< copyable "sql" >}}

```sql
ALTER TABLE person ADD UNIQUE person_unique_id (id);
```

To show all the indexes in a table, use the `SHOW INDEX` statement:

{{< copyable "sql" >}}

```sql
SHOW INDEX from person;
```

To delete an index, use the `DROP INDEX` or `ALTER TABLE` statement. `DROP INDEX` can be nested in `ALTER TABLE`:

{{< copyable "sql" >}}

```sql
DROP INDEX person_id ON person;
```

{{< copyable "sql" >}}

```sql
ALTER TABLE person DROP INDEX person_unique_id;
```

> **Note:**
> 
> DDL operations are not transactions. You don't need corresponding COMMIT statements when executing DDL.

Common DML features are adding, modifying, and deleting table records. The corresponding commands are `INSERT`, `UPDATE`, and `DELETE`.

## Insert, update, and delete data

To insert data into a table, use the `INSERT` statement:

{{< copyable "sql" >}}

```sql
INSERT INTO person VALUES("1","tom","20170912");
```

To insert data into a table containing data of some fields, use the `INSERT` statement:

{{< copyable "sql" >}}

```sql
INSERT INTO person(id,name) VALUES("2","bob");
```

To update some fields of a record in a table, use the `UPDATE` statement:

{{< copyable "sql" >}}

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

To delete the data in a table, use the `DELETE` statement:

{{< copyable "sql" >}}

```sql
DELETE FROM person WHERE id=2;
```

> **Note:**
> 
> The `UPDATE` and `DELETE` statements without the `WHERE` clause as a filter operate on the entire table.

DQL is used to retrieve the desired data rows from a table or multiple tables, usually the core content.

## Query data

To view the data in a table, use the `SELECT` statement:

{{< copyable "sql" >}}

```sql
SELECT * FROM person;
```

Add the column name to be queried after the `SELECT` statement:

{{< copyable "sql" >}}

```sql
SELECT name FROM person;
+------+
| name |
+------+
| tom  |
+------+
```

Use the `WHERE` clause to filter all records that match the conditions and then return the result:

{{< copyable "sql" >}}

```sql
SELECT * FROM person where id<5;
```

Common DCL features are creating or deleting users, and managing user privileges.

## Create, authorize, and delete a user

To create a user, use the `CREATE USER` statement. The following example creates a user named `tiuser` with the password `123456`:

{{< copyable "sql" >}}

```sql
CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
```

To grant `tiuser` the privilege to retrieve the tables in the `samp_db` database:

{{< copyable "sql" >}}

```sql
GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
```

To check the privileges of `tiuser`:

{{< copyable "sql" >}}

```sql
SHOW GRANTS for tiuser@localhost;
```

To delete `tiuser`:

{{< copyable "sql" >}}

```sql
DROP USER 'tiuser'@'localhost';
```
