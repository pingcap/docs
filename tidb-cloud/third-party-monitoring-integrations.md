---
title: Third-Party Metrics Integrations（Beta）
summary: サードパーティのメトリクス統合の使用方法を学習します。
---

# サードパーティメトリクス統合（ベータ版） {#third-party-metrics-integrations-beta}

TiDB Cloudをサードパーティのメトリクスサービスと統合することで、 TiDB Cloudのアラートを受信し、メトリクスサービスを使用してTiDBクラスタのパフォーマンスメトリクスを表示できます。サードパーティのメトリクス統合は現在ベータ版です。

## 必要なアクセス {#required-access}

サードパーティ統合設定を編集するには、組織の`Organization Owner`のロールまたは対象プロジェクトの`Project Owner`ロールを持っている必要があります。

## サードパーティの統合をビューまたは変更する {#view-or-modify-third-party-integrations}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。
2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[統合]**をクリックします。

利用可能なサードパーティ統合が表示されます。

## 制限 {#limitation}

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの場合、サードパーティのメトリック統合はサポートされていません。

-   クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAUSED** 、または**RESUMING**の場合、サードパーティのメトリクス統合は使用できません。

## 利用可能な統合 {#available-integrations}

### Datadog 統合（ベータ版） {#datadog-integration-beta}

Datadog 統合を使用すると、 TiDB Cloudを構成して、TiDB クラスターに関するメトリック データを[データドッグ](https://www.datadoghq.com/)に送信し、これらのメトリックを Datadog ダッシュボードで表示できます。

詳細な統合手順と Datadog が追跡するメトリクスのリストについては、 [TiDB CloudとDatadogの統合](/tidb-cloud/monitor-datadog-integration.md)を参照してください。

### Prometheus と Grafana の統合 (ベータ版) {#prometheus-and-grafana-integration-beta}

PrometheusとGrafanaの統合により、 TiDB CloudからPrometheus用の`scrape_config`ファイルを取得し、そのファイルの内容を使用してPrometheusを設定できます。これらのメトリクスはGrafanaダッシュボードで確認できます。

詳細な統合手順と Prometheus が追跡するメトリックのリストについては、 [TiDB Cloud をPrometheus および Grafana と統合する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)参照してください。

### New Relic 統合（ベータ版） {#new-relic-integration-beta}

New Relic 統合を使用すると、 TiDB Cloudを構成して、TiDB クラスターに関するメトリック データを[ニューレリック](https://newrelic.com/)に送信し、これらのメトリックを New Relic ダッシュボードで表示できます。

詳細な統合手順と New Relic が追跡するメトリックのリストについては、 [TiDB CloudとNew Relicの統合](/tidb-cloud/monitor-new-relic-integration.md)参照してください。
