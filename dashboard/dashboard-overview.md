---
title: Overview Page
summary: Learn the overview page of TiDB Dashboard.
---

# 概要ページ {#overview-page}

このページには、次の情報を含む TiDB クラスター全体の概要が表示されます。

-   クラスター全体の 1 秒あたりのクエリ数 (QPS)。
-   クラスター全体のクエリレイテンシー。
-   最近の期間で累計実行時間が最長となった SQL ステートメント。
-   最近の実行時間がしきい値を超えた遅いクエリ。
-   各インスタンスのノード数とステータス。
-   メッセージを監視し、警告します。

## ページにアクセスする {#access-the-page}

TiDB ダッシュボードにログインすると、デフォルトで概要ページが表示されます。または、左側のナビゲーション メニューで**[概要]**をクリックしてこのページに移動することもできます。

![Enter overview page](/media/dashboard/dashboard-overview-access-v650.png)

## QPS {#qps}

この領域には、最近 1 時間のクラスター全体の 1 秒あたりの成功したクエリと失敗したクエリの数が表示されます。

![QPS](/media/dashboard/dashboard-overview-qps.png)

> **注記：**
>
> この機能は、Prometheus 監視コンポーネントがデプロイされているクラスターでのみ使用できます。 Prometheus がデプロイされていない場合は、エラーが表示されます。

## レイテンシー {#latency}

この領域には、最近 1 時間におけるクラスター全体のクエリの 99.9%、99%、および 90% のレイテンシーが表示されます。

![Latency](/media/dashboard/dashboard-overview-latency.png)

> **注記：**
>
> この機能は、Prometheus 監視コンポーネントがデプロイされているクラスターでのみ使用できます。 Prometheus がデプロイされていない場合は、エラーが表示されます。

## Top SQLステートメント {#top-sql-statements}

この領域には、最近の期間にクラスター全体で累積最長実行時間を記録した 10 種類の SQL ステートメントが表示されます。クエリ パラメータは異なるが構造が同じ SQL ステートメントは、同じ SQL タイプに分類され、同じ行に表示されます。

![Top SQL](/media/dashboard/dashboard-overview-top-statements.png)

この領域に表示される情報は、より詳細な[SQL ステートメントページ](/dashboard/dashboard-statement-list.md)と一致しています。 **「Top SQLステートメント」**見出しをクリックすると、完全なリストが表示されます。この表の列の詳細については、 [SQL ステートメントページ](/dashboard/dashboard-statement-list.md)を参照してください。

> **注記：**
>
> この機能は、SQL ステートメント機能が有効になっているクラスターでのみ使用できます。

## 最近の遅いクエリ {#recent-slow-queries}

デフォルトでは、この領域には、最近 30 分間のクラスター全体の最新の 10 件の遅いクエリが表示されます。

![Recent slow queries](/media/dashboard/dashboard-overview-slow-query.png)

デフォルトでは、300 ミリ秒を超えて実行される SQL クエリは低速クエリとしてカウントされ、テーブルに表示されます。このしきい値は、 [tidb_slow_log_threshold](/system-variables.md#tidb_slow_log_threshold)変数または[インスタンス.tidb_slow_log_threshold](/tidb-configuration-file.md#tidb_slow_log_threshold) TiDB パラメータを変更することで変更できます。

この領域に表示される内容は、より詳細な[遅いクエリページ](/dashboard/dashboard-slow-query.md)と一致しています。 **「最近の遅いクエリ」の**タイトルをクリックすると、完全なリストが表示されます。この表の列の詳細については、この[遅いクエリページ](/dashboard/dashboard-slow-query.md)を参照してください。

> **注記：**
>
> この機能は、スロー クエリ ログが有効になっているクラスターでのみ使用できます。デフォルトでは、 TiUP を使用してデプロイされたクラスターでスロー クエリ ログが有効になっています。

## インスタンス {#instances}

この領域には、クラスター全体の TiDB、TiKV、PD、およびTiFlashのインスタンスと異常なインスタンスの合計数が要約されます。

![Instances](/media/dashboard/dashboard-overview-instances.png)

上の図のステータスは次のように説明されています。

-   Up: インスタンスは正常に実行されています (オフラインstorageインスタンスを含む)。
-   Down: ネットワークの切断やプロセスのクラッシュなど、インスタンスが異常に実行されています。

**インスタンスの**タイトルをクリックして[クラスタ情報ページ](/dashboard/dashboard-cluster-info.md)入力すると、各インスタンスの詳細な実行ステータスが表示されます。

## 監視と警告 {#monitor-and-alert}

この領域には、詳細な監視とアラートを表示するためのリンクが表示されます。

![Monitor and alert](/media/dashboard/dashboard-overview-monitor.png)

-   **ビュー Metrics** : このリンクをクリックすると、Grafana ダッシュボードにジャンプし、クラスターの詳細な監視情報を表示できます。 Grafana ダッシュボードの各監視メトリックの詳細については、 [モニタリングメトリクス](/grafana-overview-dashboard.md)を参照してください。
-   **アラートのビュー**: このリンクをクリックすると、クラスターの詳細なアラート情報を表示できる AlertManager ページにジャンプします。クラスター内にアラートが存在する場合、アラートの数がリンク テキストに直接表示されます。
-   **診断の実行**: このリンクをクリックすると、より詳細な[クラスター診断ページ](/dashboard/dashboard-diagnostics-access.md)にジャンプします。

> **注記：**
>
> **「ビュー Metrics」**リンクは、Grafana ノードがデプロイされているクラスターでのみ使用できます。 **「アラートのビュー」**リンクは、AlertManager ノードがデプロイされているクラスターでのみ使用できます。
