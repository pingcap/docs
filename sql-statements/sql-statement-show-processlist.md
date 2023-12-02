---
title: SHOW [FULL] PROCESSLIST | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [FULL] PROCESSLIST for the TiDB database.
---

# [完全な] プロセスリストを表示 {#show-full-processlist}

このステートメントは、同じ TiDBサーバーに接続されている現在のセッションをリストします。 `Info`列にはクエリ テキストが含まれますが、オプションのキーワード`FULL`が指定されない限り、クエリ テキストは切り詰められます。

## あらすじ {#synopsis}

**ShowProcesslistStmt:**

![ShowProcesslistStmt](/media/sqlgram/ShowProcesslistStmt.png)

**オプトフル:**

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

## MySQLの互換性 {#mysql-compatibility}

-   TiDB の`State`列は説明的ではありません。 TiDB では、クエリが並行して実行され、各ゴルーチンが常に異なる状態になるため、状態を単一の値として表すことはより複雑になります。

## こちらも参照 {#see-also}

-   [[TIDB]を殺す](/sql-statements/sql-statement-kill.md)
