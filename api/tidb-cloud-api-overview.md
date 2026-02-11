---
title: TiDB Cloud API Overview
summary: TiDB Cloud API とは何か、その機能、API を使用してTiDB Cloudクラスターを管理する方法について学習します。
---

# TiDB CloudAPI の概要 {#tidb-cloud-api-overview}

> **注記：**
>
> TiDB Cloud API はベータ版です。

TiDB Cloud APIは、 TiDB Cloud内の管理オブジェクトを管理するためのプログラム的なアクセスを提供する[RESTインターフェース](https://en.wikipedia.org/wiki/Representational_state_transfer)です。このAPIを使用すると、プロジェクト、クラスタ、バックアップ、復元、インポート、課金、 [データサービス](https://docs.pingcap.com/tidbcloud/data-service-overview)内のリソースなどのリソースを自動的かつ効率的に管理できます。

API には次の機能があります。

-   **JSON エンティティ。**すべてのエンティティは JSON で表現されます。
-   **HTTPSのみ。API**へのアクセスはHTTPS経由でのみ可能であり、ネットワーク経由で送信されるすべてのデータはTLSで暗号化されます。
-   **キーベースのアクセスとダイジェスト認証。TiDB** TiDB Cloud APIにアクセスする前に、APIキーを生成する必要があります。詳細については、 [APIキー管理](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-key-management)ご覧ください。すべてのリクエストは[HTTPダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)を通じて認証されるため、APIキーがネットワーク経由で送信されることはありません。

TiDB Cloud API には、次の 2 つのバージョンがあります。

-   [v1ベータ1](/api/tidb-cloud-api-v1beta1.md) : TiDB Cloud Starter、Essential、Dedicated クラスター、および課金、データ サービス、 IAMリソースを管理します。
-   [v1ベータ](/api/tidb-cloud-api-v1beta.md) : TiDB Cloudのプロジェクト、クラスター、バックアップ、インポート、および復元を管理します。
