---
title: TiDB Cloud Built-in Alerting
summary: Learn how to monitor your TiDB cluster by getting alert notification emails from TiDB Cloud.
---

# TiDB Cloudの組み込みアラート {#tidb-cloud-built-in-alerting}

TiDB Cloud組み込みアラート機能を使用すると、プロジェクト内のTiDB CloudクラスターがTiDB Cloud組み込みアラート条件のいずれかをトリガーするたびに、電子メールで簡単に通知を受けることができます。

このドキュメントでは、 TiDB Cloudからのアラート通知メールをサブスクライブする方法について説明し、参照用にTiDB Cloud組み込みのアラート条件も提供します。

## 制限 {#limitation}

TiDB Cloudの組み込みアラートをカスタマイズすることはできません。さまざまなトリガー条件、しきい値、または頻度を構成する場合、または[PagerDuty](https://www.pagerduty.com/docs/guides/datadog-integration-guide/)のようなダウンストリーム サービスでアラートが自動的にアクションをトリガーするようにする場合は、サードパーティの監視およびアラート統合の使用を検討してください。現在、 TiDB Cloudは[Datadog の統合](/tidb-cloud/monitor-datadog-integration.md)と[Prometheus と Grafana の統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)をサポートしています。

## アラート通知メールを購読する {#subscribe-to-alert-notification-emails}

プロジェクトのメンバーであり、プロジェクト内のクラスターのアラート通知メールを受け取りたい場合は、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  [**クラスター**](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ペインで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えてから、[**管理**] &gt; [<strong>アラート</strong>] をクリックします。
    -   プロジェクトが 1 つしかない場合は、[**管理**] &gt; [<strong>アラート</strong>] をクリックします。

3.  電子メール アドレスを入力し、[**購読**] をクリックします。

サブスクライバーに送信されるアラート電子メールの数を最小限に抑えるために、 TiDB Cloudはアラートを 1 つの電子メールに集約し、3 時間ごとに送信します。

## アラート通知メールの登録を解除する {#unsubscribe-from-alert-notification-emails}

プロジェクト内のクラスターのアラート通知メールを受信したくない場合は、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  [**クラスター**](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ペインで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えてから、[**管理**] &gt; [<strong>アラート</strong>] をクリックします。
    -   プロジェクトが 1 つしかない場合は、[**管理**] &gt; [<strong>アラート</strong>] をクリックします。

3.  右側のペインで、電子メール アドレスを見つけて [**削除**] をクリックします。

## TiDB Cloud組み込みアラート条件 {#tidb-cloud-built-in-alert-conditions}

次の表は、 TiDB Cloudの組み込みアラート条件と、対応する推奨アクションを示しています。

> **ノート：**
>
> これらのアラート状態は、必ずしも問題があることを意味するわけではありませんが、多くの場合、新たな問題の早期警告指標です。したがって、推奨されるアクションを実行することをお勧めします。

| 状態                                              | 推奨される行動                                                                                                                                                                                                                                                                              |
| :---------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| クラスタ全体の TiDB ノード メモリの合計使用率が 10 分間で 70% を超えました   | プロジェクト XYZ のクラスター ABC の TiDB ノード メモリの合計使用率が 10 分間で 70% を超えました。これが続くと予想される場合は、TiDB ノードを追加することをお勧めします。ノードのメモリー使用率をモニターするには、 [指標のモニタリング](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                              |
| クラスタ全体の TiKV ノード メモリの合計使用率が 10 分間で 70% を超えました   | プロジェクト XYZ のクラスター ABC の TiKV ノード メモリの合計使用率が 10 分間で 70% を超えました。これが続くと予想される場合は、TiKV ノードを追加することをお勧めします。ノードのメモリー使用率をモニターするには、 [指標のモニタリング](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                              |
| クラスタ全体の TiFlashノード メモリの合計使用率が 10 分間で 70% を超えました | プロジェクト XYZ のクラスター ABC のTiFlashノード メモリの合計使用率が 10 分間で 70% を超えました。これが続くと予想される場合は、 TiFlashノードを追加することをお勧めします。ノードのメモリー使用率をモニターするには、 [指標のモニタリング](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                          |
| `*`クラスタ内の少なくとも 1 つの TiDB ノードでメモリが不足しています        | プロジェクト XYZ のクラスター ABC 内の少なくとも 1 つの TiDB ノードで、SQL ステートメントの実行中にメモリが不足しました。 `tidb_mem_quota_query`セッション変数を使用してクエリに使用できるメモリを増やすことを検討してください。ノードのメモリ使用率を監視するには、 [指標のモニタリング](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                              |
| TiDB ノードの合計 CPU 使用率が 10 分間で 80% を超えました          | プロジェクト XYZ のクラスター ABC の TiDB ノードの合計 CPU 使用率が 10 分間で 80% を超えました。これが続くと予想される場合は、TiDB ノードを追加することをお勧めします。ノードの CPU 使用率を監視するには、 [指標のモニタリング](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                              |
| TiKV ノードの合計 CPU 使用率が 10 分間で 80% を超えました          | プロジェクト XYZ のクラスター ABC の TiKV ノード CPU 使用率の合計が 10 分間で 80% を超えました。これが続くと予想される場合は、TiKV ノードを追加することをお勧めします。ノードの CPU 使用率を監視するには、 [指標のモニタリング](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                              |
| TiFlashノードの合計 CPU 使用率が 10 分間で 80% を超えました        | プロジェクト XYZ のクラスター ABC のTiFlashノードの合計 CPU 使用率が 10 分間で 80% を超えました。これが続くと予想される場合は、 TiFlashノードを追加することをお勧めします。ノードの CPU 使用率を監視するには、 [指標のモニタリング](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                          |
| `*` TiKV ストレージ使用率が 80% を超えています                  | プロジェクト XYZ のクラスター ABC の TiKV ストレージの合計使用率が 80% を超えています。ストレージ容量を増やすには、TiKV ノードを追加することをお勧めします。ストレージ使用率をモニターするには、 [指標のモニタリング](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                          |
| `*` TiFlashストレージ使用率が 80% を超えています                | プロジェクト XYZ のクラスター ABC のTiFlashストレージの合計使用率が 80% を超えています。ストレージ容量を増やすには、 TiFlashノードを追加することをお勧めします。ストレージ使用率をモニターするには、 [指標のモニタリング](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                      |
| クラスタノードがオフラインです                                 | プロジェクト XYZ のクラスタ ABC の一部またはすべてのノードがオフラインです。 TiDB Cloud Operations チームはこの問題を認識しており、解決に取り組んでいます。最新情報は[TiDB Cloudのステータス](https://status.tidbcloud.com/)を参照してください。ノードのステータスを監視するには、 [クラスタのステータスとノードのステータス](/tidb-cloud/monitor-tidb-cluster.md#cluster-status-and-node-status)を参照してください。 |

> **ノート：**
>
> -   [Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)は、 **Condition**列で`*`とマークされているアラート条件のサブセットのみをサポートします。
> -   **推奨されるアクション**列の「クラスター ABC」と「プロジェクト XYZ」は、参照用の名前の例です。
