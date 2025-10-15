---
title: TiProxy API
summary: TiProxy API を使用して構成、ヘルス ステータス、監視データにアクセスする方法を学習します。
---

# TiProxy API {#tiproxy-api}

[TiProxy](/tiproxy/tiproxy-overview.md) 、構成、ヘルス ステータス、および監視データにアクセスするための API エンドポイントを提供します。

> **注記：**
>
> TiProxy APIはデバッグ用に特別に設計されており、TiProxyに将来導入される機能との互換性が完全には保証されない可能性があります。情報取得のためにこのツールをアプリケーションやユーティリティの開発に組み込むことは推奨されません。

TiProxy APIにアクセスするためのアドレスは`http://${host}:${port}${path}`です。3 `${host}:${port}` TiProxy設定項目[`api.addr`](/tiproxy/tiproxy-configuration.md#addr-1)で指定され、 `${path}`アクセスしたい特定のAPIエンドポイントです。例：

```bash
curl http://127.0.0.1:3080/api/admin/config/
```

## TiProxy の設定を取得する {#get-tiproxy-configuration}

### リクエストURI {#request-uri}

`GET /api/admin/config/`

### パラメータの説明 {#parameter-descriptions}

クエリパラメータは次のとおりです。

-   `format` : (オプション) 返される設定の形式を指定します。値のオプションは`json`と`toml`です。デフォルト値は`toml`です。

### 例 {#example}

次の例では、TiProxy 構成を JSON 形式で取得します。

```bash
curl "http://127.0.0.1:3080/api/admin/config/?format=json"
```

## TiProxy設定を設定する {#set-tiproxy-configuration}

現在、TiProxyの設定変更にはTOML形式のみを使用できます。指定されていない設定項目は変更されないため、変更したい項目のみを指定してください。

### リクエストURI {#request-uri}

`PUT /api/admin/config/`

### リクエスト本文 {#request-body}

TiProxyの設定をTOML形式で提供する必要があります。例：

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

このエンドポイントは、TiProxy のヘルスステータスと設定のチェックサムを取得するために使用されます。TiProxy が正常に動作している場合、このエンドポイントは設定のチェックサムを返します。TiProxy がシャットダウンまたはオフラインの場合、エラーを返します。

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

## アクセス制御 {#access-control}

[`server-http-tls`](/tiproxy/tiproxy-configuration.md#server-http-tls)でTLSを有効にし、 [安全](/tiproxy/tiproxy-configuration.md#security)セクションの`server-http-tls`サブセクションにある`cert-allowed-cn`オプションを設定することで、TiProxy APIへのアクセスを制限できます。TiProxyはクライアント証明書の共通名（CN）を[コンポーネント呼び出し元のIDを確認する](/enable-tls-between-components.md#verify-component-callers-identity)に使用します。

TLS が有効になっていない場合は、代わりにファイアウォール ルールを使用してアクセスを制御できます。
