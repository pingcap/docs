---
title: Third-Party Monitoring Integrations
summary: Learn how to use third-party monitoring integrations.
---

# サードパーティの監視統合 {#third-party-monitoring-integrations}

TiDB Cloudをサードパーティの監視サービスと統合して、 TiDB Cloudアラートを受信し、監視サービスを使用して TiDB クラスターのパフォーマンス メトリクスを表示できます。

> **ノート：**
>
> [Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)の場合、サードパーティの監視統合はサポートされていません。

## 必要なアクセス {#required-access}

サードパーティ統合設定を編集するには、組織への`Owner`アクセス権、またはターゲット プロジェクトへの`Member`アクセス権が必要です。

## サードパーティ統合をビューまたは変更する {#view-or-modify-third-party-integrations}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。
2.  [**クラスター**](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ウィンドウで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えて、 **[管理]** &gt; **[統合]**をクリックします。
    -   プロジェクトが 1 つだけの場合は、 **[管理]** &gt; **[統合]**をクリックします。

利用可能なサードパーティ統合が表示されます。

## 利用可能な統合 {#available-integrations}

### Datadog の統合 {#datadog-integration}

Datadog の統合を使用すると、TiDB クラスターに関するメトリクス データを[データドッグ](https://www.datadoghq.com/)に送信し、これらのメトリクスを Datadog ダッシュボードに表示するようにTiDB Cloudを構成できます。

詳細な統合手順と Datadog が追跡するメトリクスのリストについては、 [TiDB Cloudと Datadog を統合する](/tidb-cloud/monitor-datadog-integration.md)を参照してください。

### プロメテウスとグラファナの統合 {#prometheus-and-grafana-integration}

Prometheus と Grafana の統合により、 TiDB Cloudから Prometheus のscrape_config ファイルを取得し、そのファイルの内容を使用して Prometheus を構成できます。これらのメトリクスは、Grafana ダッシュボードで表示できます。

詳細な統合手順と Prometheus が追跡するメトリクスのリストについては、 [TiDB CloudをPrometheus および Grafana と統合する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)を参照してください。
