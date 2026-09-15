---
title: Monitor the TiFlash Cluster
summary: TiFlashの監視項目について学びます。
---

# TiFlashクラスタを監視する {#monitor-the-tiflash-cluster}

このドキュメントでは、 TiFlashの監視項目について説明します。

TiUPを使用してTiDBクラスターをデプロイする場合、監視システム（PrometheusとGrafana）も同時にデプロイされます。詳細については、 [監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

Grafanaダッシュボードは、Overview、PD、TiDB、TiKV、Node_exporterを含む一連のサブダッシュボードに分かれています。診断に役立つ多くのメトリクスが用意されています。

TiFlash には、 **TiFlash-Summary** 、 **TiFlash-Proxy-Summary** 、 **TiFlash-Proxy-Details**の3つのダッシュボードパネルがあります。これらのパネルに表示されるメトリックは、 TiFlashの現在の状態を示します。 **TiFlash-Proxy-Summary**パネルと**TiFlash-Proxy-Details**パネルは、主にRaftレイヤーの情報を表示します。メトリックの詳細は[TiKVの主要な監視指標](/grafana-tikv-dashboard.md)を参照してください。

> **Note:**
>
> TiFlashのモニターを改善するには、 TiDB v4.0.5 以降のバージョンを使用することをお勧めします。

次のセクションでは、**TiFlash-Summary**のデフォルトの監視情報を紹介します。

## Server {#server}

- Store size: 各TiFlashインスタンスで使用されるストレージサイズ。
- Available size: 各TiFlashインスタンスで使用可能なストレージサイズ。
- Capacity size: 各TiFlashインスタンスのストレージ容量。
- Uptime: 前回の再起動以降のTiFlashの実行時間。
- Memory: TiFlashインスタンスごとのメモリ使用量。
- CPU Usage: TiFlashインスタンスごとの CPU 使用率。
- FSync OPS: TiFlashインスタンスあたりの 1秒あたりの fsync 操作の数。
- File Open OPS: TiFlashインスタンスあたりの1秒あたりの`open`操作数。
- Opened File Count: 現在各TiFlashインスタンスによって開かれているファイル記述子の数。

> **Note:**
>
> Store size、FSync OPS、File Open OPS、および Opened File Count は、現在、 TiFlashストレージレイヤーの監視情報のみをカバーしており、 TiFlash-Proxy ではカバーしていません。

## Coprocessor {#coprocessor}

- Request QPS: すべてのTiFlashインスタンスによって受信されたコプロセッサリクエストの数。`batch`はバッチリクエストの数です。`batch_cop`はバッチリクエスト内のコプロセッサリクエストの数です。`cop`はコプロセッサ インターフェイスを介して直接送信されたコプロセッサリクエストの数です。`cop_dag`はすべてのコプロセッサリクエスト内の DAG リクエストの数です。`super_batch`はスーパー バッチ機能を有効にするためのリクエストの数です。
- Executor QPS: すべてのTiFlashインスタンスが受信したリクエスト内の各タイプの DAG Executor の数。`table_scan`はテーブルスキャン Executor です。`selection`は選択 Executor です。`aggregation`は集約 Executor です。`top_n`は`TopN` Executor です。`limit`は制限 Executor です。
- Request Duration: コプロセッサリクエストを処理するすべてのTiFlashインスタンスの合計期間。合計期間は、コプロセッサリクエストを受信してからリクエストへの応答が完了するまでの期間です。
- Error QPS: コプロセッサリクエストを処理するすべてのTiFlashインスタンスのエラー数。`meet_lock`は読み取りデータがロックされていることを意味します。`region_not_found`はリージョンが存在しないことを意味します。`epoch_not_match`は読み取りリージョンエポックがローカル エポックと一致していないことを意味します。`kv_client_error`はTiKV との通信でエラーが返されたことを意味します。`internal_error`はTiFlashの内部システム エラーです。`other`はその他のタイプのエラーです。
- Request Handle Duration：すべてのTiFlashインスタンスがコプロセッサリクエストを処理する期間。処理時間は、コプロセッサリクエストの実行開始から完了までです。
- Response Bytes/Seconds: すべてのTiFlashインスタンスからの応答の合計バイト数。
- Cop task memory usage: コプロセッサリクエストを処理するすべてのTiFlashインスタンスの合計メモリ使用量。
- Handling Request Number: コプロセッサリクエストを処理しているすべてのTiFlashインスタンスの総数。リクエストの分類は、Request QPSと同じです。
- Threads of RPC: 各TiFlashインスタンスで使用される RPC スレッドのリアルタイム数。
- Max Threads of RPC: 各TiFlashインスタンスで最近使用された RPC スレッドの最大数。
- Threads: 各TiFlashインスタンスで使用されるスレッドのリアルタイム数。
- Max Threads: 各TiFlashインスタンスで最近使用されたスレッドの最大数。

## Task Scheduler {#task-scheduler}

- Min TSO: 各TiFlashインスタンスで実行されているすべてのクエリの中で最小のTSOです。この値により、最小TSOのクエリの実行スケジュールが確保されます。実行中のクエリがない場合、この値は符号なし64ビット整数の最大値となります。
- Estimated Thread Usage and Limit: 各TiFlashインスタンスで実行されるすべてのクエリによって使用されるスレッドの推定量と、その量に対するソフト制限とハード制限。
- Active and Waiting Queries Count: 各TiFlashインスタンスで実行中のクエリの数と待機中のクエリの数。
- Active and Waiting Tasks Count: 各TiFlashインスタンスで実行中のタスクと待機中のタスクの数。
- Hard Limit Exceeded Count: 各TiFlashインスタンスで実行されているクエリによって使用されるスレッドの推定数がハード制限を超えた回数。
- Task Waiting Duration: 各TiFlashインスタンスでのタスクの初期化からタスクのスケジュールまでの期間。

## DDL {#ddl}

- Schema Version: 各TiFlashインスタンスに現在キャッシュされているスキーマのバージョン。
- Schema Apply OPM：すべてのTiFlashインスタンスによって1分間に`apply`操作で同期されたTiDB `schema diff`の数。この項目には、 `diff apply` 、 `full apply` 、 `failed apply`の3種類の`apply`のカウントが含まれます。`diff apply`は単一の適用の通常のプロセスです。`diff apply`が失敗した場合、 `failed apply`が`1`増加し、 TiFlashは`full apply`にロールバックし、最新のスキーマ情報を取得してTiFlashのスキーマバージョンを更新します。
- Schema Internal DDL OPM: すべてのTiFlashインスタンスで 1分あたりに実行された特定の DDL 操作の数。
- Schema Apply Duration: すべてのTiFlashインスタンスでの単一の`apply schema`操作に使用される時間。

## Storage {#storage}

- Write Command OPS: すべてのTiFlashインスタンスのストレージレイヤーで 1秒あたりに受信される書き込みリクエストの数。
- Write Amplification: 各TiFlashインスタンスの書き込み増幅 (実際のディスク書き込みバイト数を論理データの書き込みバイト数で割った値)。`total`はこの開始以降の書き込み増幅で、 `5min`は過去 5分間の書き込み増幅です。
- Read Tasks OPS: TiFlashインスタンスごとのストレージレイヤーでの 1秒あたりの読み取りタスクの数。
- Rough Set Filter Rate: ストレージレイヤーの粗セットインデックスによってフィルタされた、過去 1分間に各TiFlashインスタンスによって読み取られたパケット数の割合。
- Internal Tasks OPS: すべてのTiFlashインスタンスが 1秒あたりに内部データ ソート タスクを実行する回数。
- Internal Tasks Duration: すべてのTiFlashインスタンスが内部データ ソート タスクに費やした時間。
- Page GC Tasks OPM: すべてのTiFlashインスタンスが 1分間に Delta データ ソート タスクを実行する回数。
- Page GC Tasks Duration: Delta データ ソート タスクを実行するためにすべてのTiFlashインスタンスで消費される時間の分布。
- Disk Write OPS: すべてのTiFlashインスタンスによる 1秒あたりのディスク書き込み数。
- Disk Read OPS: すべてのTiFlashインスタンスによる 1秒あたりのディスク読み取り数。
- Write flow: すべてのTiFlashインスタンスによるディスク書き込みのトラフィック。
- Read flow: すべてのTiFlashインスタンスによるディスク読み取りのトラフィック。

> **Note:**
>
> これらのメトリックは、 TiFlashストレージレイヤーの監視情報のみをカバーし、 TiFlash-Proxy の監視情報はカバーしません。

## Storage Write Stall {#storage-write-stall}

- Write & Delta Management Throughput: すべてのインスタンスの書き込みとデータ圧縮のスループット。
    - `throughput_write` Raftを介したデータ同期のスループットを意味します。
    - `throughput_delta-management`データ圧縮のスループットを意味します。
    - `total_write` 、前回の開始以降に書き込まれた合計バイト数を意味します。
    - `total_delta-management` 、前回の開始以降に圧縮されたデータの合計バイト数を意味します。
- Write Stall Duration: インスタンスごとの書き込みおよびリージョンデータの削除 (範囲の削除) の停止期間。
- Write Throughput By Instance：インスタンスごとの書き込みスループット。Raft書き込みコマンドとRaftスナップショットを適用した場合のスループットも含まれます。
- Write Command OPS By Instance: インスタンスによって受信されたさまざまな種類のコマンドの合計数。
    - `write block` 、データ ログがRaftを通じて同期されることを意味します。
    - `delete_range` 、一部のリージョンがこのインスタンスから削除されるか、このインスタンスに移動されることを意味します。
    - `ingest` 、いくつかのリージョンスナップショットがこのインスタンスに適用されていることを意味します。

## Raft {#raft}

- Read Index OPS: 各TiFlashインスタンスが1秒あたりに`read_index`リクエストをトリガーする回数。これはトリガーされたリージョンの数に等しくなります。
- Read Index Duration: すべてのTiFlashインスタンスの`read_index`が使用する時間。ほとんどの時間は、リージョンリーダーとのやり取りと再試行に使用されます。
- Wait Index Duration: すべてのTiFlashインスタンスに対して`wait_index`が使用する時間。つまり、 `read_index`リクエストを受信した後、ローカルインデックス &gt;= read_index になるまで待機する時間です。
