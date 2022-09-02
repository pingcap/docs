---
title: Slow Queries Page of TiDB Dashboard
summary: Learn the Slow Queries page of TiDB Dashboard.
---

# TiDB ダッシュボードのスロー クエリ ページ {#slow-queries-page-of-tidb-dashboard}

TiDB ダッシュボードの [スロー クエリ] ページで、クラスター内のすべてのスロー クエリを検索して表示できます。

デフォルトでは、実行時間が 300 ミリ秒を超える SQL クエリは低速クエリと見なされます。これらのクエリは[遅いクエリ ログ](/identify-slow-queries.md)に記録され、TiDB ダッシュボードで検索できます。 [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)セッション変数または[`slow-threshold`](/tidb-configuration-file.md#slow-threshold) TiDB パラメータを使用して、低速クエリのしきい値を調整できます。

> **ノート：**
>
> スロー クエリ ログが無効になっている場合、この機能は使用できません。スロー クエリ ログはデフォルトで有効になっており、 [`enable-slow-log`](/tidb-configuration-file.md#enable-slow-log) TiDB 構成項目でスロー クエリ ログを有効または無効にできます。

## ページにアクセスする {#access-the-page}

次の 2 つの方法のいずれかを使用して、スロー クエリ ページにアクセスできます。

-   TiDB ダッシュボードにログインした後、左側のナビゲーション メニューで [**スロー クエリ**] をクリックします。

![Access slow query page](/media/dashboard/dashboard-slow-queries-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/slow_query](http://127.0.0.1:2379/dashboard/#/slow_query)にアクセスします。 `127.0.0.1:2379`を実際の PD アドレスとポートに置き換えます。

スロー クエリ ページに表示されるすべてのデータは、TiDB スロー クエリ システム テーブルとスロー クエリ ログから取得されます。詳細は[遅いクエリ ログ](/identify-slow-queries.md)を参照してください。

### フィルターを変更 {#change-filters}

時間範囲、関連するデータベース、SQL キーワード、SQL タイプ、表示するスロー クエリの数に基づいて、スロー クエリをフィルタリングできます。下の画像では、最近 30 分間の 100 件のスロー クエリがデフォルトで表示されています。

![Modify list filters](/media/dashboard/dashboard-slow-queries-list1.png)

### より多くの列を表示 {#display-more-columns}

ページの [**列]**をクリックすると、さらに列を表示するように選択できます。列名の右側にある<strong>(i)</strong>アイコンにマウスを移動すると、この列の説明が表示されます。

![Show more columns](/media/dashboard/dashboard-slow-queries-list2.png)

### カラムで並べ替え {#sort-by-column}

デフォルトでは、リストは**終了時間**の降順でソートされます。列見出しをクリックして、列で並べ替えるか、並べ替え順序を切り替えます。

![Modify sorting basis](/media/dashboard/dashboard-slow-queries-list3.png)

## 実行の詳細をビュー {#view-execution-details}

リスト内の任意の項目をクリックすると、次のようなスロー クエリの詳細な実行情報が表示されます。

-   クエリ: SQL ステートメントのテキスト (下の画像の領域 1 を参照)。
-   プラン: スロー クエリの実行プラン。実行計画の読み方については、 [クエリ実行計画を理解する](/explain-overview.md)を参照してください (下の図の領域 2 を参照)。
-   その他のソートされた SQL 実行情報 (下の画像の領域 3 を参照)。

![View execution details](/media/dashboard/dashboard-slow-queries-detail1.png)

[**展開]**リンクをクリックして、アイテムの詳細情報を表示します。 [<strong>コピー]</strong>リンクをクリックして、詳細情報をクリップボードにコピーします。

対応するタブのタイトルをクリックして、ソートされたさまざまな SQL 実行の情報を切り替えます。

![Show different sorted execution information](/media/dashboard/dashboard-slow-queries-detail2.png)
