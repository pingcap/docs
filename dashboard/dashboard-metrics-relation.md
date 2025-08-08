---
title: TiDB Dashboard Metrics Relation Graph
summary: TiDBダッシュボードに、TiDBクラスタ内の各内部プロセスの所要時間を把握するのに役立つメトリクス関係グラフという機能が導入されました。ログイン後、ユーザーはグラフにアクセスし、各監視メトリクスの所要時間がクエリ総所要時間に対する割合を確認できます。各ボックス領域は監視メトリクスを表し、総所要時間やクエリ総所要時間に対する割合などの情報を提供します。グラフにはノード間の親子関係も表示されるため、各監視メトリクスの関係を理解するのに役立ちます。
---

# TiDBダッシュボードメトリクス関係グラフ {#tidb-dashboard-metrics-relation-graph}

TiDBダッシュボードのメトリクス関係グラフは、v4.0.7で導入された機能です。この機能は、TiDBクラスタ内の各内部プロセスの実行時間に関する監視データの関係グラフを表示します。これにより、各プロセスの実行時間とそれらの関係を迅速に把握できるようになります。

## アクセスグラフ {#access-graph}

TiDB ダッシュボードにログイン後、左側のナビゲーション メニューで**[クラスタ診断]**をクリックすると、メトリック関係グラフを生成するページが表示されます。

![Metrics relation graph homepage](/media/dashboard/dashboard-metrics-relation-home-v650.png)

**範囲開始時間**と**範囲期間**を設定した後、 **「メトリック関係の生成」**をクリックすると、メトリック関係グラフのページが表示されます。

## グラフを理解する {#understand-graph}

以下の画像は、メトリクス関係グラフの例です。このグラフは、2020年7月29日 16:36:00から5分間におけるTiDBクラスター内の各監視メトリクスの所要時間の合計に対する割合を示しています。また、各監視メトリクス間の関係も示されています。

![Metrics relation graph example](/media/dashboard/dashboard-metrics-relation-example.png)

たとえば、監視メトリック`tidb_execute`のノードの意味は次のとおりです。

-   `tidb_execute`監視メトリックの合計実行時間は 19306.46 秒で、これはクエリの合計実行時間の 89.4% を占めます。
-   `tidb_execute`ノード自体の継続時間は 9070.18 秒で、これはクエリ全体の継続時間の 42% を占めます。
-   ボックス領域にマウスを移動すると、合計期間、平均期間、平均 P99 (99 パーセンタイル) 期間などのメトリックの詳細情報が表示されます。

![tidb\_execute node example](/media/dashboard/dashboard-metrics-relation-node-example.png)

### ノード情報 {#node-information}

各ボックス領域は監視メトリックを表し、次の情報を提供します。

-   監視メトリックの名前
-   監視メトリックの合計期間
-   メトリックの合計期間とクエリの合計期間の割合

*メトリックノードの合計継続時間*=*メトリックノード自体の継続時間*+*その子ノードの継続時間*。したがって、一部のノードのメトリックグラフには、 `tidb_execute`のグラフのように、ノード自体の継続時間が合計継続時間に対する割合が表示されます。

![tidb\_execute node example1](/media/dashboard/dashboard-metrics-relation-node-example1.png)

-   `tidb_execute` 、TiDB 実行エンジンでの SQL クエリの実行期間を表す監視メトリックの名前です。
-   `19306.46s` 、メトリック`tidb_execute`の合計実行時間が 19306.46 秒であることを示します。4 `89.40%` 、19306.46 秒がすべての SQL クエリ（ユーザー SQL クエリと TiDB 内部 SQL クエリを含む）の合計実行時間の 89.40% を占めていることを示します。クエリの合計実行時間は、 `tidb_query`の合計実行時間です。
-   `9070.18s` 、 `tidb_execute`ノード自体の合計実行時間が 9070.18 秒であり、残りがその子ノードによって消費された時間であることを表します。4 `42.00%` 、9070.18 秒がすべてのクエリの合計クエリ時間の 42.00% を占めることを表します。

