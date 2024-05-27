---
title: TiCDC Monitoring Metrics Details
summary: Grafana TiCDC ダッシュボードに表示されるいくつかの主要なメトリックについて学習します。
---

# TiCDC モニタリング メトリックの詳細 {#ticdc-monitoring-metrics-details}

TiUPを使用して TiDB クラスターをデプロイすると、同時にデプロイされる監視システムで TiCDC のサブダッシュボードが表示されます。主要なメトリックが表示される TiCDC ダッシュボードから、TiCDC の現在のステータスの概要を取得できます。このドキュメントでは、これらの主要なメトリックについて詳しく説明します。

このドキュメントのメトリックの説明は、デフォルト設定を使用してデータを MySQL に複製する次のレプリケーション タスクの例に基づいています。

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

TiCDC ダッシュボードには 4 つの監視パネルが含まれています。次のスクリーンショットを参照してください。

![TiCDC Dashboard - Overview](/media/ticdc/ticdc-dashboard-overview.png)

各パネルの説明は次のとおりです。

-   [**サーバ**](#server) : TiDBクラスタ内のTiKVノードとTiCDCノードの概要情報
-   [**チェンジフィード**](#changefeed) : TiCDCレプリケーションタスクの詳細情報
-   [**イベント**](#events) : TiCDCクラスタ内のデータフローに関する詳細情報
-   [**ティクヴ**](#tikv) : TiCDCに関連するTiKV情報

## サーバ {#server}

以下は**サーバー**パネルの例です。

![TiCDC Dashboard - Server metrics](/media/ticdc/ticdc-dashboard-server.png)

**サーバー**パネルの各メトリックの説明は次のとおりです。

-   稼働時間: TiKVノードとTiCDCノードが稼働している時間
-   ゴルーチン数: TiCDC ノードのゴルーチンの数
-   オープンFD数: TiCDCノードによって開かれたファイルハンドルの数
-   所有権: TiCDC クラスター内のノードの現在のステータス
-   所有権履歴: TiCDC クラスターの所有権履歴
-   CPU使用率: TiCDCノードのCPU使用率
-   メモリ使用量: TiCDCノードのメモリ使用量

## チェンジフィード {#changefeed}

以下は**Changefeed**パネルの例です。

![TiCDC Dashboard - Changefeed metrics 1](/media/ticdc/ticdc-dashboard-changefeed-1.png)

-   Changefeed テーブル数: 各 TiCDC ノードがレプリケーション タスクで複製する必要があるテーブルの数
-   プロセッサ解決ts: TiCDCクラスタで解決されたタイムスタンプ
-   テーブル解決ts: レプリケーションタスク内の各テーブルのレプリケーションの進行状況
-   チェンジフィードチェックポイント: 下流へのデータの複製の進行状況。通常、緑色のバーは黄色の線に接続されています。
-   PD etcd リクエスト数/秒: TiCDC ノードが PD に送信するリクエストの数 (1 秒あたり)
-   終了エラー数/分: 1分あたりのレプリケーションタスクを中断するエラーの数
-   チェンジフィードチェックポイントラグ:上流と下流の間のデータ複製の進行ラグ(単位は秒)
-   プロセッサ解決tsラグ:上流ノードとTiCDCノード間のデータ複製の進行ラグ(単位は秒)

![TiCDC Dashboard - Changefeed metrics 2](/media/ticdc/ticdc-dashboard-changefeed-2.png)

-   シンク書き込み時間: TiCDCがトランザクションの変更をダウンストリームに書き込むのに費やした時間のヒストグラム
-   シンク書き込み期間パーセンタイル: TiCDC が 1 秒以内にトランザクションの変更をダウンストリームに書き込むのに費やした時間 (P95、P99、および P999)
-   フラッシュシンク期間: TiCDC が非同期でデータを下流にフラッシュするのにかかった時間のヒストグラム
-   フラッシュシンク期間パーセンタイル: TiCDC が 1 秒以内にデータを非同期にダウンストリームにフラッシュするのにかかる時間 (P95、P99、および P999)

![TiCDC Dashboard - Changefeed metrics 3](/media/ticdc/ticdc-dashboard-changefeed-3.png)

-   MySQLシンク競合検出期間: MySQLシンク競合の検出に費やされた時間のヒストグラム
-   MySQL シンク競合検出期間パーセンタイル: 1 秒以内に MySQL シンク競合を検出するのに費やされた時間 (P95、P99、および P999)
-   MySQLシンクワーカー負荷: TiCDCノードのMySQLシンクワーカーのワークロード

![TiCDC Dashboard - Changefeed metrics 4](/media/ticdc/ticdc-dashboard-changefeed-4.png)

-   Changefeed キャッチアップ ETA: レプリケーション タスクがアップストリーム クラスター データに追いつくために必要な推定時間。アップストリームの書き込み速度が TiCDC レプリケーション速度よりも速い場合、メトリックは非常に大きくなる可能性があります。TiCDC レプリケーション速度は多くの要因の影響を受けるため、このメトリックは参照用であり、実際のレプリケーション時間ではない可能性があります。

## イベント {#events}

以下は**イベント**パネルの例です。

![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-1.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-2.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-3.png)

**イベント**パネルの各メトリックの説明は次のとおりです。

-   イベントフィード数: TiCDCノードのイベントフィードRPCリクエストの数
-   イベントサイズパーセンタイル: TiCDCが1秒以内にTiKVから受信するイベントサイズ(P95、P99、P999)
-   イベントフィード エラー/分: TiCDC ノードのイベントフィード RPC 要求によって 1 分あたりに報告されたエラーの数
-   KVクライアント受信イベント数/秒: TiCDCノードのKVクライアントモジュールがTiKVから1秒あたりに受信するイベント数
-   プルラー受信イベント数/秒: TiCDC ノードのプルラーモジュールが KV クライアントから 1 秒あたりに受信するイベントの数
-   プラー出力イベント数/秒: TiCDC ノードのプラーモジュールがソーターモジュールに送信するイベントの数 (1 秒あたり)
-   シンクフラッシュ行数/秒: TiCDCノードが1秒あたりにダウンストリームに書き込むイベント数
-   プラーバッファサイズ: TiCDCノードがプラーモジュールにキャッシュするイベントの数
-   エントリソーターバッファサイズ: TiCDCノードがソーターモジュールにキャッシュするイベントの数
-   プロセッサ/マウンタ バッファ サイズ: TiCDC ノードがプロセッサ モジュールとマウンタ モジュールにキャッシュするイベントの数
-   シンク行バッファサイズ: TiCDCノードがシンクモジュールにキャッシュするイベントの数
-   エントリソーターのソート期間: TiCDCノードがイベントをソートするのにかかった時間のヒストグラム
-   エントリーソーターのソート所要時間パーセンタイル: TiCDC ソートイベントが 1 秒以内に費やした時間 (P95、P99、および P999)
-   エントリソーターのマージ期間: TiCDCノードがソートされたイベントをマージするのにかかった時間のヒストグラム
-   エントリソーターのマージ所要時間パーセンタイル: TiCDC がソートされたイベントを 1 秒以内にマージするのにかかる時間 (P95、P99、および P999)
-   マウンターのアンマーシャリング期間: TiCDC ノードがイベントをアンマーシャリングするのにかかった時間のヒストグラム
-   マウンター アンマーシャリング期間パーセンタイル: 1 秒間に TiCDC アンマーシャリング イベントに費やされた時間 (P95、P99、および P999)
-   KVクライアントディスパッチイベント数/秒: KVクライアントモジュールがTiCDCノード間でディスパッチするイベントの数
-   KVクライアントバッチ解決サイズ: TiKVがTiCDCに送信する解決済みタイムスタンプメッセージのバッチサイズ

## ティクヴ {#tikv}

以下は**TiKV**パネルの例です。

![TiCDC Dashboard - TiKV metrics 1](/media/ticdc/ticdc-dashboard-tikv-1.png) ![TiCDC Dashboard - TiKV metrics 2](/media/ticdc/ticdc-dashboard-tikv-2.png)

**TiKV**パネルの各メトリックの説明は次のとおりです。

-   CDCエンドポイントCPU: TiKVノード上のCDCエンドポイントスレッドのCPU使用率
-   CDCワーカーCPU: TiKVノード上のCDCワーカースレッドのCPU使用率
-   最小解決タイムスタンプ: TiKVノード上の最小解決タイムスタンプ
-   最小解決リージョン: TiKVノード上の最小解決タイムスタンプのリージョンID
-   解決された ts ラグ期間パーセンタイル: TiKV ノード上の最小解決タイムスタンプと現在の時刻の間のラグ
-   初期スキャン期間: TiKVノードがTiCDCノードに接続する際の増分スキャンに費やされた時間のヒストグラム
-   初期スキャン期間パーセンタイル: 1秒以内にTiKVノードの増分スキャンに費やされた時間(P95、P99、P999)
-   ブロックキャッシュなしのメモリ: RocksDBブロックキャッシュを除いたTiKVノードのメモリ使用量
-   メモリ内の CDC 保留バイト数: TiKV ノード上の CDC モジュールのメモリ使用量
-   キャプチャされた領域の数: TiKVノード上のイベントキャプチャ領域の数
