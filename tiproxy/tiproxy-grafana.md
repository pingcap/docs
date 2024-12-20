---
title: TiProxy Monitoring Metrics
summary: TiProxy の監視項目について学習します。
---

# TiProxy 監視メトリクス {#tiproxy-monitoring-metrics}

このドキュメントでは、TiProxy の監視項目について説明します。

TiUP を使用して TiDB クラスターをデプロイすると、監視システム (Prometheus および Grafana) も同時にデプロイされます。詳細については、 [監視フレームワークの概要](/tidb-monitoring-framework.md)参照してください。

Grafana ダッシュボードは、Overview、PD、TiDB、TiKV、TiProxy、Node_exporter を含む一連のサブダッシュボードに分かれています。診断に役立つメトリックが多数あります。各ダッシュボードには、パネル グループとそのパネルが含まれています。

TiProxy には 4 つのパネル グループがあります。これらのパネルのメトリックは、TiProxy の現在のステータスを示します。

-   **TiProxy-Server** : インスタンス情報。
-   **TiProxy-Query-Summary** : CPS などの SQL クエリ メトリック。
-   **TiProxy-Backend** : TiProxy が接続する可能性のある TiDB ノードに関する情報。
-   **TiProxy-Balance** : 負荷分散メトリック。

## サーバ {#server}

-   CPU 使用率: 各 TiProxy インスタンスの CPU 使用率
-   メモリ使用量: 各 TiProxy インスタンスのメモリ使用量
-   稼働時間: 前回の再起動以降の各 TiProxy インスタンスの実行時間
-   接続数: 各 TiProxy インスタンスに接続されているクライアントの数
-   接続作成 OPM: 各 TiProxy インスタンスで 1 分ごとに作成される接続の数
-   切断 OPM: 1 分ごとの各理由による切断の数。理由には以下が含まれます。
    -   成功: クライアントは正常に切断されます
    -   クライアントネットワークの切断: クライアントが切断する前に`QUIT`コマンドを送信しません。ネットワークの問題やクライアントのシャットダウンによっても発生する可能性があります。
    -   クライアントのハンドシェイク失敗: クライアントが TiProxy とのハンドシェイクに失敗しました
    -   認証失敗: TiDB によってアクセスが拒否されました
    -   SQL エラー: TiDB は他の SQL エラーを返します
    -   プロキシシャットダウン: TiProxy はシャットダウンしています
    -   不正なパケット: TiProxy は MySQL パケットを解析できません
    -   バックエンドの取得失敗: TiProxy は接続に使用可能なバックエンドを見つけることができません
    -   プロキシ エラー: その他の TiProxy エラー
    -   バックエンドネットワークの中断: TiDB の読み取りまたは書き込みに失敗しました。これは、ネットワークの問題または TiDBサーバーのシャットダウンが原因である可能性があります。
    -   バックエンドのハンドシェイクが失敗しました: TiProxy は TiDBサーバーとのハンドシェイクに失敗しました
-   Goroutine 数: 各 TiProxy インスタンス上の Goroutine の数
-   所有者: さまざまなタスクを実行する TiProxy インスタンス。たとえば、 `10.24.31.1:3080 - vip` 、 `10.24.31.1:3080`の TiProxy インスタンスが仮想 IP にバインドされていることを示します。タスクには次のものが含まれます。
    -   vip: 仮想IPをバインドする
    -   metric_reader: TiDBサーバーから監視データを読み取ります

## クエリの概要 {#query-summary}

-   期間: 平均、P95、P99 SQL ステートメント実行期間。TiDB サーバーでの SQL ステートメント実行期間も含まれるため、TiDB Grafana パネルでの期間よりも長くなります。
-   インスタンスごとの P99 実行時間: 各 TiProxy インスタンスの P99 ステートメント実行時間
-   バックエンド別の P99 実行時間: 各 TiDB インスタンスで実行されるステートメントの P99 ステートメント実行時間
-   インスタンスごとの CPS: 各 TiProxy インスタンスの 1 秒あたりのコマンド数
-   バックエンドごとの CPS: 各 TiDB インスタンスの 1 秒あたりのコマンド数
-   CPS by CMD: SQL コマンド タイプ別にグループ化された 1 秒あたりのコマンド数
-   ハンドシェイク期間: クライアントと TiProxy 間のハンドシェイク フェーズの平均、P95、および P99 期間

