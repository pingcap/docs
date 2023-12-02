---
title: Security Compatibility with MySQL
summary: Learn TiDB's security compatibilities with MySQL.
---

# MySQL とのSecurity互換性 {#security-compatibility-with-mysql}

TiDB は、 MySQL 5.7と同様のセキュリティ機能をサポートし、MySQL 8.0 のいくつかのセキュリティ機能もサポートします。 TiDB のセキュリティ機能は実装において MySQL とは異なります。

## サポートされていないセキュリティ機能 {#unsupported-security-features}

-   カラムレベルの権限。
-   これらのアクセス許可属性: `max_questions` 、 `max_updated` 、および`max_user_connections` 。
-   パスワード検証ポリシー。現在のパスワードを変更するときに、そのパスワードを検証する必要があります。
-   二重パスワードポリシー。
-   ランダムなパスワード生成。
-   多要素認証。

## MySQLとの違い {#differences-with-mysql}

### パスワードの有効期限ポリシー {#password-expiration-policy}

TiDB と MySQL のパスワード有効期限ポリシーには次のような違いがあります。

-   MySQL は v5.7 および v8.0 でパスワード有効期限ポリシーをサポートします。
-   TiDB は v6.5.0 からパスワード有効期限ポリシーをサポートします。

TiDB の有効期限メカニズムは、次の点で MySQL とは異なります。

-   MySQL v5.7 および v8.0 では、クライアントとサーバーの構成を組み合わせて、クライアント接続に対して「サンドボックス モード」を有効にするかどうかが決まります。
-   TiDB では、 [`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650)構成項目だけで、クライアント接続に対して「サンドボックス モード」を有効にするかどうかが決まります。

### パスワードの複雑さのポリシー {#password-complexity-policy}

TiDB と MySQL のパスワード複雑さのポリシーには次のような違いがあります。

-   MySQL v5.7 は、 `validate_password`プラグインを使用してパスワードの複雑さのポリシーを実装します。
-   MySQL v8.0 は、 `validate_password`コンポーネントを使用してパスワードの複雑さのポリシーを再実装します。
-   TiDB では、v6.5.0 以降、組み込みのパスワード複雑さ管理機能が導入されています。

機能の実装には次の違いがあります。

-   機能を有効にします。

    -   MySQL v5.7 では、この機能は`validate_password`プラグインを使用して実装されます。プラグインをインストールすることでこの機能を有効にできます。
    -   MySQL v8.0 では、この機能は`validate_password`コンポーネントを使用して実装されます。この機能は、コンポーネントをインストールすることで有効にできます。
    -   TiDB の場合、この機能は組み込まれています。システム変数[`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)を使用してこの機能を有効にできます。

-   辞書チェック:

    -   MySQL v5.7 では、 `validate_password_dictionary_file`変数を使用してファイル パスを指定できます。このファイルには、パスワードに含めることが許可されていない単語のリストが含まれています。
    -   MySQL v8.0 では、 `validate_password.dictionary_file`変数を使用してファイル パスを指定できます。このファイルには、パスワードに含めることが許可されていない単語のリストが含まれています。
    -   TiDB では、 [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-new-in-v650)システム変数を使用して文字列を指定できます。この文字列には、パスワードに含めることが許可されていない単語のリストが含まれています。

### パスワード障害の追跡 {#password-failure-tracking}

TiDB と MySQL のパスワード障害追跡ポリシーには次のような違いがあります。

-   MySQL v5.7 はパスワード失敗の追跡をサポートしていません。
-   MySQL v8.0 はパスワード失敗の追跡をサポートしています。
-   TiDB は、v6.5.0 以降、パスワード障害追跡をサポートしています。

アカウントの失敗した試行回数とロック ステータスはグローバルに一貫している必要があり、分散データベースである TiDB は MySQL のように失敗した試行回数とロック ステータスをサーバーメモリに記録できないため、実装メカニズムが TiDB と TiDB で異なります。 MySQL。

-   自動的にロックされないユーザーの場合、次のシナリオで失敗した試行回数がリセットされます。

    -   MySQL 8.0:

        -   サーバーが再起動されると、すべてのアカウントの失敗した試行回数がリセットされます。
        -   `FLUSH PRIVILEGES`を実行すると、すべてのアカウントの失敗回数がリセットされます。
        -   `ALTER USER ... ACCOUNT UNLOCK`を実行してアカウントのロックを解除すると、カウントはリセットされます。
        -   アカウントが正常にログインすると、カウントはリセットされます。

    -   TiDB:

        -   `ALTER USER ... ACCOUNT UNLOCK`を実行してアカウントのロックを解除すると、カウントはリセットされます。
        -   アカウントが正常にログインすると、カウントはリセットされます。

