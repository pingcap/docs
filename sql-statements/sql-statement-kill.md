---
title: KILL
summary: TiDB データベースに対する KILL の使用法の概要。
---

# 殺す {#kill}

`KILL`文は、現在の TiDB クラスタ内の任意の TiDB インスタンスへの接続を終了するために使用されます。TiDB v6.2.0 以降では、 `KILL`文を使用して実行中の DDL ジョブを終了することもできます。

## 概要 {#synopsis}

```ebnf+diagram
KillStmt ::= 'KILL' 'TIDB'? ( 'CONNECTION' | 'QUERY' )? CONNECTION_ID
```

## 例 {#examples}

次の例は、現在のクラスター内のすべてのアクティブなクエリを取得し、そのうちの 1 つを終了する方法を示しています。

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

-   MySQL の`KILL`文は現在接続されている MySQL インスタンス内の接続のみを終了できますが、TiDB の`KILL`文はクラスター全体の任意の TiDB インスタンス内の接続を終了できます。
-   v7.2.0 以前のバージョンでは、MySQL コマンドラインの<kbd>Control+C</kbd>を使用して TiDB 内のクエリまたは接続を終了することはサポートされていません。

## 行動変化の説明 {#behavior-change-descriptions}

<CustomContent platform="tidb">

v7.3.0以降、TiDBは32ビット接続IDの生成をサポートしています。これはデフォルトで有効になっており、 [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730)設定項目で制御されます。Global Kill機能と32ビット接続IDの両方を有効にすると、TiDBは32ビット接続IDを生成し、MySQLコマンドラインで<kbd>Control+C</kbd>を使用してクエリまたは接続を終了できます。

> **警告：**
>
> クラスタ内のTiDBインスタンス数が2048を超えるか、単一のTiDBインスタンスの同時接続数が1048576を超えると、32ビット接続IDの容量が不足するため、自動的に64ビット接続IDにアップグレードされます。アップグレードプロセス中、既存のビジネス接続および確立済みの接続は影響を受けません。ただし、それ以降の新規接続は、MySQLコマンドラインで<kbd>Control+C</kbd>を使用して終了することはできません。

v6.1.0 以降、TiDB は Global Kill 機能をサポートしています。この機能はデフォルトで有効になっており、 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)構成によって制御されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB v7.3.0以降、32ビット接続IDの生成がサポートされ、デフォルトで有効になっています。Global Kill機能と32ビット接続IDの両方が有効になっている場合、MySQLコマンドラインで<kbd>Control+C</kbd>を使用してクエリまたは接続を終了できます。

v6.1.0 以降、TiDB は Global Kill 機能をサポートしており、これはデフォルトで有効になっています。

</CustomContent>

Global Kill機能を有効にすると、 `KILL`と`KILL TIDB`両方のステートメントでインスタンス間のクエリまたは接続を終了できるため、クエリや接続が誤って終了してしまう心配はありません。クライアントを使用して任意のTiDBインスタンスに接続し、 `KILL`または`KILL TIDB`ステートメントを実行すると、ステートメントは対象のTiDBインスタンスに転送されます。クライアントとTiDBクラスタの間にプロキシが存在する場合、 `KILL`と`KILL TIDB`ステートメントも対象のTiDBインスタンスに転送され、実行されます。

Global Kill 機能が有効になっていない場合、または v6.1.0 より前のバージョンの TiDB を使用している場合は、次の点に注意してください。

-   デフォルトでは、 `KILL` MySQL と互換性がありません。これは、ロードバランサーの背後に複数の TiDB サーバーを配置することが一般的であるため、誤った TiDBサーバーによって接続が切断される事態を防ぐのに役立ちます。現在接続中の TiDB インスタンス上の他の接続を切断するには、 `KILL TIDB`ステートメントを実行して明示的に`TIDB`サフィックスを追加する必要があります。

<CustomContent platform="tidb">

-   クライアントが常に同じTiDBインスタンスに接続されることが確実でない限り、設定ファイルで[`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query)設定することは**強く推奨されません**。これは、デフォルトのMySQLクライアントで<kbd>Control+C</kbd>を押すと、新しい接続が開かれ、その中で`KILL`実行されるためです。クライアントとTiDBクラスタの間にプロキシが存在する場合、新しい接続が別のTiDBインスタンスにルーティングされ、誤って別のセッションが強制終了される可能性があります。

</CustomContent>

-   `KILL TIDB`文はTiDBの拡張機能です。この文の機能は、MySQL `KILL [CONNECTION|QUERY]`コマンドおよびMySQLコマンドラインの<kbd>Control+C</kbd>に似ています。同じTiDBインスタンスで`KILL TIDB`安全に使用できます。

## 参照 {#see-also}

-   [プロセスリストを[完全]表示](/sql-statements/sql-statement-show-processlist.md)
-   [クラスタープロセスリスト](/information-schema/information-schema-processlist.md#cluster_processlist)
