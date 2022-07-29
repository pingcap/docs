---
title: Command-line Flags
summary: Learn about the command-line flags in DM.
---

# コマンドラインフラグ {#command-line-flags}

このドキュメントでは、DMのコマンドラインフラグを紹介します。

## DMマスター {#dm-master}

### <code>--advertise-addr</code> {#code-advertise-addr-code}

-   クライアントリクエストの受信に使用されるDMマスターの外部アドレス
-   デフォルト値は`"{master-addr}"`です
-   オプションのフラグ。 `"domain-name:port"`の形式にすることができます

### <code>--advertise-peer-urls</code> {#code-advertise-peer-urls-code}

-   DMマスターノード間の通信用の外部アドレス
-   デフォルト値は`"{peer-urls}"`です
-   オプションのフラグ。 `"http(s)://domain-name:port"`の形式にすることができます

### <code>--config</code> {#code-config-code}

-   DMマスターの構成ファイルパス
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>--data-dir</code> {#code-data-dir-code}

-   DMマスターのデータを保存するために使用されるディレクトリ
-   デフォルト値は`"default.{name}"`です
-   オプションのフラグ

### <code>--initial-cluster</code> {#code-initial-cluster-code}

-   DMマスタークラスタをブートストラップするために使用される`"{node name}={external address}"`のリスト
-   デフォルト値は`"{name}={advertise-peer-urls}"`です
-   `join`フラグが指定されていない場合は、このフラグを指定する必要があります。 3ノードクラスタの構成例は`"dm-master-1=http://172.16.15.11:8291,dm-master-2=http://172.16.15.12:8291,dm-master-3=http://172.16.15.13:8291"`です。

### <code>--join</code> {#code-join-code}

-   DMマスターノードがこのクラスタに参加するときの既存のクラスターの`advertise-addr`のリスト
-   デフォルト値は`""`です
-   `initial-cluster`フラグが指定されていない場合は、このフラグを指定する必要があります。新しいノードが2つのノードを持つクラスタに参加するとします。構成例は`"172.16.15.11:8261,172.16.15.12:8261"`です。

### <code>--log-file</code> {#code-log-file-code}

-   ログの出力ファイル名
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト値は`"info"`です
-   オプションのフラグ

### <code>--master-addr</code> {#code-master-addr-code}

-   DMマスターがクライアントの要求をリッスンするアドレス
-   デフォルト値は`""`です
-   必須フラグ

### <code>--name</code> {#code-name-code}

-   DMマスターノードの名前
-   デフォルト値は`"dm-master-{hostname}"`です
-   必須フラグ

### <code>--peer-urls</code> {#code-peer-urls-code}

-   DMマスターノード間の通信のリスニングアドレス
-   デフォルト値は`"http://127.0.0.1:8291"`です
-   必須フラグ

## DMワーカー {#dm-worker}

### <code>--advertise-addr</code> {#code-advertise-addr-code}

-   クライアントリクエストの受信に使用されるDMワーカーの外部アドレス
-   デフォルト値は`"{worker-addr}"`です
-   オプションのフラグ。 `"domain-name:port"`の形式にすることができます

### <code>--config</code> {#code-config-code}

-   DM-workerの構成ファイルパス
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>--join</code> {#code-join-code}

-   DMワーカーがこのクラスタに登録するときのクラスタのDMマスターノードの`{advertise-addr}`のリスト
-   デフォルト値は`""`です
-   必須フラグ。 3ノード（DMマスターノード）クラスタの構成例は`"172.16.15.11:8261,172.16.15.12:8261,172.16.15.13:8261"`です。

### <code>--log-file</code> {#code-log-file-code}

-   ログの出力ファイル名
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト値は`"info"`です
-   オプションのフラグ

### <code>--name</code> {#code-name-code}

-   DMワーカーノードの名前
-   デフォルト値は`"{advertise-addr}"`です
-   必須フラグ

### <code>--worker-addr</code> {#code-worker-addr-code}

-   DM-workerがクライアントの要求をリッスンするアドレス
-   デフォルト値は`""`です
-   必須フラグ

## dmctl {#dmctl}

### <code>--config</code> {#code-config-code}

-   dmctlの構成ファイルパス
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>--master-addr</code> {#code-master-addr-code}

-   dmctlによって接続されるクラスタのDMマスターノードの`{advertise-addr}`つ
-   デフォルト値は`""`です
-   dmctlがDM-masterと対話するときに必要なフラグです。

### <code>--encrypt</code> {#code-encrypt-code}

-   平文データベースのパスワードを暗号文に暗号化します
-   デフォルト値は`""`です
-   このフラグが指定されている場合、DMマスターと対話せずにプレーンテキストを暗号化するためにのみ使用されます

### <code>--decrypt</code> {#code-decrypt-code}

-   dmctlで暗号化された暗号文を平文に復号化します
-   デフォルト値は`""`です
-   このフラグが指定されている場合、DMマスターと対話せずに暗号文を復号化するためにのみ使用されます
