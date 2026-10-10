---
title: Managing Costs
summary: You can view the current month's consumption and billing history for your organization under Manage > Billing.
---

# Managing Costs

You can view the current month's consumption and billing history for your organization under **Manage** > **Billing**.

## Limiting Your Costs

For admin users, {{{ .lake }}} offers the option to set a spending limit for their organization. This allows administrators to control the maximum amount of money spent on the platform. To do this, go to the homepage and click on **Activate Spending Limit**. On the next page, you can turn on the **Enable Spending Limit** button and specify the maximum monthly spending allowed for your organization.

> **Note:**
>
> The spending limit you set will apply to each calendar month. For instance, if you set a limit on August 10th, it will be in effect for the entire month of August, from the 1st to the 31st.

When you set up a spending limit, you need to decide what action {{{ .lake }}} should take when the limit is reached. Currently, there are two options:

- **Suspend Service**: Your warehouses will not function until the current month ends or you set a higher limit.

- **Send Notifications Only**: The administrators of your organization will receive email notifications as spending limits are approached. Your warehouses can continue to function properly.

For the "Send Notifications Only" option, {{{ .lake }}} will send email notifications to administrators based on the following frequency cycle:

| Spending Range  | Notification Frequency  |
|---------------- |------------------------ |
| 80% - 90%       | Every three days        |
| 90% - 100%      | Every three days        |
| 100% or above     | Every three days        |
