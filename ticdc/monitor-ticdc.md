---
title: Key Monitoring Metrics of TiCDC
summary: Learn some key metrics displayed on the Grafana TiCDC dashboard.
---

# TiCDCの主要な監視指標 {#key-monitoring-metrics-of-ticdc}

TiUPを使用してTiDBクラスタをデプロイすると、同時にデプロイされている監視システムにTiCDCのサブダッシュボードが表示されます。 TiCDCの現在のステータスの概要は、主要なメトリックが表示されるTiCDCダッシュボードから取得できます。このドキュメントでは、これらの主要な指標について詳しく説明します。

このドキュメントのメトリックの説明は、デフォルト構成を使用してデータをMySQLにレプリケートする次のレプリケーションタスクの例に基づいています。

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

TiCDCダッシュボードには、4つの監視パネルが含まれています。次のスクリーンショットを参照してください。

![TiCDC Dashboard - Overview](/media/ticdc/ticdc-dashboard-overview.png)

各パネルの説明は次のとおりです。

-   [**サーバ**](#server) ：TiDBクラスタのTiKVノードとTiCDCノードの概要情報
-   [**チェンジフィード**](#changefeed) ：TiCDCレプリケーションタスクの詳細情報
-   [**イベント**](#events) ：TiCDCクラスタ内のデータフローに関する詳細情報
-   [**TiKV**](#tikv) ：TiCDCに関連するTiKV情報

## サーバ {#server}

次に、**サーバー**パネルの例を示します。

![TiCDC Dashboard - Server metrics](/media/ticdc/ticdc-dashboard-server.png)

**サーバー**パネルの各メトリックの説明は次のとおりです。

-   稼働時間：TiKVノードとTiCDCノードが実行されている時間
-   ゴルーチン数：TiCDCノードのゴルーチンの数
-   Open FD count：TiCDCノードによって開かれたファイルハンドルの数
-   所有権：TiCDCクラスタのノードの現在のステータス
-   所有履歴：TiCDCクラスタの所有履歴
-   CPU使用率：TiCDCノードのCPU使用率
-   メモリ使用量：TiCDCノードのメモリ使用量

## チェンジフィード {#changefeed}

次に、 **Changefeed**パネルの例を示します。

![TiCDC Dashboard - Changefeed metrics 1](/media/ticdc/ticdc-dashboard-changefeed-1.png) ![TiCDC Dashboard - Changefeed metrics 2](/media/ticdc/ticdc-dashboard-changefeed-2.png) ![TiCDC Dashboard - Changefeed metrics 3](/media/ticdc/ticdc-dashboard-changefeed-3.png)

[**チェンジフィード**]パネルの各メトリックの説明は次のとおりです。

-   変更フィードテーブル数：各TiCDCノードがレプリケーションタスクでレプリケートする必要があるテーブルの数
-   プロセッサが解決したts：TiCDCクラスタで解決されたタイムスタンプ
-   テーブル解決済みts：レプリケーションタスクの各テーブルのレプリケーションの進行状況
-   チェンジフィードチェックポイント：ダウンストリームへのデータの複製の進行状況。通常、緑色のバーは黄色の線に接続されています
-   PD etcd requests / s：TiCDCノードが1秒あたりにPDに送信するリクエストの数
-   終了エラー数：1分あたりのレプリケーションタスクを中断するエラーの数
-   チェンジフィードチェックポイントラグ：アップストリームとダウンストリーム間のデータレプリケーションの進行ラグ（単位は2番目）
-   Changefeedが解決したtslag：アップストリームノードとTiCDCノード間のデータレプリケーションの進行ラグ（単位は2番目）
-   フラッシュシンク期間：TiCDCがデータをダウンストリームに非同期的にフラッシュするために費やした時間のヒストグラム
-   フラッシュシンク期間パーセンタイル：TiCDCが1秒以内にダウンストリームにデータを非同期的にフラッシュするために費やした時間（P95、P99、およびP999）
-   シンク書き込み期間：TiCDCがダウンストリームへのトランザクション変更の書き込みに費やした時間のヒストグラム
-   シンク書き込み期間パーセンタイル：TiCDCが1秒以内にダウンストリームへのトランザクション変更を書き込むために費やした時間（P95、P99、およびP999）
-   MySQLシンクの競合検出期間：MySQLシンクの競合の検出に費やされた時間のヒストグラム
-   MySQLシンク競合検出期間パーセンタイル：1秒以内にMySQLシンク競合を検出するために費やされた時間（P95、P99、およびP999）
-   MySQLシンクワーカーの負荷：TiCDCノードのMySQLシンクワーカーのワークロード

## イベント {#events}

次に、[**イベント**]パネルの例を示します。

![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-1.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-2.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-3.png)

[**イベント**]パネルの各メトリックの説明は次のとおりです。

-   イベントフィード数：TiCDCノードのイベントフィードRPCリクエストの数
-   イベントサイズのパーセンタイル：TiCDCが1秒以内にTiKVから受信するイベントサイズ（P95、P99、およびP999）
-   Eventfeed error / m：1分あたりのTiCDCノードのEventfeedRPC要求によって報告されたエラーの数
-   KVクライアント受信イベント/秒：TiCDCノードのKVクライアントモジュールがTiKVから1秒あたりに受信するイベントの数
-   Puller receive events / s：TiCDCノードのPullerモジュールがKVクライアントから1秒あたりに受信するイベントの数
-   プーラー出力イベント/秒：TiCDCノードのプーラーモジュールが1秒あたりにソーターモジュールに送信するイベントの数
-   シンクフラッシュ行/秒：TiCDCノードが1秒あたりにダウンストリームに書き込むイベントの数
-   プーラーバッファーサイズ：TiCDCノードがプーラーモジュールにキャッシュするイベントの数
-   エントリソーターのバッファーサイズ：TiCDCノードがソーターモジュールにキャッシュするイベントの数
-   プロセッサ/マウンタバッファサイズ：TiCDCノードがプロセッサモジュールとマウンタモジュールにキャッシュするイベントの数
-   シンク行のバッファサイズ：TiCDCノードがシンクモジュールにキャッシュするイベントの数
-   エントリソーターの並べ替え期間：TiCDCノードがイベントを並べ替えるのに費やした時間のヒストグラム
-   エントリソーターの並べ替え期間のパーセンタイル：1秒以内にTiCDCの並べ替えイベントに費やされた時間（P95、P99、およびP999）
-   エントリソーターのマージ期間：ソートされたイベントをマージするTiCDCノードによって費やされた時間のヒストグラム
-   エントリソーターマージ期間パーセンタイル：1秒以内にソートされたイベントをマージするためにTiCDCによって費やされた時間（P95、P99、およびP999）
-   マウンターのアンマーシャリング期間：イベントのマーシャリング解除にTiCDCノードが費やした時間のヒストグラム
-   マウンターアンマーシャリング期間パーセンタイル：1秒以内にTiCDCアンマーシャリングイベントによって費やされた時間（P95、P99、およびP999）
-   KVクライアントディスパッチイベント/秒：KVクライアントモジュールがTiCDCノード間でディスパッチするイベントの数
-   KVクライアントのバッチ解決サイズ：TiKVがTiCDCに送信する解決済みタイムスタンプメッセージのバッチサイズ

## TiKV {#tikv}

以下は、 **TiKV**パネルの例です。

![TiCDC Dashboard - TiKV metrics 2](/media/ticdc/ticdc-dashboard-tikv-2.png) ![TiCDC Dashboard - TiKV metrics 1](/media/ticdc/ticdc-dashboard-tikv-1.png)

**TiKV**パネルの各メトリックの説明は次のとおりです。

-   CDCエンドポイントCPU：TiKVノードでのCDCエンドポイントスレッドのCPU使用率
-   CDCワーカーCPU：TiKVノードでのCDCワーカースレッドのCPU使用率
-   最小解決済みts：TiKVノードでの最小解決済みタイムスタンプ
-   最小解決済みリージョン：TiKVノードで最小解決済みタイムスタンプのリージョンID
-   解決されたtsラグ期間パーセンタイル：TiKVノードの最小解決済みタイムスタンプと現在の時刻の間のラグ
-   初期スキャン期間：TiKVノードがTiCDCノードに接続するときに増分スキャンに費やされた時間のヒストグラム
-   初期スキャン期間パーセンタイル：1秒以内にTiKVノードのインクリメンタルスキャンに費やされた時間（P95、P99、およびP999）
-   ブロックキャッシュなしのメモリ：RocksDBブロックキャッシュを除くTiKVノードのメモリ使用量
-   メモリ内のCDC保留バイト：TiKVノードでのCDCモジュールのメモリ使用量
-   キャプチャされたリージョン数：TiKVノード上のイベントキャプチャリージョンの数
