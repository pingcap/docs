---
title: Secure Connections to Serverless Tier Clusters
summary: Introduce TLS connection in TiDB Serverless Tier clusters.
---

# Serverless Tierクラスターへのセキュリティ接続 {#secure-connections-to-serverless-tier-clusters}

このドキュメントでは、TiDBServerless Tierの TLS に関する中心的な情報を紹介します。

## TiDBServerless Tierで TLS を無効にできますか? {#can-i-disable-tls-in-tidb-serverless-tier}

いいえ。

TiDBServerless TierはTLS 接続のみを許可し、非 TLS 接続を拒否します。その理由は、ユーザーがパブリック ネットワークを介して TiDBServerless Tierクラスターに接続するため、通信のセキュリティを確保するために TLS を使用することが非常に重要であるためです。

## どの TLS バージョンを使用できますか? {#what-tls-versions-can-i-use}

TiDBServerless Tierは、 TLS 1.2 および TLS 1.3 をサポートします。

TLS 1.0 および TLS 1.1 は、セキュリティ上の理由によりサポートされていません。背景情報については、IETF [TLS 1.0 と TLS 1.1 の廃止](https://datatracker.ietf.org/doc/rfc8996/)を参照してください。

## どのような証明書が必要ですか? {#what-certificates-do-i-need}

TiDBServerless Tierは、クライアントと TiDBServerless Tierクラスター間の TLS 接続の認証局 (CA) として[ISRG ルート X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt) ) はシステムのルート CA ストアに存在します。クライアントがJavaや Go などのシステムのルート CA ストアをデフォルトで使用する場合、CA ルートのパスを指定せずに TiDBServerless Tierクラスターに安全に簡単に接続できます。

