---
title: SHOW STATS_HEALTHY
summary: TiDB データベースの SHOW STATS_HEALTHY の使用法の概要。
---

# 統計を表示_健康 {#show-stats-healthy}

`SHOW STATS_HEALTHY`文は、統計の正確さの推定値を示しています。健全性のパーセンテージが低いテーブルでは、最適ではないクエリ実行プランが生成される場合があります。

[`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを実行すると、テーブルの健全性が向上します。健全性が[`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)しきい値を下回ると、 `ANALYZE`自動的に実行されます。

現在、 `SHOW STATS_HEALTHY`ステートメントは次の列を返します。

| カラム名             | 説明           |
| ---------------- | ------------ |
| `Db_name`        | データベース名      |
| `Table_name`     | テーブル名        |
| `Partition_name` | パーティション名     |
| `Healthy`        | 0から100の間の健康度 |

## 概要 {#synopsis}

```ebnf+diagram
ShowStatsHealthyStmt ::=
    "SHOW" "STATS_HEALTHY" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

サンプルデータをロードして`ANALYZE`実行します。

```sql
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 b INT NOT NULL,
 pad VARBINARY(255),
 INDEX(b)
);

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM dual;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
SELECT SLEEP(1);
ANALYZE TABLE t1;
SHOW STATS_HEALTHY; # should be 100% healthy
```

```sql
...
mysql> SHOW STATS_HEALTHY;
+---------+------------+----------------+---------+
| Db_name | Table_name | Partition_name | Healthy |
+---------+------------+----------------+---------+
| test    | t1         |                |     100 |
+---------+------------+----------------+---------+
1 row in set (0.00 sec)
```

約 30% のレコードを削除する一括更新を実行します。統計の健全性を確認します。

```sql
DELETE FROM t1 WHERE id BETWEEN 101010 AND 201010; # delete about 30% of records
SHOW STATS_HEALTHY; 
```

```sql
mysql> SHOW STATS_HEALTHY;
+---------+------------+----------------+---------+
| Db_name | Table_name | Partition_name | Healthy |
+---------+------------+----------------+---------+
| test    | t1         |                |      50 |
+---------+------------+----------------+---------+
1 row in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [分析する](/sql-statements/sql-statement-analyze-table.md)
-   [統計入門](/statistics.md)
