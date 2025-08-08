---
title: Log Redaction
summary: TiDB コンポーネントでのログ編集について学習します。
---

# ログ編集 {#log-redaction}

TiDBが詳細なログ情報を提供する場合、ログに機密データ（ユーザーデータなど）が出力される可能性があり、データセキュリティリスクが発生します。このようなリスクを回避するため、各コンポーネント（TiDB、TiKV、PD）には、ユーザーデータ値を保護するためのログ編集を有効にする設定項目が用意されています。

## TiDB側でのログ編集 {#log-redaction-in-tidb-side}

TiDB側でログ編集を有効にするには、 [`global.tidb_redact_log`](/system-variables.md#tidb_redact_log) `ON`または`MARKER`に設定します。この設定値のデフォルトは`OFF`で、ログ編集が無効であることを意味します。

`set`構文を使用してグローバル変数`tidb_redact_log`設定できます。

```sql
set @@global.tidb_redact_log = ON;
```

設定後、新しいセッションで生成されたすべてのログが編集されます。

```sql
create table t (a int, unique key (a));
Query OK, 0 rows affected (0.00 sec)

insert into t values (1),(1);
ERROR 1062 (23000): Duplicate entry '1' for key 't.a'
```

上記の`INSERT`ステートメントのエラー ログは次のように出力されます。

    [2024/07/02 11:35:32.686 +08:00] [INFO] [conn.go:1146] ["command dispatched failed"] [conn=1482686470] [session_alias=] [connInfo="id:1482686470, addr:127.0.0.1:52258 status:10, collation:utf8mb4_0900_ai_ci, user:root"] [command=Query] [status="inTxn:0, autocommit:1"] [sql="insert into `t` values ( ... )"] [txn_mode=PESSIMISTIC] [timestamp=450859193514065921] [err="[kv:1062]Duplicate entry '?' for key 't.a'"]

上記のエラー ログから、値`tidb_redact_log`が`ON`に設定されると、データ セキュリティ リスクを回避するために、機密情報が TiDB ログで`?`マークに置き換えられることがわかります。

さらに、TiDBには`MARKER`オプションが用意されています。3 `tidb_redact_log`値を`MARKER`に設定すると、TiDBはログ内の機密情報を直接置き換えるのではなく、 `‹›`でマークするため、編集ルールをカスタマイズできます。

```sql
set @@global.tidb_redact_log = MARKER;
```

上記の構成の後、新しいセッションによって生成されるすべてのログで機密情報が置き換えられるのではなく、マークされます。

```sql
create table t (a int, unique key (a));
Query OK, 0 rows affected (0.07 sec)

insert into t values (1),(1);
ERROR 1062 (23000): Duplicate entry '‹1›' for key 't.a'
```

エラーログは次のとおりです。

    [2024/07/02 11:35:01.426 +08:00] [INFO] [conn.go:1146] ["command dispatched failed"] [conn=1482686470] [session_alias=] [connInfo="id:1482686470, addr:127.0.0.1:52258 status:10, collation:utf8mb4_0900_ai_ci, user:root"] [command=Query] [status="inTxn:0, autocommit:1"] [sql="insert into `t` values ( ‹1› ) , ( ‹1› )"] [txn_mode=PESSIMISTIC] [timestamp=450859185309483010] [err="[kv:1062]Duplicate entry '‹1›' for key 't.a'"]

上記のエラーログからわかるように、 `tidb_redact_log`を`MARKER`に設定すると、TiDB はログ内で機密情報を`‹ ›`でマークします。必要に応じて、ログ内の機密情報を処理するための編集ルールをカスタマイズできます。

## TiKV側でのログ編集 {#log-redaction-in-tikv-side}

TiKV側でログ編集を有効にするには、 [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-new-in-v408) `true`または`"marker"`に設定します。この設定値のデフォルトは`false`で、ログ編集が無効であることを意味します。

## PD側でのログ編集 {#log-redaction-in-pd-side}

PD側でログ編集を有効にするには、 [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50)を`true`または`"marker"`に設定します。この設定値のデフォルトは`false`で、ログ編集が無効であることを意味します。

## TiFlash側でのログ編集 {#log-redaction-in-tiflash-side}

TiFlash側でログ編集を有効にするには、tiflash-serverの[`security.redact_info_log`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)値とtiflash-learnerの[`security.redact-info-log`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)値の両方を`true`または`"marker"`に設定します。両方の設定値はデフォルトで`false`に設定されており、ログ編集が無効になっていることを意味します。
