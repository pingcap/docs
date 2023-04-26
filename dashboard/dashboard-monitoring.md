---
title: TiDB Dashboard Monitoring Page
summary: Learn how to view the Performance Overview dashboard on TiDB Dashboard and understand key metrics displayed on the Performance Overview dashboard.
---

# TiDB ダッシュボードの監視ページ {#tidb-dashboard-monitoring-page}

監視ページでは、TiDB v6.1.0 で導入されたパフォーマンス分析およびチューニング ツールである Performance Overview ダッシュボードを表示できます。パフォーマンス概要ダッシュボードを使用すると、パフォーマンスを効率的に分析し、ユーザー応答時間のボトルネックがデータベースにあるかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要、ワークロード プロファイル、SQLレイテンシーの内訳を使用して、データベース内のボトルネックを特定できます。詳細については、 [パフォーマンス分析とチューニング](/performance-tuning-methods.md)を参照してください。

## ページにアクセスする {#access-the-page}

TiDB ダッシュボードにログインし、左側のナビゲーション バーから**[監視]**をクリックします。パフォーマンス概要ダッシュボードが表示されます。

![Monitoring page](/media/dashboard/dashboard-monitoring.png)

TiDB クラスターがTiUPを使用してデプロイされている場合は、Grafana でパフォーマンス概要ダッシュボードを表示することもできます。この展開モードでは、監視システム (Prometheus &amp; Grafana) が同時に展開されます。詳細については、 [TiDB 監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

![performance overview](/media/performance/grafana_performance_overview.png)

## パフォーマンスの概要に関する主要指標 {#key-metrics-on-performance-overview}

Performance Overview ダッシュボードは、TiDB、PD、および TiKV のメトリックを調整し、それぞれを次のセクションに示します。

-   概要: データベース時間と SQL 実行時間の概要。概要のさまざまな色を確認することで、データベースのワークロード プロファイルとパフォーマンスのボトルネックをすばやく特定できます。

-   負荷プロファイル: データベースの QPS、接続情報、アプリケーションが TiDB とやり取りする MySQL コマンドの種類、データベースの内部 TSO と KV 要求の OPS、TiKV と TiDB のリソースの使用状況など、主要なメトリックとリソースの使用状況。

-   トップダウンレイテンシーの内訳: クエリレイテンシーと接続アイドル時間の比率、クエリレイテンシーの内訳、実行中の TSO/KV 要求レイテンシー、TiKV 内の書き込みレイテンシーの内訳。

次のセクションでは、パフォーマンス概要ダッシュボードのメトリックを示します。

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

緑色のメトリックは一般的な KV 書き込み要求 (事前書き込みやコミットなど) を表し、青色のメトリックは一般的な読み取り要求を表し、他の色のメトリックは注意を払う必要がある予期しない状況を表します。たとえば、悲観的ロック KV 要求は赤でマークされ、TSO 待機は濃い茶色でマークされます。

青以外または緑以外の領域が大きい場合は、SQL 実行中にボトルネックがあることを意味します。例えば：

-   重大なロック競合が発生した場合、赤い領域が大きな割合を占めます。
-   TSO の待機に過度の時間が費やされると、こげ茶色の領域が大きな割合を占めます。

### QPS {#qps}

タイプ別に収集された、すべての TiDB インスタンスで 1 秒あたりに実行された SQL ステートメントの数: `SELECT` 、 `INSERT` 、および`UPDATE`など

### タイプ別CPS {#cps-by-type}

タイプに基づいて、すべての TiDB インスタンスによって 1 秒あたりに処理されるコマンドの数

### Plan Cache OPS を使用したクエリ {#queries-using-plan-cache-ops}

すべての TiDB インスタンスでの 1 秒あたりのプラン キャッシュを使用したクエリの数

### KV/TSO リクエスト OPS {#kv-tso-request-ops}

-   kv request total: すべての TiDB インスタンスでの 1 秒あたりの KV リクエストの総数
-   タイプ別の kv リクエスト: `Get` 、 `Prewrite` 、および`Commit`などのタイプに基づく、すべての TiDB インスタンスにおける 1 秒あたりの KV リクエストの数。
-   tso - cmd: すべての TiDB インスタンスでの 1 秒あたりの`tso cmd`リクエストの数
-   tso - request: すべての TiDB インスタンスにおける 1 秒あたりの`tso request`リクエストの数

一般に、 `tso - cmd`を`tso - request`で割ると、1 秒あたりのリクエストの平均バッチ サイズが得られます。

### 接続数 {#connection-count}

-   total: すべての TiDB インスタンスへの接続数
-   アクティブな接続: すべての TiDB インスタンスへのアクティブな接続の数
-   各 TiDB インスタンスへの接続数

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
