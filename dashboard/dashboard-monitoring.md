---
title: TiDB Dashboard Monitoring Page
summary: Learn how to view the Performance Overview dashboard on TiDB Dashboard and understand key metrics displayed on the Performance Overview dashboard.
---

# TiDB ダッシュボード監視ページ {#tidb-dashboard-monitoring-page}

モニタリング ページでは、TiDB v6.1.0 で導入されたパフォーマンス分析およびチューニング ツールであるパフォーマンス概要ダッシュボードを表示できます。パフォーマンス概要ダッシュボードを使用すると、パフォーマンスを効率的に分析し、ユーザー応答時間のボトルネックがデータベースにあるかどうかを確認できます。ボトルネックがデータベース内にある場合は、データベース時間の概要、ワークロード プロファイル、SQLレイテンシー時間の内訳を使用して、データベース内のボトルネックを特定できます。詳細は[パフォーマンスの分析とチューニング](/performance-tuning-methods.md)を参照してください。

## ページにアクセスする {#access-the-page}

TiDB ダッシュボードにログインし、左側のナビゲーション バーから**[モニタリング]**をクリックします。パフォーマンス概要ダッシュボードが表示されます。

![Monitoring page](/media/dashboard/dashboard-monitoring.png)

TiDB クラスターがTiUPを使用してデプロイされている場合は、Grafana でパフォーマンス概要ダッシュボードを表示することもできます。この展開モードでは、監視システム (Prometheus および Grafana) が同時に展開されます。詳細については、 [TiDB モニタリング フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

![performance overview](/media/performance/grafana_performance_overview.png)

## パフォーマンスの概要に関する主要な指標 {#key-metrics-on-performance-overview}

パフォーマンス概要ダッシュボードは、TiDB、PD、および TiKV のメトリクスを調整し、次のセクションにそれぞれのメトリクスを表示します。

-   概要: データベース時間と SQL 実行時間の概要。概要でさまざまな色をチェックすることで、データベースのワークロード プロファイルとパフォーマンスのボトルネックをすぐに特定できます。

-   負荷プロファイル: 主要なメトリックとリソース使用量 (データベース QPS、接続情報、アプリケーションが TiDB と対話する MySQL コマンド タイプ、データベース内部 TSO および KV リクエスト OPS、TiKV および TiDB のリソース使用量など)。

-   トップダウンのレイテンシーの内訳: クエリレイテンシーと接続アイドル時間の比率、クエリレイテンシーの内訳、実行中の TSO/KV リクエストレイテンシー、TiKV 内の書き込みレイテンシーの内訳。

次のセクションでは、パフォーマンス概要ダッシュボードのメトリクスを説明します。

### SQL タイプごとのデータベース時間 {#database-time-by-sql-type}

-   データベース時間: 1 秒あたりの合計データベース時間
-   sql_type: 各タイプの SQL ステートメントによって消費される 1 秒あたりのデータベース時間

### SQLフェーズごとのデータベース時間 {#database-time-by-sql-phase}

-   データベース時間: 1 秒あたりの合計データベース時間
-   トークンの取得/解析/コンパイル/実行: 4 つの SQL 処理フェーズで消費されるデータベース時間

通常、SQL 実行フェーズは緑色で、その他のフェーズは赤色で表示されます。緑色以外の領域が大きい場合は、実行フェーズ以外のフェーズで多くのデータベース時間が消費されていることを意味し、さらなる原因分析が必要になります。

### SQL実行時間の概要 {#sql-execute-time-overview}

-   実行時間: SQL 実行中に消費されたデータベース時間/秒
-   tso_wait: SQL 実行中の 1 秒あたりの同時 TSO 待機時間
-   kv リクエスト タイプ: SQL 実行中の 1 秒あたりの各 KV リクエスト タイプの待機時間。 KV リクエストは同時実行されるため、KV リクエストの合計待機時間は SQL 実行時間を超える可能性があります。

緑色のメトリクスは一般的な KV 書き込みリクエスト (事前書き込みやコミットなど) を表し、青のメトリクスは一般的な読み取りリクエストを表し、他の色のメトリクスは注意が必要な予期せぬ状況を表します。たとえば、悲観的ロック KV 要求は赤でマークされ、TSO 待機は濃い茶色でマークされます。

青以外または緑以外の領域が大きい場合は、SQL 実行中にボトルネックがあることを意味します。例えば：

-   深刻なロック競合が発生した場合、赤い領域が大きな割合を占めます。
-   TSO の待機に時間がかかりすぎると、濃い茶色の領域の割合が大きくなります。

### QPS {#qps}

すべての TiDB インスタンスで 1 秒あたりに実行された SQL ステートメントの数。タイプごとに収集されます: `SELECT` 、 `INSERT` 、 `UPDATE`など

### タイプ別 CPS {#cps-by-type}

タイプに基づく 1 秒あたりにすべての TiDB インスタンスによって処理されるコマンドの数

### プラン キャッシュ OPS を使用したクエリ {#queries-using-plan-cache-ops}

すべての TiDB インスタンスでの 1 秒あたりのプラン キャッシュを使用するクエリの数

### KV/TSO リクエスト OPS {#kv-tso-request-ops}

-   kv request total: すべての TiDB インスタンスにおける 1 秒あたりの KV リクエストの合計数
-   タイプ別の kv リクエスト: `Get` 、 `Prewrite` 、 `Commit`などのタイプに基づく、すべての TiDB インスタンスにおける 1 秒あたりの KV リクエストの数。
-   tso - cmd: すべての TiDB インスタンスにおける 1 秒あたりの`tso cmd`リクエストの数
-   tso - リクエスト: すべての TiDB インスタンスにおける 1 秒あたりの`tso request`リクエストの数

一般に、 `tso - cmd`を`tso - request`で割ると、1 秒あたりのリクエストの平均バッチ サイズが求められます。

### 接続数 {#connection-count}

-   total: すべての TiDB インスタンスへの接続数
-   アクティブな接続: すべての TiDB インスタンスへのアクティブな接続の数
-   各 TiDB インスタンスへの接続数

### TiDB CPU {#tidb-cpu}

-   avg: すべての TiDB インスタンスにわたる平均 CPU 使用率
-   デルタ: すべての TiDB インスタンスの最大 CPU 使用率からすべての TiDB インスタンスの最小 CPU 使用率を引いた値
-   max: すべての TiDB インスタンスにわたる最大 CPU 使用率

### TiKV CPU/IO MBps {#tikv-cpu-io-mbps}

-   CPU-Avg: すべての TiKV インスタンスの平均 CPU 使用率
-   CPU-Delta: すべての TiKV インスタンスの最大 CPU 使用率からすべての TiKV インスタンスの最小 CPU 使用率を引いた値
-   CPU-MAX: すべての TiKV インスタンス間の最大 CPU 使用率
-   IO-Avg: すべての TiKV インスタンスの平均 MBps
-   IO-Delt: すべての TiKV インスタンスの最大 MBps からすべての TiKV インスタンスの最小 MBps を引いた値
-   IO-MAX: すべての TiKV インスタンスの最大 MBps

### 間隔 {#duration}

-   期間: 実行時間

    -   クライアントから TiDB へのリクエストを受信して​​から、TiDB がリクエストを実行して結果をクライアントに返すまでの期間。一般に、クライアント要求は SQL ステートメントの形式で送信されます。ただし、この期間には`COM_PING` 、 `COM_SLEEP` 、 `COM_STMT_FETCH` 、 `COM_SEND_LONG_DATA`などのコマンドの実行時間が含まれる場合があります。
    -   TiDB はマルチクエリをサポートしています。これは、クライアントが一度に複数の SQL ステートメント ( `select 1; select 1; select 1;`など) を送信できることを意味します。この場合、このクエリの合計実行時間には、すべての SQL ステートメントの実行時間が含まれます。

-   avg: すべてのリクエストを実行する平均時間

-   99: すべてのリクエストを実行するための P99 時間

-   タイプ別の平均: タイプごとに収集された、すべての TiDB インスタンスのすべてのリクエストの実行にかかった平均時間: `SELECT` 、 `INSERT` 、および`UPDATE`

### 接続アイドル期間 {#connection-idle-duration}

接続アイドル期間は、接続がアイドル状態である期間を示します。

-   avg-in-txn: 接続がトランザクション内にある場合の平均接続アイドル時間
-   avg-not-in-txn: 接続がトランザクション内にない場合の平均接続アイドル時間
-   99-in-txn: 接続がトランザクション内にある場合の P99 接続アイドル期間
-   99-not-in-txn: 接続がトランザクション内にない場合の P99 接続アイドル期間

### 解析期間、コンパイル期間、および実行期間 {#parse-duration-compile-duration-and-execute-duration}

-   解析時間: SQL ステートメントの解析に費やされた時間
-   コンパイル時間: 解析された SQL AST を実行プランにコンパイルするのに費やされた時間
-   実行時間: SQL ステートメントの実行計画の実行に費やされる時間

これら 3 つのメトリクスにはすべて、すべての TiDB インスタンスの平均期間と 99 パーセンタイル期間が含まれます。

### 平均 TiDB KV リクエスト期間 {#avg-tidb-kv-request-duration}

タイプ`Get` 、 `Prewrite` 、および`Commit`を含む) に基づくすべての TiDB インスタンスでの KV リクエストの実行に費やされた平均時間。

