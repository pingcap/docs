---
title: TiCDC Server Configurations
summary: TiCDC で使用される CLI と構成パラメータについて学習します。
---

# TiCDC サーバー構成 {#ticdc-server-configurations}

このドキュメントでは、TiCDC で使用される CLI および構成ファイルのパラメータについて説明します。

## <code>cdc server</code> CLI パラメータ {#code-cdc-server-code-cli-parameters}

`cdc server`コマンドで使用できるオプションの説明は次のとおりです。

-   `addr` : TiCDC のリスニング アドレス、HTTP API アドレス、および TiCDC サービスの Prometheus アドレス。デフォルト値は`127.0.0.1:8300`です。
-   `advertise-addr` : クライアントが TiCDC にアクセスするために使用するアドバタイズされたアドレス。指定されていない場合、値は`addr`と同じになります。
-   `pd` : PD エンドポイントのコンマ区切りリスト。
-   `config` : TiCDC が使用する構成ファイルのアドレス (オプション)。このオプションは、TiCDC v5.0.0 以降でサポートされています。このオプションは、 TiUP v1.4.0 以降の TiCDC デプロイメントで使用できます。詳細な構成の説明については、 [TiCDC Changefeed構成](/ticdc/ticdc-changefeed-config.md)を参照してください。
-   `data-dir` : ディスクを使用してファイルを保存する必要がある場合に TiCDC が使用するディレクトリを指定します。TiCDC で使用されるソート エンジンと redo ログは、このディレクトリを使用して一時ファイルを保存します。このディレクトリの空きディスク領域が 500 GiB 以上であることを確認することをお勧めします。TiUP を使用しTiUPいる場合は、 [`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers)セクションで`data_dir`を構成するか、 `global`でデフォルトの`data_dir`パスを直接使用できます。
-   `gc-ttl` : TiCDC によって設定された PD のサービス レベル`GC safepoint`の TTL (Time To Live) と、レプリケーション タスクが一時停止できる期間 (秒単位)。デフォルト値は`86400`で、これは 24 時間を意味します。注: TiCDC レプリケーション タスクを一時停止すると、TiCDC GC セーフポイントの進行に影響します。つまり、 [TiCDC GCセーフポイントの完全な動作](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)で詳しく説明されているように、アップストリーム TiDB GC の進行に影響します。
-   `log-file` : TiCDC プロセスの実行中にログが出力されるパス。このパラメータを指定しない場合、ログは標準出力 (stdout) に書き込まれます。
-   `log-level` : TiCDC プロセス実行時のログ レベル。デフォルト値は`"info"`です。
-   `ca` : TLS 接続用の PEM 形式の CA 証明書ファイルのパスを指定します (オプション)。
-   `cert` : TLS 接続用の PEM 形式の証明書ファイルのパスを指定します (オプション)。
-   `cert-allowed-cn` : TLS 接続の共通名のパスを PEM 形式で指定します (オプション)。
-   `key` : TLS 接続用の PEM 形式の秘密鍵ファイルのパスを指定します (オプション)。
-   `tz` : TiCDC サービスが使用するタイムゾーン。TiCDC は、 `TIMESTAMP`などの時間データ型を内部的に変換するとき、またはデータをダウンストリームに複製するときに、このタイムゾーンを使用します。デフォルトは、プロセスが実行されるローカル タイムゾーンです`time-zone` ( `sink-uri`で) と`tz`同時に指定すると、内部 TiCDC プロセスは`tz`で指定されたタイムゾーンを使用し、シンクは`time-zone`で指定されたタイムゾーンを使用してダウンストリームにデータを複製します。14 で指定`tz`れたタイムゾーンが`time-zone` ( `sink-uri`で) で指定されたタイムゾーンと同じであることを確認してください。
-   `cluster-id` : (オプション) TiCDC クラスターの ID。デフォルト値は`default`です。 `cluster-id`は TiCDC クラスターの一意の識別子です。同じ`cluster-id`を持つ TiCDC ノードは同じクラスターに属します。 `cluster-id`の長さは最大 128 文字です。 `cluster-id` `^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$`のパターンに従う必要があり、 `owner` 、 `capture` 、 `task` 、 `changefeed` 、 `job` 、および`meta`のいずれかにすることはできません。

## <code>cdc server</code>構成ファイルのパラメータ {#code-cdc-server-code-configuration-file-parameters}

以下は、 `cdc server`コマンドの`config`オプションで指定された構成ファイルについて説明しています。

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
# This parameter specifies the maximum memory threshold (in bytes) for tuning GOGC: Setting a smaller threshold increases the GC frequency. Setting a larger threshold reduces GC frequency and consumes more memory resources for the TiCDC process. Once the memory usage exceeds this threshold, GOGC Tuner stops working. The default value is 0, indicating that GOGC Tuner is disabled.
gc-tuner-memory-threshold = 0

[security]
  ca-path = ""
  cert-path = ""
  key-path = ""
  # This parameter controls whether to enable the TLS client authentication. The default value is false.
  mtls = false
  # This parameter controls whether to use username and password for client authentication. The default value is false.
  client-user-required = false
  # This parameter lists the usernames that are allowed for client authentication. Authentication requests with usernames not in this list will be rejected. The default value is null.
  client-allowed-user = ["username_1", "username_2"]

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
