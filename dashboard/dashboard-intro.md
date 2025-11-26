---
title: TiDB Dashboard Introduction
summary: TiDBダッシュボードは、TiDBクラスタの監視、診断、管理のためのWeb UIです。クラスタ全体の稼働状況、コンポーネントとホストのステータス、トラフィック分布、SQL文の実行情報、スロークエリ、クラスタ診​​断、ログ検索、リソース制御、プロファイリングデータ収集などを表示します。
---

# TiDBダッシュボードの紹介 {#tidb-dashboard-introduction}

TiDBダッシュボードは、TiDBクラスターの監視、診断、管理のためのWeb UIで、バージョン4.0以降で利用可能です。PDコンポーネントに組み込まれているため、別途導入する必要はありません。

> **注記：**
>
> TiDB v6.5.0以降およびTiDB Operator v1.4.0以降では、TiDB DashboardをKubernetes上の独立したPodとしてデプロイできます。詳細については、 [TiDB ダッシュボードをTiDB Operatorで独立してデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/v1.6/get-started#deploy-tidb-dashboard-independently)参照してください。

![TiDB Dashboard interface](/media/dashboard/dashboard-intro.gif)

TiDB ダッシュボードは[GitHub](https://github.com/pingcap-incubator/tidb-dashboard)でオープンソース化されています。

このドキュメントでは、TiDBダッシュボードの主な機能を紹介します。詳細については、以下のセクションのリンクをクリックしてください。

## TiDBクラスタの全体的な実行ステータスを表示します {#show-the-overall-running-status-of-the-tidb-cluster}

TiDB ダッシュボードを使用すると、TiDB クラスターの 1 秒あたりのクエリ数 (QPS)、実行時間、最も多くのリソースを消費する SQL ステートメントの種類などの概要情報を確認できます。

詳細は[TiDBダッシュボードの概要](/dashboard/dashboard-overview.md)参照。

## コンポーネントとホストの実行ステータスを表示する {#show-the-running-status-of-components-and-hosts}

TiDB ダッシュボードを使用すると、クラスター全体の TiDB、TiKV、PD、 TiFlashコンポーネントの実行状態と、これらのコンポーネントが配置されているホストの実行状態を表示できます。

詳細は[TiDBダッシュボードのクラスタ情報ページ](/dashboard/dashboard-cluster-info.md)参照。

## 読み取りおよび書き込みトラフィックの分布と傾向を表示します {#show-distribution-and-trends-of-read-and-write-traffic}

TiDBダッシュボードのKey Visualizer機能は、クラスター全体の読み取り/書き込みトラフィックの経時的な変化をヒートマップ形式で視覚的に表示します。この機能を利用することで、アプリケーションモードの変化をタイムリーに把握したり、パフォーマンスの不均一性を示すホットスポットの問題を特定したりすることができます。

詳細は[キービジュアライザーページ](/dashboard/dashboard-key-visualizer.md)参照。

## すべてのSQL文の実行情報のリストを表示します {#show-a-list-of-execution-information-of-all-sql-statements}

すべてのSQL文の実行情報は、「SQL文」ページに表示されます。このページでは、すべてのステージにおける実行時間と合計実行回数を確認できます。これにより、最もリソースを消費しているSQLクエリを分析して特定し、クラスター全体のパフォーマンスを向上させることができます。

詳細は[TiDBダッシュボードのSQLステートメントページ](/dashboard/dashboard-statement-list.md)参照。

## 遅いクエリの詳細な実行情報を知る {#learn-the-detailed-execution-information-of-slow-queries}

TiDBダッシュボードの「スロークエリ」ページには、実行に時間のかかるすべてのSQL文のリスト（SQLテキストと実行情報を含む）が表示されます。このページは、スロークエリやパフォーマンスジッターの原因を特定するのに役立ちます。

詳細は[遅いクエリページ](/dashboard/dashboard-slow-query.md)参照。

## 一般的なクラスターの問題を診断し、レポートを生成する {#diagnose-common-cluster-problems-and-generate-reports}

TiDB ダッシュボードの診断機能は、クラスター内に一般的なリスク (不一致な構成など) や問題が存在するかどうかを自動的に判断し、レポートを生成して操作の提案を行ったり、異なる時間範囲で各クラスター メトリックの状態を比較して、起こりうる問題を分析したりします。

詳細は[TiDBダッシュボードのクラスタ診​​断ページ](/dashboard/dashboard-diagnostics-access.md)参照。

## すべてのコンポーネントのクエリログ {#query-logs-of-all-components}

TiDB ダッシュボードの [ログの検索] ページでは、クラスター内で実行中のすべてのインスタンスのログをキーワード、時間範囲、その他の条件ですばやく検索し、これらのログをパッケージ化してローカル マシンにダウンロードできます。

詳細は[検索ログページ](/dashboard/dashboard-log-search.md)参照。

## リソース制御のためのクラスター容量の見積もり {#estimate-cluster-capacity-for-resource-control}

[リソース管理](/tidb-resource-control-ru-groups.md)機能を使用してリソース分離を実装するには、クラスター管理者がリソース グループを作成し、各グループにクォータを設定できます。

リソース計画を立てる前に、クラスター全体の容量を把握しておく必要があります。詳細については、 [リソースマネージャーページ](/dashboard/dashboard-resource-manager.md)参照してください。

## 各インスタンスのプロファイリングデータを収集する {#collect-profiling-data-for-each-instance}

これは、サードパーティのツールを使用せずに、各インスタンスをオンラインでプロファイリングし、プロファイリング データ収集期間中にインスタンスが実行したさまざまな内部操作と、この期間中の操作実行時間の割合を分析できる高度なデバッグ機能です。

詳細は[プロファイルインスタンスページ](/dashboard/dashboard-profiling.md)参照。
