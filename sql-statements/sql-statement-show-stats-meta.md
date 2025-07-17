---
title: SHOW STATS_META
summary: 关于 TiDB 数据库中 SHOW STATS_META 使用情况的概述。
---

# SHOW STATS_META

你可以使用 `SHOW STATS_META` 来查看一个表中的行数以及该表中被修改的行数。在使用此语句时，可以通过 `ShowLikeOrWhere` 子句过滤所需的信息。

目前，`SHOW STATS_META` 语句输出 6 列：

| Column name | Description            |
| -------- | ------------- |
| db_name  |  数据库名称    |
| table_name | 表名称 |
| partition_name| 分区名称 |
| update_time | 最后更新时间 |
| modify_count | 被修改的行数 |
| row_count | 总行数 |

> **Note:**
>
> `update_time` 在 TiDB 根据 DML 语句更新 `modify_count` 和 `row_count` 字段时会被更新。因此，`update_time` 并不代表 `ANALYZE` 语句的最后执行时间。

## Synopsis

```ebnf+diagram
ShowStatsMetaStmt ::=
    "SHOW" "STATS_META" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## Examples

```sql
SHOW STATS_META;
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t0         |                | 2020-05-15 16:58:00 |            0 |         0 |
| test    | t1         |                | 2020-05-15 16:58:04 |            0 |         0 |
| test    | t2         |                | 2020-05-15 16:58:11 |            0 |         0 |
| test    | s          |                | 2020-05-22 19:46:43 |            0 |         0 |
| test    | t          |                | 2020-05-25 12:04:21 |            0 |         0 |
+---------+------------+----------------+---------------------+--------------+-----------+
5 rows in set (0.00 sec)
```

```sql
SHOW STATS_META WHERE table_name = 't2';
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t2         |                | 2020-05-15 16:58:11 |            0 |         0 |
+---------+------------+----------------+---------------------+--------------+-----------+
1 row in set (0.00 sec)
```

## MySQL compatibility

此语句是 TiDB 对 MySQL 语法的扩展。

## See also

* [ANALYZE](/sql-statements/sql-statement-analyze-table.md)
* [Introduction to Statistics](/statistics.md)