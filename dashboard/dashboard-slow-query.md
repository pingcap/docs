---
title: Slow Queries Page of TiDB Dashboard
summary: TiDB ダッシュボードの「遅いクエリ」ページでは、クラスター内のすべてのスロー クエリを検索して表示できます。実行時間が300ミリ秒を超えるSQLクエリは低速クエリとみなされ、遅いクエリログに記録されます。スロー クエリ ログはデフォルトで有効になっており、システム変数を使用して有効または無効にできます。低速クエリのしきい値はセッション変数またはTiDBパラメータを通じて調整できます。TiDB ダッシュボードにログインした後、左側のナビゲーション メニューで「Slow Queries」をクリックするか、ブラウザで指定のURLにアクセスしてください。
---

# TiDB ダッシュボードの「遅いクエリ」ページ {#slow-queries-page-of-tidb-dashboard}

TiDB ダッシュボードの「スロー クエリ」ページでは、クラスター内のすべてのスロー クエリを検索して表示できます。

デフォルトでは、実行時間が 300 ミリ秒を超える SQL クエリは低速クエリとみなされます。これらのクエリは[遅いクエリログ](/identify-slow-queries.md)に記録され、TiDB ダッシュボード経由で検索できます。低速クエリのしきい値は、 [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)セッション変数または[`instance.tidb_slow_log_threshold`](/tidb-configuration-file.md#tidb_slow_log_threshold) TiDB パラメータを通じて調整できます。

> **注記：**
>
> スロークエリログが無効になっている場合、この機能は使用できません。スロー クエリ ログはデフォルトで有効になっており、システム変数[`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log)を使用して有効または無効にできます。

## ページにアクセスする {#access-the-page}

次の 2 つの方法のいずれかを使用して、低速クエリ ページにアクセスできます。

-   TiDB ダッシュボードにログインした後、左側のナビゲーション メニューで**[Slow Queries]**をクリックします。

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/slow_query](http://127.0.0.1:2379/dashboard/#/slow_query)にアクセスしてください。 `127.0.0.1:2379`実際の PD アドレスとポートに置き換えます。

スロー クエリ ページに表示されるすべてのデータは、TiDB スロー クエリ システム テーブルおよびスロー クエリ ログから取得されます。詳細については[遅いクエリログ](/identify-slow-queries.md)を参照してください。

### フィルターを変更する {#change-filters}

時間範囲、関連データベース、SQL キーワード、SQL タイプ、表示する低速クエリの数に基づいて低速クエリをフィルタリングできます。以下の画像では、最近 30 分間の 100 件の低速クエリがデフォルトで表示されています。

![Modify list filters](/media/dashboard/dashboard-slow-queries-list1-v620.png)

### さらに多くの列を表示する {#display-more-columns}

ページ上の**[列]**をクリックすると、さらに列を表示することを選択できます。列名の右側にある**(i)**アイコンにマウスを移動すると、この列の説明が表示されます。

![Show more columns](/media/dashboard/dashboard-slow-queries-list2-v620.png)

### 遅いクエリをローカルにエクスポートする {#export-slow-queries-locally}

ページの右上隅にある ☰ ( [**詳細**] ) をクリックして、 **[エクスポート]**オプションを表示します。 **[エクスポート]**をクリックすると、TiDB ダッシュボードは現在のリスト内の低速クエリを CSV ファイルとしてエクスポートします。

![Export slow queries locally](/media/dashboard/dashboard-slow-queries-export-v651.png)

### 列ごとに並べ替える {#sort-by-column}

デフォルトでは、リストは**終了時間の**降順に並べ替えられます。列見出しをクリックして列で並べ替えるか、並べ替え順序を切り替えます。

![Modify sorting basis](/media/dashboard/dashboard-slow-queries-list3-v620.png)

## 実行の詳細をビュー {#view-execution-details}

リスト内の任意の項目をクリックすると、次のような遅いクエリの詳細な実行情報が表示されます。

-   クエリ: SQL ステートメントのテキスト (次の図の領域 1)
-   プラン: 低速クエリの実行プラン (次の図の領域 2)
-   その他のソート済みSQL実行情報（下図の領域3）

![View execution details](/media/dashboard/dashboard-slow-queries-detail1-v620.png)

### SQL {#sql}

> **注記：**
>
> `Query`列に記録されるクエリの最大長は、 [`tidb_stmt_summary_max_sql_length`](/system-variables.md#tidb_stmt_summary_max_sql_length-new-in-v40)システム変数によって制限されます。

**「展開」**ボタンをクリックすると、項目の詳細情報が表示されます。 **「コピー」**ボタンをクリックすると、詳細情報がクリップボードにコピーされます。

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

![Basic information](/media/dashboard/dashboard-slow-queries-detail-plans-basic.png)

#### 「時間」タブ {#time-tab}

**[時間]**タブをクリックすると、実行計画の各ステージの所要時間を確認できます。

> **注記：**
>
> 一部の操作は単一の SQL ステートメント内で並行して実行される場合があるため、各ステージの累積所要時間は SQL ステートメントの実際の実行時間を超える可能性があります。

![Execution time](/media/dashboard/dashboard-slow-queries-detail-plans-time.png)

#### 「コプロセッサー」タブ {#coprocessor-tab}

**[コプロセッサー]**タブをクリックすると、コプロセッサー読み取りに関連する情報が表示されます。

![Coprocessor read](/media/dashboard/dashboard-slow-queries-detail-plans-cop-read.png)

#### トランザクションタブ {#transaction-tab}

**「トランザクション」**タブをクリックすると、書き込まれたキーの平均数や書き込まれたキーの最大数など、実行計画とトランザクションに関連する情報が表示されます。

![Transaction](/media/dashboard/dashboard-slow-queries-detail-plans-transaction.png)
