---
title: SHOW [FULL] PROCESSLIST | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [FULL] PROCESSLIST for the TiDB database.
---

# [完全な]プロセスリストを表示する {#show-full-processlist}

このステートメントは、同じTiDBサーバーに接続されている現在のセッションを一覧表示します。 `Info`列にはクエリテキストが含まれ、オプションのキーワード`FULL`が指定されていない限り切り捨てられます。

## あらすじ {#synopsis}

**ShowProcesslistStmt：**

![ShowProcesslistStmt](/media/sqlgram/ShowProcesslistStmt.png)

**OptFull：**

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

-   TiDBの`State`列は説明的ではありません。クエリは並行して実行され、各ゴルーチンは常に異なる状態になるため、TiDBでは状態を単一の値として表すことはより複雑です。

## も参照してください {#see-also}

-   [キル[TIDB]](/sql-statements/sql-statement-kill.md)
