---
title: TiCDC Monitoring Metrics Summary
summary: TiCDC の監視メトリックについて学習します。
---

# TiCDC モニタリング指標の概要 {#ticdc-monitoring-metrics-summary}

v7.0.0以降、 TiUPを使用してGrafanaをデプロイすると、TiCDCサマリーダッシュボードがGrafanaの監視ページに自動的に追加されます。このダッシュボードを通じて、TiCDCサーバーと変更フィードのステータスを迅速に把握できます。

次の画像は、TiCDC サマリー ダッシュボードの監視パネルを示しています。

![TiCDC Summary Dashboard - Overview](/media/ticdc/ticdc-summary-monitor.png)

各監視パネルの説明は次のとおりです。

- Server: クラスター内の TiCDC ノードの概要。
- Changefeed: TiCDC 変更フィードのレイテンシーとステータス情報。
- Dataflow: TiCDC 内部モジュールによって処理されるデータ変更の統計。
- Transaction Sink: ダウンストリーム MySQL または TiDB の書き込みレイテンシー。
- MQ Sink: ダウンストリーム MQ システムの書き込みレイテンシー。
- Cloud Storage Sink: ダウンストリーム クラウドストレージの書き込み速度。
- Redo: やり直し機能が有効な場合の書き込みレイテンシー。

## Server panel {#server-panel}

**Server**パネルは次のとおりです。

![TiCDC Summary Dashboard - Server metrics](/media/ticdc/ticdc-summary-monitor-server.png)

- **Uptime**: TiCDC ノードが実行されている時間。
- **CPU usage**: TiCDC ノードの CPU 使用率。
- **Memory usage**: TiCDC ノードのメモリ使用量。

## Changefeed panel {#changefeed-panel}

**Changefeed**パネルは次のとおりです。

![TiCDC Summary Dashboard - Changefeed metrics](/media/ticdc/ticdc-summary-monitor-changefeed.png)

- **Changefeed checkpoint lag**: 上流 TiDB クラスターと下流システム間のデータレプリケーションレイテンシーを時間で測定します。一般的に、この指標はデータレプリケーションタスクの全体的な健全性を反映します。通常、遅延が小さいほど、レプリケーションタスクの状態は良好です。遅延が大きくなる場合、通常、Changefeed のレプリケーション能力または下流システムの消費能力が上流の書き込み速度に追いついていないことを示します。
- **Changefeed resolved ts lag**: 上流 TiDB クラスターと TiCDC ノード間のデータレイテンシーを時間で測定します。この指標は、変更フィードが上流からデータ変更をプルする能力を反映しています。遅延が増加すると、変更フィードが上流で生成されたデータ変更を時間内にプルできないことを意味します。

## Dataflow panel {#dataflow-panel}

![TiCDC Summary Dashboard - Puller metrics](/media/ticdc/ticdc-summary-monitor-dataflow-puller.png)

- **Puller output events/s**: TiCDCノードにおいて、PullerモジュールからSorterモジュールへ1秒あたりに出力されるデータ変更の数。この指標は、TiCDCが上流からデータ変更をプルする速度を表します。
- **Puller output events**: TiCDC ノードの Puller モジュールから Sorter モジュールに出力されたデータ変更の合計数。

![TiCDC Summary Dashboard - Sorter metrics](/media/ticdc/ticdc-summary-monitor-dataflow-sorter.png)

- **Sorter output events/s**: TiCDCノードのSinkモジュールにSorterモジュールから1秒あたりに出力されるデータ変更の数。Sorterのデータ出力レートはSinkモジュールの影響を受けることに注意してください。したがって、Sorterモジュールの出力レートがPullerモジュールの出力レートよりも低い場合、必ずしもSorterモジュールのソート速度が遅すぎることを意味するわけではありません。まずSinkモジュールに関連するメトリクスを観察し、Sinkモジュールのデータフラッシュに時間がかかり、Sorterモジュールの出力が低下していないかどうかを確認する必要があります。

