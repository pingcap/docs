---
title: 通过 Lark 创建工单并订阅工单更新
summary: 介绍关于 Lark 工单创建与更新订阅的详细信息。
---

# 通过 Lark 创建工单并订阅工单更新

对于订阅了 **Enterprise** [support plan](/tidb-cloud/connected-care-detail.md) 的客户，TiDB Cloud 在 [Lark](https://www.larksuite.com/) 中提供了一个名为 **PingCAP Support Bot** 的工单机器人。该机器人可以帮助你直接在支持工单系统中创建支持工单并接收更新。

> **注意：**
>
> Lark 的工单支持功能需按需开通。如果你有兴趣试用该功能，请联系 TiDB Cloud 支持团队：<a href="mailto:support@pingcap.com">support@pingcap.com</a>，或联系你的 Technical Account Manager (TAM)。

## 创建支持工单

1. 在 Lark 的 **PingCAP Support Group** 群组中，@提及 `@PingCAP Support Bot` 并在消息中描述你的问题。随后，机器人会发送一条仅你可见的临时卡片消息。

    ![lark-ticket-creation-1](/media/tidb-cloud/connected-lark-ticket-creation-1.png)

2. 在卡片中，在 **Reporter** 字段填写你用于 [TiDB Cloud 控制台](https://tidbcloud.com/) 的邮箱地址，按需填写其他字段，然后点击 **Submit** 创建工单。

    ![lark-ticket-creation-2](/media/tidb-cloud/connected-lark-ticket-creation-2.png)

工单创建成功后，机器人会在线程中回复工单链接。你可以点击该链接，在 [PingCAP Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals) 查看工单详情。

![lark-ticket-creation-3](/media/tidb-cloud/connected-lark-ticket-creation-3.png)

![lark-ticket-creation-4](/media/tidb-cloud/connected-lark-ticket-creation-4.png)

## 订阅工单更新

在你[创建支持工单](#创建支持工单)后，可以直接在 Lark 的 **PingCAP Support Group** 群组中接收工单更新。当支持工程师回复你的工单时，机器人会在群组中发布一条更新消息。该消息包含工单标题、工单链接以及最新评论。

![lark-ticket-creation-5](/media/tidb-cloud/connected-lark-ticket-creation-5.png)

## 常见问题

- 如何查看我的工单状态？

    使用创建工单时填写的邮箱地址登录 [PingCAP Help Center](https://tidb.support.pingcap.com/servicedesk/customer/user/requests)。你可以查看当前账户下所有历史工单及其状态。

## 联系支持

如需帮助或有任何疑问，请联系支持团队：<a href="mailto:support@pingcap.com">support@pingcap.com</a>。