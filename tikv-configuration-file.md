---
title: TiKV Configuration File
summary: Learn the TiKV configuration file.
---

# TiKVConfiguration / コンフィグレーションファイル {#tikv-configuration-file}

<!-- markdownlint-disable MD001 -->

TiKV構成ファイルは、コマンドラインパラメーターよりも多くのオプションをサポートしています。デフォルトの構成ファイルは[etc / config-template.toml](https://github.com/tikv/tikv/blob/master/etc/config-template.toml)にあり、名前を`config.toml`に変更できます。

このドキュメントでは、コマンドラインパラメータに含まれていないパラメータについてのみ説明します。詳細については、 [コマンドラインパラメータ](/command-line-flags-for-tikv-configuration.md)を参照してください。

## グローバル構成 {#global-configuration}

### <code>abort-on-panic</code> {#code-abort-on-panic-code}

-   TiKVがパニックになったときに`abort()`を呼び出してプロセスを終了するかどうかを設定します。このオプションは、TiKVがシステムにコアダンプファイルの生成を許可するかどうかに影響します。

    -   この構成アイテムの値が`false`の場合、TiKVがパニックになると、 `exit()`を呼び出してプロセスを終了します。
    -   この構成アイテムの値が`true`の場合、TiKVがパニックになると、TiKVは`abort()`を呼び出してプロセスを終了します。このとき、TiKVを使用すると、システムは終了時にコアダンプファイルを生成できます。コアダンプファイルを生成するには、コアダンプに関連するシステム構成も実行する必要があります（たとえば、 `ulimit -c`コマンドでコアダンプファイルのサイズ制限を設定し、コアダンプパスを構成します。オペレーティングシステムが異なれば、関連する構成も異なります。 ）。コアダンプファイルがディスク領域を占有しすぎてTiKVディスク領域が不足するのを防ぐために、コアダンプ生成パスをTiKVデータとは異なるディスクパーティションに設定することをお勧めします。

-   デフォルト値： `false`

### <code>slow-log-file</code> {#code-slow-log-file-code}

-   遅いログを保存するファイル
-   この設定項目が設定されていないが`log.file.filename`が設定されている場合、 `log.file.filename`で指定されたログファイルに低速ログが出力されます。
-   `slow-log-file`も`log.file.filename`も設定されていない場合、デフォルトではすべてのログが「stderr」に出力されます。
-   両方の設定項目が設定されている場合、通常のログは`log.file.filename`で指定されたログファイルに出力され、遅いログは`slow-log-file`で設定されたログファイルに出力されます。
-   デフォルト値： `""`

### <code>slow-log-threshold</code> {#code-slow-log-threshold-code}

-   遅いログを出力するためのしきい値。処理時間がこのしきい値より長い場合、遅いログが出力されます。
-   デフォルト値： `"1s"`

## ログ<span class="version-mark">v5.4.0の新規</span> {#log-span-class-version-mark-new-in-v5-4-0-span}

-   ログに関連するConfiguration / コンフィグレーション項目。

-   v5.4.0以降、 `log-rotation-size`とTiDBのログ構成項目の一貫性を保つために、 `log-file`は以前の構成項目`log-rotation-timespan`を廃止し、 `log-level`を次の構成項目に変更し`log-format` 。古い構成アイテムのみを設定し、それらの値がデフォルト以外の値に設定されている場合、古いアイテムは新しいアイテムとの互換性を維持します。古い構成アイテムと新しい構成アイテムの両方が設定されている場合、新しいアイテムが有効になります。

### <code>level</code> <span class="version-mark">v5.4.0の新機能</span> {#code-level-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログレベル
-   `"error"` `"fatal"` `"info"` `"warn"` `"debug"`
-   デフォルト値： `"info"`

### <code>format</code> <span class="version-mark">v5.4.0の新機能</span> {#code-format-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログ形式
-   オプションの`"text"` ： `"json"`
-   デフォルト値： `"text"`

### <code>enable-timestamp</code><span class="version-mark">の新機能</span> {#code-enable-timestamp-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログのタイムスタンプを有効にするか無効にするかを決定します
-   オプションの`false` ： `true`
-   デフォルト値： `true`

## log.filev5.4.0<span class="version-mark">の新機能</span> {#log-file-span-class-version-mark-new-in-v5-4-0-span}

-   ログファイルに関連するConfiguration / コンフィグレーション項目。

### <code>filename</code> <span class="version-mark">v5.4.0の新機能</span> {#code-filename-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログファイル。この構成項目が設定されていない場合、ログはデフォルトで「stderr」に出力されます。この設定項目を設定すると、対応するファイルにログが出力されます。
-   デフォルト値： `""`

### <code>max-size</code> <span class="version-mark">sizev5.4.0の新機能</span> {#code-max-size-code-span-class-version-mark-new-in-v5-4-0-span}

-   単一のログファイルの最大サイズ。ファイルサイズがこの設定項目で設定された値よりも大きい場合、システムは1つのファイルを複数のファイルに自動的に分割します。
-   デフォルト値： `300`
-   最大値： `4096`
-   ユニット：MiB

### <code>max-days</code> <span class="version-mark">daysv5.4.0の新機能</span> {#code-max-days-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKVがログファイルを保持する最大日数。
    -   構成アイテムが設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKVはログファイルをクリーンアップしません。
    -   パラメータが`0`以外の値に設定されている場合、TiKVは`max-days`秒後に期限切れのログファイルをクリーンアップします。
-   デフォルト値： `0`

### <code>max-backups</code> <span class="version-mark">backupsv5.4.0の新機能</span> {#code-max-backups-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKVが保持するログファイルの最大数。
    -   構成アイテムが設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKVはすべてのログファイルを保持します。
    -   構成項目が`0`以外の値に設定されている場合、TiKVは最大で`max-backups`で指定された古いログファイルの数を保持します。たとえば、値が`7`に設定されている場合、TiKVは最大7つの古いログファイルを保持します。
-   デフォルト値： `0`

## サーバ {#server}

-   サーバーに関連するConfiguration / コンフィグレーション項目。

### <code>status-thread-pool-size</code> {#code-status-thread-pool-size-code}

-   `HTTP`のAPIサービスのワーカースレッドの数
-   デフォルト値： `1`
-   最小値： `1`

### <code>grpc-compression-type</code> {#code-grpc-compression-type-code}

-   gRPCメッセージの圧縮アルゴリズム
-   オプションの`"deflate"` `"gzip"` `"none"`
-   デフォルト値： `"none"`
-   注：値が`gzip`の場合、TiDBダッシュボードは、場合によっては対応する圧縮アルゴリズムを完了しない可能性があるため、表示エラーが発生します。値をデフォルトの`none`に戻すと、TiDBダッシュボードが正常に表示されます。

### <code>grpc-concurrency</code> {#code-grpc-concurrency-code}

-   gRPCワーカースレッドの数。 gRPCスレッドプールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値： `5`
-   最小値： `1`

### <code>grpc-concurrent-stream</code> {#code-grpc-concurrent-stream-code}

-   gRPCストリームで許可される同時リクエストの最大数
-   デフォルト値： `1024`
-   最小値： `1`

### <code>grpc-memory-pool-quota</code> {#code-grpc-memory-pool-quota-code}

-   gRPCで使用できるメモリサイズを制限します
-   デフォルト値：制限なし
-   OOMが観察される場合に備えて、メモリを制限します。使用を制限すると、ストールが発生する可能性があることに注意してください

### <code>grpc-raft-conn-num</code> {#code-grpc-raft-conn-num-code}

-   Raft通信用のTiKVノード間のリンクの最大数
-   デフォルト値： `1`
-   最小値： `1`

### <code>max-grpc-send-msg-len</code> {#code-max-grpc-send-msg-len-code}

-   送信できるgRPCメッセージの最大長を設定します
-   デフォルト値： `10485760`
-   単位：バイト
-   最大値： `2147483647`

### <code>grpc-stream-initial-window-size</code> {#code-grpc-stream-initial-window-size-code}

-   gRPCストリームのウィンドウサイズ
-   デフォルト値： `2MB`
-   単位：KB | MB | GB
-   最小値： `"1KB"`

### <code>grpc-keepalive-time</code> {#code-grpc-keepalive-time-code}

-   そのgRPCが`keepalive`のPingメッセージを送信する時間間隔
-   デフォルト値： `"10s"`
-   最小値： `"1s"`

### <code>grpc-keepalive-timeout</code> {#code-grpc-keepalive-timeout-code}

-   gRPCストリームのタイムアウトを無効にします
-   デフォルト値： `"3s"`
-   最小値： `"1s"`

### <code>concurrent-send-snap-limit</code> {#code-concurrent-send-snap-limit-code}

-   同時に送信されるスナップショットの最大数
-   デフォルト値： `32`
-   最小値： `1`

### <code>concurrent-recv-snap-limit</code> {#code-concurrent-recv-snap-limit-code}

-   同時に受信するスナップショットの最大数
-   デフォルト値： `32`
-   最小値： `1`

### <code>end-point-recursion-limit</code> {#code-end-point-recursion-limit-code}

-   TiKVがコプロセッサーDAG式をデコードするときに許可される再帰レベルの最大数
-   デフォルト値： `1000`
-   最小値： `1`

### <code>end-point-request-max-handle-duration</code> {#code-end-point-request-max-handle-duration-code}

-   タスクを処理するためのTiDBのTiKVへのプッシュダウン要求に許可される最長の期間
-   デフォルト値： `"60s"`
-   最小値： `"1s"`

### <code>snap-max-write-bytes-per-sec</code> {#code-snap-max-write-bytes-per-sec-code}

-   スナップショットを処理するときの最大許容ディスク帯域幅
-   デフォルト値： `"100MB"`
-   単位：KB | MB | GB
-   最小値： `"1KB"`

### <code>end-point-slow-log-threshold</code> {#code-end-point-slow-log-threshold-code}

-   低速ログを出力するためのTiDBのプッシュダウン要求の時間しきい値。処理時間がこのしきい値より長い場合、遅いログが出力されます。
-   デフォルト値： `"1s"`
-   最小値： `0`

### <code>raft-client-queue-size</code> {#code-raft-client-queue-size-code}

-   TiKVのラフトメッセージのキューサイズを指定します。時間内に送信されないメッセージが多すぎるとバッファがいっぱいになるか、メッセージが破棄される場合は、システムの安定性を向上させるために、より大きな値を指定できます。
-   デフォルト値： `8192`

## readpool.unified {#readpool-unified}

読み取り要求を処理するシングルスレッドプールに関連するConfiguration / コンフィグレーションアイテム。このスレッドプールは、4.0バージョン以降、元のストレージスレッドプールおよびコプロセッサースレッドプールに取って代わります。

### <code>min-thread-count</code> {#code-min-thread-count-code}

-   統合読み取りプールの最小作業スレッド数
-   デフォルト値： `1`

### <code>max-thread-count</code> {#code-max-thread-count-code}

-   統合読み取りプールまたはUnifyReadPoolスレッドプールの最大作業スレッド数。このスレッドプールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   値の範囲： `[min-thread-count, MAX(4, CPU)]` 。 `MAX(4, CPU)`では、 `CPU`はCPUコアの数を意味します。 `MAX(4, CPU)`は、 `4`と`CPU`から大きい方の値を取ります。
-   デフォルト値：MAX（4、CPU * 0.8）

### <code>stack-size</code> {#code-stack-size-code}

-   統合スレッドプール内のスレッドのスタックサイズ
-   タイプ：整数+単位
-   デフォルト値： `"10MB"`
-   単位：KB | MB | GB
-   最小値： `"2MB"`
-   最大値：システムで実行された`ulimit -sH`のコマンドの結果で出力されたキロバイト数。

### <code>max-tasks-per-worker</code> {#code-max-tasks-per-worker-code}

-   統合読み取りプール内の単一スレッドに許可されるタスクの最大数。値を超えると`Server Is Busy`が返されます。
-   デフォルト値： `2000`
-   最小値： `2`

## readpool.storage {#readpool-storage}

ストレージスレッドプールに関連するConfiguration / コンフィグレーションアイテム。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   ストレージ要求に統合スレッドプール（ [`readpool.unified`](#readpoolunified)で構成）を使用するかどうかを決定します。このパラメーターの値が`false`の場合、別のスレッドプールが使用されます。これは、このセクションの残りのパラメーターを介して構成されます（ `readpool.storage` ）。
-   デフォルト値：このセクション（ `readpool.storage` ）に他の構成がない場合、デフォルト値は`true`です。それ以外の場合、下位互換性のために、デフォルト値は`false`です。このオプションを有効にする前に、必要に応じて[`readpool.unified`](#readpoolunified)の構成を変更してください。

### <code>high-concurrency</code> {#code-high-concurrency-code}

-   優先度の高い`read`リクエストを処理する同時スレッドの許容数
-   `8`の場合、デフォルト`cpu num`は`16` `cpu_num * 0.5` 。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値： `1`

### <code>normal-concurrency</code> {#code-normal-concurrency-code}

-   通常優先度`read`の要求を処理する同時スレッドの許容数
-   `8`の場合、デフォルト`cpu num`は`16` `cpu_num * 0.5` 。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値： `1`

### <code>low-concurrency</code> {#code-low-concurrency-code}

-   優先度の低い`read`リクエストを処理する同時スレッドの許容数
-   `8`の場合、デフォルト`cpu num`は`16` `cpu_num * 0.5` 。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値： `1`

### <code>max-tasks-per-worker-high</code> {#code-max-tasks-per-worker-high-code}

-   優先度の高いスレッドプールで1つのスレッドに許可されるタスクの最大数。値を超えると`Server Is Busy`が返されます。
-   デフォルト値： `2000`
-   最小値： `2`

### <code>max-tasks-per-worker-normal</code> {#code-max-tasks-per-worker-normal-code}

-   通常の優先順位のスレッドプールで単一のスレッドに許可されるタスクの最大数。値を超えると`Server Is Busy`が返されます。
-   デフォルト値： `2000`
-   最小値： `2`

### <code>max-tasks-per-worker-low</code> {#code-max-tasks-per-worker-low-code}

-   優先度の低いスレッドプールで単一のスレッドに許可されるタスクの最大数。値を超えると`Server Is Busy`が返されます。
-   デフォルト値： `2000`
-   最小値： `2`

### <code>stack-size</code> {#code-stack-size-code}

-   ストレージ読み取りスレッドプール内のスレッドのスタックサイズ
-   タイプ：整数+単位
-   デフォルト値： `"10MB"`
-   単位：KB | MB | GB
-   最小値： `"2MB"`
-   最大値：システムで実行された`ulimit -sH`のコマンドの結果で出力されたキロバイト数。

## <code>readpool.coprocessor</code> {#code-readpool-coprocessor-code}

コプロセッサースレッドプールに関連するConfiguration / コンフィグレーション項目。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   コプロセッサー要求に統合スレッドプール（ [`readpool.unified`](#readpoolunified)で構成）を使用するかどうかを決定します。このパラメーターの値が`false`の場合、別のスレッドプールが使用されます。これは、このセクションの残りのパラメーターを介して構成されます（ `readpool.coprocessor` ）。
-   デフォルト値：このセクション（ `readpool.coprocessor` ）のパラメーターがいずれも設定されていない場合、デフォルト値は`true`です。それ以外の場合、下位互換性のためにデフォルト値は`false`です。このパラメーターを有効にする前に、 [`readpool.unified`](#readpoolunified)の構成項目を調整してください。

### <code>high-concurrency</code> {#code-high-concurrency-code}

-   チェックポイントなどの優先度の高いコプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値： `CPU * 0.8`
-   最小値： `1`

### <code>normal-concurrency</code> {#code-normal-concurrency-code}

-   通常優先のコプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値： `CPU * 0.8`
-   最小値： `1`

### <code>low-concurrency</code> {#code-low-concurrency-code}

-   テーブルスキャンなどの優先度の低いコプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値： `CPU * 0.8`
-   最小値： `1`

### <code>max-tasks-per-worker-high</code> {#code-max-tasks-per-worker-high-code}

-   優先度の高いスレッドプールで1つのスレッドに許可されるタスクの数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値： `2000`
-   最小値： `2`

### <code>max-tasks-per-worker-normal</code> {#code-max-tasks-per-worker-normal-code}

-   通常の優先順位のスレッドプールで単一のスレッドに許可されるタスクの数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値： `2000`
-   最小値： `2`

### <code>max-tasks-per-worker-low</code> {#code-max-tasks-per-worker-low-code}

-   優先度の低いスレッドプールで単一のスレッドに許可されるタスクの数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値： `2000`
-   最小値： `2`

### <code>stack-size</code> {#code-stack-size-code}

-   コプロセッサースレッドプール内のスレッドのスタックサイズ
-   タイプ：整数+単位
-   デフォルト値： `"10MB"`
-   単位：KB | MB | GB
-   最小値： `"2MB"`
-   最大値：システムで実行された`ulimit -sH`のコマンドの結果で出力されたキロバイト数。

## 保管所 {#storage}

ストレージに関連するConfiguration / コンフィグレーションアイテム。

### <code>scheduler-concurrency</code> {#code-scheduler-concurrency-code}

-   キーの同時操作を防ぐための組み込みのメモリロックメカニズム。各キーには、異なるスロットにハッシュがあります。
-   デフォルト値： `524288`
-   最小値： `1`

### <code>scheduler-worker-pool-size</code> {#code-scheduler-worker-pool-size-code}

-   スケジューラスレッドプール内のスレッドの数。スケジューラスレッドは主に、データを書き込む前にトランザクションの整合性をチェックするために使用されます。 CPUコアの数が`16`以上の場合、デフォルト値は`8`です。それ以外の場合、デフォルト値は`4`です。スケジューラスレッドプールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値： `4`
-   値の範囲： `[1, MAX(4, CPU)]` 。 `MAX(4, CPU)`では、 `CPU`はCPUコアの数を意味します。 `MAX(4, CPU)`は、 `4`と`CPU`から大きい方の値を取ります。

### <code>scheduler-pending-write-threshold</code> {#code-scheduler-pending-write-threshold-code}

-   書き込みキューの最大サイズ。この値を超えると、TiKVへの新しい書き込みに対して`Server Is Busy`エラーが返されます。
-   デフォルト値： `"100MB"`
-   単位：MB | GB

### <code>reserve-space</code> {#code-reserve-space-code}

-   TiKVを起動すると、ディスク保護としてディスク上にいくらかのスペースが予約されます。残りのディスク容量が予約容量より少ない場合、TiKVは一部の書き込み操作を制限します。予約スペースは2つの部分に分けられます。予約スペースの80％は、ディスクスペースが不足している場合の操作に必要な追加のディスクスペースとして使用され、残りの20％は一時ファイルの保存に使用されます。スペースを再利用するプロセスで、余分なディスクスペースを使いすぎてストレージが使い果たされた場合、この一時ファイルはサービスを復元するための最後の保護として機能します。
-   一時ファイルの名前は`space_placeholder_file`で、 `storage.data-dir`ディレクトリにあります。ディスク容量が不足したためにTiKVがオフラインになった場合、TiKVを再起動すると、一時ファイルが自動的に削除され、TiKVは領域を再利用しようとします。
-   残りのスペースが不足している場合、TiKVは一時ファイルを作成しません。保護の効果は、予約されたスペースのサイズに関連しています。予約済みスペースのサイズは、ディスク容量の5％とこの構成値の間の大きい方の値です。この構成アイテムの値が`"0MB"`の場合、TiKVはこのディスク保護機能を無効にします。
-   デフォルト値： `"5GB"`
-   団結：MB | GB

### <code>enable-ttl</code> {#code-enable-ttl-code}

> **警告：**
>
> -   新しいTiKVクラスタを展開する場合に**のみ**`enable-ttl`を`true`または`false`に設定します。既存のTiKVクラスタでこの構成アイテムの値を変更し<strong>ない</strong>でください。 `enable-ttl`個の値が異なるTiKVクラスターは、異なるデータ形式を使用します。したがって、既存のTiKVクラスタでこのアイテムの値を変更すると、クラスタはさまざまな形式でデータを保存します。これにより、TiKVクラスタを再起動したときに「非ttlでTTLを有効にできません」というエラーが発生します。
> -   `enable-ttl`はTiKVクラスタで**のみ**使用してください。 <strong>TiDB</strong>ノードがあるクラスタではこの構成項目を使用しないでください（このようなクラスターでは`enable-ttl`から`true`に設定することを意味します）。そうしないと、データの破損やTiDBクラスターのアップグレードの失敗などの重大な問題が発生します。

-   TTLは「Timetolive」の略です。この項目が有効になっている場合、TiKVはTTLに到達したデータを自動的に削除します。 TTLの値を設定するには、クライアントを介してデータを書き込むときに、リクエストでTTLの値を指定する必要があります。 TTLが指定されていない場合は、TiKVが対応するデータを自動的に削除しないことを意味します。
-   デフォルト値： `false`

### <code>ttl-check-poll-interval</code> {#code-ttl-check-poll-interval-code}

-   物理スペースを再利用するためにデータをチェックする間隔。データがTTLに達すると、TiKVはチェック中に物理スペースを強制的に再利用します。
-   デフォルト値： `"12h"`
-   最小値： `"0s"`

### <code>background-error-recovery-window</code> <span class="version-mark">windowv6.1.0の新機能</span> {#code-background-error-recovery-window-code-span-class-version-mark-new-in-v6-1-0-span}

-   RocksDBが回復可能なバックグラウンドエラーを検出した後、TiKVが回復するための最大許容時間。一部のバックグラウンドSSTファイルが破損している場合、RocksDBは、破損したSSTファイルが属するピアを見つけた後、ハートビートを介してPDに報告します。次に、PDはスケジューリング操作を実行してこのピアを削除します。最後に、破損したSSTファイルが直接削除され、TiKVバックグラウンドが再び通常どおりに機能します。
-   破損したSSTファイルは、リカバリが完了する前にまだ存在しています。このような期間中、RocksDBはデータの書き込みを続行できますが、データの破損した部分が読み取られるとエラーが報告されます。
-   この時間枠内にリカバリが完了しない場合、TiKVはパニックになります。
-   デフォルト値：1h

### <code>api-version</code> <span class="version-mark">versionv6.1.0の新機能</span> {#code-api-version-code-span-class-version-mark-new-in-v6-1-0-span}

-   TiKVが生のKey-Valueストアとして機能するときにTiKVによって使用されるストレージ形式とインターフェイスバージョン。
-   値のオプション：
    -   `1` ：API V1を使用し、クライアントから渡されたデータをエンコードせず、そのままデータを保存します。 v6.1.0より前のバージョンでは、TiKVはデフォルトでAPIV1を使用します。
    -   `2` ：API V2を使用します：
        -   データはMVCC（Multi-Version Concurrency Control）形式で保存され、タイムスタンプはtikv-serverによってPD（TSO）から取得されます。
        -   API V2を使用する場合は、同時に`storage.enable-ttl = true`を設定する必要があります。 API V2はTTL機能をサポートしているため、 `enable-ttl`を明示的にオンにする必要があります。そうしないと、 `storage.enable-ttl`がデフォルトで`false`になるため、競合が発生します。
        -   API V2が有効になっている場合、期限切れのデータを再利用するには、少なくとも1つのtidb-serverインスタンスをデプロイする必要があります。このtidb-serverインスタンスは、読み取りまたは書き込みサービスを提供できないことに注意してください。高可用性を確保するために、複数のtidb-serverインスタンスをデプロイできます。
        -   APIV2にはクライアントサポートが必要です。詳細については、APIV2のクライアントの対応する命令を参照してください。
-   デフォルト値： `1`

> **警告：**

> -   TiKVAPIV2はまだ実験的機能です。実稼働環境での使用はお勧めしません。
> -   新しいTiKVクラスタをデプロイする**場合にのみ**、 `api-version`から`2`の値を設定できます。既存のTiKVクラスタでこの構成アイテムの値を変更<strong>しないでください</strong>。 `api-version`の値が異なるTiKVクラスターは、異なるデータ形式を使用します。したがって、既存のTiKVクラスタでこのアイテムの値を変更すると、クラスタはさまざまな形式でデータを保存し、データの破損を引き起こします。 TiKVクラスタを起動すると、「storage.api_versionを切り替えることができません」というエラーが発生します。
> -   API V2を有効にした後は、TiKVクラスタをv6.1.0より前のバージョンにダウングレードする**ことはできません**。そうしないと、データが破損する可能性があります。

## storage.block-cache {#storage-block-cache}

複数のRocksDB列ファミリー（CF）間でのブロックキャッシュの共有に関連するConfiguration / コンフィグレーションアイテム。これらの構成アイテムを有効にすると、列ファミリーごとに個別に構成されたブロックキャッシュが無効になります。

### <code>shared</code> {#code-shared-code}

-   ブロックキャッシュの共有を有効または無効にします。
-   デフォルト値： `true`

### <code>capacity</code> {#code-capacity-code}

-   共有ブロックキャッシュのサイズ。
-   デフォルト値：システムメモリ全体のサイズの45％
-   単位：KB | MB | GB

## storage.flow-control {#storage-flow-control}

TiKVのフロー制御メカニズムに関連するConfiguration / コンフィグレーション項目。このメカニズムは、RocksDBの書き込みストールメカニズムに置き換わるものであり、スケジューラーレイヤーでフローを制御します。これにより、RaftstoreスレッドまたはApplyスレッドのスタックによって引き起こされる二次的な災害を回避できます。

### <code>enable</code> {#code-enable-code}

-   フロー制御メカニズムを有効にするかどうかを決定します。有効にすると、TiKVはKvDBの書き込みストールメカニズムとRaftDBの書き込みストールメカニズム（memtableを除く）を自動的に無効にします。
-   デフォルト値： `true`

### <code>memtables-threshold</code> {#code-memtables-threshold-code}

-   kvDB memtableの数がこのしきい値に達すると、フロー制御メカニズムが機能し始めます。 `enable`が`true`に設定されている場合、この構成アイテムは`rocksdb.(defaultcf|writecf|lockcf).max-write-buffer-number`をオーバーライドします。
-   デフォルト値： `5`

### <code>l0-files-threshold</code> {#code-l0-files-threshold-code}

-   kvDB L0ファイルの数がこのしきい値に達すると、フロー制御メカニズムが機能し始めます。 `enable`が`true`に設定されている場合、この構成アイテムは`rocksdb.(defaultcf|writecf|lockcf).level0-slowdown-writes-trigger`をオーバーライドします。
-   デフォルト値： `20`

### <code>soft-pending-compaction-bytes-limit</code> {#code-soft-pending-compaction-bytes-limit-code}

-   KvDBの保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムは一部の書き込み要求の拒否を開始し、 `ServerIsBusy`エラーを報告します。 `enable`が`true`に設定されている場合、この構成アイテムは`rocksdb.(defaultcf|writecf|lockcf).soft-pending-compaction-bytes-limit`をオーバーライドします。
-   デフォルト値： `"192GB"`

### <code>hard-pending-compaction-bytes-limit</code> {#code-hard-pending-compaction-bytes-limit-code}

-   KvDBの保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し、 `ServerIsBusy`のエラーを報告します。 `enable`が`true`に設定されている場合、この構成アイテムは`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`をオーバーライドします。
-   デフォルト値： `"1024GB"`

## storage.io-rate-limit {#storage-io-rate-limit}

I/Oレートリミッタに関連するConfiguration / コンフィグレーション項目。

### <code>max-bytes-per-sec</code> {#code-max-bytes-per-sec-code}

-   サーバーがディスクに書き込みまたはディスクから読み取ることができる最大I/Oバイト（以下の`mode`つの構成項目によって決定される）を1秒間に制限します。この制限に達すると、TiKVはフォアグラウンド操作よりもバックグラウンド操作のスロットリングを優先します。この構成項目の値は、ディスクの最適なI / O帯域幅、たとえば、クラウドディスクベンダーによって指定された最大I/O帯域幅に設定する必要があります。この構成値がゼロに設定されている場合、ディスクI/O操作は制限されません。
-   デフォルト値： `"0MB"`

### <code>mode</code> {#code-mode-code}

-   どのタイプのI/O操作がカウントされ、 `max-bytes-per-sec`のしきい値未満に制限されるかを決定します。現在、書き込み専用モードのみがサポートされています。
-   オプション値： `"write-only"`
-   デフォルト値： `"write-only"`

## いかだ店 {#raftstore}

Raftstoreに関連するConfiguration / コンフィグレーションアイテム。

### <code>prevote</code> {#code-prevote-code}

-   `prevote`を有効または無効にします。この機能を有効にすると、ネットワークパーティションからの回復後のシステムのジッターを減らすことができます。
-   デフォルト値： `true`

### <code>capacity</code> {#code-capacity-code}

-   データを保存できる最大サイズであるストレージ容量。 `capacity`を指定しない場合、現在のディスクの容量が優先されます。同じ物理ディスクに複数のTiKVインスタンスを展開するには、このパラメーターをTiKV構成に追加します。詳細については、 [ハイブリッド展開の主要なパラメーター](/hybrid-deployment-topology.md#key-parameters)を参照してください。
-   デフォルト値： `0`
-   単位：KB | MB | GB

### <code>raftdb-path</code> {#code-raftdb-path-code}

-   Raftライブラリへのパス（デフォルトでは`storage.data-dir/raft` ）
-   デフォルト値： `""`

### <code>raft-base-tick-interval</code> {#code-raft-base-tick-interval-code}

> **ノート：**
>
> この構成アイテムは、SQLステートメントを介して照会することはできませんが、構成ファイルで構成することはできます。

-   Raftステートマシンが作動する時間間隔
-   デフォルト値： `"1s"`
-   最小値： `0`より大きい

### <code>raft-heartbeat-ticks</code> {#code-raft-heartbeat-ticks-code}

> **ノート：**
>
> この構成アイテムは、SQLステートメントを介して照会することはできませんが、構成ファイルで構成することはできます。

-   ハートビートが送信されたときに渡されたティックの数。これは、ハートビートが`raft-base-tick-interval` * `raft-heartbeat-ticks`の時間間隔で送信されることを意味します。
-   デフォルト値： `2`
-   最小値： `0`より大きい

### <code>raft-election-timeout-ticks</code> {#code-raft-election-timeout-ticks-code}

> **ノート：**
>
> この構成アイテムは、SQLステートメントを介して照会することはできませんが、構成ファイルで構成することはできます。

-   いかだ選挙が開始されたときに渡されたティックの数。これは、Raftグループがリーダーを失った場合、リーダーの選出が`raft-base-tick-interval` * `raft-election-timeout-ticks`の時間間隔のほぼ後に開始されることを意味します。
-   デフォルト値： `10`
-   最小値： `raft-heartbeat-ticks`

### <code>raft-min-election-timeout-ticks</code> {#code-raft-min-election-timeout-ticks-code}

> **ノート：**
>
> この構成アイテムは、SQLステートメントを介して照会することはできませんが、構成ファイルで構成することはできます。

-   ラフト選挙が開始される最小ティック数。数値が`0`の場合、値`raft-election-timeout-ticks`が使用されます。このパラメーターの値は、 `raft-election-timeout-ticks`以上である必要があります。
-   デフォルト値： `0`
-   最小値： `0`

### <code>raft-max-election-timeout-ticks</code> {#code-raft-max-election-timeout-ticks-code}

> **ノート：**
>
> この構成アイテムは、SQLステートメントを介して照会することはできませんが、構成ファイルで構成することはできます。

-   ラフト選挙が開始される最大ティック数。数値が`0`の場合、 `raft-election-timeout-ticks` * `2`の値が使用されます。
-   デフォルト値： `0`
-   最小値： `0`

### <code>raft-max-size-per-msg</code> {#code-raft-max-size-per-msg-code}

> **ノート：**
>
> この構成アイテムは、SQLステートメントを介して照会することはできませんが、構成ファイルで構成することはできます。

-   単一のメッセージパケットのサイズのソフト制限
-   デフォルト値： `"1MB"`
-   最小値： `0`より大きい
-   最大値： `3GB`
-   単位：KB | MB | GB

### <code>raft-max-inflight-msgs</code> {#code-raft-max-inflight-msgs-code}

> **ノート：**
>
> この構成アイテムは、SQLステートメントを介して照会することはできませんが、構成ファイルで構成することはできます。

-   確認するラフトログの数。この数を超えると、Raftステートマシンはログの送信を遅くします。
-   デフォルト値： `256`
-   最小値： `0`より大きい
-   最大値： `16384`

### <code>raft-entry-max-size</code> {#code-raft-entry-max-size-code}

-   単一ログの最大サイズの厳しい制限
-   デフォルト値： `"8MB"`
-   最小値： `0`
-   単位：MB | GB

### <code>raft-log-compact-sync-interval</code><span class="version-mark">の新機能</span> {#code-raft-log-compact-sync-interval-code-span-class-version-mark-new-in-v5-3-span}

-   不要なRaftログを圧縮する時間間隔
-   デフォルト値： `"2s"`
-   最小値： `"0s"`

### <code>raft-log-gc-tick-interval</code> {#code-raft-log-gc-tick-interval-code}

-   Raftログを削除するポーリングタスクがスケジュールされる時間間隔。 `0`は、この機能が無効になっていることを意味します。
-   デフォルト値： `"3s"`
-   最小値： `"0s"`

### <code>raft-log-gc-threshold</code> {#code-raft-log-gc-threshold-code}

-   残りのRaftログの最大許容数のソフト制限
-   デフォルト値： `50`
-   最小値： `1`

### <code>raft-log-gc-count-limit</code> {#code-raft-log-gc-count-limit-code}

-   残りのRaftログの許容数の厳しい制限
-   デフォルト値：3/4リージョンサイズに対応できるログ番号（ログごとに1MBとして計算）
-   最小値： `0`

### <code>raft-log-gc-size-limit</code> {#code-raft-log-gc-size-limit-code}

-   残りのRaftログの許容サイズの厳しい制限
-   デフォルト値：リージョンサイズの3/4
-   最小値： `0`より大きい

### <code>raft-log-reserve-max-ticks</code> <span class="version-mark">ticksv5.3の新機能</span> {#code-raft-log-reserve-max-ticks-code-span-class-version-mark-new-in-v5-3-span}

-   この構成項目で設定されたティック数が経過した後、残りのRaftログの数が`raft-log-gc-threshold`で設定された値に達しない場合でも、TiKVはこれらのログに対してガベージコレクション（GC）を実行します。
-   デフォルト値： `6`
-   最小値： `0`より大きい

### <code>raft-entry-cache-life-time</code> {#code-raft-entry-cache-life-time-code}

-   メモリ内のログキャッシュに許可される最大残り時間。
-   デフォルト値： `"30s"`
-   最小値： `0`

### <code>hibernate-regions</code> {#code-hibernate-regions-code}

-   Hibernateリージョンを有効または無効にします。このオプションを有効にすると、長時間アイドル状態のリージョンが自動的に休止状態に設定されます。これにより、アイドル状態のリージョンのRaftリーダーとフォロワー間のハートビートメッセージによって発生する余分なオーバーヘッドが削減されます。 `peer-stale-state-check-interval`を使用して、休止状態のリージョンのリーダーとフォロワーの間のハートビート間隔を変更できます。
-   デフォルト値：v5.0.2以降のバージョンでは`true` 。 v5.0.2より前のバージョンでは`false`

### <code>split-region-check-tick-interval</code> {#code-split-region-check-tick-interval-code}

-   リージョン分割が必要かどうかを確認する間隔を指定します。 `0`は、この機能が無効になっていることを意味します。
-   デフォルト値： `"10s"`
-   最小値： `0`

### <code>region-split-check-diff</code> {#code-region-split-check-diff-code}

-   リージョン分割前にリージョンデータが超過できる最大値
-   デフォルト値：リージョンサイズの1/16。
-   最小値： `0`

### <code>region-compact-check-interval</code> {#code-region-compact-check-interval-code}

-   RocksDBの圧縮を手動でトリガーする必要があるかどうかを確認する時間間隔。 `0`は、この機能が無効になっていることを意味します。
-   デフォルト値： `"5m"`
-   最小値： `0`

### <code>region-compact-check-step</code> {#code-region-compact-check-step-code}

-   手動圧縮の各ラウンドで一度にチェックされるリージョンの数
-   デフォルト値： `100`
-   最小値： `0`

### <code>region-compact-min-tombstones</code> {#code-region-compact-min-tombstones-code}

-   RocksDBの圧縮をトリガーするために必要なトゥームストーンの数
-   デフォルト値： `10000`
-   最小値： `0`

### <code>region-compact-tombstones-percent</code> {#code-region-compact-tombstones-percent-code}

-   RocksDBの圧縮をトリガーするために必要なトゥームストーンの割合
-   デフォルト値： `30`
-   最小値： `1`
-   最大値： `100`

### <code>pd-heartbeat-tick-interval</code> {#code-pd-heartbeat-tick-interval-code}

-   リージョンのPDへのハートビートがトリガーされる時間間隔。 `0`は、この機能が無効になっていることを意味します。
-   デフォルト値： `"1m"`
-   最小値： `0`

### <code>pd-store-heartbeat-tick-interval</code> {#code-pd-store-heartbeat-tick-interval-code}

-   ストアのPDへのハートビートがトリガーされる時間間隔。 `0`は、この機能が無効になっていることを意味します。
-   デフォルト値： `"10s"`
-   最小値： `0`

### <code>snap-mgr-gc-tick-interval</code> {#code-snap-mgr-gc-tick-interval-code}

-   期限切れのスナップショットファイルのリサイクルがトリガーされる時間間隔。 `0`は、この機能が無効になっていることを意味します。
-   デフォルト値： `"1m"`
-   最小値： `0`

### <code>snap-gc-timeout</code> {#code-snap-gc-timeout-code}

-   スナップショットファイルが保存される最長時間
-   デフォルト値： `"4h"`
-   最小値： `0`

### <code>snap-generator-pool-size</code> <span class="version-mark">sizev5.4.0の新機能</span> {#code-snap-generator-pool-size-code-span-class-version-mark-new-in-v5-4-0-span}

-   `snap-generator`スレッドプールのサイズを設定します。
-   リカバリシナリオでリージョンがTiKVでスナップショットをより高速に生成できるようにするには、対応するワーカーの`snap-generator`スレッドの数を増やす必要があります。この構成アイテムを使用して、 `snap-generator`スレッドプールのサイズを増やすことができます。
-   デフォルト値： `2`
-   最小値： `1`

### <code>lock-cf-compact-interval</code> {#code-lock-cf-compact-interval-code}

-   TiKVがロックカラムファミリの手動圧縮をトリガーする時間間隔
-   デフォルト値： `"256MB"`
-   デフォルト値： `"10m"`
-   最小値： `0`

### <code>lock-cf-compact-bytes-threshold</code> {#code-lock-cf-compact-bytes-threshold-code}

-   TiKVがロックカラムファミリーの手動圧縮をトリガーするサイズ
-   デフォルト値： `"256MB"`
-   最小値： `0`
-   単位：MB

### <code>notify-capacity</code> {#code-notify-capacity-code}

-   リージョンメッセージキューの最長の長さ。
-   デフォルト値： `40960`
-   最小値： `0`

### <code>messages-per-tick</code> {#code-messages-per-tick-code}

-   バッチごとに処理されるメッセージの最大数
-   デフォルト値： `4096`
-   最小値： `0`

### <code>max-peer-down-duration</code> {#code-max-peer-down-duration-code}

-   ピアに許可されている最長の非アクティブ期間。タイムアウトのあるピアは`down`としてマークされ、PDは後でそれを削除しようとします。
-   デフォルト値： `"10m"`
-   最小値：Hibernate Regionが有効になっている場合、最小値は`peer-stale-state-check-interval * 2`です。 Hibernate Regionが無効になっている場合、最小値は`0`です。

### <code>max-leader-missing-duration</code> {#code-max-leader-missing-duration-code}

-   ピアがラフトグループにリーダーがいない状態になるのに許容される最長の期間。この値を超えると、ピアはPDを使用して、ピアが削除されたかどうかを確認します。
-   デフォルト値： `"2h"`
-   最小値： `abnormal-leader-missing-duration`より大きい

### <code>abnormal-leader-missing-duration</code> {#code-abnormal-leader-missing-duration-code}

-   ピアがラフトグループにリーダーがいない状態になるのに許容される最長の期間。この値を超えると、ピアは異常と見なされ、メトリックとログにマークされます。
-   デフォルト値： `"10m"`
-   最小値： `peer-stale-state-check-interval`より大きい

### <code>peer-stale-state-check-interval</code> {#code-peer-stale-state-check-interval-code}

-   ピアがラフトグループにリーダーがない状態にあるかどうかのチェックをトリガーする時間間隔。
-   デフォルト値： `"5m"`
-   最小値： `2 * election-timeout`より大きい

### <code>leader-transfer-max-log-lag</code> {#code-leader-transfer-max-log-lag-code}

-   ラフトリーダーの転送中に転送先に許可される欠落ログの最大数
-   デフォルト値： `128`
-   最小値： `10`

### <code>max-snapshot-file-raw-size</code> <span class="version-mark">sizev6.1.0の新機能</span> {#code-max-snapshot-file-raw-size-code-span-class-version-mark-new-in-v6-1-0-span}

-   スナップショットファイルのサイズがこの構成値を超えると、このファイルは複数のファイルに分割されます。
-   デフォルト値： `100MiB`
-   最小値： `100MiB`

### <code>snap-apply-batch-size</code> {#code-snap-apply-batch-size-code}

-   インポートされたスナップショットファイルがディスクに書き込まれるときに必要なメモリキャッシュサイズ
-   デフォルト値： `"10MB"`
-   最小値： `0`
-   単位：MB

### <code>consistency-check-interval</code> {#code-consistency-check-interval-code}

> **警告：**
>
> クラスタのパフォーマンスに影響を与え、TiDBのガベージコレクションと互換性がないため、本番環境で整合性チェックを有効にすることはお勧めし**ません**。

-   整合性チェックがトリガーされる時間間隔。 `0`は、この機能が無効になっていることを意味します。
-   デフォルト値： `"0s"`
-   最小値： `0`

### <code>raft-store-max-leader-lease</code> {#code-raft-store-max-leader-lease-code}

-   ラフトリーダーの最長の信頼できる期間
-   デフォルト値： `"9s"`
-   最小値： `0`

### <code>merge-max-log-gap</code> {#code-merge-max-log-gap-code}

-   `merge`が実行されたときに許可される欠落ログの最大数
-   デフォルト値： `10`
-   最小値： `raft-log-gc-count-limit`より大きい

### <code>merge-check-tick-interval</code> {#code-merge-check-tick-interval-code}

-   TiKVがリージョンにマージが必要かどうかをチェックする時間間隔
-   デフォルト値： `"2s"`
-   最小値： `0`より大きい

### <code>use-delete-range</code> {#code-use-delete-range-code}

-   `rocksdb delete_range`のインターフェイスからデータを削除するかどうかを決定します
-   デフォルト値： `false`

### <code>cleanup-import-sst-interval</code> {#code-cleanup-import-sst-interval-code}

-   期限切れのSSTファイルがチェックされる時間間隔。 `0`は、この機能が無効になっていることを意味します。
-   デフォルト値： `"10m"`
-   最小値： `0`

### <code>local-read-batch-size</code> {#code-local-read-batch-size-code}

-   1つのバッチで処理される読み取り要求の最大数
-   デフォルト値： `1024`
-   最小値： `0`より大きい

### <code>apply-max-batch-size</code> {#code-apply-max-batch-size-code}

-   ラフトステートマシンは、BatchSystemによってデータ書き込み要求をバッチで処理します。この構成項目は、1つのバッチで要求を処理できるRaftステートマシンの最大数を指定します。
-   デフォルト値： `256`
-   最小値： `0`より大きい
-   最大値： `10240`

### <code>apply-pool-size</code> {#code-apply-pool-size-code}

-   データをディスクにフラッシュするプール内の許容スレッド数。これは、アプライスレッドプールのサイズです。このスレッドプールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値： `2`
-   値の範囲： `[1, CPU * 10]` 。 `CPU`はCPUコアの数を意味します。

### <code>store-max-batch-size</code> {#code-store-max-batch-size-code}

-   ラフトステートマシンは、BatchSystemによってバッチでディスクにログをフラッシュする要求を処理します。この構成項目は、1つのバッチで要求を処理できるRaftステートマシンの最大数を指定します。
-   `hibernate-regions`が有効になっている場合、デフォルト値は`256`です。 `hibernate-regions`が無効になっている場合、デフォルト値は`1024`です。
-   最小値： `0`より大きい
-   最大値： `10240`

### <code>store-pool-size</code> {#code-store-pool-size-code}

-   Raftを処理するプール内のスレッドの許容数。これはRaftstoreスレッドプールのサイズです。このスレッドプールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値： `2`
-   値の範囲： `[1, CPU * 10]` 。 `CPU`はCPUコアの数を意味します。

### <code>store-io-pool-size</code> <span class="version-mark">sizev5.3.0の新機能</span> {#code-store-io-pool-size-code-span-class-version-mark-new-in-v5-3-0-span}

-   Raft I / Oタスクを処理するスレッドの許容数。これは、StoreWriterスレッドプールのサイズです。このスレッドプールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値： `0`
-   最小値： `0`

### <code>future-poll-size</code> {#code-future-poll-size-code}

-   `future`を駆動するスレッドの許容数
-   デフォルト値： `1`
-   最小値： `0`より大きい

### <code>cmd-batch</code> {#code-cmd-batch-code}

-   リクエストのバッチ処理を有効にするかどうかを制御します。有効にすると、書き込みパフォーマンスが大幅に向上します。
-   デフォルト値： `true`

### <code>inspect-interval</code> {#code-inspect-interval-code}

-   一定の間隔で、TiKVはRaftstoreコンポーネントのレイテンシーを検査します。このパラメーターは、検査の間隔を指定します。待ち時間がこの値を超える場合、この検査はタイムアウトとしてマークされます。
-   タイムアウト検査の比率に基づいて、TiKVノードが遅いかどうかを判断します。
-   デフォルト値： `"500ms"`
-   最小値： `"1ms"`

### <code>raft-write-size-limit</code> <span class="version-mark">limitv5.3.0の新機能</span> {#code-raft-write-size-limit-code-span-class-version-mark-new-in-v5-3-0-span}

-   Raftデータがディスクに書き込まれるしきい値を決定します。データサイズがこの構成アイテムの値よりも大きい場合、データはディスクに書き込まれます。 `store-io-pool-size`の値が`0`の場合、この構成項目は有効になりません。
-   デフォルト値： `1MB`
-   最小値： `0`

## コプロセッサー {#coprocessor}

コプロセッサーに関連するConfiguration / コンフィグレーション項目。

### <code>split-region-on-table</code> {#code-split-region-on-table-code}

-   リージョンをテーブルで分割するかどうかを決定します。この機能はTiDBモードでのみ使用することをお勧めします。
-   デフォルト値： `false`

### <code>batch-split-limit</code> {#code-batch-split-limit-code}

-   バッチで分割されたリージョンのしきい値。この値を増やすと、リージョンの分割が高速化されます。
-   デフォルト値： `10`
-   最小値： `1`

### <code>region-max-size</code> {#code-region-max-size-code}

-   リージョンの最大サイズ。値を超えると、リージョンは多数に分割されます。
-   デフォルト値： `region-split-size / 2 * 3`
-   単位：KiB | MiB | GiB

### <code>region-split-size</code> {#code-region-split-size-code}

-   新しく分割されたリージョンのサイズ。この値は推定値です。
-   デフォルト値： `"96MiB"`
-   単位：KiB | MiB | GiB

### <code>region-max-keys</code> {#code-region-max-keys-code}

-   リージョン内のキーの最大許容数。この値を超えると、リージョンは多数に分割されます。
-   デフォルト値： `region-split-keys / 2 * 3`

### <code>region-split-keys</code> {#code-region-split-keys-code}

-   新しく分割されたリージョンのキーの数。この値は推定値です。
-   デフォルト値： `960000`

### <code>enable-region-bucket</code> <span class="version-mark">bucketv6.1.0の新機能</span> {#code-enable-region-bucket-code-span-class-version-mark-new-in-v6-1-0-span}

-   リージョンをバケットと呼ばれる小さな範囲に分割するかどうかを決定します。バケットは、スキャンの同時実行性を向上させるための同時クエリの単位として使用されます。バケットの設計の詳細については、 [動的サイズ領域](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md)を参照してください。
-   デフォルト値：false

> **警告：**
>
> -   `enable-region-bucket`は、TiDBv6.1.0で導入された実験的機能です。実稼働環境で使用することはお勧めしません。
> -   この構成は、 `region-split-size`が`region-bucket-size`の2倍以上の場合にのみ意味があります。それ以外の場合、バケットは実際には生成されません。
> -   `region-split-size`をより大きな値に調整すると、パフォーマンスが低下し、スケジューリングが遅くなるリスクがあります。

### <code>region-bucket-size</code> <span class="version-mark">sizev6.1.0の新機能</span> {#code-region-bucket-size-code-span-class-version-mark-new-in-v6-1-0-span}

-   `enable-region-bucket`が真の場合のバケットのサイズ。
-   デフォルト値： `96MiB`

> **警告：**
>
> `region-bucket-size`は、TiDBv6.1.0で導入された実験的機能です。実稼働環境で使用することはお勧めしません。

## RocksDB {#rocksdb}

RocksDBに関連するConfiguration / コンフィグレーションアイテム

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDBのバックグラウンドスレッドの数。 RocksDBスレッドプールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値：
    -   CPUコアの数が10の場合、デフォルト値は`9`です。
    -   CPUコアの数が8の場合、デフォルト値は`7`です。
    -   CPUコアの数が`N`の場合、デフォルト値は`max(2, min(N - 1, 9))`です。
-   最小値： `2`

### <code>max-background-flushes</code> {#code-max-background-flushes-code}

-   同時バックグラウンドメモリ可能フラッシュジョブの最大数
-   デフォルト値：
    -   CPUコアの数が10の場合、デフォルト値は`3`です。
    -   CPUコアの数が8の場合、デフォルト値は`2`です。
    -   CPUコアの数が`N`の場合、デフォルト値は`[(max-background-jobs + 3) / 4]`です。
-   最小値： `1`

### <code>max-sub-compactions</code> {#code-max-sub-compactions-code}

-   RocksDBで同時に実行されたサブ圧縮操作の数
-   デフォルト値： `3`
-   最小値： `1`

### <code>max-open-files</code> {#code-max-open-files-code}

-   RocksDBが開くことができるファイルの総数
-   デフォルト値： `40960`
-   最小値： `-1`

### <code>max-manifest-file-size</code> {#code-max-manifest-file-size-code}

-   RocksDBマニフェストファイルの最大サイズ
-   デフォルト値： `"128MB"`
-   最小値： `0`
-   単位：B | KB | MB | GB

### <code>create-if-missing</code> {#code-create-if-missing-code}

-   DBスイッチを自動的に作成するかどうかを決定します
-   デフォルト値： `true`

### <code>wal-recovery-mode</code> {#code-wal-recovery-mode-code}

-   WALリカバリモード
-   オプションの値：
    -   `"tolerate-corrupted-tail-records"` ：すべてのログに不完全な末尾データがあるレコードを許容して破棄します
    -   `"absolute-consistency"` ：破損したログが見つかった場合にリカバリを中止します
    -   `"point-in-time"` ：最初の破損したログが検出されるまで、ログを順番に回復します
    -   `"skip-any-corrupted-records"` ：災害後の復旧。データは可能な限り回復され、破損したレコードはスキップされます。
-   デフォルト値： `"point-in-time"`

### <code>wal-dir</code> {#code-wal-dir-code}

-   WALファイルが保存されているディレクトリ
-   デフォルト値： `"/tmp/tikv/store"`

### <code>wal-ttl-seconds</code> {#code-wal-ttl-seconds-code}

-   アーカイブされたWALファイルの存続時間。値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値： `0`
-   最小値： `0`
-   単位：秒

### <code>wal-size-limit</code> {#code-wal-size-limit-code}

-   アーカイブされたWALファイルのサイズ制限。値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値： `0`
-   最小値： `0`
-   単位：B | KB | MB | GB

### <code>enable-statistics</code> {#code-enable-statistics-code}

-   RocksDBの統計を有効にするかどうかを決定します
-   デフォルト値： `true`

### <code>stats-dump-period</code> {#code-stats-dump-period-code}

-   統計がログに出力される間隔。
-   デフォルト値： `10m`

### <code>compaction-readahead-size</code> {#code-compaction-readahead-size-code}

-   RocksDBの圧縮中に先読み機能を有効にし、先読みデータのサイズを指定します。メカニカルディスクを使用している場合は、少なくとも2MBに設定することをお勧めします。
-   デフォルト値： `0`
-   最小値： `0`
-   単位：B | KB | MB | GB

### <code>writable-file-max-buffer-size</code> {#code-writable-file-max-buffer-size-code}

-   WritableFileWriteで使用される最大バッファサイズ
-   デフォルト値： `"1MB"`
-   最小値： `0`
-   単位：B | KB | MB | GB

### <code>use-direct-io-for-flush-and-compaction</code> {#code-use-direct-io-for-flush-and-compaction-code}

-   バックグラウンドフラッシュと圧縮の読み取りと書き込みの両方に`O_DIRECT`を使用するかどうかを決定します。このオプションのパフォーマンスへの影響： `O_DIRECT`のバイパスを有効にして、OSバッファーキャッシュの汚染を防ぎますが、後続のファイル読み取りでは、コンテンツをバッファーキャッシュに再読み取りする必要があります。
-   デフォルト値： `false`

### <code>rate-bytes-per-sec</code> {#code-rate-bytes-per-sec-code}

-   RocksDBの圧縮レートリミッターで許可されている最大レート
-   デフォルト値： `10GB`
-   最小値： `0`
-   単位：B | KB | MB | GB

### <code>rate-limiter-mode</code> {#code-rate-limiter-mode-code}

-   RocksDBの圧縮レートリミッターモード
-   オプションの`"write-only"` `"all-io"` `"read-only"`
-   デフォルト値： `"write-only"`

### <code>rate-limiter-auto-tuned</code> <span class="version-mark">v5.0の新</span>機能 {#code-rate-limiter-auto-tuned-code-span-class-version-mark-new-in-v5-0-span}

-   最近のワークロードに基づいて、RocksDBの圧縮レートリミッターの構成を自動的に最適化するかどうかを決定します。この構成を有効にすると、圧縮保留バイトは通常よりわずかに高くなります。
-   デフォルト値： `true`

### <code>enable-pipelined-write</code> {#code-enable-pipelined-write-code}

-   パイプライン書き込みを有効にするかどうかを制御します。この構成を有効にすると、以前のパイプライン書き込みが使用されます。この構成を無効にすると、新しいパイプラインコミットメカニズムが使用されます。
-   デフォルト値： `false`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   これらのファイルが非同期で書き込まれている間に、OSがファイルをディスクに段階的に同期する速度
-   デフォルト値： `"1MB"`
-   最小値： `0`
-   単位：B | KB | MB | GB

### <code>wal-bytes-per-sync</code> {#code-wal-bytes-per-sync-code}

-   WALファイルの書き込み中にOSがWALファイルをディスクに段階的に同期する速度
-   デフォルト値： `"512KB"`
-   最小値： `0`
-   単位：B | KB | MB | GB

### <code>info-log-max-size</code> {#code-info-log-max-size-code}

-   情報ログの最大サイズ
-   デフォルト値： `"1GB"`
-   最小値： `0`
-   単位：B | KB | MB | GB

### <code>info-log-roll-time</code> {#code-info-log-roll-time-code}

-   情報ログが切り捨てられる時間間隔。値が`0s`の場合、ログは切り捨てられません。
-   デフォルト値： `"0s"`

### <code>info-log-keep-log-file-num</code> {#code-info-log-keep-log-file-num-code}

-   保持されるログファイルの最大数
-   デフォルト値： `10`
-   最小値： `0`

### <code>info-log-dir</code> {#code-info-log-dir-code}

-   ログが保存されるディレクトリ
-   デフォルト値： `""`

## rocksdb.titan {#rocksdb-titan}

タイタンに関連するConfiguration / コンフィグレーション項目。

### <code>enabled</code> {#code-enabled-code}

-   Titanを有効または無効にします
-   デフォルト値： `false`

### <code>dirname</code> {#code-dirname-code}

-   TitanBlobファイルが保存されているディレクトリ
-   デフォルト値： `"titandb"`

### <code>disable-gc</code> {#code-disable-gc-code}

-   TitanがBlobファイルに対して実行するガベージコレクション（GC）を無効にするかどうかを決定します
-   デフォルト値： `false`

### <code>max-background-gc</code> {#code-max-background-gc-code}

-   TitanのGCスレッドの最大数
-   デフォルト値： `4`
-   最小値： `1`

## rocksdb.defaultcf | rocksdb.writecf | rocksdb.lockcf {#rocksdb-defaultcf-rocksdb-writecf-rocksdb-lockcf}

`rocksdb.defaultcf` 、および`rocksdb.writecf`に関連するConfiguration / コンフィグレーション`rocksdb.lockcf` 。

### <code>block-size</code> {#code-block-size-code}

-   RocksDBブロックのデフォルトサイズ
-   `defaultcf`および`writecf`のデフォルト値： `"64KB"`
-   `lockcf`のデフォルト値： `"16KB"`
-   最小値： `"1KB"`
-   単位：KB | MB | GB

### <code>block-cache-size</code> {#code-block-cache-size-code}

-   RocksDBブロックのキャッシュサイズ
-   `defaultcf`のデフォルト値： `Total machine memory * 25%`
-   `writecf`のデフォルト値： `Total machine memory * 15%`
-   `lockcf`のデフォルト値： `Total machine memory * 2%`
-   最小値： `0`
-   単位：KB | MB | GB

### <code>disable-block-cache</code> {#code-disable-block-cache-code}

-   ブロックキャッシュを有効または無効にします
-   デフォルト値： `false`

### <code>cache-index-and-filter-blocks</code> {#code-cache-index-and-filter-blocks-code}

-   キャッシュインデックスとフィルターを有効または無効にします
-   デフォルト値： `true`

### <code>pin-l0-filter-and-index-blocks</code> {#code-pin-l0-filter-and-index-blocks-code}

-   レベル0のSSTファイルのインデックスブロックとフィルターブロックをメモリに固定するかどうかを決定します。
-   デフォルト値： `true`

### <code>use-bloom-filter</code> {#code-use-bloom-filter-code}

-   ブルームフィルターを有効または無効にします
-   デフォルト値： `true`

### <code>optimize-filters-for-hits</code> {#code-optimize-filters-for-hits-code}

-   フィルタのヒット率を最適化するかどうかを決定します
-   `defaultcf`のデフォルト値： `true`
-   `writecf`および`lockcf`のデフォルト値： `false`

### <code>whole-key-filtering</code> {#code-whole-key-filtering-code}

-   キー全体をブルームフィルターに配置するかどうかを決定します
-   `defaultcf`および`lockcf`のデフォルト値： `true`
-   `writecf`のデフォルト値： `false`

### <code>bloom-filter-bits-per-key</code> {#code-bloom-filter-bits-per-key-code}

-   ブルームフィルターが各キーに予約する長さ
-   デフォルト値： `10`
-   単位：バイト

### <code>block-based-bloom-filter</code> {#code-block-based-bloom-filter-code}

-   各ブロックがブルームフィルターを作成するかどうかを決定します
-   デフォルト値： `false`

### <code>read-amp-bytes-per-bit</code> {#code-read-amp-bytes-per-bit-code}

-   読み取り増幅の統計を有効または無効にします。
-   オプションの値： `0` （無効）、&gt; `0` （有効）。
-   デフォルト値： `0`
-   最小値： `0`

### <code>compression-per-level</code> {#code-compression-per-level-code}

-   各レベルのデフォルトの圧縮アルゴリズム
-   `defaultcf`のデフォルト値：[&quot;no&quot;、 &quot;no&quot;、 &quot;lz4&quot;、 &quot;lz4&quot;、 &quot;lz4&quot;、 &quot;zstd&quot;、 &quot;zstd&quot;]
-   `writecf`のデフォルト値：[&quot;no&quot;、 &quot;no&quot;、 &quot;lz4&quot;、 &quot;lz4&quot;、 &quot;lz4&quot;、 &quot;zstd&quot;、 &quot;zstd&quot;]
-   `lockcf`のデフォルト値：[&quot;no&quot;、 &quot;no&quot;、 &quot;no&quot;、 &quot;no&quot;、 &quot;no&quot;、 &quot;no&quot;、 &quot;no&quot;]

### <code>bottommost-level-compression</code> {#code-bottommost-level-compression-code}

-   最下層の圧縮アルゴリズムを設定します。この構成項目は、 `compression-per-level`の設定をオーバーライドします。
-   データはLSMツリーに書き込まれるため、RocksDBは最下層の`compression-per-level`配列で指定された最後の圧縮アルゴリズムを直接採用しません。 `bottommost-level-compression`を使用すると、最下層で最初から最高の圧縮効果の圧縮アルゴリズムを使用できます。
-   最下層の圧縮アルゴリズムを設定しない場合は、この構成項目の値を`disable`に設定します。
-   デフォルト値： `"zstd"`

### <code>write-buffer-size</code> {#code-write-buffer-size-code}

-   Memtableサイズ
-   `defaultcf`および`writecf`のデフォルト値： `"128MB"`
-   `lockcf`のデフォルト値： `"32MB"`
-   最小値： `0`
-   単位：KB | MB | GB

### <code>max-write-buffer-number</code> {#code-max-write-buffer-number-code}

-   memtableの最大数。 `storage.flow-control.enable`が`true`に設定されている場合、 `storage.flow-control.memtables-threshold`はこの構成項目をオーバーライドします。
-   デフォルト値： `5`
-   最小値： `0`

### <code>min-write-buffer-number-to-merge</code> {#code-min-write-buffer-number-to-merge-code}

-   フラッシュをトリガーするために必要なmemtableの最小数
-   デフォルト値： `1`
-   最小値： `0`

### <code>max-bytes-for-level-base</code> {#code-max-bytes-for-level-base-code}

-   基本レベル（L1）での最大バイト数。通常、memtableの4倍のサイズに設定されています。
-   `defaultcf`および`writecf`のデフォルト値： `"512MB"`
-   `lockcf`のデフォルト値： `"128MB"`
-   最小値： `0`
-   単位：KB | MB | GB

### <code>target-file-size-base</code> {#code-target-file-size-base-code}

-   基本レベルでのターゲットファイルのサイズ。 `enable-compaction-guard`の値が`true`の場合、この値は`compaction-guard-max-output-file-size`で上書きされます。
-   デフォルト値： `"8MB"`
-   最小値： `0`
-   単位：KB | MB | GB

### <code>level0-file-num-compaction-trigger</code> {#code-level0-file-num-compaction-trigger-code}

-   圧縮をトリガーするL0でのファイルの最大数
-   `defaultcf`および`writecf`のデフォルト値： `4`
-   `lockcf`のデフォルト値： `1`
-   最小値： `0`

### <code>level0-slowdown-writes-trigger</code> {#code-level0-slowdown-writes-trigger-code}

-   書き込みストールをトリガーするL0でのファイルの最大数。 `storage.flow-control.enable`が`true`に設定されている場合、 `storage.flow-control.l0-files-threshold`はこの構成項目をオーバーライドします。
-   デフォルト値： `20`
-   最小値： `0`

### <code>level0-stop-writes-trigger</code> {#code-level0-stop-writes-trigger-code}

-   書き込みを完全にブロックするために必要なL0でのファイルの最大数
-   デフォルト値： `36`
-   最小値： `0`

### <code>max-compaction-bytes</code> {#code-max-compaction-bytes-code}

-   圧縮ごとにディスクに書き込まれる最大バイト数
-   デフォルト値： `"2GB"`
-   最小値： `0`
-   単位：KB | MB | GB

### <code>compaction-pri</code> {#code-compaction-pri-code}

-   圧縮の優先タイプ
-   `"min-overlapping-ratio"`の`"oldest-largest-seq-first"` `"oldest-smallest-seq-first"` `"by-compensated-size"`
-   `defaultcf`および`writecf`のデフォルト値： `"min-overlapping-ratio"`
-   `lockcf`のデフォルト値： `"by-compensated-size"`

### <code>dynamic-level-bytes</code> {#code-dynamic-level-bytes-code}

-   動的レベルのバイトを最適化するかどうかを決定します
-   デフォルト値： `true`

### <code>num-levels</code> {#code-num-levels-code}

-   RocksDBファイルのレベルの最大数
-   デフォルト値： `7`

### <code>max-bytes-for-level-multiplier</code> {#code-max-bytes-for-level-multiplier-code}

-   各層のデフォルトの増幅倍数
-   デフォルト値： `10`

### <code>compaction-style</code> {#code-compaction-style-code}

-   締固め方法
-   オプションの`"universal"` `"fifo"` `"level"`
-   デフォルト値： `"level"`

### <code>disable-auto-compactions</code> {#code-disable-auto-compactions-code}

-   自動圧縮を無効にするかどうかを決定します。
-   デフォルト値： `false`

### <code>soft-pending-compaction-bytes-limit</code> {#code-soft-pending-compaction-bytes-limit-code}

-   保留中の圧縮バイトのソフト制限。 `storage.flow-control.enable`が`true`に設定されている場合、 `storage.flow-control.soft-pending-compaction-bytes-limit`はこの構成項目をオーバーライドします。
-   デフォルト値： `"192GB"`
-   単位：KB | MB | GB

### <code>hard-pending-compaction-bytes-limit</code> {#code-hard-pending-compaction-bytes-limit-code}

-   保留中の圧縮バイトのハード制限。 `storage.flow-control.enable`が`true`に設定されている場合、 `storage.flow-control.hard-pending-compaction-bytes-limit`はこの構成項目をオーバーライドします。
-   デフォルト値： `"256GB"`
-   単位：KB | MB | GB

### <code>enable-compaction-guard</code> {#code-enable-compaction-guard-code}

-   圧縮ガードを有効または無効にします。これは、TiKV領域の境界でSSTファイルを分割するための最適化です。この最適化により、圧縮I / Oを削減し、TiKVがより大きなSSTファイルサイズを使用できるようになり（したがって、全体としてSSTファイルが少なくなります）、同時にリージョンの移行時に古いデータを効率的にクリーンアップできます。
-   `defaultcf`および`writecf`のデフォルト値： `true`
-   `lockcf`のデフォルト値： `false`

### <code>compaction-guard-min-output-file-size</code> {#code-compaction-guard-min-output-file-size-code}

-   圧縮ガードが有効になっている場合の最小SSTファイルサイズ。この構成により、圧縮ガードが有効になっているときにSSTファイルが小さすぎるのを防ぎます。
-   デフォルト値： `"8MB"`
-   単位：KB | MB | GB

### <code>compaction-guard-max-output-file-size</code> {#code-compaction-guard-max-output-file-size-code}

-   圧縮ガードが有効になっている場合の最大SSTファイルサイズ。この構成により、圧縮ガードが有効になっているときにSSTファイルが大きくなりすぎるのを防ぎます。この構成は、同じ列ファミリーの`target-file-size-base`をオーバーライドします。
-   デフォルト値： `"128MB"`
-   単位：KB | MB | GB

## rocksdb.defaultcf.titan {#rocksdb-defaultcf-titan}

`rocksdb.defaultcf.titan`に関連するConfiguration / コンフィグレーション項目。

### <code>min-blob-size</code> {#code-min-blob-size-code}

-   Blobファイルに格納されている最小値。指定されたサイズよりも小さい値は、LSMツリーに格納されます。
-   デフォルト値： `"1KB"`
-   最小値： `0`
-   単位：KB | MB | GB

### <code>blob-file-compression</code> {#code-blob-file-compression-code}

-   Blobファイルで使用される圧縮アルゴリズム
-   `"bzip2"` `"zstd"` `"lz4"` `"lz4hc"` `"no"` `"snappy"` `"zlib"`
-   デフォルト値： `"lz4"`

### <code>blob-cache-size</code> {#code-blob-cache-size-code}

-   Blobファイルのキャッシュサイズ
-   デフォルト値： `"0GB"`
-   最小値： `0`
-   単位：KB | MB | GB

### <code>min-gc-batch-size</code> {#code-min-gc-batch-size-code}

-   1回のGCの実行に必要なBlobファイルの最小合計サイズ
-   デフォルト値： `"16MB"`
-   最小値： `0`
-   単位：KB | MB | GB

### <code>max-gc-batch-size</code> {#code-max-gc-batch-size-code}

-   1回のGC実行が許可されるBlobファイルの最大合計サイズ
-   デフォルト値： `"64MB"`
-   最小値： `0`
-   単位：KB | MB | GB

### <code>discardable-ratio</code> {#code-discardable-ratio-code}

-   Blobファイルに対してGCがトリガーされる比率。 Blobファイルの無効な値の割合がこの比率を超える場合にのみ、BlobファイルをGCに選択できます。
-   デフォルト値： `0.5`
-   最小値： `0`
-   最大値： `1`

### <code>sample-ratio</code> {#code-sample-ratio-code}

-   GC中にファイルをサンプリングするときの（Blobファイルから読み取られたデータ/ Blobファイル全体）の比率
-   デフォルト値： `0.1`
-   最小値： `0`
-   最大値： `1`

### <code>merge-small-file-threshold</code> {#code-merge-small-file-threshold-code}

-   Blobファイルのサイズがこの値よりも小さい場合でも、BlobファイルがGC用に選択されている可能性があります。この状況では、 `discardable-ratio`は無視されます。
-   デフォルト値： `"8MB"`
-   最小値： `0`
-   単位：KB | MB | GB

### <code>blob-run-mode</code> {#code-blob-run-mode-code}

-   Titanの実行モードを指定します。
-   オプションの値：
    -   `normal` ：値のサイズが`min-blob-size`を超えると、データをblobファイルに書き込みます。
    -   `read_only` ：blobファイルへの新しいデータの書き込みを拒否しますが、blobファイルから元のデータを読み取ります。
    -   `fallback` ：blobファイルのデータをLSMに書き戻します。
-   デフォルト値： `normal`

### <code>level-merge</code> {#code-level-merge-code}

-   読み取りパフォーマンスを最適化するかどうかを決定します。 `level-merge`を有効にすると、より多くのライトアンプリフィケーションが発生します。
-   デフォルト値： `false`

### <code>gc-merge-rewrite</code> {#code-gc-merge-rewrite-code}

-   マージ演算子を使用してTitanGCのblobインデックスを書き戻すかどうかを決定します。 `gc-merge-rewrite`を有効にすると、フォアグラウンドでの書き込みに対するTitanGCの影響が軽減されます。
-   デフォルト値： `false`

## raftdb {#raftdb}

`raftdb`に関連するConfiguration / コンフィグレーション項目

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDBのバックグラウンドスレッドの数。 RocksDBスレッドプールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値： `4`
-   最小値： `2`

### <code>max-sub-compactions</code> {#code-max-sub-compactions-code}

-   RocksDBで実行された同時サブ圧縮操作の数
-   デフォルト値： `2`
-   最小値： `1`

### <code>wal-dir</code> {#code-wal-dir-code}

-   WALファイルが保存されているディレクトリ
-   デフォルト値： `"/tmp/tikv/store"`

## いかだエンジン {#raft-engine}

Raft Engineに関連するConfiguration / コンフィグレーション項目。

> **ノート：**
>
> -   Raft Engine Raft Engineを初めて有効にすると、TiKVはそのデータをRocksDBからRaftEngineに転送します。したがって、TiKVが開始するまでさらに数十秒待つ必要があります。
> -   TiDBv5.4.0のRaft Engineのデータ形式は、以前のTiDBバージョンと互換性がありません。したがって、TiDBクラスタをv5.4.0から以前のバージョンにダウングレードする必要がある場合は、ダウングレードする**前**に、 `enable`を`false`に設定してRaft Engineを無効にし、構成を有効にするためにTiKVを再起動します。

### <code>enable</code> {#code-enable-code}

-   RaftEngineを使用してRaft Engineログを保存するかどうかを決定します。有効にすると、 `raftdb`の構成は無視されます。
-   デフォルト値： `true`

### <code>dir</code> {#code-dir-code}

-   raftログファイルが保存されるディレクトリ。ディレクトリが存在しない場合は、TiKVの起動時に作成されます。
-   この構成が設定されていない場合、 `{data-dir}/raft-engine`が使用されます。
-   マシンに複数のディスクがある場合は、TiKVのパフォーマンスを向上させるために、 Raft Engineのデータを別のディスクに保存することをお勧めします。
-   デフォルト値： `""`

### <code>batch-compression-threshold</code> {#code-batch-compression-threshold-code}

-   ログバッチのしきい値サイズを指定します。この構成より大きいログバッチは圧縮されます。この構成項目を`0`に設定すると、圧縮は無効になります。
-   デフォルト値： `"8KB"`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   バッファリングされた書き込みの最大累積サイズを指定します。この構成値を超えると、バッファーされた書き込みがディスクにフラッシュされます。
-   この構成項目を`0`に設定すると、増分同期が無効になります。
-   デフォルト値： `"4MB"`

### <code>target-file-size</code> {#code-target-file-size-code}

-   ログファイルの最大サイズを指定します。ログファイルがこの値より大きい場合、ログファイルはローテーションされます。
-   デフォルト値： `"128MB"`

### <code>purge-threshold</code> {#code-purge-threshold-code}

-   メインログキューのしきい値サイズを指定します。この構成値を超えると、メインログキューが削除されます。
-   この構成は、 Raft Engineのディスクスペース使用量を調整するために使用できます。
-   デフォルト値： `"10GB"`

### <code>recovery-mode</code> {#code-recovery-mode-code}

-   リカバリ中のファイルの破損に対処する方法を決定します。
-   `"tolerate-tail-corruption"`のオプション`"tolerate-any-corruption"` `"absolute-consistency"`
-   デフォルト値： `"tolerate-tail-corruption"`

### <code>recovery-read-block-size</code> {#code-recovery-read-block-size-code}

-   リカバリ中にログファイルを読み取るための最小I/Oサイズ。
-   デフォルト値： `"16KB"`
-   最小値： `"512B"`

### <code>recovery-threads</code> {#code-recovery-threads-code}

-   ログファイルのスキャンと回復に使用されるスレッドの数。
-   デフォルト値： `4`
-   最小値： `1`

### <code>memory-limit</code> {#code-memory-limit-code}

-   Raft Engineのメモリ使用量の制限を指定します。
-   この構成値が設定されていない場合、使用可能なシステムメモリの15％が使用されます。
-   デフォルト値： `Total machine memory * 15%`

## 安全 {#security}

セキュリティに関連するConfiguration / コンフィグレーション項目。

### <code>ca-path</code> {#code-ca-path-code}

-   CAファイルのパス
-   デフォルト値： `""`

### <code>cert-path</code> {#code-cert-path-code}

-   X.509証明書を含むPrivacyEnhancedMail（PEM）ファイルのパス
-   デフォルト値： `""`

### <code>key-path</code> {#code-key-path-code}

-   X.509キーを含むPEMファイルのパス
-   デフォルト値： `""`

### <code>cert-allowed-cn</code> {#code-cert-allowed-cn-code}

-   クライアントによって提示された証明書で受け入れ可能なX.509共通名のリスト。要求は、提示された共通名がリスト内のエントリの1つと完全に一致する場合にのみ許可されます。
-   デフォルト値： `[]` 。これは、クライアント証明書のCNチェックがデフォルトで無効になっていることを意味します。

### <code>redact-info-log</code><span class="version-mark">新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v4-0-8-span}

-   この構成項目は、ログの編集を有効または無効にします。構成値が`true`に設定されている場合、ログ内のすべてのユーザーデータは`?`に置き換えられます。
-   デフォルト値： `false`

## security.encryption {#security-encryption}

[安静時の暗号化](/encryption-at-rest.md) （TDE）に関連するConfiguration / コンフィグレーション項目。

### <code>data-encryption-method</code> {#code-data-encryption-method-code}

-   データファイルの暗号化方式
-   値のオプション：「plaintext」、「aes128-ctr」、「aes192-ctr」、および「aes256-ctr」
-   「plaintext」以外の値は、暗号化が有効になっていることを意味します。この場合、マスターキーを指定する必要があります。
-   デフォルト値： `"plaintext"`

### <code>data-key-rotation-period</code> {#code-data-key-rotation-period-code}

-   TiKVがデータ暗号化キーをローテーションする頻度を指定します。
-   デフォルト値： `7d`

### enable-file-dictionary-log {#enable-file-dictionary-log}

-   TiKVが暗号化メタデータを管理するときに、最適化を有効にしてI/Oとミューテックスの競合を減らします。
-   この構成パラメーターが（デフォルトで）有効になっている場合に発生する可能性のある互換性の問題を回避するには、詳細について[保管保存時の暗号化-TiKVバージョン間の互換性](/encryption-at-rest.md#compatibility-between-tikv-versions)を参照してください。
-   デフォルト値： `true`

### マスターキー {#master-key}

-   暗号化が有効になっている場合は、マスターキーを指定します。マスターキーを構成する方法については、 [保存時の暗号化化-暗号化を構成します](/encryption-at-rest.md#configure-encryption)を参照してください。

### 前のマスターキー {#previous-master-key}

-   新しいマスターキーをローテーションするときに古いマスターキーを指定します。構成形式は`master-key`と同じです。マスターキーを構成する方法については、 [保存時の暗号化化-暗号化を構成します](/encryption-at-rest.md#configure-encryption)を参照してください。

## <code>import</code> {#code-import-code}

TiDBLightningのインポートとBRの復元に関連するConfiguration / コンフィグレーションアイテム。

### <code>num-threads</code> {#code-num-threads-code}

-   RPCリクエストを処理するスレッドの数
-   デフォルト値： `8`
-   最小値： `1`

## gc {#gc}

### <code>enable-compaction-filter</code> <span class="version-mark">filterv5.0の新機能</span> {#code-enable-compaction-filter-code-span-class-version-mark-new-in-v5-0-span}

-   圧縮フィルター機能でGCを有効にするかどうかを制御します
-   デフォルト値： `true`

## バックアップ {#backup}

BRバックアップに関連するConfiguration / コンフィグレーション項目。

### <code>num-threads</code> {#code-num-threads-code}

-   バックアップを処理するワーカースレッドの数
-   デフォルト値： `MIN(CPU * 0.5, 8)`
-   値の範囲： `[1, CPU]`
-   最小値： `1`

### <code>enable-auto-tune</code> <span class="version-mark">tunev5.4.0の新機能</span> {#code-enable-auto-tune-code-span-class-version-mark-new-in-v5-4-0-span}

-   クラスタリソースの使用率が高い場合にクラスタへの影響を減らすために、バックアップタスクで使用されるリソースを制限するかどうかを制御します。詳細については、 [BRオートチューン](/br/br-auto-tune.md)を参照してください。
-   デフォルト値： `true`

## CDC {#cdc}

TiCDCに関連するConfiguration / コンフィグレーション項目。

### <code>min-ts-interval</code> {#code-min-ts-interval-code}

-   解決済みTSが計算されて転送される間隔。
-   デフォルト値： `"1s"`

### <code>old-value-cache-memory-quota</code> {#code-old-value-cache-memory-quota-code}

-   TiCDCの古い値によるメモリ使用量の上限。
-   デフォルト値： `512MB`

### <code>sink-memory-quota</code> {#code-sink-memory-quota-code}

-   TiCDCデータ変更イベントによるメモリ使用量の上限。
-   デフォルト値： `512MB`

### <code>incremental-scan-speed-limit</code> {#code-incremental-scan-speed-limit-code}

-   履歴データが段階的にスキャンされる最大速度。
-   デフォルト値： `"128MB"` 、これは1秒あたり128MBを意味します。

### <code>incremental-scan-threads</code> {#code-incremental-scan-threads-code}

-   履歴データを段階的にスキャンするタスクのスレッド数。
-   デフォルト値： `4` 、これは4スレッドを意味します。

### <code>incremental-scan-concurrency</code> {#code-incremental-scan-concurrency-code}

-   履歴データを段階的にスキャンするタスクの同時実行の最大数。
-   デフォルト値： `6` 。これは、最大6つのタスクを同時に実行できることを意味します。
-   注： `incremental-scan-concurrency`の値は`incremental-scan-threads`の値以上である必要があります。それ以外の場合、TiKVは起動時にエラーを報告します。

## 解決済み-ts {#resolved-ts}

古い読み取り要求を処理するための解決済みTSの保守に関連するConfiguration / コンフィグレーション項目。

### <code>enable</code> {#code-enable-code}

-   すべてのリージョンの解決済みTSを維持するかどうかを決定します。
-   デフォルト値： `true`

### <code>advance-ts-interval</code> {#code-advance-ts-interval-code}

-   解決済みTSが計算されて転送される間隔。
-   デフォルト値： `"1s"`

### <code>scan-lock-pool-size</code> {#code-scan-lock-pool-size-code}

-   解決済みTSを初期化するときに、TiKVがMVCC（マルチバージョン同時実行制御）ロックデータをスキャンするために使用するスレッドの数。
-   デフォルト値： `2` 、これは2スレッドを意味します。

## 悲観的-txn {#pessimistic-txn}

悲観的なトランザクションの使用法については、 [TiDB悲観的トランザクションモード](/pessimistic-transaction.md)を参照してください。

### <code>wait-for-lock-timeout</code> {#code-wait-for-lock-timeout-code}

-   TiKVのペシミスティックトランザクションが、他のトランザクションがロックを解放するのを待機する最長の時間。タイムアウトになると、エラーがTiDBに返され、TiDBはロックの追加を再試行します。ロック待機タイムアウトは`innodb_lock_wait_timeout`で設定されます。
-   デフォルト値： `"1s"`
-   最小値： `"1ms"`

### <code>wake-up-delay-duration</code> {#code-wake-up-delay-duration-code}

-   悲観的なトランザクションがロックを解除すると、ロックを待機しているすべてのトランザクションの中で、最小の`start_ts`のトランザクションのみがウェイクアップされます。その他のトランザクションは`wake-up-delay-duration`後にウェイクアップされます。
-   デフォルト値： `"20ms"`

### <code>pipelined</code> {#code-pipelined-code}

-   この構成アイテムは、ペシミスティックロックを追加するパイプラインプロセスを有効にします。この機能を有効にすると、データがロックされる可能性があることを検出すると、TiKVはすぐにTiDBに通知して、後続のリクエストを実行し、ペシミスティックロックを非同期で書き込みます。これにより、ほとんどのレイテンシが短縮され、ペシミスティックトランザクションのパフォーマンスが大幅に向上します。ただし、ペシミスティックロックの非同期書き込みが失敗する可能性はまだ低く、ペシミスティックトランザクションコミットの失敗を引き起こす可能性があります。
-   デフォルト値： `true`

### <code>in-memory</code> （v6.0.0の新機能） {#code-in-memory-code-new-in-v6-0-0}

-   インメモリペシミスティックロック機能を有効にします。この機能を有効にすると、ペシミスティックトランザクションは、ロックをディスクに書き込んだり、ロックを他のレプリカに複製したりする代わりに、ロックをメモリに保存しようとします。これにより、悲観的なトランザクションのパフォーマンスが向上します。ただし、ペシミスティックロックが失われ、ペシミスティックトランザクションのコミットが失敗する可能性はまだ低いです。
-   デフォルト値： `true`
-   `in-memory`は、 `pipelined`の値が`true`の場合にのみ有効になることに注意してください。

## クォータ {#quota}

クォータリミッターに関連するConfiguration / コンフィグレーション項目。

TiKVが展開されているマシンのリソースが限られているとします。たとえば、4vCPUと16Gメモリのみです。この状況では、TiKVのフォアグラウンドが処理する読み取りおよび書き込み要求が多すぎるため、バックグラウンドで使用されるCPUリソースがそのような要求の処理を支援するために占有され、TiKVのパフォーマンスの安定性に影響を与える可能性があります。この状況を回避するには、クォータ関連の構成アイテムを使用して、フォアグラウンドで使用されるCPUリソースを制限します。リクエストがクォータリミッターをトリガーすると、リクエストはTiKVがCPUリソースを解放するまでしばらく待機するように強制されます。正確な待機時間はリクエストの数によって異なり、最大待機時間は値[`max-delay-duration`](#max-delay-duration-new-in-v600)以下です。

> **警告：**
>
> -   Quota Limiterは、TiDB v6.0.0で導入された実験的機能であり、実稼働環境で使用することはお勧めし**ません**。
> -   この機能は、リソースが限られている環境にのみ適しており、TiKVがそれらの環境で安定して実行できるようにします。リソースが豊富な環境でこの機能を有効にすると、リクエストの量がピークに達したときにパフォーマンスが低下する可能性があります。

### <code>foreground-cpu-time</code> （v6.0.0の新機能） {#code-foreground-cpu-time-code-new-in-v6-0-0}

-   読み取りおよび書き込み要求を処理するためにTiKVフォアグラウンドによって使用されるCPUリソースのソフト制限。
-   デフォルト値： `0` （これは制限なしを意味します）
-   単位：millicpu（たとえば、 `1500`は、フォアグラウンド要求が1.5v CPUを消費することを意味します）

### <code>foreground-write-bandwidth</code> （v6.0.0の新機能） {#code-foreground-write-bandwidth-code-new-in-v6-0-0}

-   トランザクションがデータを書き込む帯域幅のソフト制限。
-   デフォルト値： `0KB` （これは制限なしを意味します）

### <code>foreground-read-bandwidth</code> （v6.0.0の新機能） {#code-foreground-read-bandwidth-code-new-in-v6-0-0}

-   トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限。
-   デフォルト値： `0KB` （これは制限なしを意味します）

### <code>max-delay-duration</code> （v6.0.0の新機能） {#code-max-delay-duration-code-new-in-v6-0-0}

-   単一の読み取りまたは書き込み要求がフォアグラウンドで処理される前に強制的に待機される最大時間。
-   デフォルト値： `500ms`

## causal- <span class="version-mark">tsv6.1.0の新機能</span> {#causal-ts-span-class-version-mark-new-in-v6-1-0-span}

TiKV API V2が有効になっている場合のタイムスタンプの取得に関連するConfiguration / コンフィグレーション項目（ `storage.api-version = 2` ）。

書き込み遅延を減らし、PDへの頻繁なアクセスを回避するために、TiKVは定期的にタイムスタンプのバッチをローカルでフェッチしてキャッシュします。ローカルにキャッシュされたタイムスタンプが使い果たされると、TiKVはすぐにタイムスタンプ要求を行います。この状況では、一部の書き込み要求のレイテンシーが増加します。この状況の発生を減らすために、TiKVは、ワークロードに応じてローカルにキャッシュされたタイムスタンプのサイズを動的に調整します。ほとんどの場合、次のパラメータを調整する必要はありません。

> **警告：**
>
> TiKVAPIV2はまだ実験的機能です。実稼働環境での使用はお勧めしません。

### <code>renew-interval</code> {#code-renew-interval-code}

-   ローカルにキャッシュされたタイムスタンプが更新される間隔。
-   `renew-interval`の間隔で、TiKVはタイムスタンプ更新のバッチを開始し、前の期間のタイムスタンプ消費に応じてキャッシュされたタイムスタンプの数を調整します。このパラメーターを大きすぎる値に設定すると、最新のTiKVワークロードの変更が時間に反映されません。このパラメータを小さすぎる値に設定すると、PDの負荷が増加します。書き込みトラフィックが大きく変動している場合、タイムスタンプが頻繁に使い果たされている場合、および書き込み遅延が増加している場合は、このパラメーターを小さい値に設定できます。同時に、PDの負荷も考慮する必要があります。
-   デフォルト値： `"100ms"`

### <code>renew-batch-min-size</code> {#code-renew-batch-min-size-code}

-   ローカルにキャッシュされたタイムスタンプの最小数。
-   TiKVは、前の期間のタイムスタンプの消費量に応じて、キャッシュされたタイムスタンプの数を調整します。ローカルにキャッシュされたタイムスタンプの使用率が低い場合、TiKVはキャッシュされたタイムスタンプの数を`renew-batch-min-size`に達するまで徐々に減らします。アプリケーションで大量のバースト書き込みトラフィックが頻繁に発生する場合は、必要に応じてこのパラメーターをより大きな値に設定できます。このパラメーターは、単一のtikvサーバーのキャッシュサイズであることに注意してください。パラメーターを大きすぎる値に設定し、クラスタに多数のtikvサーバーが含まれている場合、TSOの消費が速すぎます。
-   Grafanaの**TiKV-RAW** &gt; <strong>Causalタイムスタンプ</strong>パネルでは、 <strong>TSOバッチサイズ</strong>は、アプリケーションのワークロードに応じて動的に調整された、ローカルにキャッシュされたタイムスタンプの数です。このメトリックを参照して`renew-batch-min-size`を調整できます。
-   デフォルト値： `100`
