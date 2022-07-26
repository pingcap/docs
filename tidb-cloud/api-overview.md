---
title: TiDB Cloud API Overview
summary: Learn about what is TiDB Cloud API, its features, and how to use API to manage your TiDB Cloud clusters.
---

# TiDB Cloudの概要 {#tidb-cloud-api-overview}

TiDB Cloud APIは、 TiDB Cloud内の管理オブジェクトを管理するためのプログラムによるアクセスを提供する[RESTインターフェース](https://en.wikipedia.org/wiki/Representational_state_transfer)です。このAPIを使用すると、リソースを自動的かつ効率的に管理できます。

-   プロジェクト
-   クラスター
-   バックアップ
-   復元

APIには次の機能があります。

-   **JSONエンティティ。**すべてのエンティティはJSONで表されます。
-   **HTTPSのみ。**ネットワーク経由で送信されるすべてのデータがTLSで暗号化されていることを確認して、HTTPS経由でのみAPIにアクセスできます。
-   **キーベースのアクセスとダイジェスト認証。** TiDB Cloud APIにアクセスする前に、APIキーを生成する必要があります。すべてのリクエストは[HTTPダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)を介して認証され、APIキーがネットワーク経由で送信されないようにします。

TiDB Cloud APIの使用を開始するには、次のリソースを参照してください。

-   [はじめに](https://docs.pingcap.com/tidbcloud/api/v1#section/Get-Started)
-   [認証](https://docs.pingcap.com/tidbcloud/api/v1#section/Authentication)
-   [レート制限](https://docs.pingcap.com/tidbcloud/api/v1#section/Rate-Limiting)
-   [APIフルリファレンス](https://docs.pingcap.com/tidbcloud/api/v1#tag/Project)
