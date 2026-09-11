---
title: TiCDC Monitoring Metrics Details
summary: Grafana TiCDC ダッシュボードに表示されるいくつかの主要なメトリックについて学習します。
---

# TiCDC 監視メトリクスの詳細 {#ticdc-monitoring-metrics-details}

TiCDCの現在の状況の概要は、主要な指標が表示されるTiCDCダッシュボードから確認できます。このドキュメントでは、これらの主要な指標について詳しく説明します。

このドキュメントのメトリックの説明は、デフォルト設定を使用して MySQL にデータを複製する次のレプリケーションタスクの例に基づいています。

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

## 新しいアーキテクチャにおける TiCDC のメトリクス {#metrics-for-ticdc-in-the-new-architecture}

[新しいアーキテクチャにおけるTiCDC](/ticdc/ticdc-architecture.md)の監視ダッシュボードは**TiCDC-New-Arch**です。v8.5.4 以降のバージョンの TiDB クラスターでは、この監視ダッシュボードはクラスターのデプロイまたはアップグレード時に Grafana に統合されるため、手動操作は不要です。

クラスターのバージョンが v8.5.4 より前の場合は、TiCDC 監視メトリック ファイルを手動でインポートする必要があります。

1. 新しいアーキテクチャの TiCDC の監視メトリック ファイルをダウンロードします。

    ```shell
    wget https://raw.githubusercontent.com/pingcap/ticdc/refs/heads/release-8.5/metrics/grafana/ticdc_new_arch.json
    ```

2. ダウンロードしたメトリック ファイルを Grafana にインポートします。

    ![Import Metrics File](/media/ticdc/ticdc-new-arch-import-grafana.png)

TiCDC の新しいアーキテクチャの監視ダッシュボードには、主に次のセクションが含まれます。

