---
title: 第三方指标集成
summary: 了解如何使用第三方指标集成。
---

# 第三方指标集成

你可以将 TiDB Cloud 集成到以下第三方指标服务中，以便在这些服务中接收 TiDB Cloud 警报并查看 TiDB 集群的性能指标：

- [Datadog 集成](#datadog-集成)
- [Prometheus 和 Grafana 集成](#prometheus-和-grafana-集成)
- [New Relic 集成](#new-relic-集成)

## Datadog 集成

通过 Datadog 集成，你可以配置 TiDB Cloud，将关于 TiDB 集群的指标数据发送到 [Datadog](https://www.datadoghq.com/)，并在你的 Datadog 仪表盘中查看这些指标。

有关详细的集成步骤以及 Datadog 跟踪的指标列表，请参考 [Integrate TiDB Cloud with Datadog](/tidb-cloud/monitor-datadog-integration.md)。

## Prometheus 和 Grafana 集成

通过 Prometheus 和 Grafana 集成，你可以从 TiDB Cloud 获取一个用于 Prometheus 的 `scrape_config` 文件，并使用该文件中的内容来配置 Prometheus。你可以在 Grafana 仪表盘中查看这些指标。

有关详细的集成步骤以及 Prometheus 跟踪的指标列表，请参见 [Integrate TiDB Cloud with Prometheus and Grafana](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)。

## New Relic 集成

通过 New Relic 集成，你可以配置 TiDB Cloud，将关于 TiDB 集群的指标数据发送到 [New Relic](https://newrelic.com/)，并在你的 New Relic 仪表盘中查看这些指标。

有关详细的集成步骤以及 New Relic 跟踪的指标列表，请参见 [Integrate TiDB Cloud with New Relic](/tidb-cloud/monitor-new-relic-integration.md)。