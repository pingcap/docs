---
title: UNLOCK STATS
summary: UNLOCK STATSは、テーブルの統計のロックを解除するために使用されます。MySQLの互換性を持ち、テーブルやパーティションの統計のロックを解除することで、ANALYZEを正常に実行できるようになります。統計やSTATS_LOCKEDを表示する際にも参照されます。
---

# ステータスのロックを解除する {#unlock-stats}

`UNLOCK STATS`は、テーブルの統計のロックを解除するために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
UnlockStatsStmt ::=
    'UNLOCK' 'STATS' (TableNameList) | (TableName 'PARTITION' PartitionNameList)

TableNameList ::=
    TableName (',' TableName)*

TableName ::=
    Identifier ( '.' Identifier )?

PartitionNameList ::=
    Identifier ( ',' Identifier )*
```

## 例 {#examples}

[ロック統計](/sql-statements/sql-statement-lock-stats.md)の例を参照してテーブル`t`を作成し、その統計をロックします。

テーブル`t`の統計のロックを解除すると、 `ANALYZE`正常に実行できるようになります。

```sql
mysql> UNLOCK STATS t;
Query OK, 0 rows affected (0.01 sec)

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.03 sec)

mysql> SHOW WARNINGS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                 |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "use min(1, 110000/8) as the sample-rate=1" |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

[ロック統計](/sql-statements/sql-statement-lock-stats.md)の例を参照してテーブルを作成し`t` 、そのパーティションの統計をロックします`p1` 。

パーティション`p1`の統計のロックを解除すると、 `ANALYZE`正常に実行できるようになります。

```sql
mysql> UNLOCK STATS t PARTITION p1;
Query OK, 0 rows affected (0.00 sec)

mysql> ANALYZE TABLE t PARTITION p1;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                              |
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1" |
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [統計](/statistics.md#lock-statistics)
-   [ロック統計](/sql-statements/sql-statement-lock-stats.md)
-   [STATS_LOCKEDを表示](/sql-statements/sql-statement-show-stats-locked.md)
