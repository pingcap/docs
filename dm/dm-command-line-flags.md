---
title: TiDB Data Migration Command-line Flags
summary: DM のコマンドライン フラグについて学習します。
---

# TiDB データ移行コマンドラインフラグ {#tidb-data-migration-command-line-flags}

このドキュメントでは、DM のコマンドライン フラグについて説明します。

## DMマスター {#dm-master}

### `--advertise-addr` {#advertise-addr}

-   クライアントのリクエストを受信するために使用されるDMマスターの外部アドレス
-   デフォルト値は`"{master-addr}"`です
-   オプションフラグ。1の形式をとることができます`"domain-name:port"`

### `--advertise-peer-urls` {#advertise-peer-urls}

-   DMマスターノード間の通信用の外部アドレス
-   デフォルト値は`"{peer-urls}"`です
-   オプションフラグ。1の形式をとることができます`"http(s)://domain-name:port"`

### `--config` {#config}

-   DMマスターの設定ファイルパス
-   デフォルト値は`""`です
-   オプションフラグ

### `--data-dir` {#data-dir}

-   DMマスターのデータを保存するディレクトリ
-   デフォルト値は`"default.{name}"`です
-   オプションフラグ

### `--initial-cluster` {#initial-cluster}

-   DMマスタークラスタのブートストラップに使用される`"{node name}={external address}"`リスト
-   デフォルト値は`"{name}={advertise-peer-urls}"`です
-   `join`フラグが指定されていない場合は、このフラグを指定する必要があります。3ノードクラスタの構成例は`"dm-master-1=http://172.16.15.11:8291,dm-master-2=http://172.16.15.12:8291,dm-master-3=http://172.16.15.13:8291"`です。

### `--join` {#join}

-   DMマスターノードがこのクラスタに参加したときの既存のクラスタの`advertise-addr`リスト
-   デフォルト値は`""`です
-   `initial-cluster`フラグが指定されていない場合は、このフラグを指定する必要があります。2ノードのクラスタに新しいノードが参加する場合、設定例は`"172.16.15.11:8261,172.16.15.12:8261"`です。

### `--log-file` {#log-file}

-   ログの出力ファイル名
-   デフォルト値は`""`です
-   オプションフラグ

### `-L` {#l}

-   ログレベル
-   デフォルト値は`"info"`です
-   オプションフラグ

### `--master-addr` {#master-addr}

-   DMマスターがクライアントのリクエストをリッスンするアドレス
-   デフォルト値は`""`です
-   必須フラグ

### `--name` {#name}

-   DMマスターノードの名前
-   デフォルト値は`"dm-master-{hostname}"`です
-   必須フラグ

### `--peer-urls` {#peer-urls}

-   DMマスターノード間の通信のリスニングアドレス
-   デフォルト値は`"http://127.0.0.1:8291"`です
-   必須フラグ

### `--secret-key-path` {#secret-key-path}

-   暗号化と復号化のためのカスタマイズされた秘密鍵のパス
-   デフォルト値は`""`です
-   オプションフラグ

## DMワーカー {#dm-worker}

### `--advertise-addr` {#advertise-addr}

-   クライアントのリクエストを受信するために使用されるDMワーカーの外部アドレス
-   デフォルト値は`"{worker-addr}"`です
-   オプションフラグ。1の形式をとることができます`"domain-name:port"`

### `--config` {#config}

-   DM-workerの設定ファイルパス
-   デフォルト値は`""`です
-   オプションフラグ

### `--join` {#join}

-   DMワーカーがこのクラスタに登録したときのクラスタ内のDMマスターノードの`{advertise-addr}`のリスト
-   デフォルト値は`""`です
-   必須フラグ。3ノード（DMマスターノード）クラスタの構成例は`"172.16.15.11:8261,172.16.15.12:8261,172.16.15.13:8261"`です。

### `--log-file` {#log-file}

-   ログの出力ファイル名
-   デフォルト値は`""`です
-   オプションフラグ

### `-L` {#l}

-   ログレベル
-   デフォルト値は`"info"`です
-   オプションフラグ

### `--name` {#name}

-   DMワーカーノードの名前
-   デフォルト値は`"{advertise-addr}"`です
-   必須フラグ

### `--worker-addr` {#worker-addr}

-   DMワーカーがクライアントのリクエストをリッスンするアドレス
-   デフォルト値は`""`です
-   必須フラグ

## dmctl {#dmctl}

### `--config` {#config}

-   dmctlの設定ファイルパス
-   デフォルト値は`""`です
-   オプションフラグ

### `--master-addr` {#master-addr}

-   dmctlによって接続されるクラスタ内の任意のDMマスターノードの`{advertise-addr}`
-   デフォルト値は`""`です
-   これは、dmctlがDMマスターと対話するときに必要なフラグです。
