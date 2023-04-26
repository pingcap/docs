---
title: Monitor the TiFlash Cluster
summary: Learn the monitoring items of TiFlash.
---

# TiFlashクラスタを監視する {#monitor-the-tiflash-cluster}

このドキュメントでは、 TiFlashの監視項目について説明します。

TiUPを使用して TiDB クラスターをデプロイすると、監視システム (Prometheus &amp; Grafana) が同時にデプロイされます。詳細については、 [監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

Grafana ダッシュボードは、Overview、PD、TiDB、TiKV、および Node_exporter を含む一連のサブ ダッシュボードに分かれています。診断に役立つ多くの指標があります。

TiFlash には、 **TiFlash-Summary** 、 <strong>TiFlash-Proxy-Summary</strong> 、および<strong>TiFlash-Proxy-Details の</strong>3 つのダッシュボード パネルがあります。これらのパネルのメトリックは、 TiFlashの現在のステータスを示します。 <strong>TiFlash-Proxy-Summary</strong>および<strong>TiFlash-Proxy-Details</strong>パネルは、主にRaftレイヤーの情報を表示し、メトリクスは[TiKV の主要な監視指標](/grafana-tikv-dashboard.md)に詳述されています。

> **ノート：**
>
> TiFlashでの監視を改善するには、TiDB v4.0.5 以降のバージョンを使用することをお勧めします。

以下のセクションでは、 **TiFlash-Summary**のデフォルトの監視情報を紹介します。

## サーバ {#server}

-   ストア サイズ: 各TiFlashインスタンスによって使用されるstorageサイズ。
-   使用可能なサイズ: 各TiFlashインスタンスで使用可能なstorageサイズ。
-   容量サイズ: 各TiFlashインスタンスのstorage容量。
-   稼働時間: 最後の再起動以降のTiFlashの実行時間。
-   メモリ: TiFlashインスタンスごとのメモリ使用量。
-   CPU 使用率: TiFlashインスタンスごとの CPU 使用率。
-   FSync OPS: 1 秒あたりのTiFlashインスタンスごとの fsync 操作の数。
-   File Open OPS: 1 秒あたりのTiFlashインスタンスあたりの`open`操作の数。
-   Opened File Count: 各TiFlashインスタンスによって現在開かれているファイル記述子の数。

> **ノート：**
>
> ストア サイズ、FSync OPS、File Open OPS、および Opened File Count は現在、 TiFlashstorageレイヤーの監視情報のみをカバーし、 TiFlash-Proxy ではカバーしていません。

## コプロセッサー {#coprocessor}

-   リクエスト QPS: すべてのTiFlashインスタンスによって受信されたコプロセッサ リクエストの数。 `batch`はバッチ リクエストの数です。 `batch_cop`は、バッチ リクエスト内のコプロセッサ リクエストの数です。 `cop`は、コプロセッサー・インターフェースを介して直接送信されるコプロセッサー要求の数です。 `cop_dag`は、すべてのコプロセッサー要求における DAG 要求の数です。 `super_batch`は、スーパー バッチ機能を有効にするための要求の数です。
-   エグゼキュータ QPS: すべてのTiFlashインスタンスによって受信されたリクエスト内の各タイプの DAG エグゼキュータの数。 `table_scan`は、テーブル スキャン エグゼキュータです。 `selection`は選択エグゼキュータです。 `aggregation`は集計エグゼキュータです。 `top_n` `TopN`エグゼキュータです。 `limit`は制限実行者です。
-   Request Duration: コプロセッサー要求を処理するすべてのTiFlashインスタンスの合計時間。合計所要時間は、コプロセッサー要求を受信してから、要求に対する応答が完了するまでの時間です。
-   エラー QPS: コプロセッサ要求を処理するすべてのTiFlashインスタンスのエラー数。 `meet_lock` 、読み取りデータがロックされていることを意味します。 `region_not_found` 、リージョンが存在しないことを意味します。 `epoch_not_match`読み取りリージョンエポックがローカル エポックと矛盾していることを意味します。 `kv_client_error` 、TiKV との通信がエラーを返すことを意味します。 `internal_error`はTiFlashの内部システム エラーです。 `other`はその他の種類のエラーです。
-   リクエスト ハンドル期間: すべてのTiFlashインスタンスがコプロセッサ リクエストを処理する期間。処理時間は、コプロセッサ要求の実行開始から実行完了までです。
-   応答バイト/秒: すべてのTiFlashインスタンスからの応答の合計バイト数。
-   Cop タスクのメモリ使用量: コプロセッサ要求を処理するすべてのTiFlashインスタンスの合計メモリ使用量。
-   処理要求数: コプロセッサー要求を処理しているすべてのTiFlashインスタンスの総数。リクエストの分類は、リクエスト QPS と同じです。
-   RPC のスレッド: 各TiFlashインスタンスで使用される RPC スレッドのリアルタイム数。
-   RPC の最大スレッド数: 各TiFlashインスタンスで最近使用された RPC スレッドの最大数。
-   スレッド: 各TiFlashインスタンスで使用されるスレッドのリアルタイム数。
-   Max Threads: 各TiFlashインスタンスで最近使用されたスレッドの最大数。

## タスクスケジューラ {#task-scheduler}

-   最小 TSO: 各TiFlashインスタンスで実行されているすべてのクエリの最小 TSO。この値により、TSO が最小のクエリを実行するようにスケジュールできることが保証されます。クエリが実行されていない場合、この値は最大の符号なし 64 ビット整数です。
-   推定スレッド使用量と制限: 各TiFlashインスタンスで実行されるすべてのクエリで使用されるスレッドの推定量、および量のソフト制限とハード制限。
-   アクティブおよび待機中のクエリ数: 各TiFlashインスタンスで実行中のクエリと待機中のクエリの数。
-   アクティブおよび待機中のタスク数: 各TiFlashインスタンスで実行中のタスクと待機中のタスクの数。
-   Hard Limit Exceeded Count: 各TiFlashインスタンスで実行されているクエリによって使用されるスレッドの推定量がハード制限を超えた回数。
-   タスク待機期間: 各TiFlashインスタンスでのタスクの初期化からタスクのスケジューリングまでの期間。

## DDL {#ddl}

-   スキーマ バージョン: 各TiFlashインスタンスに現在キャッシュされているスキーマのバージョン。
-   Schema Apply OPM: 1 分あたりのすべてのTiFlashインスタンスによる`apply`操作で同期された TiDB `schema diff`の数。このアイテムに`full apply` 、 `apply` 3 種類のカウント ( `diff apply`が含まれます`failed apply`が含まれます。 `diff apply` 、単一の適用の通常のプロセスです。 `diff apply`失敗した場合、 `failed apply` `1`増加し、 TiFlash は`full apply`にロールバックし、最新のスキーマ情報をプルしてTiFlashのスキーマ バージョンを更新します。
-   Schema Internal DDL OPM: すべてのTiFlashインスタンスで 1 分あたりに実行された特定の DDL 操作の数。
-   Schema Apply Duration: すべてのTiFlashインスタンスで`apply schema`回の操作に費やされた時間。

## 保管所 {#storage}

-   書き込みコマンド OPS: すべてのTiFlashインスタンスのstorageレイヤーによって受信された 1 秒あたりの書き込み要求の数。
-   書き込み増幅: 各TiFlashインスタンスの書き込み増幅 (ディスク書き込みの実際のバイト数を論理データの書き込みバイト数で割ったもの)。 `total`はこの開始以降の書き込み増幅、 `5min`は過去 5 分間の書き込み増幅です。
-   Read Tasks OPS: 各TiFlashインスタンスの 1 秒あたりのstorageレイヤーでの読み取りタスクの数。
-   ラフ セット フィルター率:storageレイヤーのラフ セット インデックスによってフィルター処理された、直前の 1 分間に各TiFlashインスタンスによって読み取られたパケット数の割合。
-   Internal Tasks OPS: すべてのTiFlashインスタンスが 1 秒あたりに内部データ ソート タスクを実行する回数。
-   内部タスクの所要時間: 内部データの並べ替えタスクのためにすべてのTiFlashインスタンスによって費やされた時間。
-   ページ GC タスク OPM: すべてのTiFlashインスタンスが 1 分あたりにデルタ データの並べ替えタスクを実行する回数。
-   Page GC Tasks Duration: すべてのTiFlashインスタンスがデルタ データの並べ替えタスクを実行するために消費した時間の分布。
-   ディスク書き込み OPS: すべてのTiFlashインスタンスによる 1 秒あたりのディスク書き込み数。
-   ディスク読み取り OPS: すべてのTiFlashインスタンスによる 1 秒あたりのディスク読み取り数。
-   書き込みフロー: すべてのTiFlashインスタンスによるディスク書き込みのトラフィック。
-   読み取りフロー: すべてのTiFlashインスタンスによるディスク読み取りのトラフィック。

> **ノート：**
>
> これらのメトリックは、 TiFlashstorageレイヤーの監視情報のみをカバーし、 TiFlash-Proxy の情報はカバーしません。

## ストレージ書き込みストール {#storage-write-stall}

-   書き込みおよびデルタ管理スループット: すべてのインスタンスの書き込みおよびデータ圧縮のスループット。
    -   `throughput_write` Raftを介したデータ同期のスループットを意味します。
    -   `throughput_delta-management`データ圧縮のスループットを意味します。
    -   `total_write`最後の開始以降に書き込まれた合計バイト数を意味します。
    -   `total_delta-management`最後の開始以降に圧縮されたデータの合計バイト数を意味します。
-   Write Stall Duration: インスタンスごとの書き込みおよびリージョンデータの削除 (範囲の削除) のストール期間。
-   インスタンスごとの書き込みスループット: インスタンスごとの書き込みスループット。これには、 Raft書き込みコマンドとRaftスナップショットを適用することによるスループットが含まれます。
-   Write Command OPS By Instance: インスタンスが受信したさまざまな種類のコマンドの総数。
    -   `write block` 、 Raftを介して同期されたデータ ログを意味します。
    -   `delete_range` 、一部のリージョンがこのインスタンスから削除または移動されたことを意味します。
    -   `ingest`は、一部のリージョンスナップショットがこのインスタンスに適用されることを意味します。

## Raft {#raft}

-   Read Index OPS: 各TiFlashインスタンスが`read_index`リクエストをトリガーする回数。これは、トリガーされたリージョンの数と同じです。
-   Read Index Duration: すべてのTiFlashインスタンスで`read_index`が使用した時間。ほとんどの時間は、リージョンリーダーとの対話と再試行に使用されます。
-   Wait Index Duration: すべてのTiFlashインスタンスに対して`wait_index`によって使用される時間、つまり、 `read_index`要求が受信された後、ローカル インデックス &gt;= read_index になるまで待機するために使用される時間。