- [**Summary**](#summary): TiCDCクラスターの概要情報
- [**Server**](#server): TiDBクラスタ内のTiKVノードとTiCDCノードの概要情報
- [**Log Puller**](#log-puller): TiCDC Log Pullerモジュールの詳細情報
- [**Event Store**](#event-store): TiCDCイベントストアモジュールの詳細情報
- [**Sink**](#sink): TiCDCシンクモジュールの詳細情報

### Summary {#summary}

以下は**Summary**パネルの例です。

![Summary](/media/ticdc/ticdc-new-arch-metric-summary.png)

**Summary**パネルの各メトリックの説明は次のとおりです。

- Changefeed Checkpoint Lag: 下流と上流の間のレプリケーションタスクのラグ
- Changefeed ResolvedTs Lag: TiCDCノードの内部処理の進行と上流データベース間の遅延
- Upstream Write Bytes/s:アップストリームデータベースの書き込みスループット
- TiCDC Input Bytes/s: TiCDCがアップストリームから1秒あたりに受信するデータ量
- Sink Event Row Count/s: TiCDCが1秒あたりにダウンストリームに書き込む行数
- Sink Write Bytes/s: TiCDCが1秒あたりにダウンストリームに書き込むデータの量
- The Status of Changefeeds: 各チェンジフィードのステータス
- Table Dispatcher Count: 各チェンジフィードに対応するディスパッチャの数
- Memory Quota: イベントコレクタのメモリクォータと使用量。使用量が多すぎるとスロットリングが発生する可能性があります。

### Server {#server}

以下は**Server**パネルの例です。

![Server](/media/ticdc/ticdc-new-arch-metric-server.png)

**Server**パネルの各メトリックの説明は次のとおりです。

- Uptime: TiKVノードとTiCDCノードが稼働している時間
- Goroutine Count: TiCDC ノード上の Goroutine の数
- Open FD Count: TiCDCノードによって開かれたファイルハンドルの数
- CPU Usage: TiCDCノードのCPU使用率
- Memory Usage: TiCDCノードのメモリ使用量
- Ownership History: TiCDC クラスター内の所有者ノードの履歴記録
- PD Leader History:上流TiDBクラスタ内のPD Leaderノードの履歴記録

### Log Puller {#log-puller}

以下は、 **Log Puller**パネルの例です。

![Log Puller](/media/ticdc/ticdc-new-arch-metric-log-puller.png)

**Log Puller**パネルの各メトリックの説明は次のとおりです。

- Input Events/s: TiCDCが1秒あたりに受信するイベント数
- Unresolved Region Request Count: TiCDC が送信したがまだ完了していないリージョン増分スキャンリクエストの数
- Region Request Finish Scan Duration:リージョン増分スキャンにかかる時間
- Subscribed Region Count: 登録済みリージョンの総数
- Memory Quota: Log Puller のメモリクォータと使用量。過剰な使用はスロットリングを引き起こす可能性があります。
- Resolved Ts Batch Size (Regions): 1つの解決済みTsイベントに含まれるリージョンの数

### Event Store {#event-store}

以下は、**Event Store**パネルの例です。

![Event Store](/media/ticdc/ticdc-new-arch-metric-event-store.png)

**Event Store**パネルの各メトリックの説明は次のとおりです。

- Resolved Ts Lag: イベントストアの処理の進行と上流データベース間のラグ
- Register Dispatcher StartTs Lag:ディスパッチャ登録StartTsと現在の時刻のラグ
- Subscriptions Resolved Ts Lag: サブスクリプション処理の進行と上流データベース間のラグ
- Subscriptions Data GC Lag: サブスクリプションデータGCの進行状況と現在の時刻の間のラグ
- Input Event Count/s: イベントストアが1秒あたりに処理するイベントの数
- Input Bytes/s: イベントストアが1秒あたりに処理するデータ量
- Write Requests/s: イベントストアが1秒あたりに実行する書き込みリクエストの数
- Write Worker Busy Ratio: イベントストア書き込みスレッドの合計実行時間に対するI/O時間の比率
- Compressed Rows/s: イベントストアで 1秒あたりに圧縮された行数 (行サイズがしきい値を超えた場合にのみトリガーされます)
- Write Duration: イベントストアの書き込み操作にかかる時間
- Write Batch Size: 1回の書き込み操作のバッチサイズ
- Write Batch Event Count: 1回の書き込みバッチに含まれる行変更イベントの数
- Data Size On Disk: イベントストアがディスク上で占める合計データサイズ
- Data Size In Memory: イベントストアがメモリ内で占める合計データサイズ
- Scan Requests/s: イベントストアが1秒あたりに実行するスキャンリクエストの数
- Scan Bytes/s: イベントストアが1秒あたりにスキャンするデータの量

### Sink {#sink}

以下は**Sink**パネルの例です。

![Sink](/media/ticdc/ticdc-new-arch-metric-sink.png)

**Sink**パネルの各メトリックの説明は次のとおりです。

- Output Row Batch Count: シンクモジュールによって書き込まれたDMLバッチあたりの平均行数
- Output Row Count (per second): 1秒あたりに下流に書き込まれるDML行数
- Output DDL Executing Duration: 現在のノードの変更フィードのDDLイベントの実行に費やされた時間
- Sink Error Count / m: シンクモジュールによって1分あたりに報告されたエラーの数
- Output DDL Count / Minutes: 現在のノードの変更フィードに対して1分あたりに実行されたDDLの数

## クラシックアーキテクチャにおける TiCDC のメトリクス {#metrics-for-ticdc-in-the-classic-architecture}

TiUPを使用して TiDB クラスターをデプロイすると、TiDB と同時にデプロイされる TiCDC のサブダッシュボードが Grafana の[クラシックアーキテクチャ](/ticdc/ticdc-classic-architecture.md)に表示されます。

各パネルの説明は次のとおりです。

- [**Server**](#server): TiDBクラスタ内のTiKVノードとTiCDCノードの概要情報
- [**Changefeed**](#changefeed): TiCDCレプリケーションタスクの詳細情報
- [**Events**](#events): TiCDCクラスタ内のデータフローに関する詳細情報
- [**TiKV**](#tikv): TiCDCに関連するTiKV情報

### Server {#server}

以下は**Server**パネルの例です。

![TiCDC Dashboard - Server metrics](/media/ticdc/ticdc-dashboard-server.png)

**Server**パネルの各メトリックの説明は次のとおりです。

- Uptime: TiKVノードとTiCDCノードが稼働している時間
- Goroutine count: TiCDCノードのゴルーチンの数
- Open FD count: TiCDCノードによって開かれたファイルハンドルの数
- Ownership: TiCDC クラスター内のノードの現在のステータス
- Ownership history: TiCDCクラスターの所有権の履歴
- CPU usage: TiCDCノードのCPU使用率
- Memory usage: TiCDCノードのメモリ使用量

### Changefeed {#changefeed}

以下は**Changefeed**パネルの例です。

![TiCDC Dashboard - Changefeed metrics 1](/media/ticdc/ticdc-dashboard-changefeed-1.png)

- Changefeed table count: 各 TiCDC ノードがレプリケーションタスクで複製する必要があるテーブルの数
- Processor resolved ts: TiCDCクラスタで解決されたタイムスタンプ
- Table resolved ts: レプリケーションタスク内の各テーブルのレプリケーションの進行状況
- Changefeed checkpoint：下流へのデータ複製の進行状況。通常、緑色のバーは黄色の線とつながっています。
- PD etcd requests/s: TiCDCノードがPDに送信するリクエスト数（1秒あたり）
- Exit error count/m: 1分あたりにレプリケーションタスクを中断するエラーの数
- Changefeed checkpoint lag:上流と下流間のデータ複製の進行ラグ(単位は秒)
- Processor resolved ts lag:上流ノードとTiCDCノード間のデータ複製の進行ラグ（単位は秒）

![TiCDC Dashboard - Changefeed metrics 2](/media/ticdc/ticdc-dashboard-changefeed-2.png)

- Sink write duration: TiCDCがトランザクションの変更をダウンストリームに書き込むのに費やした時間のヒストグラム
- Sink write duration percentile: TiCDC が 1秒以内にトランザクションの変更をダウンストリームに書き込むのに費やした時間 (P95、P99、および P999)
- Flush sink duration: TiCDC が非同期的にデータを下流にフラッシュするのにかかった時間のヒストグラム
- Flush sink duration percentile: TiCDC が 1秒以内にデータを非同期にダウンストリームにフラッシュするのにかかる時間 (P95、P99、および P999)

![TiCDC Dashboard - Changefeed metrics 3](/media/ticdc/ticdc-dashboard-changefeed-3.png)

- MySQL sink conflict detect duration: MySQLシンク競合の検出に費やされた時間のヒストグラム
- MySQL sink conflict detect duration percentile: 1秒以内にMySQLシンク競合を検出するのに費やされた時間(P95、P99、P999)
- MySQL sink worker load: TiCDCノードのMySQLシンクワーカーのワークロード

![TiCDC Dashboard - Changefeed metrics 4](/media/ticdc/ticdc-dashboard-changefeed-4.png)

- Changefeed catch-up ETA: レプリケーションタスクが上流のクラスタデータに追いつくのに必要な推定時間です。上流の書き込み速度が TiCDC のレプリケーション速度よりも速い場合、この指標は非常に大きくなる可能性があります。TiCDC のレプリケーション速度は多くの要因に左右されるため、この指標は参考値であり、実際のレプリケーション時間とは異なる可能性があります。

### Events {#events}

以下は**Events**パネルの例です。

![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-1.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-2.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-3.png)

**Events**パネルの各メトリックの説明は次のとおりです。

- Eventfeed count: TiCDCノードのイベントフィードRPCリクエストの数
- Event size percentile: TiCDCがTiKVから1秒以内に受信するイベントサイズ（P95、P99、P999）
- Eventfeed error/m: TiCDCノードのイベントフィードRPCリクエストによって1分あたりに報告されたエラーの数
- KV client receive events/s: TiCDCノードのKVクライアントモジュールがTiKVから1秒あたりに受信するイベント数
- Puller receive events/s: TiCDCノードのPullerモジュールがKVクライアントから1秒あたりに受信するイベント数
- Puller output events/s: TiCDCノードのPullerモジュールがソーターモジュールに送信するイベント数/秒
- Sink flush rows/s: TiCDCノードが1秒あたりにダウンストリームに書き込む行数
- Puller buffer size: TiCDCノードがプラーモジュールにキャッシュするイベントの数
- Entry sorter buffer size: TiCDCノードがソーターモジュールにキャッシュするイベントの数
- Processor/Mounter buffer size: TiCDCノードがプロセッサモジュールとマウントモジュールにキャッシュするイベントの数
- Sink row buffer size: TiCDCノードがシンクモジュールにキャッシュするイベントの数
- Entry sorter sort duration: TiCDCノードがイベントをソートするのにかかった時間のヒストグラム
- Entry sorter sort duration percentile: TiCDCのソートイベントが1秒間に要した時間(P95、P99、P999)
- Entry sorter merge duration: TiCDCノードがソートされたイベントをマージするのにかかった時間のヒストグラム
- Entry sorter merge duration percentile: TiCDCがソートされたイベントを1秒以内にマージするのにかかる時間(P95、P99、P999)
- Mounter unmarshal duration: TiCDCノードがイベントをアンマーシャリングするのにかかった時間のヒストグラム
- Mounter unmarshal duration percentile: TiCDC アンマーシャリング イベントが 1秒間に要した時間 (P95、P99、および P999)
- KV client dispatch events/s: KVクライアントモジュールがTiCDCノード間で1秒あたりにディスパッチするイベント数
- KV client batch resolved size: TiKVがTiCDCに送信する解決済みタイムスタンプメッセージのバッチサイズ

### TiKV {#tikv}

以下は**TiKV**パネルの例です。

![TiCDC Dashboard - TiKV metrics 1](/media/ticdc/ticdc-dashboard-tikv-1.png) ![TiCDC Dashboard - TiKV metrics 2](/media/ticdc/ticdc-dashboard-tikv-2.png)

**TiKV**パネルの各メトリックの説明は次のとおりです。

- CDC endpoint CPU: TiKVノード上のCDCエンドポイントスレッドのCPU使用率
- CDC worker CPU: TiKVノード上のCDCワーカースレッドのCPU使用率
- Min resolved ts: TiKVノード上の最小解決タイムスタンプ
- Min resolved region: TiKVノード上の最小解決タイムスタンプのリージョンID
- Resolved ts lag duration percentile: TiKVノード上の最小解決タイムスタンプと現在の時刻の間のラグ
- Initial scan duration: TiKVノードがTiCDCノードに接続する際の増分スキャンに費やされた時間のヒストグラム
- Initial scan duration percentile: 1秒以内にTiKVノードの増分スキャンに費やされた時間(P95、P99、P999)
- Memory without block cache: RocksDBブロックキャッシュを除いたTiKVノードのメモリ使用量
- CDC pending bytes in memory: TiKVノード上のCDCモジュールのメモリ使用量
- Captured region count: TiKVノード上のイベントキャプチャリージョンの数
