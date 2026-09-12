---
title: SHOW FUNCTIONS
summary: 列出当前支持的内置标量函数和聚合函数。
---

# SHOW FUNCTIONS

列出当前支持的内置标量函数和聚合函数。

另请参阅：[system.functions](/tidb-cloud-lake/sql/system-functions.md)

## 语法 {#syntax}

```sql
SHOW FUNCTIONS [LIKE '<pattern>' | WHERE <expr>] | [LIMIT <limit>]
```

## 示例 {#example}

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

显示以 `"today"` 开头的函数：

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

使用 `WHERE` 显示以 `"today"` 开头的函数：

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