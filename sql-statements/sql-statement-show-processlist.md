---
title: SHOW [FULL] PROCESSLIST | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW [FULL] PROCESSLIST の使用法の概要。
---

# [フル]プロセスリストを表示 {#show-full-processlist}

このステートメントは、同じ TiDBサーバーに接続されている現在のセッションを一覧表示します。1 列にはクエリ テキストが含まれますが、オプションのキーワード`FULL`が指定`Info`れていない限り切り捨てられます。

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

## MySQL 互換性 {#mysql-compatibility}

-   TiDB の`State`列目は説明的ではありません。クエリが並列で実行され、各ゴルーチンが常に異なる状態になるため、状態を単一の値として表すのは TiDB ではより複雑になります。

## 参照 {#see-also}

-   [殺す [TIDB]](/sql-statements/sql-statement-kill.md)
-   [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)
