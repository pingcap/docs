---
title: Configure TiFlash
summary: TiFlash の設定方法を学びます。
---

# TiFlashの設定 {#configure-tiflash}

このドキュメントでは、 TiFlashの展開と使用に関連する構成パラメータについて説明します。

## TiFlash構成パラメータ {#tiflash-configuration-parameters}

このセクションでは、 TiFlashの設定パラメータについて説明します。

> **ヒント：**
>
> 構成項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

### <code>tiflash.toml</code>ファイルを設定する {#configure-the-code-tiflash-toml-code-file}

#### <code>listen_host</code> {#code-listen-host-code}

-   TPC/HTTP などのサービスをサポートするためのリスニング ホスト。
-   これを`"0.0.0.0"`に設定することをお勧めします。これは、このマシンのすべての IP アドレスをリッスンすることを意味します。

#### <code>tcp_port</code> {#code-tcp-port-code}

-   TiFlash TCP サービスポート。このポートは内部テストに使用され、デフォルトでは 9000 に設定されています。
-   TiFlash v7.1.0より前のバージョンでは、このポートはデフォルトで有効になっていますが、セキュリティリスクがあります。セキュリティを強化するため、このポートにアクセス制御を適用し、ホワイトリストに登録されたIPアドレスからのアクセスのみを許可することをお勧めします。TiFlash v7.1.0以降では、このポートの設定をコメントアウトすることでセキュリティリスクを回避できます。TiFlashの設定ファイルでこのポートが指定されていない場合、このポートは無効になります。
-   TiFlashデプロイメントでは、このポートを構成することは推奨され**ません**。(注: TiFlash v7.1.0 以降、 TiUP &gt;= v1.12.5 またはTiDB Operator &gt;= v1.5.0 でデプロイされたTiFlash は、デフォルトでポートを無効にし、より安全になっています。)
-   デフォルト値: `9000`

#### <code>mark_cache_size</code> {#code-mark-cache-size-code}

-   データブロックのメタデータのキャッシュサイズ制限。通常、この値を変更する必要はありません。
-   デフォルト値: `1073741824`

#### <code>minmax_index_cache_size</code> {#code-minmax-index-cache-size-code}

-   データブロックの最小-最大インデックスのキャッシュサイズ制限。通常、この値を変更する必要はありません。
-   デフォルト値: `1073741824`

#### <code>delta_index_cache_size</code> {#code-delta-index-cache-size-code}

-   DeltaIndex のキャッシュ サイズの制限。
-   デフォルト値: `0` 、制限がないことを意味します。

#### <code>path</code> {#code-path-code}