## バランス {#balance}

-   バックエンド接続: 各 TiDB インスタンスと各 TiProxy インスタンス間の接続数。たとえば、 `10.24.31.1:6000 | 10.24.31.2:4000` TiProxy インスタンス`10.24.31.1:6000`と TiDB インスタンス`10.24.31.2:4000`間の接続を示します。
-   セッション移行 OPM: 1 分ごとに発生したセッション移行の数。TiDB インスタンスが別のインスタンスに移行したセッションを記録します。たとえば、 `succeed: 10.24.31.2:4000 => 10.24.31.3:4000` TiDB インスタンス`10.24.31.2:4000`から TiDB インスタンス`10.24.31.3:4000`に正常に移行されたセッションの数を示します。
-   セッション移行期間: 平均、P95、P99 セッション移行期間。
-   セッション移行の理由: 1 分ごとに発生したセッション移行の数とその理由。理由には次のものがあります。
    -   `status` : TiProxy は[ステータスベースの負荷分散](/tiproxy/tiproxy-load-balance.md#status-based-load-balancing)実行しました。
    -   `label` : TiProxy は[ラベルベースの負荷分散](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing)実行しました。
    -   `health` : TiProxy は[ヘルスベースの負荷分散](/tiproxy/tiproxy-load-balance.md#health-based-load-balancing)実行しました。
    -   `memory` : TiProxy は[メモリベースの負荷分散](/tiproxy/tiproxy-load-balance.md#memory-based-load-balancing)実行しました。
    -   `cpu` : TiProxy は[CPUベースの負荷分散](/tiproxy/tiproxy-load-balance.md#cpu-based-load-balancing)実行しました。
    -   `location` : TiProxy は[ロケーションベースの負荷分散](/tiproxy/tiproxy-load-balance.md#location-based-load-balancing)実行しました。
    -   `conn` : TiProxy は[接続数ベースの負荷分散](/tiproxy/tiproxy-load-balance.md#connection-count-based-load-balancing)実行しました。

## バックエンド {#backend}

-   バックエンド期間の取得: TiProxy が TiDB インスタンスに接続する平均、p95、p99 期間
-   Pingバックエンド期間: 各TiProxyインスタンスと各TiProxyインスタンス間のネットワークレイテンシー。たとえば、 `10.24.31.1:6000 | 10.24.31.2:4000` TiProxyインスタンス`10.24.31.1:6000`とTiDBインスタンス`10.24.31.2:4000`間のネットワークレイテンシーを示します。
-   ヘルスチェックサイクル: TiProxy インスタンスとすべての TiDB インスタンス間のヘルスチェックサイクルの期間。たとえば、 `10.24.31.1:6000` 、TiProxy インスタンス`10.24.31.1:6000`がすべての TiDB インスタンスに対して実行する最新のヘルスチェックの期間を示します。この期間が 3 秒を超える場合、TiProxy はバックエンドの TiDB リストをタイムリーに更新できない可能性があります。

## 渋滞 {#traffic}

-   バックエンドからのバイト/秒: 各 TiDB インスタンスから各 TiProxy インスタンスに 1 秒あたりに送信されるデータの量 (バイト単位)。
-   バックエンドからのパケット/秒: 各 TiDB インスタンスから各 TiProxy インスタンスに 1 秒あたりに送信される MySQL パケットの数。
-   バックエンドへのバイト/秒: 各 TiProxy インスタンスから各 TiDB インスタンスに 1 秒あたりに送信されるデータの量 (バイト単位)。
-   バックエンドへのパケット数/秒: 各 TiProxy インスタンスから各 TiDB インスタンスに 1 秒あたりに送信される MySQL パケットの数。
-   クロスロケーション バイト/秒: 各 TiProxy インスタンスから異なる場所にある TiDB インスタンスに 1 秒あたりに送信されるデータの量 (バイト単位)。
