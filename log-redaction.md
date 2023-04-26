---
title: Log Redaction
summary: Learn the log redaction in TiDB components.
---

# ログ編集 {#log-redaction}

TiDB が詳細なログ情報を提供する場合、機密データ (ユーザー データなど) をログに出力する可能性があり、データ セキュリティ リスクが発生します。このようなリスクを回避するために、各コンポーネント(TiDB、TiKV、および PD) は、ログのリダクションを有効にしてユーザー データの値を保護する構成項目を提供します。

## TiDB 側でのログ編集 {#log-redaction-in-tidb-side}

TiDB 側でログのリダクションを有効にするには、値を[`global.tidb_redact_log`](/system-variables.md#tidb_redact_log)から`1`に設定します。この構成値のデフォルトは`0`です。これは、ログのリダクションが無効であることを意味します。

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
ERROR 1062 (23000): Duplicate entry '1' for key 't.a'
```

上記の`INSERT`ステートメントのエラー ログは次のように出力されます。

```
[2020/10/20 11:45:49.539 +08:00] [INFO] [conn.go:800] ["command dispatched failed"] [conn=5] [connInfo="id:5, addr:127.0.0.1:57222 status:10, collation:utf8_general_ci,  user:root"] [command=Query] [status="inTxn:0, autocommit:1"] [sql="insert into t values ( ? ) , ( ? )"] [txn_mode=OPTIMISTIC] [err="[kv:1062]Duplicate entry '?' for key 't.a'"]
```

上記のエラー ログから、すべての機密情報が`?`使用してシールドされ、 `tidb_redact_log`が有効になっていることがわかります。このようにして、データセキュリティのリスクが回避されます。

## TiKV 側でのログ編集 {#log-redaction-in-tikv-side}

TiKV 側でログのリダクションを有効にするには、値を[`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-new-in-v408)から`true`に設定します。この構成値のデフォルトは`false`です。これは、ログのリダクションが無効であることを意味します。

## PD 側でのログ編集 {#log-redaction-in-pd-side}

PD 側でログのリダクションを有効にするには、値を[`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50)から`true`に設定します。この構成値のデフォルトは`false`です。これは、ログのリダクションが無効であることを意味します。

## TiFlash側のログ編集 {#log-redaction-in-tiflash-side}

TiFlash側でログのリダクションを有効にするには、tiflash-server の[`security.redact_info_log`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)値と tiflash-learner の[`security.redact-info-log`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)値の両方を`true`に設定します。両方の構成値のデフォルトは`false`です。これは、ログのリダクションが無効になっていることを意味します。
