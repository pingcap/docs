---
title: 通过 PagerDuty 订阅
summary: 了解如何通过 PagerDuty 获取报警通知，从而监控 TiDB。
---

# 通过 PagerDuty 订阅

TiDB Cloud 为你提供了通过 PagerDuty、[Slack](/tidb-cloud/monitor-alert-slack.md)、[email](/tidb-cloud/monitor-alert-email.md)、[Zoom](/tidb-cloud/monitor-alert-zoom.md) 和 [Flashduty](/tidb-cloud/monitor-alert-flashduty.md) 订阅报警通知的便捷方式。本文档介绍如何通过 PagerDuty 订阅报警通知。

> **注意：**
>
> 目前，报警订阅功能适用于 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 实例和 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件

- 通过 PagerDuty 订阅功能仅对订阅了 **Enterprise** 或 **Premium** [支持计划](/tidb-cloud/connected-care-overview.md) 的组织开放。

- 要订阅 TiDB Cloud 的报警通知，你必须拥有组织的 `Organization Owner` 访问权限，或在 TiDB Cloud 中目标项目的 `Project Owner` 访问权限。

## 订阅报警通知

要接收报警通知，请按照以下步骤操作：

### 步骤 1. 生成 PagerDuty 集成密钥

1. 按照 [PagerDuty Events API v2 Overview](https://developer.pagerduty.com/docs/events-api-v2-overview#getting-started) 中的说明，生成 **Events API v2** 类型的集成密钥。
2. 保存生成的集成密钥，以便在下一步中使用。

### 步骤 2. 从 TiDB Cloud 进行订阅

报警通知订阅方式根据[你的 TiDB Cloud 方案](/tidb-cloud/select-cluster-tier.md)有所不同。

<CustomContent plan="dedicated">

> **提示：**
>
> 对于 {{{ .dedicated }}}，报警订阅针对当前项目下的所有报警。如果你在该项目下有多个 {{{ .dedicated }}} 集群，只需订阅一次即可。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，前往你组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击 **Project view** 标签页。
2. 在项目视图中，找到目标项目，然后点击该项目的 <MDSvgIcon name="icon-project-settings" />。
3. 在左侧导航栏，点击 **Project Settings** 下的 **Alert Subscription**。
4. 在 **Alert Subscription** 页面，点击右上角的 **Add Subscriber**。
5. 在 **Subscriber Type** 下拉列表中选择 **PagerDuty**。
6. 在 **Name** 字段输入名称，在 **Integration Key** 字段输入你的 PagerDuty 集成密钥。
7. 点击 **Test Connection**。

    - 如果测试成功，会显示 **Save** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示排查问题并重试连接。

8. 点击 **Save** 完成订阅。

另外，你也可以在 {{{ .dedicated }}} 集群的 **Alert** 页面右上角点击 **Subscribe**，系统会跳转到 **Alert Subscription** 页面。

</CustomContent>

<CustomContent plan="essential">

> **提示：**
>
> 对于 {{{ .essential }}}，报警订阅针对当前实例下的所有报警。如果你有多个实例，需要分别为每个实例单独订阅。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，前往你组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .essential }}} 实例的名称以进入其概览页面。
2. 在左侧导航栏，点击 **Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，点击右上角的 **Add Subscriber**。
4. 在 **Subscriber Type** 下拉列表中选择 **PagerDuty**。
5. 在 **Name** 字段输入名称，在 **Integration Key** 字段输入你的 PagerDuty 集成密钥。
6. 点击 **Test Connection**。

    - 如果测试成功，会显示 **Save** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示排查问题并重试连接。

7. 点击 **Save** 完成订阅。

另外，你也可以在 {{{ .essential }}} 实例的 **Alert** 页面右上角点击 **Subscribe**，系统会跳转到 **Alert Subscription** 页面。

</CustomContent>

如果报警条件持续未变，报警会每隔三小时发送一次通知。

## 取消订阅报警通知

如果你不再希望接收报警通知，请按照以下步骤操作。具体步骤根据[你的 TiDB Cloud 方案](/tidb-cloud/select-cluster-tier.md)有所不同。

<CustomContent plan="dedicated">
    
1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，前往你组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击 **Project view** 标签页。
2. 在项目视图中，找到目标项目，然后点击该项目的 <MDSvgIcon name="icon-project-settings" />。
3. 在左侧导航栏，点击 **Project Settings** 下的 **Alert Subscription**。
4. 在 **Alert Subscription** 页面，找到要删除的目标订阅者所在行，然后点击 **...** > **Unsubscribe**。
5. 点击 **Unsubscribe** 以确认取消订阅。

</CustomContent>

<CustomContent plan="essential">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，前往你组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .essential }}} 实例的名称以进入其概览页面。
2. 在左侧导航栏，点击 **Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，找到要删除的目标订阅者所在行，然后点击 **...** > **Unsubscribe**。
4. 点击 **Unsubscribe** 以确认取消订阅。

</CustomContent>
