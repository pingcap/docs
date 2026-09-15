---
title: SHOW STATISTICS
summary: 显示表及其列的统计信息。统计信息通过提供数据分布、行数和不同值等信息，帮助查询优化器对查询执行计划做出更优决策。
---

# SHOW STATISTICS

显示表及其列的统计信息。统计信息通过提供数据分布、行数和不同值等信息，帮助查询优化器对查询执行计划做出更优决策。

{{{ .lake }}} 会在数据插入期间自动生成统计信息。你可以使用此命令检查这些统计信息，并将其与实际数据进行比较，以识别可能影响查询性能的差异。

## 语法 {#syntax}

```sql
SHOW STATISTICS [ FROM DATABASE <database_name> | FROM TABLE <database_name>.<table_name> ]
```

| 参数 | 描述                                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| FROM DATABASE | 显示指定数据库中所有表的统计信息。                                |
| FROM TABLE | 仅显示指定表的统计信息。                                |

如果未指定参数，该命令会返回当前数据库中所有表的统计信息。

## 输出列 {#output-columns}

该命令会为每个表中的每一列返回以下列：

| 列 | 描述                                                                                                                 |
|--------|-----------------------------------------------------------------------------------------------------------------------------|
| database | 数据库名称。                                |
| table | 表名称。                                |
| column_name | 列名称。                                |
| stats_row_count | 统计信息中累计考虑的行数。由于统计信息会在插入时更新，但不会在删除时递减，因此该数值可能会**大于** actual_row_count。 |
| actual_row_count | 当前快照下表中的实际行数。 |
| distinct_count | 通过 HyperLogLog 计算得到的不同值（NDV）估算数量。 |
| null_count | 列中 NULL 值的数量。 |
| avg_size | 列中每个值的平均大小（以字节为单位）。 |

## 示例 {#examples}

### 显示当前数据库的统计信息 {#show-statistics-for-current-database}

```sql
CREATE DATABASE test_db;
USE test_db;

CREATE TABLE t1 (id INT, name VARCHAR(50));
INSERT INTO t1 VALUES (1, 'Alice'), (2, 'Bob');

SHOW STATISTICS;
```

输出：

```
database  table  column_name  stats_row_count  actual_row_count  distinct_count  null_count  avg_size
test_db   t1     id           2                2                 2               0           4
test_db   t1     name         2                2                 2               0           16
```

### 显示指定表的统计信息 {#show-statistics-for-a-specific-table}

```sql
CREATE TABLE t2 (age INT, city VARCHAR(50));
INSERT INTO t2 VALUES (25, 'New York'), (30, 'London');

SHOW STATISTICS FROM TABLE test_db.t2;
```

输出：

```
database  table  column_name  stats_row_count  actual_row_count  distinct_count  null_count  avg_size
test_db   t2     age          2                2                 2               0           4
test_db   t2     city         2                2                 2               0           19
```

### 显示数据库中所有表的统计信息 {#show-statistics-for-all-tables-in-a-database}

```sql
SHOW STATISTICS FROM DATABASE test_db;
```

这将显示 `test_db` 数据库中所有表（`t1` 和 `t2`）的统计信息。

## 相关命令 {#related-commands}

- [SHOW TABLE STATUS](/tidb-cloud-lake/sql/show-table-status.md)：显示表的状态信息