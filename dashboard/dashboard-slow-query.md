---
title: Slow Queries Page of TiDB Dashboard
summary: TiDBダッシュボードの「低速クエリ」ページでは、クラスタ内の低速クエリを検索して表示できます。実行時間が300ミリ秒を超えるクエリは低速とみなされます。ユーザーはしきい値を調整したり、ダッシュボードまたはブラウザからこのページにアクセスしたりできます。また、フィルタの変更、表示する列の追加、クエリのエクスポート、実行の詳細の表示も可能です。
---

# TiDBダッシュボードの低速クエリページ {#slow-queries-page-of-tidb-dashboard}

TiDBダッシュボードの「低速クエリ」ページでは、クラスタ内のすべての低速クエリを検索して表示できます。

デフォルトでは、実行時間が300ミリ秒を超えるSQLクエリはスロークエリとみなされます。これらのクエリは[スロークエリログ](/identify-slow-queries.md)に記録され、TiDBダッシュボードから検索できます。スロークエリのしきい値は、セッション変数[`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)またはTiDBパラメータ[`instance.tidb_slow_log_threshold`](/tidb-configuration-file.md#tidb_slow_log_threshold)で調整できます。

> **注記：**
>
> スロークエリログが無効になっている場合、この機能は利用できません。スロークエリログはデフォルトで有効になっており、システム変数[`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log)使用して有効または無効にすることができます。

## ページにアクセスしてください {#access-the-page}

低速クエリページにアクセスするには、以下の2つの方法のいずれかを使用できます。