-   TiFlashデータのstorageパス。複数のディレクトリがある場合は、各ディレクトリをカンマで区切ってください。
-   TiDB v4.0.9以降、 `path`と[`path_realtime_mode`](#path_realtime_mode)は非推奨となりました。マルチディスク展開シナリオでパフォーマンスを向上させるには、 [`storage`](#storage-new-in-v409)セクションの設定を使用してください。
-   TiDB v5.2.0 以降、 [`storage.io_rate_limit`](#storageio_rate_limit-new-in-v520)構成を使用する必要がある場合は、同時にTiFlashデータのstorageパスを[`storage.main.dir`](#dir)に設定する必要があります。
-   `storage`構成が存在する場合、 `path`と[`path_realtime_mode`](#path_realtime_mode)構成は両方とも無視されます。

<!-- Example: `"/tidb-data/tiflash-9000"` or `"/ssd0/tidb-data/tiflash,/ssd1/tidb-data/tiflash,/ssd2/tidb-data/tiflash"` -->

#### <code>path_realtime_mode</code> {#code-path-realtime-mode-code}

-   `true`に設定し、 `path`に複数のディレクトリを設定した場合、最初のディレクトリに最新のデータが保存され、残りのディレクトリには古いデータが保存されます。
-   TiDB v4.0.9以降、 [`path`](#path)と`path_realtime_mode`は非推奨となりました。マルチディスク展開シナリオでパフォーマンスを向上させるには、 [`storage`](#storage-new-in-v409)セクションの設定を使用してください。
-   `storage`構成が存在する場合、 [`path`](#path)と`path_realtime_mode`構成は両方とも無視されます。
-   デフォルト値: `false`

#### <code>tmp_path</code> {#code-tmp-path-code}

-   TiFlash一時ファイルが保存されるパス。
-   デフォルトでは、 [`path`](#path)の最初のディレクトリ、または[`storage.latest.dir`](#dir-1)に`"/tmp"`を付加したディレクトリになります。

<!-- Example: `"/tidb-data/tiflash-9000/tmp"` -->

#### storage<span class="version-mark">v4.0.9 の新機能</span> {#storage-span-class-version-mark-new-in-v4-0-9-span}

storageパス関連の設定を構成します。

##### <code>format_version</code> {#code-format-version-code}

-   DTFile 形式。
-   デフォルト値: `7`
-   `6` `4` `7` `5` `2` `3`
    -   `format_version = 2` : バージョン v6.0.0 未満のデフォルトの形式。
    -   `format_version = 3` : v6.0.0 および v6.1.x のデフォルト形式。より多くのデータ検証機能が提供されます。
    -   `format_version = 4` : バージョン v6.2.0 から v7.3.0 までのデフォルトの形式。書き込み増幅とバックグラウンド タスクのリソース消費を削減します。
    -   `format_version = 5` : v7.3.0 で導入され、v7.4.0 から v8.3.0 までのバージョンのデフォルト形式で、小さなファイルを結合することで物理ファイルの数を削減します。
    -   `format_version = 6` : v8.4.0 で導入され、ベクトル インデックスの構築とstorageを部分的にサポートします。
    -   `format_version = 7` : v8.4.0 で導入され、v8.4.0 以降のバージョンのデフォルト形式で、ベクトル インデックスの構築とstorageをサポートします。

#### storage.main {#storage-main}

##### <code>dir</code> {#code-dir-code}

-   メインデータを保存するディレクトリのリスト。例： `[ "/tidb-data/tiflash-9000" ]`または`[ "/ssd0/tidb-data/tiflash", "/ssd1/tidb-data/tiflash" ]` 。
-   全データの 90% 以上がディレクトリ リストに保存されます。

##### <code>capacity</code> {#code-capacity-code}

-   [`storage.main.dir`](#dir)内の各ディレクトリの最大storage容量。例: `[10737418240, 10737418240]` 。
-   設定されていない場合、または`0`倍数に設定されている場合、実際のディスク (ディレクトリが配置されているディスク) の容量が使用されます。
-   単位: バイト`"10GB"`などの人間が読める数値はまだサポートされていないことに注意してください。
-   `capacity`番目のリストのサイズは[`storage.main.dir`](#dir)リストのサイズと同じである必要があります。

#### storage.latest {#storage-latest}

##### <code>dir</code> {#code-dir-code}

-   最新データを保存するディレクトリのリストです。全データの約10%がこのディレクトリリストに保存されます。ここにリストされているディレクトリ（またはディレクトリ）は、 [`storage.main.dir`](#dir)よりも高いIOPSメトリックを必要とします。
-   設定されていない場合（デフォルト）、値[`storage.main.dir`](#dir)が使用されます。

<!-- Example: `[]` -->

##### <code>capacity</code> {#code-capacity-code}

-   [`storage.latest.dir`](#dir-1)内の各ディレクトリの最大storage容量。設定されていない場合、または`0`倍数に設定されている場合は、実際のディスク（ディレクトリが配置されているディスク）の容量が使用されます。

<!-- Example: `[10737418240, 10737418240]` -->

#### storage.io_rate_limit <span class="version-mark">v5.2.0 の新機能</span> {#storage-io-rate-limit-span-class-version-mark-new-in-v5-2-0-span}

I/O トラフィック制限設定を構成します。

##### <code>max_bytes_per_sec</code> {#code-max-bytes-per-sec-code}

-   ディスクの読み取りと書き込みの合計I/O帯域幅。この設定項目は、I/Oトラフィックを制限するかどうかを決定します。デフォルトでは無効になっています。TiFlashにおけるこのトラフィック制限は、ディスク帯域幅が小さく、特定のサイズに制限TiFlashれているクラウドstorageに適しています。
-   デフォルト値: `0` 。これは、I/O トラフィックがデフォルトで制限されないことを意味します。
-   単位: バイト

##### <code>max_read_bytes_per_sec</code> {#code-max-read-bytes-per-sec-code}

-   ディスク読み取りの合計 I/O 帯域幅。
-   設定項目`max_read_bytes_per_sec`および`max_write_bytes_per_sec` 、ディスクの読み取りと書き込みの I/O 帯域幅を個別に制限します。Google Cloud が提供する Persistent Disk など、ディスクの読み取りと書き込みの I/O 帯域幅の制限を個別に計算するクラウドstorageに使用できます。
-   `max_bytes_per_sec`の値が`0`でない場合は[`max_bytes_per_sec`](#max_bytes_per_sec)が優先されます。
-   デフォルト値: `0`

##### <code>max_write_bytes_per_sec</code> {#code-max-write-bytes-per-sec-code}

-   ディスク書き込みの合計 I/O 帯域幅。
-   設定項目`max_read_bytes_per_sec`および`max_write_bytes_per_sec` 、ディスクの読み取りと書き込みの I/O 帯域幅を個別に制限します。Google Cloud が提供する Persistent Disk など、ディスクの読み取りと書き込みの I/O 帯域幅の制限を個別に計算するクラウドstorageに使用できます。
-   `max_bytes_per_sec`の値が`0`でない場合は[`max_bytes_per_sec`](#max_bytes_per_sec)が優先されます。
-   デフォルト値: `0`

##### <code>foreground_write_weight</code> {#code-foreground-write-weight-code}

<!-- The following  default configurations indicate that each type of traffic gets a weight of 25% (25 / (25 + 25 + 25 + 25) = 25%) -->

-   TiFlashは内部的にI/O要求を4つのタイプに分類します。フォアグラウンド書き込み、バックグラウンド書き込み、フォアグラウンド読み取り、バックグラウンド読み取りです。1 `foreground_write_weight`フォアグラウンド書き込みI/Oトラフィックタイプに割り当てられる帯域幅の重みを制御します。通常、これらのパラメータを調整する必要はありません。
-   I/O トラフィック制限が初期化されると、 TiFlash は`foreground_write_weight` 、 [`background_write_weight`](/tiflash/tiflash-configuration.md#background_write_weight) 、 [`foreground_read_weight`](/tiflash/tiflash-configuration.md#foreground_read_weight) 、 [`background_read_weight`](/tiflash/tiflash-configuration.md#background_read_weight)の比率に従って、これら 4 種類の要求に帯域幅を割り当てます。
-   重みが`0`に設定されている場合、対応する I/O トラフィックは制限されません。
-   デフォルト値: `25` 、帯域幅の 25% の割り当てを表します。

##### <code>background_write_weight</code> {#code-background-write-weight-code}

-   TiFlashは内部的にI/O要求を4つのタイプ（フォアグラウンド書き込み、バックグラウンド書き込み、フォアグラウンド読み取り、バックグラウンド読み取り）に分類します。1 `background_write_weight` 、バックグラウンド書き込みI/Oトラフィックタイプに割り当てられる帯域幅の重みを制御します。通常、これらのパラメータを調整する必要はありません。
-   I/O トラフィック制限が初期化されると、 TiFlash は[`foreground_write_weight`](/tiflash/tiflash-configuration.md#foreground_write_weight) 、 `background_write_weight` 、 [`foreground_read_weight`](/tiflash/tiflash-configuration.md#foreground_read_weight) 、 [`background_read_weight`](/tiflash/tiflash-configuration.md#background_read_weight)の比率に従って、これら 4 種類の要求に帯域幅を割り当てます。
-   重みが`0`に設定されている場合、対応する I/O トラフィックは制限されません。
-   デフォルト値: `25` 、帯域幅の 25% の割り当てを表します。

##### <code>foreground_read_weight</code> {#code-foreground-read-weight-code}

-   TiFlashは内部的にI/O要求を4つのタイプ（フォアグラウンド書き込み、バックグラウンド書き込み、フォアグラウンド読み取り、バックグラウンド読み取り）に分類します。1 `foreground_read_weight` 、フォアグラウンド読み取りI/Oトラフィックタイプに割り当てられる帯域幅の重みを制御します。通常、これらのパラメータを調整する必要はありません。
-   I/O トラフィック制限が初期化されると、 TiFlash は[`foreground_write_weight`](/tiflash/tiflash-configuration.md#foreground_write_weight) 、 [`background_write_weight`](/tiflash/tiflash-configuration.md#background_write_weight) 、 `foreground_read_weight` 、 [`background_read_weight`](/tiflash/tiflash-configuration.md#background_read_weight)の比率に従って、これら 4 種類の要求に帯域幅を割り当てます。
-   重みが`0`に設定されている場合、対応する I/O トラフィックは制限されません。
-   デフォルト値: `25` 、帯域幅の 25% の割り当てを表します。

##### <code>background_read_weight</code> {#code-background-read-weight-code}

-   TiFlashは内部的にI/O要求を4つのタイプ（フォアグラウンド書き込み、バックグラウンド書き込み、フォアグラウンド読み取り、バックグラウンド読み取り）に分類します。1 `background_read_weight` 、バックグラウンド読み取りI/Oトラフィックタイプに割り当てられる帯域幅の重みを制御します。通常、これらのパラメータを調整する必要はありません。
-   I/O トラフィック制限が初期化されると、 TiFlash は[`foreground_write_weight`](/tiflash/tiflash-configuration.md#foreground_write_weight) 、 [`background_write_weight`](/tiflash/tiflash-configuration.md#background_write_weight) 、 [`foreground_read_weight`](/tiflash/tiflash-configuration.md#foreground_read_weight) 、 `background_read_weight`の比率に従って、これら 4 種類の要求に帯域幅を割り当てます。
-   重みが`0`に設定されている場合、対応する I/O トラフィックは制限されません。
-   デフォルト値: `25` 、帯域幅の 25% の割り当てを表します。

##### <code>auto_tune_sec</code> {#code-auto-tune-sec-code}

-   TiFlashは、現在のI/O負荷に応じて、異なるI/Oタイプのトラフィック制限を自動的に調整する機能をサポートしています。調整された帯域幅が、上記で設定した重み付け比率を超える場合があります。
-   `auto_tune_sec`自動チューニングの間隔を示します。auto_tune_sec の値が`0`の場合、自動チューニングは無効になります。
-   デフォルト値: `5`
-   単位: 秒

#### storage.s3 {#storage-s3}

以下の設定項目は、 TiFlash分散storageおよびコンピューティングアーキテクチャモードにのみ適用されます。詳細については、 [TiFlash分散ストレージおよびコンピューティングアーキテクチャと S3 サポート](/tiflash/tiflash-disaggregated-and-s3.md)参照してください。

##### <code>endpoint</code> {#code-endpoint-code}

-   S3エンドポイントアドレス。例: `http://s3.{region}.amazonaws.com` 。

##### <code>bucket</code> {#code-bucket-code}

-   TiFlash はすべてのデータをこのバケットに保存します。

##### <code>root</code> {#code-root-code}

-   S3 バケット内でデータが保存されるルートディレクトリ。例: `/cluster1_data` 。

##### <code>access_key_id</code> {#code-access-key-id-code}

-   S3 にアクセスするために使用される ACCESS_KEY_ID。

##### <code>secret_access_key</code> {#code-secret-access-key-code}

-   S3 にアクセスするために使用される SECRET_ACCESS_KEY。

#### storage.remote.cache {#storage-remote-cache}

##### <code>dir</code> {#code-dir-code}

-   分散storageおよびコンピューティングアーキテクチャ内のコンピューティング ノードのローカル データ キャッシュ ディレクトリ。

<!-- Example: `"/data1/tiflash/cache"` -->

##### <code>capacity</code> {#code-capacity-code}

-   例: `858993459200` (800 GiB)

#### フラッシュ {#flash}

##### <code>service_addr</code> {#code-service-addr-code}

-   TiFlashコプロセッサ サービスのリスニング アドレス。

<!-- Example: `"0.0.0.0:3930"` -->

##### <code>compact_log_min_gap</code> <span class="version-mark">v7.4.0 の新機能</span> {#code-compact-log-min-gap-code-span-class-version-mark-new-in-v7-4-0-span}

-   現在のRaftステート マシンによって進められた`applied_index`と最後のディスク スピル時の`applied_index`との差が`compact_log_min_gap`超えると、 TiFlash はTiKV から`CompactLog`コマンドを実行し、データをディスクにスピルします。
-   このギャップを大きくすると、 TiFlashのディスク書き込み頻度が低下し、ランダム書き込みシナリオにおける読み取りレイテンシーが短縮される可能性がありますが、メモリオーバーヘッドも増加する可能性があります。このギャップを小さくすると、 TiFlashのディスク書き込み頻度が増加し、 TiFlashのメモリ負荷が軽減される可能性があります。ただし、現段階では、このギャップを`0`に設定しても、 TiFlashのディスク書き込み頻度は TiKV よりも高くなることはありません。
-   デフォルト値を維持することをお勧めします。
-   デフォルト値: `200`

##### <code>compact_log_min_rows</code><span class="version-mark">バージョン5.0の新機能</span> {#code-compact-log-min-rows-code-span-class-version-mark-new-in-v5-0-span}

-   TiFlashによってキャッシュされた領域内の行の数またはサイズが`compact_log_min_rows`または`compact_log_min_bytes`超えると、 TiFlash はTiKV から`CompactLog`コマンドを実行し、データをディスクに書き込みます。
-   デフォルト値を維持することをお勧めします。
-   デフォルト値: `40960`

##### <code>compact_log_min_bytes</code><span class="version-mark">バージョン5.0の新機能</span> {#code-compact-log-min-bytes-code-span-class-version-mark-new-in-v5-0-span}

-   TiFlashによってキャッシュされた領域内の行の数またはサイズが`compact_log_min_rows`または`compact_log_min_bytes`超えると、 TiFlash はTiKV から`CompactLog`コマンドを実行し、データをディスクに書き込みます。
-   デフォルト値を維持することをお勧めします。
-   デフォルト値: `33554432`

##### <code>disaggregated_mode</code> {#code-disaggregated-mode-code}

-   この設定項目は、 TiFlash分散storageおよびコンピューティングアーキテクチャモードにのみ適用されます。詳細については、 [TiFlash分散ストレージおよびコンピューティングアーキテクチャと S3 サポート](/tiflash/tiflash-disaggregated-and-s3.md)参照してください。
-   値`"tiflash_compute"`オプション: `"tiflash_write"`

##### <code>graceful_wait_shutdown_timeout</code> <span class="version-mark">v8.5.4 の新機能</span> {#code-graceful-wait-shutdown-timeout-code-span-class-version-mark-new-in-v8-5-4-span}

-   TiFlashサーバーをシャットダウンする際の最大待機時間を制御します。この期間中、 TiFlash は未完了の MPP タスクの実行を継続しますが、新しいタスクは受け付けません。実行中のすべての MPP タスクがこのタイムアウト前に終了した場合、 TiFlash は直ちにシャットダウンします。それ以外の場合は、待機時間が経過した後に強制的にシャットダウンされます。
-   デフォルト値: `600`
-   単位: 秒
-   TiFlashサーバーがシャットダウンを待機している間 (猶予期間中)、TiDB は新しい MPP タスクをサーバーに送信しません。

#### フラッシュプロキシ {#flash-proxy}

##### <code>addr</code> {#code-addr-code}

-   プロキシのリスニング アドレス。
-   デフォルト値: `"127.0.0.1:20170"`

##### <code>advertise-addr</code> {#code-advertise-addr-code}

-   外部アクセスアドレス`addr` 。空のままにした場合、デフォルトで`addr`使用されます。
-   クラスターを複数のノードに展開する場合は、他のノードが`advertise-addr`を介してアクセスできることを保証する必要があります。

##### <code>status-addr</code> {#code-status-addr-code}

-   プロキシがメトリックまたはステータス情報を取得するリスニング アドレス。
-   デフォルト値: `"127.0.0.1:20292"`

##### <code>advertise-status-addr</code> {#code-advertise-status-addr-code}

-   status-addrの外部アクセスアドレス。空のままにした場合、デフォルトで`status-addr`が使用されます。
-   クラスターを複数のノードに展開する場合は、他のノードが`advertise-status-addr`を介してアクセスできることを保証する必要があります。

##### <code>engine-addr</code> {#code-engine-addr-code}

-   TiFlashコプロセッサ サービスの外部アクセス アドレス。

<!-- Example: `"10.0.1.20:3930"` -->

##### <code>data-dir</code> {#code-data-dir-code}

-   プロキシのデータstorageパス。

<!-- Example: `"/tidb-data/tiflash-9000/flash"` -->

##### <code>config</code> {#code-config-code}

-   プロキシの構成ファイル パス。

<!-- Example: `"/tidb-deploy/tiflash-9000/conf/tiflash-learner.toml"` -->

##### <code>log-file</code> {#code-log-file-code}

-   プロキシのログ パス。

<!-- Example: `"/tidb-deploy/tiflash-9000/log/tiflash_tikv.log"` -->

#### ロガー {#logger}

以下のパラメータはTiFlashログとTiFlashエラーログにのみ有効です。TiFlashTiFlashのログパラメータを設定する必要がある場合は、 [`tiflash-learner.toml`](#configure-the-tiflash-learnertoml-file)で指定してください。

##### <code>level</code> {#code-level-code}

-   ログ レベル。
-   デフォルト値: `"info"`
-   `"info"` `"debug"` `"error"` `"warn"` `"trace"`

##### <code>log</code> {#code-log-code}

-   TiFlashのログです。

<!-- Example: `"/tidb-deploy/tiflash-9000/log/tiflash.log"` -->

##### <code>errorlog</code> {#code-errorlog-code}

-   TiFlashのエラーログ。レベル`"warn"`とレベル`"error"`ログもこのログファイルに出力されます。

<!-- Example: `"/tidb-deploy/tiflash-9000/log/tiflash_error.log"` -->

##### <code>size</code> {#code-size-code}

-   1 つのログ ファイルのサイズ。
-   デフォルト値: `"100M"`

##### <code>count</code> {#code-count-code}

-   保存できるログファイルの最大数。TiFlashTiFlashとTiFlashエラーログの場合、保存できるログファイルの最大数はそれぞれ`count`です。
-   デフォルト値: `10`

#### ラフト {#raft}

##### <code>pd_addr</code> {#code-pd-addr-code}

-   PD サービス アドレス。
-   複数のアドレスはカンマで区切られます。例： `"10.0.1.11:2379,10.0.1.12:2379,10.0.1.13:2379"` 。

#### 状態 {#status}

##### <code>metrics_port</code> {#code-metrics-port-code}

-   Prometheus がメトリック情報を取得するポート。
-   デフォルト値: `8234`

#### プロファイル.デフォルト {#profiles-default}

##### <code>dt_enable_logical_split</code> {#code-dt-enable-logical-split-code}

-   DeltaTreeストレージエンジンのセグメントで論理分割を使用するかどうかを指定します。論理分割を使用すると書き込み増幅を削減できますが、ディスク領域の無駄が発生します。
-   v6.2.0以降のバージョンでは、デフォルト値の`false`を維持し、 `true`に変更しないことを強くお勧めします。詳細については、既知の問題[＃5576](https://github.com/pingcap/tiflash/issues/5576)を参照してください。
-   デフォルト値: `false`

##### <code>max_threads</code> {#code-max-threads-code}

-   `max_threads` 、 TiFlash がMPP タスクを実行する際の内部スレッド同時実行数を示します。2 `0`設定すると、 TiFlash は論理 CPU コアの数を同時実行数として使用します。
-   このパラメータは、システム変数[`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610) `-1`に設定されている場合にのみ有効になります。
-   デフォルト値: `0`

##### <code>max_memory_usage</code> {#code-max-memory-usage-code}

-   単一のクエリで生成される中間データのメモリ使用量の制限。
-   値が整数の場合、単位はバイトです。例えば、 `34359738368` 32GiBのメモリ制限を意味します。
-   値が 1 から`[0.0, 1.0)`の範囲の浮動小数点数の場合、ノードの総メモリに対する許容メモリ使用量の比率を表します。例えば、 `0.8`総メモリの 80% を意味し、 `0.0`無制限を意味します。
-   クエリがこの制限を超えるメモリを消費しようとすると、クエリは終了され、エラーが報告されます。
-   デフォルト値: `0` 、制限がないことを意味します。

##### <code>max_memory_usage_for_all_queries</code> {#code-max-memory-usage-for-all-queries-code}

-   すべてのクエリで生成される中間データのメモリ使用量制限。
-   値が整数の場合、単位はバイトです。例えば、 `34359738368` 32GiBのメモリ制限を意味し、 `0`制限なしを意味します。
-   v6.6.0以降では、 `[0.0, 1.0)`から10000000000000の範囲の浮動小数点数で値を設定できます。この数値は、許容されるメモリ使用量とノード全体のメモリ使用量の比率を表します。例えば、 `0.8`メモリの80%、 `0.0`無制限を意味します。
-   クエリがこの制限を超えるメモリを消費しようとすると、クエリは終了され、エラーが報告されます。
-   デフォルト値： `0.8` （総メモリの80%を意味します）。v6.6.0より前のバージョンでは、デフォルト値は`0` （無制限を意味します）でした。

##### <code>cop_pool_size</code><span class="version-mark">バージョン5.0の新機能</span> {#code-cop-pool-size-code-span-class-version-mark-new-in-v5-0-span}

-   TiFlashコプロセッサーが同時に実行できるcopリクエストの最大数を指定します。リクエスト数がこの値を超えても、10倍以内の場合、超過したリクエストはキューに入れられます。リクエスト数がこの値の10倍を超える場合、超過したリクエストはTiFlashによって拒否されます。設定値が`0`に設定されている場合、または設定されていない場合は、デフォルト値（物理コア数の2倍）が使用されます。
-   デフォルト値: 物理コア数の2倍

##### <code>cop_pool_handle_limit</code><span class="version-mark">バージョン5.0の新機能</span> {#code-cop-pool-handle-limit-code-span-class-version-mark-new-in-v5-0-span}

-   TiFlashコプロセッサーが同時に処理できるCOPリクエストの最大数を指定します。これには、実行中のリクエストとキューで待機中のリクエストが含まれます。リクエスト数が指定値を超えると、エラー`TiFlash Server is Busy`が返されます。
-   `-1`制限がないことを示し、 `0`デフォルト値の`10 * cop_pool_size`を使用することを示します。

##### <code>cop_pool_max_queued_seconds</code><span class="version-mark">バージョン5.0の新機能</span> {#code-cop-pool-max-queued-seconds-code-span-class-version-mark-new-in-v5-0-span}

-   cop要求がTiFlashにキューイングできる最大時間を指定します。cop要求がこの設定で指定された値よりも長くキュー内で待機した場合、エラー`TiFlash Server is Busy`が返されます。
-   `0`以下の値は制限がないことを示します。
-   デフォルト値: `15`

##### <code>batch_cop_pool_size</code><span class="version-mark">バージョン5.0の新機能</span> {#code-batch-cop-pool-size-code-span-class-version-mark-new-in-v5-0-span}

-   TiFlashコプロセッサーが同時に実行するバッチリクエストの最大数を指定します。リクエスト数が指定値を超えた場合、超過分のリクエストはキューに入れられます。設定値が`0`に設定されているか未設定の場合は、デフォルト値（物理コア数の2倍）が使用されます。
-   デフォルト値: 物理コア数の2倍

##### <code>manual_compact_pool_size</code><span class="version-mark">バージョン6.1の新機能</span> {#code-manual-compact-pool-size-code-span-class-version-mark-new-in-v6-1-span}

-   TiFlash がTiDB から`ALTER TABLE ... COMPACT`受信したときに同時に処理できる要求の数を指定します。
-   値が`0`に設定されている場合、デフォルト値`1`が優先されます。
-   デフォルト値: `1`

##### <code>enable_elastic_threadpool</code><span class="version-mark">バージョン5.4.0の新機能</span> {#code-enable-elastic-threadpool-code-span-class-version-mark-new-in-v5-4-0-span}

-   エラスティック スレッド プール機能を有効にするかどうかを制御します。この機能により、 TiFlashの同時実行性の高いシナリオで CPU 使用率が大幅に向上します。
-   デフォルト値: `true`

##### <code>dt_compression_method</code> {#code-dt-compression-method-code}

-   TiFlashstorageエンジンの圧縮アルゴリズム。
-   デフォルト値: `LZ4`
-   値のオプション: `LZ4` `LZ4HC`値は`zstd`と小文字を区別しません。

##### <code>dt_compression_level</code> {#code-dt-compression-level-code}

-   TiFlashstorageエンジンの圧縮レベル。
-   `dt_compression_method`が`LZ4`の場合は、この値を`1`に設定することをお勧めします。
-   この値は`-1` (圧縮率は低くなりますが、読み取りパフォーマンスは向上します) に設定するか、 `dt_compression_method`が`zstd`の場合は`1`に設定することをお勧めします。
-   `dt_compression_method`が`LZ4HC`の場合は、この値を`9`に設定することをお勧めします。
-   デフォルト値: `1`

##### <code>dt_page_gc_threshold</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-dt-page-gc-threshold-code-span-class-version-mark-new-in-v6-2-0-span}

-   PageStorageデータファイル内の有効データの最小比率を指定します。PageStorageデータファイル内の有効データの比率がこの設定値を下回ると、GCがトリガーされ、ファイル内のデータが圧縮されます。
-   デフォルト値: `0.5`

##### <code>max_bytes_before_external_group_by</code> <span class="version-mark">v7.0.0 の新機能</span> {#code-max-bytes-before-external-group-by-code-span-class-version-mark-new-in-v7-0-0-span}

-   ハッシュ集計演算子（キー`GROUP BY`で使用可能な最大メモリを指定します。この値を超えるとディスクへの書き込みがトリガーされます。メモリ使用量がしきい値を超えると、ハッシュ集計はメモリ使用量を[ディスクへのスピル](/tiflash/tiflash-spill-disk.md)削減します。
-   デフォルト値: `0` 。これは、メモリ使用量が無制限であり、ハッシュ集計にディスクへのスピルが使用されないことを意味します。

##### <code>max_bytes_before_external_sort</code><span class="version-mark">バージョン7.0.0の新機能</span> {#code-max-bytes-before-external-sort-code-span-class-version-mark-new-in-v7-0-0-span}

-   ソート演算子またはtopN演算子で使用可能な最大メモリを指定します。この値を超えるとディスクへの書き込みがトリガーされます。メモリ使用量がこのしきい値を超えると、ソート演算子またはtopN演算子はメモリ使用量を[ディスクへのスピル](/tiflash/tiflash-spill-disk.md)ずつ減らします。
-   デフォルト値: `0` 。これは、メモリ使用量が無制限であり、ソートや topN にディスクへのスピルが使用されないことを意味します。

##### <code>max_bytes_before_external_join</code><span class="version-mark">バージョン7.0.0の新機能</span> {#code-max-bytes-before-external-join-code-span-class-version-mark-new-in-v7-0-0-span}

-   等価結合条件を持つハッシュ結合演算子で使用可能な最大メモリを指定します。この値を超えるとディスクへの書き込みがトリガーされます。メモリ使用量がしきい値を超えると、HashJoin はメモリ使用量を[ディスクへのスピル](/tiflash/tiflash-spill-disk.md)減らします。
-   デフォルト値: `0` 。これは、メモリ使用量が無制限であり、等価結合条件によるハッシュ結合ではディスクへのスピルが使用されないことを意味します。

##### <code>enable_resource_control</code><span class="version-mark">バージョン7.4.0の新機能</span> {#code-enable-resource-control-code-span-class-version-mark-new-in-v7-4-0-span}

-   TiFlashリソース制御機能を有効にするかどうかを制御します。1 `true`設定すると、 TiFlashは[パイプライン実行モデル](/tiflash/tiflash-pipeline-model.md)を使用します。
-   デフォルト値: `true`
-   値`false`オプション: `true`

##### <code>task_scheduler_thread_soft_limit</code><span class="version-mark">バージョン6.0.0の新機能</span> {#code-task-scheduler-thread-soft-limit-code-span-class-version-mark-new-in-v6-0-0-span}

-   この項目はMinTSOスケジューラで使用されます。1つのリソースグループが使用できるスレッドの最大数を指定します。詳細については、 [TiFlash MinTSO スケジューラ](/tiflash/tiflash-mintso-scheduler.md)参照してください。
-   デフォルト値: `5000`

##### <code>task_scheduler_thread_hard_limit</code><span class="version-mark">バージョン6.0.0の新機能</span> {#code-task-scheduler-thread-hard-limit-code-span-class-version-mark-new-in-v6-0-0-span}

-   この項目はMinTSOスケジューラで使用されます。グローバルスコープ内のスレッドの最大数を指定します。詳細については、 [TiFlash MinTSO スケジューラ](/tiflash/tiflash-mintso-scheduler.md)参照してください。
-   デフォルト値: `10000`

##### <code>task_scheduler_active_set_soft_limit</code><span class="version-mark">バージョン6.4.0の新機能</span> {#code-task-scheduler-active-set-soft-limit-code-span-class-version-mark-new-in-v6-4-0-span}

-   この項目はMinTSOスケジューラに使用されます。TiFlashTiFlashで同時に実行できるクエリの最大数を指定します。詳細については、 [TiFlash MinTSO スケジューラ](/tiflash/tiflash-mintso-scheduler.md)参照してください。
-   デフォルト値: バージョン7.4.0より前のバージョンでは、デフォルト値は`vcpu * 0.25`で、これはvCPU数の4分の1を意味します。バージョン7.4.0以降では、デフォルト値は`vcpu * 2`で、これはvCPU数の2倍を意味します。

#### セキュリティ<span class="version-mark">v4.0.5 の新機能</span> {#security-span-class-version-mark-new-in-v4-0-5-span}

セキュリティ関連の設定を構成します。

##### <code>redact_info_log</code><span class="version-mark">バージョン5.0の新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v5-0-span}

-   ログ編集を有効にするかどうかを制御します。
-   デフォルト値: `false`
-   値のオプション: `true` 、 `false` 、 `"on"` 、 `"off"` 、および`"marker"` 。 `"on"` 、 `"off"` 、および`"marker"`オプションは、v8.2.0 で導入されました。
-   構成項目が`false`または`"off"`に設定されている場合、ログ編集は無効になります。
-   構成項目が`true`または`"on"`に設定されている場合、ログ内のすべてのユーザー データは`?`に置き換えられます。
-   設定項目を`"marker"`に設定すると、ログ内のすべてのユーザーデータは`‹ ›`で囲まれます。ユーザーデータに`‹`または`›`が含まれている場合、 `‹`は`‹‹`に、 `›`は`››`にエスケープされます。マークされたログに基づいて、ログを表示する際にマークされた情報を非感度化するかどうかを決定できます。
-   [`tiflash-learner.toml`](#configure-the-tiflash-learnertoml-file)での tiflash-learner のログインにも`security.redact-info-log`設定する必要があることに注意してください。

##### <code>ca_path</code> {#code-ca-path-code}

-   信頼できるSSL CAのリストを含むファイルのパス。設定する場合は、 [`cert_path`](#cert_path)と[`key_path`](#key_path)必要です。

<!-- Example: `"/path/to/ca.pem"` -->

##### <code>cert_path</code> {#code-cert-path-code}

-   PEM 形式の X509 証明書が含まれるファイルのパス。

<!-- Example: `"/path/to/tiflash-server.pem"` -->

##### <code>key_path</code> {#code-key-path-code}

-   PEM 形式の X509 キーを含むファイルのパス。

<!-- Example: `"/path/to/tiflash-server-key.pem"` -->

### <code>tiflash-learner.toml</code>ファイルを設定する {#configure-the-code-tiflash-learner-toml-code-file}

`tiflash-learner.toml`のパラメータは基本的にTiKVと同じです。TiFlashTiFlashの設定については[TiKV構成](/tikv-configuration-file.md)参照してください。以下はよく使用されるパラメータのみを示しています。ご注意ください。

-   TiKV と比較して、 TiFlash Proxy には[`raftstore.snap-handle-pool-size`](#snap-handle-pool-size-new-in-v400)追加パラメーターがあります。
-   キーが`engine`の`label`は予約されており、手動で設定することはできません。

#### ログ {#log}

##### <code>level</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-level-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiFlash Proxy のログ レベル。
-   デフォルト値: `"info"`
-   `"info"` `"debug"` `"error"` `"warn"` `"trace"`

#### ログファイル {#log-file}

##### <code>max-backups</code> <span class="version-mark">5.4.0の新機能</span> {#code-max-backups-code-span-class-version-mark-new-in-v5-4-0-span}

-   保存するログ ファイルの最大数。
-   このパラメータが設定されていないか、デフォルト値`0`に設定されている場合、 TiFlash Proxy はすべてのログ ファイルを保存します。
-   このパラメータを0以外の値に設定すると、 TiFlash Proxyは最大で`max-backups`で指定された数の古いログファイルを保持します。例えば、 `7`に設定すると、 TiFlash Proxyは最大で7つの古いログファイルを保持します。
-   デフォルト値: `0`

##### <code>max-days</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-max-days-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログ ファイルが保持される最大日数。
-   このパラメータが設定されていないか、デフォルト値`0`に設定されている場合、 TiFlash Proxy はすべてのログ ファイルを保持します。
-   このパラメータがゼロ以外の値に設定されている場合、 TiFlash Proxy は`max-days`で指定された日数後に古いログ ファイルをクリーンアップします。
-   デフォルト値: `0`

#### ラフトストア {#raftstore}

##### <code>apply-pool-size</code> {#code-apply-pool-size-code}

-   Raftデータをstorageにフラッシュするプール内の許容スレッド数。

<!-- Example: `4` -->

##### <code>store-pool-size</code> {#code-store-pool-size-code}

-   Raft を処理するスレッドの許容数。これはRaftstoreスレッド プールのサイズです。

<!-- Example: `4` -->

##### <code>snap-handle-pool-size</code> <span class="version-mark">v4.0.0 の新機能</span> {#code-snap-handle-pool-size-code-span-class-version-mark-new-in-v4-0-0-span}

-   スナップショットを処理するスレッドの数。1 `0`設定すると、マルチスレッド最適化は無効になります。
-   デフォルト値: `2`

#### 安全 {#security}

##### <code>redact-info-log</code><span class="version-mark">バージョン5.0の新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v5-0-span}

-   ログ編集を有効にするかどうかを制御します。
-   デフォルト値: `false`
-   値のオプション: `true` 、 `false` 、 `"on"` 、 `"off"` 、および`"marker"` 。 `"on"` 、 `"off"` 、および`"marker"`オプションは、v8.3.0 で導入されました。
-   構成項目が`false`または`"off"`に設定されている場合、ログ編集は無効になります。
-   構成項目が`true`または`"on"`に設定されている場合、ログ内のすべてのユーザー データは`?`に置き換えられます。
-   設定項目を`"marker"`に設定すると、ログ内のすべてのユーザーデータは`‹ ›`で囲まれます。ユーザーデータに`‹`または`›`が含まれている場合、 `‹`は`‹‹`に、 `›`は`››`にエスケープされます。マークされたログに基づいて、ログを表示する際にマークされた情報を非感度化するかどうかを決定できます。

#### セキュリティ.暗号化 {#security-encryption}

##### <code>data-encryption-method</code> {#code-data-encryption-method-code}

-   データファイルの暗号化方法。1以外の値は暗号化`"plaintext"`有効であることを意味します。その場合はマスターキーを指定する必要があります。
-   デフォルト値: `"plaintext"` 。これは、暗号化がデフォルトで無効になっていることを意味します。
-   `"aes256-ctr"` `"aes192-ctr"`オプション: `"aes128-ctr"` `"sm4-ctr"` `"plaintext"`で導入`"sm4-ctr"`れました。

##### <code>data-key-rotation-period</code> {#code-data-key-rotation-period-code}

-   データ暗号化キーをローテーションする頻度を指定します。
-   デフォルト値: `7d`

#### セキュリティ.暗号化.マスターキー {#security-encryption-master-key}

-   暗号化が有効になっている場合、マスターキーを指定します。マスターキーの設定方法については、 [暗号化を設定する](/encryption-at-rest.md#configure-encryption)参照してください。

#### セキュリティ.暗号化.以前のマスターキー {#security-encryption-previous-master-key}

-   新しいマスターキーをローテーションする際に使用する古いマスターキーを指定します。設定形式は`master-key`と同じです。マスターキーの設定方法については、 [暗号化を設定する](/encryption-at-rest.md#configure-encryption)参照してください。

#### サーバー {#server}

##### <code>labels</code> {#code-labels-code}

-   `{ zone = "us-west-1", disk = "ssd" }`などのサーバー属性を指定します。ラベルを使用してレプリカをスケジュールする方法の詳細については、 [利用可能なゾーンを設定する](/tiflash/create-tiflash-replicas.md#set-available-zones)参照してください。
-   デフォルト値: `{}`

### マルチディスク展開 {#multi-disk-deployment}

TiFlashはマルチディスク構成をサポートしています。TiFlashノードに複数のディスクがある場合、以下のセクションで説明するパラメータを設定することで、それらのディスクを最大限に活用できます。TiUPで使用するTiUPの設定テンプレートについては、 [TiFlashトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)参照してください。

v4.0.9以降のバージョンのTiDBクラスターでは、 TiFlashはstorageエンジンのメインデータと最新データを複数のディスクに保存することをサポートしています。TiFlashノードを複数のディスクにデプロイする場合は、ノードのI/Oパフォーマンスを最大限に活用するために、 `[storage]`セクションでstorageディレクトリを指定することをお勧めします。

TiFlashノード上に類似したI/Oメトリックを持つ複数のディスクがある場合は、リスト`storage.main.dir`で対応するディレクトリを指定し、リスト`storage.latest.dir`空のままにすることをお勧めします。TiFlashはI/O負荷とデータをすべてのディレクトリに分散します。

TiFlashノード上にI/Oメトリックが異なる複数のディスクがある場合は、 `storage.latest.dir`番目のリストにメトリックの高いディレクトリを指定し、 `storage.main.dir`番目のリストにメトリックの低いディレクトリを指定することをお勧めします。例えば、NVMe-SSDが1台とSATA-SSDが2台の場合、 `storage.latest.dir`を`["/nvme_ssd_a/data/tiflash"]`を`storage.main.dir` `["/sata_ssd_b/data/tiflash", "/sata_ssd_c/data/tiflash"]`設定します。TiFlashは、これらの2つのディレクトリリストにそれぞれI/O負荷とデータを分散します。この場合、 `storage.latest.dir`という容量は、計画容量全体の10%として計画する必要があることに注意してください。

> **警告：**
>
> `[storage]`設定はTiUP v1.2.5 以降でサポートされています。TiDB クラスタのバージョンが v4.0.9 以降の場合は、 TiUPのバージョンが v1.2.5 以降であることを確認してください。そうでない場合、 `[storage]`で定義されているデータディレクトリはTiUPによって管理されません。
