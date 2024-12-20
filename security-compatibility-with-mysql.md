---
title: Security Compatibility with MySQL
summary: TiDB と MySQL のセキュリティ互換性について学習します。
---

# MySQL とのSecurity互換性 {#security-compatibility-with-mysql}

TiDB はMySQL 5.7と同様のセキュリティ機能をサポートし、MySQL 8.0 の一部のセキュリティ機能もサポートしています。TiDB のセキュリティ機能は実装が MySQL とは異なります。

## サポートされていないセキュリティ機能 {#unsupported-security-features}

-   カラムレベルの権限。
-   これらの権限属性: `max_questions` 、 `max_updated` 、および`max_user_connections` 。
-   パスワード検証ポリシー。パスワードを変更するときに現在のパスワードを検証する必要があります。
-   二重パスワードポリシー。
-   ランダムなパスワード生成。
-   多要素認証。

## MySQLとの違い {#differences-with-mysql}

### パスワード有効期限ポリシー {#password-expiration-policy}

TiDB と MySQL のパスワード有効期限ポリシーには、次の違いがあります。

-   MySQL は、v5.7 および v8.0 でパスワード有効期限ポリシーをサポートしています。
-   TiDB は、v6.5.0 以降でパスワード有効期限ポリシーをサポートします。

TiDB の有効期限メカニズムは、次の点で MySQL と異なります。

-   MySQL v5.7 および v8.0 では、クライアントとサーバーの構成を組み合わせて、クライアント接続に対して「サンドボックス モード」を有効にするかどうかを決定します。
-   TiDB では、 [`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650)構成項目だけで、クライアント接続に対して「サンドボックス モード」を有効にするかどうかが決まります。

### パスワードの複雑さに関するポリシー {#password-complexity-policy}

TiDB と MySQL のパスワード複雑性ポリシーには、次の違いがあります。

-   MySQL v5.7 は、 `validate_password`プラグインを使用してパスワードの複雑さのポリシーを実装します。
-   MySQL v8.0 では、 `validate_password`コンポーネントを使用してパスワードの複雑さのポリシーが再実装されています。
-   TiDB では、v6.5.0 以降、組み込みのパスワード複雑さ管理機能が導入されています。

機能の実装には次の違いがあります。

-   機能を有効にします:

    -   MySQL v5.7では、 `validate_password`プラグインを使用してこの機能が実装されています。プラグインをインストールすることで、この機能を有効にすることができます。
    -   MySQL v8.0 では、 `validate_password`コンポーネントを使用してこの機能が実装されています。コンポーネントをインストールすることで、この機能を有効にすることができます。
    -   TiDB の場合、この機能は組み込まれています。システム変数[`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650)使用してこの機能を有効にすることができます。

-   辞書チェック:

    -   MySQL v5.7 では、 `validate_password_dictionary_file`変数を使用してファイル パスを指定できます。ファイルには、パスワードに存在できない単語のリストが含まれています。
    -   MySQL v8.0 では、 `validate_password.dictionary_file`変数を使用してファイル パスを指定できます。ファイルには、パスワードに存在できない単語のリストが含まれています。
    -   TiDB では、 [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-new-in-v650)システム変数を使用して文字列を指定できます。文字列には、パスワードに存在できない単語のリストが含まれます。

### パスワード失敗の追跡 {#password-failure-tracking}

TiDB と MySQL のパスワード失敗追跡ポリシーには、次の違いがあります。

-   MySQL v5.7 はパスワード失敗の追跡をサポートしていません。
-   MySQL v8.0 はパスワード失敗の追跡をサポートしています。
-   TiDB は、v6.5.0 以降でパスワード失敗の追跡をサポートしています。

失敗した試行回数とアカウントのロック状態はグローバルに一貫している必要があり、分散データベースである TiDB は MySQL のように失敗した試行回数とロック状態をサーバーメモリに記録できないため、実装メカニズムは TiDB と MySQL で異なります。

