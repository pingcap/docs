---
title: DM-master Configuration File
summary: DM-master の設定ファイルについて説明します。
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

#### `name` {#name}

-   DM マスターの名前。

#### `log-level` {#log-level}

-   ログ レベルを指定します。
-   デフォルト値: `info`
-   `fatal` `warn` `info` `error` `debug`

#### `log-file` {#log-file}

-   ログファイルのディレクトリを指定します。パラメータが指定されていない場合、ログは標準出力に出力されます。

#### `master-addr` {#master-addr}

-   サービスを提供するDMマスターのアドレスを指定します。IPアドレスを省略し、ポート番号のみ（例： `":8261"` ）を指定することもできます。

#### `advertise-addr` {#advertise-addr}

-   DM マスターが外部に通知するアドレスを指定します。

#### `peer-urls` {#peer-urls}

-   DM マスター ノードのピア URL を指定します。

#### `advertise-peer-urls` {#advertise-peer-urls}

-   DMマスターが外部にアドバタイズするピアURLを指定します。デフォルト値は`advertise-peer-urls`で、 [`peer-urls`](#peer-urls)と同じです。

#### `initial-cluster` {#initial-cluster}

-   値`initial-cluster`は、初期クラスター内のすべての DM マスター ノードの[`advertise-peer-urls`](#advertise-peer-urls)値の組み合わせです。

#### `join` {#join}

-   `join`の値は、クラスター内の既存の DM マスターノードの[`advertise-peer-urls`](#advertise-peer-urls)値を組み合わせたものです。DM マスターノードを新たに追加する場合は、 `initial-cluster` `join`に置き換えてください。

#### `ssl-ca` {#ssl-ca}

-   DM マスターが他のコンポーネントに接続するための信頼できる SSL CA のリストが含まれるファイルのパス。

#### `ssl-cert` {#ssl-cert}

-   DM マスターが他のコンポーネントに接続するための PEM 形式の X509 証明書を含むファイルのパス。

#### `ssl-key` {#ssl-key}

-   DM マスターが他のコンポーネントに接続するための PEM 形式の X509 キーを含むファイルのパス。

#### `cert-allowed-cn` {#cert-allowed-cn}

-   一般名リスト。

#### `secret-key-path` {#secret-key-path}

-   アップストリームおよびダウンストリームのパスワードの暗号化と復号化に使用される秘密鍵のファイルパス。ファイルには、64文字の16進数AES-256秘密鍵が含まれている必要があります。この鍵を生成する方法の一つは、ランダムデータ（例： `head -n 256 /dev/urandom | sha256sum` ）のSHA256チェックサムを計算することです。詳細については、 [DMの暗号化と復号化のための秘密鍵をカスタマイズする](/dm/dm-customized-secret-key.md)参照してください。
