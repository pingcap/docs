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

TiDB Cloud API には、次の 2 つのバージョンがあります。

-   v1ベータ1
    -   クラスターレベルのリソース:
        -   [TiDB Cloud Starter または Essential クラスタ](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless) : TiDB Cloud Starter または Essential クラスターのクラスター、ブランチ、データ エクスポート タスク、およびデータ インポート タスクを管理します。
        -   [TiDB Cloud専用クラスタ](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated) : TiDB Cloud Dedicated クラスターのクラスター、リージョン、プライベート エンドポイント接続、およびデータ インポート タスクを管理します。
    -   組織またはプロジェクトレベルのリソース:
        -   [請求する](https://docs.pingcap.com/tidbcloud/api/v1beta1/billing) : TiDB Cloudクラスターの課金を管理します。
        -   [データサービス](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice) : TiDB Cloudクラスターのデータ サービス内のリソースを管理します。
        -   [IAMは](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam) : TiDB Cloudクラスターの API キーを管理します。
        -   [MSP（非推奨）](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)
-   [v1ベータ](https://docs.pingcap.com/tidbcloud/api/v1beta)
    -   [プロジェクト](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Project)
    -   [クラスタ](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Cluster)
    -   [バックアップ](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Backup)
    -   [インポート（非推奨）](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Import)
    -   [復元する](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Restore)