-   自動的にロックされないユーザーの場合、次のシナリオで失敗した試行回数がリセットされます。

    -   MySQL 8.0:

        -   サーバーを再起動すると、すべてのアカウントの失敗した試行回数がリセットされます。
        -   `FLUSH PRIVILEGES`を実行すると、すべてのアカウントの失敗した試行回数がリセットされます。
        -   `ALTER USER ... ACCOUNT UNLOCK`実行してアカウントのロックを解除すると、カウントがリセットされます。
        -   アカウントが正常にログインすると、カウントはリセットされます。

    -   ティDB:

        -   `ALTER USER ... ACCOUNT UNLOCK`実行してアカウントのロックを解除すると、カウントがリセットされます。
        -   アカウントが正常にログインすると、カウントはリセットされます。

-   自動的にロックされるユーザーの場合、次のシナリオでは失敗した試行回数がリセットされます。

    -   MySQL 8.0:

        -   サーバーを再起動すると、すべてのアカウントの一時ロックがリセットされます。
        -   `FLUSH PRIVILEGES`実行すると、すべてのアカウントの一時ロックがリセットされます。
        -   アカウントのロック時間が終了すると、次回のログイン試行時にアカウントの一時ロックがリセットされます。
        -   `ALTER USER ... ACCOUNT UNLOCK`実行してアカウントのロックを解除すると、アカウントの一時的なロックがリセットされます。

    -   ティDB:

        -   アカウントのロック時間が終了すると、次回のログイン試行時にアカウントの一時ロックがリセットされます。
        -   `ALTER USER ... ACCOUNT UNLOCK`実行してアカウントのロックを解除すると、アカウントの一時的なロックがリセットされます。

### パスワード再利用ポリシー {#password-reuse-policy}

TiDB と MySQL のパスワード再利用ポリシーには、次の違いがあります。

-   MySQL v5.7 はパスワード再利用管理をサポートしていません。
-   MySQL v8.0 はパスワード再利用管理をサポートしています。
-   TiDB は、v6.5.0 以降でパスワード再利用管理をサポートしています。

TiDB と MySQL の実装メカニズムは一貫しています。どちらも`mysql.password_history`システム テーブルを使用してパスワード再利用管理機能を実装します。ただし、 `mysql.user`システム テーブルに存在しないユーザーを削除する場合、TiDB と MySQL の動作は異なります。

-   シナリオ: ユーザー ( `user01` ) は通常の方法で作成されず、 `INSERT INTO mysql.password_history VALUES (...)`ステートメントを使用して`user01`のレコードを`mysql.password_history`システム テーブルに追加することによって作成されます。このような場合、 `user01`のレコードは`mysql.user`システム テーブルに存在しないため、 `user01`で`DROP USER`実行すると、TiDB と MySQL の動作が異なります。

    -   MySQL: `DROP USER user01`実行すると、MySQL は`mysql.user`と`mysql.password_history`で`user01`見つけようとします。いずれかのシステム テーブルに`user01`含まれている場合、 `DROP USER`ステートメントは正常に実行され、エラーは報告されません。
    -   TiDB: `DROP USER user01`実行すると、TiDB は`mysql.user`でのみ`user01`検索しようとします。関連するレコードが見つからない場合、 `DROP USER`ステートメントは失敗し、エラーが報告されます。ステートメントを正常に実行し、 `mysql.password_history`から`user01`レコードを削除する場合は、代わりに`DROP USER IF EXISTS user01`使用します。

## 認証プラグインのステータス {#authentication-plugin-status}

TiDB は複数の認証方法をサポートしています。これらの方法は、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)と[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)使用してユーザーごとに指定できます。これらの方法は、同じ名前の MySQL の認証方法と互換性があります。

