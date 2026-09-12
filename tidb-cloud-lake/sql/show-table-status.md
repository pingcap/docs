---
title: SHOW TABLE STATUS
summary: 显示数据库中各个表的状态。状态信息包括表的各种物理大小和时间戳，详见“示例”。
---

# SHOW TABLE STATUS

显示数据库中各个表的状态。状态信息包括表的各种物理大小和时间戳，详见[示例](#examples)。

## 语法 {#syntax}

```sql
SHOW TABLE STATUS
    [ {FROM | IN} <database_name> ]
    [ LIKE 'pattern' | WHERE expr ]
```

| 参数 | 描述 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| FROM / IN | 指定一个数据库。如果省略，则该命令返回当前数据库中的结果。 |
| LIKE      | 使用大小写敏感的模式匹配按表名过滤结果。 |
| WHERE     | 使用 WHERE 子句中的表达式过滤结果。 |

## 示例 {#examples}

以下示例显示当前数据库中各个表的状态，提供名称、引擎、行数以及其他相关信息等详细内容：

```sql
SHOW TABLE STATUS;

name   |engine|version|row_format|rows|avg_row_length|data_length|max_data_length|index_length|data_free|auto_increment|create_time                  |update_time|check_time|collation|checksum|comment|cluster_by|
-------+------+-------+----------+----+--------------+-----------+---------------+------------+---------+--------------+-----------------------------+-----------+----------+---------+--------+-------+----------+
books  |FUSE  |      0|          |   2|              |        160|               |         713|         |              |2023-09-25 06:40:47.237 +0000|           |          |         |        |       |          |
mytable|FUSE  |      0|          |   5|              |         40|               |        1665|         |              |2023-08-28 07:53:05.455 +0000|           |          |         |        |       |((a + 1)) |
ontime |FUSE  |      0|          | 199|              |     147981|               |       22961|         |              |2023-09-19 07:04:06.414 +0000|           |          |         |        |       |          |
```

以下示例显示当前数据库中名称以 `'my'` 开头的表的状态：

```sql
SHOW TABLE STATUS LIKE 'my%';

name   |engine|version|row_format|rows|avg_row_length|data_length|max_data_length|index_length|data_free|auto_increment|create_time                  |update_time|check_time|collation|checksum|comment|cluster_by|
-------+------+-------+----------+----+--------------+-----------+---------------+------------+---------+--------------+-----------------------------+-----------+----------+---------+--------+-------+----------+
mytable|FUSE  |      0|          |   5|              |         40|               |        1665|         |              |2023-08-28 07:53:05.455 +0000|           |          |         |        |       |((a + 1)) |
```

以下示例显示当前数据库中行数大于 100 的表的状态：

> **注意：**
>
> 使用 SHOW TABLE STATUS 查询时，请注意某些列名（例如 `"rows"`）可能会被解释为 SQL 关键字，从而导致错误。为避免此问题，请始终使用反引号将列名括起来，如本示例所示。这样可以确保在 SQL 查询中，列名被视为标识符而不是关键字。

```sql
SHOW TABLE STATUS WHERE `rows` > 100;

name  |engine|version|row_format|rows|avg_row_length|data_length|max_data_length|index_length|data_free|auto_increment|create_time                  |update_time|check_time|collation|checksum|comment|cluster_by|
------+------+-------+----------+----+--------------+-----------+---------------+------------+---------+--------------+-----------------------------+-----------+----------+---------+--------+-------+----------+
ontime|FUSE  |      0|          | 199|              |     147981|               |       22961|         |              |2023-09-19 07:04:06.414 +0000|           |          |         |        |       |          |
```