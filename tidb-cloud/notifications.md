---
title: TiDB Cloud 控制台中的通知
summary: 了解 TiDB Cloud 控制台中的通知，包括通知类型、用途以及如何查看通知。
---

# TiDB Cloud 控制台中的通知

[TiDB Cloud 控制台](https://tidbcloud.com/) 会向你推送通知，帮助你及时了解重要更新、系统消息、产品变更、账单提醒及其他相关信息。这些通知可以帮助你随时掌握最新动态，并在不离开控制台的情况下采取必要的操作。

## 通知类型

你可能会在 TiDB Cloud 控制台中收到不同类型的通知，例如：

- **Informational notifications**

    提供有用的更新信息，例如功能使用提示、应用变更或即将到来的事件提醒。

- **Actionable notifications**

    提示你执行特定操作，例如添加信用卡。

- **Alert notifications**

    通知你存在需要立即关注的关键问题或紧急事件，例如系统错误、安全警告或重要更新。

- **Billing notifications**

    推送与账单相关的活动更新，例如积分和折扣的变动。

- **Feedback notifications**

    邀请你对某个功能的使用体验进行反馈，例如对最近的交互进行评分或填写调查问卷。

## 通知列表

下表列出了 TiDB Cloud 中可用的通知类型，以及它们的触发事件和接收人：

| Notification | Trigger event | Notification recipient |
| --- | --- | --- |
| TiDB Cloud Starter cluster creation | 创建了一个 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 集群。 | 所有项目成员 |
| TiDB Cloud Starter cluster deletion | 删除了一个 TiDB Cloud Starter 集群。 | 所有项目成员 |
| TiDB Cloud Essential cluster creation | 创建了一个 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群。 | 所有项目成员 |
| TiDB Cloud Essential cluster deletion | 删除了一个 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群。 | 所有项目成员 |
| TiDB Cloud Dedicated cluster creation | 创建了一个 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。 | 所有项目成员 |
| TiDB Cloud Dedicated cluster deletion | 删除了一个 TiDB Cloud Dedicated 集群。 | 所有项目成员 |
| Organization Budget threshold alert | 达到组织的 [预算阈值](/tidb-cloud/tidb-cloud-budget.md)。 | `Organization Owner`、`Organization Billing Manager` 和 `Organization Billing Viewer` |
| Project Budget threshold alert | 达到项目的 [预算阈值](/tidb-cloud/tidb-cloud-budget.md)。 | `Organization Owner`、`Organization Billing Manager`、`Organization Billing Viewer` 和 `Project Owner` |
| Starter cluster spending limit threshold alert | 组织下 TiDB Cloud Starter 集群的 [消费限额阈值](/tidb-cloud/manage-serverless-spend-limit.md) 达到。 | `Organization Owner`、`Organization Billing Manager`、`Organization Billing Viewer` 和 `Project Owner` |
| Credits update | 组织的 [积分](/tidb-cloud/tidb-cloud-billing.md#credits) 被应用、全部用完、被回收或过期。 | `Organization Owner`、`Organization Billing Manager` 和 `Organization Billing Viewer` |
| Discount update | 组织的 [折扣](/tidb-cloud/tidb-cloud-billing.md#discounts) 被应用、被回收或过期。 | `Organization Owner`、`Organization Billing Manager` 和 `Organization Billing Viewer` |
| Marketplace update | 组织通过云服务商市场订阅或取消订阅。 | 所有组织成员 |
| Support plan update | 组织的支持计划订阅发生变更。 | 所有组织成员 |

## 查看通知

要查看通知，请点击 [TiDB Cloud 控制台](https://tidbcloud.com/) 左下角的 **Notification**。

当有新通知时，**Notification** 旁会显示一个数字，表示有多少条通知未读。