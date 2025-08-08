---
title: DM-worker Configuration File
summary: DM-worker の設定ファイルについて学習します。
---

# DMワーカーコンフィグレーションファイル {#dm-worker-configuration-file}

このドキュメントでは、構成ファイル テンプレートと、このファイル内の各構成パラメータの説明を含む、DM ワーカーの構成について説明します。

## コンフィグレーションファイルテンプレート {#configuration-file-template}

以下は、DM ワーカーの構成ファイル テンプレートです。

```toml
# Worker Configuration.
name = "worker1"

# Log configuration.
log-level = "info"
log-file = "dm-worker.log"

# DM-worker listen address.
worker-addr = ":8262"
advertise-addr = "127.0.0.1:8262"
join = "http://127.0.0.1:8261,http://127.0.0.1:8361,http://127.0.0.1:8461"

keepalive-ttl = 60
relay-keepalive-ttl = 1800 # New in DM v2.0.2.
# relay-dir = "relay_log" # New in 5.4.0. When you use a relative path, check the deployment and start method of DM-worker to determine the full path.

ssl-ca = "/path/to/ca.pem"
ssl-cert = "/path/to/cert.pem"
ssl-key = "/path/to/key.pem"
cert-allowed-cn = ["dm"]
```

## コンフィグレーションパラメータ {#configuration-parameters}

### グローバル {#global}

#### <code>name</code> {#code-name-code}

-   DM ワーカーの名前。

#### <code>log-level</code> {#code-log-level-code}

-   ログ レベルを指定します。
-   デフォルト値: `info`
-   `fatal` `warn` `info` `error` `debug`

#### <code>log-file</code> {#code-log-file-code}

-   ログファイルのディレクトリを指定します。このパラメータが指定されていない場合、ログは標準出力に出力されます。

#### <code>worker-addr</code> {#code-worker-addr-code}

-   サービスを提供するDMワーカーのアドレスを指定します。IPアドレスを省略し、ポート番号のみ（例： `":8262"` ）を指定することもできます。

#### <code>advertise-addr</code> {#code-advertise-addr-code}

-   DM ワーカーが外部にアドバタイズするアドレスを指定します。

#### <code>join</code> {#code-join-code}

-   DM マスター構成ファイル内の 1 つ以上の[`master-addr`](/dm/dm-master-configuration-file.md#global-configuration)に対応します。

#### <code>keepalive-ttl</code> {#code-keepalive-ttl-code}

-   DM ワーカー ノードの上流データ ソースがリレー ログを有効にしていない場合の、DM ワーカー ノードから DM マスター ノードへのキープアライブ時間 (秒単位)。
-   デフォルト値: `60`
-   単位: 秒

#### <code>relay-keepalive-ttl</code> <span class="version-mark">DM v2.0.2の新機能</span> {#code-relay-keepalive-ttl-code-span-class-version-mark-new-in-dm-v2-0-2-span}

-   DM ワーカー ノードの上流データ ソースがリレー ログを有効にしている場合の、DM ワーカー ノードから DM マスター ノードへのキープアライブ時間 (秒単位)。
-   デフォルト値: `1800`
-   単位: 秒

#### <code>relay-dir</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-relay-dir-code-span-class-version-mark-new-in-v5-4-0-span}

-   バインドされた上流データソースでリレーログが有効になっている場合、DM-workerはリレーログをこのディレクトリに保存します。このパラメータは、上流データソースの設定よりも優先されます。

#### <code>ssl-ca</code> {#code-ssl-ca-code}

-   DM-worker が他のコンポーネントに接続するための信頼できる SSL CA のリストが含まれるファイルのパス。

#### <code>ssl-cert</code> {#code-ssl-cert-code}

-   DM-worker が他のコンポーネントに接続するための PEM 形式の X509 証明書を含むファイルのパス。

#### <code>ssl-key</code> {#code-ssl-key-code}

-   DM-worker が他のコンポーネントに接続するための PEM 形式の X509 キーを含むファイルのパス。

#### <code>cert-allowed-cn</code> {#code-cert-allowed-cn-code}

-   一般名リスト。
