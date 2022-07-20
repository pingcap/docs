---
title: Slow Queries Page of TiDB Dashboard
summary: Learn the Slow Queries page of TiDB Dashboard.
---

# TiDBダッシュボードの低速クエリページ {#slow-queries-page-of-tidb-dashboard}

TiDBダッシュボードの[低速クエリ]ページで、クラスタのすべての低速クエリを検索および表示できます。

デフォルトでは、実行時間が300ミリ秒を超えるSQLクエリは低速クエリと見なされます。これらのクエリは[遅いクエリログ](/identify-slow-queries.md)に記録され、TiDBダッシュボードを介して検索できます。 [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)セッション変数または[`slow-threshold`](/tidb-configuration-file.md#slow-threshold)パラメーターを使用して、低速クエリのしきい値を調整できます。

> **ノート：**
>
> 低速クエリログが無効になっている場合、この機能は使用できなくなります。低速クエリログはデフォルトで有効になっており、 [`enable-slow-log`](/tidb-configuration-file.md#enable-slow-log)構成アイテムを使用して低速クエリログを有効または無効にできます。

## ページにアクセスする {#access-the-page}

次の2つの方法のいずれかを使用して、低速クエリページにアクセスできます。

-   TiDBダッシュボードにログインした後、左側のナビゲーションメニューで[**低速クエリ**]をクリックします。

![Access slow query page](/media/dashboard/dashboard-slow-queries-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/slow_query](http://127.0.0.1:2379/dashboard/#/slow_query)にアクセスします。 `127.0.0.1:2379`を実際のPDアドレスとポートに置き換えます。

低速クエリページに表示されるすべてのデータは、TiDB低速クエリシステムテーブルと低速クエリログから取得されます。詳細については、 [遅いクエリログ](/identify-slow-queries.md)を参照してください。

### フィルタを変更する {#change-filters}

時間範囲、関連データベース、SQLキーワード、SQLタイプ、表示される低速クエリの数に基づいて、低速クエリをフィルタリングできます。下の画像では、最近30分間に100回の遅いクエリがデフォルトで表示されています。

![Modify list filters](/media/dashboard/dashboard-slow-queries-list1.png)

### その他の列を表示する {#display-more-columns}

ページの[**列]**をクリックすると、さらに列を表示するように選択できます。列名の右側にある<strong>（i）</strong>アイコンにマウスを移動すると、この列の説明が表示されます。

![Show more columns](/media/dashboard/dashboard-slow-queries-list2.png)

### カラムで並べ替え {#sort-by-column}

デフォルトでは、リストは**終了時間**の降順で並べ替えられます。列見出しをクリックして列で並べ替えるか、並べ替え順序を切り替えます。

![Modify sorting basis](/media/dashboard/dashboard-slow-queries-list3.png)

## 実行の詳細をビューする {#view-execution-details}

リスト内の任意の項目をクリックして、次のような低速クエリの詳細な実行情報を表示します。

-   クエリ：SQLステートメントのテキスト（下の画像の領域1を参照）。
-   計画：低速クエリの実行計画。実行計画の読み方については、 [クエリ実行プランを理解する](/explain-overview.md)を参照してください（下の画像の領域2を参照）。
-   その他のソートされたSQL実行情報（下の画像の領域3を参照）。

![View execution details](/media/dashboard/dashboard-slow-queries-detail1.png)

アイテムの詳細情報を表示するには、 **[展開]**リンクをクリックします。 [<strong>コピー]</strong>リンクをクリックして、詳細情報をクリップボードにコピーします。

対応するタブタイトルをクリックして、並べ替えられたさまざまなSQL実行の情報を切り替えます。

![Show different sorted execution information](/media/dashboard/dashboard-slow-queries-detail2.png)
