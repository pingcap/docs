---
title: Overview Page
summary: Learn the overview page of TiDB Dashboard.
---

# 概要ページ {#overview-page}

このページには、次の情報を含む TiDB クラスター全体の概要が表示されます。

-   クラスター全体の 1 秒あたりのクエリ数 (QPS)。
-   クラスター全体のクエリレイテンシー。
-   最近の期間で最長の実行時間を累積した SQL ステートメント。
-   最近の期間の実行時間がしきい値を超えている低速クエリ。
-   各インスタンスのノード数とステータス。
-   メッセージを監視および警告します。

## ページにアクセスする {#access-the-page}

TiDB ダッシュボードにログインすると、デフォルトで概要ページが表示されます。または、左側のナビゲーション メニューで**[概要]**をクリックしてこのページに入ることができます。

![Enter overview page](/media/dashboard/dashboard-overview-access-v650.png)

## QPS {#qps}

このエリアには、最近 1 時間のクラスター全体の 1 秒あたりの成功したクエリと失敗したクエリの数が表示されます。

![QPS](/media/dashboard/dashboard-overview-qps.png)

> **ノート：**
>
> この機能は、Prometheus 監視コンポーネントがデプロイされているクラスターでのみ使用できます。 Prometheus がデプロイされていない場合、エラーが表示されます。

## レイテンシー {#latency}

この領域は、最近 1 時間のクラスター全体のクエリの 99.9%、99%、および 90% の待機レイテンシーを示しています。

![Latency](/media/dashboard/dashboard-overview-latency.png)

> **ノート：**
>
> この機能は、Prometheus 監視コンポーネントがデプロイされているクラスターでのみ使用できます。 Prometheus がデプロイされていない場合、エラーが表示されます。

## Top SQLステートメント {#top-sql-statements}

この領域には、最近の期間にクラスター全体で最も長い実行時間を累積した 10 種類の SQL ステートメントが表示されます。クエリ パラメータが異なるが同じ構造の SQL ステートメントは、同じ SQL タイプに分類され、同じ行に表示されます。

![Top SQL](/media/dashboard/dashboard-overview-top-statements.png)

この領域に表示される情報は、より詳細な[SQL ステートメント ページ](/dashboard/dashboard-statement-list.md)と一致しています。**Top SQLステートメント**の見出しをクリックして、完全なリストを表示できます。この表の列の詳細については、 [SQL ステートメント ページ](/dashboard/dashboard-statement-list.md)を参照してください。

> **ノート：**
>
> この機能は、SQL ステートメント機能が有効になっているクラスターでのみ使用できます。

## 最近の遅いクエリ {#recent-slow-queries}

デフォルトでは、この領域には、最近 30 分間のクラスター全体の最新の 10 件のスロー クエリが表示されます。

![Recent slow queries](/media/dashboard/dashboard-overview-slow-query.png)

デフォルトでは、300 ミリ秒を超えて実行された SQL クエリはスロー クエリとしてカウントされ、テーブルに表示されます。このしきい値は、変数[tidb_slow_log_threshold](/system-variables.md#tidb_slow_log_threshold)または TiDB パラメーター[低速しきい値](/tidb-configuration-file.md#slow-threshold)を変更することで変更できます。

この領域に表示される内容は、より詳細な[スロークエリページ](/dashboard/dashboard-slow-query.md)と一致しています。 **[Recent Slow Queries]**タイトルをクリックして、完全なリストを表示できます。この表の列の詳細については、この[スロークエリページ](/dashboard/dashboard-slow-query.md)を参照してください。

> **ノート：**
>
> この機能は、スロー クエリ ログが有効になっているクラスターでのみ使用できます。デフォルトでは、 TiUP を使用してデプロイされたクラスターでスロー クエリ ログが有効になっています。

## インスタンス {#instances}

この領域には、クラスター全体の TiDB、TiKV、PD、およびTiFlashのインスタンスの総数と異常なインスタンスがまとめられています。

![Instances](/media/dashboard/dashboard-overview-instances.png)

前の図のステータスは、次のように説明されています。

-   Up: インスタンスは正常に動作しています (オフラインstorageインスタンスを含む)。
-   Down: ネットワークの切断やプロセスのクラッシュなど、インスタンスが異常に動作しています。

**インスタンスの**タイトルをクリックして、各インスタンスの詳細な実行ステータスを示す[クラスタ情報ページ](/dashboard/dashboard-cluster-info.md)入力します。

## 監視と警告 {#monitor-and-alert}

この領域には、詳細な監視とアラートを表示するためのリンクがあります。

![Monitor and alert](/media/dashboard/dashboard-overview-monitor.png)

-   **ビュー Metrics** : このリンクをクリックすると、クラスターの詳細な監視情報を表示できる Grafana ダッシュボードにジャンプします。 Grafana ダッシュボードの各モニタリング メトリックの詳細については、 [メトリックの監視](/grafana-overview-dashboard.md)を参照してください。
-   **ビュー Alerts** : このリンクをクリックすると、クラスターの詳細なアラート情報を表示できる AlertManager ページにジャンプします。クラスターにアラートが存在する場合、アラートの数がリンク テキストに直接表示されます。
-   **診断の実行**: このリンクをクリックすると、より詳細なページにジャンプします。 [クラスター診断ページ](/dashboard/dashboard-diagnostics-access.md) .

> **ノート：**
>
> **[ビュー Metrics]**リンクは、Grafana ノードがデプロイされているクラスターでのみ使用できます。 <strong>ビュー Alerts</strong>リンクは、AlertManager ノードがデプロイされているクラスターでのみ使用できます。
