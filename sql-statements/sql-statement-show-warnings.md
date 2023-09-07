---
title: SHOW WARNINGS | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW WARNINGS for the TiDB database.
---

# 警告を表示 {#show-warnings}

このステートメントは、現在のクライアント接続で以前に実行されたステートメントに対して発生した警告のリストを表示します。 MySQL と同様に、 `sql_mode`どのステートメントがエラーと警告を引き起こすかに大きく影響します。

## あらすじ {#synopsis}

**警告メッセージの表示:**

![ShowWarningsStmt](/media/sqlgram/ShowWarningsStmt.png)

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a INT UNSIGNED);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (0);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT 1/a FROM t1;
+------+
| 1/a  |
+------+
| NULL |
+------+
1 row in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS;
+---------+------+---------------+
| Level   | Code | Message       |
+---------+------+---------------+
| Warning | 1365 | Division by 0 |
+---------+------+---------------+
1 row in set (0.00 sec)

mysql> INSERT INTO t1 VALUES (-1);
ERROR 1264 (22003): Out of range value for column 'a' at row 1
mysql> SELECT * FROM t1;
+------+
| a    |
+------+
|    0 |
+------+
1 row in set (0.00 sec)

mysql> SET sql_mode='';
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (-1);
Query OK, 1 row affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+---------+------+---------------------------+
| Level   | Code | Message                   |
+---------+------+---------------------------+
| Warning | 1690 | constant -1 overflows int |
+---------+------+---------------------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM t1;
+------+
| a    |
+------+
|    0 |
|    0 |
+------+
2 rows in set (0.00 sec)

```

## MySQLの互換性 {#mysql-compatibility}

TiDB の`SHOW WARNINGS`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [エラーを表示](/sql-statements/sql-statement-show-errors.md)
