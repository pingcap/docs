---
title: DM-master Configuration File
summary: DM-master の設定ファイルについて学習します。
---

# DMマスターコンフィグレーションファイル {#dm-master-configuration-file}

このドキュメントでは、構成ファイル テンプレートと、このファイル内の各構成パラメータの説明を含む、DM-master の構成について説明します。

## コンフィグレーションファイルテンプレート {#configuration-file-template}

以下は DM-master の設定ファイル テンプレートです。

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

secret-key-path = "/path/to/secret/key"
```

## コンフィグレーションパラメータ {#configuration-parameters}

このセクションでは、DM マスターの構成パラメータについて説明します。

### グローバル構成 {#global-configuration}

| パラメータ                 | 説明                                                                                                                                                                                                                                                                                    |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`                | DMマスターの名前。                                                                                                                                                                                                                                                                            |
| `log-level`           | ログ レベルを`debug` 、 `info` 、 `warn` 、 `error` 、 `fatal`から指定します。デフォルトのログ レベルは`info`です。                                                                                                                                                                                                    |
| `log-file`            | ログ ファイルのディレクトリを指定します。パラメータが指定されていない場合、ログは標準出力に印刷されます。                                                                                                                                                                                                                                 |
| `master-addr`         | サービスを提供する DM マスターのアドレスを指定します。IP アドレスを省略し、&quot;:8261&quot; のようにポート番号のみを指定することもできます。                                                                                                                                                                                                   |
| `advertise-addr`      | DM マスターが外部に通知するアドレスを指定します。                                                                                                                                                                                                                                                            |
| `peer-urls`           | DM マスター ノードのピア URL を指定します。                                                                                                                                                                                                                                                            |
| `advertise-peer-urls` | DM マスターが外部にアドバタイズするピア URL を指定します。 `advertise-peer-urls`の値は、デフォルトでは`peer-urls`の値と同じです。                                                                                                                                                                                                 |
| `initial-cluster`     | 値`initial-cluster`は、初期クラスター内のすべての DM マスター ノードの`advertise-peer-urls`の値の組み合わせです。                                                                                                                                                                                                        |
| `join`                | `join`の値は、クラスター内の既存の DM マスター ノードの`advertise-peer-urls`の値の組み合わせです。DM マスター ノードが新しく追加された場合は、 `initial-cluster` `join`に置き換えます。                                                                                                                                                            |
| `ssl-ca`              | DM マスターが他のコンポーネントに接続するための信頼できる SSL CA のリストが含まれるファイルのパス。                                                                                                                                                                                                                               |
| `ssl-cert`            | DM マスターが他のコンポーネントに接続するための PEM 形式の X509 証明書を含むファイルのパス。                                                                                                                                                                                                                                 |
| `ssl-key`             | DM マスターが他のコンポーネントに接続するための PEM 形式の X509 キーを含むファイルのパス。                                                                                                                                                                                                                                  |
| `cert-allowed-cn`     | 一般名リスト。                                                                                                                                                                                                                                                                               |
| `secret-key-path`     | アップストリームおよびダウンストリームのパスワードを暗号化および復号化するために使用される秘密キーのファイル パス。ファイルには、64 文字の 16 進数 AES-256 秘密キーが含まれている必要があります。このキーを生成する 1 つの方法は、 `head -n 256 /dev/urandom | sha256sum`のようにランダム データの SHA256 チェックサムを計算することです。詳細については、 [DM暗号化と復号化のための秘密鍵をカスタマイズする](/dm/dm-customized-secret-key.md)参照してください。 |
