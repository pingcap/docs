---
title: SHOW COLUMN_STATS_USAGE
summary: An overview of the usage of SHOW COLUMN_STATS_USAGE for TiDB database.
---

# SHOW COLUMN_STATS_USAGE

The `SHOW COLUMN_STATS_USAGE` statement shows the last usage time and collection time of column statistics. You can also use it to locate `PREDICATE COLUMNS` and columns on which statistics have been collected.

Currently, the `SHOW COLUMN_STATS_USAGE` statement returns the following columns:

| Column name | Description            |
| -------- | ------------- |
| `Db_name`  |  The database name    |
| `Table_name` | The table name |
| `Partition_name` | The partition name |
| `Column_name` | The column name |
| `Last_used_at` | The last time when the column statistics were used in the query optimization |
| `Last_analyzed_at` | The last time when the column statistics were collected |

## Synopsis

```ebnf+diagram
ShowColumnStatsUsageStmt ::=
    "SHOW" "COLUMN_STATS_USAGE" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## Examples

```sql
SHOW COLUMN_STATS_USAGE;
```

```
+---------+------------+----------------+-------------+--------------+---------------------+
| Db_name | Table_name | Partition_name | Column_name | Last_used_at | Last_analyzed_at    |
+---------+------------+----------------+-------------+--------------+---------------------+
| test    | t1         |                | id          | NULL         | 2024-05-10 11:04:23 |
| test    | t1         |                | b           | NULL         | 2024-05-10 11:04:23 |
| test    | t1         |                | pad         | NULL         | 2024-05-10 11:04:23 |
| test    | t          |                | a           | NULL         | 2024-05-10 11:37:06 |
| test    | t          |                | b           | NULL         | 2024-05-10 11:37:06 |
+---------+------------+----------------+-------------+--------------+---------------------+
5 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
* [Introduction to Statistics](/statistics.md)