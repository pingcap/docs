---
title: SHOW STATS_LOCKED
summary: TiDB データベースに対する SHOW STATS_LOCKED の使用法の概要。
---

# STATS_LOCKED を表示 {#show-stats-locked}

`SHOW STATS_LOCKED`統計がロックされているテーブルを表示します。

現在、 `SHOW STATS_LOCKED`ステートメントは次の列を返します。

| カラム名             | 説明                   |
| ---------------- | -------------------- |
| `Db_name`        | データベース名              |
| `Table_name`     | テーブル名                |
| `Partition_name` | パーティション名             |
| `Status`         | 統計ステータス（ `locked`など） |

## 概要 {#synopsis}

```ebnf+diagram
ShowStatsLockedStmt ::= 'SHOW' 'STATS_LOCKED' ShowLikeOrWhereOpt

ShowLikeOrWhereOpt ::= 'LIKE' SimpleExpr | 'WHERE' Expression
```

## 例 {#examples}

テーブル`t`を作成し、そこにデータを挿入します。テーブル`t`の統計がロックされていない場合、 `ANALYZE`ステートメントは正常に実行できます。

```sql
mysql> CREATE TABLE t(a INT, b INT);
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO t VALUES (1,2), (3,4), (5,6), (7,8);
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.02 sec)

mysql> SHOW WARNINGS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                                                                               |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "Row count in stats_meta is much smaller compared with the row count got by PD, use min(1, 15000/4) as the sample-rate=1" |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

テーブル`t`の統計をロックし、 `SHOW STATS_LOCKED`実行します。出力には、テーブル`t`の統計がロックされたことが示されます。

```sql
mysql> LOCK STATS t;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW STATS_LOCKED;
+---------+------------+----------------+--------+
| Db_name | Table_name | Partition_name | Status |
+---------+------------+----------------+--------+
| test    | t          |                | locked |
+---------+------------+----------------+--------+
1 row in set (0.01 sec)
```

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [統計](/statistics.md#lock-statistics)
-   [ロック統計](/sql-statements/sql-statement-lock-stats.md)
-   [統計情報のロックを解除](/sql-statements/sql-statement-unlock-stats.md)
