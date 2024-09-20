---
title: TiKV Configuration File
summary: TiKV 構成ファイルについて学習します。
---

# TiKVコンフィグレーションファイル {#tikv-configuration-file}

<!-- markdownlint-disable MD001 -->

TiKV 構成ファイルは、コマンドライン パラメータよりも多くのオプションをサポートしています。 デフォルトの構成ファイルは[etc/config-template.toml](https://github.com/tikv/tikv/blob/release-7.5/etc/config-template.toml)にあり、名前を`config.toml`に変更することができます。

このドキュメントでは、コマンドラインパラメータに含まれないパラメータについてのみ説明します。詳細については、 [コマンドラインパラメータ](/command-line-flags-for-tikv-configuration.md)参照してください。

> **ヒント：**
>
> 設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

## グローバル構成 {#global-configuration}

### <code>abort-on-panic</code> {#code-abort-on-panic-code}

-   TiKV パニック時にプロセスを終了するために`abort()`呼び出すかどうかを設定します。このオプションは、TiKV がシステムでコア ダンプ ファイルを生成することを許可するかどうかに影響します。

    -   この設定項目の値が`false`の場合、TiKV がパニックになると、 `exit()`呼び出してプロセスを終了します。
    -   この設定項目の値が`true`の場合、TiKV パニックが発生すると、TiKV は`abort()`呼び出してプロセスを終了します。このとき、TiKV は終了時にシステムがコア ダンプ ファイルを生成することを許可します。コア ダンプ ファイルを生成するには、コア ダンプに関連するシステム設定も実行する必要があります (たとえば、 `ulimit -c`コマンドでコア ダンプ ファイルのサイズ制限を設定し、コア ダンプ パスを設定します。オペレーティング システムによって関連する設定は異なります)。コア ダンプ ファイルがディスク領域を占有しすぎて TiKV ディスク領域が不足するのを避けるため、コア ダンプ生成パスを TiKV データとは別のディスク パーティションに設定することをお勧めします。

-   デフォルト値: `false`

### <code>slow-log-file</code> {#code-slow-log-file-code}

-   スローログを保存するファイル
-   この設定項目が設定されておらず、 `log.file.filename`設定されている場合、スローログは`log.file.filename`で指定されたログファイルに出力されます。
-   `slow-log-file`も`log.file.filename`設定されていない場合、すべてのログはデフォルトで「stderr」に出力されます。
-   両方の設定項目が設定されている場合、通常ログは`log.file.filename`で指定したログファイルに出力され、スローログは`slow-log-file`で設定したログファイルに出力されます。
-   デフォルト値: `""`

### <code>slow-log-threshold</code> {#code-slow-log-threshold-code}

-   スローログを出力する閾値。処理時間がこの閾値より長い場合、スローログが出力されます。
-   デフォルト値: `"1s"`

### <code>memory-usage-limit</code> {#code-memory-usage-limit-code}

-   TiKV インスタンスのメモリ使用量の制限。TiKV のメモリ使用量がこのしきい値にほぼ達すると、メモリを解放するために内部キャッシュが削除されます。
-   ほとんどの場合、TiKV インスタンスは使用可能なシステムメモリの合計の 75% を使用するように設定されるため、この構成項目を明示的に指定する必要はありません。メモリの残りの 25% は OS ページ キャッシュ用に予約されています。詳細については[`storage.block-cache.capacity`](#capacity)参照してください。
-   1 台の物理マシンに複数の TiKV ノードを展開する場合でも、この構成項目を設定する必要はありません。この場合、TiKV インスタンスはメモリの`5/3 * block-cache.capacity`使用します。
-   さまざまなシステムメモリ容量の既定値は次のとおりです。

    -   システム=8G ブロックキャッシュ=3.6G メモリ使用量制限=6G ページキャッシュ=2G
    -   システム=16G ブロックキャッシュ=7.2G メモリ使用量制限=12G ページキャッシュ=4G
    -   システム=32G ブロックキャッシュ=14.4G メモリ使用量制限=24G ページキャッシュ=8G

## ログ<span class="version-mark">v5.4.0 の新機能</span> {#log-span-class-version-mark-new-in-v5-4-0-span}

-   ログに関連するコンフィグレーション項目。

-   v5.4.0 から、TiKV と TiDB のログ設定項目の整合性を保つため、TiKV は以前の設定項目`log-rotation-timespan`廃止し、 `log-level` 、 `log-format` 、 `log-file` 、 `log-rotation-size`を次の設定項目に変更しました。古い設定項目のみを設定し、その値をデフォルト以外の値に設定した場合、古い項目は新しい項目と互換性が保たれます。古い設定項目と新しい設定項目の両方が設定されている場合は、新しい項目が有効になります。

### <code>level</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-level-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログレベル
-   `"error"` `"fatal"` `"warn"` `"debug"` `"info"`
-   デフォルト値: `"info"`

### <code>format</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-format-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログ形式
-   オプション値: `"json"` 、 `"text"`
-   デフォルト値: `"text"`

### <code>enable-timestamp</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-enable-timestamp-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログ内のタイムスタンプを有効にするか無効にするかを決定します
-   オプション値: `true` 、 `false`
-   デフォルト値: `true`

## log.file <span class="version-mark">v5.4.0 の新機能</span> {#log-file-span-class-version-mark-new-in-v5-4-0-span}

-   ログ ファイルに関連するコンフィグレーション項目。

### <code>filename</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-filename-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログファイル。この設定項目が設定されていない場合、ログはデフォルトで「stderr」に出力されます。この設定項目が設定されている場合、ログは対応するファイルに出力されます。
-   デフォルト値: `""`

### <code>max-size</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-max-size-code-span-class-version-mark-new-in-v5-4-0-span}

-   1 つのログ ファイルの最大サイズ。ファイル サイズがこの設定項目で設定された値より大きい場合、システムは 1 つのファイルを自動的に複数のファイルに分割します。
-   デフォルト値: `300`
-   最大値: `4096`
-   単位: MiB

### <code>max-days</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-max-days-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKV がログ ファイルを保持する最大日数。
    -   構成項目が設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKV はログ ファイルを消去しません。
    -   パラメータが`0`以外の値に設定されている場合、TiKV は`max-days`後に期限切れのログ ファイルをクリーンアップします。
-   デフォルト値: `0`

### <code>max-backups</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-max-backups-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKV が保持するログ ファイルの最大数。
    -   構成項目が設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKV はすべてのログ ファイルを保持します。
    -   構成項目が`0`以外の値に設定されている場合、TiKV は最大で`max-backups`で指定された数の古いログ ファイルを保持します。たとえば、値が`7`に設定されている場合、TiKV は最大 7 つの古いログ ファイルを保持します。
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

-   `HTTP` API サービスのワーカー スレッドの数
-   デフォルト値: `1`
-   最小値: `1`

### <code>grpc-compression-type</code> {#code-grpc-compression-type-code}

-   gRPCメッセージの圧縮アルゴリズム
-   `"deflate"` `"gzip"` : `"none"`
-   デフォルト値: `"none"`

### <code>grpc-concurrency</code> {#code-grpc-concurrency-code}

-   gRPC ワーカースレッドの数。gRPC スレッドプールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `5`
-   最小値: `1`

### <code>grpc-concurrent-stream</code> {#code-grpc-concurrent-stream-code}

-   gRPC ストリームで許可される同時リクエストの最大数
-   デフォルト値: `1024`
-   最小値: `1`

### <code>grpc-memory-pool-quota</code> {#code-grpc-memory-pool-quota-code}

-   gRPCで使用できるメモリサイズを制限します
-   デフォルト値: 制限なし
-   OOMが観測された場合はメモリを制限してください。使用量を制限すると潜在的なストールにつながる可能性があることに注意してください。

### <code>grpc-raft-conn-num</code> {#code-grpc-raft-conn-num-code}

-   Raft通信におけるTiKVノード間の最大接続数
-   デフォルト値: `1`
-   最小値: `1`

### <code>max-grpc-send-msg-len</code> {#code-max-grpc-send-msg-len-code}

-   送信できるgRPCメッセージの最大長を設定します
-   デフォルト値: `10485760`
-   単位: バイト
-   最大値: `2147483647`

### <code>grpc-stream-initial-window-size</code> {#code-grpc-stream-initial-window-size-code}

-   gRPC ストリームのウィンドウ サイズ
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

### <code>snap-io-max-bytes-per-sec</code> {#code-snap-io-max-bytes-per-sec-code}

-   スナップショット処理時の最大許容ディスク帯域幅
-   デフォルト値: `"100MiB"`
-   単位: KiB|MiB|GiB
-   最小値: `"1KiB"`

### <code>enable-request-batch</code> {#code-enable-request-batch-code}

-   リクエストをバッチ処理するかどうかを決定します
-   デフォルト値: `true`

### <code>labels</code> {#code-labels-code}

-   `{ zone = "us-west-1", disk = "ssd" }`などのサーバー属性を指定します。
-   デフォルト値: `{}`

### <code>background-thread-count</code> {#code-background-thread-count-code}

-   エンドポイント スレッド、 BRスレッド、分割チェック スレッド、リージョンスレッド、および遅延に影響されないタスクのその他のスレッドを含む、バックグラウンド プールの作業スレッド数。
-   デフォルト値: CPU コアの数が 16 未満の場合、デフォルト値は`2`です。それ以外の場合、デフォルト値は`3`です。

### <code>end-point-slow-log-threshold</code> {#code-end-point-slow-log-threshold-code}

-   TiDB のプッシュダウン要求がスロー ログを出力するための時間しきい値。処理時間がこのしきい値よりも長い場合、スロー ログが出力されます。
-   デフォルト値: `"1s"`
-   最小値: `0`

### <code>raft-client-queue-size</code> {#code-raft-client-queue-size-code}

-   TiKV 内のRaftメッセージのキューのサイズを指定します。時間内に送信されないメッセージが多すぎてバッファーがいっぱいになったり、メッセージが破棄されたりする場合は、システムの安定性を向上させるために、より大きな値を指定できます。
-   デフォルト値: `8192`

### <code>simplify-metrics</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-simplify-metrics-code-span-class-version-mark-new-in-v6-2-0-span}

-   返される監視メトリックを簡素化するかどうかを指定します。値を`true`に設定すると、TiKV は一部のメトリックを除外することで、各リクエストに対して返されるデータの量を削減します。
-   デフォルト値: `false`

### <code>forward-max-connections-per-address</code><span class="version-mark">バージョン 5.0.0 の新機能</span> {#code-forward-max-connections-per-address-code-span-class-version-mark-new-in-v5-0-0-span}

-   サービスとサーバーへのリクエスト転送用の接続プールのサイズを設定します。値を小さくしすぎると、リクエストのレイテンシーと負荷分散に影響します。
-   デフォルト値: `4`

## 読み取りプール統合 {#readpool-unified}

読み取り要求を処理する単一のスレッド プールに関連するコンフィグレーション項目。このスレッド プールは、バージョン 4.0 以降の元のstorageスレッド プールとコプロセッサ スレッド プールに代わるものです。

### <code>min-thread-count</code> {#code-min-thread-count-code}

-   統合読み取りプールの最小作業スレッド数
-   デフォルト値: `1`

### <code>max-thread-count</code> {#code-max-thread-count-code}

-   統合読み取りプールまたは UnifyReadPool スレッド プールの最大作業スレッド数。このスレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   値の範囲: `[min-thread-count, MAX(4, CPU quota * 10)]` 。 `MAX(4, CPU quota * 10)` `4`と`CPU quota * 10`のうち大きい方の値を取得します。
-   デフォルト値: MAX(4, CPU * 0.8)

> **注記：**
>
> スレッド数を増やすとコンテキストスイッチが増え、パフォーマンスが低下する可能性があります。この構成項目の値を変更することはお勧めしません。

### <code>stack-size</code> {#code-stack-size-code}

-   統合スレッドプール内のスレッドのスタックサイズ
-   タイプ: 整数 + 単位
-   デフォルト値: `"10MiB"`
-   単位: KiB|MiB|GiB
-   最小値: `"2MiB"`
-   最大値: システムで実行された`ulimit -sH`コマンドの結果に出力される K バイト数。

### <code>max-tasks-per-worker</code> {#code-max-tasks-per-worker-code}

-   統合読み取りプール内の単一スレッドに許可されるタスクの最大数。値を超えると`Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>auto-adjust-pool-size</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-auto-adjust-pool-size-code-span-class-version-mark-new-in-v6-3-0-span}

-   スレッド プールのサイズを自動的に調整するかどうかを制御します。有効にすると、現在の CPU 使用率に基づいて UnifyReadPool スレッド プールのサイズを自動的に調整することで、TiKV の読み取りパフォーマンスが最適化されます。スレッド プールの可能な範囲は`[max-thread-count, MAX(4, CPU)]`です。最大値は[`max-thread-count`](#max-thread-count)と同じです。
-   デフォルト値: `false`

## 読み取りプール。storage {#readpool-storage}

storageスレッド プールに関連するコンフィグレーション項目。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   storage要求に統合スレッドプール（ [`readpool.unified`](#readpoolunified)で設定）を使用するかどうかを決定します。このパラメータの値が`false`場合、このセクションの残りのパラメータ（ `readpool.storage` ）を通じて設定される別のスレッドプールが使用されます。
-   デフォルト値: このセクション( `readpool.storage` )に他の設定がない場合、デフォルト値は`true`です。それ以外の場合は、下位互換性のためにデフォルト値は`false`です。このオプションを有効にする前に、必要に応じて[`readpool.unified`](#readpoolunified)の設定を変更してください。

### <code>high-concurrency</code> {#code-high-concurrency-code}

-   優先度`read`リクエストを処理する同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。9 `8` `cpu num`場合、デフォルト値は`4`です。15 `16` `cpu num`場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>normal-concurrency</code> {#code-normal-concurrency-code}

-   通常優先度`read`リクエストを処理する同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。9 `8` `cpu num`場合、デフォルト値は`4`です。15 `16` `cpu num`場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>low-concurrency</code> {#code-low-concurrency-code}

-   低優先度`read`リクエストを処理する同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。9 `8` `cpu num`場合、デフォルト値は`4`です。15 `16` `cpu num`場合、デフォルト値は`8`です。
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
-   最大値: システムで実行された`ulimit -sH`コマンドの結果に出力される K バイト数。

## <code>readpool.coprocessor</code> {#code-readpool-coprocessor-code}

コプロセッサースレッド プールに関連するコンフィグレーション項目。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   コプロセッサ要求に統合スレッドプール（ [`readpool.unified`](#readpoolunified)で設定）を使用するかどうかを決定します。このパラメータの値が`false`場合、このセクションの残りのパラメータ（ `readpool.coprocessor` ）を通じて設定される別のスレッドプールが使用されます。
-   デフォルト値: このセクション( `readpool.coprocessor` )のパラメータが設定されていない場合、デフォルト値は`true`です。それ以外の場合、下位互換性のためにデフォルト値は`false`です。このパラメータを有効にする前に、 [`readpool.unified`](#readpoolunified)の設定項目を調整してください。

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

-   高優先度スレッド プール内の 1 つのスレッドに許可されるタスクの数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-normal</code> {#code-max-tasks-per-worker-normal-code}

-   通常優先度のスレッド プール内の 1 つのスレッドに許可されるタスクの数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-low</code> {#code-max-tasks-per-worker-low-code}

-   低優先度スレッド プール内の 1 つのスレッドに許可されるタスクの数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>stack-size</code> {#code-stack-size-code}

-   コプロセッサースレッドプール内のスレッドのスタックサイズ
-   タイプ: 整数 + 単位
-   デフォルト値: `"10MiB"`
-   単位: KiB|MiB|GiB
-   最小値: `"2MiB"`
-   最大値: システムで実行された`ulimit -sH`コマンドの結果に出力される K バイト数。

## storage {#storage}

storageに関するコンフィグレーション項目。

### <code>data-dir</code> {#code-data-dir-code}

-   RocksDBディレクトリのstorageパス
-   デフォルト値: `"./"`

### <code>engine</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-engine-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   エンジン タイプを指定します。この構成は、新しいクラスターを作成するときにのみ指定でき、指定した後は変更できません。
-   デフォルト値: `"raft-kv"`
-   値のオプション:

    -   `"raft-kv"` : TiDB v6.6.0 より前のバージョンのデフォルトのエンジン タイプ。
    -   `"partitioned-raft-kv"` : TiDB v6.6.0 で導入された新しいstorageエンジン タイプ。

### <code>scheduler-concurrency</code> {#code-scheduler-concurrency-code}

-   キーの同時操作を防止するための組み込みメモリロック メカニズム。各キーには、異なるスロットにハッシュがあります。
-   デフォルト値: `524288`
-   最小値: `1`

### <code>scheduler-worker-pool-size</code> {#code-scheduler-worker-pool-size-code}

-   スケジューラ スレッド プール内のスレッド数。スケジューラ スレッドは主に、データ書き込み前にトランザクションの一貫性をチェックするために使用されます。CPU コアの数が`16`以上の場合、デフォルト値は`8`です。それ以外の場合、デフォルト値は`4`です。スケジューラ スレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `4`
-   値の範囲: `[1, MAX(4, CPU)]` 。 `MAX(4, CPU)`の場合、 `CPU` CPU コアの数を意味します。 `MAX(4, CPU)` `4`と`CPU`のうち大きい方の値になります。

### <code>scheduler-pending-write-threshold</code> {#code-scheduler-pending-write-threshold-code}

-   書き込みキューの最大サイズ。この値を超えると、TiKV への新しい書き込みに対して`Server Is Busy`エラーが返されます。
-   デフォルト値: `"100MiB"`
-   単位: MiB|GiB

### <code>enable-async-apply-prewrite</code> {#code-enable-async-apply-prewrite-code}

-   非同期コミット トランザクションが、事前書き込み要求を適用する前に TiKV クライアントに応答するかどうかを決定します。この構成項目を有効にすると、適用期間が長い場合にレイテンシーを簡単に短縮したり、適用期間が安定していない場合に遅延ジッターを削減したりできます。
-   デフォルト値: `false`

### <code>reserve-space</code> {#code-reserve-space-code}

-   TiKV が起動すると、ディスク保護としてディスク上にいくらかのスペースが予約されます。残りのディスク スペースが予約されたスペースより少ない場合、TiKV は一部の書き込み操作を制限します。予約されたスペースは 2 つの部分に分かれており、予約されたスペースの 80% はディスク スペースが不足している場合の操作に必要な追加のディスク スペースとして使用され、残りの 20% は一時ファイルを保存するために使用されます。スペースを再利用するプロセスで、余分なディスク スペースを使いすぎてstorageが枯渇した場合、この一時ファイルはサービスを復元するための最後の保護として機能します。
-   一時ファイルの名前は`space_placeholder_file`で、 `storage.data-dir`ディレクトリにあります。ディスク容量が不足して TiKV がオフラインになった場合、TiKV を再起動すると、一時ファイルが自動的に削除され、TiKV は容量の再利用を試みます。
-   残りのスペースが不十分な場合、TiKV は一時ファイルを作成しません。保護の有効性は、予約されたスペースのサイズに関係します。予約されたスペースのサイズは、ディスク容量の 5% とこの構成値のいずれか大きい値です。この構成項目の値が`"0MiB"`の場合、TiKV はこのディスク保護機能を無効にします。
-   デフォルト値: `"5GiB"`
-   単位: MiB|GiB

### <code>enable-ttl</code> {#code-enable-ttl-code}

> **警告：**
>
> -   新しい TiKV クラスターを展開する**場合のみ、** `enable-ttl` `true`または`false`に設定してください。既存の TiKV クラスターでこの構成項目の値を変更し**ないでください**。異なる`enable-ttl`値を持つ TiKV クラスターは、異なるデータ形式を使用します。したがって、既存の TiKV クラスターでこの項目の値を変更すると、クラスターは異なる形式でデータを保存し、TiKV クラスターを再起動すると「非 TTL で TTL を有効にできません」というエラーが発生します。
> -   `enable-ttl` TiKV クラスター**でのみ**使用してください`storage.api-version = 2`が設定されていない限り、TiDB ノードを持つクラスターではこの構成項目を使用し**ないでください**(つまり、そのようなクラスターでは`enable-ttl`から`true`に設定します)。そうしないと、データの破損や TiDB クラスターのアップグレードの失敗などの重大な問題が発生します。

-   [10 ...](/time-to-live.md) 「Time to live」の略です。この項目を有効にすると、TiKV は TTL に達したデータを自動的に削除します。TTL の値を設定するには、クライアント経由でデータを書き込むときにリクエストで指定する必要があります。TTL が指定されていない場合、TiKV は対応するデータを自動的に削除しません。
-   デフォルト値: `false`

### <code>ttl-check-poll-interval</code> {#code-ttl-check-poll-interval-code}

-   物理スペースを再利用するためにデータをチェックする間隔。データが TTL に達すると、TiKV はチェック中に物理スペースを強制的に再利用します。
-   デフォルト値: `"12h"`
-   最小値: `"0s"`

### <code>background-error-recovery-window</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-background-error-recovery-window-code-span-class-version-mark-new-in-v6-1-0-span}

-   RocksDB が回復可能なバックグラウンド エラーを検出した後、TiKV が回復するまでの最大許容時間。バックグラウンド SST ファイルの一部が破損している場合、RocksDB は破損した SST ファイルが属するピアを特定した後、ハートビートを介して PD に報告します。次に、PD はこのピアを削除するスケジュール操作を実行します。最後に、破損した SST ファイルが直接削除され、TiKV バックグラウンドは再び通常どおりに動作します。
-   回復が完了するまで、破損した SST ファイルがまだ存在します。その間、RocksDB はデータの書き込みを続行できますが、破損した部分のデータが読み取られるとエラーが報告されます。
-   この時間枠内に回復が完了しない場合、TiKV はpanicになります。
-   デフォルト値: 1h

### <code>api-version</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-api-version-code-span-class-version-mark-new-in-v6-1-0-span}

-   TiKV が RawKV ストアとして機能する場合に TiKV によって使用されるstorage形式とインターフェース バージョン。
-   値のオプション:
    -   `1` : API V1 を使用し、クライアントから渡されたデータをエンコードせず、そのまま保存します。v6.1.0 より前のバージョンでは、TiKV はデフォルトで API V1 を使用します。
    -   `2` : API V2 を使用します:
        -   データは[マルチバージョン同時実行制御 (MVCC)](/glossary.md#multi-version-concurrency-control-mvcc)形式で保存され、タイムスタンプは tikv-server によって PD (TSO) から取得されます。
        -   データはさまざまな用途に応じてスコープ設定され、API V2 は単一クラスター内での TiDB、トランザクション KV、および RawKV アプリケーションの共存をサポートします。
        -   API V2 を使用する場合は、同時に`storage.enable-ttl = true`設定する必要があります。API V2 は TTL 機能をサポートしているため、 [`enable-ttl`](#enable-ttl)明示的にオンにする必要があります。そうしないと、 `storage.enable-ttl`デフォルトで`false`になるため、競合が発生します。
        -   API V2 が有効になっている場合、古いデータを再利用するには、少なくとも 1 つの tidb-server インスタンスをデプロイする必要があります。この tidb-server インスタンスは、読み取りサービスと書き込みサービスを同時に提供できます。高可用性を確保するために、複数の tidb-server インスタンスをデプロイできます。
        -   API V2 にはクライアントのサポートが必要です。詳細については、API V2 のクライアントの対応する手順を参照してください。
        -   v6.2.0 以降では、RawKV の変更データ キャプチャ (CDC) がサポートされています[生のKV CDC](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc)を参照してください。
-   デフォルト値: `1`

> **警告：**

> -   API V1 と API V2 はstorage形式が異なります。TiKV に TiDB データのみが含まれている場合に**のみ**、API V2 を直接有効または無効にすることができます。その他のシナリオでは、新しいクラスターをデプロイし、 [RawKV バックアップと復元](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)使用してデータを移行する必要があります。
> -   API V2 を有効にした後は、TiKV クラスターを v6.1.0 より前のバージョンにダウングレードする**ことはできません**。ダウングレードすると、データが破損する可能性があります。

## storage.block-cache {#storage-block-cache}

複数の RocksDBカラムファミリ (CF) 間でのブロックキャッシュの共有に関連するコンフィグレーション項目。

### <code>capacity</code> {#code-capacity-code}

-   共有ブロックキャッシュのサイズ。

-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値はシステムメモリの合計サイズの 45% になります。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値はシステムメモリの合計サイズの 30% になります。

-   単位: KiB|MiB|GiB

## storage.flow-control {#storage-flow-control}

TiKV のフロー制御メカニズムに関連するコンフィグレーション項目。このメカニズムは、RocksDB の書き込み停止メカニズムを置き換え、スケジューラレイヤーでフローを制御し、スタックしたRaftstoreまたは Apply スレッドによって引き起こされる二次災害を回避します。

### <code>enable</code> {#code-enable-code}

-   フロー制御メカニズムを有効にするかどうかを決定します。有効にすると、TiKV は KvDB の書き込みストール メカニズムと RaftDB (memtable を除く) の書き込みストール メカニズムを自動的に無効にします。
-   デフォルト値: `true`

### <code>memtables-threshold</code> {#code-memtables-threshold-code}

-   kvDB memtables の数がこのしきい値に達すると、フロー制御メカニズムが動作を開始します。 `enable` `true`に設定すると、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).max-write-buffer-number`オーバーライドします。
-   デフォルト値: `5`

### <code>l0-files-threshold</code> {#code-l0-files-threshold-code}

-   kvDB L0 ファイルの数がこのしきい値に達すると、フロー制御メカニズムが動作を開始します。 `enable` `true`に設定すると、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).level0-slowdown-writes-trigger`オーバーライドします。
-   デフォルト値: `20`

### <code>soft-pending-compaction-bytes-limit</code> {#code-soft-pending-compaction-bytes-limit-code}

-   KvDB 内の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムは一部の書き込み要求を拒否し始め、 `ServerIsBusy`エラーを報告します。 `enable` `true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).soft-pending-compaction-bytes-limit`オーバーライドします。
-   デフォルト値: `"192GiB"`

### <code>hard-pending-compaction-bytes-limit</code> {#code-hard-pending-compaction-bytes-limit-code}

-   KvDB 内の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し、 `ServerIsBusy`エラーを報告します。 `enable` `true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`オーバーライドします。
-   デフォルト値: `"1024GiB"`

## storage.io レート制限 {#storage-io-rate-limit}

I/O レート リミッターに関連するコンフィグレーション項目。

### <code>max-bytes-per-sec</code> {#code-max-bytes-per-sec-code}

-   サーバーが1 秒間にディスクに書き込んだり、ディスクから読み取ったりできる最大 I/O バイト数を制限します (以下の`mode`の構成項目によって決定されます)。この制限に達すると、TiKV はフォアグラウンド操作よりもバックグラウンド操作の調整を優先します。この構成項目の値は、ディスクの最適な I/O 帯域幅 (クラウド ディスク ベンダーによって指定された最大 I/O 帯域幅など) に設定する必要があります。この構成値が 0 に設定されている場合、ディスク I/O 操作は制限されません。
-   デフォルト値: `"0MiB"`

### <code>mode</code> {#code-mode-code}

-   どのタイプの I/O 操作がカウントされ、 `max-bytes-per-sec`しきい値未満に制限されるかを決定します。現在、書き込み専用モードのみがサポートされています。
-   `"all-io"` `"write-only"`オプション: `"read-only"`
-   デフォルト値: `"write-only"`

## 日付 {#pd}

### <code>enable-forwarding</code> <span class="version-mark">v5.0.0 の新機能</span> {#code-enable-forwarding-code-span-class-version-mark-new-in-v5-0-0-span}

-   ネットワークが分離される可能性がある場合に、TiKV の PD クライアントがフォロワー経由でリーダーにリクエストを転送するかどうかを制御します。
-   デフォルト値: `false`
-   環境に分離されたネットワークがある場合、このパラメータを有効にすると、サービスが利用できない期間を短縮できます。
-   分離、ネットワーク中断、またはダウンタイムが発生したかどうかを正確に判断できない場合、このメカニズムを使用すると誤判断のリスクがあり、可用性とパフォーマンスが低下します。ネットワーク障害が発生したことがない場合は、このパラメータを有効にすることはお勧めしません。

### <code>endpoints</code> {#code-endpoints-code}

-   PD のエンドポイント。複数のエンドポイントを指定する場合は、カンマで区切る必要があります。
-   デフォルト値: `["127.0.0.1:2379"]`

### <code>retry-interval</code> {#code-retry-interval-code}

-   PD 接続を再試行する間隔。
-   デフォルト値: `"300ms"`

### <code>retry-log-every</code> {#code-retry-log-every-code}

-   PD クライアントがエラーを観測したときにエラーの報告をスキップする頻度を指定します。たとえば、値が`5`の場合、PD クライアントがエラーを観測した後、クライアントは 4 回ごとにエラーの報告をスキップし、5 回ごとにエラーを報告します。
-   この機能を無効にするには、値を`1`に設定します。
-   デフォルト値: `10`

### <code>retry-max-count</code> {#code-retry-max-count-code}

-   PD接続の初期化を再試行する最大回数
-   再試行を無効にするには、値を`0`に設定します。再試行回数の制限を解除するには、値を`-1`に設定します。
-   デフォルト値: `-1`

## ラフトストア {#raftstore}

Raftstoreに関連するコンフィグレーション項目。

### <code>prevote</code> {#code-prevote-code}

-   `prevote`有効または無効にします。この機能を有効にすると、ネットワーク パーティションからの回復後にシステムのジッターが軽減されます。
-   デフォルト値: `true`

### <code>capacity</code> {#code-capacity-code}

-   storage容量。データを保存できる最大サイズです`capacity`指定しない場合は、現在のディスクの容量が優先されます。同じ物理ディスクに複数の TiKV インスタンスをデプロイするには、このパラメータを TiKV 構成に追加します。詳細については、 [ハイブリッド展開の主なパラメータ](/hybrid-deployment-topology.md#key-parameters)参照してください。
-   デフォルト値: `0`
-   単位: KiB|MiB|GiB

### <code>raftdb-path</code> {#code-raftdb-path-code}

-   Raftライブラリへのパス。デフォルトでは`storage.data-dir/raft`です。
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

-   ハートビートが送信されるときに経過したティックの数。これは、ハートビートが`raft-base-tick-interval` * `raft-heartbeat-ticks`の時間間隔で送信されることを意味します。
-   デフォルト値: `2`
-   最小値: `0`より大きい

### <code>raft-election-timeout-ticks</code> {#code-raft-election-timeout-ticks-code}

> **注記：**
>
> この構成項目は SQL ステートメントで照会することはできませんが、構成ファイルで構成できます。

-   Raft選出が開始されたときに経過したティックの数。つまり、 Raftグループにリーダーがいない場合は、約`raft-base-tick-interval` * `raft-election-timeout-ticks`の時間間隔後にリーダー選出が開始されます。
-   デフォルト値: `10`
-   最小値: `raft-heartbeat-ticks`

### <code>raft-min-election-timeout-ticks</code> {#code-raft-min-election-timeout-ticks-code}

> **注記：**
>
> この構成項目は SQL ステートメントで照会することはできませんが、構成ファイルで構成できます。

-   Raft選択が開始される最小ティック数。数値が`0`の場合、値`raft-election-timeout-ticks`が使用されます。このパラメータの値は`raft-election-timeout-ticks`以上である必要があります。
-   デフォルト値: `0`
-   最小値: `0`

### <code>raft-max-election-timeout-ticks</code> {#code-raft-max-election-timeout-ticks-code}

> **注記：**
>
> この構成項目は SQL ステートメントで照会することはできませんが、構成ファイルで構成できます。

-   Raft選択が開始される最大ティック数。数値が`0`の場合、 `raft-election-timeout-ticks` * `2`の値が使用されます。
-   デフォルト値: `0`
-   最小値: `0`

### <code>raft-max-size-per-msg</code> {#code-raft-max-size-per-msg-code}

> **注記：**
>
> この構成項目は SQL ステートメントで照会することはできませんが、構成ファイルで構成できます。

-   単一メッセージパケットのサイズに対するソフト制限
-   デフォルト値: `"1MiB"`
-   最小値: `0`より大きい
-   最大値: `3GiB`
-   単位: KiB|MiB|GiB

### <code>raft-max-inflight-msgs</code> {#code-raft-max-inflight-msgs-code}

> **注記：**
>
> この構成項目は SQL ステートメントで照会することはできませんが、構成ファイルで構成できます。

-   確認するRaftログの数。この数を超えると、 Raftステート マシンはログの送信速度を低下させます。
-   デフォルト値: `256`
-   最小値: `0`より大きい
-   最大値: `16384`

### <code>raft-entry-max-size</code> {#code-raft-entry-max-size-code}

-   1つのログの最大サイズに対するハード制限
-   デフォルト値: `"8MiB"`
-   最小値: `0`
-   単位: MiB|GiB

### <code>raft-log-compact-sync-interval</code> <span class="version-mark">v5.3 の新機能</span> {#code-raft-log-compact-sync-interval-code-span-class-version-mark-new-in-v5-3-span}

-   不要なRaftログを圧縮する時間間隔
-   デフォルト値: `"2s"`
-   最小値: `"0s"`

### <code>raft-log-gc-tick-interval</code> {#code-raft-log-gc-tick-interval-code}

-   Raftログを削除するポーリング タスクがスケジュールされる時間間隔`0`は、この機能が無効であることを意味します。
-   デフォルト値: `"3s"`
-   最小値: `"0s"`

### <code>raft-log-gc-threshold</code> {#code-raft-log-gc-threshold-code}

-   残存Raftの最大許容数に関するソフト制限
-   デフォルト値: `50`
-   最小値: `1`

### <code>raft-log-gc-count-limit</code> {#code-raft-log-gc-count-limit-code}

-   許容される残存Raftログ数のハード制限
-   デフォルト値: 3/4リージョンサイズに収容できるログ数 (ログごとに 1MiB として計算)
-   最小値: `0`

### <code>raft-log-gc-size-limit</code> {#code-raft-log-gc-size-limit-code}

-   残余Raftの許容サイズに関するハード制限
-   デフォルト値:リージョンサイズの 3/4
-   最小値: `0`より大きい

### <code>raft-log-reserve-max-ticks</code> <span class="version-mark">v5.3 の新機能</span> {#code-raft-log-reserve-max-ticks-code-span-class-version-mark-new-in-v5-3-span}

-   この設定項目で設定されたティック数が経過した後、残りのRaftログの数が`raft-log-gc-threshold`で設定された値に達していなくても、TiKV はこれらのログに対してガベージコレクション(GC) を実行します。
-   デフォルト値: `6`
-   最小値: `0`より大きい

### <code>raft-engine-purge-interval</code> {#code-raft-engine-purge-interval-code}

-   ディスク領域をできるだけ早くリサイクルするために、古い TiKV ログ ファイルを消去する間隔。Raft エンジンは交換可能なコンポーネントであるため、一部の実装では消去プロセスが必要になります。
-   デフォルト値: `"10s"`

### <code>raft-entry-cache-life-time</code> {#code-raft-entry-cache-life-time-code}

-   メモリ内のログキャッシュに許容される最大残り時間
-   デフォルト値: `"30s"`
-   最小値: `0`

### <code>hibernate-regions</code> {#code-hibernate-regions-code}

-   Hibernate リージョン を有効または無効にします。このオプションを有効にすると、長時間アイドル状態になっているリージョン は自動的に休止状態に設定されます。これにより、アイドル状態の Region のRaftリーダーとフォロワー間のハートビートメッセージによって発生する余分なオーバーヘッドが削減されます。1 `peer-stale-state-check-interval`使用すると、休止状態の Region のリーダーとフォロワー間のハートビートビート間隔を変更できます。
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

-   RocksDB 圧縮を手動でトリガーする必要があるかどうかを確認する時間間隔。1 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"5m"`
-   最小値: `0`

