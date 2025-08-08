---
title: SHOW [FULL] PROCESSLIST | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW [FULL] PROCESSLIST の使用法の概要。
---

# プロセスリストを[完全]表示 {#show-full-processlist}

このステートメントは、同じTiDBサーバーに接続されている現在のセッションを一覧表示します。1列目`Info`はクエリテキストが含まれますが、オプションのキーワード`FULL`が指定されていない限り、切り捨てられます。

## 概要 {#synopsis}

```ebnf+diagram
ShowProcesslistStmt ::=
    "SHOW" "FULL"? "PROCESSLIST"
```

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

-   TiDBの`State`列目は説明的ではありません。クエリは並列に実行され、各ゴルーチンは常に異なる状態を持つため、状態を単一の値として表現することはTiDBではより複雑です。

## 参照 {#see-also}

-   [キル [TIDB]](/sql-statements/sql-statement-kill.md)
-   [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)
