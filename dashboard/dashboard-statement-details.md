---
title: Statement Execution Details of TiDB Dashboard
summary: View the execution details of a single SQL statement in TiDB Dashboard.
---

# TiDBダッシュボードのステートメント実行の詳細 {#statement-execution-details-of-tidb-dashboard}

リスト内の任意の項目をクリックしてSQLステートメントの詳細ページに入り、より詳細な情報を表示します。この情報には、次の部分が含まれます。

-   SQLテンプレート、SQLテンプレートID、表示されたSQL実行の現在の時間範囲、実行プランの数、およびSQLステートメントが実行されるデータベースを含むSQLステートメントの概要（下の画像の領域1を参照） 。
-   実行プランリスト：SQLステートメントに複数の実行プランがある場合、このリストが表示されます。さまざまな実行プランを選択でき、選択したプランの詳細がリストの下に表示されます。実行プランが1つしかない場合、リストは表示されません（以下の領域2を参照）。
-   選択した実行プランの詳細情報を表示するプランの実行詳細。 [実行計画の詳細](#execution-details-of-plans) （下の画像の領域3）を参照してください。

![Details](/media/dashboard/dashboard-statement-detail.png)

## 計画の実行の詳細 {#execution-details-of-plans}

計画の実行の詳細には、次の情報が含まれます。

-   SQLサンプル：プランに対応して実際に実行される特定のSQLステートメントのテキスト。時間範囲内に実行されたSQLステートメントは、SQLサンプルとして使用できます。
-   実行計画：実行計画の詳細については、 [クエリ実行プランを理解する](/explain-overview.md)を参照してください。複数の実行プランを選択すると、そのうちの1つだけが表示されます。
-   SQLステートメントの基本情報、実行時間、コプロセッサー読み取り、トランザクション、および低速クエリについては、対応するタブのタイトルをクリックして、さまざまな情報を切り替えることができます。

![Execution details of plans](/media/dashboard/dashboard-statement-plans-detail.png)

### 基本タブ {#basic-tab}

SQL実行の基本情報には、テーブル名、インデックス名、実行カウント、および合計待機時間が含まれます。 [**説明**]列には、各フィールドの詳細な説明が表示されます。

![Basic information](/media/dashboard/dashboard-statement-plans-basic.png)

### 時間タブ {#time-tab}

[**時間**]タブをクリックすると、実行プランの各段階がどのくらい続くかを確認できます。

> **ノート：**
>
> 一部の操作は単一のSQLステートメント内で並行して実行される可能性があるため、各ステージの累積期間がSQLステートメントの実際の実行時間を超える可能性があります。

![Execution time](/media/dashboard/dashboard-statement-plans-time.png)

### コプロセッサー読み取りタブ {#coprocessor-read-tab}

「**コプロセッサー読み取り」**タブをクリックすると、コプロセッサー読み取りに関連する情報が表示されます。

![Coprocessor read](/media/dashboard/dashboard-statement-plans-cop-read.png)

### [トランザクション]タブ {#transaction-tab}

[**トランザクション**]タブをクリックすると、書き込まれたキーの平均数や書き込まれたキーの最大数など、実行プランとトランザクションに関連する情報が表示されます。

![Transaction](/media/dashboard/dashboard-statement-plans-transaction.png)

### 遅いクエリタブ {#slow-query-tab}

実行プランの実行が遅すぎる場合は、[**低速クエリ**]タブで関連する低速クエリレコードを確認できます。

![Slow Query](/media/dashboard/dashboard-statement-plans-slow-queries.png)

この領域に表示される情報は、低速クエリページと同じ構造になっています。詳細については、 [TiDBダッシュボードの遅いクエリページ](/dashboard/dashboard-slow-query.md)を参照してください。
