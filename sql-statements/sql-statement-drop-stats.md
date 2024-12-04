---
title: DROP STATS
summary: An overview of the usage of DROP STATS for the TiDB database.
---

# DROP STATS

The `DROP STATS` statement is used to delete the statistics of the selected table from the selected database.

## Synopsis

```ebnf+diagram
DropStatsStmt ::=
    'DROP' 'STATS' TableName  ("PARTITION" partition | "GLOBAL")? ( ',' TableName )*

TableName ::=
    Identifier ('.' Identifier)?
```

## Usage

The following statement deletes all statistics of `TableName`. If a partitioned table is specified, this statement deletes statistics of all partitions in this table as well as [global statistics generated in dynamic pruning mode](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode).

```sql
DROP STATS TableName
```

```
Query OK, 0 rows affected (0.00 sec)
```

The following statement only deletes statistics of the specified partitions in `PartitionNameList`.

```sql
DROP STATS TableName PARTITION PartitionNameList;
```

```
Query OK, 0 rows affected (0.00 sec)
```

The following statement only deletes global statistics generated in dynamic pruning mode of the specified table.

```sql
DROP STATS TableName GLOBAL;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## Examples

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

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Introduction to Statistics](/statistics.md)
