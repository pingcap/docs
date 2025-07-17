---
title: 信息函数
summary: 了解信息函数。
---

# 信息函数

TiDB 支持大部分 [information functions](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html) 在 MySQL 8.0 中提供的功能。

## TiDB 支持的 MySQL 函数

| 名称 | 描述 |
|:-----|:------------|
| [`BENCHMARK()`](#benchmark) | 在循环中执行表达式 |
| [`CONNECTION_ID()`](#connection_id) | 返回连接的 ID（线程 ID） |
| [`CURRENT_ROLE()`](#current_role) | 返回当前连接使用的角色 |
| [`CURRENT_USER()``, `CURRENT_USER`](#current_user) | 返回已验证的用户名和主机名 |
| [`DATABASE()`](#database) | 返回当前会话使用的默认（当前）数据库名 |
| [`FOUND_ROWS()`](#found_rows) | 对于带有 `LIMIT` 子句的 `SELECT`，如果没有 `LIMIT`，返回结果集中的行数 |
| [`LAST_INSERT_ID()`](#last_insert_id) | 返回最后一次 `INSERT` 操作中 `AUTOINCREMENT` 列的值 |
| [`ROW_COUNT()`](#row_count) | 影响的行数 |
| [`SCHEMA()`](#schema) | `DATABASE()` 的同义词 |
| [`SESSION_USER()`](#session_user) | `USER()` 的同义词 |
| [`SYSTEM_USER()`](#system_user) | `USER()` 的同义词 |
| [`USER()`](#user) | 返回客户端提供的用户名和主机名 |
| [`VERSION()`](#version) | 返回表示 MySQL 服务器版本的字符串 |

### BENCHMARK()

`BENCHMARK()` 函数执行给定的表达式指定次数。

语法：

```sql
BENCHMARK(count, expression)
```

- `count`：要执行表达式的次数。
- `expression`：要重复执行的表达式。

示例：

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

`CONNECTION_ID()` 函数返回连接的 ID。根据 TiDB 的 [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730) 配置项的值，该函数返回 32 位或 64 位的连接 ID。

如果启用 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)，可以使用连接 ID 来终止跨多个 TiDB 实例的查询。

</CustomContent>

<CustomContent platform="tidb-cloud">

`CONNECTION_ID()` 函数返回连接的 ID。根据 TiDB 的 [`enable-32bits-connection-id`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-32bits-connection-id-new-in-v730) 配置项的值，该函数返回 32 位或 64 位的连接 ID。

如果启用 [`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-global-kill-new-in-v610)，可以使用连接 ID 来终止跨多个 TiDB 实例的查询。

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

`CURRENT_ROLE()` 函数返回当前会话的 [role](/role-based-access-control.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

`CURRENT_ROLE()` 函数返回当前会话的 [role](https://docs.pingcap.com/tidb/stable/role-based-access-control)。

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

`CURRENT_USER()` 函数返回当前会话使用的账户。

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

`DATABASE()` 函数返回当前会话使用的数据库架构。

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

`FOUND_ROWS()` 函数返回上一次执行的 `SELECT` 语句的结果集中的行数。

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
> `SQL_CALC_FOUND_ROWS` 查询修饰符，用于在不考虑 `LIMIT` 子句的情况下计算结果集中的总行数，仅在 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40) 被启用时才被接受。该查询修饰符从 MySQL 8.0.17 开始已被弃用，建议使用 `COUNT(*)`。

### LAST_INSERT_ID()

`LAST_INSERT_ID()` 函数返回包含 [`AUTO_INCREMENT`](/auto-increment.md) 或 [`AUTO_RANDOM`](/auto-random.md) 列的表中最后一次插入的行的 ID。

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
> - 在 TiDB 中，[`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) 可能导致结果与 MySQL 返回的不同。这种差异源于 TiDB 在每个节点缓存 ID，可能导致 ID 不按顺序或出现空隙。如果对你的应用程序来说，严格的 ID 顺序很重要，可以启用 [MySQL 兼容模式](/auto-increment.md#mysql-compatibility-mode)。
>
> - 在前述示例中，ID 增加了 2，而 MySQL 在相同场景下会生成递增 1 的 ID。更多兼容性信息，请参见 [Auto-increment ID](/mysql-compatibility.md#auto-increment-id)。

`LAST_INSERT_ID(expr)` 函数可以接受一个表达式作为参数，将其存储为下一次调用 `LAST_INSERT_ID()` 时返回的值。你可以用它作为生成序列的 MySQL 兼容方法。注意，TiDB 也支持正确的 [sequence functions](/functions-and-operators/sequence-functions.md)。

### ROW_COUNT()

`ROW_COUNT()` 函数返回受影响的行数。

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

`SCHEMA()` 函数是 [`DATABASE()`](#database) 的同义词。

### SESSION_USER()

`SESSION_USER()` 函数是 [`USER()`](#user) 的同义词。

### SYSTEM_USER()

`SYSTEM_USER()` 函数是 [`USER()`](#user) 的同义词。

### USER()

`USER()` 函数返回当前连接的用户。可能与 `CURRENT_USER()` 的输出略有不同，因为 `USER()` 显示实际的 IP 地址，而不是通配符。

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

`VERSION()` 函数返回 TiDB 版本，格式与 MySQL 兼容。若想获得更详细的结果，可以使用 [`TIDB_VERSION()`](/functions-and-operators/tidb-functions.md#tidb_version)。

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

上述示例来自 TiDB v7.5.1，标识为 MySQL 8.0.11。

<CustomContent platform="tidb">

如果你想修改返回的版本，可以调整 [`server-version`](/tidb-configuration-file.md#server-version) 配置项。

</CustomContent>

## TiDB 特有函数

以下函数仅支持 TiDB，没有对应的 MySQL 等价函数。

| 名称 | 描述 |
|:-----|:------------|
| [`CURRENT_RESOURCE_GROUP()`](/functions-and-operators/tidb-functions.md#current_resource_group)  | 返回当前会话绑定的资源组名称 |

## 不支持的函数

* `CHARSET()`
* `COERCIBILITY()`
* `COLLATION()`
* `ICU_VERSION()`
* `ROLES_GRAPHML()`
