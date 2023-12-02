---
title: Third-Party Metrics Integrations（Beta）
summary: Learn how to use third-party metrics integrations.
---

# サードパーティのメトリクス統合（ベータ版） {#third-party-metrics-integrations-beta}

TiDB Cloudをサードパーティのメトリクス サービスと統合して、 TiDB Cloudアラートを受信し、メトリクス サービスを使用して TiDB クラスターのパフォーマンス メトリクスを表示できます。サードパーティのメトリクス統合は現在ベータ版です。

## 必要なアクセス {#required-access}

サードパーティ統合設定を編集するには、組織の`Organization Owner`ロール、またはターゲット プロジェクトの`Project Owner`ロールに属している必要があります。

## サードパーティ統合をビューまたは変更する {#view-or-modify-third-party-integrations}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。
2.  クリック<mdsvgicon name="icon-left-projects">複数のプロジェクトがある場合は、左下隅でターゲット プロジェクトに切り替え、 **[プロジェクト設定]**をクリックします。</mdsvgicon>
3.  プロジェクトの**[プロジェクト設定]**ページで、左側のナビゲーション ペインの**[統合]**をクリックします。

利用可能なサードパーティ統合が表示されます。

## 制限 {#limitation}

-   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの場合、サードパーティのメトリック統合はサポートされていません。

-   クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAused** 、または**RESUMING**の場合、サードパーティのメトリック統合は使用できません。

## 利用可能な統合 {#available-integrations}

### Datadog の統合 (ベータ版) {#datadog-integration-beta}

Datadog 統合を使用すると、TiDB クラスターに関するメトリクス データを[データドッグ](https://www.datadoghq.com/)に送信し、Datadog ダッシュボードでこれらのメトリクスを表示するようにTiDB Cloudを構成できます。

詳細な統合手順と Datadog が追跡するメトリクスのリストについては、 [TiDB Cloudと Datadog を統合する](/tidb-cloud/monitor-datadog-integration.md)を参照してください。

### Prometheus と Grafana の統合 (ベータ版) {#prometheus-and-grafana-integration-beta}

Prometheus と Grafana の統合により、 TiDB Cloudから Prometheus のscrape_config ファイルを取得し、そのファイルの内容を使用して Prometheus を構成できます。これらのメトリクスは、Grafana ダッシュボードで表示できます。

詳細な統合手順と Prometheus が追跡するメトリクスのリストについては、 [TiDB CloudをPrometheus および Grafana と統合する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)を参照してください。

### New Relic の統合 (ベータ版) {#new-relic-integration-beta}

New Relic の統合を使用すると、TiDB クラスターに関するメトリック データを[ニューレリック](https://newrelic.com/)に送信し、New Relic ダッシュボードでこれらのメトリックを表示するようにTiDB Cloudを構成できます。

詳細な統合手順と New Relic が追跡するメトリクスのリストについては、 [TiDB Cloudと New Relic を統合する](/tidb-cloud/monitor-new-relic-integration.md)を参照してください。
