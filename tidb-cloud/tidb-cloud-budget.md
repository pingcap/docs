---
title: Manage Budgets for TiDB Cloud
summary: Learn about how to use the budget feature of TiDB Cloud to monitor your costs.
---

# Manage Budgets for TiDB Cloud

In TiDB Cloud, you can use the budget feature to monitor your costs and keep your spending under control.

When your monthly actual costs exceed the percentage thresholds of your specified budget, alert emails are sent to your organization owners and billing administrators. These notifications help you stay informed and take proactive measures to manage your spending, aligning your expenses with your budget.

TiDB Cloud provides two types of budgets to help you track your spending:

- **Serverless Spending Limit** budget: for each TiDB Cloud Serverless scalable cluster, TiDB Cloud automatically creates a **Serverless Spending Limit** budget. This budget helps you track the actual cost against the [spending limit](/tidb-cloud/manage-serverless-spend-limit.md) configured on that cluster. It includes three threshold rules: 75%, 90%, and 100% of the budget, which are not editable.

- **Custom** budget: you can create custom budgets to track actual costs for an entire organization or specific projects. For each budget, you can specify a budget scope, set a target spending amount, and configure alert thresholds. After creating a custom budget, you can compare your monthly actual costs with your planned costs to ensure you stay within budget.

## Prerequisites

To view, create, edit, or delete budgets of your organization or projects, you must be in the `Organization Owner` or `Organization Billing Manager` role of your organization.

## View the budget information

To view the budget page of your organization, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.
2. In the left navigation pane, click **Billing**.
3. On the **Billing** page, click the **Budgets** tab.

For each budget, you can view its name, type, status, amount used, budget amount, period, and scope.

## Create a custom budget

To create a custom budget to monitor the spending of your organization or specific projects, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.
2. In the left navigation pane, click **Billing**.
3. On the **Billing** page, click the **Budgets** tab, and then click **Create Custom Budget**. You can create up to five custom budgets.
4. Provide the budget basic settings.

    - **Name**: enter a name for the budget.
    - **Period**: select a time range for tracking costs. Currently, you can only select **Monthly**, which starts on the first day of each month and resets at the beginning of each month. TiDB Cloud tracks your actual spending during the time range against your budget amount (your planned spending).
    - **Budget scope**: apply the scope to all projects (which means the entire TiDB Cloud organization) or a specific project as needed.

5. Set the budget amount.

    - **Budget Amount**: enter a planned spending amount for the selected period.
    - **Apply credits**: choose whether to apply credits to the running total cost. Credits are used to reduce the cost of your TiDB Cloud usage. When this option is enabled, the budget tracks the running total cost minus credits.
    - **Apply discounts**: choose whether to apply discounts to the running total cost. Discounts are reductions in the regular price of TiDB Cloud service. When this option is enabled, the budget tracks the running total cost minus discounts.

6. Configure alert thresholds for the budget. If your actual spending exceeds specified thresholds during the selected period, TiDB Cloud sends a budget notification email to your organization owners and billing administrators.

    - By default, TiDB Cloud provides three alert thresholds: 75%, 90%, and 100% of the budget amount. You can modify these percentages as needed.
    - To add a new alert threshold, click **Add alert threshold.**
    - To remove a threshold, click the delete icon next to the threshold.

7. Click **Create**.

## Edit a custom budget

> **Note:**
>
> The **Serverless Spending Limit** budget cannot be edited because it is automatically created by TiDB Cloud to help you track the cost of a TiDB Cloud Serverless scalable cluster against its [spending limit](/tidb-cloud/manage-serverless-spend-limit.md).

To edit a custom budget, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.
2. In the left navigation pane, click **Billing**.
3. On the **Billing** page, click the **Budgets** tab.
4. Locate the row of your target budget, click **...** in that row, and then click **Edit**.
5. Edit the budget name, budget scope, budget amount, and alert thresholds as needed.

    > **Note:**
    >
    > Editing the budget period and whether to apply credits and discounts is not supported.

6. Click **Update**.

## Delete a custom budget

> **Note:**
>
> - Once a custom budget is deleted, you will no longer receive any alert emails related to it.
> - The **Serverless Spending Limit** budget cannot be deleted because it is automatically created by TiDB Cloud to help you track the cost of a TiDB Cloud Serverless scalable cluster against its [spending limit](/tidb-cloud/manage-serverless-spend-limit.md).

To delete a custom budget, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.
2. In the left navigation pane, click **Billing**.
3. On the **Billing** page, click the **Budgets** tab.
4. Locate the row of your target budget, click **...** in that row, and then click **Delete**.
5. Confirm the deletion.