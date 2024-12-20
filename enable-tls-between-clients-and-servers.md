---
title: Enable TLS Between TiDB Clients and Servers
summary: データのセキュリティを確保するには、安全な接続を使用します。
---

# TiDBクライアントとサーバー間のTLSを有効にする {#enable-tls-between-tidb-clients-and-servers}

デフォルトでは、TiDB はサーバーとクライアント間の安全でない接続を許可します。これにより、チャネル トラフィックを監視する第三者は、クエリ コンテンツやクエリ結果など、サーバーとクライアント間で送受信されるデータを把握し、場合によっては変更することができます。チャネルが信頼できない場合 (クライアントがパブリック ネットワーク経由で TiDBサーバーに接続している場合など)、安全でない接続では情報漏洩が発生しやすくなります。この場合、セキュリティ上の理由から、TLS で保護された接続を要求することをお勧めします。

TiDBサーバーは、 TLS (Transport Layer Security) プロトコルに基づく安全な接続をサポートしています。このプロトコルは、MySQL の安全な接続と一致しており、MySQL Client、MySQL Shell、MySQL ドライバーなどの既存の MySQL クライアントによって直接サポートされています。TLS は、SSL (セキュリティ Sockets Layer) と呼ばれることもあります。SSL プロトコルには[既知のセキュリティ脆弱性](https://en.wikipedia.org/wiki/Transport_Layer_Security)があるため、TiDB は SSL をサポートしていません。TiDB は、TLSv1.2 および TLSv1.3 というプロトコルをサポートしています。

TLS で保護された接続を使用する場合、接続には次のセキュリティ プロパティがあります。

-   機密性: 盗聴を防ぐためにトラフィックの平文は暗号化されます
-   整合性: トラフィックの平文は改ざんできない
-   認証: (オプション) クライアントはサーバーのIDを検証でき、サーバーは中間者攻撃を回避するためにクライアントのIDを検証できます。

TLS で保護された接続を使用するには、まず TiDBサーバーを構成して TLS を有効にする必要があります。次に、クライアント アプリケーションを構成して TLS を使用する必要があります。ほとんどのクライアント ライブラリでは、サーバーで TLS サポートが正しく構成されている場合、TLS が自動的に有効になります。

MySQL と同様に、TiDB では同じ TCP ポートで TLS 接続と非 TLS 接続が許可されます。TLS が有効になっている TiDBサーバーでは、暗号化された接続を介して TiDBサーバーに安全に接続するか、暗号化されていない接続を使用するかを選択できます。安全な接続の使用を要求するには、次の方法を使用できます。

-   すべてのユーザーに対して TiDBサーバーへの安全な接続を要求するようにシステム変数[`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)を構成します。
-   ユーザーを作成する場合 ( `create user` )、または既存のユーザーを変更する場合 ( `alter user` ) に`REQUIRE SSL`指定します。これは、指定されたユーザーが TiDB にアクセスするために TLS 接続を使用する必要があることを指定するためです。以下は、ユーザーを作成する例です。

    ```sql
    CREATE USER 'u1'@'%' IDENTIFIED BY 'my_random_password' REQUIRE SSL;
    ```

> **注記：**
>
> ログイン ユーザーが[ログインのための TiDB 証明書ベースの認証](/certificate-authentication.md#configure-the-user-certificate-information-for-login-verification)使用して設定した場合、ユーザーは暗黙的に TiDB への暗号化された接続を有効にする必要があります。

## 安全な接続を使用するように TiDBサーバーを構成する {#configure-tidb-server-to-use-secure-connections}

安全な接続を有効にするための関連パラメータについては、次の説明を参照してください。

-   [`auto-tls`](/tidb-configuration-file.md#auto-tls) : 自動証明書生成を有効にする (v5.2.0 以降)
-   [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) : SSL証明書のファイルパスを指定します
-   [`ssl-key`](/tidb-configuration-file.md#ssl-key) : 証明書に一致する秘密鍵を指定します
-   [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) : (オプション) 信頼されたCA証明書のファイルパスを指定します
-   [`tls-version`](/tidb-configuration-file.md#tls-version) : (オプション) 最小の TLS バージョンを指定します (例: &quot;TLSv1.2&quot;)

`auto-tls`安全な接続を許可しますが、クライアント証明書の検証は提供しません。証明書の検証と証明書の生成方法の制御については、以下の`ssl-cert` 、および`ssl-key`変数の設定に関するアドバイスを参照して`ssl-ca` 。

TiDBサーバーで独自の証明書を使用して安全な接続を有効にするには、TiDBサーバーの起動時に構成ファイルで`ssl-cert`と`ssl-key`の両方のパラメータを指定する必要があります。クライアント認証用に`ssl-ca`パラメータを指定することもできます ( [認証を有効にする](#enable-authentication)を参照)。

パラメータで指定するファイルはすべて PEM (Privacy Enhanced Mail) 形式です。現在、TiDB はパスワードで保護された秘密鍵のインポートをサポートしていないため、パスワードなしの秘密鍵ファイルを提供する必要があります。証明書または秘密鍵が無効な場合、TiDBサーバーは通常どおり起動しますが、クライアントは TLS 接続を介して TiDBサーバーに接続できません。

証明書パラメータが正しい場合、TiDB は起動時に`"INFO"`レベルのログに`mysql protocol server secure connection is enabled`出力します。

## TLS接続を使用するようにMySQLクライアントを構成する {#configure-the-mysql-client-to-use-tls-connections}

MySQL 5.7以降のバージョンのクライアントは、デフォルトで TLS 接続を確立しようとします。サーバーがTLS 接続をサポートしていない場合は、自動的に暗号化されていない接続に戻ります。バージョン 5.7 より前の MySQL クライアントは、デフォルトで非 TLS 接続を使用します。

次の`--ssl-mode`のパラメータを使用して、クライアントの接続動作を変更できます。

-   `--ssl-mode=REQUIRED` : クライアントは TLS 接続を必要とします。サーバー側が TLS 接続をサポートしていない場合、接続を確立できません。
-   `--ssl-mode`パラメータがない場合: クライアントは TLS 接続を使用しようとしますが、サーバー側が暗号化接続をサポートしていない場合は暗号化接続を確立できません。その場合、クライアントは暗号化されていない接続を使用します。
-   `--ssl-mode=DISABLED` : クライアントは暗号化されていない接続を使用します。

MySQL 8.x クライアントには、このパラメータに加えて 2 つの SSL モードがあります。

-   `--ssl-mode=VERIFY_CA` : `--ssl-ca`必要とする CA に対してサーバーからの証明書を検証します。
-   `--ssl-mode=VERIFY_IDENTITY` : `VERIFY_CA`と同じですが、接続先のホスト名が証明書と一致するかどうかも検証します。

MySQL 5.7および MariaDB クライアント以前では、 `--ssl-verify-server-cert`使用してサーバー証明書の検証を有効にすることができます。

詳細については、MySQL の[暗号化された接続のクライアント側コンフィグレーション](https://dev.mysql.com/doc/refman/8.0/en/using-encrypted-connections.html#using-encrypted-connections-client-side-configuration)参照してください。

## 認証を有効にする {#enable-authentication}

TiDBサーバーまたは MySQL クライアントで`ssl-ca`パラメータが指定されていない場合、クライアントまたはサーバーはデフォルトで認証を実行せず、中間者攻撃を防ぐことができません。たとえば、クライアントは偽装されたクライアントに「安全に」接続する可能性があります。サーバーとクライアントで認証の`ssl-ca`パラメータを設定できます。通常は、サーバーを認証するだけで済みますが、セキュリティをさらに強化するためにクライアントを認証することもできます。

-   MySQL クライアントから TiDBサーバーを認証するには:
    1.  TiDBサーバーで`ssl-cert`と`ssl-key`パラメータを指定します。
    2.  MySQL クライアントで`--ssl-ca`パラメータを指定します。
    3.  MySQL クライアントでは少なくとも`--ssl-mode` ～ `VERIFY_CA`指定します。
    4.  TiDBサーバーに設定されている証明書（ `ssl-cert` ）がクライアント`--ssl-ca`パラメータで指定されたCAによって署名されていることを確認してください。そうでない場合、認証は失敗します。

-   TiDBサーバーから MySQL クライアントを認証するには:
    1.  TiDBサーバーで`ssl-cert` 、および`ssl-key`パラメータ`ssl-ca`指定します。
    2.  クライアントでパラメータ`--ssl-cert`と`--ssl-key`指定します。
    3.  サーバー側で設定された証明書とクライアント側で設定された証明書の両方が、サーバーによって指定された`ssl-ca`によって署名されていることを確認します。

<!---->

-   相互認証を実行するには、上記の両方の要件を満たします。

デフォルトでは、サーバーからクライアントへの認証はオプションです。クライアントが TLS ハンドシェイク中に身分証明書を提示しない場合でも、TLS 接続を確立できます。ユーザーの作成時 ( `CREATE USER` )、または既存のユーザーの変更時 ( `ALTER USER` ) に`REQUIRE x509`指定して、クライアントの認証を要求することもできます。以下は、ユーザーの作成例です。

```sql
CREATE USER 'u1'@'%'  REQUIRE X509;
```

> **注記：**
>
> ログイン ユーザーが[ログインのための TiDB 証明書ベースの認証](/certificate-authentication.md#configure-the-user-certificate-information-for-login-verification)使用して設定した場合、ユーザーは暗黙的に TiDB への TLS 接続を有効にする必要があります。

## 現在の接続が暗号化を使用しているかどうかを確認します {#check-whether-the-current-connection-uses-encryption}

`SHOW STATUS LIKE "%Ssl%";`ステートメントを使用して、暗号化が使用されているかどうか、暗号化された接続で使用される暗号化プロトコル、TLS バージョン番号など、現在の接続の詳細を取得します。

暗号化された接続の結果の次の例を参照してください。結果は、クライアントがサポートする TLS バージョンまたは暗号化プロトコルによって異なります。

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

使用しているオペレーティング システムとクライアント ライブラリの暗号化ポリシーも、サポートされているプロトコルと暗号スイートのリストに影響を与える可能性があります。

### サポートされているTLSバージョン {#supported-tls-versions}

-   TLSv1.2
-   TLSv1.3

[`tls-version`](/tidb-configuration-file.md#tls-version)構成オプションを使用すると、使用できる TLS バージョンを制限できます。

実際に使用できる TLS バージョンは、OS 暗号化ポリシー、MySQL クライアント バージョン、およびクライアントが使用する SSL/TLS ライブラリによって異なります。

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

## 証明書、キー、CAを再読み込みする {#reload-certificate-key-and-ca}

証明書、キー、または CA を置き換えるには、まず対応するファイルを置き換え、次に実行中の TiDB インスタンスで[`ALTER INSTANCE RELOAD TLS`](/sql-statements/sql-statement-alter-instance.md)ステートメントを実行して、証明書 ( [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) )、キー ( [`ssl-key`](/tidb-configuration-file.md#ssl-key) )、および CA ( [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) ) を元の構成パスから再ロードします。この方法では、TiDB インスタンスを再起動する必要はありません。

新しくロードされた証明書、キー、および CA は、ステートメントが正常に実行された後に確立された接続で有効になります。ステートメントの実行前に確立された接続は影響を受けません。

## 監視 {#monitoring}

TiDB v5.2.0 以降では、ステータス変数`Ssl_server_not_after`と`Ssl_server_not_before`を使用して、証明書の有効期限の開始日と終了日を監視できます。

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
