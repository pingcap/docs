---
title: DM-master Configuration File
summary: Learn the configuration file of DM-master.
---

# DMマスターコンフィグレーションファイル {#dm-master-configuration-file}

このドキュメントでは、構成ファイル テンプレートと、このファイル内の各構成パラメーターの説明を含む、DM-master の構成について説明します。

## コンフィグレーションファイルのテンプレート {#configuration-file-template}

以下は、DM-master の構成ファイルのテンプレートです。

```toml
name = "dm-master"

# log configuration
log-level = "info"
log-file = "dm-master.log"

# DM-master listening address
master-addr = ":8261"
advertise-addr = "127.0.0.1:8261"

# URLs for peer traffic
peer-urls = "http://127.0.0.1:8291"
advertise-peer-urls = "http://127.0.0.1:8291"

# cluster configuration
initial-cluster = "master1=http://127.0.0.1:8291,master2=http://127.0.0.1:8292,master3=http://127.0.0.1:8293"
join = ""

ssl-ca = "/path/to/ca.pem"
ssl-cert = "/path/to/cert.pem"
ssl-key = "/path/to/key.pem"
cert-allowed-cn = ["dm"] 
```

## コンフィグレーションパラメータ {#configuration-parameters}

このセクションでは、DM-master の構成パラメーターを紹介します。

### グローバル構成 {#global-configuration}

| パラメータ                 | 説明                                                                                                                            |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `name`                | DM マスターの名前。                                                                                                                   |
| `log-level`           | `debug` 、 `info` 、 `warn` 、 `error` 、および`fatal`からログ レベルを指定します。デフォルトのログ レベルは`info`です。                                          |
| `log-file`            | ログ ファイル ディレクトリを指定します。パラメータが指定されていない場合、ログは標準出力に出力されます。                                                                         |
| `master-addr`         | サービスを提供する DM マスターのアドレスを指定します。 「:8261」のように、IP アドレスを省略してポート番号のみを指定することもできます。                                                    |
| `advertise-addr`      | DM-master が外部にアドバタイズするアドレスを指定します。                                                                                             |
| `peer-urls`           | DM マスター ノードのピア URL を指定します。                                                                                                    |
| `advertise-peer-urls` | DM-master が外部にアドバタイズするピア URL を指定します。 `advertise-peer-urls`の値はデフォルトで`peer-urls`の値と同じです。                                        |
| `initial-cluster`     | `initial-cluster`の値は、初期クラスター内のすべての DM マスター ノードの`advertise-peer-urls`の値の組み合わせです。                                               |
| `join`                | `join`の値は、クラスター内の既存の DM マスター ノードの`advertise-peer-urls`の値の組み合わせです。 DM-master ノードが新しく追加された場合は、 `initial-cluster` `join`に置き換えます。 |
| `ssl-ca`              | DM-master が他のコンポーネントと接続するための信頼できる SSL CA のリストを含むファイルのパス。                                                                      |
| `ssl-cert`            | DM マスターが他のコンポーネントと接続するための PEM 形式の X509 証明書を含むファイルのパス。                                                                         |
| `ssl-key`             | DM マスターが他のコンポーネントと接続するための PEM 形式の X509 キーを含むファイルのパス。                                                                          |
| `cert-allowed-cn`     | 共通名リスト。                                                                                                                       |
