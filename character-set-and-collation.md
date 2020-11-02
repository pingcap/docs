---
title: Character Set Support
summary: Learn about the supported character sets in TiDB.
aliases: ['/docs/v3.0/character-set-and-collation/','/docs/v3.0/reference/sql/character-set/','/docs/sql/character-set-support/','/docs/sql/character-set-configuration/']
---

# Character Set Support

A character set is a set of symbols and encodings. A collation is a set of rules for comparing characters in a character set.

Currently, TiDB supports the following character sets:

```sql
mysql> SHOW CHARACTER SET;
+---------|---------------|-------------------|--------+
| Charset | Description   | Default collation | Maxlen |
+---------|---------------|-------------------|--------+
| utf8    | UTF-8 Unicode | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode | utf8mb4_bin       |      4 |
| ascii   | US ASCII      | ascii_bin         |      1 |
| latin1  | Latin1        | latin1_bin        |      1 |
| binary  | binary        | binary            |      1 |
+---------|---------------|-------------------|--------+
5 rows in set (0.00 sec)
```

> **Warning:**
>
> TiDB incorrectly treats latin1 as a subset of utf8. This can lead to unexpected behaviors when you store characters that differ between latin1 and utf8 encodings. It is strongly recommended to the utf8mb4 character set. See [TiDB #18955](https://github.com/pingcap/tidb/issues/18955) for more details.

> **Note:**
>
> + In `TiDB`, `utf8` is treated as `utf8mb4`.
> + Each character set corresponds to only one default collation.

## Collation support

TiDB only supports binary collations. This means that unlike MySQL, in TiDB string comparisons are both case sensitive and accent sensitive:

```sql
mysql> SELECT * FROM information_schema.collations;
+----------------+--------------------+------+------------+-------------+---------+
| COLLATION_NAME | CHARACTER_SET_NAME | ID   | IS_DEFAULT | IS_COMPILED | SORTLEN |
+----------------+--------------------+------+------------+-------------+---------+
| utf8mb4_bin    | utf8mb4            |   46 | Yes        | Yes         |       1 |
| latin1_bin     | latin1             |   47 | Yes        | Yes         |       1 |
| binary         | binary             |   63 | Yes        | Yes         |       1 |
| ascii_bin      | ascii              |   65 | Yes        | Yes         |       1 |
| utf8_bin       | utf8               |   83 | Yes        | Yes         |       1 |
+----------------+--------------------+------+------------+-------------+---------+
5 rows in set (0.00 sec)

mysql> SHOW COLLATION WHERE Charset = 'utf8mb4';
+-------------+---------+------+---------+----------+---------+
| Collation   | Charset | Id   | Default | Compiled | Sortlen |
+-------------+---------+------+---------+----------+---------+
| utf8mb4_bin | utf8mb4 |   46 | Yes     | Yes      |       1 |
+-------------+---------+------+---------+----------+---------+
1 row in set (0.00 sec)
```

For compatibility with MySQL, TiDB will allow other collation names to be used:

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY AUTO_INCREMENT, b VARCHAR(10)) COLLATE utf8mb4_unicode_520_ci;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1, 'a');
Query OK, 1 row affected (0.00 sec)

mysql> SELECT * FROM t1 WHERE b = 'a';
+---+------+
| a | b    |
+---+------+
| 1 | a    |
+---+------+
1 row in set (0.00 sec)

mysql> SELECT * FROM t1 WHERE b = 'A';
Empty set (0.00 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) NOT NULL AUTO_INCREMENT,
  `b` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`a`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci AUTO_INCREMENT=30002
1 row in set (0.00 sec)
```

## Cluster character set and collation

Not supported yet.

## Database character set and collation

Each database has a character set and a collation. You can use the following statements to specify the database character set and collation:

```sql
CREATE DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]

ALTER DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]
```

`DATABASE` can be replaced with `SCHEMA` here.

<<<<<<< HEAD
Different databases can use different character sets and collations. Use the `character_set_database` and  `collation_database` to see the character set and collation of the current database:
=======
Different databases can use different character sets and collations. Use the `character_set_database` and `collation_database` to see the character set and collation of the current database:

{{< copyable "sql" >}}

```sql
CREATE SCHEMA test1 CHARACTER SET utf8mb4 COLLATE uft8mb4_general_ci;
```
>>>>>>> 8595ca53... Capitalize sql keywords in several files (#4117)

```sql
mysql> create schema test1 character set utf8 COLLATE uft8_general_ci;
Query OK, 0 rows affected (0.09 sec)

<<<<<<< HEAD
mysql> use test1;
=======
```sql
USE test1;
```

