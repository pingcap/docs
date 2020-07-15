---
title: Explore SQL with TiDB
summary: Learn about the basic SQL statements for the TiDB database.
aliases: ['/docs/dev/basic-sql-operations/','/docs/dev/how-to/get-started/explore-sql/']
---

# Explore SQL with TiDB

TiDB is compatible with MySQL, you can use MySQL statements directly in most of the cases. For unsupported features, see [Compatibility with MySQL](/mysql-compatibility.md#unsupported-features).

To experiment with SQL and test out TiDB compatibility with MySQL queries, you can [run TiDB directly in your web browser without installing it](https://tour.tidb.io/). You can also first deploy a TiDB cluster and then run SQL statements in it.

This page walks you through the basic TiDB SQL statements such as DDL, DML and CRUD operations. For a complete list of TiDB statements, see [TiDB SQL Syntax Diagram](https://pingcap.github.io/sqlgram/).

## Create, show, and drop a database

### Create a database

To create a database, use the `CREATE DATABASE` statement:

{{< copyable "sql" >}}

```sql
CREATE DATABASE db_name [options];
```

For example, to create a database named `samp_db`:

{{< copyable "sql" >}}

```sql
CREATE DATABASE IF NOT EXISTS samp_db;
```

### Show the databases

To show the databases, use the `SHOW DATABASES` statement:

{{< copyable "sql" >}}

```sql
SHOW DATABASES;
```

### Delete a database

To delete a database, use the `DROP DATABASE` statement:

{{< copyable "sql" >}}

```sql
DROP DATABASE samp_db;
```

## Create, show, and drop a table

### Create a table

- To create a table, use the `CREATE TABLE` statement:

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE table_name column_name data_type constraint;
    ```

    For example:

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE person (
        number INT(11),
        name VARCHAR(255),
        birthday DATE
    );
    ```

- Add `IF NOT EXISTS` to prevent an error if the table exists:

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE IF NOT EXISTS person (
        number INT(11),
        name VARCHAR(255),
        birthday DATE
    );
    ```

- To view the statement that creates the table, use the `SHOW CREATE` statement:

    {{< copyable "sql" >}}

    ```sql
    SHOW CREATE table person;
    ```

### Show the tables

- To show all the tables in a database, use the `SHOW TABLES` statement:

    {{< copyable "sql" >}}

    ```sql
    SHOW TABLES FROM samp_db;
    ```

- To show all the columns in a table, use the `SHOW FULL COLUMNS` statement:

    {{< copyable "sql" >}}

    ```sql
    SHOW FULL COLUMNS FROM person;
    ```

### Delete a table

To delete a table, use the `DROP TABLE` statement:

{{< copyable "sql" >}}

```sql
DROP TABLE person;
```

or

{{< copyable "sql" >}}

```sql
DROP TABLE IF EXISTS person;
```

## Create, show, and drop an index

### Create an index

- To create an index for the column whose value is not unique, use the `CREATE INDEX` or `ALTER TABLE` statement:

    {{< copyable "sql" >}}

    ```sql
    CREATE INDEX person_num ON person (number);
    ```

    or

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE person ADD INDEX person_num (number);
    ```

- To create a unique index for the column whose value is unique, use the `CREATE UNIQUE INDEX` or `ALTER TABLE` statement:

    {{< copyable "sql" >}}

    ```sql
    CREATE UNIQUE INDEX person_num ON person (number);
    ```

    or

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE person ADD UNIQUE person_num (number);
    ```

### Show the indexes

To show all the indexes in a table, use the `SHOW INDEX` statement:

{{< copyable "sql" >}}

```sql
SHOW INDEX from person;
```

### Delete an index

To delete an index, use the `DROP INDEX` or `ALTER TABLE` statement:

{{< copyable "sql" >}}

```sql
DROP INDEX person_num ON person;
```

{{< copyable "sql" >}}

```sql
ALTER TABLE person DROP INDEX person_num;
```

## Insert, select, update, and delete data

### Insert data

To insert data into a table, use the `INSERT` statement:

{{< copyable "sql" >}}

```sql
INSERT INTO person VALUES("1","tom","20170912");
```

### Select data

To view the data in a table, use the `SELECT` statement:

{{< copyable "sql" >}}

```sql
SELECT * FROM person;
```

```
+--------+------+------------+
| number | name | birthday   |
+--------+------+------------+
|      1 | tom  | 2017-09-12 |
+--------+------+------------+
```

### Update data

To update the data in a table, use the `UPDATE` statement:

{{< copyable "sql" >}}

```sql
UPDATE person SET birthday='20171010' WHERE name='tom';
```

{{< copyable "sql" >}}

```sql
SELECT * FROM person;
```

```
+--------+------+------------+
| number | name | birthday   |
+--------+------+------------+
|      1 | tom  | 2017-10-10 |
+--------+------+------------+
```

### Delete data

To delete the data in a table, use the `DELETE` statement:

{{< copyable "sql" >}}

```sql
DELETE FROM person WHERE number=1;
```

{{< copyable "sql" >}}

```sql
SELECT * FROM person;
```

```
Empty set (0.00 sec)
```

## Create, authorize, and delete a user

### Create a user

To create a user, use the `CREATE USER` statement. The following example creates a user named `tiuser` with the password `123456`:

{{< copyable "sql" >}}

```sql
CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
```

### Authorize a user

- To grant `tiuser` the privilege to retrieve the tables in the `samp_db` database:

    {{< copyable "sql" >}}

    ```sql
    GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
    ```

- To check the privileges of `tiuser`:

    {{< copyable "sql" >}}

    ```sql
    SHOW GRANTS for tiuser@localhost;
    ```

### Delete a user

To delete `tiuser`:

{{< copyable "sql" >}}

```sql
DROP USER 'tiuser'@'localhost';
```
