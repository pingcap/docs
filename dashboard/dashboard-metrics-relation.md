---
title: TiDB Dashboard Metrics Relation Graph
summary: Learn TiDB Dashboard metrics relation graph.
---

# TiDBダッシュボードメトリクス関係グラフ {#tidb-dashboard-metrics-relation-graph}

TiDBダッシュボードメトリック関係グラフは、v4.0.7で導入された機能です。この機能は、TiDBクラスタの各内部プロセスの期間の監視データの関係グラフを表示します。目的は、各プロセスの期間とそれらの関係をすばやく理解できるようにすることです。

## アクセスグラフ {#access-graph}

TiDBダッシュボードにログインし、左側のナビゲーションメニューで[**クラスター診断**]をクリックすると、メトリック関係グラフを生成するページが表示されます。

![Metrics relation graph homepage](/media/dashboard/dashboard-metrics-relation-home.png)

**Range StartTime**と<strong>RangeDurationを</strong>設定した後、 <strong>Generate Metrics Relation</strong>ボタンをクリックすると、メトリック関係グラフのページに入ります。

## グラフを理解する {#understand-graph}

次の画像は、メトリック関係グラフの例です。このグラフは、2020-07-2916:36:00から5分以内のTiDBクラスタの合計クエリ期間に対する各監視メトリックの期間の割合を示しています。グラフは、各監視メトリックの関係も示しています。

![Metrics relation graph example](/media/dashboard/dashboard-metrics-relation-example.png)

たとえば、 `tidb_execute`の監視メトリックのノードの意味は次のとおりです。

-   `tidb_execute`の監視メトリックの合計期間は19306.46秒であり、これは合計クエリ期間の89.4％を占めます。
-   `tidb_execute`ノード自体の期間は9070.18秒であり、これは合計クエリ期間の42％を占めます。
-   ボックス領域にマウスを合わせると、合計期間、平均期間、平均P99（99パーセンタイル）期間など、メトリックの詳細情報が表示されます。

![tidb\_execute node example](/media/dashboard/dashboard-metrics-relation-node-example.png)

### ノード情報 {#node-information}

各ボックス領域は監視メトリックを表し、次の情報を提供します。

-   監視メトリックの名前
-   監視メトリックの合計期間
-   合計クエリ期間に対するメトリックの合計期間の比率

*メトリックノードの合計期間*=<em>メトリックノード自体</em><em>の期間+その子ノードの期間</em>。したがって、一部のノードのメトリックグラフには、 `tidb_execute`のグラフなど、合計期間に対するノード自体の期間の比率が表示されます。

![tidb\_execute node example1](/media/dashboard/dashboard-metrics-relation-node-example1.png)

-   `tidb_execute`は監視メトリックの名前であり、TiDB実行エンジンでのSQLクエリの実行期間を表します。
-   `19306.46s`は、 `tidb_execute`メトリックの合計期間が19306.46秒であることを表します。 `89.40%`は、19306.46秒がすべてのSQLクエリ（ユーザーSQLクエリとTiDBの内部SQLクエリを含む）に費やされる合計時間の89.40％を占めることを表します。合計クエリ期間は`tidb_query`の合計期間です。
-   `9070.18s`は、 `tidb_execute`ノード自体の合計実行時間が9070.18秒であることを表し、残りはその子ノードによって消費される時間です。 `42.00%`は、9070.18秒がすべてのクエリの合計クエリ期間の42.00％を占めることを表します。

ボックス領域にマウスを合わせると、 `tidb_execute`メトリックノードの詳細が表示されます。

![tidb\_execute node example2](/media/dashboard/dashboard-metrics-relation-node-example2.png)

上の画像に表示されているテキスト情報は、合計期間、合計時間、平均期間、平均期間P99、P90、およびP80を含むメトリックノードの説明です。

### ノード間の親子関係 {#the-parent-child-relations-between-nodes}

このセクションでは、 `tidb_execute`のメトリックノードを例として、メトリックの子ノードを紹介します。

![tidb\_execute node relation example1](/media/dashboard/dashboard-metrics-relation-relation-example1.png)

上のグラフから、 `tidb_execute`の2つの子ノードを確認できます。

-   `pd_start_tso_wait` ：トランザクションの`start_tso`を待機する合計時間（300.66秒）。
-   `tidb_txn_cmd` ：関連するトランザクションコマンドを実行するTiDBの合計時間（9935.62秒）。

さらに、 `tidb_execute`には`tidb_cop`ボックス領域を指す点線の矢印もあります。これは次のことを示しています。

`tidb_execute`には`tidb_cop`のメトリックの期間が含まれますが、 `cop`の要求が同時に実行される場合があります。たとえば、2つのテーブルで`join`つのクエリを実行する`execute`の期間は60秒であり、その間、テーブルスキャン要求は結合された2つのテーブルで同時に実行されます。 `cop`のリクエストの実行時間がそれぞれ40秒と30秒の場合、 `cop`のリクエストの合計時間は70秒になります。ただし、 `execute`の継続時間はわずか60秒です。したがって、親ノードの期間に子ノードの期間が完全に含まれていない場合は、点線の矢印を使用して子ノードを指します。

> **ノート：**
>
> ノードに子ノードを指す点線の矢印がある場合、このノード自体の期間は不正確です。たとえば、 `tidb_execute`ノードでは、ノード自体の継続時間は9070.18秒（ `9070.18 = 19306.46 - 300.66 - 9935.62` ）です。この式では、 `tidb_cop`つの子ノードの期間は`tidb_execute`の子ノードの期間に計算されません。しかし実際には、これは真実ではありません。 `tidb_execute`自体の持続時間である9070.18秒には、 `tidb_cop`の持続時間の一部が含まれており、この部分の持続時間は決定できません。

### <code>tidb_kv_request</code>とその親ノード {#code-tidb-kv-request-code-and-its-parent-nodes}

![tidb\_execute node relation example2](/media/dashboard/dashboard-metrics-relation-relation-example2.png)

`tidb_kv_request`の親ノードである`tidb_cop`と`tidb_txn_cmd.get`には、どちらも`tidb_kv_request`を指す点線の矢印があります。これは次のことを示しています。

-   `tidb_cop`の期間には、 `tidb_kv_request`の期間の一部が含まれます。
-   `tidb_txn_cmd.get`の期間には、 `tidb_kv_request`の期間の一部も含まれます。

ただし、 `tidb_cop`に含まれる`tidb_kv_request`の期間を判断するのは困難です。

-   `tidb_kv_request.Get` ：TiDBが`Get`のタイプのKey-Valueリクエストを送信する期間。
-   `tidb_kv_request.Cop` ：TiDBが`Cop`のタイプのKey-Valueリクエストを送信する期間。

`tidb_kv_request`には、子ノードとして`tidb_kv_request.Get`ノードと`tidb_kv_request.Cop`ノードは含まれませんが、後者の2つのノードで構成されます。子ノードの名前プレフィックスは、親ノードの名前に`.xxx`を加えたものです。これは、子ノードが親ノードのサブクラスであることを意味します。このケースは次のように理解できます。

キー値要求を送信するTiDBの合計時間は14745.07秒であり、その間、 `Get`タイプと`Cop`タイプのキー値要求はそれぞれ9798.02秒と4946.46秒を消費します。
