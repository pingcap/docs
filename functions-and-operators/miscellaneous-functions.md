---
title: Miscellaneous Functions
summary: Learn about miscellaneous functions in TiDB.
---

# Miscellaneous Functions

TiDB supports most of the [miscellaneous functions](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html) available in MySQL 8.0.

## Supported functions

| Name | Description  |
|:------------|:-----------------------------------------------------------------------------------------------|
| [`ANY_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_any-value)              | Suppress `ONLY_FULL_GROUP_BY` value rejection     |
| [`BIN_TO_UUID()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_bin-to-uuid)          | Convert UUID from binary format to text format    |
| [`DEFAULT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_default)                  | Returns the default value for a table column      |
| [`GROUPING()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_grouping)                | Modifier for `GROUP BY` operations                |
| [`INET_ATON()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_inet-aton)              | Return the numeric value of an IP address         |
| [`INET_NTOA()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_inet-ntoa)              | Return the IP address from a numeric value        |
| [`INET6_ATON()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_inet6-aton)            | Return the numeric value of an IPv6 address       |
| [`INET6_NTOA()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_inet6-ntoa)            | Return the IPv6 address from a numeric value      |
| [`IS_IPV4()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_is-ipv4)                  | Whether argument is an IPv4 address               |
| [`IS_IPV4_COMPAT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_is-ipv4-compat)    | Whether argument is an IPv4-compatible address    |
| [`IS_IPV4_MAPPED()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_is-ipv4-mapped)    | Whether argument is an IPv4-mapped address        |
| [`IS_IPV6()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_is-ipv6)                  | Whether argument is an IPv6 address               |
[ [`IS_UUID()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_is-uuid)                  | Whether argument is an UUID                       |
| [`NAME_CONST()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_name-const)            | Can be used to rename a column name               |
| [`SLEEP()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_sleep)                      | Sleep for a number of seconds. Note that for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters, the `SLEEP()` function has a limitation wherein it can only support a maximum sleep time of 300 seconds.       |
| [`UUID()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid)                        | Return a Universal Unique Identifier (UUID)       |
| [`UUID_TO_BIN()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-to-bin)          | Convert UUID from text format to binary format    |
| [`VALUES()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_values)                    | Defines the values to be used during an INSERT    |

### ANY_VALUE()

```
mysql> CREATE TABLE fruits (id INT PRIMARY KEY, name VARCHAR(255));
Query OK, 0 rows affected (0.14 sec)

mysql> INSERT INTO fruits VALUES (1,'apple'),(2,'apple'),(3,'pear'),(4,'banana'),(5, 'pineapple');
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT id,name FROM fruits GROUP BY name;
ERROR 1055 (42000): Expression #1 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'test.fruits.id' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
mysql> SELECT ANY_VALUE(id),GROUP_CONCAT(id),name FROM fruits GROUP BY name;
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

Here TiDB returns an error for the first `SELECT` query as the `id` column is nonaggregated. For the second query we use the `ANY_VALUE()` function to get one value out of the group and `GROUP_CONCAT()` to get all values of the group. This can be used to avoid having to change the SQL mode for nonaggregated columns.

### BIN_TO_UUID()

`BIN_TO_UUID()` and `UUID_TO_BIN()` can be used to convert between a textual format UUID to a binary format. The second argument for these functions depends the ordering of the fields in the binary format.

```
mysql> SET @a := UUID();
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @a;
+--------------------------------------+
| @a                                   |
+--------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56 |
+--------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT UUID_TO_BIN(@a);
+------------------------------------+
| UUID_TO_BIN(@a)                    |
+------------------------------------+
| 0x9A17B457EB6D11EEBACF5405DB7AAD56 |
+------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT BIN_TO_UUID(0x9A17B457EB6D11EEBACF5405DB7AAD56);
+-------------------------------------------------+
| BIN_TO_UUID(0x9A17B457EB6D11EEBACF5405DB7AAD56) |
+-------------------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56            |
+-------------------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT UUID_TO_BIN(@a, 1);
+----------------------------------------+
| UUID_TO_BIN(@a, 1)                     |
+----------------------------------------+
| 0x11EEEB6D9A17B457BACF5405DB7AAD56     |
+----------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT BIN_TO_UUID(0x11EEEB6D9A17B457BACF5405DB7AAD56, 1);
+----------------------------------------------------+
| BIN_TO_UUID(0x11EEEB6D9A17B457BACF5405DB7AAD56, 1) |
+----------------------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56               |
+----------------------------------------------------+
1 row in set (0.00 sec)
```

### DEFAULT()

The `DEFAULT()` function is used to get the default value for a column.

```
mysql> CREATE TABLE t1 (id INT PRIMARY KEY, c1 INT DEFAULT 5);
Query OK, 0 rows affected (0.15 sec)

mysql> INSERT INTO t1 VALUES (1, 1);
Query OK, 1 row affected (0.01 sec)

mysql> UPDATE t1 SET c1=DEFAULT(c1)+3;
Query OK, 1 row affected (0.02 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> TABLE t1;
+----+------+
| id | c1   |
+----+------+
|  1 |    8 |
+----+------+
1 row in set (0.00 sec)
```

In the `UPDATE` statement the value of the `c1` column is set to the default value of the column (5) plus 3, which is 8.

### GROUPING()

See [`GROUP BY` Modifiers](/functions-and-operators/group-by-modifier.md).

### INET_ATON()

This converts a IPv4 address in dotted quad notation into a binary version that can be stored efficiently.

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

This converts a binary IPv4 addres into a dotted quad notation.

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

This is similar to [`INET_ATON()`](#inet_aton), but also handles IPv6 addresses.

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

This is similar to [`INET_NTOA()`](#inet_ntoa), but also handles IPv6 addresses.

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

This function test if the argument is a IPv4 address or not.

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

Tests if the argument is an IPv4-compatible address.

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

Tests if the argument is a IPv4-mapped address.

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

Tests if the argument is an IPv6 address.

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

Tests if the argument is a UUID.

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

This is an function for naming columns. It is recommended to use column aliases instead.

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

The statement above uses `NAME_CONST()` and the statement below uses the recommended way of aliasing columns.

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

Sleep for a number of seconds.

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

Gets a UUID v1 as defined in [RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122).

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

See also the [best practices for UUID](/best-practices/uuid.md)

### UUID_TO_BIN

See [BIN_TO_UUID()](#bin_to_uuid).

### VALUES()

This function is used to specify values in the `ON DUPLICATE KEY UPDATE` part of the [`INSERT`](/sql-statements/sql-statement-insert.md) statement.

```
mysql> CREATE TABLE t1 (id INT PRIMARY KEY, c1 INT);
Query OK, 0 rows affected (0.16 sec)

mysql> INSERT INTO t1 VALUES (1,1),(2,2),(3,3);
Query OK, 3 rows affected (0.01 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 VALUES(2,2) ON DUPLICATE KEY UPDATE c1=VALUES(id)+100;
Query OK, 2 rows affected (0.00 sec)

mysql> TABLE t1;
+----+------+
| id | c1   |
+----+------+
|  1 |    1 |
|  2 |  102 |
|  3 |    3 |
+----+------+
3 rows in set (0.00 sec)
```

## Unsupported functions

| Name | Description  |
|:------------|:-----------------------------------------------------------------------------------------------|
| [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short)            | Provides a UUID that is unique given certain assumptions not present in TiDB [TiDB #4620](https://github.com/pingcap/tidb/issues/4620) |