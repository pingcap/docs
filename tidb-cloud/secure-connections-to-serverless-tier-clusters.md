---
title: TLS Connections to Serverless Tier
summary: Introduce TLS connections in TiDB Serverless Tier.
---

# Serverless Tierへの TLS 接続 {#tls-connections-to-serverless-tier}

クライアントとTiDB Cloud Serverless Tierクラスターの間に安全な TLS 接続を確立することは、データベースに接続するための基本的なセキュリティ プラクティスの 1 つです。 Serverless Tierのサーバー証明書は、独立したサードパーティの証明書プロバイダーによって発行されます。サーバー側のデジタル証明書をダウンロードしなくても、Serverless Tierクラスターに簡単に接続できます。

## 前提条件 {#prerequisites}

-   [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)または[SSO 認証](/tidb-cloud/tidb-cloud-sso-authentication.md)でTiDB Cloudにログインします。
-   [TiDB Cloud Serverless Tierクラスターを作成する](/tidb-cloud/tidb-cloud-quickstart.md) .

## Serverless Tierクラスターへのセキュリティ接続 {#secure-connection-to-a-serverless-tier-cluster}

[TiDB Cloudコンソール](https://tidbcloud.com/)では、さまざまな接続方法の例を取得し、次のようにServerless Tierクラスターに接続できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、クラスターの名前をクリックして概要ページに移動します。

2.  右上隅にある**[接続]**をクリックします。ダイアログが表示されます。

3.  ダイアログで、希望する接続方法とオペレーティング システムを選択します。

    -   サポートされている接続方法: MySQL CLI、MyCLI、JDBC、Python、Go、および Node.js。
    -   サポートされているオペレーティング システム: MacOS、Debian、CentOS/RedHat/Fedora、Alpine、OpenSUSE、および Windows。

4.  パスワードをまだ設定していない場合は、 **[パスワードの作成]**をクリックして、Serverless Tierクラスターのランダム パスワードを生成します。クラスターに簡単に接続できるように、パスワードはサンプル接続文字列に自動的に埋め込まれます。

    > **ノート：**
    >
    > -   ランダム パスワードは、大文字と小文字、数字、および特殊文字を含む 16 文字で構成されます。
    > -   このダイアログを閉じると、生成されたパスワードは再び表示されなくなるため、パスワードを安全な場所に保存する必要があります。パスワードを忘れた場合は、このダイアログで**[パスワードのリセット]**をクリックしてリセットできます。
    > -   Serverless Tierクラスターには、インターネット経由でアクセスできます。パスワードを別の場所で使用する必要がある場合は、パスワードをリセットしてデータベースのセキュリティを確保することをお勧めします。

5.  接続文字列を使用してクラスターに接続します。

    > **ノート：**
    >
    > Serverless Tierクラスターに接続するときは、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

次の例は、MySQL CLI、MyCLI、JDBC、Python、Go、および Node.js の接続文字列を示しています。オペレーティング システムの`<CA_root_path>`取得する方法については、 [ルート証明書の管理](#root-certificate-management)参照してください。

<SimpleTab>
<div label="MySQL CLI">

MySQL CLI クライアントは、デフォルトで TLS 接続を確立しようとします。 TiDB Serverless Tierクラスターに接続する場合は、 `ssl-mode`と`ssl-ca`を設定する必要があります。

```shell
mysql --connect-timeout 15 -u <username> -h <host> -P 4000 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -D test -p
```

-   `--ssl-mode=VERIFY_IDENTITY`を指定すると、MySQL CLI クライアントは強制的に TLS を有効にし、TiDBServerless Tierクラスターを検証します。
-   システムの CA ルート パスを設定するには、 `--ssl-ca=<CA_root_path>`を使用します。

</div>

<div label="MyCLI">

[MyCLI](https://www.mycli.net/) TLS 関連のパラメーターを使用するときに TLS を自動的に有効にします。 TiDB Serverless Tierクラスターに接続する場合は、 `ssl-ca`と`ssl-verify-server-cert`を設定する必要があります。

```shell
mycli -u <username> -h <host> -P 4000 -D test --ssl-ca=<CA_root_path> --ssl-verify-server-cert
```

-   システムの CA ルート パスを設定するには、 `--ssl-ca=<CA_root_path>`を使用します。
-   `--ssl-verify-server-cert`を指定すると、TiDBServerless Tierクラスターが検証されます。

</div>

<div label="JDBC">

ここでは、例として[MySQL コネクタ/J](https://dev.mysql.com/doc/connector-j/8.0/en/)の TLS 接続構成が使用されています。

```
jdbc:mysql://<host>:4000/test?user=<username>&password=<your_password>&sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3
```

-   `sslMode=VERIFY_IDENTITY`を設定して TLS を有効にし、TiDBServerless Tierクラスターを検証します。 JDBC はデフォルトでシステム CA ルート証明書を信頼するため、証明書を構成する必要はありません。
-   TLS プロトコルのバージョンを制限するには、 `enabledTLSProtocols=TLSv1.2,TLSv1.3`を設定します。

</div>

<div label="Python">

ここでは、例として[mysql クライアント](https://pypi.org/project/mysqlclient/)の TLS 接続構成が使用されています。

```
host="<host>", user="<username>", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<CA_root_path>"}
```

-   `ssl_mode="VERIFY_IDENTITY"`を設定して TLS を有効にし、TiDBServerless Tierクラスターを検証します。
-   システムの CA ルート パスを設定するには、 `ssl={"ca": "<CA_root_path>"}`を設定します。

</div>

<div label="Go">

ここでは、例として[Go-MySQL-ドライバー](https://github.com/go-sql-driver/mysql)の TLS 接続構成が使用されています。

```
mysql.RegisterTLSConfig("tidb", &tls.Config{
  MinVersion: tls.VersionTLS12,
  ServerName: "<host>",
})

db, err := sql.Open("mysql", "<usename>:<your_password>@tcp(<host>:4000)/test?tls=tidb")
```

-   接続に`tls.Config`登録して、TLS を有効にし、TiDB Serverless Tierクラスターを検証します。 Go-MySQL-Driver はデフォルトでシステム CA ルート証明書を使用するため、証明書を構成する必要はありません。
-   TLS プロトコルのバージョンを制限するには、 `MinVersion: tls.VersionTLS12`を設定します。
-   TiDB サーバーレス層のホスト名を確認するには、 `ServerName: "<host>"`を設定します。
-   新しい TLS 構成を登録したくない場合は、接続文字列に`tls=true`を設定するだけです。

</div>

<div label="Node.js">

ここでは、例として[Mysql2](https://www.npmjs.com/package/mysql2)の TLS 接続構成が使用されています。

```
host: '<host>', port: 4000,user: '<username>', password: '<your_password>', database: 'test', ssl: {minVersion: 'TLSv1.2', rejectUnauthorized: true}
```

-   TLS プロトコルのバージョンを制限するには、 `ssl: {minVersion: 'TLSv1.2'}`を設定します。
-   TiDBServerless Tierクラスターを検証するには、 `ssl: {rejectUnauthorized: true}`を設定します。 Mysql2 はデフォルトでシステム CA ルート証明書を使用するため、証明書を構成する必要はありません。

</div>
</SimpleTab>

## ルート証明書の管理 {#root-certificate-management}

### ルート証明書の発行と有効性 {#root-certificate-issuance-and-validity}

TiDB Serverless Tier は、クライアントと TiDB Serverless Tierクラスター間の TLS 接続の認証局 (CA) として[暗号化しましょう](https://letsencrypt.org/)からの証明書を使用します。 Serverless Tier証明書の有効期限が切れると、クラスターの通常の運用や確立された TLS セキュア接続に影響を与えることなく、自動的にローテーションされます。

> **ノート：**
>
> TiDB Serverless Tier はCA ルート証明書のダウンロードを提供しません。これは、同じ CA が将来証明書を発行するために使用されることを保証しないためです。これにより、CA ルート証明書が変更されます。

クライアントがJavaや Go などのシステムのルート CA ストアをデフォルトで使用する場合、CA ルートのパスを指定しなくても、TiDB Serverless Tierクラスターに簡単に安全に接続できます。 TiDB Serverless Tierクラスターの CA 証明書を取得したい場合は、単一の CA 証明書の代わりに[Mozilla CA 証明書バンドル](https://curl.se/docs/caextract.html)ダウンロードして使用できます。

ただし、一部のドライバーと ORM は、システム ルート CA ストアを使用しません。このような場合、ドライバーまたは ORM の CA ルート パスをシステム ルート CA ストアに構成する必要があります。たとえば、macOS 上の Python で TiDB Serverless Tierクラスターに[mysql クライアント](https://github.com/PyMySQL/mysqlclient)を使用して接続する場合、 `ssl`引数に`ca: /etc/ssl/cert.pem`を設定する必要があります。

内部に複数の証明書を含む証明書ファイルを受け入れない DBeaver などの GUI クライアントを使用している場合は、 [ISRGルートX1](https://letsencrypt.org/certs/isrgrootx1.pem.txt)証明書をダウンロードする必要があります。

### ルート証明書のデフォルト パス {#root-certificate-default-path}

異なるオペレーティング システムでは、ルート証明書のデフォルトのstorageパスは次のとおりです。

**マックOS**

```
/etc/ssl/cert.pem
```

**Debian / Ubuntu / アーチ**

```
/etc/ssl/certs/ca-certificates.crt
```

**RedHat / Fedora / CentOS / Mageia**

```
/etc/pki/tls/certs/ca-bundle.crt
```

**高山**

```
/etc/ssl/cert.pem
```

**OpenSUSE**

```
/etc/ssl/ca-bundle.pem
```

**ウィンドウズ**

Windows は、CA ルートへの特定のパスを提供しません。代わりに、 [レジストリ](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/local-machine-and-current-user-certificate-stores)を使用して証明書を保存します。このため、Windows で CA ルート パスを指定するには、次の手順を実行します。

1.  [Mozilla CA 証明書バンドル](https://curl.se/docs/caextract.html)ダウンロードし、 `<path_to_mozilla_ca_cert_bundle>`などの任意のパスに保存します。
2.  Serverless Tierクラスターに接続するときは、パス ( `<path_to_mozilla_ca_cert_bundle>` ) を CA ルート パスとして使用します。

## よくある質問 {#faqs}

### TiDB Cloud Serverless Tierクラスターに接続するためにサポートされている TLS バージョンはどれですか? {#which-tls-versions-are-supported-to-connect-to-my-tidb-cloud-serverless-tier-cluster}

セキュリティ上の理由から、 TiDB Cloud Serverless Tier はTLS 1.2 と TLS 1.3 のみをサポートし、TLS 1.0 と TLS 1.1 のバージョンはサポートしていません。詳細については、IETF [TLS 1.0 と TLS 1.1 の廃止](https://datatracker.ietf.org/doc/rfc8996/)を参照してください。

### 接続クライアントとTiDB Cloud Serverless Tierの間の双方向 TLS 認証はサポートされていますか? {#is-two-way-tls-authentication-between-my-connection-client-and-tidb-cloud-serverless-tier-supported}

いいえ。

TiDB Cloud Serverless Tier は一方向の TLS 認証のみをサポートします。つまり、クライアントは公開鍵を使用してTiDB Cloudクラスター証明書の秘密鍵の署名を検証しますが、クラスターはクライアントを検証しません。

### TiDBServerless Tierは、安全な接続を確立するために TLS を構成する必要がありますか? {#does-tidb-serverless-tier-have-to-configure-tls-to-establish-a-secure-connection}

はい。

TiDB Cloud Serverless Tier はTLS 接続のみを許可し、非 SSL/TLS 接続を禁止します。その理由は、SSL/TLS は、インターネット経由でServerless Tierクラスターに接続するときに、インターネットへのデータ公開のリスクを軽減するための最も基本的なセキュリティ対策の 1 つであるためです。
