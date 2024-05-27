---
title: SHOW STATS_BUCKETS
summary: TiDB データベースの SHOW STATS_BUCKETS の使用法の概要。
---

# STATS_BUCKETSを表示 {#show-stats-buckets}

`SHOW STATS_BUCKETS`文は[統計](/statistics.md)のバケット情報を表示します。

現在、 `SHOW STATS_BUCKETS`ステートメントは次の列を返します。

| カラム名             | 説明                                                                        |
| :--------------- | :------------------------------------------------------------------------ |
| `Db_name`        | データベース名                                                                   |
| `Table_name`     | テーブル名                                                                     |
| `Partition_name` | パーティション名                                                                  |
| `Column_name`    | 列名（ `is_index`が`0`の場合）またはインデックス名（ `is_index`が`1`の場合）                      |
| `Is_index`       | インデックス列であるかどうか                                                            |
| `Bucket_id`      | バケットのID                                                                   |
| `Count`          | バケットと前のバケットに含まれるすべての値の数                                                   |
| `Repeats`        | 最大値の発生回数                                                                  |
| `Lower_bound`    | 最小値                                                                       |
| `Upper_bound`    | 最大値                                                                       |
| `Ndv`            | バケット内の異なる値の数。1 `tidb_analyze_version` `1`の場合、 `Ndv`は常に`0`となり、実際の意味はありません。 |

## 概要 {#synopsis}

```ebnf+diagram
ShowStatsBucketsStmt ::=
    "SHOW" "STATS_BUCKETS" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

```sql
SHOW STATS_BUCKETS WHERE Table_name='t';
```

    +---------+------------+----------------+-------------+----------+-----------+-------+---------+--------------------------+--------------------------+------+
    | Db_name | Table_name | Partition_name | Column_name | Is_index | Bucket_id | Count | Repeats | Lower_Bound              | Upper_Bound              | Ndv  |
    +---------+------------+----------------+-------------+----------+-----------+-------+---------+--------------------------+--------------------------+------+
    | test    | t          |                | a           |        0 |         0 |     1 |       1 | 2023-12-27 00:00:00      | 2023-12-27 00:00:00      |    0 |
    | test    | t          |                | a           |        0 |         1 |     2 |       1 | 2023-12-28 00:00:00      | 2023-12-28 00:00:00      |    0 |
    | test    | t          |                | ia          |        1 |         0 |     1 |       1 | (NULL, 2)                | (NULL, 2)                |    0 |
    | test    | t          |                | ia          |        1 |         1 |     2 |       1 | (NULL, 4)                | (NULL, 4)                |    0 |
    | test    | t          |                | ia          |        1 |         2 |     3 |       1 | (2023-12-27 00:00:00, 1) | (2023-12-27 00:00:00, 1) |    0 |
    | test    | t          |                | ia          |        1 |         3 |     4 |       1 | (2023-12-28 00:00:00, 3) | (2023-12-28 00:00:00, 3) |    0 |
    +---------+------------+----------------+-------------+----------+-----------+-------+---------+--------------------------+--------------------------+------+
    6 rows in set (0.00 sec)

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
-   [統計入門](/statistics.md)
