---
title: Connected Care 概览
summary: 介绍新一代 TiDB Cloud 支持服务 —— Connected Care。
aliases: ['/tidbcloud/connected-care-announcement']
---

# Connected Care 概览

随着各类客户在 TiDB Cloud 上不断扩展 use case 和运营规模，TiDB Cloud 致力于重新构想其支持服务，以满足客户不断变化的需求。为了带来更高价值和无缝体验，TiDB Cloud 很高兴地宣布将于 **2025 年 2 月 17 日** 正式推出全新支持服务 —— **Connected Care**。

作为此次变更的一部分，现有的支持计划自 **2025 年 2 月 17 日** 起将不再对外销售，并被归类为历史支持计划（legacy support plans）。不过，TiDB Cloud 仍会为订阅历史计划的客户持续提供完整支持，直至各自的[退役日期](#transition-to-connected-care)。

为确保平滑过渡并获得最新功能，TiDB Cloud 鼓励客户尽快迁移并采用 Connected Care 服务。

## Connected Care

Connected Care 服务旨在通过现代 communication 工具、主动支持和先进的 AI 能力，增强你与 TiDB Cloud 的连接，带来无缝且以客户为中心的体验。

在 Connected Care 服务中，包含四种支持计划：**Basic**、**Developer**（对应历史 **Standard** 计划）、**Enterprise** 和 **Premium**。

> **注意**
>
> 虽然 **Basic**、**Enterprise** 和 **Premium** 支持计划与历史计划使用了相同的名称，但它们指代的是不同的计划，服务承诺也不同。

下表概述了 Connected Care 服务中各支持计划的内容。更多信息，参见 [Connected Care 详情](/tidb-cloud/connected-care-detail.md)。

| 支持计划                                                                                                                                                                                                                       | Basic                        | Developer                                    | Enterprise                                     | Premium                                   |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------|:---------------------------------------------|:-----------------------------------------------|:------------------------------------------|
| 推荐 workload                                                                                                                                                                                                              | 个人或入门项目               | 开发中的 workload                            | 生产环境下的 workload                          | 生产环境下关键业务 workload               |
| 计费与账户支持                                                                                                                                                                                                        | ✔                            | ✔                                            | ✔                                              | ✔                                         |
| 技术支持                                                                                                                                                                                                                  | -                            | ✔                                            | ✔                                              | ✔                                         |
| 首次响应时间                                                                                                                                                                                                              | -                            | 工作时间                                     | 7x24                                           | 7x24                                      |
| [Connected: Clinic service](/tidb-cloud/tidb-cloud-clinic.md)                                                                                                                                                                      | -                            | -                                            | ✔                                              | ✔                                         |
| [Connected: AI chat in IM](/tidb-cloud/connected-ai-chat-in-im.md)                                                                                                                                                                 | -                            | -                                            | ✔                                              | ✔                                         |
| Connected: IM 订阅 TiDB Cloud 报警/告警 ([Slack](/tidb-cloud/monitor-alert-slack.md), [Zoom](/tidb-cloud/monitor-alert-zoom.md))                                                                                          | -                            | -                                            | ✔                                              | ✔                                         |
| Connected: IM 工单创建与 update 订阅 ([Slack](/tidb-cloud/connected-slack-ticket-creation.md), [Lark](/tidb-cloud/connected-lark-ticket-creation.md)) | -                            | -                                            | ✔                                              | ✔                                         |
| Connected: IM 工单交互 ([Slack](/tidb-cloud/connected-slack-ticket-interaction.md), [Lark](/tidb-cloud/connected-lark-ticket-interaction.md))   | -                            | -                                            | -                                              | ✔                                         |
| 技术 Account Manager                                                                                                                                                                                                          | -                            | -                                            | -                                              | ✔                                         |

> **注意**
>
> 所有四种支持计划的客户均可通过 [PingCAP support portal](https://tidb.support.pingcap.com/) 提交服务请求。

## 历史支持服务与 Connected Care 支持服务的区别

Connected Care 服务中的支持计划引入了全新的一系列功能，包括：

- Connected: Clinic service

    该功能提供了高级监控与诊断服务 Clinic，帮助你快速定位性能问题、优化数据库，并通过详细分析和可执行建议提升整体性能。详情参见 [Connected: Clinic Service](/tidb-cloud/tidb-cloud-clinic.md)。

- Connected: AI chat in IM

    该功能允许你通过即时消息（IM）工具与 AI 助手对话，实时获取问题解答。详情参见 [Connected: AI chat in IM](/tidb-cloud/connected-ai-chat-in-im.md)。

- Connected: IM 订阅 TiDB Cloud 报警/告警

    该功能让你可以通过 IM 工具便捷订阅报警/告警通知，及时获知关键更新。详情参见 [通过 Slack 订阅](/tidb-cloud/monitor-alert-slack.md) 和 [通过 Zoom 订阅](/tidb-cloud/monitor-alert-zoom.md)。

- Connected: IM 工单创建与 update 订阅

    该功能允许你通过 IM 工具创建支持工单，并订阅工单 update。详情参见 [通过 Slack 创建工单及订阅工单 update](/tidb-cloud/connected-slack-ticket-creation.md) 和 [通过 Lark 创建工单及订阅工单 update](/tidb-cloud/connected-lark-ticket-creation.md)。

- Connected: IM 工单交互

    该功能让你可以通过 IM 工具快速创建并与支持工单交互，实现高效 communication。详情参见 [通过 Slack 交互工单](/tidb-cloud/connected-slack-ticket-interaction.md) 和 [通过 Lark 交互工单](/tidb-cloud/connected-lark-ticket-interaction.md)。

借助这些新功能，Connected Care 服务为你带来更好的连接性、更个性化的支持，以及面向不同客户需求的高性价比解决方案。

- 新的 **Enterprise** 和 **Premium** 计划：通过 Clinic 高级监控服务、IM 订阅 TiDB Cloud 报警/告警、IM 工单 update 订阅、AI chat in IM 以及 IM 工单交互，提供现代 communication 工具和先进 AI 能力。

- 新的 **Developer** 计划：可访问与 **Basic** 计划相同的社区 channel（[Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap) 和 [Discord](https://discord.com/invite/KVRZBR2DrG)）及 [TiDB.AI](https://tidb.ai/) 协助，并可直接连接和无限制访问技术支持。

- 新的 **Basic** 计划：你可以加入社区 channel（[Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap) 和 [Discord](https://discord.com/invite/KVRZBR2DrG)）与其他社区成员交流，并使用 [TiDB.AI](https://tidb.ai/) 获取技术协助。

## 迁移到 Connected Care

下表列出了历史支持计划的下线时间表：

| 支持计划                        | 下线日期      |
|:----------------------------------------|:--------------|
| 历史 **Basic** 计划                     | 2025 年 2 月 17 日  |
| 历史 **Standard** 计划                           | 2025 年 2 月 17 日  |
| 历史 **Enterprise** 和 **Premium** 计划 | 2026 年 1 月 15 日  |

一旦历史支持计划下线，TiDB Cloud 将不再为其提供支持。如果你未在相关下线日期前迁移到 Connected Care 的任一支持计划，将会被自动迁移至 Connected Care 的 **Basic** 支持计划。

## 常见问题

### 如何查看或更改当前的支持计划？

在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，点击左下角的 **Support**。此时会显示 **Support** 页面，你当前的支持计划会以 **CURRENT** 标签高亮显示。

你可以在 **Support** 页面切换到新的支持计划（**Premium** 支持计划除外）。如需升级到 **Premium** 计划，请[联系销售](https://www.pingcap.com/contact-us)。

### 获得类似服务是否需要支付更多费用？

虽然新的 Connected Care 服务提供了更全面、功能更丰富的支持体验，但定价与之前的方案基本保持一致。TiDB Cloud 始终致力于为你的成长之路带来更多价值。

### 历史 **Basic** 计划下线后，如何获得技术支持？

你仍可获得[计费与账户支持](/tidb-cloud/tidb-cloud-support.md#create-an-account-or-billing-support-ticket)。如需技术支持，建议购买 Connected Care 服务中的支持计划。推荐从 **Developer** 计划开始，该计划包含一个月的免费试用。