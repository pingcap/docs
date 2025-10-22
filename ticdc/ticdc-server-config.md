---
title: TiCDC Server Configurations
summary: TiCDC で使用される CLI と構成パラメータについて学習します。
---

# TiCDC サーバー構成 {#ticdc-server-configurations}

このドキュメントでは、TiCDC で使用される CLI および構成ファイルのパラメータについて説明します。

## <code>cdc server</code> CLIパラメータ {#code-cdc-server-code-cli-parameters}

以下は、 `cdc server`コマンドで使用できるオプションの説明です。

-   `addr` : TiCDCのリスニングアドレス、HTTP APIアドレス、およびTiCDCサービスのPrometheusアドレス。デフォルト値は`127.0.0.1:8300`です。
-   `advertise-addr` : クライアントがTiCDCにアクセスするために使用するアドバタイズされたアドレス。指定されていない場合、値は`addr`と同じになります。
-   `pd` : PD エンドポイントのコンマ区切りリスト。
-   `config` : TiCDCが使用する設定ファイルのアドレス（オプション）。このオプションはTiCDC v5.0.0以降でサポートされています。このオプションはTiUP v1.4.0以降のTiCDCデプロイメントで使用できます。詳細な設定については、 [TiCDC Changefeedフィード構成](/ticdc/ticdc-changefeed-config.md)参照してください。
-   `data-dir` : TiCDC がディスクを使用してファイルを保存する必要がある場合に使用するディレクトリを指定します。TiCDC が使用するソートエンジンと REDO ログは、このディレクトリに一時ファイルを保存します。このディレクトリの空きディスク容量は 500 GiB 以上確保することをお勧めします。TiUPを使用している場合は、セクション[`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers)で`data_dir`設定するか、 `global`でデフォルトのパス`data_dir`直接使用できます。
-   `gc-ttl` : TiCDC によって設定される PD のサービスレベル`GC safepoint`の TTL (Time To Live) と、レプリケーションタスクが一時停止できる期間（秒単位）。デフォルト値は`86400`で、これは 24 時間を意味します。注: TiCDC レプリケーションタスクの一時停止は、TiCDC GC セーフポイントの進行に影響します。つまり、 [TiCDC GCセーフポイントの完全な動作](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)で詳述されているように、上流の TiDB GC の進行にも影響します。
-   `log-file` : TiCDCプロセス実行時にログが出力されるパス。このパラメータが指定されていない場合、ログは標準出力（stdout）に書き込まれます。
-   `log-level` : TiCDCプロセス実行時のログレベル。デフォルト値は`"info"`です。
-   `ca` : TLS 接続用の PEM 形式の CA 証明書ファイルのパスを指定します (オプション)。
-   `cert` : TLS 接続用の PEM 形式の証明書ファイルのパスを指定します (オプション)。
-   `cert-allowed-cn` : TLS 接続の PEM 形式の共通名のパスを指定します (オプション)。
-   `key` : TLS 接続用の PEM 形式の秘密鍵ファイルのパスを指定します (オプション)。
-   `tz` : TiCDCサービスが使用するタイムゾーン。TiCDCは、 `TIMESTAMP`などの時間データ型を内部的に変換する場合、またはデータをダウンストリームに複製する場合にこのタイムゾーンを使用します。デフォルトは、プロセスが実行されるローカルタイムゾーンです。4（ `sink-uri` ）と`tz` `time-zone`指定すると、TiCDC内部プロセスは`tz`で指定されたタイムゾーンを使用し、シンクは`time-zone`で指定されたタイムゾーンを使用してダウンストリームにデータを複製します。14で指定されたタイムゾーンが`tz` （ `sink-uri` ）で指定されたタイムゾーンと同じであること`time-zone`確認してください。
-   `cluster-id` : (オプション) TiCDC クラスターの ID。デフォルト値は`default`です。 `cluster-id` TiCDC クラスターの一意の識別子です。同じ`cluster-id`を持つ TiCDC ノードは同じクラスターに属します。 `cluster-id`の長さは最大 128 文字です。 `cluster-id` `^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$`のパターンに従う必要があり、 `owner` 、 `capture` 、 `task` 、 `changefeed` 、 `job` 、 `meta`のいずれかにすることはできません。

## <code>cdc server</code>構成ファイルのパラメータ {#code-cdc-server-code-configuration-file-parameters}

以下は、コマンド`cdc server`の`config`オプションで指定される設定ファイルについて説明します。デフォルトの設定ファイルは[`pkg/cmd/util/ticdc.toml`](https://github.com/pingcap/tiflow/blob/master/pkg/cmd/util/ticdc.toml)にあります。

### <code>newarch</code> <span class="version-mark">v8.5.4-release.1 の新機能</span> {#code-newarch-code-span-class-version-mark-new-in-v8-5-4-release-1-span}

-   [TiCDCの新しいアーキテクチャ](/ticdc/ticdc-architecture.md)有効にするかどうかを制御します。
-   デフォルト値: `false` 、 [TiCDC クラシックアーキテクチャ](/ticdc/ticdc-classic-architecture.md)が使用されることを示します。
-   `true`に設定すると、TiCDC の新しいアーキテクチャが有効になります。

<!-- The configuration method of the following parameters is the same as that of CLI parameters, but the CLI parameters have higher priorities. -->

### <code>addr</code> {#code-addr-code}

-   例: `"127.0.0.1:8300"`

### <code>advertise-addr</code> {#code-advertise-addr-code}

-   例: `""`

### <code>log-file</code> {#code-log-file-code}

-   例: `""`

### <code>log-level</code> {#code-log-level-code}

-   例: `"info"`

### <code>data-dir</code> {#code-data-dir-code}

-   例: `""`

### <code>gc-ttl</code> {#code-gc-ttl-code}

-   例: `86400` (24時間)

### <code>tz</code> {#code-tz-code}

-   例: `"System"`

### <code>cluster-id</code> {#code-cluster-id-code}

-   例: `"default"`

### <code>gc-tuner-memory-threshold</code> {#code-gc-tuner-memory-threshold-code}

-   GOGCチューニングの最大メモリしきい値を指定します。しきい値を小さくするとGCの頻度が増加します。しきい値を大きくするとGCの頻度は減少しますが、TiCDCプロセスで消費されるメモリリソースが増加します。メモリ使用量がこのしきい値を超えると、GOGC Tunerは動作を停止します。
-   デフォルト値: `0` 、GOGCチューナーが無効であることを示します
-   単位: バイト

### 安全 {#security}

#### <code>ca-path</code> {#code-ca-path-code}

-   例: `""`

#### <code>cert-path</code> {#code-cert-path-code}

-   例: `""`

#### <code>key-path</code> {#code-key-path-code}

-   例: `""`

#### <code>mtls</code> {#code-mtls-code}

-   TLS クライアント認証を有効にするかどうかを制御します。
-   デフォルト値: `false`

#### <code>client-user-required</code> {#code-client-user-required-code}

-   クライアント認証にユーザー名とパスワードを使用するかどうかを制御します。デフォルト値は false です。
-   デフォルト値: `false`

#### <code>client-allowed-user</code> {#code-client-allowed-user-code}

-   クライアント認証に許可されるユーザー名をリストします。このリストにないユーザー名による認証要求は拒否されます。
-   デフォルト値: `null`

<!-- Example: `["username_1", "username_2"]` -->

### <code>capture-session-ttl</code> {#code-capture-session-ttl-code}

-   TiCDCとetcdサービス間のセッション期間を指定します。このパラメータはオプションです。
-   デフォルト値: `10`
-   単位: 秒

### <code>owner-flush-interval</code> {#code-owner-flush-interval-code}

-   TiCDCクラスタ内のオーナーモジュールがレプリケーションの進行状況をプッシュしようとする間隔を指定します。このパラメータはオプションで、デフォルト値は`50000000`ナノ秒（つまり50ミリ秒）です。
-   このパラメータは、数値のみを指定する（たとえば、 `40000000`に設定すると 40000000 ナノ秒、つまり 40 ミリ秒を表します）、または数値と単位の両方を指定する（たとえば、直接`40ms`に設定する）という 2 つの方法で設定できます。
-   デフォルト値: `50000000` 、つまり50ミリ秒

### <code>processor-flush-interval</code> {#code-processor-flush-interval-code}

-   TiCDCクラスタ内のプロセッサモジュールがレプリケーションの進行状況をプッシュしようとする間隔を指定します。このパラメータはオプションで、デフォルト値は`50000000`ナノ秒（つまり50ミリ秒）です。
-   このパラメータの設定方法は`owner-flush-interval`と同様です。
-   デフォルト値: `50000000` 、つまり50ミリ秒

### ログ {#log}

#### <code>error-output</code> {#code-error-output-code}

-   zapログモジュールの内部エラーログの出力場所を指定します。このパラメータはオプションです。
-   デフォルト値: `"stderr"`

#### ログファイル {#log-file}

##### <code>max-size</code> {#code-max-size-code}

-   単一のログファイルの最大サイズを指定します。このパラメータはオプションです。
-   デフォルト値: `300`
-   単位: MiB

##### <code>max-days</code> {#code-max-days-code}

-   ログファイルを保持する最大日数を指定します。このパラメータはオプションです。
-   デフォルト値: `0` 、削除しないことを示します

##### <code>max-backups</code> {#code-max-backups-code}

-   保持するログファイルの数を指定します。このパラメータはオプションです。
-   デフォルト値: `0` 、すべてのログファイルを保持することを示します

### ソーター {#sorter}

#### <code>cache-size-in-mb</code> {#code-cache-size-in-mb-code}

-   デフォルトで起動される 8 つの Pebble DB の Sorter モジュール内の共有 Pebbleブロックキャッシュのサイズを指定します。
-   デフォルト値: `128`
-   単位: MiB

#### <code>sorter-dir</code> {#code-sorter-dir-code}

-   ソートファイルを保存するディレクトリを、データディレクトリ（ `data-dir` ）を基準として指定します。このパラメータはオプションです。
-   デフォルト値: `"/tmp/sorter"`

### kvクライアント {#kv-client}

#### <code>worker-concurrent</code> {#code-worker-concurrent-code}

-   単一のリージョンワーカーで使用できるスレッド数を指定します。このパラメータはオプションです。
-   デフォルト値: `8`

#### <code>worker-pool-size</code> {#code-worker-pool-size-code}

-   TiCDCの共有スレッドプール内のスレッド数を指定します。これは主にKVイベントの処理に使用されます。このパラメータはオプションです。
-   デフォルト値: `0` 、デフォルトのプールサイズがCPUコア数の2倍であることを示します。

#### <code>region-retry-duration</code> {#code-region-retry-duration-code}

-   リージョン接続の再試行期間を指定します。このパラメータはオプションです。
-   このパラメータは次の 2 つの方法で設定できます。
    -   数字のみを指定します。たとえば、 `50000000` 50000000ナノ秒（50ミリ秒）を表します。
    -   数値と単位の両方を指定します（例： `50ms`
-   デフォルト値: `60000000000` (1分)
