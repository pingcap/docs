---
title: KILL
summary: An overview of the usage of KILL for the TiDB database.
---

# 殺す {#kill}

`KILL`ステートメントは、現在のTiDBクラスタの任意のTiDBインスタンスの接続を終了するために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
KillStmt ::= 'KILL' 'TIDB'? ( 'CONNECTION' | 'QUERY' )? CONNECTION_ID
```

## 例 {#examples}

次の例は、現在のクラスタのすべてのアクティブなクエリを取得し、それらのいずれかを終了する方法を示しています。

{{< copyable "" >}}

```sql
SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST;
```

```
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
| ID                  | USER | INSTANCE        | INFO                                                                        |
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
| 8306449708033769879 | root | 127.0.0.1:10082 | select sleep(30), 'foo'                                                     |
| 5857102839209263511 | root | 127.0.0.1:10080 | select sleep(50)                                                            |
| 5857102839209263513 | root | 127.0.0.1:10080 | SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST |
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
```

{{< copyable "" >}}

```sql
KILL 5857102839209263511;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

-   MySQLの`KILL`ステートメントは、現在接続されているMySQLインスタンスの接続のみを終了できますが、TiDBの`KILL`ステートメントは、クラスタ全体の任意のTiDBインスタンスの接続を終了できます。
-   現在、MySQLコマンドライン<kbd>ctrl</kbd> + <kbd>c</kbd>を使用してTiDBでクエリまたは接続を終了することはサポートされていません。

## 動作変更の説明 {#behavior-change-descriptions}

<CustomContent platform="tidb">

v6.1.0以降、TiDBはグローバルキル機能をサポートします。この機能はデフォルトで有効になっており、 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)構成で制御されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

v6.1.0以降、TiDBはグローバルキル機能をサポートします。これはデフォルトで有効になっています。

</CustomContent>

グローバルキル機能が有効になっている場合、 `KILL`ステートメントと`KILL TIDB`ステートメントの両方でインスタンス間のクエリまたは接続を終了できるため、クエリまたは接続を誤って終了することを心配する必要はありません。クライアントを使用して任意のTiDBインスタンスに接続し、 `KILL`または`KILL TIDB`ステートメントを実行すると、ステートメントはターゲットTiDBインスタンスに転送されます。クライアントとTiDBクラスタの間にプロキシがある場合、 `KILL`ステートメントと`KILL TIDB`ステートメントも実行のためにターゲットTiDBインスタンスに転送されます。

グローバルキル機能が有効になっていない場合、またはv6.1.0より前のバージョンのTiDBを使用している場合は、次の点に注意してください。

-   デフォルトでは、 `KILL`はMySQLと互換性がありません。これは、ロードバランサーの背後に複数のTiDBサーバーを配置するのが一般的であるため、間違ったTiDBサーバーによって接続が終了するケースを防ぐのに役立ちます。現在接続されているTiDBインスタンスで他の接続を終了するには、 `KILL TIDB`ステートメントを実行して`TIDB`サフィックスを明示的に追加する必要があります。

<CustomContent platform="tidb">

-   クライアントが常に同じ**TiDB**インスタンスに接続されることが確実でない限り、構成ファイルに[`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query)を設定することは強くお勧めしません。これは、デフォルトのMySQLクライアントで<kbd>ctrl</kbd> + <kbd>c</kbd>を押すと、 `KILL`が実行される新しい接続が開くためです。クライアントとTiDBクラスタの間にプロキシがある場合、新しい接続が別のTiDBインスタンスにルーティングされる可能性があり、誤って別のセッションが強制終了される可能性があります。

</CustomContent>

-   `KILL TIDB`ステートメントはTiDB拡張です。このステートメントの機能は、 `KILL [CONNECTION|QUERY]`コマンドおよびMySQLコマンドライン<kbd>ctrl</kbd> + <kbd>c</kbd>に似ています。同じTiDBインスタンスで`KILL TIDB`を使用しても安全です。

## も参照してください {#see-also}

-   [[フル]プロセスリストを表示](/sql-statements/sql-statement-show-processlist.md)
-   [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)
