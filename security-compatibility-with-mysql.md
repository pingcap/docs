---
title: Security Compatibility with MySQL
summary: Learn TiDB's security compatibilities with MySQL.
---

# MySQL とのSecurityの互換性 {#security-compatibility-with-mysql}

TiDB はMySQL 5.7と同様のセキュリティ機能をサポートしており、MySQL 8.0 の一部のセキュリティ機能もサポートしています。 TiDB のセキュリティ機能は、MySQL とは実装が異なります。

## サポートされていないセキュリティ機能 {#unsupported-security-features}

-   カラムレベルの権限。
-   これらの許可属性: `max_questions` 、 `max_updated` 、および`max_user_connections` 。
-   パスワード検証ポリシー。変更時に現在のパスワードを検証する必要があります。
-   デュアル パスワード ポリシー。
-   ランダムパスワード生成。
-   多要素認証。

## MySQL との違い {#differences-with-mysql}

### パスワードの有効期限ポリシー {#password-expiration-policy}

TiDB と MySQL のパスワード有効期限ポリシーには、次の違いがあります。

-   MySQL は、v5.7 および v8.0 でパスワード有効期限ポリシーをサポートしています。
-   TiDB は、v6.5.0 以降のパスワード有効期限ポリシーをサポートしています。

TiDB の有効期限メカニズムは、次の点で MySQL とは異なります。

-   MySQL v5.7 および v8.0 では、クライアントとサーバーを組み合わせた構成によって、クライアント接続の「サンドボックス モード」を有効にするかどうかが決まります。
-   TiDB では、 [`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650)構成項目だけで、クライアント接続の「サンドボックス モード」を有効にするかどうかが決まります。

### パスワードの複雑さに関するポリシー {#password-complexity-policy}

TiDB と MySQL のパスワード複雑度ポリシーには、次の違いがあります。

-   MySQL v5.7 は、 `validate_password`プラグインを使用してパスワード複雑性ポリシーを実装します。
-   MySQL v8.0 は、 `validate_password`コンポーネントを使用してパスワード複雑性ポリシーを再実装します。
-   TiDB は、v6.5.0 から組み込みのパスワード複雑性管理機能を導入しています。

機能の実装には、次の違いがあります。

-   機能を有効にします。

    -   MySQL v5.7 では、この機能は`validate_password`プラグインを使用して実装されています。プラグインをインストールすることで、この機能を有効にすることができます。
    -   MySQL v8.0 では、この機能は`validate_password`コンポーネントを使用して実装されています。コンポーネントをインストールすることで、この機能を有効にすることができます。
    -   TiDB の場合、この機能は組み込まれています。システム変数[`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)を使用して機能を有効にすることができます。

-   辞書チェック:

    -   MySQL v5.7 では、 `validate_password_dictionary_file`変数を使用してファイル パスを指定できます。このファイルには、パスワードに使用できない単語のリストが含まれています。
    -   MySQL v8.0 では、 `validate_password.dictionary_file`変数を使用してファイル パスを指定できます。このファイルには、パスワードに使用できない単語のリストが含まれています。
    -   TiDB では、 [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-new-in-v650)システム変数を使用して文字列を指定できます。文字列には、パスワードに含めることを許可されていない単語のリストが含まれています。

### パスワードの失敗の追跡 {#password-failure-tracking}

TiDB と MySQL のパスワード失敗追跡ポリシーには、次の違いがあります。

-   MySQL v5.7 は、パスワードの失敗の追跡をサポートしていません。
-   MySQL v8.0 は、パスワードの失敗の追跡をサポートしています。
-   TiDB は、v6.5.0 から始まるパスワード障害の追跡をサポートしています。

アカウントの試行失敗回数とロック状態はグローバルに一貫している必要があり、TiDB は分散データベースであるため、MySQL のように試行失敗回数とロック状態をサーバーメモリに記録できないため、TiDB と TiDB では実装メカニズムが異なります。 MySQL。

