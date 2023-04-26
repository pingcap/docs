---
title: Key Metrics on Performance Overview
summary: Learn key metrics displayed on the Performance Overview dashboard.
---

# パフォーマンスの概要に関する主要指標 {#key-metrics-on-performance-overview}

TiUPを使用して TiDB クラスターをデプロイすると、監視システム (Prometheus &amp; Grafana) が同時にデプロイされます。詳細については、 [TiDB 監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

Grafana ダッシュボードは、PD、TiDB、TiKV、Node_exporter、Overview、および Performance Overview を含む一連のサブ ダッシュボードに分かれています。診断に役立つ多くの指標があります。

Performance Overview ダッシュボードは、TiDB、PD、および TiKV のメトリックを調整し、それぞれを次のセクションに示します。

-   概要: データベース時間と SQL 実行時間の概要。概要のさまざまな色を確認することで、データベースのワークロード プロファイルとパフォーマンスのボトルネックをすばやく特定できます。

-   負荷プロファイル: データベースの QPS、接続情報、アプリケーションが TiDB とやり取りする MySQL コマンドの種類、データベースの内部 TSO と KV 要求の OPS、TiKV と TiDB のリソースの使用状況など、主要なメトリックとリソースの使用状況。

-   トップダウンレイテンシーの内訳: クエリレイテンシーと接続アイドル時間の比率、クエリレイテンシーの内訳、実行中の TSO/KV 要求レイテンシー、TiKV 内の書き込みレイテンシーの内訳。

パフォーマンス概要ダッシュボードを使用すると、パフォーマンスを効率的に分析し、ユーザー応答時間のボトルネックがデータベースにあるかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要、ワークロード プロファイル、SQLレイテンシーの内訳を使用して、データベース内のボトルネックを特定できます。詳細については、 [パフォーマンス分析とチューニング](/performance-tuning-methods.md)を参照してください。

次のセクションでは、パフォーマンス概要ダッシュボードのメトリックを示します。

## パフォーマンスの概要 {#performance-overview}

### SQL タイプ別のデータベース時間 {#database-time-by-sql-type}

-   データベース時間: 1 秒あたりの合計データベース時間
-   sql_type: 1 秒あたりの各タイプの SQL ステートメントによって消費されたデータベース時間

### SQL フェーズごとのデータベース時間 {#database-time-by-sql-phase}

-   データベース時間: 1 秒あたりの合計データベース時間
-   get token/parse/compile/execute: 4 つの SQL 処理フェーズで消費されるデータベース時間

一般的に、SQL 実行フェーズは緑で、その他のフェーズは赤で表示されます。緑以外の領域が大きい場合は、実行フェーズ以外のフェーズで多くのデータベース時間が費やされていることを意味し、さらなる原因分析が必要です。

### SQL 実行時間の概要 {#sql-execute-time-overview}

-   実行時間: 1 秒あたりの SQL 実行中に消費されたデータベース時間
-   tso_wait: SQL 実行中の 1 秒あたりの同時 TSO 待機時間
-   kv リクエスト タイプ: SQL 実行中の 1 秒あたりの各 KV リクエスト タイプの待機時間。 KV 要求は並行して実行されるため、KV 要求の合計待機時間は SQL 実行時間を超える可能性があります。
-   tiflash_mpp: SQL 実行中の 1 秒あたりのTiFlash要求の処理時間。

緑色のメトリックは一般的な KV 書き込み要求 (プリライトやコミットなど) を表し、青色のメトリックは一般的な読み取り要求を表し、紫色のメトリックはTiFlash MPP 要求を表し、他の色のメトリックは注意を払う必要がある予期しない状況を表します。たとえば、悲観的ロック KV 要求は赤でマークされ、TSO 待機は濃い茶色でマークされます。

青以外または緑以外の領域が大きい場合は、SQL 実行中にボトルネックがあることを意味します。例えば：

-   重大なロック競合が発生した場合、赤い領域が大きな割合を占めます。
-   TSO の待機に過度の時間が費やされると、こげ茶色の領域が大きな割合を占めます。

### QPS {#qps}

タイプ別に収集された、すべての TiDB インスタンスで 1 秒あたりに実行された SQL ステートメントの数: `SELECT` 、 `INSERT` 、および`UPDATE`など

### タイプ別CPS {#cps-by-type}

タイプに基づいて、すべての TiDB インスタンスによって 1 秒あたりに処理されるコマンドの数

### Plan Cache OPS を使用したクエリ {#queries-using-plan-cache-ops}

-   avg-hit: すべての TiDB インスタンスの 1 秒あたりの実行プラン キャッシュを使用したクエリの数
-   avg-miss: すべての TiDB インスタンスの 1 秒あたりの実行プラン キャッシュを使用していないクエリの数

`avg-hit + avg-miss`は`StmtExecute`に等しく、これは 1 秒あたりに実行されるすべてのクエリの数です。

### KV/TSO リクエスト OPS {#kv-tso-request-ops}

-   kv request total: すべての TiDB インスタンスでの 1 秒あたりの KV リクエストの総数
-   タイプ別の kv リクエスト: `Get` 、 `Prewrite` 、および`Commit`などのタイプに基づく、すべての TiDB インスタンスにおける 1 秒あたりの KV リクエストの数。
-   tso - cmd: すべての TiDB インスタンスでの 1 秒あたりの`tso cmd`リクエストの数
-   tso - request: すべての TiDB インスタンスにおける 1 秒あたりの`tso request`リクエストの数

一般に、 `tso - cmd`を`tso - request`で割ると、1 秒あたりのリクエストの平均バッチ サイズが得られます。

### ソース別 KV 要求時間 {#kv-request-time-by-source}

-   kv リクエストの合計時間: すべての TiDB インスタンスでの 1 秒あたりの KV およびTiFlashリクエストの処理時間の合計
-   各 KV リクエストと対応するリクエスト ソースは積み上げ棒グラフを形成し、 `external`通常のビジネス リクエストを識別し、 `internal`内部アクティビティ リクエスト (DDL やauto analyzeリクエストなど) を識別します。

### TiDB CPU {#tidb-cpu}

-   avg: すべての TiDB インスタンスの平均 CPU 使用率
-   デルタ: すべての TiDB インスタンスの最大 CPU 使用率からすべての TiDB インスタンスの最小 CPU 使用率を引いたもの
-   max: すべての TiDB インスタンスでの最大 CPU 使用率

### TiKV CPU/IO MBps {#tikv-cpu-io-mbps}

-   CPU-Avg: すべての TiKV インスタンスの平均 CPU 使用率
-   CPU デルタ: すべての TiKV インスタンスの最大 CPU 使用率から、すべての TiKV インスタンスの最小 CPU 使用率を引いたもの
-   CPU-MAX: すべての TiKV インスタンス間の最大 CPU 使用率
-   IO-Avg: すべての TiKV インスタンスの平均 MBps
-   IO-Delt: すべての TiKV インスタンスの最大 MBps から、すべての TiKV インスタンスの最小 MBps を引いたもの
-   IO-MAX: すべての TiKV インスタンスの最大 MBps

### 間隔 {#duration}

-   期間: 実行時間

    -   クライアントから TiDB へのリクエストを受信してから、TiDB がリクエストを実行してクライアントに結果を返すまでの時間。通常、クライアント要求は SQL ステートメントの形式で送信されます。ただし、この期間には、 `COM_PING` 、 `COM_SLEEP` 、 `COM_STMT_FETCH` 、および`COM_SEND_LONG_DATA`などのコマンドの実行時間が含まれる場合があります。
    -   TiDB はマルチクエリをサポートしています。つまり、クライアントは`select 1; select 1; select 1;`などの複数の SQL ステートメントを一度に送信できます。この場合、このクエリの合計実行時間には、すべての SQL ステートメントの実行時間が含まれます。

-   avg: すべてのリクエストを実行する平均時間

-   99: すべてのリクエストを実行するための P99 期間

-   avg by type: すべての TiDB インスタンスですべてのリクエストを実行する平均時間。タイプ別に収集: `SELECT` 、 `INSERT` 、および`UPDATE`

### 接続アイドル期間 {#connection-idle-duration}

Connection Idle Duration は、接続がアイドル状態である期間を示します。

-   avg-in-txn: 接続がトランザクション内にある場合の平均接続アイドル時間
-   avg-not-in-txn: 接続がトランザクション内にない場合の平均接続アイドル時間
-   99-in-txn: 接続がトランザクション内にある場合の P99 接続のアイドル時間

### 接続数 {#connection-count}

-   total: すべての TiDB インスタンスへの接続数
-   アクティブな接続: すべての TiDB インスタンスへのアクティブな接続の数
-   tidb-{node-number}-peer: 各 TiDB インスタンスへの接続数
-   disconnect/s: TiDB クラスター内の切断の数
-   99-not-in-txn: 接続がトランザクション内にない場合の P99 接続のアイドル時間

### 解析期間、コンパイル期間、および実行期間 {#parse-duration-compile-duration-and-execute-duration}

-   解析時間: SQL ステートメントの解析に費やされた時間
-   コンパイル時間: 解析された SQL AST を実行計画にコンパイルするのにかかった時間
-   実行時間: SQL ステートメントの実行計画の実行に費やされた時間

これら 3 つのメトリクスにはすべて、すべての TiDB インスタンスの平均期間と 99 パーセンタイル期間が含まれます。

### 平均 TiDB KV リクエスト期間 {#avg-tidb-kv-request-duration}

`Get` 、 `Prewrite` 、および`Commit`を含むタイプに基づく、すべての TiDB インスタンスでの KV リクエストの実行に費やされた平均時間。

### 平均 TiKV GRPC 期間 {#avg-tikv-grpc-duration}

`kv_get` 、 `kv_prewrite` 、および`kv_commit`を含むタイプに基づく、すべての TiKV インスタンスでの gRPC リクエストの実行に費やされた平均時間。

### PD TSO 待機/RPC 期間 {#pd-tso-wait-rpc-duration}

-   wait - avg: すべての TiDB インスタンスで PD が TSO を返すのを待機する平均時間
-   rpc - avg: TSO 要求を PD に送信してから、すべての TiDB インスタンスで TSO を受信するまでの平均時間
-   wait - 99: すべての TiDB インスタンスで PD が TSO を返すのを待機する P99 時間
-   rpc - 99: TSO 要求を PD に送信してから、すべての TiDB インスタンスで TSO を受信するまでの P99 時間

### ストレージの非同期書き込み期間、保存期間、および適用期間 {#storage-async-write-duration-store-duration-and-apply-duration}

-   Storage Async Write Duration: 非同期書き込みにかかった時間
-   Store Duration: 非同期書き込み中のストア ループで消費される時間
-   適用期間: 非同期書き込み中の適用ループで消費される時間

これら 3 つのメトリクスにはすべて、すべての TiKV インスタンスの平均期間と P99 期間が含まれます。

平均storage非同期書き込み時間 = 平均ストア時間 + 平均適用時間

### ログ期間の追加、ログ期間のコミット、およびログ期間の適用 {#append-log-duration-commit-log-duration-and-apply-log-duration}

-   Append Log Duration: Raftがログを追加するために費やした時間
-   Commit Log Duration: Raftがログをコミットするために費やした時間
-   Apply Log Duration: Raftがログを適用するために費やした時間

これら 3 つのメトリクスにはすべて、すべての TiKV インスタンスの平均期間と P99 期間が含まれます。

### パフォーマンス概要パネルのインターフェース {#interface-of-the-performance-overview-panels}

![performance overview](/media/performance/grafana_performance_overview.png)

## TiFlash {#tiflash}

-   CPU: TiFlashインスタンスごとの CPU 使用率。
-   メモリ: TiFlashインスタンスごとのメモリ使用量。
-   IO 使用率: TiFlashインスタンスごとの IO 使用率。
-   MPP クエリ数: TiFlashインスタンスごとの 1 秒あたりのTiFlash MPP クエリの数。
-   リクエスト QPS: すべてのTiFlashインスタンスによって受信されたコプロセッサ リクエストの数。

    -   `batch` : バッチ リクエストの数。
    -   `batch_cop` : バッチ リクエスト内のコプロセッサ リクエストの数。
    -   `cop` : コプロセッサー・インターフェースを介して直接送信されたコプロセッサー要求の数。
    -   `cop_dag` : すべてのコプロセッサー要求における DAG 要求の数。
    -   `super_batch` : スーパー バッチ機能を有効にする要求の数。
-   エグゼキュータ QPS: すべてのTiFlashインスタンスによって受信されたリクエスト内の各タイプの DAG エグゼキュータの数。 `table_scan`は、テーブル スキャン エグゼキュータです。 `selection`は選択エグゼキュータです。 `aggregation`は集計エグゼキュータです。 `top_n` `TopN`エグゼキュータです。 `limit`は制限実行者です。
-   リクエスト期間の概要: すべてのTiFlashインスタンスのすべてのリクエスト タイプの 1 秒あたりの合計処理時間の積み上げグラフを提供します。
-   Request Duration: すべてのTiFlashインスタンスにおける各 MPP およびコプロセッサー要求タイプの合計処理時間。これは、コプロセッサー要求が受信されてから、要求の応答が完了するまでの時間であり、これには平均レイテンシーと p99レイテンシーが含まれます。
-   Request Handle Duration: すべてのTiFlashインスタンスにおける各 MPP およびコプロセッサー要求タイプの実際の処理時間。これは、コプロセッサー要求の実行開始から実行完了までであり、これには平均レイテンシーと p99レイテンシーが含まれます。
-   Raft Wait Index Duration: `wait_index`がすべてのTiFlashインスタンスに対して使用した時間、つまり、 `read_index`リクエストを受信した後、 リージョン index &gt;= `read_index`になるまで待機するために使用した時間。
-   Raft Batch Read Index Duration: すべてのTiFlashインスタンスで`read_index`が使用した時間。ほとんどの時間は、リージョンリーダーとの対話と再試行に使用されます。
-   インスタンスごとの書き込みスループット: インスタンスごとの書き込みスループット。これには、 Raft書き込みコマンドとRaftスナップショットを適用することによるスループットが含まれます。
-   書き込みフロー: すべてのTiFlashインスタンスによるディスク書き込みのトラフィック。
-   読み取りフロー: すべてのTiFlashインスタンスによるディスク読み取りのトラフィック。

## CDC {#cdc}

-   CPU 使用率: TiCDC ノードごとの CPU 使用率。
-   メモリ使用量: TiCDC ノードごとのメモリ使用量。
-   ゴルーチン数: TiCDC ノードあたりのゴルーチン数。
-   Changefeed checkpoint lag: 上流と下流の間のデータ複製 (単位は秒) の進行ラグ。
-   Changefeed resolution ts lag: 上流ノードと TiCDC ノード間のデータ複製の進行ラグ (単位は秒)。
-   変更フィードのステータス:

    -   0: 通常
    -   1: エラー
    -   2: 失敗
    -   3: 停止
    -   4: 完了
    -   -1: 不明
-   Puller output events/s: TiCDC ノードの Puller モジュールが Sorter モジュールに送信する 1 秒あたりの行数。
-   Sorter output events/s: TiCDC ノードの Sorter モジュールが Mounter モジュールに送信する 1 秒あたりの行数。
-   Mounter output events/s: TiCDC ノードの Mounter モジュールが 1 秒あたりに Sink モジュールに送信する行数。
-   テーブル シンク出力イベント/秒: TiCDC ノードのテーブル ソーター モジュールが 1 秒あたりにシンク モジュールに送信する行数。
-   SinkV2 - シンク フラッシュ行/秒: TiCDC ノードのシンク モジュールがダウンストリームに送信する 1 秒あたりの行数。
-   トランザクション Sink Full Flush Duration: TiCDC ノードの MySQL Sink によるダウンストリーム トランザクションの書き込みの平均レイテンシーと p999レイテンシー。
-   MQ Worker Send Message Duration Percentile: ダウンストリームが Kafka の場合の MQ Worker によるメッセージ送信のレイテンシー。
-   Kafka Outgoing Bytes: MQ ワークロードでダウンストリーム トランザクションを書き込むトラフィック。
