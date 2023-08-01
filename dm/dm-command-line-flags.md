---
title: TiDB Data Migration Command-line Flags
summary: Learn about the command-line flags in DM.
---

# TiDB データ移行コマンドライン フラグ {#tidb-data-migration-command-line-flags}

このドキュメントでは、DM のコマンドライン フラグを紹介します。

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

-   DMマスターの設定ファイルのパス
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>--data-dir</code> {#code-data-dir-code}

-   DMマスターのデータを格納するディレクトリ
-   デフォルト値は`"default.{name}"`です
-   オプションのフラグ

### <code>--initial-cluster</code> {#code-initial-cluster-code}

-   DM マスター クラスターのブートストラップに使用される`"{node name}={external address}"`リスト
-   デフォルト値は`"{name}={advertise-peer-urls}"`です
-   `join`フラグが指定されていない場合は、このフラグを指定する必要があります。 3ノードクラスタの構成例は`"dm-master-1=http://172.16.15.11:8291,dm-master-2=http://172.16.15.12:8291,dm-master-3=http://172.16.15.13:8291"`です。

### <code>--join</code> {#code-join-code}

-   DM マスター ノードがこのクラスターに参加するときの既存のクラスターの`advertise-addr`リスト
-   デフォルト値は`""`です
-   `initial-cluster`フラグが指定されていない場合は、このフラグを指定する必要があります。 2 つのノードを持つクラスターに新しいノードが参加すると仮定します。構成例は`"172.16.15.11:8261,172.16.15.12:8261"`です。

### <code>--log-file</code> {#code-log-file-code}

-   ログの出力ファイル名
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト値は`"info"`です
-   オプションのフラグ

### <code>--master-addr</code> {#code-master-addr-code}

-   DM マスターがクライアントのリクエストをリッスンするアドレス
-   デフォルト値は`""`です
-   必須フラグ

### <code>--name</code> {#code-name-code}

-   DMマスターノードの名前
-   デフォルト値は`"dm-master-{hostname}"`です
-   必須フラグ

### <code>--peer-urls</code> {#code-peer-urls-code}

-   DM マスター ノード間の通信のリスニング アドレス
-   デフォルト値は`"http://127.0.0.1:8291"`です
-   必須フラグ

## DMワーカー {#dm-worker}

### <code>--advertise-addr</code> {#code-advertise-addr-code}

-   クライアントリクエストの受信に使用されるDMワーカーの外部アドレス
-   デフォルト値は`"{worker-addr}"`です
-   オプションのフラグ。 `"domain-name:port"`の形式にすることができます

### <code>--config</code> {#code-config-code}

-   DM-workerの設定ファイルのパス
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>--join</code> {#code-join-code}

-   DM ワーカーがこのクラスターに登録されるときのクラスター内の DM マスター ノードのリスト`{advertise-addr}`
-   デフォルト値は`""`です
-   必須のフラグ。 3ノード(DMマスターノード)クラスタの構成例は`"172.16.15.11:8261,172.16.15.12:8261,172.16.15.13:8261"`

### <code>--log-file</code> {#code-log-file-code}

-   ログの出力ファイル名
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト値は`"info"`です
-   オプションのフラグ

### <code>--name</code> {#code-name-code}

-   DM ワーカー ノードの名前
-   デフォルト値は`"{advertise-addr}"`です
-   必須フラグ

### <code>--worker-addr</code> {#code-worker-addr-code}

-   DM ワーカーがクライアントのリクエストをリッスンするアドレス
-   デフォルト値は`""`です
-   必須フラグ

## dmctl {#dmctl}

### <code>--config</code> {#code-config-code}

-   dmctlの設定ファイルのパス
-   デフォルト値は`""`です
-   オプションのフラグ

### <code>--master-addr</code> {#code-master-addr-code}

-   dmctl によって接続されるクラスター内の任意の DM マスター ノードの`{advertise-addr}`
-   デフォルト値は`""`です
-   これは、dmctl が DM マスターと対話するときに必須のフラグです。

### <code>--encrypt</code> {#code-encrypt-code}

-   平文データベースのパスワードを暗号文に暗号化します。
-   デフォルト値は`""`です
-   このフラグが指定されている場合、DM マスターと対話せずに平文を暗号化するためにのみ使用されます。

### <code>--decrypt</code> {#code-decrypt-code}

-   dmctlで暗号化された暗号文を平文に復号します。
-   デフォルト値は`""`です
-   このフラグが指定されている場合、DM マスターと対話せずに暗号文を復号化するためにのみ使用されます。
