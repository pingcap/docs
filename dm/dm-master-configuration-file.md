---
title: DM-master Configuration File
summary: Learn the configuration file of DM-master.
---

# DMマスターConfiguration / コンフィグレーションファイル {#dm-master-configuration-file}

このドキュメントでは、DMマスターの構成を紹介します。これには、構成ファイルテンプレートと、このファイルの各構成パラメーターの説明が含まれます。

## Configuration / コンフィグレーションファイルテンプレート {#configuration-file-template}

以下は、DM-masterの構成ファイルテンプレートです。

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

## Configuration / コンフィグレーションパラメーター {#configuration-parameters}

このセクションでは、DM-masterの構成パラメーターを紹介します。

### グローバル構成 {#global-configuration}

| パラメータ                 | 説明                                                                                                                   |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------- |
| `name`                | DMマスターの名前。                                                                                                           |
| `log-level`           | ログレベルを`debug` 、 `error` `info`から`fatal`し`warn` 。デフォルトのログレベルは`info`です。                                                |
| `log-file`            | ログファイルディレクトリを指定します。パラメーターが指定されていない場合、ログは標準出力に出力されます。                                                                 |
| `master-addr`         | サービスを提供するDMマスターのアドレスを指定します。 IPアドレスを省略して、「：8261」などのポート番号のみを指定できます。                                                    |
| `advertise-addr`      | DMマスターが外部にアドバタイズするアドレスを指定します。                                                                                        |
| `peer-urls`           | DMマスターノードのピアURLを指定します。                                                                                               |
| `advertise-peer-urls` | DMマスターが外部にアドバタイズするピアURLを指定します。デフォルトの値`advertise-peer-urls`は、 `peer-urls`の値と同じです。                                     |
| `initial-cluster`     | 値`initial-cluster`は、初期クラスタのすべてのDMマスターノードの`advertise-peer-urls`の値の組み合わせです。                                            |
| `join`                | 値`join`は、クラスタに存在するDMマスターノードの`advertise-peer-urls`の値の組み合わせです。 DMマスターノードが新しく追加された場合は、 `initial-cluster`を`join`に置き換えます。 |
| `ssl-ca`              | DMマスターが他のコンポーネントと接続するための信頼できるSSLCAのリストを含むファイルのパス。                                                                    |
| `ssl-cert`            | DMマスターが他のコンポーネントと接続するためのPEM形式のX509証明書を含むファイルのパス。                                                                     |
| `ssl-key`             | DMマスターが他のコンポーネントと接続するためのPEM形式のX509キーを含むファイルのパス。                                                                      |
| `cert-allowed-cn`     | 一般名リスト。                                                                                                              |
