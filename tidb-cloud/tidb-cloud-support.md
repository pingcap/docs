---
title: TiDB Cloud 支持
summary: 了解如何联系 TiDB Cloud 支持团队。
---

# TiDB Cloud 支持

TiDB Cloud 提供分层支持计划，满足客户的不同需求。关于我们的支持服务详情，请参见 [Connected Care 详情](/tidb-cloud/connected-care-detail.md)。

## 支持渠道

TiDB Cloud 提供多种支持渠道。可用选项取决于问题的类型以及你的 [支持计划](/tidb-cloud/connected-care-detail.md)。

- 支持工单（[帮助中心](#访问-pingcap-帮助中心)）

    对于需要 TiDB Cloud 支持团队直接协助的问题，请使用基于工单的渠道。

    - [账单和账户工单](/tidb-cloud/tidb-cloud-support.md#create-an-account-or-billing-support-ticket) 对所有 TiDB Cloud 用户开放。
    - [技术支持工单](/tidb-cloud/tidb-cloud-support.md#create-a-technical-support-ticket)（有保障的响应时间）仅对付费支持计划开放。如果你没有付费支持计划，请通过社区渠道咨询技术问题。

    **Enterprise** 和 **Premium** 支持计划包含以下增强能力。详情请参见 [Connected Care 详情](/tidb-cloud/connected-care-detail.md)。
 
    - 明确 SLA 的更快响应时间
    - 通过 IM 支持实现实时沟通
    - 主动支持项目，例如 [Clinic](/tidb-cloud/tidb-cloud-clinic.md)
    - 专属或指定支持角色，如技术客户经理（TAM）

- 社区（[Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap) 和 [Discord](https://discord.com/invite/KVRZBR2DrG)）

    通过这些开放讨论渠道，你可以提问、分享经验，并获得其他用户和 PingCAP 工程师的指导。适用于一般性问题、使用讨论和非紧急技术问题。

- [TiDB.AI](https://tidb.ai/)

    TiDB.AI 是一个 AI 驱动的助手，可解答常见技术和文档相关问题，适合快速自助获取帮助。

## 访问 PingCAP 帮助中心

[PingCAP 帮助中心](https://tidb.support.pingcap.com/servicedesk/customer/portals) 是 TiDB Cloud 用户获取支持服务和管理支持工单的中心平台。

你可以直接通过 <https://tidb.support.pingcap.com/servicedesk/customer/portals> 访问 PingCAP 帮助中心，或通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 以以下方式访问：

- 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 右下角点击 **?**，然后点击 **Request Support**。
- 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 左下角点击 **Support**，然后点击 **Create Ticket**。
- 在你的项目 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击集群所在行的 **...**，然后选择 **Get Support**。
- 在集群概览页面右上角点击 **...**，然后选择 **Get Support**。

## 创建账户或账单支持工单

所有 TiDB Cloud 用户都可以创建账单和账户相关的工单。要创建关于账户或账单问题的支持工单，请按以下步骤操作：

1. 登录 [PingCAP 帮助中心](https://tidb.support.pingcap.com/servicedesk/customer/portals)，然后点击 [TiDB Cloud Account/Billing Support](https://tidb.support.pingcap.com/servicedesk/customer/portal/16)。
2. 点击 **Submit a request**。
3. 填写以下字段：

    - **Summary**：简要描述你的问题。
    - **TiDB Cloud Org**：选择相关的 TiDB Cloud 组织（如适用）。
    - **TiDB Cloud Cluster**：选择相关的 TiDB Cloud 集群（如适用）。
    - **Description**：详细描述问题。
    - **Severity**：评估该问题对业务的影响，并选择合适的严重级别。（S1 不适用于账单或账户问题。）

4. 点击 **Submit**。

## 创建技术支持工单

要创建关于技术问题的支持工单，请按以下步骤操作：

1. 登录 [PingCAP 帮助中心](https://tidb.support.pingcap.com/servicedesk/customer/portals)，然后点击 [TiDB Cloud Technical Support](https://tidb.support.pingcap.com/servicedesk/customer/portal/6)。

    > **注意：**
    >
    > [TiDB Cloud Technical Support](https://tidb.support.pingcap.com/servicedesk/customer/portal/6) 入口仅对 **Developer**、**Enterprise** 或 **Premium** [支持计划](/tidb-cloud/connected-care-detail.md)开放。如果你处于 **Basic** 计划，可以通过 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap) 或 [Discord](https://discord.com/invite/KVRZBR2DrG) 的社区渠道咨询技术问题，PingCAP 工程师和社区成员会提供指导。

2. 点击 **Submit a request**。

3. 填写以下字段：

    - **Summary**：简要描述你的问题。
    - **TiDB Cloud Org**：选择该问题相关的 TiDB Cloud 组织。
    - **TiDB Cloud Cluster**：选择相关的 TiDB Cloud 集群（如适用）。
    - **Environment**：选择你使用 TiDB Cloud 集群的对应环境。
    - **Description**：尽可能详细地描述你遇到的问题。例如，提供遇到问题的精确时间戳，附上详细的错误信息和问题的调用堆栈，并补充你的排查或分析过程。
    - **Severity**：评估该问题对业务的影响，并选择合适的严重级别。

        | Severity | 描述 |
        | --- | --- |
        | S1 | 生产环境功能完全丧失 |
        | S2 | 对生产环境运维有较大影响 |
        | S3 | 生产或非生产环境下的非关键数据库使用问题 |
        | S4 | 关于某个特性或功能如何实现或应如何配置的一般性问题。对业务影响极小，可在合理时间内容忍的问题。 |

    - **Components**：选择要报告问题的相关 TiDB Cloud 组件，如 TiDB、TiKV、PD 或 TiFlash。
    - **Affects versions**：指定与该问题相关的 TiDB Cloud 集群版本。

4. 点击 **Submit**。

## 查看支持工单

要查看所有历史支持工单，请登录 [PingCAP 帮助中心](https://tidb.support.pingcap.com/servicedesk/customer/portals)，点击右上角头像，然后点击 **Requests**。

## 查看或升级你的支持计划

TiDB Cloud 默认提供免费基础支持计划。如需扩展服务，你可以升级到付费计划。

要查看或升级你的支持计划，请按以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 左下角点击 **Support**。

    在该页面，你可以查看当前的支持计划。默认选择 **Basic** 免费计划。

2. 选择你想要的支持计划。

    <SimpleTab>
    <div label="升级到 Developer 或 Enterprise">

    若要升级到 **Developer** 或 **Enterprise**：

    1. 在 **Developer** 或 **Enterprise** 面板点击 **Upgrade**。会显示 **Upgrade to Developer Plan** 或 **Upgrade to Enterprise Plan** 页面。
    2. 查看页面上的支持服务信息。各支持计划的完整版本请参见 [Connected Care 详情](/tidb-cloud/connected-care-detail.md)。
    3. 点击 **Add Credit Card and Upgrade**，并填写 **Credit Card** 信息。

        有关账单的更多信息，请参见 [TiDB Cloud 支付方式](/tidb-cloud/tidb-cloud-billing.md#payment-method)。

    4. 在页面右下角点击 **Save Card**。

    支付完成后，你的计划将升级为 **Standard** 或 **Enterprise**。

    </div>
    <div label="升级到 Premium">

    若要将计划升级为 **Premium**：

    1. 在 **Premium** 面板点击 **Contact Sales**。会显示 **Contact Us** 页面。
    2. 在页面填写并提交你的联系信息，支持团队会与你联系并协助订阅。

    </div>
    </SimpleTab>

## 降级你的支持计划

要降级你的支持计划，请按以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 左下角点击 **Support**。
2. 选择你要切换到的支持计划，然后点击 **Downgrade**。