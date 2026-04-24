---
title: Monitoring
summary: Learn about monitoring concepts for TiDB Cloud.
---

# Monitoring

Monitoring in TiDB Cloud provides tools and integrations that enable you to oversee TiDB performance, track activity, and respond to issues in a timely manner.

## Built-in metrics

Built-in metrics refer to a full set of standard metrics that TiDB Cloud collects and presents on the **Metrics** page at the <CustomContent plan="starter,essential,premium">instance</CustomContent><CustomContent plan="dedicated">cluster</CustomContent> level. With these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

<CustomContent plan="starter,essential,dedicated">

For more information, see [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md).

</CustomContent>
<CustomContent plan="premium">

For more information, see [{{{ .premium }}} Built-in Metrics](/tidb-cloud/premium/built-in-monitoring-premium.md).

</CustomContent>

## Built-in alerting

Built-in alerting refers to the alerting mechanism that TiDB Cloud provides to assist you in monitoring your {{{ .essential }}} instances and TiDB Cloud Dedicated clusters. Currently, TiDB Cloud provides the following three types of alerts:

- Resource usage alerts

- Data migration alerts

- Changefeed alerts

On the Alerts page of the TiDB Cloud console, you can view alerts of your {{{ .essential }}} instance or TiDB Cloud Dedicated cluster, edit alert rules, and subscribe to alert notification emails.

For more information, see [TiDB Cloud Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md).

## Events

In TiDB Cloud, an event indicates a change in your TiDB Cloud resource.

- For {{{ .starter }}} and Essential instances, TiDB Cloud logs the historical events at the instance level.
- For TiDB Cloud Dedicated clusters, TiDB Cloud logs the historical events at the cluster level.

You can view the logged events on the **Events** page, including the event type, status, message, trigger time, and trigger user.

For more information, see [Events](/tidb-cloud/tidb-cloud-events.md).

## Third-party metrics integrations

TiDB Cloud lets you integrate any of the following third-party metrics services to receive TiDB Cloud alerts and view the performance metrics of your TiDB Cloud Dedicated cluster.

- [Datadog integration](/tidb-cloud/monitor-datadog-integration.md)

- [Prometheus and Grafana integration](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)

- [New Relic integration](/tidb-cloud/monitor-new-relic-integration.md)
