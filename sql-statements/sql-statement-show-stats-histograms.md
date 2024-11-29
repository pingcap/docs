---
title: SHOW STATS_HISTOGRAMS
aliases: ['/tidb/stable/sql-statement-show-histograms']
summary: TiDB データベースの SHOW HISTOGRAMS の使用法の概要。
---

# 統計ヒストグラムを表示 {#show-stats-histograms}

このステートメントは、データベース[統計](/statistics.md)の一部として[`ANALYZE`ステートメント](/sql-statements/sql-statement-analyze-table.md)によって収集されたヒストグラム情報を表示します。

現在、 `SHOW STATS_HISTOGRAMS`ステートメントは次の列を返します。

| カラム名              | 説明                                                 |
| ----------------- | -------------------------------------------------- |
| `Db_name`         | データベース名                                            |
| `Table_name`      | テーブル名                                              |
| `Partition_name`  | パーティション名                                           |
| `Column_name`     | 列名（ `is_index`が`0`場合）またはインデックス名（ `is_index`が`1`場合） |
| `Is_index`        | インデックス列であるかどうか                                     |
| `Update_time`     | 更新時間                                               |
| `Distinct_count`  | 個別のカウント                                            |
| `Null_count`      | NULL カウント                                          |
| `Avg_col_size`    | 平均コルサイズ                                            |
| `Correlation`     | この列と整数主キー列の間のピアソン相関係数。2つの列間の関連の度合いを示します。           |
| `Load_status`     | 負荷ステータス（ `allEvicted`など`allLoaded`                 |
| `Total_mem_usage` | 総メモリ使用量                                            |
| `Hist_mem_usage`  | 過去のメモリ使用量                                          |
| `Topn_mem_usage`  | TopNのメモリ使用量                                        |
| `Cms_mem_usage`   | CMSのメモリ使用量                                         |

## 概要 {#synopsis}

```ebnf+diagram
ShowStatsHistogramsStmt ::=
    "SHOW" "STATS_HISTOGRAMS" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

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

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [分析する](/sql-statements/sql-statement-analyze-table.md)
-   [統計入門](/statistics.md)
