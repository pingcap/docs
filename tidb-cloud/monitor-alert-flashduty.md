---
title: 通过 Flashduty 订阅
summary: 了解如何通过 Flashduty 获取 TiDB 集群的报警通知。
---

# 通过 Flashduty 订阅

TiDB Cloud 为你提供了通过 Flashduty、[Slack](/tidb-cloud/monitor-alert-slack.md)、[email](/tidb-cloud/monitor-alert-email.md)、[Zoom](/tidb-cloud/monitor-alert-zoom.md) 和 [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md) 订阅报警通知的便捷方式。本文档介绍如何通过 Flashduty 订阅报警通知。

> **注意：**
>
> 目前，报警订阅仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件

- 通过 Flashduty 订阅功能仅对订阅了 **Enterprise** 或 **Premium** [支持计划](/tidb-cloud/connected-care-overview.md) 的组织开放。

- 要订阅 TiDB Cloud 的报警通知，你必须拥有组织的 `Organization Owner` 访问权限，或在 TiDB Cloud 中拥有目标项目的 `Project Owner` 访问权限。

## 订阅报警通知

要接收你项目中集群的报警通知，请按照以下步骤操作：

### 步骤 1. 生成 Flashduty webhook URL

1. 按照 [Flashduty Prometheus Integration](https://docs.flashcat.cloud/en/flashduty/prometheus-integration-guide) 中的说明生成 webhook URL。
2. 保存生成的 webhook URL，以便在下一步中使用。

### 步骤 2. 从 TiDB Cloud 进行订阅

> **提示：**
>
> 报警订阅针对当前项目下的所有报警。如果你在项目中有多个集群，只需订阅一次即可。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，点击右上角的 **Add Subscriber**。
4. 在 **Subscriber Type** 下拉列表中选择 **Flashduty**。
5. 在 **Name** 字段输入名称，在 **Webhook URL** 字段输入你的 Flashduty webhook URL。
6. 点击 **Test Connection**。

    - 如果测试成功，会显示 **Save** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示排查问题并重试连接。

7. 点击 **Save** 完成订阅。

另外，你也可以在集群的 **Alert** 页面右上角点击 **Subscribe**，系统会跳转到 **Alert Subscriber** 页面。

如果报警条件持续未变，报警会每三小时发送一次通知。

## 取消订阅报警通知

如果你不再希望接收项目中集群的报警通知，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，找到你要删除的目标订阅者所在行，然后点击 **...** > **Unsubscribe**。
4. 点击 **Unsubscribe** 确认取消订阅。