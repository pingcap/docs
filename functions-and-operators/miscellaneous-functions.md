---
title: Miscellaneous Functions
summary: Learn about miscellaneous functions in TiDB.
---

# Miscellaneous Functions

TiDB supports most of the [miscellaneous functions](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html) available in MySQL 8.0.

## Supported functions

| Name | Description  |
|:------------|:-----------------------------------------------------------------------------------------------|
| [`ANY_VALUE()`](#any_value)              | Suppress `ONLY_FULL_GROUP_BY` value rejection     |
| [`BIN_TO_UUID()`](#bin_to_uuid)          | Convert UUID from binary format to text format    |
| [`DEFAULT()`](#default)                  | Returns the default value for a table column      |
| [`GROUPING()`](#grouping)                | Modifier for `GROUP BY` operations                |
| [`INET_ATON()`](#inet_aton)              | Return the numeric value of an IP address         |
| [`INET_NTOA()`](#inet_ntoa)              | Return the IP address from a numeric value        |
| [`INET6_ATON()`](#inet6_aton)            | Return the numeric value of an IPv6 address       |
| [`INET6_NTOA()`](#inet6_ntoa)            | Return the IPv6 address from a numeric value      |
| [`IS_IPV4()`](#is_ipv4)                  | Whether argument is an IPv4 address               |
| [`IS_IPV4_COMPAT()`](#is_ipv4_compat)    | Whether argument is an IPv4-compatible address    |
| [`IS_IPV4_MAPPED()`](#is_ipv4_mapped)    | Whether argument is an IPv4-mapped address        |
| [`IS_IPV6()`](#is_ipv6)                  | Whether argument is an IPv6 address               |
| [`IS_UUID()`](#is_uuid)                  | Whether argument is an UUID                       |
| [`NAME_CONST()`](#name_const)            | Can be used to rename a column name               |
| [`SLEEP()`](#sleep)                      | Sleep for a number of seconds. Note that for [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters, the `SLEEP()` function has a limitation wherein it can only support a maximum sleep time of 300 seconds.       |
| [`UUID()`](#uuid)                        | Return a Universal Unique Identifier (UUID)       |
| [`UUID_TO_BIN()`](#uuid_to_bin)          | Convert UUID from text format to binary format    |
| [`VALUES()`](#values)                    | Defines the values to be used during an INSERT    |

### ANY_VALUE()

The `ANY_VALUE()` function returns any value from a group of values. Typically, it is used in scenarios where you need to include non-aggregated columns in your `SELECT` statement along with a `GROUP BY` clause.

```sql
CREATE TABLE fruits (id INT PRIMARY KEY, name VARCHAR(255));
Query OK, 0 rows affected (0.14 sec)

INSERT INTO fruits VALUES (1,'apple'),(2,'apple'),(3,'pear'),(4,'banana'),(5, 'pineapple');
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

SELECT id,name FROM fruits GROUP BY name;
ERROR 1055 (42000): Expression #1 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'test.fruits.id' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by

SELECT ANY_VALUE(id),GROUP_CONCAT(id),name FROM fruits GROUP BY name;
+---------------+------------------+-----------+
| ANY_VALUE(id) | GROUP_CONCAT(id) | name      |
+---------------+------------------+-----------+
|             1 | 1,2              | apple     |
|             3 | 3                | pear      |
|             4 | 4                | banana    |
|             5 | 5                | pineapple |
+---------------+------------------+-----------+
4 rows in set (0.00 sec)
```

In the preceding example, TiDB returns an error for the first `SELECT` statement because the `id` column is non-aggregated and not included in the `GROUP BY` clause. To address the issue, the second `SELECT` query uses `ANY_VALUE()` to get any value from each group and uses `GROUP_CONCAT()` to concatenate all values of the `id` column within each group into a single string. This approach enables you to get one value from each group and all values of the group without changing the SQL mode for non-aggregated columns.

### BIN_TO_UUID()

`BIN_TO_UUID()` and `UUID_TO_BIN()` can be used to convert between a textual format UUID and a binary format. Both functions accept two arguments.

- The first argument specifies the value to be converted.
- The second argument (optional) controls the ordering of the fields in the binary format.

```sql
SET @a := UUID();
Query OK, 0 rows affected (0.00 sec)

SELECT @a;
+--------------------------------------+
| @a                                   |
+--------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56 |
+--------------------------------------+
1 row in set (0.00 sec)

SELECT UUID_TO_BIN(@a);
+------------------------------------+
| UUID_TO_BIN(@a)                    |
+------------------------------------+
| 0x9A17B457EB6D11EEBACF5405DB7AAD56 |
+------------------------------------+
1 row in set (0.00 sec)

SELECT BIN_TO_UUID(0x9A17B457EB6D11EEBACF5405DB7AAD56);
+-------------------------------------------------+
| BIN_TO_UUID(0x9A17B457EB6D11EEBACF5405DB7AAD56) |
+-------------------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56            |
+-------------------------------------------------+
1 row in set (0.00 sec)

SELECT UUID_TO_BIN(@a, 1);
+----------------------------------------+
| UUID_TO_BIN(@a, 1)                     |
+----------------------------------------+
| 0x11EEEB6D9A17B457BACF5405DB7AAD56     |
+----------------------------------------+
1 row in set (0.00 sec)

SELECT BIN_TO_UUID(0x11EEEB6D9A17B457BACF5405DB7AAD56, 1);
+----------------------------------------------------+
| BIN_TO_UUID(0x11EEEB6D9A17B457BACF5405DB7AAD56, 1) |
+----------------------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56               |
+----------------------------------------------------+
1 row in set (0.00 sec)
```

See also [UUID()](#uuid) and [Best practices for UUID](/best-practices/uuid.md).

### DEFAULT()

The `DEFAULT()` function is used to get the default value of a column.

```sql
CREATE TABLE t1 (id INT PRIMARY KEY, c1 INT DEFAULT 5);
Query OK, 0 rows affected (0.15 sec)

INSERT INTO t1 VALUES (1, 1);
Query OK, 1 row affected (0.01 sec)

UPDATE t1 SET c1=DEFAULT(c1)+3;
Query OK, 1 row affected (0.02 sec)
Rows matched: 1  Changed: 1  Warnings: 0

TABLE t1;
+----+------+
| id | c1   |
+----+------+
|  1 |    8 |
+----+------+
1 row in set (0.00 sec)
```

In the preceding example, the `UPDATE` statement sets the value of the `c1` column to the default value of the column (which is `5`) plus `3`, resulting in a new value of `8`.

### GROUPING()

See [`GROUP BY` modifiers](/functions-and-operators/group-by-modifier.md).

### INET_ATON()

The `INET_ATON()` function converts an IPv4 address in dotted-quad notation into a binary version that can be stored efficiently.

```sql
SELECT INET_ATON('127.0.0.1');
```

```
+------------------------+
| INET_ATON('127.0.0.1') |
+------------------------+
|             2130706433 |
+------------------------+
1 row in set (0.00 sec)
```

### INET_NTOA()

The `INET_NTOA()` function converts a binary IPv4 address into a dotted-quad notation.

```sql
SELECT INET_NTOA(2130706433);
```

```
+-----------------------+
| INET_NTOA(2130706433) |
+-----------------------+
| 127.0.0.1             |
+-----------------------+
1 row in set (0.00 sec)
```

### INET6_ATON()

The `INET6_ATON()` function is similar to [`INET_ATON()`](#inet_aton), but `INET6_ATON()` can also handle IPv6 addresses.

```sql
SELECT INET6_ATON('::1');
```

```
+--------------------------------------+
| INET6_ATON('::1')                    |
+--------------------------------------+
| 0x00000000000000000000000000000001   |
+--------------------------------------+
1 row in set (0.00 sec)
```

### INET6_NTOA()

The `INET6_NTOA()` function is similar to [`INET_NTOA()`](#inet_ntoa), but `INET6_NTOA()` can also handle IPv6 addresses.

```sql
SELECT INET6_NTOA(0x00000000000000000000000000000001);
```

```
+------------------------------------------------+
| INET6_NTOA(0x00000000000000000000000000000001) |
+------------------------------------------------+
| ::1                                            |
+------------------------------------------------+
1 row in set (0.00 sec)
```

### IS_IPV4()

The `IS_IPV4()` function tests whether the given argument is an IPv4 address or not.

```sql
SELECT IS_IPV4('127.0.0.1');
```

```
+----------------------+
| IS_IPV4('127.0.0.1') |
+----------------------+
|                    1 |
+----------------------+
1 row in set (0.00 sec)
```

```sql
SELECT IS_IPV4('300.0.0.1');
```

```
+----------------------+
| IS_IPV4('300.0.0.1') |
+----------------------+
|                    0 |
+----------------------+
1 row in set (0.00 sec)
```

### IS_IPV4_COMPAT()

The `IS_IPV4_COMPAT()` function tests whether the given argument is an IPv4-compatible address.

```sql
SELECT IS_IPV4_COMPAT(INET6_ATON('::127.0.0.1'));
```

```
+-------------------------------------------+
| IS_IPV4_COMPAT(INET6_ATON('::127.0.0.1')) |
+-------------------------------------------+
|                                         1 |
+-------------------------------------------+
1 row in set (0.00 sec)
```

### IS_IPV4_MAPPED()

The `IS_IPV4_MAPPED()` function tests whether the given argument is an IPv4-mapped address.

```sql
SELECT IS_IPV4_MAPPED(INET6_ATON('::ffff:127.0.0.1'));
```

```
+------------------------------------------------+
| IS_IPV4_MAPPED(INET6_ATON('::ffff:127.0.0.1')) |
+------------------------------------------------+
|                                              1 |
+------------------------------------------------+
1 row in set (0.00 sec)
```

### IS_IPV6()

The `IS_IPV6()` function tests whether the given argument is an IPv6 address.

```sql
SELECT IS_IPV6('::1');
```

```
+----------------+
| IS_IPV6('::1') |
+----------------+
|              1 |
+----------------+
1 row in set (0.00 sec)
```

### IS_UUID()

The `IS_UUID()` function tests whether the given argument is a [UUID](/best-practices/uuid.md).

```sql
SELECT IS_UUID('eb48c08c-eb71-11ee-bacf-5405db7aad56');
```

```
+-------------------------------------------------+
| IS_UUID('eb48c08c-eb71-11ee-bacf-5405db7aad56') |
+-------------------------------------------------+
|                                               1 |
+-------------------------------------------------+
1 row in set (0.00 sec)
```

### NAME_CONST()

The `NAME_CONST()` function is used to name columns. It is recommended to use column aliases instead.

```sql
SELECT NAME_CONST('column name', 'value') UNION ALL SELECT 'another value';
```

```
+---------------+
| column name   |
+---------------+
| another value |
| value         |
+---------------+
2 rows in set (0.00 sec)
```

The preceding statement uses `NAME_CONST()` and the following statement uses the recommended way of aliasing columns.

```sql
SELECT 'value' AS 'column name' UNION ALL SELECT 'another value';
```

```
+---------------+
| column name   |
+---------------+
| value         |
| another value |
+---------------+
2 rows in set (0.00 sec)
```

### SLEEP()

The `SLEEP()` function is used to pause the execution of queries for a specified number of seconds.

```sql
SELECT SLEEP(1.5);
```

```
+------------+
| SLEEP(1.5) |
+------------+
|          0 |
+------------+
1 row in set (1.50 sec)
```

### UUID()

The `UUID()` function returns a universally unique identifier (UUID) version 1 as defined in [RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122).

```sql
SELECT UUID();
```

```
+--------------------------------------+
| UUID()                               |
+--------------------------------------+
| cb4d5ae6-eb6b-11ee-bacf-5405db7aad56 |
+--------------------------------------+
1 row in set (0.00 sec)
```

See also [Best practices for UUID](/best-practices/uuid.md).

### UUID_TO_BIN

See [BIN_TO_UUID()](#bin_to_uuid).

### VALUES()

The `VALUES(col_name)` function is used to reference the value of a specific column in the `ON DUPLICATE KEY UPDATE` clause of an [`INSERT`](/sql-statements/sql-statement-insert.md) statement.

```sql
CREATE TABLE t1 (id INT PRIMARY KEY, c1 INT);
Query OK, 0 rows affected (0.17 sec)

INSERT INTO t1 VALUES (1,51),(2,52),(3,53),(4,54),(5,55);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

INSERT INTO t1 VALUES(2,22),(4,44) ON DUPLICATE KEY UPDATE c1=VALUES(id)+100;
Query OK, 4 rows affected (0.01 sec)
Records: 2  Duplicates: 2  Warnings: 0

TABLE t1;
+----+------+
| id | c1   |
+----+------+
|  1 |   51 |
|  2 |  102 |
|  3 |   53 |
|  4 |  104 |
|  5 |   55 |
+----+------+
5 rows in set (0.00 sec)
```

## Unsupported functions

| Name | Description  |
|:------------|:-----------------------------------------------------------------------------------------------|
| [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short)            | Provides a UUID that is unique given certain assumptions not present in TiDB [TiDB #4620](https://github.com/pingcap/tidb/issues/4620) |