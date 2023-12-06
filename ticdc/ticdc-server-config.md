---
title: TiCDC Server Configurations
summary: Learn the CLI and configuration parameters used in TiCDC.
---

# TiCDC サーバー構成 {#ticdc-server-configurations}

このドキュメントでは、TiCDC で使用される CLI および構成ファイルのパラメーターについて説明します。

## <code>cdc server</code> CLI パラメータ {#code-cdc-server-code-cli-parameters}

以下は、 `cdc server`コマンドで使用できるオプションの説明です。

-   `addr` : TiCDC のリスニング アドレス、HTTP API アドレス、および TiCDC サービスの Prometheus アドレス。デフォルト値は`127.0.0.1:8300`です。
-   `advertise-addr` : クライアントが TiCDC にアクセスする際に経由するアドバタイズされたアドレス。未指定の場合、値は`addr`と同じになります。
-   `pd` : PD エンドポイントのカンマ区切りリスト。
-   `config` : TiCDC が使用する構成ファイルのアドレス (オプション)。このオプションは、TiCDC v5.0.0 以降でサポートされています。このオプションは、 TiUP v1.4.0 以降の TiCDC 導入で使用できます。詳しい構成説明については、 [TiCDC Changefeed構成](/ticdc/ticdc-changefeed-config.md)を参照してください。
-   `data-dir` : TiCDC がファイルの保存にディスクを使用する必要がある場合に使用するディレクトリを指定します。 TiCDC によって使用されるソート エンジンと REDO ログは、このディレクトリを使用して一時ファイルを保存します。このディレクトリの空きディスク容量が 500 GiB 以上であることを確認することをお勧めします。 TiUPを使用している場合は、 [`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers)セクションで`data_dir`設定するか、 `global`でデフォルトの`data_dir`パスを直接使用できます。
-   `gc-ttl` : TiCDC によって設定された PD のサービス レベル`GC safepoint`の TTL (Time To Live)、およびレプリケーション タスクが一時停止できる期間 (秒単位)。デフォルト値は`86400`で、これは 24 時間を意味します。注: TiCDC レプリケーション タスクの一時停止は、TiCDC GC セーフポイントの進行状況に影響します。つまり、 [TiCDC GC セーフポイントの完全な動作](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)で詳しく説明されているように、上流の TiDB GC の進行状況に影響します。
-   `log-file` : TiCDC プロセス実行時にログが出力されるパス。このパラメータが指定されていない場合、ログは標準出力 (stdout) に書き込まれます。
-   `log-level` : TiCDC プロセス実行時のログ レベル。デフォルト値は`"info"`です。
-   `ca` : TLS 接続用の PEM 形式の CA 証明書ファイルのパスを指定します (オプション)。
-   `cert` : TLS 接続用の証明書ファイルのパスを PEM 形式で指定します (オプション)。
-   `cert-allowed-cn` : TLS 接続の共通名のパスを PEM 形式で指定します (オプション)。
-   `key` : TLS 接続用の秘密キー ファイルのパスを PEM 形式で指定します (オプション)。
-   `tz` : TiCDC サービスで使用されるタイムゾーン。 TiCDC は、 `TIMESTAMP`などの時間データ型を内部で変換するとき、またはデータをダウンストリームにレプリケートするときに、このタイム ゾーンを使用します。デフォルトは、プロセスが実行されるローカル タイム ゾーンです。 `time-zone` ( `sink-uri` ) と`tz`同時に指定すると、内部 TiCDC プロセスは`tz`で指定されたタイム ゾーンを使用し、シンクはデータをダウンストリームにレプリケートするために`time-zone`で指定されたタイム ゾーンを使用します。 `tz`で指定したタイムゾーンが、( `sink-uri`の) `time-zone`で指定したタイムゾーンと同じであることを確認してください。
-   `cluster-id` : (オプション) TiCDC クラスターの ID。デフォルト値は`default`です。 `cluster-id`は、TiCDC クラスターの一意の識別子です。同じ`cluster-id`を持つ TiCDC ノードは同じクラスターに属します。 `cluster-id`の長さは最大 128 文字です。 `cluster-id` `^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$`のパターンに従う必要があり、 `owner` 、 `capture` 、 `task` 、 `changefeed` 、 `job` 、 `meta`のいずれかにすることはできません。

## <code>cdc server</code>構成ファイルのパラメーター {#code-cdc-server-code-configuration-file-parameters}

`cdc server`コマンドの`config`オプションで指定する設定ファイルについて説明します。

```toml
# The configuration method of the following parameters is the same as that of CLI parameters, but the CLI parameters have higher priorities.
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

# The session duration between TiCDC and etcd services, measured in seconds. This parameter is optional and its default value is 10.
capture-session-ttl = 10 # 10s

# The interval at which the Owner module in the TiCDC cluster attempts to push the replication progress. This parameter is optional and its default value is `50000000` nanoseconds (that is, 50 milliseconds). You can configure this parameter in two ways: specifying only the number (for example, configuring it as `40000000` represents 40000000 nanoseconds, which is 40 milliseconds), or specifying both the number and unit (for example, directly configuring it as `40ms`).
owner-flush-interval = 50000000 # 50 ms

# The interval at which the Processor module in the TiCDC cluster attempts to push the replication progress. This parameter is optional and its default value is `50000000` nanoseconds (that is, 50 milliseconds). The configuration method of this parameter is the same as that of `owner-flush-interval`.
processor-flush-interval = 50000000 # 50 ms

# [log]
# # The output location for internal error logs of the zap log module. This parameter is optional and its default value is "stderr".
#   error-output = "stderr"
#   [log.file]
#     # The maximum size of a single log file, measured in MiB. This parameter is optional and its default value is 300.
#     max-size = 300 # 300 MiB
#     # The maximum number of days to retain log files. This parameter is optional and its default value is `0`, indicating never to delete.
#     max-days = 0
#     # The number of log files to retain. This parameter is optional and its default value is `0`, indicating to keep all log files.
#     max-backups = 0

#[sorter]
# The size of the shared pebble block cache in the Sorter module for the 8 pebble DBs started by default, measured in MiB. The default value is 128.
# cache-size-in-mb = 128
# The directory where sorter files are stored relative to the data directory (`data-dir`). This parameter is optional and its default value is "/tmp/sorter".
# sorter-dir = "/tmp/sorter"

# [kv-client]
#   The number of threads that can be used in a single Region worker. This parameter is optional and its default value is 8.
#   worker-concurrent = 8
#   The number of threads in the shared thread pool of TiCDC, mainly used for processing KV events. This parameter is optional and its default value is 0, indicating that the default pool size is twice the number of CPU cores.
#   worker-pool-size = 0
#   The retry duration of Region connections. This parameter is optional and its default value is `60000000000` nanoseconds (that is, 1 minute). You can configure this parameter in two ways: specifying only the number (for example, configuring it as `50000000` represents 50000000 nanoseconds, which is 50 milliseconds), or specifying both the number and unit (for example, directly configuring it as `50ms`).
#   region-retry-duration = 60000000000
```
