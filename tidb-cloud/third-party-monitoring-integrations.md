---
title: Third-Party Monitoring Integrations
summary: Learn how to use third-party monitoring integrations.
---

# サードパーティの監視統合 {#third-party-monitoring-integrations}

TiDB Cloudをサードパーティの監視サービスと統合して、 TiDB Cloudアラートを受信し、監視サービスを使用して TiDB クラスターのパフォーマンス メトリックを表示できます。

## 必要なアクセス {#required-access}

サードパーティの統合設定を編集するには、組織への`Owner`アクセス権またはターゲット プロジェクトへの`Member`アクセス権が必要です。

## サードパーティの統合をビューまたは変更する {#view-or-modify-third-party-integrations}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。
2.  [**クラスター**](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ペインで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えてから、 **[管理]** &gt; <strong>[統合]</strong>をクリックします。
    -   プロジェクトが 1 つしかない場合は、 **[管理]** &gt; <strong>[統合]</strong>をクリックします。

利用可能なサードパーティ統合が表示されます。

## 制限 {#limitation}

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターの場合、サードパーティの監視統合はサポートされていません。

-   クラスターのステータスが**CREATING** 、 <strong>RESTORING</strong> 、 <strong>PAUSED</strong> 、または<strong>RESUMING</strong>の場合、サードパーティの監視統合は使用できません。

## 利用可能な統合 {#available-integrations}

### Datadog の統合 {#datadog-integration}

Datadog 統合により、TiDB クラスターに関するメトリクス データを[データドッグ](https://www.datadoghq.com/)に送信し、Datadog ダッシュボードでこれらのメトリクスを表示するようにTiDB Cloudを構成できます。

詳細な統合手順と Datadog が追跡するメトリクスのリストについては、 [TiDB Cloudと Datadog の統合](/tidb-cloud/monitor-datadog-integration.md)を参照してください。

### Prometheus と Grafana の統合 {#prometheus-and-grafana-integration}

Prometheus と Grafana の統合により、 TiDB Cloudから Prometheus の Scrape_config ファイルを取得し、そのファイルの内容を使用して Prometheus を構成できます。これらのメトリックは、Grafana ダッシュボードで表示できます。

詳細な統合手順と Prometheus が追跡するメトリクスのリストについては、 [TiDB CloudをPrometheus および Grafana と統合する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)を参照してください。

### New Relic の統合 {#new-relic-integration}

New Relic の統合により、TiDB クラスターに関するメトリクス データを[ニューレリック](https://newrelic.com/)に送信し、これらのメトリクスを New Relic ダッシュボードで表示するようにTiDB Cloudを構成できます。

詳細な統合手順と New Relic が追跡するメトリクスのリストについては、 [TiDB CloudをNew Relic と統合する](/tidb-cloud/monitor-new-relic-integration.md)を参照してください。
