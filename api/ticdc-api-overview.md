---
title: TiCDC API Overview
summary: TiCDC の API を学習します。
---

# TiCDC API の概要 {#ticdc-api-overview}

[TiCDC](/ticdc/ticdc-overview.md) 、TiDBから増分データを複製するために使用されるツールです。具体的には、TiCDCはTiKVの変更ログを取得し、キャプチャしたデータをソートし、行ベースの増分データを下流のデータベースにエクスポートします。

TiCDC は、TiCDC クラスターのクエリと操作用に次の 2 つのバージョンの API を提供します。

-   [TiCDC オープンAPI v1](/ticdc/ticdc-open-api.md)
-   [TiCDC オープンAPI v2](/ticdc/ticdc-open-api-v2.md)

> **注記：**
>
> TiCDC OpenAPI v1は将来削除される予定です。TiCDC OpenAPI v2のご利用をお勧めします。

リクエストパラメータ、レスポンス例、使用方法など、各 API の詳細については、 [TiCDC オープンAPI v1](/ticdc/ticdc-open-api.md)および[TiCDC オープンAPI v2](/ticdc/ticdc-open-api-v2.md)参照してください。
