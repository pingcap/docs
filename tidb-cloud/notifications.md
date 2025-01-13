---
title: Notifications on the TiDB Cloud Console
summary: Learn about notifications on the TiDB Cloud console, including notifications types, purposes, and how to view them.
---

# Notifications on the TiDB Cloud Console

The [TiDB Cloud console](https://tidbcloud.com/) provides notifications to keep you informed about important updates, system messages, product changes, billing reminders, and other relevant information. These notifications help ensure that you stay informed and can take necessary actions without leaving the console.

## Notification types

You might receive different types of notifications from the TiDB Cloud console, such as:

- **Informational notifications**

    These notifications provide helpful updates, such as feature usage tips, application changes, or reminders for upcoming events.

- **Actionable notifications**

    These notifications prompt you to perform specific actions, such as adding a credit card.

- **Alert notifications**

    These notifications notify you of critical issues or urgent events requiring immediate attention, such as system errors, security warnings, or important updates.

- **Billing notifications**

    These notifications deliver updates about billing-related activities, such as credit and discount updates.

- **Feedback notifications**

    These notifications request feedback on your experience with a feature, such as rating a recent interaction or completing a survey.

## Notifications list

The following table lists the notifications available in TiDB Cloud, their trigger events, and the recipients who receive them:

| Notification | Trigger event | Notification receiver |
| --- | --- | --- |
| TiDB Cloud Serverless cluster creation | A TiDB Cloud Serverless cluster is created. | All project members |
| TiDB Cloud Serverless cluster deletion | A TiDB Cloud Serverless cluster is deleted. | All project members |
| TiDB Cloud Dedicated cluster creation | A TiDB Cloud Dedicated cluster is created. | All project members |
| TiDB Cloud Dedicated cluster deletion | A TiDB Cloud Dedicated cluster is deleted. | All project members |
| Organization Budget threshold alert | The organization [budget threshold](/tidb-cloud/tidb-cloud-budget.md) is reached. | `Organization Owner`, `Organization Billing Manager`, and `Organization Billing Viewer` |
| Project Budget threshold alert | The project [budget threshold](/tidb-cloud/tidb-cloud-budget.md) is reached. | `Organization Owner`, `Organization Billing Manager`, `Organization Billing Viewer`, and `Project Owner` |
| Serverless cluster spending limit threshold alert | The [spending limit threshold](/tidb-cloud/manage-serverless-spend-limit.md) of TiDB Cloud Serverless clusters in the organization is reached. | `Organization Owner`, `Organization Billing Manager`, `Organization Billing Viewer`, and `Project Owner` |
| Credits update | [Credits](/tidb-cloud/tidb-cloud-billing.md#credits) of the organization are applied, fully used, reclaimed, or expired. | `Organization Owner`, `Organization Billing Manager`, and `Organization Billing Viewer` |
| Discount update | [Discounts](/tidb-cloud/tidb-cloud-billing.md#discounts) of the organization are applied, reclaimed, or expired. | `Organization Owner`, `Organization Billing Manager`, and `Organization Billing Viewer` |
| Marketplace update | The organization has a subscription or unsubscription through a cloud provider marketplace. | All organization members |
| Support plan update | The support plan subscription for the organization is changed. | All organization members |

## View notifications

When a new notification is available, a blue dot is displayed on the bell icon in the lower-right corner of the TiDB Cloud console. Click the bell icon to view the notification.

Alternatively, you can click <MDSvgIcon name="icon-top-account-settings" /> in the lower-left corner of the TiDB Cloud console, and then click **Notifications** to view a list of all notifications, where you can click a specific notification for more details.
