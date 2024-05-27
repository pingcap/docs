---
title: TiDB Dashboard Metrics Relation Graph
summary: TiDB ダッシュボードには、TiDB クラスター内の各内部プロセスの所要時間を理解するのに役立つメトリック関係グラフという機能が導入されています。ログイン後、ユーザーはグラフにアクセスして、各監視メトリックの所要時間がクエリの合計所要時間に対する割合を確認できます。各ボックス領域は監視メトリックを表し、合計所要時間やクエリの合計所要時間に対する割合などの情報を提供します。グラフにはノード間の親子関係も示されており、ユーザーが各監視メトリックの関係を理解するのに役立ちます。
---

# TiDB ダッシュボード メトリック関係グラフ {#tidb-dashboard-metrics-relation-graph}

TiDB ダッシュボード メトリック関係グラフは、v4.0.7 で導入された機能です。この機能は、TiDB クラスター内の各内部プロセスの期間の監視データの関係グラフを表示します。目的は、各プロセスの期間とそれらの関係をすばやく理解できるようにすることです。

## アクセスグラフ {#access-graph}

TiDB ダッシュボードにログイン後、左側のナビゲーション メニューで**[クラスタ診断]**をクリックすると、メトリック関係グラフを生成するページが表示されます。

![Metrics relation graph homepage](/media/dashboard/dashboard-metrics-relation-home-v650.png)

**範囲開始時間**と**範囲期間**を設定した後、 **「メトリック関係の生成」**をクリックすると、メトリック関係グラフのページが表示されます。

## グラフを理解する {#understand-graph}

次の画像は、メトリック関係グラフの例です。このグラフは、2020-07-29 16:36:00 から 5 分以内の TiDB クラスターでの各監視メトリックの期間と合計クエリ期間の割合を示しています。グラフには、各監視メトリックの関係も示されています。

![Metrics relation graph example](/media/dashboard/dashboard-metrics-relation-example.png)

たとえば、監視メトリック`tidb_execute`のノードの意味は次のとおりです。

-   `tidb_execute`監視メトリックの合計期間は 19306.46 秒で、クエリの合計期間の 89.4% を占めます。
-   `tidb_execute`ノード自体の継続時間は 9070.18 秒で、これはクエリ全体の継続時間の 42% を占めます。
-   ボックス領域にマウスを移動すると、合計期間、平均期間、平均 P99 (99 パーセンタイル) 期間など、メトリックの詳細情報が表示されます。

![tidb\_execute node example](/media/dashboard/dashboard-metrics-relation-node-example.png)

### ノード情報 {#node-information}

各ボックス領域は監視メトリックを表し、次の情報を提供します。

-   監視メトリックの名前
-   監視メトリックの合計期間
-   メトリックの合計期間とクエリの合計期間の割合

*メトリック ノードの合計期間*=*メトリック ノード自体の期間*+*その子ノードの期間*。したがって、一部のノードのメトリック グラフには、 `tidb_execute`のグラフのように、ノード自体の期間と合計期間の比率が表示されます。

![tidb\_execute node example1](/media/dashboard/dashboard-metrics-relation-node-example1.png)

-   `tidb_execute`は監視メトリックの名前であり、TiDB 実行エンジンでの SQL クエリの実行期間を表します。
-   `19306.46s` 、メトリック`tidb_execute`の合計実行時間が 19306.46 秒であることを表します。 `89.40%`は、19306.46 秒がすべての SQL クエリ (ユーザー SQL クエリと TiDB の内部 SQL クエリを含む) に費やされた合計時間の 89.40% を占めることを表します。クエリの合計実行時間は、 `tidb_query`の合計実行時間です。
-   `9070.18s` 、 `tidb_execute`ノード自体の合計実行時間が 9070.18 秒であり、残りがその子ノードによって消費された時間であることを表します。4 `42.00%` 、9070.18 秒がすべてのクエリの合計クエリ時間の 42.00% を占めることを表します。

