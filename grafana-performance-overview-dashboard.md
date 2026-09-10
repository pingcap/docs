---
title: Key Metrics on Performance Overview
summary: パフォーマンス概要ダッシュボードに表示される主要な指標を確認します。
---

# パフォーマンス概要の主要指標 {#key-metrics-on-performance-overview}

TiUPを使用してTiDBクラスターをデプロイする場合、監視システム（PrometheusとGrafana）も同時にデプロイされます。詳細については、 [TiDB 監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

Grafanaダッシュボードは、PD、TiDB、TiKV、Node_exporter、概要、パフォーマンス概要を含む一連のサブダッシュボードに分かれています。診断に役立つ多くのメトリックが用意されています。

パフォーマンス概要ダッシュボードは、TiDB、PD、および TiKV のメトリックを調整し、それぞれを次のセクションで表示します。

- Overview：データベース時間とSQL実行時間の概要。概要で異なる色を確認することで、データベースのワークロードプロファイルとパフォーマンスのボトルネックを素早く特定できます。

- Load profile: データベース QPS、接続情報、アプリケーションが TiDB と対話する MySQL コマンド タイプ、データベース内部 TSO および KV リクエスト OPS、TiKV および TiDB のリソース使用量など、主要なメトリックとリソース使用量。

- Top-down latency breakdown: クエリレイテンシーと接続アイドル時間の比率、クエリレイテンシーの内訳、実行中の TSO/KV リクエストレイテンシー、TiKV 内の書き込みレイテンシーの内訳。

パフォーマンス概要ダッシュボードを使用すると、パフォーマンスを効率的に分析し、ユーザー応答時間のボトルネックがデータベースにあるかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要、ワークロードプロファイル、SQLレイテンシーの内訳を表示することで、データベース内のボトルネックを特定できます。詳細は[パフォーマンス分析とチューニング](/performance-tuning-methods.md)ご覧ください。

次のセクションでは、パフォーマンス概要ダッシュボードのメトリックについて説明します。

## Performance Overview {#performance-overview}

### Database Time by SQL Type {#database-time-by-sql-type}

- database time: 1秒あたりの合計データベース時間
- sql_type: 各タイプのSQL文で1秒あたりに消費されたデータベース時間

### Database Time by SQL Phase {#database-time-by-sql-phase}

- database time: 1秒あたりの合計データベース時間
- get token/parse/compile/execute: 4つのSQL処理フェーズで消費されるデータベース時間

SQL実行フェーズは緑色で、その他のフェーズは全体的に赤色で表示されます。緑色以外の領域が大きい場合は、実行フェーズ以外のフェーズでデータベース時間が大量に消費されていることを意味し、さらなる原因分析が必要です。

### SQL Execute Time Overview {#sql-execute-time-overview}

- execute time: SQL 実行中に 1秒あたりに消費されるデータベース時間
- tso_wait: SQL実行中の1秒あたりの同時TSO待機時間
- kv request type: SQL実行中に各KVリクエストタイプを1秒あたりに待機する時間。KVリクエストは同時実行されるため、合計KVリクエスト待機時間はSQL実行時間を超える場合があります。
- tiflash_mpp: SQL 実行中に 1秒あたりにTiFlashリクエストを処理する時間。

緑のメトリクスは一般的なKV書き込みリクエスト（プリライトやコミットなど）、青のメトリクスは一般的な読み取りリクエスト、紫のメトリクスはTiFlash MPPリクエストを表します。その他の色のメトリクスは、注意が必要な予期しない状況を表します。例えば、悲観的ロックKVリクエストは赤で、TSO待機は濃い茶色で表示されます。

青または緑以外の領域が大きい場合は、SQL実行中にボトルネックが発生していることを意味します。例：

- 重大なロック競合が発生した場合、赤色の領域が大きな割合を占めることになります。
- TSO の待ち時間に過度に時間がかかってしまうと、濃い茶色の領域が大きな割合を占めることになります。

### QPS {#qps}

すべての TiDB インスタンスで 1秒あたりに実行された SQL 文の数（タイプ別に収集: `SELECT`、`INSERT`、`UPDATE`など）

### CPS By Type {#cps-by-type}

タイプに基づいて、すべての TiDB インスタンスによって 1秒あたりに処理されるコマンドの数

### Queries Using Plan Cache OPS {#queries-using-plan-cache-ops}

- avg-hit: すべての TiDB インスタンスで 1秒あたりに実行計画 キャッシュを使用するクエリの数
- avg-miss: すべての TiDB インスタンスにおける、実行計画 キャッシュを使用していないクエリの数 (1秒あたり)

`avg-hit + avg-miss`は`StmtExecute`に等しく、これは 1秒あたりに実行されるすべてのクエリの数です。

### KV/TSO Request OPS {#kv-tso-request-ops}

- kv request total: すべてのTiDBインスタンスにおける1秒あたりのKVリクエストの合計数
- kv request by type: `Get`、`Prewrite`、`Commit`などのタイプに基づいて、すべての TiDB インスタンスでの 1秒あたりの KV リクエスト数
- tso - cmd: TiDB がすべての TiDB インスタンスの PD に送信する 1秒あたりの gRPC リクエストの数。各 gRPC リクエストには、TSO リクエストのバッチが含まれます。
- tso - request: すべての TiDB インスタンスにおける 1秒あたりの TSO リクエスト数

通常、 `tso - request`を`tso - cmd`で割った値が、1秒あたりの TSO リクエストバッチの平均サイズになります。

### KV Request Time By Source {#kv-request-time-by-source}

- kv request total time: すべての TiDB インスタンスで 1秒あたりに KV およびTiFlashリクエストを処理する合計時間
- 各 KV リクエストとそれに対応するリクエストソースは積み上げ棒グラフを形成し、 `external`通常のビジネス リクエストを識別し、 `internal`内部アクティビティ リクエスト (DDL やauto analyzeリクエストなど) を識別します。

### TiDB CPU {#tidb-cpu}

- avg: すべての TiDB インスタンスの平均 CPU 使用率
- delta: すべての TiDB インスタンスの最大 CPU 使用率からすべての TiDB インスタンスの最小 CPU 使用率を引いた値
- max: すべての TiDB インスタンスの最大 CPU 使用率

### TiKV CPU/IO MBps {#tikv-cpu-io-mbps}

- CPU-Avg: すべての TiKV インスタンスの平均 CPU 使用率
- CPU-Delta: すべての TiKV インスタンスの最大 CPU 使用率からすべての TiKV インスタンスの最小 CPU 使用率を引いた値
- CPU-MAX: すべての TiKV インスタンス間の最大 CPU 使用率
- IO-Avg: すべての TiKV インスタンスの平均 MBps
- IO-Delt: すべての TiKV インスタンスの最大 MBps からすべての TiKV インスタンスの最小 MBps を引いた値
- IO-MAX: すべての TiKV インスタンスの最大 MBps

### Duration {#duration}

- Duration: 実行時間

    - クライアントからのリクエストをTiDBが受信してから、TiDBがそのリクエストを実行し、結果をクライアントに返すまでの時間。通常、クライアントからのリクエストはSQL文の形式で送信されますが、この時間には`COM_PING` 、 `COM_SLEEP` 、 `COM_STMT_FETCH` 、 `COM_SEND_LONG_DATA`などのコマンドの実行時間も含まれる場合があります。
    - TiDBはマルチクエリをサポートしています。つまり、クライアントは一度に複数のSQL文（例： `select 1; select 1; select 1;`を送信できます。この場合、このクエリの合計実行時間には、すべてのSQL文の実行時間が含まれます。

- avg: すべてのリクエストを実行するのにかかった平均時間

- 99: すべてのリクエストを実行するためのP99期間

- avg by type: すべての TiDB インスタンス内のすべてのリクエストを実行するのにかかった平均時間（タイプ別に収集: `SELECT`、`INSERT`、`UPDATE`）

### Connection Idle Duration {#connection-idle-duration}

接続アイドル期間は、接続がアイドル状態にある期間を示します。

- avg-in-txn: トランザクション内の接続の平均アイドル時間
- avg-not-in-txn: 接続がトランザクション内にない場合の平均接続アイドル期間
- 99-in-txn: 接続がトランザクション内にある場合の P99 接続アイドル期間

### Connection Count {#connection-count}

- total: すべてのTiDBインスタンスへの接続数
- active connections: すべての TiDB インスタンスへのアクティブな接続の数
- tidb-{node-number}-peer: 各TiDBインスタンスへの接続数
- disconnection/s: TiDB クラスタ内の切断回数
- 99-not-in-txn: 接続がトランザクション内にない場合の P99 接続アイドル期間

### Parse Duration, Compile Duration, and Execute Duration {#parse-duration-compile-duration-and-execute-duration}

- Parse Duration: SQL文の解析にかかった時間
- Compile Duration: 解析されたSQL ASTを実行計画にコンパイルするのにかかる時間
- Execution Duration: SQL文の実行計画の実行に要した時間

これら3つのメトリックにはすべて、すべての TiDB インスタンスの平均期間と 99 パーセンタイル期間が含まれます。

### Avg TiDB KV Request Duration {#avg-tidb-kv-request-duration}

`Get` 、 `Prewrite` 、 `Commit`を含むタイプに基づいて、すべての TiDB インスタンスでの KV リクエストの実行に費やされた平均時間。

### Avg TiKV GRPC Duration {#avg-tikv-grpc-duration}

`kv_get` 、 `kv_prewrite` 、 `kv_commit`を含むタイプに基づいて、すべての TiKV インスタンスでの gRPC リクエストの実行に費やされた平均時間。

### PD TSO Wait/RPC Duration {#pd-tso-wait-rpc-duration}

- wait - avg: すべての TiDB インスタンスで PD が TSO を返すのを待つ平均時間
- rpc - avg: TiDB が TSO を取得するために PD に gRPC リクエストを送信してから、すべての TiDB インスタンスで TiDB が TSO を受信するまでの平均期間
- wait - 99: すべての TiDB インスタンスで PD が TSO を返すのを待つ P99 期間
- rpc - 99: TiDB が TSO を取得するために PD に gRPC リクエストを送信してから、すべての TiDB インスタンスで TiDB が TSO を受信するまでの P99 期間

### Storage Async Write Duration, Store Duration, and Apply Duration {#storage-async-write-duration-store-duration-and-apply-duration}

- Storage Async Write Duration: 非同期書き込みにかかる時間
- Store Duration: 非同期書き込み中にストアループで消費される時間
- Apply Duration: 非同期書き込み中の適用ループで消費された時間

これら3つのメトリックにはすべて、すべての TiKV インスタンスの平均期間と P99 期間が含まれます。

平均ストレージ非同期書き込み時間 = 平均保存時間 + 平均適用時間

### Append Log Duration, Commit Log Duration, and Apply Log Duration {#append-log-duration-commit-log-duration-and-apply-log-duration}

- Append Log Duration: Raftがログを追加するのにかかる時間
- Commit Log Duration: Raftがログをコミットするのにかかる時間
- Apply Log Duration: Raftがログを適用するのにかかる時間

これら3つのメトリックにはすべて、すべての TiKV インスタンスの平均期間と P99 期間が含まれます。

### Interface of the Performance Overview panels {#interface-of-the-performance-overview-panels}

![performance overview](/media/performance/grafana_performance_overview.png)

## TiFlash {#tiflash}

- CPU: TiFlashインスタンスごとの CPU 使用率。
- Memory: TiFlashインスタンスごとのメモリ使用量。
- IO utilization: TiFlashインスタンスごとの IO 使用率。
- MPP Query count: TiFlashインスタンスあたりの 1秒あたりのTiFlash MPP クエリ数。
- Request QPS: すべてのTiFlashインスタンスによって受信されたコプロセッサリクエストの数。

    - `batch` : バッチリクエストの数。
    - `batch_cop` : バッチリクエスト内のコプロセッサリクエストの数。
    - `cop` : コプロセッサ インターフェイスを介して直接送信されるコプロセッサリクエストの数。
    - `cop_dag` : すべてのコプロセッサリクエスト内の DAG リクエストの数。
    - `super_batch` : スーパーバッチ機能を有効にするリクエストの数。
- Executor QPS: すべてのTiFlashインスタンスが受信したリクエスト内の各タイプの DAG Executor の数。`table_scan`はテーブルスキャン Executor です。`selection`は選択 Executor です。`aggregation`は集約 Executor です。`top_n`は`TopN` Executor です。`limit`は制限 Executor です。
- Request Duration Overview: すべてのTiFlashインスタンスのすべてのリクエストタイプについて、1秒あたりの合計処理時間の積み上げグラフを提供します。
- Request Duration: すべてのTiFlashインスタンスにおける各MPPおよびコプロセッサリクエストタイプの合計処理期間。コプロセッサリクエストの受信からリクエストへの応答が完了するまでの時間であり、平均レイテンシーとp99レイテンシーが含まれます。
- Request Handle Duration：すべてのTiFlashインスタンスにおける各MPPおよびコプロセッサリクエストタイプの実際の処理時間。コプロセッサリクエストの実行開始から完了までの時間であり、平均レイテンシーとp99レイテンシーが含まれます。
- Raft Wait Index Duration: すべてのTiFlashインスタンスに対して`wait_index`が使用する時間。つまり、 `read_index`リクエストを受信してから、リージョンインデックスが`read_index`になるまで待機する時間です。
- Raft Batch Read Index Duration: すべてのTiFlashインスタンスの`read_index`が使用する時間。ほとんどの時間は、リージョンリーダーとのやり取りと再試行に使用されます。
- Write Throughput By Instance：インスタンスごとの書き込みスループット。Raft書き込みコマンドとRaftスナップショットを適用した場合のスループットも含まれます。
- Write flow: すべてのTiFlashインスタンスによるディスク書き込みのトラフィック。
- Read flow: すべてのTiFlashインスタンスによるディスク読み取りのトラフィック。

## CDC {#cdc}

- CPU usage: TiCDC ノードごとの CPU 使用率。
- Memory usage: TiCDC ノードごとのメモリ使用量。
- Goroutine count: TiCDC ノードあたりのゴルーチンの数。
- Changefeed checkpoint lag: アップストリームとダウンストリーム間のデータ複製の進行ラグ (単位は秒)。
- Changefeed resolved ts lag: アップストリーム ノードと TiCDC ノード間のデータ複製の進行ラグ (単位は秒)。
- The status of changefeeds:

    - 0: 正常
    - 1: エラー
    - 2: 失敗
    - 3: 停止
    - 4: 完了
    - -1: 不明
- Puller output events/s: TiCDC ノードの Puller モジュールが Sorter モジュールに 1秒あたりに送信する行数。
- Sorter output events/s: TiCDC ノードのソーターモジュールがマウンター モジュールに 1秒あたりに送信する行数。
- Mounter output events/s: TiCDC ノードのマウンター モジュールがシンク モジュールに 1秒あたりに送信する行数。
- Table sink output events/s: TiCDC ノードのテーブル ソーターモジュールがシンク モジュールに 1秒あたりに送信する行数。
- SinkV2 - Sink flush rows/s: TiCDC ノードのシンク モジュールがダウンストリームに 1秒あたりに送信する行数。
- Transaction Sink Full Flush Duration: TiCDC ノードの MySQL シンクによるダウンストリーム トランザクションの書き込みの平均レイテンシーと p999レイテンシー。
- MQ Worker Send Message Duration Percentile: ダウンストリームが Kafka の場合の MQ ワーカーによるメッセージ送信のレイテンシー。
- Kafka Outgoing Bytes: MQ ワークロードでのダウンストリーム トランザクションの書き込みトラフィック。
