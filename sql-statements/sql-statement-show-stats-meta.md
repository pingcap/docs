---
title: SHOW STATS_META
summary: SHOW STATS_META 在 TiDB 数据库中的用法概述。
---

# SHOW STATS_META

你可以使用 `SHOW STATS_META` 查看某个表中的行数以及该表中被更改的行数。在使用该语句时，可以通过 `ShowLikeOrWhere` 子句过滤所需的信息。

目前，`SHOW STATS_META` 语句输出以下列：

| 列名 | 描述            |
| -------- | ------------- |
| Db_name  |  数据库名称    |
| Table_name | 表名称 |
| Partition_name| 分区名称 |
| Update_time | 最后更新时间 |
| Modify_count | 被修改的行数 |
| Row_count | 总行数 |
| Last_analyze_time | 表最后一次被分析的时间 |

> **Note:**
>
> 当 TiDB 根据 DML 语句更新 `modify_count` 和 `row_count` 字段时，`update_time` 会被更新。因此，`update_time` 并不是 `ANALYZE` 语句的最后执行时间。

## 语法

```ebnf+diagram
ShowStatsMetaStmt ::=
    "SHOW" "STATS_META" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
SHOW STATS_META;
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count | Last_analyze_time   |
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
| test    | t0         |                | 2025-07-27 16:58:00 |            0 |         0 | 2025-07-27 16:58:00 |
| test    | t1         |                | 2025-07-27 16:58:04 |            0 |         0 | 2025-07-27 16:58:04 |
| test    | t2         |                | 2025-07-27 16:58:11 |            0 |         0 | 2025-07-27 16:58:11 |
| test    | s          |                | 2025-07-27 19:46:43 |            0 |         0 | 2025-07-27 19:46:43 |
| test    | t          |                | 2025-07-27 12:04:21 |            0 |         0 | 2025-07-27 12:04:21 |
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
5 rows in set (0.00 sec)
```

```sql
SHOW STATS_META WHERE table_name = 't2';
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count | Last_analyze_time   |
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
| test    | t2         |                | 2025-07-27 16:58:11 |            0 |         0 | 2025-07-27 16:58:11 |
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [ANALYZE](/sql-statements/sql-statement-analyze-table.md)
* [统计信息简介](/statistics.md)
