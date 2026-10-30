---
title: TLS Connections to TiDB Cloud Starter or Essential
summary: TiDB Cloud Starter およびTiDB Cloud Essential に TLS 接続を導入します。
aliases: ['/ja/tidbcloud/secure-connections-to-serverless-tier-clusters']
---

# TiDB Cloud Starter または Essential への TLS 接続 {#tls-connections-to-tidb-cloud-starter-or-essential}

クライアントとTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンス間の安全なTLS接続を確立することは、データベース接続における基本的なセキュリティ対策の一つです。TiDB Cloudのサーバー証明書は、独立したサードパーティの証明書プロバイダーによって発行されます。サーバー側のデジタル証明書をダウンロードすることなく、 TiDB Cloud StarterまたはEssentialインスタンスに簡単に接続できます。

> **Note:**
>
> TiDB Cloud Dedicated クラスターへの TLS 接続を確立する方法については、 [TiDB Cloud DedicatedへのTLS接続](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md)を参照してください。

## 前提条件 {#prerequisites}

- [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)または[SSO認証](/tidb-cloud/tidb-cloud-sso-authentication.md)経由でTiDB Cloudにログインします。
- [TiDB Cloud StarterまたはEssentialインスタンスを作成する](/tidb-cloud/create-tidb-cluster-serverless.md) 。

## TiDB Cloud StarterまたはEssentialインスタンスへの TLS 接続 {#tls-connection-to-a-starter-or-essential-instance}

[TiDB Cloudコンソール](https://tidbcloud.com/)では、さまざまな接続方法の例を取得し、次のようにTiDB Cloud StarterまたはEssentialインスタンスに接続できます。

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、TiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして概要ページに移動します。

2. 右上隅の**Connect**をクリックします。ダイアログが表示されます。

3. ダイアログでは、接続タイプのデフォルト設定を`Public`のままにして、希望する接続方法とオペレーティングシステムを選択します。

4. パスワードをまだ設定していない場合は、 **Generate Password**をクリックして、TiDB Cloud StarterまたはEssentialインスタンス用のランダムパスワードを生成します。パスワードはサンプル接続文字列に自動的に埋め込まれ、TiDB Cloud StarterまたはEssentialインスタンスへの接続が簡単になります。

    > **Note:**
    >
    > - ランダムパスワードは、大文字、小文字、数字、特殊文字を含む 16 文字で構成されます。
    > - このダイアログを閉じると、生成されたパスワードは表示されなくなりますので、安全な場所に保存してください。パスワードを忘れた場合は、このダイアログの**Reset Password**をクリックしてリセットできます。
    > - TiDB Cloud StarterまたはEssentialインスタンスにはインターネット経由でアクセスできます。他の場所でパスワードを使用する必要がある場合は、データベースのセキュリティを確保するためにパスワードをリセットすることをお勧めします。

5. 接続文字列を使用してTiDB Cloud StarterまたはEssentialインスタンスに接続します。

    > **Note:**
    >
    > TiDB Cloud StarterまたはEssentialインスタンスに接続する際は、ユーザー名にTiDB Cloud StarterまたはEssentialインスタンスのプレフィックスを含め、引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

## ルート証明書の管理 {#root-certificate-management}

### ルート証明書の発行と有効性 {#root-certificate-issuance-and-validity}

TiDB Cloudは、クライアントとTiDB Cloud StarterまたはEssentialインスタンス間のTLS接続において、 [Let's Encrypt](https://letsencrypt.org/)の証明書を証明機関（CA）として使用します。TiDB Cloud証明書の有効期限が切れると、TiDB Cloud StarterまたはEssentialインスタンスの通常の動作や確立されたTLSセキュア接続に影響を与えることなく、自動的にローテーションされます。

JavaやGoなど、クライアントがシステムのルートCAストアをデフォルトで使用する場合、CAルートのパスを指定せずにTiDB Cloud StarterまたはEssentialインスタンスに安全に接続できます。ただし、一部のドライバやORMはシステムルートCAストアを使用しません。そのような場合は、ドライバやORMのCAルートパスをシステムルートCAストアに設定する必要があります。例えば、macOS上のPythonで[mysqlclient](https://github.com/PyMySQL/mysqlclient)を使用してTiDB Cloud StarterまたはEssentialインスタンスに接続する場合、引数`ssl`に`ca: /etc/ssl/cert.pem`を設定する必要があります。

複数の証明書が含まれる証明書ファイルを受け入れない DBeaver などの GUI クライアントを使用している場合は、 [ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem)証明書をダウンロードする必要があります。

### ルート証明書のデフォルトパス {#root-certificate-default-path}

異なるオペレーティングシステムにおけるルート証明書のデフォルトのストレージパスは次のとおりです。

**macOS**

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

**Alpine**

```
/etc/ssl/cert.pem
```

**OpenSUSE**

```
/etc/ssl/ca-bundle.pem
```

**Windows**

WindowsはCAルートへの特定のパスを提供していません。代わりに、 [レジストリ](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/local-machine-and-current-user-certificate-stores)を使用して証明書を保存します。そのため、WindowsでCAルートパスを指定するには、次の手順に従います。

1. [ISRG Root X1証明書](https://letsencrypt.org/certs/isrgrootx1.pem)をダウンロードし、 `<path_to_ca>`などの任意のパスに保存します。
2. TiDB Cloud StarterまたはEssentialインスタンスに接続するときは、パス ( `<path_to_ca>` ) を CA ルートパスとして使用します。

## よくある質問 {#faqs}

### TiDB Cloud StarterまたはEssentialインスタンスに接続するためにサポートされている TLS バージョンはどれですか? {#which-tls-versions-are-supported-to-connect-to-my-starter-or-essential-instance}

セキュリティ上の理由から、 TiDB Cloud はTLS 1.2 と TLS 1.3 のみをサポートし、TLS 1.0 と TLS 1.1 はサポートしていません。詳細は IETF [TLS 1.0 および TLS 1.1 の廃止](https://datatracker.ietf.org/doc/rfc8996/)をご覧ください。

### 接続クライアントとTiDB Cloud間の双方向 TLS 認証はサポートされていますか? {#is-two-way-tls-authentication-between-my-connection-client-and-tidb-cloud-supported}

いいえ。

TiDB Cloud は一方向の TLS 認証のみをサポートします。つまり、クライアントは公開キーを使用してTiDB Cloud StarterまたはEssentialインスタンス証明書の秘密キーの署名を検証しますが、TiDB Cloud StarterまたはEssentialインスタンスはクライアントを検証しません。

### TiDB Cloudでは、安全な接続を確立するために TLS を構成する必要がありますか? {#does-tidb-cloud-have-to-configure-tls-to-establish-a-secure-connection}

標準接続の場合、 TiDB CloudはTLS接続のみを許可し、SSL/TLS以外の接続は禁止しています。これは、SSL/TLSが、インターネット経由でTiDB Cloud StarterまたはEssentialインスタンスに接続する際に、インターネットへのデータ漏洩リスクを軽減するための最も基本的なセキュリティ対策の一つであるためです。

プライベートエンドポイント接続では、 TiDB Cloudサービスへの高度に安全な一方向アクセスがサポートされ、データがパブリックインターネットに公開されないため、TLS の構成はオプションです。
