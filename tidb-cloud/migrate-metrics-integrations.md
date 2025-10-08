---
title: 迁移 Datadog 和 New Relic 集成
summary: 了解如何将 Datadog 和 New Relic 的遗留项目级指标集成迁移到新的集群级集成。
---

# 迁移 Datadog 和 New Relic 集成

TiDB Cloud 现在在集群级别管理 Datadog 和 New Relic 集成，提供了更细粒度的控制和配置。遗留的项目级 Datadog 和 New Relic 集成将于 2025 年 10 月 31 日弃用。如果你的组织仍在使用这些遗留集成，请按照本指南迁移到新的集群级集成，以最大程度减少对指标相关服务的影响。

## 前提条件

- 要为 TiDB Cloud 设置第三方指标集成，你必须拥有 TiDB Cloud 中的 `Organization Owner` 或 `Project Owner` 访问权限。

## 迁移步骤

### 第 1 步. 删除遗留的项目级 Datadog 和 New Relic 集成

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，使用左上角的下拉框切换到目标项目。

2. 在左侧导航栏，点击 **Project Settings** > **Integrations**。

3. 在 **Integrations** 页面，点击 **Integration to Datadog** 或 **Integration to New Relic** 旁边的 **Delete**。

4. 在弹出的对话框中，输入 `Delete` 以确认移除遗留集成。

### 第 2 步. 为每个集群创建新的 Datadog 或 New Relic 集成

请为项目中的每个 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群重复以下步骤。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，使用左上角的下拉框切换到目标集群。

2. 在左侧导航栏，点击 **Settings** > **Integrations**。

3. 在 **Integrations** 页面，根据需要创建新的集成。更多信息请参见 [Integrate TiDB Cloud with Datadog](/tidb-cloud/monitor-datadog-integration.md) 和 [Integrate TiDB Cloud with New Relic](/tidb-cloud/monitor-new-relic-integration.md)。

## 影响说明

删除项目级集成后，项目下所有集群将立即停止发送指标数据。这会导致下游数据的临时丢失，并中断与集成相关的服务（如监控和告警），直到你为每个集群创建新的集群级集成为止。

## 联系支持

如需帮助，请通过 <a href="mailto:support@pingcap.com">support@pingcap.com</a> 联系 TiDB Cloud 支持，或联系你的技术客户经理（TAM）。