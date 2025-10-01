---
title: Third-Party Metrics Integrations
summary: サードパーティのメトリクス統合の使用方法を学習します。
---

# サードパーティのメトリクス統合 {#third-party-metrics-integrations}

TiDB Cloud を次のサードパーティ メトリック サービスと統合して、 TiDB Cloudアラートを受信し、これらのサービスで TiDB クラスターのパフォーマンス メトリックを表示できます。

-   [Datadog統合](#datadog-integration)
-   [Prometheus と Grafana の統合 (ベータ版)](#prometheus-and-grafana-integration-beta)
-   [New Relicとの統合](#new-relic-integration)

## Datadog統合 {#datadog-integration}

Datadog 統合を使用すると、TiDB クラスターに関するメトリック データを[データドッグ](https://www.datadoghq.com/)に送信するようにTiDB Cloudを構成し、これらのメトリックを Datadog ダッシュボードで表示できます。

詳細な統合手順と Datadog が追跡するメトリクスのリストについては、 [TiDB CloudとDatadogの統合](/tidb-cloud/monitor-datadog-integration.md)を参照してください。

## Prometheus と Grafana の統合 (ベータ版) {#prometheus-and-grafana-integration-beta}

PrometheusとGrafanaの統合により、 TiDB CloudからPrometheus用の`scrape_config`ファイルを取得し、そのファイルの内容を使用してPrometheusを設定できます。これらのメトリクスはGrafanaダッシュボードで確認できます。

詳細な統合手順と Prometheus が追跡するメトリックのリストについては、 [TiDB Cloud をPrometheus および Grafana と統合する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)参照してください。

## New Relicとの統合 {#new-relic-integration}

New Relic 統合を使用すると、 TiDB Cloudを構成して、TiDB クラスターに関するメトリック データを[ニューレリック](https://newrelic.com/)に送信し、これらのメトリックを New Relic ダッシュボードで表示できます。

詳細な統合手順と New Relic が追跡するメトリックのリストについては、 [TiDB CloudとNew Relicの統合](/tidb-cloud/monitor-new-relic-integration.md)参照してください。
