---
title: Statement Execution Details of TiDB Dashboard
summary: View the execution details of a single SQL statement in TiDB Dashboard.
---

# TiDB ダッシュボードのステートメント実行の詳細 {#statement-execution-details-of-tidb-dashboard}

リスト内の任意の項目をクリックして、SQL ステートメントの詳細ページに入り、より詳細な情報を表示します。この情報には、次の部分が含まれます。

-   SQL テンプレート、SQL テンプレート ID、表示されている SQL 実行の現在の時間範囲、実行計画の数、および SQL ステートメントが実行されるデータベースを含む、SQL ステートメントの概要 (次の図の領域 1)。
-   実行計画リスト: SQL ステートメントに複数の実行計画がある場合、このリストが表示されます。 TiDB v6.2.0 では、実行計画のテキスト情報に加えて、ステートメントの各演算子と詳細情報をより直感的に学習できる視覚的な実行計画が導入されています。さまざまな実行計画を選択できます。選択した計画の詳細がリストの下に表示されます (次の図の領域 2)。
-   計画の実行の詳細。選択した実行計画の詳細情報が表示されます。 [実行計画の詳細](#execution-details-of-plans) (次の図の領域 3) を参照してください。

![Details](/media/dashboard/dashboard-statement-detail-v620.png)

## 計画の実行内容 {#execution-details-of-plans}

計画の実行の詳細には、次の情報が含まれます。

-   SQL サンプル: 計画に対応して実際に実行される特定の SQL ステートメントのテキスト。時間範囲内に実行された SQL ステートメントは、SQL サンプルとして使用される場合があります。
-   実行計画: グラフとテキストで表示される実行計画に関する完全な情報。実行計画の詳細については、 [クエリ実行計画を理解する](/explain-overview.md)を参照してください。複数の実行計画が選択されている場合は、そのうちの 1 つ (いずれか) のみが表示されます。
-   SQL ステートメントの基本情報、実行時間、コプロセッサー読み取り、トランザクション、およびスロー クエリについては、対応するタブ タイトルをクリックして、さまざまな情報に切り替えることができます。

![Execution details of plans](/media/dashboard/dashboard-statement-plans-detail.png)

### 基本タブ {#basic-tab}

SQL 実行の基本情報には、テーブル名、インデックス名、実行回数、および合計レイテンシーが含まれます。 **[説明]**列には、各フィールドの詳細な説明が表示されます。

![Basic information](/media/dashboard/dashboard-statement-plans-basic.png)

### 時間タブ {#time-tab}

**[時間]**タブをクリックすると、実行計画の各段階の継続時間を確認できます。

> **ノート：**
>
> 一部の操作は単一の SQL ステートメント内で並行して実行される可能性があるため、各ステージの累積期間が SQL ステートメントの実際の実行時間を超える場合があります。

![Execution time](/media/dashboard/dashboard-statement-plans-time.png)

### コプロセッサー読み取りタブ {#coprocessor-read-tab}

**コプロセッサー Read**タブをクリックすると、 コプロセッサー read に関する情報が表示されます。

![Coprocessor read](/media/dashboard/dashboard-statement-plans-cop-read.png)

### トランザクションタブ {#transaction-tab}

**[トランザクション]**タブをクリックすると、平均書き込みキー数や最大書き込みキー数など、実行計画やトランザクションに関する情報が表示されます。

![Transaction](/media/dashboard/dashboard-statement-plans-transaction.png)

### スロークエリタブ {#slow-query-tab}

実行プランの実行が遅すぎる場合、関連するスロー クエリ レコードが**[スロー クエリ]**タブに表示されます。

![Slow Query](/media/dashboard/dashboard-statement-plans-slow-queries.png)

このエリアに表示される情報は、スロー クエリ ページと同じ構造です。詳細は[TiDB ダッシュボードのスロー クエリ ページ](/dashboard/dashboard-slow-query.md)を参照してください。
