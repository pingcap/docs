---
title: Security Compatibility with MySQL
summary: Learn TiDB's security compatibilities with MySQL.
---

# MySQLとのセキュリティの互換性 {#security-compatibility-with-mysql}

TiDBは、次の例外を除いて、 MySQL 5.7と同様のセキュリティ機能をサポートしています。

-   カラムレベルの権限はサポートされていません
-   パスワードの有効期限、およびパスワードの最終変更された追跡とパスワードの有効期間はサポートされていません[＃9709](https://github.com/pingcap/tidb/issues/9709)
-   権限`max_updated` `max_questions`はサポートさ`max_user_connections`て`max_connections`ません
-   パスワードの検証は現在サポートされていません[＃9741](https://github.com/pingcap/tidb/issues/9741)

## 認証プラグインのステータス {#authentication-plugin-status}

TiDBは複数の認証方法をサポートしています。これらのメソッドは、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)と[`ALTER USER`](/sql-statements/sql-statement-create-user.md)を使用してユーザーごとに指定できます。これらのメソッドは、同じ名前のMySQLの認証メソッドと互換性があります。

表では、次のサポートされている認証方法のいずれかを使用できます。クライアント/サーバー接続が確立されているときにサーバーがアドバタイズするデフォルトの方法を指定するには、 [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)変数を設定します。

TLS認証のサポートは別の方法で構成されます。詳細については、 [TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)を参照してください。

| 認証方法                    | サポートされています |
| :---------------------- | :--------- |
| `mysql_native_password` | はい         |
| `sha256_password`       | いいえ        |
| `caching_sha2_password` | はい、5.2.0以降 |
| `auth_socket`           | はい、5.3.0以降 |
| [TLS Certificates]      | はい         |
| LDAP                    | いいえ        |
| PAM                     | いいえ        |
| ed25519（MariaDB）        | いいえ        |
| GSSAPI（MariaDB）         | いいえ        |
| FIDO                    | いいえ        |

[TLS Certificates]: /enable-tls-between-clients-and-servers.md
