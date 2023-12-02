---
title: TLS Connections to TiDB Serverless
summary: Introduce TLS connections in TiDB Serverless.
---

# TiDB サーバーレスへの TLS 接続 {#tls-connections-to-tidb-serverless}

クライアントと TiDB サーバーレス クラスターの間に安全な TLS 接続を確立することは、データベースに接続するための基本的なセキュリティ手法の 1 つです。 TiDB Serverless のサーバー証明書は、独立したサードパーティの証明書プロバイダーによって発行されます。サーバー側のデジタル証明書をダウンロードしなくても、TiDB サーバーレス クラスターに簡単に接続できます。

## 前提条件 {#prerequisites}

-   [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)または[SSO認証](/tidb-cloud/tidb-cloud-sso-authentication.md)を介してTiDB Cloudにログインします。
-   [TiDB サーバーレスクラスターを作成する](/tidb-cloud/tidb-cloud-quickstart.md) 。

## TiDB サーバーレスクラスターへの TLS 接続 {#tls-connection-to-a-tidb-serverless-cluster}

[TiDB Cloudコンソール](https://tidbcloud.com/)では、さまざまな接続方法の例を取得し、次のように TiDB サーバーレス クラスターに接続できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、クラスターの名前をクリックして概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。ダイアログが表示されます。

3.  ダイアログでは、エンドポイント タイプのデフォルト設定を`Public`のままにして、希望の接続方法とオペレーティング システムを選択します。

    -   サポートされている接続方法: MySQL CLI、MyCLI、JDBC、Python、Go、および Node.js。
    -   サポートされているオペレーティング システム: MacOS、Debian、CentOS/RedHat/Fedora、Alpine、OpenSUSE、および Windows。

4.  パスワードをまだ設定していない場合は、 **「パスワードの作成」**をクリックして、TiDB サーバーレスクラスター用のランダムなパスワードを生成します。クラスターに簡単に接続できるように、パスワードはサンプル接続文字列に自動的に埋め込まれます。

    > **注記：**
    >
    > -   ランダムなパスワードは、大文字、小文字、数字、特殊文字を含む 16 文字で構成されます。
    > -   このダイアログを閉じると、生成されたパスワードは再度表示されなくなるため、パスワードを安全な場所に保存する必要があります。パスワードを忘れた場合は、このダイアログで**[パスワードのリセット] を**クリックしてリセットできます。
    > -   TiDB サーバーレス クラスターにはインターネット経由でアクセスできます。他の場所でパスワードを使用する必要がある場合は、データベースのセキュリティを確保するためにパスワードをリセットすることをお勧めします。

5.  接続文字列を使用してクラスターに接続します。

    > **注記：**
    >
    > TiDB サーバーレス クラスターに接続するときは、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

次の例は、MySQL CLI、MyCLI、JDBC、Python、Go、および Node.js の接続文字列を示しています。オペレーティング システムの`<CA_root_path>`取得する方法については、 [ルート証明書の管理](#root-certificate-management)を参照してください。

<SimpleTab>
<div label="MySQL CLI">

MySQL CLI クライアントは、デフォルトで TLS 接続の確立を試みます。 TiDB サーバーレス クラスターに接続する場合は、 `ssl-mode`と`ssl-ca`を設定する必要があります。

```shell
mysql --connect-timeout 15 -u <username> -h <host> -P 4000 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -D test -p
```

-   `--ssl-mode=VERIFY_IDENTITY`を使用すると、MySQL CLI クライアントは強制的に TLS を有効にし、TiDB サーバーレス クラスターを検証します。
-   システム上の CA ルート パスを設定するには`--ssl-ca=<CA_root_path>`を使用します。

</div>

<div label="MyCLI">

[MyCLI](https://www.mycli.net/) TLS 関連パラメータを使用するときに TLS を自動的に有効にします。 TiDB サーバーレス クラスターに接続する場合は、 `ssl-ca`と`ssl-verify-server-cert`を設定する必要があります。

```shell
mycli -u <username> -h <host> -P 4000 -D test --ssl-ca=<CA_root_path> --ssl-verify-server-cert
```

-   システム上の CA ルート パスを設定するには`--ssl-ca=<CA_root_path>`を使用します。
-   `--ssl-verify-server-cert`を指定すると、TiDB サーバーレス クラスターが検証されます。

</div>

<div label="JDBC">

ここでは例として[MySQLコネクタ/J](https://dev.mysql.com/doc/connector-j/en/)の TLS 接続構成が使用されています。

    jdbc:mysql://<host>:4000/test?user=<username>&password=<your_password>&sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3

-   TLS を有効にして TiDB サーバーレス クラスターを検証するには、 `sslMode=VERIFY_IDENTITY`を設定します。 JDBC はデフォルトでシステム CA ルート証明書を信頼するため、証明書を構成する必要はありません。
-   TLS プロトコルのバージョンを制限するには、 `enabledTLSProtocols=TLSv1.2,TLSv1.3`を設定します。

</div>

<div label="Python">

ここでは例として[mysqlクライアント](https://pypi.org/project/mysqlclient/)の TLS 接続構成が使用されています。

    host="<host>", user="<username>", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<CA_root_path>"}

-   TLS を有効にして TiDB サーバーレス クラスターを検証するには、 `ssl_mode="VERIFY_IDENTITY"`を設定します。
-   システム上の CA ルート パスを設定するには、 `ssl={"ca": "<CA_root_path>"}`を設定します。

</div>

<div label="Go">

ここでは例として[Go-MySQL-ドライバー](https://github.com/go-sql-driver/mysql)の TLS 接続構成が使用されています。

    mysql.RegisterTLSConfig("tidb", &tls.Config{
      MinVersion: tls.VersionTLS12,
      ServerName: "<host>",
    })

    db, err := sql.Open("mysql", "<usename>:<your_password>@tcp(<host>:4000)/test?tls=tidb")

-   接続に`tls.Config`を登録して TLS を有効にし、TiDB サーバーレス クラスターを検証します。 Go-MySQL-Driver はデフォルトでシステム CA ルート証明書を使用するため、証明書を構成する必要はありません。
-   TLS プロトコルのバージョンを制限するには、 `MinVersion: tls.VersionTLS12`を設定します。
-   TiDB Serverless のホスト名を検証するには`ServerName: "<host>"`を設定します。
-   新しい TLS 構成を登録したくない場合は、接続文字列に`tls=true`を設定するだけで済みます。

</div>

<div label="Node.js">

ここでは例として[MySQL2](https://www.npmjs.com/package/mysql2)の TLS 接続構成が使用されています。

    host: '<host>', port: 4000,user: '<username>', password: '<your_password>', database: 'test', ssl: {minVersion: 'TLSv1.2', rejectUnauthorized: true}

-   TLS プロトコルのバージョンを制限するには、 `ssl: {minVersion: 'TLSv1.2'}`を設定します。
-   TiDB サーバーレス クラスターを検証するには`ssl: {rejectUnauthorized: true}`を設定します。 Mysql2 はデフォルトでシステム CA ルート証明書を使用するため、証明書を構成する必要はありません。

</div>
</SimpleTab>

## ルート証明書の管理 {#root-certificate-management}

### ルート証明書の発行と有効性 {#root-certificate-issuance-and-validity}

TiDB サーバーレスは、クライアントと TiDB サーバーレス クラスター間の TLS 接続の認証局 (CA) として[暗号化しましょう](https://letsencrypt.org/)の証明書を使用します。 TiDB サーバーレス証明書の有効期限が切れると、クラスターの通常の動作や確立された TLS セキュア接続に影響を与えることなく、自動的にローテーションされます。

> **注記：**
>
> TiDB サーバーレスは、CA ルート証明書のダウンロードを提供しません。これは、将来同じ CA が証明書の発行に使用されることが保証されず、CA ルート証明書が変更される可能性があるためです。

クライアントがJavaや Go などのシステムのルート CA ストアをデフォルトで使用する場合、CA ルートのパスを指定しなくても TiDB サーバーレス クラスターに安全に簡単に接続できます。それでも TiDB サーバーレス クラスターの CA 証明書を取得したい場合は、単一の CA 証明書の代わりに[Mozilla CA 証明書バンドル](https://curl.se/docs/caextract.html)ダウンロードして使用できます。

ただし、一部のドライバーと ORM はシステム ルート CA ストアを使用しません。このような場合は、ドライバーまたは ORM の CA ルート パスをシステムのルート CA ストアに構成する必要があります。たとえば、macOS 上の Python で TiDB サーバーレス クラスターに[mysqlクライアント](https://github.com/PyMySQL/mysqlclient)を使用して接続する場合、引数`ssl`に`ca: /etc/ssl/cert.pem`設定する必要があります。

DBeaver など、内部に複数の証明書を含む証明書ファイルを受け入れない GUI クライアントを使用している場合は、 [ISRG ルート X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt)証明書をダウンロードする必要があります。

### ルート証明書のデフォルトのパス {#root-certificate-default-path}

さまざまなオペレーティング システムでのルート証明書のデフォルトのstorageパスは次のとおりです。

**マックOS**

    /etc/ssl/cert.pem

**Debian / Ubuntu / Arch**

    /etc/ssl/certs/ca-certificates.crt

**RedHat / Fedora / CentOS / Mageia**

    /etc/pki/tls/certs/ca-bundle.crt

**高山**

    /etc/ssl/cert.pem

**OpenSUSE**

    /etc/ssl/ca-bundle.pem

**ウィンドウズ**

Windows は、CA ルートへの特定のパスを提供しません。代わりに、 [レジストリ](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/local-machine-and-current-user-certificate-stores)を使用して証明書を保存します。このため、Windows で CA ルート パスを指定するには、次の手順を実行します。

1.  [Mozilla CA 証明書バンドル](https://curl.se/docs/caextract.html)ダウンロードし、 `<path_to_mozilla_ca_cert_bundle>`などの任意のパスに保存します。
2.  TiDB サーバーレス クラスターに接続する場合は、パス ( `<path_to_mozilla_ca_cert_bundle>` ) を CA ルート パスとして使用します。

## よくある質問 {#faqs}

### TiDB サーバーレス クラスターへの接続ではどの TLS バージョンがサポートされていますか? {#which-tls-versions-are-supported-to-connect-to-my-tidb-serverless-cluster}

セキュリティ上の理由から、TiDB サーバーレスは TLS 1.2 と TLS 1.3 のみをサポートし、TLS 1.0 と TLS 1.1 バージョンはサポートしません。詳細については、IETF [TLS 1.0 と TLS 1.1 の廃止](https://datatracker.ietf.org/doc/rfc8996/)を参照してください。

### 接続クライアントと TiDB サーバーレス間の双方向 TLS 認証はサポートされていますか? {#is-two-way-tls-authentication-between-my-connection-client-and-tidb-serverless-supported}

いいえ。

TiDB サーバーレスは一方向の TLS 認証のみをサポートします。つまり、クラスターはクライアントを検証せずに、クライアントは公開鍵を使用してTiDB Cloudクラスター証明書の秘密鍵の署名を検証します。

### TiDB サーバーレスは安全な接続を確立するために TLS を構成する必要がありますか? {#does-tidb-serverless-have-to-configure-tls-to-establish-a-secure-connection}

標準接続の場合、TiDB サーバーレスは TLS 接続のみを許可し、非 SSL/TLS 接続を禁止します。その理由は、SSL/TLS は、インターネット経由で TiDB サーバーレス クラスターに接続するときに、データがインターネットに公開されるリスクを軽減するための最も基本的なセキュリティ対策の 1 つであるためです。

プライベート エンドポイント接続の場合、 TiDB Cloudサービスへの安全性の高い一方向アクセスがサポートされ、データがパブリック インターネットに公開されないため、TLS の構成はオプションです。
