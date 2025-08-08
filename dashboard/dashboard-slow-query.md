---
title: Slow Queries Page of TiDB Dashboard
summary: TiDBダッシュボードの「スロークエリ」ページでは、クラスター内のスロークエリを検索・表示できます。実行時間が300ミリ秒を超えるクエリは「スロー」とみなされます。ユーザーはしきい値を調整し、ダッシュボードまたはブラウザからこのページにアクセスできます。また、フィルターの変更、表示列の追加、クエリのエクスポート、実行の詳細の表示も可能です。
---

# TiDBダッシュボードのスロークエリページ {#slow-queries-page-of-tidb-dashboard}

TiDB ダッシュボードの「スロー クエリ」ページでは、クラスター内のすべてのスロー クエリを検索して表示できます。

デフォルトでは、実行時間が300ミリ秒を超えるSQLクエリはスロークエリとみなされます。これらのクエリは[スロークエリログ](/identify-slow-queries.md)に記録され、TiDBダッシュボードから検索できます。スロークエリのしきい値は、 [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)セッション変数または[`instance.tidb_slow_log_threshold`](/tidb-configuration-file.md#tidb_slow_log_threshold)パラメータで調整できます。

> **注記：**
>
> スロークエリログが無効になっている場合、この機能は使用できません。スロークエリログはデフォルトで有効になっており、システム変数[`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log)を使って有効または無効にすることができます。

## ページにアクセスする {#access-the-page}

スロー クエリ ページにアクセスするには、次の 2 つの方法のいずれかを使用できます。

-   TiDB ダッシュボードにログインしたら、左側のナビゲーション メニューで**[Slow Queries]**をクリックします。

-   ブラウザで[http://127.0.0.1:2379/ダッシュボード/#/slow_query](http://127.0.0.1:2379/dashboard/#/slow_query)アクセスしてください。3 `127.0.0.1:2379`実際のPDアドレスとポートに置き換えてください。

スロークエリページに表示されるすべてのデータは、TiDBスロークエリシステムテーブルとスロークエリログから取得されます。詳細は[スロークエリログ](/identify-slow-queries.md)ご覧ください。

### フィルターを変更する {#change-filters}

スロークエリは、時間範囲、関連データベース、SQLキーワード、SQLタイプ、表示するスロークエリの数に基づいてフィルタリングできます。下の画像では、デフォルトで過去30分間のスロークエリ100件が表示されています。

![Modify list filters](/media/dashboard/dashboard-slow-queries-list1-v620.png)

### より多くの列を表示する {#display-more-columns}

ページ上の**「列」**をクリックすると、さらに列を表示できます。列名の右側にある**(i)**アイコンにマウスを移動すると、その列の説明が表示されます。

![Show more columns](/media/dashboard/dashboard-slow-queries-list2-v620.png)

### 遅いクエリをローカルにエクスポートする {#export-slow-queries-locally}

ページの右上隅にある☰（**その他**）をクリックすると、 **「エクスポート」**オプションが表示されます。 **「エクスポート」**をクリックすると、TiDBダッシュボードは現在のリストにあるスロークエリをCSVファイルとしてエクスポートします。

![Export slow queries locally](/media/dashboard/dashboard-slow-queries-export-v651.png)

### 列で並べ替え {#sort-by-column}

デフォルトでは、リストは**終了時間**の降順で並び替えられます。列見出しをクリックすると、列ごとに並び替えたり、並び替え順を変更したりできます。

![Modify sorting basis](/media/dashboard/dashboard-slow-queries-list3-v620.png)

## 実行の詳細をビュー {#view-execution-details}

リスト内の任意の項目をクリックすると、次のような遅いクエリの詳細な実行情報が表示されます。

-   クエリ: SQL文のテキスト（次の図の領域1）
-   プラン: 遅いクエリの実行プラン (次の図の領域 2)
-   その他のソートされたSQL実行情報（次の図の領域3）

![View execution details](/media/dashboard/dashboard-slow-queries-detail1-v620.png)

### SQL {#sql}

> **注記：**
>
> `Query`列に記録されるクエリの最大長は、 [`tidb_stmt_summary_max_sql_length`](/system-variables.md#tidb_stmt_summary_max_sql_length-new-in-v40)システム変数によって制限されます。

**「展開」**ボタンをクリックすると、アイテムの詳細情報が表示されます。 **「コピー」**ボタンをクリックすると、詳細情報がクリップボードにコピーされます。

### 実行計画 {#execution-plans}

TiDBダッシュボードでは、実行計画を表、テキスト、グラフの3つの方法で表示できます。実行計画の読み方については、 [クエリ実行プランを理解する](/explain-overview.md)ご覧ください。

#### 表形式の実行計画 {#execution-plan-in-table-format}

表形式では実行計画に関する詳細情報が提供されるため、異常なオペレータメトリクスを迅速に特定し、異なるオペレータのステータスを比較するのに役立ちます。次の図は、表形式での実行計画を示しています。

![Execution plan in table format](/media/dashboard/dashboard-table-plan.png)

表形式ではテキスト形式と同様の情報が表示されますが、よりユーザーフレンドリーな操作が提供されます。

-   列幅は自由に調整できます。
-   コンテンツが列幅を超えると、自動的に切り捨てられ、完全な情報のツールヒントが表示されます。
-   実行プランが大きい場合は、ローカル分析用にテキスト ファイルとしてダウンロードできます。
-   列ピッカーを使用して列を非表示にしたり管理したりできます。

![Execution plan in table format - column picker](/media/dashboard/dashboard-table-plan-columnpicker.png)

#### グラフ形式の実行計画 {#execution-plan-in-graph-format}

グラフ形式は、複雑なSQL文の実行計画ツリーを表示し、各演算子とその内容を詳細に理解するのに適しています。次の図は、グラフ形式の実行計画を示しています。

![Execution plan in graph format](/media/dashboard/dashboard-visual-plan-2.png)

-   グラフには、左から右、上から下への実行が表示されます。
-   上位ノードは親演算子であり、下位ノードは子演算子です。
-   タイトル バーの色は、演算子が実行されるコンポーネントを示します。黄色は TiDB、青は TiKV、ピンクはTiFlashを表します。
-   タイトル バーにはオペレーターの名前が表示され、その下に表示されるテキストはオペレーターの基本情報です。

ノード領域をクリックすると、右側のサイドバーにオペレータの詳細情報が表示されます。

![Execution plan in graph format - sidebar](/media/dashboard/dashboard-visual-plan-popup.png)

### SQL実行の詳細 {#sql-execution-details}

SQL ステートメントの基本情報、実行時間、コプロセッサー読み取り、トランザクション、および低速クエリについては、対応するタブ タイトルをクリックして、さまざまな情報を切り替えることができます。

![Show different execution information](/media/dashboard/dashboard-slow-queries-detail2-v620.png)

#### 基本タブ {#basic-tab}

SQL実行の基本情報には、テーブル名、インデックス名、実行回数、合計レイテンシーが含まれます。 **「説明」**列には各フィールドの詳細な説明が表示されます。

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
