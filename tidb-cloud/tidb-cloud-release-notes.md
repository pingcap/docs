---
title: TiDB Cloud Release Notes in 2024
summary: Learn about the release notes of TiDB Cloud in 2024.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2024 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2024}

このページには、2024 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2024年5月21日 {#may-21-2024}

**一般的な変更**

-   Google Cloud でホストされている[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスタのうち[TiDB ノード サイズ](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)を新たに提供: `8 vCPU, 16 GiB`

## 2024年5月14日 {#may-14-2024}

**一般的な変更**

-   さまざまな地域の顧客にさらに対応できるよう、セクション[**タイムゾーン**](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization)のタイム ゾーンの選択範囲を拡張します。

-   VPC がTiDB Cloudの VPC とは異なるリージョンにある場合は[VPCピアリングの作成](/tidb-cloud/set-up-vpc-peering-connections.md)サポートします。

-   [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service)クエリ パラメータとともにパス パラメータをサポートします。

    この機能により、構造化 URL によるリソース識別が強化され、ユーザー エクスペリエンス、検索エンジン最適化 (SEO)、クライアント統合が改善され、開発者の柔軟性が向上し、業界標準との整合性が向上します。

    詳細については[基本的なプロパティ](/tidb-cloud/data-service-manage-endpoint.md#basic-properties)参照してください。

## 2024年4月16日 {#april-16-2024}

**CLIの変更**

-   新しい[TiDB CloudAPI](/tidb-cloud/api-overview.md)をベースに構築された[TiDB CloudCLI 1.0.0-beta.1](https://github.com/tidbcloud/tidbcloud-cli)導入します。新しい CLI には、次の新機能が追加されています。

    -   [TiDB Serverless クラスターからデータをエクスポートする](/tidb-cloud/serverless-export.md)
    -   [ローカルstorageからTiDB Serverlessクラスターにデータをインポートする](/tidb-cloud/ticloud-import-start.md)
    -   [OAuth による認証](/tidb-cloud/ticloud-auth-login.md)
    -   [TiDBボット経由で質問する](/tidb-cloud/ticloud-ai.md)

    TiDB Cloud CLI をアップグレードする前に、この新しい CLI は以前のバージョンと互換性がないことに注意してください。たとえば、CLI コマンドの`ticloud cluster` `ticloud serverless`に更新されました。詳細については、 [TiDB Cloud CLI リファレンス](/tidb-cloud/cli-reference.md)を参照してください。

## 2024年4月9日 {#april-9-2024}

**一般的な変更**

-   AWS でホストされている[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターに対して新しい[TiDB ノード サイズ](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)を提供します: `8 vCPU, 32 GiB` 。

## 2024年4月2日 {#april-2-2024}

**一般的な変更**

-   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターに対して、**無料**と**スケーラブル**の 2 つのサービス プランを導入します。

    さまざまなユーザー要件を満たすために、TiDB Serverless は無料かつスケーラブルなサービス プランを提供しています。始めたばかりの場合でも、増大するアプリケーション需要に対応するために拡張する場合でも、これらのプランは必要な柔軟性と機能を提供します。

    詳細については[クラスタ計画](/tidb-cloud/select-cluster-tier.md#cluster-plans)参照してください。

-   使用量の割り当てに達したときの TiDB Serverless クラスターのスロットル動作を変更します。これで、クラスターが使用量の割り当てに達すると、新しい接続の試行が直ちに拒否され、既存の操作に対するサービスが中断されなくなります。

    詳細については[使用量制限](/tidb-cloud/serverless-limitations.md#usage-quota)参照してください。

## 2024年3月5日 {#march-5-2024}

**一般的な変更**

-   新しい[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0)から[バージョン7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1)にアップグレードします。

**コンソールの変更**

-   [**請求する**](https://tidbcloud.com/console/org-settings/billing/payments)ページに「**コスト エクスプローラー」**タブを導入します。このタブは、組織のコスト レポートを長期にわたって分析およびカスタマイズするための直感的なインターフェイスを提供します。

    この機能を使用するには、組織の**請求**ページに移動し、**コスト エクスプローラー**タブをクリックします。

    詳細については[コストエクスプローラー](/tidb-cloud/tidb-cloud-billing.md#cost-explorer)参照してください。

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) [ノードレベルのリソースメトリック](/tidb-cloud/built-in-monitoring.md#server)の**制限**ラベルを表示します。

    **制限**ラベルには、クラスター内の各コンポーネントの CPU、メモリ、storageなどのリソースの最大使用量が表示されます。この機能強化により、クラスターのリソース使用率を監視するプロセスが簡素化されます。

    これらのメトリック制限にアクセスするには、クラスターの**[監視]**ページに移動し、 **[メトリック]**タブの**[サーバー]**カテゴリを確認します。

    詳細については[TiDB専用クラスタのメトリクス](/tidb-cloud/built-in-monitoring.md#server)参照してください。

## 2024年2月20日 {#february-20-2024}

**一般的な変更**

-   Google Cloud 上でさらに多くのTiDB Cloudノードの作成をサポートします。

    -   Google Cloud の[リージョン CIDR サイズの設定](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) of `/19`では、プロジェクトの任意のリージョン内に最大 124 個のTiDB Cloudノードを作成できるようになりました。
    -   プロジェクトの任意のリージョンに 124 を超えるノードを作成する場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)連絡して、 `/16`から`/18`までの IP 範囲のサイズをカスタマイズするためのサポートを受けることができます。

## 2024年1月23日 {#january-23-2024}

**一般的な変更**

-   TiDB、TiKV、 TiFlashのノード サイズ オプションとして 32 vCPU を追加します。

    1 つ`32 vCPU, 128 GiB` TiKV ノードごとに、ノードstorageの範囲は 200 GiB から 6144 GiB になります。

    次のシナリオでは、このようなノードを使用することをお勧めします。

    -   高負荷の本番環境
    -   非常に高いパフォーマンス

## 2024年1月16日 {#january-16-2024}

**一般的な変更**

-   プロジェクトの CIDR 構成を強化します。

    -   各プロジェクトに対してリージョン レベルの CIDR を直接設定できます。
    -   より広範な CIDR 値から CIDR 構成を選択できます。

    注: プロジェクトの以前のグローバル レベルの CIDR 設定は廃止されますが、アクティブ状態にある既存のリージョン CIDR はすべて影響を受けません。既存のクラスターのネットワークには影響はありません。

    詳細については[リージョンのCIDRを設定する](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)参照してください。

-   TiDB Serverless ユーザーは、クラスターのパブリック エンドポイントを無効にできるようになりました。

    詳細については[パブリックエンドポイントを無効にする](/tidb-cloud/connect-via-standard-connection-serverless.md#disable-a-public-endpoint)参照してください。

-   [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service)では、データ アプリ内のエンドポイントにアクセスするためのカスタム ドメインの構成がサポートされています。

    デフォルトでは、 TiDB Cloud Data Service は各データ アプリのエンドポイントにアクセスするためのドメイン`<region>.data.tidbcloud.com`を提供します。パーソナライズと柔軟性を高めるために、デフォルトのドメインを使用する代わりに、データ アプリのカスタム ドメインを構成できるようになりました。この機能により、データベース サービスにブランド化された URL を使用でき、セキュリティが強化されます。

    詳細については[データ サービスにおけるカスタム ドメイン](/tidb-cloud/data-service-custom-domain.md)参照してください。

## 2024年1月3日 {#january-3-2024}

**一般的な変更**

-   エンタープライズ認証プロセスを合理化するためのサポート[組織の SSO](https://tidbcloud.com/console/preferences/authentication) 。

    この機能を使用すると、 [Securityアサーションマークアップ言語 (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language)または[OpenIDコネクト（OIDC）](https://openid.net/developers/how-connect-works/)使用して、 TiDB Cloud を任意の ID プロバイダー (IdP) とシームレスに統合できます。

    詳細については[組織のSSO認証](/tidb-cloud/tidb-cloud-org-sso-authentication.md)参照してください。

-   新しい[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1)から[バージョン7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0)にアップグレードします。

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)のデュアル リージョン バックアップ機能が一般提供 (GA) になりました。

    この機能を使用すると、AWS または Google Cloud 内の地理的リージョン間でバックアップを複製できます。この機能により、データ保護と災害復旧機能の追加レイヤーが提供されます。

    詳細については[デュアルリージョンバックアップ](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)参照してください。
