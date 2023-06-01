---
title: TiDB Cloud API Overview
summary: Learn about what is TiDB Cloud API, its features, and how to use API to manage your TiDB Cloud clusters.
---

# TiDB CloudAPI 概要<span style="color: #fff; background-color: #00bfff; border-radius: 4px; font-size: 0.5em; vertical-align: middle; margin-left: 16px; padding: 0 2px;">ベータ版</span> {#tidb-cloud-api-overview-span-style-color-fff-background-color-00bfff-border-radius-4px-font-size-0-5em-vertical-align-middle-margin-left-16px-padding-0-2px-beta-span}

> **ノート：**
>
> [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta">TiDB CloudAPI</a>](https://docs.pingcap.com/tidbcloud/api/v1beta)はベータ版です。

TiDB CloudAPI は、 TiDB Cloud内の管理オブジェクトを管理するためのプログラムによるアクセスを提供する[<a href="https://en.wikipedia.org/wiki/Representational_state_transfer">RESTインターフェース</a>](https://en.wikipedia.org/wiki/Representational_state_transfer)です。この API を通じて、プロジェクト、クラスター、バックアップ、復元などのリソースを自動的かつ効率的に管理できます。

API には次の機能があります。

-   **JSON エンティティ。**すべてのエンティティは JSON で表現されます。
-   **HTTPS のみ。** API には HTTPS 経由でのみアクセスできるため、ネットワーク経由で送信されるすべてのデータは TLS で暗号化されます。
-   **キーベースのアクセスとダイジェスト認証。** TiDB Cloud API にアクセスする前に、API キーを生成する必要があります。すべてのリクエストは[<a href="https://en.wikipedia.org/wiki/Digest_access_authentication">HTTPダイジェスト認証</a>](https://en.wikipedia.org/wiki/Digest_access_authentication)を通じて認証され、API キーがネットワーク経由で送信されることはありません。

TiDB Cloud API の使用を開始するには、 [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta">TiDB CloudAPI ドキュメント</a>](https://docs.pingcap.com/tidbcloud/api/v1beta)の次のリソースを参照してください。

-   [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/Get-Started">始めましょう</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Get-Started)
-   [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication">認証</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication)
-   [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/Rate-Limiting">レート制限</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Rate-Limiting)
-   [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project">API の完全なリファレンス</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project)
-   [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog">変更履歴</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog)
