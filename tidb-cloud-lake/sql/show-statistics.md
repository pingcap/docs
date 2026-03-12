---
title: SHOW STATISTICS
sidebar_position: 15
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.802"/>

Displays statistical information about tables and their columns. Statistics help the query optimizer make better decisions about query execution plans by providing information about data distribution, row counts, and distinct values.

Databend automatically generates statistics during data insertion. You can use this command to inspect the statistics and compare them with actual data to identify any discrepancies that might affect query performance.

## Syntax

```sql
SHOW STATISTICS [ FROM DATABASE <database_name> | FROM TABLE <database_name>.<table_name> ]
```

| Parameter | Description                                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| FROM DATABASE | Shows statistics for all tables in the specified database.                                |
| FROM TABLE | Shows statistics for the specified table only.                                |

If no parameter is specified, the command returns statistics for all tables in the current database.

## Output Columns

The command returns the following columns for each column in each table:

| Column | Description                                                                                                                 |
|--------|-----------------------------------------------------------------------------------------------------------------------------|
| database | The database name.                                |
| table | The table name.                                |
| column_name | The column name.                                |
| stats_row_count | The accumulated number of rows considered in statistics. Since stats are updated on inserts but not decremented on deletes, this number can be **greater than** actual_row_count. |
| actual_row_count | The actual number of rows in the table under the current snapshot. |
| distinct_count | Estimated number of distinct values (NDV), computed from HyperLogLog. |
| null_count | Number of NULL values in the column. |
| avg_size | Average size in bytes of each value in the column. |

## Examples

### Show Statistics for Current Database

```sql
CREATE DATABASE test_db;
USE test_db;

CREATE TABLE t1 (id INT, name VARCHAR(50));
INSERT INTO t1 VALUES (1, 'Alice'), (2, 'Bob');

SHOW STATISTICS;
```

Output:
```
database  table  column_name  stats_row_count  actual_row_count  distinct_count  null_count  avg_size
test_db   t1     id           2                2                 2               0           4
test_db   t1     name         2                2                 2               0           16
```

### Show Statistics for a Specific Table

```sql
CREATE TABLE t2 (age INT, city VARCHAR(50));
INSERT INTO t2 VALUES (25, 'New York'), (30, 'London');

SHOW STATISTICS FROM TABLE test_db.t2;
```

Output:
```
database  table  column_name  stats_row_count  actual_row_count  distinct_count  null_count  avg_size
test_db   t2     age          2                2                 2               0           4
test_db   t2     city         2                2                 2               0           19
```

### Show Statistics for All Tables in a Database

```sql
SHOW STATISTICS FROM DATABASE test_db;
```

This will show statistics for all tables (`t1` and `t2`) in the `test_db` database.

## Related Commands

- [SHOW TABLE STATUS](show-table-status.md): Shows status information about tables
