---
title: Manage TiDB Cloud Budgets
summary: Learn about how to use the TiDB Cloud budget feature to monitor your costs.
---

# Manage TiDB Cloud Budgets

In TiDB Cloud, you can use the billing budget feature to monitor your costs and keep your spending under control.

TiDB Cloud provides two types of budgets:

- **Serverless Spending Limit** budget: for each TiDB Serverless scalable cluster, TiDB Cloud automatically creates a **Serverless Spending Limit** budget to help you track its actual cost against the [spending limit](https://docs.pingcap.com/tidbcloud/manage-serverless-spend-limit) configured on that cluster. It includes three threshold rules: 75%, 90%, and 100% of the budget.

- **Custom** budget: you can create custom budgets to track actual costs for an entire organization or specific projects, as instructed in the subsequent sections of this document. For each budget, you can configure its scope, target spending amount, and alert thresholds. After a custom budget is created, you can compare your monthly actual costs with your planned costs to ensure that you are not over budget.

 When your monthly actual costs exceed the percentage thresholds of your budget amount or [spending limit](https://docs.pingcap.com/tidbcloud/manage-serverless-spend-limit), alert emails are sent to your organization owners and billing admins, which keep you updated on how your spending aligns with your budget.

## Prerequisites

If you are in the `Organization Owner` or `Organization Billing Admin` role of your organization, you can view, create, edit, and delete budgets of your organization. Otherwise, skip this document.

## View the budget information

To view the budget page of your organization, take the following steps:

1. In the lower-left corner of the TiDB Cloud console, click <MDSvgIcon name="icon-top-organization" />, and then click **Billing**.

    > **Note:**
    >
    > If you are in multiple organizations, switch to your target organization by clicking its name.

2. On the **Billing** page, click the **Budgets** tab.

## Create a budget

To create a budget to monitor the spending of your organization or specific projects, take the following steps:

1. In the lower-left corner of the TiDB Cloud console, click <MDSvgIcon name="icon-top-organization" />, and then click **Billing**.

    > **Note:**
    >
    > If you are in multiple organizations, switch to your target organization by clicking its name.

2. On the **Billing** page, click the **Budgets** tab.

3. On the **Budgets** page, click **Create Custom Budget**. You can create up to 5 custom budgets.

4. Provide the budget basic settings.

    - **Name**: fill in a name for the budget.
    - **Period**: select a time range for tracking costs. Currently, you can select **Monthly** as recurring calendar period, which starts on the first day of each month, and resets at the beginning of each month. TiDB Cloud tracks your actual spending during the time range against your budget amount (your planned spending).
    - **Scope**: either apply the scope to all projects (which means the entire TiDB Cloud organization) or a specific project according to your actual need.

5. Set the budget amount.

    - **Budget Amount**: set a planned spending for the period you selected.
    - **Apply credits and discounts**: choose whether to apply credits and discounts to the running total cost. Credits are used to reduce the cost of your TiDB Cloud usage, and discounts are reduction in the regular price of TiDB Cloud service. When this option is enabled, the budget tracks the running total cost minus credits and discounts.

6. Set the alert thresholds for the budget. If your actual spending exceeds specified thresholds during the the period you selected, TiDB Cloud sends a budget notification email to your `Organization Owner` and `Organization Billing Admin`.

     By default, TiDB Cloud provides three alert thresholds: 75%, 90%, and 100% of the budget amount. You can modify the percentages of budget thresholds.

    - To add a new alert threshold, click add **Add alert threshold.**
    - To remove a threshold, click the delete icon next to the threshold.

7. Click **Create**.

## Edit a budget

> **Note:**
>
> The budget in the **Serverless Spending Limit** type cannot be edited because it is automatically created by TiDB Cloud according to the [spending limit](https://docs.pingcap.com/tidbcloud/manage-serverless-spend-limit) configured for your TiDB Serverless scalable cluster.

To edit a custom budget, take the following steps:

1. In the lower-left corner of the TiDB Cloud console, click <MDSvgIcon name="icon-top-organization" />, and then click **Billing**.

    > **Note:**
    >
    > If you are in multiple organizations, switch to your target organization by clicking its name.

2. On the **Billing** page, click the **Budgets** tab.

3. On the **Budgets** page, locate the row of your budget, click **...** in that row, and then click **Edit**.

## Remove a budget

> **Note:**
>
> The budget in the **Serverless Spending Limit** type cannot be deleted because it is automatically created by TiDB Cloud according to the [spending limit](https://docs.pingcap.com/tidbcloud/manage-serverless-spend-limit) configured for your TiDB Serverless scalable cluster.

To delete a custom budget, take the following steps:

1. In the lower-left corner of the TiDB Cloud console, click <MDSvgIcon name="icon-top-organization" />, and then click **Billing**.

    > **Note:**
    >
    > If you are in multiple organizations, switch to your target organization by clicking its name.

2. On the **Billing** page, click the **Budgets** tab.

3. On the **Budgets** page, locate the row of your budget, click **...** in that row, and then click **Remove**.