---
title: SHOW STATS_META
summary: An overview of the usage of SHOW STATS_META for TiDB database.
---

# 統計_メタを表示 {#show-stats-meta}

`SHOW STATS_META`を使用すると、テーブル内の行数とそのテーブル内で変更された行数を表示できます。このステートメントを使用する場合、 `ShowLikeOrWhere`節で必要な情報をフィルタリングできます。

現在、 `SHOW STATS_META`ステートメントは 6 列を出力します。

| カラム名     | 説明       |
| -------- | -------- |
| データベース名  | データベース名  |
| テーブル名    | テーブル名    |
| パーティション名 | パーティション名 |
| 更新時間     | 最終更新時間   |
| 修正数      | 変更された行数  |
| 行数       | 合計行数     |

> **注記：**
>
> TiDB が DML ステートメントに従って`modify_count`フィールドと`row_count`フィールドを更新すると、 `update_time`が更新されます。したがって`update_time` `ANALYZE`ステートメントの最後の実行時刻ではありません。

## あらすじ {#synopsis}

**ショースタンド**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFiltertable**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

**ShowLikeOrWhereOpt**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## 例 {#examples}

```sql
show stats_meta;
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
show stats_meta where table_name = 't2';
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

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [分析する](/sql-statements/sql-statement-analyze-table.md)
-   [統計入門](/statistics.md)
