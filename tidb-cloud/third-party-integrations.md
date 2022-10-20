---
title: Third-party Integrations
summary: Learn how to use third-party integrations.
---

# Third-Party Integrations

## Required access

To edit third-party integration settings, you must have the `Organization Owner` access to your organization or `Project Member` access to the target project.

## View or modify third-party integrations

1. On the TiDB Cloud console, choose a target project that you want to view or modify, and then click the **Project Settings** tab.
2. In the left pane, click **Integrations**. The available third-party integrations are displayed.

## Available integrations

### Datadog integration

Configures TiDB Cloud to send metric data about your TiDB clusters to [Datadog](https://www.datadoghq.com/). You can view these metrics in your Datadog dashboards. To get a detailed list of all metrics that Datadog tracks, refer to [Datadog Integration](/tidb-cloud/monitor-datadog-integration.md).

### Prometheus and Grafana integration

Get a scrape_config file for Prometheus from TiDB Cloud and use the content from the file to configure Prometheus. You can view these metrics in your Grafana dashboards. To get a detailed list of all metrics that Prometheus tracks, refer to [Prometheus and Grafana Integration](/tidb-cloud/monitor-prometheus-and-grafana-integration.md).
