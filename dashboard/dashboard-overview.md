---
title: Overview Page
summary: TiDB 概要ページには、クラスターの QPS、レイテンシー、上位の SQL ステートメント、最近の低速クエリ、インスタンスのステータス、および監視/アラート リンクが表示されます。このページには、TiDB ダッシュボードまたは左側のナビゲーション メニューからアクセスします。QPS とレイテンシーには、Prometheus 監視が必要です。Top SQLと低速クエリには、SQL ステートメントと低速クエリ ログを有効にする必要があります。インスタンスのステータスには、合計インスタンスと異常なインスタンスが表示されます。監視リンクとアラート リンクは、Grafana ダッシュボード、AlertManager、およびクラスター診断につながります。
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

## 品質保証 {#qps}

この領域には、過去 1 時間のクラスター全体の 1 秒あたりの成功したクエリと失敗したクエリの数が表示されます。

![QPS](/media/dashboard/dashboard-overview-qps.png)

> **注記：**
>
> この機能は、Prometheus 監視コンポーネントがデプロイされているクラスターでのみ使用できます。Prometheus がデプロイされていない場合は、エラーが表示されます。

## レイテンシー {#latency}

この領域には、過去 1 時間におけるクラスター全体のクエリの 99.9%、99%、90% のレイテンシーが表示されます。

![Latency](/media/dashboard/dashboard-overview-latency.png)

> **注記：**
>
> この機能は、Prometheus 監視コンポーネントがデプロイされているクラスターでのみ使用できます。Prometheus がデプロイされていない場合は、エラーが表示されます。

## Top SQL文 {#top-sql-statements}

この領域には、最近の期間にクラスター全体で最も長い実行時間を蓄積した 10 種類の SQL ステートメントが表示されます。クエリ パラメータは異なるが同じ構造の SQL ステートメントは、同じ SQL タイプに分類され、同じ行に表示されます。

![Top SQL](/media/dashboard/dashboard-overview-top-statements.png)

この領域に表示される情報は、より詳細な[SQL ステートメント ページ](/dashboard/dashboard-statement-list.md)と一致しています。完全なリストを表示するには、 **「Top SQLステートメント」**見出しをクリックします。この表の列の詳細については、 [SQL ステートメント ページ](/dashboard/dashboard-statement-list.md)を参照してください。

> **注記：**
>
> この機能は、SQL ステートメント機能が有効になっているクラスターでのみ使用できます。

## 最近の遅いクエリ {#recent-slow-queries}

デフォルトでは、この領域には、過去 30 分間のクラスター全体の最新の 10 件の遅いクエリが表示されます。

![Recent slow queries](/media/dashboard/dashboard-overview-slow-query.png)

デフォルトでは、300 ミリ秒を超えて実行される SQL クエリは遅いクエリとしてカウントされ、テーブルに表示されます。このしきい値は、 [tidb_slow_log_threshold](/system-variables.md#tidb_slow_log_threshold)変数または[インスタンス.tidb_slow_log_threshold](/tidb-configuration-file.md#tidb_slow_log_threshold) TiDB パラメータを変更することで変更できます。

この領域に表示される内容は、より詳細な[遅いクエリページ](/dashboard/dashboard-slow-query.md)と一致しています。 **「最近の低速クエリ」**のタイトルをクリックすると、完全なリストを表示できます。この表の列の詳細については、この[遅いクエリページ](/dashboard/dashboard-slow-query.md)を参照してください。

> **注記：**
>
> この機能は、スロー クエリ ログが有効になっているクラスターでのみ使用できます。デフォルトでは、スロー クエリ ログはTiUPを使用してデプロイされたクラスターで有効になっています。

## インスタンス {#instances}

この領域には、クラスター全体の TiDB、TiKV、PD、およびTiFlashのインスタンスの合計数と異常なインスタンス数がまとめられています。

![Instances](/media/dashboard/dashboard-overview-instances.png)

上の画像のステータスは次のように説明されます。

-   稼働中: インスタンスは正常に実行されています (オフラインstorageインスタンスを含む)。
-   ダウン: ネットワーク切断やプロセスクラッシュなど、インスタンスが異常な状態で動作しています。

**インスタンス**タイトルをクリックすると、各インスタンスの詳細な実行ステータスを示す[クラスタ情報ページ](/dashboard/dashboard-cluster-info.md)が表示されます。

## 監視と警告 {#monitor-and-alert}

この領域には、詳細なモニターとアラートを表示するためのリンクがあります。

![Monitor and alert](/media/dashboard/dashboard-overview-monitor.png)

-   **メトリックのビュー**: このリンクをクリックすると、クラスターの詳細な監視情報を表示できる Grafana ダッシュボードに移動します。Grafana ダッシュボードの各監視メトリックの詳細については、 [監視メトリクス](/grafana-overview-dashboard.md)を参照してください。
-   **アラートのビュー**: このリンクをクリックすると、クラスターの詳細なアラート情報を表示できる AlertManager ページに移動します。クラスターにアラートが存在する場合、アラートの数がリンク テキストに直接表示されます。
-   **診断の実行**: このリンクをクリックすると、より詳細な[クラスター診断ページ](/dashboard/dashboard-diagnostics-access.md)にジャンプします。

> **注記：**
>
> 「**メトリックのビュー」**リンクは、Grafana ノードがデプロイされているクラスターでのみ使用できます。「**アラートのビュー」**リンクは、AlertManager ノードがデプロイされているクラスターでのみ使用できます。
