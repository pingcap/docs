---
title: SHOW STATS_TOPN
summary: An overview of the usage of SHOW STATS_TOPN for TiDB database.
---

# SHOW STATS_TOPN

The `SHOW STATS_TOPN` statement shows the Top-N information in [statistics](/statistics.md).

Currently, the `SHOW STATS_TOPN` statement returns the following columns:

| Column name | Description |
| ---- | ----|
| `Db_name` | The database name |
| `Table_name` | The table name |
| `Partition_name` | The partition name |
| `Column_name` | The column name (when `is_index` is `0`) or the index name (when `is_index` is `1`) |
| `Is_index` | Whether it is an index column or not |
| `Value` | The value of this column |
| `Count` | How many times the value appears |

## Synopsis

```ebnf+diagram
ShowStatsTopnStmt ::=
    "SHOW" "STATS_TOPN" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## Example

```sql
SHOW STATS_TOPN WHERE Table_name='t';
```

```
+---------+------------+----------------+-------------+----------+--------------------------+-------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Value                    | Count |
+---------+------------+----------------+-------------+----------+--------------------------+-------+
| test    | t          |                | a           |        0 | 2023-12-27 00:00:00      |     1 |
| test    | t          |                | a           |        0 | 2023-12-28 00:00:00      |     1 |
| test    | t          |                | ia          |        1 | (NULL, 2)                |     1 |
| test    | t          |                | ia          |        1 | (NULL, 4)                |     1 |
| test    | t          |                | ia          |        1 | (2023-12-27 00:00:00, 1) |     1 |
| test    | t          |                | ia          |        1 | (2023-12-28 00:00:00, 3) |     1 |
+---------+------------+----------------+-------------+----------+--------------------------+-------+
6 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
* [Introduction to Statistics](/statistics.md)