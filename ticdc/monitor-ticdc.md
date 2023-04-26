---
title: Key Monitoring Metrics of TiCDC
summary: Learn some key metrics displayed on the Grafana TiCDC dashboard.
---

# TiCDC の主要な監視指標 {#key-monitoring-metrics-of-ticdc}

TiUPを使用して TiDB クラスターをデプロイすると、同時にデプロイされる監視システムに TiCDC のサブダッシュボードが表示されます。主要なメトリックが表示される TiCDC ダッシュボードから、TiCDC の現在のステータスの概要を取得できます。このドキュメントでは、これらの主要な指標について詳しく説明します。

このドキュメントのメトリクスの説明は、デフォルト設定を使用して MySQL にデータをレプリケートする次のレプリケーション タスクの例に基づいています。

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

TiCDC ダッシュボードには、4 つの監視パネルが含まれています。次のスクリーンショットを参照してください。

![TiCDC Dashboard - Overview](/media/ticdc/ticdc-dashboard-overview.png)

各パネルの説明は次のとおりです。

-   [**サーバ**](#server) : TiDB クラスター内の TiKV ノードと TiCDC ノードの概要情報
-   [**チェンジフィード**](#changefeed) : TiCDC レプリケーション タスクの詳細情報
-   [**イベント**](#events) : TiCDC クラスタ内のデータ フローに関する詳細情報
-   [**TiKV**](#tikv) : TiCDCに関連するTiKV情報

## サーバ {#server}

以下は、**サーバー**パネルの例です。

![TiCDC Dashboard - Server metrics](/media/ticdc/ticdc-dashboard-server.png)

**サーバー**パネルの各メトリックの説明は次のとおりです。

-   稼働時間: TiKV ノードと TiCDC ノードが稼働している時間
-   ゴルーチン数: TiCDC ノードのゴルーチン数
-   Open FD count: TiCDC ノードによって開かれたファイル ハンドルの数
-   所有権: TiCDC クラスター内のノードの現在のステータス
-   所有履歴: TiCDC クラスターの所有履歴
-   CPU 使用率: TiCDC ノードの CPU 使用率
-   メモリ使用量: TiCDC ノードのメモリ使用量

## チェンジフィード {#changefeed}

以下は**Changefeed**パネルの例です。

![TiCDC Dashboard - Changefeed metrics 1](/media/ticdc/ticdc-dashboard-changefeed-1.png)

-   Changefeed テーブル数: 各 TiCDC ノードがレプリケーション タスクでレプリケートする必要があるテーブルの数
-   プロセッサーが解決した ts: TiCDC クラスターで解決されたタイムスタンプ
-   テーブル解決 ts: レプリケーション タスクにおける各テーブルのレプリケーションの進行状況
-   Changefeed チェックポイント: ダウンストリームへのデータ複製の進行状況。通常、緑色のバーは黄色の線に接続されています
-   PD etcd requests/s: TiCDC ノードが 1 秒あたりに PD に送信するリクエストの数
-   終了エラー数/m: 1 分あたりのレプリケーション タスクを中断するエラーの数
-   Changefeed checkpoint lag: 上流と下流の間のデータ複製 (単位は秒) の進行ラグ。
-   Processor resolution ts lag: 上流ノードと TiCDC ノード間のデータ レプリケーションの進行ラグ (単位は秒)。

![TiCDC Dashboard - Changefeed metrics 2](/media/ticdc/ticdc-dashboard-changefeed-2.png)

-   シンク書き込み時間: TiCDC がトランザクションの変更をダウンストリームに書き込むのに費やした時間のヒストグラム
-   シンク書き込み時間パーセンタイル: TiCDC が 1 秒以内にトランザクション変更をダウンストリームに書き込むのに費やした時間 (P95、P99、および P999)
-   フラッシュ シンク期間: TiCDC がデータをダウンストリームに非同期的にフラッシュするのに費やした時間のヒストグラム
-   フラッシュ シンク期間パーセンタイル: TiCDC が 1 秒以内にデータをダウンストリームに非同期的にフラッシュするのに費やした時間 (P95、P99、および P999)

![TiCDC Dashboard - Changefeed metrics 3](/media/ticdc/ticdc-dashboard-changefeed-3.png)

-   MySQL シンク競合検出期間: MySQL シンク競合の検出に費やされた時間のヒストグラム
-   MySQL シンク競合検出期間パーセンタイル: 1 秒以内に MySQL シンク競合の検出に費やされた時間 (P95、P99、および P999)
-   MySQL シンク ワーカーの負荷: TiCDC ノードの MySQL シンク ワーカーのワークロード

![TiCDC Dashboard - Changefeed metrics 4](/media/ticdc/ticdc-dashboard-changefeed-4.png)

-   Changefeed キャッチアップ ETA: レプリケーション タスクが上流のクラスター データに追いつくために必要な推定時間。アップストリームの書き込み速度が TiCDC レプリケーション速度よりも速い場合、メトリックが非常に大きくなる可能性があります。 TiCDC のレプリケーション速度は多くの要因の影響を受けるため、このメトリックは参考用であり、実際のレプリケーション時間ではない場合があります。

## イベント {#events}

以下は、**イベント**パネルの例です。

![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-1.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-2.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-3.png)

**[イベント]**パネルの各メトリックの説明は次のとおりです。

-   Eventfeed count: TiCDC ノードの Eventfeed RPC リクエストの数
-   イベント サイズ パーセンタイル: TiCDC が TiKV から 1 秒以内に受け取るイベント サイズ (P95、P99、および P999)
-   Eventfeed error/m: TiCDC ノードの Eventfeed RPC リクエストによって報告された 1 分あたりのエラー数
-   KV クライアント受信イベント/秒: TiCDC ノードの KV クライアント モジュールが 1 秒あたりに TiKV から受信するイベントの数
-   Puller receive events/s: TiCDC ノードの Puller モジュールが 1 秒あたりに KV クライアントから受信するイベントの数
-   Puller output events/s: TiCDC ノードの Puller モジュールが Sorter モジュールに送信する 1 秒あたりのイベント数
-   シンク フラッシュ行/秒: TiCDC ノードが 1 秒あたりにダウンストリームに書き込むイベントの数
-   Puller buffer size: TiCDC ノードが Puller モジュールにキャッシュするイベントの数
-   エントリ ソーター バッファー サイズ: TiCDC ノードがソーター モジュールにキャッシュするイベントの数
-   プロセッサ/マウンタ バッファ サイズ: TiCDC ノードがプロセッサ モジュールとマウンタ モジュールにキャッシュするイベントの数
-   シンク行バッファー サイズ: TiCDC ノードがシンク モジュールにキャッシュするイベントの数
-   エントリ ソーターのソート期間: TiCDC ノードのソート イベントに費やされた時間のヒストグラム
-   エントリ ソーターの並べ替え期間パーセンタイル: 1 秒以内に TiCDC 並べ替えイベントに費やされた時間 (P95、P99、および P999)
-   エントリ ソーター マージ期間: TiCDC ノードがソートされたイベントをマージするのに費やした時間のヒストグラム
-   エントリ ソーター マージ期間パーセンタイル: TiCDC が並べ替えられたイベントを 1 秒以内にマージするのに費やした時間 (P95、P99、および P999)
-   マウンターの非整列化期間: TiCDC ノードの非整列化イベントに費やされた時間のヒストグラム
-   マウンター アンマーシャリング時間パーセンタイル: 1 秒以内に TiCDC アンマーシャリング イベントに費やされた時間 (P95、P99、および P999)
-   KV クライアント ディスパッチ イベント/秒: KV クライアント モジュールが TiCDC ノード間でディスパッチするイベントの数
-   KV クライアント バッチ解決サイズ: TiKV が TiCDC に送信する解決済みタイムスタンプ メッセージのバッチ サイズ

## TiKV {#tikv}

以下は、 **TiKV**パネルの例です。

![TiCDC Dashboard - TiKV metrics 1](/media/ticdc/ticdc-dashboard-tikv-1.png) ![TiCDC Dashboard - TiKV metrics 2](/media/ticdc/ticdc-dashboard-tikv-2.png)

**TiKV**パネルの各メトリックの説明は次のとおりです。

-   CDC エンドポイント CPU: TiKV ノード上の CDC エンドポイント スレッドの CPU 使用率
-   CDC ワーカー CPU: TiKV ノード上の CDC ワーカー スレッドの CPU 使用率
-   最小解決 ts: TiKV ノードで解決された最小タイムスタンプ
-   最小解決リージョン: TiKV ノードで解決された最小タイムスタンプのリージョンID
-   解決された ts ラグ期間パーセンタイル: TiKV ノードで解決された最小のタイムスタンプと現在の時刻との間のラグ
-   初期スキャン時間: TiKV ノードが TiCDC ノードに接続するときのインクリメンタル スキャンに費やされた時間のヒストグラム
-   初期スキャン時間パーセンタイル: 1 秒以内に TiKV ノードのインクリメンタル スキャンに費やされた時間 (P95、P99、および P999)
-   ブロックキャッシュなしのメモリ : RocksDBブロックキャッシュを除いた TiKV ノードのメモリ使用量
-   メモリ内の CDC 保留バイト : TiKV ノードでの CDC モジュールのメモリ使用量
-   キャプチャされたリージョン数: TiKV ノード上のイベント キャプチャ リージョンの数
