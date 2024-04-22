---
title: Log Redaction
summary: TiDB、TiKV、PD、およびTiFlashの各コンポーネントは、機密データがログに出力されるリスクを回避するためにログ編集を提供します。TiDBでは`global.tidb_redact_log`を`1`に設定し、TiKV、PD、TiFlashではそれぞれ`security.redact-info-log`を`true`に設定します。これにより、機密情報がシールドされ、データセキュリティのリスクが回避されます。
---

# ログの編集 {#log-redaction}

TiDB が詳細なログ情報を提供する場合、機密データ (ユーザー データなど) がログに出力される可能性があり、これによりデータ セキュリティのリスクが生じます。このようなリスクを回避するために、各コンポーネント(TiDB、TiKV、および PD) は、ユーザー データ値を保護するためのログ編集を可能にする構成アイテムを提供します。

## TiDB 側でのログ編集 {#log-redaction-in-tidb-side}

TiDB 側でログ編集を有効にするには、値[`global.tidb_redact_log`](/system-variables.md#tidb_redact_log)から`1`を設定します。この構成値のデフォルトは`0`で、これはログ編集が無効であることを意味します。

`set`構文を使用してグローバル変数`tidb_redact_log`を設定できます。

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

    [2020/10/20 11:45:49.539 +08:00] [INFO] [conn.go:800] ["command dispatched failed"] [conn=5] [connInfo="id:5, addr:127.0.0.1:57222 status:10, collation:utf8_general_ci,  user:root"] [command=Query] [status="inTxn:0, autocommit:1"] [sql="insert into t values ( ? ) , ( ? )"] [txn_mode=OPTIMISTIC] [err="[kv:1062]Duplicate entry '?' for key 't.a'"]

上記のエラー ログから、 `tidb_redact_log`を有効にした後、 `?`使用してすべての機密情報がシールドされていることがわかります。このようにして、データセキュリティのリスクが回避されます。

## TiKV 側でのログ編集 {#log-redaction-in-tikv-side}

TiKV 側でログ編集を有効にするには、値[`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-new-in-v408)から`true`を設定します。この構成値のデフォルトは`false`で、これはログ編集が無効であることを意味します。

## PD側でのログ編集 {#log-redaction-in-pd-side}

PD 側でログ編集を有効にするには、値[`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50)から`true`を設定します。この構成値のデフォルトは`false`で、これはログ編集が無効であることを意味します。

## TiFlash側でのログ編集 {#log-redaction-in-tiflash-side}

TiFlash側でログ編集を有効にするには、 tflash-server の[`security.redact_info_log`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)値と tflash-learner の[`security.redact-info-log`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)値の両方を`true`に設定します。どちらの構成値もデフォルトで`false`に設定されており、これはログ編集が無効であることを意味します。