次の表に示すサポートされている認証方法のいずれかを使用できます。クライアントとサーバー間の接続を確立するときにサーバーが通知するデフォルトの方法を指定するには、 [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)変数を設定します。 `tidb_sm3_password` 、TiDB でのみサポートされている SM3 認証方法です。したがって、この方法を使用して認証するには、 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)使用して TiDB に接続する必要があります。 `tidb_auth_token`は、 TiDB Cloudで使用される JSON Web Token (JWT) ベースの認証方法で、TiDB Self-Managed で使用するように構成することもできます。

<CustomContent platform="tidb">

TLS 認証のサポートは異なる構成になっています。詳細については、 [TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TLS 認証のサポートは異なる構成になっています。詳細については、 [TiDBクライアントとサーバー間のTLSを有効にする](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers)参照してください。

</CustomContent>

| 認証方法                         | サポート       |
| :--------------------------- | :--------- |
| `mysql_native_password`      | はい         |
| `sha256_password`            | いいえ        |
| `caching_sha2_password`      | はい、5.2.0以降 |
| `auth_socket`                | はい、5.3.0以降 |
| `tidb_sm3_password`          | はい、6.3.0以降 |
| `tidb_auth_token`            | はい、6.4.0以降 |
| `authentication_ldap_sasl`   | はい、7.1.0以降 |
| `authentication_ldap_simple` | はい、7.1.0以降 |
| TLS 証明書                      | はい         |
| LDAP の                       | はい、7.1.0以降 |
| パム                           | いいえ        |
| ed25519 (マリアDB)              | いいえ        |
| GSSAPI (MariaDB)             | いいえ        |
| ファイド                         | いいえ        |

### <code>tidb_auth_token</code> {#code-tidb-auth-token-code}

`tidb_auth_token` [JSON ウェブトークン (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)に基づくパスワードレス認証方式です。v6.4.0 では、 `tidb_auth_token` TiDB Cloudでのユーザー認証にのみ使用されます。v6.5.0 以降では、 `tidb_auth_token` TiDB Self-Managed のユーザー認証方式として設定することもできます。 `mysql_native_password`や`caching_sha2_password`などのパスワードベースの認証方式とは異なり、 `tidb_auth_token`使用してユーザーを作成する場合、カスタムパスワードを設定したり保存したりする必要はありません。TiDB にログインするには、ユーザーはパスワードの代わりに署名付きトークンを使用するだけでよいため、認証プロセスが簡素化され、セキュリティが向上します。

#### JWT {#jwt}

JWTは、ヘッダー、ペイロード、署名の3つの部分で構成されています。これらはbase64でエンコードされた後、ドットで区切られた文字列（ `.` ）に連結され、クライアントとサーバー間で送信されます。

ヘッダーは、3 つのパラメータを含む JWT のメタデータを記述します。

-   `alg` : 署名のアルゴリズム。デフォルトは`RS256`です。
-   `typ` : トークンのタイプ`JWT`です。
-   `kid` : トークン署名を生成するためのキー ID。

ヘッダーの例を次に示します。

```json
{
  "alg": "RS256",
  "kid": "the-key-id-0",
  "typ": "JWT"
}
```

ペイロードは JWT の主要部分であり、ユーザー情報を保存します。ペイロード内の各フィールドはクレームと呼ばれます。TiDB ユーザー認証に必要なクレームは次のとおりです。

-   `iss` : `TOKEN_ISSUER`が指定されていないか、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)ときに空に設定されている場合、このクレームは必要ありません。それ以外の場合、 `iss` `TOKEN_ISSUER`と同じ値を使用する必要があります。
-   `sub` : このクレームは、認証されるユーザー名と同じである必要があります。
-   `iat` : `issued at`を意味し、トークンが発行されたときのタイムスタンプです。TiDB では、この値は認証時間より遅くてはならず、認証の 15 分前より早くてはなりません。
-   `exp` : トークンの有効期限が切れるタイムスタンプ。認証時刻より早い場合、認証は失敗します。
-   `email` : ユーザーを作成するときに`ATTRIBUTE '{"email": "xxxx@pingcap.com"}`で電子メールを指定できます。ユーザーの作成時に電子メールが指定されていない場合、このクレームは空の文字列として設定する必要があります。それ以外の場合、このクレームはユーザーの作成時に指定された値と同じである必要があります。

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

署名は、ヘッダーとペイロード データに署名するために使用されます。

> **警告：**
>
> -   ヘッダーとペイロードの base64 エンコードは可逆的です。機密情報を添付し**ないで**ください。
> -   `tidb_auth_token`認証方法では、トークンをプレーンテキストで TiDB に送信するために、クライアントが[`mysql_clear_password`](https://dev.mysql.com/doc/refman/8.0/en/cleartext-pluggable-authentication.html)プラグインをサポートしている必要があります。したがって、 `tidb_auth_token`使用する前に[クライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)を行う必要があります。

#### 使用法 {#usage}

TiDB Self-Managed ユーザーの認証方法として`tidb_auth_token`設定して使用するには、次の手順を実行します。

1.  TiDB 構成ファイルで[`auth-token-jwks`](/tidb-configuration-file.md#auth-token-jwks-new-in-v640)と[`auth-token-refresh-interval`](/tidb-configuration-file.md#auth-token-refresh-interval-new-in-v640)構成します。

    たとえば、次のコマンドを使用してサンプルの JWKS を取得できます。

    ```bash
    wget https://raw.githubusercontent.com/CbcWestwolf/generate_jwt/master/JWKS.json
    ```

    次に、 `config.toml`のサンプル JWKS のパスを設定します。

    ```toml
    [security]
    auth-token-jwks = "JWKS.json"
    ```

2.  `tidb-server`起動し、定期的に JWKS を更新して`auth-token-jwks`で指定されたパスに保存します。

3.  `tidb_auth_token`でユーザーを作成し、必要に応じて`REQUIRE TOKEN_ISSUER`と`ATTRIBUTE '{"email": "xxxx@pingcap.com"}`使用して`iss`と`email`指定します。

    たとえば、 `tidb_auth_token`持つユーザー`user@pingcap.com`を作成します。

    ```sql
    CREATE USER 'user@pingcap.com' IDENTIFIED WITH 'tidb_auth_token' REQUIRE TOKEN_ISSUER 'issuer-abc' ATTRIBUTE '{"email": "user@pingcap.com"}';
    ```

4.  認証用のトークンを生成して署名し、MySQL クライアントの`mysql_clear_text`のプラグインを使用して認証します。

    `go install github.com/cbcwestwolf/generate_jwt`から JWT 生成ツールをインストールします (このツールは`tidb_auth_token`テストにのみ使用されます)。例:

    ```text
    generate_jwt --kid "the-key-id-0" --sub "user@pingcap.com" --email "user@pingcap.com" --iss "issuer-abc"
    ```

    公開鍵とトークンは次のように出力。

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

    ログイン用の最後の行にある上記のトークンをコピーします。

    ```Shell
    mycli -h 127.0.0.1 -P 4000 -u 'user@pingcap.com' -p '<the-token-generated>'
    ```

    ここで、MySQL クライアントが`mysql_clear_password`プラグインをサポートしていることを確認します。 [マイクリ](https://www.mycli.net/)デフォルトでこのプラグインをサポートし、有効にします。 [mysql コマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)を使用している場合は、このプラグインを有効にするために`--enable-cleartext-plugin`オプションを使用する必要があります。

    ```Shell
    mysql -h 127.0.0.1 -P 4000 -u 'user@pingcap.com' -p'<the-token-generated>' --enable-cleartext-plugin
    ```

    トークンの生成時に誤った`--sub`が指定された場合 ( `--sub "wronguser@pingcap.com"`など)、このトークンを使用した認証は失敗します。

[翻訳元](https://jwt.io/)が提供するデバッガーを使用してトークンをエンコードおよびデコードできます。
