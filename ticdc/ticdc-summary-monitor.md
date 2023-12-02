---
title: TiCDC Monitoring Metrics Summary
summary: Learn about the monitoring metrics of TiCDC.
---

# TiCDC モニタリング指標の概要 {#ticdc-monitoring-metrics-summary}

v7.0.0 以降、 TiUP を使用して Grafana をデプロイすると、TiCDC 概要ダッシュボードが Grafana 監視ページに自動的に追加されます。このダッシュボードを通じて、TiCDC サーバーと変更フィードのステータスをすぐに理解できます。

次の図は、TiCDC 概要ダッシュボードの監視パネルを示しています。

![TiCDC Summary Dashboard - Overview](/media/ticdc/ticdc-summary-monitor.png)

各監視パネルは次のように説明されます。

-   サーバー: クラスター内の TiCDC ノードの概要。
-   Changefeed: TiCDC 変更フィードのレイテンシーとステータス情報。
-   データフロー: TiCDC 内部モジュールによって処理されたデータ変更の統計。
-   トランザクションシンク: ダウンストリーム MySQL または TiDB の書き込みレイテンシー。
-   MQ シンク: ダウンストリーム MQ システムの書き込みレイテンシー。
-   クラウド ストレージ シンク: ダウンストリーム クラウドstorageの書き込み速度。
-   やり直し: やり直し機能が有効になっている場合の書き込みレイテンシー。

## サーバーパネル {#server-panel}

**サーバー**パネルは次のとおりです。

![TiCDC Summary Dashboard - Server metrics](/media/ticdc/ticdc-summary-monitor-server.png)

-   **Uptime** : TiCDC ノードが実行されている時間。
-   **CPU 使用率**: TiCDC ノードの CPU 使用率。
-   **メモリ使用量**: TiCDC ノードのメモリ使用量。

## チェンジフィードパネル {#changefeed-panel}

**Changefeed**パネルは次のとおりです。

![TiCDC Summary Dashboard - Changefeed metrics](/media/ticdc/ticdc-summary-monitor-changefeed.png)

-   **Changefeed Checkpoint lag** : 上流の TiDB クラスターと下流のシステム間のデータ レプリケーションのレイテンシーを時間で測定して示します。一般に、このメトリックはデータ レプリケーション タスクの全体的な健全性を反映します。通常、遅延が小さいほど、レプリケーション タスクのステータスは良好になります。遅延が増加する場合、通常、チェンジフィードのレプリケーション能力またはダウンストリーム システムの消費能力がアップストリームの書き込み速度に追いつけないことを示しています。
-   **Changefeed Resolved ts lag** : 上流の TiDB クラスターと TiCDC ノード間のデータレイテンシーを時間で測定して示します。このメトリクスは、アップストリームからデータ変更をプルするチェンジフィードの機能を反映します。遅延が増加すると、チェンジフィードがアップストリームによって生成されたデータ変更を時間内に取得できないことを意味します。

## データフローパネル {#dataflow-panel}

![TiCDC Summary Dashboard - Puller metrics](/media/ticdc/ticdc-summary-monitor-dataflow-puller.png)

-   **Puller 出力イベント/s** : TiCDC ノードで、Puller モジュールによって Sorter モジュールに出力される 1 秒あたりのデータ変更の数。このメトリクスは、TiCDC がアップストリームからデータ変更をプルする速度を反映します。
-   **Puller 出力イベント**: TiCDC ノードの Puller モジュールによって Sorter モジュールに出力されたデータ変更の総数。

![TiCDC Summary Dashboard - Sorter metrics](/media/ticdc/ticdc-summary-monitor-dataflow-sorter.png)

-   **ソーター出力イベント/秒**: ソーター モジュールによって TiCDC ノードのシンク モジュールに出力される 1 秒あたりのデータ変更の数。 Sorter のデータ出力速度は Sink モジュールの影響を受けることに注意してください。したがって、Sorter モジュールの出力速度が Puller モジュールの出力速度よりも低い場合、それは必ずしも Sorter モジュールのソート速度が遅すぎることを意味するわけではありません。まず、シンク モジュールに関連するメトリクスを観察して、シンク モジュールがデータをフラッシュするのに時間がかかり、その結果ソーター モジュールの出力が低下するかどうかを確認する必要があります。

