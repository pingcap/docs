---
title: ALTER INSTANCE
summary: Learn the overview of the `ALTER INSTANCE` usage in TiDB.
---

# ALTER INSTANCE {#alter-instance}

`ALTER INSTANCE`ステートメントは、単一のTiDBインスタンスに変更を加えるために使用されます。現在、TiDBは`RELOAD TLS`句のみをサポートしています。

## TLSをリロード {#reload-tls}

`ALTER INSTANCE RELOAD TLS`ステートメントを実行して、元の構成パスから証明書（ [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) ）、キー（ [`ssl-key`](/tidb-configuration-file.md#ssl-key) ）、およびCA（ [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) ）を再ロードできます。

新しくロードされた証明書、キー、およびCAは、ステートメントが正常に実行された後に確立された接続で有効になります。このステートメントの実行前に確立された接続は影響を受けません。

リロード中にエラーが発生すると、デフォルトでこのエラーメッセージが返され、以前のキーと証明書が引き続き使用されます。ただし、オプションの`NO ROLLBACK ON ERROR`を追加した場合、リロード中にエラーが発生した場合、エラーは返されず、後続のリクエストはTLSセキュリティ接続を無効にして処理されます。

## シンタックスダイアグラム {#syntax-diagram}

**AlterInstanceStmt：**

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

## MySQLの互換性 {#mysql-compatibility}

`ALTER INSTANCE RELOAD TLS`ステートメントは、元の構成パスからのリロードのみをサポートします。 TiDBの起動時に、読み込みパスを動的に変更したり、TLS暗号化接続機能を動的に有効にしたりすることはサポートされていません。 TiDBを再起動すると、この機能はデフォルトで無効になります。

## も参照してください {#see-also}

[TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md) 。
