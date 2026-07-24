---
title: TiCDC Server Configurations
summary: TiCDC で使用される CLI と構成パラメータについて学習します。
---

# TiCDC サーバー構成 {#ticdc-server-configurations}

このドキュメントでは、TiCDC で使用される CLI および構成ファイルのパラメータについて説明します。

## <code>cdc server</code> CLIパラメータ {#cdc-server-cli-parameters}

以下は、 `cdc server`コマンドで使用できるオプションの説明です。

-   `addr` : TiCDCのリスニングアドレス、HTTP APIアドレス、およびTiCDCサービスのPrometheusアドレス。デフォルト値は`127.0.0.1:8300`です。
-   `advertise-addr` : クライアントがTiCDCにアクセスするために使用するアドバタイズされたアドレス。指定されていない場合、値は`addr`と同じになります。
-   `pd` : PD エンドポイントのコンマ区切りリスト。
-   `config` : TiCDCが使用する設定ファイルのアドレス（オプション）。このオプションはTiCDC v5.0.0以降でサポートされています。このオプションはTiUP v1.4.0以降のTiCDCデプロイメントで使用できます。詳細な設定については、 [TiCDC Changefeed構成](/ticdc/ticdc-changefeed-config.md)参照してください。
-   `data-dir` : TiCDC がファイルを保存するためにディスクを使用する必要があるときに使用するディレクトリを指定します。TiCDC が使用するソートエンジンと REDO ログは、このディレクトリに一時ファイルを保存します。このディレクトリの空きディスク容量は 500 GiB 以上確保することをお勧めします。TiUPを使用している場合は、セクション[`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers)で`data_dir`設定するか、 `global`でデフォルトのパス`data_dir`を直接使用できます。
-   `gc-ttl` : TiCDC によって設定される PD のサービスレベル`GC safepoint`の TTL (Time To Live) と、レプリケーションタスクが一時停止できる期間（秒単位）。デフォルト値は`86400`で、これは 24 時間を意味します。注: TiCDC レプリケーションタスクの一時停止は、TiCDC GC セーフポイントの進行に影響します。つまり、 [TiCDC GCセーフポイントの完全な動作](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)で詳述されているように、上流の TiDB GC の進行にも影響します。
-   `log-file` : TiCDCプロセス実行時にログが出力されるパス。このパラメータが指定されていない場合、ログは標準出力（stdout）に書き込まれます。
-   `log-level` : TiCDCプロセス実行時のログレベル。デフォルト値は`"info"`です。
-   `ca` : TLS 接続用の PEM 形式の CA 証明書ファイルのパスを指定します (オプション)。
-   `cert` : TLS 接続用の PEM 形式の証明書ファイルのパスを指定します (オプション)。
-   `cert-allowed-cn` : TLS 接続の PEM 形式の共通名のパスを指定します (オプション)。
-   `key` : TLS 接続用の PEM 形式の秘密鍵ファイルのパスを指定します (オプション)。
-   `tz` : TiCDC サービスが使用するタイムゾーン。TiCDC は、 `TIMESTAMP`などの時間データ型を内部的に変換するとき、またはデータをダウンストリームに複製するときに、このタイムゾーンを使用します。デフォルトは、プロセスが実行されるローカルタイムゾーンです。6 `sink-uri` `time-zone`パラメータは、 `mysql`と`tidb`シンクにのみ有効で、ダウンストリーム接続セッションのタイムゾーンを設定するために使用されることに注意してください。12 パラメータと`time-zone`パラメータの`tz`を指定する場合は、両方のパラメータで同じタイムゾーンを使用するようにしてください。これは、TiCDC プロセスは内部的に`tz`で指定されたタイムゾーンを使用するのに対し、MySQL シンクと TiDB シンクはダウンストリーム操作の実行時に`time-zone`で指定されたタイムゾーンを使用するためです。
-   `cluster-id` : (オプション) TiCDC クラスターの ID。デフォルト値は`default`です。 `cluster-id`は TiCDC クラスターの一意の識別子です。同じ`cluster-id`を持つ TiCDC ノードは同じクラスターに属します。 `cluster-id`の長さは最大 128 文字です。 `cluster-id` `^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$`のパターンに従う必要があり、 `owner` 、 `capture` 、 `task` 、 `changefeed` 、 `job` 、 `meta`のいずれかにすることはできません。

## <code>cdc server</code>構成ファイルのパラメータ {#cdc-server-configuration-file-parameters}

以下は、コマンド`cdc server`の`config`オプションで指定される設定ファイルについて説明します。デフォルトの設定ファイルは[`pkg/cmd/util/ticdc.toml`](https://github.com/pingcap/tiflow/blob/master/pkg/cmd/util/ticdc.toml)にあります。

### `newarch` <span class="version-mark">v8.5.4-release.1 の新機能</span> {#newarch-new-in-v854-release1}

-   [TiCDCの新しいアーキテクチャ](/ticdc/ticdc-architecture.md)を有効にするかどうかを制御します。
-   デフォルト値: `false` 、 [TiCDC クラシックアーキテクチャ](/ticdc/ticdc-classic-architecture.md)が使用されることを示します。
-   `true`に設定すると、TiCDC の新しいアーキテクチャが有効になります。

<!-- The configuration method of the following parameters is the same as that of CLI parameters, but the CLI parameters have higher priorities. -->

### `addr` {#addr}

-   例: `"127.0.0.1:8300"`

### `advertise-addr` {#advertise-addr}

-   例: `""`

### `log-file` {#log-file}

-   例: `""`

### `log-level` {#log-level}

-   例: `"info"`

### `data-dir` {#data-dir}

-   例: `""`

### `gc-ttl` {#gc-ttl}

-   例: `86400` (24時間)

### `tz` {#tz}

-   例: `"System"`

### `cluster-id` {#cluster-id}

-   例: `"default"`

### `gc-tuner-memory-threshold` {#gc-tuner-memory-threshold}

-   GOGCチューニングの最大メモリしきい値を指定します。しきい値を小さくするとGCの頻度が増加します。しきい値を大きくするとGCの頻度は減少しますが、TiCDCプロセスで消費されるメモリリソースが増加します。メモリ使用量がこのしきい値を超えると、GOGC Tunerは動作を停止します。
-   デフォルト値: `0` 、GOGCチューナーが無効であることを示します
-   単位: バイト

### 安全 {#security}

#### `ca-path` {#ca-path}

-   例: `""`

#### `cert-path` {#cert-path}

-   例: `""`

#### `key-path` {#key-path}

-   例: `""`

#### `mtls` {#mtls}

-   TLS クライアント認証を有効にするかどうかを制御します。
-   デフォルト値: `false`

#### `client-user-required` {#client-user-required}

-   クライアント認証にユーザー名とパスワードを使用するかどうかを制御します。デフォルト値は false です。
-   デフォルト値: `false`

#### `client-allowed-user` {#client-allowed-user}

-   クライアント認証に許可されるユーザー名をリストします。このリストにないユーザー名による認証要求は拒否されます。
-   デフォルト値: `null`

<!-- Example: `["username_1", "username_2"]` -->

### `capture-session-ttl` {#capture-session-ttl}

-   TiCDCとetcdサービス間のセッション期間を指定します。このパラメータはオプションです。
-   デフォルト値: `10`
-   単位: 秒

### `owner-flush-interval` {#owner-flush-interval}

-   TiCDCクラスタ内のオーナーモジュールがレプリケーションの進行状況をプッシュしようとする間隔を指定します。このパラメータはオプションで、デフォルト値は`50000000`ナノ秒（つまり50ミリ秒）です。
-   このパラメータは、数値のみを指定する（たとえば、 `40000000`に設定すると 40000000 ナノ秒、つまり 40 ミリ秒を表します）、または数値と単位の両方を指定する（たとえば、直接`40ms`に設定する）という 2 つの方法で設定できます。
-   デフォルト値: `50000000` 、つまり50ミリ秒

### `processor-flush-interval` {#processor-flush-interval}

-   TiCDCクラスタ内のプロセッサモジュールがレプリケーションの進行状況をプッシュしようとする間隔を指定します。このパラメータはオプションで、デフォルト値は`50000000`ナノ秒（つまり50ミリ秒）です。
-   このパラメータの設定方法は`owner-flush-interval`と同様です。
-   デフォルト値: `50000000` 、つまり50ミリ秒

### ログ {#log}

#### `error-output` {#error-output}

-   zapログモジュールの内部エラーログの出力場所を指定します。このパラメータはオプションです。
-   デフォルト値: `"stderr"`

#### ログファイル {#logfile}

##### `max-size` {#max-size}

-   単一のログファイルの最大サイズを指定します。このパラメータはオプションです。
-   デフォルト値: `300`
-   単位: MiB

##### `max-days` {#max-days}

-   ログファイルを保持する最大日数を指定します。このパラメータはオプションです。
-   デフォルト値: `0` 、削除しないことを示します

##### `max-backups` {#max-backups}

-   保持するログファイルの数を指定します。このパラメータはオプションです。
-   デフォルト値: `0` 、すべてのログファイルを保持することを示します

### ソーター {#sorter}

#### `cache-size-in-mb` {#cache-size-in-mb}

-   デフォルトで起動される 8 つの Pebble DB の Sorter モジュール内の共有 Pebbleブロックキャッシュのサイズを指定します。
-   デフォルト値: `128`
-   単位: MiB

#### `sorter-dir` {#sorter-dir}

-   ソートファイルを保存するディレクトリを、データディレクトリ（ `data-dir` ）を基準として指定します。このパラメータはオプションです。
-   デフォルト値: `"/tmp/sorter"`

### kvクライアント {#kv-client}

#### `worker-concurrent` {#worker-concurrent}

-   単一のリージョンワーカーで使用できるスレッド数を指定します。このパラメータはオプションです。
-   デフォルト値: `8`

#### `worker-pool-size` {#worker-pool-size}

-   TiCDCの共有スレッドプール内のスレッド数を指定します。これは主にKVイベントの処理に使用されます。このパラメータはオプションです。
-   デフォルト値: `0` 、デフォルトのプールサイズがCPUコア数の2倍であることを示します。

#### `region-retry-duration` {#region-retry-duration}

-   リージョン接続の再試行期間を指定します。このパラメータはオプションです。
-   このパラメータは次の 2 つの方法で設定できます。
    -   数字のみを指定します。たとえば、 `50000000` 50000000ナノ秒（50ミリ秒）を表します。
    -   数値と単位の両方を指定します（例： `50ms`
-   デフォルト値: `60000000000` (1分)
