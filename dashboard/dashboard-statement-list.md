---
title: SQL Statements Page of TiDB Dashboard
summary: View the execution status of all SQL statements in the TiDB cluster.
---

# TiDB ダッシュボードの SQL ステートメント ページ {#sql-statements-page-of-tidb-dashboard}

SQL ステートメント ページには、クラスター内のすべての SQL ステートメントの実行ステータスが表示されます。このページは、合計または 1 回の実行時間が長い SQL ステートメントを分析するためによく使用されます。

このページでは、一貫した構造を持つ SQL クエリ (クエリ パラメーターが一致していない場合でも) は、同じ SQL ステートメントとして分類されます。たとえば、 `SELECT * FROM employee WHERE id IN (1, 2, 3)`と`select * from EMPLOYEE where ID in (4, 5)`は両方とも同じ`select * from employee where id in (...)` SQL ステートメントとして分類されます。

## ページにアクセスする {#access-the-page}

次の 2 つの方法のいずれかを使用して、SQL ステートメントの概要ページにアクセスできます。

-   TiDB ダッシュボードにログインした後、左側のナビゲーション メニューで**[SQL ステートメント]**をクリックします。

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/statement](http://127.0.0.1:2379/dashboard/#/statement)にアクセスしてください。 `127.0.0.1:2379`を実際の PD インスタンスのアドレスとポートに置き換えます。

SQL ステートメントの概要ページに表示されるすべてのデータは、TiDB ステートメントの概要テーブルからのものです。テーブルの詳細については、 [TiDB ステートメントの要約テーブル](/statement-summary-tables.md)を参照してください。

> **注記：**
>
> SQL ステートメントの概要ページの**平均待機時間**列では、青いバーが平均実行時間を示します。 SQL ステートメントの青いバーに黄色の線がある場合、黄色の線の左側と右側は、最近のデータ収集サイクル中の SQL ステートメントの最小実行時間と最大実行時間をそれぞれ表します。

### フィルターを変更する {#change-filters}

SQL ステートメントの概要ページの上部で、表示する SQL 実行の時間範囲を変更できます。 SQL ステートメントが実行されるデータベース別、または SQL タイプ別にリストをフィルタリングすることもできます。次の図は、最近のデータ収集サイクル (デフォルトでは最近 30 分) にわたるすべての SQL 実行を示しています。

![Modify filters](/media/dashboard/dashboard-statement-filter-options.png)

### さらに多くの列を表示 {#display-more-columns}

ページ上の**[列]**をクリックすると、さらに列を表示することを選択できます。列名の右側にある**(i)**アイコンにマウスを移動すると、この列の説明が表示されます。

![Choose columns](/media/dashboard/dashboard-statement-columns-selector.png)

### カラムで並べ替え {#sort-by-column}

デフォルトでは、リストは**合計レイテンシ**の高い順に並べ替えられます。別の列見出しをクリックして並べ替えの基準を変更するか、並べ替え順序を切り替えます。

![Modify list sorting](/media/dashboard/dashboard-statement-change-order.png)

### 設定を変更する {#change-settings}

リスト ページで、右上の**[設定]**ボタンをクリックして、SQL ステートメント機能の設定を変更します。

![Settings entry](/media/dashboard/dashboard-statement-setting-entry.png)

**「設定」**ボタンをクリックすると、次の設定ダイアログボックスが表示されます。

![Settings](/media/dashboard/dashboard-statement-settings.png)

設定ページでは、SQL ステートメント機能を無効または有効にすることができます。 SQL ステートメント機能が有効になっている場合、次の設定を変更できます。

-   収集間隔: 各 SQL ステートメント分析の期間の長さ。デフォルトでは 30 分です。 SQL ステートメント機能は、一定期間内のすべての SQL ステートメントを要約してカウントします。期間が長すぎると、概要の粒度が粗くなり、問題の特定には適していません。期間が短すぎる場合、統計の粒度は適切であり、問​​題を特定するのに適していますが、同じデータ保持期間内でより多くのレコードとより多くのメモリ使用量が発生します。したがって、実際の状況に基づいてこの値を調整し、問題を特定するときにこの値を適切に下げる必要があります。
-   データ保持期間: 概要情報の保持期間。デフォルトでは 1 日です。この期間を超えて保持されたデータはシステム テーブルから削除されます。

詳細については[ステートメント要約テーブルの構成](/statement-summary-tables.md#parameter-configuration)を参照してください。

> **注記：**
>
> -   ステートメント システム テーブルはメモリにのみ格納されるため、SQL ステートメント機能を無効にすると、システム テーブル内のデータはクリアされます。
>
> -   `Collect interval`と`retain duration`の値はメモリ使用量に影響するため、実際の状況に応じてこれらの値を調整することをお勧めします。 `retain duration`という値はあまり大きく設定しないでください。

### その他 {#others}

[`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40)ステートメント概要テーブルに格納できる SQL ステートメントの数を制限します。制限を超えると、TiDB は最近未使用のままになっている SQL ステートメントをクリアします。これらのクリアされた SQL ステートメントは、 `DIGEST`が`NULL`に設定された行として表されます。 TiDB ダッシュボードの SQL ステートメント ページでは、これらの行の情報は`Others`として表示されます。

![Others](/media/dashboard/dashboard-statement-other-row.png)

## 次のステップ {#next-step}

SQL ステートメントの実行の詳細を表示する方法の詳細については、 [TiDB ダッシュボードのステートメント実行の詳細](/dashboard/dashboard-statement-details.md)を参照してください。
