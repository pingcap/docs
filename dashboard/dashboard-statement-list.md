---
title: SQL Statements Page of TiDB Dashboard
summary: View the execution status of all SQL statements in the TiDB cluster.
---

# TiDBダッシュボードのSQLステートメントページ {#sql-statements-page-of-tidb-dashboard}

[SQLステートメント]ページには、クラスタのすべてのSQLステートメントの実行ステータスが表示されます。このページは、合計または単一の実行時間が長いSQLステートメントを分析するためによく使用されます。

このページでは、一貫性のある構造を持つSQLクエリ（クエリパラメータに一貫性がない場合でも）は、同じSQLステートメントとして分類されます。たとえば、 `SELECT * FROM employee WHERE id IN (1, 2, 3)`と`select * from EMPLOYEE where ID in (4, 5)`の両方が同じ`select * from employee where id in (...)`ステートメントとして分類されます。

## ページにアクセスする {#access-the-page}

次の2つの方法のいずれかを使用して、SQLステートメントの要約ページにアクセスできます。

-   TiDBダッシュボードにログインした後、左側のナビゲーションメニューで[ **SQLステートメント**]をクリックします。

    ![Access SQL statement summary page](/media/dashboard/dashboard-statement-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/statement](http://127.0.0.1:2379/dashboard/#/statement)にアクセスします。 `127.0.0.1:2379`を実際のPDインスタンスのアドレスとポートに置き換えます。

SQLステートメントの要約ページに表示されるすべてのデータは、TiDBステートメントの要約テーブルからのものです。テーブルの詳細については、 [TiDBステートメントの要約テーブル](/statement-summary-tables.md)を参照してください。

> **ノート：**
>
> SQLステートメントの要約ページの「**平均待ち時間**」列の青いバーは、平均実行時間を示しています。 SQLステートメントの青いバーに黄色の線がある場合、黄色の線の左側と右側はそれぞれ、最近のデータ収集サイクル中のSQLステートメントの最小実行時間と最大実行時間を表します。

### フィルターの変更 {#change-filters}

SQLステートメントの要約ページの上部で、表示するSQL実行の時間範囲を変更できます。 SQLステートメントが実行されるデータベースまたはSQLタイプでリストをフィルタリングすることもできます。次の画像は、最近のデータ収集サイクル（デフォルトでは最近の30分）でのすべてのSQL実行を示しています。

![Modify filters](/media/dashboard/dashboard-statement-filter-options.png)

### より多くの列を表示する {#display-more-columns}

ページの[**列]**をクリックすると、さらに列を表示するように選択できます。列名の右側にある<strong>（i）</strong>アイコンにマウスを移動すると、この列の説明を表示できます。

![Choose columns](/media/dashboard/dashboard-statement-columns-selector.png)

### カラムで並べ替え {#sort-by-column}

デフォルトでは、リストは**合計レイテンシー**で高いものから低いものへとソートされます。別の列見出しをクリックして、並べ替え基準を変更するか、並べ替え順序を切り替えます。

![Modify list sorting](/media/dashboard/dashboard-statement-change-order.png)

### 設定を変更する {#change-settings}

リストページで、右上の**[設定]**ボタンをクリックして、SQLステートメント機能の設定を変更します。

![Settings entry](/media/dashboard/dashboard-statement-setting-entry.png)

[**設定]**ボタンをクリックすると、次の設定ダイアログボックスが表示されます。

![Settings](/media/dashboard/dashboard-statement-settings.png)

設定ページで、SQLステートメント機能を無効または有効にできます。 SQLステートメント機能が有効になっている場合、次の設定を変更できます。

-   収集間隔：各SQLステートメント分析の期間の長さ。デフォルトでは30分です。 SQLステートメント機能は、一定期間内のすべてのSQLステートメントを要約してカウントします。期間が長すぎると、要約の粒度が粗くなり、問題の特定には適していません。期間が短すぎる場合、統計の粒度は良好であり、問題の特定には適していますが、これにより、同じデータ保持期間内でより多くのレコードとより多くのメモリ使用量が発生します。したがって、実際の状況に基づいてこの値を調整し、問題を特定するときにこの値を適切に下げる必要があります。
-   データ保持期間：要約情報の保持期間。デフォルトでは1日です。この期間より長く保持されたデータは、システムテーブルから削除されます。

詳細については、 [ステートメント要約テーブルの構成](/statement-summary-tables.md#parameter-configuration)を参照してください。

> **ノート：**
>
> -   ステートメントシステムテーブルはメモリにのみ保存されるため、SQLステートメント機能を無効にすると、システムテーブルのデータがクリアされます。
>
> -   `Collect interval`と`retain duration`の値はメモリ使用量に影響するため、実際の状況に応じてこれらの値を調整することをお勧めします。 `retain duration`の値は大きすぎないように設定してください。
