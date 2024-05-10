---
title: SHOW STATS_HISTOGRAMS
summary: An overview of the usage of SHOW STATS_HISTOGRAMS for TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-histograms/','/tidb/dev/sql-statement-show-histograms']
---

# SHOW STATS_HISTOGRAMS

This statement shows the histogram information collected by the [`ANALYZE` statement](/sql-statements/sql-statement-analyze-table.md) as part of database [statistics](/statistics.md).

Currently, the `SHOW STATS_HISTOGRAMS` statement outputs 15 columns:

| Column name | Description            |
| -------- | ------------- |
| Db_name | Database name |
| Table_name | Table name |
| Partition_name | Partition name |
| Column_name | Column name |
| Is_index | 1 if this is an index, else 0 |
| Update_time | Update time |
| Distinct_count | Distinct count |
| Null_count | NULL count |
| Avg_col_size | Average col size |
| Correlation | Correlation |
| Load_status | Load status like `allEvicted`, `allLoaded`, etc |
| Total_mem_usage | Total memory usage |
| Hist_mem_usage | Historical memory usage |
| Topn_mem_usage | TopN memory usage |
| Cms_mem_usage | CMS memory usage |

## Synopsis

```ebnf+diagram
ShowStatsHistogramsStmt ::=
    "SHOW" "STATS_HISTOGRAMS" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## Examples

```sql
SHOW STATS_HISTOGRAMS;
```

```sql
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
| test    | t          |                | a           |        0 | 2020-05-25 19:20:00 |              7 |          0 |            1 |           1 |
| test    | t2         |                | a           |        0 | 2020-05-25 19:20:01 |              6 |          0 |            8 |           0 |
| test    | t2         |                | b           |        0 | 2020-05-25 19:20:01 |              6 |          0 |         1.67 |           1 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
3 rows in set (0.00 sec)
```

```sql
SHOW STATS_HISTOGRAMS WHERE table_name = 't2';
```

```sql
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
| test    | t2         |                | b           |        0 | 2020-05-25 19:20:01 |              6 |          0 |         1.67 |           1 |
| test    | t2         |                | a           |        0 | 2020-05-25 19:20:01 |              6 |          0 |            8 |           0 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
2 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [ANALYZE](/sql-statements/sql-statement-analyze-table.md)
* [Introduction to Statistics](/statistics.md)
