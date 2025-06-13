---
title: Notifications in the TiDB Cloud Console
summary: Learn about notifications in the TiDB Cloud console, including notification types, purposes, and how to view them.
---

# Notifications in the TiDB Cloud Console

The [TiDB Cloud console](https://tidbcloud.com/) provides notifications to keep you informed about important updates, system messages, product changes, billing reminders, and other relevant information. These notifications help you stay up-to-date and take necessary actions without leaving the console.

## Notification types

You might receive different types of notifications in the TiDB Cloud console, such as:

- **Informational notifications**

    Provide helpful updates, such as feature usage tips, application changes, or reminders for upcoming events.

- **Actionable notifications**

   Prompt you to perform specific actions, such as adding a credit card.

- **Alert notifications**

    Notify you of critical issues or urgent events requiring immediate attention, such as system errors, security warnings, or important updates.

- **Billing notifications**

    Deliver updates about billing-related activities, such as credit and discount updates.

- **Feedback notifications**

    Request feedback on your experience with a feature, such as rating a recent interaction or completing a survey.

## Notifications list

The following table lists the notifications available in TiDB Cloud, along with their trigger events and recipients:

| Notification | Trigger event | Notification recipient |
| --- | --- | --- |
| TiDB Cloud Serverless cluster creation | A [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) cluster is created. | All project members |
| TiDB Cloud Serverless cluster deletion | A TiDB Cloud Serverless cluster is deleted. | All project members |
| TiDB Cloud Dedicated cluster creation | A [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster is created. | All project members |
| TiDB Cloud Dedicated cluster deletion | A TiDB Cloud Dedicated cluster is deleted. | All project members |
| Organization Budget threshold alert | The organization [budget threshold](/tidb-cloud/tidb-cloud-budget.md) is reached. | `Organization Owner`, `Organization Billing Manager`, and `Organization Billing Viewer` |
| Project Budget threshold alert | The project [budget threshold](/tidb-cloud/tidb-cloud-budget.md) is reached. | `Organization Owner`, `Organization Billing Manager`, `Organization Billing Viewer`, and `Project Owner` |
| Serverless cluster spending limit threshold alert | The [spending limit threshold](/tidb-cloud/manage-serverless-spend-limit.md) for TiDB Cloud Serverless clusters in the organization is reached. | `Organization Owner`, `Organization Billing Manager`, `Organization Billing Viewer`, and `Project Owner` |
| Credits update | [Credits](/tidb-cloud/tidb-cloud-billing.md#credits) for the organization are applied, fully used, reclaimed, or expired. | `Organization Owner`, `Organization Billing Manager`, and `Organization Billing Viewer` |
| Discount update | [Discounts](/tidb-cloud/tidb-cloud-billing.md#discounts) for the organization are applied, reclaimed, or expired. | `Organization Owner`, `Organization Billing Manager`, and `Organization Billing Viewer` |
| Marketplace update | The organization has a subscription or unsubscription through a cloud provider marketplace. | All organization members |
| Support plan update | The support plan subscription for the organization is changed. | All organization members |

## View notifications

To view notifications, click **Notification** in the lower-left corner of the [TiDB Cloud console](https://tidbcloud.com/).

When new notifications are available, a number is displayed next to **Notification** indicating how many notifications are unread.