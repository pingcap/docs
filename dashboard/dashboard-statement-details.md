---
title: Statement Execution Details of TiDB Dashboard
summary: View the execution details of a single SQL statement in TiDB Dashboard.
---

# TiDB ダッシュボードのステートメント実行の詳細 {#statement-execution-details-of-tidb-dashboard}

リスト内の任意の項目をクリックして SQL ステートメントの詳細ページに入り、より詳細な情報を表示します。この情報には次の部分が含まれます。

-   SQL ステートメントの概要。これには、SQL テンプレート、SQL テンプレート ID、表示される SQL 実行の現在の時間範囲、実行プランの数、SQL ステートメントが実行されるデータベース、および高速プラン バインディング機能 (エリア) が含まれます。次の図の 1)。
-   実行計画リスト: SQL ステートメントに複数の実行計画がある場合、このリストが表示されます。 TiDB v6.2.0 では、実行計画のテキスト情報に加えて、視覚的な実行計画が導入されており、これによりステートメントの各演算子や詳細情報をより直観的に学ぶことができます。さまざまな実行プランを選択でき、選択したプランの詳細がリストの下に表示されます (次の図の領域 2)。
-   プランの実行の詳細。選択した実行プランの詳細情報が表示されます。 [実行計画の詳細](#execution-details-of-plans) (次の図の領域 3) を参照してください。

![Details](/media/dashboard/dashboard-statement-detail-v660.png)

## 高速プランバインディング {#fast-plan-binding}

v6.6.0 以降、TiDB には高速プラン バインディング機能が導入されています。 TiDB ダッシュボードで SQL ステートメントを特定の実行プランにすばやくバインドできます。

### 使用法 {#usage}

#### 実行計画をバインドする {#bind-an-execution-plan}

1.  **「計画のバインド」**をクリックします。 **[プランのバインド]**ダイアログ ボックスが表示されます。

    ![Fast plan binding - not bound - entry](/media/dashboard/dashboard-quick-binding-entry-notbound.png)

2.  バインドするプランを選択し、 **「バインド」を**クリックします。

    ![Fast plan binding - popup](/media/dashboard/dashboard-quick-binding-popup-notbound.png)

3.  バインドが完了すると、 **「Bound」**ラベルが表示されます。

    ![Fast plan binding - popup - binding completed](/media/dashboard/dashboard-quick-binding-popup-bound.png)

#### 既存のバインディングを削除する {#drop-an-existing-binding}

1.  既存のバインドがある SQL ステートメントのページで、 **「バインディングの計画」**をクリックします。 **[プランのバインド]**ダイアログ ボックスが表示されます。

    ![Fast plan binding - bound - entry](/media/dashboard/dashboard-quick-binding-entry-bound.png)

2.  **[ドロップ]**をクリックします。

    ![Fast plan binding - popup - bound](/media/dashboard/dashboard-quick-binding-popup-bound.png)

3.  バインディングが削除されると、 **「未バインド」**ラベルが表示されます。

    ![Fast plan binding - popup](/media/dashboard/dashboard-quick-binding-popup-notbound.png)

### 制限 {#limitation}

現在、高速プラン バインディング機能は、次のタイプの SQL ステートメントをサポートしていません。

-   `SELECT` 、 `DELETE` 、 `UPDATE` 、 `INSERT` 、または`REPLACE`ではないステートメント
-   サブクエリを含むクエリ
-   TiFlashにアクセスするクエリ
-   3 つ以上のテーブルを結合するクエリ

この機能を使用するには、SUPER 権限が必要です。使用中に権限の問題が発生した場合は、 [TiDB ダッシュボードのユーザー管理](/dashboard/dashboard-user.md)を参照して必要な権限を追加してください。

## 計画の実行内容 {#execution-details-of-plans}

プランの実行の詳細には、次の情報が含まれます。

-   SQL サンプル: 計画に応じて実際に実行される特定の SQL 文のテキスト。時間範囲内に実行された SQL ステートメントは、SQL サンプルとして使用される可能性があります。
-   実行計画: 実行計画に関する完全な情報が表、グラフ、テキストで表示されます。実行計画の詳細については、 [クエリ実行計画を理解する](/explain-overview.md)を参照してください。複数の実行プランが選択されている場合は、そのうちの (いずれか) 1 つだけが表示されます。
-   SQL ステートメントの基本情報、実行時間、コプロセッサー読み取り、トランザクション、低速クエリについては、対応するタブ タイトルをクリックしてさまざまな情報を切り替えることができます。

![Execution details of plans](/media/dashboard/dashboard-statement-plans-detail.png)

### SQLサンプル {#sql-sample}

項目の詳細情報を表示するには、 **「展開」**をクリックします。詳細情報をクリップボードにコピーするには、 **「コピー」を**クリックします。

### 実行計画 {#execution-plans}

TiDB ダッシュボードでは、表、テキスト、グラフの 3 つの方法で実行計画を表示できます。実行計画の見方については、 [クエリ実行計画を理解する](/explain-overview.md)を参照してください。

#### 表形式の実行計画 {#execution-plan-in-table-format}

表形式では、実行計画に関する詳細情報が提供されるため、異常なオペレーター メトリックを迅速に特定し、さまざまなオペレーターのステータスを比較するのに役立ちます。次の図は、実行計画を表形式で示しています。

![Execution plan in table format](/media/dashboard/dashboard-table-plan.png)

表形式ではテキスト形式と同様の情報が表示されますが、よりユーザーフレンドリーな操作が可能です。

-   列幅を自由に調整できます。
-   コンテンツが列幅を超えると、コンテンツは自動的に切り詰められ、完全な情報がツールチップに表示されます。
-   実行プランが大きい場合は、ローカル分析用にテキスト ファイルとしてダウンロードできます。
-   列ピッカーを使用して列を非表示にしたり管理したりできます。

![Execution plan in table format - column picker](/media/dashboard/dashboard-table-plan-columnpicker.png)

#### 実行計画をグラフ形式で表示 {#execution-plan-in-graph-format}

グラフ形式は、複雑な SQL ステートメントの実行計画ツリーを表示し、各演算子とそれに対応する内容を詳細に理解するのに適しています。次の図は、実行計画をグラフ形式で示しています。

![Execution plan in graph format](/media/dashboard/dashboard-visual-plan-2.png)

-   グラフは、左から右、上から下の順に実行を示します。
-   上位ノードは親演算子、下位ノードは子演算子です。
-   タイトル バーの色は、オペレーターが実行されるコンポーネントを示します。黄色は TiDB を表し、青は TiKV を表し、ピンクはTiFlashを表します。
-   タイトルバーにはオペレーター名が表示され、その下のテキストはオペレーターの基本情報です。

ノードエリアをクリックすると、右側のサイドバーにオペレータの詳細情報が表示されます。

![Execution plan in graph format - sidebar](/media/dashboard/dashboard-visual-plan-popup.png)

### SQL実行の詳細 {#sql-execution-details}

SQL ステートメントの基本情報、実行時間、コプロセッサー読み取り、トランザクション、低速クエリについては、対応するタブ タイトルをクリックしてさまざまな情報を切り替えることができます。

![Show different execution information](/media/dashboard/dashboard-slow-queries-detail2-v620.png)

#### 基本タブ {#basic-tab}

SQL 実行の基本情報には、テーブル名、インデックス名、実行回数、合計レイテンシーが含まれます。 **「説明」**列には、各フィールドの詳細な説明が記載されています。

![Basic information](/media/dashboard/dashboard-statement-plans-basic.png)

#### 「時間」タブ {#time-tab}

**[時間]**タブをクリックすると、実行計画の各ステージの所要時間を確認できます。

> **注記：**
>
> 一部の操作は 1 つの SQL ステートメント内で並行して実行される場合があるため、各ステージの累積所要時間は SQL ステートメントの実際の実行時間を超える可能性があります。

![Execution time](/media/dashboard/dashboard-statement-plans-time.png)

#### コプロセッサー読み取りタブ {#coprocessor-read-tab}

**[コプロセッサー読み取り]**タブをクリックすると、コプロセッサー読み取りに関連する情報が表示されます。

![Coprocessor read](/media/dashboard/dashboard-statement-plans-cop-read.png)

#### トランザクションタブ {#transaction-tab}

**「トランザクション」**タブをクリックすると、書き込まれたキーの平均数や書き込まれたキーの最大数など、実行計画とトランザクションに関連する情報が表示されます。

![Transaction](/media/dashboard/dashboard-statement-plans-transaction.png)

#### 「スロークエリ」タブ {#slow-query-tab}

実行プランの実行が遅すぎる場合は、 **[スロー クエリ]**タブに関連するスロー クエリ レコードが表示されます。

![Slow Query](/media/dashboard/dashboard-statement-plans-slow-queries.png)

この領域に表示される情報は、スロー クエリ ページと同じ構造になっています。詳細については[TiDB ダッシュボードの低速クエリ ページ](/dashboard/dashboard-slow-query.md)を参照してください。
