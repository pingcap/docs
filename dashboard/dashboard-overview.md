---
title: Overview Page
summary: TiDB概要ページには、クラスターのQPS、レイテンシー、上位SQL文、最近のスロークエリ、インスタンスステータス、監視/アラートリンクが表示されます。TiDBダッシュボードまたは左側のナビゲーションメニューからアクセスできます。QPSとレイテンシーにはPrometheusモニタリングが必要です。Top SQLとスロークエリには、SQL文とスロークエリログが有効になっている必要があります。インスタンスステータスには、インスタンスの総数と異常なインスタンスが表示されます。監視とアラートのリンクは、Grafanaダッシュボード、AlertManager、クラスター診断にリンクしています。
---

# 概要ページ {#overview-page}

このページには、次の情報を含む TiDB クラスター全体の概要が表示されます。

-   クラスター全体の 1 秒あたりのクエリ数 (QPS)。
-   クラスター全体のクエリのレイテンシー。
-   最近の期間に最も長い実行時間を累積した SQL ステートメント。
-   最近の期間の実行時間がしきい値を超えた遅いクエリ。
-   各インスタンスのノード数とステータス。
-   メッセージを監視および警告します。

## ページにアクセスする {#access-the-page}

TiDB ダッシュボードにログインすると、デフォルトで概要ページが表示されます。または、左側のナビゲーション メニューで**[概要]**をクリックしてこのページにアクセスすることもできます。

![Enter overview page](/media/dashboard/dashboard-overview-access-v650.png)

## QPS {#qps}

この領域には、最近の 1 時間におけるクラスター全体の 1 秒あたりの成功したクエリと失敗したクエリの数が表示されます。

![QPS](/media/dashboard/dashboard-overview-qps.png)

> **注記：**
>
> この機能は、Prometheus 監視コンポーネントがデプロイされているクラスターでのみ利用できます。Prometheus がデプロイされていない場合はエラーが表示されます。

## レイテンシー {#latency}

この領域には、過去 1 時間におけるクラスター全体のクエリの 99.9%、99%、90% のレイテンシーが表示されます。

![Latency](/media/dashboard/dashboard-overview-latency.png)

> **注記：**
>
> この機能は、Prometheus 監視コンポーネントがデプロイされているクラスターでのみ利用できます。Prometheus がデプロイされていない場合はエラーが表示されます。

## Top SQL文 {#top-sql-statements}

この領域には、最近の期間にクラスター全体で最も実行時間が長かった10種類のSQL文が表示されます。クエリパラメータは異なるが構造が同じSQL文は、同じSQLタイプに分類され、同じ行に表示されます。

![Top SQL](/media/dashboard/dashboard-overview-top-statements.png)

この領域に表示される情報は、より詳細な[SQL文ページ](/dashboard/dashboard-statement-list.md)と一致しています。 **「Top SQL文」**の見出しをクリックすると、完全なリストが表示されます。この表の列の詳細については、 [SQL文ページ](/dashboard/dashboard-statement-list.md)参照してください。

> **注記：**
>
> この機能は、SQL ステートメント機能が有効になっているクラスターでのみ使用できます。

## 最近の遅いクエリ {#recent-slow-queries}

デフォルトでは、この領域には、過去 30 分間のクラスター全体の最新の 10 件の低速クエリが表示されます。

![Recent slow queries](/media/dashboard/dashboard-overview-slow-query.png)

デフォルトでは、実行時間が300ミリ秒を超えるSQLクエリはスロークエリとしてカウントされ、テーブルに表示されます。このしきい値は、 [tidb_slow_log_threshold](/system-variables.md#tidb_slow_log_threshold)変数または[インスタンス.tidb_slow_log_threshold](/tidb-configuration-file.md#tidb_slow_log_threshold) TiDBパラメータを変更することで変更できます。

この領域に表示される内容は、より詳細な[遅いクエリページ](/dashboard/dashboard-slow-query.md)内容と一致しています。 **「最近のスロークエリ」**というタイトルをクリックすると、完全なリストが表示されます。この表の列の詳細については、 [遅いクエリページ](/dashboard/dashboard-slow-query.md)をご覧ください。

> **注記：**
>
> この機能は、スロークエリログが有効になっているクラスターでのみ利用できます。TiUPを使用してデプロイされたクラスターでは、スロークエリログはデフォルトで有効になっています。

## インスタンス {#instances}

この領域には、クラスター全体の TiDB、TiKV、PD、およびTiFlashのインスタンスの総数と異常なインスタンス数がまとめられます。

![Instances](/media/dashboard/dashboard-overview-instances.png)

上の画像のステータスは次のように説明されます。

-   稼働中: インスタンスは正常に実行されています (オフラインstorageインスタンスを含む)。
-   ダウン: ネットワーク切断やプロセスクラッシュなど、インスタンスが異常な状態で動作しています。

**インスタンスの**タイトルをクリックすると、各インスタンスの詳細な実行ステータスを示す[クラスタ情報ページ](/dashboard/dashboard-cluster-info.md)が表示されます。

## 監視と警告 {#monitor-and-alert}

この領域には、詳細なモニターとアラートを表示するためのリンクがあります。

![Monitor and alert](/media/dashboard/dashboard-overview-monitor.png)

-   **メトリクスのビュー**：このリンクをクリックすると、Grafanaダッシュボードに移動し、クラスターの詳細な監視情報を確認できます。Grafanaダッシュボードの各監視メトリクスの詳細については、 [監視メトリック](/grafana-overview-dashboard.md)参照してください。
-   **アラートのビュー**：このリンクをクリックすると、AlertManagerページに移動し、クラスターの詳細なアラート情報を確認できます。クラスターにアラートが存在する場合、アラートの数がリンクテキストに直接表示されます。
-   **診断の実行**: このリンクをクリックすると、より詳細な[クラスター診断ページ](/dashboard/dashboard-diagnostics-access.md)にジャンプします。

> **注記：**
>
> **「メトリックのビュー**」リンクは、Grafanaノードがデプロイされているクラスターでのみ使用できます。 **「アラートのビュー」**リンクは、AlertManagerノードがデプロイされているクラスターでのみ使用できます。
