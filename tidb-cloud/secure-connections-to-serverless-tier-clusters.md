---
title: Secure Connections to Serverless Tier Clusters
summary: Introduce TLS connection in TiDB Serverless Tier clusters.
---

# サーバーレス層クラスターへのセキュリティ接続 {#secure-connections-to-serverless-tier-clusters}

このドキュメントでは、TiDB Serverless Tier における TLS に関するコア情報を紹介します。

## TiDB サーバーレス層で TLS を無効にすることはできますか? {#can-i-disable-tls-in-tidb-serverless-tier}

いいえ。

TiDB サーバーレス層は、TLS 接続のみを許可し、非 TLS 接続を拒否します。その理由は、ユーザーがパブリック ネットワークを介して TiDB Serverless Tier クラスターに接続するため、通信のセキュリティを確保するために TLS を使用することが非常に重要です。

## どの TLS バージョンを使用できますか? {#what-tls-versions-can-i-use}

TiDB サーバーレス層は、TLS 1.2 および TLS 1.3 のみをサポートします。

## どのような証明書が必要ですか? {#what-certificates-do-i-need}

TiDB Serverless Tier は、クライアントと TiDB Serverless Tier クラスター間の TLS 接続の認証局 (CA) として[暗号化しましょう](https://letsencrypt.org/)からの証明書を使用します。通常、Let&#39;s Encrypt のルート証明書 ( [ISRGルートX1](https://letsencrypt.org/certs/isrgrootx1.pem.txt) ) は、システムのルート CA ストアに存在します。クライアントがJavaや Go などのシステムのルート CA ストアをデフォルトで使用する場合、CA ルートのパスを指定しなくても、TiDB Serverless Tier クラスターに簡単に安全に接続できます。

ただし、一部のドライバーと ORM は、システム ルート CA ストアを使用しません。このような場合、ドライバーまたは ORM の CA ルート パスをシステム ルート CA ストアに構成する必要があります。たとえば、macOS 上の Python で TiDB Serverless Tier クラスターに[mysql クライアント](https://github.com/PyMySQL/mysqlclient)を使用して接続する場合、 `ssl`引数に`ca: /etc/ssl/cert.pem`を設定する必要があります。

> **ノート：**
>
> TiDB Serverless Tier は CA ルート証明書のダウンロードを提供しません。これは、同じ CA が将来証明書を発行するために使用されることを保証しないためです。これにより、CA ルート証明書が変更されます。
>
> ただし、TiDB Serverless Tier は、すべての一般的なシステムで提供されている一般的に利用可能な CA ルート証明書を常に使用することを保証します。
>
> TiDB Serverless Tier クラスターの CA 証明書が本当に必要な場合は、将来 CA を変更する場合に備えて、単一の CA 証明書ではなく[Mozilla CA 証明書バンドル](https://curl.se/docs/caextract.html)をダウンロードすることをお勧めします。

## TLS 接続で TiDB Serverless Tier クラスターに接続するにはどうすればよいですか? {#how-do-i-connect-to-a-tidb-serverless-tier-cluster-in-tls-connection}

TiDB Cloudは、**接続**ダイアログでいくつかの接続例を提供します。 [標準接続で接続](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection)の手順に従って、TiDB Serverless Tier クラスターに接続できます。

一般に、TLS を有効にし、サーバーを認証するための CA ルート パスを提供することは、中間者攻撃を防ぐための良い方法です。クライアントが異なれば、TLS 接続での操作も異なります。 TLS を有効にし、クライアントの実際の使用に応じてサーバーを検証します。

次の例は、MySQL CLI クライアント、MyCLI クライアント、 Java、Python、Go、および Node.js の接続文字列を示しています。

<SimpleTab>
<div label="MySQL CLI client">

デフォルトでは、MySQL CLI クライアントは TLS 接続を確立しようとします。 TiDB Serverless Tier クラスターに接続する場合は、 `ssl-mode`と`ssl-ca`を設定する必要があります。

```shell
mysql --connect-timeout 15 -u <username> -h <host> -P 4000 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -D test -p
```

-   `--ssl-mode=VERIFY_IDENTITY`を指定すると、MySQL CLI クライアントは強制的に TLS を有効にし、TiDB サーバーレス層クラスターを検証します。
-   システムの CA ルート パスを設定するには、 `--ssl-ca=<CA_root_path>`を使用します。

</div>

<div label="MyCLI client">

[MyCLI](https://www.mycli.net/)は、TLS 関連のパラメーターを使用するときに TLS を自動的に有効にします。 TiDB Serverless Tier クラスターに接続する場合は、 `ssl-ca`と`ssl-verify-server-cert`を設定する必要があります。

```shell
mycli -u <username> -h <host> -P 4000 -D test --ssl-ca=<CA_root_path> --ssl-verify-server-cert
```

-   システムの CA ルート パスを設定するには、 `--ssl-ca=<CA_root_path>`を使用します。
-   `--ssl-verify-server-cert`を指定すると、TiDB サーバーレス層クラスターが検証されます。

</div>

<div label="Java">

ここでは、例として[MySQL コネクタ/J](https://dev.mysql.com/doc/connector-j/8.0/en/)の TLS 接続構成が使用されています。

```
jdbc:mysql://<host>:4000/test?user=<username>&password=<your_password>&sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3
```

-   `sslMode=VERIFY_IDENTITY`を設定して TLS を有効にし、TiDB サーバーレス層クラスターを検証します。 JDBC はデフォルトでシステム CA ルート証明書を信頼するため、証明書を構成する必要はありません。
-   TLS プロトコルのバージョンを制限するには、 `enabledTLSProtocols=TLSv1.2,TLSv1.3`を設定します。

</div>

<div label="Python">

ここでは、例として[mysql クライアント](https://pypi.org/project/mysqlclient/)の TLS 接続構成が使用されています。

```
host="<host>", user="<username>", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<CA_root_path>"}
```

-   `ssl_mode="VERIFY_IDENTITY"`を設定して TLS を有効にし、TiDB サーバーレス層クラスターを検証します。
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

-   接続に`tls.Config`を登録して、TLS を有効にし、TiDB Serverless Tier クラスターを検証します。 Go-MySQL-Driver はデフォルトでシステム CA ルート証明書を使用するため、証明書を構成する必要はありません。
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
-   TiDB サーバーレス層クラスターを検証するには、 `ssl: {rejectUnauthorized: true}`を設定します。 Mysql2 はデフォルトでシステム CA ルート証明書を使用するため、証明書を構成する必要はありません。

</div>
</SimpleTab>

## システムの CA ルート パスはどこにありますか? {#where-is-the-ca-root-path-on-my-system}

一般的なプラットフォームでの CA ルート パスを次に示します。

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

## TiDB Serverless Tier はクライアントの身元を確認できますか? {#can-tidb-serverless-tier-verify-the-client-s-identity}

いいえ。

現在、TiDB Serverless Tier は一方向 TLS 認証を使用しています。つまり、クライアントのみがパブリック証明書ペアを使用してサーバーを検証し、サーバーはクライアントを検証しません。たとえば、MySQL CLI クライアントを使用する場合、接続文字列で`--ssl-cert`または`--ssl-key`を構成することはできません。
