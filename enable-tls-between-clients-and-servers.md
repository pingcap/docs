---
title: Enable TLS Between TiDB Clients and Servers
summary: データのセキュリティを確保するには、安全な接続を使用します。
---

# TiDBクライアントとサーバー間のTLSを有効にする {#enable-tls-between-tidb-clients-and-servers}

TiDBはデフォルトで、サーバーとクライアント間の安全でない接続を許可します。これにより、チャネルトラフィックを監視する第三者が、サーバーとクライアント間で送受信されるデータ（クエリの内容や結果など）を把握し、場合によっては改ざんすることが可能になります。チャネルが信頼できない場合（クライアントがパブリックネットワーク経由でTiDBサーバーに接続している場合など）、安全でない接続は情報漏洩のリスクを高めます。このような場合、セキュリティ上の理由から、TLSで保護された接続を要求することをお勧めします。

TiDBサーバーは、TLS（Transport Layer Security）プロトコルに基づくセキュア接続をサポートしています。このプロトコルはMySQLのセキュア接続と整合性があり、MySQL Client、MySQL Shell、MySQLドライバーなどの既存のMySQLクライアントで直接サポートされています。TLSはSSL（セキュリティ Sockets Layer）と呼ばれることもあります。SSLプロトコルには[既知のセキュリティ脆弱性](https://en.wikipedia.org/wiki/Transport_Layer_Security)があるため、TiDBはSSLをサポートしていません。TiDBは、TLSv1.2およびTLSv1.3というプロトコルをサポートしています。

TLS で保護された接続が使用される場合、接続には次のセキュリティ プロパティがあります。

-   機密性: 盗聴を防ぐためにトラフィックの平文は暗号化される
-   整合性: トラフィックの平文は改ざんできない
-   認証: (オプション) クライアントはサーバーのIDを検証でき、サーバーは中間者攻撃を回避するためにクライアントのIDを検証できます。

TLSで保護された接続を使用するには、まずTiDBサーバーでTLSを有効にする設定をする必要があります。次に、クライアントアプリケーションでTLSを使用する設定をする必要があります。ほとんどのクライアントライブラリは、サーバーでTLSサポートが正しく設定されていると、自動的にTLSを有効にします。

MySQLと同様に、TiDBでは同じTCPポートでTLS接続と非TLS接続の両方が許可されます。TLSが有効になっているTiDBサーバーでは、暗号化された接続を介してTiDBサーバーに安全に接続するか、暗号化されていない接続を使用するかを選択できます。セキュア接続の使用を必須にするには、以下の方法があります。

-   すべてのユーザーに対して TiDBサーバーへの安全な接続を要求するようにシステム変数[`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)構成します。
-   ユーザーを作成する場合（ `create user` ）、または既存のユーザーを変更する場合（ `alter user` ）に`REQUIRE SSL`指定します。これは、指定されたユーザーがTiDBにアクセスする際にTLS接続を使用する必要があることを指定します。以下はユーザーの作成例です。

    ```sql
    CREATE USER 'u1'@'%' IDENTIFIED BY 'my_random_password' REQUIRE SSL;
    ```

> **注記：**
>
> ログイン ユーザーが[ログインのためのTiDB証明書ベースの認証](/certificate-authentication.md#configure-the-user-certificate-information-for-login-verification)使用して設定した場合、ユーザーは暗黙的に TiDB への暗号化された接続を有効にする必要があります。

## 安全な接続を使用するように TiDBサーバーを構成する {#configure-tidb-server-to-use-secure-connections}

安全な接続を有効にするための関連パラメータについては、次の説明を参照してください。

-   [`auto-tls`](/tidb-configuration-file.md#auto-tls) : 自動証明書生成を有効にする (v5.2.0 以降)
-   [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) : SSL証明書のファイルパスを指定します
-   [`ssl-key`](/tidb-configuration-file.md#ssl-key) : 証明書に一致する秘密鍵を指定します
-   [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) : (オプション) 信頼されたCA証明書のファイルパスを指定します
-   [`tls-version`](/tidb-configuration-file.md#tls-version) : (オプション) 最小の TLS バージョンを指定します (例: &quot;TLSv1.2&quot;)

`auto-tls`安全な接続を許可しますが、クライアント証明書の検証は行いません。証明書の検証と証明書の生成方法を制御するには、以下の`ssl-cert` 、 `ssl-key` 、 `ssl-ca`変数の設定に関するアドバイスを参照してください。

TiDBサーバーで独自の証明書を使用した安全な接続を有効にするには、TiDBサーバーの起動時に設定ファイルでパラメータ`ssl-cert`と`ssl-key`両方を指定する必要があります。また、クライアント認証用のパラメータ`ssl-ca`指定することもできます（ [認証を有効にする](#enable-authentication)参照）。

パラメータで指定されたファイルはすべてPEM（Privacy Enhanced Mail）形式です。現在、TiDBはパスワードで保護された秘密鍵のインポートをサポートしていないため、パスワードなしの秘密鍵ファイルを提供する必要があります。証明書または秘密鍵が無効な場合、TiDBサーバーは通常どおり起動しますが、クライアントはTLS接続を介してTiDBサーバーに接続できません。

証明書パラメータが正しい場合、TiDB は起動時に`"INFO"`レベルのログに`mysql protocol server secure connection is enabled`出力します。

## TLS接続を使用するようにMySQLクライアントを構成する {#configure-the-mysql-client-to-use-tls-connections}

MySQL 5.7以降のバージョンのクライアントは、デフォルトでTLS接続を確立しようとします。サーバーがTLS接続をサポートしていない場合は、自動的に暗号化されていない接続に戻ります。MySQL 5.7より前のバージョンのクライアントは、デフォルトで非TLS接続を使用します。

次の`--ssl-mode`のパラメータを使用して、クライアントの接続動作を変更できます。

-   `--ssl-mode=REQUIRED` : クライアントはTLS接続を要求します。サーバー側がTLS接続をサポートしていない場合、接続を確立できません。
-   パラメータ`--ssl-mode`がない場合：クライアントは TLS 接続を使用しようとしますが、サーバー側が暗号化接続をサポートしていない場合は暗号化接続を確立できません。その場合、クライアントは暗号化されていない接続を使用します。
-   `--ssl-mode=DISABLED` : クライアントは暗号化されていない接続を使用します。

MySQL 8.x クライアントには、このパラメータに加えて 2 つの SSL モードがあります。

-   `--ssl-mode=VERIFY_CA` : `--ssl-ca`必要とする CA に対してサーバーからの証明書を検証します。
-   `--ssl-mode=VERIFY_IDENTITY` : `VERIFY_CA`と同じですが、接続先のホスト名が証明書と一致するかどうかも検証します。

MySQL 5.7および MariaDB クライアント以前では、 `--ssl-verify-server-cert`使用してサーバー証明書の検証を有効にすることができます。

詳細については、MySQL の[暗号化接続のクライアント側コンフィグレーション](https://dev.mysql.com/doc/refman/8.0/en/using-encrypted-connections.html#using-encrypted-connections-client-side-configuration)参照してください。

## 認証を有効にする {#enable-authentication}

TiDBサーバーまたはMySQLクライアントで`ssl-ca`パラメータが指定されていない場合、クライアントまたはサーバーはデフォルトで認証を行わず、中間者攻撃を防止できません。例えば、クライアントが偽装されたクライアントに「安全に」接続してしまう可能性があります。サーバーとクライアントで認証用の`ssl-ca`パラメータを設定できます。通常はサーバーの認証のみで十分ですが、セキュリティをさらに強化するためにクライアントの認証も行うことができます。

-   MySQL クライアントから TiDBサーバーを認証するには:
    1.  TiDBサーバーでパラメータ`ssl-cert`と`ssl-key`指定します。
    2.  MySQL クライアントで`--ssl-ca`パラメータを指定します。
    3.  MySQL クライアントでは少なくとも`--ssl-mode` ～ `VERIFY_CA`指定します。
    4.  TiDBサーバーに設定されている証明書（ `ssl-cert` ）がクライアント`--ssl-ca`パラメータで指定されたCAによって署名されていることを確認してください。そうでない場合、認証は失敗します。

-   TiDBサーバーから MySQL クライアントを認証するには:
    1.  TiDBサーバーで`ssl-cert` 、および`ssl-ca`パラメータ`ssl-key`指定します。
    2.  クライアントでパラメータ`--ssl-cert`と`--ssl-key`指定します。
    3.  サーバー側で設定された証明書とクライアント側で設定された証明書の両方が、サーバーによって指定された`ssl-ca`によって署名されていることを確認します。

<!---->

-   相互認証を実行するには、上記の両方の要件を満たします。

デフォルトでは、サーバーとクライアント間の認証はオプションです。クライアントがTLSハンドシェイク中に身分証明書を提示しない場合でも、TLS接続を確立できます。また、ユーザーの作成時（ `CREATE USER` ）または既存ユーザーの変更時（ `ALTER USER` ）に`REQUIRE x509`指定することで、クライアントの認証を要求することもできます。以下はユーザーの作成例です。

```sql
CREATE USER 'u1'@'%'  REQUIRE X509;
```

> **注記：**
>
> ログイン ユーザーが[ログインのためのTiDB証明書ベースの認証](/certificate-authentication.md#configure-the-user-certificate-information-for-login-verification)使用して設定した場合、ユーザーは暗黙的に TiDB への TLS 接続を有効にする必要があります。

## 現在の接続が暗号化を使用しているかどうかを確認します {#check-whether-the-current-connection-uses-encryption}

`SHOW STATUS LIKE "%Ssl%";`ステートメントを使用して、暗号化が使用されているかどうか、暗号化された接続で使用される暗号化プロトコル、TLS バージョン番号など、現在の接続の詳細を取得します。

暗号化された接続の結果の例を以下に示します。結果は、クライアントがサポートするTLSバージョンまたは暗号化プロトコルによって異なります。

```sql
SHOW STATUS LIKE "Ssl%";
```

    +-----------------------+------------------------------------------------------->
    | Variable_name         | Value                                                 >
    +-----------------------+------------------------------------------------------->
    | Ssl_cipher            | TLS_AES_128_GCM_SHA256                                >
    | Ssl_cipher_list       | RC4-SHA:DES-CBC3-SHA:AES128-SHA:AES256-SHA:AES128-SHA2>
    | Ssl_server_not_after  | Apr 23 07:59:47 2024 UTC                              >
    | Ssl_server_not_before | Jan 24 07:59:47 2024 UTC                              >
    | Ssl_verify_mode       | 5                                                     >
    | Ssl_version           | TLSv1.3                                               >
    +-----------------------+------------------------------------------------------->
    6 rows in set (0.0062 sec)

公式 MySQL クライアントの場合、 `STATUS`または`\s`ステートメントを使用して接続ステータスを表示することもできます。

    mysql> \s
    ...
    SSL: Cipher in use is TLS_AES_128_GCM_SHA256
    ...

## サポートされている TLS バージョン、鍵交換プロトコル、暗号化アルゴリズム {#supported-tls-versions-key-exchange-protocols-and-encryption-algorithms}

TiDB でサポートされる TLS バージョン、キー交換プロトコル、暗号化アルゴリズムは、公式の Go ライブラリによって決定されます。

使用しているオペレーティング システムとクライアント ライブラリの暗号化ポリシーも、サポートされているプロトコルと暗号スイートのリストに影響する可能性があります。

### サポートされているTLSバージョン {#supported-tls-versions}

-   TLSv1.2
-   TLSv1.3

[`tls-version`](/tidb-configuration-file.md#tls-version)構成オプションを使用すると、使用できる TLS バージョンを制限できます。

実際に使用できる TLS バージョンは、OS の暗号化ポリシー、MySQL クライアントのバージョン、およびクライアントで使用される SSL/TLS ライブラリによって異なります。

### サポートされている鍵交換プロトコルと暗号化アルゴリズム {#supported-key-exchange-protocols-and-encryption-algorithms}

-   TLS_RSA_WITH_AES_128_CBC_SHA
-   TLS_RSA_WITH_AES_256_CBC_SHA
-   TLS_RSA_WITH_AES_128_CBC_SHA256
-   TLS_RSA_WITH_AES_128_GCM_SHA256
-   TLS_RSA_WITH_AES_256_GCM_SHA384
-   TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA
-   TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA
-   TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
-   TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA
-   TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
-   TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
-   TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
-   TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
-   TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
-   TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
-   TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256
-   TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256
-   TLS_AES_128_GCM_SHA256
-   TLS_AES_256_GCM_SHA384
-   TLS_CHACHA20_POLY1305_SHA256

## 証明書、キー、CA を再読み込みします {#reload-certificate-key-and-ca}

証明書、鍵、またはCAを置き換えるには、まず対応するファイルを置き換え、次に実行中のTiDBインスタンスで[`ALTER INSTANCE RELOAD TLS`](/sql-statements/sql-statement-alter-instance.md)ステートメントを実行して、証明書（ [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) ）、鍵（ [`ssl-key`](/tidb-configuration-file.md#ssl-key) ）、およびCA（ [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) ）を元の設定パスから再読み込みします。この方法では、TiDBインスタンスを再起動する必要はありません。

新しくロードされた証明書、鍵、およびCAは、ステートメントが正常に実行された後に確立された接続に対して有効になります。ステートメントの実行前に確立された接続には影響しません。

## 監視 {#monitoring}

TiDB v5.2.0 以降では、ステータス変数`Ssl_server_not_after`と`Ssl_server_not_before`使用して、証明書の有効期限の開始日と終了日を監視できます。

```sql
SHOW GLOBAL STATUS LIKE 'Ssl\_server\_not\_%';
```

    +-----------------------+--------------------------+
    | Variable_name         | Value                    |
    +-----------------------+--------------------------+
    | Ssl_server_not_after  | Nov 28 06:42:32 2021 UTC |
    | Ssl_server_not_before | Aug 30 06:42:32 2021 UTC |
    +-----------------------+--------------------------+
    2 rows in set (0.0076 sec)

## 参照 {#see-also}

-   [TiDB コンポーネント間の TLS を有効にする](/enable-tls-between-components.md) 。