### <code>region-compact-check-step</code> {#code-region-compact-check-step-code}

-   手動圧縮の各ラウンドで一度にチェックされる領域の数
-   デフォルト値:

    -   `storage.engine="raft-kv"`場合、デフォルト値は`100`です。
    -   `storage.engine="partitioned-raft-kv"`場合、デフォルト値は`5`です。
-   最小値: `0`

### <code>region-compact-min-tombstones</code> {#code-region-compact-min-tombstones-code}

-   RocksDB 圧縮をトリガーするために必要なトゥームストーンの数
-   デフォルト値: `10000`
-   最小値: `0`

### <code>region-compact-tombstones-percent</code> {#code-region-compact-tombstones-percent-code}

-   RocksDB圧縮をトリガーするために必要な墓石の割合
-   デフォルト値: `30`
-   最小値: `1`
-   最大値: `100`

### <code>region-compact-min-redundant-rows</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-region-compact-min-redundant-rows-code-span-class-version-mark-new-in-v7-1-0-span}

-   RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の数。
-   デフォルト値: `50000`
-   最小値: `0`

### <code>region-compact-redundant-rows-percent</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-region-compact-redundant-rows-percent-code-span-class-version-mark-new-in-v7-1-0-span}

-   RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の割合。
-   デフォルト値: `20`
-   最小値: `1`
-   最大値: `100`

