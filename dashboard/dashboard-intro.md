---
title: TiDB Dashboard Introduction
summary: Introduce TiDB Dashboard.
---

# TiDB ダッシュボードの概要 {#tidb-dashboard-introduction}

TiDB ダッシュボードは、TiDB クラスターを監視、診断、管理するための Web UI であり、v4.0 以降で利用可能です。これは PDコンポーネントに組み込まれており、独立した展開は必要ありません。

> **注記：**
>
> TiDB v6.5.0 (以降) およびTiDB Operator v1.4.0 (以降) は、TiDB ダッシュボードを Kubernetes 上の独立したポッドとしてデプロイすることをサポートしています。詳細は[TiDB Operatorで TiDB ダッシュボードを独立してデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)を参照してください。

![TiDB Dashboard interface](/media/dashboard/dashboard-intro.gif)

TiDB ダッシュボードは[GitHub](https://github.com/pingcap-incubator/tidb-dashboard)でオープンソース化されています。

このドキュメントでは、TiDB ダッシュボードの主な機能を紹介します。次のセクションのリンクをクリックすると、詳細を確認できます。

## TiDB クラスターの全体的な実行ステータスを表示します。 {#show-the-overall-running-status-of-the-tidb-cluster}

TiDB ダッシュボードを使用すると、TiDB クラスターの 1 秒あたりのクエリ数 (QPS)、実行時間、最も多くのリソースを消費する SQL ステートメントの種類、およびその他の概要情報を知ることができます。

詳細については[TiDB ダッシュボードの概要](/dashboard/dashboard-overview.md)を参照してください。

## コンポーネントとホストの実行ステータスを表示する {#show-the-running-status-of-components-and-hosts}

TiDB ダッシュボードを使用すると、クラスター全体の TiDB、TiKV、PD、 TiFlashコンポーネントの実行ステータスと、これらのコンポーネントが配置されているホストの実行ステータスを表示できます。

詳細については[TiDB ダッシュボードのクラスタ情報ページ](/dashboard/dashboard-cluster-info.md)を参照してください。

## 読み取りおよび書き込みトラフィックの分布と傾向を表示する {#show-distribution-and-trends-of-read-and-write-traffic}

TiDB ダッシュボードの Key Visualizer 機能は、クラスター全体の読み取りおよび書き込みトラフィックの時間の経過に伴う変化をヒートマップの形式で視覚的に表示します。この機能を使用すると、アプリケーション モードの変更をタイムリーに検出したり、パフォーマンスが不均一なホットスポットの問題を特定したりできます。

詳細については[キービジュアライザーページ](/dashboard/dashboard-key-visualizer.md)を参照してください。

## すべてのSQL文の実行情報を一覧表示します。 {#show-a-list-of-execution-information-of-all-sql-statements}

すべての SQL ステートメントの実行情報は、「SQL ステートメント」ページにリストされます。このページを使用すると、すべての段階での実行時間と合計実行数を確認できます。これは、リソースを最も消費する SQL クエリを分析して特定し、クラスター全体のパフォーマンスを向上させるのに役立ちます。

詳細については[TiDB ダッシュボードの SQL ステートメント ページ](/dashboard/dashboard-statement-list.md)を参照してください。

## 遅いクエリの詳細な実行情報を確認する {#learn-the-detailed-execution-information-of-slow-queries}

TiDB ダッシュボードのスロー クエリ ページには、SQL テキストと実行情報を含む、実行に時間がかかるすべての SQL ステートメントのリストが表示されます。このページは、クエリの遅さやパフォーマンスのジッターの原因を特定するのに役立ちます。

詳細については[遅いクエリページ](/dashboard/dashboard-slow-query.md)を参照してください。

## 一般的なクラスターの問題を診断し、レポートを生成する {#diagnose-common-cluster-problems-and-generate-reports}

TiDB ダッシュボードの診断機能は、一般的なリスク (一貫性のない構成など) や問題がクラスター内に存在するかどうかを自動的に判断し、レポートを生成して操作の提案を提供したり、可能性を分析できるようにさまざまな時間範囲で各クラスターのメトリクスのステータスを比較したりします。問題。

詳細については[TiDB ダッシュボードのクラスタ診断ページ](/dashboard/dashboard-diagnostics-access.md)を参照してください。

## すべてのコンポーネントのログをクエリする {#query-logs-of-all-components}

TiDB ダッシュボードの「ログの検索」ページでは、クラスター内で実行中のすべてのインスタンスのログをキーワード、時間範囲、その他の条件ですばやく検索し、これらのログをパッケージ化して、ローカル マシンにダウンロードできます。

詳細については[ログの検索ページ](/dashboard/dashboard-log-search.md)を参照してください。

## リソース制御のためのクラスター容量の見積もり {#estimate-cluster-capacity-for-resource-control}

[リソース制御](/tidb-resource-control.md)機能を使用してリソース分離を実装するには、クラスター管理者はリソース グループを作成し、各グループのクォータを設定できます。

リソースを計画する前に、クラスターの全体的な容量を把握する必要があります。詳細については、 [リソースマネージャーページ](/dashboard/dashboard-resource-manager.md)を参照してください。

## インスタンスごとにプロファイリング データを収集する {#collect-profiling-data-for-each-instance}

これは高度なデバッグ機能であり、サードパーティのツールを使用せずに、各インスタンスをオンラインでプロファイリングし、プロファイリング データ収集期間中にインスタンスが実行したさまざまな内部操作とこの期間の操作実行時間の割合を分析できます。

詳細については[プロファイルインスタンスページ](/dashboard/dashboard-profiling.md)を参照してください。
