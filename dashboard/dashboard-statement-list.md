---
title: SQL Statements Page of TiDB Dashboard
summary: TiDB ダッシュボードの SQL ステートメント ページには、クラスター内のすべての SQL ステートメントの実行ステータスが表示されます。ユーザーは、長時間実行される SQL ステートメントを分析でき、アクセス、フィルター、列の追加表示、並べ替え、設定の変更などのオプションが提供されます。このページには、保存される SQL ステートメントの数を制限する機能も含まれています。詳細については、TiDB ダッシュボードのドキュメントをご覧ください。
---

# TiDBダッシュボードのSQLステートメントページ {#sql-statements-page-of-tidb-dashboard}

SQL ステートメント ページには、クラスター内のすべての SQL ステートメントの実行ステータスが表示されます。このページは、合計実行時間または単一の実行時間が長い SQL ステートメントを分析するためによく使用されます。

このページでは、一貫した構造を持つ SQL クエリ (クエリ パラメータが一貫していない場合でも) は、同じ SQL ステートメントとして分類されます。たとえば、 `SELECT * FROM employee WHERE id IN (1, 2, 3)`と`select * from EMPLOYEE where ID in (4, 5)`はどちらも同じ`select * from employee where id in (...)` SQL ステートメントとして分類されます。

## ページにアクセスする {#access-the-page}

SQL ステートメントの概要ページにアクセスするには、次の 2 つの方法のいずれかを使用できます。

-   TiDB ダッシュボードにログインしたら、左側のナビゲーション メニューで**[SQL ステートメント]**をクリックします。

-   ブラウザで[http://127.0.0.1:2379/ダッシュボード/#/ステートメント](http://127.0.0.1:2379/dashboard/#/statement)アクセスします。3 `127.0.0.1:2379`実際の PD インスタンスのアドレスとポートに置き換えます。

SQL ステートメントの概要ページに表示されるすべてのデータは、TiDB ステートメントの概要テーブルから取得されます。テーブルの詳細については、 [TiDB ステートメント サマリー テーブル](/statement-summary-tables.md)参照してください。

> **注記：**
>
> SQL ステートメントの概要ページの**「平均待ち時間」**列では、青いバーが平均実行時間を示します。SQL ステートメントの青いバーに黄色の線が表示されている場合、黄色の線の左側と右側はそれぞれ、最近のデータ収集サイクル中の SQL ステートメントの最小実行時間と最大実行時間を表します。

### フィルターを変更する {#change-filters}

SQL ステートメントの概要ページの上部で、表示する SQL 実行の時間範囲を変更できます。また、SQL ステートメントが実行されるデータベース別、または SQL タイプ別にリストをフィルターすることもできます。次の画像は、最近のデータ収集サイクル (デフォルトでは最近の 30 分間) におけるすべての SQL 実行を示しています。

![Modify filters](/media/dashboard/dashboard-statement-filter-options.png)

### より多くの列を表示 {#display-more-columns}

ページの**「列」**をクリックすると、さらに列を表示できます。マウスを列名の右側にある**(i)**アイコンに移動すると、その列の説明が表示されます。

![Choose columns](/media/dashboard/dashboard-statement-columns-selector.png)

### カラムで並べ替え {#sort-by-column}

デフォルトでは、リストは**合計レイテンシ**の高から低の順に並べ替えられます。並べ替えの基準を変更したり、並べ替え順序を切り替えるには、別の列見出しをクリックします。

![Modify list sorting](/media/dashboard/dashboard-statement-change-order.png)

### 設定を変更する {#change-settings}

リスト ページで、右上にある**[設定]**ボタンをクリックして、SQL ステートメント機能の設定を変更します。

![Settings entry](/media/dashboard/dashboard-statement-setting-entry.png)

**[設定]**ボタンをクリックすると、次の設定ダイアログボックスが表示されます。

![Settings](/media/dashboard/dashboard-statement-settings.png)

設定ページでは、SQL ステートメント機能を無効または有効にすることができます。SQL ステートメント機能を有効にすると、次の設定を変更できます。

-   収集間隔: 各 SQL ステートメント分析の期間の長さ。デフォルトでは 30 分です。SQL ステートメント機能は、一定期間内のすべての SQL ステートメントを要約してカウントします。期間が長すぎると、要約の粒度が粗くなり、問題の特定には適しません。期間が短すぎると、統計の粒度が細かくなり、問題の特定には適しますが、同じデータ保持期間内でレコード数が増え、メモリ使用量が増えます。したがって、実際の状況に基づいてこの値を調整し、問題を特定するときにこの値を適切に下げる必要があります。
-   データ保持期間: 概要情報の保持期間。デフォルトでは 1 日です。この期間より長く保持されたデータは、システム テーブルから削除されます。

詳細は[ステートメントサマリーテーブルの構成](/statement-summary-tables.md#parameter-configuration)参照。

> **注記：**
>
> -   ステートメント システム テーブルはメモリにのみ保存されるため、SQL ステートメント機能が無効になると、システム テーブル内のデータはクリアされます。
>
> -   `Collect interval`と`retain duration`の値はメモリ使用量に影響するため、実際の状況に応じてこれらの値を調整することをお勧めします。5 `retain duration`値は大きすぎないようにしてください。

### その他 {#others}

[`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40) 、ステートメント サマリー テーブルに保存できる SQL ステートメントの数を制限します。制限を超えると、TiDB は最近使用されていない SQL ステートメントをクリアします。これらのクリアされた SQL ステートメントは、 `DIGEST`が`NULL`に設定された行として表されます。TiDB ダッシュボードの SQL ステートメント ページでは、これらの行の情報は`Others`として表示されます。

![Others](/media/dashboard/dashboard-statement-other-row.png)

## 次のステップ {#next-step}

SQL ステートメントの実行詳細を表示する方法の詳細については、 [TiDBダッシュボードのステートメント実行の詳細](/dashboard/dashboard-statement-details.md)参照してください。
