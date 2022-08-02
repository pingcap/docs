---
title: Analyze and Tune Performance
summary: Learn how to analyze and tune performance of your TiDB Cloud cluster.
---

# パフォーマンスの分析と調整 {#analyze-and-tune-performance}

TiDB Cloudは、パフォーマンスを分析するために[ステートメント分析](#statement-analysis)と[キー ビジュアライザー](#key-visualizer)を提供します。

-   ステートメント分析を使用すると、ページでの SQL の実行を直接観察し、システム テーブルを照会せずにパフォーマンスの問題を簡単に特定できます。

-   Key Visualizer は、TiDB のデータ アクセス パターンとデータ ホットスポットを観察するのに役立ちます。

## ステートメント分析 {#statement-analysis}

ステートメント分析を使用するには、次の手順を実行します。

1.  クラスタの [**診断**] タブに移動します。

2.  [**ステートメント**] タブをクリックします。

3.  時間間隔ボックスで分析する期間を選択します。その後、この期間のすべてのデータベースの SQL ステートメントの実行統計を取得できます。

4.  (オプション) 特定のデータベースのみに関心がある場合は、次のボックスで対応するスキーマを選択して、結果をフィルタリングできます。

結果は表形式で表示され、異なる列で結果を並べ替えることができます。

![Statement Analysis](/media/tidb-cloud/statement-analysis.png)

詳細については、 [TiDB ダッシュボードでのステートメント実行の詳細](https://docs.pingcap.com/tidb/stable/dashboard-statement-details)を参照してください。

## キー ビジュアライザー {#key-visualizer}

主要な分析を表示するには、次の手順を実行します。

1.  クラスタの [**診断**] タブに移動します。

2.  [**キー ビジュアライザー**] タブをクリックします。

![Key Visualizer](/media/tidb-cloud/key-visualizer.png)

**Key Visualizer**ページでは、時間の経過に伴うアクセス トラフィックの変化を示す大きなヒート マップが表示されます。ヒート マップの各軸に沿った平均値を下と右側に示します。左側は、テーブル名、インデックス名、およびその他の情報です。

詳細については、 [キー ビジュアライザー](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer)を参照してください。
