---
title: TiDB Dashboard Monitoring Page
summary: TiDB Dashboardのモニタリングページでは、パフォーマンスを効率的に分析し、データベースのボトルネックを特定できます。主要なメトリクスには、データベース時間、SQL実行時間、QPS、接続数、TiDBおよびTiKVのCPU使用率、接続アイドル時間、解析・コンパイル・実行時間、TiDB KVリクエスト時間、TiKV gRPC時間、PD TSO待機/RPC時間、ストレージ非同期書き込み時間、保存時間、apply時間、ログ追加時間、ログコミット時間、ログapply時間などがあります。
---

# TiDB Dashboard監視ページ {#tidb-dashboard-monitoring-page}

モニタリングページでは、TiDB v6.1.0で導入されたパフォーマンス分析およびチューニングツールである「パフォーマンス概要」ダッシュボードを表示できます。「パフォーマンス概要」ダッシュボードを使用すると、パフォーマンスを効率的に分析し、ユーザー応答時間のボトルネックがデータベースにあるかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要、ワークロードプロファイル、SQLレイテンシーの内訳を表示することで、データベース内のボトルネックを特定できます。詳細は[パフォーマンス分析とチューニング](/performance-tuning-methods.md)ご覧ください。

## ページにアクセスする {#access-the-page}

TiDB Dashboardにログインし、左側のナビゲーションバーから**Monitoring**をクリックします。パフォーマンス概要ダッシュボードが表示されます。

![Monitoring page](/media/dashboard/dashboard-monitoring.png)

