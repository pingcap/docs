---
title: TLS Connections to TiDB Cloud Premium
summary: TiDB Cloud PremiumにTLS接続を導入します。
---

# TiDB Cloud PremiumへのTLS接続 {#tls-connections-to-tidb-cloud-premium}

TiDB Cloudでは、TLS接続の確立は、 TiDB Cloud Premiumインスタンスへの接続における基本的なセキュリティ対策の一つです。クライアント、アプリケーション、開発ツールからTiDB Cloud Premiumインスタンスへの複数のTLS接続を設定することで、データ送信のセキュリティを保護できます。セキュリティ上の理由から、 TiDB Cloud PremiumはTLS 1.2とTLS 1.3のみをサポートし、TLS 1.0とTLS 1.1はサポートしていません。

データセキュリティを確保するため、 TiDB Cloud Premiumインスタンスの認証局（CA）証明書は[AWSプライベート認証局](https://aws.amazon.com/private-ca/)にホストされています。CA証明書の秘密鍵は、 [FIPS 140-2 レベル3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139)セキュリティ基準を満たすAWS管理のハードウェアセキュリティモジュール（HSM）に保存されています。

## 前提条件 {#prerequisites}

-   [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)または[SSO認証](/tidb-cloud/tidb-cloud-sso-authentication.md)を介してTiDB Cloudにログインし、 [TiDB Cloud Premiumインスタンスを作成します](/tidb-cloud/premium/create-tidb-instance-premium.md)。

-   安全な設定でインスタンスにアクセスするためのパスワードを設定してください。

    そのためには、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 TiDB Cloud Premium インスタンスの行にある「 **...」**をクリックして、 **「ルートパスワードの変更」**を選択します。パスワード設定で、「パスワード**の自動生成」をクリックすると、数字、大文字、小文字、特殊文字を含む 16 文字のルートパスワード**が自動的に生成されます。

## TiDB Cloud Premiumインスタンスへのセキュリティ接続 {#secure-connection-to-a-tidb-cloud-premium-instance}

[TiDB Cloudコンソール](https://tidbcloud.com/)では、さまざまな接続方法の例を確認し、次のようにしてTiDB Cloud Premium インスタンスに接続できます。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 TiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動してください。

2.  右上隅の**「接続」**をクリックしてください。ダイアログが表示されます。

3.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] を**クリックして設定します。詳細については、 [IPアクセスリストを設定する](/tidb-cloud/premium/configure-ip-access-list-premium.md)参照してください。

4.  **「CA証明書」**をクリックすると、 TiDB Cloud PremiumインスタンスへのTLS接続に必要なCA証明書をダウンロードできます。このCA証明書はデフォルトでTLS 1.2をサポートしています。

    > **注記：**
    >
    > -   ダウンロードしたCA証明書は、オペレーティングシステムのデフォルトのstorageパスに保存することも、別のstorageパスを指定することもできます。以降の手順では、コード例のCA証明書パスを、ご自身のCA証明書パスに置き換える必要があります。
    > -   TiDB Cloud Premiumでは、クライアントにTLS接続の使用を強制することはなく、 [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)変数のユーザー定義設定は現在TiDB Cloud Premiumではサポートされていません。

5.  ご希望の接続方法を選択し、タブに表示されている接続文字列とサンプルコードを参照してインスタンスに接続してください。

## TiDB Cloud Premium のルート証明書を管理する {#manage-root-certificates-for-tidb-cloud-premium}

TiDB Cloud Premium は、クライアントとTiDB Cloud Premium インスタンス間の TLS 接続の CA として[AWSプライベート認証局](https://aws.amazon.com/private-ca/)からの証明書を使用します。通常、CA 証明書の秘密キーは[FIPS 140-2 レベル3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139)セキュリティ標準を満たす AWS 管理のハードウェア セキュリティ モジュール (HSM) に安全に保存されます。

## よくある質問 {#faqs}

### TiDB Cloud Premiumインスタンスへの接続には、どのTLSバージョンがサポートされていますか？ {#which-tls-versions-are-supported-to-connect-to-my-tidb-cloud-premium-instance}

セキュリティ上の理由から、 TiDB Cloud Premium は TLS 1.2 と TLS 1.3 のみをサポートし、TLS 1.0 または TLS 1.1 はサポートしません。詳細については、「IETF [TLS 1.0およびTLS 1.1のサポートを終了します](https://datatracker.ietf.org/doc/rfc8996/)参照してください。

### 私のクライアントとTiDB Cloud Premium間の双方向TLS認証はサポートされていますか？ {#is-two-way-tls-authentication-between-my-client-and-tidb-cloud-premium-supported}

いいえ。

TiDB Cloud Premiumは、現在、一方向TLS認証のみをサポートしており、双方向TLS認証はサポートしていません。双方向TLS認証が必要な場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。
