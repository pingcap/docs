---
title: 迁移 Prometheus 集成
summary: 了解如何从旧版项目级 Prometheus 集成迁移到新的集群级 Prometheus 集成。
---

# 迁移 Prometheus 集成

TiDB Cloud 现在在集群级别管理 [Prometheus 集成](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)，提供了更细粒度的控制和配置。旧版项目级 Prometheus 集成（Beta）将于 2026 年 1 月 6 日弃用。如果你的组织仍在使用这些旧版集成，请按照本指南将其迁移到新的集群级 Prometheus 集成，以最大程度减少对指标相关服务的影响。

## 前提条件

- 要为 TiDB Cloud 设置第三方指标集成，你必须拥有 TiDB Cloud 中的 `Organization Owner` 或 `Project Owner` 访问权限。

## 迁移步骤

请按照以下步骤迁移 Prometheus 集成。

### 步骤 1. 删除旧版项目级 Prometheus 集成（Beta）

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，使用左上角的下拉框切换到目标项目。

2. 在左侧导航栏，点击 **Project Settings** > **Integrations**。

3. 在 **Integrations** > **Integration to Prometheus (BETA)** 模块中，选择 **Scrape_config Files** 并点击 **Delete**。

4. 在弹出的对话框中，输入 `Delete` 以确认移除旧版集成。

### 步骤 2. 为每个集群创建新的集群级 Prometheus 集成

请为项目中的每个 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群重复以下步骤。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。

2. 在左侧导航栏，点击 **Settings** > **Integrations**。

3. 在 **Integrations** 页面，创建新的 Prometheus 集成。更多信息请参见 [将 TiDB Cloud 集成到 Prometheus 和 Grafana](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)。

## 删除项目级 Prometheus 集成（Beta）的影响

删除项目级 Prometheus 集成（Beta）后，项目下所有集群将立即停止向 Prometheus 端点暴露指标。这将导致下游数据的临时丢失，并中断与集成相关的服务（如监控和告警），直到你配置新的集群级 Prometheus 集成为止。

## 联系支持

如需帮助，请联系 TiDB Cloud 支持：<a href="mailto:support@pingcap.com">support@pingcap.com</a>，或联系你的技术客户经理（TAM）。