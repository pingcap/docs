---
title: TLS Connections to TiDB Serverless
summary: Introduce TLS connections in TiDB Serverless.
aliases: ['/tidbcloud/secure-connections-to-serverless-tier-clusters']
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

4.  パスワードをまだ設定していない場合は、 **「パスワードの生成」**をクリックして、TiDB サーバーレス クラスター用のランダムなパスワードを生成します。クラスターに簡単に接続できるように、パスワードはサンプル接続文字列に自動的に埋め込まれます。

    > **注記：**
    >
    > -   ランダムなパスワードは、大文字、小文字、数字、特殊文字を含む 16 文字で構成されます。
    > -   このダイアログを閉じると、生成されたパスワードは再度表示されなくなるため、パスワードを安全な場所に保存する必要があります。パスワードを忘れた場合は、このダイアログで**[パスワードのリセット]**をクリックしてリセットできます。
    > -   TiDB サーバーレス クラスターにはインターネット経由でアクセスできます。他の場所でパスワードを使用する必要がある場合は、データベースのセキュリティを確保するためにパスワードをリセットすることをお勧めします。

5.  接続文字列を使用してクラスターに接続します。

    > **注記：**
    >
    > TiDB サーバーレス クラスターに接続するときは、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

## ルート証明書の管理 {#root-certificate-management}

### ルート証明書の発行と有効性 {#root-certificate-issuance-and-validity}

TiDB サーバーレスは、クライアントと TiDB サーバーレス クラスター間の TLS 接続の認証局 (CA) として[暗号化しましょう](https://letsencrypt.org/)の証明書を使用します。 TiDB サーバーレス証明書の有効期限が切れると、クラスターの通常の動作や確立された TLS セキュア接続に影響を与えることなく、自動的にローテーションされます。

クライアントがJavaや Go などのシステムのルート CA ストアをデフォルトで使用する場合、CA ルートのパスを指定しなくても TiDB サーバーレス クラスターに安全に簡単に接続できます。ただし、一部のドライバーと ORM はシステム ルート CA ストアを使用しません。このような場合は、ドライバーまたは ORM の CA ルート パスをシステムのルート CA ストアに構成する必要があります。たとえば、macOS 上の Python で TiDB サーバーレス クラスターに[mysqlクライアント](https://github.com/PyMySQL/mysqlclient)を使用して接続する場合、引数`ssl`に`ca: /etc/ssl/cert.pem`設定する必要があります。

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

1.  [ISRG ルート X1 証明書](https://letsencrypt.org/certs/isrgrootx1.pem.txt)をダウンロードし、希望のパス ( `<path_to_ca>`など) に保存します。
2.  TiDB サーバーレス クラスターに接続する場合は、パス ( `<path_to_ca>` ) を CA ルート パスとして使用します。

## よくある質問 {#faqs}

### TiDB サーバーレス クラスターへの接続ではどの TLS バージョンがサポートされていますか? {#which-tls-versions-are-supported-to-connect-to-my-tidb-serverless-cluster}

セキュリティ上の理由から、TiDB サーバーレスは TLS 1.2 と TLS 1.3 のみをサポートし、TLS 1.0 と TLS 1.1 バージョンはサポートしません。詳細については、IETF [TLS 1.0 と TLS 1.1 の廃止](https://datatracker.ietf.org/doc/rfc8996/)を参照してください。

### 接続クライアントと TiDB サーバーレス間の双方向 TLS 認証はサポートされていますか? {#is-two-way-tls-authentication-between-my-connection-client-and-tidb-serverless-supported}

いいえ。

TiDB サーバーレスは一方向の TLS 認証のみをサポートします。つまり、クラスターはクライアントを検証せずに、クライアントは公開鍵を使用してTiDB Cloudクラスター証明書の秘密鍵の署名を検証します。

### TiDB サーバーレスは安全な接続を確立するために TLS を構成する必要がありますか? {#does-tidb-serverless-have-to-configure-tls-to-establish-a-secure-connection}

標準接続の場合、TiDB サーバーレスは TLS 接続のみを許可し、非 SSL/TLS 接続を禁止します。その理由は、SSL/TLS は、インターネット経由で TiDB サーバーレス クラスターに接続するときに、データがインターネットに公開されるリスクを軽減するための最も基本的なセキュリティ対策の 1 つであるためです。

プライベート エンドポイント接続の場合、 TiDB Cloudサービスへの安全性の高い一方向アクセスがサポートされ、データがパブリック インターネットに公開されないため、TLS の構成はオプションです。
