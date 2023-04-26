---
title: ALTER INSTANCE
summary: Learn the overview of the `ALTER INSTANCE` usage in TiDB.
---

# インスタンスの変更 {#alter-instance}

`ALTER INSTANCE`ステートメントは、単一の TiDB インスタンスに変更を加えるために使用されます。現在、TiDB は`RELOAD TLS`句のみをサポートしています。

## TLS のリロード {#reload-tls}

`ALTER INSTANCE RELOAD TLS`ステートメントを実行して、元の構成パスから証明書 ( [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) )、キー ( [`ssl-key`](/tidb-configuration-file.md#ssl-key) )、および CA ( [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) ) をリロードできます。

新しくロードされた証明書、キー、および CA は、ステートメントが正常に実行された後に確立された接続で有効になります。このステートメントの実行前に確立された接続は影響を受けません。

リロード中にエラーが発生すると、デフォルトでは、このエラー メッセージが返され、以前のキーと証明書が引き続き使用されます。ただし、オプションの`NO ROLLBACK ON ERROR`追加した場合、リロード中にエラーが発生した場合、エラーは返されず、後続のリクエストは TLS セキュリティ接続を無効にして処理されます。

## 構文図 {#syntax-diagram}

**AlterInstanceStmt:**

```ebnf+diagram
AlterInstanceStmt ::=
    'ALTER' 'INSTANCE' InstanceOption

InstanceOption ::=
    'RELOAD' 'TLS' ('NO' 'ROLLBACK' 'ON' 'ERROR')?
```

## 例 {#example}

{{< copyable "" >}}

```sql
ALTER INSTANCE RELOAD TLS;
```

## MySQL の互換性 {#mysql-compatibility}

`ALTER INSTANCE RELOAD TLS`ステートメントは、元の構成パスからの再読み込みのみをサポートします。 TiDB の起動時に、読み込みパスを動的に変更したり、TLS 暗号化接続機能を動的に有効にしたりすることはサポートされていません。 TiDB を再起動すると、この機能はデフォルトで無効になります。

## こちらもご覧ください {#see-also}

[TiDB クライアントとサーバー間で TLS を有効にする](/enable-tls-between-clients-and-servers.md) .
