---
title: TiDB Dashboard Introduction
summary: Introduce TiDB Dashboard.
---

# TiDB ダッシュボードの紹介 {#tidb-dashboard-introduction}

TiDB ダッシュボードは、TiDB クラスターを監視、診断、および管理するための Web UI であり、v4.0 以降で使用できます。これは PDコンポーネントに組み込まれており、個別に展開する必要はありません。

> **ノート：**
>
> TiDB v6.5.0 (およびそれ以降) およびTiDB Operator v1.4.0 (およびそれ以降) は、TiDB ダッシュボードを Kubernetes 上の独立した Pod としてデプロイすることをサポートします。詳細については、 [TiDB Operatorで TiDB ダッシュボードを個別にデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)を参照してください。

![TiDB Dashboard interface](/media/dashboard/dashboard-intro.gif)

TiDB ダッシュボードは[GitHub](https://github.com/pingcap-incubator/tidb-dashboard)でオープンソース化されています。

このドキュメントでは、TiDB ダッシュボードの主な機能を紹介します。詳細については、次のセクションのリンクをクリックしてください。

## TiDB クラスターの全体的な実行ステータスを表示します {#show-the-overall-running-status-of-the-tidb-cluster}

TiDB ダッシュボードを使用して、TiDB クラスターの 1 秒あたりのクエリ数 (QPS)、実行時間、最も多くのリソースを消費する SQL ステートメントの種類、およびその他の概要情報を確認できます。

詳細は[TiDB ダッシュボードの概要](/dashboard/dashboard-overview.md)を参照してください。

## コンポーネントとホストの実行ステータスを表示する {#show-the-running-status-of-components-and-hosts}

TiDB ダッシュボードを使用して、クラスター全体の TiDB、TiKV、PD、 TiFlashコンポーネントの実行ステータスと、これらのコンポーネントが配置されているホストの実行ステータスを表示できます。

詳細は[TiDB ダッシュボードクラスタ情報ページ](/dashboard/dashboard-cluster-info.md)を参照してください。

## 読み取りおよび書き込みトラフィックの分布と傾向を表示する {#show-distribution-and-trends-of-read-and-write-traffic}

TiDB ダッシュボードのキー ビジュアライザー機能は、クラスター全体の読み取りおよび書き込みトラフィックの経時変化をヒートマップの形式で視覚的に示します。この機能を使用して、アプリケーション モードの変更をタイムリーに検出したり、パフォーマンスが不均一なホットスポットの問題を特定したりできます。

詳細は[キー ビジュアライザー ページ](/dashboard/dashboard-key-visualizer.md)を参照してください。

## すべてのSQL文の実行情報の一覧を表示 {#show-a-list-of-execution-information-of-all-sql-statements}

すべての SQL ステートメントの実行情報は、[SQL ステートメント] ページに一覧表示されます。このページを使用して、すべての段階での実行時間と合計実行数を知ることができます。これは、最も多くのリソースを消費する SQL クエリを分析して特定し、クラスター全体のパフォーマンスを向上させるのに役立ちます。

詳細は[TiDB ダッシュボードの SQL ステートメント ページ](/dashboard/dashboard-statement-list.md)を参照してください。

## スロークエリの詳細な実行情報を学ぶ {#learn-the-detailed-execution-information-of-slow-queries}

TiDB ダッシュボードのスロー クエリ ページには、SQL テキストや実行情報など、実行に時間がかかるすべての SQL ステートメントのリストが表示されます。このページは、遅いクエリやパフォーマンスのジッターの原因を特定するのに役立ちます。

詳細は[スロークエリページ](/dashboard/dashboard-slow-query.md)を参照してください。

## 一般的なクラスターの問題を診断し、レポートを生成する {#diagnose-common-cluster-problems-and-generate-reports}

TiDB ダッシュボードの診断機能は、いくつかの一般的なリスク (不整合な構成など) または問題がクラスターに存在するかどうかを自動的に判断し、レポートを生成して操作の提案を提供するか、さまざまな時間範囲で各クラスター メトリックのステータスを比較して、可能な分析を行います。問題。

詳細は[TiDB ダッシュボードクラスタ診断ページ](/dashboard/dashboard-diagnostics-access.md)を参照してください。

## すべてのコンポーネントのクエリ ログ {#query-logs-of-all-components}

TiDB ダッシュボードの [ログの検索] ページでは、クラスター内で実行中のすべてのインスタンスのログをキーワード、時間範囲、およびその他の条件ですばやく検索し、これらのログをパッケージ化して、ローカル マシンにダウンロードできます。

詳細は[検索ログ ページ](/dashboard/dashboard-log-search.md)を参照してください。

## 各インスタンスのプロファイリング データを収集する {#collect-profiling-data-for-each-instance}

これは高度なデバッグ機能で、各インスタンスをオンラインでプロファイリングし、プロファイリング データ収集期間中にインスタンスが実行したさまざまな内部操作と、サードパーティ ツールを使用せずにこの期間中の操作実行時間の割合を分析できます。

詳細は[プロファイル インスタンス ページ](/dashboard/dashboard-profiling.md)を参照してください。
