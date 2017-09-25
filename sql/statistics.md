---
title: Introduction to Statistics
category: user guide
---

# Introduction to Statistics

Based on the statistics, the TiDB optimizer chooses the most efficient query execution plan. The statistics collect table-level and column-level information. The statistics of tables include the total number of rows and the number of modified rows. The statistics of columns include the number of different values, the number of `NULL`, and the histogram of one column.

## Collect Statistics

### Manual Collection

You can run the `ANALYZE` statement to collect statistics.

Syntax:

```sql
ANALYZE TABLE TableNameList
> The statement collects statistics of all the tables in the `TableNameList` list. 

ANALYZE TABLE TableName INDEX IndexNameList
> The statement collects statistics of the index columns on all the `IndexNameList` lists in the `TableName` tables. 
```

### Automatic Update

When you insert, delete or modify statements, TiDB automatically updates the number of rows and modified rows. TiDB keeps these information on a regular basis, and the update period is 5 * `stats-lease`. The default value of `stats-lease` is `3s`. If you specify the value as `0`, it won't update automatically.

### Control `ANALYZE` Concurrency

When you run the `ANALYZE` statement, you can adjust the concurrency through certain parameters, to control its effect on the system.

#### `tidb_build_stats_concurrency` 

Currently, when you run the `ANALYZE` statement, the calculation is divided into multiple small tasks. Each task only works on one column or index. You can use the `tidb_build_stats_concurrency` parameter to control the number of simultaneous tasks. The default value is `4`.

#### `tidb_distsql_scan_concurrency`

When you execute the task of analyzing regular columns, you can use the `tidb_distsql_scan_concurrency` parameter to control the number of Region to be read at one time. The default value is `10`.

#### `tidb_index_serial_scan_concurrency`

When you execute the task of analyzing index columns, you can use the `tidb_index_serial_scan_concurrency` parameter to control the number of Region to be read at one time. The default value is `1`.

## View Statistics

You can view the statistics status through certain statements.

### Metadata of Tables

You can use the `SHOW STATS_META` statement to view the total number of rows and the number of modified rows.

Syntax:

```sql
SHOW STATS_META [ShowLikeOrWhere]
> The statement returns the total number of rows and the number of modified rows. You can use `ShowLikeOrWhere` to filter the information you need.
```

Currently, the `SHOW STATS_META` statement returns the following 5 columns:

| Syntax Element | Description  |
| :-------- | :------------- |
| `db_name`  |  database name    |
| `table_name` | table name |
| `update_time` | update time |
| `modify_count` | the number of modified rows |
| `row_count` | the total number of rows |

### Metadata of Columns

You can use the `SHOW STATS_HISTOGRAMS` statement to view the number of different values and the number of `NULL` in all the columns.

Syntax:

```sql
SHOW STATS_HISTOGRAMS [ShowLikeOrWhere]
> The statement returns the number of different values and the number of `NULL` in all the columns. You can use `ShowLikeOrWhere` to filter the information you need.
```

Currently, the `SHOW STATS_HISTOGRAMS` statement returns the following 7 columns:

| Syntax Element | Description    |
| :-------- | :------------- |
| `db_name`  |  database name    |
| `table_name` | table name |
| `column_name` | column name |
| `is_index` | whether an index column or not |
| `update_time` | update time |
| `distinct_count` | the number of different values |
| `null_count` | the number of `NULL` |

### Buckets of Histogram

You can use the `SHOW STATS_BUCKETS` statement to view each bucket of the histogram.

Syntax:

```sql
SHOW STATS_BUCKETS [ShowLikeOrWhere]
> The statement returns information about all the buckets. You can use `ShowLikeOrWhere` to filter the information you need.
```

Currently, the `SHOW STATS_BUCKETS` statement returns the following 9 columns:

| Syntax Element | Description   |
| :-------- | :------------- |
| `db_name`  |  database name    |
| `table_name` | table name |
| `column_name` | column name |
| `is_index` | whether an index column or not |
| `bucket_id` | the ID of a bucket |
| `count` | the number of all the values that falls on the bucket and the previous buckets |
| `repeats` | the occurrence number of the maximum value |
| `lower_bound` | the minimum value |
| `upper_bound` | the maximum value |
