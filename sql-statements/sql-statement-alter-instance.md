---
title: ALTER INSTANCE
summary: TiDB での ALTER INSTANCE` の使用法の概要を学習します。
---

# インスタンスの変更 {#alter-instance}

`ALTER INSTANCE`文は、単一の TiDB インスタンスに変更を加えるために使用されます。現在、TiDB は`RELOAD TLS`句のみをサポートしています。

> **注記：**
>
> [{{{ .スターター }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) TLS 証明書を自動的に更新できるため、この機能は[{{{ .スターター }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターには適用されません。

## TLSをリロード {#reload-tls}

<CustomContent platform="tidb">

`ALTER INSTANCE RELOAD TLS`ステートメントを実行すると、証明書 ( [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) )、キー ( [`ssl-key`](/tidb-configuration-file.md#ssl-key) )、および CA ( [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) ) を元の構成パスから再ロードできます。

</CustomContent>

<CustomContent platform="tidb-cloud">

`ALTER INSTANCE RELOAD TLS`ステートメントを実行すると、証明書 ( [`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert) )、キー ( [`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key) )、および CA ( [`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca) ) を元の構成パスから再ロードできます。

</CustomContent>

新しくロードされた証明書、鍵、およびCAは、ステートメントが正常に実行された後に確立された接続に対して有効になります。このステートメントの実行前に確立された接続には影響しません。

再読み込み中にエラーが発生した場合、デフォルトではこのエラーメッセージが返され、以前の鍵と証明書が引き続き使用されます。ただし、オプションの`NO ROLLBACK ON ERROR`追加した場合、再読み込み中にエラーが発生してもエラーは返されず、以降のリクエストはTLSセキュリティ接続が無効になった状態で処理されます。

## 構文図 {#syntax-diagram}

**インスタンスステートメントの変更:**

```ebnf+diagram
AlterInstanceStmt ::=
    'ALTER' 'INSTANCE' InstanceOption

InstanceOption ::=
    'RELOAD' 'TLS' ('NO' 'ROLLBACK' 'ON' 'ERROR')?
```

## 例 {#example}

```sql
ALTER INSTANCE RELOAD TLS;
```

## MySQLの互換性 {#mysql-compatibility}

`ALTER INSTANCE RELOAD TLS`文は、元の設定パスからの再ロードのみをサポートします。ロードパスの動的な変更や、TiDB 起動時の TLS 暗号化接続機能の動的な有効化はサポートしていません。この機能は、TiDB の再起動時にデフォルトで無効になります。

## 参照 {#see-also}

<CustomContent platform="tidb">

[TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md) 。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDBクライアントとサーバー間のTLSを有効にする](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers) 。

</CustomContent>
