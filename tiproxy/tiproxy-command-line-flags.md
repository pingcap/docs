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

このセクションでは、クライアント プログラム`tiproxyctl`の構文、オプション、およびコマンドについて説明します。

> **注記：**
>
> TiProxy コントロールはデバッグ用に特別に設計されており、TiProxy で将来導入される機能と完全に互換性がない可能性があります。情報を取得するためにこのツールをアプリケーションまたはユーティリティの開発に含めることはお勧めしません。

### 構文 {#syntax}

    tiproxyctl [flags] [command]

例えば：

    tiproxyctl --curls 127.0.0.1:3080 config get

### オプション {#options}

#### <code>--log_encoder</code> {#code-log-encoder-code}

-   `tiproxyctl`のログ形式を指定します。
-   タイプ: `string`
-   デフォルト: `"tidb"`
-   デフォルトでは、TiDB と同じログ形式になります。ただし、次のいずれかとして指定することもできます。

    -   `console` : より人間が読みやすい形式
    -   `json` : 構造化されたログ形式

#### <code>--log_level</code> {#code-log-level-code}

-   tiproxyctl のログ レベルを指定します。
-   タイプ: `string`
-   デフォルト: `"warn"`
-   `debug` `info` `error`でき`warn` `panic`

#### <code>--curls</code> {#code-curls-code}

-   サーバーのアドレスを指定します。複数のリスニング アドレスを追加できます。
-   タイプ: `comma separated lists of ip:port`
-   デフォルト: `localhost:3080`
-   サーバー API ゲートウェイ アドレス。

#### <code>-k, --insecure</code> {#code-k-insecure-code}

-   サーバーにダイヤルするときに TLS CA 検証をスキップするかどうかを指定します。
-   タイプ: `boolean`
-   デフォルト: `false`
-   テストに使用されます。

#### <code>--ca</code> {#code-ca-code}

-   サーバーにダイヤルするときに CA を指定します。
-   タイプ: `string`
-   デフォルト: `""`

#### <code>--cert</code> {#code-cert-code}

-   サーバーにダイヤルするときに証明書を指定します。
-   タイプ: `string`
-   デフォルト: `""`

### コマンド {#commands}

#### <code>config set</code> {#code-config-set-code}

`tiproxyctl config set`コマンドは、標準入力から TOML 形式の構成ファイルを読み取り、これらの構成項目を TiProxy に設定します。指定されていない構成項目は変更されないため、変更する項目のみを指定する必要があります。

次の例では、他の構成項目は変更せずに、 `log.level` `'warning'`に設定します。

```bash
$ cat test.toml
[log]
level='warning'
$ cat test.toml | tiproxyctl config set
""
$ tiproxyctl config get | grep level
level = 'warning'
```

#### <code>config get</code> {#code-config-get-code}

`tiproxyctl config get`コマンドは、現在の TiProxy 構成を TOML 形式で取得するために使用されます。

#### <code>health</code> {#code-health-code}

`tiproxyctl health`コマンドは、TiProxy のヘルス ステータスと構成のチェックサムを取得するために使用されます。TiProxy が正常に実行されている場合は、構成のチェックサムを返します。TiProxy がシャットダウンまたはオフラインの場合は、エラーを返します。

出力例:

```json
{"config_checksum":3006078629}
```
