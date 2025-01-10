---
title: Notifications on the TiDB Cloud console
summary: Learn about notifications on the TiDB Cloud console, including notifications types, purposes, and how to view them.
---

# Notifications on the TiDB Cloud console

The [TiDB Cloud console](https://tidbcloud.com/) provides notifications to keep you informed about important updates, system messages, product changes, billing reminders, and other relevant information. These notifications help ensure that you stay informed and can take necessary actions without leaving the console.

## Notification types

You might receive different types of notifications from the TiDB Cloud console, such as:

- Informational notifications

    These notifications provide helpful updates, such as feature usage tips, application changes, or reminders for upcoming events.

- Actionable notifications

    These notifications prompt you to perform specific actions, such as adding a credit card.

- Alert notifications

    These notifications notify you of critical issues or urgent events requiring immediate attention, such as system errors, security warnings, or important updates.

- Billing notifications

    These notifications deliver updates about billing-related activities, such as credit and discount updates.

- Feedback notifications

    These notifications request feedback on your experience with a feature, such as rating a recent interaction or completing a survey.

## Notifications list

The following table lists the notifications available in TiDB Cloud and when they are triggered:

| Notification | Description |
| --- |  --- |
| TiDB Cloud Serverless cluster creation | It is sent to all project members after a TiDB Cloud Serverless cluster is created. |
| TiDB Cloud Serverless cluster deletion | It is sent to all project members after a TiDB Cloud Serverless cluster is deleted. |
| TiDB Cloud Dedicated cluster creation | It is sent to all project members after a TiDB Cloud Dedicated cluster is created. |
| TiDB Cloud Dedicated cluster deletion | It is sent to all project members after a TiDB Cloud Dedicated cluster is deleted. |
| Organization Budget threshold alert | It is sent to organization owners, organization billing managers, and organization viewers when the organization [budget threshold](/tidb-cloud/tidb-cloud-budget.md) is reached. |
| Project Budget threshold alert | It is sent to organization owners, organization billing managers, and organization viewers when the organization project [budget threshold](/tidb-cloud/tidb-cloud-budget.md) is reached. |
| Serverless cluster spending limit threshold alert | It is sent to organization owners, organization billing managers, and organization viewers when the [spending limit threshold](/tidb-cloud/manage-serverless-spend-limit.md) of TiDB Cloud Serverless clusters in the organization is reached. |
| Credits update | It is sent to organization owners, organization billing managers, and organization viewers after [credits](/tidb-cloud/tidb-cloud-billing.md#credits) in the organization are applied, fully used, reclaimed or expired. |
| Discount update | It is sent to organization owners, organization billing managers, and organization viewers after [discounts](/tidb-cloud/tidb-cloud-billing.md#discounts) in the organization are applied, reclaimed or expired. |
| Marketplace update | It is sent to organization owners, organization billing managers, and organization viewers after subscription or unsubscription through a cloud provider marketplace. |
| Support plan update | It is sent to all organization members when the support plan subscription of the organization is changed. |

## View notifications

When a new notification is available, a red dot is displayed on the bell icon in the lower-right corner of the TiDB Cloud console. Click the bell icon to view the notification.

Alternatively, you can click <MDSvgIcon name="icon-top-account-settings" /> in the lower-left corner of the TiDB Cloud console, and then click **Notifications** to view a list of all notifications, where you can click a specific notification for more details.
