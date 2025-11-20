---
title: TLS Connections to TiDB Cloud Premium
summary: TiDB Cloud Premium に TLS 接続を導入します。
---

# TiDB Cloud PremiumへのTLS接続 {#tls-connections-to-tidb-cloud-premium}

TiDB Cloudでは、TLS 接続の確立はTiDB Cloud Premium インスタンスへの接続における基本的なセキュリティ対策の一つです。クライアント、アプリケーション、開発ツールからTiDB Cloud Premium インスタンスへの複数の TLS 接続を設定することで、データ転送のセキュリティを保護できます。セキュリティ上の理由から、 TiDB Cloud Premium は TLS 1.2 と TLS 1.3 のみをサポートし、TLS 1.0 と TLS 1.1 はサポートしていません。

データセキュリティを確保するため、 TiDB Cloud Premium インスタンスの証明機関 (CA) 証明書は[AWS プライベート認証局](https://aws.amazon.com/private-ca/)でホストされています。CA 証明書の秘密鍵は、 [FIPS 140-2 レベル 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139)セキュリティ標準を満たす AWS 管理のハードウェアセキュリティモジュール (HSM) に保存されます。

## 前提条件 {#prerequisites}

-   [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)または[SSO認証](/tidb-cloud/tidb-cloud-sso-authentication.md) 、次に[TiDB Cloud Premiumインスタンスを作成する](/tidb-cloud/premium/create-tidb-instance-premium.md)でTiDB Cloudにログインします。

-   安全な設定でインスタンスにアクセスするためのパスワードを設定します。

    これを行うには、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動し、 TiDB Cloud Premiumインスタンスの行にある「 **...」**をクリックし、 **「ルートパスワードの変更」**を選択します。パスワード設定で「**パスワードの自動生成」**をクリックすると、数字、大文字、小文字、特殊文字を含む16文字のルートパスワードが自動的に生成されます。

## TiDB Cloud Premiumインスタンスへのセキュリティ接続 {#secure-connection-to-a-tidb-cloud-premium-instance}

[TiDB Cloudコンソール](https://tidbcloud.com/)では、さまざまな接続方法の例を取得し、次のようにTiDB Cloud Premium インスタンスに接続できます。

1.  [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動し、 TiDB Cloud Premium インスタンスの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択します。

    IPアクセスリストを設定していない場合は、 **「IPアクセスリストの設定」**をクリックして、初回接続前に設定してください。詳細については、 [IPアクセスリストを設定する](/tidb-cloud/premium/configure-ip-access-list-premium.md)参照してください。

4.  **「CA証明書」**をクリックして、TiDBインスタンスへのTLS接続用のCA証明書をダウンロードしてください。CA証明書はデフォルトでTLS 1.2をサポートしています。

    > **注記：**
    >
    > -   ダウンロードしたCA証明書は、オペレーティングシステムのデフォルトのstorageパスに保存することも、別のstorageパスを指定することもできます。以降の手順では、コード例のCA証明書パスをご自身のCA証明書パスに置き換える必要があります。
    > -   TiDB Cloud Premium では、クライアントに TLS 接続の使用を強制しません。また、 [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)変数のユーザー定義構成は現在TiDB Cloud Premium ではサポートされていません。

5.  希望する接続方法を選択し、タブ上の接続文字列とサンプル コードを参照してインスタンスに接続します。

## TiDB Cloud Premium のルート証明書を管理する {#manage-root-certificates-for-tidb-cloud-premium}

TiDB Cloud Premium は、クライアントとTiDB Cloud Premium インスタンス間の TLS 接続に[AWS プライベート認証局](https://aws.amazon.com/private-ca/)証明書を CA として使用します。通常、CA 証明書の秘密鍵は、 [FIPS 140-2 レベル 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139)セキュリティ標準を満たす AWS マネージドハードウェアセキュリティモジュール (HSM) に安全に保管されます。

## よくある質問 {#faqs}

### TiDB Cloud Premium インスタンスに接続するためにサポートされている TLS バージョンはどれですか? {#which-tls-versions-are-supported-to-connect-to-my-tidb-cloud-premium-instance}

セキュリティ上の理由から、 TiDB Cloud Premium は TLS 1.2 と TLS 1.3 のみをサポートし、TLS 1.0 と TLS 1.1 はサポートしていません。詳細は IETF [TLS 1.0 および TLS 1.1 の廃止](https://datatracker.ietf.org/doc/rfc8996/)をご覧ください。

### クライアントとTiDB Cloud Premium 間の双方向 TLS 認証はサポートされていますか? {#is-two-way-tls-authentication-between-my-client-and-tidb-cloud-premium-supported}

いいえ。

TiDB Cloud Premium は現在、片方向 TLS 認証のみをサポートしており、双方向 TLS 認証はサポートしていません。双方向 TLS 認証が必要な場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。
