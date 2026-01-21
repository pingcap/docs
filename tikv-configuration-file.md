---
title: TiKV Configuration File
summary: TiKV 構成ファイルについて学習します。
---

# TiKVコンフィグレーションファイル {#tikv-configuration-file}

<!-- markdownlint-disable MD001 -->

TiKV設定ファイルは、コマンドラインパラメータよりも多くのオプションをサポートしています。デフォルトの設定ファイルは[etc/config-template.toml](https://github.com/tikv/tikv/blob/release-8.5/etc/config-template.toml)にあり、名前を`config.toml`に変更することができます。

このドキュメントでは、コマンドラインパラメータに含まれないパラメータについてのみ説明します。詳細については、 [コマンドラインパラメータ](/command-line-flags-for-tikv-configuration.md)参照してください。

> **ヒント：**
>
> 構成項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

## グローバル構成 {#global-configuration}

### <code>abort-on-panic</code> {#code-abort-on-panic-code}

-   TiKVパニック発生時にプロセスを終了するために`abort()`呼び出すかどうかを設定します。このオプションは、TiKVがシステムにコアダンプファイルの生成を許可するかどうかに影響します。

    -   この設定項目の値が`false`場合、TiKV がパニックになると、 `exit()`呼び出してプロセスを終了します。
    -   この設定項目の値が`true`場合、TiKV パニックが発生すると、TiKV は`abort()`呼び出してプロセスを終了します。このとき、TiKV はシステムが終了時にコア ダンプ ファイルを生成することを許可します。コア ダンプ ファイルを生成するには、コア ダンプに関連するシステム設定も実行する必要があります (たとえば、 `ulimit -c`コマンドでコア ダンプ ファイルのサイズ制限を設定し、コア ダンプのパスを設定します。オペレーティング システムによって関連設定は異なります)。コア ダンプ ファイルがディスク領域を過剰に占有し、TiKV ディスク領域が不足することを回避するために、コア ダンプの生成パスを TiKV データとは異なるディスク パーティションに設定することをお勧めします。

-   デフォルト値: `false`

### <code>slow-log-file</code> {#code-slow-log-file-code}

-   スローログを保存するファイル
-   この設定項目が設定されておらず、 `log.file.filename`設定されている場合、スローログは`log.file.filename`で指定されたログファイルに出力されます。
-   `slow-log-file`と`log.file.filename`どちらも設定されていない場合は、すべてのログがデフォルトで「stderr」に出力されます。
-   両方の設定項目が設定されている場合、通常ログは`log.file.filename`で指定したログファイルに出力され、スローログは`slow-log-file`で設定したログファイルに出力されます。
-   デフォルト値: `""`

### <code>slow-log-threshold</code> {#code-slow-log-threshold-code}

-   スローログを出力する閾値。処理時間がこの閾値よりも長い場合、スローログが出力されます。
-   デフォルト値: `"1s"`

### <code>memory-usage-limit</code> {#code-memory-usage-limit-code}

-   TiKVインスタンスのメモリ使用量の制限。TiKVのメモリ使用量がこのしきい値に近づくと、内部キャッシュが削除され、メモリが解放されます。
-   ほとんどの場合、TiKVインスタンスは利用可能なシステムメモリ全体の75%を使用するように設定されているため、この設定項目を明示的に指定する必要はありません。残りの25%のメモリはOSのページキャッシュ用に予約されています。詳細は[`storage.block-cache.capacity`](#capacity)ご覧ください。
-   単一の物理マシンに複数のTiKVノードをデプロイする場合でも、この設定項目を設定する必要はありません。この場合、TiKVインスタンスはメモリを`5/3 * block-cache.capacity`使用します。
-   さまざまなシステムメモリ容量の既定値は次のとおりです。

    -   システム=8G ブロックキャッシュ=3.6G メモリ使用量制限=6G ページキャッシュ=2G
    -   システム=16G ブロックキャッシュ=7.2G メモリ使用量制限=12G ページキャッシュ=4G
    -   システム=32G ブロックキャッシュ=14.4G メモリ使用量制限=24G ページキャッシュ=8G

## ログ<span class="version-mark">v5.4.0 の新機能</span> {#log-span-class-version-mark-new-in-v5-4-0-span}

-   ログに関するコンフィグレーション項目。

-   v5.4.0以降、TiKVとTiDBのログ設定項目の整合性を保つため、TiKVは以前の設定項目`log-rotation-timespan` `log-rotation-size`し、 `log-level` `log-file`以下の設定項目に変更しました。以前の設定項目のみを設定し、その値`log-format`デフォルト以外の値に設定した場合、以前の設定項目は新しい設定項目と互換性を保ちます。以前の設定項目と新しい設定項目の両方を設定した場合、新しい設定項目が有効になります。

### <code>level</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-level-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログレベル
-   `"fatal"` `"error"` `"warn"` `"debug"` `"info"`
-   デフォルト値: `"info"`

### <code>format</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-format-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログ形式
-   オプション`"text"` : `"json"`
-   デフォルト値: `"text"`

### <code>enable-timestamp</code> <span class="version-mark">v5.4.0 の新</span>機能 {#code-enable-timestamp-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログ内のタイムスタンプを有効にするか無効にするかを決定します
-   オプション`false` : `true`
-   デフォルト値: `true`

## log.file <span class="version-mark">v5.4.0 の新機能</span> {#log-file-span-class-version-mark-new-in-v5-4-0-span}

-   ログ ファイルに関連するコンフィグレーション項目。

### <code>filename</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-filename-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログファイル。この設定項目が設定されていない場合、ログはデフォルトで「stderr」に出力されます。この設定項目が設定されている場合、ログは対応するファイルに出力されます。
-   デフォルト値: `""`

### <code>max-size</code> <span class="version-mark">5.4.0の新機能</span> {#code-max-size-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログファイルの最大サイズ。ファイルサイズがこの設定項目で設定された値より大きい場合、システムは自動的に1つのファイルを複数のファイルに分割します。
-   デフォルト値: `300`
-   最大値: `4096`
-   単位: MiB

### <code>max-days</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-max-days-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKV がログ ファイルを保持する最大日数。
    -   構成項目が設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKV はログ ファイルを消去しません。
    -   パラメータが`0`以外の値に設定されている場合、TiKV は`max-days`後に期限切れのログ ファイルをクリーンアップします。
-   デフォルト値: `0`

### <code>max-backups</code> <span class="version-mark">5.4.0の新機能</span> {#code-max-backups-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKV が保持するログ ファイルの最大数。
    -   構成項目が設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKV はすべてのログ ファイルを保持します。
    -   設定項目が`0`以外の値に設定されている場合、TiKVは最大で`max-backups`で指定された数の古いログファイルを保持します。たとえば、値が`7`に設定されている場合、TiKVは最大で 7 個の古いログファイルを保持します。
-   デフォルト値: `0`

## サーバー {#server}

-   サーバーに関連するコンフィグレーション項目。

### <code>addr</code> {#code-addr-code}

-   リスニングIPアドレスとリスニングポート
-   デフォルト値: `"127.0.0.1:20160"`

### <code>advertise-addr</code> {#code-advertise-addr-code}

-   クライアント通信のリスニングアドレスをアドバタイズする
-   この構成項目が設定されていない場合は、値`addr`が使用されます。
-   デフォルト値: `""`

### <code>status-addr</code> {#code-status-addr-code}

-   構成項目は、 `HTTP`アドレスを通じてTiKVステータスを直接報告します。

    > **警告：**
    >
    > この値が公開されると、TiKVサーバーのステータス情報が漏洩する可能性があります。

-   ステータス アドレスを無効にするには、値を`""`に設定します。

-   デフォルト値: `"127.0.0.1:20180"`

### <code>status-thread-pool-size</code> {#code-status-thread-pool-size-code}

-   `HTTP` API サービスのワーカースレッドの数
-   デフォルト値: `1`
-   最小値: `1`

### <code>grpc-compression-type</code> {#code-grpc-compression-type-code}

-   gRPCメッセージの圧縮アルゴリズム。TiKVノード間のgRPCメッセージに影響します。v6.5.11、v7.1.6、v7.5.3、v8.1.1、v8.2.0以降では、TiKVからTiDBに送信されるgRPC応答メッセージにも影響します。

-   オプション`"deflate"` `"gzip"` `"none"`

    > **注記：**
    >
    > TiDBは`"deflate"`サポートしていません。そのため、TiKVからTiDBに送信されるgRPC応答メッセージを圧縮したい場合は、この設定項目を`"gzip"`に設定してください。

-   デフォルト値: `"none"`

### <code>grpc-concurrency</code> {#code-grpc-concurrency-code}

-   gRPCワーカースレッドの数。gRPCスレッドプールのサイズを変更する場合は、 [TiKV スレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。

-   デフォルト値:

    -   v8.5.4以降では、デフォルト値は[`grpc-raft-conn-num`](#grpc-raft-conn-num)の値に基づいて計算される`grpc-raft-conn-num * 3 + 2`に調整されます。例えば、CPUコア数が8の場合、デフォルト値`grpc-raft-conn-num`は 1 になります。したがって、デフォルト値`grpc-concurrency`は`1 * 3 + 2 = 5`になります。
    -   v8.5.3 以前のバージョンでは、デフォルト値は`5`です。

-   最小値: `1`

### <code>grpc-concurrent-stream</code> {#code-grpc-concurrent-stream-code}

-   gRPC ストリームで許可される同時リクエストの最大数
-   デフォルト値: `1024`
-   最小値: `1`

### <code>grpc-memory-pool-quota</code> {#code-grpc-memory-pool-quota-code}

-   gRPC で使用できるメモリサイズを制限します
-   デフォルト値: 制限なし
-   OOMが発生した場合に備えてメモリを制限してください。使用量を制限すると、潜在的なストールにつながる可能性があることに注意してください。

### <code>grpc-raft-conn-num</code> {#code-grpc-raft-conn-num-code}

-   Raft通信におけるTiKVノード間の最大接続数

-   デフォルト値:

    -   v8.5.4 以降では、デフォルト値は`MAX(1, MIN(4, CPU cores / 8))`に調整されます。3 `MIN(4, CPU cores / 8)` 、CPU コアの数が 32 以上の場合、デフォルトの最大接続数が 4 であることを示します。
    -   v8.5.3 以前のバージョンでは、デフォルト値は`1`です。

-   最小値: `1`

### <code>max-grpc-send-msg-len</code> {#code-max-grpc-send-msg-len-code}

-   送信できる gRPC メッセージの最大長を設定します
-   デフォルト値: `10485760`
-   単位: バイト
-   最大値: `2147483647`

### <code>grpc-stream-initial-window-size</code> {#code-grpc-stream-initial-window-size-code}

-   gRPC ストリームのウィンドウサイズ
-   デフォルト値: `2MiB`
-   単位: KiB|MiB|GiB
-   最小値: `"1KiB"`

### <code>grpc-keepalive-time</code> {#code-grpc-keepalive-time-code}

-   gRPCが`keepalive` Pingメッセージを送信する時間間隔
-   デフォルト値: `"10s"`
-   最小値: `"1s"`

### <code>grpc-keepalive-timeout</code> {#code-grpc-keepalive-timeout-code}

-   gRPC ストリームのタイムアウトを無効にします
-   デフォルト値: `"3s"`
-   最小値: `"1s"`

### <code>graceful-shutdown-timeout</code><span class="version-mark">バージョン8.5.5の新機能</span> {#code-graceful-shutdown-timeout-code-span-class-version-mark-new-in-v8-5-5-span}

-   TiKV 正常シャットダウンのタイムアウト期間を指定します。
    -   この値が`0s`より大きい場合、TiKV はシャットダウン前に、指定されたタイムアウト内にこのノード上のすべてのリーダーを他の TiKV ノードに転送しようとします。タイムアウトに達した時点でまだ転送されていないリーダーが残っている場合、TiKV は残りのリーダーの転送をスキップし、シャットダウンプロセスに直接進みます。
    -   この値が`0s`の場合、TiKV の正常なシャットダウンは無効になります。
-   デフォルト値: `"20s"`
-   最小値: `"0s"`

### <code>concurrent-send-snap-limit</code> {#code-concurrent-send-snap-limit-code}

-   同時に送信されるスナップショットの最大数
-   デフォルト値: `32`
-   最小値: `1`

### <code>concurrent-recv-snap-limit</code> {#code-concurrent-recv-snap-limit-code}

-   同時に受信できるスナップショットの最大数
-   デフォルト値: `32`
-   最小値: `1`

### <code>end-point-recursion-limit</code> {#code-end-point-recursion-limit-code}

-   TiKVがコプロセッサーDAG式をデコードするときに許可される再帰レベルの最大数
-   デフォルト値: `1000`
-   最小値: `1`

### <code>end-point-request-max-handle-duration</code> {#code-end-point-request-max-handle-duration-code}

-   タスク処理のために TiDB から TiKV へのプッシュダウン要求に許可される最長時間
-   デフォルト値: `"60s"`
-   最小値: `"1s"`

### <code>end-point-memory-quota</code> <span class="version-mark">v8.2.0 の新機能</span> {#code-end-point-memory-quota-code-span-class-version-mark-new-in-v8-2-0-span}

-   TiKVコプロセッサー要求が使用できるメモリの最大量。この制限を超えると、後続のコプロセッサー要求は「サーバーがビジーです」というエラーで拒否されます。
-   デフォルト値: システムメモリ全体の 12.5% と 500 MiB のいずれか大きい方の値。

### <code>snap-io-max-bytes-per-sec</code> {#code-snap-io-max-bytes-per-sec-code}

-   スナップショット処理時の最大許容ディスク帯域幅
-   デフォルト値: `"100MiB"`
-   単位: KiB|MiB|GiB
-   最小値: `"1KiB"`

### <code>snap-min-ingest-size</code> <span class="version-mark">v8.1.2 の新機能</span> {#code-snap-min-ingest-size-code-span-class-version-mark-new-in-v8-1-2-span}

-   TiKV がスナップショットを処理するときに取り込み方式を採用するかどうかの最小しきい値を指定します。

    -   スナップショットのサイズがこのしきい値を超えると、TiKVはスナップショットからSSTファイルをRocksDBにインポートするインジェスト方式を採用します。この方式は、大きなファイルの場合、より高速です。
    -   スナップショットのサイズがこのしきい値を超えない場合、TiKVは直接書き込み方式を採用し、各データをRocksDBに個別に書き込みます。この方式は、小さなファイルの場合により効率的です。

-   デフォルト値: `"2MiB"`

-   単位: KiB|MiB|GiB

-   最小値: `0`

### <code>enable-request-batch</code> {#code-enable-request-batch-code}

-   リクエストをバッチで処理するかどうかを決定します
-   デフォルト値: `true`

### <code>labels</code> {#code-labels-code}

-   `{ zone = "us-west-1", disk = "ssd" }`などのサーバー属性を指定します。
-   デフォルト値: `{}`

### <code>background-thread-count</code> {#code-background-thread-count-code}

-   エンドポイント スレッド、 BRスレッド、分割チェック スレッド、リージョンスレッド、および遅延に影響されないタスクのその他のスレッドを含む、バックグラウンド プールの作業スレッド数。
-   デフォルト値: CPU コアの数が 16 未満の場合、デフォルト値は`2`です。それ以外の場合、デフォルト値は`3`です。

### <code>end-point-slow-log-threshold</code> {#code-end-point-slow-log-threshold-code}

-   TiDBのプッシュダウンリクエストがスローログを出力するまでの時間閾値。処理時間がこの閾値を超えると、スローログが出力されます。
-   デフォルト値: `"1s"`
-   最小値: `0`

### <code>raft-client-queue-size</code> {#code-raft-client-queue-size-code}

-   TiKVにおけるRaftメッセージのキューサイズを指定します。時間内に送信されないメッセージが多すぎるとバッファがいっぱいになったり、メッセージが破棄されたりする場合は、システムの安定性を向上させるために、より大きな値を指定できます。
-   デフォルト値: `16384`

### <code>simplify-metrics</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-simplify-metrics-code-span-class-version-mark-new-in-v6-2-0-span}

-   返される監視メトリックを簡素化するかどうかを指定します。値を`true`に設定すると、TiKV は一部のメトリックを除外することで、各リクエストに対して返されるデータの量を削減します。
-   デフォルト値: `false`

### <code>forward-max-connections-per-address</code> <span class="version-mark">v5.0.0 の新機能</span> {#code-forward-max-connections-per-address-code-span-class-version-mark-new-in-v5-0-0-span}

-   サービスとサーバーへのリクエスト転送用の接続プールのサイズを設定します。値が小さすぎると、リクエストのレイテンシーと負荷分散に影響します。
-   デフォルト値: `4`

### <code>inspect-network-interval</code> <span class="version-mark">v8.5.5 の新機能</span> {#code-inspect-network-interval-code-span-class-version-mark-new-in-v8-5-5-span}

-   TiKVヘルスチェッカーがPDおよび他のTiKVノードに対してネットワーク検出をアクティブに実行する間隔を制御します。TiKVはネットワーク検出結果に基づいて`NetworkSlowScore`を計算し、低速ノードのネットワーク状態をPDに報告します。
-   この値を`0`に設定すると、ネットワーク検出が無効になります。値を小さくすると検出頻度が上がり、ネットワークジッターをより迅速に検出できるようになりますが、ネットワーク帯域幅とCPUリソースの消費量も増加します。
-   デフォルト値: `100ms`
-   値の範囲: `0`または`[10ms, +∞)`

## 読み取りプール.統合 {#readpool-unified}

読み取りリクエストを処理する単一スレッドプールに関連するコンフィグレーション項目。このスレッドプールは、バージョン4.0以降、従来のstorageスレッドプールとコプロセッサスレッドプールに代わるものです。

### <code>min-thread-count</code> {#code-min-thread-count-code}

-   統合読み取りプールの最小作業スレッド数
-   デフォルト値: `1`

### <code>max-thread-count</code> {#code-max-thread-count-code}

-   統合読み取りプールまたはUnifyReadPoolスレッドプールの最大作業スレッド数。このスレッドプールのサイズを変更する場合は、 [TiKV スレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   値の範囲: `[min-thread-count, MAX(4, CPU quota * 10)]` 。 `MAX(4, CPU quota * 10)` `4`と`CPU quota * 10`のうち大きい方の値を取得します。
-   デフォルト値: MAX(4, CPU * 0.8)

> **注記：**
>
> スレッド数を増やすとコンテキストスイッチが増加し、パフォーマンスが低下する可能性があります。この設定項目の値を変更することは推奨されません。

### <code>stack-size</code> {#code-stack-size-code}

-   統合スレッドプール内のスレッドのスタックサイズ
-   タイプ: 整数 + 単位
-   デフォルト値: `"10MiB"`
-   単位: KiB|MiB|GiB
-   最小値: `"2MiB"`
-   最大値: システムで実行された`ulimit -sH`コマンドの結果出力される K バイト数。

### <code>max-tasks-per-worker</code> {#code-max-tasks-per-worker-code}

-   統合読み取りプール内の 1 つのスレッドに許可されるタスクの最大数。値を超えると`Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>auto-adjust-pool-size</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-auto-adjust-pool-size-code-span-class-version-mark-new-in-v6-3-0-span}

-   スレッドプールサイズを自動調整するかどうかを制御します。有効にすると、現在のCPU使用率に基づいてUnifyReadPoolスレッドプールサイズを自動調整することで、TiKVの読み取りパフォーマンスが最適化されます。スレッドプールの指定可能な範囲は`[max-thread-count, MAX(4, CPU)]`です。最大値は[`max-thread-count`](#max-thread-count)と同じです。
-   デフォルト値: `false`

### <code>cpu-threshold</code> <span class="version-mark">v8.5.5 の新機能</span> {#code-cpu-threshold-code-span-class-version-mark-new-in-v8-5-5-span}

-   統合読み取りプールのCPU使用率のしきい値を指定します。たとえば、この値を`0.8`に設定すると、スレッドプールはCPUの最大80%を使用できます。

    -   デフォルト（ `0.0`の場合）では、統合読み取りプールのCPU使用量に制限はありません。スレッドプールのサイズは、ビジースレッドスケーリングアルゴリズムによってのみ決定され、現在のタスクを処理しているスレッドの数に基づいて動的にサイズが調整されます。
    -   `0.0`より大きい値に設定すると、TiKV は既存のビジースレッド スケーリング アルゴリズムに加えて次の CPU 使用率しきい値制約を適用し、CPU リソースの使用率をより厳密に制御します。
        -   強制スケールダウン: 統合読み取りプールの CPU 使用率が構成された値に 10% のバッファを加えた値を超えると、TiKV はプールのサイズを強制的に縮小します。
        -   スケールアップ防止: 統合読み取りプールを拡張すると、CPU 使用率が構成されたしきい値から 10% のバッファを差し引いた値を超える場合、TiKV は統合読み取りプールのそれ以上の拡張を防止します。

-   この機能は、 [`readpool.unified.auto-adjust-pool-size`](#auto-adjust-pool-size-new-in-v630) `true`に設定されている場合にのみ有効になります。

-   デフォルト値: `0.0`

-   値の範囲: `[0.0, 1.0]`

## 読み取りプール。storage {#readpool-storage}

storageスレッド プールに関連するコンフィグレーション項目。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   storageリクエストに統合スレッドプール（ [`readpool.unified`](#readpoolunified)で設定）を使用するかどうかを決定します。このパラメータの値が`false`場合、このセクションの残りのパラメータ（ `readpool.storage` ）で設定された別のスレッドプールが使用されます。
-   デフォルト値: このセクション( `readpool.storage` )に他の設定がない場合、デフォルト値は`true`です。それ以外の場合は、下位互換性のため、デフォルト値は`false`です。このオプションを有効にする前に、必要に応じて[`readpool.unified`](#readpoolunified)の設定を変更してください。

### <code>high-concurrency</code> {#code-high-concurrency-code}

-   高優先度`read`リクエストを処理する同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。9 `8` `cpu num`場合、デフォルト値は`4`です。15 `cpu num` `16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>normal-concurrency</code> {#code-normal-concurrency-code}

-   通常優先度`read`リクエストを処理できる同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。9 `8` `cpu num`場合、デフォルト値は`4`です。15 `cpu num` `16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>low-concurrency</code> {#code-low-concurrency-code}

-   低優先度`read`リクエストを処理する同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。9 `8` `cpu num`場合、デフォルト値は`4`です。15 `cpu num` `16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>max-tasks-per-worker-high</code> {#code-max-tasks-per-worker-high-code}

-   高優先度スレッド プール内の 1 つのスレッドに許可されるタスクの最大数。値を超えると`Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-normal</code> {#code-max-tasks-per-worker-normal-code}

-   通常優先度のスレッド プール内の 1 つのスレッドに許可されるタスクの最大数。値を超えると`Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-low</code> {#code-max-tasks-per-worker-low-code}

-   低優先度スレッド プール内の 1 つのスレッドに許可されるタスクの最大数。値を超えると`Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>stack-size</code> {#code-stack-size-code}

-   ストレージ読み取りスレッドプール内のスレッドのスタックサイズ
-   タイプ: 整数 + 単位
-   デフォルト値: `"10MiB"`
-   単位: KiB|MiB|GiB
-   最小値: `"2MiB"`
-   最大値: システムで実行された`ulimit -sH`コマンドの結果出力される K バイト数。

## <code>readpool.coprocessor</code> {#code-readpool-coprocessor-code}

コプロセッサースレッド プールに関連するコンフィグレーション項目。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   コプロセッサリクエストに統合スレッドプール（ [`readpool.unified`](#readpoolunified)で設定）を使用するかどうかを決定します。このパラメータの値が`false`の場合、このセクションの残りのパラメータ（ `readpool.coprocessor` ）で設定された別のスレッドプールが使用されます。
-   デフォルト値: このセクション( `readpool.coprocessor` )のパラメータがいずれも設定されていない場合、デフォルト値は`true`です。それ以外の場合は、下位互換性のためデフォルト値は`false`です。このパラメータを有効にする前に、 [`readpool.unified`](#readpoolunified)の設定項目を調整してください。

### <code>high-concurrency</code> {#code-high-concurrency-code}

-   チェックポイントなどの高優先度コプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>normal-concurrency</code> {#code-normal-concurrency-code}

-   通常優先度のコプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>low-concurrency</code> {#code-low-concurrency-code}

-   テーブルスキャンなどの低優先度コプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>max-tasks-per-worker-high</code> {#code-max-tasks-per-worker-high-code}

-   高優先度スレッドプール内の1つのスレッドに許可されるタスク数。この数を超えると、 `Server Is Busy`返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-normal</code> {#code-max-tasks-per-worker-normal-code}

-   通常優先度のスレッドプール内の1つのスレッドに許可されるタスク数。この数を超えると、 `Server Is Busy`返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-low</code> {#code-max-tasks-per-worker-low-code}

-   低優先度スレッドプール内の1つのスレッドに許可されるタスク数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>stack-size</code> {#code-stack-size-code}

-   コプロセッサースレッドプール内のスレッドのスタックサイズ
-   タイプ: 整数 + 単位
-   デフォルト値: `"10MiB"`
-   単位: KiB|MiB|GiB
-   最小値: `"2MiB"`
-   最大値: システムで実行された`ulimit -sH`コマンドの結果出力される K バイト数。

## storage {#storage}

storageに関するコンフィグレーション項目。

### <code>data-dir</code> {#code-data-dir-code}

-   RocksDBディレクトリのstorageパス
-   デフォルト値: `"./"`

### <code>engine</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-engine-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   エンジンの種類を指定します。この設定は新しいクラスターを作成するときにのみ指定でき、一度指定した後は変更できません。
-   デフォルト値: `"raft-kv"`
-   値のオプション:

    -   `"raft-kv"` : TiDB v6.6.0 より前のバージョンのデフォルトのエンジン タイプ。
    -   `"partitioned-raft-kv"` : TiDB v6.6.0 で導入された新しいstorageエンジン タイプ。

### <code>scheduler-concurrency</code> {#code-scheduler-concurrency-code}

-   メモリロック機構を内蔵し、キーの同時操作を防止します。各キーには異なるスロットにハッシュが保存されています。
-   デフォルト値: `524288`
-   最小値: `1`

### <code>scheduler-worker-pool-size</code> {#code-scheduler-worker-pool-size-code}

-   スケジューラスレッドプール内のスレッド数。スケジューラスレッドは主に、データ書き込み前のトランザクションの整合性チェックに使用されます。CPUコア数が`16`以上の場合、デフォルト値は`8`です。それ以外の場合、デフォルト値は`4`です。スケジューラスレッドプールのサイズを変更する場合は、 [TiKV スレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `4`
-   値の範囲: `[1, MAX(4, CPU)]` 。 `MAX(4, CPU)`の場合、 `CPU` CPU コアの数を意味します。 `MAX(4, CPU)` `4`と`CPU`のうち大きい方の値になります。

### <code>scheduler-pending-write-threshold</code> {#code-scheduler-pending-write-threshold-code}

-   書き込みキューの最大サイズ。この値を超えると、TiKVへの新しい書き込みに対して`Server Is Busy`エラーが返されます。
-   デフォルト値: `"100MiB"`
-   単位: MiB|GiB

### <code>enable-async-apply-prewrite</code> {#code-enable-async-apply-prewrite-code}

-   非同期コミットトランザクションが、事前書き込みリクエストを適用する前にTiKVクライアントに応答するかどうかを決定します。この設定項目を有効にすると、適用期間が長い場合にレイテンシーを簡単に短縮したり、適用期間が安定していない場合に遅延ジッターを削減したりできます。
-   デフォルト値: `false`

### <code>reserve-space</code> {#code-reserve-space-code}

-   TiKVを起動すると、ディスク保護のためディスク上に一定のスペースが予約されます。ディスク残量が予約済みスペースを下回ると、TiKVは一部の書き込み操作を制限します。予約済みスペースは2つの部分に分かれており、予約済みスペースの80%はディスク容量不足時の操作に必要な追加ディスクスペースとして使用され、残りの20%は一時ファイルの保存に使用されます。スペース回収プロセスにおいて、余分なディスク容量の使用によりstorageが枯渇した場合、この一時ファイルはサービスを復旧するための最後の保護として機能します。
-   一時ファイルの名前は`space_placeholder_file`で、ディレクトリ`storage.data-dir`にあります。TiKV のディスク容量が不足してオフラインになった場合、TiKV を再起動すると、一時ファイルは自動的に削除され、TiKV は空き容量の確保を試みます。
-   残り容量が不足している場合、TiKVは一時ファイルを作成しません。保護の有効性は、確保された領域のサイズに依存します。確保された領域のサイズは、ディスク容量の5%とこの設定値のいずれか大きい方の値になります。この設定項目の値が`"0MiB"`の場合、TiKVはこのディスク保護機能を無効にします。
-   デフォルト値: `"5GiB"`
-   単位: MiB|GiB

### <code>enable-ttl</code> {#code-enable-ttl-code}

> **警告：**
>
> -   新しいTiKVクラスターをデプロイする**場合のみ、** `enable-ttl` ～ `true`または`false`に設定してください。既存のTiKVクラスターでこの設定項目の値を変更**しないでください**。異なる`enable-ttl`の値を持つTiKVクラスターは、異なるデータ形式を使用します。そのため、既存のTiKVクラスターでこの項目の値を変更すると、クラスターは異なる形式でデータを保存するため、TiKVクラスターの再起動時に「非TTLでTTLを有効にできません」というエラーが発生します。
> -   `enable-ttl` TiKVクラスタ**でのみ**使用してください。TiDBノードを含むクラスタ（つまり、そのようなクラスタでは`enable-ttl` ～ `true`を設定）では、 `storage.api-version = 2`が設定されていない限り、この設定項目を使用**しないで**ください。そうでない場合、データ破損やTiDBクラスタのアップグレード失敗などの重大な問題が発生します。

-   [TTL](/time-to-live.md)は「Time to live（存続時間）」の略です。この項目を有効にすると、TiKVはTTLに達したデータを自動的に削除します。TTLの値を設定するには、クライアント経由でデータを書き込む際にリクエストでTTLを指定する必要があります。TTLが指定されていない場合、TiKVは対応するデータを自動的に削除しません。
-   デフォルト値: `false`

### <code>ttl-check-poll-interval</code> {#code-ttl-check-poll-interval-code}

-   物理スペースを回収するためにデータをチェックする間隔。データがTTLに達した場合、TiKVはチェック中に物理スペースを強制的に回収します。
-   デフォルト値: `"12h"`
-   最小値: `"0s"`

### <code>background-error-recovery-window</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-background-error-recovery-window-code-span-class-version-mark-new-in-v6-1-0-span}

-   RocksDBが回復可能なバックグラウンドエラーを検出した後、TiKVが回復するまでの最大許容時間です。バックグラウンドSSTファイルが破損している場合、RocksDBは破損したSSTファイルが属するピアを特定した後、ハートビートを介してPDに報告します。PDは、このピアを削除するためのスケジュール操作を実行します。最終的に、破損したSSTファイルは直接削除され、TiKVのバックグラウンドは再び正常に動作します。
-   破損したSSTファイルは、リカバリが完了するまでまだ存在します。その間、RocksDBはデータの書き込みを継続できますが、破損した部分のデータを読み取るとエラーが報告されます。
-   この時間枠内にリカバリが完了しない場合、TiKV はpanicに陥ります。
-   デフォルト値: 1時間

### <code>api-version</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-api-version-code-span-class-version-mark-new-in-v6-1-0-span}

-   TiKV が RawKV ストアとして機能する場合に TiKV によって使用されるstorage形式とインターフェース バージョン。
-   値のオプション:
    -   `1` : API V1を使用し、クライアントから渡されたデータをエンコードせずにそのまま保存します。v6.1.0より前のバージョンでは、TiKVはデフォルトでAPI V1を使用します。
    -   `2` : API V2 を使用します:
        -   データは[マルチバージョン同時実行制御 (MVCC)](/glossary.md#multi-version-concurrency-control-mvcc)形式で保存され、タイムスタンプは tikv-server によって PD (TSO) から取得されます。
        -   データはさまざまな使用方法に応じてスコープが設定され、API V2 は単一クラスター内での TiDB、トランザクション KV、および RawKV アプリケーションの共存をサポートします。
        -   API V2を使用する場合は、同時に`storage.enable-ttl = true`設定する必要があります。API V2はTTL機能をサポートしているため、 [`enable-ttl`](#enable-ttl)明示的にオンにする必要があります。そうしないと、 `storage.enable-ttl`デフォルトで`false`になるため、競合が発生します。
        -   API V2 を有効にすると、古いデータを再利用するために少なくとも 1 つの tidb-server インスタンスをデプロイする必要があります。この tidb-server インスタンスは、読み取りと書き込みのサービスを同時に提供できます。高可用性を確保するため、複数の tidb-server インスタンスをデプロイできます。
        -   API V2にはクライアントのサポートが必要です。詳細については、API V2のクライアントの対応するマニュアルを参照してください。
        -   v6.2.0以降、RawKVの変更データキャプチャ（CDC）がサポートされました[生のKV CDC](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc)を参照してください。
-   デフォルト値: `1`

> **警告：**

> -   API V1とAPI V2はstorage形式が異なります。TiKVにTiDBデータのみが含まれている場合**のみ**、API V2を直接有効化または無効化できます。それ以外の場合は、新しいクラスターをデプロイし、 [RawKV バックアップと復元](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)を使用してデータを移行する必要があります。
> -   API V2 を有効にした後は、TiKV クラスターを v6.1.0 より前のバージョンにダウングレードする**ことはできません**。ダウングレードすると、データ破損が発生する可能性があります。

## <code>txn-status-cache-capacity</code> <span class="version-mark">v7.6.0 の新</span>機能 {#code-txn-status-cache-capacity-code-span-class-version-mark-new-in-v7-6-0-span}

-   TiKVのトランザクションステータスキャッシュの容量を設定します。このパラメータは変更しないでください。
-   デフォルト値: `5120000`

## storage.block-cache {#storage-block-cache}

複数の RocksDBカラムファミリ (CF) 間でのブロックキャッシュの共有に関連するコンフィグレーション項目。

### <code>capacity</code> {#code-capacity-code}

-   共有ブロックキャッシュのサイズ。

-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値はシステムメモリの合計サイズの 45% になります。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値はシステムメモリの合計サイズの 30% になります。

-   単位: KiB|MiB|GiB

### <code>low-pri-pool-ratio</code> <span class="version-mark">v8.0.0 の新機能</span> {#code-low-pri-pool-ratio-code-span-class-version-mark-new-in-v8-0-0-span}

-   Titanコンポーネントが使用できるブロックキャッシュ全体の割合を制御します。
-   デフォルト値: `0.2`

## storage.フロー制御 {#storage-flow-control}

TiKVのフロー制御メカニズムに関するコンフィグレーション項目。このメカニズムはRocksDBの書き込みストールメカニズムに代わるもので、スケジューラレイヤーでフローを制御することで、 RaftstoreまたはApplyスレッドのスタックによる二次災害を回避します。

### <code>enable</code> {#code-enable-code}

-   フロー制御メカニズムを有効にするかどうかを決定します。有効にすると、TiKVはKvDBの書き込みストールメカニズムとRaftDB（memtableを除く）の書き込みストールメカニズムを自動的に無効にします。
-   デフォルト値: `true`

### <code>memtables-threshold</code> {#code-memtables-threshold-code}

-   kvDB memtableの数がこのしきい値に達すると、フロー制御メカニズムが動作を開始します。1 `enable` `true`に設定すると、この設定項目は`rocksdb.(defaultcf|writecf|lockcf).max-write-buffer-number`オーバーライドします。
-   デフォルト値: `5`

### <code>l0-files-threshold</code> {#code-l0-files-threshold-code}

-   kvDB L0 ファイルの数がこのしきい値に達すると、フロー制御メカニズムが動作を開始します。

    > **注記：**
    >
    > 特定の条件下では、この設定項目は`rocksdb.(defaultcf|writecf|lockcf|raftcf).level0-slowdown-writes-trigger`の値を上書きできます。詳細については[`rocksdb.(defaultcf|writecf|lockcf|raftcf).level0-slowdown-writes-trigger`](/tikv-configuration-file.md#level0-slowdown-writes-trigger)参照してください。

-   デフォルト値: `20`

### <code>soft-pending-compaction-bytes-limit</code> {#code-soft-pending-compaction-bytes-limit-code}

-   KvDB 内の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムは一部の書き込み要求を拒否し始め、エラー`ServerIsBusy`を報告します。

    > **注記：**
    >
    > 特定の条件下では、この設定項目は`rocksdb.(defaultcf|writecf|lockcf|raftcf).soft-pending-compaction-bytes-limit`の値を上書きできます。詳細については[`rocksdb.(defaultcf|writecf|lockcf|raftcf).soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit-1)参照してください。

-   デフォルト値: `"192GiB"`

### <code>hard-pending-compaction-bytes-limit</code> {#code-hard-pending-compaction-bytes-limit-code}

-   KvDB内の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し、 `ServerIsBusy`エラーを報告します。3 `enable` `true`に設定すると、この設定項目は`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`オーバーライドします。
-   デフォルト値: `"1024GiB"`

## storage.io レート制限 {#storage-io-rate-limit}

I/O レート リミッターに関連するコンフィグレーション項目。

### <code>max-bytes-per-sec</code> {#code-max-bytes-per-sec-code}

-   サーバーがディスクに1秒間に書き込む、またはディスクから読み取ることができる最大I/Oバイト数を制限します（以下の`mode`の設定項目によって決定されます）。この制限に達すると、TiKVはフォアグラウンド操作よりもバックグラウンド操作のスロットリングを優先します。この設定項目の値は、ディスクの最適なI/O帯域幅（例えば、クラウドディスクベンダーが指定する最大I/O帯域幅）に設定する必要があります。この設定値を0に設定すると、ディスクI/O操作は制限されません。
-   デフォルト値: `"0MiB"`

### <code>mode</code> {#code-mode-code}

-   どのタイプのI/O操作をカウントし、しきい値`max-bytes-per-sec`未満に制限するかを決定します。現在、書き込み専用モードのみがサポートされています。
-   `"all-io"` `"write-only"`オプション: `"read-only"`
-   デフォルト値: `"write-only"`

## pd {#pd}

### <code>enable-forwarding</code> <span class="version-mark">v5.0.0 の新機能</span> {#code-enable-forwarding-code-span-class-version-mark-new-in-v5-0-0-span}

-   ネットワーク分離の可能性がある場合に、TiKV の PD クライアントがフォロワー経由でリーダーにリクエストを転送するかどうかを制御します。
-   デフォルト値: `false`
-   環境に分離されたネットワークが存在する可能性がある場合は、このパラメータを有効にすると、サービスが利用できない期間を短縮できます。
-   分離、ネットワーク中断、またはダウンタイムが発生したかどうかを正確に判断できない場合、このメカニズムを使用すると誤判断のリスクがあり、可用性とパフォーマンスの低下につながります。ネットワーク障害が発生していない場合は、このパラメータを有効にすることは推奨されません。

### <code>endpoints</code> {#code-endpoints-code}

-   PDのエンドポイント。複数のエンドポイントを指定する場合は、カンマで区切る必要があります。
-   デフォルト値: `["127.0.0.1:2379"]`

### <code>retry-interval</code> {#code-retry-interval-code}

-   PD 接続を再試行する間隔。
-   デフォルト値: `"300ms"`

### <code>retry-log-every</code> {#code-retry-log-every-code}

-   PDクライアントがエラーを検知した際にエラー報告をスキップする頻度を指定します。例えば、値が`5`の場合、PDクライアントはエラーを検知した後、4回ごとにエラー報告をスキップし、5回ごとにエラーを報告します。
-   この機能を無効にするには、値を`1`に設定します。
-   デフォルト値: `10`

### <code>retry-max-count</code> {#code-retry-max-count-code}

-   PD接続の初期化を再試行する最大回数
-   再試行を無効にするには、値を`0`に設定します。再試行回数の制限を解除するには、値を`-1`に設定します。
-   デフォルト値: `-1`

## ラフトストア {#raftstore}

Raftstoreに関連するコンフィグレーション項目。

### <code>prevote</code> {#code-prevote-code}

-   `prevote`を有効または無効にします。この機能を有効にすると、ネットワークパーティションからの回復後にシステムのジッターが軽減されます。
-   デフォルト値: `true`

### <code>capacity</code> {#code-capacity-code}

-   storage容量。これは、データを保存できる最大サイズです。1 `capacity`指定しない場合は、現在のディスクの容量が優先されます。同じ物理ディスクに複数のTiKVインスタンスをデプロイするには、このパラメータをTiKV設定に追加します。詳細については、 [ハイブリッド展開の主なパラメータ](/hybrid-deployment-topology.md#key-parameters)参照してください。
-   デフォルト値: `0`
-   単位: KiB|MiB|GiB

### <code>raftdb-path</code> {#code-raftdb-path-code}

-   Raftライブラリへのパス（デフォルトでは`storage.data-dir/raft`
-   デフォルト値: `""`

### <code>raft-base-tick-interval</code> {#code-raft-base-tick-interval-code}

> **注記：**
>
> この構成項目は SQL ステートメントで照会することはできませんが、構成ファイルで構成できます。

-   Raftステートマシンが刻む時間間隔
-   デフォルト値: `"1s"`
-   最小値: `0`より大きい

### <code>raft-heartbeat-ticks</code> {#code-raft-heartbeat-ticks-code}

> **注記：**
>
> この構成項目は SQL ステートメントで照会することはできませんが、構成ファイルで構成できます。

-   ハートビート送信時に経過したティック数。これは、ハートビートが`raft-base-tick-interval` * `raft-heartbeat-ticks`の時間間隔で送信されることを意味します。
-   デフォルト値: `2`
-   最小値: `0`より大きい

### <code>raft-election-timeout-ticks</code> {#code-raft-election-timeout-ticks-code}

> **注記：**
>
> この構成項目は SQL ステートメントで照会することはできませんが、構成ファイルで構成できます。

-   Raft選出が開始されるまでに経過したティック数。これは、 Raftグループにリーダーがいない場合、約`raft-base-tick-interval` * `raft-election-timeout-ticks`の時間間隔後にリーダー選出が開始されることを意味します。
-   デフォルト値: `10`
-   最小値: `raft-heartbeat-ticks`

### <code>raft-min-election-timeout-ticks</code> {#code-raft-min-election-timeout-ticks-code}

> **注記：**
>
> この構成項目は SQL ステートメントで照会することはできませんが、構成ファイルで構成できます。

-   Raft選出が開始される最小ティック数。値が`0`の場合、値`raft-election-timeout-ticks`が使用されます。このパラメータの値は`raft-election-timeout-ticks`以上である必要があります。
-   デフォルト値: `0`
-   最小値: `0`

### <code>raft-max-election-timeout-ticks</code> {#code-raft-max-election-timeout-ticks-code}

> **注記：**
>
> この構成項目は SQL ステートメントで照会することはできませんが、構成ファイルで構成できます。

-   Raft選出が開始される最大ティック数。この数値が`0`の場合、 `raft-election-timeout-ticks` * `2`の値が使用されます。
-   デフォルト値: `0`
-   最小値: `0`

### <code>raft-max-size-per-msg</code> {#code-raft-max-size-per-msg-code}

-   単一メッセージパケットのサイズに対するソフト制限
-   デフォルト値: `"1MiB"`
-   最小値: `0`より大きい
-   最大値: `3GiB`
-   単位: KiB|MiB|GiB

### <code>raft-max-inflight-msgs</code> {#code-raft-max-inflight-msgs-code}

-   確認するRaftログの数。この数を超えると、 Raftステートマシンはログの送信速度を低下させます。
-   デフォルト値: `256`
-   最小値: `0`より大きい
-   最大値: `16384`

### <code>raft-entry-max-size</code> {#code-raft-entry-max-size-code}

-   単一ログの最大サイズに対するハード制限
-   デフォルト値: `"8MiB"`
-   最小値: `0`
-   単位: MiB|GiB

### <code>raft-log-compact-sync-interval</code><span class="version-mark">バージョン5.3の新機能</span> {#code-raft-log-compact-sync-interval-code-span-class-version-mark-new-in-v5-3-span}

-   不要なRaftログを圧縮する時間間隔
-   デフォルト値: `"2s"`
-   最小値: `"0s"`

### <code>raft-log-gc-tick-interval</code> {#code-raft-log-gc-tick-interval-code}

-   Raftログを削除するポーリング タスクがスケジュールされる時間間隔。1 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"3s"`
-   最小値: `"0s"`

### <code>raft-log-gc-threshold</code> {#code-raft-log-gc-threshold-code}

-   残存Raftログの最大許容数に関するソフト制限
-   デフォルト値: `50`
-   最小値: `1`

### <code>raft-log-gc-count-limit</code> {#code-raft-log-gc-count-limit-code}

-   許容される残存Raftログ数のハードリミット
-   デフォルト値: 各ログが 1 KiB であると仮定して計算された、リージョンサイズの 4 分の 3 に収まるログの数
-   最小値: `0`

### <code>raft-log-gc-size-limit</code> {#code-raft-log-gc-size-limit-code}

-   残余Raftの許容サイズに関する厳密な制限
-   デフォルト値:リージョンサイズの3/4
-   最小値: `0`より大きい

### <code>raft-log-reserve-max-ticks</code><span class="version-mark">バージョン5.3の新機能</span> {#code-raft-log-reserve-max-ticks-code-span-class-version-mark-new-in-v5-3-span}

-   この設定項目で設定されたティック数が経過した後、残りのRaftログの数が`raft-log-gc-threshold`で設定された値に達していなくても、TiKV はこれらのログに対してガベージコレクション(GC) を実行します。
-   デフォルト値: `6`
-   最小値: `0`より大きい

### <code>raft-engine-purge-interval</code> {#code-raft-engine-purge-interval-code}

-   ディスク容量をできるだけ早く再利用するために、古いTiKVログファイルをパージする間隔。RaftRaftは交換可能なコンポーネントであるため、一部の実装ではパージ処理が必要になります。
-   デフォルト値: `"10s"`

### <code>raft-entry-cache-life-time</code> {#code-raft-entry-cache-life-time-code}

-   メモリ内のログキャッシュに許容される最大残り時間
-   デフォルト値: `"30s"`
-   最小値: `0`

### <code>max-apply-unpersisted-log-limit</code><span class="version-mark">バージョン8.1.0の新機能</span> {#code-max-apply-unpersisted-log-limit-code-span-class-version-mark-new-in-v8-1-0-span}

-   適用できるコミット済みだが永続化されていないRaftログの最大数。

    -   この設定項目を`0`より大きい値に設定すると、TiKVノードはコミット済みだが永続化されていないRaftログを事前に適用できるようになり、そのノードにおけるIOジッターによるロングテールレイテンシーを効果的に削減します。ただし、TiKVのメモリ使用量とRaftログが占有するディスク容量が増加する可能性があります。
    -   この設定項目を`0`に設定すると、この機能は無効になります。つまり、TiKVはRaftログがコミットされ、永続化されるまで待機してから、ログを適用する必要があります。この動作は、v8.2.0より前の動作と一致しています。

-   デフォルト値: `1024`

-   最小値: `0`

### <code>hibernate-regions</code> {#code-hibernate-regions-code}

-   リージョンの休止リージョンを有効または無効にします。このオプションを有効にすると、長時間アイドル状態になっているリージョンは自動的に休止状態に設定されます。これにより、アイドル状態のリージョンにおけるRaftリーダーとフォロワー間のハートビートメッセージによって発生する余分なオーバーヘッドが軽減されます。1 `peer-stale-state-check-interval`指定すると、休止状態のリージョンにおけるリーダーとフォロワー間のハートビート間隔を変更できます。
-   デフォルト値: v5.0.2 以降では`true` 、v5.0.2 より前のバージョンでは`false`

### <code>split-region-check-tick-interval</code> {#code-split-region-check-tick-interval-code}

-   リージョン分割が必要かどうかを確認する間隔を指定します。1 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"10s"`
-   最小値: `0`

### <code>region-split-check-diff</code> {#code-region-split-check-diff-code}

-   リージョン分割前にリージョンデータが超過できる最大値
-   デフォルト値:リージョンサイズの 1/16。
-   最小値: `0`

### <code>region-compact-check-interval</code> {#code-region-compact-check-interval-code}

> **警告：**
>
> v7.5.7 および v8.5.4 以降では、この構成項目は非推奨となり、 [`gc.auto-compaction.check-interval`](#check-interval-new-in-v757-and-v854)に置き換えられました。

-   RocksDB 圧縮を手動でトリガーする必要があるかどうかを確認する時間間隔。1 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"5m"`
-   最小値: `0`

### <code>region-compact-check-step</code> {#code-region-compact-check-step-code}

> **警告：**
>
> v7.5.7 および v8.5.4 以降では、この構成項目は非推奨です。

-   手動圧縮の各ラウンドで一度にチェックされる領域の数
-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値は`100`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`5`です。
-   最小値: `0`

### <code>region-compact-min-tombstones</code> {#code-region-compact-min-tombstones-code}

> **警告：**
>
> v7.5.7 および v8.5.4 以降では、この構成項目は非推奨となり、 [`gc.auto-compaction.tombstone-num-threshold`](#tombstone-num-threshold-new-in-v757-and-v854)に置き換えられました。

-   RocksDBの圧縮をトリガーするために必要な墓石の数
-   デフォルト値: `10000`
-   最小値: `0`

### <code>region-compact-tombstones-percent</code> {#code-region-compact-tombstones-percent-code}

> **警告：**
>
> v7.5.7 および v8.5.4 以降では、この構成項目は非推奨となり、 [`gc.auto-compaction.tombstone-percent-threshold`](#tombstone-percent-threshold-new-in-v757-and-v854)に置き換えられました。

-   RocksDBの圧縮をトリガーするために必要な墓石の割合
-   デフォルト値: `30`
-   最小値: `1`
-   最大値: `100`

### <code>region-compact-min-redundant-rows</code><span class="version-mark">バージョン7.1.0の新機能</span> {#code-region-compact-min-redundant-rows-code-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> v7.5.7 および v8.5.4 以降では、この構成項目は非推奨となり、 [`gc.auto-compaction.redundant-rows-threshold`](#redundant-rows-threshold-new-in-v757-and-v854)に置き換えられました。

-   RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の数。
-   デフォルト値: `50000`
-   最小値: `0`

### <code>region-compact-redundant-rows-percent</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-region-compact-redundant-rows-percent-code-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> v7.5.7 および v8.5.4 以降では、この構成項目は非推奨となり、 [`gc.auto-compaction.redundant-rows-percent-threshold`](#redundant-rows-percent-threshold-new-in-v757-and-v854)に置き換えられました。

-   RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の割合。
-   デフォルト値: `20`
-   最小値: `1`
-   最大値: `100`

### <code>report-region-buckets-tick-interval</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-report-region-buckets-tick-interval-code-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> `report-region-buckets-tick-interval`は TiDB v6.1.0 で導入された実験的機能です。本番環境での使用は推奨されません。

-   `enable-region-bucket`が true の場合、TiKV がバケット情報を PD に報告する間隔。
-   デフォルト値: `10s`

### <code>pd-heartbeat-tick-interval</code> {#code-pd-heartbeat-tick-interval-code}

-   PD へのリージョンのハートビートがトリガーされる時間間隔。1 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"1m"`
-   最小値: `0`

### <code>pd-store-heartbeat-tick-interval</code> {#code-pd-store-heartbeat-tick-interval-code}

-   ストアの PD へのハートビートがトリガーされる時間間隔。1 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"10s"`
-   最小値: `0`

### <code>pd-report-min-resolved-ts-interval</code><span class="version-mark">バージョン7.6.0の新機能</span> {#code-pd-report-min-resolved-ts-interval-code-span-class-version-mark-new-in-v7-6-0-span}

> **注記：**
>
> この設定項目は[`report-min-resolved-ts-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file/#report-min-resolved-ts-interval-new-in-v600)から名前が変更されました。v7.6.0以降、 `report-min-resolved-ts-interval`無効になりました。

-   TiKVがPDリーダーに解決済みTSを報告する最小間隔を指定します。1に設定すると`0`報告は無効になります。
-   デフォルト値： `"1s"` （正の最小値）。v6.3.0より前のバージョンでは、デフォルト値は`"0s"`です。
-   最小値: `0`
-   単位: 秒

### <code>snap-mgr-gc-tick-interval</code> {#code-snap-mgr-gc-tick-interval-code}

-   期限切れのスナップショット ファイルのリサイクルがトリガーされる時間間隔。1 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"1m"`
-   最小値: `0`

### <code>snap-gc-timeout</code> {#code-snap-gc-timeout-code}

-   スナップショットファイルが保存される最長時間
-   デフォルト値: `"4h"`
-   最小値: `0`

### <code>snap-generator-pool-size</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-snap-generator-pool-size-code-span-class-version-mark-new-in-v5-4-0-span}

-   `snap-generator`スレッド プールのサイズを構成します。
-   リカバリシナリオにおいて、TiKV でリージョンのスナップショット生成を高速化するには、対応するワーカーの`snap-generator`番目のスレッド数を増やす必要があります。この設定項目を使用して、 `snap-generator`番目のスレッドプールのサイズを増やすことができます。
-   デフォルト値: `2`
-   最小値: `1`

### <code>lock-cf-compact-interval</code> {#code-lock-cf-compact-interval-code}

-   TiKVがロックカラムファミリーの手動圧縮をトリガーする時間間隔
-   デフォルト値: `"10m"`
-   最小値: `0`

### <code>lock-cf-compact-bytes-threshold</code> {#code-lock-cf-compact-bytes-threshold-code}

-   TiKVがロックカラムファミリーの手動圧縮をトリガーするサイズ
-   デフォルト値: `"256MiB"`
-   最小値: `0`
-   単位: MiB

### <code>notify-capacity</code> {#code-notify-capacity-code}

-   リージョンメッセージ キューの最長の長さ。
-   デフォルト値: `40960`
-   最小値: `0`

### <code>messages-per-tick</code> {#code-messages-per-tick-code}

-   バッチごとに処理されるメッセージの最大数
-   デフォルト値: `4096`
-   最小値: `0`

### <code>max-peer-down-duration</code> {#code-max-peer-down-duration-code}

-   ピアに許可される最長時間の非アクティブ期間。タイムアウトが発生したピアは`down`とマークされ、PD は後でそのピアを削除しようとします。
-   デフォルト値: `"10m"`
-   最小値: Hibernateリージョンが有効な場合、最小値は`peer-stale-state-check-interval * 2`です。Hibernateリージョンが無効な場合、最小値は`0`です。

### <code>max-leader-missing-duration</code> {#code-max-leader-missing-duration-code}

-   Raftグループにリーダーが存在しない状態がピアに許される最長時間。この値を超えると、ピアはPDを使用して、ピアが削除されたかどうかを確認します。
-   デフォルト値: `"2h"`
-   最小値: `abnormal-leader-missing-duration`より大きい

### <code>abnormal-leader-missing-duration</code> {#code-abnormal-leader-missing-duration-code}

-   Raftグループにリーダーが存在しない状態がピアに許容される最長時間。この値を超えると、ピアは異常とみなされ、メトリックとログにマークされます。
-   デフォルト値: `"10m"`
-   最小値: `peer-stale-state-check-interval`より大きい

### <code>peer-stale-state-check-interval</code> {#code-peer-stale-state-check-interval-code}

-   ピアがRaftグループにリーダーがいない状態にあるかどうかのチェックをトリガーする時間間隔。
-   デフォルト値: `"5m"`
-   最小値: `2 * election-timeout`より大きい

### <code>leader-transfer-max-log-lag</code> {#code-leader-transfer-max-log-lag-code}

-   Raftリーダーの転送中に転送先に許可される欠落ログの最大数
-   デフォルト値: `128`
-   最小値: `10`

### <code>max-snapshot-file-raw-size</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-max-snapshot-file-raw-size-code-span-class-version-mark-new-in-v6-1-0-span}

-   スナップショット ファイルのサイズがこの設定値を超えると、このファイルは複数のファイルに分割されます。
-   デフォルト値: `100MiB`
-   最小値: `100MiB`

### <code>snap-apply-batch-size</code> {#code-snap-apply-batch-size-code}

-   インポートしたスナップショットファイルをディスクに書き込むときに必要なメモリキャッシュサイズ
-   デフォルト値: `"10MiB"`
-   最小値: `0`
-   単位: MiB

### <code>consistency-check-interval</code> {#code-consistency-check-interval-code}

> **警告：**
>
> 整合性チェックはクラスターのパフォーマンスに影響し、TiDB のガベージコレクションと互換性がないため、本番環境では有効化**しないこと**をお勧めします。

-   整合性チェックがトリガーされる時間間隔。1 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"0s"`
-   最小値: `0`

### <code>raft-store-max-leader-lease</code> {#code-raft-store-max-leader-lease-code}

-   Raftリーダーの最も長い信頼期間
-   デフォルト値: `"9s"`
-   最小値: `0`

### <code>right-derive-when-split</code> {#code-right-derive-when-split-code}

-   リージョンを分割する際、新しいリージョンの開始キーを指定します。この設定項目を`true`に設定すると、開始キーは最大分割キーになります。この設定項目を`false`に設定すると、開始キーは元のリージョンの開始キーになります。
-   デフォルト値: `true`

### <code>merge-max-log-gap</code> {#code-merge-max-log-gap-code}

-   `merge`実行したときに許容される欠落ログの最大数
-   デフォルト値: `10`
-   最小値: `raft-log-gc-count-limit`より大きい

### <code>merge-check-tick-interval</code> {#code-merge-check-tick-interval-code}

-   TiKVがリージョンのマージが必要かどうかを確認する時間間隔
-   デフォルト値: `"2s"`
-   最小値: `0`より大きい

### <code>use-delete-range</code> {#code-use-delete-range-code}

-   `rocksdb delete_range`インターフェースからデータを削除するかどうかを決定します
-   デフォルト値: `false`

### <code>cleanup-import-sst-interval</code> {#code-cleanup-import-sst-interval-code}

-   期限切れの SST ファイルをチェックする時間間隔。1 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"10m"`
-   最小値: `0`

### <code>local-read-batch-size</code> {#code-local-read-batch-size-code}

-   1バッチで処理される読み取り要求の最大数
-   デフォルト値: `1024`
-   最小値: `0`より大きい

### <code>apply-yield-write-size</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-apply-yield-write-size-code-span-class-version-mark-new-in-v6-4-0-span}

-   適用スレッドが1回のポーリングで1つのFSM（有限状態機械）に書き込める最大バイト数。これはソフトリミットです。
-   デフォルト値: `"32KiB"`
-   最小値: `0`より大きい
-   単位: KiB|MiB|GiB

### <code>apply-max-batch-size</code> {#code-apply-max-batch-size-code}

-   Raftステートマシンは、BatchSystemによってデータ書き込みリクエストをバッチ処理します。この設定項目は、1バッチでリクエストを処理できるRaftステートマシンの最大数を指定します。
-   デフォルト値: `256`
-   最小値: `0`より大きい
-   最大値: `10240`

### <code>apply-pool-size</code> {#code-apply-pool-size-code}

-   ディスクにデータをフラッシュするプール内のスレッドの許容数。これはApplyスレッドプールのサイズです。このスレッドプールのサイズを変更する場合は、 [TiKV スレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `2`
-   値の範囲: `[1, CPU * 10]` `CPU` CPU コアの数を意味します。

### <code>store-max-batch-size</code> {#code-store-max-batch-size-code}

-   Raftステートマシンは、BatchSystemによってログをディスクにフラッシュするリクエストをバッチ処理します。この設定項目は、1回のバッチでリクエストを処理できるRaftステートマシンの最大数を指定します。
-   `hibernate-regions`が有効な場合、デフォルト値は`256`です。5 `hibernate-regions`無効な場合、デフォルト値は`1024`です。
-   最小値: `0`より大きい
-   最大値: `10240`

### <code>store-pool-size</code> {#code-store-pool-size-code}

-   Raftを処理するプール内の許容スレッド数。これはRaftstoreスレッドプールのサイズです。このスレッドプールのサイズを変更する場合は、 [TiKV スレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `2`
-   値の範囲: `[1, CPU * 10]` `CPU` CPU コアの数を意味します。

### <code>store-io-pool-size</code> <span class="version-mark">v5.3.0 の新機能</span> {#code-store-io-pool-size-code-span-class-version-mark-new-in-v5-3-0-span}

-   Raft I/Oタスクを処理するスレッドの許容数。これはStoreWriterスレッドプールのサイズです。このスレッドプールのサイズを変更する場合は、 [TiKV スレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `1` (v8.0.0 より前のデフォルト値は`0` )
-   最小値: `0`

### <code>future-poll-size</code> {#code-future-poll-size-code}

-   `future`駆動するスレッドの許容数
-   デフォルト値: `1`
-   最小値: `0`より大きい

### <code>cmd-batch</code> {#code-cmd-batch-code}

-   リクエストのバッチ処理を有効にするかどうかを制御します。有効にすると、書き込みパフォーマンスが大幅に向上します。
-   デフォルト値: `true`

### <code>inspect-interval</code> {#code-inspect-interval-code}

-   TiKVは一定の間隔でRaftstoreコンポーネントのレイテンシーを検査します。このパラメータは検査間隔を指定します。レイテンシーがこの値を超えると、検査はタイムアウトとしてマークされます。
-   タイムアウト検査の比率に基づいて、TiKV ノードが遅いかどうかを判断します。
-   デフォルト値: `"100ms"`
-   最小値: `"1ms"`

### <code>raft-write-size-limit</code><span class="version-mark">バージョン5.3.0の新機能</span> {#code-raft-write-size-limit-code-span-class-version-mark-new-in-v5-3-0-span}

-   Raftデータがディスクに書き込まれるしきい値を決定します。データサイズがこの設定項目の値より大きい場合、データはディスクに書き込まれます。1の値が`store-io-pool-size` `0`場合、この設定項目は有効になりません。
-   デフォルト値: `1MiB`
-   最小値: `0`

### <code>evict-cache-on-memory-ratio</code><span class="version-mark">バージョン 7.5.0 の新機能</span> {#code-evict-cache-on-memory-ratio-code-span-class-version-mark-new-in-v7-5-0-span}

-   TiKV のメモリ使用量がシステム使用可能メモリの 90% を超え、 Raftエントリ キャッシュが占有するメモリが使用メモリ* `evict-cache-on-memory-ratio`を超えると、TiKV はRaftエントリ キャッシュを排除します。
-   この値が`0`に設定されている場合、この機能は無効であることを意味します。
-   デフォルト値: `0.1`
-   最小値: `0`

### <code>periodic-full-compact-start-times</code> <span class="version-mark">v7.6.0 の新機能</span> {#code-periodic-full-compact-start-times-code-span-class-version-mark-new-in-v7-6-0-span}

> **警告：**
>
> 定期的なフルコンパクションは実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   TiKVが定期的なフルコンパクションを開始する特定の時刻を設定します。配列で複数のタイムスケジュールを指定できます。例：
    -   `periodic-full-compact-start-times = ["03:00", "23:00"]` 、TiKV ノードのローカル タイム ゾーンに基づいて、TiKV が毎日午前 3 時と午後 11 時に完全圧縮を実行することを示します。
    -   `periodic-full-compact-start-times = ["03:00 +0000", "23:00 +0000"]` 、TiKV が UTC タイムゾーンで毎日午前 3:00 と午後 11:00 に完全圧縮を実行することを示します。
    -   `periodic-full-compact-start-times = ["03:00 +0800", "23:00 +0800"]` 、TiKV が UTC+08:00 タイムゾーンで毎日午前 3:00 と午後 11:00 に完全圧縮を実行することを示します。
-   デフォルト値: `[]` 。これは、定期的な完全圧縮がデフォルトで無効になっていることを意味します。

### <code>periodic-full-compact-start-max-cpu</code><span class="version-mark">バージョン7.6.0の新機能</span> {#code-periodic-full-compact-start-max-cpu-code-span-class-version-mark-new-in-v7-6-0-span}

-   TiKV 定期完全圧縮の最大 CPU 使用率を制限します。
-   デフォルト値: `0.1` 。これは、定期的な圧縮プロセスの最大 CPU 使用率が 10% であることを意味します。

### <code>follower-read-max-log-gap</code> <span class="version-mark">v7.4.0 の新機能</span> {#code-follower-read-max-log-gap-code-span-class-version-mark-new-in-v7-4-0-span}

-   読み取りリクエストの処理時にフォロワーが遅延できるログの最大数。この制限を超えると、読み取りリクエストは拒否されます。
-   デフォルト値: `100`

### <code>inspect-cpu-util-thd</code><span class="version-mark">バージョン7.6.0の新機能</span> {#code-inspect-cpu-util-thd-code-span-class-version-mark-new-in-v7-6-0-span}

-   低速ノード検出中に TiKV ノードがビジー状態であるかどうかを判断するための CPU 使用率しきい値。
-   値の範囲: `[0, 1]`
-   デフォルト値: `0.4` 、つまり`40%`です。

### <code>inspect-kvdb-interval</code><span class="version-mark">バージョン8.1.2の新機能</span> {#code-inspect-kvdb-interval-code-span-class-version-mark-new-in-v8-1-2-span}

-   TiKVにおける低速ノード検出時にKVディスクをチェックする間隔とタイムアウト。KVDBとRaftDBが同じマウントパスを共有している場合、この値は`0` （検出なし）に上書きされます。
-   デフォルト値: `2s`

### <code>min-pending-apply-region-count</code><span class="version-mark">バージョン 8.0.0 の新機能</span> {#code-min-pending-apply-region-count-code-span-class-version-mark-new-in-v8-0-0-span}

-   TiKV の起動時にRaftログの適用がビジー状態にあるリージョンの最大数。Raftstoreは、このようなリージョンの数がこの値を下回っている場合にのみリーダー転送を受け入れるため、ローリング再起動時の可用性の低下を軽減できます。
-   デフォルト値: `10`

### <code>request-voter-replicated-index-interval</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-request-voter-replicated-index-interval-code-span-class-version-mark-new-in-v6-6-0-span}

-   Witness ノードが投票ノードから複製されたRaftログ位置を定期的に取得する間隔を制御します。
-   デフォルト値: `5m` 、つまり 5 分です。

### <code>slow-trend-unsensitive-cause</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-slow-trend-unsensitive-cause-code-span-class-version-mark-new-in-v6-6-0-span}

-   TiKVがSlowTrend検出アルゴリズムを使用する場合、この設定項目はレイテンシー検出の感度を制御します。値が高いほど、感度は低くなります。
-   デフォルト値: `10`

### <code>slow-trend-unsensitive-result</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-slow-trend-unsensitive-result-code-span-class-version-mark-new-in-v6-6-0-span}

-   TiKVがSlowTrend検出アルゴリズムを使用する場合、この設定項目はQPS検出の感度を制御します。値が高いほど感度は低くなります。
-   デフォルト値: `0.5`

## コプロセッサ {#coprocessor}

コプロセッサーに関連するコンフィグレーション項目。

### <code>split-region-on-table</code> {#code-split-region-on-table-code}

-   テーブルごとにリージョンを分割するかどうかを決定します。この機能はTiDBモードでのみ使用することをお勧めします。
-   デフォルト値: `false`

### <code>batch-split-limit</code> {#code-batch-split-limit-code}

-   バッチ処理におけるリージョン分割のしきい値。この値を大きくすると、リージョン分割が高速化されます。
-   デフォルト値: `10`
-   最小値: `1`

### <code>region-max-size</code> {#code-region-max-size-code}

-   リージョンの最大サイズ。この値を超えると、リージョンは複数のリージョンに分割されます。
-   デフォルト値: `region-split-size / 2 * 3`
-   単位: KiB|MiB|GiB

### <code>region-split-size</code> {#code-region-split-size-code}

-   新しく分割されたリージョンのサイズ。この値は推定値です。
-   デフォルト値: `"256MiB"` 。v8.4.0 より前では、デフォルト値は`"96MiB"`です。
-   単位: KiB|MiB|GiB

### <code>region-max-keys</code> {#code-region-max-keys-code}

-   リージョン内で許容されるキーの最大数。この値を超えると、リージョンは複数のリージョンに分割されます。
-   デフォルト値: `region-split-keys / 2 * 3`

### <code>region-split-keys</code> {#code-region-split-keys-code}

-   新しく分割されたリージョン内のキーの数。この値は推定値です。
-   デフォルト値: `2560000` 。v8.4.0 より前では、デフォルト値は`960000`です。

### <code>consistency-check-method</code> {#code-consistency-check-method-code}

-   データの整合性チェックの方法を指定します
-   MVCCデータの整合性チェックの場合は値を`"mvcc"`に設定し、生データの整合性チェックの場合は値を`"raw"`に設定します。
-   デフォルト値: `"mvcc"`

## コプロセッサv2 {#coprocessor-v2}

### <code>coprocessor-plugin-directory</code> {#code-coprocessor-plugin-directory-code}

-   コンパイルされたコプロセッサプラグインが配置されているディレクトリのパス。このディレクトリ内のプラグインはTiKVによって自動的にロードされます。
-   この構成項目が設定されていない場合、コプロセッサ プラグインは無効になります。
-   デフォルト値: なし

### <code>enable-region-bucket</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-enable-region-bucket-code-span-class-version-mark-new-in-v6-1-0-span}

-   リージョンをバケットと呼ばれる小さな範囲に分割するかどうかを決定します。バケットは、スキャンの同時実行性を向上させるための同時実行クエリの単位として使用されます。バケットの設計の詳細については、 [動的サイズリージョン](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md)を参照してください。
-   デフォルト値: なし。デフォルトでは無効です。

> **警告：**
>
> -   `enable-region-bucket`は TiDB v6.1.0 で導入された実験的機能です。本番環境での使用は推奨されません。
> -   この構成は、 `region-split-size`が`region-bucket-size`の 2 倍以上の場合にのみ意味を持ちます。それ以外の場合、バケットは実際には生成されません。
> -   `region-split-size`より大きな値に調整すると、パフォーマンスが低下し、スケジュールが遅くなるリスクがあります。

### <code>region-bucket-size</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-region-bucket-size-code-span-class-version-mark-new-in-v6-1-0-span}

-   `enable-region-bucket`が true の場合のバケットのサイズ。
-   デフォルト値: v7.3.0 以降、デフォルト値は`96MiB`から`50MiB`に変更されます。

> **警告：**
>
> `region-bucket-size`は TiDB v6.1.0 で導入された実験的機能です。本番環境での使用は推奨されません。

## ロックスdb {#rocksdb}

RocksDBに関連するコンフィグレーション項目

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDBのバックグラウンドスレッドの数。RocksDBスレッドプールのサイズを変更する場合は、 [TiKV スレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値:
    -   CPU コア数が 10 の場合、デフォルト値は`9`です。
    -   CPU コア数が 8 の場合、デフォルト値は`7`です。
    -   CPU コア数が`N`の場合、デフォルト値は`max(2, min(N - 1, 9))`です。
-   最小値: `2`

### <code>max-background-flushes</code> {#code-max-background-flushes-code}

-   同時バックグラウンド メンバーテーブル フラッシュ ジョブの最大数
-   デフォルト値:
    -   CPU コア数が 10 の場合、デフォルト値は`3`です。
    -   CPU コア数が 8 の場合、デフォルト値は`2`です。
    -   CPU コア数が`N`の場合、デフォルト値は`[(max-background-jobs + 3) / 4]`です。
-   最小値: `1`

### <code>max-sub-compactions</code> {#code-max-sub-compactions-code}

-   RocksDBで同時に実行されるサブコンパクション操作の数
-   デフォルト値: `3`
-   最小値: `1`

### <code>max-open-files</code> {#code-max-open-files-code}

-   RocksDBが開くことができるファイルの総数
-   デフォルト値: `40960`
-   最小値: `-1`

### <code>max-manifest-file-size</code> {#code-max-manifest-file-size-code}

-   RocksDBマニフェストファイルの最大サイズ
-   デフォルト値: `"256MiB"` 。v8.5.3 およびそれ以前の v8.5.x バージョンの場合、デフォルト値は`"128MiB"`です。
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>create-if-missing</code> {#code-create-if-missing-code}

-   DBスイッチを自動的に作成するかどうかを決定します
-   デフォルト値: `true`

### <code>wal-recovery-mode</code> {#code-wal-recovery-mode-code}

-   WALリカバリモード
-   オプションの値:
    -   `"tolerate-corrupted-tail-records"` : すべてのログで不完全な末尾データを持つレコードを許容し、破棄します。
    -   `"absolute-consistency"` : 破損したログが見つかった場合はリカバリを中止します
    -   `"point-in-time"` : 最初の破損したログに遭遇するまでログを順番に回復します
    -   `"skip-any-corrupted-records"` ：災害後の復旧。データは可能な限り復旧され、破損したレコードはスキップされます。
-   デフォルト値: `"point-in-time"`

### <code>wal-dir</code> {#code-wal-dir-code}

-   WALファイルが保存されるディレクトリ。指定されていない場合、WALファイルはデータと同じディレクトリに保存されます。
-   デフォルト値: `""`

### <code>wal-ttl-seconds</code> {#code-wal-ttl-seconds-code}

-   アーカイブされたWALファイルの有効期間。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: 秒

### <code>wal-size-limit</code> {#code-wal-size-limit-code}

-   アーカイブされたWALファイルのサイズ制限。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>max-total-wal-size</code> {#code-max-total-wal-size-code}

-   合計での最大 RocksDB WAL サイズは、 `data-dir`のファイルのうち`*.log`のサイズです。
-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値は`"4GiB"`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`1`です。

### <code>stats-dump-period</code> {#code-stats-dump-period-code}

-   統計がログに出力される間隔。
-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値は`"10m"`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`"0"`です。

### <code>compaction-readahead-size</code> {#code-compaction-readahead-size-code}

-   RocksDBの圧縮中に先読み機能を有効にし、先読みデータのサイズを指定します。機械式ディスクを使用している場合は、少なくとも2MiBに設定することをお勧めします。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>writable-file-max-buffer-size</code> {#code-writable-file-max-buffer-size-code}

-   WritableFileWriteで使用される最大バッファサイズ
-   デフォルト値: `"1MiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>use-direct-io-for-flush-and-compaction</code> {#code-use-direct-io-for-flush-and-compaction-code}

-   バックグラウンドフラッシュとコンパクションにおいて、読み取りと書き込みの両方に`O_DIRECT`使用するかどうかを決定します。このオプションのパフォーマンスへの影響： `O_DIRECT`を有効にすると、OSバッファキャッシュの汚染を回避できますが、後続のファイル読み取りではバッファキャッシュへの内容の再読み込みが必要になります。
-   デフォルト値: `false`

### <code>rate-bytes-per-sec</code> {#code-rate-bytes-per-sec-code}

-   Titanが無効になっている場合、この設定項目はRocksDBコンパクションのI/Oレートを制限し、トラフィックピーク時のフォアグラウンドの読み取りおよび書き込みパフォーマンスへのRocksDBコンパクションの影響を軽減します。Titanが有効になっている場合、この設定項目はRocksDBコンパクションとTitan GCの合計I/Oレートを制限します。RocksDBコンパクションとTitan GCのI/OまたはCPU消費量が大きすぎる場合は、ディスクI/O帯域幅と実際の書き込みトラフィックに応じて、この設定項目を適切な値に設定してください。
-   デフォルト値: `10GiB`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>rate-limiter-refill-period</code> {#code-rate-limiter-refill-period-code}

-   I/Oトークンの補充頻度を制御します。値を小さくするとI/Oバーストは減少しますが、CPUオーバーヘッドが増加します。
-   デフォルト値: `"100ms"`

### <code>rate-limiter-mode</code> {#code-rate-limiter-mode-code}

-   RocksDBの圧縮率制限モード
-   オプション`"write-only"` `"all-io"` `"read-only"`
-   デフォルト値: `"write-only"`

### <code>rate-limiter-auto-tuned</code> <span class="version-mark">v5.0 の新機能</span> {#code-rate-limiter-auto-tuned-code-span-class-version-mark-new-in-v5-0-span}

-   RocksDBの圧縮レートリミッターの設定を、最近のワークロードに基づいて自動的に最適化するかどうかを決定します。この設定を有効にすると、圧縮保留バイト数が通常よりもわずかに多くなります。
-   デフォルト値: `true`

### <code>enable-pipelined-write</code> {#code-enable-pipelined-write-code}

-   パイプライン書き込みを有効にするかどうかを制御します。この設定を有効にすると、以前のパイプライン書き込みが使用されます。この設定を無効にすると、新しいパイプラインコミットメカニズムが使用されます。
-   デフォルト値: `false`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   ファイルが非同期的に書き込まれている間に、OSがファイルをディスクに増分的に同期する速度
-   デフォルト値: `"1MiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>wal-bytes-per-sync</code> {#code-wal-bytes-per-sync-code}

-   WAL ファイルが書き込まれている間に OS が WAL ファイルをディスクに増分的に同期する速度
-   デフォルト値: `"512KiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>info-log-max-size</code> {#code-info-log-max-size-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBのログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.file.max-size`](#max-size-new-in-v540)に置き換えられました。

-   情報ログの最大サイズ
-   デフォルト値: `"1GiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>info-log-roll-time</code> {#code-info-log-roll-time-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBのログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となりました。TiKVは時間に基づく自動ログ分割をサポートしなくなりました。代わりに、設定項目[`log.file.max-size`](#max-size-new-in-v540)使用して、ファイルサイズに基づく自動ログ分割のしきい値を設定できます。

-   情報ログが切り捨てられる時間間隔。値が`0s`の場合、ログは切り捨てられません。
-   デフォルト値: `"0s"`

### <code>info-log-keep-log-file-num</code> {#code-info-log-keep-log-file-num-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBのログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.file.max-backups`](#max-backups-new-in-v540)に置き換えられました。

-   保存されるログファイルの最大数
-   デフォルト値: `10`
-   最小値: `0`

### <code>info-log-dir</code> {#code-info-log-dir-code}

-   ログが保存されるディレクトリ
-   デフォルト値: `""`

### <code>info-log-level</code> {#code-info-log-level-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBのログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.level`](#level-new-in-v540)に置き換えられました。

-   RocksDBのログレベル
-   デフォルト値: `"info"`

### <code>write-buffer-flush-oldest-first</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-write-buffer-flush-oldest-first-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   現在の RocksDB の`memtable`のメモリ使用量がしきい値に達したときに使用するフラッシュ戦略を指定します。
-   デフォルト値: `false`
-   値のオプション:

    -   データ量が最も大きい`false` : `memtable`が SST ファイルにフラッシュされます。
    -   `true` ：最も古い`memtable`がSSTファイルにフラッシュされます。この戦略はコールドデータの`memtable`クリアできるため、コールドデータとホットデータが明確に区別できるシナリオに適しています。

### <code>write-buffer-limit</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-write-buffer-limit-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   単一の TiKV 内のすべての RocksDB インスタンスの合計メモリ制限を`memtable`に指定します。3 `0`制限がないことを意味します。

-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値は none となり、制限がないことを意味します。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値はシステムメモリの合計サイズの 20% になります。

-   単位: KiB|MiB|GiB

### <code>track-and-verify-wals-in-manifest</code> <span class="version-mark">v6.5.9、v7.1.5、v7.5.2、v8.0.0 の新機能</span> {#code-track-and-verify-wals-in-manifest-code-span-class-version-mark-new-in-v6-5-9-v7-1-5-v7-5-2-and-v8-0-0-span}

-   RocksDB MANIFESTファイルにWrite Ahead Log（WAL）ファイルに関する情報を記録するかどうか、および起動時にWALファイルの整合性を検証するかどうかを制御します。詳細については、RocksDB [MANIFESTでWALを追跡する](https://github.com/facebook/rocksdb/wiki/Track-WAL-in-MANIFEST)を参照してください。
-   デフォルト値: `true`
-   値のオプション:
    -   `true` : WAL ファイルに関する情報を MANIFEST ファイルに記録し、起動時に WAL ファイルの整合性を検証します。
    -   `false` : MANIFEST ファイルに WAL ファイルに関する情報を記録せず、起動時に WAL ファイルの整合性を検証しません。

### <code>enable-multi-batch-write</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-enable-multi-batch-write-code-span-class-version-mark-new-in-v6-2-0-span}

-   RocksDB 書き込み最適化を有効にするかどうかを制御します。これにより、WriteBatch の内容を memtable に同時に書き込むことができ、書き込みのレイテンシーが短縮されます。
-   デフォルト値: なし。ただし、明示的に`false`に設定した場合、または`rocksdb.enable-pipelined-write`または`rocksdb.enable-unordered-write`有効になっている場合を除き、デフォルトで有効になります。

## rocksdb.titan {#rocksdb-titan}

Titan に関連するコンフィグレーション項目。

### <code>enabled</code> {#code-enabled-code}

> **注記：**
>
> -   ワイド テーブルと JSON データの書き込みおよびポイント クエリのパフォーマンスを向上させるために、TiDB v7.6.0 以降では既定値が`false`から`true`に変更され、Titan がデフォルトで有効になります。
> -   v7.6.0 以降のバージョンにアップグレードされた既存のクラスターは元の構成を保持します。つまり、Titan が明示的に有効になっていない場合は、引き続き RocksDB が使用されます。
> -   TiDB v7.6.0以降にアップグレードする前にクラスタでTitanが有効になっている場合、アップグレード後もTitanは保持され、アップグレード前の[`min-blob-size`](/tikv-configuration-file.md#min-blob-size)設定が保持されます。アップグレード前に明示的に値を設定しない場合は、アップグレード後のクラスタ構成の安定性を確保するために、以前のバージョン`1KiB`のデフォルト値が保持されます。

-   Titan を有効または無効にします。
-   デフォルト値: `true`

### <code>dirname</code> {#code-dirname-code}

-   Titan Blobファイルが保存されているディレクトリ
-   デフォルト値: `"titandb"`

### <code>disable-gc</code> {#code-disable-gc-code}

-   Titan が BLOB ファイルに対して実行するガベージ コレクション (GC) を無効にするかどうかを決定します。
-   デフォルト値: `false`

### <code>max-background-gc</code> {#code-max-background-gc-code}

-   Titan の GC スレッドの最大数。TiKV**の「詳細」** &gt; **「スレッド CPU」** &gt; **「RocksDB CPU」**パネルで、Titan GC スレッドが長時間にわたって満杯になっていることが確認された場合は、Titan GC スレッドプールのサイズを増やすことを検討してください。
-   デフォルト値: `1` 。v8.0.0 より前では、デフォルト値は`4`です。
-   最小値: `1`

## rocksdb.defaultcf | rocksdb.writecf | rocksdb.lockcf | rocksdb.raftcf {#rocksdb-defaultcf-rocksdb-writecf-rocksdb-lockcf-rocksdb-raftcf}

`rocksdb.defaultcf` `rocksdb.lockcf`関連するコンフィグレーション`rocksdb.writecf` 。

### <code>block-size</code> {#code-block-size-code}

-   RocksDBブロックのデフォルトサイズ
-   `defaultcf`と`writecf`のデフォルト値： `"32KiB"`
-   `lockcf`のデフォルト値: `"16KiB"`
-   最小値: `"1KiB"`
-   単位: KiB|MiB|GiB

### <code>block-cache-size</code> {#code-block-cache-size-code}

> **警告：**
>
> v6.6.0 以降、この構成は非推奨になりました。

-   RocksDB ブロックのキャッシュ サイズ。
-   `defaultcf`のデフォルト値: `Total machine memory * 25%`
-   `writecf`のデフォルト値: `Total machine memory * 15%`
-   `lockcf`のデフォルト値: `Total machine memory * 2%`
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>disable-block-cache</code> {#code-disable-block-cache-code}

-   ブロックキャッシュを有効または無効にする
-   デフォルト値: `false`

### <code>cache-index-and-filter-blocks</code> {#code-cache-index-and-filter-blocks-code}

-   インデックスとフィルタのキャッシュを有効または無効にする
-   デフォルト値: `true`

### <code>pin-l0-filter-and-index-blocks</code> {#code-pin-l0-filter-and-index-blocks-code}

-   レベル 0 SST ファイルのインデックス ブロックとフィルター ブロックをメモリに固定するかどうかを決定します。
-   デフォルト値: `true`

### <code>use-bloom-filter</code> {#code-use-bloom-filter-code}

-   ブルームフィルターを有効または無効にする
-   デフォルト値: `true`

### <code>optimize-filters-for-hits</code> {#code-optimize-filters-for-hits-code}

-   フィルタのヒット率を最適化するかどうかを決定します
-   `defaultcf`のデフォルト値: `true`
-   `writecf`と`lockcf`のデフォルト値： `false`

### <code>optimize-filters-for-memory</code> <span class="version-mark">v7.2.0 の新機能</span> {#code-optimize-filters-for-memory-code-span-class-version-mark-new-in-v7-2-0-span}

-   メモリの内部断片化を最小限に抑えるブルーム/リボン フィルターを生成するかどうかを決定します。
-   この構成項目は[`format-version`](#format-version-new-in-v620) &gt;= 5 の場合にのみ有効になることに注意してください。
-   デフォルト値: `false`

### <code>whole-key-filtering</code> {#code-whole-key-filtering-code}

-   キー全体をブルームフィルターに入れるかどうかを決定します
-   `defaultcf`と`lockcf`のデフォルト値： `true`
-   `writecf`のデフォルト値: `false`

### <code>bloom-filter-bits-per-key</code> {#code-bloom-filter-bits-per-key-code}

-   ブルームフィルターが各キーに予約する長さ
-   デフォルト値: `10`
-   単位: バイト

### <code>block-based-bloom-filter</code> {#code-block-based-bloom-filter-code}

-   各ブロックがブルームフィルターを作成するかどうかを決定します
-   デフォルト値: `false`

### <code>ribbon-filter-above-level</code> <span class="version-mark">v7.2.0 の新機能</span> {#code-ribbon-filter-above-level-code-span-class-version-mark-new-in-v7-2-0-span}

-   この値以上のレベルにはリボンフィルターを使用し、この値未満のレベルには非ブロックベースのブルームフィルターを使用するかどうかを決定します。この設定項目が設定されている場合、 [`block-based-bloom-filter`](#block-based-bloom-filter)無視されます。
-   この構成項目は[`format-version`](#format-version-new-in-v620) &gt;= 5 の場合にのみ有効になることに注意してください。
-   デフォルト値: なし。デフォルトでは無効です。

### <code>read-amp-bytes-per-bit</code> {#code-read-amp-bytes-per-bit-code}

-   読み取り増幅の統計を有効または無効にします。
-   オプションの値: `0` (無効)、&gt; `0` (有効)。
-   デフォルト値: `0`
-   最小値: `0`

### <code>compression-per-level</code> {#code-compression-per-level-code}

-   各レベルのデフォルトの圧縮アルゴリズム
-   `defaultcf`デフォルト値: [&quot;no&quot;, &quot;no&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;zstd&quot;, &quot;zstd&quot;]
-   `writecf`デフォルト値: [&quot;no&quot;, &quot;no&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;zstd&quot;, &quot;zstd&quot;]
-   `lockcf`デフォルト値: [&quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;]

### <code>bottommost-level-compression</code> {#code-bottommost-level-compression-code}

-   最レイヤーの圧縮アルゴリズムを設定します。この設定項目は`compression-per-level`設定を上書きします。
-   RocksDB は、データが LSM ツリーに書き込まれた時点から、 `compression-per-level`配列で指定された最後の圧縮アルゴリズムを最レイヤーに直接採用しません。3 `bottommost-level-compression` 、最レイヤーが最初から圧縮効果が最も高い圧縮アルゴリズムを使用できるようになります。
-   最レイヤーに圧縮アルゴリズムを設定しない場合は、この構成項目の値を`disable`に設定します。
-   デフォルト値: `"zstd"`

### <code>write-buffer-size</code> {#code-write-buffer-size-code}

-   メモリテーブルのサイズ
-   `defaultcf`と`writecf`のデフォルト値： `"128MiB"`
-   `lockcf`のデフォルト値:
    -   `storage.engine="raft-kv"`の場合、デフォルト値は`"32MiB"`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`"4MiB"`です。
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>max-write-buffer-number</code> {#code-max-write-buffer-number-code}

-   memtableの最大数。1 `storage.flow-control.enable` `true`に設定すると、 `storage.flow-control.memtables-threshold`この設定項目を上書きします。
-   デフォルト値: `5`
-   最小値: `0`

### <code>min-write-buffer-number-to-merge</code> {#code-min-write-buffer-number-to-merge-code}

-   フラッシュをトリガーするために必要な最小のmemtable数
-   デフォルト値: `1`
-   最小値: `0`

### <code>max-bytes-for-level-base</code> {#code-max-bytes-for-level-base-code}

-   ベースレベル（レベル1）の最大バイト数。通常、memtableのサイズの4倍に設定されます。レベル1のデータサイズが制限値`max-bytes-for-level-base`に達すると、レベル1のSSTファイルと、それらに重複するレベル2のSSTファイルが圧縮されます。
-   `defaultcf`と`writecf`のデフォルト値： `"512MiB"`
-   `lockcf`のデフォルト値: `"128MiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB
-   不要な圧縮を減らすために、 `max-bytes-for-level-base`の値はL0のデータ量とほぼ同じに設定することをお勧めします。たとえば、圧縮方法が「no:no:lz4:lz4:lz4:lz4:lz4」の場合、L0とL1は圧縮されておらず、L0の圧縮のトリガー条件はSSTファイルの数が4（デフォルト値）に達することであるため、 `max-bytes-for-level-base`の値は`write-buffer-size * 4`にする必要があります。L0とL1の両方で圧縮が採用されている場合、memtableから圧縮されたSSTファイルのサイズを把握するには、RocksDBログを分析する必要があります。たとえば、ファイルサイズが32MiBの場合、 `max-bytes-for-level-base`の値を128MiB（ `32 MiB * 4` ）に設定することをお勧めします。

### <code>target-file-size-base</code> {#code-target-file-size-base-code}

-   ベースレベルでのターゲットファイルのサイズ。値が`enable-compaction-guard` `true`場合、この値は`compaction-guard-max-output-file-size`で上書きされます。
-   デフォルト値: なし。デフォルトでは`"8MiB"`意味します。
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>level0-file-num-compaction-trigger</code> {#code-level0-file-num-compaction-trigger-code}

-   圧縮をトリガーするL0のファイルの最大数
-   `defaultcf`と`writecf`のデフォルト値： `4`
-   `lockcf`のデフォルト値: `1`
-   最小値: `0`

### <code>level0-slowdown-writes-trigger</code> {#code-level0-slowdown-writes-trigger-code}

-   書き込み停止をトリガーする L0 のファイルの最大数。
-   v8.5.4 以前のバージョン: フロー制御メカニズムが有効になっている場合 ( [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)が`true` )、この構成項目の値は[`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)によって直接上書きされます。
-   v8.5.5以降：フロー制御メカニズムが有効（ [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)が`true` ）の場合、この設定項目の値が`storage.flow-control.l0-files-threshold`より大きい場合にのみ、値が[`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)に上書きされます。この動作により、フロー制御しきい値を上げた際にRocksDBの圧縮加速メカニズムが弱まるのを防ぎます。
-   デフォルト値: `20`
-   最小値: `0`

### <code>level0-stop-writes-trigger</code> {#code-level0-stop-writes-trigger-code}

-   書き込みを完全にブロックするために必要なL0のファイルの最大数
-   デフォルト値: `36`
-   最小値: `0`

### <code>max-compaction-bytes</code> {#code-max-compaction-bytes-code}

-   圧縮ごとにディスクに書き込まれる最大バイト数
-   デフォルト値: `"2GiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>compaction-pri</code> {#code-compaction-pri-code}

-   圧縮の優先タイプ
-   オプションの値:
    -   `"by-compensated-size"` : ファイル サイズの順にファイルを圧縮し、大きなファイルは優先順位を高くして圧縮します。
    -   `"oldest-largest-seq-first"` : 更新時刻が最も古いファイルの圧縮を優先します。この値は、ホットキーを狭い範囲で更新する場合に**のみ**使用してください。
    -   `"oldest-smallest-seq-first"` : 長期間にわたって次のレベルに圧縮されない範囲を持つファイルの圧縮を優先します。キー空間全体でホットキーをランダムに更新する場合、この値により書き込み増幅がわずかに軽減される可能性があります。
    -   `"min-overlapping-ratio"` : オーバーラップ率の高いファイルの圧縮を優先します。ファイルの各レベルが小さい場合（ `the file size in the next level` ÷ `the file size in this level`の結果が小さい場合）、TiKV はこのファイルを最初に圧縮します。多くの場合、この値は書き込み増幅を効果的に削減できます。
-   `defaultcf`と`writecf`のデフォルト値： `"min-overlapping-ratio"`
-   `lockcf`のデフォルト値: `"by-compensated-size"`

### <code>dynamic-level-bytes</code> {#code-dynamic-level-bytes-code}

-   動的レベルバイトを最適化するかどうかを決定します
-   デフォルト値: `true`

### <code>num-levels</code> {#code-num-levels-code}

-   RocksDBファイルの最大レベル数
-   デフォルト値: `7`

### <code>max-bytes-for-level-multiplier</code> {#code-max-bytes-for-level-multiplier-code}

-   各レイヤーのデフォルトの増幅倍数
-   デフォルト値: `10`

### <code>compaction-style</code> {#code-compaction-style-code}

-   圧縮方法
-   オプション`"universal"` `"fifo"` `"level"`
-   デフォルト値: `"level"`

### <code>disable-auto-compactions</code> {#code-disable-auto-compactions-code}

-   自動圧縮を無効にするかどうかを決定します。
-   デフォルト値: `false`

### <code>soft-pending-compaction-bytes-limit</code> {#code-soft-pending-compaction-bytes-limit-code}

-   保留中の圧縮バイトに対するソフト制限。
-   v8.5.4 以前のバージョン: フロー制御メカニズムが有効になっている場合 ( [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)が`true` )、この構成項目は[`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)によって直接上書きされます。
-   バージョン8.5.5以降：フロー制御メカニズムが有効（ [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)が`true` ）の場合、この設定項目の値が`storage.flow-control.soft-pending-compaction-bytes-limit`より大きい場合にのみ、 [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)が優先されます。この動作により、フロー制御のしきい値を上げた際にRocksDBの圧縮加速メカニズムが弱まるのを防ぎます。
-   デフォルト値: `"192GiB"`
-   単位: KiB|MiB|GiB

### <code>hard-pending-compaction-bytes-limit</code> {#code-hard-pending-compaction-bytes-limit-code}

-   保留中の圧縮バイト数のハードリミット。1 `storage.flow-control.enable` `true`に設定した場合、 `storage.flow-control.hard-pending-compaction-bytes-limit`この設定項目を上書きします。
-   デフォルト値: `"256GiB"`
-   単位: KiB|MiB|GiB

### <code>enable-compaction-guard</code> {#code-enable-compaction-guard-code}

-   TiKVリージョン境界でSSTファイルを分割する最適化であるコンパクションガードを有効または無効にします。この最適化により、コンパクションI/Oが削減され、TiKVはより大きなSSTファイルサイズ（つまり、全体的なSSTファイルの数が少ない）を使用できるようになります。また、リージョンの移行時に古いデータを効率的にクリーンアップできます。
-   `defaultcf`と`writecf`のデフォルト値： `true`
-   `lockcf`のデフォルト値: なし。デフォルトでは無効であることを意味します。

### <code>compaction-guard-min-output-file-size</code> {#code-compaction-guard-min-output-file-size-code}

-   圧縮ガードが有効になっている場合のSSTファイルの最小サイズ。この設定により、圧縮ガードが有効になっているときにSSTファイルが小さすぎる状態になるのを防ぎます。
-   デフォルト値: `"8MiB"`
-   単位: KiB|MiB|GiB

### <code>compaction-guard-max-output-file-size</code> {#code-compaction-guard-max-output-file-size-code}

-   圧縮ガードが有効な場合のSSTファイルの最大サイズ。この設定により、圧縮ガードが有効な場合にSSTファイルが大きくなりすぎるのを防ぎます。この設定は、同じカラムファミリーの`target-file-size-base`オーバーライドします。
-   デフォルト値: `"128MiB"`
-   単位: KiB|MiB|GiB

### <code>format-version</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-format-version-code-span-class-version-mark-new-in-v6-2-0-span}

-   SSTファイルのフォーマットバージョン。この設定項目は新しく書き込まれるテーブルにのみ影響します。既存のテーブルの場合、バージョン情報はフッターから読み取られます。
-   オプションの値:
    -   `0` : すべてのTiKVバージョンで読み取り可能です。デフォルトのチェックサムタイプはCRC32であり、このバージョンではチェックサムタイプの変更はサポートされていません。
    -   `1` : すべてのTiKVバージョンで読み取り可能です。xxHashなどのデフォルト以外のチェックサムタイプをサポートします。RocksDBはチェックサムタイプがCRC32以外の場合にのみデータを書き込みます。(バージョン`0`は自動的にアップグレードされます)
    -   `2` : すべてのTiKVバージョンで読み取り可能です。LZ4、BZip2、Zlib圧縮方式を使用して圧縮ブロックのエンコーディングを変更します。
    -   `3` : TiKV v2.1以降のバージョンで読み取り可能です。インデックスブロック内のキーのエンコーディングを変更します。
    -   `4` : TiKV v3.0以降のバージョンで読み取ることができます。インデックスブロック内の値のエンコードを変更します。
    -   `5` : TiKV v6.1以降のバージョンで読み取り可能です。フルフィルターとパーティションフィルターは、異なるスキーマを使用した、より高速で正確なブルームフィルター実装を使用します。
-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値は`2`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`5`です。

### <code>ttl</code><span class="version-mark">バージョン7.2.0の新機能</span> {#code-ttl-code-span-class-version-mark-new-in-v7-2-0-span}

-   TTLよりも古い更新を含むSSTファイルは、自動的に圧縮対象として選択されます。これらのSSTファイルは、最下層または最下層ファイルまで圧縮されるように、段階的に圧縮されます。
-   デフォルト値: なし。デフォルトでは SST ファイルが選択されていないことを意味します。
-   単位: s(秒)|h(時間)|d(日)

### <code>periodic-compaction-seconds</code> <span class="version-mark">v7.2.0 の新機能</span> {#code-periodic-compaction-seconds-code-span-class-version-mark-new-in-v7-2-0-span}

-   定期的な圧縮の時間間隔。この値より古い更新を含む SST ファイルが圧縮対象として選択され、これらの SST ファイルが元々存在していたレベルと同じレベルに書き換えられます。
-   デフォルト値: なし。つまり、定期的な圧縮はデフォルトで無効になっています。
-   単位: s(秒)|h(時間)|d(日)

### <code>max-compactions</code><span class="version-mark">バージョン6.6.0の新機能</span> {#code-max-compactions-code-span-class-version-mark-new-in-v6-6-0-span}

-   同時実行可能な圧縮タスクの最大数。値`0`は制限なしを意味します。
-   デフォルト値: `0`

## rocksdb.defaultcf.titan {#rocksdb-defaultcf-titan}

> **注記：**
>
> Titan は`rocksdb.defaultcf`でのみ有効化できます。 `rocksdb.writecf`では Titan を有効化できません。

`rocksdb.defaultcf.titan`に関連するコンフィグレーション項目です。

### <code>min-blob-size</code> {#code-min-blob-size-code}

> **注記：**
>
> -   TiDB v7.6.0以降、ワイドテーブルおよびJSONデータの書き込みとポイントクエリのパフォーマンスを向上させるため、Titanがデフォルトで有効化されました。デフォルト値は`min-blob-size`でしたが、 `1KiB`から`32KiB`に変更されました。つまり、 `32KiB`を超える値はTitanに保存され、その他のデータは引き続きRocksDBに保存されます。
> -   構成の一貫性を確保するために、既存のクラスターを TiDB v7.6.0 以降のバージョンにアップグレードする場合、アップグレード前に`min-blob-size`明示的に設定しないと、TiDB は以前のデフォルト値`1KiB`を保持します。
> -   `32KiB`より小さい値は、範囲スキャンのパフォーマンスに影響を与える可能性があります。ただし、ワークロードが主に大量の書き込みとポイントクエリである場合は、パフォーマンスを向上させるために値を`min-blob-size`に下げることを検討してください。

-   BLOBファイルに格納される最小値。指定されたサイズより小さい値はLSMツリーに格納されます。
-   デフォルト値: なし。デフォルトでは`"32KiB"`意味します。
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>blob-file-compression</code> {#code-blob-file-compression-code}

> **注記：**
>
> -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他の Snappy 圧縮形式はサポートされていません。
> -   TiDB v7.6.0 以降では、デフォルト値`blob-file-compression`が`"lz4"`から`"zstd"`に変更されます。

-   BLOBファイルで使用される圧縮アルゴリズム
-   `"lz4"` `"bzip2"` `"zlib"` `"no"` `"snappy"` `"lz4hc"` `"zstd"`
-   デフォルト値: `"zstd"`

### <code>zstd-dict-size</code> {#code-zstd-dict-size-code}

-   zstd 辞書の圧縮サイズ。デフォルト値は`"0KiB"`で、これは zstd 辞書の圧縮を無効にすることを意味します。この場合、Titan は単一の値に基づいてデータを圧縮しますが、RocksDB はブロックに基づいてデータを圧縮します (デフォルトでは`32KiB` )。Titan 値の平均サイズが`32KiB`未満の場合、Titan の圧縮率は RocksDB よりも低くなります。JSON を例にとると、Titan のストア サイズは RocksDB よりも 30% ～ 50% 大きくなる可能性があります。実際の圧縮率は、値の内容が圧縮に適しているかどうか、および異なる値間の類似性によって異なります。 `zstd-dict-size`構成すると (たとえば、 `16KiB`に設定すると)、zstd 辞書の圧縮を有効にして圧縮率を上げることができます。実際のストア サイズは RocksDB よりも小さくなる可能性があります。ただし、zstd 辞書の圧縮により、特定のワークロードで約 10% のパフォーマンス低下が発生する可能性があります。
-   デフォルト値: `"0KiB"`
-   単位: KiB|MiB|GiB

### <code>blob-cache-size</code> {#code-blob-cache-size-code}

-   BLOBファイルのキャッシュサイズ
-   デフォルト値: `"0GiB"`
-   最小値: `0`
-   推奨値: `0` 。v8.0.0以降、TiKVは設定項目`shared-blob-cache`を導入し、デフォルトで有効になっているため、 `blob-cache-size`別途設定する必要はありません。7の設定は、 `blob-cache-size` `shared-blob-cache` `false`に設定されている場合にのみ有効になります。
-   単位: KiB|MiB|GiB

### <code>shared-blob-cache</code> <span class="version-mark">v8.0.0 の新機能</span> {#code-shared-blob-cache-code-span-class-version-mark-new-in-v8-0-0-span}

-   Titan BLOB ファイルと RocksDB ブロック ファイルの共有キャッシュを有効にするかどうかを制御します。
-   デフォルト値: `true` 。共有キャッシュが有効な場合、ブロックファイルの優先度が高くなります。つまり、TiKVはブロックファイルのキャッシュニーズを満たすことを優先し、残りのキャッシュをBLOBファイルに使用します。

### <code>min-gc-batch-size</code> {#code-min-gc-batch-size-code}

-   GCを1回実行するために必要なBlobファイルの最小合計サイズ
-   デフォルト値: `"16MiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>max-gc-batch-size</code> {#code-max-gc-batch-size-code}

-   一度にGCを実行できるBlobファイルの最大合計サイズ
-   デフォルト値: `"64MiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>discardable-ratio</code> {#code-discardable-ratio-code}

-   BLOBファイル内の古いデータ（対応するキーが更新または削除されたデータ）の割合が以下のしきい値を超えると、Titan GCがトリガーされます。TitanがこのBLOBファイルの有効なデータを別のファイルに書き込む際、 `discardable-ratio`値を使用して書き込み増幅とスペース増幅の上限を推定できます（圧縮が無効の場合）。

    書き込み増幅の上限 = 1 / `discardable-ratio`

    空間増幅の上限 = 1 / (1 - `discardable-ratio` )

    これら2つの式から、 `discardable_ratio`の値を減らすとスペース増幅は減少しますが、TitanでのGCの頻度は増加します。値を増やすとTitan GCの頻度が減少し、対応するI/O帯域幅とCPU使用率は低下しますが、ディスク使用量は増加します。

-   デフォルト値: `0.5`

-   最小値: `0`

-   最大値: `1`

### <code>sample-ratio</code> {#code-sample-ratio-code}

-   GC中にファイルをサンプリングするときの（Blobファイルから読み取られたデータ/Blobファイル全体）の比率
-   デフォルト値: `0.1`
-   最小値: `0`
-   最大値: `1`

### <code>merge-small-file-threshold</code> {#code-merge-small-file-threshold-code}

-   BLOBファイルのサイズがこの値より小さい場合でも、そのBLOBファイルはGCの対象として選択される可能性があります。この場合、 `discardable-ratio`無視されます。
-   デフォルト値: `"8MiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>blob-run-mode</code> {#code-blob-run-mode-code}

-   Titanの実行モードを指定します。
-   オプションの値:
    -   `normal` : 値のサイズが[`min-blob-size`](#min-blob-size)超えると、データを BLOB ファイルに書き込みます。
    -   `read-only` : BLOB ファイルへの新しいデータの書き込みを拒否しますが、BLOB ファイルから元のデータは読み取ります。
    -   `fallback` : BLOB ファイル内のデータを LSM に書き戻します。
-   デフォルト値: `normal`

### <code>level-merge</code> {#code-level-merge-code}

-   読み取りパフォーマンスを最適化するかどうかを決定します。1 `level-merge`有効にすると、書き込み増幅が強化されます。
-   デフォルト値: `false`

## ラフトDB {#raftdb}

`raftdb`に関連するコンフィグレーション項目

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDBのバックグラウンドスレッドの数。RocksDBスレッドプールのサイズを変更する場合は、 [TiKV スレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `4`
-   最小値: `2`

### <code>max-sub-compactions</code> {#code-max-sub-compactions-code}

-   RocksDBで実行される同時サブコンパクション操作の数
-   デフォルト値: `2`
-   最小値: `1`

### <code>max-open-files</code> {#code-max-open-files-code}

-   RocksDBが開くことができるファイルの総数
-   デフォルト値: `40960`
-   最小値: `-1`

### <code>max-manifest-file-size</code> {#code-max-manifest-file-size-code}

-   RocksDBマニフェストファイルの最大サイズ
-   デフォルト値: `"20MiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>create-if-missing</code> {#code-create-if-missing-code}

-   値が`true`の場合、データベースが存在しない場合に作成されます。
-   デフォルト値: `true`

### <code>stats-dump-period</code> {#code-stats-dump-period-code}

-   統計がログに出力される間隔
-   デフォルト値: `10m`

### <code>wal-dir</code> {#code-wal-dir-code}

-   Raft RocksDB WALファイルが保存されるディレクトリ。WALの絶対ディレクトリパスです。この設定項目を[`rocksdb.wal-dir`](#wal-dir)と同じ値に設定**しないでください**。
-   この構成項目が設定されていない場合、ログ ファイルはデータと同じディレクトリに保存されます。
-   マシンにディスクが 2 つある場合、RocksDB データと WAL ログを別のディスクに保存するとパフォーマンスが向上します。
-   デフォルト値: `""`

### <code>wal-ttl-seconds</code> {#code-wal-ttl-seconds-code}

-   アーカイブされたWALファイルを保持する期間を指定します。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: 秒

### <code>wal-size-limit</code> {#code-wal-size-limit-code}

-   アーカイブされたWALファイルのサイズ制限。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>max-total-wal-size</code> {#code-max-total-wal-size-code}

-   RocksDB WALの合計最大サイズ
-   デフォルト値:
    -   `storage.engine="raft-kv"`の場合、デフォルト値は`"4GiB"`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`1`です。

### <code>compaction-readahead-size</code> {#code-compaction-readahead-size-code}

-   RocksDB の圧縮中に先読み機能を有効にするかどうか、また先読みデータのサイズを指定するかどうかを制御します。
-   機械式ディスクを使用する場合は、値を少なくとも`2MiB`に設定することをお勧めします。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>writable-file-max-buffer-size</code> {#code-writable-file-max-buffer-size-code}

-   WritableFileWriteで使用される最大バッファサイズ
-   デフォルト値: `"1MiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>use-direct-io-for-flush-and-compaction</code> {#code-use-direct-io-for-flush-and-compaction-code}

-   バックグラウンドフラッシュとコンパクションにおいて、読み取りと書き込みの両方に`O_DIRECT`使用するかどうかを決定します。このオプションのパフォーマンスへの影響： `O_DIRECT`を有効にすると、OSバッファキャッシュの汚染を回避できますが、後続のファイル読み取りではバッファキャッシュへの内容の再読み込みが必要になります。
-   デフォルト値: `false`

### <code>enable-pipelined-write</code> {#code-enable-pipelined-write-code}

-   パイプライン書き込みを有効にするかどうかを制御します。この設定を有効にすると、以前のパイプライン書き込みが使用されます。この設定を無効にすると、新しいパイプラインコミットメカニズムが使用されます。
-   デフォルト値: `true`

### <code>allow-concurrent-memtable-write</code> {#code-allow-concurrent-memtable-write-code}

-   同時メモリテーブル書き込みを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   ファイルが非同期的に書き込まれている間に、OSがファイルをディスクに増分的に同期する速度
-   デフォルト値: `"1MiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>wal-bytes-per-sync</code> {#code-wal-bytes-per-sync-code}

-   WALファイルが書き込まれるときにOSがWALファイルをディスクに増分的に同期する速度
-   デフォルト値: `"512KiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>info-log-max-size</code> {#code-info-log-max-size-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBのログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.file.max-size`](#max-size-new-in-v540)に置き換えられました。

-   情報ログの最大サイズ
-   デフォルト値: `"1GiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>info-log-roll-time</code> {#code-info-log-roll-time-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBのログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となりました。TiKVは時間に基づく自動ログ分割をサポートしなくなりました。代わりに、設定項目[`log.file.max-size`](#max-size-new-in-v540)使用して、ファイルサイズに基づく自動ログ分割のしきい値を設定できます。

-   情報ログを切り捨てる間隔。値が`0s`の場合、ログは切り捨てられません。
-   デフォルト値: `"0s"` (ログは切り捨てられません)

### <code>info-log-keep-log-file-num</code> {#code-info-log-keep-log-file-num-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBのログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.file.max-backups`](#max-backups-new-in-v540)に置き換えられました。

-   RaftDBに保存される情報ログファイルの最大数
-   デフォルト値: `10`
-   最小値: `0`

### <code>info-log-dir</code> {#code-info-log-dir-code}

-   情報ログが保存されるディレクトリ
-   デフォルト値: `""`

### <code>info-log-level</code> {#code-info-log-level-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBのログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.level`](#level-new-in-v540)に置き換えられました。

-   RaftDBのログレベル
-   デフォルト値: `"info"`

## いかだエンジン {#raft-engine}

Raft Engineに関連するコンフィグレーション項目。

> **注記：**
>
> -   Raft Engine を初めて有効にすると、TiKV は RocksDB からRaft Engineにデータを転送します。そのため、TiKV が起動するまで数十秒ほど待つ必要があります。
> -   TiDB v5.4.0 のRaft Engineのデータ形式は、以前の TiDB バージョンと互換性がありません。そのため、TiDB クラスターを v5.4.0 から以前のバージョンにダウングレードする必要がある場合は、ダウングレードする**前に**、 Raft Engineを`enable`から`false`に設定して無効化し、TiKV を再起動して設定を有効にしてください。

### <code>enable</code> {#code-enable-code}

-   Raftログを保存するためにRaft Engineを使用するかどうかを決定します。有効にすると、 `raftdb`の設定は無視されます。
-   デフォルト値: `true`

### <code>dir</code> {#code-dir-code}

-   raft ログファイルが保存されるディレクトリ。このディレクトリが存在しない場合は、TiKV の起動時に作成されます。
-   この設定項目が設定されていない場合は`{data-dir}/raft-engine`が使用されます。
-   マシンに複数のディスクがある場合は、TiKV のパフォーマンスを向上させるために、 Raft Engineのデータを別のディスクに保存することをお勧めします。
-   デフォルト値: `""`

### <code>spill-dir</code> <span class="version-mark">v8.4.0 の新機能</span> {#code-spill-dir-code-span-class-version-mark-new-in-v8-4-0-span}

-   Raftログファイルを保存するための補助ディレクトリです。1ディレクトリのディスク容量`dir`いっぱいになると、新しいRaftログはこのディレクトリに保存されます。設定後にこの補助ディレクトリが存在しない場合は、TiKVの起動時に自動的に作成されます。
-   この構成が設定されていない場合、補助ディレクトリは有効になりません。

> **注記：**
>
> -   この構成は、Raft Engineの`dir`と`spill-dir`異なるディスク ドライブに設定されている場合にのみ有効になります。
> -   この機能を有効にした後、無効にする場合は、TiKVを再起動する前に以下の操作を実行する必要があります。そうしないと、TiKVは起動に失敗します。
>     1.  TiKVを停止します。
>     2.  すべてのRaftログを`spill-dir`ディレクトリから[`dir`](/tikv-configuration-file.md#dir)ディレクトリにコピーします。
>     3.  TiKV 構成ファイルからこの構成を削除します。
>     4.  TiKVを再起動します。

### <code>batch-compression-threshold</code> {#code-batch-compression-threshold-code}

-   ログバッチのしきい値サイズを指定します。この設定値より大きいログバッチは圧縮されます。この設定項目を`0`に設定すると、圧縮は無効になります。
-   デフォルト値: `"4KiB"` 。v8.1.0 より前では、デフォルト値は`"8KiB"`です。

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

> **警告：**
>
> バージョン6.5.0以降、 Raft Engineはバッファリングなしでログを直接ディスクに書き込みます。そのため、この設定項目は非推奨となり、機能しなくなりました。

-   バッファリングされた書き込みの最大累積サイズを指定します。この設定値を超えると、バッファリングされた書き込みはディスクにフラッシュされます。
-   この構成項目を`0`に設定すると、増分同期は無効になります。
-   v6.5.0 より前では、デフォルト値は`"4MiB"`です。

### <code>target-file-size</code> {#code-target-file-size-code}

-   ログファイルの最大サイズを指定します。ログファイルがこの値より大きい場合、ログファイルはローテーションされます。
-   デフォルト値: `"128MiB"`

### <code>purge-threshold</code> {#code-purge-threshold-code}

-   メインログキューのしきい値サイズを指定します。この設定値を超えると、メインログキューは消去されます。
-   この設定を使用して、 Raft Engineのディスク領域の使用量を調整できます。
-   デフォルト値: `"10GiB"`

### <code>recovery-mode</code> {#code-recovery-mode-code}

-   回復中にファイルの破損を処理する方法を決定します。
-   `"tolerate-any-corruption"` `"tolerate-tail-corruption"`オプション: `"absolute-consistency"`
-   デフォルト値: `"tolerate-tail-corruption"`

### <code>recovery-read-block-size</code> {#code-recovery-read-block-size-code}

-   リカバリ中にログ ファイルを読み取るための最小 I/O サイズ。
-   デフォルト値: `"16KiB"`
-   最小値: `"512B"`

### <code>recovery-threads</code> {#code-recovery-threads-code}

-   ログ ファイルをスキャンして回復するために使用されるスレッドの数。
-   デフォルト値: `4`
-   最小値: `1`

### <code>memory-limit</code> {#code-memory-limit-code}

-   Raft Engineのメモリ使用量の制限を指定します。
-   この構成値が設定されていない場合、使用可能なシステムメモリの 15% が使用されます。
-   デフォルト値: `Total machine memory * 15%`

### <code>format-version</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-format-version-code-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> `format-version` `2`に設定した後、TiKV クラスターを v6.3.0 から以前のバージョンにダウングレードする必要がある場合は、ダウングレード**前に**次の手順を実行します。
>
> 1.  [`enable`](/tikv-configuration-file.md#enable-1)を`false`に設定してRaft Engineを無効にし、TiKV を再起動して設定を有効にします。
> 2.  `format-version`を`1`に設定します。
> 3.  `enable`を`true`に設定してRaft Engineを有効にし、TiKV を再起動して設定を有効にします。

-   Raft Engineのログ ファイルのバージョンを指定します。
-   値のオプション:
    -   `1` : TiKV v6.3.0 より前のバージョンのデフォルトのログファイルバージョン。TiKV &gt;= v6.1.0 で読み取ることができます。
    -   `2` : ログのリサイクルをサポートします。TiKV &gt;= v6.3.0 で読み取ることができます。
-   デフォルト値:
    -   `storage.engine="raft-kv"`の場合、デフォルト値は`2`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`5`です。

### <code>enable-log-recycle</code><span class="version-mark">バージョン6.3.0の新機能</span> {#code-enable-log-recycle-code-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この構成項目は、 [`format-version`](#format-version-new-in-v630) &gt;= 2 の場合にのみ使用できます。

-   Raft Engineで古いログファイルをリサイクルするかどうかを決定します。有効にすると、論理的にパージされたログファイルがリサイクル用に予約されます。これにより、書き込みワークロードのロングテールレイテンシーが削減されます。
-   デフォルト値: `true`

### <code>prefill-for-recycle</code> <span class="version-mark">v7.0.0 の新機能</span> {#code-prefill-for-recycle-code-span-class-version-mark-new-in-v7-0-0-span}

> **注記：**
>
> この設定項目は、 [`enable-log-recycle`](#enable-log-recycle-new-in-v630) `true`に設定されている場合にのみ有効になります。

-   Raft Engineのログリサイクル用に空のログファイルを生成するかどうかを決定します。有効にすると、 Raft Engineは初期化中にログリサイクル用の空のログファイルを自動的にバッチで作成し、初期化直後にログリサイクルを有効にします。
-   デフォルト値: `false`

### <code>compression-level</code> <span class="version-mark">v7.4.0 の新機能</span> {#code-compression-level-code-span-class-version-mark-new-in-v7-4-0-span}

-   Raftログファイルを書き込む際にRaft Engineが使用するLZ4アルゴリズムの圧縮効率を設定します。値が低いほど圧縮速度は速くなりますが、圧縮率は低くなります。
-   範囲: `[1, 16]`
-   デフォルト値: `1`

## 安全 {#security}

セキュリティに関するコンフィグレーション項目。

### <code>ca-path</code> {#code-ca-path-code}

-   CAファイルのパス
-   デフォルト値: `""`

### <code>cert-path</code> {#code-cert-path-code}

-   X.509証明書を含むPrivacy Enhanced Mail（PEM）ファイルのパス
-   デフォルト値: `""`

### <code>key-path</code> {#code-key-path-code}

-   X.509キーを含むPEMファイルのパス
-   デフォルト値: `""`

### <code>cert-allowed-cn</code> {#code-cert-allowed-cn-code}

-   クライアントが提示する証明書内の許容可能なX.509共通名のリスト。提示された共通名がリスト内のエントリのいずれかと完全に一致する場合にのみ、リクエストが許可されます。
-   デフォルト値: `[]` 。これは、クライアント証明書のCNチェックがデフォルトで無効になっていることを意味します。

### <code>redact-info-log</code> <span class="version-mark">v4.0.8 の新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v4-0-8-span}

-   この設定項目は、ログ編集を有効または無効にします。値のオプションは`true` 、 `false` 、 `"on"` 、 `"off"` 、 `"marker"` 。 `"on"` 、 `"off"` 、 `"marker"`オプションはバージョン8.3.0で導入されました。
-   構成項目が`false`または`"off"`に設定されている場合、ログ編集は無効になります。
-   構成項目が`true`または`"on"`に設定されている場合、ログ内のすべてのユーザー データは`?`に置き換えられます。
-   設定項目を`"marker"`に設定すると、ログ内のすべてのユーザーデータは`‹ ›`で囲まれます。ユーザーデータに`‹`または`›`が含まれている場合、 `‹`は`‹‹`に、 `›`は`››`にエスケープされます。マークされたログに基づいて、ログを表示する際にマークされた情報を非感度化するかどうかを決定できます。
-   デフォルト値: `false`
-   使用方法の詳細については、 [TiKV側でのログ編集](/log-redaction.md#log-redaction-in-tikv-side)参照してください。

## セキュリティ.暗号化 {#security-encryption}

[保存時の暗号化](/encryption-at-rest.md) (TDE)に関連するコンフィグレーション項目。

### <code>data-encryption-method</code> {#code-data-encryption-method-code}

-   データファイルの暗号化方法
-   値のオプション: &quot;plaintext&quot;、&quot;aes128-ctr&quot;、&quot;aes192-ctr&quot;、&quot;aes256-ctr&quot;、および &quot;sm4-ctr&quot; (v6.3.0 以降でサポート)
-   「プレーンテキスト」以外の値は暗号化が有効になっていることを意味し、その場合はマスター キーを指定する必要があります。
-   デフォルト値: `"plaintext"`

### <code>data-key-rotation-period</code> {#code-data-key-rotation-period-code}

-   TiKV がデータ暗号化キーをローテーションする頻度を指定します。
-   デフォルト値: `7d`

### <code>enable-file-dictionary-log</code> {#code-enable-file-dictionary-log-code}

-   TiKV が暗号化メタデータを管理するときに、I/O とミューテックスの競合を減らすための最適化を有効にします。
-   この構成パラメータが有効になっている場合（デフォルト）に互換性の問題が発生するのを回避するには、詳細については[保存時の暗号化- TiKVバージョン間の互換性](/encryption-at-rest.md#compatibility-between-tikv-versions)参照してください。
-   デフォルト値: `true`

### <code>master-key</code> {#code-master-key-code}

-   暗号化が有効になっている場合、マスターキーを指定します。マスターキーの設定方法については、 [保存時の暗号化- 暗号化の設定](/encryption-at-rest.md#configure-encryption)参照してください。

### <code>previous-master-key</code> {#code-previous-master-key-code}

-   新しいマスターキーをローテーションする際に使用する古いマスターキーを指定します。設定形式は`master-key`と同じです。マスターキーの設定方法については、 [保存時の暗号化- 暗号化の設定](/encryption-at-rest.md#configure-encryption)参照してください。

## 輸入 {#import}

TiDB Lightning のインポートとBR復元に関連するコンフィグレーション項目。

### <code>num-threads</code> {#code-num-threads-code}

-   RPCリクエストを処理するスレッドの数
-   デフォルト値: `8`
-   最小値: `1`

### <code>stream-channel-window</code> {#code-stream-channel-window-code}

-   ストリームチャンネルのウィンドウサイズ。チャンネルがいっぱいになると、ストリームはブロックされます。
-   デフォルト値: `128`

### <code>memory-use-ratio</code> <span class="version-mark">v6.5.0 の新機能</span> {#code-memory-use-ratio-code-span-class-version-mark-new-in-v6-5-0-span}

-   v6.5.0以降、PITRはメモリ内のバックアップログファイルへの直接アクセスとデータの復元をサポートします。この設定項目は、PITRに使用可能なメモリとTiKVの総メモリの比率を指定します。
-   値の範囲: [0.0, 0.5]
-   デフォルト値： `0.3` 。これは、システムメモリの30%がPITRに使用できることを意味します。値が`0.0`の場合、PITRはログファイルをローカルディレクトリにダウンロードすることで実行されます。

> **注記：**
>
> v6.5.0 より前のバージョンでは、ポイントインタイムリカバリ (PITR) は、バックアップ ファイルをローカル ディレクトリにダウンロードすることによるデータの復元のみをサポートします。

## GC {#gc}

### <code>batch-keys</code> {#code-batch-keys-code}

-   1バッチでガベージコレクションされるキーの数
-   デフォルト値: `512`

### <code>max-write-bytes-per-sec</code> {#code-max-write-bytes-per-sec-code}

-   GC ワーカーが 1 秒間に RocksDB に書き込むことができる最大バイト数。
-   値が`0`に設定されている場合、制限はありません。
-   デフォルト値: `"0"`

### <code>enable-compaction-filter</code><span class="version-mark">バージョン5.0の新機能</span> {#code-enable-compaction-filter-code-span-class-version-mark-new-in-v5-0-span}

-   圧縮フィルタ機能でGCを有効にするかどうかを制御します
-   デフォルト値: `true`

### <code>ratio-threshold</code> {#code-ratio-threshold-code}

-   GC をトリガーするガベージ比率のしきい値。
-   デフォルト値: `1.1`

### <code>num-threads</code> <span class="version-mark">v6.5.8、v7.1.4、v7.5.1、v7.6.0 の新機能</span> {#code-num-threads-code-span-class-version-mark-new-in-v6-5-8-v7-1-4-v7-5-1-and-v7-6-0-span}

-   `enable-compaction-filter`場合の GC スレッド数は`false`です。
-   デフォルト値: `1`

## gc.自動コンパクション {#gc-auto-compaction}

TiKV 自動圧縮の動作を設定します。

### <code>check-interval</code> <span class="version-mark">v7.5.7 および v8.5.4 の新機能</span> {#code-check-interval-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   TiKVが自動コンパクションをトリガーするかどうかを確認する間隔。この間隔内では、自動コンパクションの条件を満たすリージョンが優先度に基づいて処理されます。この間隔が経過すると、TiKVはリージョン情報を再スキャンし、優先度を再計算します。
-   デフォルト値: `"300s"`

### <code>tombstone-num-threshold</code> <span class="version-mark">v7.5.7 および v8.5.4 の新機能</span> {#code-tombstone-num-threshold-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   TiKV自動圧縮をトリガーするために必要なRocksDBトゥームストーンの数。トゥームストーンの数がこのしきい値に達するか、トゥームストーンの割合が[`tombstone-percent-threshold`](#tombstone-percent-threshold-new-in-v757-and-v854)に達すると、TiKVは自動圧縮をトリガーします。
-   この設定項目は、 [圧縮フィルター](/garbage-collection-configuration.md)無効になっている場合にのみ有効になります。
-   デフォルト値: `10000`
-   最小値: `0`

### <code>tombstone-percent-threshold</code> <span class="version-mark">v7.5.7 および v8.5.4 の新機能</span> {#code-tombstone-percent-threshold-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   TiKV自動圧縮をトリガーするために必要なRocksDBトゥームストーンの割合。トゥームストーンの割合がこのしきい値に達するか、トゥームストーンの数が[`tombstone-num-threshold`](#tombstone-num-threshold-new-in-v757-and-v854)に達すると、TiKVは自動圧縮をトリガーします。
-   この設定項目は、 [圧縮フィルター](/garbage-collection-configuration.md)無効になっている場合にのみ有効になります。
-   デフォルト値: `30`
-   最小値: `0`
-   最大値: `100`

### <code>redundant-rows-threshold</code> <span class="version-mark">v7.5.7 および v8.5.4 の新機能</span> {#code-redundant-rows-threshold-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   TiKV自動コンパクションをトリガーするために必要な冗長MVCC行の数。冗長行には、RocksDBトゥームストーン、TiKVの古いバージョン、およびTiKVの削除トゥームストーンが含まれます。冗長MVCC行の数がこのしきい値に達するか、これらの行の割合が[`redundant-rows-percent-threshold`](#redundant-rows-percent-threshold-new-in-v757-and-v854)に達すると、TiKVは自動コンパクションをトリガーします。
-   この構成項目は、 [圧縮フィルター](/garbage-collection-configuration.md)有効な場合にのみ有効になります。
-   デフォルト値: `50000`
-   最小値: `0`

### <code>redundant-rows-percent-threshold</code> <span class="version-mark">v7.5.7 および v8.5.4 の新機能</span> {#code-redundant-rows-percent-threshold-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   TiKV自動コンパクションをトリガーするために必要な冗長MVCC行の割合。冗長行には、RocksDBトゥームストーン、TiKVの古いバージョン、およびTiKVの削除トゥームストーンが含まれます。冗長MVCC行の数が[`redundant-rows-threshold`](#redundant-rows-threshold-new-in-v757-and-v854)に達するか、これらの行の割合が`redundant-rows-percent-threshold`に達すると、TiKVは自動コンパクションをトリガーします。
-   この構成項目は、 [圧縮フィルター](/garbage-collection-configuration.md)有効な場合にのみ有効になります。
-   デフォルト値: `20`
-   最小値: `0`
-   最大値: `100`

### <code>bottommost-level-force</code> <span class="version-mark">v7.5.7 および v8.5.4 の新機能</span> {#code-bottommost-level-force-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   RocksDB の一番下のファイルに対して圧縮を強制するかどうかを制御します。
-   デフォルト値: `true`

## バックアップ {#backup}

BRバックアップに関連するコンフィグレーション項目。

### <code>num-threads</code> {#code-num-threads-code}

-   バックアップを処理するワーカースレッドの数
-   デフォルト値: `MIN(CPU * 0.5, 8)`
-   値の範囲: `[1, CPU]`
-   最小値: `1`

### <code>batch-size</code> {#code-batch-size-code}

-   1回のバッチでバックアップするデータ範囲の数
-   デフォルト値: `8`

### <code>sst-max-size</code> {#code-sst-max-size-code}

-   バックアップSSTファイルサイズのしきい値。TiKVリージョン内のバックアップファイルのサイズがこのしきい値を超える場合、ファイルは複数のファイルにバックアップされ、TiKVリージョンは複数のリージョン範囲に分割されます。分割されたリージョン内の各ファイルのサイズは、 `sst-max-size`と同じ（またはわずかに大きい）です。
-   たとえば、リージョン`[a,e)`のバックアップ ファイルのサイズが`sst-max-size`より大きい場合、ファイルはリージョン`[a,b)` `[d,e)`複数のファイルにバックアップされ、 `[c,d)` `[b,c)`のサイズは`[b,c)` `[a,b)`のサイズと同じ (または`sst-max-size` `[c,d)`大きい) になります。
-   デフォルト値: `"384MiB"` 。v8.4.0 より前では、デフォルト値は`"144MiB"`です。

### <code>enable-auto-tune</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-enable-auto-tune-code-span-class-version-mark-new-in-v5-4-0-span}

-   クラスタリソースの使用率が高い場合に、クラスタへの影響を軽減するために、バックアップタスクで使用されるリソースを制限するかどうかを制御します。詳細については、 [BRオートチューン](/br/br-auto-tune.md)を参照してください。
-   デフォルト値: `true`

### <code>s3-multi-part-size</code> <span class="version-mark">v5.3.2 の新機能</span> {#code-s3-multi-part-size-code-span-class-version-mark-new-in-v5-3-2-span}

> **注記：**
>
> この設定は、S3 のレート制限によるバックアップ失敗に対処するために導入されました。この問題は[バックアップデータのstorage構造の改良](/br/br-snapshot-architecture.md#structure-of-backup-files)で修正されました。そのため、この設定はバージョン 6.1.1 以降では非推奨となり、推奨されなくなりました。

-   バックアップ中にS3へのマルチパートアップロードを実行する際に使用するパートサイズ。この設定値を調整することで、S3に送信されるリクエストの数を制御できます。
-   S3にデータをバックアップし、バックアップファイルがこの設定項目の値より大きい場合、 [マルチパートアップロード](https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPart.html)自動的に有効になります。圧縮率に基づくと、96MiBのリージョンで生成されるバックアップファイルは約10MiB～30MiBになります。
-   デフォルト値: 5MiB

## backup.hadoop {#backup-hadoop}

### <code>home</code> {#code-home-code}

-   HDFSシェルコマンドの場所を指定し、TiKVがシェルコマンドを見つけられるようにします。この設定項目は環境変数`$HADOOP_HOME`と同じ効果を持ちます。
-   デフォルト値: `""`

### <code>linux-user</code> {#code-linux-user-code}

-   TiKV が HDFS シェル コマンドを実行する Linux ユーザーを指定します。
-   この設定項目が設定されていない場合、TiKV は現在の Linux ユーザーを使用します。
-   デフォルト値: `""`

## ログバックアップ {#log-backup}

ログバックアップに関連するコンフィグレーション項目。

### <span class="version-mark">v6.2.0の新機能</span><code>enable</code> {#code-enable-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ バックアップを有効にするかどうかを決定します。
-   デフォルト値: `true`

### <code>file-size-limit</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-file-size-limit-code-span-class-version-mark-new-in-v6-2-0-span}

-   保存されるバックアップ ログ データのサイズ制限。
-   デフォルト値: 256MiB
-   注: 通常、値`file-size-limit`は外部storageに表示されるバックアップファイルのサイズよりも大きくなります。これは、バックアップファイルが外部storageにアップロードされる前に圧縮されるためです。

### <code>initial-scan-pending-memory-quota</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-initial-scan-pending-memory-quota-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ バックアップ中に増分スキャン データを保存するために使用されるキャッシュのクォータ。
-   デフォルト値: `min(Total machine memory * 10%, 512 MiB)`

### <code>initial-scan-rate-limit</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-initial-scan-rate-limit-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログバックアップ中の増分データスキャンにおけるスループットのレート制限。これは、ディスクから1秒あたりに読み取ることができるデータの最大量を意味します。数値のみ（例： `60` ）を指定した場合、単位はKiBではなくByteになります。
-   デフォルト値: 60MiB
-   最小値: 1MiB

### <code>max-flush-interval</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-max-flush-interval-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログバックアップでバックアップデータを外部storageに書き込む最大間隔。
-   デフォルト値: 3分

### <code>num-threads</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-num-threads-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ バックアップで使用されるスレッドの数。
-   デフォルト値: CPU * 0.5
-   値の範囲: [2, 12]

### <code>temp-path</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-temp-path-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ ファイルが外部storageにフラッシュされる前に書き込まれる一時パス。
-   デフォルト値: `${deploy-dir}/data/log-backup-temp`

## CDC {#cdc}

TiCDC に関連するコンフィグレーション項目。

### <code>min-ts-interval</code> {#code-min-ts-interval-code}

-   解決された TS が計算され転送される間隔。
-   デフォルト値: `"1s"` 。

> **注記：**
>
> バージョン6.5.0では、CDCレイテンシーを削減するため、デフォルト値の`min-ts-interval`が`"1s"`から`"200ms"`に変更されました。バージョン6.5.1以降では、ネットワークトラフィックを削減するため、このデフォルト値は`"1s"`に戻されます。

### <code>old-value-cache-memory-quota</code> {#code-old-value-cache-memory-quota-code}

-   TiCDC によるメモリ使用量の上限の古い値。
-   デフォルト値: `512MiB`

### <code>sink-memory-quota</code> {#code-sink-memory-quota-code}

-   TiCDC データ変更イベントによるメモリ使用量の上限。
-   デフォルト値: `512MiB`

### <code>incremental-scan-speed-limit</code> {#code-incremental-scan-speed-limit-code}

-   履歴データが増分スキャンされる最大速度。
-   デフォルト値: `"128MiB"` 、これは 1 秒あたり 128 MiB を意味します。

### <code>incremental-scan-threads</code> {#code-incremental-scan-threads-code}

-   履歴データを増分スキャンするタスクのスレッド数。
-   デフォルト値: `4` 、これは 4 つのスレッドを意味します。

### <code>incremental-scan-concurrency</code> {#code-incremental-scan-concurrency-code}

-   履歴データを増分スキャンするタスクの同時実行の最大数。
-   デフォルト値: `6` 。最大 6 つのタスクを同時に実行できることを意味します。
-   注意: `incremental-scan-concurrency`の値は`incremental-scan-threads`の値以上である必要があります。そうでない場合、TiKV は起動時にエラーを報告します。

### <code>incremental-scan-concurrency-limit</code> <span class="version-mark">v7.6.0 の新機能</span> {#code-incremental-scan-concurrency-limit-code-span-class-version-mark-new-in-v7-6-0-span}

-   実行待ちの履歴データの増分スキャンタスクの最大キュー長。実行待ちのタスク数がこの制限を超えると、新しいタスクは拒否されます。
-   デフォルト値: `10000` 。これは、最大 10000 個のタスクを実行キューに入れることができることを意味します。
-   注: `incremental-scan-concurrency-limit` [`incremental-scan-concurrency`](#incremental-scan-concurrency)以上である必要があります。そうでない場合、TiKV は`incremental-scan-concurrency`使用してこの構成を上書きします。

## resolved-ts {#resolved-ts}

ステイル読み取り要求に対応するために解決された TS を維持することに関連するコンフィグレーション項目。

### <code>enable</code> {#code-enable-code}

-   すべてのリージョンに対して解決済みの TS を維持するかどうかを決定します。
-   デフォルト値: `true`

### <code>advance-ts-interval</code> {#code-advance-ts-interval-code}

-   解決された TS が計算され転送される間隔。
-   デフォルト値: `"20s"`

### <code>scan-lock-pool-size</code> {#code-scan-lock-pool-size-code}

-   解決済み TS を初期化するときに TiKV が MVCC (マルチバージョン同時実行制御) ロック データをスキャンするために使用するスレッドの数。
-   デフォルト値: `2` 、つまり 2 つのスレッドを意味します。

## pessimistic-txn {#pessimistic-txn}

悲観的トランザクションの使用については、 [TiDB 悲観的トランザクションモード](/pessimistic-transaction.md)を参照してください。

### <code>wait-for-lock-timeout</code> {#code-wait-for-lock-timeout-code}

-   TiKVにおける悲観的トランザクションが、他のトランザクションによるロックの解放を待機する最長時間です。タイムアウトが発生した場合、TiDBにエラーが返され、TiDBはロックの追加を再試行します。ロック待機タイムアウトは`innodb_lock_wait_timeout`に設定されます。
-   デフォルト値: `"1s"`
-   最小値: `"1ms"`

### <code>wake-up-delay-duration</code> {#code-wake-up-delay-duration-code}

-   悲観的トランザクションがロックを解除すると、ロックを待機しているすべてのトランザクションのうち、最小の`start_ts`を持つトランザクションのみが起動されます。他のトランザクションは`wake-up-delay-duration`後に起動されます。
-   デフォルト値: `"20ms"`

### <code>pipelined</code> {#code-pipelined-code}

-   この設定項目は、悲観的ロックの追加をパイプライン処理で実行することを可能にします。この機能を有効にすると、TiKVはデータがロック可能であることを検出すると、直ちにTiDBに後続のリクエストの実行と悲観的ロックへの非同期書き込みを通知します。これにより、レイテンシーが大幅に削減され、悲観的トランザクションのパフォーマンスが大幅に向上します。ただし、悲観的ロックへの非同期書き込みが失敗する可能性は依然として低く、悲観的トランザクションのコミットが失敗する可能性があります。
-   デフォルト値: `true`

### <code>in-memory</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-in-memory-code-span-class-version-mark-new-in-v6-0-0-span}

-   インメモリ悲観的ロック機能を有効にします。この機能を有効にすると、悲観的トランザクションは、ロックをディスクに書き込んだり、他のレプリカに複製したりするのではなく、メモリ内にロックを保存しようとします。これにより、悲観的トランザクションのパフォーマンスが向上します。ただし、悲観的ロックが失われ、悲観的トランザクションのコミットが失敗する可能性は依然として低くなります。
-   デフォルト値: `true`
-   `in-memory` `pipelined`の値が`true`場合にのみ有効になることに注意してください。

### <code>in-memory-peer-size-limit</code> <span class="version-mark">v8.4.0 の新機能</span> {#code-in-memory-peer-size-limit-code-span-class-version-mark-new-in-v8-4-0-span}

-   リージョン内のメモリ使用量の[メモリ内悲観的ロック](/pessimistic-transaction.md#in-memory-pessimistic-lock)を制御します。この上限を超えると、TiKVは悲観的ロックを永続的に書き込みます。
-   デフォルト値: `512KiB`
-   単位: KiB|MiB|GiB

### <code>in-memory-instance-size-limit</code> <span class="version-mark">v8.4.0 の新機能</span> {#code-in-memory-instance-size-limit-code-span-class-version-mark-new-in-v8-4-0-span}

-   TiKVインスタンス[メモリ内悲観的ロック](/pessimistic-transaction.md#in-memory-pessimistic-lock)あたりのメモリ使用量の上限を制御します。この上限を超えると、TiKVは悲観的ロックを永続的に書き込みます。
-   デフォルト値: `100MiB`
-   単位: KiB|MiB|GiB

## クォータ {#quota}

クォータリミッターに関連するコンフィグレーション項目。

### <code>max-delay-duration</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-max-delay-duration-code-span-class-version-mark-new-in-v6-0-0-span}

-   単一の読み取りまたは書き込み要求がフォアグラウンドで処理されるまでに強制的に待機する最大時間。
-   デフォルト値: `500ms`
-   推奨設定：ほとんどの場合、デフォルト値を使用することをお勧めします。インスタンスでメモリ不足（OOM）やパフォーマンスの急激な変動が発生する場合は、値を1秒に設定することで、リクエストの待機時間を1秒未満に短縮できます。

### フォアグラウンドクォータリミッター {#foreground-quota-limiter}

フォアグラウンド クォータ リミッターに関連するコンフィグレーション項目。

TiKV がデプロイされているマシンのリソースが限られているとします (たとえば、CPU が 4v でメモリが16 G しかない)。このような状況では、TiKV のフォアグラウンドで処理される読み取りおよび書き込み要求が多すぎるため、バックグラウンドで使用される CPU リソースがそのような要求の処理に占有され、TiKV のパフォーマンスの安定性に影響する可能性があります。この状況を回避するには、フォアグラウンド クォータ関連の設定項目を使用して、フォアグラウンドで使用される CPU リソースを制限できます。要求が Quota Limiter をトリガーすると、その要求は TiKV が CPU リソースを解放するまでしばらく待機する必要があります。正確な待機時間は要求の数によって異なり、最大待機時間は[`max-delay-duration`](#max-delay-duration-new-in-v600)の値以下になります。

#### <code>foreground-cpu-time</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-foreground-cpu-time-code-span-class-version-mark-new-in-v6-0-0-span}

-   読み取りおよび書き込み要求を処理するために TiKV フォアグラウンドで使用される CPU リソースのソフト制限。
-   デフォルト値: `0` (制限なしを意味します)
-   単位: millicpu (たとえば、 `1500`フォアグラウンド要求が 1.5v CPU を消費することを意味します)
-   推奨設定：4コア以上のインスタンスの場合は、デフォルト値の`0`使用します。4コアのインスタンスの場合は、 `1000`から`1500`の範囲に設定するとバランスが取れます。2コアのインスタンスの場合は、 `1200`未満の値にしてください。

#### <code>foreground-write-bandwidth</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-foreground-write-bandwidth-code-span-class-version-mark-new-in-v6-0-0-span}

-   トランザクションがデータを書き込む帯域幅のソフト制限。
-   デフォルト値: `0KiB` (制限なしを意味します)
-   推奨設定：ほとんどの場合、デフォルト値の`0`を使用します。ただし、 `foreground-cpu-time`設定では書き込み帯域幅を制限するのに十分でない場合は、例外的に、コア数が4以下のインスタンスでは`50MiB`未満の値を設定することをお勧めします。

#### <code>foreground-read-bandwidth</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-foreground-read-bandwidth-code-span-class-version-mark-new-in-v6-0-0-span}

-   トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限。
-   デフォルト値: `0KiB` (制限なしを意味します)
-   推奨設定：ほとんどの場合、デフォルト値の`0`を使用しますが、 `foreground-cpu-time`設定では読み取り帯域幅を制限するのに十分でない場合は、例外的に、コア数が4以下のインスタンスでは`20MiB`未満の値を設定することをお勧めします。

### バックグラウンドクォータリミッター {#background-quota-limiter}

バックグラウンド クォータ リミッターに関連するコンフィグレーション項目。

TiKV がデプロイされているマシンのリソースが限られているとします。たとえば、4v の CPU と 16 G のメモリしかないとします。このような状況では、TiKV のバックグラウンドで処理される計算や読み取り/書き込み要求が多すぎて、フォアグラウンドで使用される CPU リソースがそのような要求の処理に占有され、TiKV のパフォーマンスの安定性に影響する可能性があります。この状況を回避するには、バックグラウンド クォータ関連の設定項目を使用して、バックグラウンドで使用される CPU リソースを制限できます。要求が Quota Limiter をトリガーすると、その要求は TiKV が CPU リソースを解放するまでしばらく待機する必要があります。正確な待機時間は要求の数によって異なり、最大待機時間は[`max-delay-duration`](#max-delay-duration-new-in-v600)の値以下になります。

> **警告：**
>
> -   バックグラウンド クォータ リミッターは、TiDB v6.2.0 で導入された実験的機能であり、本番環境での使用は推奨され**ません**。
> -   この機能は、TiKV がリソースが限られた環境で安定して動作することを保証するため、リソースが限られた環境にのみ適しています。リソースが豊富な環境でこの機能を有効にすると、リクエスト数がピークに達したときにパフォーマンスが低下する可能性があります。

#### <code>background-cpu-time</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-background-cpu-time-code-span-class-version-mark-new-in-v6-2-0-span}

-   TiKV バックグラウンドで読み取りおよび書き込み要求を処理するために使用される CPU リソースのソフト制限。
-   デフォルト値: `0` (制限なしを意味します)
-   単位: millicpu (たとえば、 `1500`バックグラウンド リクエストが 1.5v CPU を消費することを意味します)

#### <code>background-write-bandwidth</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-background-write-bandwidth-code-span-class-version-mark-new-in-v6-2-0-span}

-   バックグラウンド トランザクションがデータを書き込む帯域幅のソフト制限。
-   デフォルト値: `0KiB` (制限なしを意味します)

#### <code>background-read-bandwidth</code><span class="version-mark">幅 v6.2.0 の新機能</span> {#code-background-read-bandwidth-code-span-class-version-mark-new-in-v6-2-0-span}

-   バックグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限。
-   デフォルト値: `0KiB` (制限なしを意味します)

#### <code>enable-auto-tune</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-enable-auto-tune-code-span-class-version-mark-new-in-v6-2-0-span}

-   クォータの自動調整を有効にするかどうかを決定します。この設定項目を有効にすると、TiKVはTiKVインスタンスの負荷に基づいて、バックグラウンドリクエストのクォータを動的に調整します。
-   デフォルト値: `false` (自動調整が無効であることを意味します)

## causal-ts <span class="version-mark">v6.1.0 の新機能</span> {#causal-ts-span-class-version-mark-new-in-v6-1-0-span}

TiKV API V2が有効な場合にタイムスタンプを取得するためのコンフィグレーション項目（ `storage.api-version = 2` ）。

書き込みレイテンシーを削減するため、TiKVは定期的にタイムスタンプのバッチを取得し、ローカルにキャッシュします。キャッシュされたタイムスタンプは、PDへの頻繁なアクセスを回避し、TSOサービスの短期的な障害を許容するのに役立ちます。

### <code>alloc-ahead-buffer</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-alloc-ahead-buffer-code-span-class-version-mark-new-in-v6-4-0-span}

-   事前に割り当てられた TSO キャッシュ サイズ (期間内)。
-   TiKV がこの設定項目で指定された期間に基づいて TSO キャッシュを事前割り当てすることを示します。TiKV は前回の期間に基づいて TSO の使用量を推定し、 `alloc-ahead-buffer`満たす TSO をローカルに要求してキャッシュします。
-   この設定項目は、TiKV API V2が有効になっている場合にPD障害の許容度を高めるためによく使用されます（ `storage.api-version = 2` ）。
-   この設定項目の値を大きくすると、TiKVのTSO消費量とメモリオーバーヘッドが増加する可能性があります。十分なTSOを確保するには、PDの[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)の設定項目を減らすことをお勧めします。
-   テストによると、 `alloc-ahead-buffer`がデフォルト値の場合、PD リーダーが失敗して別のノードに切り替わると、書き込み要求のレイテンシーが短期的に増加し、QPS が減少 (約 15%) します。
-   ビジネスへの影響を回避するには、PD で`tso-update-physical-interval = "1ms"`設定し、TiKV で次の設定項目を設定します。
    -   `causal-ts.alloc-ahead-buffer = "6s"`
    -   `causal-ts.renew-batch-max-size = 65536`
    -   `causal-ts.renew-batch-min-size = 2048`
-   デフォルト値: `3s`

### <code>renew-interval</code> {#code-renew-interval-code}

-   ローカルにキャッシュされたタイムスタンプが更新される間隔。
-   `renew-interval`間隔で、TiKV はタイムスタンプ更新のバッチ処理を開始し、前回の期間のタイムスタンプ消費量と[`alloc-ahead-buffer`](#alloc-ahead-buffer-new-in-v640)の設定に応じて、キャッシュされたタイムスタンプの数を調整します。このパラメータを大きすぎる値に設定すると、最新の TiKV ワークロードの変更が時間内に反映されません。このパラメータを小さすぎる値に設定すると、PD の負荷が増加します。書き込みトラフィックの変動が激しい場合、タイムスタンプが頻繁に枯渇する場合、および書き込みレイテンシーが増加する場合は、このパラメータを小さい値に設定できます。同時に、PD の負荷も考慮する必要があります。
-   デフォルト値: `"100ms"`

### <code>renew-batch-min-size</code> {#code-renew-batch-min-size-code}

-   タイムスタンプ要求内の TSO の最小数。
-   TiKVは、前期間のタイムスタンプ消費量に応じて、キャッシュされるタイムスタンプの数を調整します。必要なTSOが少数の場合、TiKVは要求されるTSOの数を`renew-batch-min-size`に達するまで減らします。アプリケーションで大規模なバースト書き込みトラフィックが頻繁に発生する場合は、必要に応じてこのパラメータを大きく設定できます。このパラメータは、単一のtikvサーバーのキャッシュサイズであることに注意してください。パラメータを大きくしすぎると、クラスターに多数のtikvサーバーが含まれる場合、TSOの消費が急激に増加します。
-   Grafanaの**TiKV-RAW** &gt; **Causal timestamp**パネルでは、 **TSOバッチサイズ**は、アプリケーションのワークロードに応じて動的に調整された、ローカルにキャッシュされたタイムスタンプの数です。このメトリックを参照して`renew-batch-min-size`調整できます。
-   デフォルト値: `100`

### <code>renew-batch-max-size</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-renew-batch-max-size-code-span-class-version-mark-new-in-v6-4-0-span}

-   タイムスタンプ要求内の TSO の最大数。
-   デフォルトのTSO物理時間更新間隔（ `50ms` ）では、PDは最大262144個のTSOを提供します。要求されたTSOがこの数を超えると、PDはそれ以上のTSOを提供しなくなります。この設定項目は、TSOの枯渇と、TSO枯渇による他の業務への悪影響を回避するために使用されます。高可用性を向上させるためにこの設定項目の値を増やす場合は、十分なTSOを確保するために、同時に[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)の値を減らす必要があります。
-   デフォルト値: `8192`

## リソース管理 {#resource-control}

TiKVstorageレイヤーのリソース制御に関するコンフィグレーション項目。

### <code>enabled</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-enabled-code-span-class-version-mark-new-in-v6-6-0-span}

-   対応するリソースグループのいずれか[リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)に基づいて、ユーザーのフォアグラウンド読み取り/書き込み要求のスケジュールを有効にするかどうかを制御します。TiDBリソースグループとリソース制御の詳細については、 [リソース制御を使用してリソースグループの制限とフロー制御を実現する](/tidb-resource-control-ru-groups.md)参照してください。
-   この設定項目を有効にすると、TiDB で[`tidb_enable_resource_control](/system-variables.md#tidb_enable_resource_control-new-in-v660)有効になっている場合にのみ機能します。この設定項目を有効にすると、TiKV は優先度キューを使用して、フォアグラウンドユーザーからのキューに入れられた読み取り/書き込み要求をスケジュールします。要求のスケジュール優先度は、その要求を受信するリソースグループが既に消費しているリソース量に反比例し、対応するリソースグループのクォータに正比例します。
-   デフォルト値: `true` 。リソース グループの RU に基づくスケジュールが有効であることを意味します。

### <code>priority-ctl-strategy</code> <span class="version-mark">v8.4.0 の新機能</span> {#code-priority-ctl-strategy-code-span-class-version-mark-new-in-v8-4-0-span}

低優先度タスクのフロー制御戦略を指定します。TiKVは、低優先度タスクにフロー制御を適用することで、高優先度タスクの実行を優先します。

-   値のオプション:
    -   `aggressive` : このポリシーは、高優先度タスクのパフォーマンスを優先し、高優先度タスクのスループットとレイテンシーに大きな影響が及ばないようにしますが、低優先度タスクの実行速度は低下します。
    -   `moderate` : このポリシーは、低優先度のタスクにバランスの取れたフロー制御を課し、高優先度のタスクへの影響を少なくします。
    -   `conservative` : このポリシーは、システム リソースが完全に利用されることを優先し、低優先度のタスクが必要に応じてシステムの利用可能なリソースを完全に利用できるようにすることで、高優先度のタスクのパフォーマンスに大きな影響を与えます。
-   デフォルト値: `moderate` 。

## スプリット {#split}

[ロードベーススプリット](/configure-load-base-split.md)に関連するコンフィグレーション項目です。

### <code>byte-threshold</code> <span class="version-mark">v5.0 の新機能</span> {#code-byte-threshold-code-span-class-version-mark-new-in-v5-0-span}

-   リージョンがホットスポットとして識別されるトラフィックしきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size) 4 GiB 未満の場合、1 秒あたり`30MiB` 。
    -   [`region-split-size`](#region-split-size) 4 GiB 以上の場合は 1 秒あたり`100MiB`なります。

### <code>qps-threshold</code> {#code-qps-threshold-code}

-   リージョンがホットスポットとして識別される QPS しきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size) 4 GiB 未満の場合は`3000` 。
    -   [`region-split-size`](#region-split-size)が 4 GiB 以上の場合は`7000` 。

### <code>region-cpu-overload-threshold-ratio</code> <span class="version-mark">v6.2.0の新機能</span> {#code-region-cpu-overload-threshold-ratio-code-span-class-version-mark-new-in-v6-2-0-span}

-   リージョンがホットスポットとして識別される CPU 使用率のしきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size) 4 GiB 未満の場合は`0.25` 。
    -   [`region-split-size`](#region-split-size)が 4 GiB 以上の場合は`0.75` 。

## メモリ<span class="version-mark">v7.5.0 の新機能</span> {#memory-span-class-version-mark-new-in-v7-5-0-span}

### <code>enable-heap-profiling</code> <span class="version-mark">v7.5.0 の新機能</span> {#code-enable-heap-profiling-code-span-class-version-mark-new-in-v7-5-0-span}

-   TiKV のメモリ使用量を追跡するためにヒープ プロファイリングを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>profiling-sample-per-bytes</code> <span class="version-mark">v7.5.0 の新機能</span> {#code-profiling-sample-per-bytes-code-span-class-version-mark-new-in-v7-5-0-span}

-   ヒープ プロファイリングによって毎回サンプリングされるデータの量を、最も近い 2 の累乗に切り上げて指定します。
-   デフォルト値: `512KiB`

### <code>enable-thread-exclusive-arena</code><span class="version-mark">バージョン 8.1.0 の新機能</span> {#code-enable-thread-exclusive-arena-code-span-class-version-mark-new-in-v8-1-0-span}

-   各 TiKV スレッドのメモリ使用量を追跡するために、TiKV スレッド レベルでメモリ割り当てステータスを表示するかどうかを制御します。
-   デフォルト値: `true`

## インメモリエンジン<span class="version-mark">v8.5.0 の新機能</span> {#in-memory-engine-span-class-version-mark-new-in-v8-5-0-span}

storageレイヤーに関連する TiKV MVCC インメモリ エンジン (IME) 構成項目。

### <span class="version-mark">v8.5.0の新機能</span><code>enable</code> {#code-enable-code-span-class-version-mark-new-in-v8-5-0-span}

> **注記：**
>
> この構成項目は構成ファイルで構成できますが、SQL ステートメントを使用してクエリすることはできません。

-   マルチバージョンクエリを高速化するためにインメモリエンジンを有効にするかどうか。インメモリエンジンの詳細については、 [TiKV MVCC インメモリエンジン](/tikv-in-memory-engine.md)参照してください。
-   デフォルト値: `false` (メモリ内エンジンは無効)
-   TiKV ノードには少なくとも 8 GiB のメモリを構成することをお勧めします。最適なパフォーマンスを得るには 32 GiB 以上を構成してください。
-   TiKVノードの利用可能なメモリが不足している場合、この設定項目を`true`に設定しても、インメモリエンジンは有効化されません。このような場合は、TiKVログファイルで`"in-memory engine is disabled because"`を含むメッセージを確認し、インメモリエンジンが有効化されない理由を確認してください。

### <code>capacity</code> <span class="version-mark">v8.5.0 の新</span>機能 {#code-capacity-code-span-class-version-mark-new-in-v8-5-0-span}

> **注記：**
>
> -   インメモリ エンジンを有効にすると、 `block-cache.capacity`自動的に 10% 減少します。
> -   `capacity`手動で設定した場合、 `block-cache.capacity`自動的に減少しません。この場合、OOMを回避するために手動で値を調整する必要があります。

-   [TiKV MVCC インメモリエンジン](/tikv-in-memory-engine.md)が使用できる最大メモリサイズを制御します。メモリ容量によって、キャッシュできるリージョンの数が決まります。容量がいっぱいになると、インメモリエンジンはリージョンMVCCの冗長性に基づいて新しいリージョンをロードし、キャッシュされているリージョンを削除します。
-   デフォルト値: `min(10% of the total system memory, 5 GiB)`

### <code>gc-run-interval</code> <span class="version-mark">8.5.0の新機能</span> {#code-gc-run-interval-code-span-class-version-mark-new-in-v8-5-0-span}

-   インメモリエンジンGCがMVCCバージョンをキャッシュする時間間隔を制御します。このパラメータを減らすとGCの頻度が上がり、MVCCバージョンの数が減りますが、GCのCPU消費量が増加し、インメモリエンジンのキャッシュミスの可能性が高まります。
-   デフォルト値: `"3m"`

### <code>mvcc-amplification-threshold</code> <span class="version-mark">8.5.0の新機能</span> {#code-mvcc-amplification-threshold-code-span-class-version-mark-new-in-v8-5-0-span}

-   インメモリエンジンがリージョンを選択してロードする際のMVCC読み取り増幅のしきい値を制御します。デフォルト値は`10`で、リージョン内の1行の読み取りに10を超えるMVCCバージョンの処理が必要な場合、このリージョンはインメモリエンジンにロードされる可能性があることを示します。
-   デフォルト値: `10`
