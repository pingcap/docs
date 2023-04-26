---
title: TiCDC Server Configurations
summary: Learn the CLI and configuration parameters used in TiCDC.
---

# TiCDC サーバー構成 {#ticdc-server-configurations}

このドキュメントでは、TiCDC で使用される CLI と構成ファイルのパラメーターについて説明します。

## <code>cdc server</code> CLI パラメーター {#code-cdc-server-code-cli-parameters}

以下は、 `cdc server`コマンドで使用可能なオプションの説明です。

-   `addr` : TiCDC のリッスン アドレス、HTTP API アドレス、および TiCDC サービスの Prometheus アドレス。デフォルト値は`127.0.0.1:8300`です。
-   `advertise-addr` : クライアントが TiCDC にアクセスするために使用するアドバタイズされたアドレス。指定しない場合、値は`addr`の値と同じです。
-   `pd` : PD エンドポイントのコンマ区切りリスト。
-   `config` : TiCDC が使用する構成ファイルのアドレス (オプション)。このオプションは、TiCDC v5.0.0 以降でサポートされています。このオプションは、 TiUP v1.4.0 以降の TiCDC 展開で使用できます。詳細な構成の説明については、 [TiCDC Changefeed構成](/ticdc/ticdc-changefeed-config.md)を参照してください。
-   `data-dir` : ファイルを格納するためにディスクを使用する必要がある場合に TiCDC が使用するディレクトリを指定します。 TiCDC と REDO ログで使用されるソート エンジンは、このディレクトリを使用して一時ファイルを保存します。このディレクトリの空きディスク容量が 500 GiB 以上であることを確認することをお勧めします。 TiUPを使用している場合は、 [`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers)セクションで`data_dir`構成するか、または`global`でデフォルトの`data_dir`パスを直接使用できます。
-   `gc-ttl` : TiCDC によって設定された PD のサービス レベル`GC safepoint`の TTL (Time To Live) と、レプリケーション タスクが中断できる期間 (秒単位)。デフォルト値は`86400`で、これは 24 時間を意味します。注: TiCDC レプリケーション タスクの一時停止は、TiCDC GC セーフポイントの進行状況に影響を与えます。つまり、 [TiCDC GC セーフポイントの完全な動作](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)で詳述されているように、上流の TiDB GC の進行状況に影響を与えます。
-   `log-file` : TiCDC プロセスの実行時にログが出力されるパス。このパラメーターが指定されていない場合、ログは標準出力 (stdout) に書き込まれます。
-   `log-level` : TiCDC プロセスが実行されているときのログ レベル。デフォルト値は`"info"`です。
-   `ca` : TLS 接続用の PEM 形式の CA 証明書ファイルのパスを指定します (オプション)。
-   `cert` : TLS 接続用の PEM 形式の証明書ファイルのパスを指定します (オプション)。
-   `cert-allowed-cn` : TLS 接続の共通名のパスを PEM 形式で指定します (オプション)。
-   `key` : TLS 接続用の PEM 形式の秘密鍵ファイルのパスを指定します (オプション)。
-   `tz` : TiCDC サービスが使用するタイムゾーン。 TiCDC は、 `TIMESTAMP`などの時間データ タイプを内部で変換するとき、またはデータをダウンストリームにレプリケートするときに、このタイム ゾーンを使用します。デフォルトは、プロセスが実行されるローカル タイム ゾーンです。 `time-zone` ( `sink-uri` ) と`tz`同時に指定すると、内部の TiCDC プロセスは`tz`で指定されたタイム ゾーンを使用し、シンクは`time-zone`で指定されたタイム ゾーンを使用してデータをダウンストリームにレプリケートします。
-   `cluster-id` : (オプション) TiCDC クラスターの ID。デフォルト値は`default`です。 `cluster-id`は、TiCDC クラスターの一意の識別子です。同じ`cluster-id`の TiCDC ノードは同じクラスターに属しています。 `cluster-id`の長さは最大 128 文字です。 `cluster-id` `^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$`のパターンに従う必要があり、次のいずれかにすることはできません: `owner` 、 `capture` 、 `task` 、 `changefeed` 、 `job` 、および`meta` 。

## <code>cdc server</code>構成ファイルのパラメーター {#code-cdc-server-code-configuration-file-parameters}

`cdc server`の構成ファイルの構成は次のとおりです。

```yaml
addr = "127.0.0.1:8300"
advertise-addr = ""
log-file = ""
log-level = "info"
data-dir = ""
gc-ttl = 86400 # 24 h
tz = "System"
cluster-id = "default"

[security]
  ca-path = ""
  cert-path = ""
  key-path = ""


capture-session-ttl = 10 # 10s
owner-flush-interval = 50000000 # 50 ms
processor-flush-interval = 50000000 # 50 ms
per-table-memory-quota = 10485760 # 10 MiB

[log]
  error-output = "stderr"
  [log.file]
    max-size = 300 # 300 MiB
    max-days = 0
    max-backups = 0

[sorter]
  num-concurrent-worker = 4
  chunk-size-limit = 999
  max-memory-percentage = 30
  max-memory-consumption = 17179869184
  num-workerpool-goroutine = 16
  sort-dir = "/tmp/sorter"

# [kv-client]
#  worker-concurrent = 8
#  worker-pool-size = 0
#  region-scan-limit = 40
#  region-retry-duration = 60000000000
```
