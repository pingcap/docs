---
title: Slow Queries Page of TiDB Dashboard
summary: TiDB ダッシュボードの「低速クエリ」ページでは、クラスター内の低速クエリを検索して表示できます。実行時間が 300 ミリ秒を超えるクエリは低速とみなされます。ユーザーはしきい値を調整し、ダッシュボードまたはブラウザからページにアクセスできます。また、フィルターを変更したり、列をさらに表示したり、クエリをエクスポートしたり、実行の詳細を表示したりすることもできます。
---

# TiDBダッシュボードの低速クエリページ {#slow-queries-page-of-tidb-dashboard}

TiDB ダッシュボードの「スロー クエリ」ページでは、クラスター内のすべてのスロー クエリを検索して表示できます。

デフォルトでは、実行時間が 300 ミリ秒を超える SQL クエリは低速クエリと見なされます。これらのクエリは[スロークエリログ](/identify-slow-queries.md)に記録され、TiDB ダッシュボードで検索できます。低速クエリのしきい値は、 [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)セッション変数または[`instance.tidb_slow_log_threshold`](/tidb-configuration-file.md#tidb_slow_log_threshold) TiDB パラメータで調整できます。

> **注記：**
>
> スロー クエリ ログが無効になっている場合、この機能は使用できません。スロー クエリ ログはデフォルトで有効になっており、システム変数[`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log)を使用して有効または無効にすることができます。

## ページにアクセスする {#access-the-page}

スロー クエリ ページにアクセスするには、次の 2 つの方法のいずれかを使用できます。

-   TiDB ダッシュボードにログインしたら、左側のナビゲーション メニューで**「Slow Queries」**をクリックします。

-   ブラウザで[http://127.0.0.1:2379/ダッシュボード/#/slow_query](http://127.0.0.1:2379/dashboard/#/slow_query)アクセスします。3 `127.0.0.1:2379`実際の PD アドレスとポートに置き換えます。

スロー クエリ ページに表示されるすべてのデータは、TiDB スロー クエリ システム テーブルとスロー クエリ ログから取得されます。詳細については、 [スロークエリログ](/identify-slow-queries.md)参照してください。

### フィルターを変更する {#change-filters}

時間範囲、関連データベース、SQL キーワード、SQL タイプ、表示するスロークエリの数に基づいて、スロークエリをフィルタリングできます。下の画像では、デフォルトで、最近 30 分間の 100 件のスロークエリが表示されています。

![Modify list filters](/media/dashboard/dashboard-slow-queries-list1-v620.png)

### より多くの列を表示する {#display-more-columns}

ページの**「列」**をクリックすると、さらに列を表示できます。列名の右側にある**(i)**アイコンにマウスを移動すると、その列の説明が表示されます。

![Show more columns](/media/dashboard/dashboard-slow-queries-list2-v620.png)

### 遅いクエリをローカルにエクスポートする {#export-slow-queries-locally}

ページの右上隅にある ☰ (**詳細**) をクリックすると、**エクスポート**オプションが表示されます。**エクスポート**をクリックすると、TiDB ダッシュボードは現在のリストにあるスロー クエリを CSV ファイルとしてエクスポートします。

![Export slow queries locally](/media/dashboard/dashboard-slow-queries-export-v651.png)

### 列で並べ替え {#sort-by-column}

デフォルトでは、リストは**終了時間**の降順で並べ替えられます。列見出しをクリックして列で並べ替えるか、並べ替え順序を切り替えます。

![Modify sorting basis](/media/dashboard/dashboard-slow-queries-list3-v620.png)

## 実行の詳細をビュー {#view-execution-details}

リスト内の任意の項目をクリックすると、次のような遅いクエリの詳細な実行情報が表示されます。

-   クエリ: SQL文のテキスト（次の図の領域1）
-   プラン: 遅いクエリの実行プラン (次の図の領域 2)
-   その他のソートされたSQL実行情報（下図の領域3）

![View execution details](/media/dashboard/dashboard-slow-queries-detail1-v620.png)

### 構文 {#sql}

> **注記：**
>
> `Query`列に記録されるクエリの最大長は、 [`tidb_stmt_summary_max_sql_length`](/system-variables.md#tidb_stmt_summary_max_sql_length-new-in-v40)システム変数によって制限されます。

アイテムの詳細情報を表示するには、「**展開」**ボタンをクリックします。詳細情報をクリップボードにコピーするには、「**コピー」**ボタンをクリックします。

### 実行計画 {#execution-plans}

TiDB ダッシュボードでは、実行プランをテーブル、テキスト、グラフの 3 つの方法で表示できます。実行プランの読み方については、 [クエリ実行プランを理解する](/explain-overview.md)参照してください。

#### 表形式の実行計画 {#execution-plan-in-table-format}

テーブル形式では、実行プランに関する詳細情報が提供され、異常なオペレーター メトリックをすばやく特定し、さまざまなオペレーターのステータスを比較するのに役立ちます。次の図は、テーブル形式の実行プランを示しています。

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

![Basic information](/media/dashboard/dashboard-slow-queries-detail-plans-basic.png)

#### 時間タブ {#time-tab}

**[時間]**タブをクリックすると、実行プランの各ステージの所要時間を確認できます。

> **注記：**
>
> 一部の操作は単一の SQL ステートメント内で並行して実行される可能性があるため、各ステージの累積実行時間は SQL ステートメントの実際の実行時間を超える可能性があります。

![Execution time](/media/dashboard/dashboard-slow-queries-detail-plans-time.png)

#### コプロセッサータブ {#coprocessor-tab}

**「コプロセッサー」**タブをクリックすると、コプロセッサーの読み取りに関連する情報が表示されます。

![Coprocessor read](/media/dashboard/dashboard-slow-queries-detail-plans-cop-read.png)

#### トランザクションタブ {#transaction-tab}

**[トランザクション]**タブをクリックすると、書き込まれたキーの平均数や書き込まれたキーの最大数など、実行プランとトランザクションに関連する情報が表示されます。

![Transaction](/media/dashboard/dashboard-slow-queries-detail-plans-transaction.png)
