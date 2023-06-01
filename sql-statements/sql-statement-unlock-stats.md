---
title: UNLOCK STATS
summary: An overview of the usage of UNLOCK STATS for the TiDB database.
---

# ステータスのロックを解除する {#unlock-stats}

`UNLOCK STATS`は、テーブルの統計のロックを解除するために使用されます。

> **警告：**
>
> 統計のロックは、現在のバージョンの実験的機能です。本番環境での使用はお勧めしません。

## あらすじ {#synopsis}

```ebnf+diagram
UnlockStatsStmt ::=
    'UNLOCK' 'STATS' TableNameList

TableNameList ::=
    TableName (',' TableName)*

TableName ::=
    Identifier ( '.' Identifier )?
```

## 例 {#examples}

table `t`を作成し、そこにデータを挿入します。テーブル`t`の統計がロックされていない場合、 `ANALYZE`ステートメントは正常に実行できます。

```sql
mysql> create table t(a int, b int);
Query OK, 0 rows affected (0.03 sec)

mysql> insert into t values (1,2), (3,4), (5,6), (7,8);
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> analyze table t;
Query OK, 0 rows affected, 1 warning (0.02 sec)

mysql> show warnings;
+-------+------+-----------------------------------------------------------------+
| Level | Code | Message                                                         |
+-------+------+-----------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t |
+-------+------+-----------------------------------------------------------------+
1 row in set (0.00 sec)
```

テーブル`t`の統計をロックし、 `ANALYZE`を実行します。 `SHOW STATS_LOCKED`の出力から、テーブル`t`の統計がロックされていることがわかります。警告メッセージは、 `ANALYZE`ステートメントがテーブル`t`をスキップしたことを示しています。

```sql
mysql> lock stats t;
Query OK, 0 rows affected (0.00 sec)

mysql> show stats_locked;
+---------+------------+----------------+--------+
| Db_name | Table_name | Partition_name | Status |
+---------+------------+----------------+--------+
| test    | t          |                | locked |
+---------+------------+----------------+--------+
1 row in set (0.01 sec)

mysql> analyze table t;
Query OK, 0 rows affected, 2 warnings (0.00 sec)

mysql> show warnings;
+---------+------+-----------------------------------------------------------------+
| Level   | Code | Message                                                         |
+---------+------+-----------------------------------------------------------------+
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t |
| Warning | 1105 | skip analyze locked table: t                                    |
+---------+------+-----------------------------------------------------------------+
2 rows in set (0.00 sec)
```

テーブル`t`と`ANALYZE`の統計のロックを解除すると、再度正常に実行できるようになります。

```sql
mysql> unlock stats t;
Query OK, 0 rows affected (0.01 sec)

mysql> analyze table t;
Query OK, 0 rows affected, 1 warning (0.03 sec)

mysql> show warnings;
+-------+------+-----------------------------------------------------------------+
| Level | Code | Message                                                         |
+-------+------+-----------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t |
+-------+------+-----------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [<a href="/statistics.md#lock-statistics">統計</a>](/statistics.md#lock-statistics)
-   [<a href="/sql-statements/sql-statement-lock-stats.md">ロック統計</a>](/sql-statements/sql-statement-lock-stats.md)
-   [<a href="/sql-statements/sql-statement-show-stats-locked.md">STATS_LOCKEDを表示</a>](/sql-statements/sql-statement-show-stats-locked.md)
