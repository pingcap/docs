---
title: TiDB Cloud Built-in Alerting
summary: Learn how to monitor your TiDB cluster by getting alert notification emails from TiDB Cloud.
---

# TiDBクラウドビルトインアラート {#tidb-cloud-built-in-alerting}

TiDB Cloudの組み込みアラート機能は、プロジェクト内のTiDBCloudクラスタがTiDBCloudの組み込みアラート条件の1つをトリガーするたびに、電子メールで通知される簡単な方法を提供します。

このドキュメントでは、TiDB Cloudからのアラート通知メールをサブスクライブする方法について説明し、参照用にTiDBCloudに組み込まれているアラート条件も提供します。

## 制限 {#limitation}

TiDBCloudの組み込みアラートをカスタマイズすることはできません。さまざまなトリガー条件、しきい値、または頻度を構成する場合、またはアラートが[PagerDuty](https://www.pagerduty.com/docs/guides/datadog-integration-guide/)などのダウンストリームサービスでアクションを自動的にトリガーするようにする場合は、サードパーティの監視とアラートの統合の使用を検討してください。現在、TiDBCloudは[Datadogの統合](/tidb-cloud/monitor-datadog-integration.md)と[PrometheusとGrafanaの統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)をサポートしています。

## アラート通知メールを購読する {#subscribe-to-alert-notification-emails}

プロジェクトのメンバーであり、プロジェクト内のクラスターのアラート通知メールを受け取りたい場合は、次の手順を実行します。

1.  TiDBCloudコンソールにログインします。
2.  TiDB Cloudコンソールで、アラート通知メールを受信するプロジェクトを選択し、左上隅の歯車アイコンをクリックしてプロジェクト設定を開きます。
3.  左側のペインで、[**アラート**]をクリックします。
4.  メールアドレスを入力し、[**購読**]をクリックします。

サブスクライバーに送信されるアラートEメールの数を最小限に抑えるために、TiDBCloudはアラートを3時間ごとに送信される単一のEメールに集約します。

## アラート通知メールの購読を解除する {#unsubscribe-from-alert-notification-emails}

プロジェクト内のクラスターのアラート通知メールを受信する必要がなくなった場合は、次の手順を実行します。

1.  TiDBCloudコンソールにログインします。
2.  TiDB Cloudコンソールで、アラート通知メールを受信する必要がなくなったプロジェクトを選択します。
3.  左側のペインで、[**アラート**]をクリックします。
4.  右側のペインで、メールアドレスを見つけて[**削除**]をクリックします。

## TiDBCloudの組み込みアラート条件 {#tidb-cloud-built-in-alert-conditions}

次の表に、TiDBクラウドの組み込みアラート条件と対応する推奨アクションを示します。

> **ノート：**
>
> これらのアラート状態は必ずしも問題があることを意味するわけではありませんが、多くの場合、新たな問題の早期警告インジケーターです。したがって、推奨されるアクションを実行することをお勧めします。

| 調子                                                      | 推奨される行動                                                                                                                                                                                                                                                          |
| :------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| クラスタ全体のTiDBノードの合計メモリ使用率が10分間で70％を超えました                  | プロジェクトXYZのクラスタABCの合計TiDBノードメモリ使用率が10分間で70％を超えました。これが続くと予想される場合は、TiDBノードを追加することをお勧めします。ノードのメモリ使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                            |
| クラスタ全体のTiKVノードの合計メモリ使用率が10分間で70％を超えました                  | プロジェクトXYZのクラスタABCの合計TiKVノードメモリ使用率が10分間で70％を超えました。これが続くと予想される場合は、TiKVノードを追加することをお勧めします。ノードのメモリ使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                            |
| クラスタ全体のTiFlash<sup>ベータ</sup>ノードの合計メモリ使用率が10分間で70％を超えました | プロジェクトXYZのクラスタABCの合計TiFlash<sup>ベータ</sup>ノードメモリ使用率は、10分間で70％を超えました。これが続くと予想される場合は、TiFlash<sup>ベータ</sup>ノードを追加することをお勧めします。ノードのメモリ使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                         |
| `*`クラスタの少なくとも1つのTiDBノードでメモリが不足しています                     | プロジェクトXYZのクラスタABCの少なくとも1つのTiDBノードが、SQLステートメントの実行中にメモリーを使い果たしました。 `tidb_mem_quota_query`セッション変数を使用してクエリに使用できるメモリを増やすことを検討してください。ノードのメモリ使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                   |
| TiDBノードの合計CPU使用率が10分間で80％を超えました                         | プロジェクトXYZのクラスタABCの合計TiDBノードCPU使用率が10分間で80％を超えました。これが続くと予想される場合は、TiDBノードを追加することをお勧めします。ノードのCPU使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                            |
| TiKVノードの合計CPU使用率が10分間で80％を超えました                         | プロジェクトXYZのクラスタABCの合計TiKVノードCPU使用率は、10分間で80％を超えました。これが続くと予想される場合は、TiKVノードを追加することをお勧めします。ノードのCPU使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                           |
| TiFlash<sup>ベータ</sup>ノードの合計CPU使用率が10分間で80％を超えました        | プロジェクトXYZのクラスタABCの合計TiFlash<sup>ベータ</sup>ノードCPU使用率は、10分間で80％を超えました。これが続くと予想される場合は、TiFlash<sup>ベータ</sup>ノードを追加することをお勧めします。ノードのCPU使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                         |
| `*` TiKVストレージ使用率が80％を超える                                | プロジェクトXYZのクラスタABCの合計TiKVストレージ使用率が80％を超えています。ストレージ容量を増やすために、TiKVノードを追加することをお勧めします。ストレージ使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                                                   |
| `*` TiFlash<sup>ベータ</sup>ストレージの使用率が80％を超えています           | プロジェクトXYZのクラスタABCの合計TiFlash<sup>ベータ</sup>ストレージ使用率は80％を超えています。ストレージ容量を増やすために、TiFlash<sup>ベータ</sup>ノードを追加することをお勧めします。ストレージ使用率を監視するには、 [モニタリング指標](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics)を参照してください。                                                 |
| クラスタノードはオフラインです                                         | プロジェクトXYZのクラスタABCの一部またはすべてのノードがオフラインです。 TiDBクラウドオペレーションチームは、問題を認識して解決に取り組んでいます。最新情報は[TiDBクラウドステータス](https://status.tidbcloud.com/)を参照してください。ノードのステータスを監視するには、 [クラスタステータスとノードステータス](/tidb-cloud/monitor-tidb-cluster.md#cluster-status-and-node-status)を参照してください。 |

> **ノート：**
>
> -   [開発者層クラスター](/tidb-cloud/select-cluster-tier.md#developer-tier)は、[**条件**]列で`*`とマークされているアラート条件のサブセットのみをサポートします。
> -   「**推奨処置」**列の「クラスタABC」および「プロジェクトXYZ」は、参照用の名前の例です。
