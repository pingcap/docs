---
title: Key Metrics on Performance Overview
summary: Learn key metrics displayed on the Performance Overview dashboard.
---

# パフォーマンスの概要に関する主要な指標 {#key-metrics-on-performance-overview}

TiUPを使用してTiDBクラスタをデプロイする場合、監視システム（Prometheus＆Grafana）も同時にデプロイされます。詳細については、 [TiDBモニタリングフレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

Grafanaダッシュボードは、PD、TiDB、TiKV、Node_exporter、Overview、PerformanceOverviewなどを含む一連のサブダッシュボードに分割されています。診断に役立つ多くのメトリックがあります。

パフォーマンスの概要ダッシュボードは、TiDB、PD、およびTiKVのメトリックを調整し、次のセクションでそれぞれを示します。

-   概要：データベース時間とSQL実行時間の要約。概要のさまざまな色を確認することで、データベースのワークロードプロファイルとパフォーマンスのボトルネックをすばやく特定できます。

-   負荷プロファイル：データベースQPS、接続情報、アプリケーションがTiDBと対話するMySQLコマンドタイプ、データベース内部TSOおよびKV要求OPS、TiKVおよびTiDBのリソース使用量などの主要なメトリックとリソース使用量。

-   トップダウンレイテンシーの内訳：クエリレイテンシーと接続アイドル時間の比率、クエリレイテンシーの内訳、実行中のTSO / KVリクエストのレイテンシー、TiKV内の書き込みレイテンシーの内訳。

パフォーマンス概要ダッシュボードを使用すると、パフォーマンスを効率的に分析し、ユーザーの応答時間のボトルネックがデータベースにあるかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要、ワークロードプロファイル、およびSQLレイテンシの内訳を使用して、データベース内のボトルネックを特定できます。詳細については、 [パフォーマンス分析とチューニング](/performance-tuning-methods.md)を参照してください。

次のセクションでは、パフォーマンスの概要ダッシュボードの指標について説明します。

## SQLタイプ別のデータベース時間 {#database-time-by-sql-type}

-   データベース時間：1秒あたりの合計データベース時間
-   sql_type：1秒あたりのSQLステートメントの各タイプによって消費されるデータベース時間

## SQLフェーズごとのデータベース時間 {#database-time-by-sql-phase}

-   データベース時間：1秒あたりの合計データベース時間
-   get token / parse / compile / execute：4つのSQL処理フェーズで消費されるデータベース時間

一般的に、SQL実行フェーズは緑色で、その他のフェーズは赤色で表示されます。緑以外の領域が大きい場合は、実行フェーズ以外のフェーズで多くのデータベース時間が消費され、さらに原因分析が必要になることを意味します。

## SQL実行時間の概要 {#sql-execute-time-overview}

-   実行時間：1秒あたりのSQL実行中に消費されたデータベース時間
-   tso_wait：SQL実行中の1秒あたりの同時TSO待機時間
-   kv要求タイプ：SQL実行中の1秒あたりの各KV要求タイプの待機時間。 KV要求は同時であるため、KV要求の合計待機時間はSQL実行時間を超える可能性があります。

緑のメトリックは一般的なKV書き込み要求（プリライトやコミットなど）を表し、青のメトリックは一般的な読み取り要求を表し、他の色のメトリックは注意が必要な予期しない状況を表します。たとえば、ペシミスティックロックKV要求は赤でマークされ、TSO待機はダークブラウンでマークされます。

青以外または緑以外の領域が大きい場合は、SQLの実行中にボトルネックがあることを意味します。例えば：

-   深刻なロックの競合が発生した場合、赤い領域が大きな割合を占めます。
-   TSOの待機に過度の時間がかかると、暗褐色の領域が大きな割合を占めます。

## QPS {#qps}

タイプごとに収集された、すべての`INSERT`インスタンスで1秒あたりに実行されたSQLステートメントの数`UPDATE` `SELECT`など

## タイプ別のCPS {#cps-by-type}

タイプに基づいて、1秒あたりにすべてのTiDBインスタンスによって処理されたコマンドの数

## プランキャッシュOPSを使用したクエリ {#queries-using-plan-cache-ops}

すべてのTiDBインスタンスで1秒あたりのプランキャッシュを使用するクエリの数

## KV/TSOリクエストOPS {#kv-tso-request-ops}

-   kvリクエストの合計：すべてのTiDBインスタンスにおける1秒あたりのKVリクエストの総数
-   タイプ別のkvリクエスト： `Get`などのタイプに基づくすべての`Prewrite`インスタンスでの`Commit`秒あたりのKVリクエストの数。
-   tso-cmd：すべてのTiDBインスタンスで1秒あたり`tso cmd`リクエストの数
-   tso-リクエスト：すべてのTiDBインスタンスで1秒あたり`tso request`リクエストの数

一般に、 `tso - cmd`を`tso - request`で割ると、1秒あたりのリクエストの平均バッチサイズが得られます。

## 接続数 {#connection-count}

-   合計：すべてのTiDBインスタンスへの接続数
-   アクティブな接続：すべてのTiDBインスタンスへのアクティブな接続の数
-   各TiDBインスタンスへの接続数

## TiDB CPU {#tidb-cpu}

-   avg：すべてのTiDBインスタンスの平均CPU使用率
-   デルタ：すべてのTiDBインスタンスの最大CPU使用率からすべてのTiDBインスタンスの最小CPU使用率を引いたもの
-   max：すべてのTiDBインスタンスでの最大CPU使用率

## TiKV CPU / IO MBps {#tikv-cpu-io-mbps}

-   CPU-Avg：すべてのTiKVインスタンスの平均CPU使用率
-   CPU-Delta：すべてのTiKVインスタンスの最大CPU使用率からすべてのTiKVインスタンスの最小CPU使用率を引いたもの
-   CPU-MAX：すべてのTiKVインスタンス間の最大CPU使用率
-   IO-Avg：すべてのTiKVインスタンスの平均MBps
-   IO-Delt：すべてのTiKVインスタンスの最大MBpsからすべてのTiKVインスタンスの最小MBpsを引いたもの
-   IO-MAX：すべてのTiKVインスタンスの最大MBps

## 間隔 {#duration}

-   期間：実行時間

    -   クライアントからTiDBへのリクエストを受信してから、TiDBがリクエストを実行して結果をクライアントに返すまでの期間。一般に、クライアント要求はSQLステートメントの形式で送信されます。ただし、この期間には、 `COM_PING`などの`COM_STMT_FETCH`の実行時間を`COM_SEND_LONG_DATA`ことができ`COM_SLEEP` 。
    -   TiDBはマルチクエリをサポートしています。つまり、クライアントは`select 1; select 1; select 1;`などの複数のSQLステートメントを一度に送信できます。この場合、このクエリの合計実行時間には、すべてのSQLステートメントの実行時間が含まれます。

-   avg：すべてのリクエストを実行する平均時間

-   99：すべてのリクエストを実行するためのP99期間

-   タイプ別の平均：タイプ別に収集された、すべてのTiDBインスタンスですべてのリクエストを実行する平均時間`UPDATE` `SELECT` 、および`INSERT`

## 接続アイドル期間 {#connection-idle-duration}

接続アイドル期間は、接続がアイドル状態の期間を示します。

-   avg-in-txn：接続がトランザクション内にある場合の平均接続アイドル期間
-   avg-not-in-txn：接続がトランザクション内にない場合の平均接続アイドル期間
-   99-in-txn：接続がトランザクション内にある場合のP99接続のアイドル期間
-   99-not-in-txn：接続がトランザクション内にない場合のP99接続のアイドル期間

## 解析期間、コンパイル期間、および実行期間 {#parse-duration-compile-duration-and-execute-duration}

-   解析時間：SQLステートメントの解析に費やされた時間
-   コンパイル時間：解析されたSQLASTを実行プランにコンパイルするのにかかる時間
-   実行時間：SQLステートメントの実行プランの実行に費やされた時間

これら3つのメトリックにはすべて、すべてのTiDBインスタンスの平均期間と99パーセンタイル期間が含まれます。

## 平均TiDBKVリクエスト期間 {#avg-tidb-kv-request-duration}

`Get`を含むタイプに基づいて、すべての`Prewrite`インスタンスでKVリクエストを実行するのに`Commit`れた平均時間。

## 平均TiKVGRPC期間 {#avg-tikv-grpc-duration}

`kv_get`を含むタイプに基づいて、すべての`kv_prewrite`インスタンスで`kv_commit`リクエストを実行するのに費やされた平均時間。

## PDTSO待機/RPC期間 {#pd-tso-wait-rpc-duration}

-   wait-avg：すべてのTiDBインスタンスでPDがTSOを返すのを待機する平均時間
-   rpc --avg：すべてのTiDBインスタンスでTSO要求をPDに送信してからTSOを受信するまでの平均時間
-   待機-99：すべてのTiDBインスタンスでPDがTSOを返すのを待機するP99時間
-   rpc-99：すべてのTiDBインスタンスでTSO要求をPDに送信してからTSOを受信するまでのP99時間

## ストレージ非同期書き込み期間、ストア期間、および適用期間 {#storage-async-write-duration-store-duration-and-apply-duration}

-   ストレージ非同期書き込み期間：非同期書き込みに費やされた時間
-   ストア期間：非同期書き込み中にストアループで消費された時間
-   適用期間：非同期書き込み中に適用ループで消費された時間

これら3つのメトリックにはすべて、すべてのTiKVインスタンスの平均期間とP99期間が含まれます。

平均ストレージ非同期書き込み期間=平均ストア期間+平均適用期間

## ログ期間の追加、ログ期間のコミット、およびログ期間の適用 {#append-log-duration-commit-log-duration-and-apply-log-duration}

-   ログの追加期間： Raftがログを追加するために費やした時間
-   コミットログ期間： Raftがログをコミットするために費やした時間
-   ログの適用期間： Raftがログを適用するのに費やした時間

これら3つのメトリックにはすべて、すべてのTiKVインスタンスの平均期間とP99期間が含まれます。

## パフォーマンス概要ダッシュボードのインターフェース {#interface-of-the-performance-overview-dashboard}

![performance overview](/media/performance/grafana_performance_overview.png)
