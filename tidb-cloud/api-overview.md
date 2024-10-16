---
title: TiDB Cloud API Overview
summary: TiDB Cloud API とは何か、その機能、API を使用してTiDB Cloudクラスターを管理する方法について学習します。
---

# TiDB CloudAPI 概要<span style="color: #fff; background-color: #00bfff; border-radius: 4px; font-size: 0.5em; vertical-align: middle; margin-left: 16px; padding: 0 2px;">ベータ版</span> {#tidb-cloud-api-overview-span-style-color-fff-background-color-00bfff-border-radius-4px-font-size-0-5em-vertical-align-middle-margin-left-16px-padding-0-2px-beta-span}

> **注記：**
>
> TiDB Cloud API はベータ版です。

TiDB Cloud API は、 TiDB Cloud内の管理オブジェクトを管理するためのプログラムによるアクセスを提供する[RESTインターフェース](https://en.wikipedia.org/wiki/Representational_state_transfer)です。この API を使用すると、プロジェクト、クラスター、バックアップ、復元、インポート、課金、 [データサービス](/tidb-cloud/data-service-overview.md)内のリソースなどのリソースを自動的かつ効率的に管理できます。

API には次の機能があります。

-   **JSON エンティティ。**すべてのエンティティは JSON で表現されます。
-   **HTTPS のみ。API**には HTTPS 経由でのみアクセスでき、ネットワーク経由で送信されるすべてのデータは TLS で暗号化されます。
-   **キーベースのアクセスとダイジェスト認証。TiDB** TiDB Cloud API にアクセスする前に、API キーを生成する必要があります[APIキー管理](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-key-management)を参照)。すべてのリクエストは[HTTP ダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)を通じて認証され、API キーがネットワーク経由で送信されることはありません。

TiDB Cloud API の使用を開始するには、 TiDB Cloud API ドキュメントの次のリソースを参照してください。

-   [始める](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Get-Started)
-   [認証](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication)
-   [レート制限](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Rate-Limiting)
-   API の完全なリファレンス
    -   v1ベータ1
        -   [請求する](https://docs.pingcap.com/tidbcloud/api/v1beta1/billing)
        -   [データサービス](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)
        -   [IAMは](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam)
        -   [MSP (非推奨)](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)
    -   [v1ベータ](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project)
-   [変更履歴](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog)
