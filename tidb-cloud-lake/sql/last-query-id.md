---
title: LAST_QUERY_ID
summary: 根据当前会话中的顺序返回查询的 ID。
---

# LAST_QUERY_ID

根据当前会话中的顺序返回查询的 ID。

> **Note:**
>
> 该函数当前仅通过 MySQL 协议支持，这意味着你必须使用兼容 MySQL 协议的客户端连接到 {{{ .lake }}} 才能使用该函数。

## 语法 {#syntax}

```sql
LAST_QUERY_ID(<index>)
```

`index` 指定当前会话中的查询顺序，接受正数和负数，默认值为 `-1`。

- 正索引（从 `1` 开始）获取从会话开始起的第 n 个查询。
- 负索引从当前查询开始向后回溯获取第 n 个查询。
    - 当 `index` 为 `-1` 时，返回当前查询的查询 ID。
    - 要获取上一个查询，请将 `index` 设置为 `-2`。
- 如果索引超出查询历史范围，则返回 NULL。

## 示例 {#examples}

此示例在一个新会话中运行三个简单查询，然后同时使用正索引和负索引来获取 `SELECT 3` 的查询 ID：

|                                              | 正索引 | 负索引 |
|----------------------------------------------|----------|----------|
| `SELECT 1`                                   | 1        | -4       |
| `SELECT 2`                                   | 2        | -3       |
| `SELECT 3`                                   | 3        | -2       |
| `SELECT LAST_QUERY_ID(-2), LAST_QUERY_ID(3)` | 4        | -1       |

```bash
MacBook-Air:~ eric$ mysql -u root -h 127.0.0.1 -P 3307
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 8.0.90-v1.2.720-nightly-2280cc9480(rust-1.85.0-nightly-2025-04-08T04:40:36.379825500Z) 0

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> select 1;
+------+
| 1    |
+------+
|    1 |
+------+
1 row in set (0.02 sec)
Read 1 rows, 1.00 B in 0.004 sec., 264.46 rows/sec., 264.46 B/sec.

mysql> select 2;
+------+
| 2    |
+------+
|    2 |
+------+
1 row in set (0.01 sec)
Read 1 rows, 1.00 B in 0.003 sec., 366.94 rows/sec., 366.94 B/sec.

mysql> select 3;
+------+
| 3    |
+------+
|    3 |
+------+
1 row in set (0.01 sec)
Read 1 rows, 1.00 B in 0.003 sec., 373.16 rows/sec., 373.16 B/sec.

mysql> SELECT LAST_QUERY_ID(-2), LAST_QUERY_ID(3);
+--------------------------------------+--------------------------------------+
| last_query_id(- 2)                   | last_query_id(3)                     |
+--------------------------------------+--------------------------------------+
| 74dd6dca-f9b0-44cd-99f4-ac7d11d47fee | 74dd6dca-f9b0-44cd-99f4-ac7d11d47fee |
+--------------------------------------+--------------------------------------+
1 row in set (0.02 sec)
Read 1 rows, 1.00 B in 0.006 sec., 167.95 rows/sec., 167.95 B/sec.
```

此示例演示了当 `<index>` 为 `-1` 时，该函数返回当前查询的查询 ID：

```bash
MacBook-Air:~ eric$ mysql -u root -h 127.0.0.1 -P 3307
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.90-v1.2.720-nightly-2280cc9480(rust-1.85.0-nightly-2025-04-08T04:40:36.379825500Z) 0

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SELECT LAST_QUERY_ID(-1), LAST_QUERY_ID();
+--------------------------------------+--------------------------------------+
| last_query_id(- 1)                   | last_query_id()                      |
+--------------------------------------+--------------------------------------+
| 5a1afbc2-dc16-4b69-a0e6-615e0b970cb1 | 5a1afbc2-dc16-4b69-a0e6-615e0b970cb1 |
+--------------------------------------+--------------------------------------+
1 row in set (0.01 sec)
Read 1 rows, 1.00 B in 0.003 sec., 393.68 rows/sec., 393.68 B/sec.

mysql> SELECT LAST_QUERY_ID(-2);
+--------------------------------------+
| last_query_id(- 2)                   |
+--------------------------------------+
| 5a1afbc2-dc16-4b69-a0e6-615e0b970cb1 |
+--------------------------------------+
1 row in set (0.01 sec)
Read 1 rows, 1.00 B in 0.003 sec., 381.61 rows/sec., 381.61 B/sec.

mysql> SELECT LAST_QUERY_ID(1);
+--------------------------------------+
| last_query_id(1)                     |
+--------------------------------------+
| 5a1afbc2-dc16-4b69-a0e6-615e0b970cb1 |
+--------------------------------------+
1 row in set (0.01 sec)
Read 1 rows, 1.00 B in 0.003 sec., 353.63 rows/sec., 353.63 B/sec.
```

当 `index` 超出查询历史范围时，返回 NULL。

```bash
mysql> SELECT LAST_QUERY_ID(-100), LAST_QUERY_ID(100);
+----------------------+--------------------+
| last_query_id(- 100) | last_query_id(100) |
+----------------------+--------------------+
|                      |                    |
+----------------------+--------------------+
1 row in set (0.02 sec)
Read 1 rows, 1.00 B in 0.008 sec., 128.69 rows/sec., 128.69 B/sec.
```