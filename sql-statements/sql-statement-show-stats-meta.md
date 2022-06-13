---
title: SHOW STATS_META
summary: An overview of the usage of SHOW STATS_META for TiDB database.
---

# SHOW STATS_META {#show-stats-meta}

`SHOW STATS_META`を使用して、テーブル内の行数と、そのテーブル内で変更された行数を表示できます。このステートメントを使用すると、 `ShowLikeOrWhere`句で必要な情報をフィルタリングできます。

現在、 `SHOW STATS_META`ステートメントは6列を出力します。

| 列名             | 説明       |
| -------------- | -------- |
| db_name        | データベース名  |
| table_name     | テーブル名    |
| partition_name | パーティション名 |
| update_time    | 最終更新時刻   |
| modify_count   | 変更された行数  |
| row_count      | 合計行数     |

> **あり：**
>
> `update_time`は、TiDBがDMLステートメントに従って`modify_count`フィールドと`row_count`フィールドを更新するときに更新されます。したがって、 `update_time`は`ANALYZE`ステートメントの最後の実行時間ではありません。

## あらすじ {#synopsis}

**ShowStmt**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFiltertable**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

**ShowLikeOrWhereOpt**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## 例 {#examples}

{{< copyable "" >}}

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

{{< copyable "" >}}

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

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [分析する](/sql-statements/sql-statement-analyze-table.md)
-   [統計入門](/statistics.md)
