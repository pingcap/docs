---
title: SHOW COLUMN_STATS_USAGE
summary: TiDB データベースの SHOW COLUMN_STATS_USAGE の使用法の概要。
---

# COLUMN_STATS_USAGE を表示 {#show-column-stats-usage}

`SHOW COLUMN_STATS_USAGE`ステートメントは、列統計の最終使用時間と収集時間を表示します。また、これを使用して、統計が収集された`PREDICATE COLUMNS`と列を見つけることもできます。

現在、 `SHOW COLUMN_STATS_USAGE`ステートメントは次の列を返します。

| カラム名               | 説明                     |
| ------------------ | ---------------------- |
| `Db_name`          | データベース名                |
| `Table_name`       | テーブル名                  |
| `Partition_name`   | パーティション名               |
| `Column_name`      | 列名                     |
| `Last_used_at`     | クエリの最適化で列統計が最後に使用された時刻 |
| `Last_analyzed_at` | 列統計が最後に収集された時刻         |

## 概要 {#synopsis}

```ebnf+diagram
ShowColumnStatsUsageStmt ::=
    "SHOW" "COLUMN_STATS_USAGE" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

```sql
SHOW COLUMN_STATS_USAGE;
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

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
-   [統計入門](/statistics.md)
