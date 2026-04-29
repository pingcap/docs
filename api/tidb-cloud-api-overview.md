---
title: TiDB Cloud API Overview
summary: TiDB Cloud APIとは何か、その機能、そしてAPIを使用してTiDB Cloudクラスタを管理する方法について学びましょう。
aliases: ['/ja/tidbcloud/api-overview/']
---

# TiDB Cloud APIの概要 {#tidb-cloud-api-overview}

> **注記：**
>
> TiDB Cloud APIはベータ版です。

TiDB Cloud APIは[RESTインターフェース](https://en.wikipedia.org/wiki/Representational_state_transfer)APIであり、 TiDB Cloud内の管理オブジェクトをプログラムで管理するためのアクセスを提供します。このAPIを使用すると、プロジェクト、クラスタ、バックアップ、リストア、インポート、請求、データ[データサービス](https://docs.pingcap.com/tidbcloud/data-service-overview)内のリソースなどのリソースを自動的かつ効率的に管理できます。

このAPIには以下の機能があります。

-   **JSONエンティティ。**すべてのエンティティはJSON形式で表現されます。
-   **HTTPSのみ対応。API**へのアクセスはHTTPS経由でのみ可能で、ネットワーク上で送信されるすべてのデータはTLSで暗号化されます。
-   **キーベースのアクセスとダイジェスト認証。** TiDB Cloud API にアクセスする前に、API キーを生成する必要があります。詳細については、 [APIキー管理](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-key-management)を参照してください。すべてのリクエストは[HTTPダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)を通じて認証され、API キーがネットワーク経由で送信されることはありません。

TiDB Cloud APIは、以下のバージョンで利用可能です。

-   [v1beta2](/api/tidb-cloud-api-v1beta2.md) ： TiDB Cloud Premiumインスタンスを管理します。
-   [v1beta1](/api/tidb-cloud-api-v1beta1.md) ： TiDB Cloud Starter、 Essential、およびDedicatedクラスタ、ならびに課金、データサービス、およびIAMリソースを管理します。
-   [v1beta](/api/tidb-cloud-api-v1beta.md) : TiDB Cloudのプロジェクト、クラスター、バックアップ、インポート、リストアを管理します。
