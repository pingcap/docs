---
title: LAST_QUERY_ID
summary: 順序に基づいて現在のセッション内のクエリ ID を返します。
---

# LAST_QUERY_ID

順序に基づいて現在のセッション内のクエリ ID を返します。

> **Note:**
>
> この関数は現在 MySQL プロトコル経由でのみサポートされています。つまり、動作させるには、MySQL プロトコル互換のクライアントを使用して {{{ .lake }}} に接続する必要があります。

## 構文 {#syntax}

```sql
LAST_QUERY_ID(<index>)
```

`index` は現在のセッション内のクエリ順序を指定します。正の数と負の数を受け付け、デフォルト値は `-1` です。

- 正のインデックス（`1` から開始）は、セッション開始時点から n 番目のクエリを取得します。
- 負のインデックスは、現在のクエリからさかのぼって n 番目のクエリを取得します。
    - `index` が `-1` の場合、現在のクエリのクエリ ID を返します。
    - 直前のクエリを取得するには、`index` を `-2` に設定します。
- インデックスがクエリ履歴を超える場合は、NULL が返されます。

## 例 {#examples}

この例では、新しいセッションで 3 つの単純なクエリを実行し、その後、正と負の両方のインデックスを使用して `SELECT 3` のクエリ ID を取得します。

|                                              | 正 | 負 |
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

この例は、`<index>` が `-1` の場合に、この関数が現在のクエリのクエリ ID を返すことを示しています。

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

`index` がクエリ履歴を超える場合は、NULL が返されます。

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