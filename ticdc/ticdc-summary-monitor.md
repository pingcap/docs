---
title: TiCDC Monitoring Metrics Summary
summary: TiCDC の監視メトリックについて学習します。
---

# TiCDC モニタリング メトリックの概要 {#ticdc-monitoring-metrics-summary}

v7.0.0 以降では、 TiUPを使用して Grafana をデプロイすると、TiCDC サマリー ダッシュボードが Grafana 監視ページに自動的に追加されます。このダッシュボードを通じて、TiCDC サーバーと変更フィードのステータスをすぐに把握できます。

次の画像は、TiCDC サマリー ダッシュボードの監視パネルを示しています。

![TiCDC Summary Dashboard - Overview](/media/ticdc/ticdc-summary-monitor.png)

各監視パネルの説明は次のとおりです。

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

-   **稼働時間**: TiCDC ノードが実行されている時間。
-   **CPU 使用率**: TiCDC ノードの CPU 使用率。
-   **メモリ使用量**: TiCDC ノードのメモリ使用量。

## チェンジフィードパネル {#changefeed-panel}

**Changefeed**パネルは次のとおりです。

![TiCDC Summary Dashboard - Changefeed metrics](/media/ticdc/ticdc-summary-monitor-changefeed.png)

-   **Changefeed チェックポイント ラグ**: 時間で測定された、上流 TiDB クラスターと下流システム間のデータ レプリケーションのレイテンシーを示します。一般に、このメトリックはデータ レプリケーション タスクの全体的な健全性を反映します。通常、ラグが小さいほど、レプリケーション タスクの状態は良好です。ラグが大きくなると、通常、Changefeed のレプリケーション能力または下流システムの消費能力が上流の書き込み速度に追いつけないことを示します。
-   **Changefeed 解決 ts ラグ**: 時間で測定された、アップストリーム TiDB クラスターと TiCDC ノード間のデータレイテンシーを示します。このメトリックは、アップストリームからデータ変更をプルする changefeed の能力を反映します。ラグが増加すると、changefeed がアップストリームによって生成されたデータ変更を時間内にプルできないことを意味します。

## データフローパネル {#dataflow-panel}

![TiCDC Summary Dashboard - Puller metrics](/media/ticdc/ticdc-summary-monitor-dataflow-puller.png)

-   **Puller 出力イベント/秒**: TiCDC ノードで Puller モジュールから Sorter モジュールに 1 秒あたりに出力されるデータ変更の数。このメトリックは、TiCDC がアップストリームからデータ変更をプルする速度を反映します。
-   **Puller 出力イベント**: TiCDC ノード内の Puller モジュールから Sorter モジュールに出力されたデータ変更の合計数。

![TiCDC Summary Dashboard - Sorter metrics](/media/ticdc/ticdc-summary-monitor-dataflow-sorter.png)

-   **Sorter 出力イベント/秒**: TiCDC ノードの Sink モジュールに Sorter モジュールから 1 秒あたりに出力されるデータ変更の数。Sorter のデータ出力レートは Sink モジュールの影響を受けることに注意してください。したがって、Sorter モジュールの出力レートが Puller モジュールの出力レートよりも低いことがわかった場合、必ずしも Sorter モジュールのソート速度が遅すぎることを意味するわけではありません。まず、Sink モジュールに関連するメトリックを観察して、Sink モジュールがデータをフラッシュするのに長い時間がかかり、その結果 Sorter モジュールの出力が減少しているかどうかを確認する必要があります。

-   **ソーター出力イベント**: TiCDC ノード内のソーター モジュールによってシンク モジュールに出力されたデータ変更の合計数。

![TiCDC Summary Dashboard - Mounter metrics](/media/ticdc/ticdc-summary-monitor-dataflow-mounter.png)

