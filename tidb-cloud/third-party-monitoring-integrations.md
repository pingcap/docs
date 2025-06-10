---
title: Third-Party Metrics Integrations（Beta）
summary: Learn how to use third-party metrics integrations.
---

# Third-Party Metrics Integrations（Beta）

You can integrate TiDB Cloud with third-party metrics services to receive TiDB Cloud alerts and view the performance metrics of your TiDB cluster using the metrics services. The third-party metrics integrations are currently in beta.

## Required access

To edit third-party integration settings, you must be in the `Organization Owner` role of your organization or the `Project Owner` role of the target project.

## View or modify third-party integrations

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Project Settings** > **Integrations**.

The available third-party integrations are displayed.

## Limitation

- For [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters, third-party metrics integrations are not supported.

- Third-party metrics integrations are not available when the cluster status is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**.

## Available integrations

### Datadog integration (beta)

With the Datadog integration, you can configure TiDB Cloud to send metric data about your TiDB clusters to [Datadog](https://www.datadoghq.com/) and view these metrics in your Datadog dashboards.

For the detailed integration steps and a list of metrics that Datadog tracks, refer to [Integrate TiDB Cloud with Datadog](/tidb-cloud/monitor-datadog-integration.md).

### Prometheus and Grafana integration (beta)

With the Prometheus and Grafana integration, you can get a `scrape_config` file for Prometheus from TiDB Cloud and use the content from the file to configure Prometheus. You can view these metrics in your Grafana dashboards.

For the detailed integration steps and a list of metrics that Prometheus tracks, see [Integrate TiDB Cloud with Prometheus and Grafana](/tidb-cloud/monitor-prometheus-and-grafana-integration.md).

### New Relic integration (beta)

With the New Relic integration, you can configure TiDB Cloud to send metric data about your TiDB clusters to [New Relic](https://newrelic.com/) and view these metrics in your New Relic dashboards.

For the detailed integration steps and a list of metrics that New Relic tracks, see [Integrate TiDB Cloud with New Relic](/tidb-cloud/monitor-new-relic-integration.md).
