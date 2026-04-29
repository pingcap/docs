---
title: TiKV Configuration File
summary: TiKVの設定ファイルについて学びましょう。
---

# TiKVコンフィグレーションファイル {#tikv-configuration-file}

<!-- markdownlint-disable MD001 -->

TiKV の設定ファイルは、コマンドライン パラメータよりも多くのオプションをサポートしています。デフォルトの設定ファイルは[etc/config-template.toml](https://github.com/tikv/tikv/blob/release-8.5/etc/config-template.toml)にあり、 `config.toml`に名前を変更できます。

このドキュメントでは、コマンドライン パラメーターに含まれないパラメーターのみについて説明します。詳しくは[コマンドラインパラメータ](/command-line-flags-for-tikv-configuration.md)をご覧ください。

> **ヒント：**
>
> 設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

## グローバル設定 {#global-configuration}

### <code>abort-on-panic</code> {#code-abort-on-panic-code}

-   TiKVがパニックを起こした際に、 `abort()`を呼び出してプロセスを終了させるかどうかを設定します。このオプションは、TiKVがシステムにコアダンプファイルの生成を許可するかどうかに影響します。

    -   この構成項目の値が`false`の場合、TiKV がパニックを起こすと、 `exit()`を呼び出してプロセスを終了します。
    -   この設定項目の値が`true`の場合、TiKV がパニックを起こすと、TiKV は`abort()`を呼び出してプロセスを終了します。このとき、TiKV は終了時にコアダンプファイルを生成することをシステムに許可します。コアダンプファイルを生成するには、コアダンプに関連するシステム設定も実行する必要があります (たとえば、 `ulimit -c`コマンドを使用してコアダンプファイルのサイズ制限を設定したり、コアダンプパスを設定したりします。オペレーティングシステムによって関連する設定が異なります)。コアダンプファイルがディスク容量を過剰に占有して TiKV のディスク容量が不足するのを避けるため、コアダンプ生成パスを TiKV データのディスクパーティションとは異なるディスクパーティションに設定することをお勧めします。

-   デフォルト値: `false`

### <code>slow-log-file</code> {#code-slow-log-file-code}

-   スローログを保存するファイル
-   この設定項目が設定されていないが、 `log.file.filename`が設定されている場合、スローログは`log.file.filename`で指定されたログファイルに出力されます。
-   `slow-log-file`も`log.file.filename`も設定されていない場合、デフォルトではすべてのログが「stderr」に出力されます。
-   両方の設定項目が設定されている場合、通常のログは`log.file.filename`で指定されたログファイルに出力され、スローログは`slow-log-file`で設定されたログファイルに出力されます。
-   デフォルト値: `""`

### <code>slow-log-threshold</code> {#code-slow-log-threshold-code}

-   処理時間が遅い場合のログ出力のしきい値。処理時間がこのしきい値を超えると、処理時間が遅い場合のログが出力されます。
-   デフォルト値: `"1s"`

### <code>memory-usage-limit</code> {#code-memory-usage-limit-code}

-   TiKVインスタンスのメモリ使用量の上限。TiKVのメモリ使用量がこのしきい値に近づくと、内部キャッシュが削除されてメモリが解放されます。
-   ほとんどの場合、TiKVインスタンスはシステムメモリ全体の75%を使用するように設定されているため、この設定項目を明示的に指定する必要はありません。残りの25%のメモリはOSページキャッシュ用に予約されています。詳細は[`storage.block-cache.capacity`](#capacity)を参照してください。
-   単一の物理マシン上に複数の TiKV ノードをデプロイする場合でも、この構成項目を設定する必要はありません。この場合、TiKV インスタンスは`5/3 * block-cache.capacity`のメモリを使用します。
-   システムメモリ容量ごとのデフォルト値は以下のとおりです。

    -   システム=8G ブロックキャッシュ=3.6G メモリ使用量制限=6G ページキャッシュ=2G
    -   システム=16G ブロックキャッシュ=7.2G メモリ使用量制限=12G ページキャッシュ=4G
    -   システム=32G ブロックキャッシュ=14.4G メモリ使用量制限=24G ページキャッシュ=8G

## ログ<span class="version-mark">v5.4.0 の新機能</span> {#log-span-class-version-mark-new-in-v5-4-0-span}

-   ログに関連するコンフィグレーション項目。

-   バージョン 5.4.0 以降、TiKV と TiDB のログ設定項目を統一するため、TiKV は以前の設定項目`log-rotation-timespan`を非推奨とし、 `log-level` 、 `log-format` 、 `log-file` 、 `log-rotation-size`を以下の項目に変更します。古い設定項目のみを設定し、その値をデフォルト値以外に設定した場合、古い項目は新しい項目と互換性があります。古い設定項目と新しい設定項目の両方を設定した場合、新しい項目が有効になります。

### <code>level</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-level-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログレベル
-   オプション値: `"debug"` 、 `"info"` 、 `"warn"` 、 `"error"` 、 `"fatal"`
-   デフォルト値: `"info"`

### <code>format</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-format-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログ形式
-   オプション値: `"json"` 、 `"text"`
-   デフォルト値: `"text"`

### <code>enable-timestamp</code> <span class="version-mark">v5.4.0で追加</span> {#code-enable-timestamp-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログ内のタイムスタンプを有効にするか無効にするかを決定します。
-   オプション値: `true` 、 `false`
-   デフォルト値: `true`

## log.file <span class="version-mark">v5.4.0で追加</span> {#log-file-span-class-version-mark-new-in-v5-4-0-span}

-   ログファイルに関連するコンフィグレーション項目。

### <code>filename</code> <span class="version-mark">v5.4.0 で追加</span> {#code-filename-code-span-class-version-mark-new-in-v5-4-0-span}

-   ログファイル。この設定項目が設定されていない場合、ログはデフォルトで「stderr」に出力されます。この設定項目が設定されている場合、ログは対応するファイルに出力されます。
-   デフォルト値: `""`

### <code>max-size</code> <span class="version-mark">v5.4.0の新</span>機能 {#code-max-size-code-span-class-version-mark-new-in-v5-4-0-span}

-   単一ログファイルの最大サイズ。ファイルサイズがこの設定項目で設定された値よりも大きい場合、システムは自動的に単一ファイルを複数のファイルに分割します。
-   デフォルト値: `300`
-   最大値: `4096`
-   単位: MiB

### <code>max-days</code> <span class="version-mark">（v5.4.0の新機能）</span> {#code-max-days-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKVがログファイルを保持する最大日数。
    -   設定項目が設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKV はログファイルをクリーンアップしません。
    -   パラメータが`0`以外の値に設定されている場合、TiKV は`max-days`の後に期限切れのログファイルをクリーンアップします。
-   デフォルト値: `0`

### <code>max-backups</code> <span class="version-mark">v5.4.0の新機能</span> {#code-max-backups-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiKVが保持するログファイルの最大数。
    -   設定項目が設定されていない場合、またはその値がデフォルト値`0`に設定されている場合、TiKV はすべてのログ ファイルを保持します。
    -   設定項目が`0`以外の値に設定されている場合、TiKV は`max-backups`で指定された数までの古いログファイルを保持します。たとえば、値が`7`に設定されている場合、TiKV は最大 7 つの古いログファイルを保持します。
-   デフォルト値: `0`

## サーバー {#server}

-   サーバーに関連するコンフィグレーション項目。

### <code>addr</code> {#code-addr-code}

-   リスニングIPアドレスとリスニングポート
-   デフォルト値: `"127.0.0.1:20160"`

### <code>advertise-addr</code> {#code-advertise-addr-code}

-   顧客とのコミュニケーションのためのリスニングアドレスを宣伝する
-   この設定項目が設定されていない場合、 `addr`の値が使用されます。
-   デフォルト値: `""`

### <code>status-addr</code> {#code-status-addr-code}

-   構成アイテムは`HTTP`アドレスを介して TiKV ステータスを直接報告します。

    > **警告：**
    >
    > この値が一般に公開されると、TiKVサーバーの状態情報が漏洩する可能性があります。

-   ステータス アドレスを無効にするには、値を`""`に設定します。

-   デフォルト値: `"127.0.0.1:20180"`

### <code>status-thread-pool-size</code> {#code-status-thread-pool-size-code}

-   `HTTP` APIサービスのワーカースレッド数
-   デフォルト値: `1`
-   最小値: `1`

### <code>grpc-compression-type</code> {#code-grpc-compression-type-code}

-   gRPCメッセージの圧縮アルゴリズム。TiKVノード間のgRPCメッセージに影響します。v6.5.11、v7.1.6、v7.5.3、v8.1.1、v8.2.0以降では、TiKVからTiDBに送信されるgRPC応答メッセージにも影響します。

-   オプション値: `"none"` 、 `"deflate"` 、 `"gzip"`

    > **注記：**
    >
    > TiDB は`"deflate"`をサポートしていません。したがって、TiKV から TiDB に送信される gRPC 応答メッセージを圧縮する場合は、この設定項目を`"gzip"`に設定してください。

-   デフォルト値: `"none"`

### <code>grpc-concurrency</code> {#code-grpc-concurrency-code}

-   gRPC ワーカー スレッドの数。 gRPC スレッド プールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。

-   デフォルト値:

    -   v8.5.4以降、デフォルト値は`grpc-raft-conn-num * 3 + 2`に調整され、 [`grpc-raft-conn-num`](#grpc-raft-conn-num)の値に基づいて計算されます。たとえば、CPUコア数が8の場合、 `grpc-raft-conn-num`のデフォルト値は1になります。したがって、 `grpc-concurrency`のデフォルト値は`1 * 3 + 2 = 5`になります。
    -   v8.5.3以前のバージョンでは、デフォルト値は`5`です。

-   最小値: `1`

### <code>grpc-concurrent-stream</code> {#code-grpc-concurrent-stream-code}

-   gRPCストリームで許可される同時リクエストの最大数
-   デフォルト値: `1024`
-   最小値: `1`

### <code>grpc-memory-pool-quota</code> {#code-grpc-memory-pool-quota-code}

-   gRPCが使用できるメモリサイズを制限します。
-   デフォルト値：制限なし
-   メモリ不足が発生した場合に備えて、メモリを制限してください。ただし、使用量を制限すると、処理が停止する可能性があることに注意してください。

### <code>grpc-raft-conn-num</code> {#code-grpc-raft-conn-num-code}

-   Raft通信におけるTiKVノード間の最大接続数

-   デフォルト値:

    -   バージョン8.5.4以降、デフォルト値は`MAX(1, MIN(4, CPU cores / 8))`に調整されます。ここで`MIN(4, CPU cores / 8)`は、CPUコア数が32以上の場合、デフォルトの最大接続数が4であることを示します。
    -   v8.5.3以前のバージョンでは、デフォルト値は`1`です。

-   最小値: `1`

### <code>max-grpc-send-msg-len</code> {#code-max-grpc-send-msg-len-code}

-   送信可能なgRPCメッセージの最大長を設定します。
-   デフォルト値: `10485760`
-   単位：バイト
-   最大値: `2147483647`

### <code>grpc-stream-initial-window-size</code> {#code-grpc-stream-initial-window-size-code}

-   gRPCストリームのウィンドウサイズ
-   デフォルト値: `2MiB`
-   単位：KiB｜MiB｜GiB
-   最小値: `"1KiB"`

### <code>grpc-keepalive-time</code> {#code-grpc-keepalive-time-code}

-   そのgRPCが`keepalive` Pingメッセージを送信する時間間隔
-   デフォルト値: `"10s"`
-   最小値: `"1s"`

### <code>grpc-keepalive-timeout</code> {#code-grpc-keepalive-timeout-code}

-   gRPCストリームのタイムアウトを無効にします
-   デフォルト値: `"3s"`
-   最小値: `"1s"`

### <code>graceful-shutdown-timeout</code> <span class="version-mark">（v8.5.5の新機能）</span> {#code-graceful-shutdown-timeout-code-span-class-version-mark-new-in-v8-5-5-span}

-   TiKVの正常シャットダウンのタイムアウト期間を指定します。
    -   この値が`0s`より大きい場合、TiKV はシャットダウンする前に、指定されたタイムアウト時間内にこのノード上のすべてのリーダーを他の TiKV ノードに転送しようとします。タイムアウトに達した時点で転送されていないリーダーがまだ存在する場合、TiKV は残りのリーダー転送をスキップし、直接シャットダウン処理に進みます。
    -   この値が`0s`の場合、TiKV の正常シャットダウンは無効になります。
-   デフォルト値: `"20s"`
-   最小値: `"0s"`

### <code>concurrent-send-snap-limit</code> {#code-concurrent-send-snap-limit-code}

-   同時に送信できるスナップショットの最大数
-   デフォルト値: `32`
-   最小値: `1`

### <code>concurrent-recv-snap-limit</code> {#code-concurrent-recv-snap-limit-code}

-   同時に受信できるスナップショットの最大数
-   デフォルト値: `32`
-   最小値: `1`

### <code>end-point-recursion-limit</code> {#code-end-point-recursion-limit-code}

-   TiKVがコプロセッサーDAG式をデコードする際に許可される再帰レベルの最大数
-   デフォルト値: `1000`
-   最小値: `1`

### <code>end-point-request-max-handle-duration</code> {#code-end-point-request-max-handle-duration-code}

-   TiDBからTiKVへの処理タスクのプッシュダウン要求に許容される最長期間
-   デフォルト値: `"60s"`
-   最小値: `"1s"`

### <code>end-point-memory-quota</code> <span class="version-mark">v8.2.0 の新機能</span> {#code-end-point-memory-quota-code-span-class-version-mark-new-in-v8-2-0-span}

-   TiKVコプロセッサーのリクエストが使用できるメモリの最大容量。この制限を超えると、以降のコプロセッサーのリクエストは「サーバーがビジー状態です」というエラーで拒否されます。
-   デフォルト値：システムメモリ全体の12.5%と500MiBのうち大きい方の値。

### <code>snap-io-max-bytes-per-sec</code> {#code-snap-io-max-bytes-per-sec-code}

-   スナップショット処理時の最大許容ディスク帯域幅
-   デフォルト値: `"100MiB"`
-   単位：KiB｜MiB｜GiB
-   最小値: `"1KiB"`

### <code>snap-min-ingest-size</code> <span class="version-mark">v8.1.2の新機能</span> {#code-snap-min-ingest-size-code-span-class-version-mark-new-in-v8-1-2-span}

-   スナップショットを処理する際に、TiKVが取り込み方式を採用するかどうかの最小しきい値を指定します。

    -   スナップショットのサイズがこのしきい値を超えると、TiKVは取り込み方式を採用し、スナップショットからSSTファイルをRocksDBにインポートします。この方式は、大きなファイルの場合に高速です。
    -   スナップショットのサイズがこのしきい値を超えない場合、TiKVは直接書き込み方式を採用し、各データを個別にRocksDBに書き込みます。この方式は、小さなファイルに対してより効率的です。

-   デフォルト値: `"2MiB"`

-   単位：KiB｜MiB｜GiB

-   最小値: `0`

### <code>enable-request-batch</code> {#code-enable-request-batch-code}

-   リクエストをバッチ処理するかどうかを決定します。
-   デフォルト値: `true`

### <code>labels</code> {#code-labels-code}

-   `{ zone = "us-west-1", disk = "ssd" }`などのサーバー属性を指定します。
-   デフォルト値: `{}`

### <code>background-thread-count</code> {#code-background-thread-count-code}

-   エンドポイントスレッド、 BRスレッド、スプリットチェックスレッド、リージョンスレッド、および遅延に影響されないタスクのその他のスレッドを含む、バックグラウンドプールの稼働スレッド数。
-   デフォルト値: CPU コア数が 16 未満の場合、デフォルト値は`2`です。それ以外の場合は、デフォルト値は`3`です。

### <code>end-point-slow-log-threshold</code> {#code-end-point-slow-log-threshold-code}

-   TiDBのプッシュダウン要求がスローログを出力するまでの時間しきい値。処理時間がこのしきい値を超えると、スローログが出力されます。
-   デフォルト値: `"1s"`
-   最小値: `0`

### <code>raft-client-queue-size</code> {#code-raft-client-queue-size-code}

-   TiKVにおけるRaftメッセージのキューサイズを指定します。送信期限内に送信されないメッセージが多すぎてバッファがいっぱいになったり、メッセージが破棄されたりする場合は、より大きな値を指定することでシステムの安定性を向上させることができます。
-   デフォルト値: `16384`

### <code>simplify-metrics</code> <span class="version-mark">v6.2.0の新機能</span> {#code-simplify-metrics-code-span-class-version-mark-new-in-v6-2-0-span}

-   返される監視メトリクスを簡略化するかどうかを指定します。値を`true`に設定すると、TiKV は一部のメトリクスをフィルタリングすることで、各リクエストに対して返されるデータ量を削減します。
-   デフォルト値: `false`

### <code>forward-max-connections-per-address</code> <span class="version-mark">v5.0.0 で追加</span> {#code-forward-max-connections-per-address-code-span-class-version-mark-new-in-v5-0-0-span}

-   サービスおよびサーバーへのリクエスト転送に使用する接続プールのサイズを設定します。値を小さく設定しすぎると、リクエストのレイテンシーや負荷分散に影響が出ます。
-   デフォルト値: `4`

### <code>inspect-network-interval</code> <span class="version-mark">（v8.5.5で追加）</span> {#code-inspect-network-interval-code-span-class-version-mark-new-in-v8-5-5-span}

-   TiKV HealthChecker が PD や他の TiKV ノードに対してネットワーク検出をアクティブに実行する間隔を制御します。TiKV はネットワーク検出結果に基づいて`NetworkSlowScore`を計算し、低速ノードのネットワーク状態を PD に報告します。
-   この値を`0`に設定すると、ネットワーク検出が無効になります。値を小さく設定すると検出頻度が高くなり、ネットワークジッターをより迅速に検出できるようになりますが、ネットワーク帯域幅と CPU リソースの消費量も増加します。
-   デフォルト値: `100ms`
-   値の範囲: `0`または`[10ms, +∞)`

## リードプール.unified {#readpool-unified}

読み取り要求を処理するシングルスレッドプールに関連するコンフィグレーション項目。このスレッドプールは、バージョン4.0以降、従来のstorageスレッドプールとコプロセッサスレッドプールに取って代わるものです。

### <code>min-thread-count</code> {#code-min-thread-count-code}

-   統合リードプールの最小動作スレッド数
-   デフォルト値: `1`

### <code>max-thread-count</code> {#code-max-thread-count-code}

-   統合読み取りプールまたは UnifyReadPool スレッド プールの最大作業スレッド数。このスレッド プールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   値の範囲: `[min-thread-count, MAX(4, CPU quota * 10)]` 。 `MAX(4, CPU quota * 10)`は`4`と`CPU quota * 10`からより大きな値を取得します。
-   デフォルト値: MAX(4, CPU * 0.8)

> **注記：**
>
> スレッド数を増やすとコンテキストスイッチの回数が増え、パフォーマンスが低下する可能性があります。この設定項目の値を変更することは推奨されません。

### <code>stack-size</code> {#code-stack-size-code}

-   統合スレッドプール内のスレッドのスタックサイズ
-   型: 整数 + 単位
-   デフォルト値: `"10MiB"`
-   単位：KiB｜MiB｜GiB
-   最小値: `"2MiB"`
-   最大値: システムで実行された`ulimit -sH`コマンドの結果として出力される Kバイト数。

### <code>max-tasks-per-worker</code> {#code-max-tasks-per-worker-code}

-   統合読み取りプール内の単一スレッドで許可されるタスクの最大数。この値を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>auto-adjust-pool-size</code> <span class="version-mark">v6.3.0で追加）</span> {#code-auto-adjust-pool-size-code-span-class-version-mark-new-in-v6-3-0-span}

-   スレッドプールのサイズを自動的に調整するかどうかを制御します。有効にすると、現在の CPU 使用率に基づいて UnifyReadPool スレッドプールのサイズを自動的に調整することで、TiKV の読み取りパフォーマンスが最適化されます。スレッドプールの可能な範囲は`[max-thread-count, MAX(4, CPU)]`です。最大値は[`max-thread-count`](#max-thread-count)と同じです。
-   デフォルト値: `false`

### <code>cpu-threshold</code> <span class="version-mark">v8.5.5で追加</span> {#code-cpu-threshold-code-span-class-version-mark-new-in-v8-5-5-span}

-   統合読み取りプールのCPU使用率のしきい値を指定します。たとえば、この値を`0.8`に設定すると、スレッドプールはCPUの最大80%を使用できます。

    -   デフォルトでは（ `0.0`の場合）、統合読み取りプールの CPU 使用率に制限はありません。スレッドプールのサイズは、ビジースレッドスケーリングアルゴリズムによってのみ決定され、現在のタスクを処理するスレッド数に基づいてサイズが動的に調整されます。
    -   `0.0`より大きい値に設定されている場合、TiKVは既存のビジースレッドスケーリングアルゴリズムに加えて、CPUリソースの使用量をより厳密に制御するために、以下のCPU使用率しきい値制約を適用します。
        -   強制的なスケールダウン：統合読み取りプールのCPU使用率が設定値に10%のバッファを加えた値を超えると、TiKVはプールのサイズを強制的に縮小します。
        -   スケールアップ防止：統合リードプールを拡張すると、CPU使用率が設定されたしきい値から10%のバッファを引いた値を超える場合、TiKVは統合リードプールのそれ以上の拡張を防止します。

-   この機能は、 [`readpool.unified.auto-adjust-pool-size`](#auto-adjust-pool-size-new-in-v630) `true`に設定されている場合にのみ有効になります。

-   デフォルト値: `0.0`

-   値の範囲: `[0.0, 1.0]`

## リードプール。storage {#readpool-storage}

storageスレッドプールに関連するコンフィグレーション項目。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   storage要求に統合スレッドプール（ [`readpool.unified`](#readpoolunified)で構成）を使用するかどうかを決定します。このパラメーターの値が`false`の場合、このセクションの残りのパラメーター（ `readpool.storage` ）で構成された別のスレッドプールが使用されます。
-   デフォルト値: このセクション ( `readpool.storage` ) に他の設定がない場合、デフォルト値は`true`です。それ以外の場合は、下位互換性のために、デフォルト値は`false`です。このオプションを有効にする前に、必要に応じて[`readpool.unified`](#readpoolunified)の設定を変更してください。

### <code>high-concurrency</code> {#code-high-concurrency-code}

-   優先度の高い`read`リクエストを処理する同時実行スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>normal-concurrency</code> {#code-normal-concurrency-code}

-   通常優先度`read`リクエストを処理する同時実行スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>low-concurrency</code> {#code-low-concurrency-code}

-   優先度の低い`read`リクエストを処理する同時実行スレッドの許容数
-   `8` ≤ `cpu num` ≤ `16`の場合、デフォルト値は`cpu_num * 0.5`です。 `cpu num`が`8`より小さい場合、デフォルト値は`4`です。 `cpu num`が`16`より大きい場合、デフォルト値は`8`です。
-   最小値: `1`

### <code>max-tasks-per-worker-high</code> {#code-max-tasks-per-worker-high-code}

-   高優先度スレッドプール内の単一スレッドで許可されるタスクの最大数。この値を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-normal</code> {#code-max-tasks-per-worker-normal-code}

-   通常優先度スレッドプールにおいて、1つのスレッドで実行可能なタスクの最大数。この値を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-low</code> {#code-max-tasks-per-worker-low-code}

-   低優先度スレッドプール内の単一スレッドで許可されるタスクの最大数。この値を超えると`Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>stack-size</code> {#code-stack-size-code}

-   ストレージ読み取りスレッドプール内のスレッドのスタックサイズ
-   型: 整数 + 単位
-   デフォルト値: `"10MiB"`
-   単位：KiB｜MiB｜GiB
-   最小値: `"2MiB"`
-   最大値: システムで実行された`ulimit -sH`コマンドの結果として出力される Kバイト数。

## <code>readpool.coprocessor</code> {#code-readpool-coprocessor-code}

コプロセッサースレッドプールに関連するコンフィグレーション項目。

### <code>use-unified-pool</code> {#code-use-unified-pool-code}

-   コプロセッサ要求に統合スレッドプール（ [`readpool.unified`](#readpoolunified)で構成）を使用するかどうかを決定します。このパラメータの値が`false`の場合、このセクションの残りのパラメータ（ `readpool.coprocessor` ）で構成された別のスレッドプールが使用されます。
-   デフォルト値: このセクションのパラメータ ( `readpool.coprocessor` ) がいずれも設定されていない場合、デフォルト値は`true`です。それ以外の場合は、下位互換性のためにデフォルト値は`false`になります。このパラメータを有効にする前に、 [`readpool.unified`](#readpoolunified)の設定項目を調整してください。

### <code>high-concurrency</code> {#code-high-concurrency-code}

-   チェックポイントなどの優先度の高いコプロセッサー要求を処理する同時実行スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>normal-concurrency</code> {#code-normal-concurrency-code}

-   通常優先度のコプロセッサー要求を処理する同時実行スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>low-concurrency</code> {#code-low-concurrency-code}

-   テーブルスキャンなどの低優先度コプロセッサー要求を処理する同時実行スレッドの許容数
-   デフォルト値: `CPU * 0.8`
-   最小値: `1`

### <code>max-tasks-per-worker-high</code> {#code-max-tasks-per-worker-high-code}

-   高優先度スレッドプール内の単一スレッドに許可されるタスク数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-normal</code> {#code-max-tasks-per-worker-normal-code}

-   通常優先度スレッドプールにおいて、1つのスレッドで実行可能なタスク数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>max-tasks-per-worker-low</code> {#code-max-tasks-per-worker-low-code}

-   低優先度スレッドプール内の単一スレッドに許可されるタスク数。この数を超えると、 `Server Is Busy`が返されます。
-   デフォルト値: `2000`
-   最小値: `2`

### <code>stack-size</code> {#code-stack-size-code}

-   コプロセッサースレッドプール内のスレッドのスタックサイズ
-   型: 整数 + 単位
-   デフォルト値: `"10MiB"`
-   単位：KiB｜MiB｜GiB
-   最小値: `"2MiB"`
-   最大値: システムで実行された`ulimit -sH`コマンドの結果として出力される Kバイト数。

## storage {#storage}

storageに関連するコンフィグレーション項目。

### <code>data-dir</code> {#code-data-dir-code}

-   RocksDBディレクトリのstorageパス
-   デフォルト値: `"./"`

### <code>engine</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-engine-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   エンジンタイプを指定します。この設定は、新しいクラスターを作成する際にのみ指定でき、一度指定すると変更できません。
-   デフォルト値: `"raft-kv"`
-   お得なオプション：

    -   `"raft-kv"` : TiDB v6.6.0 より前のバージョンにおけるデフォルトのエンジンタイプ。
    -   `"partitioned-raft-kv"` : TiDB v6.6.0 で導入された新しいstorageエンジン タイプ。

### <code>scheduler-concurrency</code> {#code-scheduler-concurrency-code}

-   キーに対する同時操作を防止するための内蔵メモリロック機構。各キーは異なるスロットにハッシュ値が格納されている。
-   デフォルト値: `524288`
-   最小値: `1`

### <code>scheduler-worker-pool-size</code> {#code-scheduler-worker-pool-size-code}

-   スケジューラのスレッド プール内のスレッドの数。スケジューラ スレッドは主に、データの書き込み前にトランザクションの整合性をチェックするために使用されます。 CPU コアの数が`16`以上の場合、デフォルト値は`8`です。それ以外の場合、デフォルト値は`4`です。スケジューラ スレッド プールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `4`
-   値の範囲: `[1, MAX(4, CPU)]` 。 `MAX(4, CPU)`では、 `CPU`は CPU コアの数を意味します。 `MAX(4, CPU)`は`4`と`CPU`のうち大きい方の値を取得します。

### <code>scheduler-pending-write-threshold</code> {#code-scheduler-pending-write-threshold-code}

-   書き込みキューの最大サイズ。この値を超えると、TiKVへの新規書き込みに対して`Server Is Busy`エラーが返されます。
-   デフォルト値: `"100MiB"`
-   単位：MiB｜GiB

### <code>enable-async-apply-prewrite</code> {#code-enable-async-apply-prewrite-code}

-   非同期コミットトランザクションが、プリライト要求を適用する前にTiKVクライアントに応答するかどうかを決定します。この設定項目を有効にすると、適用時間が長い場合はレイテンシーを容易に短縮でき、適用時間が不安定な場合は遅延ジッターを低減できます。
-   デフォルト値: `false`

### <code>reserve-space</code> {#code-reserve-space-code}

-   TiKVが起動すると、ディスク保護のためにディスク上に一定量の領域が確保されます。残りのディスク容量が確保された領域よりも少ない場合、TiKVは一部の書き込み操作を制限します。確保された領域は2つの部分に分けられます。80%はディスク容量が不足した場合の操作に必要な追加ディスク容量として使用され、残りの20%は一時ファイルの保存に使用されます。領域解放の過程で、追加ディスク容量を使いすぎてstorageが枯渇した場合、この一時ファイルがサービス復旧のための最後の保護手段として機能します。
-   一時ファイルの名前は`space_placeholder_file`で、 `storage.data-dir`ディレクトリにあります。ディスク容量不足で TiKV がオフラインになった場合、TiKV を再起動すると、一時ファイルは自動的に削除され、TiKV は空き容量の確保を試みます。
-   残りの空き容量が不足している場合、TiKV は一時ファイルを作成しません。保護の有効性は、予約領域のサイズに関係します。予約領域のサイズは、ディスク容量の 5% とこの構成値のうち大きい方の値です。この構成項目が`0`またはサポートされている単位のゼロ値 (たとえば、 `0KiB` 、 `0MiB` 、または`0GiB` ) に設定されている場合、TiKV はこのディスク保護機能を無効にします。
-   デフォルト値: `"5GiB"`
-   単位: B|KB|KiB|MB|MiB|GB|GiB|TB|TiB|PB|PiB

### <code>enable-ttl</code> {#code-enable-ttl-code}

> **警告：**
>
> -   `enable-ttl`を`true`または`false`に設定してください。**既存**の TiKV クラスターでは、この構成項目の値を変更**しないでください**。 `enable-ttl`値が異なる TiKV クラスターでは、使用するデータ形式が異なります。そのため、既存の TiKV クラスターでこの項目の値を変更すると、クラスターはデータを異なる形式で保存するため、TiKV クラスターを再起動すると「非 TTL で TTL を有効にできません」というエラーが発生します。
> -   `enable-ttl` TiKV クラスタ**でのみ**使用して**ください**。TiDB ノードを含むクラスタ (つまり、そのようなクラスタでは`enable-ttl`を`true`に設定する) では、 `storage.api-version = 2`が設定されていない限り、この構成項目を使用しないでください。そうしないと、データの破損や TiDB クラスタのアップグレード失敗などの重大な問題が発生します。

-   [TTL](/time-to-live.md) 「Time to live（有効期限）」の略です。この項目を有効にすると、TiKVはTTLに達したデータを自動的に削除します。TTLの値を設定するには、クライアント経由でデータを書き込む際のリクエストで指定する必要があります。TTLが指定されていない場合、TiKVは該当するデータを自動的に削除しません。
-   デフォルト値: `false`

### <code>ttl-check-poll-interval</code> {#code-ttl-check-poll-interval-code}

-   物理領域を解放するためにデータをチェックする間隔。データがTTL（有効期限）に達すると、TiKVはチェック中に強制的に物理領域を解放します。
-   デフォルト値: `"12h"`
-   最小値: `"0s"`

### <code>background-error-recovery-window</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-background-error-recovery-window-code-span-class-version-mark-new-in-v6-1-0-span}

-   RocksDBが回復可能なバックグラウンドエラーを検出した後、TiKVが回復するまでの最大許容時間。バックグラウンドSSTファイルの一部が破損した場合、RocksDBは破損したSSTファイルが属するピアを特定した後、ハートビートを介してPDに報告します。PDはスケジューリング操作を実行してこのピアを削除します。最後に、破損したSSTファイルが直接削除され、TiKVのバックグラウンドは再び正常に動作するようになります。
-   リカバリが完了するまで、破損したSSTファイルはまだ存在しています。この間、RocksDBはデータの書き込みを継続できますが、破損したデータ部分を読み取ろうとするとエラーが報告されます。
-   この時間枠内にリカバリが完了しない場合、TiKV はpanicになります。
-   デフォルト値: 1時間

### <code>api-version</code> <span class="version-mark">v6.1.0で追加</span> {#code-api-version-code-span-class-version-mark-new-in-v6-1-0-span}

-   TiKVがRawKVストアとして機能する際にTiKVが使用するstorageフォーマットとインターフェースバージョン。
-   お得なオプション：
    -   `1` : API V1 を使用し、クライアントから渡されたデータをエンコードせず、そのまま保存します。バージョン 6.1.0 より前の TiKV では、デフォルトで API V1 が使用されます。
    -   `2` : API V2 を使用します:
        -   データは[マルチバージョン同時実行制御 (MVCC)](/glossary.md#multi-version-concurrency-control-mvcc)形式で保存され、タイムスタンプは tikv-server によって PD (TSO) から取得されます。
        -   データはさまざまな用途に応じて範囲が定められており、API V2では、単一のクラスタ内でTiDB、トランザクションKV、およびRawKVアプリケーションが共存することをサポートしています。
        -   API V2 を使用する場合は、 `storage.enable-ttl = true`も同時に設定する必要があります。API V2 は TTL 機能をサポートしているため、 [`enable-ttl`](#enable-ttl)明示的に有効にする必要があります。そうしないと、 `storage.enable-ttl`が`false`にデフォルト設定されるため、競合が発生します。
        -   API V2を有効にする場合、不要になったデータを再利用するために、少なくとも1つのtidb-serverインスタンスをデプロイする必要があります。このtidb-serverインスタンスは、読み取りサービスと書き込みサービスを同時に提供できます。高可用性を確保するため、複数のtidb-serverインスタンスをデプロイすることも可能です。
        -   API V2ではクライアント側のサポートが必要です。詳細は、API V2に対応したクライアントの取扱説明書を参照してください。
        -   バージョン6.2.0以降、RawKVの変更データキャプチャ（CDC）がサポートされています。RawKV [RawKV CDC](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc)を参照してください。
-   デフォルト値: `1`

> **警告：**

> -   API V1 と API V2 はstorage形式が異なります。 TiKV に TiDB データのみが含まれている場合に**のみ**、API V2 を直接有効または無効にできます。他のシナリオでは、新しいクラスターをデプロイし、 [RawKVのバックアップと復元](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)復元を使用してデータを移行する必要があります。
> -   API V2を有効にした後は、TiKVクラスターをv6.1.0より前のバージョンにダウングレードする**ことはできません**。ダウングレードすると、データ破損が発生する可能性があります。

## <code>txn-status-cache-capacity</code> <span class="version-mark">（v7.6.0で追加）</span> {#code-txn-status-cache-capacity-code-span-class-version-mark-new-in-v7-6-0-span}

-   TiKVにおけるトランザクションステータスキャッシュの容量を設定します。このパラメータは変更しないでください。
-   デフォルト値: `5120000`

## storage.block-cache {#storage-block-cache}

複数の RocksDBカラムファミリー (CF) 間でブロックキャッシュを共有することに関連するコンフィグレーション項目。

### <code>capacity</code> {#code-capacity-code}

-   共有ブロックキャッシュのサイズ。

-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値はシステムメモリ全体のサイズの 45% です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値はシステムメモリ全体のサイズの 30% です。

-   単位：KiB｜MiB｜GiB

### <code>low-pri-pool-ratio</code> <span class="version-mark">v8.0.0で追加</span> {#code-low-pri-pool-ratio-code-span-class-version-mark-new-in-v8-0-0-span}

-   Titanコンポーネントが使用できるブロックキャッシュ全体の割合を制御します。
-   デフォルト値: `0.2`

## storage.フロー制御 {#storage-flow-control}

TiKVにおけるフロー制御メカニズムに関連するコンフィグレーション項目。このメカニズムはRocksDBの書き込み停止メカニズムに代わるもので、スケジューラレイヤーでのフローを制御することで、 RaftstoreやApplyスレッドの停止によって引き起こされる二次的な障害を回避します。

### <code>enable</code> {#code-enable-code}

-   フロー制御メカニズムを有効にするかどうかを決定します。有効にすると、TiKV は KvDB の書き込み停止メカニズムと RaftDB の書き込み停止メカニズム (memtable を除く) を自動的に無効にします。
-   デフォルト値: `true`

### <code>memtables-threshold</code> {#code-memtables-threshold-code}

-   kvDB の memtable の数がこのしきい値に達すると、フロー制御メカニズムが動作を開始します。 `enable`が`true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).max-write-buffer-number`を上書きします。
-   デフォルト値: `5`

### <code>l0-files-threshold</code> {#code-l0-files-threshold-code}

-   kvDB L0ファイルの数がこのしきい値に達すると、フロー制御メカニズムが作動を開始します。

    > **注記：**
    >
    > 特定の条件下では、この構成項目は`rocksdb.(defaultcf|writecf|lockcf|raftcf).level0-slowdown-writes-trigger`の値を上書きできます。詳細については、 [`rocksdb.(defaultcf|writecf|lockcf|raftcf).level0-slowdown-writes-trigger`](/tikv-configuration-file.md#level0-slowdown-writes-trigger)参照してください。

-   デフォルト値: `20`

### <code>soft-pending-compaction-bytes-limit</code> {#code-soft-pending-compaction-bytes-limit-code}

-   KvDB の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムは一部の書き込み要求を拒否し始め、 `ServerIsBusy`エラーを報告します。

    > **注記：**
    >
    > 特定の条件下では、この構成項目は`rocksdb.(defaultcf|writecf|lockcf|raftcf).soft-pending-compaction-bytes-limit`の値を上書きできます。詳細については、 [`rocksdb.(defaultcf|writecf|lockcf|raftcf).soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit-1)参照してください。

-   デフォルト値: `"192GiB"`

### <code>hard-pending-compaction-bytes-limit</code> {#code-hard-pending-compaction-bytes-limit-code}

-   KvDB の保留中の圧縮バイトがこのしきい値に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し、 `ServerIsBusy`エラーを報告します。 `enable`が`true`に設定されている場合、この構成項目は`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`を上書きします。
-   デフォルト値: `"1024GiB"`

## storage.io-rate-limit {#storage-io-rate-limit}

I/Oレートリミッターに関連するコンフィグレーション項目。

### <code>max-bytes-per-sec</code> {#code-max-bytes-per-sec-code}

-   サーバーがディスクに書き込んだり、ディスクから読み取ったりできる最大I/Oバイト数を1秒間に制限します（この制限値は、下記の`mode`設定項目で決定されます）。この制限に達すると、TiKVはフォアグラウンド操作よりもバックグラウンド操作を優先的にスロットリングします。この設定項目の値は、ディスクの最適なI/O帯域幅（例えば、クラウドディスクベンダーが指定する最大I/O帯域幅）に設定する必要があります。この設定値をゼロに設定すると、ディスクI/O操作は制限されません。
-   デフォルト値: `"0MiB"`

### <code>mode</code> {#code-mode-code}

-   `max-bytes-per-sec`しきい値未満でカウントおよび制限されるI/O操作の種類を決定します。現在、書き込み専用モードのみがサポートされています。
-   値のオプション: `"read-only"` 、 `"write-only"` 、および`"all-io"`
-   デフォルト値: `"write-only"`

## pd {#pd}

### <code>enable-forwarding</code> <span class="version-mark">v5.0.0の新機能</span> {#code-enable-forwarding-code-span-class-version-mark-new-in-v5-0-0-span}

-   TiKVのPDクライアントが、ネットワークが隔離された可能性がある場合に、フォロワーを介してリーダーにリクエストを転送するかどうかを制御します。
-   デフォルト値: `false`
-   環境が孤立したネットワークである可能性がある場合、このパラメータを有効にすることで、サービスが利用できなくなる時間を短縮できます。
-   隔離、ネットワーク障害、またはダウンタイムが発生したかどうかを正確に判断できない場合、このメカニズムを使用すると誤判断のリスクがあり、可用性とパフォーマンスが低下します。ネットワーク障害が一度も発生したことがない場合は、このパラメータを有効にすることは推奨されません。

### <code>endpoints</code> {#code-endpoints-code}

-   PDのエンドポイント。複数のエンドポイントを指定する場合は、カンマで区切る必要があります。
-   デフォルト値: `["127.0.0.1:2379"]`

### <code>retry-interval</code> {#code-retry-interval-code}

-   PD接続を再試行する間隔。
-   デフォルト値: `"300ms"`

### <code>retry-log-every</code> {#code-retry-log-every-code}

-   PDクライアントがエラーを検出した際に、エラー報告をスキップする頻度を指定します。たとえば、値が`5`の場合、PDクライアントはエラーを検出した後、4回ごとにエラー報告をスキップし、5回ごとにエラーを報告します。
-   この機能を無効にするには、値を`1`に設定してください。
-   デフォルト値: `10`

### <code>retry-max-count</code> {#code-retry-max-count-code}

-   PD接続の初期化を再試行する最大回数
-   再試行を無効にするには、値を`0`に設定します。再試行回数の制限を解除するには、値を`-1`に設定します。
-   デフォルト値: `-1`

## ラフトストア {#raftstore}

Raftstoreに関連するコンフィグレーション項目。

### <code>prevote</code> {#code-prevote-code}

-   `prevote`を有効または無効にします。この機能を有効にすると、ネットワークパーティションからのリカバリ後のシステム上のジッターを軽減するのに役立ちます。
-   デフォルト値: `true`

### <code>capacity</code> {#code-capacity-code}

-   storage容量。データを保存できる最大サイズです。 `capacity`を指定しない場合、現在のディスクの容量が優先されます。複数の TiKV インスタンスを同じ物理ディスクにデプロイするには、このパラメータを TiKV 構成に追加します。詳細については、 [ハイブリッド展開の主要パラメータ](/hybrid-deployment-topology.md#key-parameters)を参照してください。
-   デフォルト値: `0`
-   単位：KiB｜MiB｜GiB

### <code>raftdb-path</code> {#code-raftdb-path-code}

-   Raftライブラリへのパス（デフォルトでは`storage.data-dir/raft`
-   デフォルト値: `""`

### <code>raft-base-tick-interval</code> {#code-raft-base-tick-interval-code}

> **注記：**
>
> この設定項目はSQL文による照会はできませんが、設定ファイル内で設定できます。

-   Raftステートマシンがティックする時間間隔
-   デフォルト値: `"1s"`
-   最小値: `0`より大きい

### <code>raft-heartbeat-ticks</code> {#code-raft-heartbeat-ticks-code}

> **注記：**
>
> この設定項目はSQL文による照会はできませんが、設定ファイル内で設定できます。

-   ハートビートが送信されるまでの経過ティック数。これは、 `raft-base-tick-interval` * `raft-heartbeat-ticks` の時間間隔でハートビートが送信`raft-heartbeat-ticks` 。
-   デフォルト値: `2`
-   最小値: `0`より大きい

### <code>raft-election-timeout-ticks</code> {#code-raft-election-timeout-ticks-code}

> **注記：**
>
> この設定項目はSQL文による照会はできませんが、設定ファイル内で設定できます。

-   Raft選挙が開始されるまでに経過したティック数。これは、 Raftグループにリーダーがいない場合、リーダー選挙が約`raft-base-tick-interval` * `raft-election-timeout-ticks`の時間間隔後に開始されることを意味します。
-   デフォルト値: `10`
-   最小値: `raft-heartbeat-ticks`

### <code>raft-min-election-timeout-ticks</code> {#code-raft-min-election-timeout-ticks-code}

> **注記：**
>
> この設定項目はSQL文による照会はできませんが、設定ファイル内で設定できます。

-   Raft選挙が開始される最小ティック数。この数が`0`の場合、 `raft-election-timeout-ticks`の値が使用されます。このパラメータの値は`raft-election-timeout-ticks`以上でなければなりません。
-   デフォルト値: `0`
-   最小値: `0`

### <code>raft-max-election-timeout-ticks</code> {#code-raft-max-election-timeout-ticks-code}

> **注記：**
>
> この設定項目はSQL文による照会はできませんが、設定ファイル内で設定できます。

-   Raft選挙が開始される最大ティック数。この数が`0`の場合、 `raft-election-timeout-ticks` * `2`の値が使用されます。
-   デフォルト値: `0`
-   最小値: `0`

### <code>raft-max-size-per-msg</code> {#code-raft-max-size-per-msg-code}

-   単一メッセージパケットのサイズに対するソフトリミット
-   デフォルト値: `"1MiB"`
-   最小値: `0`より大きい
-   最大値: `3GiB`
-   単位：KiB｜MiB｜GiB

### <code>raft-max-inflight-msgs</code> {#code-raft-max-inflight-msgs-code}

-   確認が必要なRaftログの数。この数を超えると、 Raftステートマシンはログ送信を遅くします。
-   デフォルト値: `256`
-   最小値: `0`より大きい
-   最大値: `16384`

### <code>raft-entry-max-size</code> {#code-raft-entry-max-size-code}

-   丸太1本の最大サイズに対する厳格な制限
-   デフォルト値: `"8MiB"`
-   最小値: `0`
-   単位：MiB｜GiB

### <code>raft-log-compact-sync-interval</code> <span class="version-mark">v5.3で追加</span> {#code-raft-log-compact-sync-interval-code-span-class-version-mark-new-in-v5-3-span}

-   不要ないかだの丸太を圧縮する時間間隔
-   デフォルト値: `"2s"`
-   最小値: `"0s"`

### <code>raft-log-gc-tick-interval</code> {#code-raft-log-gc-tick-interval-code}

-   Raftログを削除するポーリング タスクがスケジュールされる時間間隔。 `0`この機能が無効になっていることを意味します。
-   デフォルト値: `"3s"`
-   最小値: `"0s"`

### <code>raft-log-gc-threshold</code> {#code-raft-log-gc-threshold-code}

-   残存するRaftの最大許容数に関するソフトリミット
-   デフォルト値: `50`
-   最小値: `1`

### <code>raft-log-gc-count-limit</code> {#code-raft-log-gc-count-limit-code}

-   残存するRaftの許容数の上限
-   デフォルト値：各ログが1 KiBであると仮定して計算された、リージョンサイズの4分の3に収まるログの数
-   最小値: `0`

### <code>raft-log-gc-size-limit</code> {#code-raft-log-gc-size-limit-code}

-   残余いかだRaftの許容サイズに関する厳格な制限
-   デフォルト値：リージョンサイズの3/4
-   最小値: `0`より大きい

### <code>raft-log-reserve-max-ticks</code> <span class="version-mark">v5.3の新機能</span> {#code-raft-log-reserve-max-ticks-code-span-class-version-mark-new-in-v5-3-span}

-   この設定項目で設定されたティック数が経過した後、残存するRaftログの数が`raft-log-gc-threshold`で設定された値に達しない場合でも、TiKV はこれらのログに対してガベージコレクション(GC) を実行します。
-   デフォルト値: `6`
-   最小値: `0`より大きい

### <code>raft-engine-purge-interval</code> {#code-raft-engine-purge-interval-code}

-   ディスク容量をできるだけ早く再利用するために、古いTiKVログファイルをパージする間隔。RaftRaftは交換可能なコンポーネントであるため、一部の実装ではパージ処理が必要です。
-   デフォルト値: `"10s"`

### <code>raft-entry-cache-life-time</code> {#code-raft-entry-cache-life-time-code}

-   メモリ内のログキャッシュに許容される最大残り時間
-   デフォルト値: `"30s"`
-   最小値: `0`

### <code>max-apply-unpersisted-log-limit</code> <span class="version-mark">v8.1.0 で追加されました。</span> {#code-max-apply-unpersisted-log-limit-code-span-class-version-mark-new-in-v8-1-0-span}

-   適用可能な、コミット済みだが永続化されていないRaftログの最大数。

    -   この設定項目を`0`より大きい値に設定すると、TiKVノードはコミット済みだが永続化されていないRaftログを事前に適用できるようになり、そのノードでのIOジッターによって発生するロングテールレイテンシーを効果的に削減できます。ただし、TiKVのメモリ使用量とRaftログが占めるディスク容量が増加する可能性もあります。
    -   この設定項目を`0`に設定すると、この機能が無効になります。つまり、TiKV はRaftログがコミットされ、かつ永続化されるまで待機してから適用する必要があります。この動作は、v8.2.0 より前のバージョンの動作と一致しています。

-   デフォルト値: `1024`

-   最小値: `0`

### <code>hibernate-regions</code> {#code-hibernate-regions-code}

-   リージョンの休止リージョンを有効または無効にします。このオプションを有効にすると、長時間アイドル状態が続くリージョンは自動的に休止状態になります。これにより、アイドル状態のリージョンについて、 Raftリーダーとフォロワー間のハートビートメッセージによって発生する余分なオーバーヘッドが軽減されます。休止状態のリージョンのリーダーとフォロワー間のハートビート間隔は`peer-stale-state-check-interval`を使用して変更できます。
-   デフォルト値: v5.0.2 以降のバージョンでは`true` 、v5.0.2 より前のバージョンでは`false`

### <code>split-region-check-tick-interval</code> {#code-split-region-check-tick-interval-code}

-   リージョン分割が必要かどうかを確認する間隔を指定します。 `0`この機能が無効になっていることを意味します。
-   デフォルト値: `"10s"`
-   最小値: `0`

### <code>region-split-check-diff</code> {#code-region-split-check-diff-code}

-   リージョン分割前にリージョンデータが超過できる最大値
-   デフォルト値：リージョンサイズの1/16。
-   最小値: `0`

### <code>region-compact-check-interval</code> {#code-region-compact-check-interval-code}

> **警告：**
>
> v7.5.7およびv8.5.4以降、この設定項目は非推奨となり、 [`gc.auto-compaction.check-interval`](#check-interval-new-in-v757-and-v854)に置き換えられました。

-   RocksDB の圧縮を手動でトリガーする必要があるかどうかを確認する時間間隔。 `0`この機能が無効になっていることを意味します。
-   デフォルト値: `"5m"`
-   最小値: `0`

### <code>region-compact-check-step</code> {#code-region-compact-check-step-code}

> **警告：**
>
> バージョン7.5.7および8.5.4以降、この設定項目は非推奨となりました。

-   手動圧縮の各ラウンドで一度にチェックされるリージョンの数
-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値は`100`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`5`です。
-   最小値: `0`

### <code>region-compact-min-tombstones</code> {#code-region-compact-min-tombstones-code}

> **警告：**
>
> バージョン7.5.7および8.5.4以降、この設定項目は非推奨となり、 [`gc.auto-compaction.tombstone-num-threshold`](#tombstone-num-threshold-new-in-v757-and-v854)に置き換えられました。

-   RocksDBの圧縮をトリガーするために必要な墓石の数
-   デフォルト値: `10000`
-   最小値: `0`

### <code>region-compact-tombstones-percent</code> {#code-region-compact-tombstones-percent-code}

> **警告：**
>
> バージョン7.5.7および8.5.4以降、この設定項目は非推奨となり、 [`gc.auto-compaction.tombstone-percent-threshold`](#tombstone-percent-threshold-new-in-v757-and-v854)に置き換えられました。

-   RocksDBの圧縮をトリガーするために必要な墓石の割合
-   デフォルト値: `30`
-   最小値: `1`
-   最大値: `100`

### <code>region-compact-min-redundant-rows</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-region-compact-min-redundant-rows-code-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> バージョン7.5.7および8.5.4以降、この設定項目は非推奨となり、 [`gc.auto-compaction.redundant-rows-threshold`](#redundant-rows-threshold-new-in-v757-and-v854)に置き換えられました。

-   RocksDBのコンパクションをトリガーするために必要な冗長なMVCC行の数。
-   デフォルト値: `50000`
-   最小値: `0`

### <code>region-compact-redundant-rows-percent</code> <span class="version-mark">v7.1.0の新機能</span> {#code-region-compact-redundant-rows-percent-code-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> v7.5.7 および v8.5.4 以降、この設定項目は非推奨となり、 [`gc.auto-compaction.redundant-rows-percent-threshold`](#redundant-rows-percent-threshold-new-in-v757-and-v854)に置き換えられました。

-   RocksDBのコンパクションをトリガーするために必要な、冗長なMVCC行の割合。
-   デフォルト値: `20`
-   最小値: `1`
-   最大値: `100`

### <code>report-region-buckets-tick-interval</code> <span class="version-mark">v6.1.0で追加</span> {#code-report-region-buckets-tick-interval-code-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> `report-region-buckets-tick-interval`は、TiDB v6.1.0 で導入された実験的機能です。本番環境での使用は推奨されません。

-   `enable-region-bucket`が真の場合に、TiKVがバケット情報をPDに報告する間隔。
-   デフォルト値: `10s`

### <code>pd-heartbeat-tick-interval</code> {#code-pd-heartbeat-tick-interval-code}

-   リージョンからPDへのハートビートがトリガーされる時間間隔。 `0`この機能が無効になっていることを意味します。
-   デフォルト値: `"1m"`
-   最小値: `0`

### <code>pd-store-heartbeat-tick-interval</code> {#code-pd-store-heartbeat-tick-interval-code}

-   店舗からPDへのハートビートがトリガーされる時間間隔。 `0`この機能が無効になっていることを意味します。
-   デフォルト値: `"10s"`
-   最小値: `0`

### <code>pd-report-min-resolved-ts-interval</code> <span class="version-mark">v7.6.0で追加</span> {#code-pd-report-min-resolved-ts-interval-code-span-class-version-mark-new-in-v7-6-0-span}

> **注記：**
>
> この設定項目は、 [`report-min-resolved-ts-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file/#report-min-resolved-ts-interval-new-in-v600)から名前が変更されました。v7.6.0 以降、 `report-min-resolved-ts-interval`は無効になりました。

-   TiKVが解決済みTSをPDリーダーに報告する最小間隔を指定します。これを`0`に設定すると、報告が無効になります。
-   デフォルト値: `"1s"`は、最小の正の値です。v6.3.0 より前のバージョンでは、デフォルト値は`"0s"`でした。
-   最小値: `0`
-   単位：秒

### <code>snap-mgr-gc-tick-interval</code> {#code-snap-mgr-gc-tick-interval-code}

-   期限切れのスナップショットファイルのリサイクルがトリガーされる時間間隔。 `0`この機能が無効になっていることを意味します。
-   デフォルト値: `"1m"`
-   最小値: `0`

### <code>snap-gc-timeout</code> {#code-snap-gc-timeout-code}

-   スナップショットファイルが保存される最長期間
-   デフォルト値: `"4h"`
-   最小値: `0`

### <code>snap-generator-pool-size</code> <span class="version-mark">v5.4.0の新機能</span> {#code-snap-generator-pool-size-code-span-class-version-mark-new-in-v5-4-0-span}

-   `snap-generator`スレッドプールのサイズを設定します。
-   TiKV のリカバリシナリオでリージョンがスナップショットをより高速に生成できるようにするには、対応するワーカーの`snap-generator`スレッドの数を増やす必要があります。この構成項目を使用して、 `snap-generator`スレッド プールのサイズを増やすことができます。
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

-   リージョンメッセージキューの最長。
-   デフォルト値: `40960`
-   最小値: `0`

### <code>messages-per-tick</code> {#code-messages-per-tick-code}

-   バッチごとに処理されるメッセージの最大数
-   デフォルト値: `4096`
-   最小値: `0`

### <code>max-peer-down-duration</code> {#code-max-peer-down-duration-code}

-   ピアに許容される最長の非アクティブ期間。タイムアウトしたピアは`down`とマークされ、PD は後でそれを削除しようとします。
-   デフォルト値: `"10m"`
-   最小値: Hibernate リージョンが有効になっている場合、最小値は`peer-stale-state-check-interval * 2`です。Hibernate リージョンが無効になっている場合、最小値は`0`です。

### <code>max-leader-missing-duration</code> {#code-max-leader-missing-duration-code}

-   Raftグループのリーダーが存在しない状態がピアに許容される最長期間。この値を超えると、ピアはPDに対してピアが削除されたかどうかを確認します。
-   デフォルト値: `"2h"`
-   最小値: `abnormal-leader-missing-duration`より大きい

### <code>abnormal-leader-missing-duration</code> {#code-abnormal-leader-missing-duration-code}

-   Raftグループのリーダーが存在しない状態がピアに許容される最長期間。この値を超えると、ピアは異常とみなされ、メトリクスとログに記録されます。
-   デフォルト値: `"10m"`
-   最小値: `peer-stale-state-check-interval`より大きい

### <code>peer-stale-state-check-interval</code> {#code-peer-stale-state-check-interval-code}

-   Raftグループにリーダーが存在しない状態にあるかどうかをチェックするトリガーとなる時間間隔。
-   デフォルト値: `"5m"`
-   最小値: `2 * election-timeout`より大きい

### <code>leader-transfer-max-log-lag</code> {#code-leader-transfer-max-log-lag-code}

-   Raftリーダーの交代時に、譲受人に許可される欠落ログの最大数
-   デフォルト値: `128`
-   最小値: `10`

### <code>max-snapshot-file-raw-size</code> <span class="version-mark">v6.1.0で追加</span> {#code-max-snapshot-file-raw-size-code-span-class-version-mark-new-in-v6-1-0-span}

-   スナップショットファイルのサイズがこの設定値を超えると、そのファイルは複数のファイルに分割されます。
-   デフォルト値: `100MiB`
-   最小値: `100MiB`

### <code>snap-apply-batch-size</code> {#code-snap-apply-batch-size-code}

-   インポートされたスナップショットファイルがディスクに書き込まれる際に必要なメモリキャッシュサイズ
-   デフォルト値: `"10MiB"`
-   最小値: `0`
-   単位: MiB

### <code>consistency-check-interval</code> {#code-consistency-check-interval-code}

> **警告：**
>
> クラスタのパフォーマンスに影響を与え、TiDBのガベージコレクションと互換性がないため、本番環境では整合性チェックを有効にすることは推奨され**ません**。

-   整合性チェックがトリガーされる時間間隔。 `0`この機能が無効になっていることを意味します。
-   デフォルト値: `"0s"`
-   最小値: `0`

### <code>raft-store-max-leader-lease</code> {#code-raft-store-max-leader-lease-code}

-   Raftリーダーとして最も長く信頼された期間
-   デフォルト値: `"9s"`
-   最小値: `0`

### <code>right-derive-when-split</code> {#code-right-derive-when-split-code}

-   リージョンが分割されたときに、新しいリージョンの開始キーを指定します。この設定項目が`true`に設定されている場合、開始キーは最大分割キーになります。この設定項目が`false`に設定されている場合、開始キーは元のリージョンの開始キーになります。
-   デフォルト値: `true`

### <code>merge-max-log-gap</code> {#code-merge-max-log-gap-code}

-   `merge`が実行されたときに許容される欠落ログの最大数
-   デフォルト値: `10`
-   最小値: `raft-log-gc-count-limit`より大きい

### <code>merge-check-tick-interval</code> {#code-merge-check-tick-interval-code}

-   TiKVがリージョンのマージが必要かどうかを確認する時間間隔
-   デフォルト値: `"2s"`
-   最小値: `0`より大きい

### <code>use-delete-range</code> {#code-use-delete-range-code}

-   `rocksdb delete_range`インターフェースからデータを削除するかどうかを決定します。
-   デフォルト値: `false`

### <code>cleanup-import-sst-interval</code> {#code-cleanup-import-sst-interval-code}

-   期限切れの SST ファイルがチェックされる時間間隔。 `0`この機能が無効になっていることを意味します。
-   デフォルト値: `"10m"`
-   最小値: `0`

### <code>local-read-batch-size</code> {#code-local-read-batch-size-code}

-   1バッチで処理される読み取りリクエストの最大数
-   デフォルト値: `1024`
-   最小値: `0`より大きい

### <code>apply-yield-write-size</code> <span class="version-mark">v6.4.0で追加</span> {#code-apply-yield-write-size-code-span-class-version-mark-new-in-v6-4-0-span}

-   Applyスレッドが1回のポーリングで1つのFSM（有限状態機械）に対して書き込むことができる最大バイト数。これはソフトリミットです。
-   デフォルト値: `"32KiB"`
-   最小値: `0`より大きい
-   単位：KiB｜MiB｜GiB

### <code>apply-max-batch-size</code> {#code-apply-max-batch-size-code}

-   Raftステートマシンは、BatchSystemによってデータ書き込み要求をバッチ処理します。この設定項目は、1つのバッチで要求を処理できるRaftステートマシンの最大数を指定します。
-   デフォルト値: `256`
-   最小値: `0`より大きい
-   最大値: `10240`

### <code>apply-pool-size</code> {#code-apply-pool-size-code}

-   データをディスクにフラッシュするプール内のスレッドの許容数。これは、適用スレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `2`
-   値の範囲: `[1, CPU * 10]` 。 `CPU` CPU コアの数を表します。

### <code>store-max-batch-size</code> {#code-store-max-batch-size-code}

-   Raftステートマシンは、BatchSystemによってログをディスクに書き込む要求をバッチ処理します。この設定項目は、1つのバッチで要求を処理できるRaftステートマシンの最大数を指定します。
-   `hibernate-regions`が有効になっている場合、デフォルト値は`256`です。 `hibernate-regions`が無効になっている場合、デフォルト値は`1024`です。
-   最小値: `0`より大きい
-   最大値: `10240`

### <code>store-pool-size</code> {#code-store-pool-size-code}

-   Raftを処理するプール内のスレッドの許容数。これはRaftstoreスレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `2`
-   値の範囲: `[1, CPU * 10]` 。 `CPU` CPU コアの数を表します。

### <code>store-io-pool-size</code> <span class="version-mark">v5.3.0で追加</span> {#code-store-io-pool-size-code-span-class-version-mark-new-in-v5-3-0-span}

-   Raft I/O タスクを処理するスレッドの許容数。これは StoreWriter スレッド プールのサイズです。このスレッド プールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `1` (v8.0.0 より前のバージョンでは、デフォルト値は`0`でした)
-   最小値: `0`

### <code>future-poll-size</code> {#code-future-poll-size-code}

-   `future`を駆動するスレッドの許容数
-   デフォルト値: `1`
-   最小値: `0`より大きい

### <code>cmd-batch</code> {#code-cmd-batch-code}

-   リクエストのバッチ処理を有効にするかどうかを制御します。有効にすると、書き込みパフォーマンスが大幅に向上します。
-   デフォルト値: `true`

### <code>inspect-interval</code> {#code-inspect-interval-code}

-   TiKVは一定間隔でRaftstoreコンポーネントのレイテンシーを検査します。このパラメータは検査間隔を指定します。レイテンシーがこの値を超えると、この検査はタイムアウトとしてマークされます。
-   タイムアウト検査の比率に基づいて、TiKVノードが遅いかどうかを判断します。
-   デフォルト値: `"100ms"`
-   最小値: `"1ms"`

### <code>raft-write-size-limit</code> <span class="version-mark">v5.3.0で追加</span> {#code-raft-write-size-limit-code-span-class-version-mark-new-in-v5-3-0-span}

-   Raftデータがディスクに書き込まれるしきい値を決定します。データサイズがこの構成項目の値よりも大きい場合、データはディスクに書き込まれます。 `store-io-pool-size`の値が`0`の場合、この構成項目は有効になりません。
-   デフォルト値: `1MiB`
-   最小値: `0`

### <code>evict-cache-on-memory-ratio</code> <span class="version-mark">（v7.5.0で追加）</span> {#code-evict-cache-on-memory-ratio-code-span-class-version-mark-new-in-v7-5-0-span}

-   TiKV のメモリ使用量がシステムで使用可能なメモリの 90% を超え、 Raftエントリ キャッシュによって占有されているメモリが使用済みメモリ* `evict-cache-on-memory-ratio`を超えると、TiKV はRaftエントリ キャッシュを追い出します。
-   この値が`0`に設定されている場合、この機能は無効になっています。
-   デフォルト値: `0.1`
-   最小値: `0`

### <code>periodic-full-compact-start-times</code> <span class="version-mark">（v7.6.0の新機能）</span> {#code-periodic-full-compact-start-times-code-span-class-version-mark-new-in-v7-6-0-span}

> **警告：**
>
> 定期的な完全圧縮は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   TiKVが定期的な完全圧縮を開始する具体的な時刻を設定します。配列で複数の時刻スケジュールを指定できます。例：
    -   `periodic-full-compact-start-times = ["03:00", "23:00"]`は、TiKVノードの現地時間に基づいて、TiKVが毎日午前3時と午後11時に完全な圧縮を実行することを示しています。
    -   `periodic-full-compact-start-times = ["03:00 +0000", "23:00 +0000"]`は、TiKVがUTCタイムゾーンで毎日午前3時と午後11時に完全な圧縮を実行することを示しています。
    -   `periodic-full-compact-start-times = ["03:00 +0800", "23:00 +0800"]`は、TiKVがUTC+08:00タイムゾーンで毎日午前3時と午後11時に完全な圧縮を実行することを示しています。
-   デフォルト値: `[]`は、定期的な完全圧縮がデフォルトで無効になっていることを意味します。

### <code>periodic-full-compact-start-max-cpu</code><span class="version-mark">は v7.6.0 で追加されました。</span> {#code-periodic-full-compact-start-max-cpu-code-span-class-version-mark-new-in-v7-6-0-span}

-   TiKVの定期的な完全圧縮におけるCPU使用率の上限を制限します。
-   デフォルト値: `0.1` 、定期的な圧縮処理の最大 CPU 使用率が 10% であることを意味します。

### <code>follower-read-max-log-gap</code> <span class="version-mark">v7.4.0の新機能</span> {#code-follower-read-max-log-gap-code-span-class-version-mark-new-in-v7-4-0-span}

-   フォロワーが読み取りリクエストを処理する際に、遅延が許容されるログの最大数。この制限を超えると、読み取りリクエストは拒否されます。
-   デフォルト値: `100`

### <code>inspect-cpu-util-thd</code> <span class="version-mark">v7.6.0 で追加されました。</span> {#code-inspect-cpu-util-thd-code-span-class-version-mark-new-in-v7-6-0-span}

-   低速ノード検出時に、TiKVノードがビジー状態かどうかを判断するためのCPU使用率のしきい値。
-   値の範囲: `[0, 1]`
-   デフォルト値: `0.4` 、つまり`40%`です。

### <code>inspect-kvdb-interval</code> <span class="version-mark">v8.1.2で追加</span> {#code-inspect-kvdb-interval-code-span-class-version-mark-new-in-v8-1-2-span}

-   TiKV の低速ノード検出時に KV ディスクをチェックする間隔とタイムアウト。KVDB と RaftDB が同じマウント パスを共有している場合、この値は`0` (検出なし) で上書きされます。
-   デフォルト値: `100ms` 。v8.5.2 以前のバージョンでは、デフォルト値は`2s`です。

### <code>min-pending-apply-region-count</code> <span class="version-mark">v8.0.0で追加</span> {#code-min-pending-apply-region-count-code-span-class-version-mark-new-in-v8-0-0-span}

-   TiKV起動時にRaftログ適用中のビジー状態にあるリージョンの最大数。Raftstoreは、このようなリージョンの数がこの値以下の場合にのみリーダー転送を受け入れ、ローリング再起動時の可用性低下を軽減します。
-   デフォルト値: `10`

### <code>request-voter-replicated-index-interval</code> <span class="version-mark">v6.6.0で追加</span> {#code-request-voter-replicated-index-interval-code-span-class-version-mark-new-in-v6-6-0-span}

-   Witnessノードが定期的に投票ノードから複製されたRaftログの位置を取得する間隔を制御します。
-   デフォルト値： `5m` 、これは5分を意味します。

### <code>slow-trend-unsensitive-cause</code> <span class="version-mark">v6.6.0の新機能</span> {#code-slow-trend-unsensitive-cause-code-span-class-version-mark-new-in-v6-6-0-span}

-   TiKVがSlowTrend検出アルゴリズムを使用する場合、この設定項目はレイテンシー検出の感度を制御します。値が大きいほど感度は低くなります。
-   デフォルト値: `10`

### <code>slow-trend-unsensitive-result</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-slow-trend-unsensitive-result-code-span-class-version-mark-new-in-v6-6-0-span}

-   TiKVがSlowTrend検出アルゴリズムを使用する場合、この設定項目はQPS検出の感度を制御します。値が大きいほど感度は低くなります。
-   デフォルト値: `0.5`

## コプロセッサ {#coprocessor}

コプロセッサーに関連するコンフィグレーション項目。

### <code>split-region-on-table</code> {#code-split-region-on-table-code}

-   リージョンをテーブルごとに分割するかどうかを決定します。この機能はTiDBモードでのみ使用することをお勧めします。
-   デフォルト値: `false`

### <code>batch-split-limit</code> {#code-batch-split-limit-code}

-   バッチ処理におけるリージョン分割のしきい値。この値を大きくすると、リージョン分割が高速化されます。
-   デフォルト値: `10`
-   最小値: `1`

### <code>region-max-size</code> {#code-region-max-size-code}

-   リージョンの最大サイズ。この値を超えると、リージョンは複数のリージョンに分割されます。
-   デフォルト値: `region-split-size / 2 * 3`
-   単位：KiB｜MiB｜GiB

### <code>region-split-size</code> {#code-region-split-size-code}

-   分割後のリージョンのサイズ。この値は概算値です。
-   デフォルト値: `"256MiB"` 。v8.4.0 より前のバージョンでは、デフォルト値は`"96MiB"`です。
-   単位：KiB｜MiB｜GiB

### <code>region-max-keys</code> {#code-region-max-keys-code}

-   リージョン内で許容されるキーの最大数。この値を超えると、リージョンは複数のリージョンに分割されます。
-   デフォルト値: `region-split-keys / 2 * 3`

### <code>region-split-keys</code> {#code-region-split-keys-code}

-   新しく分割されたリージョン内のキーの数。この値は概算値です。
-   デフォルト値: `2560000` 。v8.4.0 より前のバージョンでは、デフォルト値は`960000`です。

### <code>consistency-check-method</code> {#code-consistency-check-method-code}

-   データ整合性チェックの方法を指定します。
-   MVCCデータの整合性チェックの場合は、値を`"mvcc"`に設定します。生データの整合性チェックの場合は、値を`"raw"`に設定します。
-   デフォルト値: `"mvcc"`

## コプロセッサv2 {#coprocessor-v2}

### <code>coprocessor-plugin-directory</code> {#code-coprocessor-plugin-directory-code}

-   コンパイル済みのコプロセッサプラグインが格納されているディレクトリのパス。このディレクトリ内のプラグインはTiKVによって自動的にロードされます。
-   この設定項目が設定されていない場合、コプロセッサプラグインは無効になります。
-   デフォルト値: なし

### <code>enable-region-bucket</code> <span class="version-mark">v6.1.0の新機能</span> {#code-enable-region-bucket-code-span-class-version-mark-new-in-v6-1-0-span}

-   リージョンをバケットと呼ばれる小さな範囲に分割するかどうかを決定します。バケットは、スキャンの同時実行性を向上させるために同時クエリの単位として使用されます。バケットの設計の詳細については、 [動的サイズリージョン](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md)を参照してください。
-   デフォルト値：なし。これは、デフォルトで無効になっていることを意味します。

> **警告：**
>
> -   `enable-region-bucket`は、TiDB v6.1.0 で導入された実験的機能です。本番環境での使用は推奨されません。
> -   この設定は、 `region-split-size` `region-bucket-size`の 2 倍以上である場合にのみ有効です。それ以外の場合は、バケットは実際には生成されません。
> -   `region-split-size`をより大きな値に調整すると、パフォーマンスの低下やスケジューリングの遅延のリスクが生じる可能性があります。

### <code>region-bucket-size</code> <span class="version-mark">v6.1.0の新機能</span> {#code-region-bucket-size-code-span-class-version-mark-new-in-v6-1-0-span}

-   `enable-region-bucket`が true の場合のバケットのサイズ。
-   デフォルト値: v7.3.0 以降、デフォルト値は`96MiB`から`50MiB`に変更されました。

> **警告：**
>
> `region-bucket-size`は、TiDB v6.1.0 で導入された実験的機能です。本番環境での使用は推奨されません。

## rocksdb {#rocksdb}

RocksDBに関連するコンフィグレーション項目

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDB のバックグラウンド スレッドの数。 RocksDB スレッド プールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値:
    -   CPUコア数が10の場合、デフォルト値は`9`です。
    -   CPUコア数が8の場合、デフォルト値は`7`です。
    -   CPUコア数が`N`の場合、デフォルト値は`max(2, min(N - 1, 9))`です。
-   最小値: `2`

### <code>max-background-flushes</code> {#code-max-background-flushes-code}

-   同時実行可能なバックグラウンド memtable フラッシュ ジョブの最大数
-   デフォルト値:
    -   CPUコア数が10の場合、デフォルト値は`3`です。
    -   CPUコア数が8の場合、デフォルト値は`2`です。
    -   CPUコア数が`N`の場合、デフォルト値は`[(max-background-jobs + 3) / 4]`です。
-   最小値: `1`

### <code>max-sub-compactions</code> {#code-max-sub-compactions-code}

-   RocksDBで同時に実行されたサブコンパクション操作の数
-   デフォルト値: `3`
-   最小値: `1`

### <code>max-open-files</code> {#code-max-open-files-code}

-   RocksDBが開くことができるファイルの総数
-   デフォルト値: `40960`
-   最小値: `-1`

### <code>max-manifest-file-size</code> {#code-max-manifest-file-size-code}

-   RocksDBマニフェストファイルの最大サイズ
-   デフォルト値: `"256MiB"` 。v8.5.3 およびそれ以前の v8.5.x バージョンでは、デフォルト値は`"128MiB"`です。
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>create-if-missing</code> {#code-create-if-missing-code}

-   DBスイッチを自動的に作成するかどうかを決定します
-   デフォルト値: `true`

### <code>wal-recovery-mode</code> {#code-wal-recovery-mode-code}

-   WALリカバリモード
-   オプション値:
    -   `"tolerate-corrupted-tail-records"` : すべてのログで不完全な末尾データを持つレコードを許容し、破棄します。
    -   `"absolute-consistency"` : 破損したログが見つかった場合、リカバリを中止します
    -   `"point-in-time"` : 破損したログが最初に見つかるまで、ログを順次復元します。
    -   `"skip-any-corrupted-records"` :ディザスタリカバリ。データは可能な限り復旧され、破損したレコードはスキップされます。
-   デフォルト値: `"point-in-time"`

### <code>wal-dir</code> {#code-wal-dir-code}

-   WALファイルが保存されるディレクトリ。指定しない場合、WALファイルはデータと同じディレクトリに保存されます。
-   デフォルト値: `""`

### <code>wal-ttl-seconds</code> {#code-wal-ttl-seconds-code}

-   アーカイブされたWALファイルの有効期間。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位：秒

### <code>wal-size-limit</code> {#code-wal-size-limit-code}

-   アーカイブされたWALファイルのサイズ制限。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>max-total-wal-size</code> {#code-max-total-wal-size-code}

-   RocksDB WAL の最大サイズは合計で、 `*.log`内の`data-dir`ファイルのサイズです。
-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値は`"4GiB"`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`1`です。

### <code>stats-dump-period</code> {#code-stats-dump-period-code}

-   統計情報がログに出力される間隔。
-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値は`"10m"`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`"0"`です。

### <code>compaction-readahead-size</code> {#code-compaction-readahead-size-code}

-   RocksDBの圧縮処理中に先読み機能を有効にし、先読みデータのサイズを指定します。機械式ディスクを使用している場合は、値を少なくとも2MiBに設定することをお勧めします。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>writable-file-max-buffer-size</code> {#code-writable-file-max-buffer-size-code}

-   WritableFileWriteで使用される最大バッファサイズ
-   デフォルト値: `"1MiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>use-direct-io-for-flush-and-compaction</code> {#code-use-direct-io-for-flush-and-compaction-code}

-   バックグラウンドのフラッシュと圧縮における読み取りと書き込みの両方で`O_DIRECT`を使用するかどうかを決定します。このオプションのパフォーマンスへの影響: `O_DIRECT`を有効にすると、OS バッファ キャッシュの汚染がバイパスされ防止されますが、後続のファイル読み取りではバッファ キャッシュの内容を再読み込みする必要があります。
-   デフォルト値: `false`

### <code>rate-bytes-per-sec</code> {#code-rate-bytes-per-sec-code}

-   Titanが無効になっている場合、この設定項目はRocksDB圧縮のI/Oレートを制限し、トラフィックのピーク時にRocksDB圧縮がフォアグラウンドの読み取りおよび書き込みパフォーマンスに与える影響を軽減します。Titanが有効になっている場合、この設定項目はRocksDB圧縮とTitan GCの合計I/Oレートを制限します。RocksDB圧縮とTitan GCのI/OまたはCPU消費量が大きすぎる場合は、ディスクI/O帯域幅と実際の書き込みトラフィックに応じて、この設定項目を適切な値に設定してください。
-   デフォルト値: `10GiB`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>rate-limiter-refill-period</code> {#code-rate-limiter-refill-period-code}

-   I/Oトークンの補充頻度を制御します。値を小さくするとI/Oバーストは減少しますが、CPU負荷が増加します。
-   デフォルト値: `"100ms"`

### <code>rate-limiter-mode</code> {#code-rate-limiter-mode-code}

-   RocksDBの圧縮速度制限モード
-   オプション値: `"read-only"` 、 `"write-only"` 、 `"all-io"`
-   デフォルト値: `"write-only"`

### <code>rate-limiter-auto-tuned</code> <span class="version-mark">v5.0の新機能</span> {#code-rate-limiter-auto-tuned-code-span-class-version-mark-new-in-v5-0-span}

-   最近のワークロードに基づいて、RocksDBの圧縮レート制限設定を自動的に最適化するかどうかを決定します。この設定を有効にすると、圧縮待ちバイト数が通常よりも若干多くなります。
-   デフォルト値: `true`

### <code>enable-pipelined-write</code> {#code-enable-pipelined-write-code}

-   パイプライン書き込みを有効にするかどうかを制御します。この設定を有効にすると、従来のパイプライン書き込みが使用されます。この設定を無効にすると、新しいパイプラインコミットメカニズムが使用されます。
-   デフォルト値: `false`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   OSがファイルをディスクに増分的に同期する速度（これらのファイルが非同期的に書き込まれている間）
-   デフォルト値: `"1MiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>wal-bytes-per-sync</code> {#code-wal-bytes-per-sync-code}

-   OSがWALファイルの書き込み中にWALファイルをディスクに増分同期する速度
-   デフォルト値: `"512KiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>info-log-max-size</code> {#code-info-log-max-size-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.file.max-size`](#max-size-new-in-v540)に置き換えられました。

-   情報ログの最大サイズ
-   デフォルト値: `"1GiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>info-log-roll-time</code> {#code-info-log-roll-time-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBログはTiKVのログモジュールによって管理されるようになりました。そのため、この設定項目は非推奨です。TiKVは時間に基づく自動ログ分割をサポートしなくなりました。代わりに、設定項目[`log.file.max-size`](#max-size-new-in-v540)使用して、ファイルサイズに基づく自動ログ分割のしきい値を設定できます。

-   Infoログが切り捨てられる時間間隔。値が`0s`の場合、ログは切り捨てられません。
-   デフォルト値: `"0s"`

### <code>info-log-keep-log-file-num</code> {#code-info-log-keep-log-file-num-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.file.max-backups`](#max-backups-new-in-v540)に置き換えられました。

-   保持されるログファイルの最大数
-   デフォルト値: `10`
-   最小値: `0`

### <code>info-log-dir</code> {#code-info-log-dir-code}

-   ログが保存されるディレクトリ
-   デフォルト値: `""`

### <code>info-log-level</code> {#code-info-log-level-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.level`](#level-new-in-v540)に置き換えられました。

-   RocksDBのログレベル
-   デフォルト値: `"info"`

### <code>write-buffer-flush-oldest-first</code><span class="version-mark">は v6.6.0 で追加されました。</span> {#code-write-buffer-flush-oldest-first-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   現在の RocksDB の`memtable`のメモリ使用量がしきい値に達したときに使用されるフラッシュ戦略を指定します。
-   デフォルト値: `false`
-   お得なオプション：

    -   `false` : データ量が最も大きい`memtable`が SST ファイルに書き込まれます。
    -   `true` : 最も早い`memtable`が SST ファイルに書き込まれます。この戦略により`memtable`からコールドデータを消去できるため、コールドデータとホットデータが明確に存在するシナリオに適しています。

### <code>write-buffer-limit</code> <span class="version-mark">v6.6.0 で追加されました。</span> {#code-write-buffer-limit-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   単一の TiKV 内のすべての RocksDB インスタンスの合計メモリ制限を`memtable`に指定します。 `0`制限なしを意味します。

-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値は none で、制限なしを意味します。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値はシステムメモリ全体のサイズの 20% です。

-   単位：KiB｜MiB｜GiB

### <code>track-and-verify-wals-in-manifest</code> <span class="version-mark">、v6.5.9、v7.1.5、v7.5.2、v8.0.0 で新しく追加されました。</span> {#code-track-and-verify-wals-in-manifest-code-span-class-version-mark-new-in-v6-5-9-v7-1-5-v7-5-2-and-v8-0-0-span}

-   RocksDB MANIFEST ファイルに先行書き込みログ (WAL) ファイルに関する情報を記録するかどうか、および起動時に WAL ファイルの整合性を検証するかどうかを制御します。詳細については、「RocksDB [MANIFESTでWALを追跡する](https://github.com/facebook/rocksdb/wiki/Track-WAL-in-MANIFEST)参照してください。
-   デフォルト値: `true`
-   お得なオプション：
    -   `true` : WAL ファイルに関する情報を MANIFEST ファイルに記録し、起動時に WAL ファイルの整合性を検証します。
    -   `false` : WAL ファイルに関する情報を MANIFEST ファイルに記録せず、起動時に WAL ファイルの整合性を検証しません。

### <code>enable-multi-batch-write</code> <span class="version-mark">v6.2.0 で追加されました。</span> {#code-enable-multi-batch-write-code-span-class-version-mark-new-in-v6-2-0-span}

-   RocksDBの書き込み最適化を有効にするかどうかを制御します。有効にすると、WriteBatchの内容をmemtableに同時に書き込むことができ、書き込みレイテンシーが削減されます。
-   デフォルト値：なし。ただし、 `false`に明示的に設定するか、 `rocksdb.enable-pipelined-write`または`rocksdb.enable-unordered-write`有効になっている場合を除き、デフォルトで有効になります。

## rocksdb.titan {#rocksdb-titan}

Titanに関連するコンフィグレーション項目。

### <code>enabled</code> {#code-enabled-code}

> **注記：**
>
> -   ワイドテーブルと JSON データの書き込みおよびポイントクエリのパフォーマンスを向上させるため、TiDB v7.6.0 以降、デフォルト値が`false`から`true`に変更され、Titan がデフォルトで有効になります。
> -   既存のクラスターをv7.6.0以降のバージョンにアップグレードした場合、元の構成が保持されます。つまり、Titanが明示的に有効になっていない限り、引き続きRocksDBが使用されます。
> -   クラスターが TiDB v7.6.0 以降のバージョンにアップグレードする前に Titan を有効にしていた場合、アップグレード後も Titan は維持され、アップグレード前の[`min-blob-size`](/tikv-configuration-file.md#min-blob-size)設定も維持されます。アップグレード前に明示的に値を設定しなかった場合、アップグレード後のクラスター構成の安定性を確保するため、以前のバージョンのデフォルト値`1KiB`が維持されます。

-   Titanを有効または無効にします。
-   デフォルト値: `true`

### <code>dirname</code> {#code-dirname-code}

-   Titan Blobファイルが保存されているディレクトリ
-   デフォルト値: `"titandb"`

### <code>disable-gc</code> {#code-disable-gc-code}

-   TitanがBlobファイルに対して実行するガベージコレクション（GC）を無効にするかどうかを決定します。
-   デフォルト値: `false`

### <code>max-background-gc</code> {#code-max-background-gc-code}

-   TitanにおけるGCスレッドの最大数。TiKV**の詳細**&gt;**スレッドCPU** &gt; **RocksDB CPU**パネルで、Titan GCスレッドが長時間フル稼働状態にあることが確認された場合は、Titan GCスレッドプールのサイズを増やすことを検討してください。
-   デフォルト値: `1` 。v8.0.0 より前のバージョンでは、デフォルト値は`4`です。
-   最小値: `1`

## rocksdb.defaultcf | rocksdb.writecf | rocksdb.lockcf | rocksdb.raftcf {#rocksdb-defaultcf-rocksdb-writecf-rocksdb-lockcf-rocksdb-raftcf}

`rocksdb.defaultcf` 、 `rocksdb.writecf` 、および`rocksdb.lockcf`に関連するコンフィグレーション項目。

### <code>block-size</code> {#code-block-size-code}

-   RocksDBブロックのデフォルトサイズ
-   `defaultcf`および`writecf`のデフォルト値: `"32KiB"`
-   `lockcf`のデフォルト値: `"16KiB"`
-   最小値: `"1KiB"`
-   単位：KiB｜MiB｜GiB

### <code>block-cache-size</code> {#code-block-cache-size-code}

> **警告：**
>
> バージョン6.6.0以降、この設定は非推奨となりました。

-   RocksDBブロックのキャッシュサイズ。
-   `defaultcf`のデフォルト値: `Total machine memory * 25%`
-   `writecf`のデフォルト値: `Total machine memory * 15%`
-   `lockcf`のデフォルト値: `Total machine memory * 2%`
-   最小値: `0`
-   単位：KiB｜MiB｜GiB

### <code>disable-block-cache</code> {#code-disable-block-cache-code}

-   ブロックキャッシュを有効または無効にします
-   デフォルト値: `false`

### <code>cache-index-and-filter-blocks</code> {#code-cache-index-and-filter-blocks-code}

-   インデックスとフィルタのキャッシュを有効または無効にします
-   デフォルト値: `true`

### <code>pin-l0-filter-and-index-blocks</code> {#code-pin-l0-filter-and-index-blocks-code}

-   レベル 0 SST ファイルのインデックス ブロックとフィルタ ブロックをメモリに固定するかどうかを決定します。
-   デフォルト値: `true`

### <code>use-bloom-filter</code> {#code-use-bloom-filter-code}

-   ブルームフィルターを有効または無効にします
-   デフォルト値: `true`

### <code>optimize-filters-for-hits</code> {#code-optimize-filters-for-hits-code}

-   フィルターのヒット率を最適化するかどうかを決定します
-   `defaultcf`のデフォルト値: `true`
-   `writecf`および`lockcf`のデフォルト値: `false`

### <code>optimize-filters-for-memory</code> <span class="version-mark">v7.2.0の新機能）</span> {#code-optimize-filters-for-memory-code-span-class-version-mark-new-in-v7-2-0-span}

-   メモリ内部の断片化を最小限に抑えるブルーム/リボンフィルタを生成するかどうかを決定します。
-   この設定項目は、 [`format-version`](#format-version-new-in-v620) 5以上の場合にのみ有効になることに注意してください。
-   デフォルト値: `false`

### <code>whole-key-filtering</code> {#code-whole-key-filtering-code}

-   キー全体をブルームフィルターに適用するかどうかを決定します
-   `defaultcf`および`lockcf`のデフォルト値: `true`
-   `writecf`のデフォルト値: `false`

### <code>bloom-filter-bits-per-key</code> {#code-bloom-filter-bits-per-key-code}

-   ブルームフィルターが各キーに割り当てている長さ
-   デフォルト値: `10`
-   単位：バイト

### <code>block-based-bloom-filter</code> {#code-block-based-bloom-filter-code}

-   各ブロックがブルームフィルターを作成するかどうかを決定します
-   デフォルト値: `false`

### <code>ribbon-filter-above-level</code> <span class="version-mark">v7.2.0の新機能</span> {#code-ribbon-filter-above-level-code-span-class-version-mark-new-in-v7-2-0-span}

-   この値以上のレベルではリボンフィルターを使用し、この値未満のレベルではブロックベースではないブルームフィルターを使用するかどうかを決定します。この設定項目が設定されている場合、 [`block-based-bloom-filter`](#block-based-bloom-filter)無視されます。
-   この設定項目は、 [`format-version`](#format-version-new-in-v620) 5以上の場合にのみ有効になることに注意してください。
-   デフォルト値：なし。これは、デフォルトで無効になっていることを意味します。

### <code>read-amp-bytes-per-bit</code> {#code-read-amp-bytes-per-bit-code}

-   リード増幅の統計情報を有効または無効にします。
-   オプション値: `0` (無効)、&gt; `0` (有効)。
-   デフォルト値: `0`
-   最小値: `0`

### <code>compression-per-level</code> {#code-compression-per-level-code}

-   各レベルのデフォルトの圧縮アルゴリズム
-   `defaultcf`のデフォルト値: [&quot;no&quot;, &quot;no&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;zstd&quot;, &quot;zstd&quot;]
-   `writecf`のデフォルト値: [&quot;no&quot;, &quot;no&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;lz4&quot;, &quot;zstd&quot;, &quot;zstd&quot;]
-   `lockcf`のデフォルト値: [&quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;, &quot;no&quot;]

### <code>bottommost-level-compression</code> {#code-bottommost-level-compression-code}

-   最レイヤーの圧縮アルゴリズムを設定します。この設定項目は`compression-per-level`の設定を上書きします。
-   LSMツリーにデータが書き込まれると、RocksDBは最レイヤーに対して`compression-per-level`配列で指定された最後の圧縮アルゴリズムを直接採用しません。 `bottommost-level-compression`使用すると、最レイヤーは最初から最も圧縮効果の高い圧縮アルゴリズムを使用できます。
-   最レイヤーの圧縮アルゴリズムを設定しない場合は、この設定項目の値を`disable`に設定してください。
-   デフォルト値: `"zstd"`

### <code>write-buffer-size</code> {#code-write-buffer-size-code}

-   Memtableサイズ
-   `defaultcf`および`writecf`のデフォルト値: `"128MiB"`
-   `lockcf`のデフォルト値:
    -   `storage.engine="raft-kv"`の場合、デフォルト値は`"32MiB"`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`"4MiB"`です。
-   最小値: `0`
-   単位：KiB｜MiB｜GiB

### <code>max-write-buffer-number</code> {#code-max-write-buffer-number-code}

-   メンテーブルの最大数。 `storage.flow-control.enable`が`true`に設定されている場合、 `storage.flow-control.memtables-threshold`この設定項目を上書きします。
-   デフォルト値: `5`
-   最小値: `0`

### <code>min-write-buffer-number-to-merge</code> {#code-min-write-buffer-number-to-merge-code}

-   フラッシュをトリガーするために必要な最小のmemtable数
-   デフォルト値: `1`
-   最小値: `0`

### <code>max-bytes-for-level-base</code> {#code-max-bytes-for-level-base-code}

-   ベースレベル（レベル1）における最大バイト数。一般的には、memtableのサイズの4倍に設定されます。レベル1のデータサイズ`max-bytes-for-level-base`の制限値に達すると、レベル1のSSTファイルと、それと重複するレベル2のSSTファイルが圧縮されます。
-   `defaultcf`および`writecf`のデフォルト値: `"512MiB"`
-   `lockcf`のデフォルト値: `"128MiB"`
-   最小値: `0`
-   単位：KiB｜MiB｜GiB
-   不要な圧縮を減らすため、 `max-bytes-for-level-base`の値は L0 のデータ量とほぼ等しく設定することをお勧めします。たとえば、圧縮方法が &quot;no:no:lz4:lz4:lz4:lz4:lz4&quot; の場合、L0 と L1 は圧縮されず、L0 の圧縮のトリガー条件は SST ファイルの数が 4 (デフォルト値) に達することであるため、{{B-PLACEHOLDER `max-bytes-for-level-base`の値は`write-buffer-size * 4`にする必要があります。L0 と L1 の両方で圧縮を採用する場合は、RocksDB ログを分析して、memtable から圧縮された SST ファイルのサイズを把握する必要があります。例えば、ファイルサイズが 32 MiB の場合、 `max-bytes-for-level-base`の値を 128 MiB ( `32 MiB * 4` ) に設定することをお勧めします。

### <code>target-file-size-base</code> {#code-target-file-size-base-code}

-   ベースレベルでのターゲットファイルのサイズ。 `compaction-guard-max-output-file-size`の値が`enable-compaction-guard` } の場合、この値は`true`によって上書きされます。
-   デフォルト値: None。これは、デフォルトでは`"8MiB"`を意味します。
-   最小値: `0`
-   単位：KiB｜MiB｜GiB

### <code>level0-file-num-compaction-trigger</code> {#code-level0-file-num-compaction-trigger-code}

-   L0 で圧縮をトリガーするファイルの最大数
-   `defaultcf`および`writecf`のデフォルト値: `4`
-   `lockcf`のデフォルト値: `1`
-   最小値: `0`

### <code>level0-slowdown-writes-trigger</code> {#code-level0-slowdown-writes-trigger-code}

-   L0 レジスタで書き込み停止を引き起こすファイルの最大数。
-   v8.5.4 以前のバージョンでは、フロー制御メカニズムが有効になっている場合 ( [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)が`true`の場合)、この構成項目の値は[`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)によって直接上書きされます。
-   バージョン 8.5.5 以降: フロー制御メカニズムが有効になっている場合 ( [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)が`true`の場合)、この構成項目の値は、その値が`storage.flow-control.l0-files-threshold`より大きい場合にのみ、 [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)によって上書きされます。この動作により、フロー制御しきい値を上げた際に RocksDB の圧縮高速化メカニズムが弱まるのを防ぎます。
-   デフォルト値: `20`
-   最小値: `0`

### <code>level0-stop-writes-trigger</code> {#code-level0-stop-writes-trigger-code}

-   L0 で書き込みを完全にブロックするために必要なファイルの最大数
-   デフォルト値: `36`
-   最小値: `0`

### <code>max-compaction-bytes</code> {#code-max-compaction-bytes-code}

-   圧縮ごとにディスクに書き込まれる最大バイト数
-   デフォルト値: `"2GiB"`
-   最小値: `0`
-   単位：KiB｜MiB｜GiB

### <code>compaction-pri</code> {#code-compaction-pri-code}

-   優先される圧縮の種類
-   オプション値:
    -   `"by-compensated-size"` : ファイルサイズ順にファイルを圧縮し、大きなファイルはより高い優先度で圧縮されます。
    -   `"oldest-largest-seq-first"` : 更新日時が最も古いファイルの圧縮を優先します。この値は、ホットキーを狭い範囲で更新する場合に**のみ**使用してください。
    -   `"oldest-smallest-seq-first"` : 長期間次のレベルに圧縮されていない範囲を持つファイルの圧縮を優先します。キー空間全体でホットキーをランダムに更新する場合、この値は書き込み増幅をわずかに低減できます。
    -   `"min-overlapping-ratio"` : 重複率の高いファイルの圧縮を優先します。ファイルの各レベルが小さい場合（ `the file size in the next level` ÷ `the file size in this level`の結果が小さい場合）、TiKV はこのファイルを最初に圧縮します。多くの場合、この値によって書き込み増幅を効果的に削減できます。
-   `defaultcf`および`writecf`のデフォルト値: `"min-overlapping-ratio"`
-   `lockcf`のデフォルト値: `"by-compensated-size"`

### <code>dynamic-level-bytes</code> {#code-dynamic-level-bytes-code}

-   動的レベルバイトを最適化するかどうかを決定します
-   デフォルト値: `true`

### <code>num-levels</code> {#code-num-levels-code}

-   RocksDBファイルの最大レベル数
-   デフォルト値: `7`

### <code>max-bytes-for-level-multiplier</code> {#code-max-bytes-for-level-multiplier-code}

-   レイヤーのデフォルトの増幅倍率
-   デフォルト値: `10`

### <code>compaction-style</code> {#code-compaction-style-code}

-   圧縮方法
-   オプション値: `"level"` 、 `"universal"` 、 `"fifo"`
-   デフォルト値: `"level"`

### <code>disable-auto-compactions</code> {#code-disable-auto-compactions-code}

-   自動圧縮を無効にするかどうかを決定します。
-   デフォルト値: `false`

### <code>soft-pending-compaction-bytes-limit</code> {#code-soft-pending-compaction-bytes-limit-code}

-   保留中の圧縮バイト数のソフトリミット。
-   v8.5.4 以前のバージョンでは、フロー制御メカニズムが有効になっている場合 ( [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)が`true`の場合)、この構成項目は[`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)によって直接上書きされます。
-   バージョン 8.5.5 以降: フロー制御メカニズムが有効になっている場合 ( [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)が`true`の場合)、この設定項目は、 [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)値が`storage.flow-control.soft-pending-compaction-bytes-limit`より大きい場合にのみ上書きされます。この動作により、フロー制御しきい値を上げた際に RocksDB の圧縮高速化メカニズムが弱まるのを防ぎます。
-   デフォルト値: `"192GiB"`
-   単位：KiB｜MiB｜GiB

### <code>hard-pending-compaction-bytes-limit</code> {#code-hard-pending-compaction-bytes-limit-code}

-   保留中の圧縮バイト数の上限値。 `storage.flow-control.enable` `true`に設定されている場合、 `storage.flow-control.hard-pending-compaction-bytes-limit`この設定項目を上書きします。
-   デフォルト値: `"256GiB"`
-   単位：KiB｜MiB｜GiB

### <code>enable-compaction-guard</code> {#code-enable-compaction-guard-code}

-   TiKVリージョン境界でSSTファイルを分割する最適化機能である圧縮ガードを有効または無効にします。この最適化により、圧縮I/Oを削減し、TiKVがより大きなSSTファイルサイズ（つまり、SSTファイルの総数）を使用できるようにすると同時に、リージョン移行時に古いデータを効率的にクリーンアップできます。
-   `defaultcf`および`writecf`のデフォルト値: `true`
-   `lockcf`のデフォルト値: None。これは、デフォルトで無効になっていることを意味します。

### <code>compaction-guard-min-output-file-size</code> {#code-compaction-guard-min-output-file-size-code}

-   圧縮ガードが有効になっている場合の、SSTファイルの最小サイズ。この設定により、圧縮ガードが有効になっている場合にSSTファイルが小さくなりすぎるのを防ぎます。
-   デフォルト値: `"8MiB"`
-   単位：KiB｜MiB｜GiB

### <code>compaction-guard-max-output-file-size</code> {#code-compaction-guard-max-output-file-size-code}

-   コンパクションガードが有効になっている場合の SST ファイルの最大サイズ。この設定により、コンパクションガードが有効になっている場合に SST ファイルが大きくなりすぎるのを防ぎます。この設定は、同じカラムファミリーの`target-file-size-base`を上書きします。
-   デフォルト値: `"128MiB"`
-   単位：KiB｜MiB｜GiB

### <code>format-version</code> <span class="version-mark">v6.2.0の新機能</span> {#code-format-version-code-span-class-version-mark-new-in-v6-2-0-span}

-   SSTファイルのフォーマットバージョン。この設定項目は、新規に書き込まれるテーブルにのみ影響します。既存のテーブルについては、バージョン情報はフッターから読み取られます。
-   オプション値:
    -   `0` : すべての TiKV バージョンで読み取り可能です。デフォルトのチェックサムタイプは CRC32 であり、このバージョンではチェックサムタイプの変更はサポートされていません。
    -   `1` : すべての TiKV バージョンで読み取り可能です。xxHash などのデフォルト以外のチェックサム タイプをサポートします。RocksDB は、チェックサム タイプが CRC32 でない場合にのみデータを書き込みます。（バージョン`0`は自動的にアップグレードされます）
    -   `2` : すべての TiKV バージョンで読み取ることができます。LZ4、BZip2、Zlib 圧縮を使用して圧縮ブロックのエンコーディングを変更します。
    -   `3` : TiKV v2.1以降のバージョンで読み取ることができます。インデックスブロック内のキーのエンコーディングを変更します。
    -   `4` : TiKV v3.0以降のバージョンで読み取ることができます。インデックスブロック内の値のエンコーディングを変更します。
    -   `5` : TiKV v6.1以降のバージョンで読み取ることができます。フルフィルタとパーティションフィルタは、異なるスキーマを使用した、より高速で高精度なブルームフィルタ実装を使用します。
-   デフォルト値:

    -   `storage.engine="raft-kv"`の場合、デフォルト値は`2`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`5`です。

### <code>ttl</code> <span class="version-mark">v7.2.0の新機能</span> {#code-ttl-code-span-class-version-mark-new-in-v7-2-0-span}

-   TTL（有効期限）よりも古い更新情報を持つSSTファイルは、自動的に圧縮対象として選択されます。これらのSSTファイルは、最下位レベルまたは最下位ファイルまで圧縮されるように、段階的に圧縮処理が行われます。
-   デフォルト値：なし。これは、デフォルトではSSTファイルが選択されていないことを意味します。
-   単位：s（秒）｜h（時間）｜d（日）

### <code>periodic-compaction-seconds</code> <span class="version-mark">v7.2.0 の新機能</span> {#code-periodic-compaction-seconds-code-span-class-version-mark-new-in-v7-2-0-span}

-   定期的な圧縮の間隔。この値よりも古い更新履歴を持つSSTファイルが圧縮対象として選択され、元のSSTファイルと同じ階層に書き換えられます。
-   デフォルト値：None。これは、定期的な圧縮がデフォルトで無効になっていることを意味します。
-   単位：s（秒）｜h（時間）｜d（日）

### <code>max-compactions</code> <span class="version-mark">（v6.6.0の新機能）</span> {#code-max-compactions-code-span-class-version-mark-new-in-v6-6-0-span}

-   同時実行可能な圧縮タスクの最大数。値`0`は制限なしを意味します。
-   デフォルト値: `0`

## rocksdb.defaultcf.titan {#rocksdb-defaultcf-titan}

> **注記：**
>
> Titan は`rocksdb.defaultcf`でのみ有効にできます。 `rocksdb.writecf`では Titan を有効にすることはサポートされていません。

`rocksdb.defaultcf.titan`に関連するコンフィグレーション項目。

### <code>min-blob-size</code> {#code-min-blob-size-code}

> **注記：**
>
> -   TiDB v7.6.0以降、ワイドテーブルおよびJSONデータの書き込みとポイントクエリのパフォーマンスを向上させるため、Titanがデフォルトで有効になっています。 `min-blob-size`のデフォルト値が`1KiB`から`32KiB`に変更されます。これは`32KiB`を超える値はTitanに保存され、その他のデータは引き続きRocksDBに保存されることを意味します。
> -   構成の一貫性を確保するため、TiDB v7.6.0 以降のバージョンにアップグレードする既存のクラスターでは、アップグレード前に`min-blob-size`を明示的に設定しない場合、TiDB は以前のデフォルト値`1KiB`を保持します。
> -   `32KiB`より小さい値を設定すると、範囲スキャンのパフォーマンスに影響が出る可能性があります。ただし、ワークロードが主に大量の書き込みとポイントクエリで構成されている場合は、パフォーマンス向上のために`min-blob-size`の値を小さくすることを検討してください。

-   Blobファイルに格納される最小値。指定されたサイズより小さい値はLSMツリーに格納されます。
-   デフォルト値: None。これは、デフォルトでは`"32KiB"`を意味します。
-   最小値: `0`
-   単位：KiB｜MiB｜GiB

### <code>blob-file-compression</code> {#code-blob-file-compression-code}

> **注記：**
>
> -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)になければなりません。 Snappy 圧縮の他のバリアントはサポートされていません。
> -   TiDB v7.6.0以降、 `blob-file-compression`のデフォルト値が`"lz4"`から`"zstd"`に変更されます。

-   Blobファイルで使用される圧縮アルゴリズム
-   オプション値: `"no"` 、 `"snappy"` 、 `"zlib"` 、 `"bzip2"` 、 `"lz4"` 、 `"lz4hc"` 、 `"zstd"`
-   デフォルト値: `"zstd"`

### <code>zstd-dict-size</code> {#code-zstd-dict-size-code}

-   zstd辞書の圧縮サイズ。デフォルト値は`"0KiB"`で、zstd辞書の圧縮を無効にすることを意味します。この場合、Titanは単一の値に基づいてデータを圧縮しますが、RocksDBはブロックに基づいてデータを圧縮します（デフォルトでは`32KiB` ）。Titanの値の平均サイズが`32KiB`より小さい場合、Titanの圧縮率はRocksDBよりも低くなります。JSONを例にとると、TitanのストアサイズはRocksDBよりも30%から50%大きくなる可能性があります。実際の圧縮率は、値の内容が圧縮に適しているかどうか、および異なる値間の類似性によって異なります。 `zstd-dict-size`を設定することで、zstd 辞書圧縮を有効にして圧縮率を高めることができます (例えば、 `16KiB`に設定します)。実際のストアサイズは RocksDB よりも小さくなる可能性があります。ただし、zstd 辞書圧縮は、特定のワークロードにおいて約 10% のパフォーマンス低下を引き起こす可能性があります。
-   デフォルト値: `"0KiB"`
-   単位：KiB｜MiB｜GiB

### <code>blob-cache-size</code> {#code-blob-cache-size-code}

-   Blobファイルのキャッシュサイズ
-   デフォルト値: `"0GiB"`
-   最小値: `0`
-   推奨値: `0` 。v8.0.0 以降、TiKV は`shared-blob-cache`設定項目を導入し、デフォルトで有効にしているため、 `blob-cache-size`個別に設定する必要はありません。 `blob-cache-size`の設定は、 `shared-blob-cache`が`false`に設定されている場合にのみ有効になります。
-   単位：KiB｜MiB｜GiB

### <code>shared-blob-cache</code> <span class="version-mark">v8.0.0で追加</span> {#code-shared-blob-cache-code-span-class-version-mark-new-in-v8-0-0-span}

-   TitanのブロブファイルとRocksDBのブロックファイルに対して共有キャッシュを有効にするかどうかを制御します。
-   デフォルト値: `true` 。共有キャッシュが有効になっている場合、ブロックファイルの優先度が高くなります。つまり、TiKV はブロックファイルのキャッシュ要件を満たすことを優先し、残りのキャッシュをブロブファイルに使用します。

### <code>min-gc-batch-size</code> {#code-min-gc-batch-size-code}

-   1回のGCを実行するために必要なBlobファイルの最小合計サイズ
-   デフォルト値: `"16MiB"`
-   最小値: `0`
-   単位：KiB｜MiB｜GiB

### <code>max-gc-batch-size</code> {#code-max-gc-batch-size-code}

-   1回のGC実行で許可されるBlobファイルの最大合計サイズ
-   デフォルト値: `"64MiB"`
-   最小値: `0`
-   単位：KiB｜MiB｜GiB

### <code>discardable-ratio</code> {#code-discardable-ratio-code}

-   Blob ファイル内の古いデータ (対応するキーが更新または削除されたデータ) の割合が次のしきい値を超えると、Titan GC がトリガーされます。Titan がこの Blob ファイルの有効なデータを別のファイルに書き込むとき、 `discardable-ratio`値を使用して、書き込み増幅とスペース増幅の上限を推定できます (圧縮が無効になっている場合)。

    書き込み増幅の上限 = 1 / `discardable-ratio`

    空間増幅の上限 = 1 / (1 - `discardable-ratio` )

    これら2つの式から、 `discardable_ratio`の値を小さくすると、スペースの増幅を抑えることができますが、TitanでのGCの頻度が高くなります。値を大きくすると、TitanのGCの頻度が減り、それに伴いI/O帯域幅とCPU使用率が低下しますが、ディスク使用率が増加します。

-   デフォルト値: `0.5`

-   最小値: `0`

-   最大値: `1`

### <code>sample-ratio</code> {#code-sample-ratio-code}

-   GC中にファイルをサンプリングする際の、（Blobファイルから読み取ったデータ量／Blobファイル全体）の比率
-   デフォルト値: `0.1`
-   最小値: `0`
-   最大値: `1`

### <code>merge-small-file-threshold</code> {#code-merge-small-file-threshold-code}

-   Blob ファイルのサイズがこの値より小さい場合でも、Blob ファイルは GC の対象として選択される可能性があります。この場合、 `discardable-ratio`は無視されます。
-   デフォルト値: `"8MiB"`
-   最小値: `0`
-   単位：KiB｜MiB｜GiB

### <code>blob-run-mode</code> {#code-blob-run-mode-code}

-   Titanの実行モードを指定します。
-   オプション値:
    -   `normal` : 値のサイズが[`min-blob-size`](#min-blob-size)超えると、データを blob ファイルに書き込みます。
    -   `read-only` : ブロブファイルへの新しいデータの書き込みを拒否しますが、ブロブファイルから元のデータを読み取ります。
    -   `fallback` : ブロブファイル内のデータをLSMに書き込みます。
-   デフォルト値: `normal`

### <code>level-merge</code> {#code-level-merge-code}

-   読み取りパフォーマンスを最適化するかどうかを決定します。 `level-merge`有効になっている場合、書き込み増幅が強化されます。
-   デフォルト値: `false`

## raftdb {#raftdb}

`raftdb`に関連するコンフィグレーション項目

### <code>max-background-jobs</code> {#code-max-background-jobs-code}

-   RocksDB のバックグラウンド スレッドの数。 RocksDB スレッド プールのサイズを変更する場合は、 [TiKVスレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。
-   デフォルト値: `4`
-   最小値: `2`

### <code>max-sub-compactions</code> {#code-max-sub-compactions-code}

-   RocksDBで同時に実行されるサブコンパクション操作の数
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

-   値が`true`の場合、データベースが存在しない場合は作成されます。
-   デフォルト値: `true`

### <code>stats-dump-period</code> {#code-stats-dump-period-code}

-   統計情報がログに出力される間隔
-   デフォルト値: `10m`

### <code>wal-dir</code> {#code-wal-dir-code}

-   Raft RocksDB WAL ファイルが保存されるディレクトリ。これは WAL の絶対ディレクトリパスです。この設定項目を[`rocksdb.wal-dir`](#wal-dir)と同じ値に設定**しないでください**。
-   この設定項目が設定されていない場合、ログファイルはデータと同じディレクトリに保存されます。
-   マシンに2つのディスクが搭載されている場合、RocksDBデータとWALログを異なるディスクに保存することでパフォーマンスが向上する可能性があります。
-   デフォルト値: `""`

### <code>wal-ttl-seconds</code> {#code-wal-ttl-seconds-code}

-   アーカイブされたWALファイルの保持期間を指定します。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位：秒

### <code>wal-size-limit</code> {#code-wal-size-limit-code}

-   アーカイブされたWALファイルのサイズ制限。この値を超えると、システムはこれらのファイルを削除します。
-   デフォルト値: `0`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>max-total-wal-size</code> {#code-max-total-wal-size-code}

-   RocksDB WALの最大サイズ合計
-   デフォルト値:
    -   `storage.engine="raft-kv"`の場合、デフォルト値は`"4GiB"`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`1`です。

### <code>compaction-readahead-size</code> {#code-compaction-readahead-size-code}

-   RocksDBの圧縮中に先読み機能を有効にするかどうか、および先読みデータのサイズを指定するかどうかを制御します。
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

-   バックグラウンドのフラッシュと圧縮における読み取りと書き込みの両方で`O_DIRECT`を使用するかどうかを決定します。このオプションのパフォーマンスへの影響: `O_DIRECT`を有効にすると、OS バッファ キャッシュの汚染がバイパスされ防止されますが、後続のファイル読み取りではバッファ キャッシュの内容を再読み込みする必要があります。
-   デフォルト値: `false`

### <code>enable-pipelined-write</code> {#code-enable-pipelined-write-code}

-   パイプライン書き込みを有効にするかどうかを制御します。この設定を有効にすると、従来のパイプライン書き込みが使用されます。この設定を無効にすると、新しいパイプラインコミットメカニズムが使用されます。
-   デフォルト値: `true`

### <code>allow-concurrent-memtable-write</code> {#code-allow-concurrent-memtable-write-code}

-   同時memtable書き込みを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

-   ファイルが非同期的に書き込まれている間に、OSがファイルをディスクに増分的に同期する速度
-   デフォルト値: `"1MiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>wal-bytes-per-sync</code> {#code-wal-bytes-per-sync-code}

-   WALファイルが書き込まれているときに、OSがWALファイルをディスクに増分同期する速度
-   デフォルト値: `"512KiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>info-log-max-size</code> {#code-info-log-max-size-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.file.max-size`](#max-size-new-in-v540)に置き換えられました。

-   Infoログの最大サイズ
-   デフォルト値: `"1GiB"`
-   最小値: `0`
-   単位: B|KiB|MiB|GiB

### <code>info-log-roll-time</code> {#code-info-log-roll-time-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBログはTiKVのログモジュールによって管理されるようになりました。そのため、この設定項目は非推奨です。TiKVは時間に基づく自動ログ分割をサポートしなくなりました。代わりに、設定項目[`log.file.max-size`](#max-size-new-in-v540)使用して、ファイルサイズに基づく自動ログ分割のしきい値を設定できます。

-   Infoログが切り捨てられる間隔。値が`0s`の場合、ログは切り捨てられません。
-   デフォルト値： `"0s"` （ログが切り捨てられないことを意味します）

### <code>info-log-keep-log-file-num</code> {#code-info-log-keep-log-file-num-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.file.max-backups`](#max-backups-new-in-v540)に置き換えられました。

-   RaftDBに保持される情報ログファイルの最大数
-   デフォルト値: `10`
-   最小値: `0`

### <code>info-log-dir</code> {#code-info-log-dir-code}

-   Infoログが保存されるディレクトリ
-   デフォルト値: `""`

### <code>info-log-level</code> {#code-info-log-level-code}

> **警告：**
>
> バージョン5.4.0以降、RocksDBログはTiKVのログモジュールによって管理されます。そのため、この設定項目は非推奨となり、その機能は設定項目[`log.level`](#level-new-in-v540)に置き換えられました。

-   RaftDBのログレベル
-   デフォルト値: `"info"`

## いかだエンジン {#raft-engine}

Raft Engineに関連するコンフィグレーション項目。

> **注記：**
>
> -   Raft Engineを初めて有効にすると、TiKVはRocksDBからRaft Engineにデータを転送します。そのため、TiKVが起動するまで数十秒余分に待つ必要があります。
> -   TiDB v5.4.0 のRaft Engineのデータ形式は、以前の TiDB バージョンと互換性がありません。そのため、TiDB クラスタを v5.4.0 から以前のバージョンにダウングレードする必要がある場合は、ダウングレードする**前に**、 `enable`を`false`に設定してRaft Engine を無効にし、TiKV を再起動して設定を有効にしてください。

### <code>enable</code> {#code-enable-code}

-   Raftログを保存するためにRaft Engineを使用するかどうかを決定します。有効にすると、 `raftdb`の設定は無視されます。
-   デフォルト値: `true`

### <code>dir</code> {#code-dir-code}

-   Raftのログファイルが保存されるディレクトリ。このディレクトリが存在しない場合は、TiKVの起動時に作成されます。
-   この設定項目が設定されていない場合は、 `{data-dir}/raft-engine`が使用されます。
-   お使いのコンピューターに複数のディスクが搭載されている場合は、TiKVのパフォーマンスを向上させるために、 Raft Engineのデータを別のディスクに保存することをお勧めします。
-   デフォルト値: `""`

### <code>spill-dir</code> <span class="version-mark">v8.4.0の新機能</span> {#code-spill-dir-code-span-class-version-mark-new-in-v8-4-0-span}

-   Raftログファイルを保存するための補助ディレクトリです。 `dir`ディレクトリのディスク容量がいっぱいになると、新しいRaftログはこのディレクトリに保存されます。設定後にこの補助ディレクトリが存在しない場合は、TiKVの起動時に自動的に作成されます。
-   この設定が行われていない場合、補助ディレクトリは有効になりません。

> **注記：**
>
> -   この設定は、 Raft Engineの`dir`と`spill-dir`が異なるディスクドライブに設定されている場合にのみ有効になります。
> -   この機能を有効にした後、無効にする場合は、TiKVを再起動する前に以下の操作を実行する必要があります。そうしないと、TiKVが起動に失敗します。
>     1.  TiKVを停止してください。
>     2.  `spill-dir`ディレクトリからすべてのRaft Log を[`dir`](/tikv-configuration-file.md#dir)ディレクトリにコピーします。
>     3.  TiKV設定ファイルからこの設定を削除してください。
>     4.  TiKVを再起動してください。

### <code>batch-compression-threshold</code> {#code-batch-compression-threshold-code}

-   ログバッチのしきい値サイズを指定します。この設定値よりも大きいログバッチは圧縮されます。この設定項目を`0`に設定すると、圧縮は無効になります。
-   デフォルト値: `"4KiB"` 。v8.1.0 より前のバージョンでは、デフォルト値は`"8KiB"`です。

### <code>bytes-per-sync</code> {#code-bytes-per-sync-code}

> **警告：**
>
> バージョン6.5.0以降、 Raft Engineはログをバッファリングせずに直接ディスクに書き込みます。そのため、この設定項目は非推奨となり、機能しなくなりました。

-   バッファリングされた書き込みの最大累積サイズを指定します。この設定値を超えると、バッファリングされた書き込みはディスクに書き込まれます。
-   この設定項目を`0`に設定すると、増分同期が無効になります。
-   v6.5.0より前のバージョンでは、デフォルト値は`"4MiB"`です。

### <code>target-file-size</code> {#code-target-file-size-code}

-   ログファイルの最大サイズを指定します。ログファイルがこの値を超えると、ローテーションされます。
-   デフォルト値: `"128MiB"`

### <code>purge-threshold</code> {#code-purge-threshold-code}

-   メインログキューのしきい値サイズを指定します。この設定値を超えると、メインログキューはクリアされます。
-   この設定を使用すると、 Raft Engineのディスク容量使用量を調整できます。
-   デフォルト値: `"10GiB"`

### <code>recovery-mode</code> {#code-recovery-mode-code}

-   リカバリ中にファイル破損が発生した場合の対処方法を決定します。
-   値のオプション: `"absolute-consistency"` 、 `"tolerate-tail-corruption"` 、 `"tolerate-any-corruption"`
-   デフォルト値: `"tolerate-tail-corruption"`

### <code>recovery-read-block-size</code> {#code-recovery-read-block-size-code}

-   リカバリ中にログファイルを読み取るための最小I/Oサイズ。
-   デフォルト値: `"16KiB"`
-   最小値: `"512B"`

### <code>recovery-threads</code> {#code-recovery-threads-code}

-   ログファイルのスキャンと復元に使用されるスレッド数。
-   デフォルト値: `4`
-   最小値: `1`

### <code>memory-limit</code> {#code-memory-limit-code}

-   Raft Engineのメモリ使用量の上限を指定します。
-   この設定値が設定されていない場合、利用可能なシステムメモリの15%が使用されます。
-   デフォルト値: `Total machine memory * 15%`

### <code>format-version</code> <span class="version-mark">v6.3.0の新機能</span> {#code-format-version-code-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> `format-version`を`2`に設定した後、TiKV クラスターを v6.3.0 から以前のバージョンにダウングレードする必要がある場合は、ダウングレード**の前に**以下の手順を実行してください。
>
> 1.  Raft Engineを無効にするには、 [`enable`](/tikv-configuration-file.md#enable-1)を`false`に設定し、TiKVを再起動して設定を有効にします。
> 2.  `format-version`を`1`に設定します。
> 3.  `enable`を`true`に設定してRaft Engineを有効にし、TiKV を再起動して設定を有効にしてください。

-   Raft Engineのログ ファイルのバージョンを指定します。
-   お得なオプション：
    -   `1` : TiKV v6.3.0 より前のバージョンのデフォルトのログファイルです。TiKV &gt;= v6.1.0 で読み取ることができます。
    -   `2` : ログのリサイクルをサポートします。TiKV &gt;= v6.3.0 で読み取ることができます。
-   デフォルト値:
    -   `storage.engine="raft-kv"`の場合、デフォルト値は`2`です。
    -   `storage.engine="partitioned-raft-kv"`の場合、デフォルト値は`5`です。

### <code>enable-log-recycle</code> <span class="version-mark">v6.3.0の新機能</span> {#code-enable-log-recycle-code-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この設定項目は、 [`format-version`](#format-version-new-in-v630) &gt;= 2 の場合にのみ利用可能です。

-   Raft Engineで古いログファイルを再利用するかどうかを決定します。有効にすると、論理的に削除されたログファイルが再利用のために予約されます。これにより、書き込みワークロードにおけるロングテールレイテンシーが軽減されます。
-   デフォルト値: `true`

### <code>prefill-for-recycle</code> <span class="version-mark">（v7.0.0の新機能）</span> {#code-prefill-for-recycle-code-span-class-version-mark-new-in-v7-0-0-span}

> **注記：**
>
> この設定項目は、 [`enable-log-recycle`](#enable-log-recycle-new-in-v630) `true`に設定されている場合にのみ有効になります。

-   Raft Engineでログのリサイクル用に空のログファイルを生成するかどうかを決定します。有効にすると、 Raft Engine は初期化中にログのリサイクル用に空のログファイルを自動的に生成し、初期化直後からログのリサイクルが有効になります。
-   デフォルト値: `false`

### <code>compression-level</code> <span class="version-mark">v7.4.0で追加</span> {#code-compression-level-code-span-class-version-mark-new-in-v7-4-0-span}

-   Raft EngineがRaftログファイルを書き込む際に使用するLZ4アルゴリズムの圧縮効率を設定します。値が小さいほど圧縮速度は速くなりますが、圧縮率は低くなります。
-   範囲: `[1, 16]`
-   デフォルト値: `1`

## 安全 {#security}

セキュリティに関連するコンフィグレーション項目。

### <code>ca-path</code> {#code-ca-path-code}

-   CAファイルのパス
-   デフォルト値: `""`

### <code>cert-path</code> {#code-cert-path-code}

-   X.509証明書を含むプライバシー強化メール（PEM）ファイルのパス
-   デフォルト値: `""`

### <code>key-path</code> {#code-key-path-code}

-   X.509キーを含むPEMファイルのパス
-   デフォルト値: `""`

### <code>cert-allowed-cn</code> {#code-cert-allowed-cn-code}

-   クライアントから提示される証明書において許容されるX.509共通名のリスト。提示された共通名がリスト内のいずれかのエントリと完全に一致する場合にのみ、リクエストが許可されます。
-   デフォルト値: `[]` 。これは、クライアント証明書のCNチェックがデフォルトで無効になっていることを意味します。

### <code>redact-info-log</code> <span class="version-mark">v4.0.8の新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v4-0-8-span}

-   この設定項目は、ログのマスキングを有効または無効にします。値のオプション: `true` 、 `false` 、 `"on"` 、 `"off"` 、および`"marker"` 。 `"on"` 、 `"off"` 、および`"marker"`オプションは、v8.3.0 で導入されました。
-   設定項目が`false`または`"off"`に設定されている場合、ログの編集は無効になります。
-   設定項目が`true`または`"on"`に設定されている場合、ログ内のすべてのユーザーデータは`?`に置き換えられます。
-   設定項目が`"marker"`に設定されている場合、ログ内のすべてのユーザーデータは`‹ ›`で囲まれます。ユーザーデータに`‹`または`›`が含まれている場合、 `‹`は`‹‹`にエスケープされ、 `›`は`››`にエスケープされます。マークされたログに基づいて、ログの表示時にマークされた情報を非機密化するかどうかを決定できます。
-   デフォルト値: `false`
-   詳しい使い方は[TiKV側でのログ編集](/log-redaction.md#log-redaction-in-tikv-side)をご覧ください。

## セキュリティ暗号化 {#security-encryption}

[保存時の暗号化](/encryption-at-rest.md)(TDE)に関するコンフィグレーション項目。

### <code>data-encryption-method</code> {#code-data-encryption-method-code}

-   データファイルの暗号化方法
-   値のオプション: &quot;plaintext&quot;, &quot;aes128-ctr&quot;, &quot;aes192-ctr&quot;, &quot;aes256-ctr&quot;, &quot;sm4-ctr&quot; (v6.3.0以降でサポート)
-   「plaintext」以外の値を指定すると、暗号化が有効になり、マスターキーを指定する必要があります。
-   デフォルト値: `"plaintext"`

### <code>data-key-rotation-period</code> {#code-data-key-rotation-period-code}

-   TiKVがデータ暗号化キーをローテーションする頻度を指定します。
-   デフォルト値: `7d`

### <code>enable-file-dictionary-log</code> {#code-enable-file-dictionary-log-code}

-   TiKVが暗号化メタデータを管理する際に、I/Oとミューテックスの競合を軽減するための最適化を有効にします。
-   この構成パラメーターが (デフォルトで) 有効になっている場合に発生する可能性のある互換性の問題を回避するには、詳細については[保存時の暗号化- TiKVバージョン間の互換性](/encryption-at-rest.md#compatibility-between-tikv-versions)を参照してください。
-   デフォルト値: `true`

### <code>master-key</code> {#code-master-key-code}

-   暗号化が有効な場合はマスターキーを指定します。マスターキーの設定方法については、[保存時の暗号化- 暗号化の設定](/encryption-at-rest.md#configure-encryption)参照してください。

### <code>previous-master-key</code> {#code-previous-master-key-code}

-   新しいマスター キーをローテーションするときに古いマスター キーを指定します。構成形式は`master-key`と同じです。マスターキーの設定方法については、[保存時の暗号化- 暗号化の設定](/encryption-at-rest.md#configure-encryption)参照してください。

## 輸入 {#import}

TiDB LightningのインポートおよびBR復元に関連するコンフィグレーション項目。

### <code>num-threads</code> {#code-num-threads-code}

-   RPCリクエストを処理するスレッド数
-   デフォルト値: `8`
-   最小値: `1`

### <code>stream-channel-window</code> {#code-stream-channel-window-code}

-   ストリームチャネルのウィンドウサイズ。チャネルが満杯になると、ストリームはブロックされます。
-   デフォルト値: `128`

### <code>memory-use-ratio</code> <span class="version-mark">v6.5.0で追加</span> {#code-memory-use-ratio-code-span-class-version-mark-new-in-v6-5-0-span}

-   バージョン6.5.0以降、PITRはメモリ内のバックアップログファイルに直接アクセスしてデータを復元することをサポートしています。この設定項目は、PITRで使用可能なメモリとTiKVの総メモリの比率を指定します。
-   値の範囲：[0.0, 0.5]
-   デフォルト値は`0.3`で、これはシステムメモリの 30% が PITR に使用可能であることを意味します。値が`0.0`の場合、PITR はログファイルをローカルディレクトリにダウンロードすることによって実行されます。

> **注記：**
>
> バージョン6.5.0より前のバージョンでは、ポイントインタイムリカバリ（PITR）は、バックアップファイルをローカルディレクトリにダウンロードすることによるデータ復元のみをサポートしています。

## GC {#gc}

### <code>batch-keys</code> {#code-batch-keys-code}

-   一度にガベージコレクションされるキーの数
-   デフォルト値: `512`

### <code>max-write-bytes-per-sec</code> {#code-max-write-bytes-per-sec-code}

-   GCワーカーが1秒間にRocksDBに書き込むことができる最大バイト数。
-   値が`0`に設定されている場合、制限はありません。
-   デフォルト値: `"0"`

### <code>enable-compaction-filter</code> <span class="version-mark">v5.0の新機能</span> {#code-enable-compaction-filter-code-span-class-version-mark-new-in-v5-0-span}

-   コンパクションフィルタ機能でGCを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>ratio-threshold</code> {#code-ratio-threshold-code}

-   GCをトリガーするガベージ比率のしきい値。
-   デフォルト値: `1.1`

### <code>num-threads</code> <span class="version-mark">、v6.5.8、v7.1.4、v7.5.1、v7.6.0 で追加されました。</span> {#code-num-threads-code-span-class-version-mark-new-in-v6-5-8-v7-1-4-v7-5-1-and-v7-6-0-span}

-   `enable-compaction-filter`が`false`の場合の GC スレッドの数。
-   デフォルト値: `1`

## gc.自動圧縮 {#gc-auto-compaction}

TiKVの自動圧縮の動作を設定します。

### <code>check-interval</code> <span class="version-mark">v7.5.7およびv8.5.4で追加されました。</span> {#code-check-interval-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   TiKVが自動圧縮をトリガーするかどうかを確認する間隔。この間隔内では、自動圧縮条件を満たすリージョンが優先度に基づいて処理されます。間隔が経過すると、TiKVはリージョン情報を再スキャンし、優先度を再計算します。
-   デフォルト値: `"300s"`

### <code>tombstone-num-threshold</code><span class="version-mark">は v7.5.7 および v8.5.4 で追加されました。</span> {#code-tombstone-num-threshold-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   TiKVの自動圧縮をトリガーするために必要なRocksDBのトゥームストーンの数。トゥームストーンの数がこのしきい値に達するか、トゥームストーンの割合が[`tombstone-percent-threshold`](#tombstone-percent-threshold-new-in-v757-and-v854)に達すると、TiKVは自動圧縮をトリガーします。
-   この設定項目は[圧縮フィルター](/garbage-collection-configuration.md)が無効な場合にのみ有効になります。
-   デフォルト値: `10000`
-   最小値: `0`

### <code>tombstone-percent-threshold</code> <span class="version-mark">v7.5.7 および v8.5.4 で追加</span> {#code-tombstone-percent-threshold-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   TiKVによる自動圧縮をトリガーするために必要なRocksDBのトゥームストーンの割合。トゥームストーンの割合がこのしきい値に達するか、トゥームストーンの数が[`tombstone-num-threshold`](#tombstone-num-threshold-new-in-v757-and-v854)に達すると、TiKVは自動圧縮をトリガーします。
-   この設定項目は[圧縮フィルター](/garbage-collection-configuration.md)が無効な場合にのみ有効になります。
-   デフォルト値: `30`
-   最小値: `0`
-   最大値: `100`

### <code>redundant-rows-threshold</code> <span class="version-mark">v7.5.7 および v8.5.4 で追加</span> {#code-redundant-rows-threshold-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   TiKVの自動圧縮をトリガーするために必要な冗長MVCC行の数。冗長行には、RocksDBのトゥームストーン、TiKVの古いバージョン、およびTiKVの削除トゥームストーンが含まれます。冗長MVCC行の数がこのしきい値に達するか、これらの行の割合が[`redundant-rows-percent-threshold`](#redundant-rows-percent-threshold-new-in-v757-and-v854)に達すると、TiKVは自動圧縮をトリガーします。
-   この設定項目は[圧縮フィルター](/garbage-collection-configuration.md)が有効な場合にのみ有効になります。
-   デフォルト値: `50000`
-   最小値: `0`

### <code>redundant-rows-percent-threshold</code> <span class="version-mark">（v7.5.7およびv8.5.4で追加）</span> {#code-redundant-rows-percent-threshold-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   TiKV の自動圧縮をトリガーするために必要な冗長 MVCC 行の割合。冗長行には、RocksDB のトゥームストーン、TiKV の古いバージョン、および TiKV の削除トゥームストーンが含まれます。冗長 MVCC 行の数が[`redundant-rows-threshold`](#redundant-rows-threshold-new-in-v757-and-v854)に達するか、これらの行の割合が`redundant-rows-percent-threshold`に達すると、TiKV は自動圧縮をトリガーします。
-   この設定項目は[圧縮フィルター](/garbage-collection-configuration.md)が有効な場合にのみ有効になります。
-   デフォルト値: `20`
-   最小値: `0`
-   最大値: `100`

### <code>bottommost-level-force</code> <span class="version-mark">v7.5.7 および v8.5.4 で追加</span> {#code-bottommost-level-force-code-span-class-version-mark-new-in-v7-5-7-and-v8-5-4-span}

-   RocksDBの最下位ファイルに対して強制的に圧縮を実行するかどうかを制御します。
-   デフォルト値: `true`

### <code>mvcc-read-aware-enabled</code> <span class="version-mark">v8.5.6の新機能</span> {#code-mvcc-read-aware-enabled-code-span-class-version-mark-new-in-v8-5-6-span}

-   MVCC読み取り対応の圧縮を有効にするかどうかを制御します。有効にすると、TiKVは読み取り要求中にスキャンされたMVCCバージョンの数を追跡し、この情報を使用して、MVCC読み取り増幅率の高いリージョンに対して圧縮を優先します。これにより、スキャン中に多くの古いバージョンに遭遇するホットリージョンの読み取りレイテンシーが削減されます。
-   デフォルト値: `false`

### <code>mvcc-scan-threshold</code> <span class="version-mark">v8.5.6で追加</span> {#code-mvcc-scan-threshold-code-span-class-version-mark-new-in-v8-5-6-span}

-   リージョンを圧縮候補としてマークするために、読み取り要求ごとにスキャンされる MVCC バージョンの最小数。この構成項目は、 [`mvcc-read-aware-enabled`](#mvcc-read-aware-enabled-new-in-v856) `true`に設定されている場合にのみ有効になります。
-   デフォルト値: `1000`
-   最小値: `0`

### <code>mvcc-read-weight</code> <span class="version-mark">v8.5.6で追加</span> {#code-mvcc-read-weight-code-span-class-version-mark-new-in-v8-5-6-span}

-   リージョンの圧縮優先度スコアを計算する際に、MVCC 読み取りアクティビティに適用される重み乗数。値が大きいほど、墓石密度などの他の圧縮トリガーと比較して、MVCC 読み取り増幅に重みが高くなります。この設定項目は、 [`mvcc-read-aware-enabled`](#mvcc-read-aware-enabled-new-in-v856) `true`に設定されている場合にのみ有効になります。
-   デフォルト値: `3.0`
-   最小値: `0.0`

## バックアップ {#backup}

BRバックアップに関連するコンフィグレーション項目。

### <code>num-threads</code> {#code-num-threads-code}

-   バックアップを処理するワーカー スレッドの数
-   デフォルト値: `MIN(CPU * 0.5, 8)`
-   値の範囲: `[1, CPU]`
-   最小値: `1`

### <code>batch-size</code> {#code-batch-size-code}

-   一度にバックアップするデータ範囲の数
-   デフォルト値: `8`

### <code>sst-max-size</code> {#code-sst-max-size-code}

-   バックアップSSTファイルのサイズのしきい値。TiKVリージョン内のバックアップファイルのサイズがこのしきい値を超えると、TiKVリージョンが複数のリージョン範囲に分割され、ファイルは複数のファイルにバックアップされます。分割された領域内の各ファイルは、 `sst-max-size`と同じサイズ（またはわずかに大きいサイズ）です。
-   例えば、 `[a,e)`リージョンのバックアップ ファイルのサイズが`sst-max-size`より大きい場合、そのファイルは { `[a,b)` 、 `[b,c)`および`[c,d)` `[d,e)` } の領域を持つ複数のファイルにバックアップされ、 `[a,b)` 、 `[b,c)` 、 `[c,d)`のサイズは`sst-max-size`と同じ (またはわずかに大きい) です。
-   デフォルト値: `"384MiB"` 。v8.4.0 より前のバージョンでは、デフォルト値は`"144MiB"`です。

### <code>enable-auto-tune</code> <span class="version-mark">v5.4.0の新機能</span> {#code-enable-auto-tune-code-span-class-version-mark-new-in-v5-4-0-span}

-   クラスタのリソース使用率が高い場合に、バックアップタスクが使用するリソースを制限してクラスタへの影響を軽減するかどうかを制御します。詳細については、 [BRオートチューン](/br/br-auto-tune.md)を参照してください。
-   デフォルト値: `true`

### <code>s3-multi-part-size</code> <span class="version-mark">v5.3.2の新機能</span> {#code-s3-multi-part-size-code-span-class-version-mark-new-in-v5-3-2-span}

> **注記：**
>
> この構成は、S3 レート制限によって引き起こされるバックアップの失敗に対処するために導入されました。この問題は[バックアップデータstorage構造の改良](/br/br-snapshot-architecture.md#structure-of-backup-files)により修正されました。したがって、この構成は v6.1.1 から非推奨となり、推奨されなくなりました。

-   バックアップ時にS3へのマルチパートアップロードを実行する際に使用されるパートサイズです。この設定値を調整することで、S3に送信されるリクエスト数を制御できます。
-   データが S3 にバックアップされ、バックアップ ファイルがこの設定項目の値より大きい場合、 [マルチパートアップロード](https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPart.html)が自動的に有効になります。圧縮率に基づいて、96 MiBリージョンによって生成されるバックアップ ファイルは約 10 MiB ～ 30 MiB になります。
-   デフォルト値: 5MiB

## backup.hadoop {#backup-hadoop}

### <code>home</code> {#code-home-code}

-   HDFSシェルコマンドの場所を指定し、TiKVがシェルコマンドを見つけられるようにします。この設定項目は、環境変数`$HADOOP_HOME`と同じ効果があります。
-   デフォルト値: `""`

### <code>linux-user</code> {#code-linux-user-code}

-   TiKVがHDFSシェルコマンドを実行する際に使用するLinuxユーザーを指定します。
-   この設定項目が設定されていない場合、TiKVは現在のLinuxユーザーを使用します。
-   デフォルト値: `""`

## ログバックアップ {#log-backup}

ログバックアップに関連するコンフィグレーション項目。

### <span class="version-mark">v6.2.0で</span><code>enable</code> {#code-enable-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログバックアップを有効にするかどうかを決定します。
-   デフォルト値: `true`

### <code>file-size-limit</code> <span class="version-mark">v6.2.0で追加</span> {#code-file-size-limit-code-span-class-version-mark-new-in-v6-2-0-span}

-   保存するバックアップログデータのサイズ制限。
-   デフォルト値: 256MiB
-   注：通常、 `file-size-limit`の値は、外部storageに表示されるバックアップファイルのサイズよりも大きくなります。これは、バックアップファイルが外部storageにアップロードされる前に圧縮されるためです。

### <code>initial-scan-pending-memory-quota</code> <span class="version-mark">v6.2.0 の新機能</span> {#code-initial-scan-pending-memory-quota-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログバックアップ中に増分スキャンデータを保存するために使用されるキャッシュの割り当て量。
-   デフォルト値: `min(Total machine memory * 10%, 512 MiB)`

### <code>initial-scan-rate-limit</code> <span class="version-mark">v6.2.0で追加</span> {#code-initial-scan-rate-limit-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログバックアップ中の増分データスキャンにおけるスループットの制限値。これは、1秒間にディスクから読み取れるデータの最大量を意味します。数値のみを指定した場合（例： `60` ）、単位はKiBではなくバイトになります。
-   デフォルト値: 60MiB
-   最小値: 1MiB

### <code>max-flush-interval</code> <span class="version-mark">v6.2.0で追加</span> {#code-max-flush-interval-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログバックアップにおいて、バックアップデータを外部storageに書き込む最大間隔。
-   デフォルト値：3分

### <code>num-threads</code> <span class="version-mark">（v6.2.0の新機能）</span> {#code-num-threads-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログバックアップで使用されるスレッド数。
-   デフォルト値：CPU * 0.5
-   値の範囲：[2, 12]

### <code>temp-path</code> <span class="version-mark">v6.2.0 で追加されました。</span> {#code-temp-path-code-span-class-version-mark-new-in-v6-2-0-span}

-   ログファイルが外部storageに書き込まれる前に一時的に保存されるパス。
-   デフォルト値: `${deploy-dir}/data/log-backup-temp`

## CDC {#cdc}

TiCDCに関連するコンフィグレーション項目。

### <code>min-ts-interval</code> {#code-min-ts-interval-code}

-   解決済みTSが計算され、転送される間隔。
-   デフォルト値: `"1s"` 。

> **注記：**
>
> バージョン6.5.0では、CDCの遅延を削減するために、 `min-ts-interval`のデフォルト値が`"1s"`から`"200ms"`に変更されました。バージョン6.5.1以降では、ネットワークレイテンシーを削減するために、このデフォルト値が`"1s"`に戻されます。

### <code>old-value-cache-memory-quota</code> {#code-old-value-cache-memory-quota-code}

-   TiCDCの旧値におけるメモリ使用量の上限。
-   デフォルト値: `512MiB`

### <code>sink-memory-quota</code> {#code-sink-memory-quota-code}

-   TiCDCデータ変更イベントによるメモリ使用量の上限。
-   デフォルト値: `512MiB`

### <code>incremental-scan-speed-limit</code> {#code-incremental-scan-speed-limit-code}

-   履歴データが段階的にスキャンされる最大速度。
-   デフォルト値： `"128MiB"` 、これは1秒あたり128 MiBを意味します。

### <code>incremental-scan-threads</code> {#code-incremental-scan-threads-code}

-   履歴データを増分的にスキャンするタスクに使用するスレッド数。
-   デフォルト値： `4` 、これは4つのスレッドを意味します。

### <code>incremental-scan-concurrency</code> {#code-incremental-scan-concurrency-code}

-   履歴データを増分的にスキャンするタスクの同時実行の最大数。
-   デフォルト値： `6` 。これは、最大で6つのタスクを同時に実行できることを意味します。
-   注： `incremental-scan-concurrency`の値は`incremental-scan-threads`の値以上でなければなりません。そうでない場合、TiKV は起動時にエラーを報告します。

### <code>incremental-scan-concurrency-limit</code> <span class="version-mark">（v7.6.0で追加）</span> {#code-incremental-scan-concurrency-limit-code-span-class-version-mark-new-in-v7-6-0-span}

-   履歴データを増分スキャンするタスクの実行待ちキューの最大長。実行待ちタスク数がこの制限を超えると、新規タスクは拒否されます。
-   デフォルト値： `10000` 。これは、最大で10000個のタスクを実行待ちキューに入れることができることを意味します。
-   注: `incremental-scan-concurrency-limit` [`incremental-scan-concurrency`](#incremental-scan-concurrency)以上である必要があります。そうでない場合、TiKV は`incremental-scan-concurrency`を使用してこの設定を上書きします。

## resolved-ts {#resolved-ts}

ステイル読み取りリクエストを処理するために、解決済みのTSを維持することに関連するコンフィグレーション項目。

### <code>enable</code> {#code-enable-code}

-   すべてのリージョンに対して解決済みTSを維持するかどうかを決定します。
-   デフォルト値: `true`

### <code>advance-ts-interval</code> {#code-advance-ts-interval-code}

-   解決済みTSが計算され、転送される間隔。
-   デフォルト値: `"20s"`

### <code>scan-lock-pool-size</code> {#code-scan-lock-pool-size-code}

-   Resolved TS を初期化する際に、TiKV が MVCC (マルチバージョン同時実行制御) ロックデータをスキャンするために使用するスレッドの数。
-   デフォルト値: `2`は、2つのスレッドを意味します。

## pessimistic-txn {#pessimistic-txn}

悲観的トランザクションの使用法については、 [TiDB悲観的トランザクションモード](/pessimistic-transaction.md)を参照してください。

### <code>wait-for-lock-timeout</code> {#code-wait-for-lock-timeout-code}

-   TiKV の悲観的トランザクションが他のトランザクションがロックを解放するのを待つ最長時間。タイムアウトが発生した場合、TiDB にエラーが返され、TiDB はロックの追加を再試行します。ロック待機タイムアウトは`innodb_lock_wait_timeout`で設定されます。
-   デフォルト値: `"1s"`
-   最小値: `"1ms"`

### <code>wake-up-delay-duration</code> {#code-wake-up-delay-duration-code}

-   悲観的トランザクションがロックを解放すると、ロックを待機しているすべてのトランザクションのうち、 `start_ts`最小のトランザクションのみが起動されます。他のトランザクションは`wake-up-delay-duration`の後に起動されます。
-   デフォルト値: `"20ms"`

### <code>pipelined</code> {#code-pipelined-code}

-   この設定項目を有効にすると、悲観的ロックを追加するパイプライン処理が有効になります。この機能を有効にすると、データがロック可能であることを検出した後、TiKV は直ちに TiDB に通知し、後続のリクエストを実行して悲観的ロックを非同期で書き込みます。これにより、レイテンシーが大幅に削減され、悲観的トランザクションのパフォーマンスが著しく向上します。ただし、悲観的ロックの非同期書き込みが失敗する可能性は依然として低く、その場合、悲観的トランザクションのコミットが失敗する可能性があります。
-   デフォルト値: `true`

### <code>in-memory</code> <span class="version-mark">（v6.0.0の新機能）</span> {#code-in-memory-code-span-class-version-mark-new-in-v6-0-0-span}

-   インメモリ悲観的ロック機能を有効にします。この機能を有効にすると、悲観的トランザクションはロックをディスクに書き込んだり、他のレプリカに複製したりする代わりに、ロックをメモリに保存しようとします。これにより、悲観的トランザクションのパフォーマンスが向上します。ただし、悲観的ロックが失われ、悲観的トランザクションのコミットが失敗する可能性は依然として低いながらも存在します。
-   デフォルト値: `true`
-   `in-memory`は、 `pipelined`の値が`true`の場合にのみ有効になることに注意してください。

### <code>in-memory-peer-size-limit</code> <span class="version-mark">v8.4.0で追加</span> {#code-in-memory-peer-size-limit-code-span-class-version-mark-new-in-v8-4-0-span}

-   リージョン内の[インメモリ悲観的ロック](/pessimistic-transaction.md#in-memory-pessimistic-lock)のメモリ使用制限を制御します。この制限を超えると、TiKV は悲観的ロックを永続的に書き込みます。
-   デフォルト値: `512KiB`
-   単位：KiB｜MiB｜GiB

### <code>in-memory-instance-size-limit</code> <span class="version-mark">v8.4.0で追加</span> {#code-in-memory-instance-size-limit-code-span-class-version-mark-new-in-v8-4-0-span}

-   TiKV インスタンスの[インメモリ悲観的ロック](/pessimistic-transaction.md#in-memory-pessimistic-lock)のメモリ使用量制限を制御します。この制限を超えると、TiKV は悲観的ロックを永続的に書き込みます。
-   デフォルト値: `100MiB`
-   単位：KiB｜MiB｜GiB

## クォータ {#quota}

クォータリミッターに関連するコンフィグレーション項目。

### <code>max-delay-duration</code> <span class="version-mark">v6.0.0で追加</span> {#code-max-delay-duration-code-span-class-version-mark-new-in-v6-0-0-span}

-   単一の読み取りまたは書き込みリクエストがフォアグラウンドで処理されるまでに強制的に待機させられる最大時間。
-   デフォルト値: `500ms`
-   推奨設定：ほとんどの場合、デフォルト値を使用することをお勧めします。インスタンスでメモリ不足（OOM）や激しいパフォーマンスの不安定さが発生する場合は、値を1Sに設定して、リクエストの待機時間を1秒未満に短縮できます。

### フォアグラウンドクォータリミッター {#foreground-quota-limiter}

フォアグラウンドのクォータリミッターに関連するコンフィグレーション項目。

TiKV がデプロイされているマシンにリソースが限られている場合、たとえば、CPU が 4V、メモリが16GB しかないとします。このような状況では、TiKV のフォアグラウンドが読み書き要求を過剰に処理し、バックグラウンドで使用される CPU リソースがこれらの要求の処理に占有され、TiKV のパフォーマンスの安定性に影響する可能性があります。この状況を回避するには、フォアグラウンドのクォータ関連の設定項目を使用して、フォアグラウンドで使用される CPU リソースを制限できます。要求がクォータ リミッターをトリガーすると、要求は TiKV が CPU リソースを解放するまでしばらく待機させられます。正確な待機時間は要求の数によって異なり、最大待機時間は[`max-delay-duration`](#max-delay-duration-new-in-v600)の値を超えません。

#### <code>foreground-cpu-time</code> <span class="version-mark">v6.0.0の新機能</span> {#code-foreground-cpu-time-code-span-class-version-mark-new-in-v6-0-0-span}

-   TiKVフォアグラウンドが読み取りおよび書き込み要求を処理するために使用するCPUリソースのソフトリミット。
-   デフォルト値： `0` （制限なしを意味します）
-   単位：ミリCPU（例： `1500`は、フォアグラウンドリクエストが1.5VのCPUを消費することを意味します）
-   推奨設定: 4 コアを超えるインスタンスの場合は、デフォルト値`0`を使用してください。4 コアのインスタンスの場合は、値を`1000`と`1500`の範囲に設定するとバランスが取れます。2 コアのインスタンスの場合は、値を`1200`より小さくしてください。

#### <code>foreground-write-bandwidth</code> <span class="version-mark">v6.0.0の新機能</span> {#code-foreground-write-bandwidth-code-span-class-version-mark-new-in-v6-0-0-span}

-   トランザクションがデータを書き込む際の帯域幅に対するソフトリミット。
-   デフォルト値： `0KiB` （制限なしを意味します）
-   推奨設定：ほとんどの場合、デフォルト値の`0`を使用してください。ただし、 `foreground-cpu-time`の設定では書き込み帯域幅を十分に制限できない場合は除きます。例外として、コア数が4以下のインスタンスでは、 `50MiB`よりも小さい値を設定することをお勧めします。

#### <code>foreground-read-bandwidth</code> <span class="version-mark">v6.0.0の新機能</span> {#code-foreground-read-bandwidth-code-span-class-version-mark-new-in-v6-0-0-span}

-   トランザクションとコプロセッサーがデータを読み取る際の帯域幅のソフトリミット。
-   デフォルト値： `0KiB` （制限なしを意味します）
-   推奨設定：ほとんどの場合、デフォルト値の`0`を使用してください。ただし、 `foreground-cpu-time`の設定では読み取り帯域幅を十分に制限できない場合は除きます。例外として、コア数が4以下のインスタンスでは、 `20MiB`よりも小さい値を設定することをお勧めします。

### バックグラウンドクォータリミッター {#background-quota-limiter}

バックグラウンドクォータリミッターに関連するコンフィグレーション項目。

TiKV がデプロイされているマシンにリソースが限られている場合、たとえば CPU が 4V、メモリが16GB しかない場合を考えてみましょう。このような状況では、TiKV のバックグラウンドで計算や読み書き要求が多すぎると、フォアグラウンドで使用される CPU リソースがこれらの要求の処理に占有され、TiKV のパフォーマンスの安定性に影響します。この状況を回避するには、バックグラウンドのクォータ関連の設定項目を使用して、バックグラウンドで使用される CPU リソースを制限できます。要求がクォータ リミッターをトリガーすると、TiKV が CPU リソースを解放するまで、要求はしばらく待機させられます。正確な待機時間は要求の数によって異なり、最大待機時間は[`max-delay-duration`](#max-delay-duration-new-in-v600)の値を超えません。

> **警告：**
>
> -   バックグラウンドクォータリミッターは、TiDB v6.2.0で導入された実験的機能であり、本番環境での使用は推奨され**ません**。
> -   この機能は、リソースが限られた環境でのみ適しており、TiKVがそのような環境でも安定して動作することを保証します。リソースが豊富な環境でこの機能を有効にすると、リクエスト数がピークに達した際にパフォーマンスが低下する可能性があります。

#### <code>background-cpu-time</code> <span class="version-mark">v6.2.0の新機能</span> {#code-background-cpu-time-code-span-class-version-mark-new-in-v6-2-0-span}

-   TiKVバックグラウンドが読み取りおよび書き込み要求を処理するために使用するCPUリソースのソフトリミット。
-   デフォルト値： `0` （制限なしを意味します）
-   単位：ミリCPU（例： `1500`は、バックグラウンドリクエストが1.5VのCPUを消費することを意味します）

#### <code>background-write-bandwidth</code> <span class="version-mark">v6.2.0の新機能</span> {#code-background-write-bandwidth-code-span-class-version-mark-new-in-v6-2-0-span}

-   バックグラウンドトランザクションがデータを書き込む際の帯域幅に対するソフトリミット。
-   デフォルト値： `0KiB` （制限なしを意味します）

#### <code>background-read-bandwidth</code> <span class="version-mark">v6.2.0の新機能</span> {#code-background-read-bandwidth-code-span-class-version-mark-new-in-v6-2-0-span}

-   バックグラウンドトランザクションとコプロセッサーがデータを読み取る際の帯域幅のソフトリミット。
-   デフォルト値： `0KiB` （制限なしを意味します）

#### <code>enable-auto-tune</code> <span class="version-mark">v6.2.0の新機能</span> {#code-enable-auto-tune-code-span-class-version-mark-new-in-v6-2-0-span}

-   クォータの自動調整を有効にするかどうかを決定します。この設定項目が有効になっている場合、TiKVはTiKVインスタンスの負荷に基づいて、バックグラウンドリクエストのクォータを動的に調整します。
-   デフォルト値： `false` （これは自動チューニングが無効になっていることを意味します）

## causal-ts <span class="version-mark">v6.1.0の新機能</span> {#causal-ts-span-class-version-mark-new-in-v6-1-0-span}

TiKV API V2 が有効になっている場合にタイムスタンプを取得することに関連するコンフィグレーション項目 ( `storage.api-version = 2` )。

書き込みレイテンシーを低減するため、TiKVは定期的にタイムスタンプのバッチをローカルに取得してキャッシュします。キャッシュされたタイムスタンプは、PDへの頻繁なアクセスを回避し、TSOサービスの一時的な障害を許容するのに役立ちます。

### <code>alloc-ahead-buffer</code> <span class="version-mark">v6.4.0で追加</span> {#code-alloc-ahead-buffer-code-span-class-version-mark-new-in-v6-4-0-span}

-   事前割り当て済みのTSOキャッシュサイズ（期間）。
-   TiKV は、この構成項目で指定された期間に基づいて TSO キャッシュを事前割り当てします。TiKV は、前の期間に基づいて TSO の使用量を推定し、 `alloc-ahead-buffer`満たす TSO をローカルに要求してキャッシュします。
-   この構成項目は、TiKV API V2 が有効になっている場合の PD 障害の許容度を高めるためによく使用されます ( `storage.api-version = 2` )。
-   この設定項目の値を大きくすると、TSOの消費量とTiKVのメモリオーバーヘッドが増加する可能性があります。十分なTSOを確保するには、PDの設定項目[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)の値を下げることをお勧めします。
-   テストによると、 `alloc-ahead-buffer`がデフォルト値の場合、PDリーダーが故障して別のノードに切り替わると、書き込みリクエストのレイテンシーが一時的に増加し、QPSが約15%減少します。
-   ビジネスへの影響を避けるため、PDで`tso-update-physical-interval = "1ms"`を設定し、TiKVで以下の設定項目を設定してください。
    -   `causal-ts.alloc-ahead-buffer = "6s"`
    -   `causal-ts.renew-batch-max-size = 65536`
    -   `causal-ts.renew-batch-min-size = 2048`
-   デフォルト値: `3s`

### <code>renew-interval</code> {#code-renew-interval-code}

-   ローカルにキャッシュされたタイムスタンプが更新される間隔。
-   `renew-interval`の間隔で、TiKV はタイムスタンプの更新バッチを開始し、前の期間のタイムスタンプ消費量と[`alloc-ahead-buffer`](#alloc-ahead-buffer-new-in-v640)の設定に応じてキャッシュされたタイムスタンプの数を調整します。このパラメータを大きすぎる値に設定すると、最新の TiKV ワークロードの変更がタイムリーに反映されません。このパラメータを小さすぎる値に設定すると、PD の負荷が増加します。書き込みトラフィックが大きく変動し、タイムスタンプが頻繁に枯渇し、書き込みレイテンシーが増加する場合は、このパラメータを小さめの値に設定できます。同時に、PD の負荷も考慮する必要があります。
-   デフォルト値: `"100ms"`

### <code>renew-batch-min-size</code> {#code-renew-batch-min-size-code}

-   タイムスタンプ要求におけるTSOの最小数。
-   TiKV は、前の期間のタイムスタンプ消費量に応じて、キャッシュされたタイムスタンプの数を調整します。必要な TSO が少ない場合は、TiKV は要求される TSO の数を`renew-batch-min-size`に達するまで減らします。アプリケーションで大量のバースト書き込みトラフィックが頻繁に発生する場合は、このパラメータを適切な値に設定できます。このパラメータは、単一の tikv-server のキャッシュ サイズであることに注意してください。このパラメータを大きすぎる値に設定し、クラスタに多数の tikv-server が含まれている場合、TSO の消費が速すぎることになります。
-   Grafana の**TiKV-RAW** &gt; **Causal timestamp**パネルでは、 **TSO バッチ サイズ**は、アプリケーションのワークロードに応じて動的に調整されるローカル キャッシュされたタイムスタンプの数です。このメトリックを参照して`renew-batch-min-size`を調整できます。
-   デフォルト値: `100`

### <code>renew-batch-max-size</code> <span class="version-mark">v6.4.0で追加</span> {#code-renew-batch-max-size-code-span-class-version-mark-new-in-v6-4-0-span}

-   タイムスタンプ要求におけるTSOの最大数。
-   デフォルトのTSO物理時間更新間隔（ `50ms` ）では、PDは最大262144個のTSOを提供します。要求されたTSOがこの数を超えると、PDはそれ以上TSOを提供しません。この設定項目は、TSOの枯渇と、TSO枯渇が他の業務に及ぼす逆効果を回避するために使用されます。高可用性を向上させるためにこの設定項目の値を増やす場合は、十分なTSOを確保するために、同時に[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)の値を減らす必要があります。
-   デフォルト値: `8192`

## リソース計測 {#resource-metering}

リソース計測に関連するコンフィグレーション項目。

### <code>enable-network-io-collection</code> <span class="version-mark">v8.5.6の新機能</span> {#code-enable-network-io-collection-code-span-class-version-mark-new-in-v8-5-6-span}

-   CPUデータに加えて、TiKVネットワークトラフィックと論理I/O情報を[Top SQL](/dashboard/top-sql.md)に収集するかどうかを制御します。
-   TiKVを有効にすると、リクエスト処理中に受信ネットワークバイト、送信ネットワークバイト、論理読み取りバイト、および論理書き込みバイトも記録されます。
-   TiKVはリソース消費量を報告する際、CPU時間、ネットワークトラフィック、論理I/Oに基づいて上位N件のレコードをフィルタリングし、さらにリージョン別にこれらの統計情報を報告することで、ホットスポット要求やリソース使用状況の発生源をより詳細に分析できるようにします。
-   デフォルト値: `false`

> **注記：**
>
> 論理I/Oは物理I/Oと等価ではなく、直接相関させることはできません。
>
> -   論理I/Oとは、TiKVstorageレイヤーにおいてリクエストによって処理されるデータの論理的な量を指し、例えば、読み取り時にスキャンまたは処理されるデータや、書き込みリクエストによって書き込まれるデータなどが含まれます。
> -   物理I/Oとは、基盤となるstorageデバイス上での実際のディスク読み書きトラフィックを指し、ブロックキャッシュ、圧縮、フラッシュ、その他の要因によって影響を受けます。

## リソース制御 {#resource-control}

TiKVstorageレイヤーのリソース制御に関連するコンフィグレーション項目。

### <code>enabled</code> <span class="version-mark">（v6.6.0で新規追加）</span> {#code-enabled-code-span-class-version-mark-new-in-v6-6-0-span}

-   対応するリソース グループの[リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)に従って、ユーザーのフォアグラウンド読み取り/書き込みリクエストのスケジューリングを有効にするかどうかを制御します。 TiDB リソース グループとリソース制御の詳細については、[リソース制御を使用して、リソースグループの制限とフロー制御を実現します。](/tidb-resource-control-ru-groups.md)参照してください。
-   この設定項目を有効にするには、TiDB で[`tidb_enable_resource_control](/system-variables.md#tidb_enable_resource_control-new-in-v660)が有効になっている必要があります。この設定項目が有効になっている場合、TiKV は優先度キューを使用して、フォアグラウンド ユーザーからのキューに登録された読み取り/書き込みリクエストをスケジュールします。リクエストのスケジュール優先度は、そのリクエストを受け取るリソース グループが既に消費しているリソースの量に反比例し、対応するリソース グループのクォータに比例します。
-   デフォルト値: `true` 。これは、リソースグループのRUに基づいたスケジューリングが有効になっていることを意味します。

### <code>priority-ctl-strategy</code> <span class="version-mark">v8.4.0で追加</span> {#code-priority-ctl-strategy-code-span-class-version-mark-new-in-v8-4-0-span}

優先度の低いタスクに対するフロー制御戦略を指定します。TiKVは、優先度の低いタスクにフロー制御を適用することで、優先度の高いタスクの実行を優先します。

-   お得なオプション：
    -   `aggressive` : このポリシーは優先度の高いタスクのパフォーマンスを優先し、優先度の高いタスクのスループットとレイテンシーにはほとんど影響を与えないようにしますが、優先度の低いタスクの実行速度は低下します。
    -   `moderate` : このポリシーは、優先度の低いタスクに対してバランスの取れたフロー制御を課し、優先度の高いタスクへの影響を少なくします。
    -   `conservative` : このポリシーは、システム リソースが最大限に活用されることを優先し、優先度の低いタスクが必要に応じてシステムで利用可能なリソースを最大限に活用できるようにするため、優先度の高いタスクのパフォーマンスに大きな影響を与えます。
-   デフォルト値: `moderate` 。

## スプリット {#split}

[ロードベース分割](/configure-load-base-split.md)に関するコンフィグレーション項目。

### <code>byte-threshold</code> <span class="version-mark">v5.0 で追加</span> {#code-byte-threshold-code-span-class-version-mark-new-in-v5-0-span}

-   リージョンがホットスポットとして識別されるトラフィックのしきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size) 4 GiB 未満の場合、1 秒あたり`30MiB` 。
    -   [`region-split-size`](#region-split-size)が 4 GiB 以上の場合、1 秒あたり`100MiB` 。

### <code>qps-threshold</code> {#code-qps-threshold-code}

-   リージョンがホットスポットとして識別されるQPSしきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size) 4 GiB 未満の場合、 `3000` 。
    -   [`region-split-size`](#region-split-size)が 4 GiB 以上の場合`7000` 。

### <code>region-cpu-overload-threshold-ratio</code> <span class="version-mark">v6.2.0の新機能</span> {#code-region-cpu-overload-threshold-ratio-code-span-class-version-mark-new-in-v6-2-0-span}

-   リージョンがホットスポットとして識別される際のCPU使用率のしきい値を制御します。
-   デフォルト値:

    -   [`region-split-size`](#region-split-size) 4 GiB 未満の場合、 `0.25` 。
    -   [`region-split-size`](#region-split-size)が 4 GiB 以上の場合`0.75` 。

## メモリ<span class="version-mark">v7.5.0の新機能</span> {#memory-span-class-version-mark-new-in-v7-5-0-span}

### <code>enable-heap-profiling</code> <span class="version-mark">v7.5.0の新機能</span> {#code-enable-heap-profiling-code-span-class-version-mark-new-in-v7-5-0-span}

-   TiKVのメモリ使用量を追跡するためにヒーププロファイリングを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>profiling-sample-per-bytes</code> <span class="version-mark">（v7.5.0の新機能）</span> {#code-profiling-sample-per-bytes-code-span-class-version-mark-new-in-v7-5-0-span}

-   ヒーププロファイリングによって毎回サンプリングされるデータ量を指定します。値は2のべき乗に切り上げられます。
-   デフォルト値: `512KiB`

### <code>enable-thread-exclusive-arena</code> <span class="version-mark">v8.1.0の新機能</span> {#code-enable-thread-exclusive-arena-code-span-class-version-mark-new-in-v8-1-0-span}

-   TiKVスレッドレベルでメモリ割り当て状況を表示して、各TiKVスレッドのメモリ使用量を追跡するかどうかを制御します。
-   デフォルト値: `true`

## インメモリエンジン<span class="version-mark">v8.5.0の新機能</span> {#in-memory-engine-span-class-version-mark-new-in-v8-5-0-span}

TiKV MVCC インメモリエンジン (IME) のstorageレイヤーに関連する構成項目。

### <span class="version-mark">v8.5.0で</span><code>enable</code> {#code-enable-code-span-class-version-mark-new-in-v8-5-0-span}

> **注記：**
>
> この設定項目は設定ファイルで設定できますが、SQL文で照会することはできません。

-   インメモリ エンジンを有効にしてマルチバージョン クエリを高速化するかどうか。インメモリ エンジンの詳細については、 [TiKV MVCC インメモリエンジン](/tikv-in-memory-engine.md)を参照してください。
-   デフォルト値: `false` (インメモリエンジンは無効になっています)
-   TiKVノードには最低でも8GiBのメモリを搭載することを推奨します。最適なパフォーマンスを得るには、32GiB以上を搭載することをお勧めします。
-   TiKVノードで使用可能なメモリが不足している場合、この設定項目が`true`に設定されていても、インメモリエンジンは有効になりません。このような場合は、TiKVログファイルで`"in-memory engine is disabled because"`を含むメッセージを確認し、インメモリエンジンが有効にならない理由を調べてください。

### <code>capacity</code> <span class="version-mark">（v8.5.0の新</span>機能） {#code-capacity-code-span-class-version-mark-new-in-v8-5-0-span}

> **注記：**
>
> -   インメモリエンジンが有効になると、 `block-cache.capacity`自動的に 10% 減少します。
> -   `capacity`手動で設定した場合、 `block-cache.capacity`自動的に減少しません。この場合、メモリ不足エラー（OOM）を回避するために、その値を手動で調整する必要があります。

-   [TiKV MVCC インメモリエンジン](/tikv-in-memory-engine.md)が使用できる最大メモリサイズを制御します。メモリ容量によって、キャッシュできるリージョンの数が決まります。容量がいっぱいになると、インメモリエンジンはリージョンMVCCの冗長性に基づいて新しいリージョンをロードし、キャッシュされたリージョンを削除します。
-   デフォルト値: `min(10% of the total system memory, 5 GiB)`

### <code>gc-run-interval</code> <span class="version-mark">v8.5.0で追加</span> {#code-gc-run-interval-code-span-class-version-mark-new-in-v8-5-0-span}

-   インメモリエンジンGCがMVCCバージョンをキャッシュする時間間隔を制御します。このパラメータを小さくするとGCの頻度が上がり、MVCCバージョンの数を減らすことができますが、GCのCPU使用率が増加し、インメモリエンジンのキャッシュミスが発生する確率が高くなります。
-   デフォルト値: `"3m"`

### <code>mvcc-amplification-threshold</code> <span class="version-mark">v8.5.0で追加</span> {#code-mvcc-amplification-threshold-code-span-class-version-mark-new-in-v8-5-0-span}

-   インメモリエンジンがリージョンを選択してロードする際の、MVCC読み取り増幅のしきい値を制御します。デフォルト値は`10`で、リージョン内の1行を読み取るのに10を超えるMVCCバージョンを処理する必要がある場合は、そのリージョンがインメモリエンジンにロードされる可能性があることを示します。
-   デフォルト値: `10`
