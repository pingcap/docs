---
title: SHOW FUNCTIONS
summary: 現在サポートされている組み込みのスカラー関数および集約関数を一覧表示します。
---

# SHOW FUNCTIONS

現在サポートされている組み込みのスカラー関数および集約関数を一覧表示します。

関連情報: [system.functions](/tidb-cloud-lake/sql/system-functions.md)

## 構文 {#syntax}

```sql
SHOW FUNCTIONS [LIKE '<pattern>' | WHERE <expr>] | [LIMIT <limit>]
```

## 例 {#example}

```sql
SHOW FUNCTIONS;

+-------------------------+--------------+---------------------------+
| name                    | is_aggregate | description               |
+-------------------------+--------------+---------------------------+
| !=                      |            0 |                           |
| %                       |            0 |                           |
| *                       |            0 |                           |
| +                       |            0 |                           |
| -                       |            0 |                           |
| /                       |            0 |                           |
| <                       |            0 |                           |
| <=                      |            0 |                           |
| <>                      |            0 |                           |
| =                       |            0 |                           |
+-------------------------+--------------+---------------------------+
```

`"today"` で始まる関数を表示します。

```sql
SHOW FUNCTIONS LIKE 'today%';

+--------------+--------------+-------------+
| name         | is_aggregate | description |
+--------------+--------------+-------------+
| today        |            0 |             |
| todayofmonth |            0 |             |
| todayofweek  |            0 |             |
| todayofyear  |            0 |             |
+--------------+--------------+-------------+
```

`WHERE` を使用して `"today"` で始まる関数を表示します。

```sql
SHOW FUNCTIONS WHERE name LIKE 'today%';

+--------------+--------------+-------------+
| name         | is_aggregate | description |
+--------------+--------------+-------------+
| today        |            0 |             |
| todayofmonth |            0 |             |
| todayofweek  |            0 |             |
| todayofyear  |            0 |             |
+--------------+--------------+-------------+
```