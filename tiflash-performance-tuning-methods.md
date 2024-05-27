---
title: TiFlash Performance Analysis and Tuning Methods
summary: パフォーマンス概要ダッシュボードにTiFlashメトリックを導入し、 TiFlashワークロードをより適切に理解して監視できるようにします。
---

# TiFlash のパフォーマンス分析とチューニング方法 {#tiflash-performance-analysis-and-tuning-methods}

このドキュメントでは、 TiFlashリソースの使用率と主要なパフォーマンス メトリックを紹介します。パフォーマンス概要ダッシュボードの[TiFlashパネル](/grafana-performance-overview-dashboard.md#tiflash)を通じて、 TiFlashクラスターのパフォーマンスを監視および評価できます。

## TiFlashクラスタのリソース使用率 {#resource-utilization-of-a-tiflash-cluster}

次の 3 つのメトリックを使用すると、 TiFlashクラスターのリソース使用率をすぐに取得できます。

-   CPU: TiFlashインスタンスごとの CPU 使用率。
-   メモリ: TiFlashインスタンスごとのメモリ使用量。
-   IO 使用率: TiFlashインスタンスごとの IO 使用率。

例: [CH-benCHmark ワークロード](/benchmark/benchmark-tidb-using-ch.md)リソース使用率

このTiFlashクラスターは 2 つのノードで構成され、各ノードは 16 個のコアと 48 GB のメモリで構成されています。CH-benCHmark ワークロード中、CPU 使用率は最大 1500%、メモリ使用量は最大 20 GB、IO 使用率は最大 91% に達することがあります。これらのメトリックは、 TiFlashノードのリソースが飽和状態に近づいていることを示しています。

![CH-TiFlash-MPP](/media/performance/tiflash/tiflash-resource-usage.png)

## TiFlashパフォーマンスの主要指標 {#key-metrics-for-tiflash-performance}

### スループットメトリック {#throughput-metrics}

次のメトリックを使用すると、 TiFlashのスループットを取得できます。

-   MPP クエリ数: 各TiFlashインスタンスの MPP クエリ数の瞬間値。TiFlash インスタンスで処理する必要がある現在の MPP クエリ数(処理中のクエリとスケジュール待ちのクエリを含む) を反映します。
-   リクエスト QPS: すべてのTiFlashインスタンスによって受信されたコプロセッサ要求の数。
    -   `run_mpp_task` `dispatch_mpp_task` MPP `mpp_establish_conn`です。
    -   `batch` : バッチリクエストの数。
    -   `cop` : コプロセッサ インターフェイスを介して直接送信されるコプロセッサ要求の数。
    -   `cop_execution` : 現在実行中のコプロセッサ要求の数。
    -   `remote_read` `remote_read_constructed`リモート読み取り関連のメトリックです。リモート読み取りの増加は通常`remote_read_sent`システムに問題があることを示します。
-   Executor QPS: すべてのTiFlashインスタンスが受信したリクエスト内の各タイプの DAG 演算子の数。1 `table_scan`テーブル スキャン演算子、 `selection`は選択演算子、 `aggregation`は集約演算子、 `top_n`は TopN 演算子、 `limit`は制限演算子、 `join`は結合演算子、 `exchange_sender`はデータ送信演算子、 `exchange_receiver`はデータ受信演算子です。

### レイテンシ指標 {#latency-metrics}

次のメトリックを使用すると、 TiFlashのレイテンシーを取得できます。

-   リクエスト期間の概要: すべてのTiFlashインスタンスにおけるすべてのリクエスト タイプの 1 秒あたりの合計処理期間の積み上げグラフを提供します。

    -   リクエストのタイプが`run_mpp_task` 、 `dispatch_mpp_task` 、または`mpp_establish_conn`場合、SQL ステートメントの実行がTiFlashに部分的または完全にプッシュダウンされたことを示します。これには通常、結合およびデータ分散操作が含まれます。これは、 TiFlashで最も一般的なリクエスト タイプです。
    -   リクエストのタイプが`cop`の場合、このリクエストに関連するステートメントがTiFlashに完全にプッシュダウンされていないことを示します。通常、TiDB はデータ アクセスとフィルタリングのためにテーブル フル スキャン オペレーターをTiFlashにプッシュダウンします。積み上げチャートで`cop`最も一般的なリクエスト タイプになった場合は、それが妥当かどうかを確認する必要があります。

        -   SQL ステートメントによってクエリされるデータの量が大きい場合、オプティマイザーはコスト モデルに従ってTiFlashフル テーブル スキャンの方がコスト効率が高いと見積もる場合があります。
        -   クエリ対象のテーブルのスキーマに適切なインデックスがない場合、クエリ対象のデータ量が少ない場合でも、オプティマイザーはクエリをTiFlashにプッシュしてテーブル全体をスキャンすることしかできません。この場合、適切なインデックスを作成し、TiKV を介してデータにアクセスする方が効率的です。

-   要求期間: すべてのTiFlashインスタンスにおける各 MPP およびコプロセッサ要求タイプの合計処理期間。これには平均レイテンシーと p99レイテンシーが含まれます。

-   リクエスト処理期間: `cop`と`batch cop`のリクエストの実行開始から実行完了までの時間 (待機時間を除く)。このメトリックは、平均レイテンシと P99レイテンシーを含む`cop`と`batch cop`タイプのリクエストにのみ適用されます。

例1: TiFlash MPPリクエストの処理時間の概要

次の図のワークロードでは、 `run_mpp_task`と`mpp_establish_conn`リクエストが合計処理時間の大部分を占めており、リクエストのほとんどが実行のためにTiFlashに完全にプッシュダウンされる MPP タスクであることがわかります。

`cop`リクエストの処理時間は比較的短いため、リクエストの一部はデータ アクセスとコプロセッサを介したフィルタリングのためにTiFlashにプッシュダウンされていることがわかります。

![CH-TiFlash-MPP](/media/performance/tiflash/ch-2tiflash-op.png)

例2: TiFlash `cop`リクエストが総処理時間の大部分を占める

次の図のワークロードでは、 `cop`リクエストが全体の処理時間の大部分を占めています。この場合、SQL 実行プランをチェックして、これらの`cop`リクエストが生成された理由を確認できます。

![Cop](/media/performance/tiflash/tiflash_request_duration_by_type.png)

### ラフト関連のメトリクス {#raft-related-metrics}

次のメトリックを使用して、 TiFlashのRaftレプリケーション ステータスを取得できます。

-   Raft待機インデックス期間: すべてのTiFlashインスタンスのローカルリージョンインデックスが`read_index`になるまで待機する期間。これは、 `wait_index`の操作のレイテンシーを表します。このメトリックが高すぎる場合は、TiKV からTiFlashへのデータ レプリケーションにかなりのレイテンシーがあることを示しています。考えられる理由は次のとおりです。

    -   TiKV リソースが過負荷になっています。
    -   TiFlashリソース、特に IO リソースが過負荷になっています。
    -   TiKV とTiFlashの間にネットワークのボトルネックがあります。

-   Raftバッチ読み取りインデックス期間: すべてのTiFlashインスタンスのレイテンシーは`read_index`です。このメトリックが高すぎる場合は、 TiFlashと TiKV 間のやり取りが遅いことを示しています。考えられる理由は次のとおりです。

    -   TiFlashリソースが過負荷になっています。
    -   TiKV リソースが過負荷になっています。
    -   TiFlashと TiKV の間にネットワークのボトルネックがあります。

### IOスループットメトリクス {#io-throughput-metrics}

次のメトリックを使用すると、 TiFlashの IO スループットを取得できます。

-   インスタンスごとの書き込みスループット: 各TiFlashインスタンスによって書き込まれるデータのスループット。これには、 Raftデータ ログとRaftスナップショットを適用した場合のスループットが含まれます。

-   書き込みフロー: すべてのTiFlashインスタンスによるディスク書き込みのトラフィック。

    -   ファイル記述子: TiFlashで使用される DeltaTreestorageエンジンの安定したレイヤー。
    -   Page: TiFlashで使用される DeltaTreestorageエンジンの Delta 変更レイヤーである Pagestore を指します。

-   読み取りフロー: すべてのTiFlashインスタンスのディスク読み取り操作のトラフィック。

    -   ファイル記述子: TiFlashで使用される DeltaTreestorageエンジンの安定したレイヤー。
    -   Page: TiFlashで使用される DeltaTreestorageエンジンの Delta 変更レイヤーである Pagestore を指します。

`(Read flow + Write flow) ÷ total Write Throughput By Instance`式を使用して、 TiFlashクラスター全体の書き込み増幅係数を計算できます。

例1: セルフホスト環境におけるRaftとIOメトリクス[CH-benCHmark ワークロード](/benchmark/benchmark-tidb-using-ch.md)

次の図に示すように、このTiFlashクラスターの`Raft Wait Index Duration`パーセンタイルと 99 パーセンタイルの`Raft Batch Read Index Duration` 、それぞれ 3.24 秒と 753 ミリ秒と比較的高くなっています。これは、このクラスターのTiFlashワークロードが高く、データ レプリケーションでレイテンシーが発生するためです。

このクラスターには、2 つのTiFlashノードがあります。TiKV からTiFlashへの増分データ複製速度は、約 28 MB/秒です。安定レイヤー(ファイル記述子) の最大書き込みスループットは 939 MB/秒、最大読み取りスループットは 1.1 GiB/秒です。一方、デルタレイヤー(ページ) の最大書き込みスループットは 74 MB/秒、最大読み取りスループットは 111 MB/秒です。この環境では、 TiFlash は強力な IO スループット機能を備えた専用の NVME ディスクを使用します。

![CH-2TiFlash-OP](/media/performance/tiflash/ch-2tiflash-raft-io-flow.png)

例2: パブリッククラウド展開環境における[CH-benCHmark ワークロード](/benchmark/benchmark-tidb-using-ch.md)のRaftとIOメトリック

次の図に示すように、 `Raft Wait Index Duration`の 99 パーセンタイルは最大 438 ミリ秒、 `Raft Batch Read Index Duration`の 99 パーセンタイルは最大 125 ミリ秒です。このクラスターにはTiFlashノードが 1 つだけあります。TiKV は、1 秒あたり約 5 MB の増分データをTiFlashに複製します。安定レイヤー(ファイル記述子) の最大書き込みトラフィックは 78 MB/秒、最大読み取りトラフィックは 221 MB/秒です。一方、デルタレイヤー(ページ) の最大書き込みトラフィックは 8 MB/秒、最大読み取りトラフィックは 18 MB/秒です。この環境では、 TiFlash はIO スループットが比較的弱い AWS EBS クラウド ディスクを使用します。

![CH-TiFlash-MPP](/media/performance/tiflash/ch-1tiflash-raft-io-flow-cloud.png)
