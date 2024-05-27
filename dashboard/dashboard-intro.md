---
title: TiDB Dashboard Introduction
summary: TiDB ダッシュボードは、TiDB クラスターを監視、診断、管理するための Web UI です。全体的な実行ステータス、コンポーネントとホストのステータス、トラフィックの分散、SQL ステートメントの実行情報、遅いクエリ、クラスター診断、ログ検索、リソース制御、プロファイリング データ収集が表示されます。
---

# TiDBダッシュボードの紹介 {#tidb-dashboard-introduction}

TiDB ダッシュボードは、TiDB クラスターを監視、診断、管理するための Web UI であり、v4.0 以降で利用できます。PDコンポーネントに組み込まれているため、独立したデプロイメントは必要ありません。

> **注記：**
>
> TiDB v6.5.0（以降）およびTiDB Operator v1.4.0（以降）では、Kubernetes上の独立したポッドとしてTiDB Dashboardをデプロイすることがサポートされています。詳細については、 [TiDB ダッシュボードをTiDB Operatorに独立してデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)参照してください。

![TiDB Dashboard interface](/media/dashboard/dashboard-intro.gif)

TiDB ダッシュボードは[GitHub](https://github.com/pingcap-incubator/tidb-dashboard)でオープンソース化されています。

このドキュメントでは、TiDB ダッシュボードの主な機能を紹介します。詳細については、次のセクションのリンクをクリックしてください。

## TiDBクラスタの全体的な実行ステータスを表示する {#show-the-overall-running-status-of-the-tidb-cluster}

TiDB ダッシュボードを使用すると、TiDB クラスターの 1 秒あたりのクエリ数 (QPS)、実行時間、最も多くのリソースを消費する SQL ステートメントの種類、その他の概要情報を確認できます。

詳細は[TiDBダッシュボードの概要](/dashboard/dashboard-overview.md)参照。

## コンポーネントとホストの実行ステータスを表示する {#show-the-running-status-of-components-and-hosts}

TiDB ダッシュボードを使用すると、クラスター全体の TiDB、TiKV、PD、 TiFlashコンポーネントの実行ステータスと、これらのコンポーネントが配置されているホストの実行ステータスを表示できます。

詳細は[TiDBダッシュボードクラスタ情報ページ](/dashboard/dashboard-cluster-info.md)参照。

## 読み取りおよび書き込みトラフィックの分布と傾向を表示する {#show-distribution-and-trends-of-read-and-write-traffic}

TiDB ダッシュボードの Key Visualizer 機能は、クラスター全体の読み取りおよび書き込みトラフィックの経時的な変化をヒートマップの形式で視覚的に表示します。この機能を使用すると、アプリケーション モードの変化をタイムリーに検出したり、パフォーマンスが不均一なホットスポットの問題を特定したりできます。

詳細は[キービジュアライザーページ](/dashboard/dashboard-key-visualizer.md)参照。

## すべてのSQL文の実行情報のリストを表示します {#show-a-list-of-execution-information-of-all-sql-statements}

すべての SQL ステートメントの実行情報は、SQL ステートメント ページに一覧表示されます。このページを使用すると、すべての段階での実行時間と合計実行回数を知ることができ、最も多くのリソースを消費する SQL クエリを分析して特定し、クラスター全体のパフォーマンスを向上させるのに役立ちます。

詳細は[TiDBダッシュボードのSQLステートメントページ](/dashboard/dashboard-statement-list.md)参照。

## 遅いクエリの詳細な実行情報を知る {#learn-the-detailed-execution-information-of-slow-queries}

TiDB ダッシュボードの「低速クエリ」ページには、SQL テキストや実行情報など、実行に時間のかかるすべての SQL ステートメントのリストが表示されます。このページは、低速クエリやパフォーマンスのジッターの原因を特定するのに役立ちます。

詳細は[遅いクエリページ](/dashboard/dashboard-slow-query.md)参照。

## 一般的なクラスターの問題を診断し、レポートを生成する {#diagnose-common-cluster-problems-and-generate-reports}

TiDB ダッシュボードの診断機能は、クラスター内に一般的なリスク (不一致な構成など) や問題が存在するかどうかを自動的に判断し、レポートを生成して操作の提案を行ったり、さまざまな時間範囲で各クラスター メトリックのステータスを比較して、起こりうる問題を分析したりします。

詳細は[TiDB ダッシュボードクラスタ診​​断ページ](/dashboard/dashboard-diagnostics-access.md)参照。

## すべてのコンポーネントのログを照会する {#query-logs-of-all-components}

TiDB ダッシュボードの [ログの検索] ページでは、クラスター内で実行中のすべてのインスタンスのログをキーワード、時間範囲、その他の条件ですばやく検索し、これらのログをパッケージ化してローカル マシンにダウンロードできます。

詳細は[ログ検索ページ](/dashboard/dashboard-log-search.md)参照。

## リソース制御のためのクラスター容量の見積もり {#estimate-cluster-capacity-for-resource-control}

[リソース管理](/tidb-resource-control.md)機能を使用してリソース分離を実装するには、クラスター管理者がリソース グループを作成し、各グループのクォータを設定できます。

リソース計画を立てる前に、クラスターの全体的な容量を把握しておく必要があります。詳細については、 [リソース マネージャー ページ](/dashboard/dashboard-resource-manager.md)参照してください。

## 各インスタンスのプロファイリングデータを収集する {#collect-profiling-data-for-each-instance}

これは、各インスタンスをオンラインでプロファイリングし、プロファイリング データ収集期間中にインスタンスが実行したさまざまな内部操作と、この期間中の操作実行時間の割合をサードパーティ ツールを使用せずに分析できる高度なデバッグ機能です。

詳細は[プロファイルインスタンスページ](/dashboard/dashboard-profiling.md)参照。
