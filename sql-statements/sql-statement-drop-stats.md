---
title: DROP STATS
summary: 关于 TiDB 数据库中 DROP STATS 的使用概述。
---

# DROP STATS

`DROP STATS` 语句用于删除所选数据库中指定表的统计信息。

## 语法简介

```ebnf+diagram
DropStatsStmt ::=
    'DROP' 'STATS' TableName  ("PARTITION" partition | "GLOBAL")? ( ',' TableName )*

TableName ::=
    Identifier ('.' Identifier)?
```

## 用法

以下语句会删除 `TableName` 的所有统计信息。如果指定的是分区表，则此语句会删除该表所有分区的统计信息以及 [在动态修剪模式下生成的全局统计信息](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)。

```sql
DROP STATS TableName
```

```
Query OK, 0 rows affected (0.00 sec)
```

以下语句只会删除 `PartitionNameList` 中指定分区的统计信息。

```sql
DROP STATS TableName PARTITION PartitionNameList;
```

```
Query OK, 0 rows affected (0.00 sec)
```

以下语句只会删除在动态修剪模式下为指定表生成的全局统计信息。

```sql
DROP STATS TableName GLOBAL;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## 示例

```sql
CREATE TABLE t(a INT);
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

```
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          |                | 2020-05-25 20:34:33 |            0 |         0 |
+---------+------------+----------------+---------------------+--------------+-----------+
1 row in set (0.00 sec)
```

```sql
DROP STATS t;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

```
Empty set (0.00 sec)
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [Introduction to Statistics](/statistics.md)
