---
title: Third-Party Monitoring Integrations
summary: Learn how to use third-party monitoring integrations.
---

# サードパーティの監視統合 {#third-party-monitoring-integrations}

TiDB Cloudをサードパーティの監視サービスと統合して、 TiDB Cloudアラートを受信し、監視サービスを使用して TiDB クラスターのパフォーマンス メトリックを表示できます。

> **ノート：**
>
> [サーバーレス階層クラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier)については、サードパーティの監視統合はサポートされていません。

## 必要なアクセス {#required-access}

サードパーティの統合設定を編集するには、組織への`Owner`つのアクセス権またはターゲット プロジェクトへの`Member`のアクセス権が必要です。

## サードパーティの統合をビューまたは変更する {#view-or-modify-third-party-integrations}

1.  TiDB Cloudコンソールで、表示または変更するターゲット プロジェクトを選択し、[**プロジェクト設定**] タブをクリックします。
2.  左ペインで [**統合**] をクリックします。利用可能なサードパーティ統合が表示されます。

## 利用可能な統合 {#available-integrations}

### Datadog の統合 {#datadog-integration}

Datadog 統合により、TiDB クラスターに関するメトリクス データを[データドッグ](https://www.datadoghq.com/)に送信し、Datadog ダッシュボードでこれらのメトリクスを表示するようにTiDB Cloudを構成できます。

詳細な統合手順と Datadog が追跡するメトリクスのリストについては、 [TiDB Cloudと Datadog の統合](/tidb-cloud/monitor-datadog-integration.md)を参照してください。

### Prometheus と Grafana の統合 {#prometheus-and-grafana-integration}

Prometheus と Grafana の統合により、 TiDB Cloudから Prometheus の Scrape_config ファイルを取得し、そのファイルの内容を使用して Prometheus を構成できます。これらのメトリックは、Grafana ダッシュボードで表示できます。

詳細な統合手順と Prometheus が追跡するメトリクスのリストについては、 [TiDB Cloudを Prometheus および Grafana と統合する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)を参照してください。