```sql
>>>>>>> 8595ca53... Capitalize sql keywords in several files (#4117)
Database changed
mysql> SELECT @@character_set_database, @@collation_database;
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| utf8                     | uft8_general_ci      |
+--------------------------|----------------------+
1 row in set (0.00 sec)

<<<<<<< HEAD
mysql> create schema test2 character set latin1 COLLATE latin1_general_ci;
Query OK, 0 rows affected (0.09 sec)
=======
```sql
CREATE SCHEMA test2 CHARACTER SET latin1 COLLATE latin1_bin;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
USE test2;
```
>>>>>>> 8595ca53... Capitalize sql keywords in several files (#4117)

mysql> use test2;
Database changed
mysql> SELECT @@character_set_database, @@collation_database;
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| latin1                   | latin1_general_ci    |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

You can also see the two values in INFORMATION_SCHEMA:

```sql
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';
```

## Table character set and collation

You can use the following statement to specify the character set and collation for tables:

```sql
CREATE TABLE tbl_name (column_list)
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]]

ALTER TABLE tbl_name
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]
```

For example:

```sql
mysql> CREATE TABLE t1(a int) CHARACTER SET utf8 COLLATE utf8_general_ci;
Query OK, 0 rows affected (0.08 sec)
```

The database character set and collation are used as the default values for table definitions if the table character set and collation are not specified in individual column definitions.

## Column character set and collation

See the following table for the character set and collation syntax for columns:

```sql
col_name {CHAR | VARCHAR | TEXT} (col_length)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

col_name {ENUM | SET} (val_list)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]
```

The table character set and collation are used as the default values for column definitions if the column character set and collation are not specified in individual column definitions.

## String character sets and collation

Each character literal in a string has a character set and a collation. When you use a string, this option is available:

{{< copyable "sql" >}}

```sql
[_charset_name]'string' [COLLATE collation_name]
```

Example:

```sql
SELECT 'string';
SELECT _latin1'string';
SELECT _latin1'string' COLLATE latin1_danish_ci;
```

Rules:

+ Rule 1: If you specify `CHARACTER SET charset_name` and `COLLATE collation_name`, then `CHARACTER SET charset_name` and `COLLATE collation_name` are used directly.
+ Rule 2: If you specify `CHARACTER SET charset_name` but do not specify `COLLATE collation_name`, `CHARACTER SET charset_name` and the default collation of `CHARACTER SET charset_name` are used.
+ Rule 3: If you specify neither `CHARACTER SET charset_name` nor `COLLATE collation_name`, the character set and collation given by the system variables `character_set_connection` and `collation_connection` are used.

## Connection character sets and collations

+ The server character set and collation are the values of the `character_set_server` and `collation_server` system variables.

+ The character set and collation of the default database are the values of the `character_set_database` and `collation_database` system variables. You can use `character_set_connection` and `collation_connection` to specify the character set and collation for each connection. The `character_set_client` variable is to set the client character set. Before returning the result, the `character_set_results` system variable indicates the character set in which the server returns query results to the client, including the metadata of the result.

You can use the following statement to specify a particular collation that is related to the client:

+ `SET NAMES 'charset_name' [COLLATE 'collation_name']`

    `SET NAMES` indicates what character set the client will use to send SQL statements to the server. `SET NAMES utf8` indicates that all the requests from the client use utf8, as well as the results from the server.

    The `SET NAMES 'charset_name'` statement is equivalent to the following statement combination:

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE` is optional, if absent, the default collation of the `charset_name` is used.

+ `SET CHARACTER SET 'charset_name'`

    Similar to `SET NAMES`, the `SET NAMES 'charset_name'` statement is equivalent to the following statement combination:

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET collation_connection = @@collation_database;
    ```

## Optimization levels of character sets and collations

String => Column => Table => Database => Server => Cluster

## General rules on selecting character sets and collation

+ Rule 1: If you specify `CHARACTER SET charset_name` and `COLLATE collation_name`, then `CHARACTER SET charset_name` and `COLLATE collation_name` are used directly.
+ Rule 2: If you specify `CHARACTER SET charset_name` and do not specify `COLLATE collation_name`, then `CHARACTER SET charset_name` and the default comparison collation of `CHARACTER SET charset_name` are used.
+ Rule 3: If you specify neither `CHARACTER SET charset_name` nor `COLLATE collation_name`, the character set and collation with higher optimization levels are used.

## Validity check of characters

For the specified `utf8` or `utf8mb4` character set, TiDB only supports the valid `utf8` character, and reports the `incorrect utf8 value` error when the character is invalid. This validity check of characters in TiDB is compatible with MySQL 8.0 but incompatible with MySQL 5.7 or earlier versions.

To disable this error reporting, use `set @@tidb_skip_utf8_check=1;` to skip the character check.

<<<<<<< HEAD
For more information, see [Connection Character Sets and Collations in MySQL](https://dev.mysql.com/doc/refman/5.7/en/charset-connection.html).
=======
## Collation support framework

The syntax support and semantic support for the collation are influenced by the [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) configuration item. The syntax support and semantic support are different. The former indicates that TiDB can parse and set collations. The latter indicates that TiDB can correctly use collations when comparing strings.

Before v4.0, TiDB provides only the [old framework for collations](#old-framework-for-collations). In this framework, TiDB supports syntactically parsing most of the MySQL collations but semantically takes all collations as binary collations.

Since v4.0, TiDB supports a [new framework for collations](#new-framework-for-collations). In this framework, TiDB semantically parses different collations and strictly follows the collations when comparing strings.

### Old framework for collations

Before v4.0, you can specify most of the MySQL collations in TiDB, and these collations are processed according to the default collations, which means that the byte order determines the character order. Different from MySQL, TiDB deletes the space at the end of the character according to the `PADDING` attribute of the collation before comparing characters, which causes the following behavior differences:

{{< copyable "sql" >}}

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
Query OK, 0 rows affected
INSERT INTO t VALUES ('A');
Query OK, 1 row affected
INSERT INTO t VALUES ('a');
Query OK, 1 row affected # In TiDB, it is successfully executed. In MySQL, because utf8mb4_general_ci is case-insensitive, the `Duplicate entry 'a'` error is reported.
INSERT INTO t1 VALUES ('a ');
Query OK, 1 row affected # In TiDB, it is successfully executed. In MySQL, because comparison is performed after the spaces are filled in, the `Duplicate entry 'a '` error is returned.
```