-   **ソーター出力イベント**: ソーター モジュールによって TiCDC ノードのシンク モジュールに出力されたデータ変更の総数。

![TiCDC Summary Dashboard - Mounter metrics](/media/ticdc/ticdc-summary-monitor-dataflow-mounter.png)

-   **マウンター出力イベント/秒**: TiCDC ノードでマウンター モジュールによってデコードされた 1 秒あたりのデータ変更の数。アップストリーム データの変更に多数のフィールドが含まれる場合、マウンタ モジュールのデコード速度が影響を受ける可能性があります。

-   **マウンター出力イベント**: TiCDC ノードのマウンター モジュールによってデコードされたデータ変更の総数。

![TiCDC Summary Dashboard - Sink metrics](/media/ticdc/ticdc-summary-monitor-dataflow-sink.png)

-   **シンク フラッシュ行/秒**: TiCDC ノードでシンク モジュールによってダウンストリームに出力される 1 秒あたりのデータ変更の数。このメトリクスは、データ変更がダウンストリームにレプリケートされる速度を反映します。**シンク フラッシュ行数/秒**が**プーラー出力イベント/秒**よりも低い場合、レプリケーションのレイテンシーが増加する可能性があります。

-   **シンク フラッシュ行**: シンク モジュールによって TiCDC ノードのダウンストリームに出力されたデータ変更の総数。

## トランザクションシンクパネル {#transaction-sink-panel}

**[トランザクションシンク]**パネルには、ダウンストリームが MySQL または TiDB である場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-transaction-sink.png)

-   **バックエンド フラッシュ期間**: TiCDCトランザクションシンク モジュールがダウンストリームで SQL ステートメントを実行するのにかかる期間。このメトリックを観察することで、ダウンストリームのパフォーマンスがレプリケーション速度のボトルネックになっているかどうかを判断できます。一般に、p999 値は 500 ミリ秒未満である必要があります。値がこの制限を超えると、レプリケーション速度に影響が生じ、変更フィード チェックポイントのラグが増加する可能性があります。

-   **フルフラッシュ期間**: ソーターによるソートから下流への送信まで、TiCDC の各トランザクションによって費やされる合計期間。この値から**バックエンド フラッシュ期間の**値を減算すると、ダウンストリームで実行される前のトランザクションの合計キュー時間を取得できます。キュー時間が長すぎる場合は、レプリケーション タスクにより多くのメモリクォータを割り当てることを検討できます。

## MQシンクパネル {#mq-sink-panel}

**MQ シンク**パネルには、ダウンストリームが Kafka である場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-mq-sink.png)

-   **ワーカー送信メッセージ継続時間パーセンタイル**: TiCDC MQ シンク ワーカーがダウンストリームにデータを送信するレイテンシー。
-   **Kafka Oncoming Bytes** : TiCDC MQ シンクがデータをダウンストリームに送信する速度。

## クラウドストレージシンクパネル {#cloud-storage-sink-panel}

**Cloud Storage シンク**パネルには、ダウンストリームが Cloud Storage である場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-cloud-storage.png)

-   **Write Bytes/s** : Cloud Storage Sink モジュールがダウンストリームにデータを書き込む速度。
-   **ファイル数**: Cloud Storage Sink モジュールによって書き込まれたファイルの総数。

## やり直しパネル {#redo-panel}

**[やり直し]**パネルには、やり直しログ機能が有効になっている場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-redo.png)

-   **Redo Write rows/s** : Redo モジュールによって 1 秒あたりに書き込まれる行数。やり直し機能が有効になっている場合、レプリケーション タスクのレイテンシーが増加すると、このメトリックとプーラー出力イベント/秒の値の間に大きな違いがあるかどうかを観察できます。その場合、レイテンシーのレイテンシーは、Redo モジュールの書き込み能力が不十分であることが原因である可能性があります。
-   **Redo Write byte/s** : Redo モジュールによって 1 秒あたりにデータが書き込まれる速度。
-   **REDO フラッシュ ログ期間**: REDO モジュールがデータをダウンストリームにフラッシュするのにかかる時間。このメトリック値が高い場合、この操作はレプリケーション速度に影響を与える可能性があります。
-   **REDO フラッシュオール期間**: データ変更が REDO モジュール内に留まる合計時間。
