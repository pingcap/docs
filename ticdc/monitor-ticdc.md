---
title: TiCDC Monitoring Metrics Details
summary: Grafana TiCDC ダッシュボードに表示されるいくつかの主要なメトリックについて学習します。
---

# TiCDC 監視メトリクスの詳細 {#ticdc-monitoring-metrics-details}

TiUPを使用して TiDB クラスターをデプロイすると、同時にデプロイされる監視システムに TiCDC のサブダッシュボードが表示されます。TiCDC ダッシュボードには主要なメトリクスが表示され、TiCDC の現在のステータスの概要を把握できます。このドキュメントでは、これらの主要なメトリクスについて詳しく説明します。

このドキュメントのメトリックの説明は、デフォルト設定を使用して MySQL にデータを複製する次のレプリケーション タスクの例に基づいています。

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

TiCDCダッシュボードには4つの監視パネルがあります。次のスクリーンショットをご覧ください。

![TiCDC Dashboard - Overview](/media/ticdc/ticdc-dashboard-overview.png)

各パネルの説明は次のとおりです。

-   [**サーバ**](#server) : TiDBクラスタ内のTiKVノードとTiCDCノードの概要情報
-   [**チェンジフィード**](#changefeed) : TiCDCレプリケーションタスクの詳細情報
-   [**イベント**](#events) : TiCDCクラスタ内のデータフローに関する詳細情報
-   [**TiKV**](#tikv) : TiCDCに関連するTiKV情報

## サーバ {#server}

以下は**サーバー**パネルの例です。

![TiCDC Dashboard - Server metrics](/media/ticdc/ticdc-dashboard-server.png)

**サーバー**パネルの各メトリックの説明は次のとおりです。

-   稼働時間: TiKVノードとTiCDCノードが稼働している時間
-   ゴルーチン数: TiCDCノードのゴルーチンの数
-   開いているFDの数: TiCDCノードによって開かれたファイルハンドルの数
-   所有権: TiCDC クラスター内のノードの現在のステータス
-   所有権の履歴: TiCDC クラスターの所有権の履歴
-   CPU使用率: TiCDCノードのCPU使用率
-   メモリ使用量: TiCDCノードのメモリ使用量

## チェンジフィード {#changefeed}

以下は**Changefeed**パネルの例です。

![TiCDC Dashboard - Changefeed metrics 1](/media/ticdc/ticdc-dashboard-changefeed-1.png)

-   変更フィードテーブル数: 各 TiCDC ノードがレプリケーションタスクで複製する必要があるテーブルの数
-   プロセッサ解決ts: TiCDCクラスタで解決されたタイムスタンプ
-   テーブル解決ts: レプリケーションタスク内の各テーブルのレプリケーションの進行状況
-   チェンジフィードチェックポイント：下流へのデータ複製の進行状況。通常、緑色のバーは黄色の線とつながっています。
-   PD etcdリクエスト数/秒: TiCDCノードがPDに送信するリクエスト数（1秒あたり）
-   終了エラー数/分: 1分あたりにレプリケーションタスクを中断するエラーの数
-   チェンジフィードチェックポイントラグ:上流と下流間のデータ複製の進行ラグ(単位は秒)
-   プロセッサ解決tsラグ:上流ノードとTiCDCノード間のデータ複製の進行ラグ（単位は秒）

![TiCDC Dashboard - Changefeed metrics 2](/media/ticdc/ticdc-dashboard-changefeed-2.png)

-   シンク書き込み時間: TiCDCがトランザクションの変更を下流に書き込むのに費やした時間のヒストグラム
-   シンク書き込み期間パーセンタイル: TiCDC が 1 秒以内にトランザクションの変更をダウンストリームに書き込むのに費やした時間 (P95、P99、および P999)
-   フラッシュシンク期間: TiCDC が非同期的にデータを下流にフラッシュするのにかかった時間のヒストグラム
-   フラッシュシンク期間パーセンタイル: TiCDC が 1 秒以内にデータを非同期にダウンストリームにフラッシュするのにかかった時間 (P95、P99、および P999)

![TiCDC Dashboard - Changefeed metrics 3](/media/ticdc/ticdc-dashboard-changefeed-3.png)

-   MySQLシンク競合検出期間: MySQLシンク競合の検出に費やされた時間のヒストグラム
-   MySQLシンク競合検出期間パーセンタイル: 1秒以内にMySQLシンク競合を検出するのに費やされた時間(P95、P99、P999)
-   MySQLシンクワーカーの負荷: TiCDCノードのMySQLシンクワーカーのワークロード

![TiCDC Dashboard - Changefeed metrics 4](/media/ticdc/ticdc-dashboard-changefeed-4.png)

-   Changefeed キャッチアップ ETA: レプリケーションタスクが上流のクラスタデータに追いつくのに必要な推定時間です。上流の書き込み速度が TiCDC のレプリケーション速度よりも速い場合、この指標は非常に大きくなる可能性があります。TiCDC のレプリケーション速度は多くの要因に左右されるため、この指標は参考値であり、実際のレプリケーション時間とは異なる可能性があります。

## イベント {#events}

以下は、**イベント**パネルの例です。

![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-1.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-2.png) ![TiCDC Dashboard - Events metrics 2](/media/ticdc/ticdc-dashboard-events-3.png)

**イベント**パネルの各メトリックの説明は次のとおりです。

-   イベントフィード数: TiCDCノードのイベントフィードRPCリクエストの数
-   イベントサイズのパーセンタイル: TiCDCがTiKVから1秒以内に受信するイベントサイズ（P95、P99、P999）
-   イベントフィード エラー/分: TiCDC ノードのイベントフィード RPC 要求によって 1 分あたりに報告されたエラーの数
-   KVクライアント受信イベント数/秒: TiCDCノードのKVクライアントモジュールがTiKVから1秒あたりに受信するイベント数
-   プラー受信イベント数/秒: TiCDCノードのプラーモジュールがKVクライアントから1秒あたりに受信するイベント数
-   プラー出力イベント数/秒: TiCDCノードのプラーモジュールがソーターモジュールに送信するイベント数（1秒あたり）
-   シンクフラッシュ行数/秒: TiCDCノードが1秒あたりにダウンストリームに書き込むイベント数
-   プラーバッファサイズ: TiCDCノードがプラーモジュールにキャッシュするイベントの数
-   エントリソーターバッファサイズ: TiCDCノードがソーターモジュールにキャッシュするイベントの数
-   プロセッサ/マウントバッファサイズ: TiCDCノードがプロセッサモジュールとマウントモジュールにキャッシュするイベントの数
-   シンク行バッファサイズ: TiCDCノードがシンクモジュールにキャッシュするイベントの数
-   エントリソーターのソート期間: TiCDCノードがイベントをソートするのにかかった時間のヒストグラム
-   エントリーソーターのソート所要時間パーセンタイル: TiCDC ソートイベントが 1 秒間に要した時間 (P95、P99、P999)
-   エントリソーターのマージ期間: TiCDCノードがソートされたイベントをマージするのにかかった時間のヒストグラム
-   エントリソーターのマージ所要時間パーセンタイル: TiCDCがソートされたイベントを1秒以内にマージするのにかかる時間 (P95、P99、P999)
-   マウンターのアンマーシャリング期間: TiCDCノードがイベントをアンマーシャリングするのにかかった時間のヒストグラム
-   マウンターのアンマーシャリング期間のパーセンタイル: TiCDC のアンマーシャリング イベントが 1 秒間に要した時間 (P95、P99、および P999)
-   KVクライアントディスパッチイベント数/秒: KVクライアントモジュールがTiCDCノード間でディスパッチするイベントの数
-   KVクライアントのバッチ解決サイズ: TiKVがTiCDCに送信する解決済みタイムスタンプメッセージのバッチサイズ

## TiKV {#tikv}

以下は**TiKV**パネルの例です。

![TiCDC Dashboard - TiKV metrics 1](/media/ticdc/ticdc-dashboard-tikv-1.png) ![TiCDC Dashboard - TiKV metrics 2](/media/ticdc/ticdc-dashboard-tikv-2.png)

**TiKV**パネルの各メトリックの説明は次のとおりです。

-   CDCエンドポイントCPU: TiKVノード上のCDCエンドポイントスレッドのCPU使用率
-   CDCワーカーCPU: TiKVノード上のCDCワーカースレッドのCPU使用率
-   最小解決タイムスタンプ: TiKVノード上の最小解決タイムスタンプ
-   最小解決リージョン: TiKVノード上の最小解決タイムスタンプのリージョンID
-   解決されたTSラグ期間パーセンタイル: TiKVノードの最小解決タイムスタンプと現在の時刻の間のラグ
-   初期スキャン期間: TiKVノードがTiCDCノードに接続する際の増分スキャンに費やされた時間のヒストグラム
-   初期スキャン所要時間パーセンタイル: 1秒以内にTiKVノードの増分スキャンに費やされた時間(P95、P99、P999)
-   ブロックキャッシュなしのメモリ: RocksDBブロックキャッシュを除いたTiKVノードのメモリ使用量
-   メモリ内のCDC保留バイト数: TiKVノード上のCDCモジュールのメモリ使用量
-   キャプチャされた領域数: TiKVノード上のイベントキャプチャ領域の数
