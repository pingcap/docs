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

#### <code>name</code> {#code-name-code}

-   DM マスターの名前。

#### <code>log-level</code> {#code-log-level-code}

-   ログ レベルを指定します。
-   デフォルト値: `info`
-   `fatal` `warn` `info` `error` `debug`

#### <code>log-file</code> {#code-log-file-code}

-   ログファイルのディレクトリを指定します。パラメータが指定されていない場合、ログは標準出力に出力されます。

#### <code>master-addr</code> {#code-master-addr-code}

-   サービスを提供するDMマスターのアドレスを指定します。IPアドレスを省略し、ポート番号のみ（例： `":8261"` ）を指定することもできます。

#### <code>advertise-addr</code> {#code-advertise-addr-code}

-   DM マスターが外部に通知するアドレスを指定します。

#### <code>peer-urls</code> {#code-peer-urls-code}

-   DM マスター ノードのピア URL を指定します。

#### <code>advertise-peer-urls</code> {#code-advertise-peer-urls-code}

-   DMマスターが外部にアドバタイズするピアURLを指定します。デフォルト値は`advertise-peer-urls`で、 [`peer-urls`](#peer-urls)と同じです。

#### <code>initial-cluster</code> {#code-initial-cluster-code}

-   値`initial-cluster`は、初期クラスター内のすべての DM マスター ノードの[`advertise-peer-urls`](#advertise-peer-urls)値の組み合わせです。

#### <code>join</code> {#code-join-code}

-   `join`の値は、クラスター内の既存の DM マスターノードの[`advertise-peer-urls`](#advertise-peer-urls)値を組み合わせたものです。DM マスターノードを新たに追加する場合は、 `initial-cluster` `join`に置き換えてください。

#### <code>ssl-ca</code> {#code-ssl-ca-code}

-   DM マスターが他のコンポーネントに接続するための信頼できる SSL CA のリストが含まれるファイルのパス。

#### <code>ssl-cert</code> {#code-ssl-cert-code}

-   DM マスターが他のコンポーネントに接続するための PEM 形式の X509 証明書を含むファイルのパス。

#### <code>ssl-key</code> {#code-ssl-key-code}

-   DM マスターが他のコンポーネントに接続するための PEM 形式の X509 キーを含むファイルのパス。

#### <code>cert-allowed-cn</code> {#code-cert-allowed-cn-code}

-   一般名リスト。

#### <code>secret-key-path</code> {#code-secret-key-path-code}

-   アップストリームおよびダウンストリームのパスワードの暗号化と復号化に使用される秘密鍵のファイルパス。ファイルには、64文字の16進数AES-256秘密鍵が含まれている必要があります。この鍵を生成する方法の一つは、ランダムデータ（例： `head -n 256 /dev/urandom | sha256sum` ）のSHA256チェックサムを計算することです。詳細については、 [DMの暗号化と復号化のための秘密鍵をカスタマイズする](/dm/dm-customized-secret-key.md)参照してください。
