---
title: KILL [TIDB] | TiDB SQL Statement Reference
summary: An overview of the usage of KILL [TIDB] for the TiDB database.
---

# キル[TIDB] {#kill-tidb}

ステートメント`KILL TIDB`は、TiDBの接続を終了するために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
KillStmt ::= KillOrKillTiDB ( 'CONNECTION' | 'QUERY' )? NUM

KillOrKillTiDB ::= 'KILL' 'TIDB'?
```

## 例 {#examples}

```sql
mysql> SHOW PROCESSLIST;
+------+------+-----------+------+---------+------+-------+------------------+
| Id   | User | Host      | db   | Command | Time | State | Info             |
+------+------+-----------+------+---------+------+-------+------------------+
|    1 | root | 127.0.0.1 | test | Query   |    0 | 2     | SHOW PROCESSLIST |
|    2 | root | 127.0.0.1 |      | Sleep   |    4 | 2     |                  |
+------+------+-----------+------+---------+------+-------+------------------+
2 rows in set (0.00 sec)

KILL TIDB 2;
Query OK, 0 rows affected (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

-   設計上、 `KILL`はデフォルトでMySQLと互換性がありません。これにより、ロードバランサーの背後に複数のTiDBサーバーを配置するのが一般的であるため、間違ったTiDBサーバーで接続が終了するのを防ぐことができます。

<CustomContent platform="tidb">

-   クライアントが常に同じTiDBノードに接続されることが確実でない限り、構成ファイルに[`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query)を設定しないでください。これは、デフォルトのMySQLクライアントで<kbd>ctrl</kbd> + <kbd>c</kbd>を押すと、 `KILL`が実行される新しい接続が開くためです。間にプロキシがある場合、新しい接続が別のTiDBノードにルーティングされる可能性があり、これにより別のセッションが強制終了される可能性があります。

</CustomContent>

-   `KILL TIDB`ステートメントはTiDB拡張です。このステートメントの機能は、 `KILL [CONNECTION|QUERY]`コマンドおよびMySQLコマンドラインの<kbd>ctrl</kbd> + <kbd>c</kbd>機能に似ています。同じTiDBノードで`KILL TIDB`を使用しても安全です。

## も参照してください {#see-also}

-   [[完全な]プロセスリストを表示する](/sql-statements/sql-statement-show-processlist.md)
-   [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)
