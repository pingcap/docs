---
title: KILL
summary: An overview of the usage of KILL for the TiDB database.
---

# 殺す {#kill}

`KILL`ステートメントは、現在の TiDB クラスター内の任意の TiDB インスタンスで接続を終了するために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
KillStmt ::= 'KILL' 'TIDB'? ( 'CONNECTION' | 'QUERY' )? CONNECTION_ID
```

## 例 {#examples}

次の例は、現在のクラスター内のすべてのアクティブなクエリを取得し、それらのいずれかを終了する方法を示しています。

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

## MySQL の互換性 {#mysql-compatibility}

-   MySQL の`KILL`ステートメントは、現在接続されている MySQL インスタンスでのみ接続を終了できますが、TiDB の`KILL`ステートメントは、クラスター全体の任意の TiDB インスタンスで接続を終了できます。
-   現在、MySQL コマンド ライン<kbd>ctrl</kbd> + <kbd>c</kbd>を使用して TiDB でクエリまたは接続を終了することはサポートされていません。

## 動作変更の説明 {#behavior-change-descriptions}

<CustomContent platform="tidb">

v6.1.0 以降、TiDB は Global Kill 機能をサポートします。これはデフォルトで有効になり、 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)構成によって制御されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

v6.1.0 以降、TiDB はデフォルトで有効になっている Global Kill 機能をサポートしています。

</CustomContent>

Global Kill 機能が有効になっている場合、 `KILL`と`KILL TIDB`ステートメントの両方でインスタンス全体のクエリまたは接続を終了できるため、クエリまたは接続を誤って終了することを心配する必要はありません。クライアントを使用して任意の TiDB インスタンスに接続し、 `KILL`または`KILL TIDB`ステートメントを実行すると、ステートメントはターゲットの TiDB インスタンスに転送されます。クライアントと TiDB クラスターの間にプロキシがある場合、 `KILL`ステートメントと`KILL TIDB`ステートメントも実行のためにターゲット TiDB インスタンスに転送されます。

Global Kill 機能が有効になっていない場合、または v6.1.0 より前のバージョンの TiDB を使用している場合は、次の点に注意してください。

-   デフォルトでは、 `KILL` MySQL と互換性がありません。ロードサーバーの背後に複数の TiDB サーバーを配置するのが一般的であるため、これにより、接続が間違った TiDB サーバーによって終了されるケースを防ぐことができます。現在接続されている TiDB インスタンスで他の接続を終了するには、 `KILL TIDB`ステートメントを実行して`TIDB`サフィックスを明示的に追加する必要があります。

<CustomContent platform="tidb">

-   クライアントが常に同じ TiDB インスタンスに接続されることが確実でない限り、構成ファイルに[`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query)を設定することは**強く推奨されません**。これは、デフォルトの MySQL クライアントで<kbd>ctrl</kbd> + <kbd>c</kbd>を押すと、 `KILL`が実行される新しい接続が開かれるためです。クライアントと TiDB クラスターの間にプロキシがある場合、新しい接続が別の TiDB インスタンスにルーティングされる可能性があり、誤って別のセッションを強制終了する可能性があります。

</CustomContent>

-   `KILL TIDB`ステートメントは TiDB 拡張機能です。このステートメントの機能は、MySQL `KILL [CONNECTION|QUERY]`コマンドおよび MySQL コマンド ライン<kbd>ctrl</kbd> + <kbd>c</kbd>に似ています。同じ TiDB インスタンスで`KILL TIDB`使用しても安全です。

## こちらもご覧ください {#see-also}

-   [[FULL] プロセスリストを表示](/sql-statements/sql-statement-show-processlist.md)
-   [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)
