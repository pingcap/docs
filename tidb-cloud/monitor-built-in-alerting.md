---
title: TiDB Cloud 内置告警
summary: 了解如何通过 TiDB Cloud 获取告警通知来监控你的 TiDB 集群。
---

# TiDB Cloud 内置告警

TiDB Cloud 为你提供了便捷的方式来查看告警、编辑告警规则，以及订阅告警通知。

本文档介绍了如何进行这些操作，并为你提供了 TiDB Cloud 内置告警条件以供参考。

> **注意：**
>
> 目前，告警订阅仅适用于 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 和 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 查看告警

在 TiDB Cloud 中，你可以在 **Alerts** 页面查看活跃和已关闭的告警。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，导航到你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群的名称，进入集群概览页面。
3. 在左侧导航栏点击 **Alerts**。
4. **Alerts** 页面默认显示活跃告警。你可以查看每个活跃告警的信息，如告警名称、触发时间和持续时间。
5. 如果你还想查看已关闭的告警，只需点击 **Status** 下拉列表并选择 **Closed** 或 **All**。

## 编辑告警规则

在 TiDB Cloud 中，你可以通过禁用或启用告警，或修改告警阈值来编辑告警规则。

1. 在 **Alerts** 页面，点击 **Edit Rules**。
2. 根据需要禁用或启用告警规则。
3. 点击 **Edit** 以修改告警规则的阈值。

    > **提示：**
    >
    > 目前，TiDB Cloud 提供的告警规则编辑能力有限。部分告警规则不支持编辑。如果你希望配置不同的触发条件或频率，或让告警自动触发下游服务（如 [PagerDuty](https://www.pagerduty.com/docs/guides/datadog-integration-guide/)）的操作，建议使用 [第三方监控与告警集成](/tidb-cloud/third-party-monitoring-integrations.md)。

## 订阅告警通知

在 TiDB Cloud 中，你可以通过以下方式之一订阅告警通知：

- [Email](/tidb-cloud/monitor-alert-email.md)
- [Slack](/tidb-cloud/monitor-alert-slack.md)
- [Zoom](/tidb-cloud/monitor-alert-zoom.md)
- [Flashduty](/tidb-cloud/monitor-alert-flashduty.md)
- [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md)

## TiDB Cloud 内置告警条件

下表提供了 TiDB Cloud 内置告警条件及对应的推荐操作。

> **注意：**
>
> - 这些告警条件并不一定意味着存在问题，但通常是潜在问题的早期预警信号。因此，建议采取推荐的操作。
> - 你可以在 TiDB Cloud 控制台编辑告警的阈值。
> - 部分告警规则默认处于禁用状态。你可以根据需要启用它们。

TiDB Cloud 会根据不同集群方案，结合该方案的功能，提供不同的告警规则。

<CustomContent plan="dedicated">

### 资源使用告警

| 条件 | 推荐操作 |
|:--- |:--- |
| 整个集群 TiDB 节点内存利用率超过 70% 持续 10 分钟 | 考虑增加 TiDB 节点数量或节点规格，以降低当前负载下的内存使用百分比。|
| 整个集群 TiKV 节点内存利用率超过 70% 持续 10 分钟 | 考虑增加 TiKV 节点数量或节点规格，以降低当前负载下的内存使用百分比。|
| 整个集群 TiFlash 节点内存利用率超过 70% 持续 10 分钟 | 考虑增加 TiFlash 节点数量或节点规格，以降低当前负载下的内存使用百分比。|
| TiDB 节点 CPU 利用率超过 80% 持续 10 分钟 | 考虑增加 TiDB 节点数量或节点规格，以降低当前负载下的 CPU 使用百分比。|
| TiKV 节点 CPU 利用率超过 80% 持续 10 分钟 | 考虑增加 TiKV 节点数量或节点规格，以降低当前负载下的 CPU 使用百分比。|
| TiFlash 节点 CPU 利用率超过 80% 持续 10 分钟 | 考虑增加 TiFlash 节点数量或节点规格，以降低当前负载下的 CPU 使用百分比。|
| TiKV 存储利用率超过 80% | 考虑增加 TiKV 节点数量或节点存储容量，以提升你的存储能力。|
| TiFlash 存储利用率超过 80% | 考虑增加 TiFlash 节点数量或节点存储容量，以提升你的存储能力。|
| TiDB 节点最大内存利用率超过 70% 持续 10 分钟 | 建议检查集群中是否存在 [热点](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues) 问题，或增加 TiDB 节点数量或节点规格，以降低当前负载下的内存使用百分比。|
| TiKV 节点最大内存利用率超过 70% 持续 10 分钟 | 建议检查集群中是否存在 [热点](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues) 问题，或增加 TiKV 节点数量或节点规格，以降低当前负载下的内存使用百分比。|
| TiDB 节点最大 CPU 利用率超过 80% 持续 10 分钟 | 建议检查集群中是否存在 [热点](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues) 问题，或增加 TiDB 节点数量或节点规格，以降低当前负载下的 CPU 使用百分比。|
| TiKV 节点最大 CPU 利用率超过 80% 持续 10 分钟 | 建议检查集群中是否存在 [热点](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues) 问题，或增加 TiKV 节点数量或节点规格，以降低当前负载下的 CPU 使用百分比。|

### 数据迁移告警

| 条件 | 推荐操作 |
|:--- |:--- |
| 数据迁移任务在数据导出过程中遇到错误 | 检查错误信息，并参考 [数据迁移故障排查](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) 获取帮助。|
| 数据迁移任务在数据导入过程中遇到错误 | 检查错误信息，并参考 [数据迁移故障排查](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) 获取帮助。|
| 数据迁移任务在增量迁移过程中遇到错误 | 检查错误信息，并参考 [数据迁移故障排查](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) 获取帮助。|
| 数据迁移任务在增量迁移过程中已暂停超过 6 小时 | 数据迁移任务在数据增量迁移过程中已暂停超过 6 小时。上游数据库中的 binlog 可能已被清理（取决于你的数据库 binlog 清理策略），这可能导致增量迁移失败。请参考 [数据迁移故障排查](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) 获取帮助。|
| 同步延迟大于 10 分钟且持续增长超过 20 分钟 | 请参考 [数据迁移故障排查](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) 获取帮助。|

### TiDB Cloud Dedicated 的 Changefeed 告警

| 条件                                   | 推荐操作                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|:----------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changefeed 延时超过 600 秒 | 在 TiDB Cloud 控制台的 **Changefeed** 页面和 **Changefeed Detail** 页面检查 changefeed 状态，你可以在这些页面找到一些错误信息以帮助诊断问题。<br/>可能触发该告警的原因包括：<ul><li>上游整体流量增加，导致现有 changefeed 规格无法承载。如果流量增加是暂时的，changefeed 延时会在流量恢复正常后自动恢复。如果流量持续增加，则需要扩展 changefeed。</li><li>下游或网络异常，此时请先排查并解决异常。</li><li>如果下游为 RDS，表缺少索引，可能导致写入性能低、延时高。此时需要在上游或下游添加必要的索引。</li></ul>如果你无法自行解决问题，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 获取进一步协助。|
| changefeed 状态为 `FAILED`                 | 在 TiDB Cloud 控制台的 **Changefeed** 页面和 **Changefeed Detail** 页面检查 changefeed 状态，你可以在这些页面找到一些错误信息以帮助诊断问题。<br/>如果你无法自行解决问题，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 获取进一步协助。|
| changefeed 状态为 `WARNING`              | 在 TiDB Cloud 控制台的 **Changefeed** 页面和 **Changefeed Detail** 页面检查 changefeed 状态，你可以在这些页面找到一些错误信息以帮助诊断问题。<br/>如果你无法自行解决问题，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 获取进一步协助。|

</CustomContent>

<CustomContent plan="essential">

### 性能总览告警

| 条件 | 推荐操作 |
|:--- |:--- |
| 每秒请求单位（RU/s）超过最大 RCU 的 80% | <ol><li>查看 RU 指标，判断增长是逐步的还是突发的。</li><li>如果是逐步增长，检查查询耗时是否增加。如果是，则当前最大 RCU 可能不足。</li><li>通过在 TiDB Cloud 控制台手动增加最大 RCU 来扩展容量。</li></ol><br/>如果你无法解决问题，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。|
| QPS 下降 80% | <ol><li>检查下降是否由查询延时增加导致。</li><li>确认你的应用是否正常运行。如果下降是有意为之，可忽略该告警。如果下降非预期且无法定位根因，请立即联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。</li></ol>|
| 查询 P99 延时超过 200 ms | <ol><li>排查慢查询：进入 Slow Query 页面，按最近时间范围筛选，定位新出现或运行变慢的查询。</li><li>回顾近期变更，如应用部署、表结构变更或数据导入任务，这些可能影响流量模式。</li></ol><br/>如果无法定位根因，请立即联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。|
| 查询 P95 延时超过 200 ms | <ol><li>排查慢查询：进入 Slow Query 页面，按最近时间范围筛选，定位新出现或运行变慢的查询。</li><li>回顾近期变更，如应用部署、表结构变更或数据导入任务，这些可能影响流量模式。</li></ol><br/>如果无法定位根因，请立即联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。|
| 请求错误率超过 10%  | 检查集群的近期错误和整体语句执行情况。|

### TiDB Cloud Essential 的 Changefeed 告警

| 条件                                   | 推荐操作                   |
|:----------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changefeed 延时超过 600 秒 | 在 TiDB Cloud 控制台的 **Changefeed** 页面和 **Changefeed Detail** 页面检查 changefeed 状态，你可以在这些页面找到一些错误信息以帮助诊断问题。<br/>可能触发该告警的原因包括：<ul><li>上游整体流量增加，导致现有 changefeed 规格无法承载。如果流量增加是暂时的，changefeed 延时会在流量恢复正常后自动恢复。如果流量持续增加，则需要扩展 changefeed。</li><li>下游或网络异常，此时请先排查并解决异常。</li><li>如果下游为 RDS，表缺少索引，可能导致写入性能低、延时高。此时需要在上游或下游添加必要的索引。</li></ul>如果你无法自行解决问题，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 获取进一步协助。|
| changefeed 状态为 `FAILED`                 | 在 TiDB Cloud 控制台的 **Changefeed** 页面和 **Changefeed Detail** 页面检查 changefeed 状态，你可以在这些页面找到一些错误信息以帮助诊断问题。<br/>如果你无法自行解决问题，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 获取进一步协助。|
| changefeed 状态为 `WARNING`              | 在 TiDB Cloud 控制台的 **Changefeed** 页面和 **Changefeed Detail** 页面检查 changefeed 状态，你可以在这些页面找到一些错误信息以帮助诊断问题。<br/>如果你无法自行解决问题，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 获取进一步协助。|

</CustomContent>