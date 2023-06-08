---
title: Third-Party Metrics Integrations
summary: Learn how to use third-party metrics integrations.
---

# サードパーティのメトリクスの統合 {#third-party-metrics-integrations}

TiDB Cloudをサードパーティのメトリクス サービスと統合して、 TiDB Cloudアラートを受信し、メトリクス サービスを使用して TiDB クラスターのパフォーマンス メトリクスを表示できます。

## 必要なアクセス {#required-access}

サードパーティ統合設定を編集するには、組織への`Owner`アクセス権、またはターゲット プロジェクトへの`Member`アクセス権が必要です。

## サードパーティ統合をビューまたは変更する {#view-or-modify-third-party-integrations}

1.  [<a href="https://tidbcloud.com">TiDB Cloudコンソール</a>](https://tidbcloud.com)にログインします。
2.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ウィンドウで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えて、 **[管理]** &gt; **[統合]**をクリックします。
    -   プロジェクトが 1 つだけの場合は、 **[管理]** &gt; **[統合]**をクリックします。

利用可能なサードパーティ統合が表示されます。

## 制限 {#limitation}

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverless</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターの場合、サードパーティのメトリック統合はサポートされていません。

-   クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAused** 、または**RESUMING**の場合、サードパーティのメトリック統合は使用できません。

## 利用可能な統合 {#available-integrations}

### Datadog の統合 {#datadog-integration}

Datadog の統合を使用すると、TiDB クラスターに関するメトリクス データを[<a href="https://www.datadoghq.com/">データドッグ</a>](https://www.datadoghq.com/)に送信し、これらのメトリクスを Datadog ダッシュボードに表示するようにTiDB Cloudを構成できます。

詳細な統合手順と Datadog が追跡するメトリクスのリストについては、 [<a href="/tidb-cloud/monitor-datadog-integration.md">TiDB Cloudと Datadog を統合する</a>](/tidb-cloud/monitor-datadog-integration.md)を参照してください。

### プロメテウスとグラファナの統合 {#prometheus-and-grafana-integration}

Prometheus と Grafana の統合により、 TiDB Cloudから Prometheus のscrape_config ファイルを取得し、そのファイルの内容を使用して Prometheus を構成できます。これらのメトリクスは、Grafana ダッシュボードで表示できます。

詳細な統合手順と Prometheus が追跡するメトリクスのリストについては、 [<a href="/tidb-cloud/monitor-prometheus-and-grafana-integration.md">TiDB CloudをPrometheus および Grafana と統合する</a>](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)を参照してください。

### New Relicの統合 {#new-relic-integration}

New Relic の統合を使用すると、TiDB クラスターに関するメトリック データを[<a href="https://newrelic.com/">ニューレリック</a>](https://newrelic.com/)に送信し、New Relic ダッシュボードでこれらのメトリックを表示するようにTiDB Cloudを構成できます。

詳細な統合手順と New Relic が追跡するメトリクスのリストについては、 [<a href="/tidb-cloud/monitor-new-relic-integration.md">TiDB Cloudと New Relic を統合する</a>](/tidb-cloud/monitor-new-relic-integration.md)を参照してください。
