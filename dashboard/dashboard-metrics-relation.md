---
title: TiDB Dashboard Metrics Relation Graph
summary: Learn TiDB Dashboard metrics relation graph.
---

# TiDB ダッシュボード メトリクス関係グラフ {#tidb-dashboard-metrics-relation-graph}

TiDB ダッシュボード メトリック関係グラフは、v4.0.7 で導入された機能です。この機能は、TiDB クラスター内の各内部プロセスの期間の監視データの関係グラフを表示します。目的は、各プロセスの所要時間とそれらの関係をすばやく理解できるようにすることです。

## アクセスグラフ {#access-graph}

TiDB ダッシュボードにログインし、左側のナビゲーション メニューで**[クラスタ Diagnostics]**をクリックすると、メトリック関係グラフを生成するページが表示されます。

![Metrics relation graph homepage](/media/dashboard/dashboard-metrics-relation-home-v650.png)

**Range Start Time**と<strong>Range Duration</strong>を設定した後、 <strong>Generate Metrics Relation を</strong>クリックすると、メトリック関係グラフのページに入ります。

## グラフを理解する {#understand-graph}

次の図は、メトリック関係グラフの例です。このグラフは、2020-07-29 16:36:00 から 5 分以内の TiDB クラスターでの合計クエリ時間に対する各モニタリング メトリックの時間の割合を示しています。グラフには、各監視メトリックの関係も示されています。

![Metrics relation graph example](/media/dashboard/dashboard-metrics-relation-example.png)

たとえば、 `tidb_execute`モニタリング メトリックのノードの意味は次のとおりです。

-   `tidb_execute`モニタリング メトリックの合計期間は 19306.46 秒で、これは合計クエリ期間の 89.4% を占めます。
-   `tidb_execute`ノード自体の所要時間は 9070.18 秒で、これはクエリの合計所要時間の 42% を占めています。
-   ボックス領域の上にマウスを置くと、合計期間、平均期間、平均 P99 (99 パーセンタイル) 期間など、メトリックの詳細情報が表示されます。

![tidb\_execute node example](/media/dashboard/dashboard-metrics-relation-node-example.png)

### ノード情報 {#node-information}

各ボックス領域はモニタリング メトリックを表し、次の情報を提供します。

-   モニタリング指標の名前
-   モニタリング指標の合計期間
-   クエリの合計時間に対するメトリクスの合計時間の割合

*メトリック ノードの合計期間*=<em>メトリック ノード自体の期間</em>+<em>その子ノードの期間</em>。したがって、一部のノードのメトリック グラフは、ノード自体の期間の合計期間に対する割合を表示します ( `tidb_execute`のグラフなど)。

![tidb\_execute node example1](/media/dashboard/dashboard-metrics-relation-node-example1.png)

-   `tidb_execute`はモニタリング メトリックの名前で、TiDB 実行エンジンでの SQL クエリの実行時間を表します。
-   `19306.46s` 、 `tidb_execute`メトリクスの合計継続時間が 19306.46 秒であることを表します。 `89.40%` 19306.46 秒が、すべての SQL クエリ (ユーザー SQL クエリと TiDB の内部 SQL クエリを含む) に費やされた合計時間の 89.40% を占めていることを表しています。クエリの合計所要時間は、合計`tidb_query`です。
-   `9070.18s` 、 `tidb_execute`ノード自体の合計実行時間が 9070.18 秒であることを表し、残りはその子ノードによって消費された時間です。 `42.00%` 9070.18 秒がすべてのクエリの合計クエリ時間の 42.00% を占めることを表します。

ボックス領域の上にマウスを置くと、 `tidb_execute`メトリック ノードの詳細が表示されます。

![tidb\_execute node example2](/media/dashboard/dashboard-metrics-relation-node-example2.png)

上の画像に表示されているテキスト情報は、合計期間、合計時間、平均期間、および平均期間 P99、P90、および P80 を含むメトリック ノードの説明です。

### ノード間の親子関係 {#the-parent-child-relations-between-nodes}

`tidb_execute`メトリック ノードを例として、このセクションではメトリックの子ノードを紹介します。

![tidb\_execute node relation example1](/media/dashboard/dashboard-metrics-relation-relation-example1.png)

上のグラフから、 `tidb_execute`の 2 つの子ノードを確認できます。

-   `pd_start_tso_wait` : トランザクションの`start_tso`を待機する合計時間 (300.66 秒)。
-   `tidb_txn_cmd` : TiDB が関連するトランザクション コマンドを実行する合計時間 (9935.62 秒)。

さらに、 `tidb_execute`は`tidb_cop`ボックス領域を指す点線の矢印もあり、次のように示されます。

`tidb_execute`には`tidb_cop`メトリックの期間が含まれますが、 `cop`要求が同時に実行される可能性があります。たとえば、2 つのテーブルに対して`join`クエリを実行する`execute`時間は 60 秒であり、その間、結合された 2 つのテーブルに対してテーブル スキャン リクエストが同時に実行されます。 `cop`リクエストの実行時間がそれぞれ 40 秒と 30 秒の場合、 `cop`リクエストの合計所要時間は 70 秒です。ただし、 `execute`持続時間はわずか 60 秒です。したがって、親ノードの期間に子ノードの期間が完全に含まれていない場合は、点線の矢印を使用して子ノードを指します。

> **ノート：**
>
> ノードに子ノードを指す点線の矢印がある場合、このノード自体の持続時間は不正確です。たとえば、 `tidb_execute`ノードでは、ノード自体の期間は 9070.18 秒 ( `9070.18 = 19306.46 - 300.66 - 9935.62` ) です。この式では、 `tidb_cop`子ノードの期間は`tidb_execute`の子ノードの期間に計算されません。しかし、実際にはそうではありません。 9070.18 秒という`tidb_execute`自体のデュレーションには、 `tidb_cop`デュレーションの一部が含まれており、この部分のデュレーションは特定できません。

### <code>tidb_kv_request</code>とその親ノード {#code-tidb-kv-request-code-and-its-parent-nodes}

![tidb\_execute node relation example2](/media/dashboard/dashboard-metrics-relation-relation-example2.png)

`tidb_kv_request`の親ノードである`tidb_cop`と`tidb_txn_cmd.get`は、両方とも`tidb_kv_request`を指す点線の矢印があり、次のように示されます。

-   `tidb_cop`の持続時間には`tidb_kv_request`の持続時間の一部が含まれます。
-   `tidb_txn_cmd.get`の持続時間には`tidb_kv_request`の持続時間の一部も含まれます。

ただし、 `tidb_kv_request`の期間が`tidb_cop`にどのくらい含まれているかを判断するのは困難です。

-   `tidb_kv_request.Get` : TiDB が`Get`種類のキー値リクエストを送信する期間。
-   `tidb_kv_request.Cop` : TiDB が`Cop`種類のキー値リクエストを送信する期間。

`tidb_kv_request`は子ノードとして`tidb_kv_request.Get`と`tidb_kv_request.Cop`ノードは含まれませんが、後者の 2 つのノードで構成されます。子ノードの名前プレフィックスは、親ノードの名前に`.xxx`を加えたものです。これは、子ノードが親ノードのサブクラスであることを意味します。この場合は、次のように理解できます。

TiDB がキー値リクエストを送信する合計時間は 14745.07 秒で、その間に`Get`と`Cop`タイプのキー値リクエストはそれぞれ 9798.02 秒と 4946.46 秒を消費します。
