---
title: DM-master Configuration File
summary: Learn the configuration file of DM-master.
---

# DMマスターコンフィグレーションファイル {#dm-master-configuration-file}

このドキュメントでは、構成ファイル テンプレートとこのファイル内の各構成パラメータの説明を含む、DM マスターの構成について紹介します。

## コンフィグレーションファイルのテンプレート {#configuration-file-template}

以下はDM-masterの設定ファイルのテンプレートです。

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

このセクションでは、DM マスターの設定パラメーターを紹介します。

### グローバル構成 {#global-configuration}

| パラメータ                 | 説明                                                                                                                       |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| `name`                | DM マスターの名前。                                                                                                              |
| `log-level`           | ログ レベルを`debug` 、 `info` 、 `warn` 、 `error` 、および`fatal`から指定します。デフォルトのログレベルは`info`です。                                      |
| `log-file`            | ログファイルのディレクトリを指定します。パラメーターが指定されていない場合、ログは標準出力に出力されます。                                                                    |
| `master-addr`         | サービスを提供するDMマスターのアドレスを指定します。 「:8261」のように、IP アドレスを省略してポート番号のみを指定することもできます。                                                 |
| `advertise-addr`      | DM マスターが外部にアドバタイズするアドレスを指定します。                                                                                           |
| `peer-urls`           | DM マスター ノードのピア URL を指定します。                                                                                               |
| `advertise-peer-urls` | DM マスターが外部にアドバタイズするピア URL を指定します。デフォルトでは、 `advertise-peer-urls`の値は`peer-urls`の値と同じです。                                    |
| `initial-cluster`     | 値`initial-cluster`は、最初のクラスター内のすべての DM マスター ノードの値`advertise-peer-urls`の組み合わせです。                                           |
| `join`                | 値`join`は、クラスター内の既存の DM マスター ノードの値`advertise-peer-urls`の組み合わせです。 DM マスター ノードを新たに追加する場合は、 `initial-cluster` `join`に置き換えます。 |
| `ssl-ca`              | DM マスターが他のコンポーネントに接続するための信頼できる SSL CA のリストを含むファイルのパス。                                                                    |
| `ssl-cert`            | DM マスターが他のコンポーネントに接続するための PEM 形式の X509 証明書を含むファイルのパス。                                                                    |
| `ssl-key`             | DM マスターが他のコンポーネントに接続するための PEM 形式の X509 キーを含むファイルのパス。                                                                     |
| `cert-allowed-cn`     | 通称リスト。                                                                                                                   |
