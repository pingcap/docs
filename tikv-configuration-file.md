---
title: TiKV Configuration File
summary: Learn the TiKV configuration file.
---

# TiKVコンフィグレーションファイル {#tikv-configuration-file}

<!-- markdownlint-disable MD001 -->

TiKV 構成ファイルは、コマンドライン パラメーターよりも多くのオプションをサポートしています。 [etc/config-template.toml](https://github.com/tikv/tikv/blob/master/etc/config-template.toml)にデフォルトの構成ファイルがあり、名前を`config.toml`に変更できます。

このドキュメントでは、コマンド ライン パラメーターに含まれていないパラメーターについてのみ説明します。詳細については、 [コマンドライン パラメータ](/command-line-flags-for-tikv-configuration.md)を参照してください。

## グローバル構成 {#global-configuration}

### <code>abort-on-panic</code> {#code-abort-on-panic-code}

-   TiKV がパニックしたときに`abort()`を呼び出してプロセスを終了するかどうかを設定します。このオプションは、TiKV がシステムにコア ダンプ ファイルの生成を許可するかどうかに影響します。

    -   この構成項目の値が`false`の場合、TiKV がパニックになると、プロセスを終了するために`exit()`が呼び出されます。
    -   この構成項目の値が`true`の場合、TiKV がパニックになると、TiKV は`abort()`を呼び出してプロセスを終了します。現時点では、TiKV を使用すると、システムは終了時にコア ダンプ ファイルを生成できます。コア ダンプ ファイルを生成するには、コア ダンプに関連するシステム構成も実行する必要があります (たとえば、 `ulimit -c`コマンドを使用してコア ダンプ ファイルのサイズ制限を設定し、コア ダンプ パスを構成します。オペレーティング システムによって関連する構成が異なります)。 ）。コア ダンプ ファイルがディスク領域を占有しすぎて TiKV ディスク領域が不足するのを避けるために、コア ダンプ生成パスを TiKV データのディスク パーティションとは異なるディスク パーティションに設定することをお勧めします。

-   デフォルト値: `false`

### <code>slow-log-file</code> {#code-slow-log-file-code}

-   スローログを保存するファイル
-   この構成項目を設定せずに`log.file.filename`を設定すると、 `log.file.filename`で指定されたログ ファイルにスロー ログが出力されます。
-   `slow-log-file`も`log.file.filename`設定されていない場合、すべてのログはデフォルトで「stderr」に出力されます。
-   両方の設定項目が設定されている場合、通常のログは`log.file.filename`で指定されたログ ファイルに出力され、slow ログは`slow-log-file`で指定されたログ ファイルに出力されます。
-   デフォルト値: `""`

### <code>slow-log-threshold</code> {#code-slow-log-threshold-code}

-   スローログを出力するためのしきい値。処理時間がこの閾値よりも長い場合、スローログが出力されます。
-   デフォルト値: `"1s"`

### <code>memory-usage-limit</code> {#code-memory-usage-limit-code}

-   TiKV インスタンスのメモリ使用量の制限。 TiKV のメモリ使用量がこのしきい値にほぼ達すると、内部キャッシュが削除されてメモリが解放されます。
-   ほとんどの場合、TiKV インスタンスは利用可能なシステムメモリの合計の 75% を使用するように設定されているため、この構成項目を明示的に指定する必要はありません。メモリの残りの 25% は、OS ページ キャッシュ用に予約されています。詳細は[`storage.block-cache.capacity`](#capacity)を参照してください。
-   1 台の物理マシンに複数の TiKV ノードをデプロイする場合でも、この構成項目を設定する必要はありません。この場合、TiKV インスタンスは`5/3 * block-cache.capacity`のメモリを使用します。
-   異なるシステムメモリ容量のデフォルト値は次のとおりです。

    -   system=8G block-cache=3.6G memory-usage-limit=6G page-cache=2G
    -   system=16G block-cache=7.2G memory-usage-limit=12G page-cache=4G
    -   system=32G block-cache=14.4G memory-usage-limit=24G page-cache=8G

## ログ<span class="version-mark">v5.4.0 の新機能</span> {#log-span-class-version-mark-new-in-v5-4-0-span}

-   ログに関するコンフィグレーション項目です。

-   v5.4.0 から、TiKV と TiDB のログ構成項目を一致させるために、TiKV は以前の構成項目`log-rotation-timespan`を廃止し、 `log-level` 、 `log-format` 、 `log-file` 、 `log-rotation-size`を次のように変更します。古い構成アイテムのみを設定し、それらの値がデフォルト以外の値に設定されている場合、古いアイテムは新しいアイテムと互換性があります。新旧両方の構成項目が設定されている場合、新しい項目が有効になります。

### <code>level</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-level-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログレベル
-   オプションの値: `"debug"` 、 `"info"` 、 `"warn"` 、 `"error"` 、 `"fatal"`
-   デフォルト値: `"info"`

### <code>format</code> <span class="version-mark">v5.4.0 の新</span>機能 {#code-format-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログ形式
-   オプションの値: `"json"` 、 `"text"`
-   デフォルト値: `"text"`

### <code>enable-timestamp</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-enable-timestamp-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログのタイムスタンプを有効にするか無効にするかを決定します
-   オプションの値: `true` 、 `false`
-   デフォルト値: `true`

## log.file <span class="version-mark">v5.4.0 の新機能</span> {#log-file-span-class-version-mark-new-in-v5-4-0-span}

-   ログファイルに関するコンフィグレーション項目です。

### <code>filename</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-filename-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログファイル。この設定項目が設定されていない場合、デフォルトで「stderr」にログが出力されます。この設定項目が設定されている場合、ログは対応するファイルに出力されます。
-   デフォルト値: `""`

### <span class="version-mark">v5.4.0 の新</span><code>max-size</code> {#code-max-size-code-span-class-version-mark-new-in-v5-4-0-span}

-   1 つのログ ファイルの最大サイズ。ファイル サイズがこの構成項目で設定された値よりも大きい場合、システムは単一のファイルを複数のファイルに自動的に分割します。
-   デフォルト値: `300`
-   最大値: `4096`
-   単位：MiB

### <span class="version-mark">v5.4.0 の新</span><code>max-days</code> {#code-max-days-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKV がログ ファイルを保持する最大日数。
    -   構成項目が設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKV はログ ファイルを消去しません。
    -   パラメータが`0`以外の値に設定されている場合、TiKV は`max-days`の後に期限切れのログ ファイルをクリーンアップします。
-   デフォルト値: `0`

### <code>max-backups</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-max-backups-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKV が保持するログ ファイルの最大数。
    -   構成項目が設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKV はすべてのログ ファイルを保持します。
    -   構成項目が`0`以外の値に設定されている場合、TiKV は最大で`max-backups`で指定された数の古いログ ファイルを保持します。たとえば、値が`7`に設定されている場合、TiKV は最大 7 つの古いログ ファイルを保持します。
-   デフォルト値: `0`

### <code>pd.enable-forwarding</code> <span class="version-mark">v5.0.0 の新機能</span> {#code-pd-enable-forwarding-code-span-class-version-mark-new-in-v5-0-0-span}

-   ネットワーク分離の可能性がある場合に、TiKV の PD クライアントがフォロワー経由でリーダーにリクエストを転送するかどうかを制御します。
-   デフォルト値: `false`
-   環境でネットワークが分離されている可能性がある場合、このパラメーターを有効にすると、サービスが利用できなくなる期間を短縮できます。
-   分離、ネットワークの中断、またはダウンタイムが発生したかどうかを正確に判断できない場合、このメカニズムを使用すると判断を誤るリスクがあり、可用性とパフォーマンスが低下します。ネットワーク障害が発生したことがない場合は、このパラメーターを有効にすることはお勧めしません。

## サーバー {#server}

-   サーバーに関連するコンフィグレーション項目。

### <code>addr</code> {#code-addr-code}

-   リスニング IP アドレスとリスニング ポート
-   デフォルト値: `"127.0.0.1:20160"`

### <code>advertise-addr</code> {#code-advertise-addr-code}

-   クライアント通信用のリッスン アドレスをアドバタイズする
-   この構成項目が設定されていない場合、値`addr`が使用されます。
-   デフォルト値: `""`

### <code>status-addr</code> {#code-status-addr-code}

-   構成アイテムは、 `HTTP`アドレスを介して直接 TiKV ステータスを報告します

    > **警告：**
    >
    > この値が公開されると、TiKVサーバーのステータス情報が漏洩する可能性があります。

-   ステータス アドレスを無効にするには、値を`""`に設定します。

-   デフォルト値: `"127.0.0.1:20180"`

### <code>status-thread-pool-size</code> {#code-status-thread-pool-size-code}

-   `HTTP` API サービスのワーカー スレッドの数
-   デフォルト値: `1`
-   最小値: `1`

### <code>grpc-compression-type</code> {#code-grpc-compression-type-code}

-   gRPC メッセージの圧縮アルゴリズム
-   オプションの値: `"none"` 、 `"deflate"` 、 `"gzip"`
-   デフォルト値: `"none"`

### <code>grpc-concurrency</code> {#code-grpc-concurrency-code}

-   gRPC ワーカー スレッドの数。 gRPC スレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `5`
-   最小値: `1`

### <code>grpc-concurrent-stream</code> {#code-grpc-concurrent-stream-code}

-   gRPC ストリームで許可される同時リクエストの最大数
-   デフォルト値: `1024`
-   最小値: `1`

### <code>grpc-memory-pool-quota</code> {#code-grpc-memory-pool-quota-code}

-   gRPC で使用できるメモリサイズを制限します
-   デフォルト値: 制限なし
-   OOM が観察された場合に備えてメモリを制限します。使用を制限すると、潜在的な失速につながる可能性があることに注意してください

### <code>grpc-raft-conn-num</code> {#code-grpc-raft-conn-num-code}

-   Raft通信用の TiKV ノード間のリンクの最大数
-   デフォルト値: `1`
-   最小値: `1`

### <code>max-grpc-send-msg-len</code> {#code-max-grpc-send-msg-len-code}

-   送信できる gRPC メッセージの最大長を設定します
-   デフォルト値: `10485760`
-   単位: バイト
-   最大値: `2147483647`

### <code>grpc-stream-initial-window-size</code> {#code-grpc-stream-initial-window-size-code}

-   gRPC ストリームのウィンドウ サイズ
-   デフォルト値: `2MB`
-   単位: KB|MB|GB
-   最小値: `"1KB"`

### <code>grpc-keepalive-time</code> {#code-grpc-keepalive-time-code}

-   その gRPC が`keepalive` Ping メッセージを送信する時間間隔
-   デフォルト値: `"10s"`
-   最小値: `"1s"`

### <code>grpc-keepalive-timeout</code> {#code-grpc-keepalive-timeout-code}

-   gRPC ストリームのタイムアウトを無効にします
-   デフォルト値: `"3s"`
-   最小値: `"1s"`

### <code>concurrent-send-snap-limit</code> {#code-concurrent-send-snap-limit-code}

-   同時に送信されるスナップショットの最大数
-   デフォルト値: `32`
-   最小値: `1`

### <code>concurrent-recv-snap-limit</code> {#code-concurrent-recv-snap-limit-code}

-   同時に受信するスナップショットの最大数
-   デフォルト値: `32`
-   最小値: `1`

### <code>end-point-recursion-limit</code> {#code-end-point-recursion-limit-code}

-   TiKV がコプロセッサーDAG 式をデコードするときに許可される再帰レベルの最大数
-   デフォルト値: `1000`
-   最小値: `1`

### <code>end-point-request-max-handle-duration</code> {#code-end-point-request-max-handle-duration-code}

-   タスクを処理するための TiDB の TiKV へのプッシュダウン要求に許可される最長期間
-   デフォルト値: `"60s"`
-   最小値: `"1s"`

### <code>snap-max-write-bytes-per-sec</code> {#code-snap-max-write-bytes-per-sec-code}

-   スナップショット処理時の最大許容ディスク帯域幅
-   デフォルト値: `"100MB"`
-   単位: KB|MB|GB
-   最小値: `"1KB"`

### <code>enable-request-batch</code> {#code-enable-request-batch-code}

-   リクエストをバッチで処理するかどうかを決定します
-   デフォルト値: `true`

### <code>labels</code> {#code-labels-code}

-   `{ zone = "us-west-1", disk = "ssd" }`などのサーバー属性を指定します。
-   デフォルト値: `{}`

### <code>background-thread-count</code> {#code-background-thread-count-code}

-   エンドポイント スレッド、 BRスレッド、分割チェック スレッド、リージョンスレッド、その他の遅延の影響を受けないタスクのスレッドを含む、バックグラウンド プールの作業スレッド数。
-   デフォルト値: CPU コア数が 16 未満の場合、デフォルト値は`2`です。それ以外の場合、デフォルト値は`3`です。

### <code>end-point-slow-log-threshold</code> {#code-end-point-slow-log-threshold-code}

-   TiDB のプッシュダウン リクエストがスロー ログを出力する時間のしきい値。処理時間がこの閾値よりも長い場合、スローログが出力されます。
-   デフォルト値: `"1s"`
-   最小値: `0`

### <code>raft-client-queue-size</code> {#code-raft-client-queue-size-code}

-   TiKV のRaftメッセージのキュー サイズを指定します。時間内に送信されなかったメッセージが多すぎてバッファがいっぱいになったり、メッセージが破棄されたりする場合は、より大きな値を指定してシステムの安定性を向上させることができます。
-   デフォルト値: `8192`

### <code>simplify-metrics</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-simplify-metrics-code-span-class-version-mark-new-in-v6-2-0-span}

-   返されたモニタリング メトリックを単純化するかどうかを指定します。値を`true`に設定すると、TiKV は一部のメトリックを除外することで、各リクエストに対して返されるデータの量を減らします。
-   デフォルト値: `false`

### <code>forward-max-connections-per-address</code> <span class="version-mark">v5.0.0 の新機能</span> {#code-forward-max-connections-per-address-code-span-class-version-mark-new-in-v5-0-0-span}

-   サーバーへのサービスおよび転送要求の接続プールのサイズを設定します。小さすぎる値に設定すると、リクエストのレイテンシーと負荷分散に影響します。
-   デフォルト値: `4`

## readpool.unified {#readpool-unified}

読み取り要求を処理する単一のスレッド プールに関連するコンフィグレーション項目。このスレッド プールは、4.0 バージョン以降、元のstorageスレッド プールとコプロセッサ スレッド プールに取って代わります。

### <code>min-thread-count</code> {#code-min-thread-count-code}

-   統合読み取りプールの最小作業スレッド数
-   デフォルト値: `1`

### <code>max-thread-count</code> {#code-max-thread-count-code}

-   統合読み取りプールまたは UnifyReadPool スレッド プールの最大作業スレッド数。このスレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   値の範囲: `[min-thread-count, MAX(4, CPU quota * 10)]` 。 `MAX(4, CPU quota * 10)` `4`と`CPU quota * 10`のうち大きい方の値を取ります。
-   デフォルト値: MAX(4, CPU * 0.8)

> **ノート：**
>
> スレッド数を増やすと、コンテキストの切り替えが多くなり、パフォーマンスが低下する可能性があります。この構成項目の値を変更することはお勧めしません。

### <code>stack-size</code> {#code-stack-size-code}

-   統合スレッド プール内のスレッドのスタック サイズ
-   タイプ: 整数 + 単位
-   デフォルト値: `"10MB"`
-   単位: KB|MB|GB
-   最小値: `"2MB"`
-   最大値：システムで実行された`ulimit -sH`コマンドの結果として出力される K バイト数。

### <code>max-tasks-per-worker</code> {#code-max-tasks-per-worker-code}

-   統合読み取りプール内の 1 つのスレッドに許可されるタスクの最大数。値を超えた場合は`Server Is Busy`を返します。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>auto-adjust-pool-size</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-auto-adjust-pool-size-code-span-class-version-mark-new-in-v6-3-0-span}

-   スレッド プール サイズを自動的に調整するかどうかを制御します。有効にすると、現在の CPU 使用率に基づいて UnifyReadPool スレッド プール サイズを自動的に調整することで、TiKV の読み取りパフォーマンスが最適化されます。スレッドプールの可能な範囲は`[max-thread-count, MAX(4, CPU)]`です。最大値は[`max-thread-count`](#max-thread-count)の値と同じです。
-   デフォルト値: `false`

## 読み取りプール。storage {#readpool-storage}

storageスレッド プールに関連するコンフィグレーションアイテム。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   storage要求に統合スレッド プール ( [`readpool.unified`](#readpoolunified)で構成) を使用するかどうかを決定します。このパラメーターの値が`false`の場合、別のスレッド プールが使用されます。これは、このセクションの残りのパラメーター ( `readpool.storage` ) によって構成されます。
-   デフォルト値: このセクション ( `readpool.storage` ) に他の構成がない場合、デフォルト値は`true`です。それ以外の場合、下位互換性のために、デフォルト値は`false`です。このオプションを有効にする前に、必要に応じて[`readpool.unified`](#readpoolunified)の構成を変更してください。

### <code>high-concurrency</code> {#code-high-concurrency-code}

-   高優先度`read`要求を処理する同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>normal-concurrency</code> {#code-normal-concurrency-code}

-   通常優先度`read`要求を処理する同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>low-concurrency</code> {#code-low-concurrency-code}

-   低優先度`read`要求を処理する同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>max-tasks-per-worker-high</code> {#code-max-tasks-per-worker-high-code}

-   優先度の高いスレッド プール内の 1 つのスレッドに許可されるタスクの最大数。値を超えた場合は`Server Is Busy`を返します。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-normal</code> {#code-max-tasks-per-worker-normal-code}

-   標準優先度のスレッド プール内の 1 つのスレッドに許可されるタスクの最大数。値を超えた場合は`Server Is Busy`を返します。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-low</code> {#code-max-tasks-per-worker-low-code}

-   優先度の低いスレッド プール内の 1 つのスレッドに許可されるタスクの最大数。値を超えた場合は`Server Is Busy`を返します。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>stack-size</code> {#code-stack-size-code}

-   ストレージ読み取りスレッド プール内のスレッドのスタック サイズ
-   タイプ: 整数 + 単位
-   デフォルト値: `"10MB"`
-   単位: KB|MB|GB
-   最小値: `"2MB"`
-   最大値：システムで実行された`ulimit -sH`コマンドの結果として出力される K バイト数。

## <code>readpool.coprocessor</code> {#code-readpool-coprocessor-code}

コプロセッサースレッド プールに関連するコンフィグレーション項目。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   コプロセッサー要求に統合スレッド・プール ( [`readpool.unified`](#readpoolunified)で構成) を使用するかどうかを決定します。このパラメーターの値が`false`の場合、別のスレッド プールが使用されます。これは、このセクションの残りのパラメーター ( `readpool.coprocessor` ) によって構成されます。
-   デフォルト値: このセクションのパラメーター ( `readpool.coprocessor` ) が設定されていない場合、デフォルト値は`true`です。それ以外の場合、下位互換性のためにデフォルト値は`false`です。このパラメータを有効にする前に、 [`readpool.unified`](#readpoolunified)の設定項目を調整してください。

### <code>high-concurrency</code> {#code-high-concurrency-code}

-   チェックポイントなどの優先度の高いコプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>normal-concurrency</code> {#code-normal-concurrency-code}

-   通常優先度のコプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>low-concurrency</code> {#code-low-concurrency-code}

-   テーブルスキャンなどの優先度の低いコプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>max-tasks-per-worker-high</code> {#code-max-tasks-per-worker-high-code}

-   優先順位の高いスレッド プール内の 1 つのスレッドに許可されるタスクの数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-normal</code> {#code-max-tasks-per-worker-normal-code}

-   標準優先度のスレッド プールで 1 つのスレッドに許可されるタスクの数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-low</code> {#code-max-tasks-per-worker-low-code}

-   優先順位の低いスレッド プール内の 1 つのスレッドに許可されるタスクの数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>stack-size</code> {#code-stack-size-code}

-   コプロセッサー・スレッド・プール内のスレッドのスタック・サイズ
-   タイプ: 整数 + 単位
-   デフォルト値: `"10MB"`
-   単位: KB|MB|GB
-   最小値: `"2MB"`
-   最大値：システムで実行された`ulimit -sH`コマンドの結果として出力される K バイト数。

## storage {#storage}

storageに関するコンフィグレーション項目。

### <code>data-dir</code> {#code-data-dir-code}

-   RocksDB ディレクトリのstorageパス
-   デフォルト値: `"./"`

### <code>scheduler-concurrency</code> {#code-scheduler-concurrency-code}

-   キーの同時操作を防止する内蔵メモリロック機構。各キーには、異なるスロットにハッシュがあります。
-   デフォルト値: `524288`
-   最小値: `1`

### <code>scheduler-worker-pool-size</code> {#code-scheduler-worker-pool-size-code}

-   スケジューラ スレッド プール内のスレッドの数。スケジューラ スレッドは、主にデータ書き込み前のトランザクションの一貫性をチェックするために使用されます。 CPU コアの数が`16`以上の場合、デフォルト値は`8`です。それ以外の場合、デフォルト値は`4`です。スケジューラ スレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `4`
-   値の範囲: `[1, MAX(4, CPU)]` 。 `MAX(4, CPU)`で、 `CPU` CPU コアの数を意味します。 `MAX(4, CPU)` `4`と`CPU`のうち大きい方の値を取ります。

### <code>scheduler-pending-write-threshold</code> {#code-scheduler-pending-write-threshold-code}

-   書き込みキューの最大サイズ。この値を超えると、TiKV への新しい書き込みに対して`Server Is Busy`エラーが返されます。
-   デフォルト値: `"100MB"`
-   単位: MB|GB

### <code>enable-async-apply-prewrite</code> {#code-enable-async-apply-prewrite-code}

-   事前書き込みリクエストを適用する前に、Async Commit トランザクションが TiKV クライアントに応答するかどうかを決定します。この構成項目を有効にすると、適用時間が長い場合はレイテンシーを簡単に減らすことができ、適用時間が安定しない場合は遅延ジッターを減らすことができます。
-   デフォルト値: `false`

### <code>reserve-space</code> {#code-reserve-space-code}

-   TiKV が開始されると、ディスク保護としてディスク上にいくらかのスペースが確保されます。残りのディスク容量が予約容量よりも少ない場合、TiKV は一部の書き込み操作を制限します。予約領域は 2 つの部分に分けられます。予約領域の 80% は、ディスク領域が不足している場合に操作に必要な追加のディスク領域として使用され、残りの 20% は一時ファイルを格納するために使用されます。スペースを再利用するプロセスで、余分なディスク スペースを使用しすぎてstorageが使い果たされた場合、この一時ファイルは、サービスを復元するための最後の保護として機能します。
-   一時ファイルの名前は`space_placeholder_file`で、 `storage.data-dir`ディレクトリにあります。ディスク容量が不足して TiKV がオフラインになった場合、TiKV を再起動すると、一時ファイルは自動的に削除され、TiKV は容量を再利用しようとします。
-   残りのスペースが不足している場合、TiKV は一時ファイルを作成しません。保護の有効性は、予約済みスペースのサイズに関連しています。予約領域のサイズは、ディスク容量の 5% とこの構成値の間の大きい方の値です。この構成項目の値が`"0MB"`の場合、TiKV はこのディスク保護機能を無効にします。
-   デフォルト値: `"5GB"`
-   単位: MB|GB

### <code>enable-ttl</code> {#code-enable-ttl-code}

> **警告：**
>
> -   新しい TiKV クラスターをデプロイする**場合にのみ、** `enable-ttl`から`true`または`false`を設定します。既存の TiKV クラスターでこの構成項目の値を変更<strong>しないでください</strong>。異なる`enable-ttl`値を持つ TiKV クラスターは、異なるデータ形式を使用します。したがって、既存の TiKV クラスターでこの項目の値を変更すると、クラスターはデータをさまざまな形式で保存し、TiKV クラスターを再起動するときに「非 ttl で TTL を有効にできません」というエラーが発生します。
> -   TiKV クラスター**でのみ**`enable-ttl`を使用します。 TiDB ノードを持つクラスターでは、この構成項目を使用し<strong>ないでください</strong>(そのようなクラスターでは`enable-ttl`から`true`を設定することを意味します)。そうしないと、データの破損や TiDB クラスターのアップグレードの失敗などの重大な問題が発生します。

-   TTL は「Time to live」の略です。この項目を有効にすると、TiKV は TTL に達したデータを自動的に削除します。 TTL の値を設定するには、クライアント経由でデータを書き込むときにリクエストで指定する必要があります。 TTL が指定されていない場合、TiKV は対応するデータを自動的に削除しないことを意味します。
-   デフォルト値: `false`

### <code>ttl-check-poll-interval</code> {#code-ttl-check-poll-interval-code}

-   物理スペースを再利用するためにデータをチェックする間隔。データが TTL に達すると、TiKV はチェック中に物理スペースを強制的に解放します。
-   デフォルト値: `"12h"`
-   最小値: `"0s"`

### <code>background-error-recovery-window</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-background-error-recovery-window-code-span-class-version-mark-new-in-v6-1-0-span}

-   RocksDB が回復可能なバックグラウンド エラーを検出した後、TiKV が回復するまでの最大許容時間。一部のバックグラウンド SST ファイルが破損している場合、RocksDB は、破損した SST ファイルが属するピアを特定した後、ハートビートを介して PD に報告します。その後、PD はスケジューリング操作を実行して、このピアを削除します。最後に、破損した SST ファイルが直接削除され、TiKV バックグラウンドが再び正常に機能するようになります。
-   破損した SST ファイルは、リカバリが完了するまでまだ存在します。この間、RocksDB はデータの書き込みを続行できますが、データの破損した部分を読み取るとエラーが報告されます。
-   この時間内にリカバリが完了しない場合、TiKV はpanicになります。
-   デフォルト値: 1h

### <code>api-version</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-api-version-code-span-class-version-mark-new-in-v6-1-0-span}

-   TiKV が RawKV ストアとして機能するときに TiKV が使用するstorage形式とインターフェイス バージョン。
-   値のオプション:
    -   `1` : API V1 を使用し、クライアントから渡されたデータをエンコードせず、データをそのまま格納します。 v6.1.0 より前のバージョンでは、TiKV はデフォルトで API V1 を使用します。
    -   `2` : API V2 を使用:
        -   データは Multi-Version Concurrency Control (MVCC) 形式で保存され、タイムスタンプは tikv-server によって PD (TSO) から取得されます。
        -   データはさまざまな用途に応じてスコープが設定され、API V2 は、単一のクラスター内での TiDB、トランザクション KV、および RawKV アプリケーションの共存をサポートします。
        -   API V2 を使用する場合は、同時に`storage.enable-ttl = true`を設定する必要があります。 API V2 は TTL 機能をサポートしているため、 `enable-ttl`明示的にオンにする必要があります。そうしないと、 `storage.enable-ttl`デフォルトで`false`になるため、競合が発生します。
        -   API V2 が有効になっている場合は、少なくとも 1 つの tidb-server インスタンスをデプロイして、古いデータを再利用する必要があります。この tidb-server インスタンスは、読み取りサービスと書き込みサービスを同時に提供できます。高可用性を確保するために、複数の tidb-server インスタンスをデプロイできます。
        -   API V2 にはクライアント サポートが必要です。詳細については、API V2 のクライアントの対応する命令を参照してください。
        -   v6.2.0 以降、RawKV の変更データ キャプチャ (CDC) がサポートされています。 [RawKV CDC](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc)を参照してください。
-   デフォルト値: `1`

> **警告：**

> -   API V1 と API V2 では、storage形式が異なります。 TiKV に TiDB データのみが含まれている場合に**のみ**、API V2 を直接有効または無効にできます。他のシナリオでは、新しいクラスターをデプロイし、 [RawKV のバックアップと復元](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)使用してデータを移行する必要があります。
> -   API V2 が有効になった後、TiKV クラスターを v6.1.0 より前のバージョンにダウングレードする**ことはできません**。そうしないと、データが破損する可能性があります。

## storage.block-cache {#storage-block-cache}

複数の RocksDBカラムファミリー (CF) 間でのブロックキャッシュの共有に関連するコンフィグレーション項目。これらの構成項目を有効にすると、カラムファミリーごとに個別に構成されたブロックキャッシュが無効になります。

### <code>shared</code> {#code-shared-code}

-   ブロックキャッシュの共有を有効または無効にします。
-   デフォルト値: `true`

### <code>capacity</code> {#code-capacity-code}

-   共有ブロックキャッシュのサイズ。
-   デフォルト値: 合計システムメモリのサイズの 45%
-   単位: KB|MB|GB

## storage.flow-control {#storage-flow-control}

TiKVにおけるフロー制御機構に関するコンフィグレーション項目です。このメカニズムは、RocksDB の書き込みストール メカニズムに取って代わり、Raftstoreレイヤーでフローを制御します。

### <code>enable</code> {#code-enable-code}

-   フロー制御メカニズムを有効にするかどうかを決定します。有効にすると、TiKV は KvDB の書き込みストール メカニズムと RaftDB の書き込みストール メカニズム (memtable を除く) を自動的に無効にします。
-   デフォルト値: `true`

### <code>memtables-threshold</code> {#code-memtables-threshold-code}

-   kvDB memtables の数がこのしきい値に達すると、フロー制御メカニズムが機能し始めます。 `enable`が`true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).max-write-buffer-number`をオーバーライドします。
-   デフォルト値: `5`

### <code>l0-files-threshold</code> {#code-l0-files-threshold-code}

-   kvDB L0 ファイルの数がこのしきい値に達すると、フロー制御メカニズムが機能し始めます。 `enable`が`true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).level0-slowdown-writes-trigger`をオーバーライドします。
-   デフォルト値: `20`

### <code>soft-pending-compaction-bytes-limit</code> {#code-soft-pending-compaction-bytes-limit-code}

-   KvDB の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムは一部の書き込み要求を拒否し始め、 `ServerIsBusy`エラーを報告します。 `enable`が`true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).soft-pending-compaction-bytes-limit`をオーバーライドします。
-   デフォルト値: `"192GB"`

### <code>hard-pending-compaction-bytes-limit</code> {#code-hard-pending-compaction-bytes-limit-code}

-   KvDB の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し、 `ServerIsBusy`エラーを報告します。 `enable`が`true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`をオーバーライドします。
-   デフォルト値: `"1024GB"`

## storage.io-rate-limit {#storage-io-rate-limit}

I/Oレートリミッターに関するコンフィグレーション項目です。

### <code>max-bytes-per-sec</code> {#code-max-bytes-per-sec-code}

-   サーバーが1 秒間にディスクに書き込みまたはディスクから読み取ることができる最大 I/O バイトを制限します (以下の`mode`の構成項目によって決定されます)。この制限に達すると、TiKV はフォアグラウンド操作よりもバックグラウンド操作を調整することを優先します。この構成項目の値は、ディスクの最適な I/O 帯域幅 (たとえば、クラウド ディスク ベンダーによって指定された最大 I/O 帯域幅) に設定する必要があります。この構成値がゼロに設定されている場合、ディスク I/O 操作は制限されません。
-   デフォルト値: `"0MB"`

### <code>mode</code> {#code-mode-code}

-   どのタイプの I/O 操作がカウントされ、しきい値`max-bytes-per-sec`未満に抑制されるかを決定します。現在、書き込み専用モードのみがサポートされています。
-   値のオプション: `"read-only"` 、 `"write-only"` 、および`"all-io"`
-   デフォルト値: `"write-only"`

## pd {#pd}

### <code>endpoints</code> {#code-endpoints-code}

-   PD のエンドポイント。複数のエンドポイントを指定する場合は、カンマで区切る必要があります。
-   デフォルト値: `["127.0.0.1:2379"]`

### <code>retry-interval</code> {#code-retry-interval-code}

-   PD 接続の初期化を再試行する間隔
-   デフォルト値: `"300ms"`

### <code>retry-log-every</code> {#code-retry-log-every-code}

-   クライアントがエラーを観察したときに、PD クライアントがエラーの報告をスキップする頻度を指定します。たとえば、値が`5`の場合、PD クライアントがエラーを観察した後、クライアントは 4 回ごとにエラーの報告をスキップし、5 回ごとにエラーを報告します。
-   この機能を無効にするには、値を`1`に設定します。
-   デフォルト値: `10`

### <code>retry-max-count</code> {#code-retry-max-count-code}

-   PD 接続の初期化を再試行する最大回数
-   再試行を無効にするには、その値を`0`に設定します。再試行回数の制限を解除するには、値を`-1`に設定します。
-   デフォルト値: `-1`

## いかだ屋 {#raftstore}

Raftstoreに関連するコンフィグレーション項目。

### <code>prevote</code> {#code-prevote-code}

-   `prevote`を有効または無効にします。この機能を有効にすると、ネットワーク パーティションから回復した後のシステムのジッターを減らすのに役立ちます。
-   デフォルト値: `true`

### <code>capacity</code> {#code-capacity-code}

-   データを保存できる最大サイズであるstorage容量。 `capacity`を指定しない場合、現在のディスクの容量が優先されます。複数の TiKV インスタンスを同じ物理ディスクにデプロイするには、このパラメーターを TiKV 構成に追加します。詳細については、 [ハイブリッド展開の主要なパラメーター](/hybrid-deployment-topology.md#key-parameters)を参照してください。
-   デフォルト値: `0`
-   単位: KB|MB|GB

### <code>raftdb-path</code> {#code-raftdb-path-code}

-   デフォルトでは`storage.data-dir/raft`であるRaftライブラリへのパス
-   デフォルト値: `""`

### <code>raft-base-tick-interval</code> {#code-raft-base-tick-interval-code}

> **ノート：**
>
> この構成項目は、SQL ステートメントを介して照会することはできませんが、構成ファイルで構成できます。

-   Raftステート マシンが動作する時間間隔
-   デフォルト値: `"1s"`
-   最小値: `0`より大きい

### <code>raft-heartbeat-ticks</code> {#code-raft-heartbeat-ticks-code}

> **ノート：**
>
> この構成項目は、SQL ステートメントを介して照会することはできませんが、構成ファイルで構成できます。

-   ハートビートが送信されたときに通過したティックの数。これは、ハートビートが`raft-base-tick-interval` * `raft-heartbeat-ticks`の時間間隔で送信されることを意味します。
-   デフォルト値: `2`
-   最小値: `0`より大きい

### <code>raft-election-timeout-ticks</code> {#code-raft-election-timeout-ticks-code}

> **ノート：**
>
> この構成項目は、SQL ステートメントを介して照会することはできませんが、構成ファイルで構成できます。

-   Raft選択が開始されたときに渡されたティックの数。これは、 Raftグループにリーダーがいない場合、約`raft-base-tick-interval` * `raft-election-timeout-ticks`の時間間隔の後にリーダー選出が開始されることを意味します。
-   デフォルト値: `10`
-   最小値: `raft-heartbeat-ticks`

### <code>raft-min-election-timeout-ticks</code> {#code-raft-min-election-timeout-ticks-code}

> **ノート：**
>
> この構成項目は、SQL ステートメントを介して照会することはできませんが、構成ファイルで構成できます。

-   Raft選択が開始されるティックの最小数。数値が`0`の場合、値`raft-election-timeout-ticks`が使用されます。このパラメーターの値は`raft-election-timeout-ticks`以上でなければなりません。
-   デフォルト値: `0`
-   最小値: `0`

### <code>raft-max-election-timeout-ticks</code> {#code-raft-max-election-timeout-ticks-code}

> **ノート：**
>
> この構成項目は、SQL ステートメントを介して照会することはできませんが、構成ファイルで構成できます。

-   Raft選択が開始されるティックの最大数。数値が`0`の場合、 `raft-election-timeout-ticks` * `2`の値が使用されます。
-   デフォルト値: `0`
-   最小値: `0`

### <code>raft-max-size-per-msg</code> {#code-raft-max-size-per-msg-code}

> **ノート：**
>
> この構成項目は、SQL ステートメントを介して照会することはできませんが、構成ファイルで構成できます。

-   1 つのメッセージ パケットのサイズに対するソフト リミット
-   デフォルト値: `"1MB"`
-   最小値: `0`より大きい
-   最大値: `3GB`
-   単位: KB|MB|GB

### <code>raft-max-inflight-msgs</code> {#code-raft-max-inflight-msgs-code}

> **ノート：**
>
> この構成項目は、SQL ステートメントを介して照会することはできませんが、構成ファイルで構成できます。

-   確認するRaftログの数。この数を超えると、 Raftステート マシンはログの送信を遅くします。
-   デフォルト値: `256`
-   最小値: `0`より大きい
-   最大値: `16384`

### <code>raft-entry-max-size</code> {#code-raft-entry-max-size-code}

-   1 つのログの最大サイズのハード リミット
-   デフォルト値: `"8MB"`
-   最小値: `0`
-   単位: MB|GB

### <code>raft-log-compact-sync-interval</code> <span class="version-mark">v5.3 の新機能</span> {#code-raft-log-compact-sync-interval-code-span-class-version-mark-new-in-v5-3-span}

-   不要なRaftログを圧縮する時間間隔
-   デフォルト値: `"2s"`
-   最小値: `"0s"`

### <code>raft-log-gc-tick-interval</code> {#code-raft-log-gc-tick-interval-code}

-   Raftログを削除するポーリング タスクがスケジュールされる時間間隔。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"3s"`
-   最小値: `"0s"`

### <code>raft-log-gc-threshold</code> {#code-raft-log-gc-threshold-code}

-   残りのRaftログの最大許容数のソフト リミット
-   デフォルト値: `50`
-   最小値: `1`

### <code>raft-log-gc-count-limit</code> {#code-raft-log-gc-count-limit-code}

-   残りのRaftログの許容数のハード リミット
-   デフォルト値：3/4リージョンサイズに収まるログ数（1ログあたり1MBとして計算）
-   最小値: `0`

### <code>raft-log-gc-size-limit</code> {#code-raft-log-gc-size-limit-code}

-   残りのRaftログの許容サイズのハード リミット
-   デフォルト値:リージョンサイズの 3/4
-   最小値: `0`より大きい

### <code>raft-log-reserve-max-ticks</code> <span class="version-mark">v5.3 の新機能</span> {#code-raft-log-reserve-max-ticks-code-span-class-version-mark-new-in-v5-3-span}

-   この構成項目で設定されたティック数が経過した後、残りのRaftログの数が`raft-log-gc-threshold`で設定された値に達しない場合でも、TiKV はこれらのログに対してガベージコレクション(GC) を実行します。
-   デフォルト値: `6`
-   最小値: `0`より大きい

### <code>raft-engine-purge-interval</code> {#code-raft-engine-purge-interval-code}

-   古い TiKV ログ ファイルをパージしてディスク領域をできるだけ早くリサイクルする間隔。 Raftエンジンは交換可能なコンポーネントであるため、一部の実装ではパージ プロセスが必要です。
-   デフォルト値: `"10s"`

### <code>raft-entry-cache-life-time</code> {#code-raft-entry-cache-life-time-code}

-   メモリ内のログ キャッシュに許可される最大残り時間
-   デフォルト値: `"30s"`
-   最小値: `0`

### <code>hibernate-regions</code> {#code-hibernate-regions-code}

-   Hibernate リージョンを有効または無効にします。このオプションを有効にすると、長時間アイドル状態のリージョンが自動的に休止状態に設定されます。これにより、アイドル状態のリージョンのRaftリーダーとフォロワーの間のハートビートメッセージによって引き起こされる余分なオーバーヘッドが削減されます。 `peer-stale-state-check-interval`を使用して、休止状態のリージョンのリーダーとフォロワーの間のハートビート間隔を変更できます。
-   デフォルト値: v5.0.2 以降のバージョンでは`true` 。 v5.0.2 より前のバージョンでは`false`

### <code>split-region-check-tick-interval</code> {#code-split-region-check-tick-interval-code}

-   リージョン分割が必要かどうかを確認する間隔を指定します。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"10s"`
-   最小値: `0`

### <code>region-split-check-diff</code> {#code-region-split-check-diff-code}

-   リージョン分割前にリージョンデータが超えることのできる最大値
-   デフォルト値:リージョンサイズの 1/16。
-   最小値: `0`

### <code>region-compact-check-interval</code> {#code-region-compact-check-interval-code}

-   RocksDB 圧縮を手動でトリガーする必要があるかどうかを確認する時間間隔。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"5m"`
-   最小値: `0`

### <code>region-compact-check-step</code> {#code-region-compact-check-step-code}

-   手動圧縮の各ラウンドで一度にチェックされるリージョンの数
-   デフォルト値: `100`
-   最小値: `0`

### <code>region-compact-min-tombstones</code> {#code-region-compact-min-tombstones-code}

-   RocksDB 圧縮をトリガーするために必要なトゥームストーンの数
-   デフォルト値: `10000`
-   最小値: `0`

### <code>region-compact-tombstones-percent</code> {#code-region-compact-tombstones-percent-code}

-   RocksDB 圧縮をトリガーするために必要なトゥームストーンの割合
-   デフォルト値: `30`
-   最小値: `1`
-   最大値: `100`

### <code>pd-heartbeat-tick-interval</code> {#code-pd-heartbeat-tick-interval-code}

-   PD へのリージョンのハートビートがトリガーされる時間間隔。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"1m"`
-   最小値: `0`

### <code>pd-store-heartbeat-tick-interval</code> {#code-pd-store-heartbeat-tick-interval-code}

-   PD へのストアのハートビートがトリガーされる時間間隔。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"10s"`
-   最小値: `0`

### <code>snap-mgr-gc-tick-interval</code> {#code-snap-mgr-gc-tick-interval-code}

-   期限切れのスナップショット ファイルのリサイクルがトリガーされる時間間隔。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"1m"`
-   最小値: `0`

### <code>snap-gc-timeout</code> {#code-snap-gc-timeout-code}

-   スナップショット ファイルが保存される最長時間
-   デフォルト値: `"4h"`
-   最小値: `0`

### <code>snap-generator-pool-size</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-snap-generator-pool-size-code-span-class-version-mark-new-in-v5-4-0-span}

-   `snap-generator`スレッド プールのサイズを構成します。
-   リカバリ シナリオでリージョンが TiKV でより高速にスナップショットを生成するには、対応するワーカーの`snap-generator`スレッドの数を増やす必要があります。この構成項目を使用して、 `snap-generator`スレッド プールのサイズを増やすことができます。
-   デフォルト値: `2`
-   最小値: `1`

### <code>lock-cf-compact-interval</code> {#code-lock-cf-compact-interval-code}

-   TiKV が Lock カラム Family の手動圧縮をトリガーする時間間隔
-   デフォルト値: `"10m"`
-   最小値: `0`

### <code>lock-cf-compact-bytes-threshold</code> {#code-lock-cf-compact-bytes-threshold-code}

-   TiKV がロックカラムファミリーの手動圧縮をトリガーするサイズ
-   デフォルト値: `"256MB"`
-   最小値: `0`
-   単位：MB

### <code>notify-capacity</code> {#code-notify-capacity-code}

-   リージョンメッセージ キューの最長の長さ。
-   デフォルト値: `40960`
-   最小値: `0`

### <code>messages-per-tick</code> {#code-messages-per-tick-code}

-   バッチごとに処理されるメッセージの最大数
-   デフォルト値: `4096`
-   最小値: `0`

### <code>max-peer-down-duration</code> {#code-max-peer-down-duration-code}

-   ピアに許可される最長の非アクティブ期間。タイムアウトのあるピアは`down`としてマークされ、PD は後でそれを削除しようとします。
-   デフォルト値: `"10m"`
-   最小値: Hibernate リージョンが有効な場合、最小値は`peer-stale-state-check-interval * 2`です。 Hibernate リージョンが無効になっている場合、最小値は`0`です。

### <code>max-leader-missing-duration</code> {#code-max-leader-missing-duration-code}

-   Raftグループがリーダーを欠いている状態にピアが留まることができる最長期間。この値を超えると、ピアはピアが削除されたかどうかを PD で確認します。
-   デフォルト値: `"2h"`
-   最小値: `abnormal-leader-missing-duration`より大きい

### <code>abnormal-leader-missing-duration</code> {#code-abnormal-leader-missing-duration-code}

-   Raftグループがリーダーを欠いている状態にピアが留まることができる最長期間。この値を超えると、ピアは異常と見なされ、メトリックとログでマークされます。
-   デフォルト値: `"10m"`
-   最小値: `peer-stale-state-check-interval`より大きい

### <code>peer-stale-state-check-interval</code> {#code-peer-stale-state-check-interval-code}

-   ピアがRaftグループにリーダーがない状態にあるかどうかのチェックをトリガーする時間間隔。
-   デフォルト値: `"5m"`
-   最小値: `2 * election-timeout`より大きい

### <code>leader-transfer-max-log-lag</code> {#code-leader-transfer-max-log-lag-code}

-   Raftリーダー転送中に転送先に許可される欠落ログの最大数
-   デフォルト値: `128`
-   最小値: `10`

### <code>max-snapshot-file-raw-size</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-max-snapshot-file-raw-size-code-span-class-version-mark-new-in-v6-1-0-span}

-   スナップショット ファイルのサイズがこの設定値を超えると、このファイルは複数のファイルに分割されます。
-   デフォルト値: `100MiB`
-   最小値: `100MiB`

### <code>snap-apply-batch-size</code> {#code-snap-apply-batch-size-code}

-   インポートされたスナップショット ファイルがディスクに書き込まれるときに必要なメモリキャッシュ サイズ
-   デフォルト値: `"10MB"`
-   最小値: `0`
-   単位：MB

### <code>consistency-check-interval</code> {#code-consistency-check-interval-code}

> **警告：**
>
> クラスターのパフォーマンスに影響し、TiDB のガベージコレクションと互換性がないため、本番環境で整合性チェックを有効にすることは**お**勧めしません。

-   整合性チェックがトリガーされる時間間隔。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"0s"`
-   最小値: `0`

### <code>raft-store-max-leader-lease</code> {#code-raft-store-max-leader-lease-code}

-   Raftリーダーの最長信頼期間
-   デフォルト値: `"9s"`
-   最小値: `0`

### <code>right-derive-when-split</code> {#code-right-derive-when-split-code}

-   リージョンが分割されたときに、新しいリージョンの開始キーを指定します。この構成項目が`true`に設定されている場合、開始キーは最大分割キーになります。この構成項目が`false`に設定されている場合、開始キーは元のリージョンの開始キーです。
-   デフォルト値: `true`

### <code>merge-max-log-gap</code> {#code-merge-max-log-gap-code}

-   `merge`を実行したときに許容される欠落ログの最大数
-   デフォルト値: `10`
-   最小値: `raft-log-gc-count-limit`より大きい

### <code>merge-check-tick-interval</code> {#code-merge-check-tick-interval-code}

-   リージョンのマージが必要かどうかを TiKV がチェックする時間間隔
-   デフォルト値: `"2s"`
-   最小値: `0`より大きい

### <code>use-delete-range</code> {#code-use-delete-range-code}

-   `rocksdb delete_range`インターフェイスからデータを削除するかどうかを決定します
-   デフォルト値: `false`

### <code>cleanup-import-sst-interval</code> {#code-cleanup-import-sst-interval-code}

-   期限切れの SST ファイルがチェックされる時間間隔。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"10m"`
-   最小値: `0`

### <code>local-read-batch-size</code> {#code-local-read-batch-size-code}

-   1 回のバッチで処理される読み取り要求の最大数
-   デフォルト値: `1024`
-   最小値: `0`より大きい

### <code>apply-yield-write-size</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-apply-yield-write-size-code-span-class-version-mark-new-in-v6-4-0-span}

-   1 回のポーリングで 1 つの FSM (Finite-state Machine) に対してアプライ スレッドが書き込める最大バイト数。これはソフト制限です。
-   デフォルト値: `"32KiB"`
-   最小値: `0`より大きい
-   単位: KiB|MiB|GiB

### <code>apply-max-batch-size</code> {#code-apply-max-batch-size-code}

-   Raftステート マシンは、BatchSystem によってバッチでデータ書き込み要求を処理します。この設定項目は、1 つのバッチでリクエストを処理できるRaftステート マシンの最大数を指定します。
-   デフォルト値: `256`
-   最小値: `0`より大きい
-   最大値: `10240`

### <code>apply-pool-size</code> {#code-apply-pool-size-code}

-   データをディスクにフラッシュするプール内のスレッドの許容数。これは、適用スレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `2`
-   値の範囲: `[1, CPU * 10]` 。 `CPU` CPU コアの数を意味します。

### <code>store-max-batch-size</code> {#code-store-max-batch-size-code}

-   Raftステート マシンは、BatchSystem によってバッチでログをディスクにフラッシュするための要求を処理します。この設定項目は、1 つのバッチでリクエストを処理できるRaftステート マシンの最大数を指定します。
-   `hibernate-regions`が有効な場合、デフォルト値は`256`です。 `hibernate-regions`が無効になっている場合、デフォルト値は`1024`です。
-   最小値: `0`より大きい
-   最大値: `10240`

### <code>store-pool-size</code> {#code-store-pool-size-code}

-   Raftを処理するプール内のスレッドの許容数。これはRaftstoreスレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `2`
-   値の範囲: `[1, CPU * 10]` 。 `CPU` CPU コアの数を意味します。

### <code>store-io-pool-size</code> <span class="version-mark">v5.3.0 の新機能</span> {#code-store-io-pool-size-code-span-class-version-mark-new-in-v5-3-0-span}

-   Raft I/O タスクを処理するスレッドの許容数。これは StoreWriter スレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `0`
-   最小値: `0`

### <code>future-poll-size</code> {#code-future-poll-size-code}

-   `future`を駆動するスレッドの許容数
-   デフォルト値: `1`
-   最小値: `0`より大きい

### <code>cmd-batch</code> {#code-cmd-batch-code}

-   リクエストのバッチ処理を有効にするかどうかを制御します。有効にすると、書き込みパフォーマンスが大幅に向上します。
-   デフォルト値: `true`

### <code>inspect-interval</code> {#code-inspect-interval-code}

-   一定の間隔で、TiKV はRaftstoreコンポーネントのレイテンシーを検査します。このパラメーターは、検査の間隔を指定します。レイテンシーがこの値を超えると、この検査はタイムアウトとしてマークされます。
-   タイムアウト検査の割合からTiKVノードが遅いかどうかを判断します。
-   デフォルト値: `"500ms"`
-   最小値: `"1ms"`

### <code>raft-write-size-limit</code> <span class="version-mark">v5.3.0 の新機能</span> {#code-raft-write-size-limit-code-span-class-version-mark-new-in-v5-3-0-span}

-   Raftデータがディスクに書き込まれるしきい値を決定します。データサイズがこの構成項目の値より大きい場合、データはディスクに書き込まれます。 `store-io-pool-size`の値が`0`の場合、この構成アイテムは有効になりません。
-   デフォルト値: `1MB`
-   最小値: `0`

### <code>report-min-resolved-ts-interval</code> {#code-report-min-resolved-ts-interval-code}

-   解決されたタイムスタンプが PD リーダーに報告される最小間隔を決定します。この値が`0`に設定されている場合、レポートが無効になっていることを意味します。
-   デフォルト値: `"1s"` 、これは最小の正の値です
-   最小値: `0`
-   単位：秒

## コプロセッサー {#coprocessor}

コプロセッサーに関連するコンフィグレーション項目。

### <code>split-region-on-table</code> {#code-split-region-on-table-code}

-   リージョン をテーブルごとに分割するかどうかを決定します。この機能は TiDB モードでのみ使用することをお勧めします。
-   デフォルト値: `false`

### <code>batch-split-limit</code> {#code-batch-split-limit-code}

-   バッチでのリージョン分割のしきい値。この値を大きくすると、リージョン分割が高速になります。
-   デフォルト値: `10`
-   最小値: `1`

### <code>region-max-size</code> {#code-region-max-size-code}

-   リージョンの最大サイズ。値を超えると、リージョンが多数に分割されます。
-   デフォルト値: `region-split-size / 2 * 3`
-   単位: KiB|MiB|GiB

### <code>region-split-size</code> {#code-region-split-size-code}

-   新しく分割されたリージョンのサイズ。この値は推定値です。
-   デフォルト値: `"96MiB"`
-   単位: KiB|MiB|GiB

### <code>region-max-keys</code> {#code-region-max-keys-code}

-   リージョンで許可されるキーの最大数。この値を超えると、リージョンが多数に分割されます。
-   デフォルト値: `region-split-keys / 2 * 3`

### <code>region-split-keys</code> {#code-region-split-keys-code}

-   新しく分割されたリージョン内のキーの数。この値は推定値です。
-   デフォルト値: `960000`

### <code>consistency-check-method</code> {#code-consistency-check-method-code}

-   データ整合性チェックの方法を指定します
-   MVCC データの整合性チェックの場合は、値を`"mvcc"`に設定します。生データの整合性チェックの場合、値を`"raw"`に設定します。
-   デフォルト値: `"mvcc"`

## コプロセッサー-v2 {#coprocessor-v2}

### <code>coprocessor-plugin-directory</code> {#code-coprocessor-plugin-directory-code}

-   コンパイルされたコプロセッサー・プラグインが置かれているディレクトリーのパス。このディレクトリ内のプラグインは、TiKV によって自動的に読み込まれます。
-   この構成項目が設定されていない場合、コプロセッサー プラグインは無効になります。
-   デフォルト値: `"./coprocessors"`

### <code>enable-region-bucket</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-enable-region-bucket-code-span-class-version-mark-new-in-v6-1-0-span}

-   リージョン をバケットと呼ばれる小さな範囲に分割するかどうかを決定します。バケットは、同時実行クエリの単位として使用され、スキャンの同時実行性を向上させます。バケットの設計について詳しくは、 [動的サイズリージョン](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md)を参照してください。
-   デフォルト値: false

> **警告：**
>
> -   `enable-region-bucket`は、TiDB v6.1.0 で導入された実験的機能です。本番環境で使用することはお勧めしません。
> -   この構成は、 `region-split-size`が`region-bucket-size`の 2 倍以上の場合にのみ意味があります。それ以外の場合、バケットは実際には生成されません。
> -   `region-split-size`をより大きな値に調整すると、パフォーマンスが低下し、スケジューリングが遅くなる可能性があります。

### <code>region-bucket-size</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-region-bucket-size-code-span-class-version-mark-new-in-v6-1-0-span}

-   `enable-region-bucket`が true の場合のバケットのサイズ。
-   デフォルト値: `96MiB`

> **警告：**
>
> `region-bucket-size`は、TiDB v6.1.0 で導入された実験的機能です。本番環境で使用することはお勧めしません。

### <code>report-region-buckets-tick-interval</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-report-region-buckets-tick-interval-code-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> `report-region-buckets-tick-interval`は、TiDB v6.1.0 で導入された実験的機能です。本番環境で使用することはお勧めしません。

-   `enable-region-bucket`が true の場合、TiKV がバケット情報を PD に報告する間隔。
-   デフォルト値: `10s`

## rocksdb {#rocksdb}

RocksDBに関するコンフィグレーション項目

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDB のバックグラウンド スレッドの数。 RocksDB スレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値:
    -   CPU コア数が 10 の場合、デフォルト値は`9`です。
    -   CPU コア数が 8 の場合、デフォルト値は`7`です。
    -   CPU コア数が`N`の場合、デフォルト値は`max(2, min(N - 1, 9))`です。
-   最小値: `2`

### <code>max-background-flushes</code> {#code-max-background-flushes-code}

-   同時バックグラウンド memtable フラッシュ ジョブの最大数
-   デフォルト値:
    -   CPU コア数が 10 の場合、デフォルト値は`3`です。
    -   CPU コア数が 8 の場合、デフォルト値は`2`です。
    -   CPU コア数が`N`の場合、デフォルト値は`[(max-background-jobs + 3) / 4]`です。
-   最小値: `1`

### <code>max-sub-compactions</code> {#code-max-sub-compactions-code}

-   RocksDB で同時に実行されるサブ圧縮操作の数
-   デフォルト値: `3`
-   最小値: `1`

### <code>max-open-files</code> {#code-max-open-files-code}

-   RocksDB が開くことができるファイルの総数
-   デフォルト値: `40960`
-   最小値: `-1`

### <code>max-manifest-file-size</code> {#code-max-manifest-file-size-code}

-   RocksDB マニフェスト ファイルの最大サイズ
-   デフォルト値: `"128MB"`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>create-if-missing</code> {#code-create-if-missing-code}

-   DB スイッチを自動的に作成するかどうかを決定します
-   デフォルト値: `true`

### <code>wal-recovery-mode</code> {#code-wal-recovery-mode-code}

-   WAL回復モード
-   オプションの値:
    -   `"tolerate-corrupted-tail-records"` : すべてのログで不完全な末尾データを持つレコードを許容して破棄します
    -   `"absolute-consistency"` : 破損したログが見つかった場合、リカバリを中止します
    -   `"point-in-time"` : 最初の破損したログが検出されるまで、ログを順次回復します。
    -   `"skip-any-corrupted-records"` : 災害後の復旧。データは可能な限り回復され、破損したレコードはスキップされます。
-   デフォルト値: `"point-in-time"`

### <code>wal-dir</code> {#code-wal-dir-code}

-   WALファイルが保存されているディレクトリ
-   デフォルト値: `"/tmp/tikv/store"`

### <code>wal-ttl-seconds</code> {#code-wal-ttl-seconds-code}

-   アーカイブされた WAL ファイルの存続時間。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位：秒

### <code>wal-size-limit</code> {#code-wal-size-limit-code}

-   アーカイブされた WAL ファイルのサイズ制限。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>max-total-wal-size</code> {#code-max-total-wal-size-code}

-   合計で最大の RocksDB WAL サイズ。これは`data-dir`の`*.log`ファイルのサイズです。
-   デフォルト値: `"4GB"`

### <code>enable-statistics</code> {#code-enable-statistics-code}

-   RocksDB の統計を有効にするかどうかを決定します
-   デフォルト値: `true`

### <code>stats-dump-period</code> {#code-stats-dump-period-code}

-   統計がログに出力される間隔。
-   デフォルト値: `10m`

### <code>compaction-readahead-size</code> {#code-compaction-readahead-size-code}

-   RocksDB の圧縮中に先読み機能を有効にし、先読みデータのサイズを指定します。メカニカル ディスクを使用している場合は、値を少なくとも 2MB に設定することをお勧めします。
-   デフォルト値: `0`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>writable-file-max-buffer-size</code> {#code-writable-file-max-buffer-size-code}

-   WritableFileWrite で使用される最大バッファ サイズ
-   デフォルト値: `"1MB"`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>use-direct-io-for-flush-and-compaction</code> {#code-use-direct-io-for-flush-and-compaction-code}

-   バックグラウンド フラッシュと圧縮で読み取りと書き込みの両方に`O_DIRECT`を使用するかどうかを決定します。このオプションのパフォーマンスへの影響: `O_DIRECT`バイパスを有効にして OS バッファー キャッシュの汚染を防ぎますが、その後のファイル読み取りではバッファー キャッシュの内容を再度読み取る必要があります。
-   デフォルト値: `false`

### <code>rate-bytes-per-sec</code> {#code-rate-bytes-per-sec-code}

-   RocksDB のコンパクション レート リミッタで許可される最大レート
-   デフォルト値: `10GB`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>rate-limiter-refill-period</code> {#code-rate-limiter-refill-period-code}

-   I/O トークンが補充される頻度を制御します。値を小さくすると、I/O バーストが減少しますが、CPU オーバーヘッドが増加します。
-   デフォルト値: `"100ms"`

### <code>rate-limiter-mode</code> {#code-rate-limiter-mode-code}

-   RocksDB のコンパクション レート リミッター モード
-   オプションの値: `"read-only"` 、 `"write-only"` 、 `"all-io"`
-   デフォルト値: `"write-only"`

### <code>rate-limiter-auto-tuned</code> <span class="version-mark">v5.0 の新機能</span> {#code-rate-limiter-auto-tuned-code-span-class-version-mark-new-in-v5-0-span}

-   最近のワークロードに基づいて、RocksDB の圧縮レート リミッターの構成を自動的に最適化するかどうかを決定します。この構成が有効になっている場合、圧縮保留中のバイトは通常よりわずかに高くなります。
-   デフォルト値: `true`

### <code>enable-pipelined-write</code> {#code-enable-pipelined-write-code}

-   パイプライン書き込みを有効にするかどうかを制御します。この構成が有効な場合、以前の Pipelined Write が使用されます。この構成を無効にすると、新しい Pipelined Commit メカニズムが使用されます。
-   デフォルト値: `false`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   これらのファイルが非同期的に書き込まれている間に、OS がファイルをディスクに増分的に同期する速度
-   デフォルト値: `"1MB"`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>wal-bytes-per-sync</code> {#code-wal-bytes-per-sync-code}

-   WALファイルの書き込み中に、OSがWALファイルをディスクに段階的に同期する速度
-   デフォルト値: `"512KB"`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>info-log-max-size</code> {#code-info-log-max-size-code}

-   情報ログの最大サイズ
-   デフォルト値: `"1GB"`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>info-log-roll-time</code> {#code-info-log-roll-time-code}

-   情報ログが切り捨てられる時間間隔。値が`0s`の場合、ログは切り捨てられません。
-   デフォルト値: `"0s"`

### <code>info-log-keep-log-file-num</code> {#code-info-log-keep-log-file-num-code}

-   保持されるログ ファイルの最大数
-   デフォルト値: `10`
-   最小値: `0`

### <code>info-log-dir</code> {#code-info-log-dir-code}

-   ログが保存されるディレクトリ
-   デフォルト値: `""`

### <code>info-log-level</code> {#code-info-log-level-code}

-   RocksDB のログレベル
-   デフォルト値: `"info"`

## rocksdb.titan {#rocksdb-titan}

Titan関連のコンフィグレーション項目。

### <code>enabled</code> {#code-enabled-code}

-   タイタンを有効または無効にします
-   デフォルト値: `false`

### <code>dirname</code> {#code-dirname-code}

-   Titan Blob ファイルが保存されているディレクトリ
-   デフォルト値: `"titandb"`

### <code>disable-gc</code> {#code-disable-gc-code}

-   Titan が BLOB ファイルに対して実行するガベージ コレクション (GC) を無効にするかどうかを決定します。
-   デフォルト値: `false`

### <code>max-background-gc</code> {#code-max-background-gc-code}

-   Titan の GC スレッドの最大数
-   デフォルト値: `4`
-   最小値: `1`

## rocksdb.defaultcf | rocksdb.writecf | rocksdb.lockcf {#rocksdb-defaultcf-rocksdb-writecf-rocksdb-lockcf}

`rocksdb.defaultcf` `rocksdb.writecf`関連するコンフィグレーション項目`rocksdb.lockcf` 。

### <code>block-size</code> {#code-block-size-code}

-   RocksDB ブロックのデフォルト サイズ
-   `defaultcf`および`writecf`のデフォルト値: `"64KB"`
-   `lockcf`のデフォルト値: `"16KB"`
-   最小値: `"1KB"`
-   単位: KB|MB|GB

### <code>block-cache-size</code> {#code-block-cache-size-code}

-   RocksDB ブロックのキャッシュ サイズ
-   `defaultcf`のデフォルト値: `Total machine memory * 25%`
-   `writecf`のデフォルト値: `Total machine memory * 15%`
-   `lockcf`のデフォルト値: `Total machine memory * 2%`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>disable-block-cache</code> {#code-disable-block-cache-code}

-   ブロックキャッシュを有効または無効にします
-   デフォルト値: `false`

### <code>cache-index-and-filter-blocks</code> {#code-cache-index-and-filter-blocks-code}

-   インデックスとフィルタのキャッシングを有効または無効にします
-   デフォルト値: `true`

### <code>pin-l0-filter-and-index-blocks</code> {#code-pin-l0-filter-and-index-blocks-code}

-   レベル 0 の SST ファイルのインデックス ブロックとフィルター ブロックをメモリに固定するかどうかを決定します。
-   デフォルト値: `true`

### <code>use-bloom-filter</code> {#code-use-bloom-filter-code}

-   ブルームフィルターを有効または無効にします
-   デフォルト値: `true`

### <code>optimize-filters-for-hits</code> {#code-optimize-filters-for-hits-code}

-   フィルターのヒット率を最適化するかどうかを決定します
-   `defaultcf`のデフォルト値: `true`
-   `writecf`および`lockcf`のデフォルト値: `false`

### <code>whole-key-filtering</code> {#code-whole-key-filtering-code}

-   キー全体をブルームフィルターに入れるかどうかを決定します
-   `defaultcf`および`lockcf`のデフォルト値: `true`
-   `writecf`のデフォルト値: `false`

### <code>bloom-filter-bits-per-key</code> {#code-bloom-filter-bits-per-key-code}

-   ブルームフィルターが各キーに予約する長さ
-   デフォルト値: `10`
-   単位：バイト

### <code>block-based-bloom-filter</code> {#code-block-based-bloom-filter-code}

-   各ブロックがブルームフィルターを作成するかどうかを決定します
-   デフォルト値: `false`

### <code>read-amp-bytes-per-bit</code> {#code-read-amp-bytes-per-bit-code}

-   読み取り増幅の統計を有効または無効にします。
-   オプションの値: `0` (無効)、&gt; `0` (有効)。
-   デフォルト値: `0`
-   最小値: `0`

### <code>compression-per-level</code> {#code-compression-per-level-code}

-   各レベルのデフォルトの圧縮アルゴリズム
-   `defaultcf`のデフォルト値: [&quot;no&quot;, &quot;no&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;zstd&quot;, &quot;zstd&quot;]
-   `writecf`のデフォルト値: [&quot;no&quot;, &quot;no&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;zstd&quot;, &quot;zstd&quot;]
-   `lockcf`のデフォルト値: [&quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;]

### <code>bottommost-level-compression</code> {#code-bottommost-level-compression-code}

-   最レイヤーの圧縮アルゴリズムを設定します。この構成項目は`compression-per-level`の設定をオーバーライドします。
-   データが LSM ツリーに書き込まれて以来、RocksDB は最レイヤーの`compression-per-level`配列で指定された最後の圧縮アルゴリズムを直接採用しません。 `bottommost-level-compression`場合、最初から最レイヤーで最も圧縮効果の高い圧縮アルゴリズムを使用できます。
-   最レイヤーの圧縮アルゴリズムを設定しない場合は、この構成項目の値を`disable`に設定します。
-   デフォルト値: `"zstd"`

### <code>write-buffer-size</code> {#code-write-buffer-size-code}

-   メモリブルサイズ
-   `defaultcf`および`writecf`のデフォルト値: `"128MB"`
-   `lockcf`のデフォルト値: `"32MB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>max-write-buffer-number</code> {#code-max-write-buffer-number-code}

-   memtable の最大数。 `storage.flow-control.enable`が`true`に設定されている場合、 `storage.flow-control.memtables-threshold`この構成項目をオーバーライドします。
-   デフォルト値: `5`
-   最小値: `0`

### <code>min-write-buffer-number-to-merge</code> {#code-min-write-buffer-number-to-merge-code}

-   フラッシュをトリガーするために必要な memtable の最小数
-   デフォルト値: `1`
-   最小値: `0`

### <code>max-bytes-for-level-base</code> {#code-max-bytes-for-level-base-code}

-   ベース レベル (レベル 1) の最大バイト数。通常、memtable の 4 倍のサイズに設定されます。レベル 1 のデータ サイズが制限値の`max-bytes-for-level-base`に達すると、レベル 1 の SST ファイルとそれらに重なるレベル 2 の SST ファイルが圧縮されます。
-   `defaultcf`および`writecf`のデフォルト値: `"512MB"`
-   `lockcf`のデフォルト値: `"128MB"`
-   最小値: `0`
-   単位: KB|MB|GB
-   不必要な圧縮を減らすために、値`max-bytes-for-level-base`を L0 のデータ量とほぼ同じに設定することをお勧めします。たとえば、圧縮方法`write-buffer-size * 4` 「no:no:lz4:lz4:lz4:lz4:lz4」の場合、L0 と`max-bytes-for-level-base`の圧縮がなく、L0 の圧縮のトリガー条件がSST ファイルの数が 4 (デフォルト値) に達することを確認します。 L0 と L1 の両方が圧縮を採用する場合、Memtable から圧縮された SST ファイルのサイズを理解するために RocksDB ログを分析する必要があります。たとえば、ファイル サイズが 32 MB の場合、 `max-bytes-for-level-base` ～ 128 MB の値を設定することをお勧めします ( `32 MB * 4` )。

### <code>target-file-size-base</code> {#code-target-file-size-base-code}

-   ベース レベルでのターゲット ファイルのサイズ。 `enable-compaction-guard`値が`true`の場合、この値は`compaction-guard-max-output-file-size`でオーバーライドされます。
-   デフォルト値: `"8MB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>level0-file-num-compaction-trigger</code> {#code-level0-file-num-compaction-trigger-code}

-   圧縮をトリガーする L0 のファイルの最大数
-   `defaultcf`および`writecf`のデフォルト値: `4`
-   `lockcf`のデフォルト値: `1`
-   最小値: `0`

### <code>level0-slowdown-writes-trigger</code> {#code-level0-slowdown-writes-trigger-code}

-   書き込みストールをトリガーする L0 のファイルの最大数。 `storage.flow-control.enable`が`true`に設定されている場合、 `storage.flow-control.l0-files-threshold`この構成項目をオーバーライドします。
-   デフォルト値: `20`
-   最小値: `0`

### <code>level0-stop-writes-trigger</code> {#code-level0-stop-writes-trigger-code}

-   書き込みを完全にブロックするために必要な L0 のファイルの最大数
-   デフォルト値: `36`
-   最小値: `0`

### <code>max-compaction-bytes</code> {#code-max-compaction-bytes-code}

-   圧縮ごとにディスクに書き込まれる最大バイト数
-   デフォルト値: `"2GB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>compaction-pri</code> {#code-compaction-pri-code}

-   圧縮の優先タイプ
-   オプションの値:
    -   `"by-compensated-size"` : ファイル サイズの順に圧縮し、大きなファイルは優先的に圧縮します。
    -   `"oldest-largest-seq-first"` : 更新時刻が最も古いファイルの圧縮を優先します。この値は、狭い範囲でホット キーを更新する場合に**のみ**使用してください。
    -   `"oldest-smallest-seq-first"` : 次のレベルに長期間圧縮されていない範囲を持つファイルの圧縮を優先します。キー スペース全体でホット キーをランダムに更新する場合、この値によって書き込み増幅がわずかに減少する可能性があります。
    -   `"min-overlapping-ratio"` : オーバーラップ率の高いファイルの圧縮を優先します。ファイルがさまざまなレベルで小さい場合 ( `the file size in the next level` ÷ `the file size in this level`の結果が小さい場合)、TiKV はこのファイルを最初に圧縮します。多くの場合、この値は効果的に書き込み増幅を減らすことができます。
-   `defaultcf`および`writecf`のデフォルト値: `"min-overlapping-ratio"`
-   `lockcf`のデフォルト値: `"by-compensated-size"`

### <code>dynamic-level-bytes</code> {#code-dynamic-level-bytes-code}

-   動的レベルのバイトを最適化するかどうかを決定します
-   デフォルト値: `true`

### <code>num-levels</code> {#code-num-levels-code}

-   RocksDB ファイルの最大レベル数
-   デフォルト値: `7`

### <code>max-bytes-for-level-multiplier</code> {#code-max-bytes-for-level-multiplier-code}

-   各レイヤーのデフォルトの増幅倍数
-   デフォルト値: `10`

### <code>compaction-style</code> {#code-compaction-style-code}

-   圧縮方法
-   オプションの値: `"level"` 、 `"universal"` 、 `"fifo"`
-   デフォルト値: `"level"`

### <code>disable-auto-compactions</code> {#code-disable-auto-compactions-code}

-   自動圧縮を無効にするかどうかを決定します。
-   デフォルト値: `false`

### <code>soft-pending-compaction-bytes-limit</code> {#code-soft-pending-compaction-bytes-limit-code}

-   保留中の圧縮バイトのソフト制限。 `storage.flow-control.enable`が`true`に設定されている場合、 `storage.flow-control.soft-pending-compaction-bytes-limit`この構成項目をオーバーライドします。
-   デフォルト値: `"192GB"`
-   単位: KB|MB|GB

### <code>hard-pending-compaction-bytes-limit</code> {#code-hard-pending-compaction-bytes-limit-code}

-   保留中の圧縮バイトのハード制限。 `storage.flow-control.enable`が`true`に設定されている場合、 `storage.flow-control.hard-pending-compaction-bytes-limit`この構成項目をオーバーライドします。
-   デフォルト値: `"256GB"`
-   単位: KB|MB|GB

### <code>enable-compaction-guard</code> {#code-enable-compaction-guard-code}

-   TiKVリージョンの境界で SST ファイルを分割するための最適化である圧縮ガードを有効または無効にします。この最適化は、圧縮 I/O を削減するのに役立ち、TiKV がより大きな SST ファイル サイズを使用できるようになり (したがって、SST ファイル全体が少なくなります)、同時にリージョンの移行時に古いデータを効率的にクリーンアップできます。
-   `defaultcf`および`writecf`のデフォルト値: `true`
-   `lockcf`のデフォルト値: `false`

### <code>compaction-guard-min-output-file-size</code> {#code-compaction-guard-min-output-file-size-code}

-   コンパクション ガードが有効な場合の SST ファイルの最小サイズ。この構成により、圧縮ガードが有効になっている場合に SST ファイルが小さすぎるのを防ぐことができます。
-   デフォルト値: `"8MB"`
-   単位: KB|MB|GB

### <code>compaction-guard-max-output-file-size</code> {#code-compaction-guard-max-output-file-size-code}

-   コンパクション ガードが有効な場合の SST ファイルの最大サイズ。この構成により、圧縮ガードが有効になっている場合に SST ファイルが大きくなりすぎるのを防ぐことができます。この構成は、同じカラムファミリーの`target-file-size-base`をオーバーライドします。
-   デフォルト値: `"128MB"`
-   単位: KB|MB|GB

## rocksdb.defaultcf.titan {#rocksdb-defaultcf-titan}

に関連するコンフィグレーション項目`rocksdb.defaultcf.titan` ．

### <code>min-blob-size</code> {#code-min-blob-size-code}

-   Blob ファイルに格納されている最小値。指定されたサイズより小さい値は LSM-Tree に格納されます。
-   デフォルト値: `"1KB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>blob-file-compression</code> {#code-blob-file-compression-code}

-   Blob ファイルで使用される圧縮アルゴリズム
-   オプションの値: `"no"` 、 `"snappy"` 、 `"zlib"` 、 `"bzip2"` 、 `"lz4"` 、 `"lz4hc"` 、 `"zstd"`
-   デフォルト値: `"lz4"`

### <code>blob-cache-size</code> {#code-blob-cache-size-code}

-   Blob ファイルのキャッシュ サイズ
-   デフォルト値: `"0GB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>min-gc-batch-size</code> {#code-min-gc-batch-size-code}

-   GC を 1 回実行するために必要な Blob ファイルの最小合計サイズ
-   デフォルト値: `"16MB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>max-gc-batch-size</code> {#code-max-gc-batch-size-code}

-   一度に GC を実行できる Blob ファイルの最大合計サイズ
-   デフォルト値: `"64MB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>discardable-ratio</code> {#code-discardable-ratio-code}

-   Blob ファイルに対して GC がトリガーされる比率。 Blob ファイル内の無効な値の比率がこの比率を超える場合にのみ、GC 用に Blob ファイルを選択できます。
-   デフォルト値: `0.5`
-   最小値: `0`
-   最大値: `1`

### <code>sample-ratio</code> {#code-sample-ratio-code}

-   GC 中にファイルをサンプリングしたときの (Blob ファイルから読み取られたデータ/Blob ファイル全体) の比率
-   デフォルト値: `0.1`
-   最小値: `0`
-   最大値: `1`

### <code>merge-small-file-threshold</code> {#code-merge-small-file-threshold-code}

-   Blob ファイルのサイズがこの値よりも小さい場合でも、Blob ファイルが GC 用に選択されることがあります。この場合、 `discardable-ratio`は無視されます。
-   デフォルト値: `"8MB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>blob-run-mode</code> {#code-blob-run-mode-code}

-   Titan の実行モードを指定します。
-   オプションの値:
    -   `normal` : 値のサイズが`min-blob-size`を超えると、データを BLOB ファイルに書き込みます。
    -   `read_only` : BLOB ファイルへの新しいデータの書き込みを拒否しますが、BLOB ファイルから元のデータを読み取ります。
    -   `fallback` : blob ファイルのデータを LSM に書き戻します。
-   デフォルト値: `normal`

### <code>level-merge</code> {#code-level-merge-code}

-   読み取りパフォーマンスを最適化するかどうかを決定します。 `level-merge`が有効な場合、より多くの書き込み増幅があります。
-   デフォルト値: `false`

## raftdb {#raftdb}

`raftdb`に関するコンフィグレーション項目

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDB のバックグラウンド スレッドの数。 RocksDB スレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `4`
-   最小値: `2`

### <code>max-sub-compactions</code> {#code-max-sub-compactions-code}

-   RocksDB で実行される同時サブ圧縮操作の数
-   デフォルト値: `2`
-   最小値: `1`

### <code>max-open-files</code> {#code-max-open-files-code}

-   RocksDB が開くことができるファイルの総数
-   デフォルト値: `40960`
-   最小値: `-1`

### <code>max-manifest-file-size</code> {#code-max-manifest-file-size-code}

-   RocksDB マニフェスト ファイルの最大サイズ
-   デフォルト値: `"20MB"`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>create-if-missing</code> {#code-create-if-missing-code}

-   値が`true`の場合、データベースが存在しない場合は作成されます
-   デフォルト値: `true`

### <code>enable-statistics</code> {#code-enable-statistics-code}

-   Raft RocksDB の統計を有効にするかどうかを決定します
-   デフォルト値: `true`

### <code>stats-dump-period</code> {#code-stats-dump-period-code}

-   統計がログに出力される間隔
-   デフォルト値: `10m`

### <code>wal-dir</code> {#code-wal-dir-code}

-   Raft RocksDB WAL ファイルが格納されるディレクトリ。これは、WAL の絶対ディレクトリ パスです。この構成項目を[`rocksdb.wal-dir`](#wal-dir)と同じ値に設定し**ないでください**。
-   この構成項目が設定されていない場合、ログ ファイルはデータと同じディレクトリに保存されます。
-   マシンに 2 つのディスクがある場合、RocksDB データと WAL ログを別々のディスクに格納すると、パフォーマンスが向上する可能性があります。
-   デフォルト値: `""`

### <code>wal-ttl-seconds</code> {#code-wal-ttl-seconds-code}

-   アーカイブされた WAL ファイルが保持される期間を指定します。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位：秒

### <code>wal-size-limit</code> {#code-wal-size-limit-code}

-   アーカイブされた WAL ファイルのサイズ制限。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>max-total-wal-size</code> {#code-max-total-wal-size-code}

-   合計の最大 RocksDB WAL サイズ
-   デフォルト値: `"4GB"`

### <code>compaction-readahead-size</code> {#code-compaction-readahead-size-code}

-   RocksDB 圧縮中に先読み機能を有効にし、先読みデータのサイズを指定するかどうかを制御します。
-   メカニカル ディスクを使用する場合は、値を少なくとも`2MB`に設定することをお勧めします。
-   デフォルト値: `0`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>writable-file-max-buffer-size</code> {#code-writable-file-max-buffer-size-code}

-   WritableFileWrite で使用される最大バッファ サイズ
-   デフォルト値: `"1MB"`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>use-direct-io-for-flush-and-compaction</code> {#code-use-direct-io-for-flush-and-compaction-code}

-   バックグラウンド フラッシュと圧縮で読み取りと書き込みの両方に`O_DIRECT`を使用するかどうかを決定します。このオプションのパフォーマンスへの影響: `O_DIRECT`バイパスを有効にして OS バッファー キャッシュの汚染を防ぎますが、その後のファイル読み取りではバッファー キャッシュの内容を再度読み取る必要があります。
-   デフォルト値: `false`

### <code>enable-pipelined-write</code> {#code-enable-pipelined-write-code}

-   パイプライン書き込みを有効にするかどうかを制御します。この構成が有効な場合、以前の Pipelined Write が使用されます。この構成を無効にすると、新しい Pipelined Commit メカニズムが使用されます。
-   デフォルト値: `true`

### <code>allow-concurrent-memtable-write</code> {#code-allow-concurrent-memtable-write-code}

-   memtable への同時書き込みを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   これらのファイルが非同期的に書き込まれている間に、OS がファイルをディスクに増分的に同期する速度
-   デフォルト値: `"1MB"`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>wal-bytes-per-sync</code> {#code-wal-bytes-per-sync-code}

-   WALファイルが書き込まれているときに、OSがWALファイルをディスクに段階的に同期する速度
-   デフォルト値: `"512KB"`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>info-log-max-size</code> {#code-info-log-max-size-code}

-   情報ログの最大サイズ
-   デフォルト値: `"1GB"`
-   最小値: `0`
-   単位：B|KB|MB|GB

### <code>info-log-roll-time</code> {#code-info-log-roll-time-code}

-   情報ログが切り捨てられる間隔。値が`0s`の場合、ログは切り捨てられません。
-   デフォルト値: `"0s"` (ログが切り捨てられないことを意味します)

### <code>info-log-keep-log-file-num</code> {#code-info-log-keep-log-file-num-code}

-   RaftDB に保持される情報ログ ファイルの最大数
-   デフォルト値: `10`
-   最小値: `0`

### <code>info-log-dir</code> {#code-info-log-dir-code}

-   Info ログが保存されるディレクトリ
-   デフォルト値: `""`

### <code>info-log-level</code> {#code-info-log-level-code}

-   RaftDB のログレベル
-   デフォルト値: `"info"`

## いかだエンジン {#raft-engine}

Raft Engineに関連するコンフィグレーション項目。

> **ノート：**
>
> -   初めてRaft Engine を有効にすると、TiKV はそのデータを RocksDB からRaft Engineに転送します。そのため、TiKV が起動するまでさらに数十秒待つ必要があります。
> -   TiDB v5.4.0 のRaft Engineのデータ形式は、以前の TiDB バージョンと互換性がありません。したがって、TiDB クラスターを v5.4.0 から以前のバージョンにダウングレードする必要がある場合は、ダウングレードする**前に**、 `enable`から`false`に設定してRaft Engine を無効にし、TiKV を再起動して構成を有効にします。

### <code>enable</code> {#code-enable-code}

-   Raft Engineを使用してRaftログを保存するかどうかを決定します。有効にすると、 `raftdb`の構成は無視されます。
-   デフォルト値: `true`

### <code>dir</code> {#code-dir-code}

-   raft ログ ファイルが保存されるディレクトリ。ディレクトリが存在しない場合は、TiKV の起動時に作成されます。
-   この構成項目が設定されていない場合は、 `{data-dir}/raft-engine`が使用されます。
-   マシンに複数のディスクがある場合、 Raft Engineのデータを別のディスクに保存して、TiKV のパフォーマンスを向上させることをお勧めします。
-   デフォルト値: `""`

### <code>batch-compression-threshold</code> {#code-batch-compression-threshold-code}

-   ログ バッチのしきい値サイズを指定します。この構成より大きいログ バッチは圧縮されます。この構成項目を`0`に設定すると、圧縮は無効になります。
-   デフォルト値: `"8KB"`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   バッファリングされた書き込みの最大累積サイズを指定します。この設定値を超えると、バッファリングされた書き込みがディスクにフラッシュされます。
-   この構成項目を`0`に設定すると、増分同期が無効になります。
-   デフォルト値: `"4MB"`

### <code>target-file-size</code> {#code-target-file-size-code}

-   ログ ファイルの最大サイズを指定します。ログ ファイルがこの値より大きい場合、ローテーションされます。
-   デフォルト値: `"128MB"`

### <code>purge-threshold</code> {#code-purge-threshold-code}

-   メイン ログ キューのしきい値サイズを指定します。この設定値を超えると、メイン ログ キューが消去されます。
-   この構成は、 Raft Engineのディスク容量の使用を調整するために使用できます。
-   デフォルト値: `"10GB"`

### <code>recovery-mode</code> {#code-recovery-mode-code}

-   リカバリ中のファイルの破損に対処する方法を決定します。
-   値のオプション: `"absolute-consistency"` 、 `"tolerate-tail-corruption"` 、 `"tolerate-any-corruption"`
-   デフォルト値: `"tolerate-tail-corruption"`

### <code>recovery-read-block-size</code> {#code-recovery-read-block-size-code}

-   リカバリ中にログ ファイルを読み取るための最小 I/O サイズ。
-   デフォルト値: `"16KB"`
-   最小値: `"512B"`

### <code>recovery-threads</code> {#code-recovery-threads-code}

-   ログ ファイルのスキャンと回復に使用されるスレッドの数。
-   デフォルト値: `4`
-   最小値: `1`

### <code>memory-limit</code> {#code-memory-limit-code}

-   Raft Engineのメモリ使用量の制限を指定します。
-   この構成値が設定されていない場合、使用可能なシステムメモリの 15% が使用されます。
-   デフォルト値: `Total machine memory * 15%`

### <code>format-version</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-format-version-code-span-class-version-mark-new-in-v6-3-0-span}

> **ノート：**
>
> `format-version`を`2`に設定した後、TiKV クラスターを v6.3.0 から以前のバージョンにダウングレードする必要がある場合は、ダウングレードする**前に**次の手順を実行します。
>
> 1.  [`enable`](/tikv-configuration-file.md#enable-1)から`false`設定してRaft Engine を無効にし、TiKV を再起動して構成を有効にします。
> 2.  `format-version` ～ `1`を設定します。
> 3.  `enable`から`true`設定してRaft Engine を有効にし、TiKV を再起動して構成を有効にします。

-   Raft Engineのログ ファイルのバージョンを指定します。
-   値のオプション:
    -   `1` : v6.3.0 より前の TiKV のデフォルトのログ ファイル バージョン。 TiKV &gt;= v6.1.0 で読めます。
    -   `2` : ログのリサイクルをサポートします。 TiKV &gt;= v6.3.0 で読み取ることができます。
-   デフォルト値: `2`

### <code>enable-log-recycle</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-enable-log-recycle-code-span-class-version-mark-new-in-v6-3-0-span}

> **ノート：**
>
> この構成アイテムは、 [`format-version`](#format-version-new-in-v630) &gt;= 2 の場合にのみ使用できます。

-   Raft Engineで古いログ ファイルをリサイクルするかどうかを決定します。有効にすると、論理的にパージされたログ ファイルがリサイクル用に予約されます。これにより、書き込みワークロードのロングテールレイテンシーが短縮されます。
-   デフォルト値: `false`

## 安全 {#security}

セキュリティに関するコンフィグレーション項目です。

### <code>ca-path</code> {#code-ca-path-code}

-   CA ファイルのパス
-   デフォルト値: `""`

### <code>cert-path</code> {#code-cert-path-code}

-   X.509 証明書を含む Privacy Enhanced Mail (PEM) ファイルのパス
-   デフォルト値: `""`

### <code>key-path</code> {#code-key-path-code}

-   X.509 キーを含む PEM ファイルのパス
-   デフォルト値: `""`

### <code>cert-allowed-cn</code> {#code-cert-allowed-cn-code}

-   クライアントによって提示された証明書で受け入れ可能な X.509 共通名のリスト。要求は、提示された共通名がリスト内のエントリの 1 つと完全に一致する場合にのみ許可されます。
-   デフォルト値: `[]` 。これは、クライアント証明書の CN チェックがデフォルトで無効になっていることを意味します。

### <code>redact-info-log</code> <span class="version-mark">v4.0.8 の新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v4-0-8-span}

-   この構成項目は、ログのリダクションを有効または無効にします。構成値が`true`に設定されている場合、ログ内のすべてのユーザー データは`?`に置き換えられます。
-   デフォルト値: `false`

## セキュリティ暗号化 {#security-encryption}

[保存時の暗号化](/encryption-at-rest.md) （TDE）に関するコンフィグレーション項目。

### <code>data-encryption-method</code> {#code-data-encryption-method-code}

-   データファイルの暗号化方式
-   値のオプション: &quot;plaintext&quot;、&quot;aes128-ctr&quot;、&quot;aes192-ctr&quot;、&quot;aes256-ctr&quot;、および &quot;sm4-ctr&quot; (v6.3.0 以降でサポート)
-   &quot;plaintext&quot; 以外の値は、暗号化が有効であることを意味します。この場合、マスター キーを指定する必要があります。
-   デフォルト値: `"plaintext"`

### <code>data-key-rotation-period</code> {#code-data-key-rotation-period-code}

-   TiKV がデータ暗号化キーをローテーションする頻度を指定します。
-   デフォルト値: `7d`

### <code>enable-file-dictionary-log</code> {#code-enable-file-dictionary-log-code}

-   TiKV が暗号化メタデータを管理するときに、I/O とミューテックスの競合を減らすための最適化を有効にします。
-   この構成パラメーターが (デフォルトで) 有効になっている場合に起こりうる互換性の問題を回避するには、詳細について[保存時の暗号化- TiKV バージョン間の互換性](/encryption-at-rest.md#compatibility-between-tikv-versions)を参照してください。
-   デフォルト値: `true`

### <code>master-key</code> {#code-master-key-code}

-   暗号化が有効な場合、マスター キーを指定します。マスター鍵の構成方法については、 [保存時の暗号化- 暗号化の構成](/encryption-at-rest.md#configure-encryption)を参照してください。

### <code>previous-master-key</code> {#code-previous-master-key-code}

-   新しいマスター キーをローテーションするときに、古いマスター キーを指定します。設定フォーマットは`master-key`と同じです。マスター キーの構成方法については、 [保存時の暗号化- 暗号化の構成](/encryption-at-rest.md#configure-encryption)を参照してください。

## 輸入 {#import}

TiDB Lightning のインポートとBRの復元に関するコンフィグレーション項目です。

### <code>num-threads</code> {#code-num-threads-code}

-   RPC リクエストを処理するスレッドの数
-   デフォルト値: `8`
-   最小値: `1`

### <code>stream-channel-window</code> {#code-stream-channel-window-code}

-   ストリーム チャネルのウィンドウ サイズ。チャネルがいっぱいになると、ストリームはブロックされます。
-   デフォルト値: `128`

### <span class="version-mark">v6.5.0 の新</span><code>memory-use-ratio</code> {#code-memory-use-ratio-code-span-class-version-mark-new-in-v6-5-0-span}

-   v6.5.0 以降、PITR はメモリ内のバックアップ ログ ファイルへの直接アクセスとデータの復元をサポートします。この構成項目は、TIKV の合計メモリに対する PITR で使用可能なメモリの比率を指定します。
-   値の範囲: [0.0, 0.5]
-   デフォルト値: `0.3` 。これは、システムメモリの 30% が PITR に使用できることを意味します。値が`0.0`場合、PITR はログ ファイルをローカル ディレクトリにダウンロードすることによって実行されます。

> **ノート：**
>
> v6.5.0 より前のバージョンでは、ポイントインタイム リカバリ (PITR) は、バックアップ ファイルをローカル ディレクトリにダウンロードすることによるデータの復元のみをサポートします。

## GC {#gc}

### <code>batch-keys</code> {#code-batch-keys-code}

-   1 回のバッチでガベージ コレクションされるキーの数
-   デフォルト値: `512`

### <code>max-write-bytes-per-sec</code> {#code-max-write-bytes-per-sec-code}

-   GC ワーカーが 1 秒間に RocksDB に書き込める最大バイト数。
-   値が`0`に設定されている場合、制限はありません。
-   デフォルト値: `"0"`

### <code>enable-compaction-filter</code> <span class="version-mark">v5.0 の新機能</span> {#code-enable-compaction-filter-code-span-class-version-mark-new-in-v5-0-span}

-   コンパクション フィルタ機能で GC を有効にするかどうかを制御します
-   デフォルト値: `true`

### <code>ratio-threshold</code> {#code-ratio-threshold-code}

-   GC をトリガーするガベージ比率のしきい値。
-   デフォルト値: `1.1`

## バックアップ {#backup}

BRバックアップに関するコンフィグレーション項目です。

### <code>num-threads</code> {#code-num-threads-code}

-   バックアップを処理するワーカー スレッドの数
-   デフォルト値: `MIN(CPU * 0.5, 8)`
-   値の範囲: `[1, CPU]`
-   最小値: `1`

### <code>batch-size</code> {#code-batch-size-code}

-   1 回のバッチでバックアップするデータ範囲の数
-   デフォルト値: `8`

### <code>sst-max-size</code> {#code-sst-max-size-code}

-   バックアップ SST ファイル サイズのしきい値。 TiKVリージョン内のバックアップ ファイルのサイズがこのしきい値を超える場合、ファイルは複数のファイルにバックアップされ、TiKVリージョンは複数のリージョン範囲に分割されます。分割されたリージョン内の各ファイルは、 `sst-max-size`と同じサイズ (またはわずかに大きい) です。
-   たとえば、リージョン`[a,e)` `[b,c)`バックアップ ファイルのサイズが`sst-max-size`より大きい場合、ファイルは`[b,c)` `[a,b)` `[c,d)`および`[d,e)` `[c,d)`複数のファイルにバックアップされ、 `[a,b)`のサイズは同じです。 `sst-max-size`のように (またはわずかに大きい)。
-   デフォルト値: `"144MB"`

### <code>enable-auto-tune</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-enable-auto-tune-code-span-class-version-mark-new-in-v5-4-0-span}

-   クラスタ リソースの使用率が高い場合に、バックアップ タスクで使用されるリソースを制限してクラスタへの影響を軽減するかどうかを制御します。詳細については、 [BRオートチューン](/br/br-auto-tune.md)を参照してください。
-   デフォルト値: `true`

### <code>s3-multi-part-size</code> <span class="version-mark">v5.3.2 の新機能</span> {#code-s3-multi-part-size-code-span-class-version-mark-new-in-v5-3-2-span}

> **ノート：**
>
> この構成は、S3 レート制限によって引き起こされるバックアップの失敗に対処するために導入されました。この問題は[バックアップ データstorage構造の改善](/br/br-snapshot-architecture.md#structure-of-backup-files)で修正されました。したがって、この構成は v6.1.1 から廃止され、推奨されなくなりました。

-   バックアップ中に S3 へのマルチパート アップロードを実行するときに使用されるパート サイズ。この設定の値を調整して、S3 に送信されるリクエストの数を制御できます。
-   データが S3 にバックアップされ、バックアップ ファイルがこの構成項目の値よりも大きい場合、 [マルチパートアップロード](https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPart.html)が自動的に有効になります。圧縮率に基づくと、96 MiBリージョンによって生成されるバックアップ ファイルは、約 10 MiB から 30 MiB です。
-   デフォルト値: 5MiB

## backup.hadoop {#backup-hadoop}

### <code>home</code> {#code-home-code}

-   HDFS シェル コマンドの場所を指定し、TiKV がシェル コマンドを検索できるようにします。この構成項目は、環境変数`$HADOOP_HOME`と同じ効果があります。
-   デフォルト値: `""`

### <code>linux-user</code> {#code-linux-user-code}

-   TiKV が HDFS シェル コマンドを実行する Linux ユーザーを指定します。
-   この構成項目が設定されていない場合、TiKV は現在の Linux ユーザーを使用します。
-   デフォルト値: `""`

## ログバックアップ {#log-backup}

ログバックアップに関するコンフィグレーション項目です。

### <span class="version-mark">v6.2.0 の新</span><code>enable</code> {#code-enable-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログのバックアップを有効にするかどうかを決定します。
-   デフォルト値: `true`

### <code>file-size-limit</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-file-size-limit-code-span-class-version-mark-new-in-v6-2-0-span}

-   保存するバックアップ ログ データのサイズ制限。
-   デフォルト値: 256MiB
-   注: 通常、 `file-size-limit`の値は、外部storageに表示されるバックアップ ファイルのサイズよりも大きくなります。これは、バックアップ ファイルが外部storageにアップロードされる前に圧縮されるためです。

### <code>initial-scan-pending-memory-quota</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-initial-scan-pending-memory-quota-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ バックアップ中にインクリメンタル スキャン データを格納するために使用されるキャッシュのクォータ。
-   デフォルト値: `min(Total machine memory * 10%, 512 MB)`

### <code>initial-scan-rate-limit</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-initial-scan-rate-limit-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ バックアップ中の増分データ スキャンのスループットのレート制限。
-   デフォルト値: 60。これは、レート制限がデフォルトで 60 MB/秒であることを示します。

### <code>max-flush-interval</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-max-flush-interval-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログバックアップでバックアップデータを外部storageに書き込む最大間隔。
-   デフォルト値: 3 分

### <span class="version-mark">v6.2.0 の新</span><code>num-threads</code> {#code-num-threads-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ バックアップで使用されるスレッドの数。
-   デフォルト値: CPU * 0.5
-   値の範囲: [2, 12]

### <code>temp-path</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-temp-path-code-span-class-version-mark-new-in-v6-2-0-span}

-   外部storageにフラッシュされる前にログ ファイルが書き込まれる一時パス。
-   デフォルト値: `${deploy-dir}/data/log-backup-temp`

## CDC {#cdc}

TiCDC に関連するコンフィグレーション項目。

### <code>min-ts-interval</code> {#code-min-ts-interval-code}

-   Resolved TS が計算されて転送される間隔。
-   デフォルト値: `"200ms"`

### <code>old-value-cache-memory-quota</code> {#code-old-value-cache-memory-quota-code}

-   TiCDC の古い値によるメモリ使用量の上限。
-   デフォルト値: `512MB`

### <code>sink-memory-quota</code> {#code-sink-memory-quota-code}

-   TiCDC データ変更イベントによるメモリ使用量の上限。
-   デフォルト値: `512MB`

### <code>incremental-scan-speed-limit</code> {#code-incremental-scan-speed-limit-code}

-   履歴データがインクリメンタル スキャンされる最大速度。
-   デフォルト値: `"128MB"` 。これは、1 秒あたり 128 MB を意味します。

### <code>incremental-scan-threads</code> {#code-incremental-scan-threads-code}

-   履歴データを増分スキャンするタスクのスレッド数。
-   デフォルト値: `4` 。これは 4 つのスレッドを意味します。

### <code>incremental-scan-concurrency</code> {#code-incremental-scan-concurrency-code}

-   履歴データを増分スキャンするタスクの同時実行の最大数。
-   デフォルト値: `6` 。これは、最大で 6 つのタスクを同時に実行できることを意味します。
-   注: `incremental-scan-concurrency`の値は`incremental-scan-threads`の値以上である必要があります。そうしないと、TiKV は起動時にエラーを報告します。

## resolved-ts {#resolved-ts}

ステイル読み取り要求を処理するための解決済み TS の維持に関連するコンフィグレーション項目。

### <code>enable</code> {#code-enable-code}

-   すべての地域の解決済み TS を維持するかどうかを決定します。
-   デフォルト値: `true`

### <code>advance-ts-interval</code> {#code-advance-ts-interval-code}

-   Resolved TS が計算されて転送される間隔。
-   デフォルト値:
    -   TiDB v6.5.0 の場合、デフォルト値は`"1s"`です。
    -   TiDB v6.5.1 以降の v6.5.x バージョンの場合、デフォルト値は`"20s"`です。

### <code>scan-lock-pool-size</code> {#code-scan-lock-pool-size-code}

-   解決済み TS を初期化するときに、TiKV が MVCC (マルチバージョン同時実行制御) ロック データをスキャンするために使用するスレッドの数。
-   デフォルト値: `2` 。これは 2 つのスレッドを意味します。

## pessimistic-txn {#pessimistic-txn}

悲観的トランザクションの使用法については、 [TiDB ペシミスティックトランザクションモード](/pessimistic-transaction.md)を参照してください。

### <code>wait-for-lock-timeout</code> {#code-wait-for-lock-timeout-code}

-   TiKV の悲観的トランザクションが、他のトランザクションがロックを解放するまで待機する最長時間。タイムアウトになると、TiDB にエラーが返され、TiDB はロックの追加を再試行します。ロック待機タイムアウトは`innodb_lock_wait_timeout`で設定されます。
-   デフォルト値: `"1s"`
-   最小値: `"1ms"`

### <code>wake-up-delay-duration</code> {#code-wake-up-delay-duration-code}

-   悲観的トランザクションがロックを解放すると、ロックを待っているすべてのトランザクションのうち、最小の`start_ts`のトランザクションのみが起こされます。他のトランザクションは`wake-up-delay-duration`後に起こされます。
-   デフォルト値: `"20ms"`

### <code>pipelined</code> {#code-pipelined-code}

-   この構成アイテムは、悲観的ロックを追加するパイプライン プロセスを有効にします。この機能を有効にすると、データをロックできることを検出した後、TiKV は直ちに TiDB に通知して後続のリクエストを実行し、悲観的ロックを非同期で書き込みます。これにより、ほとんどのレイテンシーが短縮され、悲観的トランザクションのパフォーマンスが大幅に向上します。しかし、悲観的ロックの非同期書き込みが失敗する可能性はまだ低く、悲観的トランザクション コミットの失敗を引き起こす可能性があります。
-   デフォルト値: `true`

### <span class="version-mark">v6.0.0 の新</span><code>in-memory</code> {#code-in-memory-code-span-class-version-mark-new-in-v6-0-0-span}

-   インメモリの悲観的ロック機能を有効にします。この機能を有効にすると、悲観的トランザクションは、ロックをディスクに書き込んだり、ロックを他のレプリカに複製したりする代わりに、ロックをメモリに保存しようとします。これにより、悲観的トランザクションのパフォーマンスが向上します。ただし、悲観的ロックが失われ、悲観的トランザクションのコミットが失敗する可能性はまだ低いです。
-   デフォルト値: `true`
-   `in-memory` `pipelined`の値が`true`の場合にのみ有効であることに注意してください。

## クォータ {#quota}

Quota Limiter に関連するコンフィグレーション項目。

### <code>max-delay-duration</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-max-delay-duration-code-span-class-version-mark-new-in-v6-0-0-span}

-   単一の読み取りまたは書き込み要求が、フォアグラウンドで処理されるまで強制的に待機される最大時間。
-   デフォルト値: `500ms`
-   推奨設定: ほとんどの場合、デフォルト値を使用することをお勧めします。インスタンスでメモリ不足 (OOM) または激しいパフォーマンス ジッターが発生した場合、値を 1S に設定して、リクエストの待機時間を 1 秒未満にすることができます。

### フォアグラウンド クォータ リミッター {#foreground-quota-limiter}

フォアグラウンド Quota Limiter に関連するコンフィグレーション項目。

TiKV がデプロイされているマシンのリソースが限られているとします (たとえば、4v CPU と 16 Gメモリのみ)。この状況では、TiKV のフォアグラウンドが処理する読み取りおよび書き込み要求が多すぎるため、バックグラウンドで使用される CPU リソースがそのような要求の処理を支援するために占有され、TiKV のパフォーマンスの安定性に影響を与える可能性があります。この状況を回避するには、フォアグラウンド クォータ関連の構成項目を使用して、フォアグラウンドで使用される CPU リソースを制限します。リクエストが Quota Limiter をトリガーすると、リクエストは TiKV が CPU リソースを解放するまでしばらく待機する必要があります。正確な待機時間はリクエストの数によって異なり、最大待機時間は[`max-delay-duration`](#max-delay-duration-new-in-v600)の値を超えません。

#### <code>foreground-cpu-time</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-foreground-cpu-time-code-span-class-version-mark-new-in-v6-0-0-span}

-   TiKV フォアグラウンドが読み取りおよび書き込み要求を処理するために使用する CPU リソースのソフト制限。
-   デフォルト値: `0` (制限なし)
-   単位: millicpu (たとえば、 `1500` 、フォアグラウンド リクエストが 1.5v CPU を消費することを意味します)
-   推奨設定: コアが 4 つを超えるインスタンスの場合は、デフォルト値`0`を使用します。 4 コアのインスタンスの場合、値を`1000`から`1500`の範囲に設定すると、バランスを取ることができます。 2 コアのインスタンスの場合は、値を`1200`より小さくしてください。

#### <code>foreground-write-bandwidth</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-foreground-write-bandwidth-code-span-class-version-mark-new-in-v6-0-0-span}

-   トランザクションがデータを書き込む帯域幅のソフト リミット。
-   デフォルト値: `0KB` (制限なし)
-   推奨される設定: `foreground-cpu-time`設定では書き込み帯域幅を制限するのに十分でない場合を除き、ほとんどの場合、デフォルト値の`0`を使用します。このような例外のため、コア数が 4 以下のインスタンスでは`50MB`より小さい値を設定することをお勧めします。

#### <code>foreground-read-bandwidth</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-foreground-read-bandwidth-code-span-class-version-mark-new-in-v6-0-0-span}

-   トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限。
-   デフォルト値: `0KB` (制限なし)
-   推奨される設定: `foreground-cpu-time`設定が読み取り帯域幅を制限するのに十分でない場合を除き、ほとんどの場合、既定値の`0`を使用します。このような例外のため、コア数が 4 以下のインスタンスでは`20MB`より小さい値を設定することをお勧めします。

### バックグラウンド クォータ リミッター {#background-quota-limiter}

バックグラウンド Quota Limiter に関連するコンフィグレーション項目。

TiKV がデプロイされているマシンのリソースが限られているとします (たとえば、4v CPU と 16 Gメモリのみ)。この状況では、TiKV のバックグラウンドが処理する計算や読み取り/書き込み要求が多すぎる可能性があり、フォアグラウンドで使用される CPU リソースがそのような要求の処理を支援するために占有され、TiKV のパフォーマンスの安定性に影響を与えます。この状況を回避するには、バックグラウンド クォータ関連の構成アイテムを使用して、バックグラウンドで使用される CPU リソースを制限します。リクエストが Quota Limiter をトリガーすると、リクエストは TiKV が CPU リソースを解放するまでしばらく待機する必要があります。正確な待機時間はリクエストの数によって異なり、最大待機時間は[`max-delay-duration`](#max-delay-duration-new-in-v600)の値を超えません。

> **警告：**
>
> -   バックグラウンド クォータ リミッターは、TiDB v6.2.0 で導入された実験的機能であり、本番環境で使用することは**お**勧めしません。
> -   この機能は、TiKV がこれらの環境で安定して実行できるように、リソースが限られている環境にのみ適しています。リソースが豊富な環境でこの機能を有効にすると、リクエスト量がピークに達したときにパフォーマンスが低下する可能性があります。

#### <code>background-cpu-time</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-background-cpu-time-code-span-class-version-mark-new-in-v6-2-0-span}

-   TiKV バックグラウンドが読み取りおよび書き込み要求を処理するために使用する CPU リソースのソフト制限。
-   デフォルト値: `0` (制限なし)
-   単位: millicpu (たとえば、 `1500`バックグラウンド要求が 1.5v CPU を消費することを意味します)

#### <code>background-write-bandwidth</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-background-write-bandwidth-code-span-class-version-mark-new-in-v6-2-0-span}

> **ノート：**
>
> この構成アイテムは`SHOW CONFIG`の結果で返されますが、現在設定しても効果はありません。

-   バックグラウンド トランザクションがデータを書き込む帯域幅のソフト リミット。
-   デフォルト値: `0KB` (制限なし)

#### <code>background-read-bandwidth</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-background-read-bandwidth-code-span-class-version-mark-new-in-v6-2-0-span}

> **ノート：**
>
> この構成アイテムは`SHOW CONFIG`の結果で返されますが、現在設定しても効果はありません。

-   バックグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト リミット。
-   デフォルト値: `0KB` (制限なし)

#### <code>enable-auto-tune</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-enable-auto-tune-code-span-class-version-mark-new-in-v6-2-0-span}

-   クォータの自動調整を有効にするかどうかを決定します。この構成項目が有効になっている場合、TiKV は、TiKV インスタンスの負荷に基づいて、バックグラウンド リクエストのクォータを動的に調整します。
-   デフォルト値: `false` (自動チューニングが無効であることを意味します)

## causal-ts <span class="version-mark">v6.1.0 の新機能</span> {#causal-ts-span-class-version-mark-new-in-v6-1-0-span}

TiKV API V2 が有効な場合のタイムスタンプの取得に関連するコンフィグレーション項目 ( `storage.api-version = 2` )。

書き込みレイテンシーを短縮するために、TiKV は定期的にタイムスタンプのバッチをローカルにフェッチしてキャッシュします。キャッシュされたタイムスタンプは、PD への頻繁なアクセスを回避し、短期間の TSO サービス障害を許容するのに役立ちます。

### <code>alloc-ahead-buffer</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-alloc-ahead-buffer-code-span-class-version-mark-new-in-v6-4-0-span}

-   事前に割り当てられた TSO キャッシュ サイズ (期間)。
-   この構成項目で指定された期間に基づいて、TiKV が TSO キャッシュを事前に割り当てることを示します。 TiKV は、前の期間に基づいて TSO の使用量を推定し、 `alloc-ahead-buffer`満たす TSO をローカルに要求してキャッシュします。
-   この構成項目は、TiKV API V2 が有効になっている場合に PD 障害の許容度を高めるためによく使用されます ( `storage.api-version = 2` )。
-   この構成項目の値を大きくすると、TSO の消費量と TiKV のメモリオーバーヘッドが増える可能性があります。十分な TSO を取得するには、PD の構成項目を[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)減らすことをお勧めします。
-   テストによると、 `alloc-ahead-buffer`がデフォルト値であり、PD リーダーに障害が発生して別のノードに切り替わると、書き込み要求でレイテンシーが短期間増加し、QPS が減少します (約 15%)。
-   ビジネスへの影響を避けるために、PD で`tso-update-physical-interval = "1ms"`を構成し、TiKV で次の構成項目を構成できます。
    -   `causal-ts.alloc-ahead-buffer = "6s"`
    -   `causal-ts.renew-batch-max-size = 65536`
    -   `causal-ts.renew-batch-min-size = 2048`
-   デフォルト値: `3s`

### <code>renew-interval</code> {#code-renew-interval-code}

-   ローカルにキャッシュされたタイムスタンプが更新される間隔。
-   `renew-interval`の間隔で、TiKV はタイムスタンプの更新のバッチを開始し、前の期間のタイムスタンプの消費と[`alloc-ahead-buffer`](#alloc-ahead-buffer-new-in-v640)の設定に従って、キャッシュされたタイムスタンプの数を調整します。このパラメータを大きすぎる値に設定すると、最新の TiKV ワークロードの変更が時間内に反映されません。このパラメータを小さすぎる値に設定すると、PD の負荷が増加します。書き込みトラフィックが激しく変動する場合、タイムスタンプが頻繁に使い尽くされる場合、および書き込みレイテンシーが増加する場合は、このパラメーターをより小さな値に設定できます。同時に、PD の負荷も考慮する必要があります。
-   デフォルト値: `"100ms"`

### <code>renew-batch-min-size</code> {#code-renew-batch-min-size-code}

-   タイムスタンプ要求の TSO の最小数。
-   TiKV は、前の期間のタイムスタンプの消費に応じて、キャッシュされたタイムスタンプの数を調整します。少数の TSO のみが必要な場合、TiKV は、数が`renew-batch-min-size`に達するまで、要求された TSO を減らします。アプリケーションで大量のバースト書き込みトラフィックが頻繁に発生する場合は、必要に応じてこのパラメーターをより大きな値に設定できます。このパラメーターは、単一の tikv サーバーのキャッシュ サイズであることに注意してください。パラメーターを大きすぎる値に設定し、クラスターに多くの tikv サーバーが含まれている場合、TSO の消費が速すぎます。
-   Grafana の**TiKV-RAW** &gt; <strong>Causal timestamp</strong>パネルでは、 <strong>TSO バッチ サイズは</strong>、アプリケーションのワークロードに従って動的に調整された、ローカルにキャッシュされたタイムスタンプの数です。このメトリックを参照して調整できます`renew-batch-min-size` 。
-   デフォルト値: `100`

### <code>renew-batch-max-size</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-renew-batch-max-size-code-span-class-version-mark-new-in-v6-4-0-span}

-   タイムスタンプ要求の TSO の最大数。
-   デフォルトの TSO 物理時間更新間隔 ( `50ms` ) では、PD は最大 262144 個の TSO を提供します。要求された TSO がこの数を超えると、PD はそれ以上 TSO を提供しません。この構成項目は、TSO の枯渇と、TSO の枯渇が他のビジネスに及ぼす逆の影響を回避するために使用されます。高可用性を改善するためにこの構成項目の値を増やす場合は、十分な TSO を得るために同時に値[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)減らす必要があります。
-   デフォルト値: `8192`
