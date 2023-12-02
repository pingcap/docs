---
title: DM-worker Configuration File
summary: Learn the configuration file of DM-worker.
---

# DM ワーカーコンフィグレーションファイル {#dm-worker-configuration-file}

このドキュメントでは、構成ファイル テンプレートとこのファイル内の各構成パラメーターの説明を含む、DM ワーカーの構成について紹介します。

## コンフィグレーションファイルのテンプレート {#configuration-file-template}

以下は、DM ワーカーの構成ファイルのテンプレートです。

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

| パラメータ                 | 説明                                                                                                                                         |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                | DM ワーカーの名前。                                                                                                                                |
| `log-level`           | ログ レベルを`debug` 、 `info` 、 `warn` 、 `error` 、および`fatal`から指定します。デフォルトのログレベルは`info`です。                                                        |
| `log-file`            | ログファイルのディレクトリを指定します。このパラメータが指定されていない場合、ログは標準出力に出力されます。                                                                                     |
| `worker-addr`         | サービスを提供するDMワーカーのアドレスを指定します。 「:8262」のように、IP アドレスを省略してポート番号のみを指定することもできます。                                                                   |
| `advertise-addr`      | DM ワーカーが外部にアドバタイズするアドレスを指定します。                                                                                                             |
| `join`                | DM マスター設定ファイル内の 1 つ以上の[`master-addr`](/dm/dm-master-configuration-file.md#global-configuration)に対応します。                                     |
| `keepalive-ttl`       | DM ワーカー ノードのアップストリーム データ ソースがリレー ログを有効にしていない場合の、DM ワーカー ノードから DM マスター ノードへのキープアライブ時間 (秒単位)。デフォルト値は 60 秒です。                                 |
| `relay-keepalive-ttl` | DM ワーカー ノードのアップストリーム データ ソースでリレー ログが有効になっている場合の、DM ワーカー ノードから DM マスター ノードへのキープアライブ時間 (秒単位)。デフォルト値は 1800 秒です。このパラメータは DM v2.0.2 以降に追加されました。 |
| `relay-dir`           | バインドされたアップストリーム データ ソースでリレー ログが有効になっている場合、DM ワーカーはリレー ログをこのディレクトリに保存します。このパラメーターは v5.4.0 の新機能であり、アップストリーム データ ソースの構成より優先されます。              |
| `ssl-ca`              | DM ワーカーが他のコンポーネントに接続するための信頼できる SSL CA のリストを含むファイルのパス。                                                                                      |
| `ssl-cert`            | DM ワーカーが他のコンポーネントに接続するための PEM 形式の X509 証明書を含むファイルのパス。                                                                                      |
| `ssl-key`             | DM ワーカーが他のコンポーネントに接続するための PEM 形式の X509 キーを含むファイルのパス。                                                                                       |
| `cert-allowed-cn`     | 通称リスト。                                                                                                                                     |
