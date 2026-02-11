---
title: 通过 Slack 订阅
summary: 了解如何通过 Slack 获取报警通知，以便监控你的 TiDB 集群。
---

# 通过 Slack 订阅

TiDB Cloud 为你提供了便捷的方式，通过 Slack、[email](/tidb-cloud/monitor-alert-email.md)、[Zoom](/tidb-cloud/monitor-alert-zoom.md)、[Flashduty](/tidb-cloud/monitor-alert-flashduty.md) 和 [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md) 订阅报警通知。本文档介绍如何通过 Slack 订阅报警通知。

> **注意：**
>
> 目前，报警订阅功能适用于 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 和 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件

- 通过 Slack 订阅功能仅对订阅了 **Enterprise** 或 **Premium** 支持计划的组织开放。

- 要订阅 TiDB Cloud 的报警通知，你必须拥有组织的 `Organization Owner` 访问权限，或在 TiDB Cloud 中拥有目标项目的 `Project Owner` 访问权限。

## 订阅报警通知

### 第 1 步：生成 Slack webhook URL

1. 如果你还没有 Slack 应用，[创建一个 Slack 应用](https://api.slack.com/apps/new)。点击 **Create New App**，选择 **From scratch**。输入名称，选择要关联的 workspace，然后点击 **Create App**。
2. 进入你的应用设置页面。你可以通过 [应用管理控制台](https://api.slack.com/apps) 加载其设置。
3. 点击 **Incoming Webhooks** 标签页，然后将 **Activate Incoming Webhooks** 切换为 **ON**。
4. 点击 **Add New Webhook to Workspace**。
5. 选择你希望接收报警通知的频道，然后点击 **Authorize**。如果你需要将 incoming webhook 添加到私有频道，必须先进入该频道。

你可以在 **Webhook URLs for Your Workspace** 部分看到一个新条目，格式如下：`https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`。

### 第 2 步：在 TiDB Cloud 中订阅

报警通知订阅方式根据集群计划有所不同。

<CustomContent plan="dedicated">

> **提示：**
>
> 报警订阅针对当前项目下的所有报警。如果你在该项目下有多个集群，只需订阅一次即可。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，点击右上角的 **Add Subscriber**。
4. 在 **Subscriber Type** 下拉列表中选择 **Slack**。
5. 在 **Name** 字段输入名称，在 **URL** 字段输入你的 Slack webhook URL。
6. 点击 **Test Connection**。

    - 如果测试成功，会显示 **Save** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示排查问题并重试连接。

7. 点击 **Save** 完成订阅。

</CustomContent>

<CustomContent plan="essential">

> **提示：**
>
> 报警订阅针对当前集群下的所有报警。如果你有多个集群，需要分别为每个集群单独订阅。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标集群。
2. 在左侧导航栏，点击 **Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，点击右上角的 **Add Subscriber**。
4. 在 **Subscriber Type** 下拉列表中选择 **Slack**。
5. 在 **Name** 字段输入名称，在 **URL** 字段输入你的 Slack webhook URL。
6. 点击 **Test Connection**。

    - 如果测试成功，会显示 **Save** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示排查问题并重试连接。

7. 点击 **Save** 完成订阅。

</CustomContent>

另外，你也可以在集群的 **Alert** 页面右上角点击 **Subscribe**，会跳转到 **Alert Subscription** 页面。

如果报警条件持续未变，报警会每隔三小时发送一次通知。

## 取消订阅报警通知

如果你不再希望接收报警通知，请按照以下步骤操作。具体步骤根据集群计划有所不同。

<CustomContent plan="dedicated">
    
1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，找到你要删除的订阅者所在行，然后点击 **...** > **Unsubscribe**。
4. 点击 **Unsubscribe** 以确认取消订阅。

</CustomContent>

<CustomContent plan="essential">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标集群。
2. 在左侧导航栏，点击 **Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，找到你要删除的订阅者所在行，然后点击 **...** > **Unsubscribe**。
4. 点击 **Unsubscribe** 以确认取消订阅。

</CustomContent>