-   TiDBダッシュボードにログイン後、左側のナビゲーションメニューにある**「低速クエリ」**をクリックします。

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/slow_query](http://127.0.0.1:2379/dashboard/#/slow_query)にアクセスしてください。 `127.0.0.1:2379`実際の PD アドレスとポートに置き換えてください。

スロー クエリ ページに表示されるすべてのデータは、TiDB スロー クエリ システム テーブルおよびスロー クエリ ログから取得されます。詳細については[スロークエリログ](/identify-slow-queries.md)を参照してください。

### フィルターを変更する {#change-filters}

低速クエリは、時間範囲、関連データベース、SQLキーワード、SQLタイプ、表示する低速クエリの数に基づいてフィルタリングできます。下の画像では、デフォルトで直近30分間の低速クエリ100件が表示されています。

![Modify list filters](/media/dashboard/dashboard-slow-queries-list1-v620.png)

### 列をさらに表示 {#display-more-columns}

ページ上の**「列」**をクリックすると、さらに多くの列を表示できます。列名の右側にある**（i）**アイコンにマウスカーソルを合わせると、その列の説明が表示されます。

![Show more columns](/media/dashboard/dashboard-slow-queries-list2-v620.png)

### 遅いクエリをローカルにエクスポートする {#export-slow-queries-locally}

ページ右上隅の☰（**その他**）をクリックすると、**エクスポート**オプションが表示されます。**エクスポートを**クリックすると、TiDB Dashboardは現在のリストにある低速クエリをCSVファイルとしてエクスポートします。

![Export slow queries locally](/media/dashboard/dashboard-slow-queries-export-v651.png)

### 列で並べ替え {#sort-by-column}

デフォルトでは、リストは**終了時刻**の降順でソートされています。列見出しをクリックすると、その列でソートしたり、ソート順を切り替えたりできます。

![Modify sorting basis](/media/dashboard/dashboard-slow-queries-list3-v620.png)

## 実行の詳細をビュー {#view-execution-details}

リスト内のいずれかの項目をクリックすると、以下の項目を含む、遅いクエリの詳細な実行情報が表示されます。

-   クエリ：SQL文のテキスト（下図の領域1）
-   計画：遅いクエリの実行計画（下図の領域2）
-   その他のソート済みSQL実行情報（下図の領域3）

![View execution details](/media/dashboard/dashboard-slow-queries-detail1-v620.png)

### SQL {#sql}

> **注記：**
>
> -   `Query`列に記録されるクエリの最大長は、 [`tidb_stmt_summary_max_sql_length`](/system-variables.md#tidb_stmt_summary_max_sql_length-new-in-v40)システム変数によって制限されます。
> -   準備済みステートメントの場合、引数はクエリの末尾にリストされます。例: `[arguments: "foo", 123]` 。印刷不可能な引数は、16 進数のリテラルとして表示されます。例: `0x01` 。

アイテムの詳細情報を表示するには、 **「展開」**ボタンをクリックします。詳細情報をクリップボードにコピーするには、 **「コピー」**ボタンをクリックします。

### 実行計画 {#execution-plans}

TiDB ダッシュボードでは、表、テキスト、グラフの 3 つの方法で実行計画を表示できます。実行計画の読み方については、[クエリ実行プランを理解する](/explain-overview.md)参照してください。

#### 実行計画を表形式で表示 {#execution-plan-in-table-format}

表形式では実行計画に関する詳細情報が提供されるため、異常なオペレータメトリクスを迅速に特定し、異なるオペレータの状態を比較するのに役立ちます。次の図は、表形式で表された実行計画を示しています。

![Execution plan in table format](/media/dashboard/dashboard-table-plan.png)

表形式はテキスト形式と同様の情報を表示しますが、よりユーザーフレンドリーな操作性を提供します。

-   列幅は自由に調整できます。
-   コンテンツが列幅を超えると、自動的に切り詰められ、完全な情報を示すツールチップが表示されます。
-   実行計画が大きい場合は、テキストファイルとしてダウンロードしてローカルで分析できます。
-   列選択ツールを使用して、列を非表示にしたり管理したりできます。

![Execution plan in table format - column picker](/media/dashboard/dashboard-table-plan-columnpicker.png)

#### 実行計画をグラフ形式で表示 {#execution-plan-in-graph-format}

グラフ形式は、複雑なSQL文の実行計画ツリーを表示し、各演算子とその対応する内容を詳細に理解するのに適しています。次の図は、グラフ形式で表した実行計画を示しています。

![Execution plan in graph format](/media/dashboard/dashboard-visual-plan-2.png)

-   グラフは、左から右、上から下の順に実行状況を示しています。
-   上位ノードは親演算子、下位ノードは子演算子です。
-   タイトルバーの色は、オペレーターが実行されるコンポーネントを示します。黄色はTiDB、青はTiKV、ピンクはTiFlashを表します。
-   タイトルバーにはオペレーター名が表示され、その下に表示されるテキストはオペレーターの基本情報です。

ノード領域をクリックすると、詳細なオペレーター情報が右側のサイドバーに表示されます。

![Execution plan in graph format - sidebar](/media/dashboard/dashboard-visual-plan-popup.png)

### SQL実行の詳細 {#sql-execution-details}

基本的な情報、実行時間、コプロセッサーの読み取り、トランザクション、SQL文の低速クエリについては、対応するタブタイトルをクリックして、さまざまな情報を切り替えることができます。

![Show different execution information](/media/dashboard/dashboard-slow-queries-detail2-v620.png)

#### 基本タブ {#basic-tab}

SQL実行の基本情報には、テーブル名、インデックス名、実行回数、および合計レイテンシーが含まれます。**説明**列には、各フィールドの詳細な説明が表示されます。

![Basic information](/media/dashboard/dashboard-slow-queries-detail-plans-basic.png)

#### タイムタブ {#time-tab}

「**時間」**タブをクリックすると、実行計画の各段階にかかる時間を確認できます。

> **注記：**
>
> 単一のSQL文内で一部の操作が並行して実行される場合があるため、各段階の累積実行時間は、SQL文の実際の実行時間を超える可能性があります。

![Execution time](/media/dashboard/dashboard-slow-queries-detail-plans-time.png)

#### コプロセッサータブ {#coprocessor-tab}

**「コプロセッサー」**タブをクリックすると、コプロセッサーの読み取りに関する情報が表示されます。

![Coprocessor read](/media/dashboard/dashboard-slow-queries-detail-plans-cop-read.png)

#### トランザクションタブ {#transaction-tab}

**「トランザクション」**タブをクリックすると、実行計画やトランザクションに関する情報（平均書き込みキー数や最大書き込みキー数など）が表示されます。

![Transaction](/media/dashboard/dashboard-slow-queries-detail-plans-transaction.png)
