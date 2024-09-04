---
title: TLS Connections to TiDB Serverless
summary: TiDB Serverless に TLS 接続を導入します。
aliases: ['/tidbcloud/secure-connections-to-serverless-tier-clusters']
---

# TiDB サーバーレスへの TLS 接続 {#tls-connections-to-tidb-serverless}

クライアントと TiDB Serverless クラスター間の安全な TLS 接続を確立することは、データベースに接続するための基本的なセキュリティ対策の 1 つです。TiDB Serverless のサーバー証明書は、独立したサードパーティの証明書プロバイダーによって発行されます。サーバー側のデジタル証明書をダウンロードしなくても、TiDB Serverless クラスターに簡単に接続できます。

## 前提条件 {#prerequisites}

-   [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)または[SSO認証](/tidb-cloud/tidb-cloud-sso-authentication.md)でTiDB Cloudにログインします。
-   [TiDB サーバーレス クラスターを作成する](/tidb-cloud/tidb-cloud-quickstart.md) 。

## TiDB サーバーレス クラスターへの TLS 接続 {#tls-connection-to-a-tidb-serverless-cluster}

[TiDB Cloudコンソール](https://tidbcloud.com/)では、さまざまな接続方法の例を取得し、次のように TiDB Serverless クラスターに接続できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。ダイアログが表示されます。

3.  ダイアログでは、接続タイプのデフォルト設定を`Public`のままにして、希望する接続方法とオペレーティング システムを選択します。

4.  まだパスワードを設定していない場合は、 **「パスワードの生成」**をクリックして、TiDB Serverless クラスターのランダム パスワードを生成します。パスワードはサンプル接続文字列に自動的に埋め込まれ、クラスターに簡単に接続できるようになります。

    > **注記：**
    >
    > -   ランダム パスワードは、大文字、小文字、数字、特殊文字を含む 16 文字で構成されます。
    > -   このダイアログを閉じると、生成されたパスワードは再度表示されなくなるため、パスワードを安全な場所に保存する必要があります。パスワードを忘れた場合は、このダイアログの**「パスワードのリセット」を**クリックしてリセットできます。
    > -   TiDB Serverless クラスターにはインターネット経由でアクセスできます。パスワードを他の場所で使用する必要が生じた場合は、データベースのセキュリティを確保するためにパスワードをリセットすることをお勧めします。

5.  接続文字列を使用してクラスターに接続します。

    > **注記：**
    >
    > TiDB Serverless クラスターに接続する場合は、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名プレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)参照してください。

## ルート証明書の管理 {#root-certificate-management}

### ルート証明書の発行と有効性 {#root-certificate-issuance-and-validity}

TiDB Serverless は、クライアントと TiDB Serverless クラスター間の TLS 接続の証明機関 (CA) として[暗号化しましょう](https://letsencrypt.org/)からの証明書を使用します。TiDB Serverless 証明書の有効期限が切れると、クラスターの通常の操作や確立された TLS セキュア接続に影響を与えることなく、証明書が自動的にローテーションされます。

Javaや Go など、クライアントがシステムのルート CA ストアをデフォルトで使用する場合、CA ルートのパスを指定せずに、TiDB Serverless クラスターに安全かつ簡単に接続できます。ただし、一部のドライバーと ORM はシステム ルート CA ストアを使用しません。その場合は、ドライバーまたは ORM の CA ルート パスをシステム ルート CA ストアに設定する必要があります。たとえば、macOS 上の Python で[mysqlクライアント](https://github.com/PyMySQL/mysqlclient)使用して TiDB Serverless クラスターに接続する場合は、 `ssl`引数に`ca: /etc/ssl/cert.pem`設定する必要があります。

複数の証明書が含まれる証明書ファイルを受け入れない DBeaver などの GUI クライアントを使用している場合は、 [ISRGルートX1](https://letsencrypt.org/certs/isrgrootx1.pem)証明書をダウンロードする必要があります。

### ルート証明書のデフォルトパス {#root-certificate-default-path}

異なるオペレーティング システムにおけるルート証明書のデフォルトのstorageパスは次のとおりです。

**MacOS**

    /etc/ssl/cert.pem

**Debian / Ubuntu / アーチ**

    /etc/ssl/certs/ca-certificates.crt

**RedHat / Fedora / CentOS / Mageia**

    /etc/pki/tls/certs/ca-bundle.crt

**高山**

    /etc/ssl/cert.pem

**オープンSUSE**

    /etc/ssl/ca-bundle.pem

**ウィンドウズ**

Windows では、CA ルートへの特定のパスは提供されません。代わりに、 [レジストリ](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/local-machine-and-current-user-certificate-stores)を使用して証明書を保存します。このため、Windows で CA ルート パスを指定するには、次の手順を実行します。

1.  [ISRG ルート X1 証明書](https://letsencrypt.org/certs/isrgrootx1.pem)をダウンロードし、 `<path_to_ca>`などの任意のパスに保存します。
2.  TiDB Serverless クラスターに接続するときは、パス ( `<path_to_ca>` ) を CA ルート パスとして使用します。

## よくある質問 {#faqs}

### TiDB Serverless クラスターに接続するためにサポートされている TLS バージョンはどれですか? {#which-tls-versions-are-supported-to-connect-to-my-tidb-serverless-cluster}

セキュリティ上の理由から、TiDB Serverless は TLS 1.2 と TLS 1.3 のみをサポートし、TLS 1.0 と TLS 1.1 バージョンはサポートしていません。詳細については、IETF [TLS 1.0 および TLS 1.1 の廃止](https://datatracker.ietf.org/doc/rfc8996/)を参照してください。

### 接続クライアントと TiDB Serverless 間の双方向 TLS 認証はサポートされていますか? {#is-two-way-tls-authentication-between-my-connection-client-and-tidb-serverless-supported}

いいえ。

TiDB Serverless は一方向の TLS 認証のみをサポートします。つまり、クライアントは公開キーを使用してTiDB Cloudクラスター証明書の秘密キーの署名を検証しますが、クラスターはクライアントを検証しません。

### TiDB Serverless では、安全な接続を確立するために TLS を構成する必要がありますか? {#does-tidb-serverless-have-to-configure-tls-to-establish-a-secure-connection}

標準接続の場合、TiDB Serverless は TLS 接続のみを許可し、非 SSL/TLS 接続は禁止します。これは、SSL/TLS が、インターネット経由で TiDB Serverless クラスターに接続する際に、インターネットへのデータ漏洩のリスクを軽減するための最も基本的なセキュリティ対策の 1 つであるためです。

プライベート エンドポイント接続では、 TiDB Cloudサービスへの高度に安全な一方向アクセスがサポートされ、データがパブリック インターネットに公開されないため、TLS の構成はオプションです。
