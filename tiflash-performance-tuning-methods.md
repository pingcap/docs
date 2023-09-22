---
title: TiFlash Performance Analysis and Tuning Methods
summary: Introduces the TiFlash metrics on the Performance Overview dashboard to help you better understand and monitor TiFlash workloads.
---

# TiFlash のパフォーマンス分析およびチューニング方法 {#tiflash-performance-analysis-and-tuning-methods}

このドキュメントでは、 TiFlashリソースの使用率と主要なパフォーマンス メトリクスを紹介します。 TiFlashクラスターのパフォーマンスは、[パフォーマンス概要] ダッシュボードの[TiFlashパネル](/grafana-performance-overview-dashboard.md#tiflash)から監視および評価できます。

## TiFlashクラスターのリソース使用率 {#resource-utilization-of-a-tiflash-cluster}

次の 3 つのメトリックを使用すると、 TiFlashクラスターのリソース使用率をすぐに取得できます。

-   CPU: TiFlashインスタンスごとの CPU 使用率。
-   メモリ: TiFlashインスタンスごとのメモリ使用量。
-   IO 使用率: TiFlashインスタンスごとの IO 使用率。

例: [CH-benCHmark のワークロード](/benchmark/benchmark-tidb-using-ch.md)の間のリソース使用率

このTiFlashクラスターは 2 つのノードで構成され、各ノードは 16 コアと 48 GB のメモリで構成されています。 CH-benCHmark ワークロード中、CPU 使用率は最大 1500%、メモリ使用率は最大 20 GB、IO 使用率は最大 91% に達する可能性があります。これらのメトリクスは、 TiFlashノードのリソースが飽和に近づいていることを示しています。

![CH-TiFlash-MPP](/media/performance/tiflash/ch-2tiflash-op.png)

## TiFlashパフォーマンスの主要な指標 {#key-metrics-for-tiflash-performance}

### スループットメトリクス {#throughput-metrics}

次のメトリクスを使用して、 TiFlashのスループットを取得できます。

-   MPP クエリ数: 各TiFlashインスタンスの MPP クエリ数の瞬間値TiFlashインスタンスによって処理する必要がある MPP クエリの現在の数 (処理中のものとスケジュールを待っているものを含む) を反映します。
-   リクエスト QPS: すべてのTiFlashインスタンスによって受信されたコプロセッサ リクエストの数。
    -   `run_mpp_task` 、 `dispatch_mpp_task` 、および`mpp_establish_conn`は MPP リクエストです。
    -   `batch` : バッチリクエストの数。
    -   `cop` : コプロセッサ インターフェイスを介して直接送信されるコプロセッサ リクエストの数。
    -   `cop_execution` : 現在実行中のコプロセッサリクエストの数。
    -   `remote_read` 、 `remote_read_constructed` 、および`remote_read_sent` 、リモート読み取り関連のメトリックです。リモート読み取りの増加は、通常、システムに問題があることを示しています。
-   Executor QPS: すべてのTiFlashインスタンスによって受信されたリクエスト内の各タイプの DAG オペレーターの数`table_scan`はテーブル スキャン オペレーター、 `selection`は選択オペレーター、 `aggregation`は集計オペレーター、 `top_n`は TopN オペレーター、 `limit`は制限です演算子、 `join`は結合演算子、 `exchange_sender`はデータ送信演算子、 `exchange_receiver`はデータ受信演算子である。

### レイテンシのメトリクス {#latency-metrics}

次のメトリクスを使用して、 TiFlashのレイテンシーを取得できます。

-   リクエスト時間の概要: すべてのTiFlashインスタンスにおけるすべてのリクエスト タイプの 1 秒あたりの合計処理時間の積み上げグラフを提供します。

    -   リクエストのタイプが`run_mpp_task` 、 `dispatch_mpp_task` 、または`mpp_establish_conn`の場合、SQL ステートメントの実行が部分的または完全にTiFlashにプッシュダウンされたことを示します。これには通常、結合操作とデータ分散操作が含まれます。これは、 TiFlashで最も一般的なリクエスト タイプです。
    -   リクエストのタイプが`cop`の場合、このリクエストに関連するステートメントがTiFlashに完全にはプッシュダウンされていないことを示します。通常、TiDB は、データ アクセスとフィルタリングのためにテーブル フル スキャン オペレーターをTiFlashにプッシュダウンします。積み上げグラフで`cop`最も一般的なリクエスト タイプになった場合は、それが妥当かどうかを確認する必要があります。

        -   SQL ステートメントによってクエリされるデータの量が多い場合、オプティマイザは、コスト モデルに従って、 TiFlashフル テーブル スキャンの方がコスト効率が高いと推定する可能性があります。
        -   クエリ対象のテーブルのスキーマに適切なインデックスがない場合、オプティマイザは、クエリ対象のデータ量が少ない場合でも、テーブル全体のスキャンのためにクエリをTiFlashにプッシュすることしかできません。この場合、適切なインデックスを作成し、TiKV 経由でデータにアクセスする方が効率的です。

-   リクエスト期間: すべてのTiFlashインスタンスにおける各 MPP およびコプロセッサ リクエスト タイプの合計処理時間。これには平均レイテンシーと p99レイテンシーが含まれます。

-   リクエスト ハンドル時間: `cop`と`batch cop`のリクエストの実行開始から実行完了までの待ち時間を除く時間。このメトリクスは、平均レイテンシと P99レイテンシーを含む、 `cop`および`batch cop`タイプのリクエストにのみ適用されます。

例 1: TiFlash MPP リクエストの処理時間の概要

次の図のワークロードでは、 `run_mpp_task`と`mpp_establish_conn`のリクエストが合計処理時間の大部分を占めており、ほとんどのリクエストが実行のためにTiFlashに完全にプッシュダウンされる MPP タスクであることを示しています。

`cop`リクエストの処理時間は比較的短く、一部のリクエストがデータ アクセスとコプロセッサによるフィルタリングのためにTiFlashにプッシュダウンされていることを示しています。

![CH-TiFlash-MPP](/media/performance/tiflash/ch-2tiflash-op.png)

例 2: TiFlash `cop`リクエストが総処理時間の大部分を占める

次の図のワークロードでは、 `cop`リクエストが合計処理時間の大部分を占めています。この場合、SQL 実行プランをチェックして、これら`cop`のリクエストが生成された理由を確認できます。

![Cop](/media/performance/tiflash/tiflash_request_duration_by_type.png)

### Raft 関連のメトリクス {#raft-related-metrics}

次のメトリクスを使用して、 TiFlashのRaftレプリケーション ステータスを取得できます。

-   Raft待機インデックス期間: すべてのTiFlashインスタンスのローカルリージョンインデックスが`read_index`以上になるまでの待機期間。これは`wait_index`操作のレイテンシーを表します。このメトリクスが高すぎる場合は、TiKV からTiFlashへのデータ レプリケーションに重大なレイテンシーがあることを示します。考えられる理由は次のとおりです。

    -   TiKV リソースが過負荷になっています。
    -   TiFlashリソース、特に IO リソースが過負荷になっています。
    -   TiKV とTiFlashの間にネットワークのボトルネックがあります。

-   Raftバッチ読み取りインデックス期間: すべてのTiFlashインスタンスのレイテンシー`read_index` 。このメトリクスが高すぎる場合は、 TiFlashと TiKV の間の相互作用が遅いことを示します。考えられる理由は次のとおりです。

    -   TiFlashリソースが過負荷になっています。
    -   TiKV リソースが過負荷になっています。
    -   TiFlashと TiKV の間にネットワークのボトルネックがあります。

### IOスループットのメトリクス {#io-throughput-metrics}

次のメトリクスを使用して、 TiFlashの IO スループットを取得できます。

-   インスタンスごとの書き込みスループット: 各TiFlashインスタンスによって書き込まれるデータのスループット。これには、 Raftデータ ログとRaftスナップショットを適用することによるスループットが含まれます。

-   書き込みフロー: すべてのTiFlashインスタンスによるディスク書き込みのトラフィック。

    -   ファイル記述子: TiFlashによって使用される DeltaTreestorageエンジンの安定したレイヤー。
    -   Page: TiFlashで使用される DeltaTreestorageエンジンのデルタ変更レイヤーである Pagestore を指します。

-   読み取りフロー: すべてのTiFlashインスタンスのディスク読み取り操作のトラフィック。

    -   ファイル記述子: TiFlashによって使用される DeltaTreestorageエンジンの安定したレイヤー。
    -   Page: TiFlashで使用される DeltaTreestorageエンジンのデルタ変更レイヤーである Pagestore を指します。

TiFlashクラスター全体の書き込み増幅率は、 `(Read flow + Write flow) ÷ total Write Throughput By Instance`の式を使用して計算できます。

例 1: セルフホスト環境におけるRaftと[CH-benCHmark のワークロード](/benchmark/benchmark-tidb-using-ch.md)の IO メトリクス

次の図に示すように、このTiFlashクラスターの`Raft Wait Index Duration`パーセンタイルと`Raft Batch Read Index Duration`の 99 パーセンタイルは、それぞれ 3.24 秒と 753 ミリ秒と比較的高くなります。これは、このクラスターのTiFlashワークロードが高く、データ レプリケーションでレイテンシーが発生するためです。

このクラスターには 2 つのTiFlashノードがあります。 TiKV からTiFlashへの増分データ レプリケーションの速度は、1 秒あたり約 28 MB です。安定レイヤー(ファイル記述子) の最大書き込みスループットは 939 MB/秒、最大読み取りスループットは 1.1 GiB/秒です。一方、デルタレイヤー(Page) の最大書き込みスループットは 74 MB/s、最大読み取りスループットは 111 MB/s です。この環境では、 TiFlash は強力な IO スループット能力を持つ専用の NVME ディスクを使用します。

![CH-2TiFlash-OP](/media/performance/tiflash/ch-2tiflash-raft-io-flow.png)

例 2: パブリック クラウド デプロイメント環境におけるRaftと[CH-benCHmark のワークロード](/benchmark/benchmark-tidb-using-ch.md)の IO メトリクス

次の図に示すように、 `Raft Wait Index Duration`の 99 パーセンタイルは最大 438 ミリ秒、 `Raft Batch Read Index Duration`の 99 パーセンタイルは最大 125 ミリ秒です。このクラスターにはTiFlashノードが 1 つだけあります。 TiKV は、1 秒あたり約 5 MB の増分データをTiFlashにレプリケートします。安定レイヤー(ファイル記述子) の最大書き込みトラフィックは 78 MB/秒、最大読み取りトラフィックは 221 MB/秒です。一方、デルタレイヤー(ページ) の最大書き込みトラフィックは 8 MB/s、最大読み取りトラフィックは 18 MB/s です。この環境では、 TiFlash は、IO スループットが比較的弱い AWS EBS クラウド ディスクを使用します。

![CH-TiFlash-MPP](/media/performance/tiflash/ch-1tiflash-raft-io-flow-cloud.png)
