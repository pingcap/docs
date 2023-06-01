---
title: TiDB Cloud Built-in Alerting
summary: Learn how to monitor your TiDB cluster by getting alert notification emails from TiDB Cloud.
---

# TiDB Cloud組み込みアラート {#tidb-cloud-built-in-alerting}

TiDB Cloud組み込みアラート機能を使用すると、プロジェクト内のTiDB Cloudクラスターが TiDB TiDB Cloud組み込みアラート条件の 1 つをトリガーするたびに、電子メールで通知を受ける簡単な方法が提供されます。

このドキュメントでは、 TiDB Cloudからのアラート通知電子メールを購読する方法について説明し、参考のためにTiDB Cloudに組み込まれたアラート条件も提供します。

## 制限 {#limitation}

TiDB Cloudの組み込みアラートをカスタマイズすることはできません。さまざまなトリガー条件、しきい値、または頻度を構成したい場合、または[プロメテウスとグラファナの統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)をサポートしています。

## アラート通知メールを購読する {#subscribe-to-alert-notification-emails}

プロジェクトのメンバーであり、プロジェクト内のクラスターのアラート通知電子メールを受け取りたい場合は、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  [**クラスター**](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ウィンドウで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えて、 **[管理]** &gt; **[アラート]**をクリックします。
    -   プロジェクトが 1 つだけの場合は、 **[管理]** &gt; **[アラート]**をクリックします。

3.  電子メール アドレスを入力し、 **[購読]**をクリックします。

加入者に送信されるアラート電子メールの数を最小限に抑えるために、 TiDB Cloudはアラートを 1 つの電子メールに集約し、3 時間ごとに送信します。

## アラート通知メールの購読を解除する {#unsubscribe-from-alert-notification-emails}

プロジェクト内のクラスターのアラート通知電子メールを受信したくない場合は、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  [**クラスター**](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ウィンドウで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えて、 **[管理]** &gt; **[アラート]**をクリックします。
    -   プロジェクトが 1 つだけの場合は、 **[管理]** &gt; **[アラート]**をクリックします。

3.  右側のペインで電子メール アドレスを見つけて、 **[削除]**をクリックします。

## TiDB Cloudの組み込みアラート条件 {#tidb-cloud-built-in-alert-conditions}

次の表に、 TiDB Cloud の組み込みアラート条件と、対応する推奨アクションを示します。

> **ノート：**
>
> これらのアラート状態は必ずしも問題があることを意味するわけではありませんが、多くの場合、新たな問題の早期警告指標となります。したがって、推奨されるアクションを取ることをお勧めします。

| 状態                                            | 推奨される行動                                                                                                                                                                                                                                                                                                                                                                                               |
| :-------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| クラスター全体の合計 TiDB ノードメモリ使用率が 10 分間で 70% を超えました  | プロジェクト XYZ のクラスター ABC の合計 TiDB ノードメモリ使用率が 10 分間で 70% を超えました。これが継続することが予想される場合は、TiDB ノードを追加することをお勧めします。ノードのメモリ使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                                                            |
| クラスター全体の合計 TiKV ノードメモリ使用率が 10 分間で 70% を超えました  | プロジェクト XYZ のクラスター ABC の合計 TiKV ノードメモリ使用率が 10 分間で 70% を超えました。この状態が継続すると予想される場合は、TiKV ノードを追加することをお勧めします。ノードのメモリ使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                                                            |
| クラスター全体の合計TiFlashノードメモリ使用率が 10 分間で 70% を超えました | プロジェクト XYZ のクラスター ABC の合計TiFlashノードメモリ使用率が 10 分間で 70% を超えました。これが継続することが予想される場合は、 TiFlashノードを追加することをお勧めします。ノードのメモリ使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                                                        |
| `*`クラスター内の少なくとも 1 つの TiDB ノードでメモリが不足しています     | プロジェクト XYZ のクラスター ABC 内の少なくとも 1 つの TiDB ノードが SQL ステートメントの実行中にメモリ不足になりました。 `tidb_mem_quota_query`セッション変数を使用してクエリに使用できるメモリを増やすことを検討してください。ノードのメモリ使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                          |
| TiDB ノードの合計 CPU 使用率が 10 分間で 80% を超えました        | プロジェクト XYZ のクラスター ABC の合計 TiDB ノード CPU 使用率が 10 分間 80% を超えました。これが継続することが予想される場合は、TiDB ノードを追加することをお勧めします。ノードの CPU 使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                                                         |
| TiKV ノードの合計 CPU 使用率が 10 分間で 80% を超えました        | プロジェクト XYZ のクラスター ABC の合計 TiKV ノード CPU 使用率が 10 分間 80% を超えました。この状態が継続すると予想される場合は、TiKV ノードを追加することをお勧めします。ノードの CPU 使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                                                         |
| TiFlashノードの合計 CPU 使用率が 10 分間で 80% を超えました      | プロジェクト XYZ のクラスター ABC の合計TiFlashノード CPU 使用率が 10 分間 80% を超えました。これが継続することが予想される場合は、 TiFlashノードを追加することをお勧めします。ノードの CPU 使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                                                     |
| `*` TiKVstorage使用率が 80% を超えています               | プロジェクト XYZ のクラスター ABC の合計 TiKVstorage使用率が 80% を超えています。 TiKV ノードを追加してstorage容量を増やすことをお勧めします。storage使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                                                                       |
| `*` TiFlashstorage使用率が 80% を超えています            | プロジェクト XYZ のクラスター ABC の合計TiFlashstorage使用率が 80% を超えています。 TiFlashノードを追加してstorage容量を増やすことをお勧めします。storage使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                                                                   |
| クラスタノードがオフラインです                               | プロジェクト XYZ のクラスター ABC の一部またはすべてのノードがオフラインです。 TiDB Cloud運用チームはこの問題を認識しており、解決に取り組んでいます。最新情報は[クラスタステータスとノードステータス](/tidb-cloud/monitor-tidb-cluster.md#cluster-status-and-node-status)参照してください。 |

> **ノート：**
>
> -   [Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) **[条件]**列で`*`とマークされているアラート条件のサブセットのみをサポートします。
> -   **推奨アクション**列の「クラスタ ABC」および「プロジェクト XYZ」は、参考のための名前の例です。
