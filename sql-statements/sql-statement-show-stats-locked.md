---
title: SHOW STATS_LOCKED
summary: An overview of the usage of SHOW STATS_LOCKED for the TiDB database.
---

# STATS_LOCKEDを表示 {#show-stats-locked}

`SHOW STATS_LOCKED` 、統計がロックされているテーブルを示します。

> **警告：**
>
> 統計のロックは、現在のバージョンの実験的機能です。本番環境での使用はお勧めできません。

## あらすじ {#synopsis}

```ebnf+diagram
ShowStatsLockedStmt ::= 'SHOW' 'STATS_LOCKED' ShowLikeOrWhereOpt

ShowLikeOrWhereOpt ::= 'LIKE' SimpleExpr | 'WHERE' Expression
```

## 例 {#examples}

table `t`を作成し、そこにデータを挿入します。テーブル`t`の統計がロックされていない場合、 `ANALYZE`ステートメントは正常に実行できます。

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

テーブル`t`の統計をロックし、 `SHOW STATS_LOCKED`を実行します。出力は、テーブル`t`の統計がロックされていることを示しています。

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

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [統計](/statistics.md#lock-statistics)
-   [ロック統計](/sql-statements/sql-statement-lock-stats.md)
-   [ステータスのロックを解除する](/sql-statements/sql-statement-unlock-stats.md)
