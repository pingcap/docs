---
title: SQL Statements Page of TiDB Dashboard
summary: TiDBダッシュボードのSQLステートメントページには、クラスター内のすべてのSQLステートメントの実行ステータスが表示されます。このページでは、実行時間の長いSQLステートメントを分析でき、アクセス、フィルタリング、列の追加表示、並べ替え、設定の変更などのオプションが提供されます。また、保存するSQLステートメントの数を制限する機能も備えています。詳細については、TiDBダッシュボードのドキュメントをご覧ください。
---

# TiDBダッシュボードのSQLステートメントページ {#sql-statements-page-of-tidb-dashboard}

SQL文ページには、クラスター内のすべてのSQL文の実行状況が表示されます。このページは、合計実行時間または単一の実行時間が長いSQL文を分析するためによく使用されます。

このページでは、構造が一貫しているSQLクエリ（クエリパラメータが不一致であっても）は、同じSQL文として分類されます。例えば、 `SELECT * FROM employee WHERE id IN (1, 2, 3)`と`select * from EMPLOYEE where ID in (4, 5)`は同じSQL文`select * from employee where id in (...)`として分類されます。

## ページにアクセスする {#access-the-page}

SQL ステートメントの概要ページにアクセスするには、次の 2 つの方法のいずれかを使用できます。

-   TiDB ダッシュボードにログインしたら、左側のナビゲーション メニューで**[SQL ステートメント]**をクリックします。

-   ブラウザで[http://127.0.0.1:2379/ダッシュボード/#/ステートメント](http://127.0.0.1:2379/dashboard/#/statement)アクセスしてください。3 `127.0.0.1:2379`実際のPDインスタンスのアドレスとポートに置き換えてください。

SQL文の概要ページに表示されるすべてのデータは、TiDB文の概要テーブルから取得されます。テーブルの詳細については、 [TiDB ステートメント サマリー テーブル](/statement-summary-tables.md)参照してください。

> **注記：**
>
> SQL ステートメントの概要ページの**「平均レイテンシ」**列では、青いバーが平均実行時間を示します。SQL ステートメントの青いバーに黄色の線が表示されている場合、黄色の線の左側と右側はそれぞれ、最新のデータ収集サイクルにおけるその SQL ステートメントの最小実行時間と最大実行時間を表します。

### フィルターを変更する {#change-filters}

SQL文の概要ページの上部で、表示するSQL実行の時間範囲を変更できます。また、SQL文が実行されたデータベースやSQLの種類でリストをフィルタリングすることもできます。次の画像は、最近のデータ収集サイクル（デフォルトでは過去30分）におけるすべてのSQL実行を示しています。

![Modify filters](/media/dashboard/dashboard-statement-filter-options.png)

### より多くの列を表示する {#display-more-columns}

ページ上の**「列」**をクリックすると、さらに列を表示できます。列名の右側にある**(i)**アイコンにマウスを移動すると、その列の説明が表示されます。

![Choose columns](/media/dashboard/dashboard-statement-columns-selector.png)

### カラムで並べ替え {#sort-by-column}

デフォルトでは、リストは**合計レイテンシ**の高低でソートされます。列見出しをクリックすると、ソート基準を変更したり、ソート順を切り替えたりできます。

![Modify list sorting](/media/dashboard/dashboard-statement-change-order.png)

### 設定を変更する {#change-settings}

リスト ページで、右上にある**[設定]**ボタンをクリックして、SQL ステートメント機能の設定を変更します。

![Settings entry](/media/dashboard/dashboard-statement-setting-entry.png)

**[設定]**ボタンをクリックすると、次の設定ダイアログボックスが表示されます。

![Settings](/media/dashboard/dashboard-statement-settings.png)

設定ページでは、SQL文機能を有効または無効にすることができます。SQL文機能を有効にすると、以下の設定を変更できます。

-   収集間隔：各SQL文の分析期間。デフォルトでは30分です。SQL文機能は、一定期間内のすべてのSQL文を集計し、カウントします。期間が長すぎると集計の粒度が粗くなり、問題の特定に適さなくなります。期間が短すぎると統計の粒度が細かくなり、問題の特定には適しますが、同じデータ保持期間内でのレコード数とメモリ使用量が増加します。したがって、実際の状況に応じてこの値を調整し、問題の特定時には適切にこの値を下げる必要があります。
-   データ保持期間：概要情報の保持期間。デフォルトでは1日です。この期間を超えて保持されたデータは、システムテーブルから削除されます。

詳細は[ステートメントサマリーテーブルの構成](/statement-summary-tables.md#parameter-configuration)参照。

> **注記：**
>
> -   ステートメント システム テーブルはメモリ内にのみ保存されるため、SQL ステートメント機能が無効にされると、システム テーブル内のデータはクリアされます。
>
> -   `Collect interval`と`retain duration`の値はメモリ使用量に影響するため、実際の状況に応じて調整することをお勧めします`retain duration`の値は大きすぎないようにしてください。

### その他 {#others}

[`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40) 、テーブル[ステートメント要約](/statement-summary-tables.md#statements_summary)と[ステートメント概要履歴](/statement-summary-tables.md#statements_summary_history)メモリに格納できるSQLダイジェストの合計数を制限します。この制限を超えると、TiDBは最近使用されていないSQL文をクリアします。クリアされたSQL文は、 `DIGEST`が`NULL`に設定された行として表されます。TiDBダッシュボードのSQL文ページでは、これらの行の情報は`Others`として表示されます。

![Others](/media/dashboard/dashboard-statement-other-row.png)

## 次のステップ {#next-step}

SQL ステートメントの実行詳細を表示する方法の詳細については、 [TiDBダッシュボードのステートメント実行の詳細](/dashboard/dashboard-statement-details.md)参照してください。
