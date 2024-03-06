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

    -   MySQL: `DROP USER user01`を実行すると、MySQL は`mysql.user`と`mysql.password_history`から`user01`見つけようとします。いずれかのシステム テーブルに`user01`含まれている場合、 `DROP USER`ステートメントは正常に実行され、エラーは報告されません。
    -   TiDB: `DROP USER user01`を実行すると、TiDB は`mysql.user`の中でのみ`user01`を見つけようとします。関連するレコードが見つからない場合、 `DROP USER`ステートメントは失敗し、エラーが報告されます。ステートメントを正常に実行して`mysql.password_history`から`user01`レコードを削除したい場合は、代わりに`DROP USER IF EXISTS user01`使用してください。

## 認証プラグインのステータス {#authentication-plugin-status}

TiDB は複数の認証方法をサポートしています。これらのメソッドは、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)と[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)を使用してユーザーごとに指定できます。これらのメソッドは、同じ名前の MySQL の認証メソッドと互換性があります。

次の表でサポートされている認証方法のいずれかを使用できます。クライアント/サーバー接続の確立時にサーバーがアドバタイズするデフォルトのメソッドを指定するには、変数[`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)を設定します。 `tidb_sm3_password`は、TiDB でのみサポートされている SM3 認証方法です。したがって、この方法を使用して認証するには、 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)を使用して TiDB に接続する必要があります。 `tidb_auth_token`は、 TiDB Cloudで使用される JSON Web Token (JWT) ベースの認証方法であり、TiDB Self-Hosted で使用するように構成することもできます。

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

### <code>tidb_auth_token</code> {#code-tidb-auth-token-code}

`tidb_auth_token`は、 [JSON ウェブトークン (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)に基づくパスワードなしの認証方法です。 v6.4.0 では、 `tidb_auth_token`はTiDB Cloudでのユーザー認証にのみ使用されます。 v6.5.0 以降、TiDB Self-Hosted のユーザー認証方法として`tidb_auth_token`を構成することもできます。 `mysql_native_passsword`や`caching_sha2_password`などのパスワードベースの認証方法とは異なり、 `tidb_auth_token`使用してユーザーを作成する場合、カスタム パスワードを設定または保存する必要はありません。 TiDB にログインするには、ユーザーはパスワードの代わりに署名付きトークンを使用するだけで済みます。これにより、認証プロセスが簡素化され、セキュリティが向上します。

#### JWT {#jwt}

JWT は、ヘッダー、ペイロード、署名の 3 つの部分で構成されます。これらは、base64 を使用してエンコードされた後、クライアントとサーバー間の送信のためにドット ( `.` ) で区切られた文字列に連結されます。

ヘッダーには、次の 3 つのパラメーターを含む JWT のメタデータが記述されます。

-   `alg` : 署名のアルゴリズム。デフォルトでは`RS256`です。
-   `typ` : トークンのタイプ、つまり`JWT` 。
-   `kid` : トークン署名を生成するためのキー ID。

ヘッダーの例を次に示します。

```json
{
  "alg": "RS256",
  "kid": "the-key-id-0",
  "typ": "JWT"
}
```

ペイロードは JWT の主要部分であり、ユーザー情報が格納されます。ペイロードの各フィールドはクレームと呼ばれます。 TiDB ユーザー認証に必要なクレームは次のとおりです。

-   `iss` : `TOKEN_ISSUER`が指定されていないか、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)のときに空に設定されている場合、このクレームは必要ありません。それ以外の場合、 `iss` `TOKEN_ISSUER`と同じ値を使用する必要があります。
-   `sub` : このクレームは、認証されるユーザー名と同じである必要があります。
-   `iat` : `issued at` 、トークンが発行されたときのタイムスタンプを意味します。 TiDB では、この値は認証時刻より遅くなったり、認証の 15 分前より前であってはなりません。
-   `exp` : トークンの有効期限が切れたときのタイムスタンプ。認証時刻より前の場合、認証は失敗します。
-   `email` : `ATTRIBUTE '{"email": "xxxx@pingcap.com"}`でユーザー作成時にメールアドレスを指定できます。ユーザーの作成時に電子メールが指定されていない場合、このクレームは空の文字列として設定する必要があります。それ以外の場合、このクレームはユーザーの作成時に指定された値と同じである必要があります。

ペイロードの例を次に示します。

```json
{
  "email": "user@pingcap.com",
  "exp": 1703305494,
  "iat": 1703304594,
  "iss": "issuer-abc",
  "sub": "user@pingcap.com"
}
```

署名は、ヘッダーとペイロードのデータに署名するために使用されます。

> **警告：**
>
> -   Base64 でのヘッダーとペイロードのエンコードは元に戻すことができます。機密情報を添付し**ない**でください。
> -   `tidb_auth_token`認証方法では、クライアントがトークンをプレーン テキストで TiDB に送信するために[`mysql_clear_password`](https://dev.mysql.com/doc/refman/8.0/en/cleartext-pluggable-authentication.html)プラグインをサポートする必要があります。したがって、 `tidb_auth_token`使用する前に[クライアントとサーバー間のTLSの有効化](/enable-tls-between-clients-and-servers.md)必要があります。

#### 使用法 {#usage}

TiDB セルフホスト ユーザーの認証方法として`tidb_auth_token`構成して使用するには、次の手順を実行します。

1.  TiDB 構成ファイルで[`auth-token-jwks`](/tidb-configuration-file.md#auth-token-jwks-new-in-v640)と[`auth-token-refresh-interval`](/tidb-configuration-file.md#auth-token-refresh-interval-new-in-v640)を構成します。

    たとえば、次のコマンドを使用して JWKS の例を取得できます。

    ```bash
    wget https://raw.githubusercontent.com/CbcWestwolf/generate_jwt/master/JWKS.json
    ```

    次に、サンプル JWKS のパスを`config.toml`で構成します。

    ```toml
    [security]
    auth-token-jwks = "JWKS.json"
    ```

2.  `tidb-server`開始し、JWKS を定期的に更新して、 `auth-token-jwks`で指定したパスに保存します。

3.  `tidb_auth_token`でユーザーを作成し、必要に応じて`REQUIRE TOKEN_ISSUER`と`ATTRIBUTE '{"email": "xxxx@pingcap.com"}`を使用して`iss`と`email`を指定します。

    たとえば、ユーザー`user@pingcap.com`と`tidb_auth_token`を作成します。

    ```sql
    CREATE USER 'user@pingcap.com' IDENTIFIED WITH 'tidb_auth_token' REQUIRE TOKEN_ISSUER 'issuer-abc' ATTRIBUTE '{"email": "user@pingcap.com"}';
    ```

4.  認証用のトークンを生成して署名し、MySQL クライアントの`mysql_clear_text`プラグインを使用して認証します。

    `go install github.com/cbcwestwolf/generate_jwt`を介して JWT 生成ツールをインストールします (このツールは`tidb_auth_token`テストにのみ使用されます)。例えば：

    ```text
    generate_jwt --kid "the-key-id-0" --sub "user@pingcap.com" --email "user@pingcap.com" --iss "issuer-abc"
    ```

    次のように公開キーとトークンを出力。

    ```text
    -----BEGIN PUBLIC KEY-----
    MIIBCgKCAQEAq8G5n9XBidxmBMVJKLOBsmdOHrCqGf17y9+VUXingwDUZxRp2Xbu
    LZLbJtLgcln1lC0L9BsogrWf7+pDhAzWovO6Ai4Aybu00tJ2u0g4j1aLiDdsy0gy
    vSb5FBoL08jFIH7t/JzMt4JpF487AjzvITwZZcnsrB9a9sdn2E5B/aZmpDGi2+Is
    f5osnlw0zvveTwiMo9ba416VIzjntAVEvqMFHK7vyHqXbfqUPAyhjLO+iee99Tg5
    AlGfjo1s6FjeML4xX7sAMGEy8FVBWNfpRU7ryTWoSn2adzyA/FVmtBvJNQBCMrrA
    hXDTMJ5FNi8zHhvzyBKHU0kBTS1UNUbP9wIDAQAB
    -----END PUBLIC KEY-----

    eyJhbGciOiJSUzI1NiIsImtpZCI6InRoZS1rZXktaWQtMCIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXJAcGluZ2NhcC5jb20iLCJleHAiOjE3MDMzMDU0OTQsImlhdCI6MTcwMzMwNDU5NCwiaXNzIjoiaXNzdWVyLWFiYyIsInN1YiI6InVzZXJAcGluZ2NhcC5jb20ifQ.T4QPh2hTB5on5xCuvtWiZiDTuuKvckggNHtNaovm1F4RvwUv15GyOqj9yMstE-wSoV5eLEcPC2HgE6eN1C6yH_f4CU-A6n3dm9F1w-oLbjts7aYCl8OHycVYnq609fNnb8JLsQAmd1Zn9C0JW899-WSOQtvjLqVSPe9prH-cWaBVDQXzUJKxwywQzk9v-Z1Njt9H3Rn9vvwwJEEPI16VnaNK38I7YG-1LN4fAG9jZ6Zwvz7vb_s4TW7xccFf3dIhWTEwOQ5jDPCeYkwraRXU8NC6DPF_duSrYJc7d7Nu9Z2cr-E4i1Rt_IiRTuIIzzKlcQGg7jd9AGEfGe_SowsA-w
    ```

    ログイン用の最後の行にある前述のトークンをコピーします。

    ```Shell
    mycli -h 127.0.0.1 -P 4000 -u 'user@pingcap.com' -p '<the-token-generated>'
    ```

    ここの MySQL クライアントが`mysql_clear_password`プラグインをサポートしていることを確認してください。 [マイクリ](https://www.mycli.net/) 、このプラグインがデフォルトでサポートされ、有効になります。 [mysqlコマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)使用している場合は、 `--enable-cleartext-plugin`オプションを使用してこのプラグインを有効にする必要があります。

    ```Shell
    mysql -h 127.0.0.1 -P 4000 -u 'user@pingcap.com' -p'<the-token-generated>' --enable-cleartext-plugin
    ```

    トークンの生成時に誤った`--sub`が指定された場合 ( `--sub "wronguser@pingcap.com"`など)、このトークンを使用した認証は失敗します。

[jwt.io](https://jwt.io/)によって提供されるデバッガーを使用して、トークンをエンコードおよびデコードできます。
