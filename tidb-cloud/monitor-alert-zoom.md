---
title: 通过 Zoom 订阅
summary: 了解如何通过 Zoom 获取报警通知，以便监控你的 TiDB 集群。
---

# 通过 Zoom 订阅

TiDB Cloud 为你提供了通过 Zoom、[Slack](/tidb-cloud/monitor-alert-slack.md)、[email](/tidb-cloud/monitor-alert-email.md)、[Flashduty](/tidb-cloud/monitor-alert-flashduty.md) 和 [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md) 订阅报警通知的便捷方式。本文档介绍如何通过 Zoom 订阅报警通知。

> **注意：**
>
> 目前，报警订阅仅适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

## 前提条件

- 通过 Zoom 订阅功能仅对订阅了 **Enterprise** 或 **Premium** 支持计划的组织开放。

- 要订阅 TiDB Cloud 的报警通知，你必须拥有组织的 `Organization Owner` 访问权限，或在 TiDB Cloud 中目标项目的 `Project Owner` 访问权限。

- 要在 Zoom 中添加并配置 Incoming Webhook Chatbot，你需要拥有 Zoom 账户的管理员权限。

## 订阅报警通知

### 步骤 1. 添加 Zoom Incoming Webhook 应用

1. 以账户管理员身份登录 [Zoom App Marketplace](https://marketplace.zoom.us/)。
2. 进入 Zoom App Marketplace 的 [Incoming Webhook App](https://marketplace.zoom.us/apps/eH_dLuquRd-VYcOsNGy-hQ) 页面，然后点击 **Add** 添加该应用。如果该应用未被预先批准，请联系你的 Zoom 管理员为你的账户批准该应用。更多信息请参见 [Approving apps and managing app requests](https://support.zoom.us/hc/en-us/articles/360027829671)。
3. 确认该应用所需的权限，然后点击 **Authorize** 添加 Incoming Webhook 应用。

### 步骤 2. 生成 Zoom webhook URL

1. 登录 Zoom 桌面客户端。
2. 点击 **Team Chat** 标签页。
3. 在 **Apps** 下，找到并选择 **Incoming Webhook**，或从上方选择你希望接收消息的聊天频道。
4. 输入以下命令以创建新连接。你需要将 `${connectionName}` 替换为你想要的连接名称，例如 `tidbcloud-alerts`：

    ```shell
    /inc connect ${connectionName}
    ```

5. 该命令会返回以下信息：

   - **Endpoint**。会提供一个 webhook URL，格式为：`https://integrations.zoom.us/chat/webhooks/incomingwebhook/XXXXXXXXXXXXXXXXXXXXXXXX`。
   - **Verification Token**

### 步骤 3. 从 TiDB Cloud 订阅

> **提示：**
>
> 报警订阅针对当前项目下的所有报警。如果你在该项目下有多个集群，只需订阅一次即可。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，点击右上角的 **Add Subscriber**。
4. 在 **Subscriber Type** 下拉列表中选择 **Zoom**。
5. 在 **Name** 字段输入名称，在 **URL** 字段输入你的 Zoom webhook URL，在 **Token** 字段输入 verification token。
6. 点击 **Test Connection**。

    - 如果测试成功，会显示 **Save** 按钮。
    - 如果测试失败，会显示错误信息。请根据提示排查并重试连接。

7. 点击 **Save** 完成订阅。

另外，你也可以在集群的 **Alert** 页面右上角点击 **Subscribe**，会跳转到 **Alert Subscriber** 页面。

如果报警条件持续未变，报警会每三小时发送一次通知。

## 取消订阅报警通知

如果你不再希望接收项目中集群的报警通知，请按以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Alert Subscription**。
3. 在 **Alert Subscription** 页面，找到你要删除的目标订阅者所在行，然后点击 **...** > **Unsubscribe**。
4. 点击 **Unsubscribe** 以确认取消订阅。