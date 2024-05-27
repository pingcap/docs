---
title: Statement Execution Details of TiDB Dashboard
summary: TiDB ダッシュボードには、SQL テンプレートの概要、実行プラン リスト、プラン バインディング機能など、SQL ステートメントの実行に関する詳細情報が表示されます。v6.6.0 以降では、高速プラン バインディングにより、実行プランをすばやくバインドおよびドロップできます。ただし、制限があり、SUPER 権限が必要です。プランの実行詳細には、SQL サンプル、完全な実行プラン情報、基本的な実行詳細が含まれます。実行プランの視覚的表現は、表、テキスト、グラフの形式で利用できます。追加のタブには、実行時間、コプロセッサー読み取り、トランザクション、および低速クエリに関する情報が表示されます。
---

# TiDBダッシュボードのステートメント実行の詳細 {#statement-execution-details-of-tidb-dashboard}

リスト内の任意の項目をクリックすると、SQL ステートメントの詳細ページに移動し、より詳細な情報が表示されます。この情報には、次の部分が含まれます。

-   SQL ステートメントの概要。これには、SQL テンプレート、SQL テンプレート ID、表示されている SQL 実行の現在の時間範囲、実行プランの数、SQL ステートメントが実行されるデータベース、および高速プラン バインディング機能が含まれます (次の図の領域 1)。
-   実行プラン リスト: SQL ステートメントに複数の実行プランがある場合は、このリストが表示されます。実行プランのテキスト情報に加えて、TiDB v6.2.0 ではビジュアル実行プランが導入され、ステートメントの各演算子と詳細情報をより直感的に理解できるようになりました。さまざまな実行プランを選択でき、選択したプランの詳細がリストの下に表示されます (次の図の領域 2)。
-   選択した実行プランの詳細情報を表示するプランの実行詳細。1 (次の図の領域[実行計画の詳細](#execution-details-of-plans) ) を参照してください。

![Details](/media/dashboard/dashboard-statement-detail-v660.png)

## 高速プランバインディング {#fast-plan-binding}

v6.6.0 以降、TiDB では高速プラン バインディング機能が導入されています。TiDB ダッシュボードで、SQL ステートメントを特定の実行プランにすばやくバインドできます。

### 使用法 {#usage}

#### 実行プランをバインドする {#bind-an-execution-plan}

1.  **[プランのバインド]**をクリックします。 **[プランのバインド]**ダイアログ ボックスが表示されます。

    ![Fast plan binding - not bound - entry](/media/dashboard/dashboard-quick-binding-entry-notbound.png)

2.  バインドするプランを選択し、 **「バインド」を**クリックします。

    ![Fast plan binding - popup](/media/dashboard/dashboard-quick-binding-popup-notbound.png)

3.  バインディングが完了すると、 **「Bound」**ラベルが表示されます。

    ![Fast plan binding - popup - binding completed](/media/dashboard/dashboard-quick-binding-popup-bound.png)

#### 既存のバインディングを削除する {#drop-an-existing-binding}

1.  既存のバインディングを持つ SQL ステートメントのページで、 **[プラン バインディング]**をクリックします。[**プラン バインディング]**ダイアログ ボックスが表示されます。

    ![Fast plan binding - bound - entry](/media/dashboard/dashboard-quick-binding-entry-bound.png)

2.  **[ドロップ]を**クリックします。

    ![Fast plan binding - popup - bound](/media/dashboard/dashboard-quick-binding-popup-bound.png)

3.  バインドが削除されると、 **「バインドされていません」**というラベルが表示されます。

    ![Fast plan binding - popup](/media/dashboard/dashboard-quick-binding-popup-notbound.png)

### 制限 {#limitation}

現在、高速プラン バインディング機能では、次の種類の SQL ステートメントはサポートされていません。

-   `SELECT` `INSERT` `UPDATE` `REPLACE` `DELETE`
-   サブクエリを含むクエリ
-   TiFlashにアクセスするクエリ
-   3つ以上のテーブルを結合するクエリ

この機能を使用するには、SUPER 権限が必要です。使用中に権限の問題が発生した場合は、 [TiDBダッシュボードユーザー管理](/dashboard/dashboard-user.md)を参照して必要な権限を追加してください。

## 計画の実行詳細 {#execution-details-of-plans}

プランの実行詳細には、次の情報が含まれます。

-   SQL サンプル: プランに対応して実際に実行される特定の SQL ステートメントのテキスト。時間範囲内で実行された任意の SQL ステートメントが SQL サンプルとして使用される可能性があります。
-   実行計画: 実行計画に関する完全な情報が、表、グラフ、テキストで表示されます。実行計画の詳細については、 [クエリ実行プランを理解する](/explain-overview.md)を参照してください。複数の実行計画を選択した場合は、そのうちの 1 つだけが表示されます。
-   SQL ステートメントの基本情報、実行時間、コプロセッサー読み取り、トランザクション、および低速クエリについては、対応するタブ タイトルをクリックして、さまざまな情報を切り替えることができます。

![Execution details of plans](/media/dashboard/dashboard-statement-plans-detail.png)

### SQLサンプル {#sql-sample}

アイテムの詳細情報を表示するには、 **「展開」**をクリックします。詳細情報をクリップボードにコピーするには、 **「コピー」**をクリックします。

### 実行計画 {#execution-plans}

TiDB ダッシュボードでは、実行プランをテーブル、テキスト、グラフの 3 つの方法で表示できます。実行プランの読み方については、 [クエリ実行プランを理解する](/explain-overview.md)参照してください。

#### 表形式の実行計画 {#execution-plan-in-table-format}

テーブル形式では、実行プランに関する詳細情報が提供されるため、異常なオペレーター メトリックをすばやく特定し、さまざまなオペレーターのステータスを比較するのに役立ちます。次の図は、テーブル形式の実行プランを示しています。

![Execution plan in table format](/media/dashboard/dashboard-table-plan.png)

表形式ではテキスト形式と同様の情報が表示されますが、よりユーザーフレンドリーな操作が提供されます。

-   列幅は自由に調整できます。
-   コンテンツが列幅を超えると、自動的に切り捨てられ、完全な情報がツールヒントに表示されます。
-   実行プランが大きい場合は、ローカル分析用にテキスト ファイルとしてダウンロードできます。
-   列ピッカーを使用して列を非表示にしたり管理したりできます。

![Execution plan in table format - column picker](/media/dashboard/dashboard-table-plan-columnpicker.png)

#### グラフ形式の実行計画 {#execution-plan-in-graph-format}

グラフ形式は、複雑な SQL ステートメントの実行プラン ツリーを表示し、各演算子とその対応する内容を詳細に理解するのに適しています。次の図は、グラフ形式の実行プランを示しています。

![Execution plan in graph format](/media/dashboard/dashboard-visual-plan-2.png)

-   グラフは左から右、上から下への実行を示します。
-   上位ノードは親演算子であり、下位ノードは子演算子です。
-   タイトル バーの色は、演算子が実行されるコンポーネントを示します。黄色は TiDB、青は TiKV、ピンクはTiFlashを表します。
-   タイトルバーにはオペレーター名が表示され、その下に表示されるテキストはオペレーターの基本情報です。

ノード領域をクリックすると、右側のサイドバーにオペレータの詳細情報が表示されます。

![Execution plan in graph format - sidebar](/media/dashboard/dashboard-visual-plan-popup.png)

### SQL実行の詳細 {#sql-execution-details}

SQL ステートメントの基本情報、実行時間、コプロセッサー読み取り、トランザクション、および低速クエリについては、対応するタブ タイトルをクリックして、さまざまな情報を切り替えることができます。

![Show different execution information](/media/dashboard/dashboard-slow-queries-detail2-v620.png)

#### 基本タブ {#basic-tab}

SQL 実行の基本情報には、テーブル名、インデックス名、実行回数、合計レイテンシーが含まれます。**説明**列には、各フィールドの詳細な説明が表示されます。

![Basic information](/media/dashboard/dashboard-statement-plans-basic.png)

#### 時間タブ {#time-tab}

**[時間]**タブをクリックすると、実行プランの各ステージの所要時間を確認できます。

> **注記：**
>
> 一部の操作は単一の SQL ステートメント内で並行して実行される可能性があるため、各ステージの累積実行時間は SQL ステートメントの実際の実行時間を超える可能性があります。

![Execution time](/media/dashboard/dashboard-statement-plans-time.png)

#### コプロセッサー読み取りタブ {#coprocessor-read-tab}

**「コプロセッサー読み取り**」タブをクリックすると、コプロセッサー読み取りに関連する情報が表示されます。

![Coprocessor read](/media/dashboard/dashboard-statement-plans-cop-read.png)

#### トランザクションタブ {#transaction-tab}

**[トランザクション]**タブをクリックすると、書き込まれたキーの平均数や書き込まれたキーの最大数など、実行プランとトランザクションに関連する情報が表示されます。

![Transaction](/media/dashboard/dashboard-statement-plans-transaction.png)

#### スロークエリタブ {#slow-query-tab}

実行プランの実行が遅すぎる場合は、[**スロー クエリ]**タブで関連するスロー クエリ レコードを確認できます。

![Slow Query](/media/dashboard/dashboard-statement-plans-slow-queries.png)

この領域に表示される情報は、スロークエリページと同じ構造です。詳細については[TiDB ダッシュボードの遅いクエリ ページ](/dashboard/dashboard-slow-query.md)を参照してください。