- **Sorter output event**: TiCDC ノードのソーターモジュールからシンク モジュールに出力されたデータ変更の合計数。

![TiCDC Summary Dashboard - Mounter metrics](/media/ticdc/ticdc-summary-monitor-dataflow-mounter.png)

- **Mounter output events/s**: TiCDCノードにおいて、マウンターモジュールによって1秒あたりにデコードされたデータ変更の数。上流のデータ変更に多数のフィールドが含まれる場合、マウンターモジュールのデコード速度に影響が出る可能性があります。

- **Mounter output event**: TiCDC ノードのマウンタ モジュールによってデコードされたデータ変更の合計数。

![TiCDC Summary Dashboard - Sink metrics](/media/ticdc/ticdc-summary-monitor-dataflow-sink.png)

- **Sink flush rows/s**: TiCDCノードにおいて、シンクモジュールが下流へ1秒あたりに出力するデータ変更の数。この指標は、データ変更が下流へ複製される速度を表します。**Sink flush rows/s**が**Puller output events/s**よりも低い場合、レプリケーションのレイテンシーが増加する可能性があります。

- **Sink flush rows**: シンク モジュールによって TiCDC ノードの下流に出力されたデータ変更の合計数。

## Transaction Sink panel {#transaction-sink-panel}

**Transaction Sink**パネルには、ダウンストリームが MySQL または TiDB の場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-transaction-sink.png)

- **Backend Flush Duration**: TiCDC トランザクション SinkモジュールがダウンストリームでSQL文を実行するのにかかる時間。この指標を観察することで、ダウンストリームのパフォーマンスがレプリケーション速度のボトルネックになっているかどうかを判断できます。通常、p999値は500ミリ秒未満である必要があります。この値がこの制限を超えると、レプリケーション速度に影響が及び、Changefeedチェックポイントの遅延が増加する可能性があります。

- **Full Flush Duration**: TiCDCにおける各トランザクションが、ソーターによるソートから下流への送信までに費やした合計時間。この値から**Backend Flush Duration**の値を差し引くことで、トランザクションが下流で実行されるまでの合計キューイング時間を取得できます。キューイング時間が長すぎる場合は、レプリケーションタスクに割り当てるメモリクォータを増やすことを検討してください。

## MQ Sink panel {#mq-sink-panel}

**MQ Sink**パネルには、ダウンストリームが Kafka の場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-mq-sink.png)

- **Worker Send Message Duration Percentile**: TiCDC MQ シンク ワーカーがダウンストリームにデータを送信する際のレイテンシー。
- **Kafka Ongoing Bytes**: TiCDC MQ Sink がダウンストリームにデータを送信する速度。

## Cloud Storage Sink panel {#cloud-storage-sink-panel}

**Cloud Storage Sink**パネルには、ダウンストリームが Cloud Storage の場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-cloud-storage.png)

- **Write Bytes/s**: Cloud Storage Sink モジュールがダウンストリームにデータを書き込む速度。
- **File Count**: Cloud Storage Sink モジュールによって書き込まれたファイルの合計数。

## Redo panel {#redo-panel}

**Redo**パネルには、やり直しログ機能が有効な場合にのみデータが表示されます。

![TiCDC Summary Dashboard - Transaction Sink metrics](/media/ticdc/ticdc-summary-monitor-redo.png)

- **Redo Write rows/s**: Redo モジュールによって1秒あたりに書き込まれる行数。Redo 機能が有効になっている場合、レプリケーションタスクのレイテンシーが増加すると、このメトリックと**Puller output events/s**の値に大きな差があるかどうかを確認できます。差がある場合、レイテンシーの増加は Redo モジュールの書き込み能力不足が原因である可能性があります。
- **Redo Write byte/s**: Redo モジュールによって 1秒あたりにデータが書き込まれる速度。
- **Redo flush log duration**：Redoモジュールがデータを下流にフラッシュするのにかかる時間。このメトリック値が高い場合、この操作はレプリケーション速度に影響を与える可能性があります。
- **Redo flushall duration**: データの変更が Redo モジュールに留まる合計時間。
