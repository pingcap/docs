---
title: Information Functions
summary: Learn about the information functions.
---

# Information Functions

TiDB supports most of the [information functions](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html) available in MySQL 8.0.

## TiDB supported MySQL functions

| Name | Description |
|:-----|:------------|
| [`BENCHMARK()`](#benchmark) | Execute an expression in a loop |
| [`CONNECTION_ID()`](#connection_id) | Return the connection ID (thread ID) for the connection  |
| [`CURRENT_ROLE()`](#current_role) | Return the role that is in use by the connection |
| [`CURRENT_USER()`, `CURRENT_USER`](#current_user) | Return the authenticated user name and host name |
| [`DATABASE()`](#database) | Return the default (current) database name  |
| [`FOUND_ROWS()`](#found_rows) | For a `SELECT` with a `LIMIT` clause, the number of the rows that are returned if there is no `LIMIT` clause |
| [`LAST_INSERT_ID()`](#last_insert_id) | Return the value of the `AUTOINCREMENT` column for the last `INSERT`   |
| [`ROW_COUNT()`](#row_count) | The number of rows affected |
| [`SCHEMA()`](#schema) | Synonym for `DATABASE()`  |
| [`SESSION_USER()`](#session_user) | Synonym for `USER()`    |
| [`SYSTEM_USER()`](#system_user) | Synonym for `USER()`   |
| [`USER()`](#user) | Return the user name and host name provided by the client    |
| [`VERSION()`](#version) | Return a string that indicates the MySQL server version   |

### BENCHMARK()

The `BENCHMARK()` function executes the given expression a specified number of times.

Syntax:

```sql
BENCHMARK(count, expression)
```

- `count`: the number of times the expression to be executed.
- `expression`: the expression to be executed repeatedly.

Example:

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

<CustomContent platform="tidb">

The `CONNECTION_ID()` function returns the ID of the connection. Based on the value of the [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730) configuration item for TiDB, this function returns a 32-bit or 64-bit connection ID.

If [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) is enabled, the connection ID can be used to kill queries across multiple TiDB instances of the same cluster.

</CustomContent>

<CustomContent platform="tidb-cloud">

The `CONNECTION_ID()` function returns the ID of the connection. Based on the value of the [`enable-32bits-connection-id`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-32bits-connection-id-new-in-v730) configuration item for TiDB, this function returns a 32-bit or 64-bit connection ID.

If [`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-global-kill-new-in-v610) is enabled, the connection ID can be used to kill queries across multiple TiDB instances of the same cluster.

</CustomContent>

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

<CustomContent platform="tidb">

The `CURRENT_ROLE()` function returns the current [role](/role-based-access-control.md) for the current session.

</CustomContent>

<CustomContent platform="tidb-cloud">

The `CURRENT_ROLE()` function returns the current [role](https://docs.pingcap.com/tidb/stable/role-based-access-control) for the current session.

</CustomContent>

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

The `CURRENT_USER()` function returns the account that is used in the current session.

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

The `DATABASE()` function returns the database schema that the current session is using.

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

The `FOUND_ROWS()` function returns the number of rows in the result set of the last executed `SELECT` statement.

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

> **Note:**
>
> The `SQL_CALC_FOUND_ROWS` query modifier, which calculates the total number of rows in a result set without considering the `LIMIT` clause, is only accepted if [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40) is enabled. This query modifier is deprecated starting from MySQL 8.0.17. It is recommended to use `COUNT(*)` instead.

### LAST_INSERT_ID()

The `LAST_INSERT_ID()` function returns the ID of the last inserted row in a table that contains an [`AUTO_INCREMENT`](/auto-increment.md) or [`AUTO_RANDOM`](/auto-random.md) column.

```sql
CREATE TABLE t1(id SERIAL);
Query OK, 0 rows affected (0.17 sec)

INSERT INTO t1() VALUES();
Query OK, 1 row affected (0.03 sec)

INSERT INTO t1() VALUES();
Query OK, 1 row affected (0.00 sec)

SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
|                3 |
+------------------+
1 row in set (0.00 sec)

TABLE t1;
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
> - In TiDB, [`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) might lead to results that differ from those returned by MySQL. This discrepancy arises because TiDB caches IDs on each node, potentially leading to IDs that are out of order or have gaps. If maintaining strict ID ordering is essential for your application, you can enable [MySQL compatible mode](/auto-increment.md#mysql-compatibility-mode).
>
> - In the preceding example, IDs increase by 2 while MySQL would generate IDs incrementing by 1 in the same scenario. For more compatibility information, see [Auto-increment ID](/mysql-compatibility.md#auto-increment-id).

The `LAST_INSERT_ID(expr)` function can accept an expression as an argument, storing the value for the next call to `LAST_INSERT_ID()`. You can use it as a MySQL-compatible method for generating sequences. Note that TiDB also supports proper [sequence functions](/functions-and-operators/sequence-functions.md).

### ROW_COUNT()

The `ROW_COUNT()` function returns the number of affected rows.

```sql
CREATE TABLE t1(id BIGINT UNSIGNED PRIMARY KEY AUTO_RANDOM);
Query OK, 0 rows affected, 1 warning (0.16 sec)

INSERT INTO t1() VALUES (),(),();
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

SELECT ROW_COUNT();
+-------------+
| ROW_COUNT() |
+-------------+
|           3 |
+-------------+
1 row in set (0.00 sec)
```

### SCHEMA()

The `SCHEMA()` function is a synonym for [`DATABASE()`](#database).

### SESSION_USER()

The `SESSION_USER()` function is a synonym for [`USER()`](#user).

### SYSTEM_USER()

The `SYSTEM_USER()` function is a synonym for [`USER()`](#user).

### USER()

The `USER()` function returns the user of the current connection. This might differ slightly from the output of `CURRENT_USER()`, as `USER()` displays the actual IP address instead of a wildcard.

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

The `VERSION()` function returns the TiDB version in a format that is compatible with MySQL. To get a more detailed result, you can use the [`TIDB_VERSION()`](/functions-and-operators/tidb-functions.md#tidb_version) function.

```sql
SELECT VERSION();
+--------------------+
| VERSION()          |
+--------------------+
| 8.0.11-TiDB-v7.5.1 |
+--------------------+
1 row in set (0.00 sec)
```

```sql
SELECT TIDB_VERSION()\G
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

The preceding example is from TiDB v7.5.1, which identifies itself as MySQL 8.0.11.

<CustomContent platform="tidb">

If you want to change the returned version, you can modify the [`server-version`](/tidb-configuration-file.md#server-version) configuration item.

</CustomContent>

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
