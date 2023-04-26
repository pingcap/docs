---
title: TiDB Data Migration Command-line Flags
summary: Learn about the command-line flags in DM.
---

# TiDB データ移行コマンドライン フラグ {#tidb-data-migration-command-line-flags}

このドキュメントでは、DM のコマンドライン フラグを紹介します。

## DMマスター {#dm-master}

### <code>--advertise-addr</code> {#code-advertise-addr-code}

-   クライアント要求を受信するために使用される DM マスターの外部アドレス
-   デフォルト値は`"{master-addr}"`です
-   オプションのフラグ。 `"domain-name:port"`の形をとることができます。

### <code>--advertise-peer-urls</code> {#code-advertise-peer-urls-code}

-   DM-master ノード間の通信用の外部アドレス
-   デフォルト値は`"{peer-urls}"`です
-   オプションのフラグ。 `"http(s)://domain-name:port"`の形をとることができます。

### <code>--config</code> {#code-config-code}

-   DM-master の構成ファイルのパス
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>--data-dir</code> {#code-data-dir-code}

-   DM-master のデータを格納するディレクトリ
-   デフォルト値は`"default.{name}"`です
-   オプションのフラグ

### <code>--initial-cluster</code> {#code-initial-cluster-code}

-   DM-master クラスタのブートストラップに使用される`"{node name}={external address}"`リスト
-   デフォルト値は`"{name}={advertise-peer-urls}"`です
-   `join`フラグを指定しない場合は、このフラグを指定する必要があります。 3ノードクラスタの構成例は`"dm-master-1=http://172.16.15.11:8291,dm-master-2=http://172.16.15.12:8291,dm-master-3=http://172.16.15.13:8291"`

### <code>--join</code> {#code-join-code}

-   DM マスター ノードがこのクラスターに参加するときの既存のクラスターの`advertise-addr`リスト
-   デフォルト値は`""`です
-   `initial-cluster`フラグを指定しない場合は、このフラグを指定する必要があります。 2 つのノードを持つクラスターに新しいノードが参加するとします。構成例は`"172.16.15.11:8261,172.16.15.12:8261"`です。

### <code>--log-file</code> {#code-log-file-code}

-   ログの出力ファイル名
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト値は`"info"`です
-   オプションのフラグ

### <code>--master-addr</code> {#code-master-addr-code}

-   DM マスターがクライアントの要求をリッスンするアドレス
-   デフォルト値は`""`です
-   必須フラグ

### <code>--name</code> {#code-name-code}

-   DM マスター ノードの名前
-   デフォルト値は`"dm-master-{hostname}"`です
-   必須フラグ

### <code>--peer-urls</code> {#code-peer-urls-code}

-   DM-master ノード間の通信用リスニング アドレス
-   デフォルト値は`"http://127.0.0.1:8291"`です
-   必須フラグ

## DMワーカー {#dm-worker}

### <code>--advertise-addr</code> {#code-advertise-addr-code}

-   クライアント要求を受信するために使用される DM-worker の外部アドレス
-   デフォルト値は`"{worker-addr}"`です
-   オプションのフラグ。 `"domain-name:port"`の形をとることができます。

### <code>--config</code> {#code-config-code}

-   DM-worker の設定ファイルのパス
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>--join</code> {#code-join-code}

-   DM-worker がこのクラスターに登録するときのクラスター内の DM-master ノードの`{advertise-addr}`のリスト
-   デフォルト値は`""`です
-   必須フラグ。 3ノード(DM-masterノード)クラスタの構成例は`"172.16.15.11:8261,172.16.15.12:8261,172.16.15.13:8261"`

### <code>--log-file</code> {#code-log-file-code}

-   ログの出力ファイル名
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト値は`"info"`です
-   オプションのフラグ

### <code>--name</code> {#code-name-code}

-   DM-worker ノードの名前
-   デフォルト値は`"{advertise-addr}"`です
-   必須フラグ

### <code>--worker-addr</code> {#code-worker-addr-code}

-   DM-worker がクライアントのリクエストをリッスンするアドレス
-   デフォルト値は`""`です
-   必須フラグ

## dmctl {#dmctl}

### <code>--config</code> {#code-config-code}

-   dmctl の構成ファイルのパス
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>--master-addr</code> {#code-master-addr-code}

-   dmctl によって接続されるクラスター内の任意の DM マスター ノードの`{advertise-addr}`
-   デフォルト値は`""`です
-   dmctl が DM-master とやり取りするときに必要なフラグです。

### <code>--encrypt</code> {#code-encrypt-code}

-   平文のデータベース パスワードを暗号文に暗号化します
-   デフォルト値は`""`です
-   このフラグが指定されている場合、DM マスターと対話せずにプレーンテキストを暗号化するためにのみ使用されます。

### <code>--decrypt</code> {#code-decrypt-code}

-   dmctl で暗号化された暗号文を平文に復号化します
-   デフォルト値は`""`です
-   このフラグが指定されている場合、DM マスターと対話せずに暗号文を復号化するためにのみ使用されます。
