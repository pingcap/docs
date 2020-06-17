---
title: DROP STATS
summary: An overview of the usage of DROP STATS for the TiDB database.
category: reference
---

# DROP STATS

`DROP STATS` 语句用于从当前所选定的数据库中删除选定表的统计信息。

## Synopsis

**DropStatsStmt:**

![DropTableStmt](/media/sqlgram/DropStatsStmt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

## Examples

{{< copyable "sql" >}}

```sql
CREATE TABLE t(a INT);
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          |                | 2020-05-25 20:34:33 |            0 |         0 |
+---------+------------+----------------+---------------------+--------------+-----------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
DROP STATS t;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

```sql
Empty set (0.00 sec)
```

## See also

* [Introduction to Statistics](/statistics.md)