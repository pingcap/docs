---
title: TiProxy Command-Line Flags
summary: TiProxy のコマンドライン起動フラグについて学習します。
---

# TiProxy コマンドラインフラグ {#tiproxy-command-line-flags}

このドキュメントでは、TiProxy を起動する際に使用できるコマンドラインフラグについて説明します。また、 `tiproxyctl`のフラグについても説明します。

## TiProxy サーバー {#tiproxy-server}

このセクションでは、サーバープログラム`tiproxy`のフラグを一覧表示します。

### <code>--advertise-addr</code> {#code-advertise-addr-code}

-   クライアントがこの TiProxy インスタンスに接続するために使用するアドレスを指定します。
-   タイプ: `string`
-   デフォルト: `""`
-   このフラグは、 TiUPまたはTiDB Operatorを使用して TiProxy をデプロイすると自動的に設定されます。設定されていない場合は、TiProxy インスタンスの外部 IP アドレスが使用されます。

### <code>--config</code> {#code-config-code}

-   TiProxy 構成ファイルのパスを指定します。
-   タイプ: `string`
-   デフォルト: `""`
-   設定ファイルを指定する必要があります。詳細な設定項目については、 [TiProxy を設定する](/tiproxy/tiproxy-configuration.md)を参照してください。設定ファイルが変更されると、TiProxyは自動的に設定を再読み込みするため、設定ファイルを直接変更しないでください。3または[`kubectl edit tc`](https://docs.pingcap.com/tidb-in-kubernetes/stable/modify-tidb-configuration) [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md)実行して設定を変更することをお勧めします。

## TiProxy コントロール {#tiproxy-control}

このセクションでは、クライアント プログラム`tiproxyctl`のインストール方法、構文、オプション、およびコマンドについて説明します。

### TiProxyコントロールをインストールする {#install-tiproxy-control}

TiProxy Control は、次の 2 つの方法のいずれかを使用してインストールできます。

> **注記：**
>
> TiProxy Control はデバッグ用に特別に設計されており、TiProxy に将来導入される機能と完全に互換性がない可能性があります。情報を取得するためにこのツールをアプリケーションやユーティリティの開発に組み込むことは推奨されません。

#### TiUPを使用してインストール {#install-using-tiup}

[TiUP](/tiup/tiup-overview.md)インストールした後、 `tiup install tiproxy`コマンドを使用して TiProxy と TiProxy Control のバイナリプログラムをダウンロードしてインストールできます。インストール後、 `tiup --binary tiproxy`コマンドを使用して TiProxy のインストールパスを確認できます。TiProxy Control は TiProxy と同じディレクトリにあります。

例えば：

```shell
tiup install tiproxy
# download https://tiup-mirrors.pingcap.com/tiproxy-v1.3.0-linux-amd64.tar.gz 22.51 MiB / 22.51 MiB 100.00% 13.99 MiB/s
ls `tiup --binary tiproxy`ctl
# /root/.tiup/components/tiproxy/v1.3.0/tiproxyctl
```

#### ソースコードからコンパイルする {#compile-from-source-code}

コンパイル環境要件: [行く](https://golang.org/) 1.21以降

コンパイル手順: [TiProxyプロジェクト](https://github.com/pingcap/tiproxy)のルート ディレクトリに移動し、 `make`コマンドを使用してコンパイルし、 `tiproxyctl`生成します。

```shell
git clone https://github.com/pingcap/tiproxy.git
cd tiproxy
make
ls bin/tiproxyctl
```

### 構文 {#syntax}

    tiproxyctl [flags] [command]

例えば：

    tiproxyctl --host 127.0.0.1 --port 3080 config get

### オプション {#options}

#### <code>--host</code> {#code-host-code}

-   TiProxyサーバーのアドレスを指定します。
-   タイプ: `string`
-   デフォルト: `localhost`

#### <code>--port</code> {#code-port-code}

-   TiProxy API ゲートウェイのポート番号を指定します。
-   タイプ: `int`
-   デフォルト: `3080`

#### <code>--log_encoder</code> {#code-log-encoder-code}

-   `tiproxyctl`のログ形式を指定します。
-   タイプ: `string`
-   デフォルト: `"tidb"`
-   デフォルトではTiDBと同じログ形式が使用されます。ただし、次のいずれかを指定することもできます。

    -   `console` : より人間が読みやすい形式
    -   `json` : 構造化されたログ形式

#### <code>--log_level</code> {#code-log-level-code}

-   tiproxyctl のログ レベルを指定します。
-   タイプ: `string`
-   デフォルト: `"warn"`
-   `debug` `info` `error`でき`panic` `warn`

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

`tiproxyctl config set`コマンドは標準入力からTOML形式の設定ファイルを読み取り、これらの設定項目をTiProxyに設定します。指定されていない設定項目は変更されないため、変更したい項目のみを指定してください。

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

`tiproxyctl health`コマンドは、TiProxy のヘルスステータスと設定のチェックサムを取得するために使用されます。TiProxy が正常に動作している場合は、設定のチェックサムを返します。TiProxy がシャットダウンまたはオフラインの場合は、エラーを返します。

出力例:

```json
{"config_checksum":3006078629}
```

#### <code>traffic capture</code> {#code-traffic-capture-code}

`tiproxyctl traffic capture`コマンドはトラフィックをキャプチャするために使用されます。

オプション:

-   `--output` : (必須) トラフィック ファイルを保存するディレクトリを指定します。
-   `--duration` : (必須) キャプチャ期間を指定します。単位は`m` (分)、 `h` (時間)、 `d` (日) のいずれかです。例えば、 `--duration=1h`指定すると 1 時間のトラフィックがキャプチャされます。

例：

次のコマンドは、 `10.0.1.10:3080`の TiProxy インスタンスに接続し、1 時間のトラフィックをキャプチャし、それを TiProxy インスタンスの`/tmp/traffic`ディレクトリに保存します。

```shell
tiproxyctl traffic capture --host 10.0.1.10 --port 3080 --output="/tmp/traffic" --duration=1h
```

#### <code>traffic replay</code> {#code-traffic-replay-code}

`tiproxyctl traffic replay`コマンドは、キャプチャされたトラフィックを再生するために使用されます。

オプション:

-   `--username` : (必須) 再生用のデータベース ユーザー名を指定します。
-   `--password` : (オプション) ユーザー名のパスワードを指定します。デフォルト値は空の文字列`""`です。
-   `--input` : (必須) トラフィック ファイルを含むディレクトリを指定します。
-   `--speed` : (オプション) 再生速度の乗数を指定します。範囲は`[0.1, 10]`です。デフォルト値は`1`で、元の速度で再生されます。

例：

次のコマンドは、ユーザー名`u1`とパスワード`123456`を使用して`10.0.1.10:3080`の TiProxy インスタンスに接続し、TiProxy インスタンスの`/tmp/traffic`ディレクトリからトラフィック ファイルを読み取り、元の速度の 2 倍でトラフィックを再生します。

```shell
tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic" --speed=2
```

#### <code>traffic cancel</code> {#code-traffic-cancel-code}

`tiproxyctl traffic cancel`コマンドは、現在のキャプチャまたは再生タスクをキャンセルするために使用されます。

#### <code>traffic show</code> {#code-traffic-show-code}

`tiproxyctl traffic show`コマンドは、履歴キャプチャおよび再生タスクを表示するために使用されます。

出力の`status`フィールドはタスクのステータスを示し、次の値が可能です。

-   `done` : タスクは正常に完了しました。
-   `canceled` : タスクはキャンセルされました。理由は`error`フィールドで確認できます。
-   `running` ：タスクは実行中です。完了率は`progress`フィールドで確認できます。

出力例:

```json
[
  {
    "type": "capture",
    "start_time": "2024-09-01T14:30:40.99096+08:00",
    "end_time": "2024-09-01T16:30:40.99096+08:00",
    "duration": "2h",
    "output": "/tmp/traffic",
    "progress": "100%",
    "status": "done"
  },
  {
    "type": "capture",
    "start_time": "2024-09-02T18:30:40.99096+08:00",
    "end_time": "2024-09-02T19:00:40.99096+08:00",
    "duration": "2h",
    "output": "/tmp/traffic",
    "progress": "25%",
    "status": "canceled",
    "error": "canceled manually"
  },
  {
    "type": "capture",
    "start_time": "2024-09-03T13:31:40.99096+08:00",
    "duration": "2h",
    "output": "/tmp/traffic",
    "progress": "45%",
    "status": "running"
  }
]
```
