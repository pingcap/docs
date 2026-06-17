---
title: パフォーマンスの分析とチューニング
summary: TiDB Cloud でパフォーマンスを分析およびチューニングする方法を学びます。
aliases: ['/ja/tidbcloud/index-insight']
---

# パフォーマンスの分析とチューニング

<CustomContent plan="starter,essential,dedicated">

TiDB Cloud では、パフォーマンスを分析するために [Slow Query](#slow-query)、[Statement Analysis](#statement-analysis)、および [Key Visualizer](#key-visualizer) を提供しています。

</CustomContent>

<CustomContent plan="premium">

TiDB Cloud では、パフォーマンスを分析するために [Slow Query](#slow-query) と [SQL Statement](#sql-statement) を提供しています。

</CustomContent>

- Slow Query では、<CustomContent plan="starter">{{{ .starter }}} instance</CustomContent><CustomContent plan="essential">{{{ .essential }}} instance</CustomContent><CustomContent plan="premium">{{{ .premium }}} instance</CustomContent><CustomContent plan="dedicated">{{{ .dedicated }}} cluster</CustomContent> 内のすべての低速クエリを検索して表示できます。また、実行計画、SQL 実行情報、その他の詳細を確認することで、各低速クエリのボトルネックを調査できます。

- <CustomContent plan="starter,essential,dedicated">Statement Analysis</CustomContent><CustomContent plan="premium">SQL Statement</CustomContent> を使用すると、システムテーブルをクエリしなくても、ページ上で SQL の実行状況を直接確認し、パフォーマンスの問題を簡単に特定できます。

<CustomContent plan="starter,essential,dedicated">

- Key Visualizer は、TiDB のデータアクセスパターンとデータホットスポットの観察に役立ちます。

> **Note:**
>
> 現在、**Key Visualizer** は TiDB Cloud Dedicated クラスタでのみ利用できます。

</CustomContent>

## Diagnosis ページを表示する {#view-the-diagnosis-page}

1. [**My TiDB**](https://tidbcloud.com/tidbs) ページで、対象の <CustomContent plan="starter">{{{ .starter }}} instance</CustomContent><CustomContent plan="essential">{{{ .essential }}} instance</CustomContent><CustomContent plan="premium">{{{ .premium }}} instance</CustomContent><CustomContent plan="dedicated">{{{ .dedicated }}} cluster</CustomContent> の名前をクリックして、その概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、まず左上のコンボボックスを使用して対象の組織に切り替えてください。

2. 左側のナビゲーションペインで、**Monitoring** > **Diagnosis** をクリックします。

## Slow Query {#slow-query}

デフォルトでは、300 ミリ秒を超えて実行される SQL クエリは低速クエリと見なされます。

<CustomContent plan="starter">{{{ .starter }}} instance</CustomContent><CustomContent plan="essential">{{{ .essential }}} instance</CustomContent><CustomContent plan="premium">{{{ .premium }}} instance</CustomContent><CustomContent plan="dedicated">{{{ .dedicated }}} cluster</CustomContent> で低速クエリを表示するには、次の手順を実行します。

<CustomContent plan="starter,essential,dedicated">

1. [**Diagnosis** ページに移動します](#view-the-diagnosis-page)。

2. **Slow Query** タブをクリックします。

3. リスト内の任意の低速クエリをクリックして、その詳細な実行情報を表示します。

4. （任意）対象の時間範囲、関連するデータベース、および SQL キーワードに基づいて低速クエリをフィルタリングできます。表示する低速クエリの数を制限することもできます。

</CustomContent>

<CustomContent plan="premium">

1. {{{ .premium }}} instance の概要ページに移動し、左側のナビゲーションペインで **Monitoring** > **Slow Query** をクリックします。

2. リストから低速クエリを選択して、その詳細な実行情報を表示します。

3. （任意）対象の時間範囲と SQL キーワードに基づいて低速クエリをフィルタリングできます。表示する低速クエリの数を制限することもできます。

</CustomContent>

結果は表形式で表示され、異なる列で並べ替えることができます。

<CustomContent plan="starter,essential">

> **Note:**
>
> トラフィックの可視性を向上させるため、{{{ .starter }}} と {{{ .essential }}} では、詳細な実行情報において AWS PrivateLink 経由の接続に対する実際のクライアント IP アドレスが表示されるようになりました。現在、この機能はベータ版であり、AWS リージョン `Frankfurt (eu-central-1)` でのみ利用できます。

</CustomContent>
<CustomContent plan="starter,essential,dedicated">

詳細については、[TiDB Dashboard の Slow Queries](https://docs.pingcap.com/tidb/stable/dashboard-slow-query) を参照してください。

</CustomContent>

<CustomContent plan="starter,essential,dedicated">

## Statement Analysis {#statement-analysis}

Statement Analysis を使用するには、次の手順を実行します。

1. [**Diagnosis** ページに移動します](#view-the-diagnosis-page)。

2. **SQL Statement** タブをクリックします。

3. 時間間隔ボックスで分析対象の期間を選択します。すると、その期間におけるすべてのデータベースの SQL 文の実行統計を取得できます。

4. （任意）特定のデータベースのみに関心がある場合は、次のボックスで対応する schema(s) を選択して結果をフィルタリングできます。

</CustomContent>

<CustomContent plan="premium">

## SQL Statement {#sql-statement}

**SQL Statement** ページを使用するには、次の手順を実行します。

1. {{{ .premium }}} instance の概要ページに移動し、左側のナビゲーションペインで **Monitoring** > **SQL Statement** をクリックします。

2. リスト内の SQL 文をクリックして、その詳細な実行情報を表示します。

3. 時間間隔ボックスで分析対象の期間を選択します。すると、その期間におけるすべてのデータベースにまたがる SQL 文の実行統計を取得できます。

4. （任意）特定のデータベースのみに関心がある場合は、次のボックスで対応する schema(s) を選択して結果をフィルタリングできます。

</CustomContent>

結果は表形式で表示され、異なる列で並べ替えることができます。

<CustomContent plan="starter,essential,dedicated">

詳細については、[TiDB Dashboard の Statement Execution Details](https://docs.pingcap.com/tidb/stable/dashboard-statement-details) を参照してください。

## Key Visualizer {#key-visualizer}

> **Note:**
>
> Key Visualizer は [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) クラスタでのみ利用できます。

キー分析を表示するには、次の手順を実行します。

1. {{{ .dedicated }}} cluster の [**Diagnosis**](#view-the-diagnosis-page) ページに移動します。

2. **Key Visualizer** タブをクリックします。

**Key Visualizer** ページでは、大きなヒートマップにより、アクセス トラフィックが時間の経過とともにどのように変化するかを確認できます。ヒートマップの各軸に沿った平均値は、下部と右側に表示されます。左側には、テーブル名、インデックス名、およびその他の関連情報が表示されます。

詳細については、[Key Visualizer](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer) を参照してください。

</CustomContent>