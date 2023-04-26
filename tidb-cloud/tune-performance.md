---
title: Analyze and Tune Performance
summary: Learn how to analyze and tune performance of your TiDB Cloud cluster.
---

# パフォーマンスの分析と調整 {#analyze-and-tune-performance}

TiDB Cloud は、パフォーマンスを分析するために[ステートメント分析](#statement-analysis) 、 [スロークエリ](#slow-query) 、および[キー ビジュアライザー](#key-visualizer)を提供します。

-   ステートメント分析を使用すると、ページでの SQL の実行を直接観察し、システム テーブルを照会せずにパフォーマンスの問題を簡単に特定できます。

-   スロー クエリを使用すると、TiDB クラスター内のすべてのスロー クエリを検索して表示し、実行計画、SQL 実行情報、およびその他の詳細を表示して、各スロー クエリのボトルネックを調べることができます。

-   Key Visualizer は、TiDB のデータ アクセス パターンとデータ ホットスポットを観察するのに役立ちます。

> **ノート：**
>
> 現在、 **Statement Analysis**と<strong>Key Visualizer</strong>は[Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)では利用できません。

## ステートメント分析 {#statement-analysis}

> **ノート：**
>
> ステートメント分析は[Dedicated Tierクラスター](/tidb-cloud/select-cluster-tier.md#dedicated-tier)でのみ使用できます。

ステートメント分析を使用するには、次の手順を実行します。

1.  クラスターの**[SQL 診断]**タブに移動します。

2.  **[SQL ステートメント]**タブをクリックします。

3.  時間間隔ボックスで分析する期間を選択します。その後、この期間のすべてのデータベースの SQL ステートメントの実行統計を取得できます。

4.  (オプション) 特定のデータベースのみに関心がある場合は、次のボックスで対応するスキーマを選択して、結果をフィルタリングできます。

結果は表形式で表示され、異なる列で結果を並べ替えることができます。

![Statement Analysis](/media/tidb-cloud/statement-analysis.png)

詳細については、 [TiDB ダッシュボードでのステートメント実行の詳細](https://docs.pingcap.com/tidb/stable/dashboard-statement-details)を参照してください。

## スロークエリ {#slow-query}

デフォルトでは、300 ミリ秒を超える SQL クエリは低速クエリと見なされます。

クラスター内のスロー クエリを表示するには、次の手順を実行します。

1.  クラスターの**[SQL 診断]**タブに移動します。

2.  **[スロー クエリ]**タブをクリックします。

3.  リスト内のスロー クエリをクリックすると、詳細な実行情報が表示されます。

4.  (オプション) ターゲットの時間範囲、関連するデータベース、および SQL キーワードに基づいて、スロー クエリをフィルタリングできます。表示するスロー クエリの数を制限することもできます。

結果は表形式で表示され、異なる列で結果を並べ替えることができます。

![Slow Queries](/media/tidb-cloud/slow-queries.png)

詳細については、 [TiDB ダッシュボードでの遅いクエリ](https://docs.pingcap.com/tidb/stable/dashboard-slow-query)を参照してください。

## キー ビジュアライザー {#key-visualizer}

> **ノート：**
>
> Key Visualizer は[Dedicated Tierクラスター](/tidb-cloud/select-cluster-tier.md#dedicated-tier)のみ使用できます。

主要な分析を表示するには、次の手順を実行します。

1.  クラスターの**[SQL 診断]**タブに移動します。

2.  **[キー ビジュアライザー]**タブをクリックします。

![Key Visualizer](/media/tidb-cloud/key-visualizer.png)

**Key Visualizer**ページでは、時間の経過に伴うアクセス トラフィックの変化を示す大きなヒート マップが表示されます。ヒート マップの各軸に沿った平均値を下と右側に示します。左側は、テーブル名、インデックス名、およびその他の情報です。

詳細については、 [キー ビジュアライザー](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer)を参照してください。