-   自動的にロックされたユーザーの場合、次のシナリオでは試行失敗の回数がリセットされます。

    -   MySQL 8.0:

        -   サーバーが再起動されると、すべてのアカウントの一時的なロックがリセットされます。
        -   `FLUSH PRIVILEGES`を実行すると、全アカウントの一時ロックが解除されます。
        -   アカウントのロック時間が終了すると、次回のログイン試行時にアカウントの一時的なロックがリセットされます。
        -   `ALTER USER ... ACCOUNT UNLOCK`を実行してアカウントのロックを解除すると、アカウントの一時的なロックがリセットされます。

    -   TiDB:

        -   アカウントのロック時間が終了すると、次回のログイン試行時にアカウントの一時的なロックがリセットされます。
        -   `ALTER USER ... ACCOUNT UNLOCK`を実行してアカウントのロックを解除すると、アカウントの一時的なロックがリセットされます。

### パスワード再利用ポリシー {#password-reuse-policy}

TiDB と MySQL のパスワード再利用ポリシーには次のような違いがあります。

-   MySQL v5.7 はパスワードの再利用管理をサポートしていません。
-   MySQL v8.0 はパスワードの再利用管理をサポートしています。
-   TiDB は v6.5.0 からパスワード再利用管理をサポートします。

実装メカニズムは TiDB と MySQL の間で一貫しています。どちらも`mysql.password_history`システム テーブルを使用して、パスワード再利用管理機能を実装します。ただし、 `mysql.user`システム テーブルに存在しないユーザーを削除する場合、TiDB と MySQL では動作が異なります。

-   シナリオ: ユーザー ( `user01` ) は通常の方法では作成されません。代わりに、 `INSERT INTO mysql.password_history VALUES (...)`ステートメントを使用して`user01`のレコードを`mysql.password_history`システム テーブルに追加することによって作成されます。このような場合、 `mysql.user`システムテーブルには`user01`のレコードが存在しないため、 `user01`で`DROP USER`実行すると、TiDB と MySQL の動作が異なります。

    -   MySQL: `DROP USER user01`を実行すると、MySQL は`mysql.user`と`mysql.password_history`で`user01`見つけようとします。いずれかのシステム テーブルに`user01`含まれている場合、 `DROP USER`ステートメントは正常に実行され、エラーは報告されません。
    -   TiDB: `DROP USER user01`を実行すると、TiDB は`mysql.user`の中でのみ`user01`を見つけようとします。関連するレコードが見つからない場合、 `DROP USER`ステートメントは失敗し、エラーが報告されます。ステートメントを正常に実行して`mysql.password_history`から`user01`レコードを削除したい場合は、代わりに`DROP USER IF EXISTS user01`使用してください。

## 認証プラグインのステータス {#authentication-plugin-status}

TiDB は複数の認証方法をサポートしています。これらのメソッドは、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)と[`ALTER USER`](/sql-statements/sql-statement-create-user.md)を使用してユーザーごとに指定できます。これらのメソッドは、同じ名前の MySQL の認証メソッドと互換性があります。

次の表でサポートされている認証方法のいずれかを使用できます。クライアント/サーバー接続の確立時にサーバーがアドバタイズするデフォルトのメソッドを指定するには、変数[`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)を設定します。 `tidb_sm3_password`は、TiDB でのみサポートされている SM3 認証方法です。したがって、この方法を使用して認証するには、 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)を使用して TiDB に接続する必要があります。 `tidb_auth_token`は、 TiDB Cloudでのみ使用される JSON Web Token (JWT) ベースの認証方法です。

<CustomContent platform="tidb">

TLS 認証のサポートの構成は異なります。詳細については、 [TiDB クライアントとサーバーの間で TLS を有効にする](/enable-tls-between-clients-and-servers.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TLS 認証のサポートの構成は異なります。詳細については、 [TiDB クライアントとサーバーの間で TLS を有効にする](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers)を参照してください。

</CustomContent>

| 認証方法                         | サポートされています  |
| :--------------------------- | :---------- |
| `mysql_native_password`      | はい          |
| `sha256_password`            | いいえ         |
| `caching_sha2_password`      | はい、5.2.0 以降 |
| `auth_socket`                | はい、5.3.0 以降 |
| `tidb_sm3_password`          | はい、6.3.0 以降 |
| `tidb_auth_token`            | はい、6.4.0 以降 |
| `authentication_ldap_sasl`   | はい、7.1.0 以降 |
| `authentication_ldap_simple` | はい、7.1.0 以降 |
| TLS証明書                       | はい          |
| LDAP                         | はい、7.1.0 以降 |
| パム                           | いいえ         |
| ed25519 (マリアDB)              | いいえ         |
| GSSAPI (MariaDB)             | いいえ         |
| フィド                          | いいえ         |
