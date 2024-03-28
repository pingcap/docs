---
title: Information Functions
summary: Learn about the information functions.
---

# Information Functions

TiDB supports most of the [information functions](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html) available in MySQL 8.0.

## TiDB supported MySQL functions

| Name | Description |
|:-----|:------------|
| [`BENCHMARK()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_benchmark) | Execute an expression in a loop |
| [`CONNECTION_ID()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_connection-id) | Return the connection ID (thread ID) for the connection  |
| [`CURRENT_ROLE()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_current-role) | Return the role that is in use by the connection |
| [`CURRENT_USER()`, `CURRENT_USER`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_current-user) | Return the authenticated user name and host name |
| [`DATABASE()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_database) | Return the default (current) database name  |
| [`FOUND_ROWS()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_found-rows) | For a `SELECT` with a `LIMIT` clause, the number of the rows that are returned if there is no `LIMIT` clause |
| [`LAST_INSERT_ID()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_last-insert-id) | Return the value of the `AUTOINCREMENT` column for the last `INSERT`   |
| [`ROW_COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_row-count) | The number of rows affected |
| [`SCHEMA()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_schema) | Synonym for `DATABASE()`  |
| [`SESSION_USER()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_session-user) | Synonym for `USER()`    |
| [`SYSTEM_USER()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_system-user) | Synonym for `USER()`   |
| [`USER()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_user) | Return the user name and host name provided by the client    |
| [`VERSION()`](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_version) | Return a string that indicates the MySQL server version   |

### BENCHMARK()

The `BENCHMARK()` function runs the expression a number of times.

```sql
SELECT BENCHMARK(5, SLEEP(2));
```

```
+------------------------+
| BENCHMARK(5, SLEEP(2)) |
+------------------------+
|                      0 |
+------------------------+
1 row in set (10.00 sec)
```

### CONNECTION_ID()

This returns the connection id of the session. Based on the [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730) configuration option for TiDB this function might return 32-bit or 64-bit ID's.

If [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) is enabled the connection ID can be used to kill queries across multiple TiDB instances of the same cluster.

```sql
SELECT CONNECTION_ID();
```

```
+-----------------+
| CONNECTION_ID() |
+-----------------+
|       322961414 |
+-----------------+
1 row in set (0.00 sec)
```

### CURRENT_ROLE()

This is to get the current [role](/role-based-access-control.md).

```sql
SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
| NONE           |
+----------------+
1 row in set (0.00 sec)
```

### CURRENT_USER()

This returns the account that is using the session.

```sql
SELECT CURRENT_USER();
```

```
+----------------+
| CURRENT_USER() |
+----------------+
| root@%         |
+----------------+
1 row in set (0.00 sec)
```

### DATABASE()

This returns the database schema that the current session is using.

```sql
SELECT DATABASE();
```

```
+------------+
| DATABASE() |
+------------+
| test       |
+------------+
1 row in set (0.00 sec)
```

### FOUND_ROWS()

```sql
SELECT 1 UNION ALL SELECT 2;
```

```
+------+
| 1    |
+------+
|    2 |
|    1 |
+------+
2 rows in set (0.01 sec)
```

```sql
SELECT FOUND_ROWS();
```

```
+--------------+
| FOUND_ROWS() |
+--------------+
|            2 |
+--------------+
1 row in set (0.00 sec)
```

> **Note**
>
> `SQL_CALC_FOUND_ROWS` is only accepted if [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40) is set. This query modifier has been deprecated in MySQL 8.0.17.

### LAST_INSERT_ID()

This returns the ID of the last row that was inserted. This works with [`AUTO_INCREMENT`](/auto-increment.md) and [`AUTO_RANDOM`](/auto-random.md) columns.

```
mysql> CREATE TABLE t1(id SERIAL);
Query OK, 0 rows affected (0.17 sec)

mysql> INSERT INTO t1() VALUES();
Query OK, 1 row affected (0.03 sec)

mysql> INSERT INTO t1() VALUES();
Query OK, 1 row affected (0.00 sec)

mysql> SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
|                3 |
+------------------+
1 row in set (0.00 sec)

mysql> TABLE t1;
+----+
| id |
+----+
|  1 |
|  3 |
+----+
2 rows in set (0.00 sec)
```

> **Note**
>
> The [`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) might lead to results that differ from what MySQL would give. If this is a concern for you then you can enable [MySQL Compatible mode](/auto-increment.md#mysql-compatibility-mode).

### ROW_COUNT()

This returns the number of affected rows.

```
mysql> CREATE TABLE t1(id BIGINT UNSIGNED PRIMARY KEY AUTO_RANDOM);
Query OK, 0 rows affected, 1 warning (0.16 sec)

mysql> INSERT INTO t1() VALUES (),(),();
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT ROW_COUNT();
+-------------+
| ROW_COUNT() |
+-------------+
|           3 |
+-------------+
1 row in set (0.00 sec)
```

### USER()

The `USER()` function returns the user of the connection. This might differ slightly from the output of `CURRENT_USER()` as this function shows the actual IP-address instead of a wildcard.

```sql
SELECT USER(), CURRENT_USER();
```

```
+----------------+----------------+
| USER()         | CURRENT_USER() |
+----------------+----------------+
| root@127.0.0.1 | root@%         |
+----------------+----------------+
1 row in set (0.00 sec)
```

### VERSION()

This function returns the version of TiDB in a way that is compatible with MySQL. The [`TIDB_VERSION()`](/functions-and-operators/tidb-functions.md#tidb_version) function can be used to get more details.

```
mysql> SELECT VERSION();
+--------------------+
| VERSION()          |
+--------------------+
| 8.0.11-TiDB-v7.5.1 |
+--------------------+
1 row in set (0.00 sec)

mysql> SELECT TIDB_VERSION()\G
*************************** 1. row ***************************
TIDB_VERSION(): Release Version: v7.5.1
Edition: Community
Git Commit Hash: 7d16cc79e81bbf573124df3fd9351c26963f3e70
Git Branch: heads/refs/tags/v7.5.1
UTC Build Time: 2024-02-27 14:28:32
GoVersion: go1.21.6
Race Enabled: false
Check Table Before Drop: false
Store: tikv
1 row in set (0.00 sec)
```

This is from TiDB v7.5.1, which identifies itself as MySQL 8.0.11.

The [`server-version`](/tidb-configuration-file.md#server-version) configuration option can be used to influence the reported version.

## TiDB specific functions

The following function is only supported by TiDB, and there is no equivalent function in MySQL.

| Name | Description |
|:-----|:------------|
| [`CURRENT_RESOURCE_GROUP()`](/functions-and-operators/tidb-functions.md#current_resource_group)  | Return the name of the resource group that the current session is bound to |

## Unsupported functions

* `CHARSET()`
* `COERCIBILITY()`
* `COLLATION()`
* `ICU_VERSION()`
* `ROLES_GRAPHML()`