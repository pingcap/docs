---
title: TiProxy API Overview
summary: TiProxy の API について学習します。
---

# TiProxy API の概要 {#tiproxy-api-overview}

[TiProxy](/tiproxy/tiproxy-overview.md)はPingCAPの公式プロキシコンポーネントです。クライアントとTiDBサーバーの間に配置され、負荷分散、接続の持続性、サービス検出、その他のTiDB機能を提供します。

TiProxy はオプションのコンポーネントです。サードパーティ製のプロキシコンポーネントを使用することも、プロキシを使用せずに TiDBサーバーに直接接続することもできます。

TiProxy API を使用して、TiProxy クラスターで次の操作を実行できます。

-   [TiProxy の設定を取得する](/tiproxy/tiproxy-api.md#get-tiproxy-configuration)
-   [TiProxy設定を設定する](/tiproxy/tiproxy-api.md#set-tiproxy-configuration)
-   [TiProxy のヘルスステータスを取得する](/tiproxy/tiproxy-api.md#get-tiproxy-health-status)
-   [TiProxy監視データを取得する](/tiproxy/tiproxy-api.md#get-tiproxy-monitoring-data)

リクエストパラメータ、レスポンス例、使用方法など、各 API の詳細については、 [TiProxy API](/tiproxy/tiproxy-api.md)参照してください。
