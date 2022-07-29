---
title: Log Redaction
summary: Learn the log redaction in TiDB components.
---

# ログ編集 {#log-redaction}

TiDBが詳細なログ情報を提供すると、機密データ（ユーザーデータなど）がログに出力される可能性があり、データのセキュリティリスクが発生します。このようなリスクを回避するために、各コンポーネント（TiDB、TiKV、およびPD）は、ログ編集がユーザーデータ値を保護できるようにする構成アイテムを提供します。

## TiDB側でのログ編集 {#log-redaction-in-tidb-side}

TiDB側でログ編集を有効にするには、値[`global.tidb_redact_log`](/system-variables.md#tidb_redact_log)を設定し`1` 。この構成値のデフォルトは`0`です。これは、ログの編集が無効になっていることを意味します。

`set`構文を使用して、グローバル変数`tidb_redact_log`を設定できます。

{{< copyable "" >}}

```sql
set @@global.tidb_redact_log=1;
```

設定後、新しいセッションで生成されたすべてのログが編集されます。

```sql
create table t (a int, unique key (a));
Query OK, 0 rows affected (0.00 sec)

insert into t values (1),(1);
ERROR 1062 (23000): Duplicate entry '1' for key 'a'
```

上記の`INSERT`ステートメントのエラーログは次のように出力されます。

```
[2020/10/20 11:45:49.539 +08:00] [INFO] [conn.go:800] ["command dispatched failed"] [conn=5] [connInfo="id:5, addr:127.0.0.1:57222 status:10, collation:utf8_general_ci,  user:root"] [command=Query] [status="inTxn:0, autocommit:1"] [sql="insert into t values ( ? ) , ( ? )"] [txn_mode=OPTIMISTIC] [err="[kv:1062]Duplicate entry '?' for key 'a'"]
```

上記のエラーログから、 `tidb_redact_log`を有効にすると`?`を使用してすべての機密情報が保護されていることがわかります。このようにして、データセキュリティのリスクが回避されます。

## TiKV側でのログ編集 {#log-redaction-in-tikv-side}

TiKV側でログ編集を有効にするには、値[`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-new-in-v408)を設定し`true` 。この構成値のデフォルトは`false`です。これは、ログの編集が無効になっていることを意味します。

## PD側のログ編集 {#log-redaction-in-pd-side}

PD側でログ編集を有効にするには、 [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50)の値を設定し`true` 。この構成値のデフォルトは`false`です。これは、ログの編集が無効になっていることを意味します。

## TiFlash側でのログ編集 {#log-redaction-in-tiflash-side}

TiFlash側でログの編集を有効にするには、tiflash-serverの[`security.redact_info_log`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)の値とtiflash-learnerの[`security.redact-info-log`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)の値の両方を`true`に設定します。両方の構成値のデフォルトは`false`です。これは、ログの編集が無効になっていることを意味します。
