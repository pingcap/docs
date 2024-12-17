---
title: Monitoring
summary: Learn about monitoring concepts for TiDB Cloud.
---

# Monitoring

Monitoring in TiDB Cloud provides tools and integrations that enable you to oversee cluster performance, track activity, and respond to issues in a timely manner.

## Built-in metrics

Built-in Metrics refer to a full set of standard metrics of your cluster that TiDB Cloud collects and presents on the Metrics page. With these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

For more information, see [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md).

## Built-in alerting

Built-in alerting refers to the cluster alerting mechanism that TiDB Cloud provides to assist you in monitoring your cluster. Currently, TiDB Cloud provides the following three types of alerts:

- Resource usage alerts

- Data migration alerts

- Changefeed alerts

On the Alerts page of the TiDB Cloud console, you can view alerts of your cluster, edit alert rules, and subscribe to alert notification emails.

For more information, see [TiDB Cloud Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md).

## Cluster events

In TiDB Cloud, an *event* indicates a change in your TiDB Cloud cluster. TiDB Cloud logs the historical events at the cluster level to help you track cluster activities. You can view the logged events on the **Events** page, including the event type, status, message, trigger time, and trigger user.

For more information, see [TiDB Cloud Cluster Event](/tidb-cloud/tidb-cloud-events.md).

## Third-party metrics integrations (Beta)

TiDB Cloud lets you integrate any of the following third-party metrics services to receive TiDB Cloud alerts and view the performance metrics of your TiDB cluster.

- Datadog integration

- Prometheus and Grafana integration

- New Relic integration

Currently, these third-party metrics integrations are in beta.
For more information, see [Third-Party Metrics Integration (Beta)](/tidb-cloud/third-party-monitoring-integrations.md).