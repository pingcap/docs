---
title: SHOW STATS_TOPN
summary: TiDB データベースの SHOW STATS_TOPN の使用法の概要。
---

# STATS_TOPNを表示 {#show-stats-topn}

`SHOW STATS_TOPN`文は[統計](/statistics.md)の Top-N 情報を表示します。

現在、 `SHOW STATS_TOPN`ステートメントは次の列を返します。

| カラム名             | 説明                                                 |
| ---------------- | -------------------------------------------------- |
| `Db_name`        | データベース名                                            |
| `Table_name`     | テーブル名                                              |
| `Partition_name` | パーティション名                                           |
| `Column_name`    | 列名（ `is_index`が`0`場合）またはインデックス名（ `is_index`が`1`場合） |
| `Is_index`       | インデックス列であるかどうか                                     |
| `Value`          | この列の値                                              |
| `Count`          | 値が何回出現するか                                          |

## 概要 {#synopsis}

```ebnf+diagram
ShowStatsTopnStmt ::=
    "SHOW" "STATS_TOPN" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#example}

```sql
SHOW STATS_TOPN WHERE Table_name='t';
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

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
-   [統計入門](/statistics.md)
