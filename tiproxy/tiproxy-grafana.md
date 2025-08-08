---
title: TiProxy Monitoring Metrics
summary: TiProxy の監視項目について学習します。
---

# TiProxy 監視メトリクス {#tiproxy-monitoring-metrics}

このドキュメントでは、TiProxy の監視項目について説明します。

TiUPを使用してTiDBクラスターをデプロイする場合、監視システム（PrometheusとGrafana）も同時にデプロイされます。詳細については、 [監視フレームワークの概要](/tidb-monitoring-framework.md)参照してください。

Grafanaダッシュボードは、Overview、PD、TiDB、TiKV、TiProxy、Node_exporterを含む一連のサブダッシュボードに分かれています。診断に役立つ多くのメトリクスが用意されています。各ダッシュボードには、パネルグループとそのパネルが含まれています。

TiProxy には 4 つのパネルグループがあります。これらのパネルに表示されるメトリックは、TiProxy の現在のステータスを示します。

-   **TiProxy-Server** : インスタンス情報。
-   **TiProxy-Query-Summary** : CPS などの SQL クエリ メトリック。
-   **TiProxy-Backend** : TiProxy が接続する可能性のある TiDB ノードに関する情報。
-   **TiProxy-Balance** : 負荷分散メトリック。

## サーバ {#server}

-   CPU使用率: 各TiProxyインスタンスのCPU使用率
-   メモリ使用量: 各 TiProxy インスタンスのメモリ使用量
-   稼働時間: 前回の再起動以降の各 TiProxy インスタンスの実行時間
-   接続数: 各 TiProxy インスタンスに接続されているクライアントの数
-   接続作成 OPM: 各 TiProxy インスタンスで 1 分ごとに作成される接続の数
-   切断OPM：1分ごとの切断理由別の数。切断理由には以下が含まれます。
    -   成功: クライアントは正常に切断されます
    -   クライアントネットワークの切断：クライアントが切断前に`QUIT`コマンドを送信しない。ネットワークの問題やクライアントのシャットダウンによっても発生する可能性がある。
    -   クライアントのハンドシェイク失敗: クライアントがTiProxyとのハンドシェイクに失敗しました
    -   認証失敗: TiDBによってアクセスが拒否されました
    -   SQL エラー: TiDB は他の SQL エラーを返します
    -   プロキシのシャットダウン: TiProxy はシャットダウンしています
    -   不正なパケット: TiProxy は MySQL パケットを解析できません
    -   バックエンドの取得失敗: TiProxy は接続に利用可能なバックエンドを見つけることができません
    -   プロキシエラー: その他の TiProxy エラー
    -   バックエンドネットワークの中断: TiDBの読み取りまたは書き込みに失敗しました。これは、ネットワークの問題、またはTiDBサーバーのシャットダウンが原因である可能性があります。
    -   バックエンドのハンドシェイク失敗: TiProxy が TiDBサーバーとのハンドシェイクに失敗しました
-   Goroutine 数: 各 TiProxy インスタンス上の Goroutine の数
-   所有者: 様々なタスクを実行するTiProxyインスタンス。例えば、 `10.24.31.1:3080 - vip` `10.24.31.1:3080`のTiProxyインスタンスが仮想IPにバインドされていることを示します。タスクには以下が含まれます。
    -   vip: 仮想IPをバインドする
    -   metric_reader: TiDBサーバーから監視データを読み取ります

## クエリサマリー {#query-summary}

-   所要時間: 平均、P95、P99 SQL文の実行時間。TiDBサーバーでのSQL文の実行時間も含まれるため、TiDB Grafanaパネルで表示される時間よりも長くなります。
-   インスタンスごとのP99実行時間: 各TiProxyインスタンスのP99ステートメント実行時間
-   バックエンド別のP99実行時間: 各TiDBインスタンスで実行されるステートメントのP99ステートメント実行時間
-   インスタンスごとの CPS: 各 TiProxy インスタンスの 1 秒あたりのコマンド数
-   バックエンド別の CPS: 各 TiDB インスタンスの 1 秒あたりのコマンド数
-   CPS by CMD: SQL コマンドの種類別にグループ化された 1 秒あたりのコマンド数
-   ハンドシェイク期間: クライアントと TiProxy 間のハンドシェイク フェーズの平均、P95、および P99 期間

