---
title: Analyze and Tune Performance
summary: TiDB Cloudでパフォーマンスを分析および調整する方法を学びます。
aliases: ['/tidbcloud/index-insight']
---

# パフォーマンスの分析と調整 {#analyze-and-tune-performance}

<CustomContent plan="starter,essential,dedicated">

TiDB Cloud は、パフォーマンスを分析するために[遅いクエリ](#slow-query) 、 [ステートメント分析](#statement-analysis) 、 [キービジュアライザー](#key-visualizer)を提供します。

</CustomContent>

<CustomContent plan="premium">

TiDB Cloud は、パフォーマンスを分析するために[遅いクエリ](#slow-query)と[SQL文](#sql-statement)を提供します。

</CustomContent>

-   スロークエリを使用すると、TiDB内のすべてのスロークエリを検索して表示できます。<customcontent plan="starter,essential,dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>実行プラン、SQL 実行情報、その他の詳細を表示して、各低速クエリのボトルネックを調査します。

-   <customcontent plan="starter,essential,dedicated">ステートメント分析</customcontent><customcontent plan="premium">SQL文</customcontent>ページ上の SQL 実行を直接観察し、システム テーブルをクエリせずにパフォーマンスの問題を簡単に見つけることができます。

<CustomContent plan="starter,essential,dedicated">

-   Key Visualizer は、TiDB のデータ アクセス パターンとデータ ホットスポットを観察するのに役立ちます。

> **注記：**
>
> 現在、 **Key Visualizer**はTiDB Cloud Dedicated クラスターでのみ使用できます。

</CustomContent>

## 診断ページをビュー {#view-the-diagnosis-page}

<CustomContent plan="starter,essential,dedicated">

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページで、ターゲット クラスターの名前をクリックして、概要ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  左側のナビゲーション ペインで、 **[監視]** &gt; **[診断]**をクリックします。

</CustomContent>

<CustomContent plan="premium">

1.  組織の[**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページで、ターゲットインスタンスの名前をクリックして、概要ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織とインスタンスを切り替えることができます。

2.  左側のナビゲーション ペインで、 **[監視]**をクリックします。

</CustomContent>

## 遅いクエリ {#slow-query}

デフォルトでは、300 ミリ秒以上かかる SQL クエリは遅いクエリと見なされます。

TiDBで遅いクエリを表示するには<customcontent plan="starter,essential,dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>、次の手順を実行します。

<CustomContent plan="starter,essential,dedicated">

1.  クラスターの[**診断**](#view-the-diagnosis-page)ページに移動します。

2.  **[スロー クエリ]**タブをクリックします。

3.  リスト内の遅いクエリをクリックすると、詳細な実行情報が表示されます。

4.  （オプション）対象期間、関連データベース、SQLキーワードに基づいてスロークエリをフィルタリングできます。また、表示するスロークエリの数を制限することもできます。

</CustomContent>

<CustomContent plan="premium">

1.  TiDB インスタンスの概要ページに移動し、左側のナビゲーション ペインで**[モニタリング]** &gt; **[スロー クエリ]**をクリックします。

2.  詳細な実行情報を表示するには、リストから遅いクエリを選択します。

3.  （オプション）対象期間とSQLキーワードに基づいてスロークエリをフィルタリングできます。また、表示するスロークエリの数を制限することもできます。

</CustomContent>

結果は表形式で表示され、さまざまな列で結果を並べ替えることができます。

<CustomContent plan="starter,essential,dedicated">

詳細については[TiDBダッシュボードの遅いクエリ](https://docs.pingcap.com/tidb/stable/dashboard-slow-query)参照してください。

</CustomContent>

<CustomContent plan="starter,essential,dedicated">

## ステートメント分析 {#statement-analysis}

ステートメント分析を使用するには、次の手順を実行します。

1.  クラスターの[**診断**](#view-the-diagnosis-page)ページに移動します。

2.  **「SQL ステートメント」**タブをクリックします。

3.  時間間隔ボックスで分析対象となる期間を選択します。すると、その期間におけるすべてのデータベースのSQL文の実行統計を取得できます。

4.  (オプション) 特定のデータベースのみを対象とする場合は、次のボックスで対応するスキーマを選択して、結果をフィルタリングできます。

</CustomContent>

<CustomContent plan="premium">

## SQL文 {#sql-statement}

**SQL ステートメント**ページを使用するには、次の手順を実行します。

1.  TiDB インスタンスの概要ページに移動し、左側のナビゲーション ペインで**[監視]** &gt; **[SQL ステートメント]**をクリックします。

2.  リスト内の SQL ステートメントをクリックすると、詳細な実行情報が表示されます。

3.  時間間隔ボックスで、分析する期間を選択します。すると、その期間における全データベースのSQL文の実行統計を取得できます。

4.  (オプション) 特定のデータベースのみを対象とする場合は、次のボックスで対応するスキーマを選択して、結果をフィルタリングできます。

</CustomContent>

結果は表形式で表示され、さまざまな列で結果を並べ替えることができます。

<CustomContent plan="starter,essential,dedicated">

詳細については[TiDBダッシュボードのステートメント実行の詳細](https://docs.pingcap.com/tidb/stable/dashboard-statement-details)参照してください。

## キービジュアライザー {#key-visualizer}

> **注記：**
>
> Key Visualizer は[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでのみ使用できます。

主要な分析を表示するには、次の手順を実行します。

1.  クラスターの[**診断**](#view-the-diagnosis-page)ページに移動します。

2.  **[キー ビジュアライザー]**タブをクリックします。

**Key Visualizer**ページでは、アクセストラフィックの経時的な変化を示す大きなヒートマップが表示されます。ヒートマップの各軸の平均値（平均値）は、下部と右側に表示されます。左側には、テーブル名、インデックス名、その他の関連情報が表示されます。

詳細については[キービジュアライザー](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer)参照してください。

</CustomContent>
