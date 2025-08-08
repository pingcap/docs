---
title: TiDB Cloud API Overview
summary: TiDB Cloud API とは何か、その機能、API を使用してTiDB Cloudクラスターを管理する方法について学習します。
---

# TiDB CloudAPI の概要 (ベータ版) {#tidb-cloud-api-overview-beta}

> **注記：**
>
> TiDB Cloud API はベータ版です。

TiDB Cloud APIは、 TiDB Cloud内の管理オブジェクトを管理するためのプログラム的なアクセスを提供する[RESTインターフェース](https://en.wikipedia.org/wiki/Representational_state_transfer)です。このAPIを使用すると、プロジェクト、クラスタ、バックアップ、リストア、インポート、課金、そして[データサービス](/tidb-cloud/data-service-overview.md)内のリソースなどのリソースを自動的かつ効率的に管理できます。

API には次の機能があります。

-   **JSON エンティティ。**すべてのエンティティは JSON で表現されます。
-   **HTTPSのみ。API**へのアクセスはHTTPS経由でのみ可能であり、ネットワーク経由で送信されるすべてのデータはTLSで暗号化されます。
-   **キーベースのアクセスとダイジェスト認証。TiDB** TiDB Cloud APIにアクセスする前に、APIキーを生成する必要があります（ [APIキー管理](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-key-management)を参照）。すべてのリクエストは[HTTPダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)を通じて認証されるため、APIキーがネットワーク経由で送信されることはありません。

TiDB Cloud API の使用を開始するには、 TiDB Cloud API ドキュメントの次のリソースを参照してください。

-   [始める](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Get-Started)
-   [認証](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication)
-   [レート制限](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Rate-Limiting)
-   API の完全なリファレンス
    -   v1ベータ1
        -   [請求する](https://docs.pingcap.com/tidbcloud/api/v1beta1/billing)
        -   [データサービス](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)
        -   [IAMは](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam)
        -   [MSP（非推奨）](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)
    -   [v1ベータ](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project)
-   [変更履歴](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog)