-   自動的にロックされていないユーザーの場合、失敗した試行回数は次のシナリオでリセットされます。

    -   MySQL 8.0:

        -   サーバーを再起動すると、すべてのアカウントの試行失敗回数がリセットされます。
        -   `FLUSH PRIVILEGES`を実行すると、全アカウントの失敗回数がリセットされます。
        -   `ALTER USER ... ACCOUNT UNLOCK`を実行してアカウントのロックを解除すると、カウントがリセットされます。
        -   アカウントが正常にログインすると、カウントはリセットされます。

    -   TiDB:

        -   `ALTER USER ... ACCOUNT UNLOCK`を実行してアカウントのロックを解除すると、カウントがリセットされます。
        -   アカウントが正常にログインすると、カウントはリセットされます。

-   自動的にロックされたユーザーの場合、失敗した試行回数は次のシナリオでリセットされます。

    -   MySQL 8.0:

        -   サーバーを再起動すると、すべてのアカウントの一時的なロックがリセットされます。
        -   `FLUSH PRIVILEGES`を実行すると、全アカウントの一時ロックが解除されます。
        -   アカウントのロック時間が終了すると、アカウントの一時ロックは次のログイン試行でリセットされます。
        -   `ALTER USER ... ACCOUNT UNLOCK`を実行してアカウントのロックを解除すると、アカウントの一時的なロックがリセットされます。

    -   TiDB:

        -   アカウントのロック時間が終了すると、アカウントの一時ロックは次のログイン試行でリセットされます。
        -   `ALTER USER ... ACCOUNT UNLOCK`を実行してアカウントのロックを解除すると、アカウントの一時的なロックがリセットされます。

### パスワード再利用ポリシー {#password-reuse-policy}

TiDB と MySQL のパスワード再利用ポリシーには、次の違いがあります。

-   MySQL v5.7 は、パスワードの再利用管理をサポートしていません。
-   MySQL v8.0 は、パスワードの再利用管理をサポートしています。
-   TiDB は v6.5.0 からパスワードの再利用管理をサポートしています。

実装メカニズムは、TiDB と MySQL の間で一貫しています。どちらも`mysql.password_history`システム テーブルを使用して、パスワード再利用管理機能を実装します。ただし、 `mysql.user`システム テーブルに存在しないユーザーを削除する場合、TiDB と MySQL では動作が異なります。

-   シナリオ: ユーザー ( `user01` ) は通常の方法では作成されません。代わりに、 `INSERT INTO mysql.password_history VALUES (...)`ステートメントを使用して`user01`のレコードを`mysql.password_history`システム テーブルに追加することによって作成されます。このような場合、 `mysql.user`システム テーブルに`user01`のレコードが存在しないため、 `user01`で`DROP USER`実行すると、TiDB と MySQL の動作が異なります。

    -   MySQL: `DROP USER user01`を実行すると、MySQL は`mysql.user`と`mysql.password_history`で`user01`見つけようとします。いずれかのシステム テーブルに`user01`含まれている場合、 `DROP USER`ステートメントは正常に実行され、エラーは報告されません。
    -   TiDB: `DROP USER user01`を実行すると、TiDB は`mysql.user`でのみ`user01`を見つけようとします。関連するレコードが見つからない場合、 `DROP USER`ステートメントは失敗し、エラーが報告されます。ステートメントを正常に実行して`mysql.password_history`から`user01`レコードを削除するには、代わりに`DROP USER IF EXISTS user01`使用します。

## 認証プラグインのステータス {#authentication-plugin-status}

TiDB は複数の認証方法をサポートしています。これらのメソッドは、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)および[`ALTER USER`](/sql-statements/sql-statement-create-user.md)を使用してユーザーごとに指定できます。これらのメソッドは、同じ名前の MySQL の認証メソッドと互換性があります。

次の表でサポートされている認証方法のいずれかを使用できます。クライアント/サーバー接続が確立されているときにサーバーがアドバタイズするデフォルトの方法を指定するには、 [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)変数を設定します。 `tidb_sm3_password`は、TiDB でのみサポートされている SM3 認証方式です。したがって、この方法を使用して認証するには、 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)を使用して TiDB に接続する必要があります。 `tidb_auth_token`は、 TiDB Cloudでのみ使用される JSON Web Token (JWT) ベースの認証方法です。

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
| `tidb_auth_token`       | はい、6.4.0 以降 |
| TLS 証明書                 | はい          |
| LDAP                    | いいえ         |
| パム                      | いいえ         |
| ed25519 (マリアDB)         | いいえ         |
| GSSAPI (MariaDB)        | いいえ         |
| ファイド                    | いいえ         |
