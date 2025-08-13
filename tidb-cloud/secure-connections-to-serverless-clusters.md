---
title: TLS Connections to TiDB Cloud Starter or Essential
summary: TiDB Cloud Starter およびTiDB Cloud Essential に TLS 接続を導入します。
aliases: ['/tidbcloud/secure-connections-to-serverless-tier-clusters']
---

# TiDB Cloud Starter または Essential への TLS 接続 {#tls-connections-to-tidb-cloud-starter-or-essential}

クライアントとTiDB Cloud StarterまたはTiDB Cloud Essentialクラスタ間の安全なTLS接続を確立することは、データベース接続における基本的なセキュリティ対策の一つです。TiDB TiDB Cloudのサーバー証明書は、独立したサードパーティの証明書プロバイダによって発行されます。サーバー側のデジタル証明書をダウンロードすることなく、 TiDB Cloudクラスタに簡単に接続できます。

> **注記：**
>
> TiDB Cloud Dedicated クラスターへの TLS 接続を確立する方法については、 [TiDB Cloud専用へのTLS接続](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md)参照してください。

## 前提条件 {#prerequisites}

-   [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)または[SSO認証](/tidb-cloud/tidb-cloud-sso-authentication.md)経由でTiDB Cloudにログインします。
-   [TiDB Cloudクラスターを作成する](/tidb-cloud/tidb-cloud-quickstart.md) 。

## TiDB Cloudクラスターへの TLS 接続 {#tls-connection-to-a-tidb-cloud-cluster}

[TiDB Cloudコンソール](https://tidbcloud.com/)では、さまざまな接続方法の例を取得し、次のようにTiDB Cloudクラスターに接続できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。ダイアログが表示されます。

3.  ダイアログでは、接続タイプのデフォルト設定を`Public`のままにして、希望する接続方法とオペレーティング システムを選択します。

4.  パスワードをまだ設定していない場合は、 **「パスワードを生成」**をクリックして、クラスター用のランダムパスワードを生成します。パスワードはサンプル接続文字列に自動的に埋め込まれ、クラスターへの接続が簡単になります。

    > **注記：**
    >
    > -   ランダム パスワードは、大文字、小文字、数字、特殊文字を含む 16 文字で構成されます。
    > -   このダイアログを閉じると、生成されたパスワードは表示されなくなりますので、安全な場所に保存してください。パスワードを忘れた場合は、このダイアログの**「パスワードをリセット」**をクリックしてリセットできます。
    > -   TiDB Cloudクラスターにはインターネット経由でアクセスできます。他の場所でパスワードを使用する必要がある場合は、データベースのセキュリティを確保するためにパスワードをリセットすることをお勧めします。

5.  接続文字列を使用してクラスターに接続します。

    > **注記：**
    >
    > TiDB Cloudクラスターに接続する際は、ユーザー名にクラスターのプレフィックスを含め、引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)参照してください。

## ルート証明書の管理 {#root-certificate-management}

### ルート証明書の発行と有効性 {#root-certificate-issuance-and-validity}

TiDB Cloudは、クライアントとTiDB Cloudクラスタ間のTLS接続において、 [レッツ・エンクリプト](https://letsencrypt.org/)の証明書を証明機関（CA）として使用します。TiDB TiDB Cloud証明書の有効期限が切れると、クラスタの通常の動作や確立されたTLSセキュア接続に影響を与えることなく、自動的にローテーションされます。

JavaやGoなど、クライアントがシステムのルートCAストアをデフォルトで使用する場合、CAルートのパスを指定せずにTiDB Cloudクラスタに安全に接続できます。ただし、一部のドライバやORMはシステムルートCAストアを使用しません。そのような場合は、ドライバやORMのCAルートパスをシステムルートCAストアに設定する必要があります。例えば、macOS上のPythonで[mysqlクライアント](https://github.com/PyMySQL/mysqlclient)使用してTiDB Cloudクラスタに接続する場合、引数`ssl`に`ca: /etc/ssl/cert.pem`設定する必要があります。

複数の証明書が含まれる証明書ファイルを受け入れない DBeaver などの GUI クライアントを使用している場合は、 [ISRGルートX1](https://letsencrypt.org/certs/isrgrootx1.pem)証明書をダウンロードする必要があります。

### ルート証明書のデフォルトパス {#root-certificate-default-path}

異なるオペレーティング システムにおけるルート証明書のデフォルトのstorageパスは次のとおりです。

**macOS**

    /etc/ssl/cert.pem

**Debian / Ubuntu / Arch**

    /etc/ssl/certs/ca-certificates.crt

**RedHat / Fedora / CentOS / Mageia**

    /etc/pki/tls/certs/ca-bundle.crt

**高山**

    /etc/ssl/cert.pem

**オープンSUSE**

    /etc/ssl/ca-bundle.pem

**ウィンドウズ**

WindowsはCAルートへの特定のパスを提供していません。代わりに、 [レジストリ](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/local-machine-and-current-user-certificate-stores)使用して証明書を保存します。そのため、WindowsでCAルートパスを指定するには、次の手順に従います。

1.  [ISRGルートX1証明書](https://letsencrypt.org/certs/isrgrootx1.pem)をダウンロードし、 `<path_to_ca>`などの任意のパスに保存します。
2.  TiDB Cloudクラスターに接続するときは、パス ( `<path_to_ca>` ) を CA ルート パスとして使用します。

## よくある質問 {#faqs}

### TiDB Cloudクラスターに接続するためにサポートされている TLS バージョンはどれですか? {#which-tls-versions-are-supported-to-connect-to-my-tidb-cloud-cluster}

セキュリティ上の理由から、 TiDB Cloud はTLS 1.2 と TLS 1.3 のみをサポートし、TLS 1.0 と TLS 1.1 はサポートしていません。詳細は IETF [TLS 1.0 および TLS 1.1 の廃止](https://datatracker.ietf.org/doc/rfc8996/)をご覧ください。

### 接続クライアントとTiDB Cloud間の双方向 TLS 認証はサポートされていますか? {#is-two-way-tls-authentication-between-my-connection-client-and-tidb-cloud-supported}

いいえ。

TiDB Cloud は一方向の TLS 認証のみをサポートします。つまり、クライアントは公開キーを使用してTiDB Cloudクラスター証明書の秘密キーの署名を検証しますが、クラスターはクライアントを検証しません。

### TiDB Cloud、安全な接続を確立するために TLS を構成する必要がありますか? {#does-tidb-cloud-have-to-configure-tls-to-establish-a-secure-connection}

標準接続の場合、 TiDB CloudはTLS接続のみを許可し、SSL/TLS以外の接続は禁止しています。これは、SSL/TLSが、インターネット経由でTiDB Cloudクラスターに接続する際に、インターネットへのデータ漏洩リスクを軽減するための最も基本的なセキュリティ対策の一つであるためです。

プライベート エンドポイント接続では、 TiDB Cloudサービスへの高度に安全な一方向アクセスがサポートされ、データがパブリック インターネットに公開されないため、TLS の構成はオプションです。
