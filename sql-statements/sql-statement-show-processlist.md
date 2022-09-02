---
title: SHOW [FULL] PROCESSLIST | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [FULL] PROCESSLIST for the TiDB database.
---

# [FULL] プロセスリストを表示 {#show-full-processlist}

このステートメントは、同じ TiDBサーバーに接続されている現在のセッションを一覧表示します。 `Info`列には、オプションのキーワード`FULL`が指定されていない限り切り捨てられるクエリ テキストが含まれます。

## あらすじ {#synopsis}

**ShowProcesslistStmt:**

![ShowProcesslistStmt](/media/sqlgram/ShowProcesslistStmt.png)

**OptFull:**

![OptFull](/media/sqlgram/OptFull.png)

## 例 {#examples}

```sql
mysql> SHOW PROCESSLIST;
+------+------+-----------------+------+---------+------+------------+------------------+
| Id   | User | Host            | db   | Command | Time | State      | Info             |
+------+------+-----------------+------+---------+------+------------+------------------+
|    5 | root | 127.0.0.1:45970 | test | Query   |    0 | autocommit | SHOW PROCESSLIST |
+------+------+-----------------+------+---------+------+------------+------------------+
1 rows in set (0.00 sec)
```

## MySQL の互換性 {#mysql-compatibility}

-   TiDB の`State`列は説明的ではありません。 TiDB では状態を単一の値として表現するのはより複雑です。これは、クエリが並行して実行され、各ゴルーチンが常に異なる状態になるためです。

## こちらもご覧ください {#see-also}

-   [キル [TIDB]](/sql-statements/sql-statement-kill.md)
