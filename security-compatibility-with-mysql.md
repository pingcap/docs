---
title: Security Compatibility with MySQL
summary: Learn TiDB's security compatibilities with MySQL.
---

# MySQL とのセキュリティの互換性 {#security-compatibility-with-mysql}

TiDB はMySQL 5.7と同様のセキュリティ機能をサポートしていますが、次の例外があります。

-   カラムレベルの権限はサポートされていません
-   パスワードの有効期限、パスワードの最終変更の追跡、およびパスワードの有効期間はサポートされていません[#9709](https://github.com/pingcap/tidb/issues/9709)
-   許可属性`max_questions` 、 `max_updated` 、 `max_connections` 、 `max_user_connections`はサポートされていません
-   パスワード検証は現在サポートされていません[#9741](https://github.com/pingcap/tidb/issues/9741)

## 認証プラグインのステータス {#authentication-plugin-status}

TiDB は複数の認証方法をサポートしています。これらのメソッドは、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)および[`ALTER USER`](/sql-statements/sql-statement-create-user.md)を使用してユーザーごとに指定できます。これらのメソッドは、同じ名前の MySQL の認証メソッドと互換性があります。

次の表でサポートされている認証方法のいずれかを使用できます。クライアント/サーバー接続が確立されているときにサーバーがアドバタイズするデフォルトの方法を指定するには、 [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)変数を設定します。 `tidb_sm3_password`は、TiDB でのみサポートされている SM3 認証方式です。したがって、この方法を使用して認証するには、 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)を使用して TiDB に接続する必要があります。

<CustomContent platform="tidb">

TLS 認証のサポートの構成は異なります。詳細については、 [TiDB クライアントとサーバー間の TLS を有効にする](/enable-tls-between-clients-and-servers.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TLS 認証のサポートの構成は異なります。詳細については、 [TiDB クライアントとサーバー間の TLS を有効にする](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers)を参照してください。

</CustomContent>

| 認証方法                    | 対応          |
| :---------------------- | :---------- |
| `mysql_native_password` | はい          |
| `sha256_password`       | いいえ         |
| `caching_sha2_password` | はい、5.2.0 以降 |
| `auth_socket`           | はい、5.3.0 以降 |
| `tidb_sm3_password`     | はい、6.3.0 以降 |
| TLS 証明書                 | はい          |
| LDAP                    | いいえ         |
| パム                      | いいえ         |
| ed25519 (マリアDB)         | いいえ         |
| GSSAPI (MariaDB)        | いいえ         |
| ファイド                    | いいえ         |