### <code>report-region-buckets-tick-interval</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-report-region-buckets-tick-interval-code-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> `report-region-buckets-tick-interval` 、TiDB v6.1.0 で導入された実験的機能です。本番環境での使用はお勧めしません。

-   `enable-region-bucket`が true の場合、TiKV がバケット情報を PD に報告する間隔。
-   デフォルト値: `10s`

### <code>pd-heartbeat-tick-interval</code> {#code-pd-heartbeat-tick-interval-code}

-   PD へのリージョンのハートビートがトリガーされる時間間隔`0`この機能が無効であることを意味します。
-   デフォルト値: `"1m"`
-   最小値: `0`

### <code>pd-store-heartbeat-tick-interval</code> {#code-pd-store-heartbeat-tick-interval-code}

-   ストアの PD へのハートビートがトリガーされる時間間隔`0`この機能が無効であることを意味します。
-   デフォルト値: `"10s"`
-   最小値: `0`

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
-   リカバリ シナリオでリージョンが TiKV でスナップショットをより速く生成できるようにするには、対応するワーカーの`snap-generator`スレッドの数を増やす必要があります。この構成項目を使用して、 `snap-generator`スレッド プールのサイズを増やすことができます。
-   デフォルト値: `2`
-   最小値: `1`

### <code>lock-cf-compact-interval</code> {#code-lock-cf-compact-interval-code}

-   TiKVがロックカラムファミリの手動圧縮をトリガーする時間間隔
-   デフォルト値: `"10m"`
-   最小値: `0`

### <code>lock-cf-compact-bytes-threshold</code> {#code-lock-cf-compact-bytes-threshold-code}

-   TiKV がロックカラムファミリの手動圧縮をトリガーするサイズ
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

-   ピアに許可される最長の非アクティブ期間。タイムアウトのあるピアは`down`としてマークされ、PD は後でそれを削除しようとします。
-   デフォルト値: `"10m"`
-   最小値: Hibernate リージョンが有効な場合、最小値は`peer-stale-state-check-interval * 2`です。Hibernate リージョンが無効な場合、最小値は`0`です。

### <code>max-leader-missing-duration</code> {#code-max-leader-missing-duration-code}

-   ピアがRaftグループにリーダーがいない状態を維持できる最長時間。この値を超えると、ピアは PD を使用してピアが削除されたかどうかを確認します。
-   デフォルト値: `"2h"`
-   最小値: `abnormal-leader-missing-duration`より大きい

### <code>abnormal-leader-missing-duration</code> {#code-abnormal-leader-missing-duration-code}

-   Raftグループにリーダーがいない状態でピアが存在できる最長時間。この値を超えると、ピアは異常とみなされ、メトリックとログにマークされます。
-   デフォルト値: `"10m"`
-   最小値: `peer-stale-state-check-interval`より大きい

### <code>peer-stale-state-check-interval</code> {#code-peer-stale-state-check-interval-code}

-   ピアがRaftグループにリーダーがいない状態にあるかどうかのチェックをトリガーする時間間隔。
-   デフォルト値: `"5m"`
-   最小値: `2 * election-timeout`より大きい

### <code>leader-transfer-max-log-lag</code> {#code-leader-transfer-max-log-lag-code}

-   Raftリーダー転送中に転送先に許可される失われたログの最大数
-   デフォルト値: `128`
-   最小値: `10`

### <code>max-snapshot-file-raw-size</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-max-snapshot-file-raw-size-code-span-class-version-mark-new-in-v6-1-0-span}

-   スナップショット ファイルのサイズがこの設定値を超えると、このファイルは複数のファイルに分割されます。
-   デフォルト値: `100MiB`
-   最小値: `100MiB`

### <code>snap-apply-batch-size</code> {#code-snap-apply-batch-size-code}

-   インポートされたスナップショットファイルをディスクに書き込むときに必要なメモリキャッシュサイズ
-   デフォルト値: `"10MiB"`
-   最小値: `0`
-   単位: MiB

### <code>consistency-check-interval</code> {#code-consistency-check-interval-code}

> **警告：**
>
> 一貫性チェックはクラスターのパフォーマンスに影響し、TiDB のガベージコレクションと互換性がないため、本番環境では有効にし**ない**ことをお勧めします。

