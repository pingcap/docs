---
title: Monitoring
summary: 了解 TiDB Cloud 的监控概念。
---

# Monitoring

TiDB Cloud 的监控为你提供了工具和集成，能够监督集群性能、跟踪活动，并及时响应问题。

## 内置指标

内置指标是指 TiDB Cloud 收集并在 **Metrics** 页面展示的集群全套标准指标。通过这些指标，你可以轻松识别性能问题，并判断当前的数据库部署是否满足你的需求。

更多信息，参见 [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md)。

## 内置告警

内置告警是指 TiDB Cloud 提供的集群告警机制，帮助你监控集群。目前，TiDB Cloud 提供以下三类告警：

- 资源使用告警

- 数据迁移告警

- Changefeed 告警

在 TiDB Cloud 控制台的 Alerts 页面，你可以查看集群的告警、编辑告警规则，并订阅告警通知邮件。

更多信息，参见 [TiDB Cloud Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md)。

## 集群事件

在 TiDB Cloud 中，事件表示你的 TiDB Cloud 集群发生的变更。TiDB Cloud 会在集群级别记录历史事件，帮助你跟踪集群活动。你可以在 **Events** 页面查看已记录的事件，包括事件类型、状态、消息、触发时间和触发用户。

更多信息，参见 [TiDB Cloud Cluster Event](/tidb-cloud/tidb-cloud-events.md)。

## 第三方指标集成

TiDB Cloud 允许你集成以下任意第三方指标服务，以接收 TiDB Cloud 告警并查看 TiDB 集群的性能指标。

- [Datadog 集成（预览版）](/tidb-cloud/monitor-datadog-integration.md)

- [Prometheus 和 Grafana 集成（Beta）](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)

- [New Relic 集成（预览版）](/tidb-cloud/monitor-new-relic-integration.md)