ボックス領域にマウスを移動すると、 `tidb_execute`メトリック ノードの詳細が表示されます。

![tidb\_execute node example2](/media/dashboard/dashboard-metrics-relation-node-example2.png)

上記の画像に表示されているテキスト情報は、メトリック ノードの説明であり、合計期間、合計時間、平均期間、平均期間 P99、P90、P80 が含まれます。

### ノード間の親子関係 {#the-parent-child-relations-between-nodes}

このセクションでは、 `tidb_execute`メトリック ノードを例に、メトリックの子ノードを紹介します。

![tidb\_execute node relation example1](/media/dashboard/dashboard-metrics-relation-relation-example1.png)

上のグラフから、 `tidb_execute`の 2 つの子ノードがわかります。

-   `pd_start_tso_wait` : トランザクションの`start_tso`待機する合計時間。これは 300.66 秒です。
-   `tidb_txn_cmd` : TiDB が関連するトランザクション コマンドを実行する合計時間。9935.62 秒です。

さらに、 `tidb_execute`は`tidb_cop`ボックス領域を指す点線の矢印もあり、次のことを示しています。

`tidb_execute` `tidb_cop`番目のメトリックの実行時間が含まれますが、同時に`cop`リクエストが実行される場合があります。例えば、2 つのテーブルに対して`join`クエリを実行する`execute`番目の実行時間は 60 秒ですが、その間に結合した 2 つのテーブルに対してテーブルスキャンリクエストが同時に実行されます。10 `cop`のリクエストの実行時間がそれぞれ 40 秒と 30 秒の場合、 `cop`のリクエストの合計実行時間は 70 秒になります。しかし、 `execute`実行時間はわずか 60 秒です。したがって、親ノードの実行時間に子ノードの実行時間が完全に含まれていない場合、点線の矢印は子ノードを指します。

> **注記：**
>
> ノードに子ノードを指す点線矢印がある場合、そのノード自体の持続時間は不正確です。例えば、 `tidb_execute`のノードの場合、ノード自体の持続時間は9070.18秒（ `9070.18 = 19306.46 - 300.66 - 9935.62` ）です。この式では、 `tidb_cop`子ノードの持続時間は`tidb_execute`番目の子ノードの持続時間に含まれていません。しかし、実際にはそうではありません。9番目のノード自体の持続時間である9070.18秒には、 `tidb_cop` `tidb_execute`ノードの持続時間の一部が含まれており、この部分の持続時間は特定できません。

### <code>tidb_kv_request</code>とその親ノード {#code-tidb-kv-request-code-and-its-parent-nodes}

![tidb\_execute node relation example2](/media/dashboard/dashboard-metrics-relation-relation-example2.png)

`tidb_kv_request`の親ノードである`tidb_cop`と`tidb_txn_cmd.get`は、どちらも`tidb_kv_request`を指す点線矢印があり、次のことを示しています。

-   `tidb_cop`の持続時間には`tidb_kv_request`の持続時間の一部が含まれます。
-   `tidb_txn_cmd.get`の持続時間には`tidb_kv_request`の持続時間の一部も含まれます。

しかし、 `tidb_kv_request`の持続時間が`tidb_cop`にどれだけ含まれているかを判断することは困難です。

-   `tidb_kv_request.Get` : TiDB が`Get`種類のキー値要求を送信する期間。
-   `tidb_kv_request.Cop` : TiDB が`Cop`種類のキー値要求を送信する期間。

`tidb_kv_request`子ノードとして`tidb_kv_request.Get`と`tidb_kv_request.Cop`ノードを含みませんが、後者の2つのノードで構成されます。子ノードの名前プレフィックスは親ノードの名前に`.xxx`を加えたもので、これは子ノードが親ノードのサブクラスであることを意味します。このケースは次のように理解できます。

TiDB がキー値要求を送信する合計時間は 14745.07 秒で、そのうち、タイプ`Get`と`Cop`キー値要求にはそれぞれ 9798.02 秒と 4946.46 秒かかります。
