---
title: SHOW STATS_BUCKETS
summary: An overview of the usage of SHOW STATS_BUCKETS for TiDB database.
---

# SHOW STATS_BUCKETS

The `SHOW STATS_BUCKETS` statement shows the bucket information in [statistics](/statistics.md).

Currently, the `SHOW STATS_BUCKETS` statement returns the following columns:

| Column name | Description   |
| :-------- | :------------- |
| `Db_name`  |  The database name    |
| `Table_name` | The table name |
| `Partition_name` | The partition name |
| `Column_name` | The column name (when `is_index` is `0`) or the index name (when `is_index` is `1`) |
| `Is_index` | Whether it is an index column or not |
| `Bucket_id` | The ID of a bucket |
| `Count` | The number of all the values that falls on the bucket and the previous buckets |
| `Repeats` | The occurrence number of the maximum value |
| `Lower_bound` | The minimum value |
| `Upper_bound` | The maximum value |
| `Ndv` | The number of distinct values in the bucket. This field is deprecated and always shows `0` due to its inaccurate value. |

## Synopsis

```ebnf+diagram
ShowStatsBucketsStmt ::=
    "SHOW" "STATS_BUCKETS" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## Examples

```sql
SHOW STATS_BUCKETS WHERE Table_name='t';
```

```
+---------+------------+----------------+-------------+----------+-----------+-------+---------+--------------------------+--------------------------+------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Bucket_id | Count | Repeats | Lower_Bound              | Upper_Bound              | Ndv  |
+---------+------------+----------------+-------------+----------+-----------+-------+---------+--------------------------+--------------------------+------+
| test    | t          |                | a           |        0 |         0 |     1 |       1 | 2023-12-27 00:00:00      | 2023-12-27 00:00:00      |    0 |
| test    | t          |                | a           |        0 |         1 |     2 |       1 | 2023-12-28 00:00:00      | 2023-12-28 00:00:00      |    0 |
| test    | t          |                | ia          |        1 |         0 |     1 |       1 | (NULL, 2)                | (NULL, 2)                |    0 |
| test    | t          |                | ia          |        1 |         1 |     2 |       1 | (NULL, 4)                | (NULL, 4)                |    0 |
| test    | t          |                | ia          |        1 |         2 |     3 |       1 | (2023-12-27 00:00:00, 1) | (2023-12-27 00:00:00, 1) |    0 |
| test    | t          |                | ia          |        1 |         3 |     4 |       1 | (2023-12-28 00:00:00, 3) | (2023-12-28 00:00:00, 3) |    0 |
+---------+------------+----------------+-------------+----------+-----------+-------+---------+--------------------------+--------------------------+------+
6 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
* [Introduction to Statistics](/statistics.md)