ただし、一部のドライバーと ORM はシステム ルート CA ストアを使用しません。このような場合は、ドライバーまたは ORM の CA ルート パスをシステムのルート CA ストアに構成する必要があります。たとえば、macOS 上の Python で TiDBServerless Tierクラスターに[mysqlクライアント](https://github.com/PyMySQL/mysqlclient)を使用して接続する場合、引数`ssl`に`ca: /etc/ssl/cert.pem`設定する必要があります。

> **ノート：**
>
> TiDBServerless Tierでは、CA ルート証明書のダウンロードは提供していません。これは、将来同じ CA が証明書の発行に使用されることが保証されず、CA ルート証明書が変更される可能性があるためです。
>
> ただし、TiDBServerless Tierでは、すべての一般的なシステムで提供されている、一般的に利用可能な CA ルート証明書を常に使用することが保証されます。
>
> TiDBServerless Tierクラスターの CA 証明書が本当に必要な場合は、将来 CA を変更する場合に備えて、単一の CA 証明書の代わりに[Mozilla CA 証明書バンドル](https://curl.se/docs/caextract.html)をダウンロードすることをお勧めします。
>
> DBeaver など、内部に複数の証明書を含む証明書ファイルを受け入れない GUI クライアントを使用している場合は、 [ISRG ルート X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt)証明書をダウンロードする必要があります。

## TLS 接続で TiDBServerless Tierクラスターに接続するにはどうすればよいですか? {#how-do-i-connect-to-a-tidb-serverless-tier-cluster-in-tls-connection}

TiDB Cloud、 **[接続]**ダイアログにいくつかの接続例が表示されます。 [標準接続で接続する](/tidb-cloud/connect-via-standard-connection.md)の手順に従って、TiDBServerless Tierクラスターに接続できます。

一般に、TLS を有効にし、サーバーを認証するための CA ルート パスを提供することは、中間者攻撃を防ぐための良い方法です。クライアントが異なれば、TLS 接続における操作も異なります。 TLS を有効にし、クライアントの実際の使用状況に応じてサーバーを検証します。

次の例は、MySQL CLI クライアント、MyCLI クライアント、 Java、Python、Go、および Node.js の接続文字列を示しています。

<SimpleTab>
<div label="MySQL CLI client">

MySQL CLI クライアントは、デフォルトで TLS 接続の確立を試みます。 TiDBServerless Tierクラスターに接続する場合は、 `ssl-mode`と`ssl-ca`を設定する必要があります。

```shell
mysql --connect-timeout 15 -u <username> -h <host> -P 4000 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -D test -p
```

-   `--ssl-mode=VERIFY_IDENTITY`を使用すると、MySQL CLI クライアントは強制的に TLS を有効にし、TiDBServerless Tierクラスターを検証します。
-   システム上の CA ルート パスを設定するには`--ssl-ca=<CA_root_path>`を使用します。

</div>

<div label="MyCLI client">

[MyCLI](https://www.mycli.net/) TLS 関連パラメータを使用するときに TLS を自動的に有効にします。 TiDBServerless Tierクラスターに接続する場合は、 `ssl-ca`と`ssl-verify-server-cert`を設定する必要があります。

```shell
mycli -u <username> -h <host> -P 4000 -D test --ssl-ca=<CA_root_path> --ssl-verify-server-cert
```

-   システム上の CA ルート パスを設定するには`--ssl-ca=<CA_root_path>`を使用します。
-   `--ssl-verify-server-cert`を指定すると、TiDBServerless Tierクラスターが検証されます。

</div>

<div label="Java">

ここでは例として[MySQLコネクタ/J](https://dev.mysql.com/doc/connector-j/8.0/en/)の TLS 接続構成が使用されています。

```
jdbc:mysql://<host>:4000/test?user=<username>&password=<your_password>&sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3
```

-   TLS を有効にして TiDBServerless Tierクラスターを検証するには、 `sslMode=VERIFY_IDENTITY`を設定します。 JDBC はデフォルトでシステム CA ルート証明書を信頼するため、証明書を構成する必要はありません。
-   TLS プロトコルのバージョンを制限するには、 `enabledTLSProtocols=TLSv1.2,TLSv1.3`を設定します。

</div>

<div label="Python">

ここでは例として[mysqlクライアント](https://pypi.org/project/mysqlclient/)の TLS 接続構成が使用されています。

```
host="<host>", user="<username>", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<CA_root_path>"}
```

-   TLS を有効にして TiDBServerless Tierクラスターを検証するには、 `ssl_mode="VERIFY_IDENTITY"`を設定します。
-   システム上の CA ルート パスを設定するには、 `ssl={"ca": "<CA_root_path>"}`を設定します。

</div>

<div label="Go">

ここでは例として[Go-MySQL-ドライバー](https://github.com/go-sql-driver/mysql)の TLS 接続構成が使用されています。

```
mysql.RegisterTLSConfig("tidb", &tls.Config{
  MinVersion: tls.VersionTLS12,
  ServerName: "<host>",
})

db, err := sql.Open("mysql", "<usename>:<your_password>@tcp(<host>:4000)/test?tls=tidb")
```

-   接続に`tls.Config`を登録して TLS を有効にし、TiDBServerless Tierクラスターを検証します。 Go-MySQL-Driver はデフォルトでシステム CA ルート証明書を使用するため、証明書を構成する必要はありません。
-   TLS プロトコルのバージョンを制限するには、 `MinVersion: tls.VersionTLS12`を設定します。
-   TiDB サーバーレス層のホスト名を検証するには、 `ServerName: "<host>"`を設定します。
-   新しい TLS 構成を登録したくない場合は、接続文字列に`tls=true`を設定するだけで済みます。

</div>

<div label="Node.js">

ここでは例として[MySQL2](https://www.npmjs.com/package/mysql2)の TLS 接続構成が使用されています。

```
host: '<host>', port: 4000,user: '<username>', password: '<your_password>', database: 'test', ssl: {minVersion: 'TLSv1.2', rejectUnauthorized: true}
```

-   TLS プロトコルのバージョンを制限するには、 `ssl: {minVersion: 'TLSv1.2'}`を設定します。
-   TiDBServerless Tierクラスターを検証するには`ssl: {rejectUnauthorized: true}`を設定します。 Mysql2 はデフォルトでシステム CA ルート証明書を使用するため、証明書を構成する必要はありません。

</div>
</SimpleTab>

## 私のシステム上の CA ルート パスはどこにありますか? {#where-is-the-ca-root-path-on-my-system}

以下に、一般的なプラットフォーム上の CA ルート パスを示します。

**マックOS**

```
/etc/ssl/cert.pem
```

**Debian / Ubuntu / Arch**

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

Windows は、CA ルートへの特定のパスを提供しません。代わりに、 [レジストリ](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/local-machine-and-current-user-certificate-stores)使用して証明書を保存します。このため、Windows で CA ルート パスを指定するには、次の手順を実行します。

1.  [Mozilla CA 証明書バンドル](https://curl.se/docs/caextract.html)ダウンロードし、 `<path_to_mozilla_ca_cert_bundle>`などの任意のパスに保存します。
2.  Serverless Tierクラスターに接続する場合は、CA ルート パスとしてパス ( `<path_to_mozilla_ca_cert_bundle>` ) を使用します。

## TiDBServerless Tierはクライアントの ID を検証できますか? {#can-tidb-serverless-tier-verify-the-client-s-identity}

いいえ。

現在、TiDBServerless Tierは一方向 TLS 認証を使用します。これは、クライアントのみがパブリック証明書ペアを使用してサーバーを検証し、サーバーはクライアントを検証しないことを意味します。たとえば、MySQL CLI クライアントを使用する場合、接続文字列に`--ssl-cert`または`--ssl-key`を設定することはできません。
