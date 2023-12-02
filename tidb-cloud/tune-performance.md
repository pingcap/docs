---
title: Analyze and Tune Performance
summary: Learn how to analyze and tune performance of your TiDB Cloud cluster.
---

# パフォーマンスの分析と調整 {#analyze-and-tune-performance}

TiDB Cloud は、パフォーマンスを分析するために[遅いクエリ](#slow-query) 、 [ステートメント分析](#statement-analysis) 、 [キービジュアライザー](#key-visualizer) 、および[インデックスインサイト（ベータ版）](#index-insight-beta)を提供します。

-   スロー クエリを使用すると、TiDB クラスター内のすべてのスロー クエリを検索して表示し、実行プラン、SQL 実行情報、およびその他の詳細を表示して、各スロー クエリのボトルネックを調査できます。

-   ステートメント分析を使用すると、ページ上の SQL 実行を直接観察し、システム テーブルをクエリせずにパフォーマンスの問題を簡単に特定できます。

-   Key Visualizer は、TiDB のデータ アクセス パターンとデータ ホットスポットを観察するのに役立ちます。

-   Index Insight は、有意義で実用的なインデックスの推奨事項を提供します。

> **注記：**
>
> 現在、 **Key Visualizer**と**Index Insight (ベータ版)**は[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)のクラスターでは使用できません。

## 遅いクエリ {#slow-query}

デフォルトでは、300 ミリ秒を超える SQL クエリは低速クエリとみなされます。

クラスター内の遅いクエリを表示するには、次の手順を実行します。

1.  クラスターの**「診断」**ページに移動します。

2.  **「スロークエリ」**タブをクリックします。

3.  リスト内の低速クエリをクリックすると、その詳細な実行情報が表示されます。

4.  (オプション) ターゲット時間範囲、関連データベース、SQL キーワードに基づいて遅いクエリをフィルタリングできます。表示される低速クエリの数を制限することもできます。

結果は表の形式で表示され、さまざまな列で結果を並べ替えることができます。

詳細については、 [TiDB ダッシュボードの遅いクエリ](https://docs.pingcap.com/tidb/stable/dashboard-slow-query)を参照してください。

## ステートメント分析 {#statement-analysis}

ステートメント分析を使用するには、次の手順を実行します。

1.  クラスターの**「診断」**ページに移動します。

2.  **「SQL ステートメント」**タブをクリックします。

3.  時間間隔ボックスで分析する期間を選択します。これにより、この期間におけるすべてのデータベースの SQL ステートメントの実行統計を取得できます。

4.  (オプション) 特定のデータベースのみに関心がある場合は、次のボックスで対応するスキーマを選択して結果をフィルタリングできます。

結果は表の形式で表示され、さまざまな列で結果を並べ替えることができます。

詳細については、 [TiDB ダッシュボードでのステートメント実行の詳細](https://docs.pingcap.com/tidb/stable/dashboard-statement-details)を参照してください。

## キービジュアライザー {#key-visualizer}

> **注記：**
>
> Key Visualizer は[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターでのみ使用できます。

主要な分析を表示するには、次の手順を実行します。

1.  クラスターの**「診断」**ページに移動します。

2.  **「キー ビジュアライザー」**タブをクリックします。

**Key Visualizer**ページでは、アクセス トラフィックの時間の経過に伴う変化を大きなヒート マップで表示します。ヒートマップの各軸に沿った平均値を下と右側に示します。左側はテーブル名、インデックス名などの情報です。

詳細については、 [キービジュアライザー](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer)を参照してください。

## インデックスインサイト（ベータ版） {#index-insight-beta}

TiDB Cloudの Index Insight 機能は、インデックスを効果的に利用していない遅いクエリに対して推奨インデックスを提供することで、クエリのパフォーマンスを最適化する強力な機能を提供します。

> **注記：**
>
> Index Insight は現在ベータ版であり、 [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターでのみ使用できます。

詳細については、 [インデックスの洞察](/tidb-cloud/index-insight.md)を参照してください。
