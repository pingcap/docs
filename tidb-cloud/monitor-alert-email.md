---
title: 通过 Email 订阅
summary: 了解如何通过 Email 获取报警通知，从而监控你的 TiDB 集群。
---

# 通过 Email 订阅

TiDB Cloud 为你提供了通过 email、[Slack](/tidb-cloud/monitor-alert-slack.md)、[Zoom](/tidb-cloud/monitor-alert-zoom.md)、[Flashduty](/tidb-cloud/monitor-alert-flashduty.md) 和 [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md) 订阅报警通知的便捷方式。本文档介绍如何通过 email 订阅报警通知。

> **注意：**
>
> 目前，报警订阅仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件

- 要订阅 TiDB Cloud 的报警通知，你必须拥有组织的 `Organization Owner` 访问权限，或 TiDB Cloud 目标项目的 `Project Owner` 访问权限。

## 订阅报警通知

> **提示：**
>
> 报警订阅针对当前项目下的所有报警。如果你在项目中有多个集群，只需订阅一次即可。

要获取你项目中集群的报警通知，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，点击右上角的 **Add Subscriber**。
4. 在 **Subscriber Type** 下拉列表中选择 **Email**。
5. 输入你的 email 地址。
6. 点击 **Test Connection**。

    - 如果测试成功，会显示 **Save** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示排查问题后重试连接。

7. 点击 **Save** 完成订阅。

另外，你也可以在集群的 [**Alert**](/tidb-cloud/monitor-built-in-alerting.md#view-alerts) 页面右上角点击 **Subscribe**，会跳转到 **Alert Subscriber** 页面。

如果报警条件持续未变，报警会每三小时发送一次 email 通知。

## 取消订阅报警通知

如果你不再希望接收项目中集群的报警通知，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，找到你要删除的目标订阅者所在行，然后点击 **...** > **Unsubscribe**。
4. 点击 **Unsubscribe** 确认取消订阅。