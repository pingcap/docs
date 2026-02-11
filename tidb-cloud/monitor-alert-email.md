---
title: 通过 Email 订阅
summary: 了解如何通过 Email 获取报警通知，从而监控你的 TiDB 集群。
---

# 通过 Email 订阅

TiDB Cloud 为你提供了通过 email、[Slack](/tidb-cloud/monitor-alert-slack.md)、[Zoom](/tidb-cloud/monitor-alert-zoom.md)、[Flashduty](/tidb-cloud/monitor-alert-flashduty.md) 和 [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md) 订阅报警通知的便捷方式。本文档介绍如何通过 email 订阅报警通知。

> **注意：**
>
> 目前，报警订阅功能适用于 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 和 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件

- 要订阅 TiDB Cloud 的报警通知，你必须拥有组织的 `Organization Owner` 访问权限，或在 TiDB Cloud 中拥有目标项目的 `Project Owner` 访问权限。

## 订阅报警通知

要接收报警通知，请按照以下步骤操作。不同集群方案的操作步骤有所不同。

<CustomContent plan="dedicated">
    
> **提示：**
>
> 报警订阅针对当前项目下的所有报警。如果你在该项目下有多个集群，只需订阅一次即可。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，点击右上角的 **Add Subscriber**。
4. 在 **Subscriber Type** 下拉列表中选择 **Email**。
5. 输入你的 email 地址。
6. 点击 **Test Connection**。

    - 如果测试成功，会显示 **Save** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示排查问题后重试连接。

7. 点击 **Save** 完成订阅。
   
</CustomContent>

<CustomContent plan="essential">

> **提示：**
>
> 报警订阅针对当前集群下的所有报警。如果你有多个集群，需要分别为每个集群单独订阅。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标集群。
2. 在左侧导航栏，点击 **Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，点击右上角的 **Add Subscriber**。
4. 在 **Subscriber Type** 下拉列表中选择 **Email**。
5. 输入你的 email 地址。
6. 点击 **Test Connection**。

    - 如果测试成功，会显示 **Save** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示排查问题后重试连接。

7. 点击 **Save** 完成订阅。
   
</CustomContent>

另外，你也可以在集群的 [**Alert**](/tidb-cloud/monitor-built-in-alerting.md#view-alerts) 页面右上角点击 **Subscribe**，会跳转到 **Alert Subscription** 页面。

如果报警条件持续未变，报警会每三小时通过 email 发送一次通知。

## 取消订阅报警通知

如果你不再希望接收报警通知，请按照以下步骤操作。不同集群方案的操作步骤有所不同。

<CustomContent plan="dedicated">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，找到你要删除的订阅者所在行，然后点击 **...** > **Unsubscribe**。
4. 点击 **Unsubscribe** 确认取消订阅。

</CustomContent>

<CustomContent plan="essential">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标集群。
2. 在左侧导航栏，点击 **Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，找到你要删除的订阅者所在行，然后点击 **...** > **Unsubscribe**。
4. 点击 **Unsubscribe** 确认取消订阅。

</CustomContent>