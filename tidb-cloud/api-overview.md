---
title: TiDB Cloud API Overview
summary: Learn about what is TiDB Cloud API, its features, and how to use API to manage your TiDB Cloud clusters.
---

# TiDB CloudAPI 概要<span style="color: #fff; background-color: #00bfff; border-radius: 4px; font-size: 0.5em; vertical-align: middle; margin-left: 16px; padding: 0 2px;">ベータ版</span> {#tidb-cloud-api-overview-span-style-color-fff-background-color-00bfff-border-radius-4px-font-size-0-5em-vertical-align-middle-margin-left-16px-padding-0-2px-beta-span}

> **ノート：**
>
> [TiDB CloudAPI](https://docs.pingcap.com/tidbcloud/api/v1beta)はベータ版です。

TiDB Cloud API は、 TiDB Cloud内の管理オブジェクトを管理するためのプログラムによるアクセスを提供する[REST インターフェイス](https://en.wikipedia.org/wiki/Representational_state_transfer)です。この API を通じて、プロジェクト、クラスター、バックアップ、復元、インポートなどのリソースを自動的かつ効率的に管理できます。

API には次の機能があります。

-   **JSON エンティティ。**すべてのエンティティは JSON で表現されます。
-   **HTTPS のみ。** HTTPS 経由でのみ API にアクセスできるため、ネットワーク経由で送信されるすべてのデータは TLS で暗号化されます。
-   **キーベースのアクセスとダイジェスト認証。** TiDB Cloud API にアクセスする前に、API キーを生成する必要があります。すべてのリクエストは[HTTP ダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)によって認証され、API キーがネットワーク経由で送信されないようにします。

TiDB Cloud API の使用を開始するには、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)の次のリソースを参照してください。

-   [始めましょう](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Get-Started)
-   [認証](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication)
-   [レート制限](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Rate-Limiting)
-   [API の完全なリファレンス](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project)
-   [変更ログ](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog)
