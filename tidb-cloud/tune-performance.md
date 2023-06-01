---
title: Analyze and Tune Performance
summary: Learn how to analyze and tune performance of your TiDB Cloud cluster.
---

# パフォーマンスの分析と調整 {#analyze-and-tune-performance}

TiDB Cloud は、パフォーマンスを分析するために[キービジュアライザー](#key-visualizer)を提供します。

-   ステートメント分析を使用すると、ページ上の SQL 実行を直接観察し、システム テーブルをクエリせずにパフォーマンスの問題を簡単に特定できます。

-   スロー クエリを使用すると、TiDB クラスター内のすべてのスロー クエリを検索して表示し、実行プラン、SQL 実行情報、その他の詳細を表示して、各スロー クエリのボトルネックを調査できます。

-   Key Visualizer は、TiDB のデータ アクセス パターンとデータ ホットスポットを観察するのに役立ちます。

> **ノート：**
>
> 現在、これら 3 つの機能は[Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)では利用できません。

## ステートメント分析 {#statement-analysis}

ステートメント分析を使用するには、次の手順を実行します。

1.  クラスターの**「SQL 診断」**タブに移動します。

2.  **「SQL ステートメント」**タブをクリックします。

3.  時間間隔ボックスで分析する期間を選択します。これにより、この期間におけるすべてのデータベースの SQL ステートメントの実行統計を取得できます。

4.  (オプション) 特定のデータベースのみに関心がある場合は、次のボックスで対応するスキーマを選択して結果をフィルタリングできます。

結果は表の形式で表示され、さまざまな列で結果を並べ替えることができます。

![Statement Analysis](/media/tidb-cloud/statement-analysis.png)

詳細については、 [TiDB ダッシュボードでのステートメント実行の詳細](https://docs.pingcap.com/tidb/stable/dashboard-statement-details)を参照してください。

## 遅いクエリ {#slow-query}

デフォルトでは、300 ミリ秒を超える SQL クエリは低速クエリとみなされます。

クラスター内の遅いクエリを表示するには、次の手順を実行します。

1.  クラスターの**「SQL 診断」**タブに移動します。

2.  **「スロークエリ」**タブをクリックします。

3.  リスト内の低速クエリをクリックすると、その詳細な実行情報が表示されます。

4.  (オプション) ターゲット時間範囲、関連データベース、SQL キーワードに基づいて遅いクエリをフィルタリングできます。表示される低速クエリの数を制限することもできます。

結果は表の形式で表示され、さまざまな列で結果を並べ替えることができます。

![Slow Queries](/media/tidb-cloud/slow-queries.png)

詳細については、 [TiDB ダッシュボードの遅いクエリ](https://docs.pingcap.com/tidb/stable/dashboard-slow-query)を参照してください。

## キービジュアライザー {#key-visualizer}

主要な分析を表示するには、次の手順を実行します。

1.  クラスターの**「SQL 診断」**タブに移動します。

2.  **「キー ビジュアライザー」**タブをクリックします。

![Key Visualizer](/media/tidb-cloud/key-visualizer.png)

**Key Visualizer**ページでは、アクセス トラフィックの時間の経過に伴う変化を大きなヒート マップで表示します。ヒートマップの各軸に沿った平均値を下と右側に示します。左側はテーブル名、インデックス名などの情報です。

詳細については、 [キービジュアライザー](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer)を参照してください。
