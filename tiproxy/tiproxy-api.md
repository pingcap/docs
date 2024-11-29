---
title: TiProxy API
summary: TiProxy API を使用して、構成、ヘルス ステータス、監視データにアクセスする方法を学習します。
---

# TiプロキシAPI {#tiproxy-api}

[Tiプロキシ](/tiproxy/tiproxy-overview.md) 、構成、ヘルス ステータス、および監視データにアクセスするための API エンドポイントを提供します。

> **注記：**
>
> TiProxy API はデバッグ用に特別に設計されており、TiProxy で将来導入される機能と完全に互換性がない可能性があります。情報を取得するためにこのツールをアプリケーションまたはユーティリティ開発に含めることはお勧めしません。

TiProxy API にアクセスするためのアドレスは`http://${host}:${port}${path}`です。ここで、 `${host}:${port}` TiProxy 構成項目[`api.addr`](/tiproxy/tiproxy-configuration.md#addr-1)によって指定され、 `${path}`アクセスする特定の API エンドポイントです。例:

```bash
curl http://127.0.0.1:3080/api/admin/config/
```

## TiProxy 設定を取得する {#get-tiproxy-configuration}

### リクエストURI {#request-uri}

`GET /api/admin/config/`

### パラメータの説明 {#parameter-descriptions}

クエリパラメータは次のとおりです。

-   `format` : (オプション) 返される構成の形式を指定します。値のオプションは`json`と`toml`です。デフォルト値は`toml`です。

### 例 {#example}

次の例では、TiProxy 構成を JSON 形式で取得します。

```bash
curl "http://127.0.0.1:3080/api/admin/config/?format=json"
```

## TiProxy設定を設定する {#set-tiproxy-configuration}

現在、TiProxy 構成を変更するには TOML 形式のみを使用できます。指定されていない構成項目は変更されないため、変更する項目のみを指定する必要があります。

### リクエストURI {#request-uri}

`PUT /api/admin/config/`

### リクエスト本文 {#request-body}

TiProxy 構成を TOML 形式で提供する必要があります。例:

```toml
[log]
level='warning'
```

### 例 {#example}

次の例では、他の構成項目は変更せずに、 `log.level` `'warning'`に設定します。

1.  現在の TiProxy 構成を取得します。

    ```bash
    curl http://127.0.0.1:3080/api/admin/config/
    ```

    出力は次のようになります。

    ```toml
    [log]
    encoder = 'tidb'
    level = 'info'
    ```

2.  `test.toml`ファイルで`log.level`の値を指定し、 `PUT /api/admin/config/`リクエストを送信して`log.level`の値を更新します。

    ```shell
    $ cat test.toml
    [log]
    level='warning'
    $ curl -X PUT --data-binary @test.toml http://127.0.0.1:3080/api/admin/config/
    ```

3.  変更された TiProxy 構成を取得します。

    ```bash
    curl http://127.0.0.1:3080/api/admin/config/
    ```

    出力は次のようになります。

    ```toml
    [log]
    encoder = 'tidb'
    level = 'warning'
    ```

## TiProxy のヘルスステータスを取得する {#get-tiproxy-health-status}

このエンドポイントは、TiProxy のヘルス ステータスと構成のチェックサムを取得するために使用されます。TiProxy が正常に実行されている場合、このエンドポイントは構成のチェックサムを返します。TiProxy がシャットダウンまたはオフラインの場合は、エラーを返します。

### リクエストURI {#request-uri}

`GET /api/debug/health`

### 例 {#example}

```bash
curl http://127.0.0.1:3080/api/debug/health
```

出力は次のようになります。

```bash
{"config_checksum":3006078629}
```

## TiProxy監視データを取得する {#get-tiproxy-monitoring-data}

### リクエストURI {#request-uri}

`GET /metrics/`

### 例 {#example}

```bash
curl http://127.0.0.1:3080/metrics/
```
