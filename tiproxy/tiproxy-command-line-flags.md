---
title: TiProxy Command-Line Flags
summary: TiProxy のコマンドライン起動フラグについて学習します。
---

# TiProxy コマンドラインフラグ {#tiproxy-command-line-flags}

このドキュメントでは、TiProxy を起動するときに使用できるコマンドライン フラグについて説明します。また、 `tiproxyctl`のフラグについても説明します。

## TiProxy サーバー {#tiproxy-server}

このセクションでは、サーバープログラム`tiproxy`のフラグを一覧表示します。

### <code>--config</code> {#code-config-code}

-   TiProxy 構成ファイルのパスを指定します。
-   タイプ: `string`
-   デフォルト: `""`
-   設定ファイルを指定する必要があります。詳細な設定項目については[TiProxy を構成する](/tiproxy/tiproxy-configuration.md)を参照してください。なお、設定ファイルが変更されると、TiProxy は自動的に設定を再読み込みします。そのため、設定ファイルを直接変更しないでください。 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md)または[`kubectl edit tc`](https://docs.pingcap.com/tidb-in-kubernetes/stable/modify-tidb-configuration)を実行して設定を変更することをお勧めします。

## TiProxy コントロール {#tiproxy-control}

このセクションでは、クライアント プログラム`tiproxyctl`のフラグを一覧表示します。

### <code>--log_encoder</code> {#code-log-encoder-code}

-   `tiproxyctl`のログ形式を指定します。
-   タイプ: `string`
-   デフォルト: `"tidb"`
-   デフォルトでは、TiDB と同じログ形式になります。ただし、次のいずれかとして指定することもできます。

    -   `console` : より人間が読みやすい形式
    -   `json` : 構造化されたログ形式

### <code>--log_level</code> {#code-log-level-code}

-   tiproxyctl のログ レベルを指定します。
-   タイプ: `string`
-   デフォルト: `"warn"`
-   `debug` `info` `panic`でき`error` `warn`

### <code>--curls</code> {#code-curls-code}

-   サーバーのアドレスを指定します。複数のリスニング アドレスを追加できます。
-   タイプ: `comma separated lists of ip:port`
-   デフォルト: `localhost:3080`
-   サーバー API ゲートウェイ アドレス。

### <code>-k</code> 、 <code>--insecure</code> {#code-k-code-code-insecure-code}

-   サーバーにダイヤルするときに TLS CA 検証をスキップするかどうかを指定します。
-   タイプ: `boolean`
-   デフォルト: `false`
-   テストに使用されます。

### <code>--ca</code> {#code-ca-code}

-   サーバーにダイヤルするときに CA を指定します。
-   タイプ: `string`
-   デフォルト: `""`

### <code>--cert</code> {#code-cert-code}

-   サーバーにダイヤルするときに証明書を指定します。
-   タイプ: `string`
-   デフォルト: `""`
