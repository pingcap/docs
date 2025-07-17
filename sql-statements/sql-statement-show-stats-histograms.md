---
title: SHOW STATS_HISTOGRAMS
summary: An overview of the usage of SHOW STATS_HISTOGRAMS for TiDB database.
---

# SHOW STATS_HISTOGRAMS

This statement shows the histogram information collected by the [`ANALYZE` statement](/sql-statements/sql-statement-analyze-table.md) as part of database [statistics](/statistics.md).

Currently, the `SHOW STATS_HISTOGRAMS` statement returns the following columns:

| Column name | Description            |
| -------- | ------------- |
| `Db_name` | Database name |
| `Table_name` | The table name |
| `Partition_name` | The partition name |
| `Column_name` | The column name (when `is_index` is `0`) or the index name (when `is_index` is `1`) |
| `Is_index` | Whether it is an index column or not |
| `Update_time` | The update time |
| `Distinct_count` | The distinct count |
| `Null_count` | NULL count |
| `Avg_col_size` | The average col size |
| `Correlation` | Pearson correlation coefficient between this column and the integer primary key column, indicating the degree of association between the two columns |
| `Load_status` | Load status, such as `allEvicted` and `allLoaded` |
| `Total_mem_usage` | The total memory usage |
| `Hist_mem_usage` | The historical memory usage |
| `Topn_mem_usage` | The TopN memory usage |
| `Cms_mem_usage` | The CMS memory usage |

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