-   一貫性チェックがトリガーされる時間間隔`0`は、この機能が無効であることを意味します。
-   デフォルト値: `"0s"`
-   最小値: `0`

### <code>raft-store-max-leader-lease</code> {#code-raft-store-max-leader-lease-code}

-   Raftリーダーの最も長い信頼期間
-   デフォルト値: `"9s"`
-   最小値: `0`

### <code>right-derive-when-split</code> {#code-right-derive-when-split-code}

-   リージョンが分割されるときに、新しいリージョンの開始キーを指定します。この構成項目が`true`に設定されている場合、開始キーは最大分割キーになります。この構成項目が`false`に設定されている場合、開始キーは元のリージョンの開始キーになります。
-   デフォルト値: `true`

### <code>merge-max-log-gap</code> {#code-merge-max-log-gap-code}

-   `merge`実行した場合に許容されるログの最大欠落数
-   デフォルト値: `10`
-   最小値: `raft-log-gc-count-limit`より大きい

### <code>merge-check-tick-interval</code> {#code-merge-check-tick-interval-code}

-   TiKVがリージョンのマージが必要かどうかをチェックする時間間隔
-   デフォルト値: `"2s"`
-   最小値: `0`より大きい

### <code>use-delete-range</code> {#code-use-delete-range-code}

-   `rocksdb delete_range`インターフェースからデータを削除するかどうかを決定します
-   デフォルト値: `false`

### <code>cleanup-import-sst-interval</code> {#code-cleanup-import-sst-interval-code}

-   期限切れの SST ファイルをチェックする時間間隔`0`は、この機能が無効であることを意味します。
-   デフォルト値: `"10m"`
-   最小値: `0`

### <code>local-read-batch-size</code> {#code-local-read-batch-size-code}

-   1バッチで処理される読み取り要求の最大数
-   デフォルト値: `1024`
-   最小値: `0`より大きい

### <code>apply-yield-write-size</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-apply-yield-write-size-code-span-class-version-mark-new-in-v6-4-0-span}

-   1 回のポーリングで、適用スレッドが 1 つの FSM (有限状態マシン) に書き込むことができる最大バイト数。これはソフト制限です。
-   デフォルト値: `"32KiB"`
-   最小値: `0`より大きい
-   単位: KiB|MiB|GiB

### <code>apply-max-batch-size</code> {#code-apply-max-batch-size-code}

-   Raftステート マシンは、BatchSystem によってデータ書き込み要求をバッチで処理します。この構成項目は、1 つのバッチで要求を処理できるRaftステート マシンの最大数を指定します。
-   デフォルト値: `256`
-   最小値: `0`より大きい
-   最大値: `10240`

### <code>apply-pool-size</code> {#code-apply-pool-size-code}

-   データをディスクにフラッシュするプール内の許容スレッド数。これは、適用スレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `2`
-   値の範囲: `[1, CPU * 10]` `CPU` CPU コアの数を意味します。

### <code>store-max-batch-size</code> {#code-store-max-batch-size-code}

-   Raftステート マシンは、BatchSystem によってログをディスクにフラッシュする要求をバッチで処理します。この構成項目は、1 つのバッチで要求を処理できるRaftステート マシンの最大数を指定します。
-   `hibernate-regions`が有効な場合、デフォルト値は`256`です。5 `hibernate-regions`無効な場合、デフォルト値は`1024`です。
-   最小値: `0`より大きい
-   最大値: `10240`

### <code>store-pool-size</code> {#code-store-pool-size-code}

-   Raft を処理するプール内の許容スレッド数、つまりRaftstoreスレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `2`
-   値の範囲: `[1, CPU * 10]` `CPU` CPU コアの数を意味します。

### <code>store-io-pool-size</code> <span class="version-mark">v5.3.0 の新機能</span> {#code-store-io-pool-size-code-span-class-version-mark-new-in-v5-3-0-span}

-   Raft I/O タスクを処理するスレッドの許容数。これは、StoreWriter スレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `0`
-   最小値: `0`

### <code>future-poll-size</code> {#code-future-poll-size-code}

-   `future`駆動するスレッドの許容数
-   デフォルト値: `1`
-   最小値: `0`より大きい

### <code>cmd-batch</code> {#code-cmd-batch-code}

-   リクエストのバッチ処理を有効にするかどうかを制御します。有効にすると、書き込みパフォーマンスが大幅に向上します。
-   デフォルト値: `true`

### <code>inspect-interval</code> {#code-inspect-interval-code}

-   一定の間隔で、TiKV はRaftstoreコンポーネントのレイテンシーを検査します。このパラメータは検査の間隔を指定します。レイテンシーがこの値を超えると、この検査はタイムアウトとしてマークされます。
-   タイムアウト検査の比率に基づいて、TiKV ノードが遅いかどうかを判断します。
-   デフォルト値: `"100ms"`
-   最小値: `"1ms"`

### <code>raft-write-size-limit</code> <span class="version-mark">v5.3.0 の新機能</span> {#code-raft-write-size-limit-code-span-class-version-mark-new-in-v5-3-0-span}

-   Raftデータがディスクに書き込まれるしきい値を決定します。データ サイズがこの設定項目の値より大きい場合、データはディスクに書き込まれます`store-io-pool-size`の値が`0`の場合、この設定項目は有効になりません。
-   デフォルト値: `1MiB`
-   最小値: `0`

### <code>report-min-resolved-ts-interval</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-report-min-resolved-ts-interval-code-span-class-version-mark-new-in-v6-0-0-span}

-   最小解決タイムスタンプが PD リーダーに報告される間隔を決定します。この値が`0`に設定されている場合、レポートは無効になります。
-   デフォルト値: v6.3.0 より前では、デフォルト値は`"0s"`です。v6.3.0 以降では、デフォルト値は`"1s"`で、これは最小の正の値です。
-   最小値: `0`
-   単位: 秒

### <code>evict-cache-on-memory-ratio</code> <span class="version-mark">v7.5.0 の新機能</span> {#code-evict-cache-on-memory-ratio-code-span-class-version-mark-new-in-v7-5-0-span}

-   TiKV のメモリ使用量がシステム使用可能メモリの 90% を超え、 Raftエントリ キャッシュが占有するメモリが使用メモリ* `evict-cache-on-memory-ratio`を超えると、TiKV はRaftエントリ キャッシュを削除します。
-   この値が`0`に設定されている場合、この機能は無効になっていることを意味します。
-   デフォルト値: `0.1`
-   最小値: `0`

## コプロセッサ {#coprocessor}

コプロセッサーに関連するコンフィグレーション項目。

### <code>split-region-on-table</code> {#code-split-region-on-table-code}

-   テーブルごとにリージョンを分割するかどうかを決定します。この機能は TiDB モードでのみ使用することをお勧めします。
-   デフォルト値: `false`

### <code>batch-split-limit</code> {#code-batch-split-limit-code}

-   バッチでのリージョン分割のしきい値。この値を大きくすると、リージョン分割が高速化されます。
-   デフォルト値: `10`
-   最小値: `1`

### <code>region-max-size</code> {#code-region-max-size-code}

-   リージョンの最大サイズ。この値を超えると、リージョンは複数のリージョンに分割されます。
-   デフォルト値: `region-split-size / 2 * 3`
-   単位: KiB|MiB|GiB

### <code>region-split-size</code> {#code-region-split-size-code}

-   新しく分割されたリージョンのサイズ。この値は推定値です。
-   デフォルト値: `"96MiB"`
-   単位: KiB|MiB|GiB

### <code>region-max-keys</code> {#code-region-max-keys-code}

-   リージョン内で許容されるキーの最大数。この値を超えると、リージョンは複数のリージョンに分割されます。
-   デフォルト値: `region-split-keys / 2 * 3`

### <code>region-split-keys</code> {#code-region-split-keys-code}

-   新しく分割されたリージョン内のキーの数。この値は推定値です。
-   デフォルト値: `960000`

### <code>consistency-check-method</code> {#code-consistency-check-method-code}

-   データの整合性チェックの方法を指定します
-   MVCC データの一貫性チェックの場合は値を`"mvcc"`に設定します。生データの一貫性チェックの場合は値を`"raw"`に設定します。
-   デフォルト値: `"mvcc"`

## コプロセッサ v2 {#coprocessor-v2}

### <code>coprocessor-plugin-directory</code> {#code-coprocessor-plugin-directory-code}

-   コンパイルされたコプロセッサ プラグインが配置されているディレクトリのパス。このディレクトリ内のプラグインは、TiKV によって自動的にロードされます。
-   この構成項目が設定されていない場合、コプロセッサ プラグインは無効になります。
-   デフォルト値: `"./coprocessors"`

### <code>enable-region-bucket</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-enable-region-bucket-code-span-class-version-mark-new-in-v6-1-0-span}

-   リージョンをバケットと呼ばれる小さな範囲に分割するかどうかを決定します。バケットは、スキャンの同時実行性を向上させるために同時クエリの単位として使用されます。バケットの設計の詳細については、 [動的サイズリージョン](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md)を参照してください。
-   デフォルト値: false

> **警告：**
>
> -   `enable-region-bucket` 、TiDB v6.1.0 で導入された実験的機能です。本番環境での使用はお勧めしません。
> -   この構成は、 `region-split-size`が`region-bucket-size`の 2 倍以上の場合にのみ意味を持ちます。それ以外の場合、バケットは実際には生成されません。
> -   `region-split-size`より大きな値に調整すると、パフォーマンスが低下し、スケジュールが遅くなるリスクがあります。

### <code>region-bucket-size</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-region-bucket-size-code-span-class-version-mark-new-in-v6-1-0-span}

-   `enable-region-bucket`が true の場合のバケットのサイズ。
-   デフォルト値: v7.3.0 以降では、デフォルト値が`96MiB`から`50MiB`に変更されます。

> **警告：**
>
> `region-bucket-size` 、TiDB v6.1.0 で導入された実験的機能です。本番環境での使用はお勧めしません。

## ロックスdb {#rocksdb}

RocksDBに関連するコンフィグレーション項目

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDB のバックグラウンド スレッドの数。RocksDB スレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値:
    -   CPU コア数が 10 の場合、デフォルト値は`9`です。
    -   CPU コア数が 8 の場合、デフォルト値は`7`です。
    -   CPU コア数が`N`の場合、デフォルト値は`max(2, min(N - 1, 9))`です。
-   最小値: `2`

### <code>max-background-flushes</code> {#code-max-background-flushes-code}

-   同時バックグラウンド メンバテーブル フラッシュ ジョブの最大数
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
-   デフォルト値: `"128MiB"`
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
    -   `"skip-any-corrupted-records"` : 災害後の復旧。データは可能な限り復旧され、破損したレコードはスキップされます。
-   デフォルト値: `"point-in-time"`

### <code>wal-dir</code> {#code-wal-dir-code}

-   WAL ファイルが保存されるディレクトリ。指定しない場合、WAL ファイルはデータと同じディレクトリに保存されます。
-   デフォルト値: `""`

### <code>wal-ttl-seconds</code> {#code-wal-ttl-seconds-code}

-   アーカイブされた WAL ファイルの存続時間。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: 秒

### <code>wal-size-limit</code> {#code-wal-size-limit-code}

