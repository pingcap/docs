---
title: TiProxy Monitoring Metrics
summary: TiProxy の監視項目について学習します。
---

# TiProxy 監視メトリクス {#tiproxy-monitoring-metrics}

このドキュメントでは、TiProxy の監視項目について説明します。

TiUPを使用してTiDBクラスターをデプロイする場合、監視システム（PrometheusとGrafana）も同時にデプロイされます。詳細については、 [監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

Grafanaダッシュボードは、Overview、PD、TiDB、TiKV、TiProxy、Node_exporterを含む一連のサブダッシュボードに分かれています。診断に役立つ多くのメトリクスが用意されています。各ダッシュボードには、パネルグループとそのパネルが含まれています。

TiProxy には 4つのパネルグループがあります。これらのパネルに表示されるメトリックは、TiProxy の現在のステータスを示します。

- **TiProxy-Server** : インスタンス情報。
- **TiProxy-Query-Summary** : CPS などの SQL クエリ メトリック。
- **TiProxy-Backend** : TiProxy が接続する可能性のある TiDB ノードに関する情報。
- **TiProxy-Balance** : 負荷分散メトリック。

## Server {#server}

- CPU Usage: 各TiProxyインスタンスのCPU使用率
- Memory Usage: 各 TiProxy インスタンスのメモリ使用量
- Uptime: 前回の再起動以降の各 TiProxy インスタンスの実行時間
- Connection Count: 各 TiProxy インスタンスに接続されているクライアントの数
- Create Connection OPM: 各 TiProxy インスタンスで 1分ごとに作成される接続の数
- Disconnection OPM: 1分ごとの切断理由別の数。切断理由には以下が含まれます。
    - success: クライアントは正常に切断されます
    - client network break: クライアントが切断前に`QUIT`コマンドを送信しません。ネットワークの問題やクライアントのシャットダウンによっても発生する可能性があります。
    - client handshake fail: クライアントがTiProxyとのハンドシェイクに失敗しました
    - auth fail: TiDBによってアクセスが拒否されました
    - SQL error: TiDB はその他の SQL エラーを返します
    - proxy shutdown: TiProxy はシャットダウンしています
    - malformed packet: TiProxy は MySQL パケットを解析できません
    - get backend fail: TiProxy は接続に利用可能なバックエンドを見つけることができません
    - proxy error: その他の TiProxy エラー
    - backend network break: TiDBの読み取りまたは書き込みに失敗しました。これは、ネットワークの問題、またはTiDBサーバーのシャットダウンが原因である可能性があります。
    - backend handshake fail: TiProxy が TiDBサーバーとのハンドシェイクに失敗しました
- Goroutine Count: 各 TiProxy インスタンス上の Goroutine の数
- Owner: 様々なタスクを実行するTiProxyインスタンス。例えば、 `10.24.31.1:3080 - vip`は、 `10.24.31.1:3080`のTiProxyインスタンスが仮想IPにバインドされていることを示します。タスクには以下が含まれます。
    - vip: 仮想IPをバインドする
    - metric_reader: TiDBサーバーから監視データを読み取ります

## Query-Summary {#query-summary}

- Duration: 平均、P95、P99 SQL文の実行時間。TiDBサーバーでのSQL文の実行時間も含まれるため、TiDB Grafanaパネルで表示される時間よりも長くなります。
- P99 Duration By Instance: 各TiProxyインスタンスのP99ステートメント実行時間
- P99 Duration By Backend: 各TiDBインスタンスで実行されるステートメントのP99ステートメント実行時間
- CPS by Instance: 各 TiProxy インスタンスの 1秒あたりのコマンド数
- CPS by Backend: 各 TiDB インスタンスの 1秒あたりのコマンド数
- CPS by CMD: SQL コマンドの種類別にグループ化された 1秒あたりのコマンド数
- Handshake Duration: クライアントと TiProxy 間のハンドシェイク フェーズの平均、P95、および P99 期間

## Balance {#balance}

- Backend Connections: 各TiDBインスタンスと各TiProxyインスタンス間の接続数。例えば、 `10.24.31.1:6000 | 10.24.31.2:4000`は、TiProxyインスタンス`10.24.31.1:6000`とTiDBインスタンス`10.24.31.2:4000`間の接続数を示します。
- Session Migration OPM: 1分ごとに発生したセッション移行の数。TiDBインスタンスが別のインスタンスに移行したセッションを記録します。たとえば、 `succeed: 10.24.31.2:4000 => 10.24.31.3:4000`は、TiDBインスタンス`10.24.31.2:4000`からTiDBインスタンス`10.24.31.3:4000`に正常に移行されたセッションの数を示します。
- Session Migration Duration: 平均、P95、P99 セッション移行期間。
- Session Migration Reasons: 1分ごとに発生したセッション移行の数とその理由。理由には以下が含まれます。
    - `status` : TiProxy が[ステータスベースの負荷分散](/tiproxy/tiproxy-load-balance.md#status-based-load-balancing)を実行しました。
    - `label` : TiProxy が[ラベルベースの負荷分散](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing)を実行しました。
    - `health` : TiProxy が[ヘルスベースの負荷分散](/tiproxy/tiproxy-load-balance.md#health-based-load-balancing)を実行しました。
    - `memory` : TiProxy が[メモリベースの負荷分散](/tiproxy/tiproxy-load-balance.md#memory-based-load-balancing)を実行しました。
    - `cpu` : TiProxy が[CPUベースの負荷分散](/tiproxy/tiproxy-load-balance.md#cpu-based-load-balancing)を実行しました。
    - `location` : TiProxy が[ロケーションベースの負荷分散](/tiproxy/tiproxy-load-balance.md#location-based-load-balancing)を実行しました。
    - `conn` : TiProxy が[接続数ベースの負荷分散](/tiproxy/tiproxy-load-balance.md#connection-count-based-load-balancing)を実行しました。

## Backend {#backend}

- Get Backend Duration: TiProxy が TiDB インスタンスに接続する平均、p95、p99 期間
- Ping Backend Duration: 各TiProxyインスタンス間のネットワークレイテンシー。例えば、 `10.24.31.1:6000 | 10.24.31.2:4000`は、TiProxyインスタンス`10.24.31.1:6000`とTiDBインスタンス`10.24.31.2:4000`間のネットワークレイテンシーを示します。
- Health Check Cycle: TiProxyインスタンスとすべてのTiDBインスタンス間のヘルスチェックサイクルの所要時間。例えば、 `10.24.31.1:6000`は、TiProxyインスタンス`10.24.31.1:6000`がすべてのTiDBインスタンスに対して実行する最新のヘルスチェックの所要時間を示します。この所要時間が3秒を超える場合、TiProxyはバックエンドのTiDBリストを適切なタイミングで更新できない可能性があります。

## Traffic {#traffic}

- Bytes/Second from Backends: 各 TiDB インスタンスから各 TiProxy インスタンスに 1秒あたりに送信されたデータの量 (バイト単位)。
- Packets/Second from Backends: 各 TiDB インスタンスから各 TiProxy インスタンスに 1秒あたりに送信された MySQL パケットの数。
- Bytes/Second to Backends: 各 TiProxy インスタンスから各 TiDB インスタンスに 1秒あたりに送信されたデータの量 (バイト単位)。
- Packets/Second to Backends: 各 TiProxy インスタンスから各 TiDB インスタンスに 1秒あたりに送信される MySQL パケットの数。
- Cross Location Bytes/Second: 各 TiProxy インスタンスから異なる場所にある TiDB インスタンスに 1秒あたりに送信されるデータの量 (バイト単位)。
