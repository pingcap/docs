---
title: 管理 TiDB Cloud 预算
summary: 了解如何使用 TiDB Cloud 的预算功能来监控你的成本。
---

# 管理 TiDB Cloud 预算

在 TiDB Cloud 中，你可以使用预算功能来监控你的成本，并控制你的支出。

当你的月度实际成本超过你指定预算的百分比阈值时，系统会向你的组织所有者和账单管理员发送告警邮件。这些通知可以帮助你及时了解支出情况，并采取主动措施管理你的支出，使你的费用与预算保持一致。

TiDB Cloud 提供两种类型的预算，帮助你跟踪支出：

- **Serverless Spending Limit** 预算：对于每个 TiDB Cloud Serverless 可扩展集群，TiDB Cloud 会自动创建一个 **Serverless Spending Limit** 预算。该预算帮助你根据该集群上配置的 [spending limit](/tidb-cloud/manage-serverless-spend-limit.md) 跟踪实际成本。它包含三个阈值规则：预算的 75%、90% 和 100%，这些阈值不可编辑。

- **Custom** 预算：你可以创建自定义预算，用于跟踪整个组织或特定项目的实际成本。对于每个预算，你可以指定预算范围、设置目标支出金额，并配置告警阈值。创建自定义预算后，你可以将每月实际成本与计划成本进行对比，确保支出不超出预算。

## 前提条件

要查看、创建、编辑或删除你组织或项目的预算，你必须拥有组织的 `Organization Owner` 或 `Organization Billing Manager` 角色。

## 查看预算信息

要查看你组织的预算页面，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航栏中，点击 **Billing**。
3. 在 **Billing** 页面，点击 **Budgets** 标签页。

对于每个预算，你可以查看其名称、类型、状态、已用金额、预算金额、周期和范围。

## 创建自定义预算

要创建自定义预算以监控你组织或特定项目的支出，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航栏中，点击 **Billing**。
3. 在 **Billing** 页面，点击 **Budgets** 标签页，然后点击 **Create Custom Budget**。你最多可以创建 5 个自定义预算。
4. 填写预算的基本设置。

    - **Name**：输入预算名称。
    - **Period**：选择用于跟踪成本的时间范围。目前只能选择 **Monthly**，即每月的第一天开始，并在每月初重置。TiDB Cloud 会在该时间范围内根据你的预算金额（计划支出）跟踪你的实际支出。
    - **Budget scope**：根据需要，将范围应用于所有项目（即整个 TiDB Cloud 组织）或某个特定项目。

5. 设置预算金额。

    - **Budget Amount**：为所选周期输入计划支出金额。
    - **Apply credits**：选择是否将代金券应用于累计总成本。代金券用于抵扣你在 TiDB Cloud 上的使用成本。启用该选项后，预算会跟踪累计总成本减去代金券后的金额。
    - **Apply discounts**：选择是否将折扣应用于累计总成本。折扣是 TiDB Cloud 服务常规价格的减免。启用该选项后，预算会跟踪累计总成本减去折扣后的金额。

6. 配置预算的告警阈值。如果你的实际支出在所选周期内超过指定阈值，TiDB Cloud 会向你的组织所有者和账单管理员发送预算通知邮件。

    - 默认情况下，TiDB Cloud 提供三个告警阈值：预算金额的 75%、90% 和 100%。你可以根据需要修改这些百分比。
    - 若要添加新的告警阈值，点击 **Add alert threshold.**
    - 若要移除某个阈值，点击该阈值旁边的删除图标。

7. 点击 **Create**。

## 编辑自定义预算

> **注意：**
>
> **Serverless Spending Limit** 预算无法编辑，因为它是由 TiDB Cloud 自动创建，用于帮助你根据 [spending limit](/tidb-cloud/manage-serverless-spend-limit.md) 跟踪 TiDB Cloud Serverless 可扩展集群的成本。

要编辑自定义预算，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航栏中，点击 **Billing**。
3. 在 **Billing** 页面，点击 **Budgets** 标签页。
4. 找到目标预算所在行，点击该行的 **...**，然后点击 **Edit**。
5. 根据需要编辑预算名称、预算范围、预算金额和告警阈值。

    > **注意：**
    >
    > 不支持编辑预算周期以及是否应用代金券和折扣。

6. 点击 **Update**。

## 删除自定义预算

> **注意：**
>
> - 一旦自定义预算被删除，你将不再收到与其相关的任何告警邮件。
> - **Serverless Spending Limit** 预算无法删除，因为它是由 TiDB Cloud 自动创建，用于帮助你根据 [spending limit](/tidb-cloud/manage-serverless-spend-limit.md) 跟踪 TiDB Cloud Serverless 可扩展集群的成本。

要删除自定义预算，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航栏中，点击 **Billing**。
3. 在 **Billing** 页面，点击 **Budgets** 标签页。
4. 找到目标预算所在行，点击该行的 **...**，然后点击 **Delete**。
5. 确认删除操作。