---
title: Enable TLS Between TiDB Clients and Servers
summary: Use the encrypted connection to ensure data security.
---

# TiDB クライアントとサーバーの間で TLS を有効にする {#enable-tls-between-tidb-clients-and-servers}

TiDB のサーバーとクライアント間の非暗号化接続はデフォルトで許可されており、これにより、チャネル トラフィックを監視するサードパーティは、サーバーとクライアントの間で送受信されるデータ (クエリ内容やクエリ結果など) を知ることができます。チャネルが信頼できない場合 (クライアントがパブリック ネットワーク経由で TiDBサーバーに接続している場合など)、暗号化されていない接続では情報漏洩が発生する可能性があります。この場合、セキュリティ上の理由から、暗号化された接続を要求することをお勧めします。

TiDBサーバーは、 TLS (Transport Layer Security) に基づく暗号化接続をサポートしています。このプロトコルは MySQL 暗号化接続と一致しており、MySQL クライアント、MySQL シェル、MySQL ドライバーなどの既存の MySQL クライアントによって直接サポートされています。 TLS は、SSL (セキュリティ Sockets Layer) と呼ばれることもあります。 SSL プロトコルには[既知のセキュリティ脆弱性](https://en.wikipedia.org/wiki/Transport_Layer_Security)あるため、TiDB は SSL をサポートしません。 TiDB は、TLSv1.0、TLSv1.1、TLSv1.2、および TLSv1.3 のプロトコルをサポートします。

暗号化された接続が使用される場合、接続には次のセキュリティ特性があります。

-   機密性: トラフィックの平文は盗聴を避けるために暗号化されます。
-   整合性: トラフィックの平文は改ざんできません
-   認証: (オプション) クライアントはサーバーの ID を検証し、サーバーは中間者攻撃を回避するためにクライアントの ID を検証できます。

TLS で保護された接続を使用するには、まず TLS を有効にするように TiDBサーバーを構成する必要があります。次に、TLS を使用するようにクライアント アプリケーションを構成する必要があります。サーバーで TLS サポートが正しく構成されている場合、ほとんどのクライアント ライブラリは TLS を自動的に有効にします。

MySQL と同様に、TiDB では、同じ TCP ポート上で TLS 接続と非 TLS 接続が可能です。 TLS が有効になっている TiDBサーバーの場合、暗号化された接続を通じて TiDBサーバーに安全に接続するか、暗号化されていない接続を使用するかを選択できます。次の方法を使用して、安全な接続の使用を要求できます。

-   すべてのユーザーに対して TiDBサーバーへの安全な接続を要求するようにシステム変数`require_secure_transport`を構成します。
-   ユーザーを作成する場合 ( `create user` )、または既存のユーザーを変更する場合 ( `alter user` ) に`REQUIRE SSL`指定します。これは、指定されたユーザーが TiDB にアクセスするために暗号化された接続を使用する必要があることを指定します。ユーザーを作成する例を次に示します。

    ```sql
    CREATE USER 'u1'@'%' IDENTIFIED BY 'my_random_password' REQUIRE SSL;
    ```

> **注記：**
>
> ログイン ユーザーが[TiDB 証明書ベースのログイン認証](/certificate-authentication.md#configure-the-user-certificate-information-for-login-verification)使用して設定した場合、ユーザーは TiDB への暗号化された接続を有効にすることが暗黙的に要求されます。

## 安全な接続を使用するように TiDBサーバーを構成する {#configure-tidb-server-to-use-secure-connections}

安全な接続を有効にするための関連パラメータについては、次の説明を参照してください。

-   [`auto-tls`](/tidb-configuration-file.md#auto-tls) : 証明書の自動生成を有効にします (v5.2.0 以降)
-   [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) : SSL証明書のファイルパスを指定します。
-   [`ssl-key`](/tidb-configuration-file.md#ssl-key) : 証明書と一致する秘密キーを指定します
-   [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) : (オプション) 信頼された CA 証明書のファイル パスを指定します。
-   [`tls-version`](/tidb-configuration-file.md#tls-version) : (オプション) 最小の TLS バージョンを指定します (例: 「TLSv1.2」)。

`auto-tls`安全な接続を許可しますが、クライアント証明書の検証は提供しません。証明書の検証と証明書の生成方法の制御については、以下の`ssl-cert` 、 `ssl-key` 、および`ssl-ca`変数の構成に関するアドバイスを参照してください。

TiDBサーバーで独自の証明書を使用した安全な接続を有効にするには、TiDBサーバーの起動時に構成ファイルで`ssl-cert`と`ssl-key`の両方のパラメーターを指定する必要があります。クライアント認証に`ssl-ca`パラメータを指定することもできます ( [認証を有効にする](#enable-authentication)を参照)。

パラメータで指定されたすべてのファイルは PEM (Privacy Enhanced Mail) 形式です。現在、TiDB はパスワードで保護された秘密キーのインポートをサポートしていないため、パスワードなしで秘密キー ファイルを提供する必要があります。証明書または秘密キーが無効な場合、TiDBサーバーは通常どおり起動しますが、クライアントは暗号化された接続を介して TiDBサーバーに接続できません。

証明書パラメータが正しい場合、TiDB は起動時に`secure connection is enabled`を出力します。それ以外の場合は、 `secure connection is NOT ENABLED`を出力します。

TiDB バージョン v5.2.0 より前の場合、 `mysql_ssl_rsa_setup --datadir=./certs`を使用して証明書を生成できます。 `mysql_ssl_rsa_setup`ツールは MySQL Server の一部です。

## 暗号化された接続を使用するように MySQL クライアントを構成する {#configure-the-mysql-client-to-use-encrypted-connections}

MySQL 5.7以降のバージョンのクライアントは、デフォルトで暗号化された接続を確立しようとします。サーバーが暗号化された接続をサポートしていない場合は、自動的に非暗号化接続に戻ります。バージョン 5.7 より前の MySQL のクライアントは、デフォルトで暗号化されていない接続を使用します。

次の`--ssl-mode`パラメータを使用して、クライアントの接続動作を変更できます。

-   `--ssl-mode=REQUIRED` : クライアントは暗号化された接続を必要とします。サーバー側が暗号化された接続をサポートしていない場合、接続を確立できません。
-   `--ssl-mode`パラメータがない場合: クライアントは暗号化接続を使用しようとしますが、サーバー側が暗号化接続をサポートしていない場合、暗号化接続は確立できません。その後、クライアントは暗号化されていない接続を使用します。
-   `--ssl-mode=DISABLED` : クライアントは暗号化されていない接続を使用します。

MySQL 8.0 クライアントには、このパラメータに加えて 2 つの SSL モードがあります。

-   `--ssl-mode=VERIFY_CA` : `--ssl-ca`を必要とする CA に対してサーバーからの証明書を検証します。
-   `--ssl-mode=VERIFY_IDENTITY` : `VERIFY_CA`と同じですが、接続先のホスト名が証明書と一致するかどうかも検証します。

詳細については、MySQL の[暗号化された接続のためのクライアント側のコンフィグレーション](https://dev.mysql.com/doc/refman/8.0/en/using-encrypted-connections.html#using-encrypted-connections-client-side-configuration)を参照してください。

## 認証を有効にする {#enable-authentication}

TiDBサーバーまたは MySQL クライアントで`ssl-ca`パラメーターが指定されていない場合、クライアントまたはサーバーはデフォルトで認証を実行しないため、中間者攻撃を防ぐことができません。たとえば、クライアントは偽装されたクライアントに「安全に」接続する可能性があります。サーバーとクライアントで認証用の`ssl-ca`パラメーターを構成できます。通常、必要なのはサーバーの認証のみですが、セキュリティをさらに強化するためにクライアントを認証することもできます。

-   MySQL クライアントから TiDBサーバーを認証するには:
    1.  TiDBサーバーで`ssl-cert`および`ssl-key`パラメータを指定します。
    2.  MySQL クライアントで`--ssl-ca`パラメータを指定します。
    3.  MySQLクライアントでは少なくとも`--ssl-mode` ～ `VERIFY_CA`を指定してください。
    4.  TiDBサーバーで構成された証明書 ( `ssl-cert` ) が、クライアント`--ssl-ca`パラメーターで指定された CA によって署名されていることを確認してください。それ以外の場合、認証は失敗します。

-   TiDBサーバーから MySQL クライアントを認証するには:
    1.  TiDBサーバーで`ssl-cert` 、および`ssl-ca`パラメータ`ssl-key`指定します。
    2.  クライアントで`--ssl-cert`および`--ssl-key`パラメータを指定します。
    3.  サーバー構成の証明書とクライアント構成の証明書の両方が、サーバーによって指定された`ssl-ca`によって署名されていることを確認してください。

<!---->

-   相互認証を行うには、上記の両方の要件を満たす必要があります。

デフォルトでは、サーバーからクライアントへの認証はオプションです。 TLS ハンドシェイク中にクライアントが識別証明書を提示しなくても、TLS 接続は確立できます。ユーザーの作成 ( `create user` )、権限の付与 ( `grant` )、または既存のユーザーの変更 ( `alter user` ) に`require x509`を指定して、クライアントの認証を要求することもできます。ユーザーを作成する例を次に示します。

```sql
create user 'u1'@'%'  require x509;
```

> **注記：**
>
> ログイン ユーザーが[TiDB 証明書ベースのログイン認証](/certificate-authentication.md#configure-the-user-certificate-information-for-login-verification)使用して設定した場合、ユーザーは TiDB への暗号化された接続を有効にすることが暗黙的に要求されます。

## 現在の接続で暗号化が使用されているかどうかを確認する {#check-whether-the-current-connection-uses-encryption}

`SHOW STATUS LIKE "%Ssl%";`ステートメントを使用して、暗号化が使用されているかどうか、暗号化された接続で使用される暗号化プロトコル、TLS バージョン番号など、現在の接続の詳細を取得します。

暗号化された接続での結果の次の例を参照してください。結果は、クライアントがサポートする TLS バージョンまたは暗号化プロトコルによって異なります。

    mysql> SHOW STATUS LIKE "%Ssl%";
    ......
    | Ssl_verify_mode | 5                            |
    | Ssl_version     | TLSv1.2                      |
    | Ssl_cipher      | ECDHE-RSA-AES128-GCM-SHA256  |
    ......

公式 MySQL クライアントの場合、 `STATUS`または`\s`ステートメントを使用して接続ステータスを表示することもできます。

    mysql> \s
    ...
    SSL: Cipher in use is ECDHE-RSA-AES128-GCM-SHA256
    ...

## サポートされている TLS バージョン、キー交換プロトコル、および暗号化アルゴリズム {#supported-tls-versions-key-exchange-protocols-and-encryption-algorithms}

TiDB でサポートされる TLS バージョン、鍵交換プロトコル、および暗号化アルゴリズムは、公式のGolangライブラリによって決定されます。

オペレーティング システムの暗号化ポリシーと使用しているクライアント ライブラリも、サポートされるプロトコルと暗号スイートのリストに影響を与える可能性があります。

### サポートされている TLS バージョン {#supported-tls-versions}

-   TLSv1.0 (デフォルトでは無効)
-   TLSv1.1
-   TLSv1.2
-   TLSv1.3

`tls-version`構成オプションを使用すると、使用できる TLS バージョンを制限できます。

使用できる実際の TLS バージョンは、OS の暗号化ポリシー、MySQL クライアントのバージョン、およびクライアントで使用される SSL/TLS ライブラリによって異なります。

### サポートされているキー交換プロトコルと暗号化アルゴリズム {#supported-key-exchange-protocols-and-encryption-algorithms}

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

## 証明書、キー、CA をリロードする {#reload-certificate-key-and-ca}

証明書、キー、または CA を置き換えるには、まず対応するファイルを置き換えてから、実行中の TiDB インスタンスで[`ALTER INSTANCE RELOAD TLS`](/sql-statements/sql-statement-alter-instance.md)ステートメントを実行して、証明書 ( [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) )、キー ( [`ssl-key`](/tidb-configuration-file.md#ssl-key) )、および CA ( [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) ) を元の構成からリロードします。パス。この方法では、TiDB インスタンスを再起動する必要はありません。

新しくロードされた証明書、キー、および CA は、ステートメントが正常に実行された後に確立された接続で有効になります。ステートメントの実行前に確立された接続は影響を受けません。

## 監視 {#monitoring}

TiDB v5.2.0 以降、 `Ssl_server_not_after`および`Ssl_server_not_before`ステータス変数を使用して、証明書の有効性の開始日と終了日を監視できます。

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

## こちらも参照 {#see-also}

-   [TiDB コンポーネント間で TLS を有効にする](/enable-tls-between-components.md) 。