TiDBクラスターをTiUPを使用してデプロイした場合、Grafanaでパフォーマンス概要ダッシュボードを表示することもできます。このデプロイメントモードでは、監視システム（PrometheusとGrafana）も同時にデプロイされます。詳細については、 [TiDB 監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

![performance overview](/media/performance/grafana_performance_overview.png)

## パフォーマンス概要の主要指標 {#key-metrics-on-performance-overview}

パフォーマンス概要ダッシュボードは、TiDB、PD、および TiKV のメトリックを調整し、それぞれを次のセクションで表示します。

- **Overview**：データベース時間とSQL実行時間の概要。概要で異なる色を確認することで、データベースのワークロードプロファイルとパフォーマンスのボトルネックを素早く特定できます。

- **負荷プロファイル**: データベース QPS、接続情報、アプリケーションが TiDB と対話する MySQL コマンド タイプ、データベース内部 TSO および KV リクエスト OPS、TiKV および TiDB のリソース使用量など、主要なメトリックとリソース使用量。

- **トップダウンのレイテンシーの内訳**: クエリレイテンシーと接続アイドル時間の比率、クエリレイテンシーの内訳、実行中の TSO/KV リクエストレイテンシー、TiKV 内の書き込みレイテンシーの内訳。

次のセクションでは、パフォーマンス概要ダッシュボードのメトリックについて説明します。

### Database Time by SQL Type {#database-time-by-sql-type}

- `database time` : 1秒あたりの合計データベース時間
- `sql_type` : 各タイプのSQL文が1秒あたりに消費するデータベース時間

### Database Time by SQL Phase {#database-time-by-sql-phase}

- `database time` : 1秒あたりの合計データベース時間
- `get token/parse/compile/execute` : 4つのSQL処理フェーズで消費されたデータベース時間

SQL実行フェーズは緑色で、その他のフェーズは全体的に赤色で表示されます。緑色以外の領域が大きい場合は、実行フェーズ以外のフェーズでデータベース時間が大量に消費されていることを意味し、さらなる原因分析が必要です。

### SQL Execute Time Overview {#sql-execute-time-overview}

- `execute time` : SQL実行中に1秒あたりに消費されたデータベース時間
- `tso_wait` : SQL実行中の1秒あたりの同時TSO待機時間
- `kv request type` ：SQL実行中に各KVリクエストタイプを1秒あたりに待機する時間。KVリクエストは同時実行されるため、合計KVリクエスト待機時間はSQL実行時間を超える場合があります。

緑色のメトリクスは一般的なKV書き込みリクエスト（プリライトやコミットなど）を表し、青色のメトリクスは一般的な読み取りリクエストを表します。その他の色のメトリクスは、注意が必要な予期しない状況を表します。例えば、悲観的ロックKVリクエストは赤色で、TSO待機は濃い茶色で表示されます。

青または緑以外の領域が大きい場合は、SQL実行中にボトルネックが発生していることを意味します。例：

- 重大なロック競合が発生した場合、赤色の領域が大きな割合を占めることになります。
- TSO の待ち時間に過度に時間がかかってしまうと、濃い茶色の領域が大きな割合を占めることになります。

### QPS {#qps}

すべての TiDB インスタンスで 1秒あたりに実行された SQL 文の数（タイプ別に収集: `SELECT`、`INSERT`、`UPDATE`など）

### CPS By Type {#cps-by-type}

タイプに基づいて、すべての TiDB インスタンスによって 1秒あたりに処理されるコマンドの数

### Queries Using Plan Cache OPS {#queries-using-plan-cache-ops}

すべての TiDB インスタンスにおける 1秒あたりのプランキャッシュを使用するクエリの数

### KV/TSO Request OPS {#kv-tso-request-ops}

- kv request total: すべてのTiDBインスタンスにおける1秒あたりのKVリクエストの合計数
- kv request by type: `Get`、`Prewrite`、`Commit`などのタイプに基づいて、すべての TiDB インスタンスでの 1秒あたりの KV リクエスト数
- tso - cmd: TiDB がすべての TiDB インスタンスの PD に送信する 1秒あたりの gRPC リクエストの数。各 gRPC リクエストには、TSO リクエストのバッチが含まれます。
- tso - request: すべての TiDB インスタンスにおける 1秒あたりの TSO リクエスト数

通常、 `tso - request` `tso - cmd`で割った値が、1秒あたりの TSO リクエストバッチの平均サイズになります。

### Connection Count {#connection-count}

- `total` : すべてのTiDBインスタンスへの接続数
- `active connections` : すべてのTiDBインスタンスへのアクティブな接続の数
- 各TiDBインスタンスへの接続数

### TiDB CPU/Memory {#tidb-cpu-memory}

- `CPU-Avg` : すべての TiDB インスタンスの平均 CPU 使用率
- `CPU-Delta` : すべての TiDB インスタンスの最大 CPU 使用率からすべての TiDB インスタンスの最小 CPU 使用率を引いた値
- `CPU-Max` : すべての TiDB インスタンスの最大 CPU 使用率
- `CPU-Quota` : TiDBが使用できるCPUコアの数
- `Mem-Max` : すべての TiDB インスタンスの最大メモリ使用率

### TiKV CPU/Memory {#tikv-cpu-memory}

- `CPU-Avg` : すべての TiKV インスタンスの平均 CPU 使用率
- `CPU-Delta` : すべての TiKV インスタンスの最大 CPU 使用率からすべての TiKV インスタンスの最小 CPU 使用率を引いた値
- `CPU-Max` : すべての TiKV インスタンスの最大 CPU 使用率
- `CPU-Quota` : TiKVが使用できるCPUコアの数
- `Mem-Max` : すべての TiKV インスタンスの最大メモリ使用率

### PD CPU/Memory {#pd-cpu-memory}

- `CPU-Max` : すべてのPDインスタンスの最大CPU使用率
- `CPU-Quota` : PDが使用できるCPUコアの数
- `Mem-Max` : すべてのPDインスタンスの最大メモリ使用率

### Read Traffic {#read-traffic}

- `TiDB -> Client` : TiDBからクライアントへの送信トラフィック統計
- `Rocksdb -> TiKV` :ストレージレイヤー内での読み取り操作中に TiKV が RocksDB から取得するデータフロー

### Write Traffic {#write-traffic}

- `Client -> TiDB` : クライアントから TiDB への受信トラフィック統計
- `TiDB -> TiKV: general` : フォアグラウンドトランザクションが TiDB から TiKV に書き込まれる速度
- `TiDB -> TiKV: internal` : 内部トランザクションが TiDB から TiKV に書き込まれる速度
- `TiKV -> Rocksdb` : TiKVからRocksDBへの書き込み操作の流れ
- `RocksDB Compaction` : RocksDBの圧縮操作によって生成された合計読み取りおよび書き込みI/Oフロー

### Duration {#duration}

- `Duration` : 実行時間

    - クライアントからのリクエストをTiDBが受信してから、TiDBがそのリクエストを実行し、結果をクライアントに返すまでの時間。通常、クライアントからのリクエストはSQL文の形式で送信されますが、この時間には`COM_PING` 、 `COM_SLEEP` 、 `COM_STMT_FETCH` 、 `COM_SEND_LONG_DATA`などのコマンドの実行時間も含まれる場合があります。
    - TiDBはマルチクエリをサポートしています。つまり、クライアントは一度に複数のSQL文（例： `select 1; select 1; select 1;`を送信できます。この場合、このクエリの合計実行時間には、すべてのSQL文の実行時間が含まれます。

- `avg` : すべてのリクエストを実行する平均時間

- `99` : すべてのリクエストを実行するためのP99期間

- `avg by type` : すべての TiDB インスタンス内のすべてのリクエストを実行するのにかかった平均時間（タイプ別に収集: `SELECT`、`INSERT`、`UPDATE`）

### Connection Idle Duration {#connection-idle-duration}

接続アイドル期間は、接続がアイドル状態にある期間を示します。

- `avg-in-txn` : 接続がトランザクション内にあるときの平均接続アイドル期間
- `avg-not-in-txn` : 接続がトランザクション内にない場合の平均接続アイドル期間
- `99-in-txn` : 接続がトランザクション内にある場合の P99 接続アイドル期間
- `99-not-in-txn` : 接続がトランザクション内にない場合の P99 接続アイドル期間

### Parse Duration, Compile Duration, and Execute Duration {#parse-duration-compile-duration-and-execute-duration}

- `Parse Duration` : SQL文の解析に要した時間
- `Compile Duration` : 解析されたSQL ASTを実行計画にコンパイルするのにかかる時間
- `Execution Duration` : SQL文の実行計画の実行に費やされた時間

これら3つのメトリックにはすべて、すべての TiDB インスタンスの平均期間と 99 パーセンタイル期間が含まれます。

### Avg TiDB KV Request Duration {#avg-tidb-kv-request-duration}

`Get` 、 `Prewrite` 、 `Commit`を含むタイプに基づいて、すべての TiDB インスタンスでの KV リクエストの実行に費やされた平均時間。

### Avg TiKV GRPC Duration {#avg-tikv-grpc-duration}

`kv_get` 、 `kv_prewrite` 、 `kv_commit`を含むタイプに基づいて、すべての TiKV インスタンスでの gRPC リクエストの実行に費やされた平均時間。

### PD TSO Wait/RPC Duration {#pd-tso-wait-rpc-duration}

- `wait - avg` : すべての TiDB インスタンスで PD が TSO を返すのを待つ平均時間
- `rpc - avg` : PDにTSOリクエストを送信してからすべてのTiDBインスタンスでTSOを受信するまでの平均時間
- `wait - 99` : すべての TiDB インスタンスで PD が TSO を返すのを待つ P99時間
- `rpc - 99` : PDにTSOリクエストを送信してからすべてのTiDBインスタンスでTSOを受信するまでのP99時間

### Storage Async Write Duration, Store Duration, and Apply Duration {#storage-async-write-duration-store-duration-and-apply-duration}

- `Storage Async Write Duration` : 非同期書き込みにかかった時間
- `Store Duration` : 非同期書き込み中のストアループで消費された時間
- `Apply Duration` : 非同期書き込み中のapplyループで消費された時間

これら3つのメトリックにはすべて、すべての TiKV インスタンスの平均期間と P99 期間が含まれます。

平均ストレージ非同期書き込み時間 = 平均保存時間 + 平均apply時間

### Append Log Duration, Commit Log Duration, and Apply Log Duration {#append-log-duration-commit-log-duration-and-apply-log-duration}

- `Append Log Duration` : Raftがログを追加するのにかかった時間
- `Commit Log Duration` : Raftがログをコミットするのにかかる時間
- `Apply Log Duration` : Raftがログをapplyするのに要した時間

これら3つのメトリックにはすべて、すべての TiKV インスタンスの平均期間と P99 期間が含まれます。
