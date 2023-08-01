---
title: TiCDC Monitoring Metrics Details
summary: Learn some key metrics displayed on the Grafana TiCDC dashboard.
---

# TiCDC モニタリングメトリクスの詳細 {#ticdc-monitoring-metrics-details}

TiUPを使用して TiDB クラスターをデプロイすると、同時にデプロイされたモニタリング システムに TiCDC のサブダッシュボードが表示されます。 TiCDC の現在のステータスの概要は、主要な指標が表示される TiCDC ダッシュボードから取得できます。このドキュメントでは、これらの主要な指標について詳しく説明します。

このドキュメントのメトリクスの説明は、デフォルト構成を使用してデータを MySQL にレプリケートする次のレプリケーション タスクの例に基づいています。

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

TiCDC ダッシュボードには 4 つの監視パネルが含まれています。次のスクリーンショットを参照してください。

![TiCDC Dashboard - Overview](/media/ticdc/ticdc-dashboard-overview.png)

各パネルの説明は次のとおりです。

-   [**サーバ**](#server) : TiDB クラスター内の TiKV ノードと TiCDC ノードの概要情報
-   [**チェンジフィード**](#changefeed) : TiCDC レプリケーション タスクの詳細情報
-   [**イベント**](#events) : TiCDC クラスター内のデータ フローに関する詳細情報
-   [**TiKV**](#tikv) : TiCDC に関連する TiKV 情報

## サーバ {#server}

以下は**「サーバー」**パネルの例です。

![TiCDC Dashboard - Server metrics](/media/ticdc/ticdc-dashboard-server.png)

**「サーバー」**パネルの各メトリックの説明は次のとおりです。

-   稼働時間: TiKV ノードと TiCDC ノードが実行されている時間
-   ゴルーチン数: TiCDC ノードのゴルーチンの数
-   Open FD count: TiCDC ノードによってオープンされたファイル ハンドルの数
-   所有権: TiCDC クラスター内のノードの現在のステータス
-   所有権履歴: TiCDC クラスターの所有権履歴
-   CPU 使用率: TiCDC ノードの CPU 使用率
-   メモリ使用量: TiCDC ノードのメモリ使用量

## チェンジフィード {#changefeed}

以下は、 **Changefeed**パネルの例です。

![TiCDC Dashboard - Changefeed metrics 1](/media/ticdc/ticdc-dashboard-changefeed-1.png)

-   Changefeed テーブル数: レプリケーション タスクで各 TiCDC ノードがレプリケートする必要があるテーブルの数
-   プロセッサー解決済み ts: TiCDC クラスター内で解決されたタイムスタンプ
-   テーブル解決済み ts: レプリケーション タスク内の各テーブルのレプリケーションの進行状況
-   変更フィード チェックポイント: ダウンストリームへのデータの複製の進行状況。通常、緑色のバーは黄色の線に接続されます。
-   PD etcd リクエスト/秒: TiCDC ノードが 1 秒あたりに PD に送信するリクエストの数
-   終了エラー数/分: レプリケーション タスクを中断した 1 分あたりのエラー数
-   チェンジフィード チェックポイント ラグ: 上流と下流間のデータ レプリケーションの進行ラグ (単位は秒)
-   プロセッサー解決 ts ラグ: 上流ノードと TiCDC ノード間のデータ複製の進行ラグ (単位は秒)

![TiCDC Dashboard - Changefeed metrics 2](/media/ticdc/ticdc-dashboard-changefeed-2.png)

-   シンク書き込み期間: TiCDC がトランザクション変更をダウンストリームに書き込むのに費やした時間のヒストグラム
-   シンク書き込み期間パーセンタイル: TiCDC が 1 秒以内にトランザクション変更をダウンストリームに書き込むのに費やした時間 (P95、P99、および P999)
-   フラッシュ シンク期間: TiCDC がデータをダウンストリームに非同期的にフラッシュするのに費やした時間のヒストグラム
-   フラッシュ シンク期間パーセンタイル: TiCDC が 1 秒以内にデータをダウンストリームに非同期的にフラッシュするのに費やした時間 (P95、P99、および P999)

![TiCDC Dashboard - Changefeed metrics 3](/media/ticdc/ticdc-dashboard-changefeed-3.png)

-   MySQL シンク競合検出期間: MySQL シンク競合の検出に費やされた時間のヒストグラム
-   MySQL シンク競合検出期間パーセンタイル: 1 秒以内に MySQL シンク競合を検出するのに費やした時間 (P95、P99、および P999)
-   MySQL シンク ワーカーの負荷: TiCDC ノードの MySQL シンク ワーカーのワークロード

![TiCDC Dashboard - Changefeed metrics 4](/media/ticdc/ticdc-dashboard-changefeed-4.png)

-   Changefeed catch-up ETA: レプリケーション タスクが上流のクラスター データに追いつくのに必要な推定時間。アップストリームの書き込み速度が TiCDC レプリケーション速度よりも速い場合、メトリックは非常に大きくなる可能性があります。 TiCDC レプリケーション速度は多くの要因の影響を受けるため、このメトリクスは参照のみを目的としており、実際のレプリケーション時間ではない可能性があります。

## イベント {#events}

以下は、 **「イベント」**パネルの例です。

![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-1.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-2.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-3.png)

**[イベント]**パネルの各メトリックの説明は次のとおりです。

-   イベントフィード数: TiCDC ノードのイベントフィード RPC リクエストの数
-   イベント サイズ パーセンタイル: TiCDC が 1 秒以内に TiKV から受信したイベント サイズ (P95、P99、および P999)
-   Eventfeed error/m: TiCDC ノードの Eventfeed RPC リクエストによって報告された 1 分あたりのエラー数
-   KV クライアント受信イベント/秒: TiCDC ノードの KV クライアント モジュールが TiKV から受信する 1 秒あたりのイベント数
-   プーラー受信イベント/秒: TiCDC ノードのプーラー モジュールが KV クライアントから 1 秒あたりに受信するイベントの数
-   Puller 出力イベント/秒: TiCDC ノードの Puller モジュールが Sorter モジュールに送信する 1 秒あたりのイベント数
-   シンクフラッシュ行/秒: TiCDC ノードが 1 秒あたりにダウンストリームに書き込むイベントの数
-   Puller バッファー サイズ: TiCDC ノードが Puller モジュールにキャッシュするイベントの数
-   エントリ ソーター バッファ サイズ: TiCDC ノードがソーター モジュールにキャッシュするイベントの数
-   プロセッサ/マウンタ バッファ サイズ: TiCDC ノードがプロセッサ モジュールおよびマウンタ モジュールにキャッシュするイベントの数
-   シンク行バッファー サイズ: TiCDC ノードがシンク モジュールにキャッシュするイベントの数
-   エントリー・ソーターのソート期間: TiCDC ノードがイベントのソートに費やした時間のヒストグラム
-   エントリー・ソーターのソート期間パーセンタイル: 1 秒以内に TiCDC ソート・イベントに費やされた時間 (P95、P99、および P999)
-   エントリソーターのマージ期間: TiCDC ノードがソートされたイベントをマージするのに費やした時間のヒストグラム
-   エントリ ソーターのマージ期間パーセンタイル: TiCDC が 1 秒以内にソートされたイベントをマージするのに費やした時間 (P95、P99、および P999)
-   マウンタのアンマーシャリング期間: TiCDC ノードのアンマーシャリング イベントに費やされた時間のヒストグラム
-   マウンタのアンマーシャリング期間パーセンタイル: 1 秒以内に TiCDC アンマーシャリング イベントに費やされた時間 (P95、P99、および P999)
-   KV クライアント ディスパッチ イベント/秒: KV クライアント モジュールが TiCDC ノード間でディスパッチするイベントの数
-   KV クライアントのバッチ解決サイズ: TiKV が TiCDC に送信する解決されたタイムスタンプ メッセージのバッチ サイズ

## TiKV {#tikv}

以下は**TiKV**パネルの例です。

![TiCDC Dashboard - TiKV metrics 1](/media/ticdc/ticdc-dashboard-tikv-1.png) ![TiCDC Dashboard - TiKV metrics 2](/media/ticdc/ticdc-dashboard-tikv-2.png)

**TiKV**パネルの各メトリックの説明は次のとおりです。

-   CDC エンドポイント CPU: TiKV ノード上の CDC エンドポイント スレッドの CPU 使用率
-   CDC ワーカー CPU: TiKV ノード上の CDC ワーカー スレッドの CPU 使用率
-   最小解決 ts: TiKV ノード上の最小解決タイムスタンプ
-   最小解決リージョン: TiKV ノード上の最小解決タイムスタンプのリージョンID
-   解決された ts ラグ期間のパーセンタイル: TiKV ノード上の最小解決タイムスタンプと現在時刻との間のラグ。
-   初期スキャン期間: TiKV ノードが TiCDC ノードに接続するときに増分スキャンに費やされた時間のヒストグラム
-   初期スキャン期間パーセンタイル: 1 秒以内の TiKV ノードの増分スキャンに費やされた時間 (P95、P99、および P999)
-   ブロックキャッシュなしのメモリ : RocksDBブロックキャッシュを除いた TiKV ノードのメモリ使用量
-   メモリ内の CDC 保留バイト数 : TiKV ノード上の CDC モジュールのメモリ使用量
-   キャプチャされたリージョン数: TiKV ノード上のイベントをキャプチャしたリージョンの数