ボックス領域の上にマウスを置くと、 `tidb_execute`メトリック ノードの詳細が表示されます。

![tidb\_execute node example2](/media/dashboard/dashboard-metrics-relation-node-example2.png)

上記の画像に表示されているテキスト情報は、メトリック ノードの説明であり、合計期間、合計時間、平均期間、平均期間 P99、P90、P80 が含まれます。

### ノード間の親子関係 {#the-parent-child-relations-between-nodes}

このセクションでは、 `tidb_execute`メトリック ノードを例に、メトリックの子ノードについて説明します。

![tidb\_execute node relation example1](/media/dashboard/dashboard-metrics-relation-relation-example1.png)

上のグラフから、 `tidb_execute`の 2 つの子ノードがわかります。

-   `pd_start_tso_wait` : トランザクションの`start_tso`を待機する合計時間、つまり 300.66 秒。
-   `tidb_txn_cmd` : TiDB が関連するトランザクション コマンドを実行する合計時間。9935.62 秒です。

さらに、 `tidb_execute` `tidb_cop`ボックス領域を指す点線の矢印もあり、次のことを示しています。

`tidb_execute`には`tidb_cop`メトリックの期間が含まれますが、 `cop`リクエストが同時に実行される可能性があります。たとえば、2 つのテーブルで`join`クエリを実行する`execute`期間は 60 秒で、その間に結合した 2 つのテーブルでテーブル スキャン リクエストが同時に実行されます。10 `cop`の実行期間がそれぞれ 40 秒と 30 秒の場合、 `cop`リクエストの合計期間は 70 秒です。ただし、 `execute`期間は 60 秒のみです。したがって、親ノードの期間に子ノードの期間が完全に含まれていない場合は、点線の矢印を使用して子ノードを指します。

> **注記：**
>
> ノードに子ノードを指す点線の矢印がある場合、このノード自体の継続時間は不正確です。たとえば、 `tidb_execute`ノードでは、ノード自体の継続時間は 9070.18 秒 ( `9070.18 = 19306.46 - 300.66 - 9935.62` ) です。この式では、 `tidb_cop`子ノードの継続時間は`tidb_execute`の子ノードの継続時間に計算されません。 `tidb_execute` 、実際にはそうではありません。9 自体の継続時間である 9070.18 秒には、 `tidb_cop`の継続時間の一部が含まれており、この部分の継続時間は決定できません。

### <code>tidb_kv_request</code>とその親ノード {#code-tidb-kv-request-code-and-its-parent-nodes}

![tidb\_execute node relation example2](/media/dashboard/dashboard-metrics-relation-relation-example2.png)

`tidb_kv_request`の親ノードである`tidb_cop`と`tidb_txn_cmd.get`には、両方とも`tidb_kv_request`を指す点線の矢印があり、次のことを示しています。

-   `tidb_cop`の持続時間には`tidb_kv_request`の持続時間の一部が含まれます。
-   `tidb_txn_cmd.get`の持続時間には`tidb_kv_request`の持続時間の一部も含まれます。

しかし、 `tidb_kv_request`の持続時間が`tidb_cop`にどれだけ含まれているかを判断するのは困難です。

-   `tidb_kv_request.Get` : TiDB が`Get`種類のキー値要求を送信する期間。
-   `tidb_kv_request.Cop` : TiDB が`Cop`種類のキー値要求を送信する期間。

`tidb_kv_request`には`tidb_kv_request.Get`と`tidb_kv_request.Cop`ノードが子ノードとして含まれませんが、後者の 2 つのノードで構成されます。子ノードの名前プレフィックスは親ノードの名前に`.xxx`を加えたもので、子ノードが親ノードのサブクラスであることを意味します。このケースは次のように理解できます。

TiDB がキー値要求を送信する合計時間は 14745.07 秒で、そのうち`Get`および`Cop`タイプのキー値要求にはそれぞれ 9798.02 秒と 4946.46 秒かかります。