-   アーカイブされた WAL ファイルのサイズ制限。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>max-total-wal-size</code> {#code-max-total-wal-size-code}

-   合計の最大 RocksDB WAL サイズ。これは`data-dir`ファイルのうち`*.log`のサイズです。
-   デフォルト値:

    -   `storage.engine="raft-kv"`場合、デフォルト値は`"4GiB"`です。
    -   `storage.engine="partitioned-raft-kv"`場合、デフォルト値は`1`です。

### <code>stats-dump-period</code> {#code-stats-dump-period-code}

-   統計がログに出力される間隔。
-   デフォルト値:

    -   `storage.engine="raft-kv"`場合、デフォルト値は`"10m"`です。
    -   `storage.engine="partitioned-raft-kv"`場合、デフォルト値は`"0"`です。

### <code>compaction-readahead-size</code> {#code-compaction-readahead-size-code}

-   RocksDB の圧縮中に先読み機能を有効にし、先読みデータのサイズを指定します。機械式ディスクを使用している場合は、値を少なくとも 2MiB に設定することをお勧めします。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>writable-file-max-buffer-size</code> {#code-writable-file-max-buffer-size-code}

-   WritableFileWriteで使用される最大バッファサイズ
-   デフォルト値: `"1MiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>use-direct-io-for-flush-and-compaction</code> {#code-use-direct-io-for-flush-and-compaction-code}

-   バックグラウンドのフラッシュと圧縮で読み取りと書き込みの両方に`O_DIRECT`使用するかどうかを決定します。このオプションのパフォーマンスへの影響: `O_DIRECT`有効にすると、OS バッファ キャッシュのバイパスと汚染が防止されますが、後続のファイル読み取りでは、バッファ キャッシュへの内容の再読み取りが必要になります。
-   デフォルト値: `false`

### <code>rate-bytes-per-sec</code> {#code-rate-bytes-per-sec-code}

-   RocksDBの圧縮レートリミッターによって許可される最大レート
-   デフォルト値: `10GiB`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>rate-limiter-refill-period</code> {#code-rate-limiter-refill-period-code}

-   I/O トークンが補充される頻度を制御します。値が小さいほど I/O バーストは減少しますが、CPU オーバーヘッドが増加します。
-   デフォルト値: `"100ms"`

### <code>rate-limiter-mode</code> {#code-rate-limiter-mode-code}

-   RocksDBの圧縮率制限モード
-   `"write-only"` `"all-io"` : `"read-only"`
-   デフォルト値: `"write-only"`

### <code>rate-limiter-auto-tuned</code> <span class="version-mark">v5.0 の新機能</span> {#code-rate-limiter-auto-tuned-code-span-class-version-mark-new-in-v5-0-span}

-   最近のワークロードに基づいて、RocksDB の圧縮レート リミッターの構成を自動的に最適化するかどうかを決定します。この構成を有効にすると、圧縮保留バイトが通常よりもわずかに多くなります。
-   デフォルト値: `true`

### <code>enable-pipelined-write</code> {#code-enable-pipelined-write-code}

-   パイプライン書き込みを有効にするかどうかを制御します。この構成を有効にすると、以前のパイプライン書き込みが使用されます。この構成を無効にすると、新しいパイプラインコミット メカニズムが使用されます。
-   デフォルト値: `false`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   ファイルが非同期的に書き込まれている間に、OSがファイルをディスクに段階的に同期する速度
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
> v5.4.0 以降、RocksDB ログは TiKV のログ モジュールによって管理されます。そのため、この構成項目は非推奨となり、その機能は構成項目[`log.file.max-size`](#max-size-new-in-v540)に置き換えられました。

-   情報ログの最大サイズ
-   デフォルト値: `"1GiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>info-log-roll-time</code> {#code-info-log-roll-time-code}

> **警告：**
>
> v5.4.0 以降、RocksDB ログは TiKV のログ モジュールによって管理されます。したがって、この構成項目は非推奨です。TiKV は時間に基づく自動ログ分割をサポートしなくなりました。代わりに、構成項目[`log.file.max-size`](#max-size-new-in-v540)使用して、ファイル サイズに基づく自動ログ分割のしきい値を設定できます。

-   情報ログが切り捨てられる時間間隔。値が`0s`の場合、ログは切り捨てられません。
-   デフォルト値: `"0s"`

### <code>info-log-keep-log-file-num</code> {#code-info-log-keep-log-file-num-code}

> **警告：**
>
> v5.4.0 以降、RocksDB ログは TiKV のログ モジュールによって管理されます。そのため、この構成項目は非推奨となり、その機能は構成項目[`log.file.max-backups`](#max-backups-new-in-v540)に置き換えられました。

-   保存されるログファイルの最大数
-   デフォルト値: `10`
-   最小値: `0`

### <code>info-log-dir</code> {#code-info-log-dir-code}

-   ログが保存されるディレクトリ
-   デフォルト値: `""`

### <code>info-log-level</code> {#code-info-log-level-code}

> **警告：**
>
> v5.4.0 以降、RocksDB ログは TiKV のログ モジュールによって管理されます。そのため、この構成項目は非推奨となり、その機能は構成項目[`log.level`](#level-new-in-v540)に置き換えられました。

-   RocksDBのログレベル
-   デフォルト値: `"info"`

### <code>write-buffer-flush-oldest-first</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-write-buffer-flush-oldest-first-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   現在の RocksDB の`memtable`のメモリ使用量がしきい値に達したときに使用するフラッシュ戦略を指定します。
-   デフォルト値: `false`
-   値のオプション:

    -   データ量が最も大きい`false` : `memtable`が SST ファイルにフラッシュされます。
    -   `true` : 最も古い`memtable`が SST ファイルにフラッシュされます。この戦略では、コールド データの`memtable`をクリアできるため、コールド データとホット データが明確に区別できるシナリオに適しています。

### <code>write-buffer-limit</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-write-buffer-limit-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   単一の TiKV 内のすべての RocksDB インスタンスの合計メモリ制限を`memtable`に指定します。3 `0`制限がないことを意味します。

-   デフォルト値:

    -   `storage.engine="raft-kv"`場合、デフォルト値は`0`となり、制限がないことを意味します。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値はシステムメモリの合計サイズの 20% になります。

-   単位: KiB|MiB|GiB

### <code>track-and-verify-wals-in-manifest</code> <span class="version-mark">v6.5.9、v7.1.5、v7.5.2 の新機能</span> {#code-track-and-verify-wals-in-manifest-code-span-class-version-mark-new-in-v6-5-9-v7-1-5-and-v7-5-2-span}

-   RocksDB MANIFEST ファイルに Write Ahead Log (WAL) ファイルに関する情報を記録するかどうか、および起動時に WAL ファイルの整合性を検証するかどうかを制御します。詳細については、RocksDB [MANIFEST で WAL を追跡する](https://github.com/facebook/rocksdb/wiki/Track-WAL-in-MANIFEST)を参照してください。
-   デフォルト値: `false`
-   値のオプション:
    -   `true` : MANIFEST ファイルに WAL ファイルに関する情報を記録し、起動時に WAL ファイルの整合性を検証します。
    -   `false` : MANIFEST ファイルに WAL ファイルに関する情報を記録せず、起動時に WAL ファイルの整合性を検証しません。

## ロックスdb.titan {#rocksdb-titan}

Titanに関連するコンフィグレーション項目。

### <code>enabled</code> {#code-enabled-code}

-   Titanを有効または無効にする
-   デフォルト値: `false`

### <code>dirname</code> {#code-dirname-code}

-   Titan Blobファイルが保存されるディレクトリ
-   デフォルト値: `"titandb"`

### <code>disable-gc</code> {#code-disable-gc-code}

-   Titan が BLOB ファイルに対して実行するガベージ コレクション (GC) を無効にするかどうかを決定します。
-   デフォルト値: `false`

### <code>max-background-gc</code> {#code-max-background-gc-code}

-   Titan の GC スレッドの最大数
-   デフォルト値: `4`
-   最小値: `1`

## rocksdb.defaultcf | rocksdb.writecf | rocksdb.lockcf {#rocksdb-defaultcf-rocksdb-writecf-rocksdb-lockcf}

`rocksdb.defaultcf` `rocksdb.lockcf` `rocksdb.writecf`するコンフィグレーション項目。

### <code>block-size</code> {#code-block-size-code}

-   RocksDBブロックのデフォルトサイズ
-   `defaultcf`と`writecf`のデフォルト値: `"32KiB"`
-   `lockcf`のデフォルト値: `"16KiB"`
-   最小値: `"1KiB"`
-   単位: KiB|MiB|GiB

### <code>block-cache-size</code> {#code-block-cache-size-code}

> **警告：**
>
> v6.6.0 以降では、この構成は非推奨です。

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

-   インデックスとフィルターのキャッシュを有効または無効にする
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
-   `writecf`と`lockcf`のデフォルト値: `false`

### <code>optimize-filters-for-memory</code> <span class="version-mark">v7.2.0 の新機能</span> {#code-optimize-filters-for-memory-code-span-class-version-mark-new-in-v7-2-0-span}

-   メモリの内部断片化を最小限に抑えるブルーム/リボン フィルターを生成するかどうかを決定します。
-   この構成項目は[`format-version`](#format-version-new-in-v620) &gt;= 5 の場合にのみ有効になることに注意してください。
-   デフォルト値: `false`

### <code>whole-key-filtering</code> {#code-whole-key-filtering-code}

-   キー全体をブルームフィルターに入れるかどうかを決定します
-   `defaultcf`と`lockcf`のデフォルト値: `true`
-   `writecf`のデフォルト値: `false`

### <code>bloom-filter-bits-per-key</code> {#code-bloom-filter-bits-per-key-code}

-   ブルームフィルターが各キーに予約する長さ
-   デフォルト値: `10`
-   単位: バイト

### <code>block-based-bloom-filter</code> {#code-block-based-bloom-filter-code}

-   各ブロックがブルームフィルターを作成するかどうかを決定します
-   デフォルト値: `false`

### <code>ribbon-filter-above-level</code> <span class="version-mark">v7.2.0 の新機能</span> {#code-ribbon-filter-above-level-code-span-class-version-mark-new-in-v7-2-0-span}

-   この値以上のレベルにはリボン フィルターを使用し、この値未満のレベルには非ブロックベースのブルーム フィルターを使用するかどうかを決定します。この構成項目が設定されている場合、 [`block-based-bloom-filter`](#block-based-bloom-filter)無視されます。
-   この構成項目は[`format-version`](#format-version-new-in-v620) &gt;= 5 の場合にのみ有効になることに注意してください。
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

-   最レイヤーの圧縮アルゴリズムを設定します。この設定項目は`compression-per-level`設定を上書きします。
-   RocksDB は、データが LSM ツリーに書き込まれてから、 `compression-per-level`レイヤーで指定された最後の圧縮アルゴリズムを最下層に直接採用しません`bottommost-level-compression`により、最レイヤーは最初から圧縮効果が最も高い圧縮アルゴリズムを使用できるようになります。
-   最レイヤーに圧縮アルゴリズムを設定しない場合は、この構成項目の値を`disable`に設定します。
-   デフォルト値: `"zstd"`

### <code>write-buffer-size</code> {#code-write-buffer-size-code}

-   メモリテーブルのサイズ
-   `defaultcf`と`writecf`のデフォルト値: `"128MiB"`
-   `lockcf`のデフォルト値:
    -   `storage.engine="raft-kv"`場合、デフォルト値は`"32MiB"`です。
    -   `storage.engine="partitioned-raft-kv"`場合、デフォルト値は`"4MiB"`です。
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>max-write-buffer-number</code> {#code-max-write-buffer-number-code}

-   memtable の最大数`storage.flow-control.enable` `true`に設定すると、 `storage.flow-control.memtables-threshold`この構成項目を上書きします。
-   デフォルト値: `5`
-   最小値: `0`

### <code>min-write-buffer-number-to-merge</code> {#code-min-write-buffer-number-to-merge-code}

-   フラッシュをトリガーするために必要な最小のmemtable数
-   デフォルト値: `1`
-   最小値: `0`

### <code>max-bytes-for-level-base</code> {#code-max-bytes-for-level-base-code}

-   基本レベル (レベル 1) の最大バイト数。通常、memtable のサイズの 4 倍に設定されます。レベル 1 のデータ サイズが制限値の`max-bytes-for-level-base`に達すると、レベル 1 の SST ファイルと、それらに重複するレベル 2 の SST ファイルが圧縮されます。
-   `defaultcf`と`writecf`のデフォルト値: `"512MiB"`
-   `lockcf`のデフォルト値: `"128MiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB
-   不要な圧縮を減らすために、 `max-bytes-for-level-base`の値は L0 のデータ量とほぼ同じに設定することをお勧めします。たとえば、圧縮方法が「no:no:lz4:lz4:lz4:lz4:lz4」の場合、 `max-bytes-for-level-base`の値は`write-buffer-size * 4`にする必要があります。これは、L0 と L1 の圧縮がなく、L0 の圧縮のトリガー条件は SST ファイルの数が 4 (デフォルト値) に達することであるためです。L0 と L1 の両方で圧縮が採用されている場合、memtable から圧縮された SST ファイルのサイズを理解するには、RocksDB ログを分析する必要があります。たとえば、ファイル サイズが 32 MiB の場合、 `max-bytes-for-level-base`の値を 128 MiB ( `32 MiB * 4` ) に設定することをお勧めします。

### <code>target-file-size-base</code> {#code-target-file-size-base-code}

-   ベース レベルでのターゲット ファイルのサイズ。値が`enable-compaction-guard` `true`場合、この値は`compaction-guard-max-output-file-size`で上書きされます。
-   デフォルト値: `"8MiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>level0-file-num-compaction-trigger</code> {#code-level0-file-num-compaction-trigger-code}

-   圧縮をトリガーする L0 のファイルの最大数
-   `defaultcf`と`writecf`のデフォルト値: `4`
-   `lockcf`のデフォルト値: `1`
-   最小値: `0`

### <code>level0-slowdown-writes-trigger</code> {#code-level0-slowdown-writes-trigger-code}

-   書き込み停止をトリガーする L0 のファイルの最大数。1 `storage.flow-control.enable` `true`に設定すると、 `storage.flow-control.l0-files-threshold`この構成項目を上書きします。
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
    -   `"oldest-largest-seq-first"` : 更新時間が最も古いファイルの圧縮を優先します。この値は、狭い範囲でホットキーを更新する場合に**のみ**使用してください。
    -   `"oldest-smallest-seq-first"` : 長時間にわたって次のレベルに圧縮されない範囲を持つファイルの圧縮を優先します。キー空間全体でホット キーをランダムに更新する場合、この値によって書き込み増幅がわずかに減少する可能性があります。
    -   `"min-overlapping-ratio"` : 重複率の高いファイルの圧縮を優先します。ファイルのさまざまなレベルが小さい場合 ( `the file size in the next level` ÷ `the file size in this level`の結果が小さい場合)、TiKV はこのファイルを最初に圧縮します。多くの場合、この値により書き込み増幅を効果的に削減できます。
-   `defaultcf`と`writecf`のデフォルト値: `"min-overlapping-ratio"`
-   `lockcf`のデフォルト値: `"by-compensated-size"`

### <code>dynamic-level-bytes</code> {#code-dynamic-level-bytes-code}

-   動的レベルバイトを最適化するかどうかを決定します
-   デフォルト値: `true`

### <code>num-levels</code> {#code-num-levels-code}

-   RocksDB ファイル内の最大レベル数
-   デフォルト値: `7`

### <code>max-bytes-for-level-multiplier</code> {#code-max-bytes-for-level-multiplier-code}

-   各レイヤーのデフォルトの増幅倍数
-   デフォルト値: `10`

### <code>compaction-style</code> {#code-compaction-style-code}

-   圧縮方法
-   `"universal"` `"fifo"` : `"level"`
-   デフォルト値: `"level"`

### <code>disable-auto-compactions</code> {#code-disable-auto-compactions-code}

-   自動圧縮を無効にするかどうかを決定します。
-   デフォルト値: `false`

### <code>soft-pending-compaction-bytes-limit</code> {#code-soft-pending-compaction-bytes-limit-code}

-   保留中の圧縮バイトのソフト制限`storage.flow-control.enable` `true`に設定すると、 `storage.flow-control.soft-pending-compaction-bytes-limit`この構成項目を上書きします。
-   デフォルト値: `"192GiB"`
-   単位: KiB|MiB|GiB

### <code>hard-pending-compaction-bytes-limit</code> {#code-hard-pending-compaction-bytes-limit-code}

-   保留中の圧縮バイトのハード制限`storage.flow-control.enable` `true`に設定すると、 `storage.flow-control.hard-pending-compaction-bytes-limit`この構成項目を上書きします。
-   デフォルト値: `"256GiB"`
-   単位: KiB|MiB|GiB

### <code>enable-compaction-guard</code> {#code-enable-compaction-guard-code}

-   圧縮ガード (TiKVリージョン境界で SST ファイルを分割するための最適化) を有効または無効にします。この最適化により、圧縮 I/O を削減し、TiKV がより大きな SST ファイル サイズ (したがって、全体的な SST ファイルが少なくなる) を使用できるようになります。また、リージョンを移行するときに、古いデータを効率的にクリーンアップできるようになります。
-   `defaultcf`と`writecf`のデフォルト値: `true`
-   `lockcf`のデフォルト値: `false`

### <code>compaction-guard-min-output-file-size</code> {#code-compaction-guard-min-output-file-size-code}

-   圧縮ガードが有効な場合の最小 SST ファイル サイズ。この構成により、圧縮ガードが有効な場合に SST ファイルが小さすぎることが防止されます。
-   デフォルト値: `"8MiB"`
-   単位: KiB|MiB|GiB

### <code>compaction-guard-max-output-file-size</code> {#code-compaction-guard-max-output-file-size-code}

-   圧縮ガードが有効な場合の最大 SST ファイル サイズ。この構成により、圧縮ガードが有効な場合に SST ファイルが大きくなりすぎることが防止されます。この構成は、同じカラムファミリーの`target-file-size-base`オーバーライドします。
-   デフォルト値: `"128MiB"`
-   単位: KiB|MiB|GiB

### <code>format-version</code> <span class="version-mark">v6.2.0 の新</span>機能 {#code-format-version-code-span-class-version-mark-new-in-v6-2-0-span}

-   SST ファイルの形式バージョン。この構成項目は、新しく書き込まれたテーブルにのみ影響します。既存のテーブルの場合、バージョン情報はフッターから読み取られます。
-   オプションの値:
    -   `0` : すべての TiKV バージョンで読み取ることができます。デフォルトのチェックサム タイプは CRC32 であり、このバージョンではチェックサム タイプの変更はサポートされていません。
    -   `1` : すべての TiKV バージョンで読み取ることができます。xxHash などのデフォルト以外のチェックサム タイプをサポートします。RocksDB は、チェックサム タイプが CRC32 でない場合にのみデータを書き込みます。(バージョン`0`は自動的にアップグレードされます)
    -   `2` : すべての TiKV バージョンで読み取ることができます。LZ4、BZip2、Zlib 圧縮を使用して圧縮ブロックのエンコードを変更します。
    -   `3` : TiKV v2.1 以降のバージョンで読み取ることができます。インデックス ブロック内のキーのエンコードを変更します。
    -   `4` : TiKV v3.0 以降のバージョンで読み取ることができます。インデックス ブロック内の値のエンコードを変更します。
    -   `5` : TiKV v6.1 以降のバージョンで読み取ることができます。フル フィルターとパーティション フィルターは、異なるスキーマを使用した、より高速で正確なブルーム フィルター実装を使用します。
-   デフォルト値:

    -   `storage.engine="raft-kv"`場合、デフォルト値は`2`です。
    -   `storage.engine="partitioned-raft-kv"`場合、デフォルト値は`5`です。

### <code>ttl</code> <span class="version-mark">v7.2.0 の新機能</span> {#code-ttl-code-span-class-version-mark-new-in-v7-2-0-span}

-   TTL よりも古い更新を含む SST ファイルは、自動的に圧縮対象として選択されます。これらの SST ファイルは、カスケード方式で圧縮され、最下位レベルまたはファイルに圧縮されます。
-   デフォルト値: `"0s"` 。これは、デフォルトでは SST ファイルが選択されていないことを意味します。
-   単位: s(秒)|h(時間)|d(日)

### <code>periodic-compaction-seconds</code> <span class="version-mark">v7.2.0 の新機能</span> {#code-periodic-compaction-seconds-code-span-class-version-mark-new-in-v7-2-0-span}

-   定期的な圧縮の時間間隔。この値より古い更新を含む SST ファイルは圧縮対象として選択され、これらの SST ファイルが元々存在していたレベルと同じレベルに書き換えられます。
-   デフォルト値: `"0s"` 。これは、定期的な圧縮がデフォルトで無効になっていることを意味します。
-   単位: s(秒)|h(時間)|d(日)

## rocksdb.defaultcf.titan {#rocksdb-defaultcf-titan}

`rocksdb.defaultcf.titan`に関連するコンフィグレーション項目です。

### <code>min-blob-size</code> {#code-min-blob-size-code}

-   Blob ファイルに保存される最小の値。指定されたサイズより小さい値は LSM ツリーに保存されます。
-   デフォルト値: `"1KiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>blob-file-compression</code> {#code-blob-file-compression-code}

-   BLOBファイルで使用される圧縮アルゴリズム
-   `"lz4"` `"lz4hc"` `"bzip2"` `"no"` `"snappy"` `"zlib"` `"zstd"`
-   デフォルト値: `"lz4"`

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。Snappy 圧縮の他のバリエーションはサポートされていません。

### <code>blob-cache-size</code> {#code-blob-cache-size-code}

-   BLOBファイルのキャッシュサイズ
-   デフォルト値: `"0GiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>min-gc-batch-size</code> {#code-min-gc-batch-size-code}

-   GCを1回実行するために必要なBlobファイルの最小合計サイズ
-   デフォルト値: `"16MiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>max-gc-batch-size</code> {#code-max-gc-batch-size-code}

-   GC を 1 回実行できる BLOB ファイルの最大合計サイズ
-   デフォルト値: `"64MiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>discardable-ratio</code> {#code-discardable-ratio-code}

-   BLOB ファイルに対して GC がトリガーされる比率。BLOB ファイル内の無効な値の割合がこの比率を超える場合にのみ、BLOB ファイルが GC に選択されます。
-   デフォルト値: `0.5`
-   最小値: `0`
-   最大値: `1`

### <code>sample-ratio</code> {#code-sample-ratio-code}

-   GC 中にファイルをサンプリングするときの (Blob ファイルから読み取られたデータ / Blob ファイル全体) の比率
-   デフォルト値: `0.1`
-   最小値: `0`
-   最大値: `1`

### <code>merge-small-file-threshold</code> {#code-merge-small-file-threshold-code}

-   Blob ファイルのサイズがこの値より小さい場合でも、Blob ファイルは GC に選択される可能性があります。この場合、 `discardable-ratio`無視されます。
-   デフォルト値: `"8MiB"`
-   最小値: `0`
-   単位: KiB|MiB|GiB

### <code>blob-run-mode</code> {#code-blob-run-mode-code}

-   Titanの実行モードを指定します。
-   オプションの値:
    -   `normal` : 値のサイズが`min-blob-size`超えると、データを BLOB ファイルに書き込みます。
    -   `read_only` : BLOB ファイルへの新しいデータの書き込みを拒否しますが、BLOB ファイルから元のデータは読み取ります。
    -   `fallback` : BLOB ファイル内のデータを LSM に書き戻します。
-   デフォルト値: `normal`

### <code>level-merge</code> {#code-level-merge-code}

-   読み取りパフォーマンスを最適化するかどうかを決定します。1 `level-merge`有効にすると、書き込み増幅がさらに大きくなります。
-   デフォルト値: `false`

## ラフトDB {#raftdb}

`raftdb`に関連するコンフィグレーション項目

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDB のバックグラウンド スレッドの数。RocksDB スレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
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

-   Raft RocksDB WAL ファイルが保存されるディレクトリ。これは WAL の絶対ディレクトリ パスです。この構成項目を[`rocksdb.wal-dir`](#wal-dir)と同じ値に設定し**ないでください**。
-   この設定項目が設定されていない場合、ログ ファイルはデータと同じディレクトリに保存されます。
-   マシンに 2 つのディスクがある場合、RocksDB データと WAL ログを別のディスクに保存するとパフォーマンスが向上します。
-   デフォルト値: `""`

### <code>wal-ttl-seconds</code> {#code-wal-ttl-seconds-code}

-   アーカイブされた WAL ファイルを保持する期間を指定します。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: 秒

### <code>wal-size-limit</code> {#code-wal-size-limit-code}

-   アーカイブされた WAL ファイルのサイズ制限。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>max-total-wal-size</code> {#code-max-total-wal-size-code}

-   RocksDB WALの合計最大サイズ
-   デフォルト値:
    -   `storage.engine="raft-kv"`場合、デフォルト値は`"4GiB"`です。
    -   `storage.engine="partitioned-raft-kv"`場合、デフォルト値は`1`です。

### <code>compaction-readahead-size</code> {#code-compaction-readahead-size-code}

-   RocksDB の圧縮中に先読み機能を有効にするかどうかを制御し、先読みデータのサイズを指定します。
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

-   バックグラウンドのフラッシュと圧縮で読み取りと書き込みの両方に`O_DIRECT`使用するかどうかを決定します。このオプションのパフォーマンスへの影響: `O_DIRECT`有効にすると、OS バッファ キャッシュのバイパスと汚染が防止されますが、後続のファイル読み取りでは、バッファ キャッシュへの内容の再読み取りが必要になります。
-   デフォルト値: `false`

### <code>enable-pipelined-write</code> {#code-enable-pipelined-write-code}

-   パイプライン書き込みを有効にするかどうかを制御します。この構成を有効にすると、以前のパイプライン書き込みが使用されます。この構成を無効にすると、新しいパイプラインコミット メカニズムが使用されます。
-   デフォルト値: `true`

### <code>allow-concurrent-memtable-write</code> {#code-allow-concurrent-memtable-write-code}

-   同時メモリテーブル書き込みを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   ファイルが非同期的に書き込まれている間に、OSがファイルをディスクに段階的に同期する速度
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
> v5.4.0 以降、RocksDB ログは TiKV のログ モジュールによって管理されます。そのため、この構成項目は非推奨となり、その機能は構成項目[`log.file.max-size`](#max-size-new-in-v540)に置き換えられました。

-   情報ログの最大サイズ
-   デフォルト値: `"1GiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>info-log-roll-time</code> {#code-info-log-roll-time-code}

> **警告：**
>
> v5.4.0 以降、RocksDB ログは TiKV のログ モジュールによって管理されます。したがって、この構成項目は非推奨です。TiKV は時間に基づく自動ログ分割をサポートしなくなりました。代わりに、構成項目[`log.file.max-size`](#max-size-new-in-v540)使用して、ファイル サイズに基づく自動ログ分割のしきい値を設定できます。

-   情報ログが切り捨てられる間隔。値が`0s`の場合、ログは切り捨てられません。
-   デフォルト値: `"0s"` (ログは切り捨てられません)

### <code>info-log-keep-log-file-num</code> {#code-info-log-keep-log-file-num-code}

> **警告：**
>
> v5.4.0 以降、RocksDB ログは TiKV のログ モジュールによって管理されます。そのため、この構成項目は非推奨となり、その機能は構成項目[`log.file.max-backups`](#max-backups-new-in-v540)に置き換えられました。

-   RaftDB に保存される情報ログファイルの最大数
-   デフォルト値: `10`
-   最小値: `0`

### <code>info-log-dir</code> {#code-info-log-dir-code}

-   情報ログが保存されるディレクトリ
-   デフォルト値: `""`

### <code>info-log-level</code> {#code-info-log-level-code}

> **警告：**
>
> v5.4.0 以降、RocksDB ログは TiKV のログ モジュールによって管理されます。そのため、この構成項目は非推奨となり、その機能は構成項目[`log.level`](#level-new-in-v540)に置き換えられました。

-   RaftDBのログレベル
-   デフォルト値: `"info"`

## いかだエンジン {#raft-engine}

Raft Engineに関連するコンフィグレーション項目。

> **注記：**
>
> -   初めてRaft Engineを有効にすると、 TiKV はデータを RocksDB からRaft Engineに転送します。そのため、 TiKV が起動するまでさらに数十秒待つ必要があります。
> -   TiDB v5.4.0 のRaft Engineのデータ形式は、以前の TiDB バージョンと互換性がありません。したがって、TiDB クラスターを v5.4.0 から以前のバージョンにダウングレードする必要がある場合は、ダウングレードする**前に**、 `enable`を`false`に設定してRaft Engineを無効にし、TiKV を再起動して構成を有効にします。

### <code>enable</code> {#code-enable-code}

-   Raftログを保存するためにRaft Engineを使用するかどうかを決定します。有効にすると、 `raftdb`の設定は無視されます。
-   デフォルト値: `true`

### <code>dir</code> {#code-dir-code}

-   raft ログ ファイルが保存されるディレクトリ。ディレクトリが存在しない場合は、TiKV の起動時に作成されます。
-   この設定項目が設定されていない場合は`{data-dir}/raft-engine`が使用されます。
-   マシンに複数のディスクがある場合は、TiKV のパフォーマンスを向上させるために、 Raft Engineのデータを別のディスクに保存することをお勧めします。
-   デフォルト値: `""`

### <code>batch-compression-threshold</code> {#code-batch-compression-threshold-code}

-   ログ バッチのしきい値サイズを指定します。この構成より大きいログ バッチは圧縮されます。この構成項目を`0`に設定すると、圧縮は無効になります。
-   デフォルト値: `"8KiB"`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   バッファリングされた書き込みの最大累積サイズを指定します。この構成値を超えると、バッファリングされた書き込みはディスクにフラッシュされます。
-   この構成項目を`0`に設定すると、増分同期は無効になります。
-   デフォルト値: `"4MiB"`

### <code>target-file-size</code> {#code-target-file-size-code}

-   ログ ファイルの最大サイズを指定します。ログ ファイルがこの値より大きい場合、ログ ファイルはローテーションされます。
-   デフォルト値: `"128MiB"`

### <code>purge-threshold</code> {#code-purge-threshold-code}

-   メイン ログ キューのしきい値サイズを指定します。この構成値を超えると、メイン ログ キューは消去されます。
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

### <code>format-version</code> <span class="version-mark">v6.3.0 の新</span>機能 {#code-format-version-code-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> `format-version` `2`に設定した後、TiKV クラスターを v6.3.0 から以前のバージョンにダウングレードする必要がある場合は、ダウングレードする**前に**次の手順を実行します。
>
> 1.  [`enable`](/tikv-configuration-file.md#enable-1)を`false`に設定してRaft Engineを無効にし、TiKV を再起動して設定を有効にします。
> 2.  `format-version` `1`に設定します。
> 3.  `enable`から`true`に設定してRaft Engineを有効にし、TiKV を再起動して設定を有効にします。

-   Raft Engineのログ ファイルのバージョンを指定します。
-   値のオプション:
    -   `1` : v6.3.0 より前の TiKV のデフォルトのログ ファイル バージョン。TiKV &gt;= v6.1.0 で読み取ることができます。
    -   `2` : ログのリサイクルをサポートします。TiKV &gt;= v6.3.0 で読み取ることができます。
-   デフォルト値:
    -   `storage.engine="raft-kv"`場合、デフォルト値は`2`です。
    -   `storage.engine="partitioned-raft-kv"`場合、デフォルト値は`5`です。

### <code>enable-log-recycle</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-enable-log-recycle-code-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この構成項目は、 [`format-version`](#format-version-new-in-v630) &gt;= 2 の場合にのみ使用できます。

-   Raft Engineで古いログ ファイルをリサイクルするかどうかを決定します。有効にすると、論理的に消去されたログ ファイルはリサイクル用に予約されます。これにより、書き込みワークロードのロングテールレイテンシーが削減されます。
-   デフォルト値: `true`

### <code>prefill-for-recycle</code> <span class="version-mark">v7.0.0 の新機能</span> {#code-prefill-for-recycle-code-span-class-version-mark-new-in-v7-0-0-span}

> **注記：**
>
> この設定項目は、 [`enable-log-recycle`](#enable-log-recycle-new-in-v630) `true`に設定されている場合にのみ有効になります。

-   Raft Engineでログのリサイクル用に空のログ ファイルを生成するかどうかを決定します。有効にすると、 Raft Engineは初期化中にログのリサイクル用に空のログ ファイルのバッチを自動的に入力し、初期化後すぐにログのリサイクルが有効になります。
-   デフォルト値: `false`

## 安全 {#security}

セキュリティに関するコンフィグレーション項目。

### <code>ca-path</code> {#code-ca-path-code}

-   CAファイルのパス
-   デフォルト値: `""`

### <code>cert-path</code> {#code-cert-path-code}

-   X.509証明書を含むPrivacy Enhanced Mail (PEM)ファイルのパス
-   デフォルト値: `""`

### <code>key-path</code> {#code-key-path-code}

-   X.509キーを含むPEMファイルのパス
-   デフォルト値: `""`

### <code>cert-allowed-cn</code> {#code-cert-allowed-cn-code}

-   クライアントによって提示された証明書内の許容可能な X.509 共通名のリスト。提示された共通名がリスト内のエントリの 1 つと完全に一致する場合にのみ、要求が許可されます。
-   デフォルト値: `[]` 。これは、クライアント証明書の CN チェックがデフォルトで無効になっていることを意味します。

### <code>redact-info-log</code> <span class="version-mark">v4.0.8 の新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v4-0-8-span}

-   この設定項目は、ログ編集を有効または無効にします。設定値が`true`に設定されている場合、ログ内のすべてのユーザー データは`?`に置き換えられます。
-   デフォルト値: `false`

## セキュリティ.暗号化 {#security-encryption}

[保存時の暗号化](/encryption-at-rest.md) （TDE）に関連するコンフィグレーション項目。

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
-   この構成パラメータが有効になっている場合（デフォルト）に互換性の問題が発生するのを回避するには、詳細については[保存時の暗号化- TiKV バージョン間の互換性](/encryption-at-rest.md#compatibility-between-tikv-versions)参照してください。
-   デフォルト値: `true`

### <code>master-key</code> {#code-master-key-code}

-   暗号化が有効になっている場合は、マスター キーを指定します。マスター キーの設定方法については、 [保存時の暗号化- 暗号化の設定](/encryption-at-rest.md#configure-encryption)参照してください。

### <code>previous-master-key</code> {#code-previous-master-key-code}

-   新しいマスターキーをローテーションするときに、古いマスターキーを指定します。設定形式は`master-key`と同じです。マスターキーの設定方法については、 [保存時の暗号化- 暗号化の設定](/encryption-at-rest.md#configure-encryption)参照してください。

## 輸入 {#import}

TiDB Lightning のインポートとBR の復元に関連するコンフィグレーション項目。

### <code>num-threads</code> {#code-num-threads-code}

-   RPCリクエストを処理するスレッドの数
-   デフォルト値: `8`
-   最小値: `1`

### <code>stream-channel-window</code> {#code-stream-channel-window-code}

-   ストリーム チャネルのウィンドウ サイズ。チャネルがいっぱいになると、ストリームはブロックされます。
-   デフォルト値: `128`

### <code>memory-use-ratio</code> <span class="version-mark">v6.5.0 の新</span>機能 {#code-memory-use-ratio-code-span-class-version-mark-new-in-v6-5-0-span}

-   v6.5.0 以降、PITR はメモリ内のバックアップ ログ ファイルに直接アクセスしてデータを復元することをサポートします。この構成項目は、PITR に使用可能なメモリと TiKV の合計メモリの比率を指定します。
-   値の範囲: [0.0, 0.5]
-   デフォルト値: `0.3` 。これは、システムメモリの 30% が PITR に使用できることを意味します。値が`0.0`の場合、PITR はログ ファイルをローカル ディレクトリにダウンロードすることによって実行されます。

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

### <code>enable-compaction-filter</code> <span class="version-mark">v5.0 の新機能</span> {#code-enable-compaction-filter-code-span-class-version-mark-new-in-v5-0-span}

-   圧縮フィルター機能でGCを有効にするかどうかを制御します
-   デフォルト値: `true`

### <code>ratio-threshold</code> {#code-ratio-threshold-code}

-   GC をトリガーするガベージ率のしきい値。
-   デフォルト値: `1.1`

### <code>num-threads</code> <span class="version-mark">v6.5.8、v7.1.4、v7.5.1 の新機能</span> {#code-num-threads-code-span-class-version-mark-new-in-v6-5-8-v7-1-4-and-v7-5-1-span}

-   `enable-compaction-filter`場合の GC スレッド数は`false`です。
-   デフォルト値: `1`

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

-   バックアップ SST ファイル サイズのしきい値。TiKVリージョン内のバックアップ ファイルのサイズがこのしきい値を超えると、TiKVリージョンが複数のリージョン範囲に分割され、ファイルが複数のファイルにバックアップされます。分割されたリージョン内の各ファイルのサイズは`sst-max-size`と同じ (またはわずかに大きい) です。
-   たとえば、リージョン`[a,e)`のバックアップ ファイルのサイズが`sst-max-size`より大きい場合、ファイル`[b,c)` `[a,b)` `[d,e)` `[c,d)` `[c,d)` `[a,b)`サイズと同じ (または`sst-max-size`に大きい`[b,c)`になります。
-   デフォルト値: `"144MiB"`

### <code>enable-auto-tune</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-enable-auto-tune-code-span-class-version-mark-new-in-v5-4-0-span}

-   クラスター リソースの使用率が高い場合に、クラスターへの影響を軽減するために、バックアップ タスクで使用されるリソースを制限するかどうかを制御します。詳細については、 [BRオートチューン](/br/br-auto-tune.md)を参照してください。
-   デフォルト値: `true`

### <code>s3-multi-part-size</code> <span class="version-mark">v5.3.2 の新機能</span> {#code-s3-multi-part-size-code-span-class-version-mark-new-in-v5-3-2-span}

> **注記：**
>
> この設定は、S3 レート制限によって発生するバックアップ障害に対処するために導入されました。この問題は[バックアップデータのstorage構造の改善](/br/br-snapshot-architecture.md#structure-of-backup-files)で修正されました。したがって、この設定は v6.1.1 から非推奨となり、推奨されなくなりました。

-   バックアップ中に S3 へのマルチパートアップロードを実行するときに使用するパートサイズ。この設定の値を調整して、S3 に送信されるリクエストの数を制御できます。
-   S3 にデータをバックアップし、バックアップ ファイルがこの設定項目の値より大きい場合は、 [マルチパートアップロード](https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPart.html)自動的に有効になります。圧縮率に基づくと、96 MiB のリージョンで生成されるバックアップ ファイルは約 10 MiB ～ 30 MiB になります。
-   デフォルト値: 5MiB

## backup.hadoop {#backup-hadoop}

### <code>home</code> {#code-home-code}

-   HDFS シェル コマンドの場所を指定し、TiKV がシェル コマンドを見つけられるようにします。この構成項目は、環境変数`$HADOOP_HOME`と同じ効果があります。
-   デフォルト値: `""`

### <code>linux-user</code> {#code-linux-user-code}

-   TiKV が HDFS シェル コマンドを実行する Linux ユーザーを指定します。
-   この設定項目が設定されていない場合、TiKV は現在の Linux ユーザーを使用します。
-   デフォルト値: `""`

## ログバックアップ {#log-backup}

ログバックアップに関連するコンフィグレーション項目。

### <code>enable</code> <span class="version-mark">v6.2.0 の新</span>機能 {#code-enable-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ バックアップを有効にするかどうかを決定します。
-   デフォルト値: `true`

### <code>file-size-limit</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-file-size-limit-code-span-class-version-mark-new-in-v6-2-0-span}

-   保存されるバックアップ ログ データのサイズ制限。
-   デフォルト値: 256MiB
-   注: 通常、値`file-size-limit`は外部storageに表示されるバックアップ ファイルのサイズよりも大きくなります。これは、バックアップ ファイルが外部storageにアップロードされる前に圧縮されるためです。

### <code>initial-scan-pending-memory-quota</code> <span class="version-mark">v6.2.0 の新</span>機能 {#code-initial-scan-pending-memory-quota-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ バックアップ中に増分スキャン データを保存するために使用されるキャッシュのクォータ。
-   デフォルト値: `min(Total machine memory * 10%, 512 MiB)`

### <code>initial-scan-rate-limit</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-initial-scan-rate-limit-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ バックアップ中の増分データ スキャンのスループットのレート制限。これは、1 秒あたりにディスクから読み取ることができるデータの最大量を意味します。数値のみを指定する場合 (たとえば、 `60` )、単位は KiB ではなくバイトになることに注意してください。
-   デフォルト値: 60MiB

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
> v6.5.0 では、CDCレイテンシーを削減するために、デフォルト値`min-ts-interval`が`"1s"`から`"200ms"`に変更されました。v6.5.1 以降では、ネットワーク トラフィックを削減するために、このデフォルト値が`"1s"`に戻されます。

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
-   デフォルト値: `4` 、つまり 4 つのスレッドを意味します。

### <code>incremental-scan-concurrency</code> {#code-incremental-scan-concurrency-code}

-   履歴データを増分スキャンするタスクの同時実行の最大数。
-   デフォルト値: `6` 。最大 6 つのタスクを同時に実行できることを意味します。
-   注意: `incremental-scan-concurrency`の値は`incremental-scan-threads`の値以上である必要があります。そうでない場合、TiKV は起動時にエラーを報告します。

## resolved-ts {#resolved-ts}

ステイル読み取り要求に対応するために解決された TS を維持することに関連するコンフィグレーション項目。

### <code>enable</code> {#code-enable-code}

-   すべてのリージョンの解決済み TS を維持するかどうかを決定します。
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

-   TiKV 内の悲観的トランザクションが他のトランザクションがロックを解放するのを待機する最長時間。タイムアウトになると、TiDB にエラーが返され、TiDB はロックの追加を再試行します。ロック待機タイムアウトは`innodb_lock_wait_timeout`に設定されます。
-   デフォルト値: `"1s"`
-   最小値: `"1ms"`

### <code>wake-up-delay-duration</code> {#code-wake-up-delay-duration-code}

-   悲観的トランザクションがロックを解除すると、ロックを待機しているすべてのトランザクションのうち、最小の`start_ts`を持つトランザクションのみが起動されます。他のトランザクションは`wake-up-delay-duration`後に起動されます。
-   デフォルト値: `"20ms"`

### <code>pipelined</code> {#code-pipelined-code}

-   この設定項目により、悲観的ロックを追加するパイプライン プロセスが有効になります。この機能を有効にすると、データがロック可能であることを検出すると、TiKV は TiDB に後続の要求を実行して悲観的ロックを非同期に書き込むように直ちに通知します。これにより、レイテンシーがほとんど削減され、悲観悲観的トランザクションのパフォーマンスが大幅に向上します。ただし、悲観的ロックの非同期書き込みが失敗し、悲観的トランザクションのコミットが失敗する可能性は依然として低いままです。
-   デフォルト値: `true`

### <code>in-memory</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-in-memory-code-span-class-version-mark-new-in-v6-0-0-span}

-   メモリ内の悲観的ロック機能を有効にします。この機能を有効にすると、悲観的トランザクションは、ロックをディスクに書き込んだり、他のレプリカにロックを複製したりするのではなく、メモリにロックを保存しようとします。これにより、悲観的トランザクションのパフォーマンスが向上します。ただし、悲観的ロックが失われ、悲観的トランザクションのコミットが失敗する可能性は依然として低いままです。
-   デフォルト値: `true`
-   `in-memory` `pipelined`の値が`true`場合にのみ有効になることに注意してください。

## クォータ {#quota}

クォータリミッターに関連するコンフィグレーション項目。

### <code>max-delay-duration</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-max-delay-duration-code-span-class-version-mark-new-in-v6-0-0-span}

-   単一の読み取りまたは書き込み要求がフォアグラウンドで処理されるまでに強制的に待機する最大時間。
-   デフォルト値: `500ms`
-   推奨設定: ほとんどの場合、デフォルト値を使用することをお勧めします。インスタンスでメモリ不足 (OOM) または激しいパフォーマンスジッターが発生する場合は、値を 1S に設定して、リクエストの待機時間を 1 秒未満にすることができます。

### フォアグラウンドクォータリミッター {#foreground-quota-limiter}

フォアグラウンド クォータ リミッターに関連するコンフィグレーション項目。

TiKV がデプロイされているマシンのリソースが限られているとします (たとえば、CPU が 4v でメモリが 16 G しかない)。この状況では、TiKV のフォアグラウンドで処理される読み取りおよび書き込み要求が多すぎるため、バックグラウンドで使用される CPU リソースがそのような要求の処理に占有され、TiKV のパフォーマンスの安定性に影響する可能性があります。この状況を回避するには、フォアグラウンドのクォータ関連の構成項目を使用して、フォアグラウンドで使用される CPU リソースを制限できます。要求によって Quota Limiter がトリガーされると、その要求は TiKV が CPU リソースを解放するまでしばらく待機する必要があります。正確な待機時間は要求の数によって異なり、最大待機時間は[`max-delay-duration`](#max-delay-duration-new-in-v600)の値以下になります。

#### <code>foreground-cpu-time</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-foreground-cpu-time-code-span-class-version-mark-new-in-v6-0-0-span}

-   読み取りおよび書き込み要求を処理するために TiKV フォアグラウンドで使用される CPU リソースのソフト制限。
-   デフォルト値: `0` (制限なしを意味します)
-   単位: ミリCPU (たとえば、 `1500`フォアグラウンド要求が 1.5V CPU を消費することを意味します)
-   推奨設定: 4 つ以上のコアを持つインスタンスの場合は、デフォルト値`0`を使用します。4 つのコアを持つインスタンスの場合は、値を`1000`から`1500`の範囲に設定するとバランスが取れます。2 つのコアを持つインスタンスの場合は、値を`1200`未満にしてください。

#### <code>foreground-write-bandwidth</code><span class="version-mark">幅 v6.0.0 の新機能</span> {#code-foreground-write-bandwidth-code-span-class-version-mark-new-in-v6-0-0-span}

-   トランザクションがデータを書き込む帯域幅のソフト制限。
-   デフォルト値: `0KiB` (制限なしを意味します)
-   推奨設定: `foreground-cpu-time`設定では書き込み帯域幅を制限するのに十分でない限り、ほとんどの場合はデフォルト値`0`を使用します。このような例外の場合、コア数が 4 以下のインスタンスでは`50MiB`より小さい値を設定することをお勧めします。

#### <code>foreground-read-bandwidth</code><span class="version-mark">幅 v6.0.0 の新機能</span> {#code-foreground-read-bandwidth-code-span-class-version-mark-new-in-v6-0-0-span}

-   トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限。
-   デフォルト値: `0KiB` (制限なしを意味します)
-   推奨設定: `foreground-cpu-time`設定では読み取り帯域幅を制限するのに十分でない限り、ほとんどの場合はデフォルト値`0`を使用します。このような例外の場合、コア数が 4 以下のインスタンスでは`20MiB`より小さい値を設定することをお勧めします。

### バックグラウンドクォータリミッター {#background-quota-limiter}

バックグラウンド クォータ リミッターに関連するコンフィグレーション項目。

TiKV がデプロイされているマシンのリソースが限られているとします。たとえば、CPU が 4v でメモリが16 G しかない場合などです。このような状況では、TiKV のバックグラウンドで処理される計算や読み取り/書き込み要求が多すぎる可能性があります。その結果、フォアグラウンドで使用される CPU リソースがそのような要求の処理に占有され、TiKV のパフォーマンスの安定性に影響を及ぼします。この状況を回避するには、バックグラウンド クォータ関連の構成項目を使用して、バックグラウンドで使用される CPU リソースを制限できます。要求によって Quota Limiter がトリガーされると、その要求は TiKV が CPU リソースを解放するまでしばらく待機する必要があります。正確な待機時間は要求の数によって異なり、最大待機時間は[`max-delay-duration`](#max-delay-duration-new-in-v600)の値以下になります。

> **警告：**
>
> -   バックグラウンド クォータ リミッターは、TiDB v6.2.0 で導入された実験的機能であり、本番環境での使用は推奨され**ません**。
> -   この機能は、リソースが限られている環境にのみ適しており、これらの環境で TiKV が安定して実行されることを保証します。リソースが豊富な環境でこの機能を有効にすると、リクエストの量がピークに達したときにパフォーマンスが低下する可能性があります。

#### <code>background-cpu-time</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-background-cpu-time-code-span-class-version-mark-new-in-v6-2-0-span}

-   TiKV バックグラウンドで読み取りおよび書き込み要求を処理するために使用される CPU リソースのソフト制限。
-   デフォルト値: `0` (制限なしを意味します)
-   単位: ミリCPU (たとえば、 `1500`バックグラウンド リクエストが 1.5V CPU を消費することを意味します)

#### <code>background-write-bandwidth</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-background-write-bandwidth-code-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この設定項目は`SHOW CONFIG`の結果として返されますが、現在設定しても効果はありません。

-   バックグラウンド トランザクションがデータを書き込む帯域幅のソフト制限。
-   デフォルト値: `0KiB` (制限なしを意味します)

#### <code>background-read-bandwidth</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-background-read-bandwidth-code-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この設定項目は`SHOW CONFIG`の結果として返されますが、現在設定しても効果はありません。

-   バックグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限。
-   デフォルト値: `0KiB` (制限なしを意味します)

#### <code>enable-auto-tune</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-enable-auto-tune-code-span-class-version-mark-new-in-v6-2-0-span}

-   クォータの自動調整を有効にするかどうかを決定します。この構成項目を有効にすると、TiKV は TiKV インスタンスの負荷に基づいてバックグラウンド要求のクォータを動的に調整します。
-   デフォルト値: `false` (自動チューニングが無効であることを意味します)

## causal-ts <span class="version-mark">v6.1.0 の新機能</span> {#causal-ts-span-class-version-mark-new-in-v6-1-0-span}

TiKV API V2が有効な場合にタイムスタンプを取得することに関連するコンフィグレーション項目（ `storage.api-version = 2` ）。

書き込みレイテンシーを削減するために、TiKV は定期的にタイムスタンプのバッチをフェッチしてローカルにキャッシュします。キャッシュされたタイムスタンプは、PD への頻繁なアクセスを回避し、短期間の TSO サービス障害を許容するのに役立ちます。

### <code>alloc-ahead-buffer</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-alloc-ahead-buffer-code-span-class-version-mark-new-in-v6-4-0-span}

-   事前に割り当てられた TSO キャッシュ サイズ (期間内)。
-   TiKV がこの構成項目で指定された期間に基づいて TSO キャッシュを事前割り当てすることを示します。TiKV は、前の期間に基づいて TSO の使用量を推定し、 `alloc-ahead-buffer`満たす TSO をローカルに要求してキャッシュします。
-   この設定項目は、TiKV API V2が有効になっている場合にPD障害の許容度を高めるためによく使用されます（ `storage.api-version = 2` ）。
-   この設定項目の値を大きくすると、TSO の消費量と TiKV のメモリオーバーヘッドが増加する可能性があります。十分な TSO を得るには、PD の[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)の設定項目を減らすことをお勧めします。
-   テストによると、デフォルト値が`alloc-ahead-buffer`の場合、PD リーダーが失敗して別のノードに切り替わると、書き込み要求のレイテンシーが短期的に増加し、QPS が減少 (約 15%) します。
-   ビジネスへの影響を回避するには、PD で`tso-update-physical-interval = "1ms"`設定し、TiKV で次の設定項目を設定します。
    -   `causal-ts.alloc-ahead-buffer = "6s"`
    -   `causal-ts.renew-batch-max-size = 65536`
    -   `causal-ts.renew-batch-min-size = 2048`
-   デフォルト値: `3s`

### <code>renew-interval</code> {#code-renew-interval-code}

-   ローカルにキャッシュされたタイムスタンプが更新される間隔。
-   `renew-interval`の間隔で、TiKV はタイムスタンプの一括更新を開始し、前の期間のタイムスタンプの消費と[`alloc-ahead-buffer`](#alloc-ahead-buffer-new-in-v640)の設定に応じて、キャッシュされたタイムスタンプの数を調整します。このパラメータを大きすぎる値に設定すると、最新の TiKV ワークロードの変更が時間内に反映されません。このパラメータを小さすぎる値に設定すると、PD の負荷が増加します。書き込みトラフィックの変動が激しい場合、タイムスタンプが頻繁に使い果たされる場合、および書き込みレイテンシーが増加する場合は、このパラメータを小さい値に設定できます。同時に、PD の負荷も考慮する必要があります。
-   デフォルト値: `"100ms"`

### <code>renew-batch-min-size</code> {#code-renew-batch-min-size-code}

-   タイムスタンプ要求内の TSO の最小数。
-   TiKV は、前の期間のタイムスタンプの消費に応じて、キャッシュされたタイムスタンプの数を調整します。必要な TSO が少数の場合、TiKV は要求される TSO の数を`renew-batch-min-size`達するまで減らします。アプリケーションで大規模なバースト書き込みトラフィックが頻繁に発生する場合は、このパラメータを必要に応じて大きな値に設定できます。このパラメータは、単一の tikv サーバーのキャッシュ サイズであることに注意してください。パラメータを大きすぎる値に設定し、クラスターに多数の tikv サーバーが含まれている場合、TSO の消費が速すぎます。
-   Grafana の**TiKV-RAW** &gt; **Causal timestamp**パネルでは、 **TSO バッチ サイズは、**アプリケーションのワークロードに応じて動的に調整された、ローカルにキャッシュされたタイムスタンプの数です。このメトリックを参照して`renew-batch-min-size`調整できます。
-   デフォルト値: `100`

### <code>renew-batch-max-size</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-renew-batch-max-size-code-span-class-version-mark-new-in-v6-4-0-span}

-   タイムスタンプ要求内の TSO の最大数。
-   デフォルトの TSO 物理時間更新間隔 ( `50ms` ) では、PD は最大 262144 個の TSO を提供します。要求された TSO がこの数を超えると、PD はそれ以上の TSO を提供しません。この構成項目は、TSO の枯渇と、TSO 枯渇による他のビジネスへの逆の影響を回避するために使用されます。この構成項目の値を増やして高可用性を向上させる場合は、十分な TSO を得るために、同時に[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)の値を減らす必要があります。
-   デフォルト値: `8192`

## リソース制御 {#resource-control}

TiKVstorageレイヤーのリソース制御に関連するコンフィグレーション項目。

### <code>enabled</code> <span class="version-mark">v6.6.0 の新</span>機能 {#code-enabled-code-span-class-version-mark-new-in-v6-6-0-span}

-   対応するリソース グループの[リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru)に従って、ユーザーのフォアグラウンド読み取り/書き込み要求のスケジュールを有効にするかどうかを制御します。TiDB リソース グループとリソース制御の詳細については、 [TiDB リソース制御](/tidb-resource-control.md)参照してください。
-   この構成項目を有効にすると、TiDB で[`tidb_enable_resource_control](/system-variables.md#tidb_enable_resource_control-new-in-v660)有効になっている場合にのみ機能します。この構成項目を有効にすると、TiKV は優先キューを使用して、フォアグラウンド ユーザーからのキューに入れられた読み取り/書き込み要求をスケジュールします。要求のスケジュール優先度は、この要求を受信するリソース グループによってすでに消費されているリソースの量に反比例し、対応するリソース グループのクォータに正比例します。
-   デフォルト値: `true` 。これは、リソース グループの RU に基づくスケジュールが有効であることを意味します。

## スプリット {#split}

[ロードベーススプリット](/configure-load-base-split.md)に関連するコンフィグレーション項目です。

### <code>byte-threshold</code> <span class="version-mark">v5.0 の新機能</span> {#code-byte-threshold-code-span-class-version-mark-new-in-v5-0-span}

-   リージョンがホットスポットとして識別されるトラフィックしきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size)が 4 GiB 未満の場合、1 秒あたり`30MiB` 。
    -   [`region-split-size`](#region-split-size)が 4 GiB 以上の場合は 1 秒あたり`100MiB` 。

### <code>qps-threshold</code> {#code-qps-threshold-code}

-   リージョンがホットスポットとして識別される QPS しきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size) 4 GiB 未満の場合は`3000`です。
    -   [`region-split-size`](#region-split-size)が 4 GiB 以上の場合は`7000` 。

### <code>region-cpu-overload-threshold-ratio</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-region-cpu-overload-threshold-ratio-code-span-class-version-mark-new-in-v6-2-0-span}

-   リージョンがホットスポットとして識別される CPU 使用率のしきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size) 4 GiB 未満の場合は`0.25`です。
    -   [`region-split-size`](#region-split-size)が 4 GiB 以上の場合は`0.75` 。

## メモリ<span class="version-mark">v7.5.0 の新機能</span> {#memory-span-class-version-mark-new-in-v7-5-0-span}

### <code>enable-heap-profiling</code> <span class="version-mark">v7.5.0 の新</span>機能 {#code-enable-heap-profiling-code-span-class-version-mark-new-in-v7-5-0-span}

-   TiKV のメモリ使用量を追跡するためにヒープ プロファイリングを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>profiling-sample-per-bytes</code> <span class="version-mark">v7.5.0 の新機能</span> {#code-profiling-sample-per-bytes-code-span-class-version-mark-new-in-v7-5-0-span}

-   ヒープ プロファイリングによって毎回サンプリングされるデータの量を、最も近い 2 の累乗に切り上げて指定します。
-   デフォルト値: `512KiB`