## バランス {#balance}

-   バックエンド接続: 各TiDBインスタンスと各TiProxyインスタンス間の接続数。例えば、 `10.24.31.1:6000 | 10.24.31.2:4000` TiProxyインスタンス`10.24.31.1:6000`とTiDBインスタンス`10.24.31.2:4000`間の接続数を示します。
-   セッション移行OPM: 1分ごとに発生したセッション移行の数。TiDBインスタンスが別のインスタンスに移行したセッションを記録します。たとえば、 `succeed: 10.24.31.2:4000 => 10.24.31.3:4000` TiDBインスタンス`10.24.31.2:4000`からTiDBインスタンス`10.24.31.3:4000`に正常に移行されたセッションの数を示します。
-   セッション移行期間: 平均、P95、P99 セッション移行期間。
-   セッション移行の理由: 1分ごとに発生したセッション移行の数とその理由。理由には以下が含まれます。
    -   `status` : TiProxy が[ステータスベースの負荷分散](/tiproxy/tiproxy-load-balance.md#status-based-load-balancing)実行しました。
    -   `label` : TiProxy が[ラベルベースの負荷分散](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing)実行しました。
    -   `health` : TiProxy が[ヘルスベースの負荷分散](/tiproxy/tiproxy-load-balance.md#health-based-load-balancing)実行しました。
    -   `memory` : TiProxy が[メモリベースの負荷分散](/tiproxy/tiproxy-load-balance.md#memory-based-load-balancing)実行しました。
    -   `cpu` : TiProxy が[CPUベースの負荷分散](/tiproxy/tiproxy-load-balance.md#cpu-based-load-balancing)実行しました。
    -   `location` : TiProxy が[ロケーションベースの負荷分散](/tiproxy/tiproxy-load-balance.md#location-based-load-balancing)実行しました。
    -   `conn` : TiProxy が[接続数ベースの負荷分散](/tiproxy/tiproxy-load-balance.md#connection-count-based-load-balancing)実行しました。

## バックエンド {#backend}

-   バックエンド期間の取得: TiProxy が TiDB インスタンスに接続する平均、p95、p99 期間
-   Pingバックエンド期間: 各TiProxyインスタンス間のネットワークレイテンシー。例えば、 `10.24.31.1:6000 | 10.24.31.2:4000` TiProxyインスタンス`10.24.31.1:6000`とTiDBインスタンス`10.24.31.2:4000`間のネットワークレイテンシーを示します。
-   ヘルスチェックサイクル: TiProxyインスタンスとすべてのTiDBインスタンス間のヘルスチェックサイクルの所要時間。例えば、 `10.24.31.1:6000` TiProxyインスタンス`10.24.31.1:6000`すべてのTiDBインスタンスに対して実行する最新のヘルスチェックの所要時間を示します。この所要時間が3秒を超える場合、TiProxyはバックエンドのTiDBリストを適切なタイミングで更新できない可能性があります。

## 渋滞 {#traffic}

-   バックエンドからのバイト/秒: 各 TiDB インスタンスから各 TiProxy インスタンスに 1 秒あたりに送信されたデータの量 (バイト単位)。
-   バックエンドからのパケット/秒: 各 TiDB インスタンスから各 TiProxy インスタンスに 1 秒あたりに送信された MySQL パケットの数。
-   バックエンドへのバイト/秒: 各 TiProxy インスタンスから各 TiDB インスタンスに 1 秒あたりに送信されたデータの量 (バイト単位)。
-   バックエンドへのパケット数/秒: 各 TiProxy インスタンスから各 TiDB インスタンスに 1 秒あたりに送信される MySQL パケットの数。
-   クロスロケーション バイト/秒: 各 TiProxy インスタンスから異なる場所にある TiDB インスタンスに 1 秒あたりに送信されるデータの量 (バイト単位)。
