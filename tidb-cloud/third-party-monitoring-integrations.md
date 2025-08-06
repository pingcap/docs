---
title: Third-Party Metrics Integrations
summary: Learn how to use third-party metrics integrations.
---

# Third-Party Metrics Integrations

You can integrate TiDB Cloud with the following third-party metrics services to receive TiDB Cloud alerts and view the performance metrics of your TiDB cluster in these services:

- [Datadog integration (Preview)](#datadog-integration-preview)
- [Prometheus and Grafana integration (Beta)](#prometheus-and-grafana-integration-beta)
- [New Relic integration (Preview)](#new-relic-integration-preview)

## Datadog integration (Preview)

With the Datadog integration, you can configure TiDB Cloud to send metric data about your TiDB clusters to [Datadog](https://www.datadoghq.com/) and view these metrics in your Datadog dashboards.

For the detailed integration steps and a list of metrics that Datadog tracks, refer to [Integrate TiDB Cloud with Datadog](/tidb-cloud/monitor-datadog-integration.md).

## Prometheus and Grafana integration (Beta)

With the Prometheus and Grafana integration, you can get a `scrape_config` file for Prometheus from TiDB Cloud and use the content from the file to configure Prometheus. You can view these metrics in your Grafana dashboards.

For the detailed integration steps and a list of metrics that Prometheus tracks, see [Integrate TiDB Cloud with Prometheus and Grafana](/tidb-cloud/monitor-prometheus-and-grafana-integration.md).

## New Relic integration (Preview)

With the New Relic integration, you can configure TiDB Cloud to send metric data about your TiDB clusters to [New Relic](https://newrelic.com/) and view these metrics in your New Relic dashboards.

For the detailed integration steps and a list of metrics that New Relic tracks, see [Integrate TiDB Cloud with New Relic](/tidb-cloud/monitor-new-relic-integration.md).
