---
title: TiDB Data Migration Command-line Flags
summary: DM のコマンドライン フラグについて学習します。
---

# TiDB データ移行コマンドラインフラグ {#tidb-data-migration-command-line-flags}

このドキュメントでは、DM のコマンドライン フラグについて説明します。

## DMマスター {#dm-master}

### <code>--advertise-addr</code> {#code-advertise-addr-code}

-   クライアント要求を受信するために使用されるDMマスターの外部アドレス
-   デフォルト値は`"{master-addr}"`です
-   オプションのフラグ。1の形式になります`"domain-name:port"`

### <code>--advertise-peer-urls</code> {#code-advertise-peer-urls-code}

-   DMマスターノード間の通信用の外部アドレス
-   デフォルト値は`"{peer-urls}"`です
-   オプションのフラグ。1の形式になります`"http(s)://domain-name:port"`

### <code>--config</code> {#code-config-code}

-   DMマスターの設定ファイルパス
-   デフォルト値は`""`です
-   オプションフラグ

### <code>--data-dir</code> {#code-data-dir-code}

-   DMマスターのデータを保存するディレクトリ
-   デフォルト値は`"default.{name}"`です
-   オプションフラグ

### <code>--initial-cluster</code> {#code-initial-cluster-code}

-   DMマスタークラスタのブートストラップに使用される`"{node name}={external address}"`リスト
-   デフォルト値は`"{name}={advertise-peer-urls}"`です
-   `join`フラグが指定されていない場合は、このフラグを指定する必要があります。3ノードクラスタの構成例は`"dm-master-1=http://172.16.15.11:8291,dm-master-2=http://172.16.15.12:8291,dm-master-3=http://172.16.15.13:8291"`です。

### <code>--join</code> {#code-join-code}

-   DMマスターノードがこのクラスタに参加したときの既存のクラスタの`advertise-addr`リスト
-   デフォルト値は`""`です
-   `initial-cluster`フラグが指定されていない場合は、このフラグを指定する必要があります。新しいノードが2つのノードを持つクラスターに参加すると仮定すると、構成例は`"172.16.15.11:8261,172.16.15.12:8261"`になります。

### <code>--log-file</code> {#code-log-file-code}

-   ログの出力ファイル名
-   デフォルト値は`""`です
-   オプションフラグ

### <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト値は`"info"`です
-   オプションフラグ

### <code>--master-addr</code> {#code-master-addr-code}

-   DMマスターがクライアントのリクエストをリッスンするアドレス
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

### <code>--secret-key-path</code> {#code-secret-key-path-code}

-   暗号化と復号化のためのカスタマイズされた秘密鍵のパス
-   デフォルト値は`""`です
-   オプションフラグ

## DMワーカー {#dm-worker}

### <code>--advertise-addr</code> {#code-advertise-addr-code}

-   クライアントのリクエストを受信するために使用される DM ワーカーの外部アドレス
-   デフォルト値は`"{worker-addr}"`です
-   オプションのフラグ。1の形式になります`"domain-name:port"`

### <code>--config</code> {#code-config-code}

-   DM-workerの設定ファイルパス
-   デフォルト値は`""`です
-   オプションフラグ

### <code>--join</code> {#code-join-code}

-   DMワーカーがこのクラスタに登録したときのクラスタ内のDMマスターノードのリスト`{advertise-addr}`
-   デフォルト値は`""`です
-   必須フラグ。3ノード（DMマスターノード）クラスタの構成例は`"172.16.15.11:8261,172.16.15.12:8261,172.16.15.13:8261"`です。

### <code>--log-file</code> {#code-log-file-code}

-   ログの出力ファイル名
-   デフォルト値は`""`です
-   オプションフラグ

### <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト値は`"info"`です
-   オプションフラグ

### <code>--name</code> {#code-name-code}

-   DMワーカーノードの名前
-   デフォルト値は`"{advertise-addr}"`です
-   必須フラグ

### <code>--worker-addr</code> {#code-worker-addr-code}

-   DMワーカーがクライアントのリクエストをリッスンするアドレス
-   デフォルト値は`""`です
-   必須フラグ

## dmctl {#dmctl}

### <code>--config</code> {#code-config-code}

-   dmctlの設定ファイルパス
-   デフォルト値は`""`です
-   オプションフラグ

### <code>--master-addr</code> {#code-master-addr-code}

-   dmctlによって接続されるクラスタ内の任意のDMマスターノードの`{advertise-addr}`
-   デフォルト値は`""`です
-   dmctlがDMマスターと対話するときに必要なフラグです。
