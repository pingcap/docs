---
title: SHOW STATS_META
summary: TiDB データベースの SHOW STATS_META の使用法の概要。
---

# STATS_METAを表示 {#show-stats-meta}

`SHOW STATS_META`使用すると、テーブル内の行数と、そのテーブルで変更された行数を表示できます。このステートメントを使用する場合、 `ShowLikeOrWhere`句を使用して必要な情報をフィルタリングできます。

現在、 `SHOW STATS_META`ステートメントは 6 つの列を出力します。

| カラム名     | 説明       |
| -------- | -------- |
| データベース名  | データベース名  |
| テーブル名    | テーブル名    |
| パーティション名 | パーティション名 |
| 更新時間     | 最終更新時間   |
| 修正回数     | 変更された行数  |
| 行数       | 合計行数     |

> **注記：**
>
> `update_time` 、TiDBがDML文に従って`modify_count`と`row_count`フィールドを更新したときに更新されます。したがって、 `update_time` `ANALYZE`文の最終実行時刻ではありません。

## 概要 {#synopsis}

```ebnf+diagram
ShowStatsMetaStmt ::=
    "SHOW" "STATS_META" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

```sql
SHOW STATS_META;
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t0         |                | 2020-05-15 16:58:00 |            0 |         0 |
| test    | t1         |                | 2020-05-15 16:58:04 |            0 |         0 |
| test    | t2         |                | 2020-05-15 16:58:11 |            0 |         0 |
| test    | s          |                | 2020-05-22 19:46:43 |            0 |         0 |
| test    | t          |                | 2020-05-25 12:04:21 |            0 |         0 |
+---------+------------+----------------+---------------------+--------------+-----------+
5 rows in set (0.00 sec)
```

```sql
SHOW STATS_META WHERE table_name = 't2';
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t2         |                | 2020-05-15 16:58:11 |            0 |         0 |
+---------+------------+----------------+---------------------+--------------+-----------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [分析](/sql-statements/sql-statement-analyze-table.md)
-   [統計入門](/statistics.md)
