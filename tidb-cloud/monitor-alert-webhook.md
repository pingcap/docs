---
title: 通过 Webhook 订阅
summary: 了解如何通过通用 webhook 接收告警通知来监控你的 TiDB 集群。
---

# 通过 Webhook 订阅

TiDB Cloud 提供了一种简便方式，让你可以通过 [Generic Webhook](/tidb-cloud/monitor-alert-webhook.md)、[email](/tidb-cloud/monitor-alert-email.md)、[Slack](/tidb-cloud/monitor-alert-slack.md)、[Zoom](/tidb-cloud/monitor-alert-zoom.md)、[Flashduty](/tidb-cloud/monitor-alert-flashduty.md) 和 [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md) 订阅告警通知。本文介绍如何通过通用 webhook 订阅告警通知。

> **Note:**
>
> 当前，告警订阅适用于 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 实例、[TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium) 实例和 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件 {#prerequisites}

- 通过 webhook 订阅功能仅适用于订阅了 **Enterprise** 或 **Premium** 支持计划的组织。

- 你需要从希望接收告警通知的平台获取一个 webhook URL（例如 Telegram、Microsoft Teams，或你自己的值班系统，该系统能够接收带有 JSON payload 的 HTTP POST 请求）。当前，TiDB Cloud 不支持自定义请求头或 payload 格式。

<CustomContent plan="dedicated">

- 要订阅 TiDB Cloud 的告警通知，你必须对所在组织具有 `Organization Owner` 访问权限，或对 TiDB Cloud 中的目标项目具有 `Project Owner` 访问权限。

</CustomContent>

<CustomContent plan="essential,premium">

- 要订阅 TiDB Cloud 的告警通知，你必须对所在组织具有 `Organization Owner` 访问权限，或对 TiDB Cloud 中的目标实例具有 `Project Owner` 或 `Instance Manager` 访问权限。

</CustomContent>

## 订阅告警通知 {#subscribe-to-alert-notifications}

告警通知订阅方式因[你的 TiDB Cloud 计划](/tidb-cloud/select-cluster-tier.md)而异。

<CustomContent plan="dedicated">

要订阅 {{{ .dedicated }}} 集群的告警通知，请按以下步骤操作：

> **Tip:**
>
> 对于 {{{ .dedicated }}}，告警订阅适用于当前项目中的所有告警。如果你的项目中有多个 {{{ .dedicated }}} 集群，只需订阅一次。

1. 在 [TiDB Cloud console](https://tidbcloud.com) 中，进入你所在组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击 **Project view** 标签页。
2. 在项目视图中，找到目标项目，然后点击该项目的 <MDSvgIcon name="icon-project-settings" />。
3. 在左侧导航栏中，点击 **Project Settings** 下的 **Alert Subscription**。
4. 在 **Alert Subscription** 页面右上角，点击 **Add Subscriber**。
5. 在 **Subscriber Type** 下拉列表中选择 **Webhook**。
6. 在 **Name** 字段中输入名称，并在 **Webhook URL** 字段中输入你的 webhook URL。
7. 点击 **Save**。后端会为你测试连接并保存。

    如果测试失败，会显示错误信息。请根据提示排查问题并重试连接。

或者，你也可以在目标 {{{ .dedicated }}} 集群的 **Alert** 页面右上角点击 **Subscribe**。系统会将你引导至 **Alert Subscription** 页面。

</CustomContent>

<CustomContent plan="essential">

> **Tip:**
>
> 对于 {{{ .essential }}}，告警订阅适用于当前实例中的所有告警。如果你有多个 {{{ .essential }}} 实例，则需要分别为每个实例单独订阅。

1. 在 [TiDB Cloud console](https://tidbcloud.com) 中，进入你所在组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .essential }}} 实例的名称，进入其实例概览页面。
2. 在左侧导航栏中，点击 **Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面右上角，点击 **Add Subscriber**。
4. 在 **Subscriber Type** 下拉列表中选择 **Webhook**。
5. 在 **Name** 字段中输入名称，并在 **Webhook URL** 字段中输入你的 webhook URL。
6. 点击 **Save**。后端会为你测试连接并保存。

    如果测试失败，会显示错误信息。请根据提示排查问题并重试连接。

或者，你也可以在目标 {{{ .essential }}} 实例的 **Alert** 页面右上角点击 **Subscribe**。系统会将你引导至 **Alert Subscription** 页面。

</CustomContent>

<CustomContent plan="premium">

> **Tip:**
>
> 对于 {{{ .premium }}}，告警订阅适用于当前实例中的所有告警。如果你有多个 {{{ .premium }}} 实例，则需要分别为每个实例单独订阅。

1. 在 [TiDB Cloud console](https://tidbcloud.com) 中，进入你所在组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .premium }}} 实例的名称，进入其实例概览页面。
2. 在左侧导航栏中，点击 **Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面右上角，点击 **Add Subscriber**。
4. 在 **Subscriber Type** 下拉列表中选择 **Webhook**。
5. 在 **Name** 字段中输入名称，并在 **Webhook URL** 字段中输入你的 webhook URL。
6. 点击 **Save**。后端会为你测试连接并保存。

    如果测试失败，会显示错误信息。请根据提示排查问题并重试连接。

或者，你也可以在目标 {{{ .premium }}} 实例的 **Alert** 页面右上角点击 **Subscribe**。系统会将你引导至 **Alert Subscription** 页面。

</CustomContent>

如果告警条件保持不变，系统会每三小时发送一次告警通知。

## 取消订阅告警通知 {#unsubscribe-from-alert-notifications}

如果你不再希望接收告警通知，请按以下步骤操作。具体步骤因[你的 TiDB Cloud 计划](/tidb-cloud/select-cluster-tier.md)而异。

<CustomContent plan="dedicated">

1. 在 [TiDB Cloud console](https://tidbcloud.com) 中，进入你所在组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击 **Project view** 标签页。
2. 在项目视图中，找到目标项目，然后点击该项目的 <MDSvgIcon name="icon-project-settings" />。
3. 在左侧导航栏中，点击 **Project Settings** 下的 **Alert Subscription**。
4. 在 **Alert Subscription** 页面中，找到要删除的目标订阅者所在行，然后点击 **...** > **Unsubscribe**。
5. 点击 **Unsubscribe** 确认取消订阅。

</CustomContent>

<CustomContent plan="essential">

1. 在 [TiDB Cloud console](https://tidbcloud.com) 中，进入你所在组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .essential }}} 实例的名称，进入其实例概览页面。
2. 在左侧导航栏中，点击 **Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面中，找到要删除的目标订阅者所在行，然后点击 **...** > **Unsubscribe**。
4. 点击 **Unsubscribe** 确认取消订阅。

</CustomContent>

<CustomContent plan="premium">

1. 在 [TiDB Cloud console](https://tidbcloud.com) 中，进入你所在组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .premium }}} 实例的名称，进入其实例概览页面。
2. 在左侧导航栏中，点击 **Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面中，找到要删除的目标订阅者所在行，然后点击 **...** > **Unsubscribe**。
4. 点击 **Unsubscribe** 确认取消订阅。

</CustomContent>
