---
title: TiKV Configuration File
summary: Learn the TiKV configuration file.
---

# TiKVコンフィグレーションファイル {#tikv-configuration-file}

<!-- markdownlint-disable MD001 -->

TiKV 構成ファイルは、コマンドライン パラメーターよりも多くのオプションをサポートしています。デフォルトの構成ファイルは[etc/config-template.toml](https://github.com/tikv/tikv/blob/master/etc/config-template.toml)にあり、その名前を`config.toml`に変更します。

このドキュメントでは、コマンドライン パラメーターに含まれないパラメーターのみについて説明します。詳細については、 [コマンドラインパラメータ](/command-line-flags-for-tikv-configuration.md)を参照してください。

> **ヒント：**
>
> 設定項目の値を調整する必要がある場合は、 [構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

## グローバル構成 {#global-configuration}

### <code>abort-on-panic</code> {#code-abort-on-panic-code}

-   TiKV パニック時に`abort()`を呼び出してプロセスを終了するかどうかを設定します。このオプションは、TiKV がシステムでコア ダンプ ファイルの生成を許可するかどうかに影響します。

    -   この構成項目の値が`false`の場合、TiKV がパニックになると、 `exit()`を呼び出してプロセスを終了します。
    -   この構成項目の値が`true`の場合、TiKV がパニックになると、TiKV は`abort()`を呼び出してプロセスを終了します。現時点では、TiKV により、システムは終了時にコア ダンプ ファイルを生成できます。コア ダンプ ファイルを生成するには、コア ダンプに関連するシステム構成 (たとえば、 `ulimit -c`コマンドを使用してコア ダンプ ファイルのサイズ制限を設定し、コア ダンプ パスを構成するなど) を実行する必要もあります。オペレーティング システムが異なると、関連する構成も異なります。 ）。コア ダンプ ファイルが多くのディスク領域を占有し、TiKV のディスク領域が不足することを避けるために、TiKV データとは異なるディスク パーティションにコア ダンプ生成パスを設定することをお勧めします。

-   デフォルト値: `false`

### <code>slow-log-file</code> {#code-slow-log-file-code}

-   遅いログを保存するファイル
-   この設定項目が設定されておらず、 `log.file.filename`が設定されている場合、スローログは`log.file.filename`で指定されたログファイルに出力されます。
-   `slow-log-file`も`log.file.filename`設定されていない場合、デフォルトですべてのログが「stderr」に出力されます。
-   両方の設定項目が設定されている場合、通常ログは`log.file.filename`で指定したログファイルに出力され、スローログは`slow-log-file`で指定したログファイルに出力されます。
-   デフォルト値: `""`

### <code>slow-log-threshold</code> {#code-slow-log-threshold-code}

-   低速ログを出力するためのしきい値。処理時間がこの閾値よりも長い場合、遅いログが出力されます。
-   デフォルト値: `"1s"`

### <code>memory-usage-limit</code> {#code-memory-usage-limit-code}

-   TiKV インスタンスのメモリ使用量の制限。 TiKV のメモリ使用量がこのしきい値にほぼ達すると、内部キャッシュが削除されてメモリが解放されます。
-   ほとんどの場合、TiKV インスタンスは利用可能なシステムメモリの合計の 75% を使用するように設定されているため、この構成項目を明示的に指定する必要はありません。メモリの残りの 25% は OS ページ キャッシュ用に予約されています。詳細については[`storage.block-cache.capacity`](#capacity)を参照してください。
-   単一の物理マシンに複数の TiKV ノードを展開する場合でも、この構成項目を設定する必要はありません。この場合、TiKV インスタンスは`5/3 * block-cache.capacity`のメモリを使用します。
-   さまざまなシステムメモリ容量のデフォルト値は次のとおりです。

    -   システム=8G ブロックキャッシュ=3.6G メモリ使用量制限=6G ページキャッシュ=2G
    -   システム=16G ブロックキャッシュ=7.2G メモリ使用量制限=12G ページキャッシュ=4G
    -   システム=32G ブロックキャッシュ=14.4G メモリ使用量制限=24G ページキャッシュ=8G

## ログ<span class="version-mark">v5.4.0 の新機能</span> {#log-span-class-version-mark-new-in-v5-4-0-span}

-   ログに関するコンフィグレーション項目です。

-   v5.4.0 より、TiKV と TiDB のログ設定項目を整合させるため、TiKV は以前の設定項目`log-rotation-timespan`を非推奨とし、 `log-level` 、 `log-format` 、 `log-file` 、 `log-rotation-size`を以下の設定項目に変更します。古い構成項目のみを設定し、その値がデフォルト以外の値に設定されている場合、古い項目は新しい項目との互換性を維持します。新旧両方の設定項目が設定されている場合は、新しい設定項目が有効になります。

### <code>level</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-level-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログレベル
-   オプションの値: `"debug"` 、 `"info"` 、 `"warn"` 、 `"error"` 、 `"fatal"`
-   デフォルト値: `"info"`

### <code>format</code> <span class="version-mark">v5.4.0 の新</span>機能 {#code-format-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログ形式
-   オプション`"text"`値: `"json"`
-   デフォルト値: `"text"`

### イネーブルタイムスタンプ<span class="version-mark">v5.4.0 の新</span><code>enable-timestamp</code> {#code-enable-timestamp-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログのタイムスタンプを有効にするか無効にするかを決定します。
-   オプション`false`値: `true`
-   デフォルト値: `true`

## log.file <span class="version-mark">v5.4.0 の新機能</span> {#log-file-span-class-version-mark-new-in-v5-4-0-span}

-   ログファイルに関するコンフィグレーション項目です。

### <code>filename</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-filename-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログファイル。本設定項目が設定されていない場合、デフォルトでログは「stderr」に出力されます。この設定項目を設定すると、対応するファイルにログが出力されます。
-   デフォルト値: `""`

### <code>max-size</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-max-size-code-span-class-version-mark-new-in-v5-4-0-span}

-   単一のログ ファイルの最大サイズ。ファイルサイズがこの設定項目で設定した値より大きい場合、システムは自動的に 1 つのファイルを複数のファイルに分割します。
-   デフォルト値: `300`
-   最大値： `4096`
-   単位: MiB

### <code>max-days</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-max-days-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKV がログ ファイルを保持する最大日数。
    -   構成項目が設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKV はログ ファイルをクリーンアップしません。
    -   このパラメーターが`0`以外の値に設定されている場合、TiKV は`max-days`の後に期限切れのログ ファイルをクリーンアップします。
-   デフォルト値: `0`

### <code>max-backups</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-max-backups-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKV が保持するログ ファイルの最大数。
    -   構成項目が設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKV はすべてのログ ファイルを保持します。
    -   構成項目が`0`以外の値に設定されている場合、TiKV は最大で`max-backups`で指定された数の古いログ ファイルを保持します。たとえば、値が`7`に設定されている場合、TiKV は最大 7 つの古いログ ファイルを保持します。
-   デフォルト値: `0`

### <code>pd.enable-forwarding</code> <span class="version-mark">v5.0.0 の新機能</span> {#code-pd-enable-forwarding-code-span-class-version-mark-new-in-v5-0-0-span}

-   ネットワーク分離の可能性がある場合に、TiKV の PD クライアントがフォロワー経由でリーダーにリクエストを転送するかどうかを制御します。
-   デフォルト値: `false`
-   環境でネットワークが分離されている可能性がある場合、このパラメータを有効にすると、サービスが利用できなくなる期間を短縮できます。
-   分離、ネットワークの中断、またはダウンタイムが発生したかどうかを正確に判断できない場合、このメカニズムを使用すると判断を誤るリスクがあり、可用性とパフォーマンスの低下が発生します。ネットワーク障害が発生したことがない場合は、このパラメータを有効にすることはお勧めできません。

## サーバー {#server}

-   サーバーに関連するコンフィグレーション項目。

### <code>addr</code> {#code-addr-code}

-   リスニングIPアドレスとリスニングポート
-   デフォルト値: `"127.0.0.1:20160"`

### <code>advertise-addr</code> {#code-advertise-addr-code}

-   クライアント通信用のリスニング アドレスをアドバタイズする
-   この構成項目が設定されていない場合は、値`addr`が使用されます。
-   デフォルト値: `""`

### <code>status-addr</code> {#code-status-addr-code}

-   構成アイテムは、 `HTTP`アドレスを通じて TiKV ステータスを直接報告します。

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
-   `"gzip"` `"deflate"`値: `"none"`
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
-   OOM が発生した場合に備えてメモリを制限します。使用量を制限すると、ストールが発生する可能性があることに注意してください

### <code>grpc-raft-conn-num</code> {#code-grpc-raft-conn-num-code}

-   Raft通信における TiKV ノード間の最大リンク数
-   デフォルト値: `1`
-   最小値: `1`

### <code>max-grpc-send-msg-len</code> {#code-max-grpc-send-msg-len-code}

-   送信できる gRPC メッセージの最大長を設定します
-   デフォルト値: `10485760`
-   単位: バイト
-   最大値： `2147483647`

### <code>grpc-stream-initial-window-size</code> {#code-grpc-stream-initial-window-size-code}

-   gRPC ストリームのウィンドウ サイズ
-   デフォルト値: `2MB`
-   単位: KB|MB|GB
-   最小値: `"1KB"`

### <code>grpc-keepalive-time</code> {#code-grpc-keepalive-time-code}

-   gRPC が`keepalive` Ping メッセージを送信する時間間隔
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

-   タスクを処理するための TiDB の TiKV へのプッシュダウン リクエストに許可される最長期間
-   デフォルト値: `"60s"`
-   最小値: `"1s"`

### <code>snap-io-max-bytes-per-sec</code> {#code-snap-io-max-bytes-per-sec-code}

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

-   バックグラウンド プールの作業スレッド数。これには、エンドポイント スレッド、 BRスレッド、分割チェック スレッド、リージョンスレッド、および遅延に影響されないタスクのその他のスレッドが含まれます。
-   デフォルト値: CPU コアの数が 16 未満の場合、デフォルト値は`2`です。それ以外の場合、デフォルト値は`3`です。

### <code>end-point-slow-log-threshold</code> {#code-end-point-slow-log-threshold-code}

-   TiDB のプッシュダウン リクエストが低速ログを出力するまでの時間のしきい値。処理時間がこの閾値よりも長い場合、スローログが出力されます。
-   デフォルト値: `"1s"`
-   最小値: `0`

### <code>raft-client-queue-size</code> {#code-raft-client-queue-size-code}

-   TiKV のRaftメッセージのキュー サイズを指定します。時間内に送信されなかったメッセージが多すぎてバッファがいっぱいになったり、メッセージが破棄されたりする場合は、より大きな値を指定してシステムの安定性を向上させることができます。
-   デフォルト値: `8192`

### <code>simplify-metrics</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-simplify-metrics-code-span-class-version-mark-new-in-v6-2-0-span}

-   返された監視メトリックを簡素化するかどうかを指定します。値を`true`に設定すると、TiKV は一部のメトリックをフィルターで除外することにより、各リクエストに対して返されるデータの量を減らします。
-   デフォルト値: `false`

### <code>forward-max-connections-per-address</code> <span class="version-mark">v5.0.0 の新機能</span> {#code-forward-max-connections-per-address-code-span-class-version-mark-new-in-v5-0-0-span}

-   サービスおよびサーバーへのリクエストの転送用の接続プールのサイズを設定します。設定する値が小さすぎると、リクエストのレイテンシーと負荷分散に影響します。
-   デフォルト値: `4`

## 読み取りプール.統合 {#readpool-unified}

読み取りリクエストを処理する単一スレッド プールに関連するコンフィグレーションアイテム。このスレッド プールは、バージョン 4.0 以降、元のstorageスレッド プールおよびコプロセッサ スレッド プールに取って代わります。

### <code>min-thread-count</code> {#code-min-thread-count-code}

-   統合読み取りプールの最小作業スレッド数
-   デフォルト値: `1`

### <code>max-thread-count</code> {#code-max-thread-count-code}

-   統合読み取りプールまたは UnifyReadPool スレッド プールの最大作業スレッド数。このスレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   値の範囲: `[min-thread-count, MAX(4, CPU quota * 10)]` 。 `MAX(4, CPU quota * 10)` `4`と`CPU quota * 10`のうち大きい方の値を取得します。
-   デフォルト値: MAX(4、CPU * 0.8)

> **注記：**
>
> スレッド数を増やすとコンテキストの切り替えが多くなり、パフォーマンスが低下する可能性があります。この構成項目の値を変更することはお勧めできません。

### <code>stack-size</code> {#code-stack-size-code}

-   統合スレッド プール内のスレッドのスタック サイズ
-   タイプ: 整数 + 単位
-   デフォルト値: `"10MB"`
-   単位: KB|MB|GB
-   最小値: `"2MB"`
-   最大値：システム内で`ulimit -sH`コマンドを実行した結果出力されるKバイト数。

### <code>max-tasks-per-worker</code> {#code-max-tasks-per-worker-code}

-   統合読み取りプール内の単一スレッドに許可されるタスクの最大数。値を超えた場合は`Server Is Busy`を返します。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>auto-adjust-pool-size</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-auto-adjust-pool-size-code-span-class-version-mark-new-in-v6-3-0-span}

-   スレッド プール サイズを自動的に調整するかどうかを制御します。有効にすると、現在の CPU 使用率に基づいて UnifyReadPool スレッド プール サイズを自動的に調整することで、TiKV の読み取りパフォーマンスが最適化されます。スレッド プールの可能な範囲は`[max-thread-count, MAX(4, CPU)]`です。最大値は[`max-thread-count`](#max-thread-count)と同じです。
-   デフォルト値: `false`

## リードプール。storage {#readpool-storage}

storageスレッドプールに関連するコンフィグレーション項目。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   storage要求に統合スレッド プール ( [`readpool.unified`](#readpoolunified)で構成) を使用するかどうかを決定します。このパラメータの値が`false`の場合、別のスレッド プールが使用されます。これは、このセクション ( `readpool.storage` ) の残りのパラメータを通じて構成されます。
-   デフォルト値: このセクション ( `readpool.storage` ) に他の構成がない場合、デフォルト値は`true`です。それ以外の場合、下位互換性のために、デフォルト値は`false`です。このオプションを有効にする前に、必要に応じて[`readpool.unified`](#readpoolunified)の構成を変更してください。

### <code>high-concurrency</code> {#code-high-concurrency-code}

-   高優先度`read`リクエストを処理する同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>normal-concurrency</code> {#code-normal-concurrency-code}

-   通常優先度`read`リクエストを処理する同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>low-concurrency</code> {#code-low-concurrency-code}

-   優先度の低い`read`リクエストを処理する同時スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>max-tasks-per-worker-high</code> {#code-max-tasks-per-worker-high-code}

-   高優先度のスレッド プール内の単一スレッドに許可されるタスクの最大数。値を超えた場合は`Server Is Busy`を返します。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-normal</code> {#code-max-tasks-per-worker-normal-code}

-   通常優先度のスレッド プール内の 1 つのスレッドに許可されるタスクの最大数。値を超えた場合は`Server Is Busy`を返します。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-low</code> {#code-max-tasks-per-worker-low-code}

-   低優先度のスレッド プール内の単一スレッドに許可されるタスクの最大数。値を超えた場合は`Server Is Busy`を返します。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>stack-size</code> {#code-stack-size-code}

-   ストレージ読み取りスレッド プール内のスレッドのスタック サイズ
-   タイプ: 整数 + 単位
-   デフォルト値: `"10MB"`
-   単位: KB|MB|GB
-   最小値: `"2MB"`
-   最大値：システム内で`ulimit -sH`コマンドを実行した結果出力されるKバイト数。

## <code>readpool.coprocessor</code> {#code-readpool-coprocessor-code}

コプロセッサースレッドプールに関連するコンフィグレーション項目。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   コプロセッサ要求に統合スレッド プール ( [`readpool.unified`](#readpoolunified)で構成) を使用するかどうかを決定します。このパラメータの値が`false`の場合、別のスレッド プールが使用されます。これは、このセクション ( `readpool.coprocessor` ) の残りのパラメータを通じて構成されます。
-   デフォルト値: このセクション ( `readpool.coprocessor` ) のパラメータが何も設定されていない場合、デフォルト値は`true`です。それ以外の場合、下位互換性のためにデフォルト値は`false`です。このパラメータを有効にする前に、 [`readpool.unified`](#readpoolunified)の設定項目を調整してください。

### <code>high-concurrency</code> {#code-high-concurrency-code}

-   チェックポイントなどの優先度の高いコプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>normal-concurrency</code> {#code-normal-concurrency-code}

-   通常優先度のコプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>low-concurrency</code> {#code-low-concurrency-code}

-   テーブル スキャンなど、優先度の低いコプロセッサー要求を処理する同時スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>max-tasks-per-worker-high</code> {#code-max-tasks-per-worker-high-code}

-   高優先度のスレッド プール内の単一スレッドに許可されるタスクの数。この数を超えると`Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-normal</code> {#code-max-tasks-per-worker-normal-code}

-   通常優先度のスレッド プール内の 1 つのスレッドに許可されるタスクの数。この数を超えると`Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-low</code> {#code-max-tasks-per-worker-low-code}

-   低優先度のスレッド プール内の単一スレッドに許可されるタスクの数。この数を超えると`Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>stack-size</code> {#code-stack-size-code}

-   コプロセッサースレッドプール内のスレッドのスタックサイズ
-   タイプ: 整数 + 単位
-   デフォルト値: `"10MB"`
-   単位: KB|MB|GB
-   最小値: `"2MB"`
-   最大値：システム内で`ulimit -sH`コマンドを実行した結果出力されるKバイト数。

## storage {#storage}

storageに関するコンフィグレーション項目。

### <code>data-dir</code> {#code-data-dir-code}

-   RocksDB ディレクトリのstorageパス
-   デフォルト値: `"./"`

### <code>engine</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-engine-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   エンジンの種類を指定します。この構成は、新しいクラスターの作成時にのみ指定でき、一度指定すると変更できません。
-   デフォルト値: `"raft-kv"`
-   値のオプション:

    -   `"raft-kv"` : TiDB v6.6.0 より前のバージョンのデフォルトのエンジン タイプ。
    -   `"partitioned-raft-kv"` : TiDB v6.6.0 で導入された新しいstorageエンジン タイプ。

### <code>scheduler-concurrency</code> {#code-scheduler-concurrency-code}

-   キーの同時操作を防止するメモリロック機構を内蔵しています。各キーは異なるスロットにハッシュを持ちます。
-   デフォルト値: `524288`
-   最小値: `1`

### <code>scheduler-worker-pool-size</code> {#code-scheduler-worker-pool-size-code}

-   スケジューラのスレッド プール内のスレッドの数。スケジューラ スレッドは主に、データの書き込み前にトランザクションの整合性をチェックするために使用されます。 CPU コアの数が`16`以上の場合、デフォルト値は`8`です。それ以外の場合、デフォルト値は`4`です。スケジューラのスレッドプールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `4`
-   値の範囲: `[1, MAX(4, CPU)]` 。 `MAX(4, CPU)`の`CPU` CPU コアの数を意味します。 `MAX(4, CPU)` `4`と`CPU`のうち大きい方の値を取得します。

### <code>scheduler-pending-write-threshold</code> {#code-scheduler-pending-write-threshold-code}

-   書き込みキューの最大サイズ。この値を超えると、TiKV への新規書き込みに対して`Server Is Busy`エラーが返されます。
-   デフォルト値: `"100MB"`
-   単位: MB|GB

### <code>enable-async-apply-prewrite</code> {#code-enable-async-apply-prewrite-code}

-   事前書き込みリクエストを適用する前に、非同期コミット トランザクションが TiKV クライアントに応答するかどうかを決定します。この設定項目を有効にすると、適用期間が長い場合にレイテンシーを簡単に削減でき、適用期間が安定していない場合に遅延ジッターを削減できます。
-   デフォルト値: `false`

### <code>reserve-space</code> {#code-reserve-space-code}

-   TiKV が開始されると、ディスク保護としてディスク上に一部のスペースが予約されます。残りのディスク容量が予約容量より少ない場合、TiKV は一部の書き込み操作を制限します。予約領域は 2 つの部分に分かれており、予約領域の 80% はディスク領域が不足した場合の運用に必要な追加ディスク領域として使用され、残りの 20% は一時ファイルの保存に使用されます。スペースを再利用するプロセスで、余分なディスクスペースを使用しすぎてstorageが使い果たされた場合、この一時ファイルはサービスを復元するための最後の保護として機能します。
-   一時ファイルの名前は`space_placeholder_file`で、 `storage.data-dir`ディレクトリにあります。ディスク領域が不足して TiKV がオフラインになった場合、TiKV を再起動すると、一時ファイルは自動的に削除され、TiKV は領域を再利用しようとします。
-   残りの容量が不足している場合、TiKV は一時ファイルを作成しません。保護の有効性は、予約されたスペースのサイズに関係します。予約領域のサイズは、ディスク容量の 5% とこの設定値の間の大きい方の値になります。この構成項目の値が`"0MB"`の場合、TiKV はこのディスク保護機能を無効にします。
-   デフォルト値: `"5GB"`
-   単位: MB|GB

### <code>enable-ttl</code> {#code-enable-ttl-code}

> **警告：**
>
> -   新しい TiKV クラスターをデプロイする**場合にのみ、** `enable-ttl`から`true`または`false`を設定します。既存の TiKV クラスターでこの構成項目の値を変更**しないでください**。異なる`enable-ttl`値を持つ TiKV クラスターは、異なるデータ形式を使用します。したがって、既存の TiKV クラスターでこの項目の値を変更すると、クラスターはデータを別の形式で保存することになり、TiKV クラスターを再起動するときに「非 TTL では TTL を有効にできません」というエラーが発生します。
> -   TiKV クラスター**内でのみ**`enable-ttl`を使用します。 TiDB ノードを含むクラスターではこの構成項目を使用し**ないでください**(つまり、そのようなクラスターでは`enable-ttl`から`true`を設定します)。そうしないと、データの破損や TiDB クラスターのアップグレードの失敗などの重大な問題が発生します。

-   TTL は「生存時間」の略です。この項目を有効にすると、TiKV は TTL に達したデータを自動的に削除します。 TTL の値を設定するには、クライアント経由でデータを書き込むときにリクエストで TTL 値を指定する必要があります。 TTL が指定されていない場合は、TiKV が対応するデータを自動的に削除しないことを意味します。
-   デフォルト値: `false`

### <code>ttl-check-poll-interval</code> {#code-ttl-check-poll-interval-code}

-   物理スペースを再利用するためにデータをチェックする間隔。データが TTL に達すると、TiKV はチェック中に物理スペースを強制的に再利用します。
-   デフォルト値: `"12h"`
-   最小値: `"0s"`

### <code>background-error-recovery-window</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-background-error-recovery-window-code-span-class-version-mark-new-in-v6-1-0-span}

-   RocksDB が回復可能なバックグラウンド エラーを検出した後、TiKV が回復するまでの最大許容時間。一部のバックグラウンド SST ファイルが破損した場合、RocksDB は破損した SST ファイルが属するピアを特定した後、ハートビート経由で PD に報告します。次に、PD はスケジューリング操作を実行して、このピアを削除します。最後に、破損した SST ファイルは直接削除され、TiKV バックグラウンドは再び通常どおりに動作するようになります。
-   破損した SST ファイルは、回復が完了する前にまだ存在します。この期間中、RocksDB はデータの書き込みを続行できますが、データの破損した部分が読み取られるとエラーが報告されます。
-   この時間枠内にリカバリが完了しない場合、TiKV はpanicになります。
-   デフォルト値: 1h

### <code>api-version</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-api-version-code-span-class-version-mark-new-in-v6-1-0-span}

-   TiKV が RawKV ストアとして機能するときに TiKV によって使用されるstorage形式とインターフェイスのバージョン。
-   値のオプション:
    -   `1` : API V1を使用し、クライアントから渡されたデータをエンコードせず、そのままのデータを格納します。 v6.1.0 より前のバージョンでは、TiKV はデフォルトで API V1 を使用します。
    -   `2` : API V2 を使用します:
        -   データはマルチバージョン同時実行制御 (MVCC) 形式で保存され、タイムスタンプは tikv-server によって PD (TSO) から取得されます。
        -   データはさまざまな用途に応じてスコープ設定され、API V2 は単一クラスター内での TiDB、トランザクション KV、および RawKV アプリケーションの共存をサポートします。
        -   API V2 を使用する場合は、同時に`storage.enable-ttl = true`を設定する必要があります。 API V2 は TTL 機能をサポートしているため、 `enable-ttl`明示的にオンにする必要があります。そうしないと、 `storage.enable-ttl`のデフォルトが`false`になるため、競合します。
        -   API V2 が有効になっている場合、古いデータを再利用するには、少なくとも 1 つの tidb-server インスタンスをデプロイする必要があります。この tidb-server インスタンスは、読み取りサービスと書き込みサービスを同時に提供できます。高可用性を確保するために、複数の tidb-server インスタンスをデプロイできます。
        -   API V2 にはクライアントのサポートが必要です。詳細については、API V2 のクライアントの対応する命令を参照してください。
        -   v6.2.0 以降、RawKV の変更データ キャプチャ (CDC) がサポートされています。 [RawKV CDC](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc)を参照してください。
-   デフォルト値: `1`

> **警告：**

> -   API V1 と API V2 はstorage形式が異なります。 TiKV に TiDB データのみが含まれている場合に**のみ**、API V2 を直接有効または無効にできます。他のシナリオでは、新しいクラスターをデプロイし、 [RawKV のバックアップと復元](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)使用してデータを移行する必要があります。
> -   API V2 を有効にした後は、TiKV クラスターを v6.1.0 より前のバージョンにダウングレードする**ことはできません**。そうしないと、データが破損する可能性があります。

## storageのブロックキャッシュ {#storage-block-cache}

複数の RocksDB カラム Families (CF) 間でのブロックキャッシュの共有に関連するコンフィグレーションアイテム。

### <code>capacity</code> {#code-capacity-code}

-   共有ブロックキャッシュのサイズ。
-   デフォルト値: 総システムメモリサイズの 45%
-   単位: KB|MB|GB

## storageとフロー制御 {#storage-flow-control}

TiKVのフロー制御機構に関するコンフィグレーション項目。このメカニズムは、RocksDB の書き込み停止メカニズムを置き換え、スケジューラーレイヤーでフローを制御します。これにより、スタックしたRaftstoreまたはアプライ スレッドによって引き起こされる二次災害が回避されます。

### <code>enable</code> {#code-enable-code}

-   フロー制御メカニズムを有効にするかどうかを決定します。 TiKV を有効にすると、KvDB の書き込み停止メカニズムと RaftDB の書き込み停止メカニズム (memtable を除く) が自動的に無効になります。
-   デフォルト値: `true`

### <code>memtables-threshold</code> {#code-memtables-threshold-code}

-   kvDB memtable の数がこのしきい値に達すると、フロー制御メカニズムが動作し始めます。 `enable`が`true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).max-write-buffer-number`をオーバーライドします。
-   デフォルト値: `5`

### <code>l0-files-threshold</code> {#code-l0-files-threshold-code}

-   kvDB L0 ファイルの数がこのしきい値に達すると、フロー制御メカニズムが動作し始めます。 `enable`が`true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).level0-slowdown-writes-trigger`をオーバーライドします。
-   デフォルト値: `20`

### <code>soft-pending-compaction-bytes-limit</code> {#code-soft-pending-compaction-bytes-limit-code}

-   KvDB 内の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムが一部の書き込みリクエストの拒否を開始し、 `ServerIsBusy`エラーを報告します。 `enable`が`true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).soft-pending-compaction-bytes-limit`をオーバーライドします。
-   デフォルト値: `"192GB"`

### <code>hard-pending-compaction-bytes-limit</code> {#code-hard-pending-compaction-bytes-limit-code}

-   KvDB 内の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムはすべての書き込みリクエストを拒否し、 `ServerIsBusy`エラーを報告します。 `enable`が`true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`をオーバーライドします。
-   デフォルト値: `"1024GB"`

## storageの.io-rate-limit {#storage-io-rate-limit}

I/Oレートリミッタに関するコンフィグレーション項目。

### <code>max-bytes-per-sec</code> {#code-max-bytes-per-sec-code}

-   サーバーが1 秒間にディスクに書き込みまたはディスクから読み取ることができる最大 I/O バイト (以下の`mode`の構成項目によって決定) を制限します。この制限に達すると、TiKV はフォアグラウンド操作よりもバックグラウンド操作のスロットリングを優先します。この構成項目の値は、ディスクの最適な I/O 帯域幅 (たとえば、クラウド ディスク ベンダーによって指定された最大 I/O 帯域幅) に設定する必要があります。この構成値をゼロに設定すると、ディスク I/O 操作は制限されません。
-   デフォルト値: `"0MB"`

### <code>mode</code> {#code-mode-code}

-   どのタイプの I/O 操作をカウントし、しきい値`max-bytes-per-sec`未満に制限するかを決定します。現在、書き込み専用モードのみがサポートされています。
-   値のオプション: `"read-only"` 、 `"write-only"` 、および`"all-io"`
-   デフォルト値: `"write-only"`

## PD {#pd}

### <code>endpoints</code> {#code-endpoints-code}

-   PD のエンドポイント。複数のエンドポイントを指定する場合は、カンマで区切る必要があります。
-   デフォルト値: `["127.0.0.1:2379"]`

### <code>retry-interval</code> {#code-retry-interval-code}

-   PD接続の初期化をリトライする間隔
-   デフォルト値: `"300ms"`

### <code>retry-log-every</code> {#code-retry-log-every-code}

-   PD クライアントがエラーを観察したときに、エラーの報告をスキップする頻度を指定します。たとえば、値が`5`の場合、PD クライアントはエラーを観察した後、4 回ごとにエラーの報告をスキップし、5 回ごとにエラーを報告します。
-   この機能を無効にするには、値を`1`に設定します。
-   デフォルト値: `10`

### <code>retry-max-count</code> {#code-retry-max-count-code}

-   PD接続の初期化をリトライする最大回数
-   再試行を無効にするには、その値を`0`に設定します。再試行回数の制限を解除するには、値を`-1`に設定します。
-   デフォルト値: `-1`

## ラフトストア {#raftstore}

Raftstoreに関連するコンフィグレーション項目。

### <code>prevote</code> {#code-prevote-code}

-   `prevote`を有効または無効にします。この機能を有効にすると、ネットワーク分割から回復した後のシステムのジッターを軽減できます。
-   デフォルト値: `true`

### <code>capacity</code> {#code-capacity-code}

-   storage容量。データを保存できる最大サイズです。 `capacity`を指定しない場合は、現在のディスクの容量が優先されます。複数の TiKV インスタンスを同じ物理ディスクにデプロイするには、このパラメータを TiKV 構成に追加します。詳細は[ハイブリッド展開の主要なパラメータ](/hybrid-deployment-topology.md#key-parameters)を参照してください。
-   デフォルト値: `0`
-   単位: KB|MB|GB

### <code>raftdb-path</code> {#code-raftdb-path-code}

-   Raftライブラリへのパス (デフォルトでは`storage.data-dir/raft`
-   デフォルト値: `""`

### <code>raft-base-tick-interval</code> {#code-raft-base-tick-interval-code}

> **注記：**
>
> この構成項目は SQL ステートメントを介してクエリすることはできませんが、構成ファイルで構成することができます。

-   Raftステート マシンが動作する時間間隔
-   デフォルト値: `"1s"`
-   最小値: `0`より大きい

### <code>raft-heartbeat-ticks</code> {#code-raft-heartbeat-ticks-code}

> **注記：**
>
> この構成項目は SQL ステートメントを介してクエリすることはできませんが、構成ファイルで構成することができます。

-   ハートビートの送信時に通過したティック数。これは、ハートビートが`raft-base-tick-interval` * `raft-heartbeat-ticks`の時間間隔で送信されることを意味します。
-   デフォルト値: `2`
-   最小値: `0`より大きい

### <code>raft-election-timeout-ticks</code> {#code-raft-election-timeout-ticks-code}

> **注記：**
>
> この構成項目は SQL ステートメントを介してクエリすることはできませんが、構成ファイルで構成することができます。

-   Raft の選択が開始されたときに渡されたティックの数。これは、 Raftグループにリーダーがいない場合、約`raft-base-tick-interval` * `raft-election-timeout-ticks`の時間間隔の後にリーダーの選挙が開始されることを意味します。
-   デフォルト値: `10`
-   最小値: `raft-heartbeat-ticks`

### <code>raft-min-election-timeout-ticks</code> {#code-raft-min-election-timeout-ticks-code}

> **注記：**
>
> この構成項目は SQL ステートメントを介してクエリすることはできませんが、構成ファイルで構成することができます。

-   Raft選挙が開始される間の最小ティック数。数値が`0`の場合、値`raft-election-timeout-ticks`が使用されます。このパラメータの値は`raft-election-timeout-ticks`以上である必要があります。
-   デフォルト値: `0`
-   最小値: `0`

### <code>raft-max-election-timeout-ticks</code> {#code-raft-max-election-timeout-ticks-code}

> **注記：**
>
> この構成項目は SQL ステートメントを介してクエリすることはできませんが、構成ファイルで構成することができます。

-   Raft選挙が開始される最大ティック数。数値が`0`の場合、 `raft-election-timeout-ticks` * `2`の値が使用されます。
-   デフォルト値: `0`
-   最小値: `0`

### <code>raft-max-size-per-msg</code> {#code-raft-max-size-per-msg-code}

> **注記：**
>
> この構成項目は SQL ステートメントを介してクエリすることはできませんが、構成ファイルで構成することができます。

-   単一メッセージ パケットのサイズに対するソフト制限
-   デフォルト値: `"1MB"`
-   最小値: `0`より大きい
-   最大値： `3GB`
-   単位: KB|MB|GB

### <code>raft-max-inflight-msgs</code> {#code-raft-max-inflight-msgs-code}

> **注記：**
>
> この構成項目は SQL ステートメントを介してクエリすることはできませんが、構成ファイルで構成することができます。

-   確認するRaft丸太の数。この数値を超えると、 Raftステート マシンのログ送信が遅くなります。
-   デフォルト値: `256`
-   最小値: `0`より大きい
-   最大値： `16384`

### <code>raft-entry-max-size</code> {#code-raft-entry-max-size-code}

-   単一ログの最大サイズのハード制限
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

-   Raftの残存丸太の最大許容数のソフトリミット
-   デフォルト値: `50`
-   最小値: `1`

### <code>raft-log-gc-count-limit</code> {#code-raft-log-gc-count-limit-code}

-   Raftの残存丸太の許容数のハードリミット
-   デフォルト値: 3/4リージョンサイズに収容できるログ数 (各ログあたり 1MB として計算)
-   最小値: `0`

### <code>raft-log-gc-size-limit</code> {#code-raft-log-gc-size-limit-code}

-   Raft の残存丸太の許容サイズに対する厳しい制限
-   デフォルト値:リージョンサイズの 3/4
-   最小値: `0`より大きい

### <code>raft-log-reserve-max-ticks</code> <span class="version-mark">v5.3 の新機能</span> {#code-raft-log-reserve-max-ticks-code-span-class-version-mark-new-in-v5-3-span}

-   この構成項目で設定されたティック数が経過した後、残りのRaftログの数が`raft-log-gc-threshold`で設定された値に達していない場合でも、TiKV はこれらのログに対してガベージコレクション(GC) を実行します。
-   デフォルト値: `6`
-   最小値: `0`より大きい

### <code>raft-engine-purge-interval</code> {#code-raft-engine-purge-interval-code}

-   ディスク領域をできるだけ早くリサイクルするために、古い TiKV ログ ファイルをパージする間隔。 Raftエンジンは交換可能なコンポーネントであるため、実装によってはパージ プロセスが必要です。
-   デフォルト値: `"10s"`

### <code>raft-entry-cache-life-time</code> {#code-raft-entry-cache-life-time-code}

-   メモリ内のログ キャッシュに許可される最大残り時間
-   デフォルト値: `"30s"`
-   最小値: `0`

### <code>hibernate-regions</code> {#code-hibernate-regions-code}

-   Hibernateリージョンを有効または無効にします。このオプションを有効にすると、長時間アイドル状態のリージョンは自動的に休止状態に設定されます。これにより、アイドル状態のリージョンのRaftリーダーとフォロワーの間のハートビートメッセージによって生じる余分なオーバーヘッドが削減されます。 `peer-stale-state-check-interval`を使用すると、休止状態のリージョンのリーダーとフォロワー間のハートビート間隔を変更できます。
-   デフォルト値: v5.0.2 以降のバージョンでは`true` 。 v5.0.2 より前のバージョンでは`false`

### <code>split-region-check-tick-interval</code> {#code-split-region-check-tick-interval-code}

-   リージョン分割が必要かどうかを確認する間隔を指定します。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"10s"`
-   最小値: `0`

### <code>region-split-check-diff</code> {#code-region-split-check-diff-code}

-   リージョン分割前にリージョンデータが超えることが許可される最大値
-   デフォルト値:リージョンサイズの 1/16。
-   最小値: `0`

### <code>region-compact-check-interval</code> {#code-region-compact-check-interval-code}

-   RocksDB の圧縮を手動でトリガーする必要があるかどうかを確認する時間間隔。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"5m"`
-   最小値: `0`

### <code>region-compact-check-step</code> {#code-region-compact-check-step-code}

-   手動圧縮の各ラウンドで一度にチェックされるリージョンの数
-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値は`100`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`5`です。
-   最小値: `0`

### <code>region-compact-min-tombstones</code> {#code-region-compact-min-tombstones-code}

-   RocksDB の圧縮をトリガーするために必要なトゥームストーンの数
-   デフォルト値: `10000`
-   最小値: `0`

### <code>region-compact-tombstones-percent</code> {#code-region-compact-tombstones-percent-code}

-   RocksDB の圧縮をトリガーするために必要なトゥームストーンの割合
-   デフォルト値: `30`
-   最小値: `1`
-   最大値： `100`

### <code>region-compact-min-redundant-rows</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-region-compact-min-redundant-rows-code-span-class-version-mark-new-in-v7-1-0-span}

-   RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の数。この設定は、Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) に対してのみ有効です。
-   デフォルト値: `50000`
-   最小値: `0`

### <code>region-compact-redundant-rows-percent</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-region-compact-redundant-rows-percent-code-span-class-version-mark-new-in-v7-1-0-span}

-   RocksDB 圧縮をトリガーするために必要な冗長 MVCC 行の割合。この設定は、Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) に対してのみ有効です。
-   デフォルト値: `20`
-   最小値: `1`
-   最大値： `100`

### <code>report-region-buckets-tick-interval</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-report-region-buckets-tick-interval-code-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> `report-region-buckets-tick-interval`は、TiDB v6.1.0 で導入された実験的機能です。本番環境で使用することはお勧めできません。

-   `enable-region-bucket`が true の場合、TiKV がバケット情報を PD に報告する間隔。
-   デフォルト値: `10s`

### <code>pd-heartbeat-tick-interval</code> {#code-pd-heartbeat-tick-interval-code}

-   リージョンの PD へのハートビートがトリガーされる時間間隔。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"1m"`
-   最小値: `0`

### <code>pd-store-heartbeat-tick-interval</code> {#code-pd-store-heartbeat-tick-interval-code}

-   ストアの PD へのハートビートがトリガーされる時間間隔。 `0` 、この機能が無効であることを意味します。
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

-   `snap-generator`スレッド プールのサイズを設定します。
-   リカバリ シナリオで TiKV でリージョンがスナップショットをより速く生成できるようにするには、対応するワーカーの`snap-generator`スレッドの数を増やす必要があります。この構成アイテムを使用して、 `snap-generator`スレッド プールのサイズを増やすことができます。
-   デフォルト値: `2`
-   最小値: `1`

### <code>lock-cf-compact-interval</code> {#code-lock-cf-compact-interval-code}

-   TiKV がロックカラムファミリーの手動圧縮をトリガーする時間間隔
-   デフォルト値: `"10m"`
-   最小値: `0`

### <code>lock-cf-compact-bytes-threshold</code> {#code-lock-cf-compact-bytes-threshold-code}

-   TiKV がロックカラムファミリーの手動圧縮をトリガーするサイズ
-   デフォルト値: `"256MB"`
-   最小値: `0`
-   単位：MB

### <code>notify-capacity</code> {#code-notify-capacity-code}

-   リージョンメッセージキューの最長の長さ。
-   デフォルト値: `40960`
-   最小値: `0`

### <code>messages-per-tick</code> {#code-messages-per-tick-code}

-   バッチごとに処理されるメッセージの最大数
-   デフォルト値: `4096`
-   最小値: `0`

### <code>max-peer-down-duration</code> {#code-max-peer-down-duration-code}

-   ピアに許可される非アクティブ期間の最長。タイムアウトのあるピアは`down`としてマークされ、PD は後でそのピアを削除しようとします。
-   デフォルト値: `"10m"`
-   最小値: ハイバネートリージョンが有効な場合、最小値は`peer-stale-state-check-interval * 2`です。 Hibernateリージョンが無効な場合、最小値は`0`です。

### <code>max-leader-missing-duration</code> {#code-max-leader-missing-duration-code}

-   Raftグループにリーダーがいない状態にピアが存在できる最長期間。この値を超えると、ピアは PD でピアが削除されたかどうかを確認します。
-   デフォルト値: `"2h"`
-   最小値: `abnormal-leader-missing-duration`より大きい

### <code>abnormal-leader-missing-duration</code> {#code-abnormal-leader-missing-duration-code}

-   Raftグループにリーダーがいない状態にピアが存在できる最長期間。この値を超えると、ピアは異常とみなされ、メトリクスとログにマークが付けられます。
-   デフォルト値: `"10m"`
-   最小値: `peer-stale-state-check-interval`より大きい

### <code>peer-stale-state-check-interval</code> {#code-peer-stale-state-check-interval-code}

-   Raftグループにリーダーがいない状態にピアがあるかどうかのチェックをトリガーする時間間隔。
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

-   インポートされたスナップショット ファイルをディスクに書き込むときに必要なメモリキャッシュ サイズ
-   デフォルト値: `"10MB"`
-   最小値: `0`
-   単位：MB

### <code>consistency-check-interval</code> {#code-consistency-check-interval-code}

> **警告：**
>
> 本番環境で一貫性チェックを有効にすることはお勧め**できません**。これは、クラスタのパフォーマンスに影響を与え、TiDB のガベージコレクションと互換性がないからです。

-   整合性チェックがトリガーされる時間間隔。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"0s"`
-   最小値: `0`

### <code>raft-store-max-leader-lease</code> {#code-raft-store-max-leader-lease-code}

-   Raftのリーダーとして最も長く信頼されていた期間
-   デフォルト値: `"9s"`
-   最小値: `0`

### <code>right-derive-when-split</code> {#code-right-derive-when-split-code}

-   リージョン分割時の新しいリージョンの開始キーを指定します。この設定項目が`true`に設定されている場合、開始キーは最大の分割キーになります。この設定項目が`false`に設定されている場合、開始キーは元のリージョンの開始キーになります。
-   デフォルト値: `true`

### <code>merge-max-log-gap</code> {#code-merge-max-log-gap-code}

-   `merge`を実行した場合に許容される欠落ログの最大数
-   デフォルト値: `10`
-   最小値: `raft-log-gc-count-limit`より大きい

### <code>merge-check-tick-interval</code> {#code-merge-check-tick-interval-code}

-   TiKV がリージョンをマージする必要があるかどうかをチェックする時間間隔
-   デフォルト値: `"2s"`
-   最小値: `0`より大きい

### <code>use-delete-range</code> {#code-use-delete-range-code}

-   `rocksdb delete_range`インターフェイスからデータを削除するかどうかを決定します
-   デフォルト値: `false`

### <code>cleanup-import-sst-interval</code> {#code-cleanup-import-sst-interval-code}

-   期限切れの SST ファイルをチェックする時間間隔。 `0` 、この機能が無効であることを意味します。
-   デフォルト値: `"10m"`
-   最小値: `0`

### <code>local-read-batch-size</code> {#code-local-read-batch-size-code}

-   1 回のバッチで処理される読み取りリクエストの最大数
-   デフォルト値: `1024`
-   最小値: `0`より大きい

### <code>apply-yield-write-size</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-apply-yield-write-size-code-span-class-version-mark-new-in-v6-4-0-span}

-   適用スレッドがポーリングの 1 ラウンドで 1 つの FSM (有限状態マシン) に対して書き込むことができる最大バイト数。これはソフトリミットです。
-   デフォルト値: `"32KiB"`
-   最小値: `0`より大きい
-   単位: KiB|MiB|GiB

### <code>apply-max-batch-size</code> {#code-apply-max-batch-size-code}

-   Raftステート マシンは、BatchSystem によってデータ書き込みリクエストをバッチで処理します。この設定項目は、1 つのバッチでリクエストを処理できるRaftステート マシンの最大数を指定します。
-   デフォルト値: `256`
-   最小値: `0`より大きい
-   最大値： `10240`

### <code>apply-pool-size</code> {#code-apply-pool-size-code}

-   データをディスクにフラッシュするプール内のスレッドの許容数。これは、適用スレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `2`
-   値の範囲: `[1, CPU * 10]` 。 `CPU` CPU コアの数を意味します。

### <code>store-max-batch-size</code> {#code-store-max-batch-size-code}

-   Raftステート マシンは、BatchSystem によってバッチでディスクにログをフラッシュするリクエストを処理します。この設定項目は、1 つのバッチでリクエストを処理できるRaftステート マシンの最大数を指定します。
-   `hibernate-regions`が有効な場合、デフォルト値は`256`です。 `hibernate-regions`が無効になっている場合、デフォルト値は`1024`です。
-   最小値: `0`より大きい
-   最大値： `10240`

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

-   リクエストのバッチ処理を有効にするかどうかを制御します。これを有効にすると、書き込みパフォーマンスが大幅に向上します。
-   デフォルト値: `true`

### <code>inspect-interval</code> {#code-inspect-interval-code}

-   TiKV は、特定の間隔でRaftstoreコンポーネントのレイテンシーを検査します。このパラメータは検査の間隔を指定します。レイテンシーがこの値を超える場合、この検査はタイムアウトとしてマークされます。
-   タイムアウト検査の割合に基づいて、TiKVノードが遅いかどうかを判断します。
-   デフォルト値: `"500ms"`
-   最小値: `"1ms"`

### <code>raft-write-size-limit</code> <span class="version-mark">v5.3.0 の新機能</span> {#code-raft-write-size-limit-code-span-class-version-mark-new-in-v5-3-0-span}

-   Raftデータがディスクに書き込まれるしきい値を決定します。データサイズがこの設定項目の値より大きい場合、データはディスクに書き込まれます。 `store-io-pool-size`の値が`0`の場合、この構成項目は有効になりません。
-   デフォルト値: `1MB`
-   最小値: `0`

### <code>report-min-resolved-ts-interval</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-report-min-resolved-ts-interval-code-span-class-version-mark-new-in-v6-0-0-span}

-   最小解決タイムスタンプが PD リーダーに報告される間隔を決定します。この値が`0`に設定されている場合、レポートが無効になっていることを意味します。
-   デフォルト値: v6.3.0 より前のデフォルト値は`"0s"`です。 v6.3.0 以降、デフォルト値は`"1s"`で、これは正の最小値です。
-   最小値: `0`
-   単位：秒

## コプロセッサ {#coprocessor}

コプロセッサーに関するコンフィグレーション項目。

### <code>split-region-on-table</code> {#code-split-region-on-table-code}

-   リージョンをテーブルごとに分割するかどうかを決定します。この機能は TiDB モードでのみ使用することをお勧めします。
-   デフォルト値: `false`

### <code>batch-split-limit</code> {#code-batch-split-limit-code}

-   バッチに分割されるリージョンのしきい値。この値を増やすと、リージョン分割が高速化されます。
-   デフォルト値: `10`
-   最小値: `1`

### <code>region-max-size</code> {#code-region-max-size-code}

-   リージョンの最大サイズ。この値を超えると、リージョンが多数に分割されます。
-   デフォルト値: `region-split-size / 2 * 3`
-   単位: KiB|MiB|GiB

### <code>region-split-size</code> {#code-region-split-size-code}

-   新しく分割されたリージョンのサイズ。この値は推定値です。
-   デフォルト値: `"96MiB"`
-   単位: KiB|MiB|GiB

### <code>region-max-keys</code> {#code-region-max-keys-code}

-   リージョン内のキーの最大許容数。この値を超えると、リージョンが多数に分割されます。
-   デフォルト値: `region-split-keys / 2 * 3`

### <code>region-split-keys</code> {#code-region-split-keys-code}

-   新しく分割されたリージョン内のキーの数。この値は推定値です。
-   デフォルト値: `960000`

### <code>consistency-check-method</code> {#code-consistency-check-method-code}

-   データの整合性チェックの方法を指定します
-   MVCC データの整合性チェックの場合、値を`"mvcc"`に設定します。生データの整合性チェックの場合は、値を`"raw"`に設定します。
-   デフォルト値: `"mvcc"`

## コプロセッサーv2 {#coprocessor-v2}

### <code>coprocessor-plugin-directory</code> {#code-coprocessor-plugin-directory-code}

-   コンパイルされたコプロセッサ プラグインが配置されるディレクトリのパス。このディレクトリ内のプラグインは、TiKV によって自動的にロードされます。
-   この設定項目が設定されていない場合、コプロセッサ プラグインは無効になります。
-   デフォルト値: `"./coprocessors"`

### <code>enable-region-bucket</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-enable-region-bucket-code-span-class-version-mark-new-in-v6-1-0-span}

-   リージョンをバケットと呼ばれる小さな範囲に分割するかどうかを決定します。バケットは、スキャンの同時実行性を向上させるために同時クエリの単位として使用されます。バケットの設計の詳細については、 [動的サイズリージョン](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md)を参照してください。
-   デフォルト値: false

> **警告：**
>
> -   `enable-region-bucket`は、TiDB v6.1.0 で導入された実験的機能です。本番環境で使用することはお勧めできません。
> -   この構成は、 `region-split-size`が`region-bucket-size`の 2 倍以上の場合にのみ意味を持ちます。それ以外の場合、バケットは実際には生成されません。
> -   `region-split-size`をより大きな値に調整すると、パフォーマンスが低下し、スケジュールが遅くなるリスクがある可能性があります。

### <code>region-bucket-size</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-region-bucket-size-code-span-class-version-mark-new-in-v6-1-0-span}

-   `enable-region-bucket`が true の場合のバケットのサイズ。
-   デフォルト値: `96MiB`

> **警告：**
>
> `region-bucket-size`は、TiDB v6.1.0 で導入された実験的機能です。本番環境で使用することはお勧めできません。

## ロックスデータベース {#rocksdb}

RocksDBに関するコンフィグレーション項目

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDB のバックグラウンド スレッドの数。 RocksDB スレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値:
    -   CPU コア数が 10 の場合、デフォルト値は`9`です。
    -   CPU コアの数が 8 の場合、デフォルト値は`7`です。
    -   CPU コア数が`N`の場合、デフォルト値は`max(2, min(N - 1, 9))`です。
-   最小値: `2`

### <code>max-background-flushes</code> {#code-max-background-flushes-code}

-   同時バックグラウンド memtable フラッシュ ジョブの最大数
-   デフォルト値:
    -   CPU コア数が 10 の場合、デフォルト値は`3`です。
    -   CPU コアの数が 8 の場合、デフォルト値は`2`です。
    -   CPU コア数が`N`の場合、デフォルト値は`[(max-background-jobs + 3) / 4]`です。
-   最小値: `1`

### <code>max-sub-compactions</code> {#code-max-sub-compactions-code}

-   RocksDB で同時に実行されるサブコンパクション操作の数
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
-   単位: B|KB|MB|GB

### <code>create-if-missing</code> {#code-create-if-missing-code}

-   DBスイッチを自動的に作成するかどうかを決定します。
-   デフォルト値: `true`

### <code>wal-recovery-mode</code> {#code-wal-recovery-mode-code}

-   WALリカバリモード
-   オプションの値:
    -   `"tolerate-corrupted-tail-records"` : すべてのログ上で不完全な末尾データを持つレコードを許容し、破棄します。
    -   `"absolute-consistency"` : 破損したログが見つかった場合、回復を中止します。
    -   `"point-in-time"` : 最初の破損したログが見つかるまで、ログを順番に回復します。
    -   `"skip-any-corrupted-records"` : 災害後の回復。データは可能な限り復元され、破損したレコードはスキップされます。
-   デフォルト値: `"point-in-time"`

### <code>wal-dir</code> {#code-wal-dir-code}

-   WALファイルが保存されているディレクトリ
-   デフォルト値: `"/tmp/tikv/store"`

### <code>wal-ttl-seconds</code> {#code-wal-ttl-seconds-code}

-   アーカイブされた WAL ファイルの生存時間。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位：秒

### <code>wal-size-limit</code> {#code-wal-size-limit-code}

-   アーカイブされた WAL ファイルのサイズ制限。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>max-total-wal-size</code> {#code-max-total-wal-size-code}

-   RocksDB WAL の合計最大サイズ。これは、 `data-dir`のファイル内の`*.log`のファイルのサイズです。
-   デフォルト値: `"4GB"`

### <code>stats-dump-period</code> {#code-stats-dump-period-code}

-   統計情報がログに出力される間隔。
-   デフォルト値: `10m`

### <code>compaction-readahead-size</code> {#code-compaction-readahead-size-code}

-   RocksDB の圧縮中に先読み機能を有効にし、先読みデータのサイズを指定します。メカニカル ディスクを使用している場合は、値を少なくとも 2MB に設定することをお勧めします。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>writable-file-max-buffer-size</code> {#code-writable-file-max-buffer-size-code}

-   WritableFileWrite で使用される最大バッファ サイズ
-   デフォルト値: `"1MB"`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>use-direct-io-for-flush-and-compaction</code> {#code-use-direct-io-for-flush-and-compaction-code}

-   バックグラウンドのフラッシュと圧縮での読み取りと書き込みの両方に`O_DIRECT`を使用するかどうかを決定します。このオプションのパフォーマンスへの影響: `O_DIRECT`バイパスを有効にすると、OS バッファ キャッシュの汚染が防止されますが、後続のファイルの読み取りでは、バッファ キャッシュへの内容の再読み取りが必要になります。
-   デフォルト値: `false`

### <code>rate-bytes-per-sec</code> {#code-rate-bytes-per-sec-code}

-   RocksDB の圧縮レート リミッターによって許可される最大レート
-   デフォルト値: `10GB`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>rate-limiter-refill-period</code> {#code-rate-limiter-refill-period-code}

-   I/O トークンが補充される頻度を制御します。値を小さくすると、I/O バーストは減少しますが、CPU オーバーヘッドが増加します。
-   デフォルト値: `"100ms"`

### <code>rate-limiter-mode</code> {#code-rate-limiter-mode-code}

-   RocksDB の圧縮レート リミッター モード
-   `"all-io"` `"write-only"`値: `"read-only"`
-   デフォルト値: `"write-only"`

### <code>rate-limiter-auto-tuned</code> <span class="version-mark">v5.0 の新機能</span> {#code-rate-limiter-auto-tuned-code-span-class-version-mark-new-in-v5-0-span}

-   最近のワークロードに基づいて RocksDB の圧縮レート リミッターの構成を自動的に最適化するかどうかを決定します。この構成を有効にすると、圧縮保留中のバイト数が通常よりわずかに多くなります。
-   デフォルト値: `true`

### <code>enable-pipelined-write</code> {#code-enable-pipelined-write-code}

-   パイプライン書き込みを有効にするかどうかを制御します。この構成が有効な場合、以前のパイプライン書き込みが使用されます。この設定を無効にすると、新しいパイプライン コミット メカニズムが使用されます。
-   デフォルト値: `false`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   ファイルが非同期で書き込まれている間に、OS がファイルをディスクに増分同期する速度。
-   デフォルト値: `"1MB"`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>wal-bytes-per-sync</code> {#code-wal-bytes-per-sync-code}

-   WAL ファイルの書き込み中に OS が WAL ファイルをディスクに増分同期する速度
-   デフォルト値: `"512KB"`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>info-log-max-size</code> {#code-info-log-max-size-code}

-   情報ログの最大サイズ
-   デフォルト値: `"1GB"`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>info-log-roll-time</code> {#code-info-log-roll-time-code}

-   情報ログが切り詰められる時間間隔。値が`0s`の場合、ログは切り捨てられません。
-   デフォルト値: `"0s"`

### <code>info-log-keep-log-file-num</code> {#code-info-log-keep-log-file-num-code}

-   保存されるログ ファイルの最大数
-   デフォルト値: `10`
-   最小値: `0`

### <code>info-log-dir</code> {#code-info-log-dir-code}

-   ログが保存されるディレクトリ
-   デフォルト値: `""`

### <code>info-log-level</code> {#code-info-log-level-code}

-   RocksDB のログレベル
-   デフォルト値: `"info"`

### <code>write-buffer-flush-oldest-first</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-write-buffer-flush-oldest-first-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   現在の RocksDB の`memtable`のメモリ使用量がしきい値に達したときに使用されるフラッシュ戦略を指定します。
-   デフォルト値: `false`
-   値のオプション:

    -   データ量が最も大きい`false` : `memtable`が SST ファイルにフラッシュされます。
    -   `true` : 最も古い`memtable` SST ファイルにフラッシュされます。この戦略はコールド データの`memtable`クリアできるため、コールド データとホット データが明らかなシナリオに適しています。

### <code>write-buffer-limit</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-write-buffer-limit-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   単一の TiKV 内のすべての RocksDB インスタンスの合計メモリ制限を`memtable`に指定します。デフォルト値はマシンのメモリの 25% です。少なくとも 5 GiB のメモリを構成することをお勧めします。この設定は、Partitioned Raft KV ( `storage.engine` = `"partitioned-raft-kv"` ) に対してのみ有効です。
-   デフォルト値: 25%
-   単位: KiB|MiB|GiB

## ロックスデータベースタイタン {#rocksdb-titan}

タイタン関連のコンフィグレーション項目。

### <code>enabled</code> {#code-enabled-code}

-   Titan を有効または無効にします
-   デフォルト値: `false`

### <code>dirname</code> {#code-dirname-code}

-   Titan Blob ファイルが保存されているディレクトリ
-   デフォルト値: `"titandb"`

### <code>disable-gc</code> {#code-disable-gc-code}

-   Titan が Blob ファイルに対して実行するガベージ コレクション (GC) を無効にするかどうかを決定します
-   デフォルト値: `false`

### <code>max-background-gc</code> {#code-max-background-gc-code}

-   Titan の GC スレッドの最大数
-   デフォルト値: `4`
-   最小値: `1`

## ロックスデータベース.defaultcf |ロックスデータベースロックスデータベース.lockcf {#rocksdb-defaultcf-rocksdb-writecf-rocksdb-lockcf}

`rocksdb.defaultcf` 、 `rocksdb.writecf` 、 `rocksdb.lockcf`に関するコンフィグレーション項目。

### <code>block-size</code> {#code-block-size-code}

-   RocksDB ブロックのデフォルトのサイズ
-   `defaultcf`と`writecf`のデフォルト値: `"32KB"`
-   `lockcf`のデフォルト値: `"16KB"`
-   最小値: `"1KB"`
-   単位: KB|MB|GB

### <code>block-cache-size</code> {#code-block-cache-size-code}

> **警告：**
>
> v6.6.0 以降、この構成は非推奨になります。

-   RocksDB ブロックのキャッシュ サイズ。
-   `defaultcf`のデフォルト値: `Total machine memory * 25%`
-   `writecf`のデフォルト値: `Total machine memory * 15%`
-   `lockcf`のデフォルト値: `Total machine memory * 2%`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>disable-block-cache</code> {#code-disable-block-cache-code}

-   ブロックキャッシュを有効または無効にします
-   デフォルト値: `false`

### <code>cache-index-and-filter-blocks</code> {#code-cache-index-and-filter-blocks-code}

-   キャッシュインデックスとフィルターを有効または無効にします。
-   デフォルト値: `true`

### <code>pin-l0-filter-and-index-blocks</code> {#code-pin-l0-filter-and-index-blocks-code}

-   レベル 0 SST ファイルのインデックス ブロックとフィルター ブロックをメモリに固定するかどうかを決定します。
-   デフォルト値: `true`

### <code>use-bloom-filter</code> {#code-use-bloom-filter-code}

-   ブルームフィルターを有効または無効にします
-   デフォルト値: `true`

### <code>optimize-filters-for-hits</code> {#code-optimize-filters-for-hits-code}

-   フィルターのヒット率を最適化するかどうかを決定します。
-   `defaultcf`のデフォルト値: `true`
-   `writecf`と`lockcf`のデフォルト値: `false`

### <code>whole-key-filtering</code> {#code-whole-key-filtering-code}

-   キー全体をブルームフィルターに入れるかどうかを決定します
-   `defaultcf`と`lockcf`のデフォルト値: `true`
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
-   `lockcf`のデフォルト値: [&quot;いいえ&quot;、&quot;いいえ&quot;、&quot;いいえ&quot;、&quot;いいえ&quot;、&quot;いいえ&quot;、&quot;いいえ&quot;、&quot;いいえ&quot;]

### <code>bottommost-level-compression</code> {#code-bottommost-level-compression-code}

-   最レイヤーの圧縮アルゴリズムを設定します。この構成項目は`compression-per-level`設定をオーバーライドします。
-   データが LSM ツリーに書き込まれて以来、RocksDB は最レイヤーの`compression-per-level`配列で指定された最後の圧縮アルゴリズムを直接採用しません。 `bottommost-level-compression`により、最レイヤーは最初から最適な圧縮効果の圧縮アルゴリズムを使用できるようになります。
-   最レイヤーの圧縮アルゴリズムを設定したくない場合は、この設定項目の値を`disable`に設定します。
-   デフォルト値: `"zstd"`

### <code>write-buffer-size</code> {#code-write-buffer-size-code}

-   メムテーブルのサイズ
-   `defaultcf`と`writecf`のデフォルト値: `"128MB"`
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

-   基本レベル (レベル 1) の最大バイト数。通常、memtable の 4 倍のサイズに設定されます。レベル 1 のデータ サイズが制限値`max-bytes-for-level-base`に達すると、レベル 1 の SST ファイルと、それらに重複するレベル 2 の SST ファイルが圧縮されます。
-   `defaultcf`と`writecf`のデフォルト値: `"512MB"`
-   `lockcf`のデフォルト値: `"128MB"`
-   最小値: `0`
-   単位: KB|MB|GB
-   不必要な圧縮を減らすために、値`max-bytes-for-level-base`を L0 のデータ量とほぼ同じに設定することをお勧めします。たとえば、圧縮方法が「no:no:lz4:lz4:lz4:lz4:lz4」の場合、L0 と L1 には圧縮がなく、L0 の圧縮のトリガー条件は次のとおりであるため、 `max-bytes-for-level-base`の値は`write-buffer-size * 4`になります。 SST ファイルの数が 4 (デフォルト値) に達していることを確認します。 L0 と L1 の両方で圧縮を採用する場合、memtable から圧縮された SST ファイルのサイズを理解するには、RocksDB ログを分析する必要があります。たとえば、ファイル サイズが 32 MB の場合、 `max-bytes-for-level-base` ～ 128 MB の値を設定することをお勧めします ( `32 MB * 4` )。

### <code>target-file-size-base</code> {#code-target-file-size-base-code}

-   基本レベルでのターゲット ファイルのサイズ。 `enable-compaction-guard`値が`true`の場合、この値は`compaction-guard-max-output-file-size`で上書きされます。
-   デフォルト値: `"8MB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>level0-file-num-compaction-trigger</code> {#code-level0-file-num-compaction-trigger-code}

-   圧縮をトリガーする L0 のファイルの最大数
-   `defaultcf`と`writecf`のデフォルト値: `4`
-   `lockcf`のデフォルト値: `1`
-   最小値: `0`

### <code>level0-slowdown-writes-trigger</code> {#code-level0-slowdown-writes-trigger-code}

-   書き込み停止をトリガーする L0 のファイルの最大数。 `storage.flow-control.enable`が`true`に設定されている場合、 `storage.flow-control.l0-files-threshold`この構成項目をオーバーライドします。
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
    -   `"by-compensated-size"` : ファイル サイズの順にファイルを圧縮し、大きなファイルを優先して圧縮します。
    -   `"oldest-largest-seq-first"` : 更新時刻が最も古いファイルの圧縮を優先します。この値は、狭い範囲のホット キーを更新する場合に**のみ**使用してください。
    -   `"oldest-smallest-seq-first"` : 長期間次のレベルに圧縮されない範囲を持つファイルの圧縮を優先します。キー空間全体でホット キーをランダムに更新する場合、この値により書き込み増幅がわずかに減少する可能性があります。
    -   `"min-overlapping-ratio"` : オーバーラップ率が高いファイルの圧縮を優先します。ファイルがさまざまなレベルで小さい場合 ( `the file size in the next level` ÷ `the file size in this level`の結果が小さい場合)、TiKV は最初にこのファイルを圧縮します。多くの場合、この値により書き込み増幅を効果的に削減できます。
-   `defaultcf`と`writecf`のデフォルト値: `"min-overlapping-ratio"`
-   `lockcf`のデフォルト値: `"by-compensated-size"`

### <code>dynamic-level-bytes</code> {#code-dynamic-level-bytes-code}

-   動的レベルバイトを最適化するかどうかを決定します
-   デフォルト値: `true`

### <code>num-levels</code> {#code-num-levels-code}

-   RocksDB ファイル内の最大レベル数
-   デフォルト値: `7`

### <code>max-bytes-for-level-multiplier</code> {#code-max-bytes-for-level-multiplier-code}

-   レイヤーのデフォルトの増幅倍数
-   デフォルト値: `10`

### <code>compaction-style</code> {#code-compaction-style-code}

-   圧縮方法
-   `"fifo"` `"universal"`値: `"level"`
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

-   TiKVリージョン境界で SST ファイルを分割するための最適化であるコンパクション ガードを有効または無効にします。この最適化により、圧縮 I/O が削減され、TiKV がより大きな SST ファイル サイズを使用できるようになり (したがって、全体の SST ファイルが少なくなります)、リージョンの移行時に古いデータを効率的にクリーンアップできるようになります。
-   `defaultcf`と`writecf`のデフォルト値: `true`
-   `lockcf`のデフォルト値: `false`

### <code>compaction-guard-min-output-file-size</code> {#code-compaction-guard-min-output-file-size-code}

-   コンパクション ガードが有効な場合の SST ファイルの最小サイズ。この構成により、コンパクション ガードが有効になっているときに SST ファイルが小さすぎることが防止されます。
-   デフォルト値: `"8MB"`
-   単位: KB|MB|GB

### <code>compaction-guard-max-output-file-size</code> {#code-compaction-guard-max-output-file-size-code}

-   コンパクション ガードが有効な場合の SST ファイルの最大サイズ。この構成により、コンパクション ガードが有効になっているときに SST ファイルが大きくなりすぎることがなくなります。この構成は、同じカラムファミリーの`target-file-size-base`をオーバーライドします。
-   デフォルト値: `"128MB"`
-   単位: KB|MB|GB

### <code>format-version</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-format-version-code-span-class-version-mark-new-in-v6-2-0-span}

-   SST ファイルのフォーマット バージョン。この構成項目は、新しく書き込まれたテーブルにのみ影響します。既存のテーブルの場合、バージョン情報はフッターから読み取られます。
-   オプションの値:
    -   `0` : すべての TiKV バージョンで読み取り可能。デフォルトのチェックサム タイプは CRC32 であり、このバージョンではチェックサム タイプの変更はサポートされていません。
    -   `1` : すべての TiKV バージョンで読み取り可能。 xxHash などのデフォルト以外のチェックサム タイプをサポートします。 RocksDB は、チェックサム タイプが CRC32 でない場合にのみデータを書き込みます。 (バージョン`0`は自動的にアップグレードされます)
    -   `2` : すべての TiKV バージョンで読み取り可能。 LZ4、BZip2、Zlib 圧縮を使用して圧縮ブロックのエンコードを変更します。
    -   `3` : TiKV v2.1 以降のバージョンで読み込むことができます。インデックス ブロック内のキーのエンコーディングを変更します。
    -   `4` : TiKV v3.0 以降のバージョンで読み込むことができます。インデックス ブロック内の値のエンコードを変更します。
    -   `5` : TiKV v6.1 以降のバージョンで読み込むことができます。フル フィルターとパーティション フィルターでは、異なるスキーマを使用した、より高速で正確なブルーム フィルター実装が使用されます。
-   デフォルト値: `2`

### <code>ttl</code> <span class="version-mark">v7.1.2 の新機能</span> {#code-ttl-code-span-class-version-mark-new-in-v7-1-2-span}

-   TTL より古い更新を含む SST ファイルは、圧縮対象として自動的に選択されます。これらの SST ファイルはカスケード方式で圧縮されるため、最下位のレベルまたはファイルに圧縮されます。
-   デフォルト値: `"0s"`は、デフォルトでは SST ファイルが選択されていないことを意味します。
-   単位: s(秒)|h(時)|d(日)

### <code>periodic-compaction-seconds</code> <span class="version-mark">v7.1.2 の新機能</span> {#code-periodic-compaction-seconds-code-span-class-version-mark-new-in-v7-1-2-span}

-   定期的な圧縮の時間間隔。この値より古い更新を含む SST ファイルは圧縮対象として選択され、これらの SST ファイルが元々存在していたレベルと同じレベルに再書き込みされます。
-   -   デフォルト値: `"0s"`は、定期的な圧縮がデフォルトで無効であることを意味します。
-   単位: s(秒)|h(時)|d(日)

## ロックsdb.defaultcf.titan {#rocksdb-defaultcf-titan}

`rocksdb.defaultcf.titan`に関するコンフィグレーション項目。

### <code>min-blob-size</code> {#code-min-blob-size-code}

-   Blob ファイルに保存される最小値。指定されたサイズより小さい値は LSM ツリーに格納されます。
-   デフォルト値: `"1KB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>blob-file-compression</code> {#code-blob-file-compression-code}

-   Blob ファイルで使用される圧縮アルゴリズム
-   オプションの値: `"no"` 、 `"snappy"` 、 `"zlib"` 、 `"bzip2"` 、 `"lz4"` 、 `"lz4hc"` 、 `"zstd"`
-   デフォルト値: `"lz4"`

> **注記：**
>
> Snappy 圧縮ファイルは[公式の Snappy フォーマット](https://github.com/google/snappy)に存在する必要があります。 Snappy 圧縮の他のバリアントはサポートされていません。

### <code>blob-cache-size</code> {#code-blob-cache-size-code}

-   BLOB ファイルのキャッシュ サイズ
-   デフォルト値: `"0GB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>min-gc-batch-size</code> {#code-min-gc-batch-size-code}

-   GC を 1 回実行するために必要な BLOB ファイルの最小合計サイズ
-   デフォルト値: `"16MB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>max-gc-batch-size</code> {#code-max-gc-batch-size-code}

-   1 回の GC 実行に許可される BLOB ファイルの最大合計サイズ
-   デフォルト値: `"64MB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>discardable-ratio</code> {#code-discardable-ratio-code}

-   Blob ファイルに対して GC がトリガーされる比率。 Blob ファイル内の無効な値の割合がこの割合を超えている場合にのみ、Blob ファイルを GC 用に選択できます。
-   デフォルト値: `0.5`
-   最小値: `0`
-   最大値： `1`

### <code>sample-ratio</code> {#code-sample-ratio-code}

-   GC 中にファイルをサンプリングするときの (Blob ファイルから読み取られたデータ/Blob ファイル全体) の比率
-   デフォルト値: `0.1`
-   最小値: `0`
-   最大値： `1`

### <code>merge-small-file-threshold</code> {#code-merge-small-file-threshold-code}

-   Blob ファイルのサイズがこの値より小さい場合でも、Blob ファイルが GC に選択される可能性があります。この場合、 `discardable-ratio`は無視されます。
-   デフォルト値: `"8MB"`
-   最小値: `0`
-   単位: KB|MB|GB

### <code>blob-run-mode</code> {#code-blob-run-mode-code}

-   Titan の実行モードを指定します。
-   オプションの値:
    -   `normal` : 値のサイズが`min-blob-size`を超える場合、データを BLOB ファイルに書き込みます。
    -   `read_only` : BLOB ファイルへの新しいデータの書き込みを拒否しますが、BLOB ファイルから元のデータを読み取ります。
    -   `fallback` : BLOB ファイル内のデータを LSM に書き込みます。
-   デフォルト値: `normal`

### <code>level-merge</code> {#code-level-merge-code}

-   読み取りパフォーマンスを最適化するかどうかを決定します。 `level-merge`を有効にすると、書き込み増幅が増加します。
-   デフォルト値: `false`

## ラフトデータベース {#raftdb}

`raftdb`に関するコンフィグレーション項目

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDB のバックグラウンド スレッドの数。 RocksDB スレッド プールのサイズを変更する場合は、 [TiKV スレッド プールのパフォーマンス チューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `4`
-   最小値: `2`

### <code>max-sub-compactions</code> {#code-max-sub-compactions-code}

-   RocksDB で同時に実行されるサブコンパクション操作の数
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
-   単位: B|KB|MB|GB

### <code>create-if-missing</code> {#code-create-if-missing-code}

-   値が`true`の場合、データベースが存在しない場合にデータベースが作成されます。
-   デフォルト値: `true`

### <code>stats-dump-period</code> {#code-stats-dump-period-code}

-   統計情報をログに出力する間隔
-   デフォルト値: `10m`

### <code>wal-dir</code> {#code-wal-dir-code}

-   Raft RocksDB WAL ファイルが保存されているディレクトリ。これは、WAL の絶対ディレクトリ パスです。この構成項目を[`rocksdb.wal-dir`](#wal-dir)と同じ値に設定し**ないでください**。
-   この設定項目が設定されていない場合、ログファイルはデータと同じディレクトリに保存されます。
-   マシン上に 2 つのディスクがある場合、RocksDB データと WAL ログを別のディスクに保存すると、パフォーマンスが向上する可能性があります。
-   デフォルト値: `""`

### <code>wal-ttl-seconds</code> {#code-wal-ttl-seconds-code}

-   アーカイブされた WAL ファイルを保持する期間を指定します。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位：秒

### <code>wal-size-limit</code> {#code-wal-size-limit-code}

-   アーカイブされた WAL ファイルのサイズ制限。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>max-total-wal-size</code> {#code-max-total-wal-size-code}

-   RocksDB WAL の合計最大サイズ
-   デフォルト値: `"4GB"`

### <code>compaction-readahead-size</code> {#code-compaction-readahead-size-code}

-   RocksDB の圧縮中に先読み機能を有効にするかどうかを制御し、先読みデータのサイズを指定します。
-   メカニカル ディスクを使用する場合は、値を少なくとも`2MB`に設定することをお勧めします。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>writable-file-max-buffer-size</code> {#code-writable-file-max-buffer-size-code}

-   WritableFileWrite で使用される最大バッファ サイズ
-   デフォルト値: `"1MB"`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>use-direct-io-for-flush-and-compaction</code> {#code-use-direct-io-for-flush-and-compaction-code}

-   バックグラウンドのフラッシュと圧縮での読み取りと書き込みの両方に`O_DIRECT`を使用するかどうかを決定します。このオプションのパフォーマンスへの影響: `O_DIRECT`バイパスを有効にすると、OS バッファ キャッシュの汚染が防止されますが、後続のファイルの読み取りでは、バッファ キャッシュへの内容の再読み取りが必要になります。
-   デフォルト値: `false`

### <code>enable-pipelined-write</code> {#code-enable-pipelined-write-code}

-   パイプライン書き込みを有効にするかどうかを制御します。この構成が有効な場合、以前のパイプライン書き込みが使用されます。この設定を無効にすると、新しいパイプライン コミット メカニズムが使用されます。
-   デフォルト値: `true`

### <code>allow-concurrent-memtable-write</code> {#code-allow-concurrent-memtable-write-code}

-   memtable の同時書き込みを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   ファイルが非同期で書き込まれている間に、OS がファイルをディスクに増分同期する速度。
-   デフォルト値: `"1MB"`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>wal-bytes-per-sync</code> {#code-wal-bytes-per-sync-code}

-   WAL ファイルの書き込み時に OS が WAL ファイルをディスクに増分同期する速度
-   デフォルト値: `"512KB"`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>info-log-max-size</code> {#code-info-log-max-size-code}

-   情報ログの最大サイズ
-   デフォルト値: `"1GB"`
-   最小値: `0`
-   単位: B|KB|MB|GB

### <code>info-log-roll-time</code> {#code-info-log-roll-time-code}

-   情報ログが切り詰められる間隔。値が`0s`の場合、ログは切り捨てられません。
-   デフォルト値: `"0s"` (ログが切り捨てられないことを意味します)

### <code>info-log-keep-log-file-num</code> {#code-info-log-keep-log-file-num-code}

-   RaftDB に保存される情報ログ ファイルの最大数
-   デフォルト値: `10`
-   最小値: `0`

### <code>info-log-dir</code> {#code-info-log-dir-code}

-   情報ログが保存されるディレクトリ
-   デフォルト値: `""`

### <code>info-log-level</code> {#code-info-log-level-code}

-   RaftDB のログレベル
-   デフォルト値: `"info"`

## いかだエンジン {#raft-engine}

Raft Engineに関連するコンフィグレーション項目。

> **注記：**
>
> -   初めてRaft Engine を有効にすると、TiKV はデータを RocksDB からRaft Engineに転送します。したがって、TiKV が開始されるまでさらに数十秒待つ必要があります。
> -   TiDB v5.4.0 のRaft Engineのデータ形式は、以前の TiDB バージョンと互換性がありません。したがって、TiDB クラスターを v5.4.0 から以前のバージョンにダウングレードする必要がある場合は、ダウングレードする**前に**、 `enable`から`false`に設定してRaft Engine を無効にし、構成を有効にするために TiKV を再起動します。

### <code>enable</code> {#code-enable-code}

-   Raftログを保存するためにRaft Engineを使用するかどうかを決定します。有効にすると、 `raftdb`の設定は無視されます。
-   デフォルト値: `true`

### <code>dir</code> {#code-dir-code}

-   raft ログ ファイルが保存されるディレクトリ。ディレクトリが存在しない場合は、TiKV の起動時に作成されます。
-   この設定項目が設定されていない場合は、 `{data-dir}/raft-engine`が使用されます。
-   マシン上に複数のディスクがある場合、TiKV のパフォーマンスを向上させるために、 Raft Engineのデータを別のディスクに保存することをお勧めします。
-   デフォルト値: `""`

### <code>batch-compression-threshold</code> {#code-batch-compression-threshold-code}

-   ログバッチのしきい値サイズを指定します。この構成より大きいログ バッチは圧縮されます。この構成項目を`0`に設定すると、圧縮は無効になります。
-   デフォルト値: `"8KB"`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   バッファリングされた書き込みの最大累積サイズを指定します。この設定値を超えると、バッファされた書き込みがディスクにフラッシュされます。
-   この構成項目を`0`に設定すると、増分同期は無効になります。
-   デフォルト値: `"4MB"`

### <code>target-file-size</code> {#code-target-file-size-code}

-   ログファイルの最大サイズを指定します。ログ ファイルがこの値より大きい場合、ログ ファイルはローテーションされます。
-   デフォルト値: `"128MB"`

### <code>purge-threshold</code> {#code-purge-threshold-code}

-   メインログキューのしきい値サイズを指定します。この設定値を超えると、メイン ログ キューがパージされます。
-   この設定を使用して、 Raft Engineのディスク領域使用量を調整できます。
-   デフォルト値: `"10GB"`

### <code>recovery-mode</code> {#code-recovery-mode-code}

-   リカバリ中のファイル破損に対処する方法を決定します。
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

> **注記：**
>
> `format-version`を`2`に設定した後、TiKV クラスターを v6.3.0 から以前のバージョンにダウングレードする必要がある場合は、ダウングレードする**前に**次の手順を実行します。
>
> 1.  [`enable`](/tikv-configuration-file.md#enable-1)から`false`設定してRaft Engine を無効にし、TiKV を再起動して設定を有効にします。
> 2.  `format-version` ～ `1`を設定します。
> 3.  `enable`から`true`設定してRaft Engine を有効にし、TiKV を再起動して設定を有効にします。

-   Raft Engineのログ ファイルのバージョンを指定します。
-   値のオプション:
    -   `1` : v6.3.0 より前の TiKV のデフォルトのログ ファイル バージョン。 TiKV 以降の v6.1.0 で読み込むことができます。
    -   `2` : ログのリサイクルをサポートします。 TiKV 以降の v6.3.0 で読み込むことができます。
-   デフォルト値: `2`

### <code>enable-log-recycle</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-enable-log-recycle-code-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この設定項目は、 [`format-version`](#format-version-new-in-v630) &gt;= 2 の場合にのみ使用できます。

-   Raft Engineで古いログ ファイルをリサイクルするかどうかを決定します。これを有効にすると、論理的にパージされたログ ファイルがリサイクル用に予約されます。これにより、書き込みワークロードのロングテールレイテンシーが短縮されます。
-   デフォルト値: `true`

### <code>prefill-for-recycle</code> <span class="version-mark">v7.0.0 の新機能</span> {#code-prefill-for-recycle-code-span-class-version-mark-new-in-v7-0-0-span}

> **注記：**
>
> この設定項目は、 [`enable-log-recycle`](#enable-log-recycle-new-in-v630)が`true`に設定されている場合にのみ有効になります。

-   Raft Engineでログをリサイクルするために空のログ ファイルを生成するかどうかを決定します。これを有効にすると、 Raft Engine は初期化中にログのリサイクルのために空のログ ファイルのバッチを自動的に埋め、初期化直後にログのリサイクルが有効になります。
-   デフォルト値: `false`

## 安全 {#security}

セキュリティに関するコンフィグレーション項目。

### <code>ca-path</code> {#code-ca-path-code}

-   CA ファイルのパス
-   デフォルト値: `""`

### <code>cert-path</code> {#code-cert-path-code}

-   X.509 証明書を含むプライバシー強化メール (PEM) ファイルのパス
-   デフォルト値: `""`

### <code>key-path</code> {#code-key-path-code}

-   X.509 キーを含む PEM ファイルのパス
-   デフォルト値: `""`

### <code>cert-allowed-cn</code> {#code-cert-allowed-cn-code}

-   クライアントによって提示された証明書で許容される X.509 共通名のリスト。リクエストは、提示された共通名がリスト内のエントリの 1 つと完全に一致する場合にのみ許可されます。
-   デフォルト値: `[]` 。これは、クライアント証明書の CN チェックがデフォルトで無効になっていることを意味します。

### <code>redact-info-log</code> <span class="version-mark">v4.0.8 の新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v4-0-8-span}

-   この構成項目は、ログの編集を有効または無効にします。構成値が`true`に設定されている場合、ログ内のすべてのユーザー データは`?`に置き換えられます。
-   デフォルト値: `false`

## セキュリティ.暗号化 {#security-encryption}

[保存時の暗号化](/encryption-at-rest.md) (TDE)に関するコンフィグレーション項目。

### <code>data-encryption-method</code> {#code-data-encryption-method-code}

-   データファイルの暗号化方式
-   値のオプション: 「plaintext」、「aes128-ctr」、「aes192-ctr」、「aes256-ctr」、および「sm4-ctr」 (v6.3.0 以降でサポート)
-   「plaintext」以外の値は暗号化が有効であることを意味し、その場合はマスターキーを指定する必要があります。
-   デフォルト値: `"plaintext"`

### <code>data-key-rotation-period</code> {#code-data-key-rotation-period-code}

-   TiKV がデータ暗号化キーをローテーションする頻度を指定します。
-   デフォルト値: `7d`

### <code>enable-file-dictionary-log</code> {#code-enable-file-dictionary-log-code}

-   TiKV が暗号化メタデータを管理する場合、最適化を有効にして I/O とミューテックスの競合を削減します。
-   この構成パラメータが (デフォルトで) 有効になっている場合に発生する可能性のある互換性の問題を回避するには、詳細については[保存時の暗号化- TiKV バージョン間の互換性](/encryption-at-rest.md#compatibility-between-tikv-versions)を参照してください。
-   デフォルト値: `true`

### <code>master-key</code> {#code-master-key-code}

-   暗号化が有効な場合はマスターキーを指定します。マスターキーの構成方法については、 [保存時の暗号化- 暗号化を構成する](/encryption-at-rest.md#configure-encryption)を参照してください。

### <code>previous-master-key</code> {#code-previous-master-key-code}

-   新しいマスター キーをローテーションするときに古いマスター キーを指定します。設定形式は`master-key`と同様です。マスターキーの構成方法については、 [保存時の暗号化- 暗号化を構成する](/encryption-at-rest.md#configure-encryption)を参照してください。

## 輸入 {#import}

TiDB LightningインポートおよびBRリストアに関連するコンフィグレーション項目。

### <code>num-threads</code> {#code-num-threads-code}

-   RPC リクエストを処理するスレッドの数
-   デフォルト値: `8`
-   最小値: `1`

### <code>stream-channel-window</code> {#code-stream-channel-window-code}

-   ストリーム チャネルのウィンドウ サイズ。チャンネルがいっぱいになると、ストリームはブロックされます。
-   デフォルト値: `128`

### <code>memory-use-ratio</code> <span class="version-mark">v6.5.0 の新機能</span> {#code-memory-use-ratio-code-span-class-version-mark-new-in-v6-5-0-span}

-   v6.5.0 以降、PITR はメモリ内のバックアップ ログ ファイルへの直接アクセスとデータの復元をサポートします。この設定項目は、TiKV の合計メモリに対する PITR に使用可能なメモリの比率を指定します。
-   値の範囲: [0.0、0.5]
-   デフォルト値: `0.3` 。これは、システムメモリの 30% が PITR に使用できることを意味します。値が`0.0`場合、PITR はログ ファイルをローカル ディレクトリにダウンロードすることによって実行されます。

> **注記：**
>
> v6.5.0 より前のバージョンでは、ポイントインタイム リカバリ (PITR) は、バックアップ ファイルをローカル ディレクトリにダウンロードすることによるデータの復元のみをサポートします。

## GC {#gc}

### <code>batch-keys</code> {#code-batch-keys-code}

-   1 回のバッチでガベージ コレクションされるキーの数
-   デフォルト値: `512`

### <code>max-write-bytes-per-sec</code> {#code-max-write-bytes-per-sec-code}

-   GC ワーカーが 1 秒間に RocksDB に書き込むことができる最大バイト数。
-   値が`0`に設定されている場合、制限はありません。
-   デフォルト値: `"0"`

### <code>enable-compaction-filter</code> <span class="version-mark">v5.0 の新機能</span> {#code-enable-compaction-filter-code-span-class-version-mark-new-in-v5-0-span}

-   圧縮フィルター機能で GC を有効にするかどうかを制御します
-   デフォルト値: `true`

### <code>ratio-threshold</code> {#code-ratio-threshold-code}

-   GC をトリガーするガベージ率のしきい値。
-   デフォルト値: `1.1`

## バックアップ {#backup}

BRバックアップに関するコンフィグレーション項目。

### <code>num-threads</code> {#code-num-threads-code}

-   バックアップを処理するワーカー スレッドの数
-   デフォルト値: `MIN(CPU * 0.5, 8)`
-   値の範囲: `[1, CPU]`
-   最小値: `1`

### <code>batch-size</code> {#code-batch-size-code}

-   1 回のバッチでバックアップするデータ範囲の数
-   デフォルト値: `8`

### <code>sst-max-size</code> {#code-sst-max-size-code}

-   バックアップ SST ファイル サイズのしきい値。 TiKVリージョン内のバックアップ ファイルのサイズがこのしきい値を超える場合、ファイルは TiKVリージョンを複数のリージョン範囲に分割して複数のファイルにバックアップされます。分割されたリージョン内の各ファイルのサイズは`sst-max-size`と同じ (またはわずかに大きい) です。
-   たとえば、リージョン`[a,e)`のバックアップ ファイルのサイズが`sst-max-size`より大きい場合、ファイルはリージョン`[a,b)` 、 `[b,c)` 、 `[c,d)`および`[d,e)`の複数のファイルにバックアップされますが、 `[a,b)` 、 `[b,c)` 、 `[c,d)`のサイズは同じです。 `sst-max-size`のものと同じ (またはわずかに大きい)。
-   デフォルト値: `"144MB"`

### <code>enable-auto-tune</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-enable-auto-tune-code-span-class-version-mark-new-in-v5-4-0-span}

-   クラスターのリソース使用率が高い場合に、クラスターへの影響を軽減するためにバックアップ タスクで使用されるリソースを制限するかどうかを制御します。詳細については、 [BRオートチューン](/br/br-auto-tune.md)を参照してください。
-   デフォルト値: `true`

### <code>s3-multi-part-size</code> <span class="version-mark">v5.3.2 の新機能</span> {#code-s3-multi-part-size-code-span-class-version-mark-new-in-v5-3-2-span}

> **注記：**
>
> この構成は、S3 レート制限によって引き起こされるバックアップの失敗に対処するために導入されました。この問題は[バックアップデータのstorage構造を改良する](/br/br-snapshot-architecture.md#structure-of-backup-files)で修正されました。したがって、この構成は v6.1.1 から非推奨となり、推奨されなくなりました。

-   バックアップ中に S3 へのマルチパート アップロードを実行するときに使用されるパート サイズ。この設定の値を調整して、S3 に送信されるリクエストの数を制御できます。
-   データが S3 にバックアップされ、バックアップ ファイルがこの設定項目の値より大きい場合、 [マルチパートアップロード](https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPart.html)が自動的に有効になります。圧縮率に基づいて、96 MiBリージョンによって生成されるバックアップ ファイルは約 10 MiB ～ 30 MiB になります。
-   デフォルト値: 5MiB

## backup.hadoop {#backup-hadoop}

### <code>home</code> {#code-home-code}

-   HDFS シェル コマンドの場所を指定し、TiKV がシェル コマンドを検索できるようにします。この設定項目は、環境変数`$HADOOP_HOME`と同じ効果があります。
-   デフォルト値: `""`

### <code>linux-user</code> {#code-linux-user-code}

-   TiKV が HDFS シェル コマンドを実行する Linux ユーザーを指定します。
-   この構成項目が設定されていない場合、TiKV は現在の Linux ユーザーを使用します。
-   デフォルト値: `""`

## ログバックアップ {#log-backup}

ログバックアップに関するコンフィグレーション項目です。

### <span class="version-mark">v6.2.0 の新機能</span><code>enable</code> {#code-enable-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログのバックアップを有効にするかどうかを決定します。
-   デフォルト値: `true`

### <code>file-size-limit</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-file-size-limit-code-span-class-version-mark-new-in-v6-2-0-span}

-   保存されるバックアップ ログ データのサイズ制限。
-   デフォルト値: 256MiB
-   注: 通常、値`file-size-limit`は、外部storageに表示されるバックアップ ファイルのサイズより大きくなります。これは、バックアップ ファイルが外部storageにアップロードされる前に圧縮されるためです。

### <code>initial-scan-pending-memory-quota</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-initial-scan-pending-memory-quota-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ バックアップ中に増分スキャン データを保存するために使用されるキャッシュのクォータ。
-   デフォルト値: `min(Total machine memory * 10%, 512 MB)`

### <code>initial-scan-rate-limit</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-initial-scan-rate-limit-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ バックアップ中の増分データ スキャンのスループットのレート制限。
-   デフォルト値: 60。デフォルトのレート制限が 60 MB/秒であることを示します。

### <code>max-flush-interval</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-max-flush-interval-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログバックアップにおいてバックアップデータを外部storageに書き込む最大間隔。
-   デフォルト値: 3分

### <code>num-threads</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-num-threads-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログのバックアップに使用されるスレッドの数。
-   デフォルト値: CPU * 0.5
-   値の範囲: [2、12]

### <code>temp-path</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-temp-path-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログ ファイルが外部storageにフラッシュされる前に書き込まれる一時パス。
-   デフォルト値: `${deploy-dir}/data/log-backup-temp`

## CDC {#cdc}

TiCDC に関するコンフィグレーション項目。

### <code>min-ts-interval</code> {#code-min-ts-interval-code}

-   解決された TS が計算されて転送される間隔。
-   デフォルト値: `"200ms"`

### <code>old-value-cache-memory-quota</code> {#code-old-value-cache-memory-quota-code}

-   TiCDC の古い値によるメモリ使用量の上限。
-   デフォルト値: `512MB`

### <code>sink-memory-quota</code> {#code-sink-memory-quota-code}

-   TiCDC データ変更イベントによるメモリ使用量の上限。
-   デフォルト値: `512MB`

### <code>incremental-scan-speed-limit</code> {#code-incremental-scan-speed-limit-code}

-   履歴データが段階的にスキャンされる最大速度。
-   デフォルト値: `"128MB"` 、1 秒あたり 128 MB を意味します。

### <code>incremental-scan-threads</code> {#code-incremental-scan-threads-code}

-   履歴データを段階的にスキャンするタスクのスレッド数。
-   デフォルト値: `4` 、これは 4 つのスレッドを意味します。

### <code>incremental-scan-concurrency</code> {#code-incremental-scan-concurrency-code}

-   履歴データを段階的にスキャンするタスクの同時実行の最大数。
-   デフォルト値: `6` 。これは、最大 6 つのタスクを同時に実行できることを意味します。
-   注: `incremental-scan-concurrency`の値は`incremental-scan-threads`以上である必要があります。そうしないと、TiKV は起動時にエラーを報告します。

## resolved-ts {#resolved-ts}

ステイル読み取りリクエストを処理するために解決済み TS を維持することに関連するコンフィグレーション項目。

### <code>enable</code> {#code-enable-code}

-   すべてのリージョンの解決済み TS を維持するかどうかを決定します。
-   デフォルト値: `true`

### <code>advance-ts-interval</code> {#code-advance-ts-interval-code}

-   解決された TS が計算されて転送される間隔。
-   デフォルト値: `"20s"`

### <code>scan-lock-pool-size</code> {#code-scan-lock-pool-size-code}

-   解決済み TS の初期化時に、TiKV が MVCC (マルチバージョン同時実行制御) ロック データをスキャンするために使用するスレッドの数。
-   デフォルト値: `2` 、これは 2 つのスレッドを意味します。

## pessimistic-txn {#pessimistic-txn}

悲観的トランザクションの使用法については、 [TiDB ペシミスティックトランザクションモード](/pessimistic-transaction.md)を参照してください。

### <code>wait-for-lock-timeout</code> {#code-wait-for-lock-timeout-code}

-   TiKV の悲観的トランザクションが、他のトランザクションがロックを解放するのを待機する最長時間。タイムアウトになると、TiDB にエラーが返され、TiDB はロックの追加を再試行します。ロック待機タイムアウトは`innodb_lock_wait_timeout`に設定されます。
-   デフォルト値: `"1s"`
-   最小値: `"1ms"`

### <code>wake-up-delay-duration</code> {#code-wake-up-delay-duration-code}

-   悲観的トランザクションがロックを解放すると、ロックを待っているすべてのトランザクションのうち、最も小さい`start_ts`を持つトランザクションだけがウェイクアップされます。他のトランザクションは`wake-up-delay-duration`後に起動されます。
-   デフォルト値: `"20ms"`

### <code>pipelined</code> {#code-pipelined-code}

-   この構成項目により、悲観的ロックを追加するパイプライン処理が可能になります。この機能を有効にすると、データがロックできることを検出した後、TiKV はただちに TiDB に後続のリクエストを実行し、悲観的ロックを非同期で書き込むように通知します。これにより、レイテンシーのほとんどが短縮され、悲観的トランザクションのパフォーマンスが大幅に向上します。ただし、悲観的ロックの非同期書き込みが失敗する可能性は依然として低いため、悲観的トランザクションのコミットが失敗する可能性があります。
-   デフォルト値: `true`

### <code>in-memory</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-in-memory-code-span-class-version-mark-new-in-v6-0-0-span}

-   メモリ内の悲観的ロック機能を有効にします。この機能を有効にすると、悲観的トランザクションは、ロックをディスクに書き込んだり、ロックを他のレプリカに複製したりする代わりに、ロックをメモリに保存しようとします。これにより、悲観的トランザクションのパフォーマンスが向上します。ただし、悲観的ロックが失われ、悲観的トランザクションのコミットが失敗する可能性は依然として低いです。
-   デフォルト値: `true`
-   `in-memory` `pipelined`の値が`true`の場合にのみ有効であることに注意してください。

## クォータ {#quota}

クォータリミッターに関するコンフィグレーション項目。

### <code>max-delay-duration</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-max-delay-duration-code-span-class-version-mark-new-in-v6-0-0-span}

-   単一の読み取りまたは書き込みリクエストがフォアグラウンドで処理されるまで強制的に待機する最大時間。
-   デフォルト値: `500ms`
-   推奨設定: ほとんどの場合、デフォルト値を使用することをお勧めします。インスタンスでメモリ不足 (OOM) または激しいパフォーマンスのジッターが発生した場合は、値を 1S に設定して、リクエストの待機時間を 1 秒より短くすることができます。

### フォアグラウンド クォータ リミッター {#foreground-quota-limiter}

フォアグラウンド クォータ リミッターに関するコンフィグレーション項目。

TiKV がデプロイされているマシンのリソースが限られている (たとえば、CPU が 4 v とメモリが16 G しかない) とします。この状況では、TiKV のフォアグラウンドで処理される読み取りおよび書き込みリクエストが多すぎるため、バックグラウンドで使用される CPU リソースがそのようなリクエストの処理を支援するために占有され、TiKV のパフォーマンスの安定性に影響を与える可能性があります。この状況を回避するには、フォアグラウンド クォータ関連の構成項目を使用して、フォアグラウンドで使用される CPU リソースを制限します。リクエストによってクォータ リミッターがトリガーされると、リクエストは TiKV が CPU リソースを解放するまでしばらく待機することになります。正確な待機時間はリクエストの数によって異なり、最大待機時間は値[`max-delay-duration`](#max-delay-duration-new-in-v600)を超えることはありません。

#### <code>foreground-cpu-time</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-foreground-cpu-time-code-span-class-version-mark-new-in-v6-0-0-span}

-   TiKV フォアグラウンドが読み取りおよび書き込みリクエストを処理するために使用する CPU リソースのソフト制限。
-   デフォルト値: `0` (制限なしを意味します)
-   単位: millicpu (たとえば、 `1500`フォアグラウンド要求が 1.5v CPU を消費することを意味します)
-   推奨設定: 4 コアを超えるインスタンスの場合は、デフォルト値`0`を使用します。 4 コアのインスタンスの場合、値を`1000` ～ `1500`の範囲に設定するとバランスが取れます。 2 コアのインスタンスの場合は、値を`1200`より小さくしてください。

#### <code>foreground-write-bandwidth</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-foreground-write-bandwidth-code-span-class-version-mark-new-in-v6-0-0-span}

-   トランザクションがデータを書き込む帯域幅のソフト制限。
-   デフォルト値: `0KB` (制限なしを意味します)
-   推奨設定: `foreground-cpu-time`設定では書き込み帯域幅を制限するのに十分でない場合を除き、ほとんどの場合はデフォルト値`0`を使用します。このような例外を考慮して、4 コア以下のインスタンスでは`50MB`より小さい値を設定することをお勧めします。

#### <code>foreground-read-bandwidth</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-foreground-read-bandwidth-code-span-class-version-mark-new-in-v6-0-0-span}

-   トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限。
-   デフォルト値: `0KB` (制限なしを意味します)
-   推奨設定: `foreground-cpu-time`設定では読み取り帯域幅を制限するのに十分でない場合を除き、ほとんどの場合はデフォルト値`0`を使用します。このような例外を考慮して、4 コア以下のインスタンスでは`20MB`より小さい値を設定することをお勧めします。

### バックグラウンド クォータ リミッター {#background-quota-limiter}

バックグラウンドクォータリミッターに関するコンフィグレーション項目。

TiKV がデプロイされているマシンのリソースが限られている (たとえば、CPU が 4 v とメモリが16 G しかない) とします。この状況では、TiKV のバックグラウンドで処理される計算と読み取りおよび書き込みリクエストが多すぎる可能性があるため、フォアグラウンドで使用される CPU リソースがそのようなリクエストの処理を支援するために占有され、TiKV のパフォーマンスの安定性に影響します。この状況を回避するには、バックグラウンド クォータ関連の設定項目を使用して、バックグラウンドで使用される CPU リソースを制限します。リクエストによってクォータ リミッターがトリガーされると、リクエストは TiKV が CPU リソースを解放するまでしばらく待機することになります。正確な待機時間はリクエストの数によって異なり、最大待機時間は値[`max-delay-duration`](#max-delay-duration-new-in-v600)を超えることはありません。

> **警告：**
>
> -   バックグラウンド クォータ リミッターは、TiDB v6.2.0 で導入された実験的機能であり、本番環境での使用は推奨されませ**ん**。
> -   この機能は、リソースが限られた環境で TiKV を安定して実行できるようにするためにのみ適しています。リソースが豊富な環境でこの機能を有効にすると、リクエストの量がピークに達したときにパフォーマンスの低下が発生する可能性があります。

#### <code>background-cpu-time</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-background-cpu-time-code-span-class-version-mark-new-in-v6-2-0-span}

-   読み取りおよび書き込みリクエストを処理するために TiKV バックグラウンドで使用される CPU リソースのソフト制限。
-   デフォルト値: `0` (制限なしを意味します)
-   単位: millicpu (たとえば、 `1500`バックグラウンド要求が 1.5v CPU を消費することを意味します)

#### <code>background-write-bandwidth</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-background-write-bandwidth-code-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この構成項目は`SHOW CONFIG`の結果として返されますが、現在設定しても効果はありません。

-   バックグラウンド トランザクションがデータを書き込む帯域幅のソフト制限。
-   デフォルト値: `0KB` (制限なしを意味します)

#### <code>background-read-bandwidth</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-background-read-bandwidth-code-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この構成項目は`SHOW CONFIG`の結果として返されますが、現在設定しても効果はありません。

-   バックグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限。
-   デフォルト値: `0KB` (制限なしを意味します)

#### <code>enable-auto-tune</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-enable-auto-tune-code-span-class-version-mark-new-in-v6-2-0-span}

-   クォータの自動調整を有効にするかどうかを決定します。この構成項目が有効になっている場合、TiKV は TiKV インスタンスの負荷に基づいてバックグラウンド リクエストのクォータを動的に調整します。
-   デフォルト値: `false` (自動チューニングが無効であることを意味します)

## causal-ts <span class="version-mark">v6.1.0 の新機能</span> {#causal-ts-span-class-version-mark-new-in-v6-1-0-span}

TiKV API V2 が有効な場合のタイムスタンプの取得に関連するコンフィグレーション項目 ( `storage.api-version = 2` )。

書き込みレイテンシーを短縮するために、TiKV はタイムスタンプのバッチをローカルに定期的に取得してキャッシュします。キャッシュされたタイムスタンプは、PD への頻繁なアクセスを回避し、短期間の TSO サービス障害を許容するのに役立ちます。

### <code>alloc-ahead-buffer</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-alloc-ahead-buffer-code-span-class-version-mark-new-in-v6-4-0-span}

-   事前に割り当てられた TSO キャッシュ サイズ (期間内)。
-   TiKV が、この構成項目で指定された期間に基づいて TSO キャッシュを事前に割り当てることを示します。 TiKV は、前の期間に基づいて TSO 使用量を推定し、 `alloc-ahead-buffer`満たす TSO をローカルに要求してキャッシュします。
-   この構成項目は、TiKV API V2 が有効になっている場合 ( `storage.api-version = 2` )、PD 障害の許容度を高めるためによく使用されます。
-   この構成項目の値を増やすと、TSO の消費量と TiKV のメモリオーバーヘッドが増加する可能性があります。十分な TSO を取得するには、PD の[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)構成項目を減らすことをお勧めします。
-   テストによると、デフォルト値が`alloc-ahead-buffer`の場合、PD リーダーに障害が発生して別のノードに切り替わると、書き込みレイテンシーのレイテンシが短期間増加し、QPS が低下します (約 15%)。
-   ビジネスへの影響を避けるために、PD で`tso-update-physical-interval = "1ms"`を構成し、TiKV で次の構成項目を構成できます。
    -   `causal-ts.alloc-ahead-buffer = "6s"`
    -   `causal-ts.renew-batch-max-size = 65536`
    -   `causal-ts.renew-batch-min-size = 2048`
-   デフォルト値: `3s`

### <code>renew-interval</code> {#code-renew-interval-code}

-   ローカルにキャッシュされたタイムスタンプが更新される間隔。
-   TiKV は`renew-interval`の間隔でタイムスタンプのリフレッシュのバッチを開始し、前の期間のタイムスタンプの消費量と[`alloc-ahead-buffer`](#alloc-ahead-buffer-new-in-v640)の設定に従って、キャッシュされたタイムスタンプの数を調整します。このパラメーターの設定値が大きすぎると、最新の TiKV ワークロードの変更が時間内に反映されません。このパラメータを小さい値に設定すると、PD の負荷が増加します。書き込みトラフィックが大きく変動する場合、タイムスタンプが頻繁に使い果たされる場合、および書き込みレイテンシーが増加する場合は、このパラメータをより小さい値に設定できます。同時に PD の負荷も考慮する必要があります。
-   デフォルト値: `"100ms"`

### <code>renew-batch-min-size</code> {#code-renew-batch-min-size-code}

-   タイムスタンプ要求内の TSO の最小数。
-   TiKV は、前の期間のタイムスタンプの消費量に応じて、キャッシュされたタイムスタンプの数を調整します。少数の TSO のみが必要な場合、TiKV は、数が`renew-batch-min-size`に達するまで要求された TSO を減らします。アプリケーションで大量のバースト書き込みトラフィックが頻繁に発生する場合は、必要に応じてこのパラメータをより大きな値に設定できます。このパラメータは単一の tikv サーバーのキャッシュ サイズであることに注意してください。パラメーターの設定値が大きすぎ、クラスターに多数の tikv サーバーが含まれている場合、TSO の消費が速すぎます。
-   Grafana の**[TiKV-RAW]** &gt; **[Causal timestamp]**パネルでは、 **TSO バッチ サイズは**、アプリケーションのワークロードに応じて動的に調整された、ローカルにキャッシュされたタイムスタンプの数です。この指標を参照して`renew-batch-min-size`を調整できます。
-   デフォルト値: `100`

### <code>renew-batch-max-size</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-renew-batch-max-size-code-span-class-version-mark-new-in-v6-4-0-span}

-   タイムスタンプ要求内の TSO の最大数。
-   デフォルトの TSO 物理時間更新間隔 ( `50ms` ) では、PD は最大 262144 個の TSO を提供します。要求された TSO がこの数を超えると、PD はそれ以上 TSO を提供しません。この構成アイテムは、TSO の枯渇と、TSO の枯渇による他のビジネスへの逆影響を回避するために使用されます。高可用性を向上させるためにこの構成項目の値を増やす場合、十分な TSO を取得するには、同時に[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)の値を減らす必要があります。
-   デフォルト値: `8192`

## リソース制御 {#resource-control}

TiKVstorageレイヤーのリソース制御に関するコンフィグレーション項目。

### <code>enabled</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-enabled-code-span-class-version-mark-new-in-v6-6-0-span}

-   対応するリソース グループの[リクエストユニット(RU)](/tidb-resource-control.md#what-is-request-unit-ru)に従って、ユーザーのフォアグラウンド読み取り/書き込み要求のスケジューリングを有効にするかどうかを制御します。 TiDB リソース グループとリソース制御については、 [TiDB リソース制御](/tidb-resource-control.md)を参照してください。
-   この設定項目を有効にすると、TiDB で[`tidb_enable_resource_control](/system-variables.md#tidb_enable_resource_control-new-in-v660)が有効になっている場合にのみ機能します。この構成項目が有効になっている場合、TiKV はプライオリティ キューを使用して、フォアグラウンド ユーザーからのキューに入れられた読み取り/書き込み要求をスケジュールします。リクエストのスケジューリング優先度は、このリクエストを受信するリソース グループによって既に消費されているリソースの量に反比例し、対応するリソース グループのクォータに正の相関関係があります。
-   デフォルト値: `true` 。これは、リソース グループの RU に基づくスケジューリングが有効であることを意味します。

## スプリット {#split}

[ロードベースの分割](/configure-load-base-split.md)に関するコンフィグレーション項目。

### <code>byte-threshold</code> <span class="version-mark">v5.0 の新機能</span> {#code-byte-threshold-code-span-class-version-mark-new-in-v5-0-span}

-   リージョンがホットスポットとして識別されるトラフィックのしきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size) 4 GB 未満の場合、1 秒あたり`30MiB` 。
    -   [`region-split-size`](#region-split-size)が 4 GB 以上の場合、1 秒あたり`100MiB` 。

### <code>qps-threshold</code> {#code-qps-threshold-code}

-   リージョンがホットスポットとして識別される QPS しきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size) 4GB未満の場合は`3000` 。
    -   [`region-split-size`](#region-split-size)が 4 GB 以上の場合は`7000` 。

### <code>region-cpu-overload-threshold-ratio</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-region-cpu-overload-threshold-ratio-code-span-class-version-mark-new-in-v6-2-0-span}

-   リージョンがホットスポットとして識別される CPU 使用率のしきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size) 4GB未満の場合は`0.25` 。
    -   [`region-split-size`](#region-split-size)が 4 GB 以上の場合は`0.75` 。
