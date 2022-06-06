---
title: DM-worker Configuration File
summary: Learn the configuration file of DM-worker.
---

# DM-workerConfiguration / コンフィグレーションファイル {#dm-worker-configuration-file}

このドキュメントでは、DMワーカーの構成を紹介します。これには、構成ファイルテンプレートと、このファイルの各構成パラメーターの説明が含まれます。

## Configuration / コンフィグレーションファイルテンプレート {#configuration-file-template}

以下は、DM-workerの構成ファイルテンプレートです。

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

## Configuration / コンフィグレーションパラメーター {#configuration-parameters}

### グローバル {#global}

| パラメータ                 | 説明                                                                                                                                    |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| `name`                | DMワーカーの名前。                                                                                                                            |
| `log-level`           | ログレベルを`debug` 、 `error` `info`から`fatal`し`warn` 。デフォルトのログレベルは`info`です。                                                                 |
| `log-file`            | ログファイルディレクトリを指定します。このパラメーターが指定されていない場合、ログは標準出力に出力されます。                                                                                |
| `worker-addr`         | サービスを提供するDM-workerのアドレスを指定します。 IPアドレスを省略して、「：8262」などのポート番号のみを指定できます。                                                                  |
| `advertise-addr`      | DM-workerが外部にアドバタイズするアドレスを指定します。                                                                                                      |
| `join`                | DM-master構成ファイルの1つ以上の[`master-addr` s](/dm/dm-master-configuration-file.md#global-configuration)に対応します。                               |
| `keepalive-ttl`       | DM-workerノードのアップストリームデータソースがリレーログを有効にしない場合の、DM-workerノードからDM-masterノードまでのキープアライブ時間（秒単位）。デフォルト値は60秒です。                                 |
| `relay-keepalive-ttl` | DM-workerノードのアップストリームデータソースがリレーログを有効にしている場合の、DM-workerノードからDM-masterノードまでのキープアライブ時間（秒単位）。デフォルト値は1800秒です。このパラメーターは、DMv2.0.2以降に追加されました。 |
| `relay-dir`           | バインドされたアップストリームデータソースでリレーログが有効になっている場合、DM-workerはリレーログをこのディレクトリに保存します。このパラメーターはv5.4.0の新機能であり、アップストリームデータソースの構成よりも優先されます。              |
| `ssl-ca`              | DM-workerが他のコンポーネントと接続するための信頼できるSSLCAのリストを含むファイルのパス。                                                                                  |
| `ssl-cert`            | DM-workerが他のコンポーネントと接続するためのPEM形式のX509証明書を含むファイルのパス。                                                                                   |
| `ssl-key`             | DM-workerが他のコンポーネントと接続するためのPEM形式のX509キーを含むファイルのパス。                                                                                    |
| `cert-allowed-cn`     | 一般名リスト。                                                                                                                               |
