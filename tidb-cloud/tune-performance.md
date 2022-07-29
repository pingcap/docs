---
title: Analyze and Tune Performance
summary: Learn how to analyze and tune performance of your TiDB Cloud cluster.
---

# パフォーマンスの分析と調整 {#analyze-and-tune-performance}

TiDB Cloudは、パフォーマンスを分析するための[ステートメント分析](#statement-analysis)と[キービジュアライザー](#key-visualizer)を提供します。

-   ステートメント分析を使用すると、ページでのSQLの実行を直接観察し、システムテーブルにクエリを実行せずにパフォーマンスの問題を簡単に見つけることができます。

-   Key Visualizerは、TiDBのデータアクセスパターンとデータホットスポットを監視するのに役立ちます。

## ステートメント分析 {#statement-analysis}

ステートメント分析を使用するには、次の手順を実行します。

1.  クラスタの[**診断**]タブに移動します。デフォルトでは、[<strong>ステートメント</strong>]サブタブが表示されます。

2.  [時間間隔]ボックスで分析する期間を選択します。次に、この期間のすべてのデータベースのSQLステートメントの実行統計を取得できます。

3.  （オプション）特定のデータベースのみに関心がある場合は、次のボックスで対応するスキーマを選択して、結果をフィルタリングできます。

結果は表の形式で表示され、さまざまな列で結果を並べ替えることができます。

![Statement Analysis](/media/tidb-cloud/statement-analysis.png)

詳細については、 [TiDBダッシュボードでのステートメント実行の詳細](https://docs.pingcap.com/tidb/stable/dashboard-statement-details)を参照してください。

## キービジュアライザー {#key-visualizer}

主要な分析を表示するには、次の手順を実行します。

1.  クラスタの[**診断**]タブに移動します。

2.  [**キービジュアライザー**]タブを選択します。

![Key Visualizer](/media/tidb-cloud/key-visualizer.png)

[**キービジュアライザー]**ページの大きなヒートマップには、時間の経過に伴うアクセストラフィックの変化が表示されます。ヒートマップの各軸に沿った平均値は、下と右側に示されています。左側はテーブル名、インデックス名、その他の情報です。

詳細については、 [キービジュアライザー](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer)を参照してください。
