---
title: Enable TLS Between TiDB Clients and Servers
summary: データセキュリティを確保するため、安全な接続を使用してください。
---

# TiDBクライアントとサーバー間でTLSを有効にする {#enable-tls-between-tidb-clients-and-servers}

TiDBはデフォルトでは、サーバーとクライアント間の安全でない接続を許可します。これにより、チャネルトラフィックを監視する第三者は、クエリの内容や結果を含む、サーバーとクライアント間で送受信されるデータを把握し、場合によっては改ざんすることが可能になります。チャネルが信頼できない場合（例えば、クライアントがパブリックネットワーク経由でTiDBサーバーに接続されている場合）、安全でない接続は情報漏洩のリスクが高まります。このような場合は、セキュリティ上の理由から、TLSで保護された接続を必須とすることをお勧めします。

TiDBサーバーは、TLS（Transport Layer Security）プロトコルに基づくセキュアな接続をサポートしています。このプロトコルはMySQLのセキュアな接続と互換性があり、MySQLクライアント、MySQLシェル、MySQLドライバなどの既存のMySQLクライアントで直接サポートされています。TLSはSSL（セキュリティ [既知のセキュリティ脆弱性](https://en.wikipedia.org/wiki/Transport_Layer_Security)Layer）と呼ばれることもあります。SSLプロトコルには があるため、TiDBはSSLをサポートしていません。TiDBはTLSv1.2とTLSv1.3をサポートしています。

TLSで保護された接続を使用する場合、その接続には以下のセキュリティ特性があります。

-   機密性：盗聴を防ぐため、通信内容は暗号化されます。
-   完全性：通信内容の平文は改ざんできない
-   認証：（オプション）中間者攻撃を回避するために、クライアントはサーバーの身元を確認し、サーバーはクライアントの身元を確認することができます。

TLSで保護された接続を使用するには、まずTiDBサーバーでTLSを有効にするように設定する必要があります。次に、クライアントアプリケーションでTLSを使用するように設定する必要があります。ほとんどのクライアントライブラリは、サーバーでTLSサポートが正しく設定されていれば、TLSを自動的に有効にします。

MySQLと同様に、TiDBは同じTCPポート上でTLS接続と非TLS接続の両方を許可します。TLSが有効になっているTiDBサーバーの場合、暗号化された接続を介してTiDBサーバーに安全に接続するか、暗号化されていない接続を使用するかを選択できます。安全な接続の使用を必須にするには、次の方法を使用できます。

-   システム変数[`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)を設定して、すべてのユーザーが TiDBサーバーへの安全な接続を必須とするようにします。
-   ユーザーを作成するとき（ `REQUIRE SSL` 、または既存のユーザーを変更するとき（ `CREATE USER` ）に`ALTER USER`を指定すると、指定されたユーザーはTiDBにアクセスするためにTLS接続を使用する必要があることが指定されます。以下は、ユーザーを作成する例です。

    ```sql
    CREATE USER 'u1'@'%' IDENTIFIED BY 'my_random_password' REQUIRE SSL;
    ```

> **Note:**
>
> ログイン ユーザーが[TiDBの証明書ベース認証によるログイン](/certificate-authentication.md#configure-the-user-certificate-information-for-login-verification)を使用して設定した場合、ユーザーは TiDB への暗号化された接続を有効にすることが暗黙的に要求されます。

## TiDBサーバーをセキュア接続を使用するように設定する {#configure-tidb-server-to-use-secure-connections}

安全な接続を有効にするための関連パラメータについては、以下の説明を参照してください。

-   [`auto-tls`](/tidb-configuration-file.md#auto-tls) ：証明書の自動生成を有効にする（バージョン5.2.0以降）
-   [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) ：SSL証明書のファイルパスを指定します。
-   [`ssl-key`](/tidb-configuration-file.md#ssl-key) : 証明書に一致する秘密鍵を指定します。
-   [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) : (オプション) 信頼済みCA証明書のファイルパスを指定します
-   [`tls-version`](/tidb-configuration-file.md#tls-version) : (オプション) 最小TLSバージョンを指定します。例: &quot;TLSv1.2&quot;

`auto-tls`安全な接続を可能にしますが、クライアント証明書の検証は提供しません。証明書の検証、および証明書の生成方法を制御するには、以下の`ssl-cert` 、 `ssl-key` 、および`ssl-ca`変数の設定に関するアドバイスを参照してください。

TiDBサーバーで独自の証明書を使用して安全な接続を有効にするには、TiDBサーバーを起動する際に、構成ファイルで`ssl-cert`と`ssl-key`両方のパラメータを指定する必要があります。サーバー認証のために`ssl-ca`パラメータを指定することもできます（[認証を有効にする](#enable-authentication)）。

パラメータで指定されるファイルはすべてPEM（Privacy Enhanced Mail）形式です。現在、TiDBはパスワードで保護された秘密鍵のインポートをサポートしていないため、パスワードなしの秘密鍵ファイルを提供する必要があります。証明書または秘密鍵が無効な場合、TiDBサーバーは通常どおり起動しますが、クライアントはTLS接続を介してTiDBサーバーに接続できません。

証明書のパラメータが正しい場合、TiDB は起動時に`mysql protocol server secure connection is enabled`を`"INFO"`レベルのログに出力します。

## TiProxyがTLS接続を使用するように設定する {#configure-tiproxy-to-use-tls-connections}

[TiProxy](/tiproxy/tiproxy-overview.md)でTLS接続を有効にするには、TiProxy設定ファイルで[`sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls)設定項目を指定します。この設定の詳細とバックエンド接続でTLSを有効にする方法については、 [TiProxyのセキュリティ](/tiproxy/tiproxy-overview.md#security)参照してください。

## MySQLクライアントをTLS接続を使用するように設定する {#configure-the-mysql-client-to-use-tls-connections}

MySQL 5.7以降のバージョンのクライアントは、デフォルトでTLS接続を確立しようとします。サーバーがTLS接続をサポートしていない場合、自動的に暗号化されていない接続に切り替わります。MySQL 5.7より前のバージョンのクライアントは、デフォルトでTLSを使用しない接続を使用します。

以下の`--ssl-mode`パラメータを使用すると、クライアントの接続動作を変更できます。

-   `--ssl-mode=REQUIRED` : クライアントはTLS接続を必要とします。サーバー側がTLS接続をサポートしていない場合、接続を確立できません。
-   `--ssl-mode`パラメータがない場合: クライアントは TLS 接続を使用しようとしますが、サーバー側が暗号化接続をサポートしていない場合は、暗号化接続を確立できません。その場合、クライアントは暗号化されていない接続を使用します。
-   `--ssl-mode=DISABLED` : クライアントは暗号化されていない接続を使用しています。

MySQL 8.xクライアントには、このパラメータに加えて2つのSSLモードがあります。

-   `--ssl-mode=VERIFY_CA` : `--ssl-ca`を必要とする CA に対してサーバーからの証明書を検証します。
-   `--ssl-mode=VERIFY_IDENTITY` : `VERIFY_CA`と同じですが、接続先のホスト名が証明書と一致するかどうかも検証します。

MySQL 5.7および MariaDB クライアント以前のバージョンでは、 `--ssl-verify-server-cert`を使用してサーバー証明書の検証を有効にできます。

詳細については、「MySQL の[暗号化接続のためのクライアント側コンフィグレーション](https://dev.mysql.com/doc/refman/8.0/en/using-encrypted-connections.html#using-encrypted-connections-client-side-configuration)参照してください。

## 認証を有効にする {#enable-authentication}

TiDBサーバーまたはMySQLクライアントで`ssl-ca`パラメータが指定されていない場合、クライアントまたはサーバーはデフォルトで認証を実行せず、中間者攻撃を防ぐことができません。たとえば、クライアントが偽装されたクライアントに「安全に」接続してしまう可能性があります。サーバーとクライアントの両方で`ssl-ca`パラメータを設定して認証を行うことができます。通常はサーバーの認証のみが必要ですが、クライアントの認証も行うことでセキュリティをさらに強化できます。

-   MySQLクライアントからTiDBサーバーを認証するには：
    1.  TiDBサーバーで`ssl-cert`および`ssl-key`パラメータを指定します。
    2.  MySQLクライアントで`--ssl-ca`パラメータを指定します。
    3.  MySQLクライアントで、 `--ssl-mode`から`VERIFY_CA`までを指定してください。
    4.  TiDBサーバーに設定されている証明書（ `ssl-cert` ）が、クライアントの`--ssl-ca`パラメータで指定されたCAによって署名されていることを確認してください。そうでない場合、認証は失敗します。

-   TiDBサーバーからMySQLクライアントを認証するには：
    1.  TiDBサーバーで`ssl-cert` 、 `ssl-key` 、および`ssl-ca`パラメーターを指定します。
    2.  クライアントで`--ssl-cert`および`--ssl-key`パラメータを指定します。
    3.  サーバーで設定された証明書とクライアントで設定された証明書の両方が、サーバーで指定された`ssl-ca`によって署名されていることを確認してください。

<!---->

-   相互認証を行うには、上記の2つの要件を満たす必要があります。

デフォルトでは、サーバーとクライアント間の認証はオプションです。TLS ハンドシェイク中にクライアントが識別証明書を提示しなくても、TLS 接続は確立できます。ユーザーを作成するとき`REQUIRE x509` 、または既存のユーザーを変更するとき ( `CREATE USER` ) に`ALTER USER` } を指定することで、クライアントの認証を必須にすることもできます。以下は、ユーザーを作成する例です。

```sql
CREATE USER 'u1'@'%' REQUIRE X509;
```

> **Note:**
>
> ログイン ユーザーが[TiDBの証明書ベース認証によるログイン](/certificate-authentication.md#configure-the-user-certificate-information-for-login-verification)使用して設定した場合、ユーザーは TiDB への TLS 接続を有効にすることが暗黙的に要求されます。

## 現在の接続が暗号化を使用しているかどうかを確認してください。 {#check-whether-the-current-connection-uses-encryption}

`SHOW STATUS LIKE "%Ssl%";`ステートメントを使用すると、暗号化が使用されているかどうか、暗号化された接続で使用される暗号化プロトコル、TLS バージョン番号など、現在の接続の詳細を取得できます。

暗号化接続における結果の例を以下に示します。結果は、クライアントがサポートするTLSバージョンや暗号化プロトコルによって異なります。

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

`Ssl_cipher`の値が空でない場合、接続は暗号化されます。

公式のMySQLクライアントでは、 `STATUS`または`\s`ステートメントを使用して接続ステータスを表示することもできます。

    mysql> \s
    ...
    SSL: Cipher in use is TLS_AES_128_GCM_SHA256
    ...

## サポートされているTLSバージョン、鍵交換プロトコル、および暗号化アルゴリズム {#supported-tls-versions-key-exchange-protocols-and-encryption-algorithms}

TiDBがサポートするTLSバージョン、鍵交換プロトコル、暗号化アルゴリズムは、公式のGoライブラリによって決定されます。

お使いのオペレーティングシステムおよび使用しているクライアントライブラリの暗号化ポリシーも、サポートされるプロトコルと暗号スイートのリストに影響を与える可能性があります。

### サポートされているTLSバージョン {#supported-tls-versions}

-   TLSv1.2
-   TLSv1.3

[`tls-version`](/tidb-configuration-file.md#tls-version)設定オプションを使用すると、使用できるTLSバージョンを制限できます。

実際に使用できるTLSバージョンは、OSの暗号化ポリシー、MySQLクライアントのバージョン、およびクライアントが使用するSSL/TLSライブラリによって異なります。

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

## 証明書、キー、およびCAを再読み込みします。 {#reload-certificate-key-and-ca}

証明書、キー、または認証局 (CA) を交換するには、まず対応するファイルを置き換えてから、実行中の TiDB インスタンスで[`ALTER INSTANCE RELOAD TLS`](/sql-statements/sql-statement-alter-instance.md)ステートメントを実行し、元の構成パスから証明書 ( [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) )、キー ( [`ssl-key`](/tidb-configuration-file.md#ssl-key) )、および認証局 ( [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) ) を再ロードします。この方法であれば、TiDB インスタンスを再起動する必要はありません。

新しく読み込まれた証明書、鍵、および認証局は、ステートメントが正常に実行された後に確立された接続に適用されます。ステートメントの実行前に確立された接続には影響しません。

## 監視 {#monitoring}

TiDB v5.2.0以降では、 `Ssl_server_not_after`および`Ssl_server_not_before`ステータス変数を使用して、証明書の有効期間の開始日と終了日を監視できます。

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

## 関連項目 {#see-also}

-   [TiDBコンポーネント間でTLSを有効にする](/enable-tls-between-components.md)。
