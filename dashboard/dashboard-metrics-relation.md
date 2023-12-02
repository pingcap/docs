---
title: TiDB Dashboard Metrics Relation Graph
summary: Learn TiDB Dashboard metrics relation graph.
---

# TiDB ダッシュボードのメトリクス関係グラフ {#tidb-dashboard-metrics-relation-graph}

TiDB ダッシュボード メトリクス関係グラフは、v4.0.7 で導入された機能です。この機能は、TiDB クラスター内の各内部プロセスの継続時間の監視データの関係グラフを表示します。目的は、各プロセスの期間とその関係をすぐに理解できるようにすることです。

## アクセスグラフ {#access-graph}

TiDB ダッシュボードにログインした後、左側のナビゲーション メニューで**[クラスタ診断]**をクリックすると、メトリック関係グラフを生成するページが表示されます。

![Metrics relation graph homepage](/media/dashboard/dashboard-metrics-relation-home-v650.png)

**[範囲開始時刻]**と**[範囲期間]**を設定した後、 **[メトリクス関係の生成]**をクリックすると、メトリクス関係グラフのページが表示されます。

## グラフを理解する {#understand-graph}

次の画像は、メトリクス関係グラフの例です。このグラフは、2020-07-29 16:36:00 以降 5 分以内の TiDB クラスター内の合計クエリ継続時間に対する各モニタリング メトリクスの継続時間の割合を示しています。グラフには、各監視メトリックの関係も示されています。

![Metrics relation graph example](/media/dashboard/dashboard-metrics-relation-example.png)

たとえば、監視メトリック`tidb_execute`のノードの意味は次のとおりです。

-   `tidb_execute`モニタリング メトリックの合計期間は 19306.46 秒で、クエリ合計期間の 89.4% を占めます。
-   `tidb_execute`ノード自体の継続時間は 9070.18 秒で、これは合計クエリ継続時間の 42% を占めます。
-   ボックス領域にマウスを置くと、合計期間、平均期間、平均 P99 (99 パーセンタイル) 期間などのメトリクスの詳細情報が表示されます。

![tidb\_execute node example](/media/dashboard/dashboard-metrics-relation-node-example.png)

### ノード情報 {#node-information}

各ボックス領域は監視メトリックを表し、次の情報を提供します。

-   監視メトリックの名前
-   モニタリングメトリクスの合計期間
-   クエリの合計期間に対するメトリクスの合計期間の割合

*メトリック ノードの合計期間*=*メトリック ノード自体の期間*+*その子ノードの期間*。したがって、一部のノードのメトリック グラフには、 `tidb_execute`のグラフなど、合計期間に対するノード自体の期間の割合が表示されます。

![tidb\_execute node example1](/media/dashboard/dashboard-metrics-relation-node-example1.png)

-   `tidb_execute`はモニタリング メトリックの名前で、TiDB 実行エンジンでの SQL クエリの実行時間を表します。
-   `19306.46s` 、 `tidb_execute`メトリックの合計期間が 19306.46 秒であることを表します。 `89.40%` 19306.46 秒が、すべての SQL クエリ (ユーザー SQL クエリと TiDB の内部 SQL クエリを含む) に費やされる合計時間の 89.40% を占めることを表します。合計クエリ期間は`tidb_query`の合計期間です。
-   `9070.18s` 、 `tidb_execute`ノード自体の合計実行時間が 9070.18 秒であることを表し、残りはその子ノードによって消費される時間です。 `42.00%` 9070.18 秒がすべてのクエリの合計クエリ時間の 42.00% を占めることを表します。

マウスをボックス領域の上に置くと、 `tidb_execute`メトリック ノードの詳細が表示されます。

![tidb\_execute node example2](/media/dashboard/dashboard-metrics-relation-node-example2.png)

上の画像に表示されているテキスト情報は、合計期間、合計時間、平均期間、平均期間 P99、P90、および P80 を含むメトリック ノードの説明です。

### ノード間の親子関係 {#the-parent-child-relations-between-nodes}

`tidb_execute`メトリック ノードを例として、このセクションではメトリックの子ノードを紹介します。

![tidb\_execute node relation example1](/media/dashboard/dashboard-metrics-relation-relation-example1.png)

上のグラフから、 `tidb_execute`の 2 つの子ノードがわかります。

-   `pd_start_tso_wait` : トランザクションの`start_tso`を待機する合計時間、つまり 300.66 秒です。
-   `tidb_txn_cmd` : TiDB が関連するトランザクション コマンドを実行する合計時間 (9935.62 秒)。

さらに、 `tidb_execute`は`tidb_cop`ボックス領域を指す点線の矢印もあり、次のことを示しています。

`tidb_execute`には`tidb_cop`メトリックの期間が含まれますが、 `cop`リクエストが同時に実行される可能性があります。たとえば、2 つのテーブルに対して`execute` `join`クエリを実行する期間は 60 秒で、その間、結合された 2 つのテーブルに対してテーブル スキャン リクエストが同時に実行されます。 `cop`のリクエストの実行時間がそれぞれ 40 秒と 30 秒である場合、 `cop`のリクエストの合計時間は 70 秒になります。ただし、 `execute`持続時間はわずか 60 秒です。したがって、親ノードの継続時間が子ノードの継続時間を完全に含んでいない場合は、点線の矢印が子ノードを指すために使用されます。

> **注記：**
>
> ノードにその子ノードを指す点線の矢印がある場合、このノード自体の継続時間は不正確です。たとえば、 `tidb_execute`ノードでは、ノード自体の継続時間は 9070.18 秒 ( `9070.18 = 19306.46 - 300.66 - 9935.62` ) です。この式では、 `tidb_cop`子ノードの継続時間は、 `tidb_execute`の子ノードの継続時間には計算されません。しかし実際には、これは真実ではありません。 `tidb_execute`の継続時間である 9070.18 秒には`tidb_cop`継続時間の一部が含まれており、この部分の継続時間は特定できません。

### <code>tidb_kv_request</code>とその親ノード {#code-tidb-kv-request-code-and-its-parent-nodes}

![tidb\_execute node relation example2](/media/dashboard/dashboard-metrics-relation-relation-example2.png)

`tidb_kv_request`の親ノードである`tidb_cop`と`tidb_txn_cmd.get`両方とも`tidb_kv_request`を指す点線の矢印があり、これは次のことを示しています。

-   `tidb_cop`の持続時間には`tidb_kv_request`の持続時間の一部が含まれます。
-   `tidb_txn_cmd.get`の持続時間には`tidb_kv_request`の持続時間の一部も含まれます。

ただし、 `tidb_kv_request`の継続時間が`tidb_cop`にどの程度含まれるかを判断するのは困難です。

-   `tidb_kv_request.Get` : TiDB が`Get`種類のキーと値のリクエストを送信する期間。
-   `tidb_kv_request.Cop` : TiDB が`Cop`種類のキーと値のリクエストを送信する期間。

`tidb_kv_request`子ノードとして`tidb_kv_request.Get`と`tidb_kv_request.Cop`ノードを含まず、後の 2 つのノードで構成されます。子ノードの名前プレフィックスは、親ノードの名前に`.xxx`を加えたものになります。これは、子ノードが親ノードのサブクラスであることを意味します。このケースは次のように理解できます。

TiDB が Key-Value リクエストを送信する合計時間は 14745.07 秒で、この間、タイプ`Get`と`Cop`の Key-Value リクエストはそれぞれ 9798.02 秒と 4946.46 秒を消費します。
