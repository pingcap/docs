---
title: TiDB Dashboard Introduction
summary: Introduce TiDB Dashboard.
---

# TiDBダッシュボードの紹介 {#tidb-dashboard-introduction}

TiDBダッシュボードは、TiDBクラスタを監視、診断、および管理するためのWeb UIであり、v4.0以降で使用できます。これはPDコンポーネントに組み込まれており、独立した展開は必要ありません。

![TiDB Dashboard interface](/media/dashboard/dashboard-intro.gif)

TiDBダッシュボードは[GitHub](https://github.com/pingcap-incubator/tidb-dashboard)でオープンソースです。

このドキュメントでは、TiDBダッシュボードの主な機能を紹介します。詳細については、次のセクションのリンクをクリックしてください。

## TiDBクラスタの全体的な実行ステータスを表示する {#show-the-overall-running-status-of-the-tidb-cluster}

TiDBダッシュボードを使用して、TiDBクラスターの1秒あたりのクエリ数（QPS）、実行時間、最も多くのリソースを消費するSQLステートメントのタイプ、およびその他の概要情報を学習できます。

詳細については、 [TiDBダッシュボードの概要](/dashboard/dashboard-overview.md)を参照してください。

## コンポーネントとホストの実行ステータスを表示する {#show-the-running-status-of-components-and-hosts}

TiDBダッシュボードを使用して、クラスタ全体でのTiDB、TiKV、PD、TiFlashコンポーネントの実行ステータス、およびこれらのコンポーネントが配置されているホストの実行ステータスを表示できます。

詳細については、 [TiDBダッシュボードクラスター情報ページ](/dashboard/dashboard-cluster-info.md)を参照してください。

## 読み取りおよび書き込みトラフィックの分布と傾向を表示する {#show-distribution-and-trends-of-read-and-write-traffic}

TiDBダッシュボードのキービジュアライザー機能は、クラスタ全体の読み取りおよび書き込みトラフィックの経時変化をヒートマップの形式で視覚的に表示します。この機能を使用して、アプリケーションモードの変更をタイムリーに検出したり、パフォーマンスが不均一なホットスポットの問題を特定したりできます。

詳細については、 [キービジュアライザーページ](/dashboard/dashboard-key-visualizer.md)を参照してください。

## すべてのSQLステートメントの実行情報のリストを表示します {#show-a-list-of-execution-information-of-all-sql-statements}

すべてのSQLステートメントの実行情報は、「SQLステートメント」ページにリストされています。このページを使用して、すべての段階での実行時間と合計実行を学習できます。これは、最も多くのリソースを消費するSQLクエリを分析および特定し、クラスタ全体のパフォーマンスを向上させるのに役立ちます。

詳細については、 [TiDBダッシュボードのSQLステートメントページ](/dashboard/dashboard-statement-list.md)を参照してください。

## 遅いクエリの詳細な実行情報を学ぶ {#learn-the-detailed-execution-information-of-slow-queries}

TiDBダッシュボードの[低速クエリ]ページには、SQLテキストや実行情報など、実行に時間がかかるすべてのSQLステートメントのリストが表示されます。このページは、クエリの速度低下やパフォーマンスのジッターの原因を特定するのに役立ちます。

詳細については、 [遅いクエリページ](/dashboard/dashboard-slow-query.md)を参照してください。

## 一般的なクラスタの問題を診断し、レポートを生成します {#diagnose-common-cluster-problems-and-generate-reports}

TiDBダッシュボードの診断機能は、いくつかの一般的なリスク（一貫性のない構成など）または問題がクラスタに存在するかどうかを自動的に判断し、レポートを生成して操作の提案を提供するか、さまざまな時間範囲で各クラスタメトリックのステータスを比較して可能な分析を行います問題。

詳細については、 [TiDBダッシュボードクラスター診断ページ](/dashboard/dashboard-diagnostics-access.md)を参照してください。

## すべてのコンポーネントのクエリログ {#query-logs-of-all-components}

TiDBダッシュボードの[ログの検索]ページでは、クラスタで実行中のすべてのインスタンスのログをキーワード、時間範囲、およびその他の条件ですばやく検索し、これらのログをパッケージ化して、ローカルマシンにダウンロードできます。

詳細については、 [検索ログページ](/dashboard/dashboard-log-search.md)を参照してください。

## 各インスタンスのプロファイリングデータを収集します {#collect-profiling-data-for-each-instance}

これは高度なデバッグ機能であり、サードパーティのツールを使用せずに、各インスタンスをオンラインでプロファイリングし、プロファイリングデータ収集期間中にインスタンスが実行したさまざまな内部操作とこの期間の操作実行時間の割合を分析できます。

詳細については、 [プロファイルインスタンスページ](/dashboard/dashboard-profiling.md)を参照してください。

> **ノート：**
>
> デフォルトでは、TiDBダッシュボードは使用状況の詳細をPingCAPと共有して、製品を改善する方法を理解するのに役立ちます。共有されるものと共有を無効にする方法の詳細については、 [テレメトリー](/telemetry.md)を参照してください。
