---
title: Enable TLS Between TiDB Clients and Servers
summary: Use the encrypted connection to ensure data security.
---

# TiDBクライアントとサーバー間のTLSを有効にする {#enable-tls-between-tidb-clients-and-servers}

TiDBのサーバーとクライアント間の暗号化されていない接続はデフォルトで許可されます。これにより、チャネルトラフィックを監視するサードパーティは、クエリコンテンツ、クエリ結果などを含むがこれらに限定されない、サーバーとクライアント間で送受信されるデータを知ることができます。 。チャネルが信頼できない場合（クライアントがパブリックネットワークを介してTiDBサーバーに接続されている場合など）、暗号化されていない接続では情報が漏洩する傾向があります。この場合、セキュリティ上の理由から、暗号化された接続を要求することをお勧めします。

TiDBサーバーは、TLS（Transport Layer Security）に基づく暗号化された接続をサポートします。プロトコルはMySQL暗号化接続と一貫性があり、MySQLクライアント、MySQLシェル、MySQLドライバーなどの既存のMySQLクライアントによって直接サポートされます。 TLSはSSL（セキュリティ Sockets Layer）と呼ばれることもあります。 SSLプロトコルには[既知のセキュリティの脆弱性](https://en.wikipedia.org/wiki/Transport_Layer_Security)があるため、TiDBはSSLをサポートしていません。 TiDBは、TLSv1.0、TLSv1.1、TLSv1.2、およびTLSv1.3のプロトコルをサポートしています。

暗号化された接続を使用する場合、接続には次のセキュリティプロパティがあります。

-   機密性：トラフィックの平文は盗聴を避けるために暗号化されています
-   整合性：トラフィックの平文を改ざんすることはできません
-   認証:(オプション）クライアントはサーバーのIDを確認でき、サーバーはクライアントのIDを確認して、man-in-the-middle攻撃を回避できます。

TLSで保護された接続を使用するには、最初にTLSを有効にするようにTiDBサーバーを構成する必要があります。次に、TLSを使用するようにクライアントアプリケーションを構成する必要があります。サーバーでTLSサポートが正しく構成されている場合、ほとんどのクライアントライブラリはTLSを自動的に有効にします。

MySQLと同様に、TiDBは同じTCPポートでTLS接続と非TLS接続を許可します。 TLSが有効になっているTiDBサーバーの場合、暗号化された接続を介してTiDBサーバーに安全に接続するか、暗号化されていない接続を使用するかを選択できます。次の方法を使用して、安全な接続の使用を要求できます。

-   すべてのユーザーにTiDBサーバーへの安全な接続を要求するようにシステム変数`require_secure_transport`を構成します。
-   ユーザーを作成するときは`REQUIRE SSL`を指定し（ `create user` ）、既存のユーザーを変更するときは（ `alter user` ）、指定したユーザーがTiDBにアクセスするために暗号化された接続を使用する必要があることを指定します。以下は、ユーザーの作成例です。

    {{< copyable "" >}}

    ```sql
    CREATE USER 'u1'@'%' IDENTIFIED BY 'my_random_password' REQUIRE SSL;
    ```

> **ノート：**
>
> ログインユーザーが[ログイン用のTiDB証明書ベースの認証](/certificate-authentication.md#configure-the-user-certificate-information-for-login-verification)を使用して構成した場合、ユーザーはTiDBへの暗号化された接続を有効にする必要があります。

## 安全な接続を使用するようにTiDBサーバーを構成する {#configure-tidb-server-to-use-secure-connections}

安全な接続を有効にするための関連パラメーターについては、以下の説明を参照してください。

-   [`auto-tls`](/tidb-configuration-file.md#auto-tls) ：自動証明書生成を有効にします（v5.2.0以降）
-   [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) ：SSL証明書のファイルパスを指定します
-   [`ssl-key`](/tidb-configuration-file.md#ssl-key) ：証明書と一致する秘密鍵を指定します
-   [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) :(オプション）信頼できるCA証明書のファイルパスを指定します
-   [`tls-version`](/tidb-configuration-file.md#tls-version) :(オプション）最小TLSバージョンを指定します（例： &quot;TLSv1.2&quot;）

`auto-tls`は安全な接続を許可しますが、クライアント証明書の検証は提供しません。証明書の検証、および証明書の生成方法を制御するには、以下の`ssl-cert` 、および`ssl-key`変数の構成に関するアドバイスを参照して`ssl-ca` 。

TiDBサーバーで独自の証明書を使用して安全な接続を有効にするには、TiDBサーバーを起動するときに、構成ファイルで`ssl-cert`と`ssl-key`の両方のパラメーターを指定する必要があります。クライアント認証用に`ssl-ca`パラメーターを指定することもできます（ [認証を有効にする](#enable-authentication)を参照）。

パラメータで指定されたすべてのファイルは、PEM（Privacy Enhanced Mail）形式です。現在、TiDBはパスワードで保護された秘密鍵のインポートをサポートしていないため、パスワードなしで秘密鍵ファイルを提供する必要があります。証明書または秘密鍵が無効な場合、TiDBサーバーは通常どおり起動しますが、クライアントは暗号化された接続を介してTiDBサーバーに接続できません。

証明書パラメーターが正しい場合、TiDBは開始時に`secure connection is enabled`を出力します。それ以外の場合は、 `secure connection is NOT ENABLED`を出力します。

v5.2.0より前のバージョンのTiDBの場合、 `mysql_ssl_rsa_setup --datadir=./certs`を使用して証明書を生成できます。 `mysql_ssl_rsa_setup`ツールはMySQLサーバーの一部です。

## 暗号化された接続を使用するようにMySQLクライアントを構成する {#configure-the-mysql-client-to-use-encrypted-connections}

MySQL 5.7以降のバージョンのクライアントは、デフォルトで暗号化された接続を確立しようとします。サーバーが暗号化された接続をサポートしていない場合、サーバーは自動的に暗号化されていない接続に戻ります。バージョン5.7より前のMySQLのクライアントは、デフォルトで暗号化されていない接続を使用します。

次の`--ssl-mode`つのパラメータを使用して、クライアントの接続動作を変更できます。

-   `--ssl-mode=REQUIRED` ：クライアントには暗号化された接続が必要です。サーバー側が暗号化された接続をサポートしていない場合、接続を確立できません。
-   `--ssl-mode`つのパラメーターがない場合：クライアントは暗号化された接続を使用しようとしますが、サーバー側が暗号化された接続をサポートしていない場合、暗号化された接続を確立できません。次に、クライアントは暗号化されていない接続を使用します。
-   `--ssl-mode=DISABLED` ：クライアントは暗号化されていない接続を使用します。

MySQL 8.0クライアントには、このパラメーターに加えて2つのSSLモードがあります。

-   `--ssl-mode=VERIFY_CA` ： `--ssl-ca`を必要とするCAに対して、サーバーからの証明書を検証します。
-   `--ssl-mode=VERIFY_IDENTITY` ： `VERIFY_CA`と同じですが、接続先のホスト名が証明書と一致するかどうかも検証します。

詳細については、MySQLの[暗号化された接続のクライアント側のConfiguration / コンフィグレーション](https://dev.mysql.com/doc/refman/5.7/en/using-encrypted-connections.html#using-encrypted-connections-client-side-configuration)を参照してください。

## 認証を有効にする {#enable-authentication}

TiDBサーバーまたはMySQLクライアントで`ssl-ca`パラメーターが指定されていない場合、クライアントまたはサーバーはデフォルトで認証を実行せず、man-in-the-middle攻撃を防ぐことができません。たとえば、クライアントは偽装されたクライアントに「安全に」接続する場合があります。サーバーとクライアントでの認証用に`ssl-ca`のパラメーターを構成できます。通常、サーバーを認証するだけで済みますが、クライアントを認証してセキュリティをさらに強化することもできます。

-   MySQLクライアントからTiDBサーバーを認証するには：
    1.  TiDBサーバーで`ssl-cert`と`ssl-key`のパラメーターを指定します。
    2.  MySQLクライアントで`--ssl-ca`つのパラメーターを指定します。
    3.  少なくともMySQLクライアントでは`--ssl-mode`から`VERIFY_CA`を指定します。
    4.  TiDBサーバーで構成された証明書（ `ssl-cert` ）が、クライアント`--ssl-ca`パラメーターで指定されたCAによって署名されていることを確認してください。それ以外の場合、認証は失敗します。

-   TiDBサーバーからMySQLクライアントを認証するには：
    1.  TiDBサーバーで`ssl-cert` 、および`ssl-key`パラメーターを指定し`ssl-ca` 。
    2.  クライアントで`--ssl-cert`と`--ssl-key`のパラメーターを指定します。
    3.  サーバー構成の証明書とクライアント構成の証明書の両方が、サーバーによって指定された`ssl-ca`によって署名されていることを確認してください。

<!---->

-   相互認証を実行するには、上記の両方の要件を満たします。

デフォルトでは、サーバーからクライアントへの認証はオプションです。クライアントがTLSハンドシェイク中に識別証明書を提示しなくても、TLS接続を確立できます。また、ユーザーの作成時（ `create user` ）、権限の付与時（ `grant` ）、または既存のユーザーの変更時（ `alter user` ）に`require x509`を指定して、クライアントの認証を要求することもできます。以下は、ユーザーの作成例です。

{{< copyable "" >}}

```sql
create user 'u1'@'%'  require x509;
```

> **ノート：**
>
> ログインユーザーが[ログイン用のTiDB証明書ベースの認証](/certificate-authentication.md#configure-the-user-certificate-information-for-login-verification)を使用して構成した場合、ユーザーはTiDBへの暗号化された接続を有効にする必要があります。

## 現在の接続が暗号化を使用しているかどうかを確認します {#check-whether-the-current-connection-uses-encryption}

`SHOW STATUS LIKE "%Ssl%";`ステートメントを使用して、暗号化が使用されているかどうか、暗号化された接続で使用されている暗号化プロトコル、TLSバージョン番号など、現在の接続の詳細を取得します。

暗号化された接続での結果の次の例を参照してください。結果は、クライアントがサポートするさまざまなTLSバージョンまたは暗号化プロトコルに応じて変わります。

```
mysql> SHOW STATUS LIKE "%Ssl%";
......
| Ssl_verify_mode | 5                            |
| Ssl_version     | TLSv1.2                      |
| Ssl_cipher      | ECDHE-RSA-AES128-GCM-SHA256  |
......
```

公式のMySQLクライアントの場合、 `STATUS`または`\s`ステートメントを使用して接続ステータスを表示することもできます。

```
mysql> \s
...
SSL: Cipher in use is ECDHE-RSA-AES128-GCM-SHA256
...
```

## サポートされているTLSバージョン、鍵交換プロトコル、および暗号化アルゴリズム {#supported-tls-versions-key-exchange-protocols-and-encryption-algorithms}

TiDBでサポートされているTLSバージョン、鍵交換プロトコル、および暗号化アルゴリズムは、公式のGolangライブラリによって決定されます。

オペレーティングシステムと使用しているクライアントライブラリの暗号化ポリシーも、サポートされているプロトコルと暗号スイートのリストに影響を与える可能性があります。

### サポートされているTLSバージョン {#supported-tls-versions}

-   TLSv1.0（デフォルトでは無効）
-   TLSv1.1
-   TLSv1.2
-   TLSv1.3

`tls-version`構成オプションを使用して、使用できるTLSバージョンを制限できます。

使用できる実際のTLSバージョンは、OS暗号化ポリシー、MySQLクライアントのバージョン、およびクライアントが使用するSSL/TLSライブラリによって異なります。

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

## 証明書、キー、およびCAをリロードします {#reload-certificate-key-and-ca}

証明書、キー、またはCAを置き換えるには、最初に対応するファイルを置き換え、次に実行中のTiDBインスタンスで[`ALTER INSTANCE RELOAD TLS`](/sql-statements/sql-statement-alter-instance.md)ステートメントを実行して、元の構成から証明書（ [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) ）、キー（ [`ssl-key`](/tidb-configuration-file.md#ssl-key) ）、およびCA（ [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) ）を再ロードします。道。このように、TiDBインスタンスを再起動する必要はありません。

新しくロードされた証明書、キー、およびCAは、ステートメントが正常に実行された後に確立された接続で有効になります。ステートメントの実行前に確立された接続は影響を受けません。

## モニタリング {#monitoring}

TiDB v5.2.0以降、 `Ssl_server_not_after`および`Ssl_server_not_before`ステータス変数を使用して、証明書の有効性の開始日と終了日を監視できます。

```sql
SHOW GLOBAL STATUS LIKE 'Ssl\_server\_not\_%';
```

```
+-----------------------+--------------------------+
| Variable_name         | Value                    |
+-----------------------+--------------------------+
| Ssl_server_not_after  | Nov 28 06:42:32 2021 UTC |
| Ssl_server_not_before | Aug 30 06:42:32 2021 UTC |
+-----------------------+--------------------------+
2 rows in set (0.0076 sec)
```

## も参照してください {#see-also}

-   [TiDBコンポーネント間のTLSを有効にする](/enable-tls-between-components.md) 。
