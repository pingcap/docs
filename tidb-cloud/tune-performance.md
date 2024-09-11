---
title: Analyze and Tune Performance
summary: TiDB Cloudクラスターのパフォーマンスを分析および調整する方法を学びます。
---

# パフォーマンスの分析と調整 {#analyze-and-tune-performance}

TiDB Cloud は、パフォーマンスを分析するために[遅いクエリ](#slow-query) 、 [ステートメント分析](#statement-analysis) 、 [キービジュアライザー](#key-visualizer) 、 [インデックスインサイト（ベータ版）](#index-insight-beta)を提供します。

-   スロー クエリを使用すると、TiDB クラスター内のすべてのスロー クエリを検索して表示し、実行プラン、SQL 実行情報、その他の詳細を表示して、各スロー クエリのボトルネックを調査できます。

-   ステートメント分析を使用すると、ページ上の SQL 実行を直接観察し、システム テーブルをクエリせずにパフォーマンスの問題を簡単に見つけることができます。

-   Key Visualizer は、TiDB のデータ アクセス パターンとデータ ホットスポットを観察するのに役立ちます。

-   Index Insight は、意味のある実用的なインデックス推奨事項を提供します。

> **注記：**
>
> 現在、 **Key Visualizer**と**Index Insight (ベータ版) は**[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターで利用できません。

## 遅いクエリ {#slow-query}

デフォルトでは、300 ミリ秒以上かかる SQL クエリは遅いクエリと見なされます。

クラスター内の遅いクエリを表示するには、次の手順を実行します。

1.  クラスターの**診断**ページに移動します。

2.  **[スロー クエリ]**タブをクリックします。

3.  リスト内の遅いクエリをクリックすると、詳細な実行情報が表示されます。

4.  (オプション) ターゲット時間範囲、関連データベース、SQL キーワードに基づいて、スロー クエリをフィルターできます。また、表示されるスロー クエリの数を制限することもできます。

結果は表形式で表示され、さまざまな列で結果を並べ替えることができます。

詳細については[TiDB ダッシュボードの遅いクエリ](https://docs.pingcap.com/tidb/stable/dashboard-slow-query)参照してください。

## ステートメント分析 {#statement-analysis}

ステートメント分析を使用するには、次の手順を実行します。

1.  クラスターの**診断**ページに移動します。

2.  **「SQL ステートメント」**タブをクリックします。

3.  時間間隔ボックスで分析する期間を選択します。すると、この期間内のすべてのデータベースの SQL ステートメントの実行統計を取得できます。

4.  (オプション) 特定のデータベースのみを対象とする場合は、次のボックスで対応するスキーマを選択して結果をフィルタリングできます。

結果は表形式で表示され、さまざまな列で結果を並べ替えることができます。

詳細については[TiDBダッシュボードのステートメント実行の詳細](https://docs.pingcap.com/tidb/stable/dashboard-statement-details)参照してください。

## キービジュアライザー {#key-visualizer}

> **注記：**
>
> Key Visualizer は[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでのみ使用できます。

主要な分析を表示するには、次の手順を実行します。

1.  クラスターの**診断**ページに移動します。

2.  [**キー ビジュアライザー]**タブをクリックします。

**Key Visualizer**ページでは、大きなヒート マップで、時間の経過に伴うアクセス トラフィックの変化が表示されます。ヒート マップの各軸に沿った平均値が下と右側に表示されます。左側には、テーブル名、インデックス名などの情報が表示されます。

詳細については[キービジュアライザー](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer)参照してください。

## インデックスインサイト（ベータ版） {#index-insight-beta}

TiDB Cloudの Index Insight 機能は、インデックスを効果的に使用していない低速クエリに対して推奨インデックスを提供することで、クエリ パフォーマンスを最適化する強力な機能を提供します。

> **注記：**
>
> Index Insight は現在ベータ版であり、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでのみ使用できます。

詳細については[インデックスインサイト](/tidb-cloud/index-insight.md)参照してください。