### 平均 TiKV GRPC 継続時間 {#avg-tikv-grpc-duration}

タイプ`kv_get` 、 `kv_prewrite` 、 `kv_commit`など) に基づくすべての TiKV インスタンスでの gRPC リクエストの実行に費やされた平均時間。

### PD TSO 待機/RPC 期間 {#pd-tso-wait-rpc-duration}

-   wait - avg: すべての TiDB インスタンスで PD が TSO を返すまでの平均待ち時間
-   rpc - avg: すべての TiDB インスタンスで TSO リクエストを PD に送信してから TSO を受信するまでの平均時間
-   wait - 99: すべての TiDB インスタンスで PD が TSO を返すまでの P99 時間
-   rpc - 99: TSO リクエストを PD に送信してから、すべての TiDB インスタンスで TSO を受信するまでの P99 時間

### ストレージ非同期書き込み期間、保存期間、および適用期間 {#storage-async-write-duration-store-duration-and-apply-duration}

-   ストレージの非同期書き込み時間: 非同期書き込みにかかる時間
-   ストア期間: 非同期書き込み中のストア ループで消費された時間
-   適用期間: 非同期書き込み中の適用ループで消費された時間

これら 3 つのメトリクスには、すべての TiKV インスタンスの平均継続時間と P99 継続時間が含まれます。

平均storage非同期書き込み期間 = 平均ストア期間 + 平均適用期間

### ログ期間の追加、ログ期間のコミット、およびログ期間の適用 {#append-log-duration-commit-log-duration-and-apply-log-duration}

-   ログの追加期間: Raftがログを追加するために費やした時間
-   コミットログ期間: Raftがログをコミットするのに費やした時間
-   ログの適用期間: Raftがログを適用するために費やした時間

これら 3 つのメトリクスには、すべての TiKV インスタンスの平均継続時間と P99 継続時間が含まれます。