-   **マウンタ出力イベント/秒**: TiCDC ノードでマウンタ モジュールによって 1 秒あたりにデコードされたデータ変更の数。アップストリーム データの変更に多数のフィールドが含まれる場合、マウンタ モジュールのデコード速度が影響を受ける可能性があります。

-   **マウンタ出力イベント**: TiCDC ノードのマウンタ モジュールによってデコードされたデータ変更の合計数。

![TiCDC Summary Dashboard - Sink metrics](/media/ticdc/ticdc-summary-monitor-dataflow-sink.png)

-   **シンク フラッシュ行数/秒**: TiCDC ノードでシンク モジュールによってダウンストリームに 1 秒あたりに出力されるデータ変更の数。このメトリックは、データ変更がダウンストリームにレプリケートされる速度を反映します。**シンク フラッシュ行数/秒が****プルラー出力イベント数/秒**よりも低い場合、レプリケーションのレイテンシーが長くなる可能性があります。

-   **シンク フラッシュ行**: シンク モジュールによって TiCDC ノードの下流に出力されるデータ変更の合計数。

## トランザクションシンクパネル {#transaction-sink-panel}

**トランザクションシンク**パネルには、ダウンストリームが MySQL または TiDB の場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-transaction-sink.png)

-   **バックエンド フラッシュ期間**: TiCDCトランザクションシンク モジュールがダウンストリームで SQL ステートメントを実行するのにかかる期間。このメトリックを観察することで、ダウンストリームのパフォーマンスがレプリケーション速度のボトルネックになっているかどうかを判断できます。通常、p999 値は 500 ミリ秒未満である必要があります。値がこの制限を超えると、レプリケーション速度が影響を受け、Changefeed チェックポイント ラグが増加する可能性があります。

-   **フル フラッシュ期間**: ソーターによるソートからダウンストリームへの送信まで、TiCDC 内の各トランザクションによって消費される合計期間。この値から**バックエンド フラッシュ期間の**値を減算すると、ダウンストリームで実行される前のトランザクションの合計キューイング時間を取得できます。キューイング時間が長すぎる場合は、レプリケーション タスクにメモリクォータをさらに割り当てることを検討できます。

## MQシンクパネル {#mq-sink-panel}

**MQ シンク**パネルには、ダウンストリームが Kafka の場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-mq-sink.png)

-   **ワーカー送信メッセージ期間パーセンタイル**: TiCDC MQ シンク ワーカーがダウンストリームにデータを送信する際のレイテンシー。
-   **Kafka 進行中のバイト**: TiCDC MQ シンクがダウンストリームにデータを送信する速度。

## クラウドストレージシンクパネル {#cloud-storage-sink-panel}

**Cloud Storage シンク**パネルには、ダウンストリームが Cloud Storage の場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-cloud-storage.png)

-   **書き込みバイト数/秒**: Cloud Storage Sink モジュールがダウンストリームにデータを書き込む速度。
-   **ファイル数**: Cloud Storage Sink モジュールによって書き込まれたファイルの合計数。

## やり直しパネル {#redo-panel}

**やり直し**パネルには、やり直しログ機能が有効になっている場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-redo.png)

-   **Redo 書き込み行数/秒**: Redo モジュールによって 1 秒あたりに書き込まれる行数。Redo 機能が有効になっている場合、レプリケーション タスクのレイテンシーが増加すると、このメトリックと Puller 出力イベント数/秒の値に大きな違いがあるかどうかを観察できます。違いがある場合、レイテンシーの増加は Redo モジュールの書き込み容量が不十分なために発生している可能性があります。
-   **Redo 書き込みバイト/秒**: Redo モジュールによって 1 秒あたりにデータが書き込まれる速度。
-   **Redo フラッシュ ログ期間**: Redo モジュールがデータをダウンストリームにフラッシュするのにかかる時間。このメトリック値が高い場合、この操作はレプリケーション速度に影響を与える可能性があります。
-   **Redo flushall 期間**: データの変更が Redo モジュールに留まる合計時間。
