---
title: Monitoring
summary: 了解 TiDB Cloud 的监控概念。
---

# Monitoring

TiDB Cloud 的监控为你提供了工具和集成，能够监督 TiDB 性能、跟踪活动，并及时响应问题。

## 内置指标

内置指标是指 TiDB Cloud 收集并在 **Metrics** 页面展示的全套标准指标，展示粒度为 <CustomContent plan="starter,essential,premium">实例</CustomContent><CustomContent plan="dedicated">集群</CustomContent> 级别。通过这些指标，你可以轻松识别性能问题，并判断当前的数据库部署是否满足你的需求。

<CustomContent plan="starter,essential,dedicated">

更多信息，参见 [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md)。

</CustomContent>
<CustomContent plan="premium">

更多信息，参见 [{{{ .premium }}} Built-in Metrics](/tidb-cloud/premium/built-in-monitoring-premium.md)。

</CustomContent>

## 内置告警

内置告警是指 TiDB Cloud 提供的告警机制，帮助你监控 {{{ .essential }}} 实例和 TiDB Cloud Dedicated 集群。目前，TiDB Cloud 提供以下三类告警：

- 资源使用告警

- 数据迁移告警

- Changefeed 告警

在 TiDB Cloud 控制台的 Alerts 页面，你可以查看 {{{ .essential }}} 实例或 TiDB Cloud Dedicated 集群的告警、编辑告警规则，并订阅告警通知邮件。

更多信息，参见 [TiDB Cloud Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md)。

## Events {#events}

在 TiDB Cloud 中，事件表示 TiDB Cloud 资源的变更。

- 对于 {{{ .starter }}} 和 Essential 实例，TiDB Cloud 在实例级别记录历史事件。
- 对于 TiDB Cloud Dedicated 集群，TiDB Cloud 在集群级别记录历史事件。

你可以在 **Events** 页面查看已记录的事件，包括事件类型、状态、消息、触发时间和触发用户。

更多信息，参见 [Events](/tidb-cloud/tidb-cloud-events.md)。

## 第三方指标集成

TiDB Cloud 支持集成以下任一第三方指标服务，以接收 TiDB Cloud 告警并查看 TiDB Cloud Dedicated 集群的性能指标。

- [Datadog integration](/tidb-cloud/monitor-datadog-integration.md)

- [Prometheus and Grafana integration](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)

- [New Relic integration](/tidb-cloud/monitor-new-relic-integration.md)
