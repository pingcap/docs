---
title: SHOW STATS_HISTOGRAMS
summary: 关于 TiDB 数据库中 SHOW STATS_HISTOGRAMS 的使用概述。
---

# SHOW STATS_HISTOGRAMS

此语句显示由 [`ANALYZE` 语句](/sql-statements/sql-statement-analyze-table.md) 作为数据库 [统计信息](/statistics.md) 一部分收集的直方图信息。

目前，`SHOW STATS_HISTOGRAMS` 语句返回以下列：

| 列名 | 描述 |
| -------- | ------------- |
| `Db_name` | 数据库名称 |
| `Table_name` | 表名 |
| `Partition_name` | 分区名称 |
| `Column_name` | 列名（当 `is_index` 为 `0` 时）或索引名（当 `is_index` 为 `1` 时） |
| `Is_index` | 是否为索引列 |
| `Update_time` | 更新时间 |
| `Distinct_count` | 不同值数量 |
| `Null_count` | NULL 值数量 |
| `Avg_col_size` | 列的平均大小 |
| `Correlation` | 该列与整数主键列之间的 Pearson 相关系数，表示两列之间的关联程度 |
| `Load_status` | 加载状态，例如 `allEvicted` 和 `allLoaded` |
| `Total_mem_usage` | 总内存使用量 |
| `Hist_mem_usage` | 历史内存使用量 |
| `Topn_mem_usage` | TopN 内存使用量 |
| `Cms_mem_usage` | CMS 内存使用量 |

## 概要

```ebnf+diagram
ShowStatsHistogramsStmt ::=
    "SHOW" "STATS_HISTOGRAMS" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

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
3 行结果（0.00 秒）
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
2 行结果（0.00 秒）
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [ANALYZE](/sql-statements/sql-statement-analyze-table.md)
* [统计信息简介](/statistics.md)