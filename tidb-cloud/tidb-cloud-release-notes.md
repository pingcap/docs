---
title: TiDB Cloud Release Notes in 2024
summary: Learn about the release notes of TiDB Cloud in 2024.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2024 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2024}

このページには 2024 年[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリースノートが記載されています。

## 2024 年 3 月 5 日 {#march-5-2024}

**一般的な変更点**

-   新しい[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0)から[v7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1)にアップグレードします。

**コンソールの変更**

-   [**請求する**](https://tidbcloud.com/console/org-settings/billing/payments)ページの**[Cost Explorer]**タブを紹介します。このタブは、組織の長期的なコスト レポートを分析およびカスタマイズするための直感的なインターフェイスを提供します。

    この機能を使用するには、組織の**[請求]**ページに移動し、 **[コスト エクスプローラー]**タブをクリックします。

    詳細については、 [コストエクスプローラー](/tidb-cloud/tidb-cloud-billing.md#cost-explorer)を参照してください。

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) [ノードレベルのリソースメトリック](/tidb-cloud/built-in-monitoring.md#server)の**制限**ラベルを表示します。

    **制限**ラベルには、クラスター内の各コンポーネントの CPU、メモリ、storageなどのリソースの最大使用量が表示されます。この機能強化により、クラスターのリソース使用率を監視するプロセスが簡素化されます。

    これらのメトリック制限にアクセスするには、クラスターの**[監視]**ページに移動し、 **[メトリック]**タブの**[サーバー]**カテゴリを確認します。

    詳細については、 [TiDB 専用クラスターのメトリック](/tidb-cloud/built-in-monitoring.md#server)を参照してください。

## 2024 年 2 月 20 日 {#february-20-2024}

**一般的な変更点**

-   Google Cloud 上でのさらに多くのTiDB Cloudノードの作成をサポートします。

    -   Google Cloud の`/19`の[リージョン CIDR サイズの構成](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)により、プロジェクトの任意のリージョン内に最大 124 のTiDB Cloudノードを作成できるようになりました。
    -   プロジェクトの任意のリージョンに 124 を超えるノードを作成する場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)に連絡して、 `/16`から`/18`の範囲の IP 範囲サイズをカスタマイズするための支援を得ることができます。

## 2024 年 1 月 23 日 {#january-23-2024}

**一般的な変更点**

-   TiDB、TiKV、およびTiFlashのノード サイズ オプションとして 32 vCPU を追加します。

    各`32 vCPU, 128 GiB` TiKV ノードのノードstorageの範囲は 200 GiB ～ 6144 GiB です。

    このようなノードは、次のシナリオで使用することをお勧めします。

    -   ワークロードの高い本番環境
    -   非常に高いパフォーマンス

## 2024 年 1 月 16 日 {#january-16-2024}

**一般的な変更点**

-   プロジェクトの CIDR 構成を強化します。

    -   各プロジェクトにリージョンレベルの CIDR を直接設定できます。
    -   より広範囲の CIDR 値から CIDR 構成を選択できます。

    注: プロジェクトの以前のグローバル レベルの CIDR 設定は廃止されましたが、アクティブ状態にある既存のすべてのリージョン CIDR は影響を受けません。既存のクラスターのネットワークには影響はありません。

    詳細については、 [リージョンの CIDR を設定する](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)を参照してください。

-   TiDB サーバーレス ユーザーは、クラスターのパブリック エンドポイントを無効にすることができるようになりました。

    詳細については、 [パブリックエンドポイントを無効にする](/tidb-cloud/connect-via-standard-connection-serverless.md#disable-a-public-endpoint)を参照してください。

-   [データサービス（ベータ版）](https://tidbcloud.com/console/data-service)データ アプリのエンドポイントにアクセスするためのカスタム ドメインの構成がサポートされています。

    デフォルトでは、 TiDB Cloudデータ サービスは、各データ アプリのエンドポイントにアクセスするためのドメイン`<region>.data.tidbcloud.com`を提供します。パーソナライゼーションと柔軟性を強化するために、デフォルトのドメインを使用する代わりに、データ アプリのカスタム ドメインを構成できるようになりました。この機能により、データベース サービスにブランド URL を使用できるようになり、セキュリティが強化されます。

    詳細については、 [Data Service のカスタム ドメイン](/tidb-cloud/data-service-custom-domain.md)を参照してください。

## 2024 年 1 月 3 日 {#january-3-2024}

**一般的な変更点**

-   企業の認証プロセスを合理化するためのサポート[組織の SSO](https://tidbcloud.com/console/preferences/authentication) 。

    この機能を使用すると、 [Securityアサーション マークアップ言語 (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language)または[OpenID Connect (OIDC)](https://openid.net/developers/how-connect-works/)を使用してTiDB Cloud を任意のアイデンティティ プロバイダー (IdP) とシームレスに統合できます。

    詳細については、 [組織のSSO認証](/tidb-cloud/tidb-cloud-org-sso-authentication.md)を参照してください。

-   新しい[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[v7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1)から[v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0)にアップグレードします。

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)のデュアル リージョン バックアップ機能が一般提供 (GA) になりました。

    この機能を使用すると、AWS または Google Cloud 内の地理的リージョン間でバックアップをレプリケートできます。この機能は、データ保護および災害復旧機能の追加レイヤーを提供します。

    詳細については、 [デュアルリージョンバックアップ](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)を参照してください。
