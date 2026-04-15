---
title: ALTER INSTANCE
summary: TiDBにおけるALTER INSTANCE`の使用方法の概要を学びましょう。
---

# インスタンスの変更 {#alter-instance}

`ALTER INSTANCE`ステートメントは、単一の TiDB インスタンスに変更を加えるために使用されます。現在、TiDB は`RELOAD TLS`句のみをサポートしています。

> **注記：**
>
> [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) TLS証明書を自動的に更新できるため、この機能は[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスには適用されません。

## TLSを再読み込みする {#reload-tls}

<CustomContent platform="tidb">

`ALTER INSTANCE RELOAD TLS`ステートメントを実行すると、元の構成パスから証明書 ( [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) )、キー ( [`ssl-key`](/tidb-configuration-file.md#ssl-key) )、および CA ( [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) ) を再読み込みできます。

</CustomContent>

<CustomContent platform="tidb-cloud">

`ALTER INSTANCE RELOAD TLS`ステートメントを実行すると、元の構成パスから証明書 ( [`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert) )、キー ( [`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key) )、および CA ( [`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca) ) を再読み込みできます。

</CustomContent>

新しく読み込まれた証明書、鍵、および認証局は、ステートメントが正常に実行された後に確立される接続に適用されます。このステートメントの実行前に確立された接続には影響しません。

リロード中にエラーが発生した場合、デフォルトではこのエラーメッセージが返され、以前のキーと証明書が引き続き使用されます。ただし、オプションの`NO ROLLBACK ON ERROR`を追加している場合は、リロード中にエラーが発生してもエラーは返されず、以降のリクエストはTLSセキュリティ接続が無効になった状態で処理されます。

## 構文図 {#syntax-diagram}

**AlterInstanceStmt:**

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

## MySQLとの互換性 {#mysql-compatibility}

`ALTER INSTANCE RELOAD TLS`ステートメントは、元の構成パスからの再読み込みのみをサポートします。TiDB の起動時に読み込みパスを動的に変更したり、TLS 暗号化接続機能を動的に有効化したりすることはサポートしていません。この機能は、TiDB を再起動するとデフォルトで無効になります。

## 関連項目 {#see-also}

<CustomContent platform="tidb">

[TiDBクライアントとサーバー間でTLSを有効にする](/enable-tls-between-clients-and-servers.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDBクライアントとサーバー間でTLSを有効にする](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers)。

</CustomContent>
