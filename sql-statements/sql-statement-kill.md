---
title: KILL
summary: An overview of the usage of KILL for the TiDB database.
---

# 殺す {#kill}

`KILL`ステートメントは、現在の TiDB クラスター内の任意の TiDB インスタンスの接続を終了するために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
KillStmt ::= 'KILL' 'TIDB'? ( 'CONNECTION' | 'QUERY' )? CONNECTION_ID
```

## 例 {#examples}

次の例は、現在のクラスター内のすべてのアクティブなクエリを取得し、それらのいずれかを終了する方法を示しています。

```sql
SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST;
```

    +---------------------+------+-----------------+-----------------------------------------------------------------------------+
    | ID                  | USER | INSTANCE        | INFO                                                                        |
    +---------------------+------+-----------------+-----------------------------------------------------------------------------+
    | 8306449708033769879 | root | 127.0.0.1:10082 | select sleep(30), 'foo'                                                     |
    | 5857102839209263511 | root | 127.0.0.1:10080 | select sleep(50)                                                            |
    | 5857102839209263513 | root | 127.0.0.1:10080 | SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST |
    +---------------------+------+-----------------+-----------------------------------------------------------------------------+

```sql
KILL 5857102839209263511;
```

    Query OK, 0 rows affected (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

-   MySQL の`KILL`ステートメントは、現在接続されている MySQL インスタンス内の接続のみを終了できますが、TiDB の`KILL`ステートメントは、クラスター全体の任意の TiDB インスタンス内の接続を終了できます。
-   v7.2.0 以前のバージョンでは、MySQL コマンド ライン<kbd>Control+C</kbd>を使用して TiDB でのクエリまたは接続を終了することはサポートされていません。

## 行動変化の説明 {#behavior-change-descriptions}

<CustomContent platform="tidb">

v7.3.0 以降、TiDB は 32 ビット接続 ID の生成をサポートします。これはデフォルトで有効になり、 [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730)構成項目によって制御されます。 Global Kill 機能と 32 ビット接続 ID の両方が有効になっている場合、TiDB は 32 ビット接続 ID を生成し、MySQL コマンドラインで<kbd>Control+C</kbd>を使用してクエリまたは接続を終了できます。

> **警告：**
>
> クラスター内の TiDB インスタンスの数が 2048 を超えるか、単一 TiDB インスタンスの同時接続数が 1048576 を超えると、32 ビットの接続 ID スペースが不足し、自動的に 64 ビットの接続 ID にアップグレードされます。アップグレード プロセス中、既存のビジネスおよび確立された接続は影響を受けません。ただし、MySQL コマンドラインで<kbd>Control+C</kbd>を使用して後続の新しい接続を終了することはできません。

v6.1.0 以降、TiDB は Global Kill 機能をサポートします。この機能はデフォルトで有効になり、 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)構成によって制御されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

v7.3.0 以降、TiDB は 32 ビット接続 ID の生成をサポートしており、これはデフォルトで有効になっています。 Global Kill 機能と 32 ビット接続 ID の両方が有効になっている場合は、MySQL コマンドラインで<kbd>Control+C</kbd>を使用してクエリまたは接続を終了できます。

v6.1.0 以降、TiDB は Global Kill 機能をサポートしており、これはデフォルトで有効になっています。

</CustomContent>

Global Kill 機能が有効になっている場合、 `KILL`と`KILL TIDB`ステートメントの両方でインスタンス全体のクエリまたは接続を終了できるため、クエリまたは接続が誤って終了することを心配する必要はありません。クライアントを使用して任意の TiDB インスタンスに接続し、 `KILL`または`KILL TIDB`ステートメントを実行すると、ステートメントはターゲット TiDB インスタンスに転送されます。クライアントと TiDB クラスターの間にプロキシがある場合、 `KILL`および`KILL TIDB`ステートメントも実行のためにターゲット TiDB インスタンスに転送されます。

Global Kill 機能が有効になっていない場合、または v6.1.0 より前の TiDB バージョンを使用している場合は、次の点に注意してください。

-   デフォルトでは、 `KILL` MySQL と互換性がありません。これは、ロード バランサの背後に複数の TiDB サーバーを配置するのが一般的であるため、接続が間違った TiDBサーバーによって終了される事態を防ぐのに役立ちます。現在接続されている TiDB インスタンス上の他の接続を終了するには、 `KILL TIDB`ステートメントを実行して明示的に`TIDB`サフィックスを追加する必要があります。

<CustomContent platform="tidb">

-   クライアントが常に同じ TiDB インスタンスに接続されることが確実でない限り、構成ファイルで[`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query)を設定することは**強く推奨されません**。これは、デフォルトの MySQL クライアントで<kbd>Control+C</kbd>を押すと、 `KILL`が実行される新しい接続が開かれるためです。クライアントと TiDB クラスターの間にプロキシがある場合、新しい接続が別の TiDB インスタンスにルーティングされる可能性があり、これにより誤って別のセッションが強制終了される可能性があります。

</CustomContent>

-   `KILL TIDB`ステートメントは TiDB 拡張機能です。このステートメントの機能は、MySQL `KILL [CONNECTION|QUERY]`コマンドおよび MySQL コマンド ライン<kbd>Control+C</kbd>に似ています。同じ TiDB インスタンスで`KILL TIDB`を使用しても安全です。

## こちらも参照 {#see-also}

-   [[完全な] プロセスリストを表示](/sql-statements/sql-statement-show-processlist.md)
-   [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)