### New framework for collations

In TiDB 4.0, a complete framework for collations is introduced. This new framework supports semantically parsing collations and introduces the `new_collations_enabled_on_first_bootstrap` configuration item to decide whether to enable the new framework when a cluster is first initialized. If you initialize the cluster after the configuration item is enabled, you can check whether the new collation is enabled through the `new_collation_enabled` variable in the `mysql`.`tidb` table:

{{< copyable "sql" >}}

```sql
SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME='new_collation_enabled';
```

```sql
+----------------+
| VARIABLE_VALUE |
+----------------+
| True           |
+----------------+
1 row in set (0.00 sec)
```

Under the new framework, TiDB support the `utf8_general_ci`, `utf8mb4_general_ci`, `utf8_unicode_ci`, and `utf8mb4_unicode_ci` collations which are compatible with MySQL.

When one of `utf8_general_ci`, `utf8mb4_general_ci`, `utf8_unicode_ci`, and `utf8mb4_unicode_ci` is used, the string comparison is case-insensitive and accent-insensitive. At the same time, TiDB also corrects the collation's `PADDING` behavior:

{{< copyable "sql" >}}

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
Query OK, 0 rows affected (0.00 sec)
INSERT INTO t VALUES ('A');
Query OK, 1 row affected (0.00 sec)
INSERT INTO t VALUES ('a');
ERROR 1062 (23000): Duplicate entry 'a' for key 'PRIMARY' # TiDB is compatible with the case-insensitive collation of MySQL.
INSERT INTO t VALUES ('a ');
ERROR 1062 (23000): Duplicate entry 'a ' for key 'PRIMARY' # TiDB modifies the `PADDING` behavior to be compatible with MySQL.
```

> **Note:**
>
> The implementation of padding in TiDB is different from that in MySQL. In MySQL, padding is implemented by filling in spaces. In TiDB, padding is implemented by cutting out the spaces at the end. The two approaches are the same in most cases. The only exception is when the end of the string contains characters that are less than spaces (0x20). For example, the result of `'a' < 'a\t'` in TiDB is `1`, but in MySQL, `'a' < 'a\t'` is equivalent to `'a ' < 'a\t'`, and the result is `0`.

## Coercibility values of collations in expressions

If an expression involves multiple clauses of different collations, you need to infer the collation used in the calculation. The rules are as follows:

+ The coercibility value of the explicit `COLLATE` clause is `0`.
+ If the collations of two strings are incompatible, the coercibility value of the concatenation of two strings with different collations is `1`.
+ The collation of the column, `CAST()`, `CONVERT()`, or `BINARY()` has a coercibility value of `2`.
+ The system constant (the string returned by `USER ()` or `VERSION ()`) has a coercibility value of `3`.
+ The coercibility value of constants is `4`.
+ The coercibility value of numbers or intermediate variables is `5`.
+ `NULL` or expressions derived from `NULL` has a coercibility value of `6`.

When inferring collations, TiDB prefers using the collation of expressions with lower coercibility values. If the coercibility values of two clauses are the same, the collation is determined according to the following priority:

binary > utf8mb4_bin > (utf8mb4_general_ci = utf8mb4_unicode_ci) > utf8_bin > (utf8_general_ci = utf8_unicode_ci) > latin1_bin > ascii_bin

TiDB cannot infer the collation and reports an error in the following situations:

- If the collations of two clauses are different and the coercibility value of both clauses is `0`.
- If the collations of two clauses are incompatible and the returned type of expression is `String`.

## `COLLATE` clause

TiDB supports using the `COLLATE` clause to specify the collation of an expression. The coercibility value of this expression is `0`, which has the highest priority. See the following example:

{{< copyable "sql" >}}

```sql
SELECT 'a' = _utf8mb4 'A' collate utf8mb4_general_ci;
```

```sql
+-----------------------------------------------+
| 'a' = _utf8mb4 'A' collate utf8mb4_general_ci |
+-----------------------------------------------+
|                                             1 |
+-----------------------------------------------+
1 row in set (0.00 sec)
```

For more details, see [Connection Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-connection.html).
>>>>>>> 8595ca53... Capitalize sql keywords in several files (#4117)
